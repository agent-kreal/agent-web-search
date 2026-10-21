#!/usr/bin/env python3
"""Union-pool benchmark v2 (фаза 3 плана improvement-plan-2026-10-19.md).

Три подкоманды:

  build        raw.jsonl прогона -> pools.jsonl (RRF-пул кандидатов на запрос)
               + judge_v2_<scenario>.md файлы для сабагентов-судей
  score        pools.jsonl + scores_v2_*.jsonl (разметка судей) ->
               pooled recall@K / precision@K / quality по провайдерам
  agreement    два набора scores (судья A vs судья B) -> по-URL согласие
               (Cohen's kappa) + Spearman ранкингов провайдеров (шаг 3.4)

RRF: score(u) = sum over providers 1/(60 + rank). Пул = все уникальные
нормализованные URL выдач провайдеров (top-K каждого), судья размечает пул
целиком; золото = T=1 & S=1 (judge-prompt-v2.md).

Повторные вызовы поиска не нужны: build работает поверх уже замороженных
raw.jsonl прогонов (бесплатно).
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

# канон norm_url/RRF_K — engine/merge.py (фаза 4.1): бенч и multi-команда
# используют одну нормализацию, чтобы разметка и слияние не разъезжались
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from engine.merge import RRF_K, norm_url  # noqa: E402

# Порядок вывода в таблицах (как в aggregate.py)
PROVIDERS = ["tavily", "youcom", "zai", "exa", "brave", "linkup",
             "parallel-anon", "ddg"]


def load_raw(run_dir: Path) -> dict[tuple[str, str], list[dict]]:
    """(scenario, query) -> список записей прогонов (по одной на провайдера)."""
    by_q: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for line in (run_dir / "raw.jsonl").read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        by_q[(r["scenario"], r["query"])].append(r)
    return by_q


def cmd_build(run_dir: Path, top: int) -> int:
    by_q = load_raw(run_dir)
    pools_out = []
    scen_qs: dict[str, list[dict]] = defaultdict(list)

    for (scenario, query), recs in sorted(by_q.items()):
        issued: dict[str, list[str]] = {}
        cand: dict[str, dict] = {}  # norm_url -> {url, title, snippet, rrf, ranks}
        for r in recs:
            if not r.get("ok"):
                continue
            urls, ranks = [], {}
            for rank, item in enumerate(r.get("results", [])[:top], 1):
                nu = norm_url(item["url"])
                if not nu:
                    continue
                if nu not in ranks:          # дубликаты внутри одной выдачи
                    ranks[nu] = rank
                    urls.append(nu)
                c = cand.setdefault(nu, {"url": item["url"],
                                         "title": item.get("title") or "",
                                         "snippet": (item.get("snippet") or "")[:300],
                                         "rrf": 0.0, "ranks": {}})
                c["rrf"] += 1.0 / (RRF_K + rank)
                c["ranks"][r["provider"]] = rank
            if urls:
                issued[r["provider"]] = urls
        pool = sorted(cand.values(), key=lambda c: -c["rrf"])
        q_idx = len(scen_qs[scenario]) + 1
        row = {"scenario": scenario, "query": query, "q": q_idx,
               "pool": pool, "issued": issued}
        pools_out.append(row)
        scen_qs[scenario].append(row)

    pools_path = run_dir / "pools.jsonl"
    with pools_path.open("w") as f:
        for row in pools_out:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # judge-файлы: по сценарию, кандидаты без имён провайдеров (полная слепота)
    for scenario, rows in sorted(scen_qs.items()):
        lines = [f"# scenario: {scenario} (union-pool v2)\n"]
        for row in rows:
            lines.append(f"\n## Q{row['q']}: {row['query']}\n")
            for i, c in enumerate(row["pool"], 1):
                lines.append(f"C{i}. {c['title']}")
                lines.append(f"   {c['url']}")
                if c["snippet"]:
                    lines.append(f"   {c['snippet']}")
                lines.append("")
        (run_dir / f"judge_v2_{scenario}.md").write_text("\n".join(lines))

    n_urls = sum(len(r["pool"]) for r in pools_out)
    print(f"{len(pools_out)} queries, {n_urls} pool URLs "
          f"(mean {n_urls / max(1, len(pools_out)):.1f}/query)")
    print(f"pools: {pools_path}")
    print(f"judge files: {run_dir}/judge_v2_<scenario>.md "
          f"({len(scen_qs)} scenarios)")
    return 0


def load_scores(run_dir: Path, pattern: str = "scores_v2_*.jsonl",
                exclude: str | None = None) -> dict[tuple[str, int], dict[int, dict]]:
    """(scenario, q) -> {cand_idx: {T,S,A}}; exclude отфильтровывает второй
    набор судей по суффиксу имени файла (для agreement)."""
    marks: dict[tuple[str, int], dict[int, dict]] = defaultdict(dict)
    for f in sorted(run_dir.glob(pattern)):
        if exclude and f.name.startswith(exclude):
            continue
        for line in f.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            marks[(r["scenario"], r["q"])][r["c"]] = {"T": r["T"], "S": r["S"],
                                                      "A": r["A"]}
    return marks


def load_pools(run_dir: Path) -> list[dict]:
    return [json.loads(l) for l in (run_dir / "pools.jsonl").read_text().splitlines()
            if l.strip()]


def _spearman(a: list[float], b: list[float]) -> float:
    if len(a) < 3:
        return float("nan")

    def ranks(xs):
        order = sorted(range(len(xs)), key=lambda i: xs[i])
        rk = [0.0] * len(xs)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                rk[order[k]] = avg
            i = j + 1
        return rk

    ra, rb = ranks(a), ranks(b)
    ma, mb = statistics.mean(ra), statistics.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    da = sum((x - ma) ** 2 for x in ra) ** 0.5
    db = sum((y - mb) ** 2 for y in rb) ** 0.5
    return num / (da * db) if da and db else float("nan")


def provider_metrics(pools: list[dict], marks, top: int,
                     weights=(0.4, 0.4, 0.2)) -> dict:
    """pooled recall@top / precision@top / quality по провайдерам + union-RRF."""
    w_t, w_s, w_a = weights
    per_prov: dict[str, dict] = defaultdict(
        lambda: {"rec": [], "prec": [], "q": []})
    gold_empty = []
    n_q = 0

    for row in pools:
        key = (row["scenario"], row["q"])
        if key not in marks:
            continue
        n_q += 1
        m = marks[key]
        gold, scored = set(), {}
        for i, c in enumerate(row["pool"], 1):
            if i in m:
                rel = m[i]["T"] == 1 and m[i]["S"] == 1
                if rel:
                    gold.add(c["url"])
                scored[c["url"]] = w_t * m[i]["T"] + w_s * m[i]["S"] + w_a * m[i]["A"]
        if not gold:
            gold_empty.append(f"{row['scenario']}/Q{row['q']}")
            continue

        for prov, urls in row["issued"].items():
            k_urls = [u for u in urls[:top] if u in scored]
            hit = sum(1 for u in k_urls if u in gold)
            st = per_prov[prov]
            st["rec"].append(hit / len(gold))
            st["prec"].append(hit / len(k_urls) if k_urls else 0.0)
            st["q"].extend(scored[u] for u in urls if u in scored)
        # референс: сам RRF-ранг
        rrf_urls = [c["url"] for c in row["pool"][:top] if c["url"] in scored]
        hit = sum(1 for u in rrf_urls if u in gold)
        st = per_prov["union-rrf"]
        st["rec"].append(hit / len(gold))
        st["prec"].append(hit / len(rrf_urls) if rrf_urls else 0.0)
        st["q"].extend(scored[u] for u in rrf_urls)

    out = {}
    for prov, st in per_prov.items():
        out[prov] = {
            "recall": statistics.mean(st["rec"]) if st["rec"] else None,
            "precision": statistics.mean(st["prec"]) if st["prec"] else None,
            "quality": statistics.mean(st["q"]) if st["q"] else None,
            "n": len(st["rec"]),
        }
    return {"providers": out, "n_q": n_q, "gold_empty": gold_empty}


def cmd_score(run_dir: Path, top: int) -> int:
    pools = load_pools(run_dir)
    marks = load_scores(run_dir, exclude="scores_v2_j2_")
    if not marks:
        print("нет scores_v2_*.jsonl — сначала судьи (judge-prompt-v2.md)")
        return 1
    res = provider_metrics(pools, marks, top)
    provs = [p for p in PROVIDERS if p in res["providers"]] + \
            [p for p in res["providers"] if p not in PROVIDERS]
    print(f"судейство: {res['n_q']} запросов (из {len(pools)}); "
          f"gold-empty: {len(res['gold_empty'])}"
          + (f" {res['gold_empty']}" if res["gold_empty"] else ""))
    print(f"\n{'provider':<13} {'R@' + str(top):>6} {'P@' + str(top):>6} {'quality':>8} {'n':>4}")
    rows = sorted(provs, key=lambda p: -(res["providers"][p]["recall"] or 0))
    for p in rows:
        m = res["providers"][p]
        r = f"{m['recall']:.2f}" if m["recall"] is not None else "—"
        pr = f"{m['precision']:.2f}" if m["precision"] is not None else "—"
        q = f"{m['quality']:.3f}" if m["quality"] is not None else "—"
        print(f"{p:<13} {r:>6} {pr:>6} {q:>8} {m['n']:>4}")

    # по сценариям (recall)
    print("\n## recall по сценариям")
    scen = sorted({p["scenario"] for p in pools})
    print(f"{'scenario':<13} " + " ".join(f"{p[:9]:>9}" for p in rows))
    for s in scen:
        sp = [p for p in pools if p["scenario"] == s]
        sub = provider_metrics(sp, marks, top)
        cells = []
        for p in rows:
            m = sub["providers"].get(p)
            cells.append(f"{m['recall']:.2f}" if m and m["recall"] is not None else "—")
        print(f"{s:<13} " + " ".join(f"{c:>9}" for c in cells))

    out_path = run_dir / "union_metrics.json"
    out_path.write_text(json.dumps(
        {"top": top, **{k: v for k, v in res.items() if k != "providers"},
         "ranking": {p: res["providers"][p] for p in rows}},
        ensure_ascii=False, indent=2))
    print(f"\nmetrics: {out_path}")
    return 0


def cmd_agreement(run_dir: Path, top: int, a_glob: str, b_glob: str) -> int:
    """3.4: согласие двух судей — kappa по бинарной релевантности (T∧S)
    и Spearman ранкингов провайдеров по pooled recall."""
    pools = load_pools(run_dir)
    ma = load_scores(run_dir, a_glob, exclude="scores_v2_j2_")
    mb = load_scores(run_dir, b_glob)
    keys = sorted(set(ma) & set(mb))
    if not keys:
        print(f"нет пересечения разметок ({a_glob} vs {b_glob})")
        return 1

    agree = [0, 0, 0, 0]  # [both-rel, both-nonrel, a-only, b-only]
    for k in keys:
        for c in set(ma[k]) & set(mb[k]):
            ra = ma[k][c]["T"] == 1 and ma[k][c]["S"] == 1
            rb = mb[k][c]["T"] == 1 and mb[k][c]["S"] == 1
            agree[0 if ra and rb else 1 if not ra and not rb
                  else 2 if ra else 3] += 1
    n = sum(agree)
    if n == 0:
        print("пустое пересечение по кандидатам")
        return 1
    po = (agree[0] + agree[1]) / n
    pa = (agree[0] + agree[2]) / n          # доля rel у A
    pb = (agree[0] + agree[3]) / n          # доля rel у B
    pe = pa * pb + (1 - pa) * (1 - pb)
    kappa = (po - pe) / (1 - pe) if pe < 1 else float("nan")

    ra = provider_metrics([p for p in pools if (p["scenario"], p["q"]) in ma],
                          ma, top)["providers"]
    rb = provider_metrics([p for p in pools if (p["scenario"], p["q"]) in mb],
                          mb, top)["providers"]
    common = [p for p in PROVIDERS if p in ra and p in rb]
    rho = _spearman([ra[p]["recall"] for p in common],
                    [rb[p]["recall"] for p in common]) if len(common) >= 3 else float("nan")

    print(f"пересечение: {len(keys)} запросов, {n} кандидатов")
    print(f"по-URL согласие: {po:.1%} (rel у A {pa:.1%}, у B {pb:.1%})")
    print(f"кандидаты: оба rel {agree[0]}, оба nonrel {agree[1]}, "
          f"только A {agree[2]}, только B {agree[3]}")
    print(f"Cohen's kappa (T∧S): {kappa:.3f}")
    print(f"Spearman recall-ранкингов ({len(common)} провайдеров): {rho:.3f}")
    flags = []
    if kappa < 0.6:
        flags.append(f"kappa {kappa:.2f} < 0.6 — разметка спорная")
    if rho < 0.8:
        flags.append(f"Spearman {rho:.2f} < 0.8 — ранкинг неустойчив")
    print("\n".join("⚠ " + f for f in flags) if flags else "согласие в норме")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("build", "score", "agreement"):
        s = sub.add_parser(name)
        s.add_argument("--run", required=True, help="dir с raw.jsonl/pools.jsonl")
        s.add_argument("--top", type=int, default=5,
                       help="top-K выдачи провайдера в пул (default 5)")
        if name == "agreement":
            s.add_argument("--a", default="scores_v2_*.jsonl",
                           help="glob набора судьи A")
            s.add_argument("--b", default="scores_v2_j2_*.jsonl",
                           help="glob набора судьи B (второй судья)")
    a = ap.parse_args()
    run_dir = Path(a.run)
    if a.cmd == "build":
        return cmd_build(run_dir, a.top)
    if a.cmd == "score":
        return cmd_score(run_dir, a.top)
    return cmd_agreement(run_dir, a.top, a.a, a.b)


if __name__ == "__main__":
    sys.exit(main())
