#!/usr/bin/env python3
"""Сводка фазы 4: P/R@10 всех систем multi на едином (полностью досуженном)
золоте.

Золото = все размеченные URL всех прогонов фазы (baseline 0.4 + досье 4.3,
4.1, 4.2, probe). Системы: baseline (phase0), 4.3, 4.1 (RRF), 4.2 (backfill),
probe (принудительный добор), union-RRF (потолок). Каждый пересчёт меняет
знаменатель золота — потому ВСЕ системы считаются на актуальном наборе.

Запуск: python3 bench/multi_phase4_summary.py [--write]
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "bench-results" / "runs"
TOP = 10

GOLD_SOURCES = [
    RUNS / "2026-10-19-phase0" / "multi_relevance.jsonl",
    RUNS / "2026-10-19-phase4-4.3" / "multi_relevance_new.jsonl",
    RUNS / "2026-10-19-phase4-4.1" / "multi_relevance_new.jsonl",
    RUNS / "2026-10-19-phase4-4.2" / "multi_relevance_new.jsonl",
    RUNS / "2026-10-19-phase4-probe" / "probe_relevance.jsonl",
]

SYSTEMS = [
    ("baseline (concat+dedupe)", RUNS / "2026-10-19-phase0", "multi"),
    ("4.3 schema", RUNS / "2026-10-19-phase4-4.3", "multi"),
    ("4.1 RRF", RUNS / "2026-10-19-phase4-4.1", "multi"),
    ("4.2 RRF+backfill", RUNS / "2026-10-19-phase4-4.2", "multi"),
    ("probe (форс-добор)", RUNS / "2026-10-19-phase4-probe", "multi"),
    ("union-RRF (потолок)", RUNS / "2026-10-19-phase0", "union"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true",
                    help="записать золото и summary в runs/")
    a = ap.parse_args()

    rel: dict[str, dict[str, int]] = {}
    n_src = 0
    for f in GOLD_SOURCES:
        if not f.exists():
            print(f"[skip] нет файла золота: {f.name} ({f.parent.name})")
            continue
        for l in f.read_text().splitlines():
            if not l.strip():
                continue
            d = json.loads(l)
            rel.setdefault(d["task"], {})[d["url"]] = d["rel"]
            n_src += 1
    tasks = [json.loads(l) for l in
             (ROOT / "bench" / "multi_tasks.jsonl").read_text().splitlines()
             if l.strip()]

    def pr(run_dir: Path, which: str):
        rows = []
        for t in tasks:
            slug = t["task"]
            gold = {u for u, v in rel[slug].items() if v == 1}
            fp = run_dir / "multi" / f"{slug}__{which}.json"
            if not fp.exists():
                return None
            d = json.loads(fp.read_text())
            top = [x["url"] for x in (d.get("results") or d.get("pool", []))[:TOP]]
            hits = sum(1 for u in top if u in gold)
            rows.append((hits / len(top) if top else 0.0,
                         hits / len(gold) if gold else 0.0, slug))
        return (statistics.mean(r[0] for r in rows),
                statistics.mean(r[1] for r in rows), rows)

    n_rel = sum(v == 1 for t in rel for v in rel[t].values())
    print(f"золото: {n_src} размеченных строк, rel=1: {n_rel}")
    print(f"\n{'система':<24} {'P@10':>6} {'R@10':>6}")
    out_rows = []
    per_task = {}
    for name, run_dir, which in SYSTEMS:
        res = pr(run_dir, which)
        if res is None:
            print(f"{name:<24}   (нет артефакта)")
            continue
        p, r, rows = res
        out_rows.append((name, p, r))
        per_task[name] = {row[2]: {"P": row[0], "R": row[1]} for row in rows}
        print(f"{name:<24} {p:>6.2f} {r:>6.2f}")

    if a.write:
        gold_out = RUNS / "2026-10-19-phase4" / "multi_relevance_all.jsonl"
        gold_out.parent.mkdir(exist_ok=True)
        with gold_out.open("w") as f:
            for t, urls in rel.items():
                for u, v in urls.items():
                    f.write(json.dumps({"task": t, "url": u, "rel": v},
                                       ensure_ascii=False) + "\n")
        (RUNS / "2026-10-19-phase4" / "phase4_summary.json").write_text(
            json.dumps({"systems": out_rows, "per_task": per_task},
                       ensure_ascii=False, indent=1))
        print(f"\nзаписано: {gold_out} и phase4_summary.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
