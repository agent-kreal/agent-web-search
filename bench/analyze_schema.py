#!/usr/bin/env python3
"""Оффлайн-анализ schema-брака в замороженных выдачах (шаг 4.3 фазы 4).

Считает по провайдерам, сколько записей отфильтровал бы валидатор:
  - no_url       — пустой/без хоста url
  - no_text      — title и snippet оба пустые
  - no_title     — title пуст (snippet есть)
  - no_snippet   — snippet пуст (title есть)
  - short_snip   — snippet < порога (default 200)
Работает поверх raw.jsonl прогона — квоты не тратит.

Запуск: python3 bench/analyze_schema.py --run <dir> [--short 200]
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent


def classify(item: dict, short: int) -> list[str]:
    """Список причин брака записи выдачи (пустой = запись валидна)."""
    reasons = []
    url = (item.get("url") or "").strip()
    try:
        ok_url = bool(urlparse(url).netloc)
    except ValueError:
        ok_url = False
    if not ok_url:
        reasons.append("no_url")
    title = (item.get("title") or "").strip()
    snip = (item.get("snippet") or "").strip()
    if not title and not snip:
        reasons.append("no_text")
    elif not title:
        reasons.append("no_title")
    elif not snip:
        reasons.append("no_snippet")
    elif len(snip) < short:
        reasons.append("short_snip")
    return reasons


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True, help="dir с raw.jsonl")
    ap.add_argument("--short", type=int, default=200,
                    help="порог короткого сниппета (default 200)")
    a = ap.parse_args()

    raw = Path(a.run) / "raw.jsonl"
    # причины брака по провайдерам
    stats: dict[str, dict] = defaultdict(lambda: defaultdict(int))
    # длина сниппета в выдачах по провайдерам (для выбора порога)
    lens: dict[str, list[int]] = defaultdict(list)
    n_items = defaultdict(int)
    for line in raw.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if not r.get("ok"):
            continue
        for item in r.get("results", []):
            n_items[r["provider"]] += 1
            for why in classify(item, a.short):
                stats[r["provider"]][why] += 1
            snip = (item.get("snippet") or "").strip()
            if snip:
                lens[r["provider"]].append(len(snip))

    print(f"{'provider':<13} {'items':>6} " + " ".join(
        f"{w:>10}" for w in ("no_url", "no_text", "no_title", "no_snippet",
                             "short_snip")))
    total = defaultdict(int)
    for prov in sorted(n_items):
        row = stats[prov]
        cells = []
        for w in ("no_url", "no_text", "no_title", "no_snippet", "short_snip"):
            cells.append(f"{row[w]:>10}")
            total[w] += row[w]
        print(f"{prov:<13} {n_items[prov]:>6} " + " ".join(cells))
    print(f"{'TOTAL':<13} {sum(n_items.values()):>6} " + " ".join(
        f"{total[w]:>10}" for w in
        ("no_url", "no_text", "no_title", "no_snippet", "short_snip")))

    # распределение длины сниппетов: где проходит порог
    print(f"\n## доля сниппетов короче порога (по провайдерам)")
    for thr in (100, 150, 200, 300):
        row = []
        for prov in sorted(lens):
            frac = sum(1 for x in lens[prov] if x < thr) / max(1, len(lens[prov]))
            row.append(f"{prov} {frac:.0%}")
        print(f"  <{thr}: " + "; ".join(row))

    out = Path(a.run) / "schema_analysis.json"
    out.write_text(json.dumps({
        "short_threshold": a.short,
        "n_items": n_items,
        "rejects": {p: dict(stats[p]) for p in sorted(stats)},
    }, ensure_ascii=False, indent=2))
    print(f"\n{out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
