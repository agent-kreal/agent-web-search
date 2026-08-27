"""Z.ai web_search_prime — the GLM Coding Plan search quota (1000/mo),
called directly over MCP HTTP instead of a Claude Code MCP entry.
Quality leader of the chain; quota resets monthly."""

from __future__ import annotations

import json
import re
from typing import List, Optional

from .. import config, quotas
from ..mcpclient import McpClient, McpError
from .base import Provider, ProviderError, QuotaSpec, SearchResult

MCP_URL = "https://api.z.ai/api/mcp/web_search_prime/mcp"

# "Your limit will reset at 2026-09-18 16:28:19" — no timezone, assume UTC
_RESET_RE = re.compile(r"reset at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})")


class ZaiProvider(Provider):
    name = "zai"
    quota = QuotaSpec(limit=1000, period="month", label="GLM Coding Plan 1000/mo")

    def __init__(self):
        self.auth = config.zai_auth_header()
        if not self.auth:
            self.available_reason = "no Z.ai token found"

    def search(self, query: str, *, n: int = 8, freshness: Optional[str] = None) -> List[SearchResult]:
        client = McpClient(MCP_URL, headers={"Authorization": self.auth}, timeout=45)
        args = {"search_query": query, "content_size": "medium"}
        if freshness == "day":
            args["search_recency_filter"] = "oneDay"
        elif freshness == "week":
            args["search_recency_filter"] = "oneWeek"
        try:
            result = client.call_tool("web_search_prime", args)
        except McpError as e:
            msg = str(e)
            if e.status == 429 or "Limit Exhausted" in msg or "1310" in msg:
                m = _RESET_RE.search(msg)
                until = m.group(1).replace(" ", "T") + "+00:00" if m else None
                quotas.mark_exhausted(self.name, until, "month")
                raise ProviderError(f"zai quota exhausted until {until}", quota_exhausted=True) from None
            raise ProviderError(f"zai: {msg}", retryable=e.status >= 500 or e.status == 0) from None
        text = next((c.get("text", "") for c in result.get("content", [])
                     if c.get("type") == "text"), "")
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            raise ProviderError("zai: non-JSON response", retryable=True) from None
        items = data.get("web_search", data) if isinstance(data, dict) else data
        if isinstance(items, dict):
            items = items.get("results", [])
        out = []
        for r in items or []:
            if not isinstance(r, dict):
                continue
            out.append(SearchResult(
                url=r.get("url", ""), title=r.get("title", ""),
                snippet=r.get("snippet", r.get("page_content", ""))[:500],
                date=r.get("publish_date"), provider=self.name,
            ))
        if not out:
            raise ProviderError("zai returned no results", retryable=False)
        quotas.spend(self.name, 1, "month")
        return out[:n]
