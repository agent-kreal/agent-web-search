"""RRF-слияние fan-out выдач multi (фаза 4.1, 2026-10-19).

До фазы 4 multi конкатенировал выдачи запросов в порядке завершения
потоков и дедуплицировал по URL — ранг результата = случайность таймингов.
Теперь итоговый ранг = Reciprocal Rank Fusion по всем спискам
(запрос × провайдер): score(u) = sum 1/(RRF_K + rank).

Канон нормализации URL и RRF живёт здесь; bench/run_union.py (v2-протокол
судейства) импортирует отсюда, чтобы бенч и CLI не разъезжались.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List

RRF_K = 60

# (?:^|[?&]): partition уже съел "?" — без ^ первый параметр-utm не
# вырезался (баг, наследованный из bench/run_union.py; поймано тестами 4.1).
# Хвостовой [&] забирает разделитель за вырезанным параметром.
_UTM = re.compile(r"(?:^|[?&])(utm_[a-z]+|fbclid|gclid|yclid|_ga[^=&]*)=[^&]*&?", re.I)


def norm_url(u: str) -> str:
    """Лёгкая нормализация для дедупа: убрать трекинг-параметры и фрагмент,
    lowercase хост, слэш в конце. Не трогает путь/регистр после хоста."""
    u = u.strip()
    u = u.split("#", 1)[0]
    pre, _, rest = u.partition("?")
    rest = _UTM.sub("", rest).strip("&")
    u = pre + ("?" + rest if rest else "")
    if "://" in u:
        scheme, _, tail = u.partition("://")
        host, _, path = tail.partition("/")
        u = f"{scheme}://{host.lower()}" + (f"/{path}" if path else "")
    return u


@dataclass
class MergedResult:
    url: str
    title: str = ""
    snippet: str = ""
    date: str | None = None
    provider: str = ""
    score: float = 0.0
    best_rank: int = 0            # лучший одиночный ранг (тай-брейк)
    sources: List[str] = field(default_factory=list)   # "запрос · провайдер"

    def to_dict(self) -> dict:
        d = {"url": self.url, "title": self.title, "snippet": self.snippet,
             "provider": self.provider, "queries": self.sources,
             "rrf": round(self.score, 5)}
        if self.date:
            d["date"] = self.date
        return d


def rrf_merge(ranked: List[List[dict]], source_names: List[str] | None = None
              ) -> List[MergedResult]:
    """Слияние проранжированных списков записей {url,title,snippet,date,
    provider} по RRF. Дубликаты схлопываются по norm_url: побеждает запись
    с лучшим рангом (title/snippet от неё), score и sources суммируются."""
    assert source_names is None or len(source_names) == len(ranked)
    cand: dict[str, MergedResult] = {}
    order: dict[str, int] = {}
    for li, items in enumerate(ranked):
        name = source_names[li] if source_names else str(li)
        for rank, it in enumerate(items, 1):
            key = norm_url(it.get("url", ""))
            if not key:
                continue
            c = cand.get(key)
            if c is None:
                c = MergedResult(url=it.get("url", ""), title=it.get("title", ""),
                                 snippet=it.get("snippet", ""),
                                 date=it.get("date"),
                                 provider=it.get("provider", ""),
                                 best_rank=rank)
                cand[key] = c
                order[key] = len(order)
            elif rank < c.best_rank:
                # лучший ранг приносит свои title/snippet (сниппет сильного
                # запроса информативнее)
                c.title = it.get("title", "") or c.title
                c.snippet = it.get("snippet", "") or c.snippet
                c.date = it.get("date") or c.date
                c.best_rank = rank
            c.score += 1.0 / (RRF_K + rank)
            if name not in c.sources:
                c.sources.append(name)
    return sorted(cand.values(), key=lambda c: (-c.score, c.best_rank,
                                                order[norm_url(c.url)]))
