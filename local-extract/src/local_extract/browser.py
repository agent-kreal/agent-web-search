"""Browser-тир: Playwright chromium по отрендеренному DOM.
Паттерн aider: goto(networkidle) с таймаутом, при таймауте — забираем
page.content() как есть (частичный рендер часто достаточен)."""

from __future__ import annotations

import time

from .httpclient import UA, FetchResponse, TierError


def fetch_browser(url: str, timeout_s: float = 25.0) -> FetchResponse:
    try:
        from playwright.sync_api import sync_playwright
        from playwright.sync_api import TimeoutError as PWTimeout
    except ImportError:
        raise TierError("unsupported", "playwright not installed "
                         "(cd local-extract && uv run playwright install chromium)") from None

    t0 = time.monotonic()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                page = browser.new_page(user_agent=UA)
                nav = None
                try:
                    nav = page.goto(url, wait_until="networkidle",
                                    timeout=timeout_s * 1000)
                except PWTimeout:
                    pass            # не дождались тишины — берём что отрендерилось
                html = page.content()
                status = nav.status if nav is not None else 0
                ctype = ""
                if nav is not None:
                    try:
                        ctype = (nav.headers or {}).get("content-type", "")
                    except Exception:
                        pass
                return FetchResponse(
                    status, html.encode("utf-8", "replace"), url, "browser",
                    int((time.monotonic() - t0) * 1000),
                    {"content-type": ctype},
                )
            finally:
                browser.close()
    except TierError:
        raise
    except Exception as e:
        raise TierError("network", f"{type(e).__name__}: {str(e)[:100]}") from None
