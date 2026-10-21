"""RRF-слияние fan-out (фаза 4.1, 2026-10-19).

multi до 4.1 конкатенировал выдачи в порядке завершения потоков — ранг был
случайностью таймингов. rrf_merge считает score = sum 1/(60+rank) по всем
запросам×провайдерам. Run: python3 -m unittest discover tests -v
"""

from __future__ import annotations

import unittest

from engine.merge import norm_url, rrf_merge


class NormUrlTest(unittest.TestCase):
    def test_fragment_and_utm_stripped(self):
        self.assertEqual(norm_url("https://Example.com/a?utm_source=x&id=1#frag"),
                         "https://example.com/a?id=1")

    def test_plain_untouched(self):
        self.assertEqual(norm_url("https://example.com/A/b"), "https://example.com/A/b")

    def test_empty(self):
        self.assertEqual(norm_url(""), "")


class RrfMergeTest(unittest.TestCase):
    def test_overlap_outranks_singletons(self):
        # url-a в топе обоих списков → RRF выше любого одиночного топа
        a = [{"url": "https://x/a", "title": "A", "snippet": "s", "provider": "p1"},
             {"url": "https://x/b", "title": "B", "snippet": "s", "provider": "p1"}]
        b = [{"url": "https://x/a?utm_source=t", "title": "A2", "snippet": "s2", "provider": "p2"},
             {"url": "https://x/c", "title": "C", "snippet": "s", "provider": "p2"}]
        merged = rrf_merge([a, b], source_names=["q1", "q2"])
        self.assertEqual(merged[0].url, "https://x/a")
        self.assertAlmostEqual(merged[0].score, 2 / 61)
        self.assertEqual(len(merged), 3)

    def test_dedupe_by_norm_url_keeps_best_rank_fields(self):
        # одна и та же страница с utm и без: схлопываются, поля — от лучшего ранга
        a = [{"url": "https://x/a", "title": "чистый", "snippet": "s1", "provider": "p1"}]
        b = [{"url": "https://x/a?utm_campaign=z", "title": "грязный",
              "snippet": "s2", "provider": "p2"}]
        merged = rrf_merge([a, b], source_names=["q1", "q2"])
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0].title, "чистый")
        self.assertEqual(merged[0].sources, ["q1", "q2"])

    def test_tie_break_deterministic(self):
        # одинаковый score у одиночных топ-1 → сортировка стабильна (порядок
        # первого появления), не зависит от таймингов потоков
        a = [{"url": f"https://x/{i}", "title": str(i), "snippet": "s", "provider": "p"}
             for i in range(3)]
        b = [{"url": f"https://y/{i}", "title": str(i), "snippet": "s", "provider": "p"}
             for i in range(3)]
        m1 = [m.url for m in rrf_merge([a, b], source_names=["q1", "q2"])]
        m2 = [m.url for m in rrf_merge([a, b], source_names=["q1", "q2"])]
        self.assertEqual(m1, m2)
        self.assertEqual(m1[0], "https://x/0")

    def test_empty_lists(self):
        self.assertEqual(rrf_merge([[], []], source_names=["q1", "q2"]), [])

    def test_to_dict_shape(self):
        a = [{"url": "https://x/a", "title": "A", "snippet": "s",
              "date": "2026-01-01", "provider": "p"}]
        d = rrf_merge([a], source_names=["q1"])[0].to_dict()
        self.assertEqual(d["queries"], ["q1"])
        self.assertIn("rrf", d)
        self.assertEqual(d["date"], "2026-01-01")


if __name__ == "__main__":
    unittest.main()
