# wsearch — quota-aware web search for AI agents

One CLI call gives your agent web search and URL reading: 10 search providers
with **local quota tracking** (fallback fires *before* the 429, not after),
**intent-based routing** (docs / research / fact / news / ru / debug / github),
and a **free local-first extraction cascade** that keeps ~80% of fetches off
paid APIs. Python 3 stdlib, zero dependencies, made to be driven by
[Claude Code](https://claude.com/claude-code) (or any agent) via a skill.

```
wsearch search "playwright wait_until domcontentloaded vs networkidle"   # → exa (docs intent)
wsearch search "тарифы yandex vision OCR цена за страницу"               # → youcom (fact intent)
wsearch search "web search agent open source"                            # → gh (github intent, free)
wsearch fetch "https://habr.com/ru/articles/765216/"                     # → local cascade, free
wsearch fetch "https://arxiv.org/pdf/2401.00001" --provider jina         # → PDF specialist
```

## Why this exists

- The built-in WebSearch tool doesn't work from every region and burns a
  quota you can't see or control.
- Free-tier search APIs are plentiful but tiny (100–2000 calls/mo each) — an
  agent needs several, consumed *deliberately*: monthly renewable quotas first
  (they expire — use them), keyless/free modes next, one-off $ grants last.
- Fetch (URL → markdown) is usually routed straight to paid extractors
  (Firecrawl/Tavily), while a local cascade of
  [trafilatura](https://github.com/adbar/trafilatura) → curl_cffi → Playwright
  covers ~80% of pages *better and for free*.

No existing tool did all three, so this repo grew one — every design decision
backed by a benchmark (see [The decision trail](#the-decision-trail)).

## What's inside

| Piece | What it does |
|---|---|
| `web-search` + `engine/` | The CLI (stdlib-only): search, multi (fan-out), fetch, gather, status, chain, usage |
| `local-extract/` | Local extraction cascade (uv project): httpx+trafilatura → curl_cffi → Playwright |
| `skill/` | Claude Code skill (`SKILL.md`) + a ready-to-paste `CLAUDE.md` rule |
| `docs/` | Architecture, provider research, how the router works |
| `bench/` | **Search provider benchmark**: 32 real queries × 8 scenarios × 7 providers → intent routing |
| `bench-extract/` | **Extraction benchmark**: 35 URLs × 9 scenarios × 8 extractors + offline WCXB validation |

### Search providers (order = the quota policy)

| # | Provider | Quota | Notes |
|---|---|---|---|
| 1 | tavily | 1000/mo → keyless | dual-mode: keyed → keyless degrade in the same slot |
| 2 | you.com | 100/day | free MCP, burns daily — spend early |
| 3 | z.ai | 1000/mo | web_search_prime MCP (GLM plan) |
| 4 | exa | ~1400/mo | semantic, best for docs/research (1.53/2 in bench) |
| 5 | brave | 2000/mo | best RU coverage |
| 6 | gh | free (30/min) | native GitHub repo search via the `gh` CLI; first for the github intent |
| 7 | parallel-anon | keyless | anonymous Parallel MCP |
| 8 | linkup | ~4000/mo | big bucket, weak quality — fan-out only |
| 9 | ddg | keyless | scraping floor; anti-bot kills 30/32 under load |
| 10 | parallel | one-off $ grant | last resort |

Fallback is local and deterministic: `state/quotas.json` tracks resets
(monthly/daily), 429s are parsed for reset dates, cooldowns are respected.
Intent detection reorders the chain per query (measured, see
`bench/REPORT.md`) — visible in output as `[intent: docs (auto: ...)]`.

### Fetch cascade (URL → markdown)

`gh` (github.com natively: README/blob/PR/issue/releases via the local
`gh` CLI — private repos too, with your credentials) → `local`
(httpx+trafilatura → curl_cffi → Playwright browser tier; JSON API responses
are returned as pretty-printed text instead of dying in the HTML extractor;
Russian Trusted Root CA is bundled, so *.gov.ru TLS works out of the box) →
`firecrawl` (anti-bot) → `tavily` → `jina` (PDF!) → `parallel`. 30-min cache.
The extraction benchmark showed local wins on articles, docs, RU media and
tables (quality 0.71–0.76 vs 0.33–0.58 for services, median 1.3 s, free);
specialists: **jina for PDFs** (markdown headers from PDF; firecrawl
repetition-loops, tavily blobs), **firecrawl for Cloudflare/anti-bot**, and
*never* parallel for full text (it summarizes with "…" ellipses). Watch out
for tavily: 17% of its "successes" were empty (<200 chars) — the chain treats
short output as failure and falls through.

## The decision trail

This repo is as much about *how the decisions were made* as about the tool.
Internal docs and benchmark reports are in Russian; the numbers speak for
themselves.

1. **Apr 2026 — [searcharvester](https://github.com/vakovalskii/searcharvester)**
   by Valery Kovalskii — self-hosted SearXNG + trafilatura in docker. This is
   where the whole journey started: it worked, then datacenter-IP bans killed
   the search layer. Lesson: scraping floors are fragile; extraction was fine.
2. **Aug 2026 — quota exhaustion of the Z.ai MCP** triggered a rebuild:
   one day to a unified CLI with a local quota counter — the idea that
   inspired this project was
   [syabro/pi-web-search](https://github.com/syabro/pi-web-search) (nice
   provider fallback for Pi agents), extended with quota tracking *before*
   the 429, intent routing, local extraction and telemetry.
3. **bench/ (search)** — 32 queries taken verbatim from a real agent-session
   history (~1150 queries analyzed, 8 scenarios), 7 providers, blind LLM
   judges + hit@3 against gold domains: exa leads docs/semantic (1.75–1.83/2),
   youcom is the most stable (hit@3 94%), tavily takes ru-news, linkup is
   measurably worst (1.11 → demoted), ddg dies to anti-bot (30/32 → last).
   → shipped `--intent` + autodetect (validated 32/32).
4. **local-extract + bench-extract/** — brought extraction back home (from
   the docker grave): a uv-sized cascade instead of an 8 GB stack. Core
   validated offline on WCXB (F1 0.832 ≈ vanilla trafilatura 0.829), then 35
   live URLs × 9 scenarios vs 4 paid/keyless services with snippet-gold
   metrics + LLM judges. → local-first fetch chain, PDF→jina, anti-bot→
   firecrawl rules in the skill, ~80% of fetches free.

## Install

```bash
git clone https://github.com/agent-kreal/agent-web-search && cd agent-web-search
cp .env.example .env && chmod 600 .env   # fill in the keys you have (all optional)
ln -s "$(pwd)/web-search" ~/.local/bin/wsearch
wsearch status                            # should print provider/quota table
```

Optional, for the local extraction cascade with the browser tier:

```bash
cd local-extract && uv sync && uv run python -m local_extract "https://example.com"
```

### Claude Code skill

```bash
mkdir -p ~/.claude/skills/web-search
cp skill/SKILL.md ~/.claude/skills/web-search/SKILL.md
# edit the path in it to point at your clone
```

Then paste the rule from [`skill/CLAUDE.md-snippet.md`](skill/CLAUDE.md-snippet.md)
into your global `~/.claude/CLAUDE.md` — from that moment the agent routes
*all* web search and URL reading through `wsearch`, picking providers by
scenario instead of guessing.

## Benchmarks

- [`bench/REPORT.md`](bench/REPORT.md) — search providers by scenario (RU+EN).
- [`bench-extract/REPORT.md`](bench-extract/REPORT.md) — extractors by page
  type, economics, v2 ideas.
- Both are reproducible: `bench/run_bench.py`, `bench-extract/run_bench.py`
  (resume-safe, throttled, `--json` pipelines included). Vendor datasets are
  fetched by scripts, not stored.

## License & credits

MIT. Inspired by [syabro/pi-web-search](https://github.com/syabro/pi-web-search)
(which is based on code-yeongyu/pi-websearch). Extraction core:
[trafilatura](https://github.com/adbar/trafilatura). Benchmark reference
corpus: [WCXB](https://github.com/Murrough-Foley/web-content-extraction-benchmark).
