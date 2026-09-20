"""ChainError telemetry: failed chains must log every attempt's reason.

Audit 09.09: failed invocations logged tried=[] (the RuntimeError carried
no context) and forced --provider calls were indistinguishable from
chain failures. Run: python3 -m unittest discover tests -v
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from engine import router, usage
from engine.providers.base import Provider, ProviderError, SearchResult


class FakeProvider(Provider):
    def __init__(self, name: str, mode: str):
        self.name = name
        if mode == "unavailable":
            self.available_reason = "no key (test)"

    def search(self, query, *, n=8, freshness=None):
        if self.name == "failer":
            raise ProviderError("fake boom", retryable=False)
        return [SearchResult(url="https://x", title="t", provider=self.name)]


class ChainErrorTest(unittest.TestCase):
    def setUp(self):
        # isolate the router chain and the usage log from the real ones
        self._chain = router.SEARCH_CHAIN
        router.SEARCH_CHAIN = [FakeProvider("unavail", "unavailable"),
                               FakeProvider("failer", "fail")]
        self.addCleanup(setattr, router, "SEARCH_CHAIN", self._chain)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self._state, self._log = usage.STATE, usage.LOG
        usage.STATE = Path(self.tmp.name)
        usage.LOG = usage.STATE / "usage.jsonl"
        self.addCleanup(setattr, usage, "STATE", self._state)
        self.addCleanup(setattr, usage, "LOG", self._log)

    def _read_log(self) -> list:
        if not usage.LOG.exists():
            return []
        import json
        return [json.loads(l) for l in usage.LOG.read_text().splitlines()]

    def test_chain_failure_carries_tried(self):
        """Unavailable (skip) + failing (error) attempts both ride along."""
        with self.assertRaises(router.ChainError) as ctx:
            router.search("q")
        tried = ctx.exception.tried
        self.assertEqual([t["name"] for t in tried], ["unavail", "failer"])
        self.assertIn("skipped: no key (test)", tried[0]["error"])
        self.assertEqual(tried[1]["error"], "fake boom")

    def test_chain_error_is_runtime_error(self):
        """cli.main catches RuntimeError — the contract must hold."""
        self.assertTrue(issubclass(router.ChainError, RuntimeError))

    def test_success_path_empty_tried(self):
        router.SEARCH_CHAIN = [FakeProvider("ok", "ok")]
        out = router.search("q")
        self.assertEqual(out["provider"], "ok")
        self.assertEqual(out["tried"], [])

    def test_cli_logs_tried_and_forced_on_failure(self):
        from engine import cli
        try:
            cli.cmd_search(type("A", (), {
                "query": "q", "n": 3, "freshness": None,
                "provider": ["failer"], "intent": None, "json": False})())
        except router.ChainError:
            pass
        rows = self._read_log()
        self.assertEqual(len(rows), 1)
        rec = rows[0]
        self.assertFalse(rec["ok"])
        self.assertEqual(rec["forced"], ["failer"])       # pin is visible
        self.assertEqual(rec["tried"][0]["name"], "failer")
        self.assertEqual(rec["tried"][0]["error"], "fake boom")
        self.assertNotIn("skipped", str(rec["tried"]))    # only the pinned one ran

    def test_no_forced_field_when_not_pinned(self):
        from engine import cli
        try:
            cli.cmd_search(type("A", (), {
                "query": "q", "n": 3, "freshness": None,
                "provider": None, "intent": None, "json": False})())
        except router.ChainError:
            pass
        rec = self._read_log()[0]
        self.assertNotIn("forced", rec)                   # field only when pinned


if __name__ == "__main__":
    unittest.main()
