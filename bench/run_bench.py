#!/usr/bin/env python3
"""Benchmark runner: run every provider against the scenario dataset.

Usage:
    python3 bench/run_bench.py                     # full run (resume-safe)
    python3 bench/run_bench.py --providers tavily,brave
    python3 bench/run_bench.py --scenarios ru-news

Reads bench/dataset.jsonl: {"scenario": "...", "query": "...", "freshness": "week"|null}
Calls `./wsearch search <query> -n 5 --provider X [--freshness F] --json`
(one provider pinned — no fallback, so we measure THAT provider).
Appends one line per (query, provider) to bench/results/raw.jsonl; existing
pairs are skipped on restart. Latency is wall-clock of the subprocess.

$-grant providers (parallel keyed, youcom keyed) are never run — see PLAN.md.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # repo root
WSEARCH = ROOT / "web-search"
DATASET = ROOT / "bench" / "dataset.jsonl"
RAW = ROOT / "bench" / "results" / "raw.jsonl"

# Renewable/keyless only. zai is quota-dead till 2026-09-18; parallel keyed
# and youcom keyed burn one-off $ grants — excluded on purpose.
DEFAULT_PROVIDERS = ["tavily", "youcom", "exa", "brave", "linkup",
                     "parallel-anon", "ddg"]


def load_dataset(only: set[str] | None) -> list[dict]:
    rows = []
    for line in DATASET.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if only and r["scenario"] not in only:
            continue
        rows.append(r)
    return rows


def done_pairs() -> set[tuple[str, str]]:
    done: set[tuple[str, str]] = set()
    if RAW.exists():
        for line in RAW.read_text().splitlines():
            if not line.strip():
                continue
            try:
                r = json.loads(line)
                done.add((r["query"], r["provider"]))
            except json.JSONDecodeError:
                continue
    return done


def run_one(provider: str, row: dict) -> dict:
    cmd = [str(WSEARCH), "search", row["query"], "-n", "5",
           "--provider", provider, "--json"]
    if row.get("freshness"):
        cmd += ["--freshness", row["freshness"]]
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    wall = round(time.time() - t0, 2)
    rec = {"scenario": row["scenario"], "query": row["query"],
           "provider": provider, "wall_sec": wall,
           "freshness": row.get("freshness")}
    if p.returncode == 0:
        try:
            out = json.loads(p.stdout)
            rec["ok"] = True
            rec["results"] = out.get("results", [])
            rec["n_results"] = len(out.get("results", []))
        except json.JSONDecodeError as e:
            rec["ok"] = False
            rec["error"] = f"bad json: {e}; stdout[:200]={p.stdout[:200]}"
    else:
        rec["ok"] = False
        err = p.stderr.strip() or p.stdout.strip()
        rec["error"] = err[:500]
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--providers", default=",".join(DEFAULT_PROVIDERS))
    ap.add_argument("--scenarios", default=None,
                    help="comma-separated scenario filter")
    ap.add_argument("--sleep", type=float, default=1.0,
                    help="pause between calls, be polite")
    args = ap.parse_args()

    providers = [p.strip() for p in args.providers.split(",") if p.strip()]
    only = set(args.scenarios.split(",")) if args.scenarios else None
    rows = load_dataset(only)
    done = done_pairs()

    todo = [(p, r) for r in rows for p in providers if (r["query"], p) not in done]
    total = len(rows) * len(providers)
    print(f"{len(rows)} queries x {len(providers)} providers = {total} pairs, "
          f"{len(done)} already done, {len(todo)} to run")

    RAW.parent.mkdir(parents=True, exist_ok=True)
    stats: dict[str, dict] = {}
    with RAW.open("a") as fout:
        for i, (prov, row) in enumerate(todo, 1):
            rec = run_one(prov, row)
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fout.flush()
            st = stats.setdefault(prov, {"ok": 0, "fail": 0, "wall": []})
            st["ok" if rec["ok"] else "fail"] += 1
            st["wall"].append(rec["wall_sec"])
            mark = "✓" if rec["ok"] else f"✗ {rec.get('error', '')[:60]}"
            print(f"[{i:3}/{len(todo)}] {prov:<13} {row['scenario']:<11} "
                  f"{rec['wall_sec']:5.1f}s  {mark}  {row['query'][:48]}",
                  flush=True)
            if i < len(todo):
                time.sleep(args.sleep)

    print("\n=== run summary ===")
    for prov, st in stats.items():
        w = st["wall"]
        med = sorted(w)[len(w) // 2] if w else 0
        print(f"{prov:<13} ok={st['ok']:3} fail={st['fail']:3} "
              f"median={med:5.1f}s max={max(w) if w else 0:5.1f}s")
    print(f"\nraw results: {RAW}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
