# web-search — единый веб-поиск для AI-агента

CLI-файл `web-search` (алиас `wsearch` в `~/.local/bin/` — симлинк, зовётся из
любой папки): один вызов для агента, под капотом — 9 провайдеров в цепочке
фолбэка и локальный счётчик квот, который скипает исчерпанного провайдера
**до** 429, а не после. Python3 stdlib, **ноль зависимостей и venv** — «установка»
закончена, пока папка на месте. Скилл для Claude Code: `~/.claude/skills/web-search/`.

## Предыстория (зачем этот тул)

- Исследование 21.08: `~/Documents/free-web-search-for-agents-2026-08-21.md` —
  три слоя бесплатного поиска (keyless MCP / фри-тиры / скрейпинг), вывод:
  готового тула с фолбэком по квотам не существует, надо собирать свой
  (вариант Б). Уникальная фишка — счётчик остатков квот — реализована здесь.
- До 27.08 стек был разрозненный: MCP web-search-prime (Z.ai, 1000 вызовов/мес
  из GLM Coding Plan — кончились 21.08, ресет 18.09) + отдельный скилл /brave +
  мёртвый SearXNG-скилл. Требование: **один скилл, без MCP, скрипты под капотом**.
- 27.08 тул собран и live-проверен из РФ; старые скиллы и MCP ретированы
  (см. «Что было ретировано»).

## Провайдеры и политика роутинга

Политика (владелец, пересмотрена 27.08 после сверки тарифов с доками):
**сначала вырабатываем возобновляемые месячные квоты (остаток сгорает на
ресете — «use it or lose it»), затем keyless/free-режимы тех же сервисов,
затем бесплатное скрейпинг-дно; разовые $-гранты (не пополняются) — самый
последний рубеж.** Сверка тарифов 27.08: tavily 1000/мес (ресет 1-го числа),
youcom 100/**день** (сгорают ежедневно — потому второй в цепочке), zai 1000/мес
из подписки, exa $10/мес, brave легаси 2000/мес (новым планам дают $5-кредит/мес),
linkup top-up **до** $20/мес (не накапливается), firecrawl 1000–2000/мес.
Разовые гранты: parallel $18.46 (signup; есть и $5/мес recurring, но баланс
в основном разовый — потому весь keyed-слот в конец), youcom keyed $100
(НЗ, закомментирован в .env). Dual-mode провайдер tavily не выпадает из
цепочки при исчерпании keyed-режима — дегрейдится на keyless в том же слоте.

### Search-цепочка

| # | name | квота | режим | заметки |
|---|---|---|---|---|
| 1 | tavily | 1000 кредитов/мес (ресет 1-го) → keyless | keyed→keyless | REST `api.tavily.com/search`; keyless-режим — заголовок `X-Tavily-Access-Mode: keyless`; при 429 в keyed — ретрай keyless в том же вызове |
| 2 | youcom | 100/**день** (сгорают ежедневно) | free | MCP `api.you.com/mcp?profile=free`, тул `you-search`, без ключей; keyed-ключ ($100 разовый кредит) лежит в .env закомментированным — НЗ |
| 3 | zai | 1000/мес (GLM Coding Plan) | keyed | MCP `api.z.ai/api/mcp/web_search_prime/mcp`; тулза `web_search_prime`; 429 содержит «reset at …» — парсится и запоминается (сейчас: исчерпан до 2026-09-18) |
| 4 | exa | $10/мес ≈ 1400 поисков | keyed | REST `api.exa.ai/search`; search $7/1k, +$1/результат сверх 10; `contents.highlights: true` (токен-эффективно, рекомендация Exa для агентов); ключ в UUID-формате с дефисами |
| 5 | brave | 2000/мес (легаси-план; новым — $5-кредит/мес) | keyed | REST `api.search.brave.com`; лучший RU-поклон; ключ также читается из `~/.claude/.brave_api_key` |
| 6 | gh | free (gh CLI, 30 req/min search) | free | `gh api search/repositories` — нативный поиск репо (★/язык/обновление); первым при intent=github (слова «github/репозиторий/repo/open source»); RU-запросы GitHub-поиск не матчит — фолбэк вниз штатный |
| 7 | parallel-anon | безлимит keyless | free | анонимный слот того же Parallel MCP («пониженные» лимиты, generous for hobby) |
| 8 | linkup | top-up до $20/мес ≈ 4000 std | keyed | REST `api.linkup.so/v1/search`; **API дрейфнул**: `q` + `outputType: searchResults\|sourcedAnswer\|structured` (НЕ `query`/`sourcedResults`); deep ≈ 2× цены; при исчерпании 429; понижен 27.08 по бенчу (качество 1.11/2) — большой «бак» для массового fan-out |
| 9 | ddg | безлимит keyless | скрейпинг | POST `html.duckduckgo.com/html/`, браузерный UA, полл 1.5 c; 202 = антибот-челлендж; **30/32 вызовов под серией убиты антиботом (бенч 27.08)** — самый-самый последний |
| 10 | parallel | **$18.46 разовый грант** (+$5/мес recurring) | keyed | MCP `search.parallel.ai/mcp`, Bearer; `web_search` (args: `objective` + **`search_queries` массив!**) + `web_fetch` (до 20 URL/вызов); грант не пополняется — **последний рубеж** |

**Итого возобновляемых: ~12 400 поиск/мес + безлимитное keyless-дно; в резерве — разовые гранты (parallel $18.46, youcom keyed $100). Ноль карт.**

### Fetch-цепочка (URL → markdown)

| # | name | заметки |
|---|---|---|
| 1 | gh | **github.com нативно** через локальный gh CLI (креды владельца): README репо (+шапка ★/lang/desc), файл blob (перебор ref/path для feature-веток + default_branch при мёртвой ветке), PR (+комментарии, диффстат), issue (авто-переход на PR-рендер), releases. Провал/не-поддержанный тип (wiki/orgs/topics) → фолбэк в общий каскад. `matches_url`-предфильтр в router: не-github URL скипаются тихо. Приватные репо — по кредам gh |
| 2 | local | **бесплатный каскад**: httpx+trafilatura (markdown, F1 0.924) → curl_cffi (TLS-имперсонация chrome при блоке) → playwright chromium (SPA). uv-проект `local-extract/`, вызов subprocess-ом; провал (антибот/IP-бан/PDF) → фолбэк ниже. Алиасы для `--provider`: `local-http`, `local-curl`, `local-browser` |
| 3 | firecrawl | REST `api.firecrawl.dev/v1/scrape`, formats: markdown; 1000–2000 кредитов/мес (ресет ~23-го) — возобновляемые; сильны JS-страницы и PDF |
| 4 | tavily | `/extract` (keyed→keyless) |
| 5 | jina | `r.jina.ai/<url>` keyless ~20 RPM, дно |
| 6 | parallel | `web_fetch` — лучшее качество, но тратит $-грант — **последним** |

Кэш fetch-результатов: `state/fetch_cache.json`, TTL 30 мин, до 200 записей,
ключ — нормализованный URL (без utm/fragment). Срабатывает до всей цепочки;
`--no-cache` — мимо кэша, `wsearch reset fetch-cache` — чистка. Локальный
тир всегда тянет до 32k символов, усечение `--max-chars` — на выдаче (кэш
переиспользуется при разных лимитах).

Serper (2500 разово) рассматривался как НЗ — **выброшен 27.08** по решению
владельца (бюджета и без него хватает).

## Intent-роутинг (27.08, по бенчмарку `bench/REPORT.md`)

Роутер детектит сценарий запроса и переупорядочивает цепочку — «кто лучший
в этом сценарии, тот и первый». Квотная политика не меняется: исчерпанные
скипаются как обычно, фолбэк вниз работает, интент лишь выбирает порядок
среди доступных.

| intent | автодетект (ключевые слова) | порядок |
|---|---|---|
| `docs` | api, github, pypi, документация, library | exa → youcom → tavily |
| `research` | «vs», сравнение, обзор, best practices | exa → youcom → brave |
| `fact` | pricing, rate limit, тариф, цена, стоимость | youcom → exa → brave |
| `news` | --freshness, release, changelog, релиз | RU: tavily → youcom → brave; EN: exa → tavily → youcom |
| `github` | github, репозиторий, repo, open source — ищем ПРОЕКТ | gh → exa → youcom → tavily → brave |
| `ru` | кириллица без спец-признаков | youcom → brave → tavily |
| `debug` | error, exception, hangs, regression | tavily → youcom → brave |

Явно: `--intent docs|research|fact|news|ru|debug|github`. Запросы с `site:`
дополнительно скидывают exa (на них пустеет) и parallel-anon (игнорирует
оператор) в конец. Интент виден в шапке вывода: `[intent: docs (auto: …)]`.
Автодетект валидирован на 32 запросах бенч-датасета (32/32, см.
`engine/intent.py`).

## Телеметрия (27.08)

Каждый вызов (search/fetch/multi/gather) пишет строку в `state/usage.jsonl`
(gitignored): intent, источник интента (flag/auto), провайдер, tried-фолбэки
(с причиной и секундами каждой попытки — и при успехе, и при полном отказе
цепочки: `ChainError` несёт `tried`, forced-пин `--provider` виден в поле
`forced`), латентность, ok/ошибка. Аудит:
`wsearch usage [--days 30]` — распределение
по интентам, фолбэки, пустые выдачи, повторы запросов (прокси-сигнал
«первый ответ не помог»). Через месяц: судья-сэмплы живого трафика +
пере-прогон бенча (`bench/run_bench.py`).

## Команды

```bash
wsearch search "query" [-n 8] [--freshness day|week|month] [--provider X] [--intent docs] [--json]
wsearch multi  --queries "q1|q2|q3"        # параллельный fan-out + dedupe по URL
wsearch fetch  "https://..." [--max-chars 6000] [--provider local-browser] [--no-cache]
wsearch gather --urls "u1,u2,u3"           # параллельное чтение (4 потока)
wsearch status [--live]                    # остатки квот; --live: сверка с API провайдеров
wsearch usage [--days 30]                  # аудит использования (интенты, фолбэки, повторы)
wsearch chain                              # активная цепочка (0 запросов)
wsearch reset [provider|fetch-cache]       # сброс счётчиков / чистка кэша
```

Выход: компактный текст (заголовок/URL/сниппет — экономит контекст) или `--json`.
Ошибки — JSON в stderr, exit 1. `--provider` — забронировать конкретного
(повторяемый флаг; алиасы `local-http`/`local-curl`/`local-browser` форсят
ступень локального каскада). `LOCAL_EXTRACT_DISABLE=1` — выключить local-тир
(деградация на сервисную цепочку).

## Квоты: server-truth first (главная фишка)

`state/quotas.json` (v2) — гибрид: серверный снапшот **+** локальный счётчик:

```json
"linkup": {
  "server": {"unit": "usd", "remaining": 19.415, "baseline_used": 44,
             "fetched_at": "…", "limit": null, "period_end": null},
  "local":  {"window_start": "2026-09", "used": 44},
  "exhausted_until": null }
```

Источники серверной истины: **firecrawl** `GET /v2/team/credit-usage`,
**linkup** `GET /v1/credits/balance` (обе — `wsearch status --live`, бесплатные);
**brave** — заголовки `X-RateLimit-*` каждого ответа, пассивно. exa: team-API
требует service-ключ (404 на free tier) — локальный счётчик с sanity-cap 750.
tavily/zai/youcom — API остатков нет, локальный счётчик + их 429.

Правила `quotas.remaining()`: свежий снапшот (≤6 ч) → серверный остаток минус
расход с момента сверки (интерполяция через `baseline_used`); снапшот ≤7 дней —
тот же расчёт с пометкой возраста; старше/нет → локальный счётчик. $-балансы
(linkup) переживают смену окна (baseline ре-анкорится), ресет-квоты
(requests/credits) — снапшот дропается на ролловере. Юниты не смешиваются:
`$19.41 left` / `1711 credits left` / `743 left`.

Дрейф счётчика логируется (`cmd: livecheck` в `state/usage.jsonl`, виден в
`wsearch usage`): первый же замер показал firecrawl −258 credits против
локальной оценки. Свежий серверный остаток > 0 снимает ложный `exhausted_until`
(антидот эпизоду 03.09: 429 rate-limit заглушил exa на месяц при живом балансе).

Роутер (`engine/router.py`) перед вызовом: скип если `exhausted_until` в
будущем или остаток ≤ 0 (`quota at 0 (server|local counter)`). Реальный
429 → `mark_exhausted` (zai — с распарсенной датой сброса из тела ошибки).

Тесты: `python3 -m unittest discover tests` (17 шт. — ledger v2 + парсер
brave-заголовков; реальный `state/` не трогается).

## Layout

```
wsearch                # executable stub (sys.path + engine.cli)
engine/                # stdlib-only, ноль зависимостей
  cli.py               # argparse, вывод, multi/gather (ThreadPoolExecutor)
  router.py            # цепочка, скип по квоте, фолбэк по ошибкам, кэш
  quotas.py            # ledger v2: server-truth + local counter, remaining/status_line
  livecheck.py         # серверная сверка квот (firecrawl/linkup) + лог дрейфа
  fetchcache.py        # кэш fetch-результатов (TTL 30 мин, state/fetch_cache.json)
  mcpclient.py         # минимальный MCP Streamable-HTTP клиент (JSON-RPC)
  config.py            # .env + discovery ключей
  providers/           # по файлу на провайдера + __init__ с цепочками
    base.py            # SearchResult/FetchResult/Provider/QuotaSpec
    local.py           # обёртка subprocess -> local-extract (первый в fetch)
local-extract/         # uv-проект локального каскада (hatchling, src-layout)
  src/local_extract/   # cascade/classify/extract/httpclient/browser/protocol
  .venv/               # gitignored; setup: uv sync && uv run playwright install chromium
state/quotas.json      # счётчики (gitignored)
state/fetch_cache.json # кэш fetch (gitignored)
tests/                 # unittest: ledger v2 + brave-заголовки
.env                   # ключи (chmod 600, gitignored)
```

## Ключи и .env

`.env` рядом с `wsearch`: `TAVILY_API_KEY`, `PARALLEL_API_KEY`, `EXA_API_KEY`,
`LINKUP_API_KEY`, `FIRECRAWL_API_KEY`, `BRAVE_API_KEY`, `ZAI_TOKEN`,
`YOUCOM_API_KEY` (закомментирован, НЗ). Fallback-источники: brave-ключ —
`~/.claude/.brave_api_key`, zai — `mcpServers` из `~/.claude.json` (пока
MCP-конфиг жив).

Гочча .env: **inline-комментарии** в строке значения отрезаются только после
пробел+`#` (чинено 27.08: ключ exa уезжал в заголовок с хвостом `# free …` → 401).

## Гоччи протоколов (учтены в mcpclient.py)

- MCP Streamable HTTP: Accept обязан быть `application/json, text/event-stream`
  **до** initialize.
- Ответ может быть SSE с notifications вперемешку (youcom шлёт notification
  о результатах отдельным event'ом) — парсим data:-строки по нашему id.
- You.com **не выдаёт** `mcp-session-id` — клиент работает без него.
- Parallel `web_search`: аргумент `search_queries` — массив; одиночная строка
  даёт pydantic-ошибку.
- Z.ai 429-тело содержит дату сброса «Your limit will reset at YYYY-MM-DD …»
  (UTC, без зоны) — парсим и запоминаем.

## Что было ретировано 27.08 (и как вернуть)

| Что | Куда делось | Вернуть |
|---|---|---|
| MCP `web-search-prime` (Z.ai) | удалён из `~/.claude.json`; токен → `.env ZAI_TOKEN` | `claude mcp add -s user -t http web-search-prime https://api.z.ai/api/mcp/web_search_prime/mcp --header "Authorization: Bearer <ZAI_TOKEN>"`; бэкап старого конфига: `~/.claude.json.bak-20260827` |
| скилл `/brave` | `~/.claude/skills-disabled/brave-retired-20260827` | mv обратно в `~/.claude/skills/` |
| скилл `/web-search` (SearXNG, июнь) | `~/.claude/skills-disabled/web-search-searxng-retired-20260827` (бэкенд localhost:8000 мёртв с июля) | он не нужен: новый `/web-search` занял имя |
| симлинк `~/.local/bin/brave_search.sh` | удалён | - |

Глобальный `~/.claude/CLAUDE.md` (секция «Веб-поиск») переписан под этот тул.

## Хронология

- **2026-08-21** — исследование (3 сабагента + live-проверки из РФ), отчёт
  в Documents; найдены 4 keyless MCP и фри-тиры; застряло на 5 открытых вопросах.
- **2026-08-27** — реализация за одну сессию: каркас + все адаптеры + счётчик,
  live-тесты каждого провайдера из РФ, регистрации по ходу: Tavily (1000/мес),
  Parallel (ключ от владельца + $18.46), You.com (ключ НЗ), Firecrawl (~2000/мес),
  Exa ($10/мес), Linkup ($20/мес). Z.ai самозапомнился исчерпанным до 18.09.
  Serper выброшен. Ретир brave-скилла и Z.ai MCP, CLAUDE.md и память обновлены.
- **2026-08-27 (вечер)** — локальный fetch: uv-проект `local-extract/`
  (httpx+trafilatura → curl_cffi → playwright, 3 research-сабагента + план),
  провайдер `local` первым в fetch-цепочке, кэш fetch-результатов 30 мин.
  Живые проверки: статика/SSR ~0.5 с через local-http, SPA (excalidraw) —
  browser-тир 3.3 с, Cloudflare (nowsecure.nl) — чистый фолбэк на firecrawl,
  деградация без venv и `LOCAL_EXTRACT_DISABLE=1` — цепочка жива.
- **2026-08-27 (ночь)** — бенчмарк 7 провайдеров на 32 реальных запросах
  (`bench/REPORT.md`: exa/youcom лидеры, linkup понижен, ddg под антиботом),
  intent-роутинг (`--intent` + автодетект, 32/32 валидация), телеметрия
  `usage.jsonl` + `wsearch usage`, переименование CLI в `web-search`
  (алиас `wsearch` в `~/.local/bin`). Git-история с этого дня.
- **2026-09-18** — ожидаемый ресет zai-квоты (поднимется сам, ничего не делать;
  потом прогнать `bench/run_bench.py --providers zai` и вписать в матрицу).

## Связанное

- Отчёт-исследование: `~/Documents/free-web-search-for-agents-2026-08-21.md`
- Скилл: `~/.claude/skills/web-search/SKILL.md`
- Прошлая итерация (eval-harness над SearXNG, июнь): `~/Projects/web-search-tool/`
- Память: `reference_web-search-stack.md`, `project_free-web-search.md`
