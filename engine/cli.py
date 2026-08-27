"""CLI: wsearch <search|fetch|gather|multi|status|chain> ...

Design follows the old searchkit.py contract:
  - clean JSON to stdout (--json / default compact text), errors to stderr
  - exit codes: 0 ok, 1 runtime, 2 usage
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from . import fetchcache, intent as intent_mod, quotas, router, usage
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


def _log_search(query, out, t0, *, err=None, intent=None, intent_source=None,
                freshness=None):
    """One usage.jsonl line per real search call (ok or failed)."""
    usage.log({
        "cmd": "search", "query": query, "intent": intent,
        "intent_source": intent_source, "freshness": freshness,
        "provider": (out or {}).get("provider"),
        "tried": (out or {}).get("tried", []),
        "n_results": len((out or {}).get("results", [])),
        "wall_sec": round(time.time() - t0, 2), "ok": err is None,
        **({"error": str(err)[:200]} if err else {}),
    })


def cmd_search(a) -> int:
    t0 = time.time()
    ikey, isrc, ireason = intent_mod.resolve(a.query, a.freshness, a.intent)
    try:
        out = router.search(a.query, n=a.n, freshness=a.freshness,
                            providers=a.provider, intent=ikey)
    except RuntimeError as e:
        _log_search(a.query, None, t0, err=e, freshness=a.freshness,
                    intent=ikey, intent_source=isrc)
        raise
    _log_search(a.query, out, t0, freshness=a.freshness,
                intent=ikey, intent_source=isrc)
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


def cmd_fetch(a) -> int:
    t0 = time.time()
    try:
        res = router.fetch(a.url, max_chars=a.max_chars, providers=a.provider,
                           use_cache=not a.no_cache)
    except RuntimeError as e:
        usage.log({"cmd": "fetch", "url": a.url, "provider": None, "tried": [],
                   "cached": False, "n_results": 0,
                   "wall_sec": round(time.time() - t0, 2), "ok": False,
                   "error": str(e)[:200]})
        raise
    usage.log({"cmd": "fetch", "url": a.url, "provider": res["provider"],
               "tried": res.get("tried", []),
               "cached": res.get("cached", False),
               "n_results": 1 if res["result"].content else 0,
               "wall_sec": round(time.time() - t0, 2), "ok": True})
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
    with ThreadPoolExecutor(max_workers=min(4, len(urls))) as ex:
        futs = {ex.submit(router.fetch, u, max_chars=a.max_chars,
                          use_cache=not a.no_cache): u for u in urls}
        for fut in as_completed(futs):
            u = futs[fut]
            try:
                res = fut.result()
                docs[u] = {"provider": res["result"].provider or res["provider"],
                           "title": res["result"].title,
                           "content": res["result"].content,
                           "cached": res.get("cached", False)}
                usage.log({"cmd": "fetch", "url": u, "provider": res["provider"],
                           "tried": res.get("tried", []),
                           "cached": res.get("cached", False), "n_results": 1,
                           "wall_sec": round(time.time() - starts[u], 2), "ok": True})
            except RuntimeError as e:
                docs[u] = {"error": str(e)}
                usage.log({"cmd": "fetch", "url": u, "provider": None, "tried": [],
                           "cached": False, "n_results": 0,
                           "wall_sec": round(time.time() - starts[u], 2),
                           "ok": False, "error": str(e)[:200]})
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
    all_results: list = []
    per_q = {}
    starts = {q: time.time() for q in queries}
    resolved = {q: intent_mod.resolve(q, a.freshness, a.intent) for q in queries}

    def _one(q):
        ikey, _, _ = resolved[q]
        return router.search(q, n=a.n, freshness=a.freshness,
                             providers=a.provider, intent=ikey)

    with ThreadPoolExecutor(max_workers=min(4, len(queries))) as ex:
        futs = {ex.submit(_one, q): q for q in queries}
        for fut in as_completed(futs):
            q = futs[fut]
            ikey, isrc, _ = resolved[q]
            try:
                out = fut.result()
                per_q[q] = {"provider": out["provider"], "count": len(out["results"]),
                            "intent": ikey}
                all_results.extend(out["results"])
                _log_search(q, out, starts[q], freshness=a.freshness,
                            intent=ikey, intent_source=isrc)
            except RuntimeError as e:
                per_q[q] = {"error": str(e)}
                _log_search(q, None, starts[q], err=e, freshness=a.freshness,
                            intent=ikey, intent_source=isrc)
    # dedupe by URL preserving order
    seen, uniq = set(), []
    for r in all_results:
        if r.url not in seen:
            seen.add(r.url)
            uniq.append(r)
    if a.json:
        print(json.dumps({"queries": per_q, "results": [r.to_dict() for r in uniq]},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"# multi-search ({len(queries)} queries, {len(uniq)} unique)")
    for q, info in per_q.items():
        print(f"#   {q!r}: {info}")
    lines, _ = _compact(uniq)
    for l in lines:
        print(l)
    return 0


def cmd_status(a) -> int:
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
            "quota": quotas.status_line(p.name, p.quota.limit, p.quota.period, p.quota.label),
            "can_fetch": p.can_fetch,
        })
    if a.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    print(f"{'provider':<10} {'status':<12} quota")
    for r in rows:
        st = "ok" if r["available"] else "no key"
        print(f"{r['provider']:<10} {st:<12} {r['quota']}")
    return 0


def cmd_chain(a) -> int:
    """Show the effective chain without querying anything (quota-free)."""
    out = router.search("", dry_chain=True, providers=a.provider)
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
    f.add_argument("--provider", action="append",
                   help="force provider(s): firecrawl, jina, local, "
                        "local-http/local-curl/local-browser (cascade step)")
    f.add_argument("--no-cache", action="store_true",
                   help="bypass the fetch cache (read and write)")
    f.add_argument("--json", action="store_true")
    f.set_defaults(fn=cmd_fetch)

    g = sub.add_parser("gather", help="multiple URLs -> markdown (parallel)")
    g.add_argument("--urls", required=True, help="comma-separated")
    g.add_argument("--max-chars", type=int, default=4000)
    g.add_argument("--no-cache", action="store_true")
    g.add_argument("--json", action="store_true")
    g.set_defaults(fn=cmd_gather)

    m = sub.add_parser("multi", help="fan-out queries (parallel) + dedupe")
    m.add_argument("--queries", required=True, help="queries separated by |")
    m.add_argument("-n", type=int, default=8)
    m.add_argument("--freshness", choices=["day", "week", "month"], default=None)
    m.add_argument("--provider", action="append",
                   help="pin provider(s) for all queries (repeatable)")
    m.add_argument("--intent", choices=["docs", "research", "fact", "news", "ru", "debug", "github"],
                   help="routing intent for ALL queries (default: autodetect per query)")
    m.add_argument("--json", action="store_true")
    m.set_defaults(fn=cmd_multi)

    st = sub.add_parser("status", help="quota ledger + provider health")
    st.add_argument("--json", action="store_true")
    st.set_defaults(fn=cmd_status)

    ch = sub.add_parser("chain", help="show effective chain (no requests)")
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
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
