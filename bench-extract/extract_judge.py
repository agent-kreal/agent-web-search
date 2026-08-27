#!/usr/bin/env python3
"""Материал для LLM-джаджа: results/judge_<scenario>.md по raw.jsonl.

На каждый URL — блоки всех экстракторов (фиксированный порядок): метаданные
(wall, chars, tier, сниппет-скоры, структура-признаки) + head 1800 + mid 1200.
Фейлы — ERROR, пустые — (empty).

Запуск: python3 bench-extract/extract_judge.py [--scenario X]
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from grade import snippet_metrics, structure_feats  # noqa: E402 — тот же каталог

BENCH = Path(__file__).resolve().parent
RAW = BENCH / "results" / "raw.jsonl"
DATASET = BENCH / "dataset.jsonl"
OUTDIR = BENCH / "results"

ORDER = ["local-auto", "local-http", "local-curl", "local-browser",
         "firecrawl", "tavily", "jina", "parallel"]
HEAD_CUT, MID_CUT = 1800, 1200


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario")
    args = ap.parse_args()

    rows = {(r["scenario"], r["q"]): r for r in
            (json.loads(l) for l in DATASET.read_text().splitlines() if l.strip())}
    recs = [json.loads(l) for l in RAW.read_text().splitlines() if l.strip()]

    by_scen: dict[str, dict] = defaultdict(dict)
    for r in recs:
        by_scen[r["scenario"]].setdefault(r["q"], {})[r["extractor"]] = r

    for scen, byq in sorted(by_scen.items()):
        if args.scenario and scen != args.scenario:
            continue
        out = [f"# scenario: {scen}", ""]
        for q in sorted(byq):
            row = rows[(scen, q)]
            out.append(f"## U{q}: {row['url']}")
            out.append(f"_(note: {row['note']})_")
            out.append("")
            for ext in ORDER:
                r = byq[q].get(ext)
                if r is None:
                    out.append(f"**[{ext}]** — не прогонялся (для parallel — норм, если нет пометки)")
                    out.append("")
                    continue
                if not r["ok"]:
                    out.append(f"**[{ext}]** ERROR: {(r.get('error') or '')[:120]}")
                    out.append("")
                    continue
                sm = snippet_metrics(r, row)
                feats = structure_feats(r)
                tag = (f"**[{ext}]** ({r['wall_sec']}s, {r['chars']} chars"
                       + (f", tier {r['tier']}" if r.get("tier") else "")
                       + f"; wr={sm['with_recall']}, wo={sm['without_rate']}"
                       + f"; hdr {feats['headers']}, code {feats['codeblocks']}"
                         f", links {feats['links']}, lists {feats['lists']})")
                body = (r.get("head") or "")[:HEAD_CUT]
                mid = (r.get("mid") or "")[:MID_CUT]
                text = body + ("\n\n[…середина…]\n\n" + mid if mid else "")
                if r["chars"] < 200:
                    text = "(пустой вывод, <200 симв.)"
                out.append(tag)
                out.append("```")
                out.append(text)
                out.append("```")
                out.append("")
        p = OUTDIR / f"judge_{scen}.md"
        p.write_text("\n".join(out), encoding="utf-8")
        print(f"{p} ({len(byq)} URL)")
    return 0


if __name__ == "__main__":
    main()
