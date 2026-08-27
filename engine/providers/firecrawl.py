"""Firecrawl — keyed scrape (markdown of JS-heavy pages, PDFs).
~2000 credits/mo (reset on the 23rd), 1 credit ≈ 1 scrape.
Register: firecrawl.dev. Fetch-only slot; no search capability used."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

from .. import config, quotas
from .base import FetchResult, Provider, ProviderError, QuotaSpec

API = "https://api.firecrawl.dev/v1/scrape"


class FirecrawlProvider(Provider):
    name = "firecrawl"
    quota = QuotaSpec(limit=2000, period="month", label="~2000 credits/mo, reset ~23rd")

    def __init__(self):
        self.key = config.get("FIRECRAWL_API_KEY")
        if not self.key:
            self.available_reason = "no key — register at firecrawl.dev"
        self.can_fetch = True

    def fetch(self, url: str, *, max_chars: int = 6000) -> FetchResult:
        req = urllib.request.Request(
            API, data=json.dumps({"url": url, "formats": ["markdown"]}).encode(),
            method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {self.key}")
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 402:  # credits spent — skip until the monthly reset
                quotas.mark_exhausted(self.name, None, "month")
                raise ProviderError("firecrawl 402 credits", quota_exhausted=True) from None
            if e.code == 429:  # rate limit — brief cooldown, NOT a month
                cooldown = (datetime.now(timezone.utc) + timedelta(seconds=90)).isoformat(timespec="seconds")
                quotas.mark_exhausted(self.name, cooldown)
                raise ProviderError("firecrawl 429 rate-limit", retryable=True) from None
            detail = e.read().decode("utf-8", "replace")[:200]
            raise ProviderError(f"firecrawl {e.code}: {detail}", retryable=(e.code >= 500)) from None
        except urllib.error.URLError as e:
            raise ProviderError(f"firecrawl network: {e.reason}") from None
        d = (data.get("data") or {})
        md = d.get("markdown") or ""
        quotas.spend(self.name, 1, "month")
        return FetchResult(url=url, title=d.get("metadata", {}).get("title", ""),
                           content=md[:max_chars], provider=self.name)
