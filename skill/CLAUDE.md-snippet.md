# Snippet for the global ~/.claude/CLAUDE.md

Paste this into `~/.claude/CLAUDE.md` (and copy `skill/SKILL.md` to
`~/.claude/skills/web-search/SKILL.md`, fixing the repo path). Adjust the
provider list to the keys you actually have — everything you don't configure
is skipped automatically.

```markdown
# Web search

For ANY web search and URL reading use the `wsearch` CLI (python3 stdlib, no
dependencies; repo at /path/to/agent-web-search, symlink ~/.local/bin/wsearch,
callable from any directory). No MCP, no curl, no built-in WebSearch.

Chain with automatic fallback and a local quota counter. Policy: renewable
monthly quotas first (they expire on reset — burn them), then keyless/free and
the scraping floor, one-off $ grants — the very last.
Search: tavily(1000/mo) → youcom(100/day) → zai(1000/mo) → exa(~1400/mo) →
brave(2000/mo) → parallel-anon → linkup(~4000/mo) → ddg-scrape →
parallel($-grant, last).
Fetch (URL→markdown): local cascade (free, ~80% of pages — articles/docs/RU
media beat the services) → firecrawl(~2000/mo, anti-bot) → tavily → jina →
parallel($-grant, last). Pinpoints: PDF → `--provider jina`,
anti-bot/CF → `--provider firecrawl` (benchmark bench-extract/REPORT.md).

Commands: `wsearch search "q" [-n N] [--freshness day|week|month]
[--provider X] [--intent docs|research|fact|news|ru|debug] [--json]`,
`wsearch multi --queries "q1|q2|q3"` (fan-out), `wsearch fetch URL`,
`wsearch gather --urls "u1,u2"`, `wsearch status` (quota leftovers),
`wsearch usage` (audit: intents/fallbacks/retries). The router autodetects the
scenario (docs/research → exa, facts → youcom, RU news → tavily, debug
strings → tavily) and reorders providers — benchmark bench/REPORT.md; the
intent is shown in the output header.

When the user says "search the web", "look up", "research", «поищи»,
«найди в интернете», «загугли» — use the `/web-search` skill (full rules in
its SKILL.md).

Never use the built-in WebSearch tool; don't work around it with curl/MCP.
```
