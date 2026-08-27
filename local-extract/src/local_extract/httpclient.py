"""Тиры загрузки: httpx (обычный) и curl_cffi (TLS-имперсонация chrome).
Оба возвращают единый FetchResponse. curl_cffi импортируется лениво —
его тянет только браузерный/антибот-путь."""

from __future__ import annotations

import time
from dataclasses import dataclass, field

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36")
MAX_BODY = 5 * 1024 * 1024  # 5 МБ — хватает для любых статей


class TierError(Exception):
    """Сбой ступени: reason in network | timeout | unsupported."""

    def __init__(self, reason: str, detail: str = ""):
        super().__init__(detail or reason)
        self.reason = reason
        self.detail = detail


@dataclass
class FetchResponse:
    status: int
    body: bytes
    final_url: str
    via: str                       # http | curl | browser
    elapsed_ms: int
    headers: dict = field(default_factory=dict)


def fetch_http(url: str, timeout: float = 10.0) -> FetchResponse:
    import httpx

    t0 = time.monotonic()
    try:
        r = httpx.get(
            url,
            headers={
                "User-Agent": UA,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en,ru;q=0.8",
            },
            follow_redirects=True,
            timeout=timeout,
        )
    except httpx.TimeoutException as e:
        raise TierError("timeout", type(e).__name__) from None
    except httpx.HTTPError as e:
        raise TierError("network", str(e)[:120]) from None
    return FetchResponse(
        r.status_code, r.content[:MAX_BODY], str(r.url), "http",
        int((time.monotonic() - t0) * 1000), dict(r.headers),
    )


def fetch_curl(url: str, timeout: float = 15.0) -> FetchResponse:
    from curl_cffi import requests as creq   # лениво

    t0 = time.monotonic()
    try:
        r = creq.get(url, impersonate="chrome", timeout=timeout,
                     allow_redirects=True)
    except Exception as e:                    # RequestsError и все его варианты
        name = type(e).__name__
        reason = "timeout" if "timeout" in name.lower() else "network"
        raise TierError(reason, f"{name}: {str(e)[:100]}") from None
    try:
        hdrs = dict(r.headers)
    except Exception:
        hdrs = {}
    return FetchResponse(
        r.status_code, r.content[:MAX_BODY], str(r.url), "curl",
        int((time.monotonic() - t0) * 1000), hdrs,
    )
