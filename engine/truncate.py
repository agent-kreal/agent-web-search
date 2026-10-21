"""Умная резка fetch-контента по границам (фаза 1.1, план 2026-10-19).

Заменяет тупое content[:max_chars] в router.fetch: обрез не посреди
слова/предложения/JSON-значения, а на ближайшей границе в окне отката.
Baseline-мотивация: замер 19.10 (measure_cut.py) — доля выдач с хвостом
mid-token; цель фазы — довести её до ~0 на текстовых страницах.

Границы (walk назад от лимита, побеждает ближайшая к лимиту):
  - граница абзаца "\n\n";
  - конец предложения [.!?…] перед пробелом/переводом строки (+ закрывающие
    кавычки/скобки после знака);
  - строка markdown-структуры (заголовок #, пункт списка, строка таблицы,
    fence) — рез ПЕРЕД ней;
  - незакрытый code-fence ``` — рез по последней полной строке блока;
  - pretty-printed JSON — по последней полной строке.

Fallback: если в окне отката (15% лимита, min 200) границы нет — старый
тупой рез в limit: сохранить объём важнее идеальной границы (минифицированный
JSON, сплошной текст без точек). Флаг --raw-cut оставляет старое поведение
насовсем (эскейп-люк фазы 1.3).
"""
from __future__ import annotations

import re

# окно отката: граница ищется в [limit - backoff, limit]
MIN_BACKOFF = 200
BACKOFF_FRAC = 0.15

_SENT_END = ".!?…"
# NB: \] обязателен — класс собирается f-подстановкой в regex, иначе ]
# внутри строки закроет символьный класс раньше времени
_CLOSERS = "\"'»\\)"
# строка начинается со структурного markdown-маркера → резать перед ней
_STRUCT_LINE = re.compile(r"^(#{1,6} |- |\* |\d+\. |> |\| ```)", re.M)


def _limit_for_fence(content: str, limit: int) -> int | None:
    """Незакрытый code-fence вокруг точки limit → граница по строкам блока.

    Возвращает новый предел или None (fence не мешает). Считаем ``` до limit:
    нечётное число = мы внутри блока; тогда режем по последнему \\n внутри
    блока (полная строка кода), а если блок начался совсем рядом с limit —
    выкидываем fence целиком (незачем оставлять открытый огрызок).
    """
    head = content[:limit]
    fences = [m.start() for m in re.finditer(r"^```", head, re.M)]
    if len(fences) % 2 == 0:
        return None
    fence_open = fences[-1]
    if limit - fence_open > 80:          # блок уже длинный: рез по строке
        nl = head.rfind("\n", 0, limit)
        return nl + 1 if nl > fence_open else None
    prev_nl = head.rfind("\n", 0, fence_open)
    return prev_nl + 1 if prev_nl != -1 else fence_open  # выкинуть fence


def _limit_for_json(content: str, limit: int) -> int | None:
    """Pretty-printed JSON (строки с отступами): рез по границе строки."""
    stripped = content.lstrip()
    if not stripped[:1] in ("{", "["):
        return None
    head = content[:limit]
    nl = head.rfind("\n")
    if nl <= 0:
        return None
    # граница строки JSON: после запятой/скобки; не посреди ключа/значения
    before = head[:nl].rstrip()
    if before and before[-1] in ",{}[]\"":
        return nl + 1
    nl2 = head.rfind("\n", 0, nl)
    return nl2 + 1 if nl2 != -1 and head[:nl2].rstrip()[-1:] in ",{}[]\"" else None


def _limit_for_text(content: str, limit: int, backoff: int) -> int | None:
    """Текст: ближайшая к limit граница предложения/абзаца/структуры."""
    base = max(0, limit - backoff)
    window = content[base:limit]

    cands: list[int] = []

    # все границы абзацев в окне
    par = window.rfind("\n\n")
    if par != -1:
        cands.append(par + base + 2)

    # все концы предложений: [.!?…]["»')] перед \s
    for m in re.finditer(rf'[{_SENT_END}][{_CLOSERS}]*(?=\s)', window):
        cands.append(m.end() + base)

    # все структурные строки markdown — рез перед ними
    for m in _STRUCT_LINE.finditer(window):
        cands.append(m.start() + base)

    cands = sorted(c for c in cands if c > 0)
    if not cands:
        return None
    # граница, заканчивающаяся на ':' (повисшее «labels:» перед вырезанным
    # код-блоком/списком), — хуже нижеследующей чистой границы (spot-check 19.10)
    for c in reversed(cands):
        if content[c - 1] != ":":
            return c
    return cands[-1]


def smart_truncate(content: str, limit: int) -> str:
    """Обрезка content до <= limit по границе; fallback — тупой рез."""
    if limit <= 0 or len(content) <= limit:
        return content
    backoff = max(MIN_BACKOFF, int(limit * BACKOFF_FRAC))

    new_limit = (_limit_for_fence(content, limit)
                 or _limit_for_json(content, limit)
                 or _limit_for_text(content, limit, backoff))
    if new_limit is None or new_limit <= 0 or new_limit > limit:
        return content[:limit]                      # старое поведение
    out = content[:new_limit].rstrip() + "\n"
    # рез внутри code-fence: блок остаётся незакрытым → дописать закрывашку,
    # иначе markdown-рендер и парсеры downstream съедают весь хвост как код
    if out.count("```") % 2 == 1:
        out += "```\n"
    return out
