"""Brave Search API — keyed, 2000 queries/month free tier, 1 rps.
Key: .env BRAVE_API_KEY or ~/.claude/.brave_api_key."""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import List, Optional

from .. import config, quotas
from .base import Provider, ProviderError, QuotaSpec, SearchResult

API = "https://api.search.brave.com/res/v1/web/search"


class BraveProvider(Provider):
    name = "brave"
    quota = QuotaSpec(limit=2000, period="month", label="free tier 2000/mo, 1 rps")

    def __init__(self):
        self.key = config.brave_api_key()
        if not self.key:
            self.available_reason = "no Brave API key"

    def search(self, query: str, *, n: int = 8, freshness: Optional[str] = None) -> List[SearchResult]:
        url = f"{API}?q={urllib.parse.quote(query)}&count={n}"
        if freshness == "day":
            url += "&freshness=pd"
        elif freshness == "week":
            url += "&freshness=pw"
        elif freshness == "month":
            url += "&freshness=pm"
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/json")
        req.add_header("X-Subscription-Token", self.key)
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = json.loads(resp.read().decode())
                self._record_ratelimit(resp)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                quotas.mark_exhausted(self.name, None, "month")
                raise ProviderError("brave 429 rate/quota", quota_exhausted=True) from None
            detail = e.read().decode("utf-8", "replace")[:200]
            raise ProviderError(f"brave {e.code}: {detail}", retryable=(e.code >= 500)) from None
        except urllib.error.URLError as e:
            raise ProviderError(f"brave network: {e.reason}") from None
        out = []
        for r in (data.get("web") or {}).get("results", []):
            out.append(SearchResult(
                url=r.get("url", ""), title=r.get("title", ""),
                snippet=r.get("description", "")[:500],
                date=r.get("age"), provider=self.name,
            ))
        if not out:
            raise ProviderError("brave returned no results", retryable=False)
        quotas.spend(self.name, 1, "month")
        return out[:n]

    @staticmethod
    def _record_ratelimit(resp) -> None:
        """Brave ships rate-limit truth in EVERY response (free, passive).
        Paired buckets per window: x-ratelimit-policy '50;w=1, 0;w=2592000'
        (= 50/sec + a 30-day bucket), with x-ratelimit-limit/-remaining in
        the same order (live-verified 09.09: '50, 0' / '49, 0'). The quota
        bucket is the LONGEST window; a 0-limit bucket means 'not tracked'
        (searches succeed at 0,0) — record nothing and keep the local
        counter instead of writing a bogus 'exhausted'."""
        def _ints(header: str) -> list:
            out = []
            for part in (resp.headers.get(header) or "").split(","):
                try:
                    out.append(int(part.strip()))
                except ValueError:
                    pass
            return out
        windows = []
        for part in (resp.headers.get("X-RateLimit-Policy") or "").split(","):
            try:
                windows.append(int(part.split("w=")[-1]))
            except ValueError:
                windows.append(0)
        lims, rems = _ints("X-RateLimit-Limit"), _ints("X-RateLimit-Remaining")
        if windows and len(windows) == len(lims) == len(rems):
            i = windows.index(max(windows))  # longest window = quota bucket
            # a quota window spans at least a day; a lone w=1 bucket is a
            # throughput (rps) limit, not a quota — ignore it
            if windows[i] >= 86400 and lims[i] > 0:
                quotas.set_server("brave", unit="requests",
                                  remaining=rems[i], limit=lims[i])
            return
        # legacy layout without policy: '1, 15000' — a PAIR (rps + monthly);
        # a lone bucket is ambiguous (may be just rps) — ignore it
        if len(lims) >= 2 and len(rems) >= 2 and lims[-1] > 0:
            quotas.set_server("brave", unit="requests",
                              remaining=rems[-1], limit=lims[-1])
