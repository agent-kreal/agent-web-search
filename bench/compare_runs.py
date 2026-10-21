#!/usr/bin/env python3
"""Сравнение двух прогонов бенчмарка по union-метрикам (шаг 3.7).

Usage:
    python3 bench/compare_runs.py <run_dir_A> <run_dir_B> [--metric recall]

Читает union_metrics.json (пишет run_union.py score) каждого прогона,
выводит дельту по провайдерам: recall@K / precision@K / quality.
Порядок строк — по метрике прогона B. Регрессия >2 п.п. помечается ⚠.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load(run: Path) -> dict:
    f = run / "union_metrics.json"
    if not f.exists():
        sys.exit(f"нет {f} — сначала run_union.py score --run {run}")
    return json.loads(f.read_text())


def main() -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("run_a", type=Path)
    ap.add_argument("run_b", type=Path)
    ap.add_argument("--metric", default="recall",
                    choices=["recall", "precision", "quality"])
    a = ap.parse_args()

    ma, mb = load(a.run_a), load(a.run_b)
    ka = {k: v for k, v in ma["ranking"].items() if v.get(a.metric) is not None}
    kb = {k: v for k, v in mb["ranking"].items() if v.get(a.metric) is not None}
    common = [p for p in ka if p in kb]

    name = f"{a.metric}@{mb.get('top', '?')}"
    print(f"A: {a.run_a.name} ({ma.get('n_q', '?')} q)  vs  "
          f"B: {a.run_b.name} ({mb.get('n_q', '?')} q)  — {name}\n")
    print(f"{'provider':<13} {'A':>6} {'B':>6} {'Δ':>7}")
    rows = sorted(common, key=lambda p: -kb[p][a.metric])
    for p in rows:
        va, vb = ka[p][a.metric], kb[p][a.metric]
        d = vb - va
        mark = " ⚠" if d < -0.02 else ""
        print(f"{p:<13} {va:>6.2f} {vb:>6.2f} {d:>+7.2f}{mark}")
    only_a = [p for p in ka if p not in kb]
    only_b = [p for p in kb if p not in ka]
    if only_a:
        print(f"только в A: {', '.join(only_a)}")
    if only_b:
        print(f"только в B: {', '.join(only_b)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
