"""Livecheck: ask provider APIs what quota actually remains (server truth).

Free GET endpoints (verified live 09.09):
  firecrawl  GET api.firecrawl.dev/v2/team/credit-usage
             -> data.remainingCredits (+ planCredits, billing period: 23rd)
  linkup     GET api.linkup.so/v1/credits/balance -> {"balance": 19.415} (usd)
  brave      no endpoint — X-RateLimit-* response headers are read
             passively in providers/brave.py after every search
  exa        team API needs a *service* key (team plans); personal
             free-tier keys get 404 (verified 09.09) — local counter only

Each check stores a server snapshot (quotas.set_server) and logs the
counter drift to usage.jsonl ({"cmd": "livecheck", ...}) so episodes like
exa-03.09 (a 429 hid a live balance for a month) are visible, not silent.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import List, Optional

from . import config, quotas, usage


def _get_json(url: str, headers: dict) -> dict:
    req = urllib.request.Request(url)
    for k, v in headers.items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:200]
        raise RuntimeError(f"HTTP {e.code}: {detail}") from None
    except urllib.error.URLError as e:
        raise RuntimeError(f"network: {e.reason}") from None


def check_firecrawl() -> dict:
    key = config.get("FIRECRAWL_API_KEY")
    if not key:
        raise RuntimeError("no key")
    data = _get_json("https://api.firecrawl.dev/v2/team/credit-usage",
                     {"Authorization": f"Bearer {key}"})
    d = data.get("data") or {}
    out = {"unit": "credits", "remaining": d.get("remainingCredits")}
    if out["remaining"] is None:
        raise RuntimeError(f"unexpected schema: {json.dumps(data)[:200]}")
    if d.get("planCredits") is not None:
        out["limit"] = d["planCredits"]
    if d.get("billingPeriodEnd"):
        out["period_end"] = d["billingPeriodEnd"]
    return out


def check_linkup() -> dict:
    key = config.get("LINKUP_API_KEY")
    if not key:
        raise RuntimeError("no key")
    data = _get_json("https://api.linkup.so/v1/credits/balance",
                     {"Authorization": f"Bearer {key}"})
    if data.get("balance") is None:
        raise RuntimeError(f"unexpected schema: {json.dumps(data)[:200]}")
    return {"unit": "usd", "remaining": data["balance"]}


CHECKS = {"firecrawl": check_firecrawl, "linkup": check_linkup}


def _provider_meta() -> dict:
    """{name: QuotaSpec} for drift estimation (local units -> server units)."""
    from .providers import FETCH_CHAIN, SEARCH_CHAIN
    meta = {}
    for p in SEARCH_CHAIN + FETCH_CHAIN:
        meta.setdefault(p.name, p.quota)
    return meta


def _local_estimate(name: str, quota) -> Optional[float]:
    """Local counter's idea of the remainder, in the SERVER's unit."""
    if quota is None or quota.limit is None:
        return None
    e = quotas.get_entry(name)
    loc = e.get("local")
    if not isinstance(loc, dict):
        loc = e
    used = int(loc.get("used", 0) or 0)
    return max(0.0, (quota.limit - used)) * quota.price


def run(providers: Optional[List[str]] = None) -> List[dict]:
    """Fetch server truth for keyed providers, store snapshots, log drift."""
    meta = _provider_meta()
    results = []
    for name, fn in CHECKS.items():
        if providers and name not in providers:
            continue
        try:
            snap = fn()
        except RuntimeError as e:
            results.append({"provider": name, "ok": False, "error": str(e)})
            usage.log({"cmd": "livecheck", "provider": name, "ok": False,
                       "error": str(e)[:200]})
            continue
        quotas.set_server(name, unit=snap["unit"], remaining=snap["remaining"],
                          limit=snap.get("limit"),
                          period_end=snap.get("period_end"))
        local_est = _local_estimate(name, meta.get(name))
        drift = (snap["remaining"] - local_est) if local_est is not None else None
        usage.log({"cmd": "livecheck", "provider": name, "ok": True,
                   "unit": snap["unit"], "server_remaining": snap["remaining"],
                   "local_estimated": local_est, "drift": drift})
        results.append({"provider": name, "ok": True, "unit": snap["unit"],
                        "server_remaining": snap["remaining"],
                        "local_estimated": local_est, "drift": drift,
                        "period_end": snap.get("period_end")})
    return results
