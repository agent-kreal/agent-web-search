"""Provider registry + priority chain.

Policy (user, 2026-08-27, revised after tariff research): burn RENEWABLE
monthly quotas first (they expire at reset — use them or lose them), then
keyless/free tiers of the same services, then the free scraping floor, and
only as the last resort the one-off $-grants (they never refill — keep
them for emergencies).

Search chain (renewable -> keyless -> floor -> grants; revised 27.08 after
the benchmark, bench/REPORT.md §6.3 — linkup demoted for quality, ddg demoted
to the very last non-$ slot because its anti-bot kills bursts: 30/32 failed
under a steady 1 rps):
  1. tavily        1000 credits/mo, resets on the 1st -> auto-drops to keyless
  2. youcom        keyless MCP, 100/day (expires DAILY — spend it)
  3. zai           GLM Coding Plan 1000/mo (subscription quota)
  4. exa           $10/mo credit ~1400 searches (best quality: docs/semantic)
  5. brave         legacy 2000/mo, best for RU queries
  6. parallel-anon anonymous MCP (keyless floor)
  7. linkup        top-up to $20/mo ~4000 searches — big tank, but weakest
                  relevance (1.11/2 in bench); keep for bulk fan-out
  8. ddg           scraping floor — anti-bot under bursts, VERY last before $
  9. parallel      keyed: one-off $ grant — last resort only

Fetch chain (URL -> markdown): local cascade (httpx+trafilatura -> curl_cffi
-> playwright, free, covers ~80-90% of pages) -> firecrawl -> tavily extract
-> jina -> parallel ($ grant, last). Local aliases for --provider:
local-http / local-curl / local-browser force a cascade step.
"""

from typing import List

from .base import FetchResult, Provider, ProviderError, QuotaSpec, SearchResult
from .brave import BraveProvider
from .ddg import DdgProvider
from .exa import ExaProvider
from .firecrawl import FirecrawlProvider
from .jina import JinaProvider
from .linkup import LinkupProvider
from .local import LocalProvider
from .parallel import ParallelProvider
from .tavily import TavilyProvider
from .youcom import YoucomProvider
from .zai import ZaiProvider

__all__ = [
    "FetchResult", "Provider", "ProviderError", "QuotaSpec", "SearchResult",
    "BraveProvider", "DdgProvider", "ExaProvider", "FirecrawlProvider",
    "JinaProvider", "LinkupProvider", "LocalProvider", "ParallelProvider",
    "TavilyProvider", "YoucomProvider", "ZaiProvider",
]

SEARCH_CHAIN: List[Provider] = [
    TavilyProvider(),               # 1000/mo reset on the 1st -> keyless
    YoucomProvider(),               # 100/day, expires daily
    ZaiProvider(),                  # 1000/mo GLM plan (exhausted till 2026-09-18)
    ExaProvider(),                  # $10/mo ~1400, best quality (docs/semantic)
    BraveProvider(),                # legacy 2000/mo, RU-friendly
    ParallelProvider(keyed=False),  # anonymous keyless floor
    LinkupProvider(),               # big tank, weak relevance — bulk fan-out
    DdgProvider(),                  # anti-bot under bursts — VERY last before $
    ParallelProvider(keyed=True),   # one-off $ grant — last resort
]

# Fetch chain (URL -> markdown): free local cascade first (~80-90% of pages),
# then renewable credits, keyless bottom, $ grant last.
FETCH_CHAIN: List[Provider] = [
    LocalProvider(),                # free: httpx+trafilatura -> curl_cffi -> playwright
    FirecrawlProvider(),            # ~2000 credits/mo (renewable), JS/PDF
    TavilyProvider(),               # extract (keyed -> keyless)
    JinaProvider(),                 # r.jina.ai keyless bottom
    ParallelProvider(keyed=True),   # web_fetch, $ grant — last resort
]
