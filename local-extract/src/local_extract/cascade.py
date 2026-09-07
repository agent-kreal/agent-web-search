"""Оркестратор: порядок ступеней, дедлайн-бюджет, таблица решений, трейс.

Каскад (auto): httpx -> [curl_cffi при блоке/сетевом сбое] -> [playwright при
JS-пустышке/тонкой экстракции]. Каждая ступень пишет запись в trace.

Таблица решений (вердикт ступени http):
  ok / tiny_ok      -> успех (tier=http)
  blocked           -> тир curl
  js_shell          -> hydration-пейлоад -> успех (note=hydration), иначе тир browser
  thin              -> тир browser
  empty             -> провал extract_failed (браузеру нечего дорендеривать)
  pdf               -> провал unsupported/pdf (работа для firecrawl)
  TierError         -> один ретрай тиром curl (другой сетевой стек живучее)
"""

from __future__ import annotations

import time
from typing import Optional, Tuple
from urllib.parse import urlparse

from . import classify, extract as exmod, protocol
from .httpclient import FetchResponse, TierError, fetch_curl, fetch_http

STEP_HTTP_TIMEOUT = 10.0
STEP_CURL_TIMEOUT = 15.0
BROWSER_MAX_GOTO = 25.0
BROWSER_MIN_BUDGET = 8.0    # ниже этого браузер не стартуем (launch+goto+extract)
TINY_HTML = 2048            # «честно маленькая» страница — короткая выдача ок
BIG_HTML = 10240            # большой HTML со скриптами при короткой выдаче = JS

_FETCHERS = {
    "http": lambda url: fetch_http(url, STEP_HTTP_TIMEOUT),
    "curl": lambda url: fetch_curl(url, STEP_CURL_TIMEOUT),
}


def _verdict(resp: FetchResponse) -> Tuple[str, str, str]:
    """-> (verdict, title, text).
    verdict in ok|tiny_ok|blocked|js_shell|thin|empty|pdf"""
    body = resp.body
    if body[:512].lstrip()[:4].lower().startswith(b"%pdf") or \
            "application/pdf" in (resp.headers or {}).get("content-type", ""):
        return ("pdf", "", "")
    # JSON API-ответ (content-type или тело с {/[): не HTML — экстрактору
    # нечего искать, тело само и есть контент; иначе вердикт empty ложно
    # ронял каскад на живых API-эндпоинтах
    ct = (resp.headers or {}).get("content-type", "")
    if "json" in ct or body.lstrip()[:1] in (b"{", b"["):
        text, title = exmod.extract_json(body)
        return ("ok", title, text)
    if classify.is_block(resp.status, body):
        return ("blocked", "", "")
    md, title, tlen = exmod.extract_html(body, resp.final_url)
    scripts = classify.has_scripts(body)
    if md is None or tlen == 0:
        # Пустая экстракция: есть скрипты -> браузеру есть что исполнить;
        # без скриптов пусто = брать нечего вообще.
        if scripts:
            shell = classify.is_js_shell(body)
            return ("js_shell" if shell else "thin",
                    title or classify.title_of(body), "")
        return ("empty", title, "")
    if tlen >= exmod.MIN_TEXT:
        return ("ok", title, md)
    # Короткая выдача: маленькая страница без скриптов — честный результат
    # (tiny_ok); любые скрипты при короткой выдаче — пробуем браузер.
    if not scripts and len(body) < TINY_HTML:
        return ("tiny_ok", title, md)
    if scripts:
        return ("js_shell" if classify.is_js_shell(body) else "thin",
                title, md)
    return ("empty", title, md)


def _trace_step(trace: list, tier: str, resp: Optional[FetchResponse] = None,
                verdict: str = "", note: str = "", error: str = "") -> None:
    step: dict = {"tier": tier}
    if resp is not None:
        step.update({"status": resp.status, "ms": resp.elapsed_ms,
                     "html_len": len(resp.body)})
    if verdict:
        step["verdict"] = verdict
    if note:
        step["note"] = note
    if error:
        step["error"] = error
    trace.append(step)


def run(url: str, *, tier: str = "auto", max_chars: int = 32768,
        budget_s: float = 55.0) -> Tuple[dict, int]:
    """-> (outcome_dict, exit_code). Не кидает исключений наружу."""
    t0 = time.monotonic()
    trace: list = []

    def elapsed_ms() -> int:
        return int((time.monotonic() - t0) * 1000)

    def budget_left() -> float:
        return budget_s - (time.monotonic() - t0)

    def ok(resp: FetchResponse, tier_name: str, title: str, text: str,
           note: str = "") -> Tuple[dict, int]:
        # ступень уже записана в trace (run_step/browser_step) — только note
        if note and trace and trace[-1].get("tier") == tier_name:
            trace[-1]["note"] = note
        return (protocol.outcome_ok(url=resp.final_url or url, title=title,
                                    content=text[:max_chars], tier=tier_name,
                                    status=resp.status, elapsed_ms=elapsed_ms(),
                                    trace=trace),
                protocol.EXIT_OK)

    def fail(reason: str, note: str = "") -> Tuple[dict, int]:
        return (protocol.outcome_fail(reason, url, elapsed_ms(), trace, note),
                protocol.EXIT_FAIL)

    def run_step(name: str, url_arg: str):
        """-> (resp | None, verdict, title, text). verdict='tier_error' при сбое."""
        try:
            resp = _FETCHERS[name](url_arg)
        except TierError as e:
            detail = f": {e.detail}" if e.detail else ""
            _trace_step(trace, name, error=f"{e.reason}{detail}")
            return (None, "tier_error", "", "")
        verdict, title, text = _verdict(resp)
        _trace_step(trace, name, resp=resp, verdict=verdict)
        return (resp, verdict, title, text)

    def browser_step() -> Tuple[dict, int]:
        """Ступень playwright с проверкой бюджета."""
        if budget_left() < BROWSER_MIN_BUDGET:
            _trace_step(trace, "browser", error=f"budget left {budget_left():.0f}s < {BROWSER_MIN_BUDGET}s")
            return fail("blocked", "budget")
        try:
            from .browser import fetch_browser
        except ImportError:
            return fail("unsupported", "playwright missing")
        try:
            resp = fetch_browser(url, min(BROWSER_MAX_GOTO, max(5.0, budget_left())))
        except TierError as e:
            detail = f": {e.detail}" if e.detail else ""
            _trace_step(trace, "browser", error=f"{e.reason}{detail}")
            return fail(e.reason)
        verdict, title, text = _verdict(resp)
        _trace_step(trace, "browser", resp=resp, verdict=verdict)
        if verdict in ("ok", "tiny_ok"):
            return ok(resp, "browser", title, text)
        if verdict == "pdf":
            return fail("unsupported", "pdf")
        if verdict == "blocked":
            return fail("blocked")
        return fail("extract_failed")

    # --- preflight (без сети) ---
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return fail("unsupported", "scheme")
    if parsed.path.lower().endswith(".pdf"):
        return fail("unsupported", "pdf")

    # --- forced tier: одна ступень, её вердикт финален ---
    if tier != "auto":
        if tier == "browser":
            return browser_step()
        resp, verdict, title, text = run_step(tier, url)
        if verdict == "tier_error":
            # у forced-шага ошибки сети/таймаута уже финальны
            return fail(_last_tier_error_reason(trace))
        if verdict in ("ok", "tiny_ok"):
            return ok(resp, tier, title, text)
        if verdict == "blocked":
            return fail("blocked")
        if verdict == "pdf":
            return fail("unsupported", "pdf")
        return fail("extract_failed")

    # --- ступень 1: httpx ---
    r1, v1, title1, text1 = run_step("http", url)
    if v1 == "tier_error":
        pass    # сетевой сбой/таймаут -> ретрай другим стеком (curl)
    elif v1 in ("ok", "tiny_ok"):
        return ok(r1, "http", title1, text1)
    elif v1 == "pdf":
        return fail("unsupported", "pdf")
    elif v1 == "empty":
        return fail("extract_failed")
    elif v1 == "js_shell" and r1 is not None:
        hyd = classify.hydration_payload(r1.body)
        if hyd:
            return ok(r1, "http", classify.title_of(r1.body), hyd,
                      note="hydration")
        # пейлоада нет — сразу браузер (TLS-фингерпринт не исполнит JS)

    # --- ступень 2: curl_cffi (только при блоке или сетевом сбое;
    # js_shell/thin идут сразу в браузер — TLS не исполнит JS) ---
    v2: Optional[str] = None
    if v1 in ("blocked", "tier_error"):
        r2, v2, title2, text2 = run_step("curl", url)
        if v2 == "tier_error":
            pass  # упала и curl — пробуем браузер, если хватит бюджета
        elif v2 in ("ok", "tiny_ok"):
            return ok(r2, "curl", title2, text2)
        elif v2 == "pdf":
            return fail("unsupported", "pdf")
        elif v2 == "empty":
            return fail("extract_failed")

    # --- ступень 3: playwright ---
    return browser_step()


def _last_tier_error_reason(trace: list) -> str:
    """reason последней ступени с ошибкой тира (network|timeout|unsupported)."""
    for step in reversed(trace):
        err = step.get("error", "")
        if err:
            for r in ("timeout", "unsupported", "network"):
                if err.startswith(r):
                    return r
            return "network"
    return "network"
