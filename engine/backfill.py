"""Adaptive backfill для multi (фаза 4.2, 2026-10-19; финальная редакция
после ревью 19.10 — только фейл-триггер).

Первоначальная редакция (покрытие термов + уникальные домены) срезана по
данным: на датасете multi триггеры не сработали ни разу, а принудительный
probe (runs/2026-10-19-phase4-probe) показал, что добор по «непокрытым
термам» генерирует шумовые запросы («deployment documentation», «vars
error fix») и портит топ: точность доборных URL 15%, P@10 0.64→0.40.
Оставлен единственный триггер без этого риска: если один из запросов
fan-out упал (провайдер лёг/квота) — доборный круг из 2 шаблонных
переформулировок по самому весомому терму фейл-запроса. Лимит 1 круг.
"""

from __future__ import annotations

import re
from collections import Counter

_STOP = frozenset("""
и или как что где когда зачем почему для про без под над все весь вся
this that with from what which where when how why the and for you your
com www ru org html http https vs
""".split())

_TOKEN = re.compile(r"[a-zа-яё0-9][a-zа-яё0-9_]*")


def key_terms(queries: list[str]) -> dict[str, int]:
    """Токен → сколько запросов его содержат (вес терма).

    Значимый токен: ≥2 символов (короткие имена инструментов — «uv» —
    осмысленны; однобуквенный мусор отсечён regex) и не стоп-слово."""
    per_q = [{t for t in _TOKEN.findall(q.lower()) if t not in _STOP}
             for q in queries]
    weight: Counter = Counter()
    for toks in per_q:
        weight.update(toks)
    return dict(weight)


def should_backfill(failed: list[str]) -> tuple[bool, str]:
    """(триггер, причина): фейл-запросы fan-out → доборный круг."""
    if failed:
        return True, f"failed_queries={len(failed)}"
    return False, ""


# шаблоны переформулировок по интенту (2 на круг — план «2–3», экономнее к
# квотам; X подставляется с исходным регистром из запроса)
_TEMPLATES = {
    "docs":     ["{X} documentation", "{X} examples"],
    "github":   ["{X} documentation", "{X} examples"],
    "research": ["{X} overview", "{X} comparison"],
    "fact":     ["what is {X}", "{X} explained"],
    "news-ru":  ["{X} последние новости", "{X} что известно"],
    "news-en":  ["{X} news", "{X} latest"],
    "ru":       ["{X} что это", "{X} документация примеры"],
    "debug":    ["{X} error fix", "{X} documentation"],
}
_DEFAULT_TEMPLATES = ["{X} documentation", "{X} examples"]

# слова-шаблоны бессмысленны как X («documentation documentation») —
# исключаются из кандидатов доборного терма
_TEMPLATE_WORDS = frozenset(
    "documentation documentation example examples overview comparison "
    "explained news latest документация пример примеры новости "
    "решение проблемы fix error what is это известно".split())


def backfill_queries(failed: list[str], intent: str | None) -> list[str]:
    """2 шаблонные переформулировки по самому весомному терму фейл-запросов.

    Терм ищется в исходном регистре (регистр из запроса — «RLS», не «rls» —
    важен для шаблона); при равных весах берётся специфичнее (длиннее):
    «handshake», не «error», из «ssl handshake error»."""
    ranked = sorted(key_terms(failed).items(),
                    key=lambda x: (-x[1], -len(x[0]), x[0]))
    meaningful = [t for t, _ in ranked if t not in _TEMPLATE_WORDS]
    terms = meaningful or [t for t, _ in ranked]
    if not terms:
        return []
    term = terms[0]
    orig = term
    for q in failed:
        found = None
        for m in re.finditer(r"[A-Za-zА-ЯЁа-яё0-9][A-Za-zА-ЯЁа-яё0-9_]*", q):
            if m.group(0).lower() == term:
                found = m.group(0)
                break
        if found:
            orig = found
            break
    templates = _TEMPLATES.get(intent or "", _DEFAULT_TEMPLATES)
    return [t.format(X=orig) for t in templates]
