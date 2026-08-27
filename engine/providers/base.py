"""Provider base: unified result shape + quota contract."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


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


@dataclass
class FetchResult:
    url: str
    title: str = ""
    content: str = ""                   # markdown
    provider: str = ""


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
