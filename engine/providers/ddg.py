"""DuckDuckGo html endpoint — keyless bottom of the chain (scraping).
POST to html.duckduckgo.com/html/, browser UA, 1-2s politeness pause on
consecutive calls. Known-good from RU as of 2026-08-21/27."""

from __future__ import annotations

import html as htmllib
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import List, Optional

from .base import Provider, ProviderError, QuotaSpec, SearchResult

ENDPOINT = "https://html.duckduckgo.com/html/"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

_HREF_RE = re.compile(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', re.S)
_SNIP_RE = re.compile(r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>', re.S)
_TAG_RE = re.compile(r"<[^>]+>")
_last_call = 0.0


def _clean(s: str) -> str:
    return htmllib.unescape(_TAG_RE.sub("", s)).strip()


def _unredirect(href: str) -> str:
    # DDG wraps external links: //duckduckgo.com/l/?uddg=<urlencoded>&rut=...
    if "uddg=" in href:
        q = urllib.parse.parse_qs(urllib.parse.urlparse("https:" + href if href.startswith("//") else href).query)
        if "uddg" in q:
            return q["uddg"][0]
    if href.startswith("//"):
        return "https:" + href
    return href


class DdgProvider(Provider):
    name = "ddg"
    quota = QuotaSpec(limit=None, period="none",
                      label="keyless scraping; throttle 1.5s between calls")

    def search(self, query: str, *, n: int = 8, freshness: Optional[str] = None) -> List[SearchResult]:
        global _last_call
        wait = 1.5 - (time.time() - _last_call)
        if wait > 0:
            time.sleep(wait)
        _last_call = time.time()
        body = urllib.parse.urlencode({"q": query}).encode()
        req = urllib.request.Request(ENDPOINT, data=body, method="POST")
        req.add_header("User-Agent", UA)
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                page = resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            # 202 = anti-bot challenge
            raise ProviderError(f"ddg {e.code} (challenge?)", retryable=(e.code >= 500)) from None
        except urllib.error.URLError as e:
            raise ProviderError(f"ddg network: {e.reason}") from None
        links = _HREF_RE.findall(page)
        snips = [_clean(s) for s in _SNIP_RE.findall(page)]
        if not links:
            raise ProviderError("ddg: 0 results parsed (layout changed or challenge)", retryable=False)
        out = []
        for i, (href, title) in enumerate(links[:n]):
            out.append(SearchResult(
                url=_unredirect(htmllib.unescape(href)),
                title=_clean(title),
                snippet=snips[i] if i < len(snips) else "",
                provider=self.name,
            ))
        return out
