"""Usage telemetry: append-only log of every real call, for later audits.

state/usage.jsonl — one line per search/fetch/multi/gather invocation:
  {ts, cmd, query|url, intent, intent_source (flag|auto|none),
   provider, tried: [{name, error, wall_sec}] — providers that
   errored/were skipped before success, each with the reason and its
   cost in seconds (quota skips cost 0),
   freshness, n_results, wall_sec, ok}

Monthly audit: `wsearch usage --days 30` aggregates intents, providers,
fallback rate, errors, empty SERPs, latency and repeated queries (a repeat
soon after the first try is a proxy signal "first answer didn't help").

Privacy: file is local, same trust level as state/quotas.json (gitignored).
Rotation: at 5 MB the log moves to usage.jsonl.1 (one generation kept).
"""

from __future__ import annotations

import json
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

STATE = Path(__file__).resolve().parent.parent / "state"
LOG = STATE / "usage.jsonl"
MAX_BYTES = 5 * 1024 * 1024


def log(record: dict) -> None:
    """Append one usage line. Never raises: telemetry must not break calls."""
    try:
        STATE.mkdir(exist_ok=True)
        if LOG.exists() and LOG.stat().st_size > MAX_BYTES:
            LOG.replace(LOG.with_suffix(".jsonl.1"))
        rec = {"ts": datetime.now().isoformat(timespec="seconds"), **record}
        with LOG.open("a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _read(days: int | None = None) -> list[dict]:
    rows = []
    files = [LOG, LOG.with_suffix(".jsonl.1")]
    for f in files:
        if not f.exists():
            continue
        for line in f.read_text().splitlines():
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    if days is not None:
        cutoff = datetime.now() - timedelta(days=days)
        rows = [r for r in rows if _ts(r) >= cutoff]
    return rows


def _ts(r: dict) -> datetime:
    try:
        return datetime.fromisoformat(r["ts"])
    except (KeyError, ValueError):
        return datetime.fromtimestamp(0)


def _fmt_pct(x: float) -> str:
    return f"{100 * x:.0f}%"


def summary(days: int | None = 30) -> dict:
    """Aggregate the log into a structure ready for print or --json."""
    rows = _read(days)
    if not rows:
        return {"calls": 0, "period": None}

    searches = [r for r in rows if r.get("cmd") in ("search", "multi")]
    fetches = [r for r in rows if r.get("cmd") in ("fetch", "gather")]

    def by(col: str, subset: list[dict]) -> dict:
        out = {}
        groups = defaultdict(list)
        for r in subset:
            groups[str(r.get(col) or "none")].append(r)
        for key, recs in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            ok = [r for r in recs if r.get("ok")]
            walls = [r.get("wall_sec") or 0 for r in recs]
            fallback = [r for r in ok if r.get("tried")]
            empty = [r for r in ok if r.get("n_results") == 0]
            out[key] = {
                "calls": len(recs),
                "ok": len(ok),
                "fallbacks": len(fallback),
                "empty": len(empty),
                "med_wall": round(statistics.median(walls), 1) if walls else 0,
            }
        return out

    # repeated (normalized) queries — proxy for "first answer didn't help"
    norm = Counter()
    for r in searches:
        if r.get("query"):
            norm[" ".join(str(r["query"]).lower().split())] += 1
    repeats = [{"query": q, "times": n} for q, n in norm.most_common(8) if n > 1]

    return {
        "calls": len(rows),
        "period": {"from": rows[0]["ts"], "to": rows[-1]["ts"], "days": days},
        "by_intent": by("intent", searches),
        "intent_source": dict(Counter(str(r.get("intent_source") or "none")
                                      for r in searches)),
        "by_provider": by("provider", [r for r in rows if r.get("ok")]),
        "search_calls": len(searches),
        "fetch_calls": len(fetches),
        "errors": sum(1 for r in rows if not r.get("ok")),
        "repeated_queries": repeats,
    }


def print_summary(days: int | None) -> None:
    s = summary(days)
    if not s.get("calls"):
        print(f"# usage: no logged calls yet ({LOG})")
        return
    p = s["period"]
    print(f"# usage: {s['calls']} calls  ({p['from']} .. {p['to']})"
          f"  searches={s['search_calls']} fetches={s['fetch_calls']}"
          f"  errors={s['errors']}")
    if s["by_intent"]:
        print("\n## searches by intent")
        for intent, d in s["by_intent"].items():
            fb = _fmt_pct(d["fallbacks"] / d["calls"])
            print(f"  {intent:<10} {d['calls']:>4} calls  "
                  f"fallbacks {d['fallbacks']:>3} ({fb})  "
                  f"empty {d['empty']:>3}  med {d['med_wall']}s")
    if s["intent_source"]:
        print(f"\n## intent source: {dict(s['intent_source'])}")
    if s["by_provider"]:
        print("\n## served by provider")
        for prov, d in s["by_provider"].items():
            print(f"  {prov:<13} {d['calls']:>4}  empty {d['empty']:>3}  "
                  f"med {d['med_wall']}s")
    if s["repeated_queries"]:
        print("\n## repeated queries (possible 'didn't help' signal)")
        for r in s["repeated_queries"]:
            print(f"  x{r['times']}  {r['query'][:70]}")
    print(f"\n# raw: {LOG}")
