#!/usr/bin/env python3
"""Мини-multi-baseline (шаг 0.4 фазы 0): P/R URL-пула multi против union-pool.

Для каждой задачи из bench/multi_tasks.jsonl:
  1) `wsearch multi --queries "q1|q2|q3" -n 5 --json` — текущее поведение
     (каскад с фолбэком на каждый запрос, dedupe по URL);
  2) union-источники: каждый запрос × 4 провайдера (youcom, zai, exa, brave)
     через `wsearch search --provider X -n 5 --json` — пин, без фолбэка.
Пост-обработка:
  - union pool: все уникальные URL из (2), ранжированные RRF (k=60);
  - gold-кандидаты: top-10 union по RRF;
  - multi top-10: первые 10 uniq из (1).
  - judge-файл: task → строки url/title/snippet/source → бинарная разметка
    релевантности (отдельные сабагенты-судьи, файл *_relevance.jsonl).

Выход: bench-results/runs/<RUN>/multi/*.json + judge_multi.md

Запуск: python3 bench/run_multi.py [--run 2026-10-19-phase0] [--sleep 1]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS = ROOT / "bench" / "multi_tasks.jsonl"
RUNS = ROOT / "bench-results" / "runs"
UNION_PROVIDERS = ["youcom", "zai", "exa", "brave"]
RRF_K = 60
TOP = 10


def call(args: list[str]) -> dict | None:
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return None
    if p.returncode != 0:
        return None
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="2026-10-19-phase0")
    ap.add_argument("--sleep", type=float, default=1.0)
    args = ap.parse_args()

    out_dir = RUNS / args.run / "multi"
    out_dir.mkdir(parents=True, exist_ok=True)

    tasks = [json.loads(l) for l in TASKS.read_text().splitlines() if l.strip()]
    judge_lines = []
    for t in tasks:
        slug = t["task"]
        print(f"\n=== {slug}: {t['topic'][:60]}")

        # 1) multi как есть
        d = call([str(ROOT / "web-search"), "multi",
                  "--queries", "|".join(t["queries"]), "-n", "5", "--json"])
        multi_results = (d or {}).get("results", [])
        (out_dir / f"{slug}__multi.json").write_text(
            json.dumps(d, ensure_ascii=False, indent=1))
        multi_top = multi_results[:TOP]
        print(f"  multi: {len(multi_results)} uniq results")
        time.sleep(args.sleep)

        # 2) union sources
        union: dict[str, dict] = {}
        rrf: dict[str, float] = {}
        for q in t["queries"]:
            for prov in UNION_PROVIDERS:
                d = call([str(ROOT / "web-search"), "search", q, "-n", "5",
                          "--provider", prov, "--json"])
                items = (d or {}).get("results", [])
                for rank, it in enumerate(items, 1):
                    u = it.get("url", "")
                    if not u:
                        continue
                    rrf[u] = rrf.get(u, 0.0) + 1.0 / (RRF_K + rank)
                    if u not in union:
                        union[u] = {"url": u, "title": it.get("title", ""),
                                    "snippet": it.get("snippet", ""),
                                    "providers": []}
                    if prov not in union[u]["providers"]:
                        union[u]["providers"].append(prov)
                time.sleep(args.sleep)
        pool = sorted(union.values(), key=lambda x: -rrf[x["url"]])
        (out_dir / f"{slug}__union.json").write_text(
            json.dumps({"pool": pool, "rrf": rrf}, ensure_ascii=False, indent=1))
        gold_cand = pool[:TOP]
        print(f"  union: {len(pool)} uniq, top-{TOP} отобрано для judge")

        # 3) judge-файл: всё, что нужно размечать
        judge_lines.append(f"## TASK {slug}")
        judge_lines.append(f"ТЕМА: {t['topic']}")
        seen = set()

        def emit(url_info, source):
            if url_info["url"] in seen:
                return
            seen.add(url_info["url"])
            sn = (url_info.get("snippet") or "").replace("\n", " ")[:200]
            judge_lines.append(
                f"URL: {url_info['url']}\n  TITLE: {(url_info.get('title') or '')[:100]}"
                f"\n  SNIP: {sn}\n  SOURCE: {source}")

        for it in gold_cand:
            emit(it, "union")
        for it in multi_top:
            emit(it, "multi")

    (RUNS / args.run / "judge_multi.md").write_text("\n".join(judge_lines))
    print(f"\njudge file: {RUNS / args.run / 'judge_multi.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
