"""Provider base: unified result shape + quota contract."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
from urllib.parse import urlparse

# Schema-валидация (фаза 4.3, 19.10): минимальная осмысленная длина сниппета.
# 50, не 200 из плана: zai стабильно отдаёт 61–192 (content_size=medium — его
# формат, не деградация), ddg 57% <200 — порог 200 браковал бы здоровые
# выдачи. Ловим пустышки ("...", "N/A") и сломанный формат ответа.
MIN_SNIPPET = 50


@dataclass
class SearchResult:
    url: str
    title: str = ""
    snippet: str = ""
    date: Optional[str] = None
    provider: str = ""

    def to_dict(self) -> dict:
        d = {"url": self.url, "title": self.title, "snippet": self.snippet}
        if self.date:
            d["date"] = self.date
        d["provider"] = self.provider
        return d


@dataclass
class QuotaSpec:
    """How the provider's quota behaves for the local counter."""

    limit: Optional[int] = None        # None = unknown/unlimited (keyless)
    period: str = "none"               # none | day | month | once
    label: str = ""                    # human note for `status`
    unit: str = "requests"             # requests | credits | usd (server-truth units)
    price: float = 1.0                 # server units per 1 local unit
                                      # (usd: $ per request; credits/requests: 1.0)


@dataclass
class FetchResult:
    url: str
    title: str = ""
    content: str = ""                   # markdown
    provider: str = ""


def reject_reason(r: "SearchResult") -> Optional[str]:
    """Причина schema-брака записи выдачи или None (фаза 4.3).

    Провайдеры периодически меняют схему ответа молча (zai 24.09:
    url→link/snippet→content; youcom 19.10: snippets→description — записи
    месяцами ходили с пустыми сниппетами). Брак: без url / без текста
    вовсе / title есть, а сниппета нет / сниппет-пустышка. Полностью
    забракованная выдача фолбэкает каскадом вниз (router.search)."""
    url = (r.url or "").strip()
    try:
        ok_url = bool(urlparse(url).netloc)
    except ValueError:
        ok_url = False
    if not ok_url:
        return "no_url"
    title = (r.title or "").strip()
    snip = (r.snippet or "").strip()
    if not title and not snip:
        return "no_text"
    if not snip:
        return "no_snippet"       # tavily-урок: «успех» без контента
    if len(snip) < MIN_SNIPPET:
        return "short_snip"
    return None


class ProviderError(RuntimeError):
    def __init__(self, msg: str, *, quota_exhausted: bool = False, retryable: bool = True):
        super().__init__(msg)
        self.quota_exhausted = quota_exhausted
        self.retryable = retryable


class Provider:
    """One search backend. Subclass and set NAME; register in __init__.py."""

    name: str = "?"
    # search: required; fetch: optional (can_read)
    quota = QuotaSpec()
    available_reason: Optional[str] = None   # why not available (no key etc.)
    # set by the router when --provider matched an alias (e.g. local-browser
    # forces the local cascade's browser step)
    forced_tier: Optional[str] = None

    def available(self) -> bool:
        return self.available_reason is None

    def search(self, query: str, *, n: int = 8, freshness: Optional[str] = None) -> List[SearchResult]:
        raise NotImplementedError

    # Optional fetch capability (URL -> markdown)
    can_fetch = False

    def fetch(self, url: str, *, max_chars: int = 6000) -> FetchResult:
        raise NotImplementedError
