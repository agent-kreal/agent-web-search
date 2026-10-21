"""Фаза 5.1: пустой «успех» сервисного fetch-тира = фейл → фолбэк вниз.

bench-extract: tavily 17% «успехов» <200 симв. (wiki-TOC/антибот), jina —
challenge-страницы, firecrawl 3%. Проверка — до fetchcache.put (пустоту
нельзя кэшировать). gh/local exempt: нативные тиры fail loudly, их короткий
вывод — реальный контент. Порог зажат запрошенным cap (raw-cut)."""

import unittest
from unittest import mock

from engine import router
from engine.providers.base import FetchResult, Provider


class FakeFetchProvider(Provider):
    def __init__(self, name: str, content: str, title: str = "t"):
        self.name = name
        self.can_fetch = True
        self._content = content
        self._title = title

    def fetch(self, url: str, *, max_chars: int = 6000) -> FetchResult:
        # имитирует raw_cut-провайдеров: чинит кап сам
        return FetchResult(url=url, title=self._title,
                           content=self._content[:max_chars], provider=self.name)


GOOD = "x" * 500


class FetchMinLenTest(unittest.TestCase):
    def setUp(self):
        self._chain = router.FETCH_CHAIN
        self.addCleanup(setattr, router, "FETCH_CHAIN", self._chain)
        # кэш мимо: чтение пустое, запись перехватываем
        self._get = router.fetchcache.get
        router.fetchcache.get = lambda url: None
        self.addCleanup(setattr, router.fetchcache, "get", self._get)

    def _run(self, chain, **kw):
        router.FETCH_CHAIN = chain
        puts = []
        with mock.patch.object(router.fetchcache, "put",
                               side_effect=lambda *a, **kw: puts.append(kw or a)):
            out = router.fetch("https://x/", use_cache=True, **kw)
        return out, puts

    def test_service_short_falls_down(self):
        out, _ = self._run([FakeFetchProvider("tavily", "коротыш"),
                            FakeFetchProvider("jina", GOOD)])
        self.assertEqual(out["provider"], "jina")
        self.assertEqual(out["tried"][0]["name"], "tavily")
        self.assertIn("empty extraction", out["tried"][0]["error"])

    def test_short_success_not_cached(self):
        _, puts = self._run([FakeFetchProvider("tavily", "коротыш"),
                             FakeFetchProvider("jina", GOOD)])
        # кэшируется только победитель; пустой tavily-«успех» не положен
        self.assertEqual([p["provider"] for p in puts], ["jina"])

    def test_local_short_is_real_content(self):
        out, _ = self._run([FakeFetchProvider("local", "real short page")])
        self.assertEqual(out["provider"], "local")
        self.assertEqual(out["tried"], [])

    def test_gh_short_is_real_content(self):
        out, _ = self._run([FakeFetchProvider("gh", "# tiny readme\n")])
        self.assertEqual(out["provider"], "gh")

    def test_raw_cut_small_cap_no_false_fail(self):
        # raw-cut с max_chars=100: честные 100 симв. — не фейл
        out, _ = self._run([FakeFetchProvider("tavily", "y" * 100)],
                           raw_cut=True, max_chars=100)
        self.assertEqual(out["provider"], "tavily")

    def test_raw_cut_shorter_than_cap_still_fails(self):
        out, _ = self._run([FakeFetchProvider("tavily", "y" * 50),
                            FakeFetchProvider("jina", "z" * 100)],
                           raw_cut=True, max_chars=100)
        self.assertEqual(out["provider"], "jina")


class NewsOrderTest(unittest.TestCase):
    """5.4: news-en и news-ru = ddg → linkup (v2 re-baseline: ddg доминирует
    на свежести; exa на en-news худшим был R 0.132, tavily на ru-news Q 0.580
    — 7-й из 9; по итогу ревью 20.10)."""

    def test_news_en_order(self):
        chain = router._effective_chain("openai gpt-5 release notes", "news-en")
        self.assertEqual([p.name for p in chain[:2]], ["ddg", "linkup"])

    def test_news_ru_order(self):
        chain = router._effective_chain("релиз claude code новые функции",
                                        "news-ru")
        self.assertEqual([p.name for p in chain[:2]], ["ddg", "linkup"])

    def test_news_intent_keys_exist(self):
        self.assertIn("news-en", router.INTENT_ORDER)
        self.assertIn("news-ru", router.INTENT_ORDER)


if __name__ == "__main__":
    unittest.main()
