#!/usr/bin/env python3
"""Сборка материала для сниппет-золота датасета части B.

На каждый URL датасета:
  tmp-full/<q>.md          — полный markdown от local-auto (32k) — источник with[]
  tmp-full/<q>.meta.json   — ok/tier/elapsed_ms прогона
  tmp-full/<q>.htmltext.txt— сырой текст HTML (httpx + strip тегов) — источник
                             проверок «фраза есть на странице»
  tmp-full/<q>.boiler.json — стандартные boiler-фразы, реально встречающиеся на
                             странице → кандидаты without[]

Запуск: local-extract/.venv/bin/python bench-extract/make_snippet_material.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "bench-extract"
VENV_PY = str(ROOT / "local-extract" / ".venv" / "bin" / "python")
TMP = BENCH / "tmp-full"

# 2+ слов — меньше false-positive против «Home»/«Search» в контенте
BOILER = [
    "Skip to content", "Accept all cookies", "Accept all", "Cookie settings",
    "All rights reserved", "Privacy Policy", "Privacy policy", "Terms of Service",
    "Terms of Use", "Sign in", "Log in", "Sign up", "Subscribe to",
    "Follow us", "Contact us", "Back to top", "Subscribe now", "Get started",
    "Learn More", "Read More", "Related Articles", "Share this",
    "Все права защищены", "Политика конфиденциальности",
    "Пользовательское соглашение", "Войти", "Регистрация", "Подписаться на",
    "Обратная связь", "Связаться с нами", "Все новости", "Главные новости",
]


class TextExtract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.chunks: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip and data.strip():
            self.chunks.append(data.strip())


def main() -> int:
    TMP.mkdir(exist_ok=True)
    rows = [json.loads(l) for l in (BENCH / "dataset.jsonl").read_text().splitlines() if l.strip()]
    for row in rows:
        key = f"{row['scenario']}-{row['q']}"      # уникально (q дублируется между сценариями)
        url = row["url"]
        md_p, html_p = TMP / f"{key}.md", TMP / f"{key}.htmltext.txt"
        if md_p.exists() and html_p.exists():
            print(f"[{key}] уже есть, скип")
            continue
        # 1) local-auto полный прогон
        p = subprocess.run([VENV_PY, "-m", "local_extract", url, "--max-chars", "32000"],
                           capture_output=True, text=True, timeout=90)
        try:
            d = json.loads(p.stdout)
        except json.JSONDecodeError:
            d = {"ok": False, "reason": "bad-json", "stderr": p.stderr[:300]}
        (TMP / f"{key}.meta.json").write_text(json.dumps(
            {"ok": d.get("ok"), "tier": d.get("tier"), "elapsed_ms": d.get("elapsed_ms"),
             "reason": d.get("reason"), "title": d.get("title")}, ensure_ascii=False))
        md_p.write_text(d.get("content") or "", encoding="utf-8")
        # 2) сырой HTML -> текст (для without-кандидатов и валидации with)
        text = ""
        try:
            r = httpx.get(url, timeout=20, follow_redirects=True,
                          headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                 "Chrome/139.0.0.0 Safari/537.36"})
            parser = TextExtract()
            parser.feed(r.text)
            text = " ".join(parser.chunks)
        except Exception as e:
            text = f"__FETCH_FAILED__ {type(e).__name__}"
        html_p.write_text(text[:200_000], encoding="utf-8")
        boiler = [b for b in BOILER if b.lower() in text.lower()][:6]
        (TMP / f"{key}.boiler.json").write_text(json.dumps(boiler, ensure_ascii=False))
        print(f"[{key}] {row['scenario']:<12} ok={d.get('ok')} tier={d.get('tier')} "
              f"md_len={len(md_p.read_text())} boiler={len(boiler)} {url}")
    print("готово")
    return 0


if __name__ == "__main__":
    sys.exit(main())
