#!/usr/bin/env python3
"""Замер обрезов «посреди токена» в ДЕФОЛТНОМ fetch (шаг 0.3 фазы 0).

Для каждого URL из bench-extract/dataset.jsonl: `wsearch fetch URL --no-cache --json`
— дефолтный каскад провайдеров, дефолтный max-chars (6000). Классифицируем конец
content по последнему непустому символу:
  sentence-end : . ! ? … » ” '
  soft         : ) ] } : ; ,
  newline      : контент заканчивался пустой строкой (граница абзаца)
  mid-token    : буква/цифра → ОБРЕЗ посреди предложения/слова
Также фиксируем: достигнут ли лимит (len >= max_chars - 10) и provider.

Выход: bench-results/runs/<RUN>/cut_measure.jsonl + сводка в stdout.

Запуск: python3 bench-extract/measure_cut.py [--run 2026-10-19-phase0]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "bench-extract"
DATASET = BENCH / "dataset.jsonl"
RUNS = ROOT / "bench-results" / "runs"

END_SENT = set(".!?…»”’\"'")


def classify_tail(content: str) -> dict:
    raw_end = content.endswith("\n")
    stripped = content.rstrip()
    if not stripped:
        return {"tail_class": "empty", "hit_cap": False}
    last = stripped[-1]
    if raw_end and content.endswith("\n\n"):
        cls = "newline"                      # граница абзаца
    elif last in END_SENT:
        cls = "sentence-end"
    elif last in ")]}:;,":
        cls = "soft"
    elif last.isalnum():
        cls = "mid-token"                    # обрез посреди слова/предложения
    else:
        cls = "other"
    return {"tail_class": cls}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="2026-10-19-phase0")
    args = ap.parse_args()

    out_dir = RUNS / args.run
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "cut_measure.jsonl"

    rows = [json.loads(l) for l in DATASET.read_text().splitlines() if l.strip()]
    stats = {"n": 0, "ok": 0, "fail": 0, "mid-token": 0, "at_cap": 0,
             "mid-token-at-cap": 0, "chars": []}
    with out_file.open("w") as fout:
        for r in rows:
            stats["n"] += 1
            cmd = [str(ROOT / "web-search"), "fetch", r["url"],
                   "--no-cache", "--json"]
            t0 = time.time()
            try:
                p = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
            except subprocess.TimeoutExpired:
                rec = {"q": r["q"], "url": r["url"], "ok": False,
                       "error": "timeout 90s"}
                fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
                stats["fail"] += 1
                continue
            wall = round(time.time() - t0, 1)
            if p.returncode != 0:
                rec = {"q": r["q"], "url": r["url"], "ok": False,
                       "error": (p.stderr.strip() or p.stdout.strip())[:200]}
                fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
                stats["fail"] += 1
                print(f"[{r['q']:>2}] FAIL {r['url'][:60]}")
                continue
            d = json.loads(p.stdout)
            content = d.get("content") or ""
            meta = {"q": r["q"], "url": r["url"], "ok": True,
                    "provider": d.get("provider"), "chars": len(content),
                    "max_chars": d.get("max_chars"), "wall": wall}
            meta.update(classify_tail(content))
            at_cap = d.get("max_chars") and len(content) >= d["max_chars"] - 10
            meta["hit_cap"] = bool(at_cap)
            fout.write(json.dumps(meta, ensure_ascii=False) + "\n")
            stats["ok"] += 1
            stats["chars"].append(len(content))
            if meta["tail_class"] == "mid-token":
                stats["mid-token"] += 1
            if at_cap:
                stats["at_cap"] += 1
                if meta["tail_class"] == "mid-token":
                    stats["mid-token-at-cap"] += 1
            print(f"[{r['q']:>2}] {meta['tail_class']:<13} len={len(content):>6} "
                  f"cap={int(bool(at_cap))} {r['url'][:50]}")

    chars = sorted(stats["chars"])
    med = chars[len(chars) // 2] if chars else 0
    ok = stats["ok"] or 1
    print(f"\n=== summary ({out_file}) ===")
    print(f"ok={stats['ok']}/{stats['n']}  fails={stats['fail']}")
    print(f"median chars={med}  max={max(chars) if chars else 0}")
    print(f"mid-token tails: {stats['mid-token']}/{ok} "
          f"({100 * stats['mid-token'] / ok:.0f}%)")
    print(f"at cap: {stats['at_cap']}/{ok}; mid-token AND at cap: "
          f"{stats['mid-token-at-cap']}/{ok} "
          f"({100 * stats['mid-token-at-cap'] / ok:.0f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
