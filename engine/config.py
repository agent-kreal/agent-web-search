"""Config: .env loading + key discovery from existing installs.

Priority: real env var > .env next to the project root > well-known files
(~/.claude/.brave_api_key, ~/.claude.json mcpServers token).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _load_dotenv() -> dict:
    env = {}
    env_path = PROJECT_ROOT / ".env"
    if env_path.is_file():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            v = v.strip()
            # strip inline comments: VALUE  # comment (only after whitespace,
            # so '#' inside a key/token is preserved)
            if " #" in v:
                v = v.split(" #", 1)[0].rstrip()
            env[k.strip()] = v.strip('"').strip("'")
    return env


_DOTENV = _load_dotenv()


def get(name: str, default: Optional[str] = None) -> Optional[str]:
    if name in os.environ and os.environ[name]:
        return os.environ[name]
    if _DOTENV.get(name):
        return _DOTENV[name]
    return default


def brave_api_key() -> Optional[str]:
    key = get("BRAVE_API_KEY")
    if key:
        return key
    p = Path.home() / ".claude" / ".brave_api_key"
    if p.is_file():
        return p.read_text().strip()
    return None


def zai_auth_header() -> Optional[str]:
    """`Authorization: Bearer ...` for the Z.ai web_search_prime MCP."""
    hdr = get("ZAI_AUTH_HEADER")
    if hdr:
        return hdr
    tok = get("ZAI_TOKEN")
    if tok:
        return f"Bearer {tok}"
    try:
        cfg = json.loads((Path.home() / ".claude.json").read_text())
        hdr = cfg.get("mcpServers", {}).get("web-search-prime", {}).get("headers", {}).get("Authorization")
        if hdr:
            return hdr
    except (OSError, json.JSONDecodeError):
        pass
    return None
