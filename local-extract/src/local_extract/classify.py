"""Эвристики классификации ответа: антибот-блок vs JS-пустышка vs hydration.
Чистые функции по bytes (маркеры ASCII, кириллица не мешает) — тестируются без сети.
"""

from __future__ import annotations

import json
import re
from typing import Optional

# Статусы, которые почти всегда = антибот/IP-фильтр (не «страница не нашлась» —
# 404 оставляем как честный ответ с телом).
_BLOCK_STATUSES = {401, 403, 429, 503}

_CHALLENGE_MARKERS = (
    "just a moment", "attention required", "cf-chl", "cf_chl",
    "checking your browser", "verify you are human", "unusual traffic",
    "request blocked", "access denied", "ddos protection", "sucuri",
    "captcha-delivery", "px-captcha",
)

# Пустые SPA-контейнеры при наличии скриптов.
_SHELL_RE = re.compile(
    r'<div[^>]+id="(?:root|app|__next|___gatsby)"[^>]*>\s*</div>', re.I)
_HAS_SCRIPTS_RE = re.compile(r"<script", re.I)
_HAS_CONTENT_RE = re.compile(r"<(?:article|h1|main)[\s>]", re.I)
_TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)

# Hydration-пейлоады: контент уже в HTML, браузер не нужен.
_NEXT_DATA_RE = re.compile(
    r'<script[^>]+id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.S)
_STATE_RES = (
    re.compile(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});\s*</script>', re.S),
    re.compile(r'window\.__APOLLO_STATE__\s*=\s*(\{.*?\});\s*</script>', re.S),
)


def _text(body: bytes, limit: int = 200_000) -> str:
    return body[:limit].decode("utf-8", "replace").lower()


def has_scripts(body: bytes) -> bool:
    return bool(_HAS_SCRIPTS_RE.search(_text(body, 50_000)))


def title_of(body: bytes) -> str:
    m = _TITLE_RE.search(body[:100_000].decode("utf-8", "replace"))
    return m.group(1).strip()[:300] if m else ""


def is_block(status: int, body: bytes) -> bool:
    """Антибот-блок: статус-код или маркер челленджа в теле."""
    if status in _BLOCK_STATUSES:
        return True
    t = _text(body)
    return any(m in t for m in _CHALLENGE_MARKERS)


def is_js_shell(body: bytes) -> bool:
    """SPA-пустышка: пустые корневые контейнеры (или noscript-просьба включить
    JS) при наличии скриптов и отсутствии article/h1/main."""
    t = _text(body)
    if _HAS_CONTENT_RE.search(t):
        return False
    if not _HAS_SCRIPTS_RE.search(t):
        return False
    return bool(_SHELL_RE.search(t)) or "enable javascript" in t


def _collect_text(node, out: list, min_len: int = 80) -> None:
    """Рекурсивный сбор «текстоподобных» строк из разобранного JSON."""
    if isinstance(node, dict):
        for v in node.values():
            _collect_text(v, out, min_len)
    elif isinstance(node, list):
        for v in node:
            _collect_text(v, out, min_len)
    elif isinstance(node, str):
        s = node.strip()
        if len(s) < min_len:
            return
        # отбрасываем css/base64/url/разметку: это строки без естественных пробелов
        # или начинающиеся с типовых артефактов
        if s.startswith((".", "#", "@", "data:", "http", "/", "<!")):
            return
        if s.count("{") + s.count("}") > 4:
            return
        if " " not in s:        # слитные токены — не текст
            return
        out.append(s)


def hydration_payload(body: bytes) -> Optional[str]:
    """Достать готовый контент из __NEXT_DATA__ / __INITIAL_STATE__ без браузера.
    -> склеенный текст (>= MIN строк) или None (брать нечего)."""
    raw = body[:2_000_000].decode("utf-8", "replace")
    candidates = _NEXT_DATA_RE.findall(raw)
    for rx in _STATE_RES:
        candidates.extend(rx.findall(raw))
    chunks: list = []
    for c in candidates:
        try:
            data = json.loads(c)
        except Exception:
            continue
        _collect_text(data, chunks)
    if not chunks:
        return None
    text = "\n\n".join(chunks)
    return text if len(text) >= 200 else None
