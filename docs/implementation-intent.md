# План внедрения: intent-роутинг (Б+В) + телеметрия (Г) + переименование

Дата: 27.08. Основание: `bench/REPORT.md` §6 (рекомендации утверждены владельцем).
Цель: «недетерминированный» роутинг — агент (или CLI сам) выбирает стартовый
порядок провайдеров по сценарию запроса; всё логируется для месячного аудита.

> **СТАТУС: ВЫПОЛНЕН полностью 27.08** (все этапы ниже отмечены сделанными;
> коммиты: rename → telemetry → chain → intent routing). Валидация автодетекта
> 32/32; живой smoke: playwright-запрос через intent=docs отдал официальную
> доку playwright.dev первой строкой (в бенче её не давал никто, кроме exa).

## Этап 0 — переименование + симлинк (~10 мин)

- [ ] `wsearch` → `web-search` (mv внутри репо)
- [ ] симлинк `~/.local/bin/wsearch` → `<repo>/web-search`
      (короткий вызов из любой директории, обратная совместимость)
- [ ] обновить упоминания: SKILL.md, ~/.claude/CLAUDE.md, README.md,
      docs/how-it-works.md, bench/run_bench.py, память (reference_web-search-stack.md)
- [ ] smoke: `wsearch chain` + `<repo>/web-search chain`

## Этап 1 — телеметрия Г: usage.jsonl + команда usage (~50 строк)

- [ ] `engine/usage.py`: append-only `state/usage.jsonl`, строка на вызов:
      `{ts, cmd, query, intent, intent_source: flag|auto|none, provider,
        tried: [{name, error, wall_sec}], freshness, n_results, wall_sec, ok}`
      (27.08 вечером: tried обогащён причинами и ценой каждой попытки);
      ротация при >5 МБ (→ .1)
- [ ] хук в cli.py: search/fetch/multi/gather пишут факт (fetch: url вместо query)
- [ ] команда `usage [--days 30] [--json]`: по интентам/провайдерам — вызовы,
      фолбэки (tried непустой), error-rate, пустые выдачи, медиана latency,
      топ повторов запросов (прокси-сигнал «не помогло»)
- [ ] конфид: файл локальный, права как у quotas.json; в .gitignore уже есть state/

## Этап 2 — правка цепочки (точечные, из REPORT §6.3) (~5 строк)

- [ ] SEARCH_CHAIN: linkup вниз (после parallel-anon):
      tavily → youcom → zai → exa → brave → parallel-anon → linkup → ddg → parallel-$
- [ ] ddg — комментарий «последний рубеж, антибот под серией» (решение владельца)

## Этап 3 — Б: флаг `--intent` (~40 строк)

- [ ] таблица INTENT_CHAINS в router.py (перестановки SEARCH_CHAIN по REPORT §6.1):
      - `docs`   → exa → youcom → tavily → …
      - `research` → exa → youcom → brave → …
      - `fact`   → youcom → exa → brave → …
      - `news`   → ru-язык: tavily → youcom → brave / en: exa → tavily → …
      - `ru`     → youcom → brave → tavily → …
      - `debug`  → tavily → youcom → brave → … (exa в конец)
      - site:-режим: exa и parallel-anon в конец (внутри автодетекта/роутера)
- [ ] флаг `--intent` на `search` и `multi`; квотная логика не меняется:
      исчерпанные скипаются как обычно, фолбэк вниз работает
- [ ] неизвестный intent → дефолтная цепочка + предупреждение

## Этап 4 — В: автодетект интента (~60 строк)

- [ ] `engine/intent.py: detect(query, freshness) -> (intent|None, reason)`:
      - `site:` в запросе → site-режим
      - кавычки-цитаты + error/exception/traceback/crash/зависает/регрессия → debug
      - pricing/free tier/rate limit/лимит/тариф/цена/стоимость/версия+число → fact
      - кириллица + (свежесть или --freshness) → news(ru); кириллица → ru
      - docs/documentation/api/github/pypi/дока + имя библиотеки → docs
      - vs/best practices/сравнение/обзор/alternatives/how to choose → research
      - иначе → None (дефолтная цепочка)
- [ ] порядок правил важен (site: → debug → fact → news/ru → docs → research)
- [ ] логировать intent_source=auto; при явном флаге — flag

## Этап 5 — валидация (~15 мин)

- [ ] прогнать detect() на 32 запросах dataset.jsonl — сверка с разметкой
      сценариев (цель: ≥80% совпадений; спорные — глазами)
- [ ] smoke: `wsearch search "playwright docs"` (→ docs?), запрос с `site:`,
      RU-новость, debug-строка; `--intent docs` вручную; `usage` показывает вызовы
- [ ] bench/run_bench.py жив (пин --provider не зависит от интентов)

## Этап 6 — доки + память (~20 мин)

- [ ] SKILL.md: вызовы через `wsearch` (PATH), таблица интентов «сценарий → флаг»,
      упоминание автодетекта, команда usage
- [ ] ~/.claude/CLAUDE.md секция «Веб-поиск»: алиас, интенты одной строкой
- [ ] README.md: раздел intent-роутинг + телеметрия; хронология
- [ ] bench/REPORT.md §6.2: пометка «внедрено Б+В+Г, 27.08»
- [ ] память reference_web-search-stack.md + MEMORY.md

## Отложено

- zai в матрицу бенча — после ресета 18.09 (`run_bench.py --providers zai`)
- судья-сэмплы живого трафика — через месяц, когда usage.jsonl накопится
- Пере-прогон бенча через месяц (news-запросы освежить)
