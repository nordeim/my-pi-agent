#!/usr/bin/env python3
# github_folder_downloader.py 
# version: 3.0
"""Download and mirror a GitHub repository folder without cloning the repository.

Usage:
  python github_folder_downloader.py URL DESTINATION [options]

Retrieval is layered:
  Tier 1: targeted GitHub API + raw retrieval (only the requested subtree).
  Tier 2: repository ZIP archive, selective extraction.
  Tier 3: repository TAR.GZ archive, selective extraction.

Only regular files are materialized; downloaded content is never executed.
Symlinks, hardlinks, devices, FIFOs, and submodules are skipped by default
(or rejected with --symlink-policy fail). Destination writes are atomic:
a partial file never survives as a finished artifact.

Exit codes:
  0  success
  1  unexpected error
  2  usage error / destination not usable
  3  ambiguous ref (retry with --ref)
  4  URL parse error
  5  resolution error (ref or folder not found)
  6  retrieval error (network, archive)
  7  commit error (destination conflict)
  130 interrupted

See --help for limits and options.
"""
from __future__ import annotations

import argparse
import datetime
import email.utils
import hashlib
import http.client
import json
import logging
import os
import random
import re
import shutil
import stat
import sys
import tarfile
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import IO, Final, TypeVar

LOG = logging.getLogger("github-folder-downloader")
USER_AGENT: Final = "github-folder-downloader/3.0 (Python urllib)"
API_BASE: Final = "https://api.github.com"
RAW_BASE: Final = "https://raw.githubusercontent.com"
CODELOAD_BASE: Final = "https://codeload.github.com"
MIB: Final = 1024 * 1024
DEFAULT_MAX_DOWNLOAD: Final = 100 * MIB
DEFAULT_MAX_EXTRACT: Final = 250 * MIB
DEFAULT_MAX_FILES: Final = 5000
DEFAULT_MAX_DEPTH: Final = 100
DEFAULT_MAX_COMPRESSION_RATIO: Final = 1000
COMPRESSION_RATIO_MIN_SIZE: Final = MIB
CHUNK: Final = 64 * 1024
API_JSON_LIMIT: Final = 10 * MIB
ERROR_BODY_LIMIT: Final = 1024
ERROR_DETAIL_LIMIT: Final = 300
RETRY_ATTEMPTS: Final = 3
RETRY_BASE_DELAY: Final = 0.5
RETRY_MAX_DELAY: Final = 8.0
RETRY_AFTER_CAP: Final = 60.0
RETRY_STATUS: Final = frozenset({429, 500, 502, 503, 504})
ARCHIVE_MAX_EXPANSION: Final = 100
MIN_ARCHIVE_ENTRIES: Final = 1000
ENTRY_CAP_FACTOR: Final = 10
SYMLINK_MODE: Final = "120000"
WINDOWS_ILLEGAL: Final = re.compile(r'[<>:"|?*\x00-\x1f]')
WINDOWS_RESERVED: Final = frozenset(
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{i}" for i in range(1, 10)}
    | {f"LPT{i}" for i in range(1, 10)}
)

EXIT_OK: Final = 0
EXIT_FAILURE: Final = 1
EXIT_USAGE: Final = 2
EXIT_AMBIGUOUS: Final = 3
EXIT_URL: Final = 4
EXIT_RESOLVE: Final = 5
EXIT_RETRIEVE: Final = 6
EXIT_COMMIT: Final = 7
EXIT_INTERRUPTED: Final = 130

T = TypeVar("T")


class DownloadError(Exception):
    """Expected operational failure, optionally carrying an HTTP status."""

    def __init__(self, message: str, *, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status


class UsageError(DownloadError):
    """Invalid CLI input or destination state discovered at startup."""


class URLParseError(DownloadError):
    """The supplied URL is structurally invalid."""


class ResolutionError(DownloadError):
    """The ref or folder could not be resolved."""


class AmbiguousRefError(ResolutionError):
    """Several ref/folder interpretations of one URL are valid."""

    def __init__(self, message: str, interpretations: Sequence[str]) -> None:
        super().__init__(message)
        self.interpretations = tuple(interpretations)


class RetrievalError(DownloadError):
    """Network or archive retrieval failed."""


class CommitError(DownloadError):
    """Destination-side failure. Never triggers archive fallback."""


@dataclass(frozen=True)
class RepoTarget:
    owner: str
    repo: str
    ref: str
    path: str
    commit_sha: str
    tree_sha: str
    subtree_sha: str = ""


@dataclass(frozen=True)
class TreeEntry:
    path: str
    kind: str
    sha: str
    size: int
    mode: str


def safe_relpath(path: str) -> PurePosixPath:
    """Validate a repository/archive path and split it into materializable parts.

    Structural checks use normalized separators so traversal, absolute, drive,
    and UNC forms are rejected on every platform. Materialization keeps the
    original separators: on POSIX a backslash is a legal filename character and
    must not silently become a directory boundary.
    """
    if not path or "\x00" in path:
        raise DownloadError(f"Unsafe or empty path: {path!r}")
    normalized = path.replace("\\", "/")
    probe = PurePosixPath(normalized)
    if probe.is_absolute() or ".." in probe.parts:
        raise DownloadError(f"Unsafe path (absolute or traversal): {path!r}")
    if re.match(r"^[A-Za-z]:", normalized) or normalized.startswith("//"):
        raise DownloadError(f"Unsafe path (drive or UNC): {path!r}")
    parts = tuple(p for p in path.split("/") if p not in ("", "."))
    if not parts:
        raise DownloadError(f"Unsafe or empty path: {path!r}")
    if os.name == "nt":
        for part in parts:
            stem = part.split(".")[0].upper()
            if (
                "\\" in part
                or WINDOWS_ILLEGAL.search(part)
                or stem in WINDOWS_RESERVED
                or part.endswith((" ", "."))
            ):
                raise DownloadError(f"Path component is not valid on Windows: {part!r}")
    return PurePosixPath(*parts)


def safe_destination_path(base: Path, rel: PurePosixPath, *, allow_root_symlink: bool = False) -> Path:
    """Resolve `rel` under `base`, rejecting any pre-existing symlink component.

    Prevents a symlink in the destination (placed by a prior process or the
    user) from redirecting the write outside the intended tree.
    """
    if not allow_root_symlink and base.is_symlink():
        raise CommitError(f"Destination root is a symlink: {base}")
    current = base
    for part in rel.parts:
        current = current / part
        try:
            st = os.lstat(current)
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(st.st_mode):
            raise CommitError(f"Refusing to write through symlink: {current}")
    return current


class SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    """urllib copies request headers verbatim on redirect; credentials must not
    cross origins, and a redirect must never downgrade HTTPS."""

    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: IO[bytes],
        code: int,
        msg: str,
        headers: Mapping[str, str],
        newurl: str,
    ) -> urllib.request.Request | None:
        new_req = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new_req is None:
            return None
        target = urllib.parse.urlsplit(newurl)
        if target.scheme != "https":
            raise DownloadError(f"Refusing non-HTTPS redirect target for {req.full_url}")
        origin = urllib.parse.urlsplit(req.full_url)
        if (target.hostname or "").lower() != (origin.hostname or "").lower():
            for key in list(new_req.headers):
                if key.lower() == "authorization":
                    del new_req.headers[key]
        return new_req


_opener_installed = False


def ensure_safe_opener() -> None:
    global _opener_installed
    if not _opener_installed:
        urllib.request.install_opener(urllib.request.build_opener(SafeRedirectHandler()))
        _opener_installed = True


def _retry_after_seconds(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        pass
    try:
        when = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=datetime.timezone.utc)
    return max(0.0, (when - datetime.datetime.now(datetime.timezone.utc)).total_seconds())


def _backoff(attempt: int, base: float = RETRY_BASE_DELAY) -> float:
    return min(RETRY_MAX_DELAY, base * (2 ** (attempt - 1))) * (0.5 + random.random() / 2)


def _error_detail(exc: urllib.error.HTTPError) -> str:
    try:
        body = exc.read(ERROR_BODY_LIMIT)
    except (OSError, ValueError):
        return ""
    return body.decode("utf-8", "replace")[:ERROR_DETAIL_LIMIT]


def _http_message(url: str, status: int, detail: str, headers: Mapping[str, str] | None) -> str:
    remaining = headers.get("X-RateLimit-Remaining") if headers is not None else None
    if status in (403, 429) and remaining == "0":
        reset = headers.get("X-RateLimit-Reset") if headers is not None else None
        return (
            f"GitHub API rate limit exceeded (HTTP {status}) for {url}"
            + (f"; quota resets at epoch {reset}" if reset else "")
            + ". Set a token via --token-env for a higher quota."
        )
    if status == 401:
        return f"HTTP 401 for {url}: authentication failed; check the token in --token-env."
    if status == 404:
        return f"HTTP 404 for {url}: not found (private repository or wrong ref/path?)."
    return f"HTTP {status} for {url}: {detail}"


def _check_content_length(value: str | None, limit: int | None, url: str) -> None:
    if limit is None or not value:
        return
    try:
        length = int(value)
    except ValueError:
        return
    if length > limit:
        raise DownloadError(f"Response exceeds size limit ({limit} bytes): {url}")


def _perform(
    url: str,
    *,
    timeout: float,
    token: str | None,
    accept: str,
    handle: Callable[[http.client.HTTPResponse], T],
    retries: int = RETRY_ATTEMPTS,
    backoff_base: float = RETRY_BASE_DELAY,
) -> T:
    """Single HTTP seam: HTTPS-only, bounded retries, credential-safe redirects."""
    ensure_safe_opener()
    if not url.lower().startswith("https://"):
        raise DownloadError("HTTPS is required for network requests.")
    headers = {"User-Agent": USER_AGENT, "Accept": accept}
    if token:
        headers["Authorization"] = "Bearer " + token
    for attempt in range(1, retries + 1):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return handle(response)
        except urllib.error.HTTPError as exc:
            status, detail, resp_headers = exc.code, _error_detail(exc), exc.headers
            exc.close()
            if status in RETRY_STATUS and attempt < retries:
                hinted = _retry_after_seconds(resp_headers.get("Retry-After") if resp_headers else None)
                if hinted is not None and hinted > RETRY_AFTER_CAP:
                    raise DownloadError(
                        f"HTTP {status} for {url}: server asks to retry after {hinted:.0f}s "
                        f"(cap {RETRY_AFTER_CAP:.0f}s); retry later.",
                        status=status,
                    ) from exc
                delay = hinted if hinted is not None else _backoff(attempt, backoff_base)
                LOG.warning("HTTP %s for %s; retry %d/%d in %.1fs",
                            status, url, attempt + 1, retries, delay)
                time.sleep(delay)
                continue
            raise DownloadError(_http_message(url, status, detail, resp_headers), status=status) from exc
        except (urllib.error.URLError, TimeoutError, ConnectionError,
                http.client.IncompleteRead, http.client.RemoteDisconnected) as exc:
            if attempt < retries:
                delay = _backoff(attempt, backoff_base)
                LOG.warning("Network error for %s (%s); retry %d/%d in %.1fs",
                            url, exc, attempt + 1, retries, delay)
                time.sleep(delay)
                continue
            raise DownloadError(f"Network error for {url}: {exc}") from exc
    raise DownloadError(f"Request failed after {retries} attempts: {url}")


def request_bytes(
    url: str,
    *,
    timeout: float,
    token: str | None = None,
    accept: str = "application/vnd.github+json",
    limit: int | None = None,
    retries: int = RETRY_ATTEMPTS,
    backoff_base: float = RETRY_BASE_DELAY,
) -> bytes:
    def handle(response: http.client.HTTPResponse) -> bytes:
        _check_content_length(response.headers.get("Content-Length"), limit, url)
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = response.read(CHUNK)
            if not chunk:
                break
            total += len(chunk)
            if limit is not None and total > limit:
                raise DownloadError(f"Response exceeds size limit ({limit} bytes): {url}")
            chunks.append(chunk)
        return b"".join(chunks)

    return _perform(url, timeout=timeout, token=token, accept=accept, handle=handle,
                    retries=retries, backoff_base=backoff_base)


def stream_to_file(
    url: str,
    out: Path,
    *,
    timeout: float,
    token: str | None,
    max_size: int,
    accept: str = "application/octet-stream",
    retries: int = RETRY_ATTEMPTS,
    backoff_base: float = RETRY_BASE_DELAY,
) -> int:
    def handle(response: http.client.HTTPResponse) -> int:
        _check_content_length(response.headers.get("Content-Length"), max_size, url)
        total = 0
        with out.open("wb") as fh:
            while True:
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                total += len(chunk)
                if total > max_size:
                    raise DownloadError(f"Download exceeds configured limit ({max_size} bytes): {url}")
                fh.write(chunk)
        return total

    try:
        return _perform(url, timeout=timeout, token=token, accept=accept, handle=handle,
                        retries=retries, backoff_base=backoff_base)
    except BaseException:
        # A partial download must never survive as a "recoverable" artifact.
        out.unlink(missing_ok=True)
        raise


def _json_object(value: object, context: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise DownloadError(f"Unexpected GitHub API response ({context}): expected an object.")
    return {str(k): v for k, v in value.items()}


def _json_list(value: object, context: str) -> list[object]:
    if not isinstance(value, list):
        raise DownloadError(f"Unexpected GitHub API response ({context}): expected a list.")
    return list(value)


def _string_field(obj: dict[str, object], key: str, context: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value:
        raise DownloadError(f"Unexpected GitHub API response ({context}): missing string '{key}'.")
    return value


def api_json(
    url: str,
    *,
    timeout: float,
    token: str | None,
    retries: int = RETRY_ATTEMPTS,
    backoff_base: float = RETRY_BASE_DELAY,
) -> object:
    payload = request_bytes(url, timeout=timeout, token=token, limit=API_JSON_LIMIT,
                            retries=retries, backoff_base=backoff_base)
    try:
        result: object = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DownloadError(f"Invalid JSON response from GitHub API: {url}") from exc
    return result


def encode_path(path: str) -> str:
    return "/".join(urllib.parse.quote(part, safe="") for part in path.split("/") if part)


def parse_url(url: str) -> tuple[str, str, list[str], str]:
    """Parse a github.com owner/repo tree URL into owner, repo, tail, kind.

    A folder URL must include both a ref candidate and a path candidate. For
    "whole tree at a specific ref", use the repository root URL with --ref.
    """
    try:
        parsed = urllib.parse.urlsplit(url)
    except ValueError as exc:
        raise URLParseError(f"Invalid URL: {exc}") from exc
    if parsed.scheme != "https" or parsed.hostname != "github.com" or parsed.username or parsed.password:
        raise URLParseError("Expected an HTTPS github.com URL.")
    if parsed.query or parsed.fragment:
        raise URLParseError("Query strings and fragments are not supported in folder URLs.")
    parts = [urllib.parse.unquote(p) for p in parsed.path.strip("/").split("/") if p]
    if len(parts) < 2:
        raise URLParseError("URL must include OWNER and REPO.")
    owner, repo = parts[0], parts[1]
    if repo.endswith(".git"):
        repo = repo[:-4]
    if not owner or not repo or any("/" in x or x in (".", "..") for x in (owner, repo)):
        raise URLParseError("Invalid owner or repository name.")
    if len(parts) == 2:
        return owner, repo, [], "root"
    if parts[2] != "tree" or len(parts) < 5:
        raise URLParseError(
            "Expected a folder URL in the form https://github.com/OWNER/REPO/tree/REF/PATH.")
    return owner, repo, parts[3:], "tree"


def get_repo_default_branch(
    owner: str, repo: str, *,
    timeout: float, token: str | None,
    retries: int = RETRY_ATTEMPTS, backoff_base: float = RETRY_BASE_DELAY,
) -> str:
    data = _json_object(
        api_json(f"{API_BASE}/repos/{encode_path(owner)}/{encode_path(repo)}",
                 timeout=timeout, token=token, retries=retries, backoff_base=backoff_base),
        "repository")
    return _string_field(data, "default_branch", "repository")


def _commit_for_ref(
    owner: str, repo: str, ref: str, *,
    timeout: float, token: str | None,
    retries: int = RETRY_ATTEMPTS, backoff_base: float = RETRY_BASE_DELAY,
) -> tuple[str, str] | None:
    """Return (commit_sha, root_tree_sha); None only when the ref does not exist."""
    url = (f"{API_BASE}/repos/{encode_path(owner)}/{encode_path(repo)}"
           f"/commits/{encode_path(ref)}")
    try:
        data = _json_object(
            api_json(url, timeout=timeout, token=token,
                     retries=retries, backoff_base=backoff_base),
            "commit")
    except DownloadError as exc:
        if exc.status == 404:
            return None
        raise  # rate limits, auth and server faults must not masquerade as a miss
    sha = _string_field(data, "sha", "commit")
    commit = _json_object(data.get("commit"), "commit body")
    tree = _json_object(commit.get("tree"), "commit tree")
    return sha, _string_field(tree, "sha", "commit tree")


@dataclass
class TreeCache:
    owner: str
    repo: str
    timeout: float
    token: str | None
    retries: int = RETRY_ATTEMPTS
    backoff_base: float = RETRY_BASE_DELAY
    _trees: dict[str, list[TreeEntry]] = field(default_factory=dict)

    def listing(self, tree_sha: str) -> list[TreeEntry]:
        cached = self._trees.get(tree_sha)
        if cached is not None:
            return cached
        url = (f"{API_BASE}/repos/{encode_path(self.owner)}/{encode_path(self.repo)}"
               f"/git/trees/{encode_path(tree_sha)}")
        data = _json_object(
            api_json(url, timeout=self.timeout, token=self.token,
                     retries=self.retries, backoff_base=self.backoff_base),
            "tree")
        entries = [_tree_entry(item) for item in _json_list(data.get("tree"), "tree entries")]
        self._trees[tree_sha] = entries
        return entries


def _tree_entry(item: object) -> TreeEntry:
    obj = _json_object(item, "tree entry")
    size, mode = obj.get("size", 0), obj.get("mode", "")
    return TreeEntry(
        path=_string_field(obj, "path", "tree entry"),
        kind=_string_field(obj, "type", "tree entry"),
        sha=_string_field(obj, "sha", "tree entry"),
        size=size if isinstance(size, int) and size >= 0 else 0,
        mode=mode if isinstance(mode, str) else "",
    )


def _subtree_sha(cache: TreeCache, root_tree: str, path: str, *, max_depth: int) -> str | None:
    """Walk only the path components (O(depth) calls) to the target subtree."""
    if not path:
        return root_tree
    parts = path.split("/")
    if len(parts) > max_depth:
        raise DownloadError(f"Folder depth exceeds configured limit ({max_depth}).")
    current = root_tree
    for part in parts:
        match = next((e for e in cache.listing(current) if e.path == part and e.kind == "tree"), None)
        if match is None:
            return None
        current = match.sha
    return current


def _recursive_subtree(cache: TreeCache, tree_sha: str) -> list[TreeEntry] | None:
    url = (f"{API_BASE}/repos/{encode_path(cache.owner)}/{encode_path(cache.repo)}"
           f"/git/trees/{encode_path(tree_sha)}?recursive=1")
    data = _json_object(
        api_json(url, timeout=cache.timeout, token=cache.token,
                 retries=cache.retries, backoff_base=cache.backoff_base),
        "recursive tree")
    if data.get("truncated") is True:
        return None
    return [_tree_entry(item) for item in _json_list(data.get("tree"), "recursive tree")]


def _walk_subtree(cache: TreeCache, tree_sha: str, *, max_files: int, max_depth: int) -> list[TreeEntry]:
    """Iterative, subtree-scoped walk used when the recursive listing is truncated."""
    out: list[TreeEntry] = []
    stack: list[tuple[str, str]] = [(tree_sha, "")]
    files = 0
    while stack:
        sha, prefix = stack.pop()
        for entry in cache.listing(sha):
            rel = f"{prefix}/{entry.path}" if prefix else entry.path
            depth = len(PurePosixPath(rel).parts)
            if depth > max_depth:
                raise DownloadError(f"Folder depth exceeds configured limit ({max_depth}).")
            if entry.kind == "tree":
                out.append(TreeEntry(rel, "tree", entry.sha, 0, entry.mode))
                stack.append((entry.sha, rel))
            elif entry.kind == "blob":
                # Symlinks are not materialized and must not count toward max_files.
                if entry.mode != SYMLINK_MODE:
                    files += 1
                    if files > max_files:
                        raise DownloadError(f"Folder contains more than {max_files} files.")
                out.append(TreeEntry(rel, "blob", entry.sha, entry.size, entry.mode))
            else:
                out.append(TreeEntry(rel, entry.kind, entry.sha, 0, entry.mode))
    return out


def fetch_folder_entries(cache: TreeCache, tree_sha: str, *, max_files: int,
                         max_depth: int) -> list[TreeEntry]:
    recursive = _recursive_subtree(cache, tree_sha)
    if recursive is None:
        LOG.info("Recursive tree listing truncated; walking the target subtree directory by directory.")
        return _walk_subtree(cache, tree_sha, max_files=max_files, max_depth=max_depth)
    files = 0
    for entry in recursive:
        if len(PurePosixPath(entry.path).parts) > max_depth:
            raise DownloadError(f"Folder depth exceeds configured limit ({max_depth}).")
        if entry.kind == "blob" and entry.mode != SYMLINK_MODE:
            files += 1
    if files > max_files:
        raise DownloadError(f"Folder contains more than {max_files} files.")
    return recursive


def resolve_target(
    owner: str, repo: str, tail: list[str], kind: str, *,
    timeout: float,
    token: str | None,
    ref_override: str | None = None,
    max_depth: int = DEFAULT_MAX_DEPTH,
    retries: int = RETRY_ATTEMPTS,
    backoff_base: float = RETRY_BASE_DELAY,
) -> RepoTarget:
    cache = TreeCache(owner, repo, timeout, token, retries=retries, backoff_base=backoff_base)

    if kind == "root" and ref_override is None:
        ref = get_repo_default_branch(owner, repo, timeout=timeout, token=token,
                                      retries=retries, backoff_base=backoff_base)
        resolved = _commit_for_ref(owner, repo, ref, timeout=timeout, token=token,
                                   retries=retries, backoff_base=backoff_base)
        if resolved is None:
            raise ResolutionError(f"Ref not found: {ref}")
        sha, tree = resolved
        return RepoTarget(owner, repo, ref, "", sha, tree, tree)

    if ref_override is not None:
        ref = ref_override
        # Strip the ref prefix from tail if present: users who pin --ref should
        # not have to strip it from the URL themselves.
        ref_parts = ref.split("/")
        if tail[:len(ref_parts)] == ref_parts:
            path = "/".join(tail[len(ref_parts):])
        else:
            path = "/".join(tail)
        resolved = _commit_for_ref(owner, repo, ref, timeout=timeout, token=token,
                                   retries=retries, backoff_base=backoff_base)
        if resolved is None:
            raise ResolutionError(f"Ref not found: {ref}")
        sha, tree = resolved
        subtree = tree if not path else _subtree_sha(cache, tree, path, max_depth=max_depth)
        if subtree is None:
            raise ResolutionError(f"Folder not found at ref {ref}: {path or '(repository root)'}")
        return RepoTarget(owner, repo, ref, path, sha, tree, subtree)

    matches: list[RepoTarget] = []
    for split in range(len(tail), 0, -1):
        ref, path = "/".join(tail[:split]), "/".join(tail[split:])
        resolved = _commit_for_ref(owner, repo, ref, timeout=timeout, token=token,
                                   retries=retries, backoff_base=backoff_base)
        if resolved is None:
            continue
        sha, tree = resolved
        subtree = _subtree_sha(cache, tree, path, max_depth=max_depth)
        if subtree is None:
            continue
        matches.append(RepoTarget(owner, repo, ref, path, sha, tree, subtree))
        # Shorter candidates are still examined: a silent longest-match choice
        # could mirror the wrong folder.
    if not matches:
        raise ResolutionError(
            "Could not resolve the URL ref and folder path. Check the URL; "
            "if the branch name contains slashes, re-run with --ref.")
    if len(matches) > 1:
        raise AmbiguousRefError(
            "Ambiguous URL: multiple ref/folder interpretations exist. Re-run with --ref:",
            [f"--ref {m.ref}  (folder: {m.path or '(repository root)'})" for m in matches])
    return matches[0]


def git_blob_sha(data: bytes) -> str:
    """Git's content identifier (SHA-1 by Git's design, not a security signature)."""
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def download_blob(
    target: RepoTarget, path: str, *,
    timeout: float, token: str | None, max_size: int,
    retries: int = RETRY_ATTEMPTS, backoff_base: float = RETRY_BASE_DELAY,
) -> bytes:
    # Pin the resolved commit: branch names are mutable and slash-refs are
    # ambiguous on the raw host.
    url = (f"{RAW_BASE}/{encode_path(target.owner)}/{encode_path(target.repo)}"
           f"/{encode_path(target.commit_sha)}/{encode_path(path)}")
    return request_bytes(url, timeout=timeout, token=token,
                         accept="application/octet-stream", limit=max_size,
                         retries=retries, backoff_base=backoff_base)


def _verify_blob(entry: TreeEntry, data: bytes) -> None:
    if entry.size and len(data) != entry.size:
        raise DownloadError(
            f"Size mismatch for {entry.path}: expected {entry.size} bytes, got {len(data)}.")
    if entry.sha and git_blob_sha(data) != entry.sha:
        raise DownloadError(f"Integrity check failed for {entry.path}: Git blob SHA mismatch.")


def stage_api_folder(
    target: RepoTarget, stage: Path, *,
    timeout: float, token: str | None,
    max_download: int, max_files: int, max_depth: int,
    max_extract: int = DEFAULT_MAX_EXTRACT,
    symlink_policy: str = "skip",
    retries: int = RETRY_ATTEMPTS,
    backoff_base: float = RETRY_BASE_DELAY,
) -> tuple[int, int]:
    cache = TreeCache(target.owner, target.repo, timeout, token,
                      retries=retries, backoff_base=backoff_base)
    subtree = target.subtree_sha or _subtree_sha(cache, target.tree_sha, target.path, max_depth=max_depth)
    if subtree is None:
        raise ResolutionError(f"Target folder not found: {target.path or '(repository root)'}")
    entries = fetch_folder_entries(cache, subtree, max_files=max_files, max_depth=max_depth)
    files: list[TreeEntry] = []
    for entry in entries:
        if entry.kind == "commit":
            LOG.warning("Skipping submodule (not retrieved): %s", entry.path)
        elif entry.kind == "blob" and entry.mode == SYMLINK_MODE:
            if symlink_policy == "fail":
                raise DownloadError(f"Symlink entry not supported (--symlink-policy fail): {entry.path}")
            LOG.warning("Skipping symlink (not materialized): %s", entry.path)
        elif entry.kind == "blob":
            files.append(entry)
    if not files:
        raise DownloadError(
            f"No regular files found in the requested folder: {target.path or '(repository root)'}")
    if len(files) > max_files:
        raise DownloadError(f"Folder contains more than {max_files} files.")
    total = 0
    for entry in files:
        safe = safe_relpath(entry.path)
        if len(safe.parts) > max_depth:
            raise DownloadError(f"Folder depth exceeds configured limit ({max_depth}).")
        if entry.size > max_download:
            raise DownloadError(f"File exceeds per-download limit: {entry.path}")
        data = download_blob(target, entry.path, timeout=timeout, token=token,
                             max_size=max_download, retries=retries, backoff_base=backoff_base)
        _verify_blob(entry, data)
        total += len(data)
        if total > max_extract:
            raise DownloadError(f"Folder exceeds extracted-size limit ({max_extract} bytes).")
        dest = stage.joinpath(*safe.parts)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    return len(files), total


def archive_urls(target: RepoTarget) -> list[tuple[str, str]]:
    owner, repo = encode_path(target.owner), encode_path(target.repo)
    commit = urllib.parse.quote(target.commit_sha, safe="")
    return [
        ("zip", f"{CODELOAD_BASE}/{owner}/{repo}/zip/{commit}"),
        ("tar.gz", f"{CODELOAD_BASE}/{owner}/{repo}/tar.gz/{commit}"),
    ]


def archive_filename(target: RepoTarget, fmt: str) -> str:
    base = re.sub(r"[^A-Za-z0-9._-]+", "-", f"{target.repo}-{target.ref}").strip("-") or "repository"
    return f"{base}.{fmt}"


def archive_prefix(target: RepoTarget, members: Sequence[str]) -> str:
    roots = {parts[0] for name in members if (parts := [p for p in name.replace("\\", "/").split("/") if p])}
    if len(roots) != 1:
        raise DownloadError("Archive has an unexpected root structure.")
    root = next(iter(roots))
    path = target.path.strip("/")
    return root + ("/" + path if path else "")


def _entry_cap(max_files: int) -> int:
    return max(MIN_ARCHIVE_ENTRIES, ENTRY_CAP_FACTOR * max_files)


def _copy_bounded(src: IO[bytes], dst: IO[bytes], budget: int, label: str) -> int:
    """Count actual bytes written: archive headers are untrusted declarations."""
    total = 0
    while True:
        chunk = src.read(CHUNK)
        if not chunk:
            break
        total += len(chunk)
        if total > budget:
            raise DownloadError(f"Extracted content exceeds size limit while reading {label}")
        dst.write(chunk)
    return total


def extract_zip_target(
    archive: Path, stage: Path, target: RepoTarget, *,
    max_extract: int, max_files: int, max_depth: int,
    symlink_policy: str = "skip",
    max_compression_ratio: int = DEFAULT_MAX_COMPRESSION_RATIO,
) -> tuple[int, int]:
    cap = _entry_cap(max_files)
    with zipfile.ZipFile(archive) as zf:
        infos = zf.infolist()
        if len(infos) > cap:
            raise DownloadError(f"Archive contains too many entries ({len(infos)} > {cap}).")
        prefix = archive_prefix(target, [i.filename for i in infos]).rstrip("/") + "/"
        selected: list[tuple[zipfile.ZipInfo, str]] = []
        declared = 0
        for info in infos:
            name = info.filename.replace("\\", "/")
            if not name.startswith(prefix) or name.endswith("/"):
                continue
            rel = name[len(prefix):]
            if not rel:
                continue
            parts = safe_relpath(rel)
            if len(parts.parts) > max_depth:
                raise DownloadError("Archive folder depth exceeds limit.")
            if info.is_dir():
                continue
            mode = (info.external_attr >> 16) & 0xFFFF
            if mode:
                file_type = stat.S_IFMT(mode)
                if file_type == stat.S_IFLNK:
                    if symlink_policy == "fail":
                        raise DownloadError(f"ZIP contains symlink (--symlink-policy fail): {rel}")
                    LOG.warning("Skipping ZIP symlink: %s", rel)
                    continue
                if file_type not in (0, stat.S_IFREG):
                    raise DownloadError(f"ZIP contains a non-regular entry: {rel}")
            if info.file_size < 0 or info.file_size > max_extract:
                raise DownloadError(f"ZIP entry exceeds extraction limit: {rel}")
            if (info.file_size > COMPRESSION_RATIO_MIN_SIZE
                    and info.compress_size > 0):
                ratio = info.file_size / info.compress_size
                if ratio > max_compression_ratio:
                    raise DownloadError(
                        f"ZIP entry has suspicious compression ratio ({ratio:.0f}:1): {rel}")
            declared += info.file_size
            if declared > max_extract:
                raise DownloadError("ZIP extracted content exceeds size limit.")
            selected.append((info, rel))
        if not selected:
            raise DownloadError(
                f"Requested folder not found in archive: {target.path or '(repository root)'}")
        if len(selected) > max_files:
            raise DownloadError("ZIP extracted file count exceeds limit.")
        written = 0
        for info, rel in selected:
            dest = stage.joinpath(*safe_relpath(rel).parts)
            dest.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as src, dest.open("wb") as dst:
                written += _copy_bounded(src, dst, max_extract - written, rel)
        return len(selected), written


def extract_tar_target(
    archive: Path, stage: Path, target: RepoTarget, *,
    max_extract: int, max_files: int, max_depth: int,
    symlink_policy: str = "skip",
) -> tuple[int, int]:
    """Single streaming pass: member data is bounded before it is decompressed."""
    cap = _entry_cap(max_files)
    scan_budget = max(max_extract, ARCHIVE_MAX_EXPANSION * archive.stat().st_size)
    root: str | None = None
    prefix = ""
    scanned = written = count = entries = 0
    with tarfile.open(archive, "r|gz") as tf:
        for member in tf:
            entries += 1
            if entries > cap:
                raise DownloadError(f"Archive contains too many entries (> {cap}).")
            scanned += max(0, member.size)
            if scanned > scan_budget:
                raise DownloadError(
                    f"Archive expansion exceeds the safe scan budget ({scan_budget} bytes); "
                    "refusing to decompress further.")
            parts = [p for p in member.name.replace("\\", "/").split("/") if p]
            if not parts:
                continue
            if root is None:
                root = parts[0]
                path = target.path.strip("/")
                prefix = root + ("/" + path if path else "") + "/"
            elif parts[0] != root:
                raise DownloadError("Archive has an unexpected root structure.")
            name = member.name.replace("\\", "/")
            if not name.startswith(prefix) or member.isdir():
                continue
            rel = name[len(prefix):]
            if not rel:
                continue
            safe = safe_relpath(rel)
            if len(safe.parts) > max_depth:
                raise DownloadError("TAR extracted folder depth exceeds limit.")
            if not member.isfile():
                if member.issym() or member.islnk():
                    if symlink_policy == "fail":
                        raise DownloadError(
                            f"TAR contains symlink (--symlink-policy fail): {rel}")
                    LOG.warning("Skipping TAR symlink: %s", rel)
                    continue
                raise DownloadError(f"TAR contains a non-regular entry: {rel}")
            if member.size < 0 or member.size > max_extract:
                raise DownloadError(f"TAR entry exceeds extraction limit: {rel}")
            count += 1
            if count > max_files:
                raise DownloadError("TAR extracted file count exceeds limit.")
            src = tf.extractfile(member)
            if src is None:
                raise DownloadError(f"Unable to read archive member: {rel}")
            dest = stage.joinpath(*safe.parts)
            dest.parent.mkdir(parents=True, exist_ok=True)
            with src, dest.open("wb") as dst:
                written += _copy_bounded(src, dst, max_extract - written, rel)
    if count == 0:
        raise DownloadError(
            f"Requested folder not found in archive: {target.path or '(repository root)'}")
    return count, written


def _rollback(installed: Sequence[Path], backed_up: Sequence[tuple[Path, Path]]) -> None:
    for dst in reversed(installed):
        try:
            dst.unlink(missing_ok=True)
        except OSError:
            LOG.exception("Rollback could not remove %s", dst)
    for dst, backup in reversed(backed_up):
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup, dst)
        except OSError:
            LOG.exception("Rollback failed for %s", dst)


def commit_files(
    stage: Path, destination: Path, *,
    no_overwrite: bool,
    allow_destination_symlink: bool = False,
) -> int:
    """Per-file transactional commit; rolls back on any interruption."""
    files = sorted(p for p in stage.rglob("*") if p.is_file())
    installed: list[Path] = []
    backed_up: list[tuple[Path, Path]] = []
    # Backups live outside the staged-content namespace: a repository file may
    # legitimately be named ".rollback".
    with tempfile.TemporaryDirectory(prefix="gh-commit-backup-") as backup_tmp:
        backup_root = Path(backup_tmp)
        try:
            for src in files:
                rel = PurePosixPath(src.relative_to(stage).as_posix())
                dst = safe_destination_path(destination, rel,
                                            allow_root_symlink=allow_destination_symlink)
                if dst.exists():
                    if not dst.is_file():
                        raise CommitError(f"Destination conflict: {dst} is not a regular file.")
                    if no_overwrite:
                        raise CommitError(f"File exists and --no-overwrite is set: {dst}")
                    backup = backup_root / rel.as_posix()
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(dst, backup)
                    backed_up.append((dst, backup))
                dst.parent.mkdir(parents=True, exist_ok=True)
                tmp = dst.with_name(f"{dst.name}.tmp-download-{uuid.uuid4().hex[:8]}")
                shutil.copyfile(src, tmp)
                os.replace(tmp, dst)
                installed.append(dst)
        except BaseException:
            _rollback(installed, backed_up)
            raise
    return len(files)


def preserve_archive(
    archive: Path, destination: Path, name: str, *,
    no_overwrite: bool = False,
    allow_destination_symlink: bool = False,
) -> Path | None:
    destination.mkdir(parents=True, exist_ok=True)
    if not allow_destination_symlink and destination.is_symlink():
        raise CommitError(f"Destination root is a symlink: {destination}")
    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-") or "repository"
    if archive.name.endswith(".tar.gz"):
        suffix = ".tar.gz"
    else:
        suffix = archive.suffix or ".archive"
    dest = destination / f"{safe_name}-fallback{suffix}"
    if dest.is_symlink():
        raise CommitError(f"Refusing to preserve archive through symlink: {dest}")
    if no_overwrite and dest.exists():
        LOG.warning("Skipping archive preservation (--no-overwrite): %s", dest)
        return None
    fd, tmp_name = tempfile.mkstemp(dir=destination, prefix=".ghfd-archive-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh, archive.open("rb") as src:
            shutil.copyfileobj(src, fh, CHUNK)
        os.replace(tmp_name, dest)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise
    return dest


def download_with_archive_fallback(
    target: RepoTarget, destination: Path, *,
    timeout: float, token: str | None,
    max_download: int, max_extract: int,
    max_files: int, max_depth: int,
    keep_archive: bool, no_overwrite: bool,
    symlink_policy: str = "skip",
    allow_destination_symlink: bool = False,
    max_compression_ratio: int = DEFAULT_MAX_COMPRESSION_RATIO,
    retries: int = RETRY_ATTEMPTS,
    backoff_base: float = RETRY_BASE_DELAY,
) -> tuple[int, int, str]:
    errors: list[str] = []
    preserved: list[Path] = []
    destination.mkdir(parents=True, exist_ok=True)
    for fmt, url in archive_urls(target):
        with tempfile.TemporaryDirectory(prefix="gh-folder-") as tmp:
            tmpdir = Path(tmp)
            archive = tmpdir / f"repository.{fmt}"
            try:
                stream_to_file(url, archive, timeout=timeout, token=token,
                               max_size=max_download,
                               retries=retries, backoff_base=backoff_base)
            except DownloadError as exc:
                errors.append(f"{fmt} download: {exc}")
                LOG.warning("%s download failed: %s", fmt.upper(), exc)
                continue
            stage = tmpdir / "stage"
            stage.mkdir()
            try:
                if fmt == "zip":
                    count, size = extract_zip_target(
                        archive, stage, target, max_extract=max_extract,
                        max_files=max_files, max_depth=max_depth,
                        symlink_policy=symlink_policy,
                        max_compression_ratio=max_compression_ratio)
                else:
                    count, size = extract_tar_target(
                        archive, stage, target, max_extract=max_extract,
                        max_files=max_files, max_depth=max_depth,
                        symlink_policy=symlink_policy)
            except Exception as exc:
                errors.append(f"{fmt} extraction: {exc}")
                LOG.warning("%s extraction failed: %s", fmt.upper(), exc)
                try:
                    saved = preserve_archive(
                        archive, destination, archive_filename(target, fmt),
                        no_overwrite=no_overwrite,
                        allow_destination_symlink=allow_destination_symlink)
                    if saved is not None:
                        preserved.append(saved)
                        LOG.warning("Preserved archive for manual recovery: %s", saved)
                except OSError as save_exc:
                    errors.append(f"preservation failed: {save_exc}")
                continue
            # Commit failures are destination-side: no preservation, no second format.
            commit_files(stage, destination, no_overwrite=no_overwrite,
                         allow_destination_symlink=allow_destination_symlink)
            # Cleanup: drop recovery archives retained from earlier failed attempts.
            for old in preserved:
                try:
                    old.unlink(missing_ok=True)
                except OSError:
                    LOG.warning("Cleanup failed for %s", old)
            if keep_archive:
                saved = preserve_archive(
                    archive, destination, archive_filename(target, fmt),
                    no_overwrite=no_overwrite,
                    allow_destination_symlink=allow_destination_symlink)
                if saved is not None:
                    LOG.info("Retained archive: %s", saved)
            return count, size, fmt
    raise RetrievalError("Archive fallback failed: " + " | ".join(errors))


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download and mirror a GitHub repository folder without cloning the repository.",
        epilog=("Exit codes: 0 success, 1 unexpected, 2 usage, 3 ambiguous ref, "
                "4 URL, 5 resolve, 6 retrieve, 7 commit, 130 interrupted."))
    parser.add_argument("github_folder_url", help="HTTPS GitHub folder URL, or repository root URL")
    parser.add_argument("destination", help="Local destination directory")
    parser.add_argument("--ref", default=None,
                        help="Pin the branch/tag/commit ref; the rest of the URL tail is the folder path")
    parser.add_argument("--timeout", type=float, default=30.0,
                        help="Network operation timeout in seconds (default: 30)")
    parser.add_argument("--max-download-size", type=int, default=100,
                        help="Per-response/archive download cap in MiB (default: 100)")
    parser.add_argument("--max-extracted-size", type=int, default=250,
                        help="Total reconstructed content cap in MiB (default: 250)")
    parser.add_argument("--max-files", type=int, default=DEFAULT_MAX_FILES,
                        help=f"Maximum files to materialize (default: {DEFAULT_MAX_FILES})")
    parser.add_argument("--max-depth", type=int, default=DEFAULT_MAX_DEPTH,
                        help=f"Maximum path depth (default: {DEFAULT_MAX_DEPTH})")
    parser.add_argument("--max-compression-ratio", type=int, default=DEFAULT_MAX_COMPRESSION_RATIO,
                        help=("Reject ZIP entries whose uncompressed/compressed ratio exceeds this "
                              f"(default: {DEFAULT_MAX_COMPRESSION_RATIO}); only checked on entries "
                              f"above {COMPRESSION_RATIO_MIN_SIZE // MIB} MiB"))
    parser.add_argument("--symlink-policy", choices=("skip", "fail"), default="skip",
                        help="Symlink handling across all tiers (default: skip)")
    parser.add_argument("--keep-archive", action="store_true",
                        help="Retain the archive even after successful extraction")
    parser.add_argument("--no-overwrite", action="store_true",
                        help="Refuse to overwrite existing destination files")
    parser.add_argument("--allow-destination-symlink", action="store_true",
                        help="Permit the destination root itself to be a symlink")
    parser.add_argument("--retries", type=int, default=RETRY_ATTEMPTS,
                        help=f"HTTP retry attempts per request (default: {RETRY_ATTEMPTS})")
    parser.add_argument("--backoff-base", type=float, default=RETRY_BASE_DELAY,
                        help=f"Exponential backoff base in seconds (default: {RETRY_BASE_DELAY})")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--token-env", default="GITHUB_TOKEN",
                        help="Environment variable holding the GitHub token (default: GITHUB_TOKEN)")
    args = parser.parse_args(argv)
    if (args.timeout <= 0 or args.max_download_size <= 0 or args.max_extracted_size <= 0
            or args.max_files <= 0 or args.max_depth <= 0 or args.max_compression_ratio <= 0):
        parser.error("Timeout and all size/count/depth/ratio limits must be positive.")
    if args.retries < 0 or args.backoff_base < 0:
        parser.error("--retries and --backoff-base must be non-negative.")
    return args


def _run(args: argparse.Namespace) -> int:
    timeout: float = float(args.timeout)
    max_download: int = int(args.max_download_size) * MIB
    max_extract: int = int(args.max_extracted_size) * MIB
    max_files: int = int(args.max_files)
    max_depth: int = int(args.max_depth)
    max_ratio: int = int(args.max_compression_ratio)
    no_overwrite: bool = bool(args.no_overwrite)
    keep_archive: bool = bool(args.keep_archive)
    symlink_policy: str = str(args.symlink_policy)
    allow_dest_symlink: bool = bool(args.allow_destination_symlink)
    retries: int = int(args.retries)
    backoff_base: float = float(args.backoff_base)
    token_env: str = str(args.token_env)
    ref_override: str | None = str(args.ref) if args.ref else None

    dest_raw = Path(str(args.destination)).expanduser()
    if dest_raw.is_symlink() and not allow_dest_symlink:
        raise UsageError(
            f"Destination is a symlink; use --allow-destination-symlink to permit: {dest_raw}")
    try:
        destination = dest_raw.resolve()
    except OSError as exc:
        raise CommitError(f"Cannot resolve destination {dest_raw}: {exc}") from exc
    if destination.exists() and not destination.is_dir():
        raise UsageError(f"Destination exists but is not a directory: {destination}")

    token = os.environ.get(token_env) or None

    owner, repo, tail, kind = parse_url(str(args.github_folder_url))
    target = resolve_target(
        owner, repo, tail, kind,
        timeout=timeout, token=token, ref_override=ref_override,
        max_depth=max_depth, retries=retries, backoff_base=backoff_base)
    LOG.info("Resolved repository=%s/%s ref=%s path=%s commit=%s",
             target.owner, target.repo, target.ref,
             target.path or "(repository root)", target.commit_sha[:12])
    destination.mkdir(parents=True, exist_ok=True)

    primary_failed = False
    with tempfile.TemporaryDirectory(prefix="gh-folder-primary-") as tmp:
        stage = Path(tmp) / "stage"
        stage.mkdir()
        try:
            count, size = stage_api_folder(
                target, stage, timeout=timeout, token=token,
                max_download=max_download, max_files=max_files, max_depth=max_depth,
                max_extract=max_extract, symlink_policy=symlink_policy,
                retries=retries, backoff_base=backoff_base)
        except DownloadError as exc:
            LOG.warning("Primary retrieval failed: %s", exc)
            primary_failed = True
        else:
            # Commit is outside the staging handler: a destination conflict
            # must not trigger a whole-repository archive download.
            commit_files(stage, destination, no_overwrite=no_overwrite,
                         allow_destination_symlink=allow_dest_symlink)
            LOG.info("SUCCESS: %d file(s), %.2f MiB via GitHub API/raw retrieval.",
                     count, size / MIB)
            return EXIT_OK

    if primary_failed:
        count, size, fmt = download_with_archive_fallback(
            target, destination, timeout=timeout, token=token,
            max_download=max_download, max_extract=max_extract,
            max_files=max_files, max_depth=max_depth,
            keep_archive=keep_archive, no_overwrite=no_overwrite,
            symlink_policy=symlink_policy,
            allow_destination_symlink=allow_dest_symlink,
            max_compression_ratio=max_ratio,
            retries=retries, backoff_base=backoff_base)
        LOG.info("SUCCESS: %d file(s), %.2f MiB via %s archive fallback.",
                 count, size / MIB, fmt)
    return EXIT_OK


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(levelname)s: %(message)s")
    ensure_safe_opener()
    try:
        return _run(args)
    except AmbiguousRefError as exc:
        LOG.error("%s", exc)
        for interpretation in exc.interpretations:
            LOG.error("  possible: %s", interpretation)
        return EXIT_AMBIGUOUS
    except UsageError as exc:
        LOG.error("%s", exc)
        return EXIT_USAGE
    except URLParseError as exc:
        LOG.error("%s", exc)
        return EXIT_URL
    except ResolutionError as exc:
        LOG.error("%s", exc)
        return EXIT_RESOLVE
    except RetrievalError as exc:
        LOG.error("%s", exc)
        return EXIT_RETRIEVE
    except CommitError as exc:
        LOG.error("%s", exc)
        return EXIT_COMMIT
    except DownloadError as exc:
        LOG.error("%s", exc)
        return EXIT_FAILURE
    except OSError as exc:
        LOG.error("Filesystem error: %s", exc)
        return EXIT_COMMIT
    except KeyboardInterrupt:
        LOG.error("Interrupted.")
        return EXIT_INTERRUPTED
    except Exception:
        LOG.exception("Unexpected error.")
        return EXIT_FAILURE


if __name__ == "__main__":
    sys.exit(main())
