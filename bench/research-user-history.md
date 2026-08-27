# Реальные сценарии веб-поиска из истории сессий Claude Code

Дата сбора: 2026-08-27. Цель — репрезентативный датасет для бенчмарка поисковых провайдеров (`wsearch`).

> **Публичная версия**: датасет собран из реальной истории сессий автора; часть
> дословных запросов (карьера, личные обстоятельства, политика, инфраструктура)
> заменена нейтральными аналогами того же сценария/языка/свежести. Методика,
> статистика и выводы — исходные, метрики REPORT считались на полном наборе.

## Методика и источники

История сессий: `~/.claude/projects/*/*.jsonl` (+ вложенные `subagents/`). Извлечены три поколения поисковых вызовов:

1. **MCP `web_search_prime`** (период ~30.07–26.08, до перехода на wsearch) — **1102 уникальных запроса** (параметр `search_query`). Основной массив.
2. **`brave_search.sh`** (Brave API CLI, ~24–27.08) — **~35–70 уникальных запросов** (часть с флагами свежести `-f pm/pw/py`, региона `-c US/RU`, языка).
3. **`wsearch search/multi`** (новый CLI, 26–27.08) — **16+ уникальных запросов** (включая fan-out `multi --queries "q1|q2|q3"`).

Встроенный WebSearch не использовался ни разу (заблокирован в permissions). Даты — по mtime файлов сессий (точность до дня).

Общая характеристика массива web_search_prime (n=1102): **41% с кириллицей / 59% en-only**; 203 запроса с кавычками-фразами (`"..."`), 24 с `site:`; у brave-вызовов ~95 имеют флаг свежести (`-f pm` — самый частый, далее `-f pw`, `-f py`).

Отдельно отмечено: в соседнем проекте автора уже был smoke-бенчмарк SimpleQA-20 (20 вопросов с gold-ответами, grading по substring) — синтетический, не из реальной истории.

Типичный паттерн использования: пользователь (часто голосом) формулирует задачу словами («поищи», «найди в интернете»), агент декомпозирует её в 3–10 узких англоязычных или русских запросов с точными терминами. Поэтому ниже обе реальности: (а) запросы, как их реально посылал агент, (б) исходные формулировки пользователя.

---

## 1. ru-general — русский общий (без привязки к свежести)

| Дата | Запрос (дословно) |
|---|---|
| 2026-08-05 | телеграм бот python aiogram хостинг бесплатно варианты |
| 2026-08-05 | распознавание речи whisper.cpp модели русский язык |
| 2026-08-05 | домашний файловый сервер NAS synology альтернативы open source |
| 2026-08-05 | git для нетехнических команд обучение базовые команды |
| 2026-08-05 | ведение документации проекта confluence альтернативы open source селфхостинг |
| 2026-07-31 | открытые данные России API транспорт расписание разработчикам |

## 2. ru-news — русский, свежесть/новости

| Дата | Запрос (дословно) |
|---|---|
| 2026-08-24 | выход python 3.14 что нового changelog |
| 2026-08-24 | python 3.14 релиз новые фичи обзор |
| 2026-08-14 | GLM 5.3 выход релиз Zhipu |
| 2026-08-14 | GLM 5.3 Zhipu AI анонс модели новости |
| 2026-08-27 | GLM-5.3-Flash Z.ai coding plan release *(brave, `-f pm`)* |
| 2026-08-26 | график ЕГЭ 2026 изменения расписание *(brave, `-f pm`)* |

## 3. en-news — английский, свежесть/новости

| Дата | Запрос (дословно) |
|---|---|
| 2026-08-24 | linux kernel 6.15 release notes highlights |
| 2026-08-24 | linux kernel 6.15 merge window new features summary |
| 2026-08-14 | GLM-5.3 released announcement |
| 2026-08-25 | site:reddit.com z.ai OR GLM coding plan API down August *(brave, `-f pw`)* |
| 2026-08-25 | whisper.cpp changelog release notes streaming mode *(brave, `-f pm`)* |
| 2026-08-24 | best local LLM apps macOS Apple Silicon 2026 LM Studio Ollama MLX recommendations *(brave, `-f py`)* |

## 4. exact-fact — точный факт / версия / цифра / цена / квота

Крупнейший паттерн пользователя: цены, лимиты, версии API. Подчёркивание — самые характерные.

| Дата | Запрос (дословно) |
|---|---|
| 2026-08-26 | Yandex Cloud Vision OCR цены за страницу тарифы |
| 2026-08-26 | "Vision" OCR Yandex "за 1 000 страниц" ИЛИ "за 1000 страниц" цена тариф rub *(brave)* |
| 2026-08-21 | Z.ai GLM web search API pricing free tier per 1000 searches |
| 2026-08-21 | 智谱 bigmodel.cn web search API 价格 免费额度 search-pro |
| 2026-08-22 | Exa AI search API free tier 1000 requests per month pricing |
| 2026-08-22 | Serper.dev free 2500 credits API key signup |
| 2026-08-21 | Linkup API free tier 4000 queries one-time or monthly |
| 2026-08-21 | Kagi search API pricing discontinued 2026 |
| 2026-08-21 | r.jina.ai free rate limit without API key requests per minute |
| 2026-08-20 | Топвизор тарифы цены за операции снятие позиций рублей |
| 2026-08-20 | резидентные прокси для парсинга цена за гигабайт |
| 2026-08-27 | patchright pypi latest version release 2026 *(wsearch)* |
| 2026-08-27 | curl_cffi latest version changelog 2025 pypi MIT license dependencies *(wsearch)* |
| 2026-08-13 | MusicBrainz API rate limit 1 second genre tags Python musicbrainzngs |
| 2026-08-13 | Discogs API rate limit 60 per minute authentication electronic genre style |

## 5. semantic — по смыслу / исследовательский (обзор, сравнение подходов)

| Дата | Запрос (дословно) |
|---|---|
| 2026-08-19 | Claude Code subagents best practices 2025 |
| 2026-08-19 | Claude Code subagents parallel research tasks isolation context documentation |
| 2026-08-19 | claude code subagents automatic delegation vs manual trigger community lessons |
| 2026-08-19 | Anthropic engineering multi-agent research system orchestrating subagents |
| 2026-08-14 | LLM prompt decomposition vs single monolithic prompt information extraction quality |
| 2026-08-14 | Anthropic prompt chaining workflows vs single agent when to decompose |
| 2026-08-14 | GenName generative entity linking LLM zero-shot |
| 2026-08-14 | GitHub LLM entity linking pipeline fuzzy candidates reranker repository |
| 2026-08-13 | music recommendation system explainable audio features github |
| 2026-08-12 | Mem0 vs Letta MemGPT vs Zep agent memory framework comparison 2026 |
| 2026-08-16 | AI agent personal finance tracking natural language 2026 comparison |
| 2026-08-26 | github auto-generate development changelog from AI coding agent session logs |

## 6. code-docs — код, доки, библиотеки, API

Включая отдельный мегакластер enterprise-документации (07.08, ~90 запросов за день — самый крупный однодневный кластер всей истории).

| Дата | Запрос (дословно) |
|---|---|
| 2026-08-26 | Yandex AI Studio deepseek-v4-flash API reasoningMode отключить reasoning completionOptions |
| 2026-08-26 | llm.api.cloud.yandex.net foundationModels/v1/completion modelUri deepseek пример запроса |
| 2026-08-06 | Yandex OAuth mail:smtp_full mail:imap_full scope list full access send |
| 2026-08-13 | yandex music api token QR login plus subscription MarshalX |
| 2026-08-13 | MarshalX yandex-music-api Python library GitHub |
| 2026-08-12 | Perplexity API sonar chat completions endpoint documentation api.perplexity.ai curl example |
| 2026-08-21 | ddgs python library duckduckgo_search renamed rate limit 2026 |
| 2026-08-04 | Redmine API документация интеграция создание задач |
| 2026-08-27 | playwright page.goto wait_until domcontentloaded vs networkidle SPA rendering best practice *(wsearch)* |
| 2026-08-27 | reuse chromium between python script runs remote-debugging-port connect_over_cdp save launch time scraping *(wsearch)* |
| 2026-08-07 | kafka connect configuration transforms chain example documentation |
| 2026-08-07 | "Kafka The Definitive Guide" pdf free chapters download |
| 2026-08-07 | airflow dag trigger REST API status endpoint example |

## 7. local-ru — РФ-специфика: организации, рынок, цены, инфраструктура

| Дата | Запрос (дословно) |
|---|---|
| 2026-08-20 | разработка телеграм бота под ключ стоимость Москва агентство |
| 2026-08-20 | Arsenkin Tools обзор 2026 GEO ИИ-выдача нейровыдача Яндекс |
| 2026-08-20 | SpyWords мониторинг ИИ-поиска новый инструмент 2026 |
| 2026-08-20 | ozon seller api лимиты запросов документация |
| 2026-08-11 | LLM API провайдеры Россия gpt-oss deepseek open-source 2026 список |
| 2026-08-07 | два провайдера интернета балансировка отказоустойчивость роутер |
| 2026-07-30 | Яндекс 360 для бизнеса API вебхуки события новое письмо почта |
| 2026-08-05 | магистратура IT заочно стоимость вузов Москва сравнение *(brave)* |
| 2026-08-05 | МГТУ им Баумана магистратура проходной балл *(brave)* |

## 8. debug-errors — поиск по точной строке ошибки / issue / регрессии

Явная категория, не заложенная в исходной схеме: поищи-почему-сломалось с точными цитатами из логов.

| Дата | Запрос (дословно) |
|---|---|
| 2026-08-24 | Claude Code "cannot determine the safety of Bash" "temporarily unavailable" auto mode *(brave)* |
| 2026-08-26 | python 3.14 ssl read hangs forever socket timeout not honored *(brave)* |
| 2026-08-26 | python http.client response read blocks forever server closed connection without TLS close_notify *(brave)* |
| 2026-08-26 | cpython 3.14 regression urllib ssl socket timeout github issue *(brave)* |
| 2026-08-07 | wireguard intermittent handshake failure nat keepalive android |
| 2026-08-02 | docker desktop vpnkit high cpu macos fix |
| 2026-08-24 | Z.ai api "Making sure you" bot Anubis blocked API *(brave)* |
| 2026-08-24 | z.ai GLM coding plan API errors timeouts anti-bot 522 *(brave, `-f pm`)* |

## 9. Исходные формулировки пользователя (до декомпозиции агентом)

Раздел исключён из публичной версии: дословные голосовые/чатовые формулировки
автора. По характеру это «поищи…», «найди в интернете…», «что нового про…» —
агент декомпозирует их в 3–10 узких запросов из таблиц выше.

---

## Итоговая статистика

Полный массив: **~1150+ реальных поисковых запросов** за 30.07–27.08 (1102 web_search_prime + ~35–70 brave + 16+ wsearch).

Категоризация отобранных 61 запросов выше:

| Категория | Кол-во | Доля |
|---|---|---|
| exact-fact (цена/версия/квота) | 15 | 25% |
| semantic (исследовательский) | 12 | 20% |
| code-docs (доки/API) | 13 | 21% |
| local-ru (РФ-специфика) | 9 | 15% |
| debug-errors (строки ошибок) | 8 | 13% |
| ru-news | 6 | 10% |
| en-news | 6 | 10% |
| ru-general | 6 | 10% |

(Сумма > 61: часть ru/en-news запросов частично пересекается — один факт искали на двух языках; пересчитано без двойного счёта доля news ≈ 16%.)

По всему массиву web_search_prime: ru 41% / en 59%; ~18% запросов содержат кавычки-фразы; ~2% `site:`; по javаскрипт-массиву brave ~40% вызовов со свежестью (в основном `-f pm`/`-f pw`).

**Выводы для бенчмарка:**
1. Доминируют точные технические запросы (exact-fact + code-docs + debug-errors ≈ 59%) — провайдер обязан хорошо искать доки, PR в GitHub, PyPI, enterprise-доки и строки ошибок.
2. Свежесть — реальный, но не главный сценарий (~16%): релизы моделей, changelog, статус API, news-factcheck.
3. Русский язык — 41%: обязательно включить ru-general, local-ru (цены/тарифы РФ-сервисов, организации) и ru-news.
4. Запросы длинные (в среднем 6–10 терминов), часто с операторами (`site:`, кавычки, `OR`, `filetype:`) — бенчмарк должен включать операторные запросы.
5. Типовая длина сессии: 5–15 связанных запросов на одну задачу (fan-out по синонимам) — имеет смысл мерить не только top-1, но и покрытие кластера запросов.
