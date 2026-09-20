"""Brave X-RateLimit-* header parsing (passive server-truth capture).

Run: python3 -m unittest discover tests -v
Live-verified format 09.09: paired buckets with x-ratelimit-policy
'50;w=1, 0;w=2592000' where the 30-day bucket shows 0/0 = NOT TRACKED
(searches succeed) — must not be recorded as 'exhausted'.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from engine import quotas
from engine.providers.brave import BraveProvider


class FakeResp:
    def __init__(self, headers: dict):
        self.headers = headers


class BraveRateLimitTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        orig = quotas.STATE_FILE
        quotas.STATE_FILE = Path(self.tmp.name) / "quotas.json"
        self.addCleanup(setattr, quotas, "STATE_FILE", orig)

    def test_untracked_monthly_bucket_not_recorded(self):
        """Live format: '50, 0'/'49, 0' + policy — 30d bucket 0-limit means
        not tracked; recording it would fake-block the provider."""
        BraveProvider._record_ratelimit(FakeResp({
            "X-RateLimit-Limit": "50, 0",
            "X-RateLimit-Policy": "50;w=1, 0;w=2592000",
            "X-RateLimit-Remaining": "49, 0",
            "X-RateLimit-Reset": "1, 1858094",
        }))
        self.assertNotIn("server", quotas.get_entry("brave"))

    def test_tracked_monthly_bucket_recorded(self):
        """Same layout but with a real 2000/mo bucket -> snapshot written."""
        BraveProvider._record_ratelimit(FakeResp({
            "X-RateLimit-Limit": "50, 2000",
            "X-RateLimit-Policy": "50;w=1, 2000;w=2592000",
            "X-RateLimit-Remaining": "49, 1915",
        }))
        sv = quotas.server_view("brave")
        self.assertIsNotNone(sv)
        self.assertEqual(sv["remaining"], 1915)
        self.assertEqual(sv["limit"], 2000)

    def test_legacy_layout_without_policy(self):
        """Older docs format '1, 15000' — monthly figure last."""
        BraveProvider._record_ratelimit(FakeResp({
            "X-RateLimit-Limit": "1, 15000",
            "X-RateLimit-Remaining": "1, 14800",
        }))
        sv = quotas.server_view("brave")
        self.assertIsNotNone(sv)
        self.assertEqual(sv["remaining"], 14800)
        self.assertEqual(sv["limit"], 15000)

    def test_rps_only_headers_ignored(self):
        """A single per-second bucket is not a quota — no snapshot."""
        BraveProvider._record_ratelimit(FakeResp({
            "X-RateLimit-Limit": "50",
            "X-RateLimit-Policy": "50;w=1",
            "X-RateLimit-Remaining": "49",
        }))
        self.assertNotIn("server", quotas.get_entry("brave"))


if __name__ == "__main__":
    unittest.main()
