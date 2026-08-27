# Часть A: самопроверка ядра local-extract на WCXB (2026-08-27)

Наши данные: 300 стр dev-сплита (стратифицированно, min 8 на тип), метрики —
код WCXB (`word_f1`, `snippet_check`), тот же venv/trafilatura для всех трёх
конфигов. Прогон: `run_wcxb.py`, сырые числа: `results/wcxb-summary.json`.

## Результаты

| config | F1 | P | R | with↑ | without↓ |
|---|---|---|---|---|---|
| ours-md (боевой markdown, frontmatter срезан) | 0.777 | 0.765 | 0.856 | 60.6% | 8.9% |
| ours-text (наш md → strip_markdown → plain) | **0.832** | 0.870 | 0.849 | 70.3% | 8.2% |
| vanilla (trafilatura.extract без флагов) | 0.829 | 0.868 | 0.847 | 72.9% | 7.8% |

Per-type F1 (ours-text / vanilla): article 0.92/0.92, documentation 0.95/0.96,
service 0.79/0.80, forum 0.71/0.72, product 0.66/0.68, collection 0.62/0.60,
listing 0.65/0.59.

## Выводы

1. **Ядро валидировано: наш конфиг (markdown + include_links/images + no
   comments) НЕ проседает против vanilla trafilatura** (0.832 vs 0.829 при
   честном приведении к plain). Тюнить флаги нечего — разницы нет.
2. **Markdown-обвес стоит ~5 п. F1 в word-F1-метрике** (0.777 vs 0.832) — это
   плата формата (URL в `[x](url)`, маркеры), а не качество извлечения: для
   LLM-потребителя markdown богаче. Вывод: сравнивать markdown-экстракторы
   word-F1 по plain-gold можно только после strip; в части B основной метрикой
   качества будут сниппеты + джадж, а не word-F1.
3. Если когда-нибудь нужен plain text на выходе — дешёвый `strip_markdown()`
   почти не теряет против нативного plain (0.832 vs 0.829).
4. **Слабые типы ядра trafilatura: product (0.66), listing (0.65), collection
   (0.62), forum (0.71)** против article 0.92 / docs 0.95. Гипотеза в часть B:
   на форумах и «витринных» страницах сервисные экстракторы (firecrawl) могут
   отыгрываться — проверяем классом `forum`.
5. Наш агрегат 0.83 ниже публикуемого либорда (trafilatura 0.958,
   rs_trafilatura 0.970) из-за методологии: либорд — среднее по всему
   dev-сплиту (article ≈ 70% веса), у нас равномерная стратификация
   (product/listing тянут вниз). На article-классе у нас 0.92.

Тюнинг конфига по итогам части A: **не требуется**.
