"""CLI: python -m local_extract <url> [--max-chars N] [--tier auto|http|curl|browser]
                            [--budget SECONDS]

Контракт: stdout — ровно один JSON (см. protocol.py), ошибки — stderr + exit 1.
Вызывается stdlib-обёрткой wsearch напрямую из .venv (без uv run).
"""

from __future__ import annotations

import argparse
import json
import logging
import sys

# Глушим сторонний logging ДО импорта тиров: stdout обязан быть чистым.
logging.disable(logging.WARNING)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="local_extract",
        description="Local fetch+extract cascade (httpx+trafilatura -> curl_cffi -> playwright)")
    ap.add_argument("url", help="URL to fetch")
    ap.add_argument("--max-chars", type=int, default=32768)
    ap.add_argument("--tier", choices=["auto", "http", "curl", "browser"],
                    default="auto")
    ap.add_argument("--budget", type=float, default=55.0,
                    help="total seconds for the whole cascade")
    a = ap.parse_args(argv)

    from .cascade import run
    outcome, code = run(a.url, tier=a.tier, max_chars=a.max_chars,
                        budget_s=a.budget)
    print(json.dumps(outcome, ensure_ascii=False))
    return code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception:
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
