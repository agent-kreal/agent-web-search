"""Unit tests for the v2 quota ledger (server-truth first).

Run: python3 -m unittest discover tests -v
(STATE_FILE is swapped to a tmpdir — the real state/ is never touched.)
"""

from __future__ import annotations

import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from engine import quotas


class QuotaLedgerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        path = Path(self.tmp.name) / "quotas.json"
        self._orig = quotas.STATE_FILE
        quotas.STATE_FILE = path
        self.addCleanup(setattr, quotas, "STATE_FILE", self._orig)

    def _write(self, state: dict):
        quotas.STATE_FILE.write_text(
            __import__("json").dumps(state, indent=2))

    # --- v1 -> v2 migration ------------------------------------------------

    def test_legacy_entry_local_fallback(self):
        """v1 flat entry reads as local; remaining works unchanged."""
        self._write({"brave": {"window_start": quotas._window_start(
            "month", quotas._now()), "used": 84}})
        rem = quotas.remaining("brave", 2000, "month")
        self.assertEqual(rem, 1916)

    def test_spend_rewrites_legacy_to_v2(self):
        self._write({"brave": {"window_start": quotas._window_start(
            "month", quotas._now()), "used": 84}})
        quotas.spend("brave", 1, "month")
        e = quotas.get_entry("brave")
        self.assertEqual(e["local"]["used"], 85)
        self.assertNotIn("used", e)      # flat duplicate gone
        self.assertEqual(quotas._local(e), e["local"])

    # --- server truth -------------------------------------------------------

    def test_server_snapshot_wins_over_local(self):
        """Server says 1711 credits while local counter guesses 1969:
        remaining() must return the server figure (interpolated)."""
        quotas.set_server("firecrawl", unit="credits", remaining=1711,
                          limit=1000)
        rem = quotas.remaining("firecrawl", 2000, "month")
        self.assertEqual(rem, 1711)

    def test_interpolation_subtracts_spend_since_snapshot(self):
        quotas.set_server("firecrawl", unit="credits", remaining=1711)
        quotas.spend("firecrawl", 3, "month")
        rem = quotas.remaining("firecrawl", 2000, "month")
        self.assertEqual(rem, 1711 - 3)  # credits: 1 local unit = 1 credit

    def test_interpolation_usd_price(self):
        """linkup: $0.005 per local unit — 4 searches cost $0.02."""
        quotas.set_server("linkup", unit="usd", remaining=19.415)
        quotas.spend("linkup", 4, "month")
        rem = quotas.remaining("linkup", 4000, "month", price=0.005)
        assert rem is not None
        self.assertAlmostEqual(rem, 19.415 - 4 * 0.005)

    def test_stale_snapshot_ignored(self):
        """Older than SERVER_MAX_AGE -> local counter fallback."""
        old = (datetime.now(timezone.utc)
               - quotas.SERVER_MAX_AGE - timedelta(hours=1)).isoformat()
        self._write({"firecrawl": {
            "server": {"unit": "credits", "remaining": 1711,
                       "baseline_used": 0, "fetched_at": old},
            "local": {"window_start": quotas._window_start(
                "month", quotas._now()), "used": 31}}})
        self.assertIsNone(quotas.server_view("firecrawl"))
        self.assertEqual(quotas.remaining("firecrawl", 2000, "month"), 1969)

    def test_server_at_zero_blocks(self):
        quotas.set_server("linkup", unit="usd", remaining=0.0)
        rem = quotas.remaining("linkup", 4000, "month", price=0.005)
        assert rem is not None
        self.assertLessEqual(rem, 0)  # router's skip test

    def test_live_server_clears_exhausted(self):
        """exa-03.09 antidote: fresh remaining > 0 lifts the 429 marker."""
        quotas.mark_exhausted("exa", None, "month")
        self.assertIsNotNone(quotas.is_exhausted("exa"))
        quotas.set_server("exa", unit="usd", remaining=8.5)
        self.assertIsNone(quotas.is_exhausted("exa"))

    def test_window_roll_drops_snapshot_and_restores_limit(self):
        """Reset-quota (credits): snapshot anchored in the old window dies,
        local counter reports a full fresh window."""
        quotas.set_server("firecrawl", unit="credits", remaining=1711)
        past = (datetime.now(timezone.utc) - timedelta(days=40)).strftime("%Y-%m")
        state = quotas._load()
        state["firecrawl"]["local"]["window_start"] = past
        quotas._save(state)
        self.assertIsNone(quotas.server_view("firecrawl"))
        self.assertEqual(quotas.remaining("firecrawl", 2000, "month"), 2000)

    def test_usd_snapshot_survives_window_roll(self):
        """$ balance (linkup) is continuous: the snapshot stays valid across
        window rolls, interpolation re-anchors to the fresh counter."""
        quotas.set_server("linkup", unit="usd", remaining=19.415)
        past = (datetime.now(timezone.utc) - timedelta(days=40)).strftime("%Y-%m")
        state = quotas._load()
        state["linkup"]["local"]["window_start"] = past
        quotas._save(state)
        sv = quotas.server_view("linkup", price=0.005)
        self.assertIsNotNone(sv)  # usd survives the roll
        quotas.spend("linkup", 2, "month")  # roll + 2 searches
        rem = quotas.remaining("linkup", 4000, "month", price=0.005)
        assert rem is not None
        self.assertAlmostEqual(rem, 19.415 - 2 * 0.005)

    def test_spend_after_roll_drops_snapshot(self):
        quotas.set_server("firecrawl", unit="credits", remaining=1711)
        past = (datetime.now(timezone.utc) - timedelta(days=40)).strftime("%Y-%m")
        state = quotas._load()
        state["firecrawl"]["local"]["window_start"] = past
        quotas._save(state)
        quotas.spend("firecrawl", 1, "month")  # detects roll, resets window
        self.assertNotIn("server", quotas.get_entry("firecrawl"))

    # --- status line --------------------------------------------------------

    def test_status_line_units(self):
        quotas.set_server("linkup", unit="usd", remaining=19.415)
        line = quotas.status_line("linkup", 4000, "month", "x",
                                  unit="usd", price=0.005)
        self.assertIn("$19.41 left (server", line)  # 19.415 -> .2f banker's
        quotas.set_server("firecrawl", unit="credits", remaining=1711)
        line = quotas.status_line("firecrawl", 2000, "month", "x",
                                  unit="credits")
        self.assertIn("1711 credits left (server", line)

    def test_status_line_local_requests(self):
        self._write({"youcom": {"window_start": quotas._window_start(
            "day", quotas._now()), "used": 20}})
        line = quotas.status_line("youcom", 100, "day", "x")
        self.assertEqual(line, "80 left per day")


if __name__ == "__main__":
    unittest.main()
