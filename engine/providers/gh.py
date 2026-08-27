"""GitHub-тир: нативная обработка github.com через локальный gh CLI.

Идея из конкурентного анализа (docs/competitors-2026-08.md, Tier 1 #5,
источник pi-web-access): HTML-страницы GitHub — худший вход для экстракции
(навигация/обёртки), а gh CLI уже авторизован у владельца. Тир ставится ПЕРВЫМ
в FETCH_CHAIN и перехватывает только github.com (router тихо скипает его для
остальных URL через matches_url). Поддержанные типы: README репо, файл (blob),
PR, issue, releases. Остальные страницы GitHub (wiki, orgs, topics, профиль
владельца...) и любые провалы уходят фолбэком в обычный каскад.

Тот же провайдер — keyless search через `gh api search/repositories`
(30 req/min авторизованным): ставится первым при intent=github (слова
«github / репозиторий / repo / open source» в запросе).

Как local.py: наружу выходит ТОЛЬКО ProviderError (роутер фолбэчит
исключительно по нему). max_chars игнорируется до финального усечения
в router.fetch; внутренний кап CONTENT_CAP — чтобы кэш не пух."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import time
import urllib.parse
from datetime import date, timedelta
from typing import Any, List, Optional

from .base import FetchResult, Provider, ProviderError, QuotaSpec, SearchResult

CONTENT_CAP = 32768
SUBPROCESS_TIMEOUT = 30          # gh быстрый; 30 c хватает на 2-3 вызова
GH_HOSTS = ("github.com", "www.github.com")

# слова-суффиксы табов PR/issue отрезаются в _parse (остаётся номер)
_SEARCH_STOPWORDS = ("github", "репозитор", "repo", "repository",
                     "opensource", "open source")
_last_search = 0.0               # троттлинг search API (30 req/min)


def _api(endpoint: str, *, raw: bool = False) -> tuple[Optional[Any], str]:
    """Один gh api вызов. Возвращает (parsed_json | raw_text, err_kind|"").
    err_kind: not_found | auth | rate | network | http_<code>."""
    cmd = ["gh", "api", endpoint]
    if raw:
        cmd += ["-H", "Accept: application/vnd.github.raw+json"]
    try:
        proc = subprocess.run(cmd, capture_output=True,
                              timeout=SUBPROCESS_TIMEOUT)
    except subprocess.TimeoutExpired:
        return None, "network"
    except OSError:
        return None, "network"
    if proc.returncode == 0:
        out = proc.stdout.decode("utf-8", "replace")
        if raw:
            return out, ""
        try:
            return json.loads(out), ""
        except json.JSONDecodeError:
            return None, "bad_json"
    err = proc.stderr.decode("utf-8", "replace").lower()
    # gh формулирует 404 по-разному: "Not Found", "No commit found for the
    # ref ...", — нормализуем любые 404 в not_found
    if "not found" in err or re.search(r"\b404\b", err):
        return None, "not_found"
    if "bad credentials" in err or "not logged in" in err or "auth" in err:
        return None, "auth"
    if "rate limit" in err or "abuse detection" in err:
        return None, "rate"
    m = re.search(r"\bhttp (\d{3})\b", err) or re.search(r"\bstatus code (\d{3})\b", err)
    if m:
        return None, f"http_{m.group(1)}"
    return None, "network"


def _fail(action: str, err: str) -> ProviderError:
    msg = {"not_found": "not found on github",
           "auth": "gh CLI not authenticated",
           "rate": "rate limited",
           "network": "network/subprocess error"}.get(err, f"error: {err}")
    retryable = err not in ("not_found", "auth", "bad_json")
    return ProviderError(f"github {action}: {msg}", retryable=retryable)


def _looks_binary(text: str) -> bool:
    return "\x00" in text[:1024]


class GhProvider(Provider):
    name = "gh"
    quota = QuotaSpec(limit=None, period="none",
                      label="free via gh CLI (search 30/min)")
    can_fetch = True

    def __init__(self):
        if shutil.which("gh") is None:
            self.available_reason = "gh CLI not installed"

    # ---- fetch -----------------------------------------------------------

    def matches_url(self, url: str) -> bool:
        """Предфильтр роутера: тир перехватывает только github.com
        (raw.githubusercontent остаётся local-http, gist — v1 не поддержан)."""
        try:
            return urllib.parse.urlparse(url).hostname in GH_HOSTS
        except ValueError:
            return False

    def _parse(self, url: str) -> Optional[dict]:
        """github.com/{owner}/{repo}[/{kind}...] -> {owner, repo, kind, ...}.
        None = страница не поддержана (фолбэк в общий каскад)."""
        segs = [s for s in urllib.parse.urlparse(url).path.split("/") if s]
        if len(segs) < 2:
            return None                      # профиль/orgs/topics/about...
        owner, repo = segs[0], segs[1].removesuffix(".git")
        if not (re.fullmatch(r"[A-Za-z0-9_.-]+", owner)
                and re.fullmatch(r"[A-Za-z0-9_.-]+", repo)):
            return None
        if len(segs) == 2:
            return {"kind": "repo"}
        head = segs[2].lower()
        if head in ("pull",) and len(segs) >= 4 and segs[3].isdigit():
            return {"kind": "pr", "num": int(segs[3])}
        if head == "issues" and len(segs) >= 4 and segs[3].isdigit():
            return {"kind": "issue", "num": int(segs[3])}
        if head == "releases":
            tag = segs[4] if len(segs) >= 5 and segs[3] == "tag" else None
            return {"kind": "releases", "tag": tag}
        if head == "blob" and len(segs) >= 5:
            # branch может быть многосегментным (feature/x/y): точный сплит
            # ref/path неизвестен — резолвим перебором от коротких ref
            return {"kind": "file", "segs": segs[3:]}
        return None                          # wiki, tree, compare, forks...

    def fetch(self, url: str, *, max_chars: int = 6000) -> FetchResult:
        info = self._parse(url)
        if info is None:
            # github-страница не поддержана — честный фолбэк в каскад
            raise ProviderError("github: unsupported page type", retryable=False)
        segs = [s for s in urllib.parse.urlparse(url).path.split("/") if s]
        owner, repo = segs[0], segs[1].removesuffix(".git")
        kind = info["kind"]
        if kind == "repo":
            return self._fetch_repo(url, owner, repo)
        if kind == "file":
            return self._fetch_file(url, owner, repo, info["segs"])
        if kind == "pr":
            return self._fetch_pr(url, owner, repo, info["num"])
        if kind == "issue":
            return self._fetch_issue(url, owner, repo, info["num"])
        return self._fetch_releases(url, owner, repo, info.get("tag"))

    def _meta_header(self, owner: str, repo: str) -> tuple[Optional[dict], str]:
        return _api(f"repos/{owner}/{repo}")

    def _fetch_repo(self, url: str, owner: str, repo: str) -> FetchResult:
        meta, err = self._meta_header(owner, repo)
        if err or not isinstance(meta, dict):
            raise _fail(f"repo {owner}/{repo}", err or "bad_json")
        head = (f"# {owner}/{repo}\n\n"
                f"★ {meta.get('stargazers_count', '?')} · "
                f"{meta.get('language') or '—'} · "
                f"updated {(meta.get('pushed_at') or '')[:10]}\n"
                f"> {meta.get('description') or ''}\n\n---\n\n")
        readme, err = _api(f"repos/{owner}/{repo}/readme", raw=True)
        if not err and readme and not _looks_binary(readme):
            content = head + readme
        else:
            # README нет — покажем корень репозитория, это полезнее фолбэка
            root, err2 = _api(f"repos/{owner}/{repo}/contents")
            if err2 or not isinstance(root, list):
                raise _fail(f"repo {owner}/{repo} (no readme)", err2 or err)
            listing = "\n".join(
                f"- {e.get('type', '?'):4} {e.get('name', '?')}" for e in root)
            content = head + "## Files\n\n" + listing + "\n"
        return FetchResult(url=url, title=f"{owner}/{repo}",
                           content=content[:CONTENT_CAP], provider="github-repo")

    def _raw_file(self, owner: str, repo: str, ref: str, path: str):
        ep = (f"repos/{owner}/{repo}/contents/"
              f"{urllib.parse.quote(path)}?ref={urllib.parse.quote(ref)}")
        return _api(ep, raw=True)

    def _fetch_file(self, url: str, owner: str, repo: str,
                    segs: List[str]) -> FetchResult:
        # перебор сплитов ref/path от коротких веток к длинным (обычно 1-2)
        for k in range(1, min(4, len(segs))):
            ref = "/".join(segs[:k])
            path = "/".join(segs[k:])
            text, err = self._raw_file(owner, repo, ref, path)
            if err == "not_found":
                continue                     # не этот сплит
            if err:
                raise _fail(f"file {path}", err)
            if not text or _looks_binary(text):
                raise ProviderError(f"github file {path}: empty/binary",
                                    retryable=False)
            head = f"# {owner}/{repo}:{path} (ref {ref})\n\n"
            return FetchResult(url=url, title=path,
                               content=(head + text)[:CONTENT_CAP],
                               provider="github-file")
        # последний шанс: ветка из URL мертва (master->main после ренейма) —
        # путь без ref-сегмента на дефолтной ветке репозитория
        meta, _ = _api(f"repos/{owner}/{repo}")
        branch = meta.get("default_branch") if isinstance(meta, dict) else None
        if branch and segs[0] != branch and len(segs) > 1:
            path = "/".join(segs[1:])
            text, err2 = self._raw_file(owner, repo, branch, path)
            if not err2 and text and not _looks_binary(text):
                head = f"# {owner}/{repo}:{path} (ref {branch})\n\n"
                return FetchResult(url=url, title=path,
                                   content=(head + text)[:CONTENT_CAP],
                                   provider="github-file")
        raise ProviderError(
            f"github file: no ref/path split resolved "
            f"({'/'.join(segs)}) — branch too deep or gone", retryable=False)

    def _render_discussion(self, owner: str, repo: str, kind: str, num: int,
                           main: dict, comments: list) -> str:
        if kind == "pr":
            state = ("merged" if main.get("merged_at")
                     else "draft" if main.get("draft") else main.get("state", "?"))
            extra = (f" · +{main.get('additions', '?')}/-{main.get('deletions', '?')}"
                     if main.get("additions") is not None else "")
        else:
            state = main.get("state", "?")
            extra = ""
        out = [f"# {kind.upper()} #{num} — {main.get('title', '')} [{state}]",
               f"{owner}/{repo} · by {main.get('user', {}).get('login', '?')}"
               f" · {(main.get('created_at') or '')[:10]}{extra}", "",
               (main.get("body") or "*(no body)*")[:8000]]
        if comments:
            out += ["", f"## Comments ({len(comments)})", ""]
            for c in comments[-12:]:
                body = (c.get("body") or "").strip()[:1200]
                out += [f"**{c.get('user', {}).get('login', '?')}** "
                        f"({(c.get('created_at') or '')[:10]}):", body, ""]
        return "\n".join(out)

    def _fetch_pr(self, url: str, owner: str, repo: str, num: int) -> FetchResult:
        pr, err = _api(f"repos/{owner}/{repo}/pulls/{num}")
        if err or not isinstance(pr, dict):
            raise _fail(f"PR #{num}", err or "bad_json")
        comments, _ = _api(f"repos/{owner}/{repo}/issues/{num}/comments")
        content = self._render_discussion(owner, repo, "pr", num,
                                          pr, comments or [])
        return FetchResult(url=url, title=f"PR #{num}: {pr.get('title', '')}",
                           content=content[:CONTENT_CAP], provider="github-pr")

    def _fetch_issue(self, url: str, owner: str, repo: str, num: int) -> FetchResult:
        iss, err = _api(f"repos/{owner}/{repo}/issues/{num}")
        if err or not isinstance(iss, dict):
            raise _fail(f"issue #{num}", err or "bad_json")
        if "pull_request" in iss:            # issue-номер может быть PR
            return self._fetch_pr(url, owner, repo, num)
        comments, _ = _api(f"repos/{owner}/{repo}/issues/{num}/comments")
        content = self._render_discussion(owner, repo, "issue", num,
                                          iss, comments or [])
        return FetchResult(url=url, title=f"issue #{num}: {iss.get('title', '')}",
                           content=content[:CONTENT_CAP], provider="github-issue")

    def _fetch_releases(self, url: str, owner: str, repo: str,
                        tag: Optional[str]) -> FetchResult:
        rels, err = _api(f"repos/{owner}/{repo}/releases?per_page=10")
        if err or not isinstance(rels, list):
            raise _fail(f"releases {owner}/{repo}", err or "bad_json")
        items = rels
        if tag:
            items = [r for r in items if r.get("tag_name") == tag] or items
        if not items:
            content = f"# {owner}/{repo}\n\nNo releases published.\n"
        else:
            parts = [f"# {owner}/{repo} — releases", ""]
            for r in items[:5]:
                parts += [f"## {r.get('tag_name', '?')} — "
                          f"{r.get('name') or '(untitled)'} "
                          f"({(r.get('published_at') or '')[:10]})", "",
                          (r.get("body") or "").strip()[:4000], ""]
            content = "\n".join(parts)
        return FetchResult(url=url, title=f"{owner}/{repo} releases",
                           content=content[:CONTENT_CAP],
                           provider="github-releases")

    # ---- search ----------------------------------------------------------

    def search(self, query: str, *, n: int = 8,
               freshness: Optional[str] = None) -> List[SearchResult]:
        global _last_search
        wait = 1.0 - (time.time() - _last_search)
        if wait > 0:
            time.sleep(wait)
        _last_search = time.time()

        # убираем слова-триггеры интента («github», «репозиторий»…) —
        # для search/repositories они мусорные уточнители
        q = query
        for w in _SEARCH_STOPWORDS:
            q = re.sub(rf"(?i)(?<!\w){re.escape(w)}\S*", " ", q)
        q = " ".join(q.split()).strip() or query
        if freshness:
            days = {"day": 3, "week": 7, "month": 30}.get(freshness, 30)
            since = (date.today() - timedelta(days=days)).isoformat()
            q = f"{q} pushed:>={since}"
        data, err = _api(
            f"search/repositories?q={urllib.parse.quote_plus(q)}"
            f"&per_page={max(1, min(n, 30))}")
        if err:
            raise _fail("search", err)
        items = (data or {}).get("items") or []
        if not items:
            raise ProviderError("gh: no repositories matched", retryable=False)
        out = []
        for it in items[:n]:
            snippet = (f"★{it.get('stargazers_count', 0)} · "
                       f"{it.get('language') or '—'} · "
                       f"{it.get('description') or ''} · "
                       f"updated {(it.get('pushed_at') or '')[:10]}")
            out.append(SearchResult(
                url=it.get("html_url", ""),
                title=it.get("full_name", ""),
                snippet=snippet,
                date=(it.get("pushed_at") or "")[:10],
                provider=self.name))
        return out
