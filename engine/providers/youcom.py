"""You.com — free MCP profile (no credentials), 100 queries/day, you-search."""

from __future__ import annotations

import json
from typing import List, Optional

from .. import config, quotas
from ..mcpclient import McpClient, McpError
from .base import Provider, ProviderError, QuotaSpec, SearchResult

MCP_URL = "https://api.you.com/mcp?profile=free"


class YoucomProvider(Provider):
    name = "youcom"
    quota = QuotaSpec(limit=100, period="day", label="free profile 100/day")

    def __init__(self):
        self._client: Optional[McpClient] = None
        self.api_key = config.get("YOUCOM_API_KEY")
        if self.api_key:
            # keyed: higher limits, but every call spends the $100 account credit
            self.quota = QuotaSpec(limit=None, period="none",
                                   label="keyed: spends $100 account credit")

    def _mcp(self) -> McpClient:
        if self._client is None:
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else None
            self._client = McpClient(MCP_URL, headers=headers, timeout=40)
        return self._client

    def search(self, query: str, *, n: int = 8, freshness: Optional[str] = None) -> List[SearchResult]:
        args = {"query": query}
        if freshness in ("day", "week"):
            args["created"] = "lastWeek" if freshness == "week" else "lastDay"
        try:
            result = self._mcp().call_tool("you-search", args)
        except McpError as e:
            msg = str(e)
            if e.status == 429 or "rate" in msg.lower() or "limit" in msg.lower():
                quotas.mark_exhausted(self.name, None, "day")
                raise ProviderError("youcom daily limit hit", quota_exhausted=True) from None
            raise ProviderError(f"youcom: {msg}", retryable=e.status >= 500 or e.status == 0) from None
        text = next((c.get("text", "") for c in result.get("content", [])
                     if c.get("type") == "text"), "")
        try:
            data = json.loads(text)
            web = (data.get("results") or {}).get("web", [])
        except (json.JSONDecodeError, AttributeError):
            raise ProviderError("youcom: unparseable response", retryable=True) from None
        out = []
        for r in web[:n]:
            snippets = r.get("snippets") or [""]
            out.append(SearchResult(
                url=r.get("url", ""), title=r.get("title", ""),
                snippet=snippets[0][:500], provider=self.name,
            ))
        if not out:
            raise ProviderError("youcom returned no results", retryable=False)
        quotas.spend(self.name, 1, "day")
        return out
