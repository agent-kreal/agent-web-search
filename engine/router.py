"""Router: try providers in priority order, skipping exhausted ones BEFORE
spending a request, falling through on errors. The quota ledger turns a
real 429 into a skip for all subsequent calls until reset."""

from __future__ import annotations

import os
import re
import time
from typing import List, Optional
from urllib.parse import urlparse, urlunparse

from . import fetchcache, quotas
from .prefilter import strip_junk
from .providers import FETCH_CHAIN, SEARCH_CHAIN, FetchResult, Provider, ProviderError
from .providers.base import reject_reason
from .providers.local import CONTENT_CAP as FETCH_FULL_CAP
from .sanitize import sanitize, untrusted_wrap
from .truncate import smart_truncate

# Фаза 2 (19.10): fetched-контент = untrusted. WS_SANITIZE=0 выключает
# фильтры и обёртку целиком (emergency escape).
SANITIZE_OFF = os.environ.get("WS_SANITIZE", "1") == "0"

# Фаза 5.1 (bench-extract): сервисные экстракторы возвращают ok=true с
# пустотой — tavily 17% «успехов» <200 симв. (wiki-TOC/антибот), jina —
# challenge-страницы. Такой «успех» = фейл → фолбэк вниз. gh/local exempt:
# нативные тиры fail loudly (empty% 0 на бенче), их короткий вывод —
# реальный короткий контент, а не битая экстракция.
SERVICE_FETCH_TIERS = frozenset({"firecrawl", "tavily", "jina", "parallel"})
MIN_FETCH_CHARS = 200


def _issue_content(content: str, max_chars: int, raw_cut: bool,
                   url: str = "") -> tuple[str, list[dict]]:
    """Финальная подготовка fetch-контента к выдаче.

    raw_cut — только старый тупой рез (фаза 0), без санитизации/обёртки.
    Дефолт (фазы 1–2): sanitize (BrowseSafe-паттерны) → untrusted-обёртка →
    prefilter мусора → smart-резка. Возвращает (content, sanitize_findings)
    — findings пустые, если санитайзер выключен."""
    if raw_cut:
        return content[:max_chars], []
    cleaned, findings = (content, []) if SANITIZE_OFF else sanitize(content)
    wrapped = cleaned if SANITIZE_OFF else untrusted_wrap(url, cleaned)
    body = smart_truncate(strip_junk(wrapped)[0], max_chars)
    return body, findings


class ChainError(RuntimeError):
    """Whole chain failed. Carries `tried` ({name, error, wall_sec}) so the
    usage log keeps every attempt's reason even on a total failure — the
    audit (09.09) showed failed invocations logged tried=[] and hid which
    providers actually errored vs were skipped."""

    def __init__(self, msg: str, tried: list):
        super().__init__(msg)
        self.tried = tried

# Intent -> preferred provider order (benchmark bench/REPORT.md §6.1).
# Only reorders the chain: quota skipping and fallback-down are unchanged.
# youcom исключён из подъёмов 20.10: free MCP paywalled, keyed REST — one-off
# $-грант в хвосте цепочки; поднимем интентом снова, если кредиты станут
# возобновляемыми. Его прошлая сила (fact 94% hit@3, RU-топ) распределена:
# fact→exa (лидер v2-бенча), ru→zai.
INTENT_ORDER: dict = {
    "docs":     ["exa", "tavily"],                 # exa: only one that returns official docs
    "research": ["exa", "brave"],
    "fact":     ["exa", "tavily", "brave"],        # exa — лидер v2 (0.789 quality)
    # v2 re-baseline 20.10 (n_q=7), по итогу ревью: ddg R 0.269 / P 0.820 /
    # Q 0.824 — лучший (n=5: антибот резал серию бенча, одиночные запросы не
    # серия), linkup Q 0.809 — второй. Прошлый лидер v1 tavily — 7-й из 9
    # (Q 0.580: устаревшие страницы, EN-статьи на RU-вопрос), brave 0.586.
    "news-ru":  ["ddg", "linkup"],
    # v2 re-baseline 20.10 (n_q=8): ddg R 0.376 / Q 0.782 — доминирует с отрывом
    # (2-й linkup R 0.174), linkup Q 0.680 — второй; exa первым проваливался
    # (R 0.132 — худший), zai Q 0.481 — замыкающий. ddg в дефолтной цепочке
    # последний из-за антибота под СЕРИЯМИ — одиночный news-запрос не серия;
    # если антибот всё же бьёт — мгновенный фолбэк на linkup.
    "news-en":  ["ddg", "linkup"],
    "ru":       ["zai", "brave", "tavily"],        # zai:RU-качество ок (бенч 24.09, 5/5)
    "debug":    ["tavily", "brave"],               # exa risky: sometimes empty on error strings
    "github":   ["gh", "exa", "tavily", "brave"],  # gh: native repo search (free)
}


# Telegram web preview: нормализация ДО кэша и всех провайдеров — ключ кэша
# и нижестоящие тиры (firecrawl/jina) получают /s/-версию. Дубль логики
# живёт в local-extract/src/local_extract/tg.py (subprocess-контракт не
# даёт общий импорт); менять — синхронно в обоих.
_TG_HOSTS = frozenset({"t.me", "telegram.me", "telegram.dog"})
_TG_INVITE = re.compile(r"^/(?:\+[\w-]+|joinchat/)", re.I)
_TG_CHANNEL = re.compile(r"^/(?!s/)([^/]+)(/.*)?$")


def _normalize_fetch_url(url: str) -> str:
    """t.me/<канал>[/<id>] -> t.me/s/<канал>[/<id>]; telegram.me/dog -> t.me."""
    try:
        parts = urlparse(url)
    except ValueError:
        return url
    if parts.netloc.lower() not in _TG_HOSTS:
        return url
    path = parts.path or "/"
    if not _TG_INVITE.match(path):
        m = _TG_CHANNEL.match(path)
        if m:
            path = f"/s{path}"
    return urlunparse((parts.scheme or "https", "t.me", path, "",
                       parts.query, ""))


def _is_tg_invite(url: str) -> bool:
    try:
        return bool(_TG_INVITE.match(urlparse(url).path)) \
            and urlparse(url).netloc.lower() in _TG_HOSTS
    except ValueError:
        return False


def _skip_reason(p: Provider) -> Optional[str]:
    if not p.available():
        return p.available_reason or "unavailable"
    reason = quotas.is_exhausted(p.name)
    if reason:
        return reason
    rem = quotas.remaining(p.name, p.quota.limit, p.quota.period,
                           price=p.quota.price)
    if rem is not None and rem <= 0:
        # server snapshot (quota endpoint / rate-limit headers) beats a
        # possibly-drifted local counter — say which one said "empty"
        has_server = quotas.server_view(p.name, price=p.quota.price,
                                        period=p.quota.period) is not None
        return "quota at 0 (server)" if has_server else "quota at 0 (local counter)"
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
    """Returns {"results": [...], "provider": name, "tried": [{name, error}],
    "rejected": n} — rejected = сколько записей сняла schema-валидация
    (фаза 4.3); полностью забракованная выдача = фолбэк вниз по цепочке."""
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
            # фаза 4.3: schema-валидация до merge (брак не доезжает ни до
            # выдачи, ни до multi-слияния); вся выдача забракована = симптом
            # сломанного формата ответа → каскад идёт ниже
            keep = [r for r in results if reject_reason(r) is None]
            n_rej = len(results) - len(keep)
            if not keep:
                raise ProviderError(
                    f"all {n_rej} results rejected by schema check",
                    retryable=True)
            return {"results": keep, "provider": p.name, "tried": tried,
                    "rejected": n_rej}
        except ProviderError as e:
            tried.append({"name": p.name, "error": str(e),
                          "wall_sec": round(time.monotonic() - t0, 1)})
            last = e
            continue
    raise ChainError(
        "all providers failed: " + "; ".join(f"{t['name']}: {t['error']}" for t in tried),
        tried,
    ) from last


def fetch(url: str, *, max_chars: int = 6000,
          providers: Optional[List[str]] = None,
          use_cache: bool = True,
          raw_cut: bool = False) -> dict:
    """Returns {"result": FetchResult, "provider": name, "tried": [...],
    "cached": bool}. Cache hits answer before any provider is tried (even
    exhausted ones); the final max_chars truncation happens here, so the
    cache can hold the full copy (local tier always returns up to 32k).

    Smart cut (default since 19.10, фаза 1 плана improvement-plan-2026-10-19):
    providers are asked for the full copy (FETCH_FULL_CAP), the cache stores
    it, and the issued content is cut to max_chars on a sentence/paragraph/
    fence boundary (engine/truncate.py) instead of a blind [:max_chars].
    raw_cut=True (флаг --raw-cut / env WS_RAW_CUT=1) keeps the old blind
    cut everywhere."""
    # Telegram: нормализация до кэша (ключ) и до всех провайдеров; инвайт-
    # ссылкам web preview не существует — сразу честный фейл, не жжём тиры
    if _is_tg_invite(url):
        raise ChainError(
            f"telegram invite link (private): {url} — web preview не существует",
            [{"name": "preflight", "error": "telegram invite link",
              "wall_sec": 0}],
        )
    url = _normalize_fetch_url(url)
    if use_cache:
        hit = fetchcache.get(url)
        if hit is not None:
            cached_content = hit.get("content") or ""
            issue, findings = _issue_content(cached_content, max_chars, raw_cut,
                                             url=hit.get("url") or url)
            fr = FetchResult(url=hit.get("url") or url,
                             title=hit.get("title", ""),
                             content=issue,
                             provider=hit.get("provider", "cache"))
            return {"result": fr, "provider": fr.provider, "cached": True,
                    "tried": [], "sanitize": findings}
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
            # smart-режим просит полную копию (кэш хранит её целиком); финальная
            # резка — на выдаче. raw_cut — старое поведение: режет и провайдер.
            cap = max_chars if raw_cut else FETCH_FULL_CAP
            fr = p.fetch(url, max_chars=cap)
            # фаза 5.1: пустой «успех» сервисного тира = фейл → ниже по цепочке.
            # Порог зажат запрошенным cap (raw-cut с крошечным max_chars не
            # должен ложно фейлить честный короткий ответ). Проверка — ДО
            # fetchcache.put: пустоту нельзя кэшировать (TTL 30 мин отравления).
            n_chars = len(fr.content.strip())
            if p.name in SERVICE_FETCH_TIERS and n_chars < min(MIN_FETCH_CHARS, cap):
                raise ProviderError(
                    f"ok but empty extraction: {n_chars} chars "
                    f"< {min(MIN_FETCH_CHARS, cap)}", retryable=False)
            if use_cache:
                fetchcache.put(url, provider=fr.provider or p.name,
                               title=fr.title, content=fr.content)
            issue, findings = _issue_content(fr.content, max_chars, raw_cut, url=url)
            fr.content = issue
            return {"result": fr, "provider": p.name, "tried": tried,
                    "sanitize": findings}
        except ProviderError as e:
            tried.append({"name": p.name, "error": str(e),
                          "wall_sec": round(time.monotonic() - t0, 1)})
            last = e
            continue
    raise ChainError(
        f"all fetch providers failed for {url}: "
        + "; ".join(f"{t['name']}: {t['error']}" for t in tried),
        tried,
    ) from last
