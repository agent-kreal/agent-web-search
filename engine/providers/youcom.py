"""You.com — keyed REST ($5/1k calls) или free MCP (paywalled 20.10).

20.10: анонимный you-search на api.you.com/mcp прикрыт пейволлом (402/x402;
free-профиль отдаёт keyless только you-discover). Keyed-режим переведён с MCP
на REST POST ydc-index.io/v1/search (X-API-Key; POST — актуальный путь, GET —
legacy без новых фич): $5/1k вызовов, кредиты аккаунта без периода. Баланс —
серверно через livecheck (/v1/billing/account_balance; api.you.com за
Cloudflare банит TLS-фингерпринт urllib кодом 1010 — там curl-fallback)."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from .. import config, quotas
from ..mcpclient import McpClient, McpError
from .base import Provider, ProviderError, QuotaSpec, SearchResult

MCP_URL = "https://api.you.com/mcp?profile=free"
REST_URL = "https://ydc-index.io/v1/search"


class YoucomProvider(Provider):
    name = "youcom"
    quota = QuotaSpec(limit=100, period="day", label="free MCP 100/day (paywalled 20.10)")

    def __init__(self):
        self._client: Optional[McpClient] = None
        self.api_key = config.get("YDC_API_KEY") or config.get("YOUCOM_API_KEY")
        if self.api_key:
            # keyed REST: $5/1k calls, кредиты без периода — счёт в $,
            # остаток знает только сервер (livecheck: account_balance)
            self.quota = QuotaSpec(limit=None, period="none", unit="usd",
                                   price=0.005,
                                   label="keyed REST: $5/1k, balance via livecheck")

    def _search_rest(self, query: str, *, n: int,
                     freshness: Optional[str]) -> List[SearchResult]:
        assert self.api_key  # searched via the keyed branch only
        body = {"query": query, "count": n}
        if freshness in ("day", "week", "month", "year"):
            body["freshness"] = freshness
        req = urllib.request.Request(
            REST_URL, data=json.dumps(body).encode(),
            headers={"X-API-Key": self.api_key,
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                text = r.read().decode()
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:200]
            if e.code == 402:
                quotas.mark_exhausted(self.name, None, "none")  # 1h cooldown
                raise ProviderError("youcom credits exhausted (402)",
                                    quota_exhausted=True) from None
            if e.code == 429:
                # QPS-лимит платного API, не квота: наверх для ретрая/фолбэка
                raise ProviderError(f"youcom: 429: {detail}", retryable=True) from None
            raise ProviderError(f"youcom: HTTP {e.code}: {detail}",
                                retryable=e.code >= 500) from None
        except urllib.error.URLError as e:
            raise ProviderError(f"youcom: {e.reason}", retryable=True) from None
        try:
            out = self._parse(text)[:n]
        except (json.JSONDecodeError, AttributeError):
            raise ProviderError("youcom: unparseable response", retryable=True) from None
        if not out:
            raise ProviderError("youcom returned no results", retryable=False)
        quotas.spend(self.name, 1, "none")
        return out

    def _mcp(self) -> McpClient:
        if self._client is None:
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else None
            self._client = McpClient(MCP_URL, headers=headers, timeout=40)
        return self._client

    def search(self, query: str, *, n: int = 8, freshness: Optional[str] = None) -> List[SearchResult]:
        if self.api_key:
            return self._search_rest(query, n=n, freshness=freshness)
        args = {"query": query}
        if freshness in ("day", "week"):
            args["created"] = "lastWeek" if freshness == "week" else "lastDay"
        try:
            result = self._mcp().call_tool("you-search", args)
        except McpError as e:
            msg = str(e)
            if e.status == 402 or "free tier limit exceeded" in msg.lower():
                # paywall (не квота): 20.10 free-профиль MCP закрыт «upgrade».
                # Маркер не «до завтра» — перевзводился бы ежедневно на каждой попытке.
                until = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(timespec="seconds")
                quotas.mark_exhausted(self.name, until)
                raise ProviderError("youcom free tier paywalled (402), free-профиль мёртв",
                                    quota_exhausted=True) from None
            if e.status == 429 or "rate" in msg.lower() or "limit" in msg.lower():
                quotas.mark_exhausted(self.name, None, "day")
                raise ProviderError("youcom daily limit hit", quota_exhausted=True) from None
            raise ProviderError(f"youcom: {msg}", retryable=e.status >= 500 or e.status == 0) from None
        text = next((c.get("text", "") for c in result.get("content", [])
                     if c.get("type") == "text"), "")
        try:
            out = self._parse(text)[:n]
        except (json.JSONDecodeError, AttributeError):
            raise ProviderError("youcom: unparseable response", retryable=True) from None
        if not out:
            raise ProviderError("youcom returned no results", retryable=False)
        quotas.spend(self.name, 1, "day")
        return out

    @staticmethod
    def _parse(text: str) -> List[SearchResult]:
        """MCP you-search text -> результаты. Схема сменилась (замечено
        19.10, фаза 4.3): snippets → description, появились page_age и
        contents.highlights. Старое поле держим как fallback — free-профиль
        не версионируется, порядок полей может гулять."""
        data = json.loads(text)
        web = (data.get("results") or {}).get("web", [])
        out = []
        for r in web:
            snippet = (r.get("description") or "").strip()
            if not snippet:
                snippet = ((r.get("snippets") or [""])[0] or "").strip()
            if not snippet:
                # длинный контент-кусок: режем до сниппетного размера
                hl = ((r.get("contents") or {}).get("highlights") or [""])[0]
                snippet = (hl or "").strip()
            out.append(SearchResult(
                url=r.get("url", ""), title=r.get("title", ""),
                snippet=snippet[:500], date=r.get("page_age"),
                provider="youcom",
            ))
        return out
