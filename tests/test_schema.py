"""Schema-валидация выдачи + youcom-схема (фаза 4.3, 2026-10-19).

Провайдеры молча меняют формат ответа (zai 24.09 url→link; youcom 19.10
snippets→description — записи месяцами ходили с пустыми сниппетами).
Валидатор reject_reason бракует записи до merge; router.search при полной
забракованной выдаче фолбэкает вниз. Run: python3 -m unittest discover tests -v
"""

from __future__ import annotations

import json
import unittest

from engine import router
from engine.providers.base import Provider, ProviderError, SearchResult, reject_reason
from engine.providers.youcom import YoucomProvider


def ok(**kw) -> SearchResult:
    base = {"url": "https://example.com/a", "title": "T",
            "snippet": "нормальный сниппет достаточной длины для валидности"}
    base.update(kw)
    return SearchResult(**base)


class RejectReasonTest(unittest.TestCase):
    def test_valid_passes(self):
        self.assertIsNone(reject_reason(ok()))

    def test_zai_style_short_but_real_snippet_passes(self):
        # zai content_size=medium отдаёт 61–192 симв. — это его формат,
        # не деградация; порог 50 должен их пропускать
        self.assertIsNone(reject_reason(ok(snippet="с" * 61)))

    def test_no_url(self):
        self.assertEqual(reject_reason(ok(url="")), "no_url")
        self.assertEqual(reject_reason(ok(url="not-a-url")), "no_url")

    def test_no_text(self):
        self.assertEqual(reject_reason(ok(title="", snippet="")), "no_text")

    def test_no_snippet_tavily_lesson(self):
        # title есть, контента нет — «успех» без содержания
        self.assertEqual(reject_reason(ok(snippet="")), "no_snippet")

    def test_stub_snippet(self):
        self.assertEqual(reject_reason(ok(snippet="...")), "short_snip")
        self.assertEqual(reject_reason(ok(snippet="N/A")), "short_snip")


class FakeProvider(Provider):
    def __init__(self, name: str, results=None, mode: str = "ok"):
        self.name = name
        self._results = results
        if mode == "unavailable":
            self.available_reason = "no key (test)"

    def search(self, query, *, n=8, freshness=None):
        if self._results is None:
            raise ProviderError("fake boom", retryable=False)
        return self._results


class SchemaFilterInRouterTest(unittest.TestCase):
    def setUp(self):
        self._chain = router.SEARCH_CHAIN
        self.addCleanup(setattr, router, "SEARCH_CHAIN", self._chain)

    def test_partial_reject_keeps_valid(self):
        junk = ok(url="https://x/1", snippet="")
        good = ok(url="https://x/2")
        router.SEARCH_CHAIN = [FakeProvider("prov", [junk, good])]
        out = router.search("q")
        self.assertEqual(out["rejected"], 1)
        self.assertEqual([r.url for r in out["results"]], ["https://x/2"])

    def test_fully_rejected_falls_back_down_chain(self):
        router.SEARCH_CHAIN = [FakeProvider("broken", [ok(snippet="")]),
                               FakeProvider("ok", [ok(url="https://x/2")])]
        out = router.search("q")
        self.assertEqual(out["provider"], "ok")
        names = [t["name"] for t in out["tried"]]
        self.assertEqual(names, ["broken"])
        self.assertIn("schema check", out["tried"][0]["error"])


class YoucomSchemaTest(unittest.TestCase):
    def _mcp_text(self, records) -> str:
        return json.dumps({"results": {"web": records}})

    def test_new_schema_description_and_page_age(self):
        # живой ответ 19.10: snippets нет, есть description + page_age
        text = self._mcp_text([{
            "url": "https://a", "title": "A",
            "description": "Описание результата поиска",
            "page_age": "2026-01-02T03:04:05",
        }])
        out = YoucomProvider._parse(text)
        self.assertEqual(out[0].snippet, "Описание результата поиска")
        self.assertEqual(out[0].date, "2026-01-02T03:04:05")

    def test_highlights_fallback_when_description_empty(self):
        text = self._mcp_text([{
            "url": "https://a", "title": "A", "description": "",
            "contents": {"highlights": ["Длинный контент из highlights"]},
        }])
        out = YoucomProvider._parse(text)
        self.assertEqual(out[0].snippet, "Длинный контент из highlights")

    def test_old_schema_snippets_still_works(self):
        text = self._mcp_text([{"url": "https://a", "title": "A",
                                "snippets": ["старое поле"]}],
                              )
        out = YoucomProvider._parse(text)
        self.assertEqual(out[0].snippet, "старое поле")

    def test_parsed_records_pass_schema_check(self):
        # распарсенная выдача не должна целиком браковаться валидатором
        text = self._mcp_text([
            {"url": "https://a", "title": "A",
             "description": "Описание результата поиска, достаточно длинное, "
                            "чтобы пройти порог валидатора"},
            {"url": "https://b", "title": "B",
             "contents": {"highlights": [
                 "Длинный контент без поля description, взятый "
                 "из contents.highlights ответа youcom"]}},
        ])
        for r in YoucomProvider._parse(text):
            self.assertIsNone(reject_reason(r))


if __name__ == "__main__":
    unittest.main()
