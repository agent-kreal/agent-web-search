"""Контракт local-extract <-> wsearch stdlib-обёртка.

stdout — ровно один JSON-объект:
  ok:   {"ok": true,  "url", "title", "content", "tier", "status", "elapsed_ms", "trace"}
  fail: {"ok": false, "reason", "note", "url", "elapsed_ms", "trace"}
        reason in blocked | extract_failed | network | timeout | unsupported

exit-коды: 0 ok | 1 crash (traceback в stderr) | 2 usage | 3 clean fail
(3 = «локально не вышло», wsearch фолбэчит на сервисных провайдеров).
"""

from __future__ import annotations

EXIT_OK = 0
EXIT_CRASH = 1
EXIT_USAGE = 2
EXIT_FAIL = 3


def outcome_ok(url: str, title: str, content: str, tier: str,
               status: int, elapsed_ms: int, trace: list) -> dict:
    return {
        "ok": True,
        "url": url,
        "title": title,
        "content": content,
        "tier": tier,
        "status": status,
        "elapsed_ms": elapsed_ms,
        "trace": trace,
    }


def outcome_fail(reason: str, url: str, elapsed_ms: int, trace: list,
                 note: str = "") -> dict:
    return {
        "ok": False,
        "reason": reason,
        "note": note,
        "url": url,
        "elapsed_ms": elapsed_ms,
        "trace": trace,
    }
