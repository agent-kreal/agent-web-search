"""Linkup — keyed, 4000 free searches (one-off grant, no card).
Register: linkup.so. Slot activates with LINKUP_API_KEY in .env."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import List, Optional

from .. import config, quotas
from .base import Provider, ProviderError, QuotaSpec, SearchResult

API = "https://api.linkup.so/v1/search"


class LinkupProvider(Provider):
    name = "linkup"
    # $20 credit topped back up monthly for eligible accounts;
    # standard searchResults = $0.005/query -> ~4000/mo, deep costs more
    # (usd server-truth: balance endpoint; price = $ per 1 local unit)
    quota = QuotaSpec(limit=4000, period="month", unit="usd", price=0.005,
                      label="$20/mo top-up ≈ 4000 std searches")

    def __init__(self):
        self.key = config.get("LINKUP_API_KEY")
        if not self.key:
            self.available_reason = "no key — register at linkup.so"

    def search(self, query: str, *, n: int = 8, freshness: Optional[str] = None) -> List[SearchResult]:
        body = {"q": query, "depth": "deep" if freshness else "standard",
                "outputType": "searchResults"}
        req = urllib.request.Request(
            API, data=json.dumps(body).encode(), method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {self.key}")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (429, 402):
                quotas.mark_exhausted(self.name, None, "month")
                raise ProviderError(f"linkup {e.code} quota", quota_exhausted=True) from None
            detail = e.read().decode("utf-8", "replace")[:200]
            raise ProviderError(f"linkup {e.code}: {detail}", retryable=(e.code >= 500)) from None
        except urllib.error.URLError as e:
            raise ProviderError(f"linkup network: {e.reason}") from None
        out = []
        for r in data.get("results", []):
            out.append(SearchResult(
                url=r.get("url", ""), title=r.get("name") or r.get("title", ""),
                snippet=(r.get("content") or "")[:500], provider=self.name,
            ))
        if not out:
            raise ProviderError("linkup returned no results", retryable=False)
        # std search = $0.005 (1 credit unit of 4000); deep costs more
        quotas.spend(self.name, 2 if freshness else 1, "month")
        return out[:n]
