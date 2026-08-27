# local-extract — локальный каскад fetch+extract для wsearch

Отдельный uv-проект (сам `wsearch` остаётся stdlib-only). Вызывается subprocess-ом:
`.venv/bin/python -m local_extract <url> --max-chars N` → один JSON на stdout.

## Setup (один раз)

```bash
cd local-extract
uv sync                                # venv + зависимости + uv.lock
uv run playwright install chromium     # браузер для SPA-тира (~300 МБ)
```

## Каскад

```
httpx (10 c) ── блок/сбой ──> curl_cffi impersonate=chrome (15 c)
   │                                   │
   │ js-пустышка ──── hydration? ──> успех без браузера
   └──────────────────────────────> playwright chromium (<=25 c goto,
                                     networkidle с таймаутом, при таймауте —
                                     берём что отрендерилось)
любая ступень: trafilatura (markdown, F1 0.924); <200 симв. или challenge — провал
```

Провал (exit 3, JSON с reason) = wsearch фолбэчит на сервисных провайдеров.
PDF — сразу провал (unsupported/pdf, работа для firecrawl).

## CLI

```bash
.venv/bin/python -m local_extract https://example.com
.venv/bin/python -m local_extract https://spa.site --tier browser   # форс ступени
```

Протокол: `protocol.py` (exit 0 ok / 1 crash / 2 usage / 3 clean-fail).
