"""Категорийный prefilter fetch-контента (фаза 1.2, план 2026-10-19).

Выкидывает УВЕРЕННЫЙ мусор до усечения (Perplexity query-aware compression:
UI&nav −58%, metadata −46%, ads −43% — но у нас без модели, эвристиками).
Консервативность важнее полноты: лучше оставить строку меню, чем вырезать
контент. Code-fence блоки не трогаем вообще.

Категории (таксономия Perplexity-джаджа):
  ui_nav   : 3+ подряд строк-ссылок на якоря (inline-TOC), хлебные крошки;
  metadata : копирайты, cookie/privacy строки, share/follow-строки;
  ads      : newsletter-CTA / subscribe-строки.

Вызов: strip_junk(content) -> (content, stats). Интеграция — в router.fetch
на выдаче (кэш хранит исходник), вместе со smart_truncate.
"""
from __future__ import annotations

import re

# строка-ссылка на якорь этого же документа: [-] [Text](#anchor)
_ANCHOR_LINE = re.compile(r"^\s*(?:[-*+]\s*)?\[[^\]]{1,80}\]\(#[^)]{1,120}\)\s*$")
# хлебная крошка: 2+ ссылок с разделителями › / > · | между ними, строка короткая
_BREADCRUMB = re.compile(
    r"^\s*(?:\[([^\]]{1,60})\]\([^)#]{1,120}\)|[A-Za-zА-Яа-яЁё0-9 .&-]{1,40})"
    r"(?:\s*(?:›|>|/|·|\|)\s*\[[^\]]{1,60}\]\([^)#]{1,120}\)){1,5}\s*$")
# метаданные/CTA: строка ЦЕЛИКОМ из этого (короткая, без другого текста)
_JUNK_LINE = re.compile(
    r"^\s*(?:"
    r"(?:all\s+rights\s+reserved|copyright\s*©?\s*\d{2,4}.*|©\s*\d{2,4}.*|\(c\)\s*\d{2,4}.*)"
    r"|(?:share\s+(?:this|on|article)\b.{0,60})"
    r"|(?:follow\s+(?:us|on)\b.{0,60})"
    r"|(?:subscribe(?:\s+to\s+our\s+newsletter)?[!.]?)"
    r"|(?:sign\s+up\s+for\s+our\s+newsletter[!.]?)"
    r"|(?:cookie\s+(?:settings|preferences|policy)\b.{0,60})"
    r"|(?:we\s+use\s+cookies\b.{0,80})"
    r"|(?:accept\s+(?:all\s+)?cookies\b.{0,40})"
    r"|(?:privacy\s+policy|terms\s+of\s+(?:service|use)|cookie\s+policy)\s*[|·/]\s*"
    r"(?:privacy\s+policy|terms\s+of\s+(?:service|use)|cookie\s+policy)"
    r")\s*[.!]?\s*$", re.I)
# строка только из соцсетей-ссылок (2+), короткая
_SOCIAL_ROW = re.compile(
    r"^\s*(?:\[[^\]]{0,40}\]\((?:https?://)?(?:www\.)?"
    r"(?:twitter|x|linkedin|facebook|t\.me|instagram|youtube|github)\.com[^)]{0,80}\)"
    r"\s*[|·/]?\s*){2,}\s*$", re.I)

NAV_RUN_MIN = 3          # якорные ссылки подряд: минимум для уверенности
PROTECT_FENCE = True


def _strip_line_junk(line: str, stats: dict) -> str:
    if _JUNK_LINE.match(line):
        stats["metadata"] += 1
        return ""
    if _SOCIAL_ROW.match(line):
        stats["ads"] += 1
        return ""
    return line


def strip_junk(content: str) -> tuple[str, dict]:
    """(контент без уверенного мусора, {ui_nav, metadata, ads, chars_removed})."""
    stats = {"ui_nav": 0, "metadata": 0, "ads": 0, "chars_removed": 0}
    if not content:
        return content, stats

    # code-fence защита: обрабатываем только сегменты вне ``` блоков
    segments = re.split(r"(^```.*?^```)$", content, flags=re.M | re.S)

    out_parts: list[str] = []
    for idx, seg in enumerate(segments):
        if idx % 2 == 1:                      # сам fence-блок
            out_parts.append(seg)
            continue
        lines = seg.split("\n")

        # 1) прогонянем по строкам: якорные ран-блоки
        res: list[str] = []
        i = 0
        while i < len(lines):
            if _ANCHOR_LINE.match(lines[i]):
                j = i
                while j < len(lines) and _ANCHOR_LINE.match(lines[j]):
                    j += 1
                if j - i >= NAV_RUN_MIN:
                    stats["ui_nav"] += j - i
                    i = j                    # выкинуть блок якорных ссылок
                    continue
            res.append(lines[i])
            i += 1

        # 2) построчные метаданные/CTA
        res = [_strip_line_junk(l, stats) for l in res]

        # 3) хлебные крошки
        res = ["" if (_BREADCRUMB.match(l) and "]" in l) else l for l in res]

        out_parts.append("\n".join(res))

    out = "".join(out_parts)
    # схлопнуть дыры от вырезанного (2+ пустых строк -> 2)
    out = re.sub(r"\n{3,}", "\n\n", out)
    stats["chars_removed"] = len(content) - len(out)
    return out, stats
