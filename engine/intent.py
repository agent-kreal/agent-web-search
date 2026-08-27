"""Intent detection: map a raw query to a routing intent (bench/REPORT.md §6.1).

resolve(query, freshness, forced) -> (intent_key, source, reason)
  intent_key: docs | research | fact | news-ru | news-en | ru | debug | None
  source:     flag | auto | none

The intent only REORDERS the fallback chain (best-quality provider first per
scenario); quota skipping and fallback-down behave exactly as in the default
chain. Queries with a `site:` operator additionally demote exa (returned
empty on site: queries in the bench) and parallel-anon (ignores the operator)
to the end — handled in router, not here.
"""

from __future__ import annotations

import re

_CYR = re.compile(r"[а-яё]", re.IGNORECASE)

_DEBUG = (
    "error", "exception", "traceback", "tracebackmost", "crash", "crashes",
    "hangs", "hang", "зависает", "ошибка", "ошибк", "падает", "regression",
    "bug", "not working", "не работает", "fails", "fail with", "dies",
    "is down", "api down", "outage", "522", "503", "fix",
)
_FACT = (
    "pricing", "price", "prices", "tariff", "tariffs", "тариф", "цена",
    "цены", "стоимость", "сколько стоит", "free tier", "rate limit",
    "лимит", "квот", "quota", "per month", "в месяц", "лимиты", "cost",
    "how much",
)
_NEWS = (
    "release", "released", "релиз", "вышла", "вышел", "выходит",
    "announcement", "анонс", "changelog", "news", "новости", "обновлени",
    "update", "what's new", "поступление",
)
_DOCS = (
    "docs", "documentation", "документаци", "api", "github", "pypi",
    "pip install", "reference", "manual", "library", "библиотек", "example",
    "пример", "sap note", "readthedocs",
)
# явное намерение искать проект/репозиторий — идём в нативный gh (free).
# «library/библиотек» намеренно НЕ тут: «python library api docs» — это docs.
_GITHUB = (
    "github", "репозитор", "repo", "opensource", "open source",
)
_RESEARCH = (
    "vs", "versus", "best practices", "comparison", "сравнени", "обзор",
    "alternatives", "альтернатив", "how to choose", "как выбрать",
    "benchmark", "review", "лучшие", "best way", "patterns", "паттерн",
)


def is_ru(query: str) -> bool:
    return bool(_CYR.search(query))


def _matches(query_lower: str, words: tuple) -> bool:
    """Word-boundary matching so 'hang' doesn't fire inside 'changelog'."""
    for w in words:
        if re.search(rf"(?<!\w){re.escape(w)}(?!\w)", query_lower):
            return True
    return False


def detect(query: str, freshness: str | None = None) -> tuple[str | None, str]:
    """Classify by keyword priority: debug -> fact -> news -> github -> ru ->
    docs -> research (github before ru: «найди github репозиторий…» — github)."""
    q = query.lower()
    if _matches(q, _DEBUG):
        return "debug", "error-ish keyword"
    if _matches(q, _FACT):
        return "fact", "pricing/limit keyword"
    if freshness or _matches(q, _NEWS):
        return "news", "freshness flag / release keyword"
    if _matches(q, _GITHUB):
        return "github", "repo-search keyword"
    if is_ru(query):
        return "ru", "cyrillic query"
    if _matches(q, _DOCS):
        return "docs", "docs-ish keyword"
    if _matches(q, _RESEARCH):
        return "research", "vs/comparison keyword"
    return None, "no signal"


def resolve(query: str, freshness: str | None = None,
            forced: str | None = None) -> tuple[str | None, str, str]:
    """Merge the --intent flag with autodetection into the final routing key."""
    if forced:
        if forced == "news":
            key = "news-ru" if is_ru(query) else "news-en"
        else:
            key = forced
        return key, "flag", "explicit --intent"
    key, reason = detect(query, freshness)
    if key == "news":
        key = "news-ru" if is_ru(query) else "news-en"
    source = "auto" if key else "none"
    return key, source, reason
