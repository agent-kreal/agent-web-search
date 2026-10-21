"""Livecheck: ask provider APIs what quota actually remains (server truth).

Free GET endpoints (verified live 09.09):
  firecrawl  GET api.firecrawl.dev/v2/team/credit-usage
             -> data.remainingCredits (+ planCredits, billing period: 23rd)
  linkup     GET api.linkup.so/v1/credits/balance -> {"balance": 19.415} (usd)
  zai        GET api.z.ai/api/monitor/usage/quota/limit (dashboard API of the
             GLM Coding Plan; raw key, no Bearer — verified 19.10) ->
             TIME_LIMIT = the web_search_prime MCP pool: usage(limit)/
             currentValue(used)/remaining/nextResetTime. Server truth for the
             quota zai.py counts locally as 1000/mo (first live check showed
             local 767 spent vs server 225 — the counter is pessimistic).
  youcom     GET api.you.com/v1/billing/account_balance (X-API-Key) ->
             data.attributes.balance in CENTS (10000.0 = $100). api.you.com
             sits behind Cloudflare and bans urllib's TLS fingerprint with
             "error code: 1010" (verified 20.10) — falls back to system curl,
             which passes. Keyed REST costs $5/1k calls (youcom.py).
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
from datetime import datetime
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


def check_zai() -> dict:
    """Monitor API of the GLM plan -> web_search_prime MCP pool (server truth).

    Same undocumented endpoint the z.ai dashboard uses (via claude-glm-stack's
    zai-quota.py, verified live 19.10): the key is the raw token, no Bearer.
    TIME_LIMIT carries the MCP pool zai.py debits locally as 1000/mo calls.
    """
    hdr = config.zai_auth_header()
    if not hdr:
        raise RuntimeError("no key")
    key = hdr[7:] if hdr.lower().startswith("bearer ") else hdr
    data = _get_json("https://api.z.ai/api/monitor/usage/quota/limit",
                     {"Authorization": key, "Content-Type": "application/json"})
    limits = (data.get("data") or {}).get("limits") or []
    tl = next((l for l in limits if l.get("type") == "TIME_LIMIT"), None)
    if tl is None or tl.get("remaining") is None:
        raise RuntimeError(f"unexpected schema: {json.dumps(data)[:200]}")
    out = {"unit": "requests", "remaining": tl["remaining"]}
    if tl.get("usage") is not None:
        out["limit"] = tl["usage"]
    ms = tl.get("nextResetTime")
    if ms:
        out["period_end"] = datetime.fromtimestamp(ms / 1000).isoformat()
    return out


def _curl_get_json(url: str, headers: dict) -> dict:
    """System-curl fallback: api.you.com's Cloudflare bans urllib's TLS
    fingerprint with "error code: 1010" (verified 20.10) while curl passes."""
    import subprocess
    cmd = ["curl", "-s", "--max-time", "15", url]
    for k, v in headers.items():
        cmd += ["-H", f"{k}: {v}"]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True,
                             timeout=20).stdout
        return json.loads(out)
    except (subprocess.SubprocessError, json.JSONDecodeError) as e:
        raise RuntimeError(f"curl fallback failed: {e}") from None


def check_youcom() -> dict:
    """Keyed REST balance: remaining credits in USD (verified live 20.10).
    Balance is in cents: 10000.0 == $100.00. Only meaningful with a key —
    the free MCP profile has no balance."""
    key = config.get("YDC_API_KEY") or config.get("YOUCOM_API_KEY")
    if not key:
        raise RuntimeError("no key")
    headers = {"X-API-Key": key}
    url = "https://api.you.com/v1/billing/account_balance"
    try:
        data = _get_json(url, headers)
    except RuntimeError as e:
        if "1010" not in str(e):
            raise
        data = _curl_get_json(url, headers)  # Cloudflare vs urllib
    cents = ((data.get("data") or {}).get("attributes") or {}).get("balance")
    if cents is None:
        raise RuntimeError(f"unexpected schema: {json.dumps(data)[:200]}")
    return {"unit": "usd", "remaining": round(cents / 100, 2)}


CHECKS = {"firecrawl": check_firecrawl, "linkup": check_linkup,
          "zai": check_zai, "youcom": check_youcom}


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
