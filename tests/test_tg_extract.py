"""tg.py: парсер Telegram web preview — чистые функции, без сети.

Fixtures сняты с живых страниц 20.09.2026. Парсер stdlib-only, поэтому
тесты идут системным python без local-extract venv — как остальные тесты
engine (unittest, см. README).
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "local-extract", "src"))

from local_extract import tg  # noqa: E402

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


class TestNormalizeUrl(unittest.TestCase):
    CASES = [
        # t.me/<канал> без /s/ (страница-приглашение без постов)
        ("https://t.me/demo_empty", "https://t.me/s/demo_empty"),
        ("https://t.me/demo_missing", "https://t.me/s/demo_missing"),
        ("https://t.me/demo_ch3", "https://t.me/s/demo_ch3"),
        ("https://t.me/demo_ch4", "https://t.me/s/demo_ch4"),
        # пост-ссылка, алиасы домена, уже-нормальные, query, схема
        ("https://t.me/durov/528", "https://t.me/s/durov/528"),
        ("https://telegram.me/durov", "https://t.me/s/durov"),
        ("https://telegram.dog/durov/1", "https://t.me/s/durov/1"),
        ("https://t.me/s/durov", "https://t.me/s/durov"),
        ("https://t.me/s/durov/528", "https://t.me/s/durov/528"),
        ("https://t.me/s/durov?before=528", "https://t.me/s/durov?before=528"),
        ("http://t.me/durov", "http://t.me/s/durov"),
        # не трогаем: инвайты, чужие домены
        ("https://t.me/+AbCdEf123", "https://t.me/+AbCdEf123"),
        ("https://t.me/joinchat/xyz", "https://t.me/joinchat/xyz"),
        ("https://example.com/t.me/durov", "https://example.com/t.me/durov"),
        ("https://habr.com/ru/all/", "https://habr.com/ru/all/"),
    ]

    def test_normalize(self):
        for raw, norm in self.CASES:
            self.assertEqual(tg.normalize_url(raw), norm, raw)

    def test_normalize_service_path_side_effect(self):
        # служебные пути телеграма (/settings, /share) тоже получают /s/:
        # телеграм отвечает на них своей страницей без постов -> парсер
        # честно скажет «no posts». Побочный, безопасный кейс.
        self.assertEqual(tg.normalize_url("https://t.me/settings"),
                         "https://t.me/s/settings")

    def test_is_invite_url(self):
        yes = ["https://t.me/+AbCdEf123", "https://t.me/joinchat/xyz",
               "https://telegram.me/+xyz"]
        no = ["https://t.me/s/durov", "https://t.me/durov",
              "https://habr.com/+xyz"]
        for u in yes:
            self.assertTrue(tg.is_invite_url(u), u)
        for u in no:
            self.assertFalse(tg.is_invite_url(u), u)

    def test_is_tg_url(self):
        yes = ["https://t.me/s/durov", "https://telegram.me/durov",
               "https://TELEGRAM.DOG/durov"]
        no = ["https://habr.com", "https://not-t.me/durov"]
        for u in yes:
            self.assertTrue(tg.is_tg_url(u), u)
        for u in no:
            self.assertFalse(tg.is_tg_url(u), u)


def _fixture(name: str) -> bytes:
    with open(os.path.join(FIX, name), "rb") as f:
        return f.read()


class TestExtract(unittest.TestCase):
    def test_live_channel(self):
        md, title, n, note = tg.extract(_fixture("tg_durov.html"))
        self.assertEqual(n, 10)
        self.assertTrue(md and not note)
        self.assertTrue(title.startswith("Telegram: @durov (Pavel Durov)"))
        # структура: заголовки постов с id, датой, просмотрами
        self.assertIn("## durov/", md)
        self.assertIn("UTC", md)
        self.assertIn("views", md)
        # эмодзи из tg-emoji фолбэка (<b>⛔️</b> внутри CSS-спрайта)
        self.assertIn("⛔️", md)
        # переносы <br> сохранились абзацами
        self.assertIn("\n\n", md)
        # link_preview: сайт—заголовок—описание—URL одной строкой
        self.assertIn("→ ", md)
        self.assertIn("https://", md)

    def test_target_post_marked(self):
        md, _t, n, _note = tg.extract(_fixture("tg_durov.html"), "durov/526")
        if n == 10:  # пост мог не попасть в обрезанный fixture
            self.assertEqual("← запрошенный пост" in md,
                             "## durov/526" in md)

    def test_contact_page(self):
        md, _title, n, note = tg.extract(_fixture("tg_contact.html"))
        self.assertIsNone(md)
        self.assertEqual(n, 0)
        self.assertIn("not found or private", note)

    def test_empty_channel(self):
        md, _title, n, note = tg.extract(_fixture("tg_empty.html"))
        self.assertIsNone(md)
        self.assertEqual(n, 0)
        self.assertIn("no posts", note)

    def test_garbage(self):
        md, _t, n, note = tg.extract(b"<html><body>garbage</body></html>")
        self.assertIsNone(md)
        self.assertEqual(n, 0)
        self.assertIn("no posts", note)


if __name__ == "__main__":
    unittest.main()
