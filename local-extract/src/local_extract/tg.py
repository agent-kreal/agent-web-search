"""Telegram web preview (t.me/s/<канал>) -> markdown.

Preview — статический HTML без JS (ту же страницу видит залогаут-браузер),
поэтому хватает http-тира каскада. Отдельный экстрактор, а не trafilatura:
вёрстка чата — не статья, trafilatura на ней стабильно даёт thin
(t.me — один из топ-доменов fetch агента).

Парсинг регекспами, а не html.parser: разметка машинно-генерированная и
стабильная годами (на неё опирается весь экосистемный скрейпинг — RSSHub
с 2019), блоки постов плоские, вложенных div внутри текста сообщения нет.
Чистый stdlib — модуль тестируется системным python без local-extract
venv; fixtures в web-search/tests/fixtures/tg_*.html.

Ограничения preview (осознанные): только публичные каналы с включённым
preview; нет реакций и комментариев; одна страница ~20 постов, пагинация
(?before=<id>) вне скоупа — это уже мониторинг, не разовое чтение ссылки.
"""

from __future__ import annotations

import html as htmllib
import re
from typing import List, Optional, Tuple
from urllib.parse import urlparse, urlunparse

TG_HOSTS = frozenset({"t.me", "telegram.me", "telegram.dog"})
# путь, ведущий в приватность: preview для него не существует by design
_INVITE_PATH_RE = re.compile(r"^/(?:\+[\w-]+|joinchat/)", re.I)


def is_tg_url(url: str) -> bool:
    try:
        return urlparse(url).netloc.lower() in TG_HOSTS
    except ValueError:
        return False


def is_invite_url(url: str) -> bool:
    try:
        parts = urlparse(url)
    except ValueError:
        return False
    return (parts.netloc.lower() in TG_HOSTS
            and bool(_INVITE_PATH_RE.match(parts.path)))


def normalize_url(url: str) -> str:
    """t.me/<канал>[/<id>] -> t.me/s/<канал>[/<id>]; алиасы домена -> t.me.

    Канал без /s/ — страница-приглашение без постов (классический источник thin).
    Query сохраняется (?before=<id> — постраничная навигация preview).
    Инвайт-ссылки и прочие пути (/settings, /share/url...) проходят как есть.
    Дубль этой логики живёт в engine/router.py (wsearch не может импортить
    local-extract — там subprocess-контракт); менять — синхронно в обоих.
    """
    try:
        parts = urlparse(url)
    except ValueError:
        return url
    if parts.netloc.lower() not in TG_HOSTS:
        return url
    path = parts.path or "/"
    if not _INVITE_PATH_RE.match(path):
        m = re.match(r"^/(?!s/)([^/]+)(/.*)?$", path)
        if m:
            path = f"/s{path}"
    return urlunparse((parts.scheme or "https", "t.me", path, "",
                       parts.query, ""))


# --- парсер -------------------------------------------------------------

_MEDIA_LABELS = (
    ("tgme_widget_message_photo", "📷 фото"),
    ("tgme_widget_message_video", "🎬 видео"),
    ("tgme_widget_message_roundvideo", "📹 видеосообщение"),
    ("tgme_widget_message_voice", "🎤 голосовое"),
    ("tgme_widget_message_sticker", "стикер"),
    ("tgme_widget_message_document", "📎 файл"),
    ("tgme_widget_message_poll", "📊 опрос"),
    ("tgme_widget_message_location", "📍 геометка"),
    ("tgme_widget_message_dice", "🎲"),
)

_WRAP_RE = re.compile(r'<div class="tgme_widget_message_wrap[^"]*"')
_POST_ID_RE = re.compile(r'data-post="([^"/]+/\d+)"')
_DATE_RE = re.compile(r'<time datetime="([^"]+)"')
_VIEWS_RE = re.compile(r'class="tgme_widget_message_views">([^<]*)<')
_TEXT_RE = re.compile(
    r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', re.S)
_SERVICE_RE = re.compile(r'class="tgme_widget_message[^"]*service_message')
_PREVIEW_RE = re.compile(
    r'<a class="tgme_widget_message_link_preview[^"]*"[^>]*href="([^"]+)"'
    r'[^>]*>(.*?)</a>', re.S)
_PV_FIELD_RES = {
    "site": re.compile(r'class="link_preview_site_name[^"]*"[^>]*>(.*?)</div>', re.S),
    "title": re.compile(r'class="link_preview_title[^"]*"[^>]*>(.*?)</div>', re.S),
    "desc": re.compile(r'class="link_preview_description[^"]*"[^>]*>(.*?)</div>', re.S),
}
_AUTHOR_RE = re.compile(r'class="tgme_widget_message_owner_name"[^>]*>(.*?)</a>', re.S)
_CONTACT_RE = re.compile(r"<title>Telegram: Contact @")


def _strip_tags(s: str) -> str:
    """Внутренности текста сообщения -> markdown: <br> в перенос, <a> в
    [текст](href), tg-emoji/прочие теги выкидываются (эмодзи живёт в <b>
    внутри i.emoji — CSS-спрайт с текстовым фолбэком)."""
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
               lambda m: f"[{_strip_tags(m.group(2))}]({m.group(1)})", s,
               flags=re.S)
    s = re.sub(r"<[^>]+>", "", s)
    return htmllib.unescape(s)


def _clean_inline(s: str) -> str:
    return htmllib.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def _fmt_date(iso: str) -> str:
    m = re.match(r"(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})", iso or "")
    return f"{m.group(1)} {m.group(2)} UTC" if m else (iso or "")[:16]


def extract(html: bytes, target_post: str = "") -> Tuple[Optional[str], str, int, str]:
    """HTML preview -> (markdown | None, title, n_posts, note).

    markdown None = постов нет; note объясняет, почему (contact-страница =
    канала нет/приватный, иначе пусто/выключен preview).
    target_post: 'канал/123' из URL — помечается в выдаче.
    """
    try:
        src = html.decode("utf-8", "replace")
    except Exception:
        return None, "", 0, "tg decode error"

    chunks = _WRAP_RE.split(src)[1:]          # [начало блока поста, ...]
    channel = ""
    author = ""
    posts: List[dict] = []
    for chunk in chunks:
        pid_m = _POST_ID_RE.search(chunk[:600])
        if not pid_m:
            continue                           # service-сообщения без data-post
        pid = pid_m.group(1)
        if not channel:
            channel = pid.split("/", 1)[0]
            a = _AUTHOR_RE.search(chunk)
            if a:
                author = _clean_inline(a.group(1))
        if _SERVICE_RE.search(chunk[:600]):
            continue                           # «Channel created» и прочие
        t = _TEXT_RE.search(chunk)
        text = _strip_tags(t.group(1)).strip() if t else ""
        media = [label for prefix, label in _MEDIA_LABELS
                 if f'class="{prefix}' in chunk]
        pv_parts: List[str] = []
        pv = _PREVIEW_RE.search(chunk)
        if pv:
            url, inner = pv.group(1), pv.group(2)
            fields = []
            for key in ("site", "title", "desc"):
                fm = _PV_FIELD_RES[key].search(inner)
                fields.append(_clean_inline(fm.group(1)) if fm else "")
            pv_parts = [p for p in (*fields, url) if p]
        if not (text or media or pv_parts):
            continue
        d = _DATE_RE.search(chunk)
        v = _VIEWS_RE.search(chunk)
        posts.append({"id": pid, "date": d.group(1) if d else "",
                      "views": v.group(1).strip() if v else "",
                      "text": text, "media": media, "preview": pv_parts})

    if not posts:
        if _CONTACT_RE.search(src[:4096]):
            return None, "", 0, "tg channel not found or private (contact page)"
        return None, "", 0, "tg preview has no posts (empty or disabled)"

    who = f"@{channel}" + (f" ({author})" if author else "")
    title = f"Telegram: {who} — {len(posts)} постов (web preview)"
    out = [f"# {title}", ""]
    for post in posts:
        meta = [post["id"], _fmt_date(post["date"])]
        if post["views"]:
            meta.append(f"{post['views']} views")
        if target_post and post["id"] == target_post:
            meta.append("← запрошенный пост")
        out.append("## " + " · ".join(m for m in meta if m))
        out.append("")
        if post["text"]:
            out.append(post["text"])
        if post["media"]:
            out.append("")
            out.append(" ".join(post["media"]))
        if post["preview"]:
            out.append("")
            out.append("→ " + " — ".join(post["preview"]))
        out.append("")
    return "\n".join(out).strip() + "\n", title, len(posts), ""
