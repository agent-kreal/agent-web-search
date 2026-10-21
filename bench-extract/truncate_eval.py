#!/usr/bin/env python3
"""Оценка резки на замороженных копиях (фаза 1, бесплатно, повторяемо).

Сравнивает на frozen_content.jsonl:
  raw6000   = content[:6000]                (старое поведение router)
  smart6000 = smart_truncate(content, 6000) (новое, engine/truncate.py)
Метрики на каждый вариант: with_recall (обязательные фразы из dataset),
длина, tail-класс (mid-token хвост?), потеря длины относительно raw.

Выход: таблица по URL + средние; файл bench-results/runs/<RUN>/truncate_eval.json
Запуск: python3 bench-extract/truncate_eval.py [--limit N] [--run 2026-10-19-phase1]
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from bench_extract_shim import snippet_recall, tail_class  # type: ignore

FROZEN = ROOT / "bench-results" / "runs" / "2026-10-19-phase0" / "frozen_content.jsonl"
DATASET = ROOT / "bench-extract" / "dataset.jsonl"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="2026-10-19-phase1")
    args = ap.parse_args()

    from engine.truncate import smart_truncate

    rows = {r["q"]: r for r in
            (json.loads(l) for l in DATASET.read_text().splitlines() if l.strip())}
    frozen = [json.loads(l) for l in FROZEN.read_text().splitlines() if l.strip()]

    out_path = ROOT / "bench-results" / "runs" / args.run / "truncate_eval.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    per = []
    print(f"{'q':>3} {'chars':>6} | {'rec_raw':>7} {'rec_smart':>9} | "
          f"{'len_raw':>7} {'len_smart':>9} {'lost%':>6} | tail")
    for f in frozen:
        row = rows.get(f["q"], {})
        content = f["content"]
        if not content:
            continue
        raw = content[:6000]
        # полный конвейер smart-режима router (фаза 1.2 + 1.1)
        from engine.prefilter import strip_junk
        cleaned, junk_stats = strip_junk(content)
        smart = smart_truncate(cleaned, 6000)
        rec_raw = snippet_recall(raw, row.get("with"))
        rec_smart = snippet_recall(smart, row.get("with"))
        lost = 100 * (len(raw) - len(smart)) / max(1, len(raw))
        per.append({"q": f["q"], "url": f["url"], "chars": f["chars"],
                    "rec_raw": rec_raw, "rec_smart": rec_smart,
                    "len_raw": len(raw), "len_smart": len(smart),
                    "lost_pct": round(lost, 1),
                    "junk_chars": junk_stats["chars_removed"],
                    "junk_nav": junk_stats["ui_nav"],
                    "junk_meta": junk_stats["metadata"] + junk_stats["ads"],
                    "tail_raw": tail_class(raw), "tail_smart": tail_class(smart)})
        print(f"{f['q']:>3} {f['chars']:>6} | {rec_raw:>7} {rec_smart:>9} | "
              f"{len(raw):>7} {len(smart):>9} {lost:>5.1f}% | junk −{junk_stats['chars_removed']:>5} | "
              f"{per[-1]['tail_raw']}->{per[-1]['tail_smart']}")

    n = len(per) or 1
    avg = {
        "n": len(per),
        "rec_raw": round(statistics.mean(p["rec_raw"] for p in per if p["rec_raw"] is not None), 3),
        "rec_smart": round(statistics.mean(p["rec_smart"] for p in per if p["rec_smart"] is not None), 3),
        "mid_raw": sum(1 for p in per if p["tail_raw"] == "mid-token") / n,
        "mid_smart": sum(1 for p in per if p["tail_smart"] == "mid-token") / n,
        "lost_pct_med": statistics.median(p["lost_pct"] for p in per),
        "junk_chars_total": sum(p["junk_chars"] for p in per),
        "junk_nav_lines": sum(p["junk_nav"] for p in per),
        "junk_meta_lines": sum(p["junk_meta"] for p in per),
    }
    print("\n=== summary ===")
    for k, v in avg.items():
        print(f"{k:>14}: {v}")
    out_path.write_text(json.dumps({"avg": avg, "per": per}, ensure_ascii=False, indent=1))
    print(f"\n{out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
