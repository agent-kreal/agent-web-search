"""Единственное место, знающее API trafilatura (дрейф версий чинится здесь).

Вход — bytes: у trafilatura свой детект кодировки (isutf8 -> cchardet ->
charset_normalizer), передавать httpx.Response-объект нельзя (TypeError).
"""

from __future__ import annotations

import json
import re
from typing import Optional, Tuple

import trafilatura

# Порог «полезной» экстракции. extract() возвращает None только при полной
# пустоте; антибот-челлендж обычно даёт короткий мусор (rescue-каскад
# подмешивает baseline-текст), поэтому короткую выдачу считаем провалом.
MIN_TEXT = 200

_FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n?", re.S)


def _body_len(markdown: str) -> int:
    """Длина без YAML frontmatter (title/url/hostname ~70 служебных символов,
    которые иначе занижают порог и пропускают антибот-мусор)."""
    return len(_FRONTMATTER_RE.sub("", markdown).strip())


def extract_html(html: bytes, url: str) -> Tuple[Optional[str], str, int]:
    """-> (markdown | None, title, text_len). markdown is None = пусто."""
    try:
        doc = trafilatura.extract_with_metadata(
            html,
            url=url,
            output_format="markdown",   # include_formatting включается автоматически
            include_links=True,
            include_images=True,
            include_comments=False,
        )
    except Exception:
        return None, "", 0
    if doc is None:
        return None, "", 0
    text = doc.text or ""
    return text, doc.title or "", _body_len(text)


def extract_json(body: bytes) -> Tuple[str, str]:
    """JSON-ответ API -> текст для выдачи: pretty-print (LLM читает структуру),
    при кривом JSON — сырое тело как есть. Title у API нет."""
    text = body.decode("utf-8", "replace").strip()
    try:
        text = json.dumps(json.loads(text), ensure_ascii=False, indent=1)
    except ValueError:
        pass
    return text, ""
