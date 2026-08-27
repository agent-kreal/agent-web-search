#!/usr/bin/env python3
"""Часть A: самопроверка ядра local-extract на WCXB (офлайн, без сети).

Гоняет три конфигурации на стратифицированной подвыборке dev-сплита:
  ours-md    — extract_with_metadata с нашими флагами (markdown), как в бою;
               frontmatter срезан (в gold его нет)
  ours-text  — тот же markdown, но strip-нутый в plain text ([x](url) -> x,
               маркеры списков/заголовков/код-fences сняты) — «а если дёшево
               почистить перед отдачей в word-F1»
  vanilla    — trafilatura.extract() без флагов (baseline в нашем окружении;
               сверка с опубликованным 0.958)

Метрики — импортом из wcxb/evaluate.py (word_f1, snippet_check), считаем по
подвыборке (их evaluate_results() берёт весь сплит и нулирует отсутствующие).
Запуск: local-extract/.venv/bin/python bench-extract/run_wcxb.py [--n 300]
"""

from __future__ import annotations

import argparse
import gzip
import json
import random
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent        # repo root
WCXB = ROOT / "bench-extract" / "wcxb"
sys.path.insert(0, str(WCXB))
sys.path.insert(0, str(ROOT / "local-extract" / "src"))

from evaluate import snippet_check, word_f1  # noqa: E402  (wcxb vendor)
from local_extract import extract as exmod   # noqa: E402  (наш модуль)
import trafilatura                            # noqa: E402

TYPE_ORDER = ["article", "forum", "product", "collection",
              "listing", "documentation", "service"]


def strip_markdown(md: str) -> str:
    """Markdown -> plain text (для честного word-F1 против plain-gold)."""
    s = exmod._FRONTMATTER_RE.sub("", md)
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)          # картинки вон
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)      # [x](url) -> x
    s = re.sub(r"```[a-zA-Z0-9_-]*\n?", "", s)          # код-фенсы (тело остаётся)
    s = re.sub(r"^#{1,6}\s*", "", s, flags=re.M)        # заголовки
    s = re.sub(r"^[\s]*[-*+]\s+", "", s, flags=re.M)    # списки
    s = re.sub(r"^>\s?", "", s, flags=re.M)             # цитаты
    s = re.sub(r"[*_`]+", "", s)                        # акценты
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def stratified_ids(n: int) -> list[str]:
    meta = json.loads((WCXB / "metadata.json").read_text())
    by_type: dict[str, list[str]] = defaultdict(list)
    for fid, info in sorted(meta["files"].items()):
        if info["split"] == "dev":
            by_type[info["page_type"]].append(fid)
    total = sum(len(v) for v in by_type.values())
    rng = random.Random(20260827)                      # детерминированно
    picked: list[str] = []
    for _, ids in sorted(by_type.items()):
        k = max(8, round(n * len(ids) / total))        # каждому типу >= 8 стр
        picked += rng.sample(ids, min(k, len(ids)))
    return sorted(picked)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--save", default=str(ROOT / "bench-extract" / "results" / "wcxb-summary.json"))
    args = ap.parse_args()

    ids = stratified_ids(args.n)
    print(f"WCXB dev: {len(ids)} страниц, стратифицированно по {len(TYPE_ORDER)} типам")

    preds = {"ours-md": {}, "ours-text": {}, "vanilla": {}}
    for i, fid in enumerate(ids, 1):
        html = gzip.open(WCXB / "dev" / "html" / f"{fid}.html.gz", "rb").read()
        gt_url = json.loads((WCXB / "dev" / "ground-truth" / f"{fid}.json").read_text()).get("url", "")

        doc = exmod.trafilatura.extract_with_metadata(   # наш боевой вызов
            html, url=gt_url, output_format="markdown",
            include_links=True, include_images=True, include_comments=False)
        md = doc.text if doc else ""
        md = exmod._FRONTMATTER_RE.sub("", md).strip()  # gold без frontmatter
        preds["ours-md"][fid] = md
        preds["ours-text"][fid] = strip_markdown(md)
        preds["vanilla"][fid] = trafilatura.extract(html, url=gt_url) or ""
        if i % 50 == 0:
            print(f"  {i}/{len(ids)}")

    # --- метрики wcxb-кодом, по подвыборке ---
    out = {}
    for cfg, table in preds.items():
        rows = []
        per_type: dict[str, list[float]] = defaultdict(list)
        for fid in ids:
            gt_raw = json.loads((WCXB / "dev" / "ground-truth" / f"{fid}.json").read_text())
            gt = gt_raw.get("ground_truth", {})
            p, r, f1 = word_f1(table[fid], gt.get("main_content", "") or "")
            pt = gt_raw.get("_internal", {}).get("page_type", {}).get("primary", "article")
            rows.append({"f1": f1, "p": p, "r": r,
                         "with": snippet_check(table[fid], gt.get("with", [])),
                         "without": snippet_check(table[fid], gt.get("without", []))})
            per_type[pt].append(f1)
        n = len(rows)
        out[cfg] = {
            "n": n,
            "f1": round(sum(x["f1"] for x in rows) / n, 4),
            "precision": round(sum(x["p"] for x in rows) / n, 4),
            "recall": round(sum(x["r"] for x in rows) / n, 4),
            "with_rate": round(sum(x["with"] for x in rows) / n, 4),
            "without_rate": round(sum(x["without"] for x in rows) / n, 4),
            "per_type": {pt: round(sum(v) / len(v), 4) for pt, v in sorted(per_type.items())},
        }

    print(f"\n{'config':<10} {'F1':>7} {'with↑':>7} {'without↓':>9}")
    for cfg, m in out.items():
        print(f"{cfg:<10} {m['f1']:>7.4f} {m['with_rate']:>7.1%} {m['without_rate']:>9.1%}")
    for cfg in preds:
        print(f"\n{cfg}: per-type F1 — " +
              "  ".join(f"{pt}:{v:.3f}" for pt, v in out[cfg]["per_type"].items()))

    Path(args.save).parent.mkdir(parents=True, exist_ok=True)
    Path(args.save).write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\nсохранено: {args.save}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
