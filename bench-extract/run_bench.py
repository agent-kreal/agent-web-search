#!/usr/bin/env python3
"""Часть B: прогон 8 экстракторов на датасете живых URL (bench-extract/dataset.jsonl).

Участники:
  local-auto / local-http / local-curl / local-browser — напрямую venv
  (полный JSON: tier/elapsed_ms/trace), бесплатно;
  firecrawl / tavily / jina — через ./web-search fetch --provider X --no-cache
  (тратят кредиты; jina keyless ~20 RPM);
  parallel — то же, только URL с "parallel": true ($-грант).

Строка raw.jsonl: scenario, q, url, extractor, wall_sec, ok, chars, tier,
provider, error, trace, head, mid (полный markdown не храним — raw был бы ~10MB).
Resume-safe: пары (url, extractor) из существующего raw.jsonl скипаются.

Запуск: python3 bench-extract/run_bench.py [--extractors csv] [--scenarios csv] [--limit N]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # repo root
BENCH = ROOT / "bench-extract"
CLI = str(ROOT / "web-search")                          # wsearch -> web-search (соседний чат)
VENV_PY = str(ROOT / "local-extract" / ".venv" / "bin" / "python")
DATASET = BENCH / "dataset.jsonl"
RAW = BENCH / "results" / "raw.jsonl"

LOCAL_TIERS = ["local-auto", "local-http", "local-curl", "local-browser"]
SERVICE = ["firecrawl", "tavily", "jina", "parallel"]
ALL = LOCAL_TIERS + SERVICE

SLEEP = {"local-auto": 0, "local-http": 0, "local-curl": 0.2, "local-browser": 0.5,
         "firecrawl": 4.0, "tavily": 1.0, "jina": 3.5, "parallel": 1.0}
MAX_CHARS = "32000"
HEAD, MID = 2000, 2000


def load_dataset(scenarios=None, limit=None):
    rows = [json.loads(l) for l in DATASET.read_text().splitlines() if l.strip()]
    if scenarios:
        rows = [r for r in rows if r["scenario"] in scenarios]
    if limit:
        rows = rows[:limit]
    return rows


def done_pairs() -> set:
    done = set()
    if RAW.exists():
        for l in RAW.read_text().splitlines():
            try:
                d = json.loads(l)
                done.add((d["url"], d["extractor"]))
            except json.JSONDecodeError:
                continue
    return done


def emit(rec: dict):
    with RAW.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def slices(text: str) -> dict:
    """head + mid вместо полного content (экономия места в raw)."""
    if len(text) <= HEAD + MID:
        return {"head": text, "mid": ""}
    mid_start = (len(text) - MID) // 2
    return {"head": text[:HEAD], "mid": text[mid_start:mid_start + MID]}


def run_local(url: str, tier: str) -> dict:
    cmd = [VENV_PY, "-m", "local_extract", url, "--max-chars", MAX_CHARS]
    if tier != "auto":
        cmd += ["--tier", tier.split("-", 1)[1]]
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=70)
    wall = round(time.time() - t0, 2)
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "chars": 0, "tier": None, "provider": None,
                "error": f"bad json rc={p.returncode}: {p.stderr[:300]}", "trace": []}
    if d.get("ok"):
        content = d.get("content") or ""
        return {"ok": True, "chars": len(content), "tier": d.get("tier"),
                "provider": f"local-{d.get('tier')}", "error": None, "wall": wall,
                "trace": d.get("trace", []), **slices(content)}
    return {"ok": False, "chars": 0, "tier": d.get("tier"), "provider": None,
            "error": f"{d.get('reason')}/{d.get('note') or ''}", "wall": wall,
            "trace": d.get("trace", [])}


def run_service(url: str, name: str) -> dict:
    cmd = [CLI, "fetch", url, "--provider", name, "--max-chars", MAX_CHARS,
           "--no-cache", "--json"]
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        wall = round(time.time() - t0, 2)
    except subprocess.TimeoutExpired:
        return {"ok": False, "chars": 0, "tier": None, "provider": None,
                "error": "cli timeout 90s", "wall": 90.0, "trace": []}
    if p.returncode != 0:
        err = p.stderr.strip().splitlines()[-1][:300] if p.stderr.strip() else f"rc={p.returncode}"
        return {"ok": False, "chars": 0, "tier": None, "provider": None,
                "error": err, "wall": wall, "trace": []}
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "chars": 0, "tier": None, "provider": None,
                "error": "bad cli json", "wall": wall, "trace": []}
    content = d.get("content") or ""
    return {"ok": True, "chars": len(content), "tier": None,
            "provider": d.get("provider", name), "error": None, "wall": wall,
            "trace": [], **slices(content)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--extractors", help="csv из: " + ",".join(ALL))
    ap.add_argument("--scenarios", help="csv фильтр сценариев")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--retry-failed", help="extractor: удалить его fail-строки из raw и перегнать")
    args = ap.parse_args()

    if args.retry_failed:
        lines = RAW.read_text().splitlines() if RAW.exists() else []
        keep = [l for l in lines
                if not (json.loads(l)["extractor"] == args.retry_failed and not json.loads(l)["ok"])]
        dropped = len(lines) - len(keep)
        RAW.write_text("\n".join(keep) + ("\n" if keep else ""))
        print(f"--retry-failed {args.retry_failed}: удалено {dropped} fail-строк")

    extractors = args.extractors.split(",") if args.extractors else ALL
    scenarios = args.scenarios.split(",") if args.scenarios else None
    rows = load_dataset(scenarios, args.limit)
    done = done_pairs()
    print(f"{len(rows)} URL × {len(extractors)} экстракторов; "
          f"уже готово {len(done)} пар — скипаем")

    for ext in extractors:
        if ext not in ALL:
            print(f"неизвестный экстрактор {ext}, пропуск")
            continue
        todo = [r for r in rows
                if (r["url"], ext) not in done
                and (ext != "parallel" or r.get("parallel"))]
        print(f"\n=== {ext}: {len(todo)} URL ===")
        for r in todo:
            try:
                result = (run_local(r["url"], ext) if ext.startswith("local-")
                          else run_service(r["url"], ext))
            except subprocess.TimeoutExpired:
                result = {"ok": False, "chars": 0, "tier": None, "provider": None,
                          "error": "timeout 70s", "wall": 70.0, "trace": []}
            rec = {"scenario": r["scenario"], "q": r["q"], "url": r["url"],
                   "extractor": ext, "ok": result["ok"], "chars": result["chars"],
                   "tier": result["tier"], "provider": result["provider"],
                   "error": result["error"], "trace": result["trace"],
                   "wall_sec": result.get("wall"),
                   **{k: result.get(k, "") for k in ("head", "mid")}}
            emit(rec)
            print(f"  [{r['q']:>2}] ok={int(result['ok'])} chars={result['chars']:>6} {r['url'][:60]}")
            if SLEEP.get(ext):
                time.sleep(SLEEP[ext])

    # summary
    print("\n=== summary ===")
    stats: dict[str, list] = {}
    for l in RAW.read_text().splitlines():
        try:
            d = json.loads(l)
        except json.JSONDecodeError:
            continue
        stats.setdefault(d["extractor"], []).append(d)
    for ext, recs in sorted(stats.items()):
        oks = [x for x in recs if x["ok"]]
        walls = sorted(x["wall_sec"] for x in recs if isinstance(x.get("wall_sec"), (int, float)))
        med = walls[len(walls) // 2] if walls else None
        print(f"{ext:<14} ok {len(oks)}/{len(recs)}  median wall {med}")
    return 0


if __name__ == "__main__":
    main()
