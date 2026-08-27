#!/usr/bin/env python3
"""Extract top-3 results per (query, provider) into compact judge files.

Output: bench/results/judge_<scenario>.md — one file per scenario, every
query followed by 7 provider blocks (top-3: title / url / snippet trimmed).
These files are what the judge (LLM or human) grades: relevance 0/1/2 per
item + hit@3 against the gold domain.

Usage: python3 bench/extract_top.py [--k 3]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

BENCH = Path(__file__).resolve().parent
RAW = BENCH / "results" / "raw.jsonl"
OUT_DIR = BENCH / "results"

AD_MARKERS = ("duckduckgo.com/y.js", "ad_domain=", "bing.com/aclick")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=3)
    args = ap.parse_args()

    rows = [json.loads(l) for l in RAW.read_text().splitlines() if l.strip()]

    by_scen: dict[str, dict[str, dict[str, dict]]] = defaultdict(dict)
    for r in rows:
        if not r["ok"]:
            continue
        items = [x for x in r.get("results", [])
                 if not any(m in x.get("url", "") for m in AD_MARKERS)][:args.k]
        by_scen[r["scenario"]].setdefault(r["query"], {})[r["provider"]] = {
            "wall": r["wall_sec"], "items": items,
        }

    OUT_DIR.mkdir(exist_ok=True)
    for scen, queries in sorted(by_scen.items()):
        lines = [f"# scenario: {scen}", ""]
        for qi, (query, provs) in enumerate(queries.items(), 1):
            lines.append(f"## Q{qi}: {query}")
            for prov in ["tavily", "youcom", "exa", "brave", "linkup",
                         "parallel-anon", "ddg"]:
                d = provs.get(prov)
                if d is None:
                    lines.append(f"**[{prov}]** ERROR/absent")
                    lines.append("")
                    continue
                lines.append(f"**[{prov}]** ({d['wall']:.1f}s)")
                if not d["items"]:
                    lines.append("(no results)")
                for j, it in enumerate(d["items"], 1):
                    title = (it.get("title") or "")[:110]
                    url = it.get("url", "")[:150]
                    snip = (it.get("snippet") or "").replace("\n", " ")[:280]
                    lines.append(f"{j}. {title}\n   {url}\n   {snip}")
                lines.append("")
        out = OUT_DIR / f"judge_{scen}.md"
        out.write_text("\n".join(lines))
        print(f"{scen:<13} {len(queries)} queries -> {out.name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
