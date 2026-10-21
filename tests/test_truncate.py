"""smart_truncate: резка по границам, не посреди токена (фаза 1.1, 2026-10-19).

Run: python3 -m unittest discover tests -v
Мотивация и протокол замеров: docs/improvement-plan-2026-10-19.md (фаза 1),
baseline-замер обрезов — bench-extract/measure_cut.py.
"""

from __future__ import annotations

import unittest

from engine.truncate import smart_truncate


def para(n: int = 40, word: str = "слово") -> str:
    return " ".join(word for _ in range(n))


class SmartTruncateTest(unittest.TestCase):
    def test_short_untouched(self):
        text = "короткий текст"
        self.assertEqual(smart_truncate(text, 100), text)

    def test_sentence_boundary(self):
        # 10 предложений; лимит приходится на середину 6-го
        text = ". ".join(f"Предложение номер {i} с хвостом из пары слов" for i in range(1, 11)) + "."
        out = smart_truncate(text, 200)
        self.assertLessEqual(len(out), 200)
        self.assertTrue(out.rstrip().endswith("."), f"нет границы: ...{out[-40:]!r}")
        self.assertTrue(out.startswith("Предложение номер 1"))

    def test_paragraph_boundary_preferred_when_closest(self):
        text = para(30) + "\n\n" + para(30) + "\n\n" + para(30)
        limit = len(text) - 50          # внутри последнего абзаца
        out = smart_truncate(text, limit)
        # граница предложения внутри абзаца ближе, чем \n\n — берём её
        self.assertLessEqual(len(out), limit)
        self.assertNotIn("слово слово слово слово", out[-20:])

    def test_fallback_hard_cut_when_no_boundary(self):
        # один гигантский абзац без точек: окно отката не найдёт границу
        text = "б" * 5000
        out = smart_truncate(text, 500)
        self.assertEqual(len(out), 500)      # старое поведение: тупой рез
        self.assertEqual(out, "b" * 0 or out)  # sanity: непустой

    def test_code_fence_not_left_open(self):
        body = para(20) + "\n\n```python\n" + "\n".join(f"x{i} = {i}" for i in range(60)) + "\n```"
        limit = len(body) - 30          # внутри code-блока
        out = smart_truncate(body, limit)
        self.assertEqual(out.count("```") % 2, 0, "fence остался незакрытым")
        self.assertTrue(out.rstrip().endswith(("```", str(out.rstrip()[-3:]))))

    def test_fence_near_limit_dropped_entirely(self):
        body = para(40) + "\n\n```python\ncode_line_1\ncode_line_2"
        limit = len(body) - 10
        out = smart_truncate(body, limit)
        self.assertNotIn("```", out, "огрызок fence у лимита надо выкинуть")

    def test_pretty_json_cut_on_line(self):
        obj = "{\n" + ",\n".join(f'  "key{i}": "value {i}"' for i in range(200)) + "\n}"
        limit = 900
        out = smart_truncate(obj, limit)
        self.assertLessEqual(len(out), limit)
        last_line = out.rstrip().splitlines()[-1].rstrip()
        self.assertTrue(last_line.endswith((",", "{", "}")),
                        f"JSON режется посреди строки: {last_line!r}")

    def test_minified_json_falls_back(self):
        obj = '{"a":1,' * 500 + '"end":0}'
        out = smart_truncate(obj, 333)
        self.assertEqual(len(out), 333)       # тупой рез: границ нет

    def test_markdown_struct_line_boundary(self):
        text = para(60) + "\n\n## Заголовок секции\n\n" + para(60)
        limit = len(text) - 100
        out = smart_truncate(text, limit)
        self.assertFalse(out.rstrip().startswith("##"), "не должен начинаться с заголовка-огрызка")

    def test_backoff_window_respected(self):
        # граница есть, но далеко за окном отката → тупой рез (сохраняем объём)
        text = para(200) + ". Конец." + " хвост без точек и границ " * 100
        limit = 2000
        out = smart_truncate(text, limit)
        self.assertGreater(len(out), 2000 * 0.8, "откат съел слишком много текста")


if __name__ == "__main__":
    unittest.main()
