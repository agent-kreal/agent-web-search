"""Инжекшн-санитайзер fetch-контента (фаза 2, план 2026-10-19; BrowseSafe).

Веб-контент = untrusted: найденные инъекции промптов не должны молча
попадать в контекст агента. Двухуровневая политика (hybrid detection из
BrowseSafe, но без модели — эвристиками):

  REMOVE — почти никогда не легитимные в контенте страницы артефакты:
    - hidden-HTML (display:none / visibility:hidden / font-size:0) с текстом;
    - data-instructions/prompt/system-подобные атрибуты;
    - HTML-комментарии с instruction-лексикой;
    - delimiter-инъекции (--- END OF CONTEXT --- и т.п.);
    - chat-маркеры SYSTEM: / ASSISTANT: / <|im_start|> в начале строки.

  FLAG — спорные (легитимны в статьях про промптинг/безопасность), не
    вырезаются, но попадают в предупреждение: ignore/disregard/forget-
    instructions, «You are now», стелс («Standard procedure requires»,
    «Note to AI»), exfiltration-фразы с URL.

Code-fence блоки (```…```) не сканируются вообще: примеры инъекций в
статьях и доке — легитимный контент (hard negatives из BrowseSafe).

Вызов: sanitize(content) -> (content, findings[{kind, action, evidence}]).
Интеграция — router._issue_content (до prefilter/truncate); кэш хранит
исходник. Выключатель — env WS_SANITIZE=0 (санитайзер и обёртка off).
"""
from __future__ import annotations

import re

# ---------- REMOVE-паттерны (высокая уверенность) ----------

# hidden-элемент с содержимым: <tag ... style="...display:none...">text</tag>
_HIDDEN_HTML = re.compile(
    r"<(span|div|p|section|article|h[1-6]|small|label)\b[^>]*"
    r"style=\"[^\"]*(?:display\s*:\s*none|visibility\s*:\s*hidden"
    r"|font-size\s*:\s*0(?:px)?|opacity\s*:\s*0(?:\.0+)?)[^\"]*\"[^>]*>"
    r".*?</\1\s*>", re.I | re.S)

# data-атрибуты с инструкциями + закрывающий тег (вырезаем элемент целиком)
_DATA_ATTR_EL = re.compile(
    r"<(span|div|p|section)\b[^>]*\bdata-(?:instructions?|prompt|system"
    r"|ai-?message|assistant)[^>]*>.*?</\1\s*>", re.I | re.S)

# HTML-комментарий с instruction-лексикой
_HTML_COMMENT_INSTR = re.compile(
    r"<!--.*?(?:ignore|instructions?|system\s+prompt|assistant|you\s+must"
    r"|ai\s+(?:model|assistant)|disregard|override).*?-->", re.I | re.S)

# delimiter-инъекция: строка из дефисов/равенств + END/BEGIN OF CONTEXT/...
_DELIMITER_LINE = re.compile(
    r"^[=\-*_~#]{3,}\s*(?:END|BEGIN|STOP)\s+(?:OF\s+)?"
    r"(?:CONTEXT|RESULTS?|OUTPUT|DOCUMENT|CONTENT|INSTRUCTIONS?|SYSTEM"
    r"|PROMPT|RESPONSE|MESSAGE)[^\n]*$", re.I | re.M)

# chat-маркеры в начале строки (SYSTEM:/ASSISTANT: почти не легитимны
# в контенте страницы; USER: бывает в форумах — его не трогаем)
_CHAT_MARKER = re.compile(r"^(?:SYSTEM|ASSISTANT)\s*:[^\n]*$", re.I | re.M)
_CHAT_TAG = re.compile(r"<\|(?:im_start|im_end|system|assistant)\|>[^\n]*", re.I)

# ---------- FLAG-паттерны (спорные: бывает легитимным контентом) ----------

_FLAG_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("override", re.compile(
        r"\b(?:ignore|disregard|forget)\b[^.\n]{0,50}\b"
        r"(?:instructions?|prompts?|rules?|context|training|directions)\b", re.I)),
    # RU-инъекции: «забудь/игнорируй предыдущие инструкции/указания/правила»
    ("override", re.compile(
        r"\b(?:игнор|забуд|отмен|пропуст|пренебрег)\w*[^.\n]{0,60}\b"
        r"(?:инструк|указан|правил|контекст|наставлен|установк)\w*", re.I)),
    ("override", re.compile(
        r"\b(?:new|updated|revised)\s+instructions?\s*:", re.I)),
    ("persona", re.compile(
        r"\byou\s+are\s+now\b[^.\n]{0,60}", re.I)),
    ("persona", re.compile(
        r"\b(?:act|pretend)\s+as\s+(?:if\s+you\s+were\s+)?(?:a|an|the)\b[^.\n]{0,50}", re.I)),
    ("stealth", re.compile(
        r"\b(?:standard\s+procedure\s+requires|note\s+to\s+(?:the\s+)?(?:ai|assistant|llm|model)"
        r"|dear\s+(?:ai|assistant|chatbot|language\s+model)"
        r"|if\s+you\s+are\s+an?\s+(?:ai|assistant|language\s+model|llm)\b"
        r"|as\s+per\s+(?:our|the)\s+(?:guidelines|instructions)\b)", re.I)),
    ("exfiltrate", re.compile(
        r"\b(?:send|transmit|exfiltrate|post|upload|share)\b[^.\n]{0,60}"
        r"\b(?:data|context|conversation|instructions|content|text)\b[^.\n]{0,80}"
        r"https?://", re.I)),
    ("override", re.compile(
        r"\b(?:obey|follow|comply\s+with)\b[^.\n]{0,40}\b(?:new|these|my|the\s+above)\b"
        r"[^.\n]{0,30}\b(?:instructions?|rules?|directives?)\b", re.I)),
]


def _split_fences(content: str) -> list[tuple[str, bool]]:
    """[(сегмент, is_fence)] — фенсы не сканируем."""
    parts = re.split(r"(^```.*?^```)$", content, flags=re.M | re.S)
    return [(p, i % 2 == 1) for i, p in enumerate(parts)]


def sanitize(content: str) -> tuple[str, list[dict]]:
    """Возвращает (контент, findings). REMOVE-паттерны вырезаются, FLAG — нет."""
    findings: list[dict] = []
    if not content:
        return content, findings

    out: list[str] = []
    for seg, is_fence in _split_fences(content):
        if is_fence:
            out.append(seg)
            continue
        for name, pat in (("hidden_html", _HIDDEN_HTML),
                          ("data_attr", _DATA_ATTR_EL),
                          ("html_comment", _HTML_COMMENT_INSTR)):
            for m in pat.finditer(seg):
                findings.append({"kind": name, "action": "remove",
                                 "evidence": m.group(0)[:120]})
            seg = pat.sub("", seg)
        for name, pat in (("delimiter", _DELIMITER_LINE),
                          ("chat_marker", _CHAT_MARKER),
                          ("chat_tag", _CHAT_TAG)):
            def _rm(m: re.Match, _n=name) -> None:
                findings.append({"kind": _n, "action": "remove",
                                 "evidence": m.group(0)[:120]})
            for m in pat.finditer(seg):
                _rm(m)
            seg = pat.sub("", seg)
        for kind, pat in _FLAG_PATTERNS:
            for m in pat.finditer(seg):
                findings.append({"kind": kind, "action": "flag",
                                 "evidence": m.group(0)[:120]})
        out.append(seg)

    cleaned = "".join(out)
    if findings:
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned, findings


def untrusted_wrap(url: str, content: str) -> str:
    """Обёртка Trust Boundary (BrowseSafe): плоские маркеры без дефисов,
    чтобы не конфликтовать с delimiter-инжекциями страниц."""
    return (f"<<<UNTRUSTED WEB CONTENT: {url}>>>\n{content}"
            f"<<<END UNTRUSTED WEB CONTENT>>>")
