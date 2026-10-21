#!/usr/bin/env python3
"""Повторный multi-замер для фазы 4 (4.3 / 4.1 / 4.2): только multi-часть.

Отличия от run_multi.py (который собирал baseline с нуля): union-источники
не перегоняются (заморожены в baseline-прогоне, от движка не зависят) —
файлы <slug>__union.json копируются; multi-выдача прогоняется заново на
текущем движке; для URL, которых нет в baseline-разметке, генерируется
judge-файл (досуживание золота). После судейства: мердж разметок в
<run>/multi_relevance.jsonl и python3 bench/multi_pr.py --run <run>.

Запуск:
  python3 bench/rerun_multi.py --run 2026-10-19-phase4-4.3 [--baseline 2026-10-19-phase0] \
      [--sleep 1] [-- extra-флаги wsearch multi, напр. --no-backfill]
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS = ROOT / "bench" / "multi_tasks.jsonl"
RUNS = ROOT / "bench-results" / "runs"


def call(args: list[str]) -> dict | None:
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        return None
    if p.returncode != 0:
        print(f"  [fail rc={p.returncode}] {p.stderr[:200]}")
        return None
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True, help="новый run-dir (создаётся)")
    ap.add_argument("--baseline", default="2026-10-19-phase0",
                    help="прогон с замороженными union.json и разметкой")
    ap.add_argument("--sleep", type=float, default=1.0)
    ap.add_argument("--label", default="multi",
                    help="метка source в judge-файле (multi-4.3 и т.п.)")
    ap.add_argument("extra", nargs="*",
                    help="флаги wsearch multi после -- (напр. --no-backfill)")
    args = ap.parse_args()

    base = RUNS / args.baseline
    out_dir = RUNS / args.run / "multi"
    out_dir.mkdir(parents=True, exist_ok=True)

    # разметка baseline: task -> {url: rel} (для отсева уже размеченных)
    marked: dict[str, dict[str, int]] = {}
    for l in (base / "multi_relevance.jsonl").read_text().splitlines():
        if not l.strip():
            continue
        d = json.loads(l)
        marked.setdefault(d["task"], {})[d["url"]] = d["rel"]

    tasks = [json.loads(l) for l in TASKS.read_text().splitlines() if l.strip()]
    judge_lines: list[str] = []
    n_new = 0
    for t in tasks:
        slug = t["task"]
        print(f"=== {slug}")
        # union-копия из baseline (если ещё не скопирована — репрогон того же
        # run не должен перетирать живые union-замеры)
        u_dst = out_dir / f"{slug}__union.json"
        if not u_dst.exists():
            shutil.copy(base / "multi" / f"{slug}__union.json", u_dst)

        cmd = [str(ROOT / "web-search"), "multi",
               "--queries", "|".join(t["queries"]), "-n", "5", "--json"] + args.extra
        d = call(cmd)
        results = (d or {}).get("results", [])
        (out_dir / f"{slug}__multi.json").write_text(
            json.dumps(d, ensure_ascii=False, indent=1))
        print(f"  multi: {len(results)} uniq results")

        new_items = [r for r in results[:10]
                     if r.get("url") not in marked.get(slug, {})]
        if new_items:
            judge_lines.append(f"## TASK {slug}")
            judge_lines.append(f"ТЕМА: {t['topic']}")
            for r in new_items:
                sn = (r.get("snippet") or "").replace("\n", " ")[:200]
                judge_lines.append(
                    f"URL: {r['url']}\n  TITLE: {(r.get('title') or '')[:100]}"
                    f"\n  SNIP: {sn}\n  SOURCE: {args.label}")
                n_new += 1
        time.sleep(args.sleep)

    if judge_lines:
        (RUNS / args.run / "judge_multi_new.md").write_text("\n".join(judge_lines))
    print(f"\nновых URL для судейства: {n_new}")
    if judge_lines:
        print(f"judge file: {RUNS / args.run / 'judge_multi_new.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
