# bench-extract: бенчмарк экстракторов (local-каскад vs сервисные)

Полный план: `~/.claude/plans/snazzy-churning-pixel.md` (утверждён 27.08.2026).
Соседний `bench/` (бенчмарк поиска) — другой чат, не трогаем.

## Участники

local-auto / local-http / local-curl / local-browser (бесплатно, напрямую venv —
полный JSON c tier/trace) против firecrawl (~1837 мес), tavily (~886 мес),
jina (keyless), parallel (12 URL, $-грант).

## Этапы

- [x] **A. WCXB-самопроверка ядра** — `run_wcxb.py` + `wcxb-notes.md`.
  Итог: наш конфиг ≈ vanilla trafilatura (F1 0.832 vs 0.829 на 300 стр),
  тюнить нечего; markdown-обвес стоит ~5 п. F1 только в word-F1-метрике.
  Слабые типы ядра: product/listing/forum (0.6-0.7).
- [x] **B1. Датасет** — `dataset.jsonl`: 35 URL, 9 сценариев
  (static-docs 4, article-en 5, article-ru 4, spa-app 4, docs-js 5, forum 4,
  antibot 3, pdf 3, tables 3), все live-проверены 27.08. Сниппет-золото:
  with[] (из полного local-auto markdown) + without[] (стандартный boiler ∩
  текст страницы), сборщик — `make_snippet_material.py` → tmp-full/.
- [x] **B2. Прогон** — `run_bench.py` (resume-safe, троттлинг, head/mid 2k+2k
  в raw.jsonl). 258 пар. Найденные и починенные по ходу баги тула:
  firecrawl 429=rate-limit ошибочно помечал провайдера исчерпанным на МЕСЯЦ
  (чинено: 429 → cooldown 90с, 402 → месяц; sleep в раннере 4с);
  jina падал UnicodeEncodeError на кириллических URL (чинено: percent-encode);
  раннер получил --retry-failed.
- [x] **B3. Объективщина** — `grade.py` → results/grade.json.
  Ключевое: local-auto 80% ok (провалы: SO, antibot×3, pdf×3 — почти всё by
  design), with_recall 96% (self-bias: фразы из local-markdown), firecrawl
  with_recall 50% + without_rate 32% (навигация разбавляет), tavily ok 100%
  но empty 17%, parallel — пересказы с "..." (chars_med 3688).
- [x] **B4. Джадж** — все 9 scores_*.jsonl готовы (субагенты sonnet-слот;
  static-docs вручную). Находки: антибот — только firecrawl реален; pdf —
  jina лучший; article-ru/docs-js/tables — local доминирует; forum —
  jina structure лучшая, local чист на семантичном HTML; HN — s.gif-мусор
  у local; tavily: empty-«успехи» 17%, wiki-тела вытеснены TOC.
- [x] **B5. Агрегация** — `aggregate.py`; по ходу чинены: ключ rows по url
  (весь quality падал в judge-only), нормализация метрики (`&lt;br&gt;`-вставки
  firecrawl, дефис-переносы PDF-tavily, entities) в grade.py:norm.
- [x] **C. Отчёт** — `REPORT.md` (TL;DR, методика+оговорки, overall,
  матрица с ok/n, «сценарий → экстрактор», экономика ~80%, v2, бюджет-факт,
  черновик SKILL.md-дописки). Осталось: согласование с владельцем →
  SKILL.md + CLAUDE.md-починка → коммит.

## Бюджет (факт против плана)

| провайдер | план | примечание |
|---|---|---|
| firecrawl | 35 | 2% от 1837 |
| tavily | 35 | ~4% от 886 (общий мешок с search-бенчем соседа!) |
| parallel | 12 | $-грант, ~$0.5-1 |
| jina, local, WCXB | 0 | — |
