"""Локальный каскад fetch: subprocess к local-extract (uv-проект:
httpx+trafilatura -> curl_cffi -> playwright). Всегда первый в FETCH_CHAIN.

Контракт (local-extract/src/local_extract/protocol.py): один JSON на stdout,
exit 0 ok / 1-2 crash / 3 clean fail. Обёртка гарантирует, что наружу выходит
ТОЛЬКО ProviderError — любое другое исключение уронило бы всю цепочку
(роутер фолбэчит исключительно по ProviderError).

max_chars здесь игнорируется: каскад всегда тянет до CONTENT_CAP, финальное
усечение делает router.fetch (развязка с кэшем: в кэше лежит полная копия,
--max-chars применяется при выдаче)."""

from __future__ import annotations

import json
import os
import subprocess

from .base import FetchResult, Provider, ProviderError, QuotaSpec

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VENV_PY = os.path.join(_PROJECT_ROOT, "local-extract", ".venv", "bin", "python")
CONTENT_CAP = 32768
SUBPROCESS_TIMEOUT = 65          # внутренний бюджет каскада 55 c + импорты

_SETUP_HINT = ("local-extract venv not found — "
               "cd local-extract && uv sync && uv run playwright install chromium")


class LocalProvider(Provider):
    name = "local"
    # алиасы для --provider: форс конкретной ступени каскада
    aliases = {"local-http": "http", "local-curl": "curl", "local-browser": "browser"}
    quota = QuotaSpec(limit=None, period="none", label="free, local cascade")
    can_fetch = True
    forced_tier = None           # ставится роутером при брони по алиасу

    def __init__(self):
        if os.environ.get("LOCAL_EXTRACT_DISABLE"):
            self.available_reason = "disabled via LOCAL_EXTRACT_DISABLE"
        elif not os.path.exists(VENV_PY):
            self.available_reason = _SETUP_HINT

    def fetch(self, url: str, *, max_chars: int = 6000) -> FetchResult:
        cmd = [VENV_PY, "-m", "local_extract", url,
               "--max-chars", str(CONTENT_CAP), "--tier", "auto"]
        if self.forced_tier:
            cmd[-1] = self.forced_tier
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        try:
            proc = subprocess.run(cmd, capture_output=True,
                                  timeout=SUBPROCESS_TIMEOUT, env=env)
        except subprocess.TimeoutExpired:
            raise ProviderError(f"local: timeout after {SUBPROCESS_TIMEOUT}s") from None
        except FileNotFoundError:
            raise ProviderError("local: venv python missing") from None
        except OSError as e:
            raise ProviderError(f"local: subprocess error: {e}") from None

        try:
            out = json.loads(proc.stdout.decode("utf-8", "replace"))
        except (json.JSONDecodeError, UnicodeDecodeError, TypeError):
            raise ProviderError(
                f"local: bad subprocess output rc={proc.returncode}: "
                f"{proc.stdout[:120]!r}") from None

        if out.get("ok"):
            return FetchResult(url=out.get("url") or url,
                               title=out.get("title") or "",
                               content=out.get("content") or "",
                               provider=f"local-{out.get('tier', 'http')}")
        # clean fail (rc 3) или неожиданная структура — фолбэк на сервисы
        reason = out.get("reason") or f"crashed rc={proc.returncode}"
        note = out.get("note") or ""
        tail = "; ".join(
            f"{s.get('tier')}: {s.get('verdict') or s.get('error', '')}"
            for s in (out.get("trace") or [])[-3:])
        msg = f"local: {reason}" + (f"/{note}" if note else "")
        if tail:
            msg += f" [{tail}]"
        raise ProviderError(msg)
