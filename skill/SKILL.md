---
name: web-search
description: Unified web search for the agent — CLI `wsearch` with automatic fallback across 10 providers (tavily → zai → exa → brave → gh → parallel-anon → linkup → ddg → youcom-$ → parallel-$), a local quota counter (fallback BEFORE the 429), response schema validation and RRF fusion for multi fan-out. Policy: renewable monthly quotas first, then keyless/free, then the scraping floor; one-off $ grants go last. Use for ALL web search and URL reading (fetch: github.com natively via gh CLI → free local cascade → firecrawl → tavily → jina → parallel-$, 30-min cache) and fan-out research: "search the web", "look up", "research", «поищи», «найди в интернете», «загугли», "find online", "freshness", comparing sources, reading pages, GitHub repo search.
allowed-tools: Bash
---

# Web Search — single entry point `wsearch`

CLI file `/path/to/agent-web-search/web-search`, symlink alias
`~/.local/bin/wsearch` (python3 stdlib, no dependencies — just `wsearch` from
any directory). The router picks a provider, skips quota-exhausted ones and
falls through on errors. Keys live in `/path/to/agent-web-search/.env`
(see `.env.example`).

## Which command when

| Task | Command |
|---|---|
| One search | `wsearch search "query" -n 8` |
| Freshness (news) | `... search "query" --freshness day\|week\|month` |
| 3+ queries on one topic (fan-out, parallel) | `... multi --queries "q1\|q2\|q3"` |
| Read one URL | `... fetch "https://..."` |
| Read several URLs (parallel) | `... gather --urls "u1,u2,u3"` |
| Quota leftovers / health | `... status` |
| Which chain is active now | `... chain` |
| Usage audit (intents, fallbacks, retries) | `... usage [--days 30]` |
| Full JSON (for scripts) | add `--json` |

## Intent routing

The router detects the query scenario and reorders providers
(benchmark `bench/REPORT.md`, v2 re-baseline 10.2026: each has its own
strength). Autodetect by keywords, or set explicitly:
`--intent docs|research|fact|news|ru|debug|github`.

| Scenario | Autodetect cues | Order |
|---|---|---|
| `docs` | api, github, pypi, docs, library | exa → tavily |
| `research` | "vs", comparison, review, best practices | exa → brave |
| `fact` | pricing, rate limit, тариф, цена, стоимость | exa → tavily → brave |
| `news` | --freshness, release, changelog, релиз, новости | ddg → linkup (both RU and EN; anti-bot only hits bursts, a single query is safe) |
| `github` | github, репозиторий, repo, open source | gh → exa → tavily → brave |
| `ru` | cyrillic without special cues | zai → brave → tavily |
| `debug` | error, exception, hangs, regression, «не работает» | tavily → brave |

- Queries with `site:` — exa and parallel-anon move to the end automatically
  (exa fails on them, parallel-anon ignores the operator).
- Quota policy is unchanged: exhausted providers are skipped, fallback works,
  intent only picks the order among the available.
- Output shows `[intent: docs (auto: docs-ish keyword)]` — if autodetect
  missed, force `--intent` or pin `--provider X`.

## Rules

1. **All** web search goes through `wsearch`, not through other MCP/curl.
   Pin a specific provider: `--provider brave`.
2. Russian-language queries are usually fine anywhere; if results are weak,
   retry with `--provider brave`.
3. Don't call `wsearch status`/`chain` without need — they're free but noisy.
4. Quotas are counted locally (`state/quotas.json`): fallback goes to the next
   provider BEFORE hitting a 429. After a real 429 the provider is remembered
   as exhausted until its reset date — that's normal, don't "fix" it.
5. Output is compact: title, URL, snippet — saves context. `--json` when
   machine processing is needed.

## Providers (order: renewable → keyless → floor → one-off grants)

1. `tavily` — 1000 credits/mo (reset on the 1st) → keyless degrade
2. `zai` — 1000/mo from a GLM Coding Plan (RU-friendly)
3. `exa` — ~1400/mo ($10/mo), semantic search, best at docs/research (v2 leader)
4. `brave` — 2000/mo, best for RU queries
5. `gh` — free native GitHub repo search via the local gh CLI
6. `parallel-anon` — anonymous Parallel, keyless
7. `linkup` — ~4000/mo, big bucket — mass fan-out, backup for news
8. `ddg` — scraping floor; anti-bot under bursts — but first for single news queries
9. `youcom` — keyed REST ($100 one-off grant, $5/1k; the free MCP profile was paywalled 10.2026)
10. `parallel` — one-off $ grant — the last resort

Fetch chain: `gh` (github.com natively: README/file/PR/issue/releases, private
repos per gh credentials) → `local` (free cascade httpx+trafilatura →
curl_cffi → playwright, covers ~80% of pages; aliases for --provider:
`local-http`, `local-curl`, `local-browser`) → `firecrawl` (~2000/mo,
anti-bot) → `tavily` (extract) → `jina` (r.jina.ai) → `parallel`
(web_fetch, $-grant — last). 30-min cache (`--no-cache` to bypass,
`wsearch reset fetch-cache` to clean). A service-tier "success" shorter than
200 chars is treated as a fail and the chain falls through automatically —
only real content reaches the cache. Credits are spent only when local
extraction is blocked (anti-bot / IP ban).

## Choosing a fetch provider (benchmark `bench-extract/REPORT.md`)

Default — just `wsearch fetch URL`: the local cascade covers articles / docs /
RU media / tables better than the services (quality 0.71–0.76 vs 0.33–0.58,
free, median 1.3 s). Deliberately pin a provider only for special scenarios:

| Scenario | Command | Why |
|---|---|---|
| PDF link | `wsearch fetch URL --provider jina` | the only one producing markdown headers from a PDF; firecrawl repetition-loops on complex layouts, tavily glues into a blob |
| Cloudflare / anti-bot | `wsearch fetch URL --provider firecrawl` | the only one with real content; tavily/jina return emptiness/challenge pages |
| Need structure from an SPA dump | `wsearch fetch URL --provider jina` | local (browser tier) pulls full content but flat |

- Never `--provider parallel` for full text: it's a summarizer — retells with
  "…" ellipses (~3.7k chars vs 11–25k for the rest).
- A pinned provider's result under 200 chars still falls through to the next
  tier automatically (the 17% empty "successes" of tavily-extract motivated
  the length check) — no manual retry needed.
