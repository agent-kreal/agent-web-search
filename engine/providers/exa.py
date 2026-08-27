"""Exa — keyed search API ($10/mo credit ≈ 1400 searches, no card needed).
Register: dashboard.exa.ai -> API Keys. Slot activates when key lands in .env."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import List, Optional

from .. import config, quotas
from .base import Provider, ProviderError, QuotaSpec, SearchResult

API = "https://api.exa.ai/search"


class ExaProvider(Provider):
    name = "exa"
    quota = QuotaSpec(limit=1400, period="month", label="$10 monthly credit ~1400/mo")

    def __init__(self):
        self.key = config.get("EXA_API_KEY")
        if not self.key:
            self.available_reason = "no key — register at dashboard.exa.ai"

    def search(self, query: str, *, n: int = 8, freshness: Optional[str] = None) -> List[SearchResult]:
        # highlights: token-efficient query-relevant excerpts (Exa's own
        # recommendation for agent loops; canonical ref: docs.exa.ai search guide)
        body = {"query": query, "numResults": n, "type": "auto",
                "contents": {"highlights": True}}
        if freshness in ("day", "week", "month"):
            body["category"] = "news"
        req = urllib.request.Request(API, data=json.dumps(body).encode(), method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("x-api-key", self.key)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (429, 402):
                quotas.mark_exhausted(self.name, None, "month")
                raise ProviderError(f"exa {e.code} quota/credit", quota_exhausted=True) from None
            detail = e.read().decode("utf-8", "replace")[:200]
            raise ProviderError(f"exa {e.code}: {detail}", retryable=(e.code >= 500)) from None
        except urllib.error.URLError as e:
            raise ProviderError(f"exa network: {e.reason}") from None
        out = []
        for r in data.get("results", []):
            highlights = r.get("highlights") or []
            snippet = " … ".join(h.strip() for h in highlights if h.strip())[:500]
            out.append(SearchResult(
                url=r.get("url", ""), title=r.get("title", ""),
                snippet=snippet,
                date=(r.get("publishedDate") or "")[:10] or None,
                provider=self.name,
            ))
        if not out:
            raise ProviderError("exa returned no results", retryable=False)
        quotas.spend(self.name, 1, "month")
        return out[:n]
