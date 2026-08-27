#!/usr/bin/env python3
"""Объективные метрики части B из results/raw.jsonl (без LLM).

- по экстрактору: ok%, empty% (ok, но <200 симв.), median/p90 wall, median chars
- матрица сценарий×экстрактор: ok% + median chars
- сниппет-метрики: with_recall (доля обязательных фраз в экстракте — по head+mid,
  нормализация: только буквы/цифры/одинарные пробелы) и without_rate (бойлерплейт)
- local-auto: распределение финальных тиров по сценариям
- структура-признаки по head+mid: заголовки, код-блоки, ссылки, списки

Выход: stdout + results/grade.json (для aggregate.py).
Запуск: python3 bench-extract/grade.py [--extractor X]
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
from collections import defaultdict
from pathlib import Path

BENCH = Path(__file__).resolve().parent
RAW = BENCH / "results" / "raw.jsonl"
DATASET = BENCH / "dataset.jsonl"
OUT = BENCH / "results" / "grade.json"

EMPTY_CHARS = 200
EXTRACTORS = ["local-auto", "local-http", "local-curl", "local-browser",
              "firecrawl", "tavily", "jina", "parallel"]


def norm(s: str) -> str:
    """Слабая нормализация для матчинга сниппетов: буквы/цифры/пробелы, lower.
    Разметочные артефакты убираем ДО общей зачистки, иначе они разрывают фразы:
    firecrawl вставляет экранированные &lt;br&gt; переносы (джадж article-en),
    tavily-PDF хранит дефисы переносов ("re-ceptors"), entities дают мусорные
    токены ("nbsp", "mdash"). Правила симметричны для фразы и текста."""
    s = re.sub(r"&lt;br\s*/?\s*&gt;", " ", s, flags=re.I)       # экранированный <br>
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)               # настоящий <br>
    s = re.sub(r"&[a-zA-Z][a-zA-Z0-9]*;|&#\d+;", " ", s)       # прочие entities
    s = re.sub(r"([a-zа-яё])-([a-zа-яё])", r"\1\2", s)         # дефис-склейка (PDF)
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)       # картинки
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)   # [x](url) -> x
    s = re.sub(r"[^0-9A-Za-zА-Яа-яЁё]+", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def snippet_metrics(rec: dict, row: dict) -> dict:
    hay = norm((rec.get("head") or "") + " " + (rec.get("mid") or ""))
    out = {}
    for field, name in (("with", "with_recall"), ("without", "without_rate")):
        phrases = row.get(field) or []
        if not phrases:
            out[name] = None
            continue
        found = sum(1 for p in phrases if norm(p) in hay)
        out[name] = round(found / len(phrases), 3)
    return out


def structure_feats(rec: dict) -> dict:
    text = (rec.get("head") or "") + "\n" + (rec.get("mid") or "")
    return {
        "headers": len(re.findall(r"^#{1,6}\s", text, re.M)),
        "codeblocks": text.count("```"),
        "links": len(re.findall(r"\]\(", text)),
        "lists": len(re.findall(r"^\s*[-*+]\s", text, re.M)),
    }


def pct(a: int, b: int) -> str:
    return f"{a / b * 100:.0f}%" if b else "—"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--extractor", help="только один экстрактор")
    args = ap.parse_args()

    rows = {r["url"]: r for r in
            (json.loads(l) for l in DATASET.read_text().splitlines() if l.strip())}
    recs = [json.loads(l) for l in RAW.read_text().splitlines() if l.strip()]
    if args.extractor:
        recs = [r for r in recs if r["extractor"] == args.extractor]

    per_ext: dict[str, list] = defaultdict(list)
    for r in recs:
        per_ext[r["extractor"]].append(r)

    report: dict[str, dict] = {}
    print(f"{'extractor':<15} {'ok':>7} {'empty':>7} {'wall_med':>9} {'wall_p90':>9} {'chars_med':>10}")
    for ext in EXTRACTORS:
        rs = per_ext.get(ext, [])
        if not rs:
            continue
        oks = [r for r in rs if r["ok"]]
        empty = [r for r in oks if r["chars"] < EMPTY_CHARS]
        walls = sorted(r["wall_sec"] for r in rs if isinstance(r.get("wall_sec"), (int, float)))
        chars = sorted(r["chars"] for r in oks) or [0]
        p90 = walls[int(len(walls) * 0.9)] if walls else None
        m = {"n": len(rs), "ok": len(oks), "ok_pct": round(len(oks) / len(rs), 3),
             "empty": len(empty), "empty_pct": round(len(empty) / len(rs), 3),
             "wall_med": statistics.median(walls) if walls else None,
             "wall_p90": p90, "chars_med": statistics.median(chars)}
        # сниппеты и структура — по строкам
        snip_w, snip_wo, feats = [], [], []
        for r in rs:
            sm = snippet_metrics(r, rows.get(r["url"], {}))
            if sm["with_recall"] is not None:
                snip_w.append(sm["with_recall"])
            if sm["without_rate"] is not None:
                snip_wo.append(sm["without_rate"])
            if r["ok"]:
                feats.append(structure_feats(r))
        if snip_w:
            m["with_recall"] = round(statistics.mean(snip_w), 3)
            m["with_n"] = len(snip_w)
        if snip_wo:
            m["without_rate"] = round(statistics.mean(snip_wo), 3)
            m["without_n"] = len(snip_wo)
        if feats:
            m["feats"] = {k: round(statistics.mean(f[k] for f in feats), 1) for k in feats[0]}
        report[ext] = m
        print(f"{ext:<15} {pct(len(oks), len(rs)):>7} {pct(len(empty), len(rs)):>7} "
              f"{m['wall_med'] or 0:>8.1f}s {p90 or 0:>8.1f}s {m['chars_med']:>10.0f}")
        if "with_recall" in m:
            print(f"{'':<15} with_recall {m['with_recall']:.1%} (n={m['with_n']})   "
                  f"without_rate {m.get('without_rate', 0):.1%} (n={m.get('without_n', 0)})   "
                  f"feats {m.get('feats')}")

    # матрица сценарий×экстрактор
    print("\n== ok% / median chars по сценариям ==")
    hdr = f"{'scenario':<13}" + "".join(f"{e:>16}" for e in EXTRACTORS if e in report)
    print(hdr)
    matrix = {}
    scen_recs: dict[tuple, list] = defaultdict(list)
    for r in recs:
        scen_recs[(r["scenario"], r["extractor"])].append(r)
    for scen in dict.fromkeys(r["scenario"] for r in recs):
        matrix[scen] = {}
        cells = []
        for ext in report:
            rs = scen_recs.get((scen, ext), [])
            if not rs:
                cells.append(f"{'—':>16}")
                continue
            oks = [r for r in rs if r["ok"]]
            chars = statistics.median([r["chars"] for r in oks]) if oks else 0
            cell = f"{pct(len(oks), len(rs))} {chars:>6.0f}"
            cells.append(f"{cell:>16}")
            matrix[scen][ext] = {"ok_pct": round(len(oks) / len(rs), 3), "chars_med": chars}
        print(f"{scen:<13}" + "".join(cells))

    # tier-распределение local-auto
    tiers = defaultdict(lambda: defaultdict(int))
    for r in recs:
        if r["extractor"] == "local-auto":
            t = r.get("tier") or ("fail" if not r["ok"] else "?")
            tiers[r["scenario"]][t] += 1
    if tiers:
        print("\n== local-auto: финальные тиры по сценариям ==")
        for scen, td in tiers.items():
            print(f"  {scen:<13} " + "  ".join(f"{k}:{v}" for k, v in sorted(td.items())))

    # ошибки
    fails = defaultdict(list)
    for r in recs:
        if not r["ok"]:
            fails[r["extractor"]].append(f"{r['scenario']}/{r['q']}: {(r.get('error') or '')[:80]}")
    if fails:
        print("\n== фейлы ==")
        for ext, fl in sorted(fails.items()):
            print(f"  {ext} ({len(fl)}):")
            for f in fl[:12]:
                print(f"    {f}")

    OUT.write_text(json.dumps({"per_ext": report, "matrix": matrix}, indent=2, ensure_ascii=False))
    print(f"\nсохранено: {OUT}")
    return 0


if __name__ == "__main__":
    main()
