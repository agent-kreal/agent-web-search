"""Local quota ledger: spend BEFORE the 429, not after.

state/quotas.json keeps per-provider counters:
    { "brave": {"used": 12, "window_start": "2026-08-01", ...},
      "zai":   {"exhausted_until": "2026-09-18T16:28:19", ...} }

- periodic quotas (day/month) roll over automatically
- `exhausted_until` set from a real 429/limit response (e.g. Z.ai tells us
  the reset timestamp) makes the router skip the provider for free
- unknown-quota keyless providers are not counted (nothing to count)
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

STATE_DIR = Path(__file__).resolve().parent.parent / "state"
STATE_FILE = STATE_DIR / "quotas.json"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _load() -> dict:
    try:
        return json.loads(STATE_FILE.read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def _save(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def _window_start(period: str, now: datetime) -> str:
    if period == "day":
        return now.strftime("%Y-%m-%d")
    if period == "month":
        return now.strftime("%Y-%m")
    return now.strftime("%Y-%m-%d")  # `once` windows never roll


def get_entry(provider: str) -> dict:
    return _load().get(provider, {})


def is_exhausted(provider: str) -> Optional[str]:
    """Return a human reason if provider should be skipped, else None."""
    e = get_entry(provider)
    until = e.get("exhausted_until")
    if until:
        try:
            if _now() < datetime.fromisoformat(until):
                return f"exhausted until {until}"
        except ValueError:
            pass
    return None


def remaining(provider: str, limit: Optional[int], period: str) -> Optional[int]:
    if limit is None:
        return None
    e = get_entry(provider)
    if e.get("window_start") != _window_start(period, _now()):
        return limit  # window rolled — full quota back
    return max(0, limit - int(e.get("used", 0)))


def spend(provider: str, count: int = 1, period: str = "none") -> None:
    state = _load()
    e = state.get(provider, {})
    ws = _window_start(period, _now())
    if e.get("window_start") != ws:
        e = {"window_start": ws, "used": 0}
    e["used"] = int(e.get("used", 0)) + count
    e["updated"] = _now().isoformat(timespec="seconds")
    state[provider] = e
    _save(state)


def mark_exhausted(provider: str, until: Optional[str] = None, period: str = "none") -> None:
    """Called on a real 429/limit error. `until` = ISO timestamp if the
    provider told us; else derive from the period; else 1 hour cooldown."""
    state = _load()
    e = state.get(provider, {})
    if until:
        try:
            ts = datetime.fromisoformat(until)
        except ValueError:
            ts = None
    else:
        now = _now()
        if period == "day":
            ts = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "month":
            ts = (now + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            ts = now + timedelta(hours=1)
    if ts:
        e["exhausted_until"] = ts.astimezone(timezone.utc).isoformat(timespec="seconds")
    e["exhausted_marked"] = _now().isoformat(timespec="seconds")
    state[provider] = e
    _save(state)


def status_line(provider: str, limit: Optional[int], period: str, label: str) -> str:
    reason = is_exhausted(provider)
    if reason:
        return reason
    rem = remaining(provider, limit, period)
    if rem is None:
        return label or "no known limit (keyless)"
    return f"{rem} left{(' per ' + period) if period in ('day', 'month') else ''}"


def reset(provider: Optional[str] = None) -> None:
    state = _load()
    if provider:
        state.pop(provider, None)
    else:
        state = {}
    _save(state)
