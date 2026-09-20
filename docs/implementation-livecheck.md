# План: серверная истина по квотам (livecheck) вместо виртуального счётчика

Дата: 2026-09-09. Статус: план согласован, к реализации.
Контекст: аудит `state/usage.jsonl` (09.09) показал — эпизод 03.09, когда 429 rate-limit
ошибочно заглушил exa на месяц при живом балансе $19.20 (потрачено всего $1.47).
Корневая причина: локальный счётчик вызовов — единственный источник истины о квотах,
реального остатка агент не видит. Этот план перестраивает модель на «server-truth first».

## Исследование (завершено 09.09, факты из доков — проверены)

| Провайдер | Источник истины | Формат | Цена опроса |
|---|---|---|---|
| **firecrawl** | `GET https://api.firecrawl.dev/v2/team/credit-usage` (Bearer `FIRECRAWL_API_KEY`) | remaining credits | бесплатно |
| **linkup** | `GET https://api.linkup.so/v1/credits/balance` (Bearer) | баланс $ | бесплатно |
| **exa** | `GET https://api.exa.ai/team/api-keys/{id}/usage` (тот же `x-api-key`) | **потраченное** за период: `total_cost_usd` + `cost_breakdown`. Баланса в API НЕТ → остаток = грант $10/мес − spent_тек.месяц (стартовые $20 сверху не считаем, консервативно). Месячный grant у free tier капает на дату регистрации, не на 1-е число | бесплатно |
| **brave** | заголовки **каждого** ответа: `X-RateLimit-Limit` (формат `1, 15000` = 1 rps + 15000/мес), `X-RateLimit-Remaining` | остаток запросов | ноль вызовов, пассивно |
| tavily | ❌ API нет, только дашборд app.tavily.com; search depth: `basic/fast/ultra-fast` = 1 кредит, `advanced` = **2 кредита** | — | локальный счётчик |
| zai | ❌ эндпоинта нет; 429 несёт дату сброса — уже парсится (`providers/zai.py:44`) | — | уже покрыто |
| youcom / ddg / jina / parallel-anon | keyless, считать нечего | — | — |

Доки-источники: docs.firecrawl.dev/api-reference/endpoint/credit-usage,
docs.linkup.so/pages/documentation/endpoints/account/balance,
exa.ai/docs/reference/team-management/get-api-key-usage,
api-dashboard.search.brave.com/documentation/guides/rate-limiting,
docs.tavily.com/documentation/api-reference/endpoint/search.

Итог покрытия: все $-лимитированные провайдеры (firecrawl, linkup, exa, brave) — сервером;
подписочные (tavily, zai) — локальный счётчик + их собственные 429-сообщения.

## Фаза 1 — модель данных: quotas.json v2

Сейчас: `{"used": 115, "window_start": ...}` — счётчик вызовов, дрейфует.

Станет (гибрид, приоритет сервера):

```json
"exa": {
  "server": {"unit": "usd", "limit": 10, "remaining": 8.53, "fetched_at": "2026-09-09T15:00:00+00:00"},
  "local":  {"window_start": "2026-09", "used": 115},
  "exhausted_until": null
}
```

Правила `quotas.py::remaining()`:
1. Свежий `server.remaining` (TTL 6 ч) → он **минус** расход локального счётчика
   с момента `fetched_at` (интерполяция между опросами).
2. Сервер недоступен/просрочен → fallback на локальный счётчик (как сейчас).
3. `QuotaSpec.unit: "requests" | "credits" | "usd"` — не смешивать доллары с запросами;
   статусы в родных единицах: `$8.5 left`, `584 credits left`.

Миграция: старые записи читаются как `local`, поля `server` добавляются с Nones.

## Фаза 2 — engine/livecheck.py + команда

- По одному фетчеру на провайдера (firecrawl, linkup, exa), каждый нормализует ответ
  в `{unit, remaining, limit}` и пишет в `quotas.json` под `server`.
- **`wsearch status --live`** — опросить всех keyed, таблица «сервер vs локальная оценка
  vs дрейф», обновить quotas.json.
- Логирование каждой сверки в `state/usage.jsonl`:
  `{"cmd": "livecheck", "provider": "exa", "server_remaining": 8.53, "local_estimated": 8.10, "drift": 0.43}`
  — дрейф счётчика виден в `wsearch usage`, эпизоды типа exa-03.09 перестают быть невидимыми.
- Автоопрос: НЕ в каждом запросе (задержки), а при `wsearch status` + руками `--live`.
  Опция на будущее: TTL-триггер после каждых N spend.

## Фаза 3 — пассивный сбор (ноль вызовов)

- `providers/brave.py`: после каждого успешного ответа читать `X-RateLimit-Remaining`
  → перезаписывать `server.remaining`. Счётчик brave перестаёт дрейфовать.
- `providers/tavily.py`: `advanced` depth = 2 кредита → `spend(count=2)`; сейчас 1:1 — занижаем расход.

## Фаза 4 — интеграция в router и CLI

- `router._skip_reason()`: `server.remaining <= 0` → skip «server: exhausted».
- `wsearch chain` / `status`: серверные остатки с меткой времени сверки.
- exa: локальный `limit=750` остаётся sanity-cap поверх долларового остатка.

## Фаза 5 — проверка и фиксация

1. Живые тесты: по одному вызову на эндпоинт (бесплатные), сверка с дашбордами
   (exa известен: $19.20 на 09.09; firecrawl/linkup глянуть в их дашбордах).
2. Unit-тесты `remaining()` на три ветки: server-fresh / интерполяция / fallback.
3. Обновить README.md и docs/how-it-works.md (раздел квот → «server-truth first»).
4. Коммиты по шагам: модель → livecheck → brave-заголовки → интеграция.

## Открытые вопросы (решатся на первом живом прогоне)

- **exa `id` ключа** для usage-эндпоинта: из дашборда руками или list-endpoint;
  в `.env` как `EXA_KEY_ID`.
- **firecrawl v2 URL** при ключе, выданном на v1 API — проверить (обычно ключ общий).
- Точные JSON-схемы ответов firecrawl/linkup — снять с живых ответов.

## Объём

~180–200 строк: livecheck.py (~100), quotas.py (~40), brave.py (~10), cli.py (~20),
вывод статусов (~15). Обратной совместимости ничего не ломает: провайдеры без
серверного источника работают как раньше.
