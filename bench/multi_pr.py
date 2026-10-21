#!/usr/bin/env python3
"""P/R@10 multi против union-пула по разметке multi_relevance.jsonl (0.4).

Для каждой задачи: gold = URL с rel=1 (из всей разметки задачи);
multi_top10 = вывод wsearch multi (первые 10 uniq);
union_top10 = пул 4 провайдеров по RRF (первые 10).
  precision@10 = |top ∩ gold| / |top|
  recall@10    = |top ∩ gold| / |gold|
Печатает по задачам + средние; для фазы 4 те же числа после RRF/backfill.

Запуск: python3 bench/multi_pr.py [--run 2026-10-19-phase0]
"""
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "bench-results" / "runs"
TOP = 10


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="2026-10-19-phase0")
    args = ap.parse_args()

    base = RUNS / args.run
    rel: dict[str, dict[str, int]] = {}
    for l in (base / "multi_relevance.jsonl").read_text().splitlines():
        if not l.strip():
            continue
        d = json.loads(l)
        rel.setdefault(d["task"], {})[d["url"]] = d["rel"]

    tasks = [json.loads(l) for l in
             (ROOT / "bench" / "multi_tasks.jsonl").read_text().splitlines() if l.strip()]
    rows = []
    print(f"{'task':<16} {'gold':>4} | {'mP@10':>6} {'mR@10':>6} | {'uP@10':>6} {'uR@10':>6}")
    for t in tasks:
        slug = t["task"]
        r = rel.get(slug, {})
        gold = {u for u, v in r.items() if v == 1}

        multi = json.loads((base / "multi" / f"{slug}__multi.json").read_text())
        m_top = [x["url"] for x in multi.get("results", [])[:TOP]]
        union = json.loads((base / "multi" / f"{slug}__union.json").read_text())
        u_top = [x["url"] for x in union.get("pool", [])[:TOP]]

        def pr(top: list[str]) -> tuple[float, float]:
            hits = sum(1 for u in top if u in gold)
            p = hits / len(top) if top else 0.0
            rc = hits / len(gold) if gold else 0.0
            return p, rc

        mp, mr = pr(m_top)
        up, ur = pr(u_top)
        rows.append({"task": slug, "gold": len(gold), "mP": mp, "mR": mr,
                     "uP": up, "uR": ur, "multi_n": len(m_top)})
        print(f"{slug:<16} {len(gold):>4} | {mp:>6.2f} {mr:>6.2f} | {up:>6.2f} {ur:>6.2f}")

    print("\n=== средние по 8 задачам ===")
    print(f"multi:   P@10={statistics.mean(r['mP'] for r in rows):.2f}  "
          f"R@10={statistics.mean(r['mR'] for r in rows):.2f}")
    print(f"unionRRF P@10={statistics.mean(r['uP'] for r in rows):.2f}  "
          f"R@10={statistics.mean(r['uR'] for r in rows):.2f}   (потолок слияния для фазы 4)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
