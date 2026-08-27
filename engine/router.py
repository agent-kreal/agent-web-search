"""Router: try providers in priority order, skipping exhausted ones BEFORE
spending a request, falling through on errors. The quota ledger turns a
real 429 into a skip for all subsequent calls until reset."""

from __future__ import annotations

import time
from typing import List, Optional

from . import fetchcache, quotas
from .providers import FETCH_CHAIN, SEARCH_CHAIN, FetchResult, Provider, ProviderError

# Intent -> preferred provider order (benchmark bench/REPORT.md §6.1).
# Only reorders the chain: quota skipping and fallback-down are unchanged.
INTENT_ORDER: dict = {
    "docs":     ["exa", "youcom", "tavily"],       # exa: only one that returns official docs
    "research": ["exa", "youcom", "brave"],
    "fact":     ["youcom", "exa", "brave"],        # youcom hit@3 94%
    "news-ru":  ["tavily", "youcom", "brave"],     # tavily best, NEVER linkup first
    "news-en":  ["exa", "tavily", "youcom"],
    "ru":       ["youcom", "brave", "tavily"],     # tavily pulls EN lists on RU-specific queries
    "debug":    ["tavily", "youcom", "brave"],     # exa risky: sometimes empty on error strings
    "github":   ["gh", "exa", "youcom", "tavily", "brave"],  # gh: native repo search (free)
}


def _skip_reason(p: Provider) -> Optional[str]:
    if not p.available():
        return p.available_reason or "unavailable"
    reason = quotas.is_exhausted(p.name)
    if reason:
        return reason
    rem = quotas.remaining(p.name, p.quota.limit, p.quota.period)
    if rem is not None and rem <= 0:
        return "local quota counter at 0"
    return None


def _chain(names: Optional[List[str]], default: List[Provider]) -> List[Provider]:
    """Build the chain from --provider names. Aliases (e.g. local-http)
    resolve to the same provider and force its cascade tier."""
    for p in default:
        if hasattr(p, "forced_tier"):
            p.forced_tier = None
    if not names:
        return default
    by_name = {p.name: p for p in default}
    for p in default:
        for alias in (getattr(p, "aliases", None) or {}):
            by_name[alias] = p
    chain = []
    for n in names:
        p = by_name.get(n)
        if p is None:
            continue
        aliases = getattr(p, "aliases", None) or {}
        if n in aliases and hasattr(p, "forced_tier"):
            p.forced_tier = aliases[n]
        chain.append(p)
    return chain


def _effective_chain(query: str, intent: Optional[str]) -> List[Provider]:
    """Default chain reordered by intent; `site:` queries demote providers
    that ignore the operator (parallel-anon) or choke on it (exa returned
    empty in the bench)."""
    base = SEARCH_CHAIN
    if intent and intent in INTENT_ORDER:
        order = INTENT_ORDER[intent]
        rank = {name: i for i, name in enumerate(order)}
        base = sorted(base, key=lambda p: rank.get(p.name, len(rank)))
    if "site:" in query.lower():
        weak = [p for p in base if p.name in ("exa", "parallel-anon")]
        base = [p for p in base if p not in weak] + weak
    return base


def search(query: str, *, n: int = 8, freshness: Optional[str] = None,
           providers: Optional[List[str]] = None,
           intent: Optional[str] = None,
           dry_chain: bool = False) -> dict:
    """Returns {"results": [...], "provider": name, "tried": [{name, error}]}"""
    chain = _chain(providers, _effective_chain(query, intent))
    tried = []
    if dry_chain:
        return {"results": [], "provider": None,
                "chain": [{"name": p.name, "skip": _skip_reason(p)} for p in chain]}
    last = None
    for p in chain:
        skip = _skip_reason(p)
        if skip:
            tried.append({"name": p.name, "error": f"skipped: {skip}",
                          "wall_sec": 0})
            continue
        t0 = time.monotonic()
        try:
            results = p.search(query, n=n, freshness=freshness)
            return {"results": results, "provider": p.name, "tried": tried}
        except ProviderError as e:
            tried.append({"name": p.name, "error": str(e),
                          "wall_sec": round(time.monotonic() - t0, 1)})
            last = e
            continue
    raise RuntimeError(
        "all providers failed: " + "; ".join(f"{t['name']}: {t['error']}" for t in tried)
    ) from last


def fetch(url: str, *, max_chars: int = 6000,
          providers: Optional[List[str]] = None,
          use_cache: bool = True) -> dict:
    """Returns {"result": FetchResult, "provider": name, "tried": [...],
    "cached": bool}. Cache hits answer before any provider is tried (even
    exhausted ones); the final max_chars truncation happens here, so the
    cache can hold the full copy (local tier always returns up to 32k)."""
    if use_cache:
        hit = fetchcache.get(url)
        if hit is not None:
            fr = FetchResult(url=hit.get("url") or url,
                             title=hit.get("title", ""),
                             content=(hit.get("content") or "")[:max_chars],
                             provider=hit.get("provider", "cache"))
            return {"result": fr, "provider": fr.provider, "cached": True, "tried": []}
    chain = _chain(providers, FETCH_CHAIN)
    tried = []
    last = None
    for p in chain:
        if not p.can_fetch:
            continue
        # домен-специфичные тиры (gh) срабатывают только на своих URL —
        # чужие скипаем тихо, без записи в tried
        matcher = getattr(p, "matches_url", None)
        if matcher and not matcher(url):
            continue
        skip = _skip_reason(p)
        if skip:
            tried.append({"name": p.name, "error": f"skipped: {skip}",
                          "wall_sec": 0})
            continue
        t0 = time.monotonic()
        try:
            fr = p.fetch(url, max_chars=max_chars)
            if use_cache:
                fetchcache.put(url, provider=fr.provider or p.name,
                               title=fr.title, content=fr.content)
            fr.content = fr.content[:max_chars]
            return {"result": fr, "provider": p.name, "tried": tried}
        except ProviderError as e:
            tried.append({"name": p.name, "error": str(e),
                          "wall_sec": round(time.monotonic() - t0, 1)})
            last = e
            continue
    raise RuntimeError(
        f"all fetch providers failed for {url}: "
        + "; ".join(f"{t['name']}: {t['error']}" for t in tried)
    ) from last
