"""Exa — keyed search API (free tier $10 credits/mo; search $7/1k + highlights
$1/1k pages ≈ $0.013/request ≈ 750/mo). Register: dashboard.exa.ai -> API Keys.
Slot activates when key lands in .env."""

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
    quota = QuotaSpec(limit=750, period="month", label="free tier $10/mo ≈750 (≈$0.013/request)")

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
            # 402 = баланс реально кончился → до 1-го числа; 429 = rate-limit
            # free tier → часа хватает (эпизод 03.09: 429 заглушил exa на месяц
            # при живом балансе $19). Коды не смешивать!
            if e.code == 402:
                quotas.mark_exhausted(self.name, None, "month")
                raise ProviderError("exa 402 out of credit", quota_exhausted=True) from None
            if e.code == 429:
                quotas.mark_exhausted(self.name, None, "none")
                raise ProviderError("exa 429 rate-limit", quota_exhausted=False) from None
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
