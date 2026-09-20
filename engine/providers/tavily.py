"""Tavily — keyless REST (X-Tavily-Access-Mode: keyless) with seamless
upgrade to a keyed account when TAVILY_API_KEY appears in .env."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import List, Optional

from .. import config, quotas
from .base import FetchResult, Provider, ProviderError, QuotaSpec, SearchResult

API = "https://api.tavily.com/search"


class TavilyProvider(Provider):
    name = "tavily"
    quota = QuotaSpec(limit=None, period="none", label="keyless rate-limited")
    can_fetch = True
    KEYED_LIMIT = 1000  # credits/mo, basic search = 1 credit

    def __init__(self):
        self.api_key = config.get("TAVILY_API_KEY")
        if self.api_key:
            self.quota = QuotaSpec(limit=self.KEYED_LIMIT, period="month",
                                   unit="credits",
                                   label="keyed 1000 credits/mo -> keyless after")

    def _keyed_active(self) -> bool:
        """Keyed while the monthly credit lasts; silently drop to keyless
        once the local counter (or a real 429) says it's spent."""
        if not self.api_key:
            return False
        if quotas.is_exhausted(self.name):
            return False
        if (quotas.remaining(self.name, self.KEYED_LIMIT, "month") or 0) <= 0:
            return False
        return True

    def _headers(self) -> dict:
        if self._keyed_active():
            return {"Authorization": f"Bearer {self.api_key}"}
        return {"X-Tavily-Access-Mode": "keyless"}

    def search(self, query: str, *, n: int = 8, freshness: Optional[str] = None) -> List[SearchResult]:
        body = {"query": query, "max_results": n}
        if freshness == "day":
            body["topic"] = "news"
        req = urllib.request.Request(API, data=json.dumps(body).encode(), method="POST")
        req.add_header("Content-Type", "application/json")
        for k, v in self._headers().items():
            req.add_header(k, v)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:300]
            if e.code in (429, 402) and self._keyed_active():
                # key quota hit mid-flight: mark spent, retry once keyless
                quotas.mark_exhausted(self.name, None, "month")
                return self.search(query, n=n, freshness=freshness)
            if e.code in (429, 402):
                raise ProviderError(f"tavily {e.code}: {detail}", quota_exhausted=True) from None
            raise ProviderError(f"tavily {e.code}: {detail}", retryable=(e.code >= 500)) from None
        except urllib.error.URLError as e:
            raise ProviderError(f"tavily network: {e.reason}") from None
        out = []
        for r in data.get("results", []):
            out.append(SearchResult(
                url=r.get("url", ""), title=r.get("title", ""),
                snippet=r.get("content", "")[:500],
                provider=self.name,
            ))
        if not out:
            raise ProviderError("tavily returned no results", retryable=False)
        if self._keyed_active():
            # credits: basic/fast (default depth) = 1; if a `depth: advanced`
            # ever lands in the body above, this must become spend(..., 2)
            quotas.spend(self.name, 1, "month")
        return out[:n]

    def fetch(self, url: str, *, max_chars: int = 6000) -> FetchResult:
        """Tavily /extract — same keyless/keyed duality."""
        req = urllib.request.Request(
            "https://api.tavily.com/extract",
            data=json.dumps({"urls": [url]}).encode(), method="POST")
        req.add_header("Content-Type", "application/json")
        for k, v in self._headers().items():
            req.add_header(k, v)
        try:
            with urllib.request.urlopen(req, timeout=40) as resp:
                data = json.loads(resp.read().decode())
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            raise ProviderError(f"tavily extract: {e}") from None
        res = (data.get("results") or [{}])[0]
        return FetchResult(url=url, title=res.get("title", ""),
                           content=res.get("raw_content", "")[:max_chars], provider=self.name)
