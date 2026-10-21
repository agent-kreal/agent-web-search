#!/usr/bin/env python3
"""Заморозка полных копий страниц для фазы 1 (умная резка) — прогон 19.10.

Один раз собирает content (до 32k) для всех URL bench-extract/dataset.jsonl:
сначала local (free), при фейле — firecrawl (тратит кредиты только там, где
local не справляется: pdf/spa-app/antibot). Дальше все повторы фазы 1
(резка/judge/подбор max-chars) гоняются по файлу — без API и трат квот
(search_evals-подход: outputs per-run).

Выход: bench-results/runs/2026-10-19-phase0/frozen_content.jsonl
Запуск: python3 bench-extract/freeze_content.py
"""
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "bench-extract" / "dataset.jsonl"
OUT = ROOT / "bench-results" / "runs" / "2026-10-19-phase0" / "frozen_content.jsonl"


def fetch(url: str, provider: str) -> dict | None:
    cmd = [str(ROOT / "web-search"), "fetch", url, "--provider", provider,
           "--max-chars", "32768", "--no-cache", "--json"]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    except subprocess.TimeoutExpired:
        return None
    if p.returncode != 0:
        return None
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return None


def main() -> int:
    rows = [json.loads(l) for l in DATASET.read_text().splitlines() if l.strip()]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as fout:
        for r in rows:
            d = fetch(r["url"], "local")
            provider = "local"
            if not d or not (d.get("content") or "").strip():
                d = fetch(r["url"], "firecrawl")
                provider = "firecrawl"
            content = (d or {}).get("content") or ""
            rec = {"q": r["q"], "scenario": r["scenario"], "url": r["url"],
                   "provider": provider, "chars": len(content),
                   "content": content}
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(f"[{r['q']:>2}] {provider:<9} {len(content):>6}  {r['url'][:60]}")
            time.sleep(1.0)
    print(f"\nfrozen: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
