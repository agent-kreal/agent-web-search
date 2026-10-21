#!/usr/bin/env python3
"""Принудительный probe backfill (фаза 4.2): полезен ли добор на датасете.

Триггеры should_backfill на 8 задачах multi_tasks.jsonl не сработали ни разу
(шаги 4.1/4.3 уже вылечили большинство провалов, покрытие-эвристика не
видит семантических провалов). Чтобы ответить на вопрос метрики фазы —
«доля задач, где backfill добавил релевантные URL» — прогоняем доборный
круг ПРИНУДИТЕЛЬНО на каждой задаче: берём фактический топ прогона,
считаем backfill_queries (как сделал бы триггер), зовём 2 запроса,
RRF-мерджим и пишем артефакт + judge-файл новых URL.

Запуск: python3 bench/probe_backfill.py [--run 2026-10-19-phase4-4.2] [--sleep 1]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine import intent as intent_mod                     # noqa: E402
from engine import merge                                    # noqa: E402
from engine.backfill import backfill_queries, key_terms     # noqa: E402

TASKS = ROOT / "bench" / "multi_tasks.jsonl"
RUNS = ROOT / "bench-results" / "runs"


def call(query: str) -> list[dict]:
    p = subprocess.run([str(ROOT / "web-search"), "search", query,
                        "-n", "5", "--json"],
                       capture_output=True, text=True, timeout=120)
    if p.returncode != 0:
        return []
    try:
        return json.loads(p.stdout).get("results", [])
    except json.JSONDecodeError:
        return []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="2026-10-19-phase4-4.2",
                    help="прогон, чьи топы пробиваем добором")
    ap.add_argument("--sleep", type=float, default=1.0)
    args = ap.parse_args()

    base = RUNS / args.run
    out = RUNS / "2026-10-19-phase4-probe" / "multi"
    out.mkdir(parents=True, exist_ok=True)

    # уже размеченное золото
    marked: dict[str, dict[str, int]] = {}
    for f in sorted(RUNS.glob("2026-10-19-phase4*/multi_relevance*.jsonl")) + \
            [RUNS / "2026-10-19-phase0/multi_relevance.jsonl"]:
        if not f.exists():
            continue
        for l in f.read_text().splitlines():
            if not l.strip():
                continue
            d = json.loads(l)
            marked.setdefault(d["task"], {})[d["url"]] = d["rel"]

    tasks = [json.loads(l) for l in TASKS.read_text().splitlines() if l.strip()]
    judge_lines: list[str] = []
    report = []
    for t in tasks:
        slug = t["task"]
        top = json.loads((base / "multi" / f"{slug}__multi.json").read_text())
        queries = t["queries"]
        ikey, _, _ = intent_mod.resolve(queries[0], None, None)
        bf_qs = backfill_queries(queries, top["results"][:10], ikey)
        print(f"=== {slug}: добор {bf_qs}")
        extra_lists, src = [], queries[:]
        for q in bf_qs:
            res = call(q)
            extra_lists.append([r for r in res])
            src.append(q)
            time.sleep(args.sleep)
        base_lists = []
        # исходные списки топа восстановим из multi-выдачи: там RRF-мердж;
        # для probe достаточно смёрджить топ + доборные выдачи
        base_lists.append(top["results"])
        names = ["base-top"] + bf_qs
        merged = merge.rrf_merge(base_lists + extra_lists, source_names=names)
        merged_dicts = [m.to_dict() for m in merged]
        (out / f"{slug}__multi.json").write_text(json.dumps(
            {"queries": top.get("queries", {}),
             "backfill": {"triggered": True, "probe": True, "queries": bf_qs},
             "results": merged_dicts}, ensure_ascii=False, indent=1))
        new_items = [r for r in merged_dicts[:10]
                     if r["url"] not in marked.get(slug, {})
                     and r["url"] not in {x["url"] for x in top["results"][:10]}]
        report.append({"task": slug, "bf_queries": bf_qs,
                       "top10_before": [r["url"] for r in top["results"][:10]],
                       "top10_after": [r["url"] for r in merged_dicts[:10]],
                       "new_in_top10": [r["url"] for r in new_items]})
        if new_items:
            judge_lines.append(f"## TASK {slug}")
            judge_lines.append(f"ТЕМА: {t['topic']}")
            for r in new_items:
                sn = (r.get("snippet") or "").replace("\n", " ")[:200]
                judge_lines.append(
                    f"URL: {r['url']}\n  TITLE: {(r.get('title') or '')[:100]}"
                    f"\n  SNIP: {sn}\n  SOURCE: backfill-probe")
    (RUNS / "2026-10-19-phase4-probe" / "probe_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1))
    if judge_lines:
        (RUNS / "2026-10-19-phase4-probe" / "judge_probe.md").write_text(
            "\n".join(judge_lines))
    n_new = sum(len(r["new_in_top10"]) for r in report)
    print(f"\nновых URL в топ-10 после добора: {n_new}")
    print(f"report: {RUNS / '2026-10-19-phase4-probe' / 'probe_report.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
