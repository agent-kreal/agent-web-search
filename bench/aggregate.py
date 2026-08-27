#!/usr/bin/env python3
"""Aggregate judge scores into the scenario x provider matrix.

Reads bench/results/scores_*.jsonl (written by judge subagents):
{"scenario", "q", "provider", "scores": [0..2 x3], "hit": bool, "note"}

Prints: per-scenario table (avg relevance 0-2, hit@3 rate), overall ranking,
per-provider notes histogram. Markdown-ready for REPORT.md.
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

RES = Path(__file__).resolve().parent / "results"

PROVIDERS = ["tavily", "youcom", "exa", "brave", "linkup", "parallel-anon"]


def load() -> list[dict]:
    rows = []
    for f in sorted(RES.glob("scores_*.jsonl")):
        for line in f.read_text().splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


def cell(recs: list[dict]) -> str:
    if not recs:
        return "—"
    avg = statistics.mean([s for r in recs for s in r["scores"]])
    hits = sum(1 for r in recs if r.get("hit"))
    return f"{avg:.2f}/{hits}{len(recs)}"


def main() -> int:
    rows = load()
    print(f"loaded {len(rows)} scored blocks\n")

    by_scen_prov = defaultdict(list)
    by_prov = defaultdict(list)
    for r in rows:
        by_scen_prov[(r["scenario"], r["provider"])].append(r)
        by_prov[r["provider"]].append(r)

    scenarios = sorted({s for s, _ in by_scen_prov})

    # header
    print("| scenario | " + " | ".join(PROVIDERS) + " |")
    print("|---" * (len(PROVIDERS) + 1) + "|")
    for s in scenarios:
        cells = [cell(by_scen_prov.get((s, p), [])) for p in PROVIDERS]
        print(f"| {s} | " + " | ".join(cells) + " |")

    # overall
    print("\n## overall (avg relevance 0-2 | hit-rate | n)")
    stats = []
    for p in PROVIDERS:
        recs = by_prov.get(p, [])
        if not recs:
            continue
        avg = statistics.mean([s for r in recs for s in r["scores"]])
        hitrate = sum(1 for r in recs if r.get("hit")) / len(recs)
        top2 = sum(1 for r in recs if r["scores"] and r["scores"][0] == 2) / len(recs)
        stats.append((avg, hitrate, top2, p, len(recs)))
    stats.sort(reverse=True)
    print(f"{'provider':<13} {'avg_rel':>7} {'hit@3':>6} {'top1=2':>6} {'n':>4}")
    for avg, hitrate, top2, p, n in stats:
        print(f"{p:<13} {avg:>7.2f} {hitrate:>6.0%} {top2:>6.0%} {n:>4}")

    # per-provider best/worst scenarios
    print("\n## per-provider best/worst scenario (by avg relevance)")
    for p in PROVIDERS:
        cells = {s: statistics.mean([x for r in by_scen_prov.get((s, p), [])
                                     for x in r["scores"]])
                 for s in scenarios if by_scen_prov.get((s, p))}
        if not cells:
            continue
        best = max(cells, key=lambda s: cells[s])
        worst = min(cells, key=lambda s: cells[s])
        print(f"{p:<13} best={best} ({cells[best]:.2f})  worst={worst} ({cells[worst]:.2f})")

    # notes histogram
    print("\n## frequent notes")
    notes = Counter()
    for r in rows:
        n = (r.get("note") or "").strip().lower()
        if n and n not in ("-", ""):
            notes[n] += 1
    for n, c in notes.most_common(15):
        print(f"  {c:>3}  {n}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
