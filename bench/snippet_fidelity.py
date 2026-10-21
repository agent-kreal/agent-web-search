#!/usr/bin/env python3
"""Snippet-fidelity spot-check (шаг 3.6 плана improvement-plan-2026-10-19.md).

Проверяем, что сниппеты провайдеров честные: на 20 случайных (провайдер, url,
snippet) парах из raw.jsonl фетчим страницу (wsearch fetch, local-first) и
fuzzy-ищем сниппет в контенте.

Usage:
    python3 bench/snippet_fidelity.py --run <dir> [--n 20] [--seed 42]

Вердикт на пару (после нормализации: NFKC, lowercase, кавычки/тире — к
простым, дата-префиксы DDG срезаны):
  present — сниппет найден в контенте: подстрока первых 60 симв. ИЛИ
            longest-common-substring >= 70% длины сниппета (верстка markdown
            вокруг выдержки может отличаться)
  partial — LCS >= 45% (пересказ/лёгкая правка, но узнаваем)
  absent  — сниппета в контенте нет (галлюцинация, устаревший кэш провайдера
            или динамическая страница — курс/статус на момент индексации)
Итог: доля present+partial по провайдерам. Артефакт: fidelity.jsonl рядом.
"""
from __future__ import annotations

import argparse
import difflib
import json
import random
import re
import subprocess
import sys
import time
import unicodedata
from collections import defaultdict
from pathlib import Path

WSEARCH = Path(__file__).resolve().parent.parent / "web-search"
_WS = re.compile(r"\s+")


_DATE_PREFIX = re.compile(r"^[a-zа-я]{3}\.? \d{1,2}, \d{4} [-—] ", re.I)


def norm(s: str) -> str:
    """lowercase, юникод-NFKC, схлопнутые пробелы; «…»/кавычки — к простым."""
    s = unicodedata.normalize("NFKC", s or "").lower()
    s = (s.replace("…", "...").replace("«", '"').replace("»", '"')
          .replace("“", '"').replace("”", '"').replace("‘", "'")
          .replace("’", "'").replace("—", "-").replace("–", "-"))
    s = _WS.sub(" ", s).strip()
    s = _DATE_PREFIX.sub("", s)          # DDG/Google дата-префикс сниппета
    return s.strip(". ").strip("... ")


def verdict(snippet: str, content: str) -> str:
    ns, nc = norm(snippet), norm(content)
    if not ns:
        return "skip"
    if ns[:60] in nc:
        return "present"
    # longest common substring: сниппет-выдержка должна найтись почти целиком,
    # даже если экстрактор переверстал markdown вокруг неё
    m = difflib.SequenceMatcher(None, nc, ns, autojunk=False).find_longest_match(
        0, len(nc), 0, len(ns))
    cov = m.size / len(ns)
    if cov >= 0.7:
        return "present"
    if cov >= 0.45:
        return "partial"
    return "absent"


def fetch(url: str) -> str:
    p = subprocess.run([str(WSEARCH), "fetch", url, "--json",
                        "--max-chars", "60000"],
                       capture_output=True, text=True, timeout=120)
    if p.returncode != 0:
        return ""
    try:
        return json.loads(p.stdout).get("content") or ""
    except json.JSONDecodeError:
        return ""


def main() -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("--run", required=True, type=Path, help="dir с raw.jsonl")
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()

    pairs = []
    for line in (a.run / "raw.jsonl").read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if not r.get("ok"):
            continue
        for item in r.get("results", []):
            sn = (item.get("snippet") or "").strip()
            if len(sn) >= 60:  # короткие не информативны для проверки
                pairs.append({"provider": r["provider"],
                              "scenario": r["scenario"],
                              "url": item["url"], "snippet": sn})
    random.Random(a.seed).shuffle(pairs)
    pairs = pairs[:a.n]
    print(f"{len(pairs)} пар на проверку (seed {a.seed})")

    out_path = a.run / "fidelity.jsonl"
    with out_path.open("w") as f:
        for i, pr in enumerate(pairs, 1):
            t0 = time.time()
            content = fetch(pr["url"])
            v = verdict(pr["snippet"], content) if content else "fetch-fail"
            rec = {**pr, "verdict": v, "content_len": len(content),
                   "wall_sec": round(time.time() - t0, 1)}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            print(f"[{i:2}/{len(pairs)}] {pr['provider']:<13} {v:<10} "
                  f"{rec['wall_sec']:>5}s  {pr['url'][:60]}", flush=True)

    rows = [json.loads(l) for l in out_path.read_text().splitlines() if l.strip()]
    by_prov: dict[str, list[str]] = defaultdict(list)
    for r in rows:
        # честная проверка только там, где страница реально вытащена:
        # короткий контент = фейл экстрактора, а не ложь сниппета
        if r["verdict"] in ("fetch-fail", "skip") or r["content_len"] < 2000:
            by_prov[r["provider"]].append("thin")
        else:
            by_prov[r["provider"]].append(r["verdict"])
    print(f"\n{'provider':<13} {'present':>8} {'partial':>8} {'absent':>7} {'thin':>5}  honest% (checked)")
    for p, vs in sorted(by_prov.items(), key=lambda x: -len(x[1])):
        n_ok = sum(1 for v in vs if v == "present")
        n_part = sum(1 for v in vs if v == "partial")
        n_abs = sum(1 for v in vs if v == "absent")
        n_thin = sum(1 for v in vs if v == "thin")
        checked = n_ok + n_part + n_abs
        honest = (n_ok + n_part) / checked * 100 if checked else 0
        h = f"{honest:.0f}%" if checked else "—"
        print(f"{p:<13} {n_ok:>8} {n_part:>8} {n_abs:>7} {n_thin:>5}  {h} ({checked})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
