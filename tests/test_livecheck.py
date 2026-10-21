"""Livecheck zai: monitor API -> MCP pool of web_search_prime.

First live check 19.10 showed the local 1000/mo counter is pessimistic
(767 spent locally vs 225 on the server), so the server snapshot both
fixes the estimate and clears stale exhausted markers via set_server.
Run: python3 -m unittest discover tests -v
"""

from __future__ import annotations

import unittest
from datetime import datetime
from unittest import mock

from engine import livecheck

# Shape of GET api.z.ai/api/monitor/usage/quota/limit (captured live 19.10)
MONITOR_PAYLOAD = {
    "data": {
        "level": 2,
        "limits": [
            {
                "type": "TIME_LIMIT",
                "usage": 1000,          # pool size
                "currentValue": 225,    # spent
                "remaining": 775,
                "percentage": 22,
                "nextResetTime": 1794990499998,
                "usageDetails": [
                    {"modelCode": "search-prime", "usage": 225},
                    {"modelCode": "web-reader", "usage": 0},
                ],
            },
            {"type": "TOKENS_LIMIT", "usage": None, "remaining": None,
             "percentage": 18, "nextResetTime": 1792440230674},
        ],
    }
}


class ZaiCheck(unittest.TestCase):
    def test_parses_mcp_pool(self):
        with mock.patch.object(livecheck.config, "zai_auth_header",
                               return_value="Bearer test-key"), \
             mock.patch.object(livecheck, "_get_json",
                               return_value=MONITOR_PAYLOAD) as gj:
            out = livecheck.check_zai()
        self.assertEqual(out["remaining"], 775)
        self.assertEqual(out["limit"], 1000)
        self.assertEqual(out["unit"], "requests")
        self.assertEqual(out["period_end"],
                         datetime.fromtimestamp(1794990499.998).isoformat())
        # monitor endpoint wants the raw key, Bearer stripped
        headers = gj.call_args[0][1]
        self.assertEqual(headers["Authorization"], "test-key")

    def test_raw_key_passthrough(self):
        with mock.patch.object(livecheck.config, "zai_auth_header",
                               return_value="test-key"), \
             mock.patch.object(livecheck, "_get_json",
                               return_value=MONITOR_PAYLOAD):
            out = livecheck.check_zai()
        self.assertEqual(out["remaining"], 775)

    def test_no_time_limit_is_schema_error(self):
        payload = {"data": {"limits": [{"type": "TOKENS_LIMIT",
                                        "remaining": None}]}}
        with mock.patch.object(livecheck.config, "zai_auth_header",
                               return_value="Bearer k"), \
             mock.patch.object(livecheck, "_get_json", return_value=payload):
            with self.assertRaises(RuntimeError) as ctx:
                livecheck.check_zai()
        self.assertIn("unexpected schema", str(ctx.exception))

    def test_no_key(self):
        with mock.patch.object(livecheck.config, "zai_auth_header",
                               return_value=None):
            with self.assertRaises(RuntimeError) as ctx:
                livecheck.check_zai()
        self.assertIn("no key", str(ctx.exception))

    def test_registered_in_checks(self):
        self.assertIn("zai", livecheck.CHECKS)


YOU_BALANCE = {"data": {"type": "account", "id": "h",
                        "attributes": {"balance": 10000.0}}}  # cents == $100


class YoucomCheck(unittest.TestCase):
    def test_balance_usd(self):
        with mock.patch.object(livecheck.config, "get", return_value="k"), \
             mock.patch.object(livecheck, "_get_json",
                               return_value=YOU_BALANCE):
            out = livecheck.check_youcom()
        self.assertEqual(out, {"unit": "usd", "remaining": 100.0})

    def test_cloudflare_1010_falls_back_to_curl(self):
        with mock.patch.object(livecheck.config, "get", return_value="k"), \
             mock.patch.object(livecheck, "_get_json",
                               side_effect=RuntimeError("HTTP 403: error code: 1010")), \
             mock.patch.object(livecheck, "_curl_get_json",
                               return_value=YOU_BALANCE) as curl:
            out = livecheck.check_youcom()
        self.assertEqual(out["remaining"], 100.0)
        curl.assert_called_once()

    def test_other_errors_do_not_fall_back(self):
        with mock.patch.object(livecheck.config, "get", return_value="k"), \
             mock.patch.object(livecheck, "_get_json",
                               side_effect=RuntimeError("HTTP 500: boom")), \
             mock.patch.object(livecheck, "_curl_get_json") as curl:
            with self.assertRaises(RuntimeError):
                livecheck.check_youcom()
        curl.assert_not_called()

    def test_no_key(self):
        with mock.patch.object(livecheck.config, "get", return_value=None):
            with self.assertRaises(RuntimeError) as ctx:
                livecheck.check_youcom()
        self.assertIn("no key", str(ctx.exception))

    def test_registered_in_checks(self):
        self.assertIn("youcom", livecheck.CHECKS)


if __name__ == "__main__":
    unittest.main()
