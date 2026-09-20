"""Синхронность двух реализаций t.me-нормализации.

Дубль существует осознанно (wsearch stdlib не может импортить local-extract
uv-проект — subprocess-контракт), но обязан не расходиться: этот тест гоняет
один и тот же набор URL через engine.router._normalize_fetch_url и
local_extract.tg.normalize_url и требует побитового совпадения.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "local-extract", "src"))

from engine import router  # noqa: E402
from local_extract import tg  # noqa: E402

URLS = [
    "https://t.me/demo_empty",
    "https://t.me/demo_missing",
    "https://t.me/demo_ch3",
    "https://t.me/demo_ch4",
    "https://t.me/durov/528",
    "https://telegram.me/durov",
    "https://telegram.dog/durov/1",
    "https://t.me/s/durov",
    "https://t.me/s/durov?before=528",
    "https://t.me/+AbCdEf123",
    "https://t.me/joinchat/xyz",
    "https://habr.com/ru/all/",
    "https://example.com/",
]


class TestTgUrlSync(unittest.TestCase):
    def test_normalize_duplicates_in_sync(self):
        for u in URLS:
            self.assertEqual(router._normalize_fetch_url(u),
                             tg.normalize_url(u), u)

    def test_invite_detection_in_sync(self):
        for u in URLS:
            self.assertEqual(router._is_tg_invite(u),
                             tg.is_invite_url(u) and tg.is_tg_url(u), u)


if __name__ == "__main__":
    unittest.main()
