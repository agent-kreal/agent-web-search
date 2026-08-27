#!/usr/bin/env python3
"""Агрегация бенчмарка экстракторов: grade.json + scores_*.jsonl → матрицы.

quality (формула зафиксирована в REPORT.md):
  quality = 0.5*with_recall + 0.35*judge_mean + 0.15*(1 - without_rate)
  judge_mean = mean(structure, clean, content)/6   (0..1)
  Если сниппетов нет (wr/wo = None): quality* = judge_mean, помечается '*'.

Запуск: python3 bench-extract/aggregate.py
"""

from __future__ import annotations

import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

BENCH = Path(__file__).resolve().parent
GRADE = BENCH / "results" / "grade.json"
SCORES = sorted((BENCH / "results").glob("scores_*.jsonl"))

ORDER = ["local-auto", "local-http", "local-curl", "local-browser",
         "firecrawl", "tavily", "jina", "parallel"]
PRICE = {"local-auto": "free", "local-http": "free", "local-curl": "free",
         "local-browser": "free", "jina": "free (RPM)",
         "firecrawl": "1 credit", "tavily": "1 credit", "parallel": "$-grant"}


def load_scores() -> dict:
    """{scenario: {q: {extractor: {structure, clean, content, note}}}}"""
    out: dict = defaultdict(dict)
    for f in SCORES:
        scen = f.stem.replace("scores_", "")
        for l in f.read_text().splitlines():
            if not l.strip():
                continue
            d = json.loads(l)
            out[scen].setdefault(d["q"], {})[d["extractor"]] = d
    return out


def main() -> int:
    grade = json.loads(GRADE.read_text())
    per_ext, matrix = grade["per_ext"], grade["matrix"]
    scores = load_scores()

    # --- сниппет-скоры по (scenario, q, extractor) из raw (как в grade) ---
    from grade import snippet_metrics  # noqa: E402
    rows = {r["url"]: r for r in
            (json.loads(l) for l in (BENCH / "dataset.jsonl").read_text().splitlines() if l.strip())}
    raw = [json.loads(l) for l in (BENCH / "results" / "raw.jsonl").read_text().splitlines() if l.strip()]

    qual: dict[tuple, dict] = {}
    notes: Counter = Counter()
    for r in raw:
        if not r["ok"]:
            continue
        key = (r["scenario"], r["q"])
        sm = snippet_metrics(r, rows.get(r["url"], {}))
        jd = scores.get(r["scenario"], {}).get(r["q"], {}).get(r["extractor"])
        jm = (statistics.mean([jd["structure"], jd["clean"], jd["content"]]) / 6
              if jd else None)
        wr, wo = sm["with_recall"], sm["without_rate"]
        if jm is None:
            continue    # не судился
        if wr is None:
            qv, star = jm, "*"
        else:
            wo_f = wo if wo is not None else 0.0
            qv, star = 0.5 * wr + 0.35 * jm + 0.15 * (1 - wo_f), ""
        qual[(r["scenario"], r["q"], r["extractor"])] = {
            "quality": round(qv, 3), "star": star, "judge": round(jm, 3),
            "wr": wr, "wo": wo}
        if jd and jd.get("note"):
            notes[jd["note"]] += 1

    # --- матрица сценарий×экстрактор ---
    print("== quality по сценариям (judge доступен только там, где есть scores) ==")
    hdr = f"{'scenario':<13}" + "".join(f"{e:>14}" for e in ORDER if e in per_ext)
    print(hdr)
    scen_q: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    for (scen, q, ext), v in qual.items():
        scen_q[scen][ext].append(v["quality"])
    for scen, exts in sorted(scen_q.items()):
        cells = []
        for ext in ORDER:
            vals = exts.get(ext)
            if vals:
                star = "*" if any(v["star"] for (s, _q, e), v in qual.items()
                                  if s == scen and e == ext) else ""
                cells.append(f"{statistics.mean(vals):.2f}{star}")
            else:
                cells.append("—")
        print(f"{scen:<13}" + "".join(f"{c:>14}" for c in cells))

    # --- overall ---
    print("\n== overall: качество × скорость × цена ==")
    print(f"{'extractor':<15}{'quality':>9}{'ok%':>7}{'empty%':>8}{'wall_med':>10}{'chars_med':>11}{'цена':>10}")
    rank = []
    for ext in ORDER:
        m = per_ext.get(ext)
        if not m:
            continue
        vals = [v["quality"] for (s, q, e), v in qual.items() if e == ext]
        qmean = statistics.mean(vals) if vals else None
        rank.append((qmean if qmean is not None else -1, ext, m, vals))
    for qmean, ext, m, vals in sorted(rank, reverse=True):
        stars = sum(1 for (s, q, e), v in qual.items() if e == ext and v["star"])
        print(f"{ext:<15}{qmean:>9.2f}{m['ok_pct']*100:>6.0f}%{m['empty_pct']*100:>7.0f}%"
              f"{m['wall_med'] or 0:>9.1f}s{m['chars_med']:>11.0f} {PRICE.get(ext,'?'):>10}"
              + (f"  ({stars} URL judge-only)" if stars else ""))

    # --- гистограмма note ---
    if notes:
        print("\n== частые note джаджа ==")
        for note, n in notes.most_common(15):
            print(f"  {n:>2}× {note}")

    # --- best/worst ---
    print("\n== best/worst сценарий (quality) ==")
    for _qmean, ext, _m, _vals in rank:
        per_scen = {}
        for s, exts in scen_q.items():
            v = exts.get(ext)
            if v:
                per_scen[s] = statistics.mean(v)
        if len(per_scen) > 1:
            best = max(per_scen.items(), key=lambda kv: kv[1])
            worst = min(per_scen.items(), key=lambda kv: kv[1])
            print(f"  {ext:<14} best {best[0]} ({best[1]:.2f})   "
                  f"worst {worst[0]} ({worst[1]:.2f})")
    return 0


if __name__ == "__main__":
    main()
