"""r.jina.ai — keyless URL reader (~20 RPM anonymous), markdown output.
The fetch-side bottom of the chain."""

from __future__ import annotations

import urllib.error
import urllib.parse
import urllib.request

from .base import FetchResult, Provider, ProviderError, QuotaSpec


class JinaProvider(Provider):
    name = "jina"
    quota = QuotaSpec(limit=None, period="none", label="keyless ~20 RPM")
    can_fetch = True

    def fetch(self, url: str, *, max_chars: int = 6000) -> FetchResult:
        # кириллица и прочий не-ASCII в пути обязаны быть percent-encoded,
        # иначе urllib падает с UnicodeEncodeError (ru.wikipedia, 27.08)
        safe_url = urllib.parse.quote(url, safe=":/?#[]@!$&'()*+,;=%")
        req = urllib.request.Request(f"https://r.jina.ai/{safe_url}")
        req.add_header("User-Agent", "wsearch/1.0")
        try:
            with urllib.request.urlopen(req, timeout=40) as resp:
                text = resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            raise ProviderError(f"jina {e.code}", retryable=(e.code == 429 or e.code >= 500)) from None
        except urllib.error.URLError as e:
            raise ProviderError(f"jina network: {e.reason}") from None
        # "Title: ...\n\nURL Source: ...\n\nMarkdown Content:\n..."
        title = ""
        if text.startswith("Title: "):
            title = text.split("\n", 1)[0][7:].strip()
        return FetchResult(url=url, title=title, content=text[:max_chars], provider=self.name)
