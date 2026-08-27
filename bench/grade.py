#!/usr/bin/env python3
"""Summarise bench results: latency, error rate, ad-junk, result counts.

This is the OBJECTIVE part (no LLM judging): everything computable straight
from bench/results/raw.jsonl. Relevance judging (hit@3, 0/1/2) is a separate
manual/LLM pass — see grade_judge.py.

Usage:
    python3 bench/grade.py                # per-provider and per-scenario summary
    python3 bench/grade.py --provider ddg
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

RAW = Path(__file__).resolve().parent / "results" / "raw.jsonl"

# duckduckgo html endpoint leaks bing/yahoo ad redirects — count as junk
AD_MARKERS = ("duckduckgo.com/y.js", "ad_domain=", "bing.com/aclick",)


def load() -> list[dict]:
    rows = []
    for line in RAW.read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def clean_results(rec: dict) -> list[dict]:
    out = []
    for r in rec.get("results", []):
        url = r.get("url", "")
        if any(m in url for m in AD_MARKERS):
            continue
        out.append(r)
    return out


def fmt_pct(x: float) -> str:
    return f"{100 * x:5.1f}%"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", default=None)
    args = ap.parse_args()

    rows = load()
    if args.provider:
        rows = [r for r in rows if r["provider"] == args.provider]

    # ---- per provider ----
    print(f"{'provider':<13} {'n':>3} {'ok':>4} {'err%':>6} {'empty':>5} "
          f"{'ads':>4} {'med_lat':>7} {'p90_lat':>7} {'med_n':>5}")
    by_prov = defaultdict(list)
    for r in rows:
        by_prov[r["provider"]].append(r)
    for prov, recs in sorted(by_prov.items()):
        n = len(recs)
        ok = [r for r in recs if r["ok"]]
        empty = [r for r in ok if r.get("n_results", 0) == 0]
        ads = sum(1 for r in ok
                  if len(r.get("results", [])) != len(clean_results(r)))
        lats = sorted(r["wall_sec"] for r in recs)
        p90 = lats[int(0.9 * (len(lats) - 1))] if lats else 0
        med_n = statistics.median([len(clean_results(r)) for r in ok]) if ok else 0
        print(f"{prov:<13} {n:>3} {len(ok):>4} {fmt_pct(1 - len(ok)/n):>6} "
              f"{len(empty):>5} {ads:>4} "
              f"{statistics.median(lats) if lats else 0:>6.1f}s {p90:>6.1f}s "
              f"{med_n:>5.0f}")

    # ---- per scenario x provider: errors and emptiness quick view ----
    print("\nscenario x provider (ok/total, median latency)")
    scen_prov = defaultdict(list)
    for r in rows:
        scen_prov[(r["scenario"], r["provider"])].append(r)
    scenarios = sorted({s for s, _ in scen_prov})
    providers = sorted({p for _, p in scen_prov})
    header = f"{'scenario':<13}" + "".join(f"{p[:10]:>12}" for p in providers)
    print(header)
    for s in scenarios:
        cells = []
        for p in providers:
            recs = scen_prov.get((s, p), [])
            if not recs:
                cells.append(f"{'—':>12}")
                continue
            ok = [r for r in recs if r["ok"]]
            med = statistics.median([r["wall_sec"] for r in recs])
            cells.append(f"{len(ok)}/{len(recs)} {med:4.1f}s".rjust(12))
        print(f"{s:<13}" + "".join(cells))

    # ---- failures detail ----
    fails = [r for r in rows if not r["ok"]]
    if fails:
        print(f"\n{len(fails)} failures:")
        for r in fails:
            print(f"  {r['provider']:<13} {r['scenario']:<12} "
                  f"{r.get('error', '')[:90]}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
