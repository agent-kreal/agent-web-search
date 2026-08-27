"""Parallel — own web index, anonymous MCP access, generous hobby limits.
web_search + web_fetch (up to 20 URLs per call)."""

from __future__ import annotations

import json
from typing import List, Optional

from .. import config
from ..mcpclient import McpClient, McpError
from .base import FetchResult, Provider, ProviderError, QuotaSpec, SearchResult

MCP_URL = "https://search.parallel.ai/mcp"


class ParallelProvider(Provider):
    # one class, two chain slots: keyed (spends balance, higher limits) and
    # anonymous (free bottom). ParallelProvider(keyed=False) = anon slot.
    name = "parallel"
    quota = QuotaSpec(limit=None, period="none", label="keyed: spends balance")
    can_fetch = True

    def __init__(self, keyed: bool = True):
        self._keyed = keyed
        self._client: Optional[McpClient] = None
        self.api_key = config.get("PARALLEL_API_KEY") if keyed else None
        if not keyed:
            self.name = "parallel-anon"
            self.quota = QuotaSpec(limit=None, period="none", label="anonymous MCP")

    def _mcp(self) -> McpClient:
        if self._client is None:
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else None
            self._client = McpClient(MCP_URL, headers=headers, timeout=60)
        return self._client

    def search(self, query: str, *, n: int = 8, freshness: Optional[str] = None) -> List[SearchResult]:
        args = {
            "objective": query,
            "search_queries": [query],
        }
        try:
            result = self._mcp().call_tool("web_search", args)
        except McpError as e:
            raise ProviderError(f"parallel: {e}",
                                quota_exhausted=("429" in str(e) or "limit" in str(e).lower()),
                                retryable=e.status >= 500 or e.status == 0) from None
        text = next((c.get("text", "") for c in result.get("content", [])
                     if c.get("type") == "text"), "")
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            raise ProviderError("parallel: non-JSON tool response", retryable=True) from None
        out = []
        for r in data.get("results", [])[:n]:
            excerpts = r.get("excerpts") or []
            snippet = (excerpts[0] if isinstance(excerpts, list) and excerpts else "")[:500]
            out.append(SearchResult(
                url=r.get("url", ""), title=r.get("title", ""),
                snippet=snippet, date=r.get("publish_date"), provider=self.name,
            ))
        if not out:
            raise ProviderError("parallel returned no results", retryable=False)
        return out

    def fetch(self, url: str, *, max_chars: int = 6000) -> FetchResult:
        try:
            result = self._mcp().call_tool(
                "web_fetch", {"urls": [url], "objective": "full page content"})
        except McpError as e:
            raise ProviderError(f"parallel fetch: {e}") from None
        text = next((c.get("text", "") for c in result.get("content", [])
                     if c.get("type") == "text"), "")
        try:
            data = json.loads(text)
            r = (data.get("results") or [{}])[0]
            content = r.get("full_content") or (r.get("excerpts") or [""])[0]
            title = r.get("title", "")
        except (json.JSONDecodeError, IndexError):
            content, title = text, ""
        return FetchResult(url=url, title=title, content=content[:max_chars], provider=self.name)
