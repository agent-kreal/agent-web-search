"""Adaptive backfill, финальная редакция (фаза 4.2 после решения 19.10):
триггер только по фейл-запросам fan-out. Покрытие/домены срезаны по данным
probe (шумовой X портил топ: P@10 0.64→0.40).
Run: python3 -m unittest discover tests -v
"""

from __future__ import annotations

import unittest

from engine.backfill import backfill_queries, key_terms, should_backfill


QUERIES = ["uv pip install corporate proxy error",
           "uv python install SSL error behind proxy",
           "uv pip proxy configuration env vars"]


class KeyTermsTest(unittest.TestCase):
    def test_common_terms_weighed(self):
        w = key_terms(QUERIES)
        self.assertEqual(w["proxy"], 3)     # во всех трёх
        self.assertEqual(w["uv"], 3)
        self.assertEqual(w["ssl"], 1)

    def test_short_tokens_counted(self):
        w = key_terms(["Ангара-А5 запуск 2026"])
        self.assertIn("а5", w)              # 2 символа — но имя предмета
        self.assertIn("2026", w)

    def test_stopwords_dropped(self):
        w = key_terms(["how to install the package"])
        self.assertNotIn("how", w)
        self.assertNotIn("the", w)
        self.assertIn("install", w)


class ShouldBackfillTest(unittest.TestCase):
    def test_failed_queries_trigger(self):
        trig, why = should_backfill([QUERIES[0]])
        self.assertTrue(trig)
        self.assertIn("failed_queries=1", why)

    def test_no_failures_no_trigger(self):
        # покрытие/домены больше не триггерят (срезаны по данным probe)
        trig, why = should_backfill([])
        self.assertFalse(trig)
        self.assertEqual(why, "")


class BackfillQueriesTest(unittest.TestCase):
    def test_docs_intent_templates(self):
        qs = backfill_queries(["caddy dns challenge config broken",
                               "caddy acme dns provider down"], "docs")
        self.assertEqual(len(qs), 2)
        self.assertTrue(any("documentation" in q for q in qs))

    def test_ru_intent_templates(self):
        qs = backfill_queries(["автоматический бэкап time machine завис"],
                              "ru")
        self.assertTrue(any("что это" in q or "документация" in q for q in qs))

    def test_specific_over_generic_on_tie(self):
        # при равных весах берётся специфичный терм, не служебный «error»
        qs = backfill_queries(["ssl handshake error"], "debug")
        self.assertTrue(any("handshake" in q.lower() for q in qs))
        self.assertFalse(any(q.count("error") > 1 for q in qs))

    def test_template_words_not_used_as_x(self):
        qs = backfill_queries(["supabase documentation search"], "docs")
        joined = " ".join(qs)
        self.assertNotIn("documentation documentation", joined)
        self.assertIn("supabase", joined)

    def test_original_case_preserved(self):
        qs = backfill_queries(["Supabase RLS setup broken"], "docs")
        self.assertTrue(any("RLS" in q or "Supabase" in q for q in qs))

    def test_no_terms_no_queries(self):
        self.assertEqual(backfill_queries(["как как как"], None), [])


if __name__ == "__main__":
    unittest.main()
