"""Fetch result cache: повторное чтение того же URL — мгновенно и бесплатно.

state/fetch_cache.json: {norm_url: {"url", "provider", "title", "content",
                                    "fetched_at", "expires_at"}}

- кэшируются только успехи; TTL 30 мин
- ключ — нормализованный URL (lowercase host, без fragment и трекинг-параметров,
  отсортированный query), оригинальный URL живёт в записи
- eviction при каждом save: просроченные, затем самые старые до <= MAX_ENTRIES
- threading.Lock: gather гоняет 4 потока в одном процессе; два параллельных
  wsearch-процесса — last-write-wins (та же модель, что у quotas.py)
"""

from __future__ import annotations

import json
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

STATE_DIR = Path(__file__).resolve().parent.parent / "state"
CACHE_FILE = STATE_DIR / "fetch_cache.json"

TTL_MINUTES = 30
MAX_ENTRIES = 200
MAX_CONTENT = 32768            # синхронно с local.py CONTENT_CAP

_LOCK = threading.Lock()

# трекинг-параметры, не влияющие на контент
_TRACKING_PREFIXES = ("utm_", "fbclid", "gclid", "yclid", "igshid", "mc_", "ref")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def norm_key(url: str) -> str:
    try:
        parts = urlsplit(url.strip())
    except ValueError:
        return url
    scheme = parts.scheme.lower()
    host = (parts.hostname or "").lower()
    if not host:
        return url
    port = parts.port
    default_port = (scheme == "https" and port == 443) or (scheme == "http" and port == 80)
    netloc = host if (port is None or default_port) else f"{host}:{port}"
    q = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
         if not any(k.lower().startswith(p) for p in _TRACKING_PREFIXES)]
    q.sort()
    return urlunsplit((scheme, netloc, parts.path or "/", urlencode(q), ""))


def _load() -> dict:
    try:
        return json.loads(CACHE_FILE.read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def _save(cache: dict) -> None:
    # eviction: просроченные, затем самые старые до лимита
    now = _now()
    fresh = {}
    for k, v in cache.items():
        try:
            if datetime.fromisoformat(v.get("expires_at", "")) > now:
                fresh[k] = v
        except ValueError:
            continue
    if len(fresh) > MAX_ENTRIES:
        ordered = sorted(fresh.items(), key=lambda kv: kv[1].get("fetched_at", ""))
        fresh = dict(ordered[-MAX_ENTRIES:])
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(fresh, indent=2, ensure_ascii=False))


def get(url: str) -> Optional[dict]:
    """-> запись кэша или None (просрочено/нет)."""
    with _LOCK:
        entry = _load().get(norm_key(url))
    if not entry:
        return None
    try:
        if datetime.fromisoformat(entry.get("expires_at", "")) <= _now():
            return None
    except ValueError:
        return None
    return entry


def put(url: str, *, provider: str, title: str, content: str) -> None:
    if not content:
        return
    with _LOCK:
        cache = _load()
        cache[norm_key(url)] = {
            "url": url,
            "provider": provider,
            "title": title or "",
            "content": content[:MAX_CONTENT],
            "fetched_at": _now().isoformat(timespec="seconds"),
            "expires_at": (_now() + timedelta(minutes=TTL_MINUTES)).isoformat(timespec="seconds"),
        }
        _save(cache)


def clear() -> None:
    with _LOCK:
        _save({})
