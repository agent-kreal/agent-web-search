"""Тиры загрузки: httpx (обычный) и curl_cffi (TLS-имперсонация chrome).
Оба возвращают единый FetchResponse. curl_cffi импортируется лениво —
его тянет только браузерный/антибот-путь."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36")
MAX_BODY = 5 * 1024 * 1024  # 5 МБ — хватает для любых статей

# Корни НУЦ Минцифры: госсайты (*.digital.gov.ru и др.) отдают цепочки,
# которых нет в certifi (Mozilla их не включает) -> CERTIFICATE_VERIFY_FAILED.
# Бандл = certifi + оба русских серта; пересобирается сам, когда любой
# источник обновился (mtime), запись атомарная (os.replace).
_CERTS_DIR = Path(__file__).resolve().parent.parent.parent / "certs"
_NUC_ROOT = _CERTS_DIR / "russian_trusted_root_ca.pem"
_NUC_SUB = _CERTS_DIR / "russian_trusted_sub_ca.pem"
_BUNDLE = _CERTS_DIR / "ca-bundle.crt"


def ca_bundle() -> str:
    """Путь к CA-бандлу для verify. Русских сертов нет — дефолтный certifi."""
    import certifi

    if not (_NUC_ROOT.exists() and _NUC_SUB.exists()):
        return certifi.where()
    newest_src = max(os.path.getmtime(p) for p in
                     (certifi.where(), _NUC_ROOT, _NUC_SUB))
    if not _BUNDLE.exists() or os.path.getmtime(_BUNDLE) < newest_src:
        parts = []
        for p in (certifi.where(), _NUC_ROOT, _NUC_SUB):
            parts.append(Path(p).read_bytes().rstrip(b"\n") + b"\n")
        tmp = _BUNDLE.with_suffix(".tmp")
        tmp.write_bytes(b"".join(parts))
        os.replace(tmp, _BUNDLE)
    return str(_BUNDLE)


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
            verify=ca_bundle(),
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
                     allow_redirects=True, verify=ca_bundle())
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
