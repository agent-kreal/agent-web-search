"""strip_junk: консервативный prefilter UI&nav/metadata/ads (фаза 1.2, 19.10).

Run: python3 -m unittest discover tests -v
Критерий консервативности: контентные строки с «share»/«cookie» внутри
предложения НЕ трогаются; code-fence не трогается вообще.
"""

from __future__ import annotations

import unittest

from engine.prefilter import strip_junk


class StripJunkTest(unittest.TestCase):
    def test_anchor_run_removed(self):
        nav = "\n".join(f"- [Section {i}](#section-{i})" for i in range(1, 6))
        text = "# Title\n\n" + nav + "\n\nПолезный текст первого раздела. Продолжение мысли.\n"
        out, stats = strip_junk(text)
        self.assertEqual(stats["ui_nav"], 5)
        self.assertNotIn("](#", out)
        self.assertIn("Полезный текст", out)

    def test_two_anchors_kept(self):
        # меньше NAV_RUN_MIN подряд — НЕ мусор (может быть легитимным списком
        # из пары ссылок внутри контента)
        nav = "- [A](#a)\n- [B](#b)\n"
        out, stats = strip_junk("Текст до.\n\n" + nav + "Текст после.\n")
        self.assertEqual(stats["ui_nav"], 0)
        self.assertIn("[A](#a)", out)

    def test_breadcrumb_removed(self):
        crumb = "[Home](https://x.com) / [Docs](https://x.com/d) / [API](https://x.com/a)"
        out, stats = strip_junk("Статья.\n\n" + crumb + "\n\nТело статьи.\n")
        self.assertNotIn("[Home]", out)
        self.assertIn("Тело статьи", out)

    def test_metadata_lines_removed(self):
        junk = "\n".join([
            "All rights reserved.",
            "© 2026 Example Corp",
            "Share this article",
            "Follow us on Twitter",
            "Subscribe to our newsletter!",
            "We use cookies to improve your experience",
        ])
        out, stats = strip_junk(junk + "\n\nКонтент остался.\n")
        self.assertEqual(stats["metadata"], 6)
        self.assertIn("Контент остался.", out)

    def test_content_words_not_touched(self):
        # «share»/«cookie» ВНУТРИ предложения с другим текстом — не мусор
        text = ("Market share of the product grew. "
                "The browser stores a cookie per session, which matters. "
                "Follow the algorithm described below.\n")
        out, stats = strip_junk(text)
        self.assertEqual(stats["metadata"], 0)
        self.assertEqual(out.strip(), text.strip())

    def test_code_fence_protected(self):
        code = "```markdown\n- [x](#a)\n- [y](#b)\n- [z](#c)\nAll rights reserved.\n```"
        out, stats = strip_junk("Intro.\n\n" + code + "\n\nOutro.\n")
        self.assertEqual(stats["ui_nav"], 0)
        self.assertEqual(stats["metadata"], 0)
        self.assertIn("- [x](#a)", out)

    def test_social_row_removed(self):
        row = "[Twitter](https://twitter.com/x) | [LinkedIn](https://linkedin.com/x)"
        out, stats = strip_junk("Текст.\n\n" + row + "\n\nЕщё текст.\n")
        self.assertEqual(stats["ads"], 1)
        self.assertNotIn("twitter.com", out)

    def test_empty(self):
        self.assertEqual(strip_junk(""), ("", {"ui_nav": 0, "metadata": 0,
                                               "ads": 0, "chars_removed": 0}))


if __name__ == "__main__":
    unittest.main()
