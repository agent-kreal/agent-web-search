"""Youcom keyed REST (20.10): POST ydc-index.io/v1/search, X-API-Key.

Free MCP profile got paywalled (402/x402) — keyed mode moved to REST at
$5/1k calls. Balance (account_balance) lives in livecheck tests instead.
Run: python3 -m unittest discover tests -v
"""

from __future__ import annotations

import email.message
import io
import json
import unittest
import urllib.error
from unittest import mock

from engine.providers.base import ProviderError
from engine.providers.youcom import REST_URL, YoucomProvider

REST_OK = json.dumps({"results": {"web": [
    {"url": "https://a.example", "title": "A",
     "description": "описание результата достаточной длины для schema-валидации"},
    {"url": "https://b.example", "title": "B",
     "snippets": ["сниппет из snippets-поля тоже достаточно длинный"]},
]}})


def _http_error(code: int, body: str = "") -> urllib.error.HTTPError:
    return urllib.error.HTTPError(REST_URL, code, "err", email.message.Message(),
                                  io.BytesIO(body.encode()))


class FakeResp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()


def make_provider() -> YoucomProvider:
    with mock.patch.object(__import__("engine.config", fromlist=["get"]),
                           "get", return_value="ydc-test-key"):
        p = YoucomProvider()
    return p


class YoucomRest(unittest.TestCase):
    def setUp(self):
        self.p = make_provider()
        self.assertTrue(self.p.api_key)
        self.assertEqual(self.p.quota.unit, "usd")
        self.assertAlmostEqual(self.p.quota.price, 0.005)

    def _search(self, urlopen_result):
        with mock.patch("engine.providers.youcom.urllib.request.urlopen",
                        return_value=urlopen_result) as u, \
             mock.patch("engine.providers.youcom.quotas") as q:
            out = self.p.search("test query", n=5)
        return out, u, q

    def test_success_and_body(self):
        out, u, q = self._search(FakeResp(REST_OK.encode()))
        self.assertEqual(len(out), 2)
        self.assertEqual(out[0].url, "https://a.example")
        self.assertIn("описание", out[0].snippet)
        body = json.loads(u.call_args[0][0].data.decode())
        self.assertEqual(body["query"], "test query")
        self.assertEqual(body["count"], 5)
        self.assertNotIn("freshness", body)
        self.assertEqual(u.call_args[0][0].headers.get("X-api-key"),
                         "ydc-test-key")
        q.spend.assert_called_once_with("youcom", 1, "none")

    def test_freshness_mapped(self):
        with mock.patch("engine.providers.youcom.urllib.request.urlopen",
                        return_value=FakeResp(REST_OK.encode())) as u, \
             mock.patch("engine.providers.youcom.quotas"):
            self.p.search("q", freshness="week")
        body = json.loads(u.call_args[0][0].data.decode())
        self.assertEqual(body["freshness"], "week")

    def test_402_credits_exhausted(self):
        with mock.patch("engine.providers.youcom.urllib.request.urlopen",
                        side_effect=_http_error(402)), \
             mock.patch("engine.providers.youcom.quotas") as q:
            with self.assertRaises(ProviderError) as ctx:
                self.p.search("q")
        self.assertTrue(ctx.exception.quota_exhausted)
        q.mark_exhausted.assert_called_once()

    def test_429_retryable_not_quota(self):
        with mock.patch("engine.providers.youcom.urllib.request.urlopen",
                        side_effect=_http_error(429, "slow down")), \
             mock.patch("engine.providers.youcom.quotas") as q:
            with self.assertRaises(ProviderError) as ctx:
                self.p.search("q")
        self.assertTrue(ctx.exception.retryable)
        q.mark_exhausted.assert_not_called()

    def test_empty_web_no_results(self):
        empty = json.dumps({"results": {"web": []}})
        with mock.patch("engine.providers.youcom.urllib.request.urlopen",
                        return_value=FakeResp(empty.encode())), \
             mock.patch("engine.providers.youcom.quotas") as q:
            with self.assertRaises(ProviderError) as ctx:
                self.p.search("q")
        self.assertFalse(ctx.exception.retryable)
        q.spend.assert_not_called()

    def test_urlerror_retryable(self):
        with mock.patch("engine.providers.youcom.urllib.request.urlopen",
                        side_effect=urllib.error.URLError("conn reset")), \
             mock.patch("engine.providers.youcom.quotas"):
            with self.assertRaises(ProviderError) as ctx:
                self.p.search("q")
        self.assertTrue(ctx.exception.retryable)


if __name__ == "__main__":
    unittest.main()
