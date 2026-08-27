# Веб-поиск и веб-извлечение: как это устроено и как работает в моём стеке

**Статус:** полный отчёт сессии-исследования от 27.08.2026 (все три research-блока закрыты).
**Связанное:** `README.md` (устройство тула).

---

## 1. Двухслойная модель: поиск и извлечение — разные вселенные

Любой агент (Claude Code, Cline, deep-research-бот) ходит в веб двумя принципиально разными способами:

```
Слой 1 — SEARCH                 Слой 2 — EXTRACT / FETCH
запрос ("glm-4.6 release")      известный URL ("https://…/blog/glm")
        │                                │
        ▼                                ▼
   поисковый движок              HTTP GET + парсинг HTML
   (чужой индекс, датацентр)     (можно сделать на своём ноутбуке)
        │                                │
        ▼                                ▼
   5–10 результатов:             чистый markdown страницы:
   title + url + сниппет         заголовки, текст, ссылки, таблицы
   (по 100–500 символов)         (тысячи символов)
```

**Ключевая асимметрия** (главная мысль всего исследования):

| | Search | Extract |
|---|---|---|
| Что нужно воспроизвести | индекс миллиардов страниц + краулер-ферма + ранжирование | один HTTP GET + парсер HTML |
| Можно ли сделать локально | **нет** (датацентровая штука) | **да**, тривиально |
| За что платим кредитами | за доступ к чужому индексу | за чужую инфраструктуру обхода (антибот, IP-пулы) — а не за сам «GET → markdown» |
| Бесплатная альтернатива | скрейпинг чужой выдачи (хрупко, баны) | локальный fetch + trafilatura (надёжно,.quality ~0.92 F1) |

### 1.1. Правильные слова (консенсус англоязычных доков)

- **fetch** — получить содержимое **одного известного URL** (HTTP GET → контент). Самый низкоуровневый.
- **scrape** — извлечь **данные из конкретной страницы**, обычно с рендерингом/чисткой/структурированием.
- **crawl** — **дискавери**: рекурсивный обход сайта по ссылкам от seed-URL, на выходе карта/инвентарь URL. Классическая формула: *crawling discovers, scraping extracts*; типовой pipeline = crawl → scrape.
- **extract / parse** — превращение уже полученного HTML в чистый markdown или структурированные поля (JSON по схеме/CSS-селекторам).
- Оговорка: вендоры смешивают (Firecrawl `/crawl` сразу и дискаверит, и извлекает).

### 1.2. Классы сервисов (типология по apiserpent / Brave / Olostep)

Поисковые API делятся на **три подкласса** — они НЕ одинаковы:

1. **Классический SERP API** (Brave, Serper, SerpApi) — возвращает **реальную выдачу** движка: позиции, SERP-фичи (featured snippet, People Also Ask), гео-таргетинг. Тела страниц нет, только сниппеты. Нужен, когда важен ранг или точная выдача.
2. **RAG-content / LLM-oriented** (Tavily, Linkup-гибрид) — «поиск + скрейп + чистка в одном вызове»: отдаёт не сниппеты, а вычищенный токен-дружелюбный контент, иногда готовый ответ. Точных позиций Google нет.
3. **Neural / semantic** (Exa, экс-Metaphor) — собственный индекс, документы предобработаны в **embeddings**; находит страницы «по смыслу», даже когда слова запроса не совпадают. Не показывает реальный ранг Google.

Сервисы извлечения делятся на два класса:

- **Reader API** (Jina `r.jina.ai`) — «один URL → LLM-friendly markdown, дёшево и просто». Эталон: префикс к URL, внутри headless Chrome + их модель ReaderLM для чистки.
- **Scraper API** (Firecrawl, ScrapingBee, Browserless) — инфраструктура: headless-браузеры, антибот-обход, ротация прокси, JS-рендеринг, PDF. Плюс **crawler**-эндпоинты (рекурсивный обход всего сайта).

Отдельный термин — **agentic search / deep research**: retrieval-паттерн, где LLM-агент сам планирует многошаговый поиск (декомпозиция → серия поисков → оценка → переформулировка → цикл с reflection → синтез с цитатами). По данным Brave/SAGE, агент в среднем делает ~5 поисковых шагов. Deep research — коммерческое имя флагманской реализации этого паттерна.

### 1.3. Типовой цикл агента (как я этим пользуюсь на практике)

1. Сформулировать 1–3 запроса → `wsearch search` / `multi` (параллельный fan-out с dedupe по URL).
2. Прочитать сниппеты, выбрать 2–5 перспективных URL.
3. `wsearch fetch` / `gather` (параллельное чтение нескольких URL) → markdown.
4. Если информации мало — переформулировать запросы, повторить (это и есть agentic search).
5. Синтез с указанием источников.

Сниппет — это «аннотация на обложке»: по нему решаем, открывать ли книгу. Extract — сама книга. Кредиты поиска тратятся на шаге 1, кредиты извлечения — на шаге 3; благодаря локальному extraction (раздел 5) шаг 3 станет почти бесплатным.

---

## 2. Search-слой в wsearch: 9 провайдеров, как они устроены

### 2.1. Как контролируется всё это хозяйство

- **Цепочка с приоритетами** (`engine/providers/__init__.py`): tavily → youcom → zai → exa → brave → linkup → parallel-anon → ddg → **parallel($)**. Политика владельца (пересмотрена 27.08 после сверки тарифов с доками): **сначала вырабатываем возобновляемые месячные квоты (остаток сгорает на ресете), затем keyless/free-режимы, затем скрейпинг-дно; разовые $-гранты, которые не пополняются — самый последний рубеж.** youcom стоит вторым, потому что его 100/день сгорают ежедневно; linkup последним в эшелоне — самый большой «бак» (~4000/мес).
- **Локальный счётчик квот** (`state/quotas.json`): per-provider `used` / `window_start` (day|month|once) / `exhausted_until`. Роутер **перед** вызовом проверяет остаток → скип без запроса, **ДО** получения 429.
- **Реальный 429** → `mark_exhausted`: провайдер запоминается исчерпанным до даты сброса (zai, например, парсит дату сброса прямо из тела ошибки).
- **Dual-mode** (tavily): при смерти keyed-режима провайдер не выпадает из цепочки, а дегрейдится на keyless в том же вызове.
- Смотрится одной командой: `wsearch status` (остатки) и `wsearch chain` (кто сейчас активен).

### 2.2. Провайдер за провайдером

**1. tavily** — REST `api.tavily.com/search`, класс «LLM-oriented». Отправляем `{"query", "max_results"}`, при `--freshness day` уходит `topic: news`. Возвращает готовые чистые сниппеты (`content` по ~500 симв.) — сразу в контекст LLM, без чистки. **Dual-mode**: с ключом — 1000 кредитов/мес (заголовок `Authorization: Bearer`), при исчерпании — бесшовный переход на keyless (`X-Tavily-Access-Mode: keyless`) внутри того же вызова. Также умеет `/extract` (fetch-цепочка). Сильная сторона: скорость, аккуратные сниппеты. Слабее: свежесть/даты в выдаче.

**2. parallel** — MCP `search.parallel.ai/mcp` (Streamable HTTP, JSON-RPC), тул `web_search`. **Свой веб-индекс** (не агрегат Google) — независимый ранг. Гочча протокола: аргументы `objective` + `search_queries` — **обязательно массив** (одиночная строка = pydantic-422). Возвращает `title/url/excerpts[]/publish_date` — **единственный из цепочки, кто даёт даты публикации в выдаче**. Keyed-слот тратит $-баланс ($18.46 на момент подключения); у того же MCP есть `web_fetch` (до 20 URL за вызов) — потому parallel стоит и первым в fetch-цепочке.

**3. zai** — MCP `api.z.ai/api/mcp/web_search_prime/mcp`, тул `web_search_prime` — тот самый MCP из GLM Coding Plan («zti»). Квота 1000 вызовов/мес из подписки. Сейчас **исчерпан до 2026-09-18 16:28 UTC** — роутер скипает его бесплатно, дата сброса спарсена из тела 429 («Your limit will reset at …») и запомнена. Поднимется сам.

**4. exa** — REST `api.exa.ai/search`, класс **neural/semantic**: находит по смыслу, а не по ключевым словам. Отправляем `{"query", "numResults", "type": "auto", "contents": {"highlights": true}}` — highlights это готовые релевантные выжимки (рекомендация самих Exa для агентских циклов, токен-эффективно). При freshness уходит `category: news`. Даты есть (`publishedDate`). $10/мес кредита ≈ 1400 поисков. Сильная сторона: исследовательские/семантические запросы («страницы в духе вот этой»), англоязычный контент.

**5. linkup** — REST `api.linkup.so/v1/search`, французский «гибрид SERP + Web Search API». **API дрейфнул** (гочча, поймана live-тестом): тело `{"q", "depth": "standard|deep", "outputType": "searchResults|sourcedAnswer|structured"}` — не `query` и не `sourcedResults`. $20-кредит **пополняется до $20 ежемесячно** ≈ 4000 std-поисков/мес (deep дороже ×2). При исчерпании — 429, запоминаем до конца месяца.

**6. youcom** — MCP `api.you.com/mcp?profile=free`, тул `you-search`, **без ключей**, 100 запросов/день. Свежесть через аргумент `created: lastDay/lastWeek`. Гочча: SSE-ответ содержит notification-событие перед результатом — клиент парсит data-строки по request-id. Keyed-ключ ($100-кредит аккаунта) лежит в .env закомментированным как НЗ.

**7. brave** — REST `api.search.brave.com`, классический **SERP API**: реальная выдача Brave-индекса, freshness `pd/pw/pm`. 2000/мес. **Лучший RU-поклон в цепочке** — для русскоязычных запросов качество заметно выше среднего. Сниппеты короче (`description` + `extra_snippets`).

**8. parallel-anon** — анонимный слот того же Parallel MCP (те же тулзы, без Bearer). «Пониженные» лимиты, но generous для hobby — безлимитное бесплатное дно перед скрейпингом.

**9. ddg** — скрейпинг-дно: POST на `html.duckduckgo.com/html/` с браузерным UA, парсинг выдачи регулярками, полл 1.5 с, разворачивание редиректов `uddg=`. Не API — «поиск без поискового движка»: читаем чужую выдачу. Всегда может сломаться (антибот-челлендж 202), потому и последний. Зато неубиваем по квотам и часто хорош для RU.

### 2.3. Одинаковы ли провайдеры? Нет — сводная таблица

| # | Провайдер | Класс движка | Сниппеты для LLM | Даты | RU-качество | Свежесть | Квота | Роль |
|---|---|---|---|---|---|---|---|---|
| 1 | tavily | LLM-oriented | ★★★ сразу чистые | — | среднее | topic=news | 1000/мес (ресет 1-го) → keyless | рабочий конь №1 |
| 2 | youcom | ? (free MCP) | ★★ | — | среднее | created=lastDay | 100/**день** (сгорают ежедневно!) | ежедневная мелочёвка |
| 3 | zai | ? (подписка GLM) | ★★ | — | среднее | recency-фильтр | 1000/мес (до 18.09 ✗) | запасной из подписки |
| 4 | exa | neural/semantic | ★★★ highlights | ★★ | слабее (англ.) | category=news | $10/мес ~1400 | «по смыслу», research |
| 5 | brave | SERP (реальная выдача) | ★ короткие | — | ★★★ | pd/pw/pm | 2000/мес (легаси) | RU-запросы |
| 6 | linkup | гибрид | ★★ content | — | среднее | depth=deep | top-up до $20 ~4000/мес | дешёвый объём, большой бак |
| 7 | parallel-anon | свой индекс | ★★ | ★★★ | среднее | — | безлимит | free-дно |
| 8 | ddg | скрейпинг выдачи | ★ сырые | — | ★★★ | — | безлимит | аварийное дно |
| 9 | parallel | свой индекс | ★★ excerpts | ★★★ publish_date | среднее | — | **$18.46 разовый грант** (+$5/мес rec.) | **последний рубеж** |

Практические выводы: RU-запрос → brave (или ddg); исследовательский англоязычный → exa; нужны даты публикаций → parallel; максимальная дешевизна → linkup; быстрые текущие новости → tavily news / youcom lastDay.

### 2.4. Экономика search-слоя

**~8400 keyed-поисков/мес + 100/день youcom + безлимитное keyless-дно. Ноль привязанных карт.** Сдача 429 исключена дизайном: счётчик тратит keyed-лимиты вперёд и уходит вниз по цепочке до скрейпинга.

---

## 3. Extract-слой сейчас: 4 сервисных провайдера (и почему это хочется поменять)

Текущая fetch-цепочка `wsearch fetch URL` (после пересогласования 27.08):

| # | Провайдер | Как | Квота/цена | Чем силён |
|---|---|---|---|---|
| 1 | firecrawl | REST `/v1/scrape`, formats: markdown | 1000–2000 кредитов/мес (возобновляемые, ресет ~23-го) | JS-тяжёлые страницы, PDF |
| 2 | tavily | REST `/extract` (keyed→keyless) | keyed-кредиты | быстрый простой HTML |
| 3 | jina | `r.jina.ai/<url>` | keyless ~20 RPM | вечное бесплатное дно |
| 4 | parallel | MCP `web_fetch` (до 20 URL/вызов) | **$-грант $18.46** — последним | качество, даты |

Проблема: **всё уезжает на чужие серверы** — ~3000 кредитов/мес суммарно + $-баланс, хотя 80–90% страниц можно извлечь локально бесплатно и быстрее. Отсюда план раздела 5.

---

## 4. История стека (как я сюда попал)

1. **Апрель 2026 — [searcharvester](https://github.com/vakovalskii/searcharvester)** (Валерий Ковальский) — с этого репо всё начиналось. Self-hosted «search + extract + deep research» в docker compose: `/search` — Tavily-совместимый API поверх **SearXNG** (метапоиск → Google/Bing/DDG/Brave), `/extract` — **trafilatura** с пресетами размера (s=5k / m=10k / l=25k / f=пагинация по 25k, кэш 30 мин), `/research` — Hermes-агент. Работало, пока **NL-VPN-IP не забанили поисковики** → поиск умер.
2. **Июнь — web-search-tool** — своя eval-harness над SearXNG. Тоже умер (баны IP на VPS, «forever-war»).
3. **Август — Z.ai MCP (web_search_prime) + скилл brave** как fallback. Z.ai-квота кончилась 21.08 (ресет 18.09).
4. **27.08 — wsearch** (этот тул): 9 search + 4 fetch провайдеров, счётчик квот, фолбэк до 429.

**Живая проверка 27.08:** контейнеры searcharvester подняты (`tavily-adapter:8000`, `searxng:8999`, frontend:9762; образ 8.2 ГБ). Результаты:
- `/extract` (trafilatura в докере) **работает**: GitHub ✓, Habr ✓, example.com ✓; Wikipedia → 403 — это **IP-репутация** (NL-датацентр-IP), а не поломка тула.
- `/search` (SearXNG) **тоже жив**: внешний IP сменился — прежний бан **слетел**, Google/Brave отвечают. Но это хрупкий слой: сегодня жив, завтра капча — держать бонусом, не основой.

Вывод-референс: extraction у меня **уже был локальным** и работал — в докере. Осталось вынести его из 8-ГБ докер-стека в лёгкий uv-проект внутрь wsearch (раздел 5).

---

## 5. Локальный extraction: проработка (итоги research)

### 5.1. Лестница уровней

| Уровень | Что | Цена | Покрытие |
|---|---|---|---|
| **L0: plain fetch** | HTTP GET + чистка HTML → markdown | бесплатно, локально | ~80–90% страниц |
| **L1: main-content extraction** | L0 + алгоритм «главного контента» (trafilatura): срезает нав/рекламу/футер, сохраняет заголовки/списки/таблицы/ссылки | бесплатно, локально | то же, но чисто |
| **L2: headless-браузер** | реальный Chromium рендерит JS, потом L1 по отрендеренному DOM | бесплатно, локально | + SPA, динамика |
| **L3: облачный scraper** | firecrawl / jina / tavily / parallel — их серверы, IP-пулы, антибот | кредиты | + Cloudflare, баны, PDF |

Платим на L3 не за «GET → markdown», а за **обход защиты**: фермы «чистых» IP, стелс-сборки браузеров (headless сам по себе палится), JS-рендер на их CPU.

### 5.2. Что говорят бенчмарки (2026)

- **trafilatura — лучший open-source экстрактор**: собственный бенчмарк (обновлён 04.08.2026, 990 документов): standard **F1 = 0.924**, favor_precision 0.920, favor_recall 0.918, fast 0.918. Конкуренты: readability-lxml **0.826**, magic-html 0.889, justext 0.862, newspaper4k 0.801, html2text 0.663, inscriptis 0.694. Независимая оценка (OSTI/ORNL): trafilatura 0.937 vs Readability 0.914.
- Используется HuggingFace, IBM, NVIDIA, AI2, Internet Archive. 6.7k★, активна. `markdown` — first-class формат вывода.
- Нюанс (BulkMD): на «чистых article-страницах» Readability чуть точнее (0.94 vs 0.91), но проваливается на лендингах/дашбордах/форумах — trafilatura стабильнее по спектру.
- Молодой претендент **rs-trafilatura** (Rust+PyO3, март 2026): F1 0.966, 44 мс/страница, **confidence-score, предсказывающий F1** каждой экстракции (ниже порога → fallback). Концептуально ровно наш пайплайн, но проект молодой — следить.

### 5.3. Рекомендованный стек (через uv, без докера)

```
uv add httpx "trafilatura[all]" playwright
uv run playwright install chromium
```

- **Tier 1 (L0+L1)**: `httpx.get()` → `trafilatura.extract(html, output_format="markdown", include_links=True, include_images=True)`. `fast=True` для потока, standard для качества.
- **Tier 2 (L2)**: тот же URL через Playwright (headless chromium) → тот же trafilatura по отрендеренному DOM.
- **Tier 3 (L3)**: существующие сервисные провайдеры wsearch — только для жёсткого антибота.
- Опционально «всё из коробки»: **crawl4ai** (79.5k★, Apache-2.0, «zero keys») — внутри уже playwright + patchright + playwright-stealth + свои content-фильтры; extract-часть юзается как библиотека. Минус: тяжёлые deps.

### 5.4. Антидетект-браузеры (если vanilla Playwright режется)

Бенчмарк 2026 (31 Cloudflare-цель, 651 прогон):
- **nodriver** — лучший (28 OK / 0 blocked): системный Chrome по сырому CDP; минус — низкоуровневый async API.
- **curl_cffi** (без браузера вообще!) — 26 OK: TLS-fingerprint-подмена; для многих антиботов хватает замены httpx → curl_cffi, без headless.
- **patchright** — drop-in замена playwright (тот же API, патчит Chromium на уровне CDP), 25 OK vs 24 у vanilla — прирост скромный, но дешёвый: `uv add patchright`.
- **Camoufox** (Firefox-fork, глубокая подмена fingerprint) — следующий эшелон.
- undetected-chromedriver — поддержка замедлилась, не рекомендуется.

### 5.5. Нужен ли локальный LLM-конвертер (ReaderLM-v2)? — Нет

- Технически легко: 1.5B, GGUF Q4_K_M ~1 ГБ, на 24 ГБ M5 Pro влезает с запасом, 512K контекст.
- Против: (1) лицензия **CC-BY-NC 4.0** — только некоммерческое; (2) скорость — секунды на страницу против миллисекунд у trafilatura; (3) качество уже 0.92–0.94 у rule-based, LLM-конвертеры решающего выигрыша не дают (MinerU-HTML ~1570 мс/страницу на A100 без роста F1). LLM-конвертер выигрывает только на экзотических layout'ах — там проще отдать страницу vision-LLM или облачному сервису tier-3.

### 5.6. Эвристика «JS-пустышка» (когда plain GET не годится и нужен браузер)

Сигналы (fetch → classify → render только по доказательствам):
1. Пустые app-руты: `<div id="root"></div>`, `<div id="app"></div>`, `<main id="__next"></main>` — скрипты есть, текста нет.
2. Мало текста после экстракции (сотни символов) при большом исходном HTML.
3. Для статьи нет `h1`/`<article>`/JSON-LD `articleBody`; для товара нет цены/JSON-LD `product`.
4. Hydration-пейлоады `__NEXT_DATA__`, `window.__INITIAL_STATE__`, `__APOLLO_STATE__` — сначала проверить, нет ли контента прямо внутри (тогда спарсить без браузера!).
5. Много `<script src>` + крошечное тело; «enable JavaScript» в `<noscript>`.
6. Отличать **блок** (403/429/503, challenge, Turnstile → это антибот: tier-3 или curl_cffi/patchright) от **ошибки экстракции** (контент есть, но срезан → recall-режим trafilatura / readability).
7. Продвинутый вариант (идея rs-trafilatura): confidence-score каждой экстракции, ниже порога → браузер.

### 5.7. Целевая архитектура wsearch после интеграции — **РЕАЛИЗОВАНО 27.08 (вечер)**

```
wsearch fetch URL:
  1. local (каскад внутри ОДНОГО subprocess, uv-проект local-extract/)   ← бесплатно
     1a. httpx GET (10 c) + trafilatura markdown
     1b. curl_cffi impersonate=chrome (15 c) — только при блоке/сетевом сбое
     1c. playwright chromium (<=25 c goto) — при JS-пустышке/тонкой экстракции;
         hydration-пейлоады (__NEXT_DATA__ и др.) парсятся без браузера
     провал (антибот/IP-бан/PDF) → exit 3 с reason → фолбэк ниже
  2. firecrawl     (антибот/JS/PDF, 1000–2000/мес возобновляемые)                       ← кредиты
  3. tavily extract                                                                  ← keyed→keyless
  4. jina            (r.jina.ai)                                                       ← free-дно
  5. parallel       (web_fetch, $-грант $18.46)                          ← последний рубеж
```

Решение по архитектуре: один слот `local` с каскадом внутри subprocess (а не
три слота в цепочке) — различение «блок → curl_cffi» vs «JS-пустышка → сразу
браузер» требует данных ступени (статус, размер HTML, маркеры challenge),
которых у stdlib-обёртки нет; плюс 1 spawn на URL вместо 1–3 при gather.
Имя ступени возвращается в JSON: FetchResult.provider = local-http |
local-curl | local-browser; `--provider local-http|local-curl|local-browser`
форсит ступень через алиасы.

Кэш: `state/fetch_cache.json` (TTL 30 мин, ≤200 записей, ключ — нормализованный
URL без utm/fragment; local тянет до 32k, `--max-chars` применяется на выдаче).
`--no-cache`, `wsearch reset fetch-cache`, `LOCAL_EXTRACT_DISABLE=1`.

Живые замеры 27.08: статика/SSR (habr, react.dev, wikipedia, HN) — local-http
~0.4–0.8 с; SPA (excalidraw.com) — http thin → browser ok за 3.3 с;
Cloudflare (nowsecure.nl) — http thin → browser blocked → firecrawl; мёртвый
хост — все три ступени network → сервисная цепочка. Кредиты extract-слоя
теперь тратятся только там, где локально действительно нельзя.

Кредиты тратятся почти только на **поиск** (невоспроизводимый слой), как и задумано. Сам `wsearch` остаётся stdlib-only: локальный экстрактор — отдельный uv-проект рядом, вызывается subprocess-ом (как офис-скиллы).

### 5.8. Что всё равно останется сервисам

- **IP-репутация**: Wikipedia 403 на NL-VPN-IP — локально не открыть, сервер Firecrawl в EU пройдёт.
- **RU↔World двусторонние блокировки**: часть зарубежного не открывается из РФ-сети, часть сайтов банит RU/VPN-IP — облачный fetch neutralен.
- Жёсткий антибот (Cloudflare Turnstile и старше), PDF-обход, масштаб.

---

## 6. Как search/fetch устроены у других агентов (проверено по коду/докам)

| Агент | Поиск | Чтение страниц |
|---|---|---|
| **Cline** | `web_search` только через собственный облачный бэкенд Cline; в SDK — плагином, официальный пример на **Exa** | SDK `web-fetch`: native fetch (30s, 5MB) + headless Chrome (CDP) для JS-страниц |
| **Roo Code** | встроенного поиска **нет** (issues #11075, #10676); весь веб — через MCP (рекомендуют Perplexity/Tavily MCP) | через MCP |
| **OpenHands** | **Tavily через официальный tavily-mcp** (search/extract/crawl/map), ключ в настройках; без ключа поиска нет | BrowserToolSet поверх browser-use (Playwright) |
| **Continue** | `web_search` через **свой облачный прокси** (trial-proxy `/web`) — пользователь ключей не приносит | plain fetch + Mozilla Readability + node-html-markdown → markdown |
| **Goose (Block)** | встроенного поиска **нет** (issue #5537); fetch-mcp (`uvx mcp-server-fetch`, keyless) или browserbase-mcp | MCP-расширения |
| **aider** | поиска **нет** (issue #2754) | `/web <url>`: цепочка **Playwright (chromium) → httpx → pypandoc → markdown** — локально! |
| **Gemini CLI** | `google_web_search` — Google Search grounding через Gemini API | `web_fetch` до 20 URL за вызов (urlContext API), **fallback на локальный fetch** |
| **Codex CLI** | серверный `web_search` (вкл. по умолчанию), режимы cached (индекс OpenAI) / indexed / live; Search/OpenPage/FindInPage в одном туле | в том же туле |
| **Cursor** | Web Search Tool + `@Web`/`@Docs`; провайдер не раскрывается | встроенный нативный **Browser tool** (navigate/click/screenshot) |

**Общий вывод research: никто из больших агентов НЕ делает локальную fallback-цепочку провайдеров со счётчиком квот.** Все делятся на три лагеря:

1. **Свой облачный бэкенд / LLM-API** — Codex, Gemini CLI, Cursor, Cline, Continue (пользователь не выбирает провайдера, всё вендорно).
2. **Один внешний провайдер через MCP** — OpenHands (Tavily).
3. **«Вынесено в MCP, приноси своё»** — Roo Code, Goose, aider.

Ближе всех к нашей философии — **aider**: его fetch-цепочка Playwright → httpx → markdown — ровно тот локальный подход из раздела 5, который планируем (и_reference-архитектура searcharvester, но уже без SearXNG-зависимости). wsearch с его 9-провайдерной цепочкой, локальным счётчиком квот и фолбэком ДО 429 — по research выходит **уникальной штукой**: ни один из девяти агентов такого не имеет.

Источники: github.com/cline/cline (WebSearchToolHandler.ts, web-fetch.ts) · docs.openhands.dev/usage/advanced/search-engine-setup · github.com/continuedev/continue (WebContextProvider.ts) · github.com/block/goose/issues/5537 · github.com/Aider-AI/aider/blob/main/aider/scrape.py · geminicli.com/docs/tools/web-search · developers.openai.com/codex/config-basic · cursor.com/docs/agent/tools/browser

---

## 7. Источники

**Типология и термины:** apiserpent.com/blog/serp-api-vs-tavily-exa-ai-agents · brave.com/learn/best-search-api-2026 · brave.com/search/api/glossary/agentic-search · zyte.com/learn/difference-between-web-scraping-and-web-crawling · browserless.io/blog/scrape-vs-crawl · olostep.com/blog/best-web-search-apis · linkup.so/blog/best-serp-apis-web-search · platform.claude.com/docs (web-fetch-tool)

**Экстракция и бенчмарки:** trafilatura.readthedocs.io/en/latest/evaluation.html · bulkmd.app/blog/readability-vs-trafilatura-extractors · osti.gov/servlets/purl/2429881 · github.com/adbar/trafilatura · github.com/Murrough-Foley/rs-trafilatura · murroughfoley.com/rs-trafilatura-rust-web-content-extraction

**Антидетект:** ianlpaterson.com/blog/anti-detect-browser-benchmark-patchright-nodriver-curl-cffi · github.com/Kaliiiiiiiiii-Vinyzu/patchright-python · github.com/daijro/camoufox

**ReaderLM и фреймворки:** jina.ai/models/ReaderLM-v2 · jina.ai/reader (лицензия CC-BY-NC FAQ) · github.com/unclecode/crawl4ai · github.com/firecrawl/firecrawl/blob/main/SELF_HOST.md · github.com/microsoft/markitdown · github.com/DS4SD/docling · github.com/jina-ai/reader

**Эвристики:** webclaw.io/blog/javascript-rendering-api-browser-fallback-web-scraping
