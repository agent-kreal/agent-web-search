"""Minimal MCP Streamable-HTTP client (JSON-RPC over POST, stdlib only).

Covers the subset we need: initialize -> notifications/initialized ->
tools/call. Handles both plain-JSON and SSE (`text/event-stream`) responses,
and servers that do / don't require an mcp-session-id header.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Optional

UA = "wsearch/1.0 (+local skill)"
DEFAULT_TIMEOUT = 45


class McpError(RuntimeError):
    """MCP-level error (JSON-RPC error object or -429 style tool error)."""

    def __init__(self, msg: str, *, status: int = 0, raw: str = ""):
        super().__init__(msg)
        self.status = status
        self.raw = raw


class McpClient:
    def __init__(self, url: str, *, headers: Optional[dict] = None, timeout: int = DEFAULT_TIMEOUT):
        self.url = url
        self.extra_headers = headers or {}
        self.timeout = timeout
        self.session_id: Optional[str] = None
        self._next_id = 1

    # -- low-level ---------------------------------------------------------- #

    def _post(self, payload: dict) -> str:
        body = json.dumps(payload).encode()
        req = urllib.request.Request(self.url, data=body, method="POST")
        req.add_header("Content-Type", "application/json")
        # MCP streamable http requires both accept types
        req.add_header("Accept", "application/json, text/event-stream")
        req.add_header("User-Agent", UA)
        for k, v in self.extra_headers.items():
            req.add_header(k, v)
        if self.session_id:
            req.add_header("Mcp-Session-Id", self.session_id)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                sid = resp.headers.get("Mcp-Session-Id")
                if sid:
                    self.session_id = sid
                return resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:500]
            raise McpError(f"HTTP {e.code} from MCP server: {detail}", status=e.code, raw=detail) from None
        except urllib.error.URLError as e:
            raise McpError(f"network error: {e.reason}", status=0) from None

    def _parse(self, raw: str, want_id: int) -> dict:
        """Extract the JSON-RPC response for want_id from JSON or SSE body.

        SSE bodies may interleave notification events with the result event;
        pick the data: line whose parsed object carries our id.
        """
        if raw.lstrip().startswith("{"):
            return json.loads(raw)
        candidates = []
        for line in raw.splitlines():
            line = line.strip()
            if line.startswith("data:"):
                candidates.append(line[5:].strip())
        for c in reversed(candidates):
            try:
                obj = json.loads(c)
            except json.JSONDecodeError:
                continue
            if obj.get("id") == want_id:
                return obj
        if candidates:
            try:
                return json.loads(candidates[-1])
            except json.JSONDecodeError:
                pass
        raise McpError(f"unparseable MCP response: {raw[:300]}", raw=raw)

    # -- protocol ----------------------------------------------------------- #

    def initialize(self, client_name: str = "wsearch") -> None:
        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": client_name, "version": "1.0"},
            },
        }
        self._next_id += 1
        resp = self._parse(self._post(payload), payload["id"])
        if "error" in resp:
            raise McpError(f"initialize error: {resp['error']}")
        # notifications/initialized — some servers 404/ignore it, never fatal
        try:
            self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})
        except McpError:
            pass

    def call_tool(self, name: str, arguments: dict, *, init_if_needed: bool = True) -> Any:
        if init_if_needed and self.session_id is None:
            self.initialize()
        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        }
        self._next_id += 1
        resp = self._parse(self._post(payload), payload["id"])
        if "error" in resp:
            raise McpError(f"tool error: {resp['error']}", raw=json.dumps(resp["error"]))
        result = resp.get("result", {})
        if result.get("isError"):
            texts = [c.get("text", "") for c in result.get("content", []) if c.get("type") == "text"]
            raise McpError("; ".join(texts) or "unknown tool error", raw=";".join(texts))
        return result
