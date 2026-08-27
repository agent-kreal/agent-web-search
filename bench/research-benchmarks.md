# Бенчмарки и методики оценки веб-поиска для LLM-агентов

Research: 2026-08-27. Цель — переиспользовать чужие подходы для сравнения 7 поисковых API (tavily / exa / brave / linkup / you.com / parallel / ddg) на ~30 запросах: оценка качества **SERP**, а не LLM-ответов.

---

## 1. Сводная таблица бенчмарков

| Бенчмарк | Автор / год | Что меряет | Размер | Метрика | Применимость для сравнения search-API |
|---|---|---|---|---|---|
| **SimpleQA** | OpenAI, 2024 ([arxiv 2411.04368](https://arxiv.org/html/2411.04368v1), [HF openai/simpleqa](https://huggingface.co/datasets/openai/simpleqa), gated) | Short-form фактология: 1 вопрос → 1 indisputable ответ, adversarially собраны против GPT-4 | 4,326 q | Грейдер LLM ставит CORRECT / INCORRECT / NOT_ATTEMPTED; report: accuracy, F1 (harmonic mean correct×attempted), accuracy-given-attempted (CGA) | **Максимальная** — де-факто индустриальный стандарт для search-API: Tavily, Linkup, Parallel, Octen гоняют именно её. Пайплайн «SERP → reader LLM → grader» — готовый рецепт |
| **SimpleQA Verified** | arXiv, 2025 ([2509.07968](https://arxiv.org/html/2509.07968v2)) | Чистка SimpleQA: убраны вопросы, отвечаемые из parametric knowledge без поиска | подмножество | те же | Лучше для честной оценки retrieval (модель не «угадает» из памяти). Брать его вместо raw SimpleQA |
| **SealQA** | Virginia Tech, 2025 ([arxiv 2506.01062](https://arxiv.org/abs/2506.01062), [HF vtllms/sealqa](https://huggingface.co/datasets/vtllms/sealqa)) | Факты, где обычный веб-поиск даёт **конфликтующие/шумные** результаты (entity disambiguation, fast-changing факты). Сплиты `seal_0` (где фейлят frontier-модели) и `seal_hard` | ~7k+ q (неск. сплитов) | Answer accuracy с official grading prompt | **Максимальная**: по мнению Tavily — «тот самый бенчмарк для агентов»: сложнее SimpleQA, но single-step → качество SERP видно сквозь harness. Провайдеры уже сравниваются на нём публично (Tavily 49.5%/55.7% vs Exa Auto / Parallel / Perplexity / Brave / You.com) |
| **FreshQA** | Google, 2023 (FreshLLMs, ACL Findings'24; [github freshllms/freshqa](https://github.com/freshllms/freshqa), 402★) | Свежесть/устаревание: never-changing / slow-changing / fast-changing / **false-premise** (вопрос с ложной посылкой) | 600 q (dev 100 / test 500) | **FreshEval**: LLM-judge с регулярно обновляемыми эталонными ответами; binary accuracy + breakdown по fact-type | **Высокая**: единственный массовый бенчмарк, где «возраст данных» — первоклассная ось. Идеален для оценки freshness-различий между API (см. Octen: разброс 43–56% между провайдерами) |
| **FRAMES** | Google, 2024 ([arxiv 2409.12941](https://arxiv.org/html/2409.12941v3), [HF google/frames](https://huggingface.co/datasets/google/frames)) | Factuality + **Retrieval** + Reasoning: multi-hop вопросы, требующие 2–15 Wikipedia-статей | 824 q | Отдельно: retrieval accuracy (золотая статья попала ли в выдачу — по сути **hit@k по URL**), answer correctness | **Высокая для нашей постановки**: rare-пример, где retrieval-метрика (наличие gold-страницы в топ-k) считается явно — это ровно то, что нужно для SERP-оценки без agent-loop |
| **BrowseComp** | OpenAI, 2025 ([openai.com/index/browsecomp](https://openai.com/index/browsecomp), [HF openai/browsecomp](https://huggingface.co/datasets/openai/browsecomp), gated) | Agentic browsing: ответ easy to verify, hard to locate; 70%+ вопросов люди не могут ответить без браузера | 1,266 q | Answer accuracy (strict, LLM-graded) | **Низкая для нас**: слишком agentic — качество отдельного SERP-вызова прячется за harness'ом (много итераций, реформуляций). Годится только как smoke-test верхнего уровня |
| **GAIA** | Meta/HF, 2023 ([arxiv 2311.12983](https://arxiv.org/abs/2311.12983)) | General assistant: reasoning + multimodality + tools, уровни 1–3; human baseline 92% | 466 q (300 с ответами публично) | Accuracy | Низкая: tool-агностик, меряет агента целиком, не поиск |
| **HotpotQA** | 2018 (ACL) | Multi-hop QA (2-hop) по Wikipedia | 113k q (dev 7,405) | EM/F1; в IR-режиме — nDCG@10 (входит в BEIR) | Средняя как источник: берем сами вопросы + gold-страницы как anchor-URL. FRAMES уже сделал это лучше (отфильтровал) |
| **BEIR** | Cambridge et al., 2021 ([arxiv 2104.08663](https://arxiv.org/abs/2104.08663), [ir-datasets.com/beir.html](https://ir-datasets.com/beir.html)) | Zero-shot retrieval по 18 корпусам (вкл. hotpotqa, scidocs, arguana…) | ~миллионы qrels | **nDCG@10** (главная), recall@100 | Неприменим напрямую к живому вебу (qrels только по статичному корпусу), но источник метрики nDCG и «золотого» стандарта IR-оценки. Pyserini + trec_eval — инструменты подсчёта |
| **MIRACL** | 2022–23 ([project-miracl.github.io](https://project-miracl.github.io), [HF miracl/miracl](https://huggingface.co/datasets/miracl/miracl)) | Multilingual retrieval, **18 языков включая русский**; Wikipedia-корпус, человеческие qrels | 18 × ~тысячи q | nDCG@10 + recall@100 | Средняя: RU-след есть, но корпус статичный (Wikipedia dump), не веб-SERP. RU-подмножество можно взять как источник RU-запросов с золотыми страницами |
| **RusBEIR** | 2025 ([arxiv 2504.12879](https://arxiv.org/html/2504.12879v1), [github kaengreg/rusBeIR](https://github.com/kaengreg/rusBeIR)) | Русский zero-shot IR: 17 датасетов (SberQuAD-retrieval 45,328 q, RuBQ, rusSciBench…) | 45k+ q только SberQuAD | nDCG@10 | Если нужен RU-мини-бенч — готовые RU-запросы + релевантные документы |
| **GISA** | 2026 (см. [Semantic Scholar](https://www.semanticscholar.org/paper/841cdba14696a6490db0a27858495fa73c601ab3)) | General information-seeking: 373 human-crafted запроса + **полные человеческие поисковые траектории**, deterministic eval | 373 q | deterministic | Интересен как методология (gold-траектории = anchors), датасет новый/малораспространённый |

---

## 2. Метрики: что практично для 7 API × ~30 запросов

Ключевая проблема: **N=30 → огромный биномиальный CI**. Разница в answer-accuracy < 15–20 п.п. статистически неотличима (Wilson 95% CI при p=0.7, n=30 — примерно ±16 п.п.). Отсюда приоритет объективных per-snippet метрик над сквозной accuracy.

По убыванию практичности:

1. **hit@3 / hit@5 (gold URL/domain match)** — объективно, дёшево, без LLM. Для каждого запроса один раз размечается «золотой» URL (или домен) ручной проверкой любого API; дальше механическое сравнение. У Octen это называется *objective anchors* («do we return the known-correct page», hit@1/hit@k, exact URL match). На малом N — **основная метрика**. Домен-матч мягче URL-матча (мирроры/канонизация), URL-матч строже.
2. **LLM-as-judge relevance (reference-free), 0/1/2 per snippet → avg relevance@3** — судья оценивает «содержит ли сниппет информацию, отвечающую на вопрос», без эталона. Tavily/QuotientAI эмпирически нашли: *reference-free document relevance даёт более сильный сигнал, чем answer-only scoring* (разрывы между провайдерами на dynamic-вопросах виднее). На 30×7×5=1050 сниппетов — это дёшево (одним judge-модель-вызовом на сниппет или батчем).
3. **Answer accuracy (SimpleQA-style)** — reader LLM отвечает **только** по сниппетам, официальный грейдер ставит CORRECT/INCORRECT/NOT_ATTEMPTED → accuracy, F1, CGA. На N=30 годится как вторичная, но не primary: шумно. Правило Tavily: reader/grader/prompts/budget **идентичны для всех провайдеров**, единственная переменная — выдача.
4. **Freshness** — два способа: (а) подмножество fast-changing вопросов из FreshQA с judge-проверкой «ответ актуален на сегодня»; (б) объективно — дата публикации/индексации страницы из выдачи (published_date в ответах многих API) → медианный возраст источника по категориям запросов.
5. **Pairwise blind judge (win-rate)** — судья видит два SERP (порядок рандомизирован/свопнут — против position bias), выбирает лучший по rubric. У Octen: blind, position-swapped, rubric-grounded. На 7 провайдеров = 21 пара — дорого; применять **только к топ-2/3 финалистам** после отсева по hit@k.
6. **nDCG@10** — требует full relevance-разметки всех позиций всех провайдеров (30×7×10 = 2100 сниппетов). При малом N выигрыша в различительной силе перед hit@3 + relevance@3 почти нет, а стоимость и шанс ошибки разметки выше. **Не брать основной**; имеет смысл, если захотим учесть позицию релевантного результата (hit@k игнорирует ранг) — тогда градация 0/1/2 на сниппет уже есть и nDCG считается бесплатно из неё же.
7. **Операционные**: latency P50/P90 (лучше server-reported time, как у Octen, а не client round-trip — иначе меряется сеть), error/429-rate, доля дубликатов URL, полнота выдачи (сколько валидных результатов вернулось).

Схема «три взаимопроверяющих метода» (Octen): conclusion trusted только если согласны (1) pairwise judge, (2) objective anchors, (3) end-to-end answer accuracy. Для мини-версии: **hit@3 + LLM-judge relevance@3 + accuracy на SimpleQA-подмножестве** — уже даёт триаду.

---

## 3. Готовые датасеты (скачать и переиспользовать)

| Датасет | Где | Формат | RU? | Как использовать у нас |
|---|---|---|---|---|
| SimpleQA | [HF openai/simpleqa](https://huggingface.co/datasets/openai/simpleqa) (gated, free access) | CSV: problem, answer | нет | Сэмплировать 10–15 q fixed-seed; answer = ground truth для грейдера |
| SealQA | [HF vtllms/sealqa](https://huggingface.co/datasets/vtllms/sealqa) | parquet/csv: question, answer, fact-type, difficulty, год | нет | Взять 5–10 q из seal_0 (самые показательные для качества SERP) |
| FreshQA | [github freshllms/freshqa](https://github.com/freshllms/freshqa) — `freshqa_dataset.csv` | CSV: question, answer, fact_type (never/slow/fast-changing, false-premise) | нет | 8–10 fast-changing + 2 false-premise; FreshEval-промпты там же |
| FRAMES | [HF google/frames](https://huggingface.co/datasets/google/frames) | CSV: question, answer, **wiki_pages (список золотых URL)** | нет | Gold-URL уже размечены → готовые anchors для hit@k без ручной разметки |
| BrowseComp | [HF openai/browsecomp](https://huggingface.co/datasets/openai/browsecomp) (gated) |.parquet: problem, hint, answer | нет | Опционально 2–3 q как «экстремальный» тест |
| MIRACL (ru) | [HF miracl/miracl](https://huggingface.co/datasets/miracl/miracl) | queries/qrels/корпус | **да** | RU-запросы + золотые Wikipedia-страницы → RU-подмножество нашего бенча |
| RusBEIR / SberQuAD | [github kaengreg/rusBeIR](https://github.com/kaengreg/rusBeIR), [arxiv 2504.12879](https://arxiv.org/html/2504.12879v1) | tsv (qrels) | **да** | Запасной RU-источник (SberQuAD 45k q) |

Практика: полный download не нужен — у всех есть прямой CSV/parquet; для 30 запросов качаем руками один раз и кладём в `bench/datasets/`.

---

## 4. Паттерны чужих eval-harness'ов

### 4.1 tavily-ai/tavily-SimpleQA (github)
Эталонный паттерн «провайдер-сравнение»:
- **Два трека**: (1) answer accuracy на SimpleQA, (2) **document relevance** на динамических датасетах (через QuotientAI + их open-source [Dynamic Eval Dataset Generator](https://github.com/Eyalbenba/tavily-web-eval-generator) — генерирует свежие запросы+страницы по теме).
- `config.json` хранит параметры вызова каждого провайдера (симметричность бюджетов).
- Параллельные независимые пайплайны per provider, **checkpoint/resume** при обрывах.
- Их результаты (reader gpt-4.1, 2025): Tavily 93.3% / Perplexity Search 85.92% / Google-SERPer 82.15% / **Brave 76.05% / Exa 71.24%**; по document relevance: Tavily 83.0 / PPLX 71.2 / Google 58.1 / Brave 56.2 / **Exa 51.3**. (Самооценка вендора — верить с поправкой, но методология воспроизводима.)
- Более свежий пост (SealQA, та же схема: max_results=10 → reader gpt-5.4-mini → grader gpt-4.1-mini official prompt): SealQA-0 49.5%, SealQA-Hard 55.7%, SimpleQA 97.6%, «превзойдены Exa Auto, Parallel Advanced, Perplexity, Brave, You.com».

### 4.2 LinkupPlatform/eval-simpleQA (github)
Минималистичный harness от Linkup (одного из наших провайдеров):
- `eval.py --mode evaluate|compare --policy1 X --policy2 Y --num-samples N`; политики = search API + режим (linkup deep/standard, tavily advanced).
- Результаты: `results/{policy}_results.jsonl` (per-question), `{policy}_summary.json`, `{policy}_checkpoint.json` — чекпоинт на каждый вопрос.
- Метрики: F-score, accuracy, attempt-rate, avg latency; ретраи + 5-мин timeout per question.
- Их числа (SelfQA, 2026): Linkup Deep F1 0.910 / Tavily 0.728.

### 4.3 Octen-Team/benchmark-for-accuracy (github) — лучший найденный образец
Полный фреймворк именно для «our search backend vs competitors (exa, brave, tavily, parallel, perplexity)»:
- **Тройная перекрёстная проверка**: pairwise blind judge (win-rate, position-swapped) / objective anchors (hit@1, hit@k по gold URL) / end-to-end agent eval (answer accuracy + official grade).
- **Два режима**: in-house benchmark (свой датасет: синтез запросов → auto-resolve gold answers & URLs → SERP-grounded rubrics → judge) и open-source benchmarks (SimpleQA/FreshQA через тот же harness; тег `meta.benchmark` автоматически выбирает официальный грейдер).
- **Всё JSONL + git-versioned**: любые два прогона напрямую сравнимы, отчёты регенерируются из артефактов (`scripts/benchmark_report`), regression diff между ранами.
- Latency меряют отдельным search-only probe, P50/P90 из **server-reported** времени.
- Их bakeoff (2026-07, single-shot 1 search/query, judge minimax-m2.5): SimpleQA: octen 95.2% / exa-instant 89.2% / parallel-turbo 88.6% / tavily-ultrafast 69.9%; FreshQA: 55.8 / 52.8 / 52.8 / 43.2. Важный урок: **один и тот же провайдер в разных tier'ах даёт разброс в 20+ п.п.** — фиксировать tier/параметры и указывать их в отчёте обязательно.

### 4.4 Прочие
- **LearningCircuit/local-deep-research + ldr-benchmarks**: community-лидерборд (CSV в репо, авто-синк с HF dataset) по SimpleQA/BrowseComp/xbench-DeepSearch; паттерн «результаты коммитятся как данные».
- **Braintrust / autoevals, EvalScope**: готовые обёртки SimpleQA-грейдера (LLMClassifier с официальным промптом) — не писать промпт самому.
- **Parallel blog** (benchmarks Task API на SealQA) — вендорский, но подтверждает: SealQA сейчас главная площадка «вызыва» между search-API.

---

## 5. ПРАКТИЧЕСКИЙ ВЫВОД: как построить наш мини-бенчмарк

**Датасет (~30 q, собрать руками из готового):**
- 12 q — SimpleQA Verified (fixed seed; verify, чтобы ответ нельзя было дать без поиска);
- 6 q — SealQA (seal_0): проверка качества на конфликтной выдаче;
- 6 q — FreshQA fast-changing + 2 false-premise: ось свежести;
- 4 q — наши реальные прод-запросы (из реального использования wsearch);
- 3 q — RU-язычные (свойм головой или из MIRACL-ru; вопрос + gold URL).
- Для каждого: gold answer (из датасета) + gold URL/domain (у FRAMES готово; для остальных — одна ручная проверка, берём первый авторитетный источник из любого API).

**Прогон:**
- Все 7 API, single-shot (1 запрос = 1 вызов, без agent-loop — иначе меряем harness, а не SERP), k=5 (top-5 как у Tavily близко к их 10; можно 3+10 двумя проходами).
- Зафиксировать и записать в отчёт: endpoint-параметры каждого провайдера (tier! — урок Octen про 20 п.п. разброса), дату/время прогона, reader-модель и judge-модель (одни на всех; судья ≠ ридер).
- Сырые ответы складывать в JSONL (query_id, provider, raw SERP, latency) — git-versioned, per Octen; чекпоинт после каждого вопроса, per Linkup.

**Метрики (primary → secondary):**
1. **hit@3 по gold URL/domain** — основной (объективный, различимый на N=30);
2. **LLM-judge relevance@3, reference-free 0/1/2** — второй сигнал (Tavily/Quotient: сильнее answer-only);
3. answer accuracy + F1/CGA на SimpleQA-подмножестве (официальный грейдер из autoevals);
4. freshness: judge «актуально ли на дату» + возраст страниц из published_date;
5. ops: latency P50/P90 (client-side честнее для нас — мы выбираем API, а не их бэкенд), error-rate, доля дубликатов/пустых результатов.

**Анализ:** Wilson CI для всех долей; при N=30 не делать выводов по accuracy-разницам <15 п.п.; финальную пару-тройку фаворитов прогнать через pairwise blind judge (порядок свопнут) — это дёшево (21×30 судейств не нужно, только 3 пары × 30).

**Чего не делать:** nDCG@10 как основная метрика (стоимость полной разметки не окупается на 30 запросах); BrowseComp/GAIA как основной инструмент (agentic-шум); полный SimpleQA (4326 q) — жглот квот без новой информации против 30-q сэмпла + CI.

---

## Источники
- SimpleQA: https://openai.com/index/introducing-simpleqa · https://arxiv.org/html/2411.04368v1 · Verified: https://arxiv.org/html/2509.07968v2
- SealQA: https://arxiv.org/abs/2506.01062 · https://huggingface.co/datasets/vtllms/sealqa
- FreshQA/FreshEval: https://arxiv.org/html/2310.03214v1 · https://github.com/freshllms/freshqa · https://docs.nvidia.com/aiq-blueprint/2.0.0/evaluation/benchmarks/freshqa.html
- FRAMES: https://arxiv.org/html/2409.12941v3 · https://huggingface.co/datasets/google/frames
- BrowseComp: https://openai.com/index/browsecomp · GAIA: https://arxiv.org/abs/2311.12983
- BEIR: https://arxiv.org/abs/2104.08663 · https://ir-datasets.com/beir.html · Elastic про nDCG@10: https://www.elastic.co/search-labs/blog/evaluating-search-relevance-part-1
- MIRACL: https://project-miracl.github.io · https://huggingface.co/datasets/miracl/miracl
- RusBEIR: https://arxiv.org/html/2504.12879v1 · https://github.com/kaengreg/rusBeIR
- Harness'ы: https://github.com/tavily-ai/tavily-SimpleQA · https://github.com/LinkupPlatform/eval-simpleQA · https://github.com/Octen-Team/benchmark-for-accuracy · https://github.com/Eyalbenba/tavily-web-eval-generator · https://github.com/LearningCircuit/ldr-benchmarks
- Блоги: Tavily SimpleQA SOTA — https://tavily.com/blog/tavily-evaluation-part-1-tavily-achieves-sota-on-simpleqa-benchmark · Tavily SealQA #1 — https://www.tavily.com/blog/tavily-ranks-1-on-sealqa-and-simpleqa · Parallel SealQA — https://parallel.ai/blog/benchmarks-task-api-sealqa
- LLM-as-judge: https://www.evidentlyai.com/llm-guide/llm-as-a-judge · autoevals SimpleQA grader — https://www.braintrust.dev/docs/cookbook/recipes/SimpleQA
