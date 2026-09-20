"""Quota ledger: server truth first, local counter as fallback.

state/quotas.json keeps per-provider records (v2, hybrid):
    { "linkup": {
        "server": {"unit": "usd", "remaining": 19.415, "limit": 20.0,
                   "baseline_used": 44, "fetched_at": "2026-09-09T...", },
        "local":  {"window_start": "2026-09", "used": 44},
        "exhausted_until": null } }

Legacy v1 entries (flat {used, window_start, ...}) are read as `local`
on the fly; spend() rewrites them into v2.

Truth priority (episodes like exa-03.09 — a 429 hid a live balance —
must never repeat):
  1. server snapshot (quota endpoint / rate-limit headers), interpolated:
     remaining − local spend since `fetched_at` (baseline_used anchor)
  2. local request counter (v1 behaviour)
  3. `exhausted_until` from a real 429/limit response still skips first,
     but a fresh server snapshot with remaining > 0 clears it.

Snapshot freshness: <= SERVER_TTL (6h) is "fresh"; anything older than
SERVER_MAX_AGE (7d) is discarded (window may have rolled since) — between
the two the snapshot is used with interpolation and shown with its age.
When the local window rolls, the snapshot is dropped (its baseline points
into the previous window).
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

STATE_DIR = Path(__file__).resolve().parent.parent / "state"
STATE_FILE = STATE_DIR / "quotas.json"

SERVER_TTL = timedelta(hours=6)     # fetched recently -> shown as fresh
SERVER_MAX_AGE = timedelta(days=7)  # older -> ignore, local counter only


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


def _local(e: dict) -> dict:
    """Local-counter part of an entry. Legacy v1 entries are flat — build
    a COPY of the counter fields (spend() reattaches it under "local";
    aliasing `e` itself would create a self-reference)."""
    loc = e.get("local")
    if isinstance(loc, dict):
        return loc
    return {"window_start": e.get("window_start"),
            "used": int(e.get("used", 0) or 0)}


def _parse_ts(s: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def get_entry(provider: str) -> dict:
    return _load().get(provider, {})


def is_exhausted(provider: str) -> Optional[str]:
    """Return a human reason if provider should be skipped, else None."""
    e = get_entry(provider)
    until = e.get("exhausted_until")
    if until:
        ts = _parse_ts(until)
        if ts and _now() < ts:
            return f"exhausted until {until}"
    return None


# --- server snapshots ------------------------------------------------------


def set_server(provider: str, *, unit: str, remaining: float,
               limit: Optional[float] = None,
               period_end: Optional[str] = None) -> None:
    """Store a server-truth snapshot. `baseline_used` anchors interpolation:
    local spend since this moment is subtracted from `remaining`.
    A live `remaining > 0` also clears a stale exhausted marker (the 429
    may have been a rate-limit, not an empty tank — exa 03.09)."""
    state = _load()
    e = state.get(provider, {})
    # normalise legacy flat entry to v2 before touching it
    if not isinstance(e.get("local"), dict):
        e = {"local": _local(e),
             **({"exhausted_until": e["exhausted_until"]}
                if e.get("exhausted_until") else {})}
    snap = {"unit": unit, "remaining": float(remaining),
            "baseline_used": int(e["local"].get("used", 0) or 0),
            "fetched_at": _now().isoformat(timespec="seconds")}
    if limit is not None:
        snap["limit"] = float(limit)
    if period_end:
        snap["period_end"] = period_end
    e["server"] = snap
    if remaining > 0:
        e.pop("exhausted_until", None)
    e["updated"] = _now().isoformat(timespec="seconds")
    state[provider] = e
    _save(state)


def server_view(provider: str, *, price: float = 1.0,
                period: str = "month") -> Optional[dict]:
    """Usable server snapshot + interpolated remaining, or None.
    price: local-unit -> server-unit rate (usd providers: $ per 1 request;
    request/credit providers leave the default 1.0)."""
    e = get_entry(provider)
    s = e.get("server")
    if not isinstance(s, dict) or s.get("remaining") is None:
        return None
    fetched = _parse_ts(s.get("fetched_at", ""))
    if fetched is None or _now() - fetched > SERVER_MAX_AGE:
        return None
    loc = _local(e)
    ws = loc.get("window_start")
    if (ws is not None and ws != _window_start(period, _now())
            and s.get("unit") != "usd"):
        # reset-quotas (requests/credits) restart each window: a snapshot
        # anchored in the previous window is not about the current quota.
        # $ balances survive window rolls — keep the snapshot.
        return None
    used_now = int(loc.get("used", 0) or 0) if ws is not None else 0
    spent_since = max(0, used_now - int(s.get("baseline_used", 0)))
    interp = float(s["remaining"]) - spent_since * price
    return {"unit": s.get("unit", "requests"), "remaining": interp,
            "snapshot_remaining": float(s["remaining"]),
            "limit": s.get("limit"), "period_end": s.get("period_end"),
            "fetched_at": s.get("fetched_at"),
            "age_sec": int((_now() - fetched).total_seconds()),
            "fresh": _now() - fetched <= SERVER_TTL}


def _fmt(remaining: float, unit: str) -> str:
    if unit == "usd":
        return f"${remaining:.2f}"
    suffix = "" if unit == "requests" else f" {unit}"
    return f"{round(remaining)}{suffix}"


# --- remaining / spend / exhaust -------------------------------------------


def remaining(provider: str, limit: Optional[int], period: str,
              *, price: float = 1.0) -> Optional[float]:
    """Best-known remaining quota, in the SERVER's unit when a usable
    snapshot exists (interpolated), else in local request units.
    <= 0 means "do not use" for both kinds — unit-agnostic skip test."""
    sv = server_view(provider, price=price, period=period)
    if sv is not None:
        return sv["remaining"]
    if limit is None:
        return None
    e = get_entry(provider)
    loc = _local(e)
    if loc.get("window_start") != _window_start(period, _now()):
        return float(limit) * price  # window rolled — full quota back
    return max(0.0, float(limit) - int(loc.get("used", 0))) * price


def spend(provider: str, count: int = 1, period: str = "none") -> None:
    state = _load()
    e = state.get(provider, {})
    ws = _window_start(period, _now())
    loc = _local(e)
    if loc.get("window_start") != ws:
        srv = e.get("server")
        if isinstance(srv, dict):
            if srv.get("unit") == "usd":
                # $ balance is continuous across window rolls — keep the
                # snapshot, just re-anchor interpolation to the fresh counter
                srv["baseline_used"] = 0
            elif loc.get("window_start") is not None:
                # reset-quota rolled for real: the snapshot's baseline points
                # into the previous window — it can't be interpolated anymore
                e.pop("server", None)
        loc = {"window_start": ws, "used": 0}
    loc["used"] = int(loc.get("used", 0)) + count
    e["local"] = loc
    e.pop("window_start", None)  # legacy duplicate of the same fields
    e.pop("used", None)
    e["updated"] = _now().isoformat(timespec="seconds")
    state[provider] = e
    _save(state)


def mark_exhausted(provider: str, until: Optional[str] = None, period: str = "none") -> None:
    """Called on a real 429/limit error. `until` = ISO timestamp if the
    provider told us; else derive from the period; else 1 hour cooldown."""
    state = _load()
    e = state.get(provider, {})
    if until:
        ts = _parse_ts(until)
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


def status_line(provider: str, limit: Optional[int], period: str, label: str,
                *, unit: str = "requests", price: float = 1.0) -> str:
    reason = is_exhausted(provider)
    if reason:
        return reason
    sv = server_view(provider, price=price, period=period)
    if sv is not None:
        age = _fmt_age(sv["age_sec"])
        return f"{_fmt(sv['remaining'], sv['unit'])} left (server, {age})"
    rem = remaining(provider, limit, period)
    if rem is None:
        return label or "no known limit (keyless)"
    per = f" per {period}" if period in ("day", "month") else ""
    return f"{_fmt(rem, unit)} left{per}"


def _fmt_age(sec: int) -> str:
    if sec < 90:
        return f"{sec}s"
    if sec < 90 * 60:
        return f"{sec // 60}m"
    if sec < 36 * 3600:
        return f"{sec // 3600}h"
    return f"{sec // 86400}d"


def reset(provider: Optional[str] = None) -> None:
    state = _load()
    if provider:
        state.pop(provider, None)
    else:
        state = {}
    _save(state)
