"""CLI: wsearch <search|fetch|gather|multi|status|chain> ...

Design follows the old searchkit.py contract:
  - clean JSON to stdout (--json / default compact text), errors to stderr
  - exit codes: 0 ok, 1 runtime, 2 usage
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from . import backfill as backfill_mod
from . import fetchcache, intent as intent_mod, merge, quotas, router, usage
from .providers import FETCH_CHAIN, SEARCH_CHAIN


def _compact(results, seen_urls=None):
    lines = []
    seen = seen_urls if seen_urls is not None else set()
    for r in results:
        if r.url in seen:
            continue
        seen.add(r.url)
        head = r.title or r.url
        meta = f" [{r.date}]" if r.date else ""
        lines.append(f"{head}{meta}\n  {r.url}" + (f"\n  {r.snippet[:300]}" if r.snippet else ""))
    return lines, seen


def _tried(out, err) -> list:
    """Attempts to log: from a successful result, or carried by ChainError
    (the audit 09.09: failed invocations logged tried=[] and hid which
    providers errored vs were skipped)."""
    if out is not None:
        return out.get("tried", [])
    return getattr(err, "tried", None) or []


def _log_search(query, out, t0, *, err=None, intent=None, intent_source=None,
                freshness=None, forced=None):
    """One usage.jsonl line per real search call (ok or failed)."""
    usage.log({
        "cmd": "search", "query": query, "intent": intent,
        "intent_source": intent_source, "freshness": freshness,
        **({"forced": forced} if forced else {}),
        "provider": (out or {}).get("provider"),
        "tried": _tried(out, err),
        "n_results": len((out or {}).get("results", [])),
        # фаза 4.3: сколько записей сняла schema-валидация (поле только
        # когда брак был — компактный лог)
        **({"n_rejected": out["rejected"]}
           if out and out.get("rejected") else {}),
        "wall_sec": round(time.time() - t0, 2), "ok": err is None,
        **({"error": str(err)[:400]} if err else {}),
    })


def cmd_search(a) -> int:
    t0 = time.time()
    ikey, isrc, ireason = intent_mod.resolve(a.query, a.freshness, a.intent)
    try:
        out = router.search(a.query, n=a.n, freshness=a.freshness,
                            providers=a.provider, intent=ikey)
    except RuntimeError as e:
        _log_search(a.query, None, t0, err=e, freshness=a.freshness,
                    intent=ikey, intent_source=isrc, forced=a.provider)
        raise
    _log_search(a.query, out, t0, freshness=a.freshness,
                intent=ikey, intent_source=isrc, forced=a.provider)
    if a.json:
        print(json.dumps({
            "intent": ikey, "intent_source": isrc,
            "provider": out["provider"],
            "results": [r.to_dict() for r in out["results"]],
            "tried": out["tried"],
        }, ensure_ascii=False, indent=2))
        return 0
    lines, _ = _compact(out["results"])
    tag = f" [intent: {ikey} ({isrc}: {ireason})]" if ikey else ""
    print(f"# web-search: {a.query!r} — via {out['provider']}{tag}")
    for l in lines:
        print(l)
    if out["tried"]:
        for t in out["tried"]:
            w = t.get("wall_sec")
            ttag = f" ({w}s)" if w else ""
            print(f"[skip] {t['name']}{ttag}: {t['error']}", file=sys.stderr)
    return 0


def _warn_injections(url: str, findings: list) -> None:
    """BrowseSafe-фаза 2: предупреждение в stderr — найденные в fetched-контенте
    инъекции (удалённые и флагнутые) не должны проходить молча."""
    if not findings:
        return
    kinds: dict[str, int] = {}
    for f in findings:
        k = f"{f['action']}:{f['kind']}"
        kinds[k] = kinds.get(k, 0) + 1
    detail = ", ".join(f"{k}×{v}" for k, v in sorted(kinds.items()))
    print(f"⚠ injection flags [{url}]: {detail}", file=sys.stderr)
    for f in findings[:3]:
        print(f"  · {f['action']:6} {f['kind']}: {f['evidence'][:100]!r}",
              file=sys.stderr)


def cmd_fetch(a) -> int:
    t0 = time.time()
    raw_cut = a.raw_cut or os.environ.get("WS_RAW_CUT") == "1"
    try:
        res = router.fetch(a.url, max_chars=a.max_chars, providers=a.provider,
                           use_cache=not a.no_cache, raw_cut=raw_cut)
    except RuntimeError as e:
        usage.log({"cmd": "fetch", "url": a.url, "provider": None,
                   "tried": _tried(None, e),
                   **({"forced": a.provider} if a.provider else {}),
                   "cached": False, "n_results": 0,
                   "wall_sec": round(time.time() - t0, 2), "ok": False,
                   "error": str(e)[:400]})
        raise
    usage.log({"cmd": "fetch", "url": a.url, "provider": res["provider"],
               "tried": res.get("tried", []),
               "cached": res.get("cached", False),
               "n_results": 1 if res["result"].content else 0,
               "wall_sec": round(time.time() - t0, 2), "ok": True})
    _warn_injections(a.url, res.get("sanitize") or [])
    fr = res["result"]
    cached = res.get("cached", False)
    if a.json:
        print(json.dumps({"provider": fr.provider or res["provider"], "url": fr.url,
                          "title": fr.title, "content": fr.content,
                          "cached": cached},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"# fetch: {fr.url} — via {fr.provider or res['provider']}"
          + (" (cached)" if cached else ""))
    print(f"# title: {fr.title}")
    print(fr.content)
    return 0


def cmd_gather(a) -> int:
    urls = [u.strip() for u in a.urls.split(",") if u.strip()]
    docs = {}
    starts = {u: time.time() for u in urls}
    raw_cut = a.raw_cut or os.environ.get("WS_RAW_CUT") == "1"
    with ThreadPoolExecutor(max_workers=min(4, len(urls))) as ex:
        futs = {ex.submit(router.fetch, u, max_chars=a.max_chars,
                          use_cache=not a.no_cache, raw_cut=raw_cut): u for u in urls}
        for fut in as_completed(futs):
            u = futs[fut]
            try:
                res = fut.result()
                docs[u] = {"provider": res["result"].provider or res["provider"],
                           "title": res["result"].title,
                           "content": res["result"].content,
                           "cached": res.get("cached", False)}
                _warn_injections(u, res.get("sanitize") or [])
                usage.log({"cmd": "fetch", "url": u, "provider": res["provider"],
                           "tried": res.get("tried", []),
                           "cached": res.get("cached", False), "n_results": 1,
                           "wall_sec": round(time.time() - starts[u], 2), "ok": True})
            except RuntimeError as e:
                docs[u] = {"error": str(e)}
                usage.log({"cmd": "fetch", "url": u, "provider": None,
                           "tried": _tried(None, e),
                           **({"forced": a.provider} if a.provider else {}),
                           "cached": False, "n_results": 0,
                           "wall_sec": round(time.time() - starts[u], 2),
                           "ok": False, "error": str(e)[:400]})
    if a.json:
        print(json.dumps(docs, ensure_ascii=False, indent=2))
        return 0
    for u, d in docs.items():
        print(f"===== {u} =====")
        if "error" in d:
            print(f"[error] {d['error']}")
        else:
            tag = " (cached)" if d.get("cached") else ""
            print(f"# via {d['provider']}{tag} — {d['title']}")
            print(d["content"][:a.max_chars])
        print()
    return 0


def cmd_multi(a) -> int:
    queries = [q.strip() for q in a.queries.split("|") if q.strip()]
    per_q = {}
    bf_info: dict = {"triggered": False}
    starts: dict[str, float] = {q: time.time() for q in queries}
    resolved = {q: intent_mod.resolve(q, a.freshness, a.intent) for q in queries}

    def _one(q):
        ikey, _, _ = resolved.get(q) or intent_mod.resolve(q, a.freshness, a.intent)
        return router.search(q, n=a.n, freshness=a.freshness,
                             providers=a.provider, intent=ikey)

    # выдача каждого запроса (каскад = 1 провайдер) отдельным списком —
    # фаза 4.1: ранг результата = RRF по спискам, а не порядок потоков
    lists: dict[str, list] = {q: [] for q in queries}

    def _fanout(qs: list[str]) -> None:
        with ThreadPoolExecutor(max_workers=min(4, len(qs))) as ex:
            futs = {ex.submit(_one, q): q for q in qs}
            for fut in as_completed(futs):
                q = futs[fut]
                ikey, isrc, _ = resolved.get(q) or intent_mod.resolve(
                    q, a.freshness, a.intent)
                try:
                    out = fut.result()
                    per_q[q] = {"provider": out["provider"], "count": len(out["results"]),
                                "intent": ikey}
                    lists[q] = out["results"]
                    _log_search(q, out, starts[q], freshness=a.freshness,
                                intent=ikey, intent_source=isrc, forced=a.provider)
                except RuntimeError as e:
                    per_q[q] = {"error": str(e)}
                    _log_search(q, None, starts[q], err=e, freshness=a.freshness,
                                intent=ikey, intent_source=isrc, forced=a.provider)

    _fanout(queries)

    def _rrf(all_queries: list[str]) -> list[dict]:
        merged = merge.rrf_merge(
            [[r.to_dict() for r in lists.get(q, [])] for q in all_queries],
            source_names=all_queries)
        return [m.to_dict() for m in merged]

    if a.no_rrf:
        # эскейп к поведению до 4.1: конкатенация в порядке запросов + dedupe
        # (детерминированная версия старого)
        seen, uniq = set(), []
        for q in queries:
            for r in lists.get(q, []):
                if r.url not in seen:
                    seen.add(r.url)
                    uniq.append(r.to_dict())
        merged_dicts = uniq
        n_uniq = len(merged_dicts)
    else:
        merged_dicts = _rrf(queries)
        n_uniq = len(merged_dicts)

    # фаза 4.2: adaptive backfill — только фейл-триггер (по итогу ревью
    # 19.10: покрытие/домены срезаны по данным probe — шумовой X портил топ);
    # доборный круг из 2 переформулировок по терму фейл-запроса
    if not a.no_rrf and not a.no_backfill:
        failed = [q for q in queries if "error" in per_q.get(q, {})]
        trig, reason = backfill_mod.should_backfill(failed)
        if trig:
            ikey0 = resolved[queries[0]][0]
            bf_queries = backfill_mod.backfill_queries(failed, ikey0)
            bf_info = {"triggered": True, "reason": reason, "queries": bf_queries}
            for q in bf_queries:
                starts[q] = time.time()
                resolved[q] = intent_mod.resolve(q, a.freshness, a.intent)
            _fanout(bf_queries)
            merged_dicts = _rrf(queries + bf_queries)
            n_uniq = len(merged_dicts)

    if a.json:
        print(json.dumps({"queries": per_q, "backfill": bf_info,
                          "results": merged_dicts},
                         ensure_ascii=False, indent=2))
        return 0
    mode = "concat+dedupe (--no-rrf)" if a.no_rrf else "RRF"
    print(f"# multi-search ({len(queries)} queries, {n_uniq} unique, {mode})")
    for q, info in per_q.items():
        print(f"#   {q!r}: {info}")
    if bf_info["triggered"]:
        print(f"# backfill: {bf_info['reason']} → {bf_info['queries']}")
    for d in merged_dicts:
        head = d["title"] or d["url"]
        meta = f" [{d['date']}]" if d.get("date") else ""
        via = f" [{d['provider']}]" if d.get("provider") else ""
        print(f"{head}{meta}{via}\n  {d['url']}" +
              (f"\n  {d['snippet'][:300]}" if d.get("snippet") else ""))
    return 0


def cmd_status(a) -> int:
    live = None
    if getattr(a, "live", False):
        from . import livecheck
        live = livecheck.run()
    rows = []
    seen_names = set()
    for p in SEARCH_CHAIN + FETCH_CHAIN:
        if p.name in seen_names:
            continue
        seen_names.add(p.name)
        rows.append({
            "provider": p.name,
            "available": p.available(),
            "reason": p.available_reason or "",
            "quota": quotas.status_line(p.name, p.quota.limit, p.quota.period,
                                        p.quota.label, unit=p.quota.unit,
                                        price=p.quota.price),
            "can_fetch": p.can_fetch,
        })
    if a.json:
        out = rows if live is None else {"livecheck": live, "status": rows}
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    print(f"{'provider':<10} {'status':<12} quota")
    for r in rows:
        st = "ok" if r["available"] else "no key"
        print(f"{r['provider']:<10} {st:<12} {r['quota']}")
    if live is not None:
        print("# livecheck (server truth vs local estimate):")
        for l in live:
            if not l["ok"]:
                print(f"#   {l['provider']:<10} ERROR: {l['error']}")
                continue
            def _v(x, unit):
                return f"${x:.2f}" if unit == "usd" else (
                    f"{round(x)}" if x is not None else "?")
            drift = ("?" if l["drift"] is None
                     else _v(l["drift"], l["unit"]))
            print(f"#   {l['provider']:<10} server {_v(l['server_remaining'], l['unit'])}"
                  f" | local est {_v(l['local_estimated'], l['unit'])}"
                  f" | drift {drift}")
    return 0


def cmd_chain(a) -> int:
    """Show the effective chain without querying anything (quota-free)."""
    # --intent: показать порядок для сценария (пустой запрос → «news»
    # резолвится в news-en, кириллицы нет)
    intent = intent_mod.resolve("", forced=a.intent)[0] if a.intent else None
    out = router.search("", dry_chain=True, providers=a.provider, intent=intent)
    if a.json:
        print(json.dumps(out["chain"], ensure_ascii=False, indent=2))
        return 0
    print("# search chain:")
    for c in out["chain"]:
        mark = "  ✓" if not c["skip"] else f"  ✗ {c['skip']}"
        print(f"  {c['name']:<10}{mark}")
    print("# fetch chain: " + ", ".join(p.name for p in FETCH_CHAIN if p.can_fetch))
    return 0


def cmd_reset(a) -> int:
    if a.provider == "fetch-cache":
        fetchcache.clear()
        print("fetch cache cleared")
        return 0
    quotas.reset(a.provider)
    print(f"quota state reset: {a.provider or 'ALL'}")
    return 0


def cmd_usage(a) -> int:
    if a.json:
        print(json.dumps(usage.summary(a.days), ensure_ascii=False, indent=2))
        return 0
    usage.print_summary(a.days)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="wsearch",
                                 description="Unified web search for agents (multi-provider with quota-aware fallback)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="single query through the fallback chain")
    s.add_argument("query")
    s.add_argument("-n", type=int, default=8, help="max results (default 8)")
    s.add_argument("--freshness", choices=["day", "week", "month"], default=None)
    s.add_argument("--provider", action="append", help="force provider(s), e.g. --provider brave")
    s.add_argument("--intent", choices=["docs", "research", "fact", "news", "ru", "debug", "github"],
                   help="routing intent (default: autodetect from the query)")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_search)

    f = sub.add_parser("fetch", help="single URL -> markdown (local cascade first)")
    f.add_argument("url")
    f.add_argument("--max-chars", type=int, default=6000)
    f.add_argument("--raw-cut", action="store_true",
                   help="blind [:max-chars] cut (pre-19.10 behavior); "
                        "default cuts on sentence/paragraph boundaries")
    f.add_argument("--provider", action="append",
                   help="force provider(s): firecrawl, jina, local, "
                        "local-http/local-curl/local-browser (cascade step)")
    f.add_argument("--no-cache", action="store_true",
                   help="bypass the fetch cache (read and write)")
    f.add_argument("--json", action="store_true")
    f.set_defaults(fn=cmd_fetch)

    g = sub.add_parser("gather", help="multiple URLs -> markdown (parallel)")
    g.add_argument("--urls", required=True, help="comma-separated")
    # фаза 5.3: frontier фазы 1 — 4000 на грани (−15% recall против 6000),
    # плато 6–12k; выравниваем с fetch-дефолтом
    g.add_argument("--max-chars", type=int, default=6000)
    g.add_argument("--raw-cut", action="store_true",
                   help="blind [:max-chars] cut (pre-19.10 behavior)")
    g.add_argument("--no-cache", action="store_true")
    g.add_argument("--json", action="store_true")
    g.set_defaults(fn=cmd_gather)

    m = sub.add_parser("multi", help="fan-out queries (parallel) + RRF merge")
    m.add_argument("--queries", required=True, help="queries separated by |")
    m.add_argument("-n", type=int, default=8)
    m.add_argument("--freshness", choices=["day", "week", "month"], default=None)
    m.add_argument("--provider", action="append",
                   help="pin provider(s) for all queries (repeatable)")
    m.add_argument("--intent", choices=["docs", "research", "fact", "news", "ru", "debug", "github"],
                   help="routing intent for ALL queries (default: autodetect per query)")
    m.add_argument("--no-rrf", action="store_true",
                   help="pre-4.1 merge: concat in query order + URL dedupe")
    m.add_argument("--no-backfill", action="store_true",
                   help="disable the adaptive backfill round (4.2)")
    m.add_argument("--json", action="store_true")
    m.set_defaults(fn=cmd_multi)

    st = sub.add_parser("status", help="quota ledger + provider health")
    st.add_argument("--live", action="store_true",
                    help="refresh server-side quotas first (free endpoints, "
                         "firecrawl/linkup) and show counter drift")
    st.add_argument("--json", action="store_true")
    st.set_defaults(fn=cmd_status)

    ch = sub.add_parser("chain", help="show effective chain (no requests)")
    ch.add_argument("--intent", choices=["docs", "research", "fact", "news", "ru", "debug", "github"])
    ch.add_argument("--provider", action="append")
    ch.add_argument("--json", action="store_true")
    ch.set_defaults(fn=cmd_chain)

    rs = sub.add_parser("reset", help="reset local quota counters (wsearch reset [provider])")
    rs.add_argument("provider", nargs="?", default=None)
    rs.set_defaults(fn=cmd_reset)

    us = sub.add_parser("usage", help="usage telemetry summary (intents, providers, repeats)")
    us.add_argument("--days", type=int, default=30, help="lookback window (default 30)")
    us.add_argument("--json", action="store_true")
    us.set_defaults(fn=cmd_usage)

    a = ap.parse_args(argv)
    try:
        return a.fn(a)
    except RuntimeError as e:
        err = {"error": str(e)}
        tried = getattr(e, "tried", None)
        if tried:  # ChainError: attempts visible to the caller, no re-runs needed
            err["tried"] = tried
        print(json.dumps(err, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
