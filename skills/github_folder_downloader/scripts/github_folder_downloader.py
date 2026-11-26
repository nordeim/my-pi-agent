#!/usr/bin/env python3
# github_folder_downloader.py 
# version: 3.1
"""Download and mirror a GitHub repository folder without cloning the repository.

Usage
-----
  python github_folder_downloader.py URL DESTINATION [options]
  python github_folder_downloader.py URL DESTINATION --ref feature/x --json
  python github_folder_downloader.py --self-test

Retrieval tiers: (1) targeted GitHub API + raw, (2) repository ZIP, (3) TAR.GZ.

Safety model
------------
* HTTPS only. Redirects never downgrade TLS and never carry credentials to a
  different origin. A PRIVATE opener is used (no global urllib mutation).
* Every byte is bounded: per-response, per-file, aggregate, entry count,
  directory count, path depth, decompression work, and a global wall clock.
* Archive metadata is untrusted: ACTUAL written bytes are counted, not the
  sizes declared in headers.
* On POSIX a backslash is a legal filename character and is preserved in every
  tier (never silently turned into a directory boundary).
* Destination writes never follow symlinks. On POSIX the commit walks the
  destination with directory descriptors opened O_NOFOLLOW; elsewhere it falls
  back to lstat checks. Files are replaced atomically and rolled back on any
  interruption.
* Nothing downloaded is ever executed.

Exit codes (stable contract)
----------------------------
  0 success | 1 failure | 2 usage/destination | 3 ambiguous ref | 130 interrupted
--json emits a machine-readable summary that distinguishes failure classes
without changing this contract.

Known limitations (documented, not hidden)
------------------------------------------
* Git LFS payloads are not fetched: pointers are materialised and reported
  (--lfs fail turns this into an error). Submodules are never fetched.
* Downloads are sequential (rate-limit friendly); no resume/Range support.
* Committed files get mode 0644 (0755 when Git marks them executable);
  retained archives are written 0600.
* Empty directories present in the Git tree are recreated.

Requires Python 3.10+. Standard library only.
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
import secrets
import shutil
import ssl
import stat
import struct
import sys
import tarfile
import tempfile
import threading
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections.abc import Callable, Iterable, Mapping, Sequence
from contextlib import ExitStack
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import IO, Final, TypeVar, cast

__version__: Final = "3.1.0"

LOG: Final = logging.getLogger("github-folder-downloader")

USER_AGENT: Final = f"github-folder-downloader/{__version__} (Python urllib)"
API_BASE: Final = "https://api.github.com"
RAW_BASE: Final = "https://raw.githubusercontent.com"
CODELOAD_BASE: Final = "https://codeload.github.com"
API_VERSION: Final = "2022-11-28"

MIB: Final = 1024 * 1024
DEFAULT_MAX_DOWNLOAD: Final = 100 * MIB
DEFAULT_MAX_EXTRACT: Final = 250 * MIB
DEFAULT_MAX_FILES: Final = 5000
DEFAULT_MAX_DIRS: Final = 20000
DEFAULT_MAX_DEPTH: Final = 100
DEFAULT_DEADLINE: Final = 900.0
CHUNK: Final = 64 * 1024
API_JSON_LIMIT: Final = 10 * MIB
ERROR_BODY_LIMIT: Final = 1024
ERROR_DETAIL_LIMIT: Final = 300
MAX_RETRIES: Final = 10
RETRY_BASE_DELAY: Final = 0.5
RETRY_MAX_DELAY: Final = 8.0
RETRY_AFTER_CAP: Final = 60.0
RETRY_STATUS: Final = frozenset({429, 500, 502, 503, 504})
ARCHIVE_MAX_EXPANSION: Final = 100
TAR_HEADER_COST: Final = 512
MIN_ARCHIVE_ENTRIES: Final = 20000
MAX_ARCHIVE_ENTRIES: Final = 500000
ENTRY_CAP_FACTOR: Final = 10
RATIO_WARN_DEFAULT: Final = 1000
RATIO_MIN_SIZE: Final = MIB
SYMLINK_MODE: Final = "120000"
SUBMODULE_MODE: Final = "160000"
EXEC_MODE: Final = "100755"
LFS_PREFIX: Final = b"version https://git-lfs.github.com/spec/v1"
RETENTION_DIR: Final = ".ghfd-archives"
WINDOWS_ILLEGAL: Final = re.compile(r'[<>:"|?*\x00-\x1f]')
WINDOWS_RESERVED: Final = frozenset(
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{i}" for i in range(1, 10)}
    | {f"LPT{i}" for i in range(1, 10)}
)
OWNER_RE: Final = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$")
REPO_RE: Final = re.compile(r"^[A-Za-z0-9._-]{1,100}$")
HEX_SHA_RE: Final = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
CONTROL_CHARS: Final = re.compile(r"[\x00-\x1f\x7f]")
SPECIAL_ROOTS: Final = frozenset({"pax_global_header", "__MACOSX"})

IS_WINDOWS: Final = os.name == "nt"
EXIT_OK: Final = 0
EXIT_FAILURE: Final = 1
EXIT_USAGE: Final = 2
EXIT_AMBIGUOUS: Final = 3
EXIT_INTERRUPTED: Final = 130

T = TypeVar("T")


# --------------------------------------------------------------------------- #
# Errors                                                                       #
# --------------------------------------------------------------------------- #
class DownloadError(Exception):
    """Expected operational failure; optionally carries an HTTP status."""

    def __init__(self, message: str, *, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status


class UsageError(DownloadError):
    """Invalid CLI input or unusable destination."""


class URLParseError(DownloadError):
    """The supplied URL is not a supported GitHub folder URL."""


class ResolutionError(DownloadError):
    """The ref or folder could not be resolved."""


class AmbiguousRefError(ResolutionError):
    """Several ref/folder interpretations of one URL are valid."""

    def __init__(self, message: str, interpretations: Sequence[str]) -> None:
        super().__init__(message)
        self.interpretations = tuple(interpretations)


class RetrievalError(DownloadError):
    """Network or archive retrieval failed."""


class IntegrityError(DownloadError):
    """Content did not match its declared size or Git blob hash."""


class LimitExceeded(DownloadError):
    """A configured resource limit was reached."""


class DeadlineExceeded(LimitExceeded):
    """The global wall-clock budget was exhausted."""


class CommitError(DownloadError):
    """Destination-side failure; never triggers archive fallback."""


# --------------------------------------------------------------------------- #
# Small utilities                                                              #
# --------------------------------------------------------------------------- #
def safe_log(value: object, limit: int = 200) -> str:
    """Render a value for logs without allowing control-character injection."""
    text = str(value)
    if len(text) > limit:
        text = text[:limit] + "..."
    return CONTROL_CHARS.sub(lambda m: f"\\x{ord(m.group()):02x}", text)


def log_event(level: int, event: str, **fields: object) -> None:
    """Structured, injection-safe logging (event=key value ...)."""
    if fields:
        detail = " ".join(f"{k}={safe_log(v)}" for k, v in fields.items())
        LOG.log(level, "event=%s %s", event, detail)
    else:
        LOG.log(level, "event=%s", event)


class Deadline:
    """Monotonic wall-clock budget shared by every phase."""

    def __init__(self, seconds: float) -> None:
        self.seconds = float(seconds)
        self._end = time.monotonic() + float(seconds)

    def remaining(self) -> float:
        return self._end - time.monotonic()

    def check(self, phase: str) -> None:
        if self.remaining() <= 0:
            raise DeadlineExceeded(
                f"Global deadline of {self.seconds:.0f}s exceeded during {phase}. "
                "Raise --deadline or narrow the request.")

    def timeout(self, wanted: float) -> float:
        self.check("network")
        return max(0.001, min(wanted, self.remaining()))


@dataclass(frozen=True)
class Config:
    """Every tunable in one place (no long keyword chains across call sites)."""

    timeout: float = 30.0
    retries: int = 3
    backoff_base: float = RETRY_BASE_DELAY
    max_download: int = DEFAULT_MAX_DOWNLOAD
    max_extract: int = DEFAULT_MAX_EXTRACT
    max_files: int = DEFAULT_MAX_FILES
    max_dirs: int = DEFAULT_MAX_DIRS
    max_depth: int = DEFAULT_MAX_DEPTH
    max_archive_entries: int = 0
    ratio_warn: int = RATIO_WARN_DEFAULT
    symlink_policy: str = "skip"
    lfs_policy: str = "warn"
    no_overwrite: bool = False
    keep_archive: bool = False
    allow_destination_symlink: bool = False
    fsync: bool = False
    dry_run: bool = False
    token: str | None = None
    deadline: Deadline = field(default_factory=lambda: Deadline(DEFAULT_DEADLINE))

    @property
    def archive_entry_cap(self) -> int:
        if self.max_archive_entries > 0:
            return self.max_archive_entries
        return min(MAX_ARCHIVE_ENTRIES,
                   max(MIN_ARCHIVE_ENTRIES, ENTRY_CAP_FACTOR * self.max_files))


def encode_path(path: str) -> str:
    """Percent-encode each path component (slashes stay separators)."""
    return "/".join(urllib.parse.quote(part, safe="") for part in path.split("/") if part)


def git_blob_sha(data: bytes) -> str:
    """Git's content identifier (SHA-1 by Git's design, not a signature)."""
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def git_blob_sha_file(path: Path, size: int, *, sha256: bool = False) -> str:
    """Hash a staged file as a Git blob without holding it in memory."""
    hasher = hashlib.sha256() if sha256 else hashlib.sha1()
    hasher.update(b"blob " + str(size).encode("ascii") + b"\0")
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(CHUNK)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def is_lfs_pointer(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            return handle.read(len(LFS_PREFIX)) == LFS_PREFIX
    except OSError:
        return False


# --------------------------------------------------------------------------- #
# Path safety                                                                  #
# --------------------------------------------------------------------------- #
def safe_relpath(path: str) -> PurePosixPath:
    """Validate a repository/archive path and split it into materialisable parts.

    Structural checks use normalised separators so traversal, absolute, drive
    and UNC forms are rejected on every platform. Materialisation keeps the
    ORIGINAL separators: on POSIX a backslash is a legal filename character.
    """
    if not path or "\x00" in path:
        raise DownloadError(f"Unsafe or empty path: {safe_log(path)!r}")
    normalized = path.replace("\\", "/")
    probe = PurePosixPath(normalized)
    if probe.is_absolute() or ".." in probe.parts:
        raise DownloadError(f"Unsafe path (absolute or traversal): {safe_log(path)!r}")
    if re.match(r"^[A-Za-z]:", normalized) or normalized.startswith("//"):
        raise DownloadError(f"Unsafe path (drive or UNC): {safe_log(path)!r}")
    parts = tuple(p for p in path.split("/") if p not in ("", "."))
    if not parts:
        raise DownloadError(f"Unsafe or empty path: {safe_log(path)!r}")
    if IS_WINDOWS:
        for part in parts:
            stem = part.split(".")[0].upper()
            if ("\\" in part or WINDOWS_ILLEGAL.search(part)
                    or stem in WINDOWS_RESERVED or part.endswith((" ", "."))):
                raise DownloadError(f"Path component is not valid on Windows: {safe_log(part)!r}")
    return PurePosixPath(*parts)


def member_views(raw: str) -> tuple[str, str]:
    """Return (matching_view, original_view) with IDENTICAL character indices.

    Backslash->slash replacement is length preserving and leading './' is
    stripped from both views, so a prefix matched on the normalised view can be
    sliced off the original view without corrupting POSIX backslash filenames.
    """
    norm = raw.replace("\\", "/")
    start = 0
    while norm[start:start + 2] == "./":
        start += 2
    return norm[start:], raw[start:]


def collision_key(rel: str, *, fold: bool) -> tuple[str, ...]:
    parts = rel.split("/")
    if not fold:
        return tuple(parts)
    return tuple(unicodedata.normalize("NFC", p).casefold() for p in parts)


def detect_collisions(files: Iterable[str], dirs: Iterable[str], *, fold: bool) -> list[str]:
    """Detect case/normalisation collisions and file-vs-directory conflicts."""
    file_list = sorted(files)
    dir_list = sorted(dirs)
    seen: dict[tuple[str, ...], str] = {}
    problems: list[str] = []
    for rel in file_list + dir_list:
        key = collision_key(rel, fold=fold)
        if key in seen and seen[key] != rel:
            problems.append(f"{seen[key]!r} and {rel!r} collide on this filesystem")
        else:
            seen[key] = rel
    file_keys = {collision_key(rel, fold=fold) for rel in file_list}
    for rel in file_list:
        key = collision_key(rel, fold=fold)
        for depth in range(1, len(key)):
            prefix = key[:depth]
            if prefix in file_keys:
                problems.append(f"{rel!r} needs directory {seen[prefix]!r} which is a file")
    return problems


def filesystem_folds_case(directory: Path) -> bool:
    """Probe the destination filesystem (macOS/Windows fold case and NFC/NFD)."""
    probe = directory / ".ghfd-case-probe-a"
    twin = directory / ".ghfd-case-probe-A"
    try:
        fd = os.open(probe, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except OSError:
        return IS_WINDOWS
    os.close(fd)
    try:
        return twin.exists()
    finally:
        try:
            probe.unlink()
        except OSError:
            pass


# --------------------------------------------------------------------------- #
# HTTP layer                                                                   #
# --------------------------------------------------------------------------- #
class SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    """urllib copies request headers verbatim on redirect.

    Credentials must never cross origins and a redirect must never downgrade
    TLS. Same host but a different port is a different origin.
    """

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
            raise DownloadError(f"Refusing non-HTTPS redirect target for {safe_log(req.full_url)}")
        origin = urllib.parse.urlsplit(req.full_url)
        same_origin = ((target.hostname or "").lower() == (origin.hostname or "").lower()
                       and (target.port or 443) == (origin.port or 443))
        if not same_origin:
            for key in list(new_req.headers):
                if key.lower() == "authorization":
                    del new_req.headers[key]
            log_event(logging.DEBUG, "redirect_credentials_stripped",
                      host=target.hostname, code=code)
        return new_req


_OPENER: urllib.request.OpenerDirector | None = None
_OPENER_LOCK = threading.Lock()


def _build_opener() -> urllib.request.OpenerDirector:
    context = ssl.create_default_context()
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    try:
        context.minimum_version = ssl.TLSVersion.TLSv1_2
    except (AttributeError, ValueError):
        LOG.debug("event=tls_min_version_unavailable")
    return urllib.request.build_opener(
        SafeRedirectHandler(), urllib.request.HTTPSHandler(context=context))


def get_opener() -> urllib.request.OpenerDirector:
    """A PRIVATE opener: importing this module never mutates global urllib state."""
    global _OPENER
    with _OPENER_LOCK:
        if _OPENER is None:
            _OPENER = _build_opener()
        return _OPENER


def _open_request(req: urllib.request.Request, timeout: float) -> http.client.HTTPResponse:
    """Single network seam (tests patch this, not urllib globally)."""
    return cast(http.client.HTTPResponse, get_opener().open(req, timeout=timeout))


def retry_after_seconds(value: str | None) -> float | None:
    if not value:
        return None
    text = value.strip()
    try:
        seconds = float(text)
    except ValueError:
        pass
    else:
        if seconds != seconds or seconds in (float("inf"), float("-inf")):
            return None  # NaN / infinity are not usable hints
        return max(0.0, seconds)
    try:
        when = email.utils.parsedate_to_datetime(text)
    except (TypeError, ValueError):
        return None
    if when is None:
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=datetime.timezone.utc)
    return max(0.0, (when - datetime.datetime.now(datetime.timezone.utc)).total_seconds())


def backoff_delay(attempt: int, base: float) -> float:
    """Exponential backoff with full jitter, hard-capped."""
    ceiling = min(RETRY_MAX_DELAY, base * (2 ** max(0, attempt - 1)))
    return ceiling * (0.5 + random.random() / 2)


def _error_detail(exc: urllib.error.HTTPError) -> str:
    try:
        body = exc.read(ERROR_BODY_LIMIT)
    except (OSError, ValueError):
        return ""
    return body.decode("utf-8", "replace")[:ERROR_DETAIL_LIMIT]


def http_message(url: str, status: int, detail: str, headers: Mapping[str, str] | None) -> str:
    remaining = headers.get("X-RateLimit-Remaining") if headers is not None else None
    if status in (403, 429) and remaining == "0":
        reset = headers.get("X-RateLimit-Reset") if headers is not None else None
        return (f"GitHub API rate limit exceeded (HTTP {status}) for {url}"
                + (f"; quota resets at epoch {reset}" if reset else "")
                + ". Set a token via --token-env for a higher quota.")
    if status == 401:
        return f"HTTP 401 for {url}: authentication failed; check the token in --token-env."
    if status == 404:
        return f"HTTP 404 for {url}: not found (private repository, or wrong ref/path?)."
    return f"HTTP {status} for {url}: {detail}"


def check_content_length(value: str | None, limit: int | None, url: str) -> None:
    if limit is None or not value:
        return
    try:
        length = int(value)
    except ValueError:
        return
    if length > limit:
        raise LimitExceeded(f"Response exceeds size limit ({limit} bytes): {url}")


def _is_secondary_rate_limit(status: int, detail: str, headers: Mapping[str, str] | None) -> bool:
    if status != 403:
        return False
    if headers is not None and headers.get("Retry-After"):
        return True
    return "secondary rate limit" in detail.lower()


class Client:
    """Bounded, credential-safe HTTP with retries, jitter and a global deadline."""

    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg

    def _headers(self, accept: str) -> dict[str, str]:
        headers = {"User-Agent": USER_AGENT, "Accept": accept,
                   "X-GitHub-Api-Version": API_VERSION}
        if self.cfg.token:
            headers["Authorization"] = "Bearer " + self.cfg.token
        return headers

    def _perform(self, url: str, *, accept: str,
                 handle: Callable[[http.client.HTTPResponse], T]) -> T:
        if not url.lower().startswith("https://"):
            raise DownloadError("HTTPS is required for network requests.")
        cfg = self.cfg
        attempts = cfg.retries + 1  # --retries 0 means exactly one attempt
        headers = self._headers(accept)
        for attempt in range(1, attempts + 1):
            timeout = cfg.deadline.timeout(cfg.timeout)
            req = urllib.request.Request(url, headers=headers)
            try:
                with _open_request(req, timeout) as response:
                    return handle(response)
            except urllib.error.HTTPError as exc:
                status = exc.code
                detail = _error_detail(exc)
                resp_headers = exc.headers
                exc.close()
                retryable = (status in RETRY_STATUS
                             or _is_secondary_rate_limit(status, detail, resp_headers))
                if retryable and attempt < attempts:
                    hinted = retry_after_seconds(
                        resp_headers.get("Retry-After") if resp_headers else None)
                    if hinted is not None and hinted > RETRY_AFTER_CAP:
                        raise RetrievalError(
                            f"HTTP {status} for {url}: server asks to retry after {hinted:.0f}s "
                            f"(cap {RETRY_AFTER_CAP:.0f}s); retry later.", status=status) from exc
                    delay = hinted if hinted is not None else backoff_delay(attempt, cfg.backoff_base)
                    delay = min(delay, max(0.0, cfg.deadline.remaining()))
                    log_event(logging.WARNING, "http_retry", status=status, url=url,
                              attempt=f"{attempt + 1}/{attempts}", delay=f"{delay:.1f}s")
                    time.sleep(delay)
                    continue
                raise RetrievalError(
                    http_message(url, status, detail, resp_headers), status=status) from exc
            except ssl.SSLCertVerificationError as exc:
                raise RetrievalError(
                    f"TLS certificate verification failed for {url}: {exc}") from exc
            except (urllib.error.URLError, TimeoutError, ConnectionError,
                    http.client.IncompleteRead, ssl.SSLError) as exc:
                if attempt < attempts:
                    delay = min(backoff_delay(attempt, cfg.backoff_base),
                                max(0.0, cfg.deadline.remaining()))
                    log_event(logging.WARNING, "network_retry", url=url, error=exc,
                              attempt=f"{attempt + 1}/{attempts}", delay=f"{delay:.1f}s")
                    time.sleep(delay)
                    continue
                raise RetrievalError(f"Network error for {url}: {exc}") from exc
        raise RetrievalError(f"Request failed after {attempts} attempts: {url}")

    def read_bytes(self, url: str, *, limit: int | None = None,
                   accept: str = "application/vnd.github+json") -> bytes:
        def handle(response: http.client.HTTPResponse) -> bytes:
            check_content_length(response.headers.get("Content-Length"), limit, url)
            chunks: list[bytes] = []
            total = 0
            while True:
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                total += len(chunk)
                if limit is not None and total > limit:
                    raise LimitExceeded(f"Response exceeds size limit ({limit} bytes): {url}")
                chunks.append(chunk)
            return b"".join(chunks)

        return self._perform(url, accept=accept, handle=handle)

    def json(self, url: str) -> object:
        payload = self.read_bytes(url, limit=API_JSON_LIMIT)
        try:
            return json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RetrievalError(f"Invalid JSON response from GitHub API: {url}") from exc

    def download_to(self, url: str, out: Path, *, max_size: int,
                    accept: str = "application/octet-stream") -> int:
        """Stream to disk (never buffer a whole file in memory)."""
        def handle(response: http.client.HTTPResponse) -> int:
            check_content_length(response.headers.get("Content-Length"), max_size, url)
            total = 0
            with out.open("wb") as fh:
                while True:
                    chunk = response.read(CHUNK)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > max_size:
                        raise LimitExceeded(
                            f"Download exceeds configured limit ({max_size} bytes): {url}")
                    fh.write(chunk)
            return total

        try:
            return self._perform(url, accept=accept, handle=handle)
        except BaseException:
            out.unlink(missing_ok=True)  # a partial download is never an artifact
            raise


def json_object(value: object, context: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise RetrievalError(f"Unexpected GitHub API response ({context}): expected an object.")
    return {str(k): v for k, v in value.items()}


def json_list(value: object, context: str) -> list[object]:
    if not isinstance(value, list):
        raise RetrievalError(f"Unexpected GitHub API response ({context}): expected a list.")
    return list(value)


def string_field(obj: Mapping[str, object], key: str, context: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value:
        raise RetrievalError(f"Unexpected GitHub API response ({context}): missing string '{key}'.")
    return value


# --------------------------------------------------------------------------- #
# URL parsing                                                                  #
# --------------------------------------------------------------------------- #
def parse_url(url: str) -> tuple[str, str, list[str], str]:
    """Parse a github.com URL into (owner, repo, tail, kind).

    Supported: repository root, /tree/REF (whole repo at REF) and /tree/REF/PATH.
    Slashes inside a ref are resolved by trying every split, never by guessing.
    """
    try:
        parsed = urllib.parse.urlsplit(url)
    except ValueError as exc:
        raise URLParseError(f"Invalid URL: {exc}") from exc
    if parsed.scheme != "https" or (parsed.hostname or "").lower() != "github.com":
        raise URLParseError("Expected an HTTPS github.com URL.")
    if parsed.username or parsed.password:
        raise URLParseError("URL must not contain credentials.")
    if parsed.query or parsed.fragment:
        raise URLParseError("Query strings and fragments are not supported in folder URLs.")
    parts = [urllib.parse.unquote(p) for p in parsed.path.split("/") if p]
    for segment in parts:
        if "/" in segment or "\x00" in segment:
            raise URLParseError("Encoded separators or NUL bytes are not allowed in URL segments.")
    if len(parts) < 2:
        raise URLParseError("URL must include OWNER and REPO.")
    owner, repo = parts[0], parts[1]
    if repo.endswith(".git"):
        repo = repo[:-4]
    if owner in (".", "..") or repo in (".", ".."):
        raise URLParseError("Invalid owner or repository name.")
    if not OWNER_RE.match(owner):
        raise URLParseError(f"Invalid GitHub owner: {safe_log(owner)!r}")
    if not REPO_RE.match(repo):
        raise URLParseError(f"Invalid GitHub repository name: {safe_log(repo)!r}")
    if len(parts) == 2:
        return owner, repo, [], "root"
    if parts[2] != "tree" or len(parts) < 4:
        raise URLParseError(
            "Expected https://github.com/OWNER/REPO, .../tree/REF or .../tree/REF/PATH.")
    return owner, repo, parts[3:], "tree"


# --------------------------------------------------------------------------- #
# Resolution                                                                   #
# --------------------------------------------------------------------------- #
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


def tree_entry(item: object) -> TreeEntry:
    obj = json_object(item, "tree entry")
    size, mode = obj.get("size", 0), obj.get("mode", "")
    return TreeEntry(
        path=string_field(obj, "path", "tree entry"),
        kind=string_field(obj, "type", "tree entry"),
        sha=string_field(obj, "sha", "tree entry"),
        size=size if isinstance(size, int) and size >= 0 else 0,
        mode=mode if isinstance(mode, str) else "")


def repo_api(client: Client, owner: str, repo: str) -> str:
    return f"{API_BASE}/repos/{encode_path(owner)}/{encode_path(repo)}"


def default_branch(client: Client, owner: str, repo: str) -> str:
    data = json_object(client.json(repo_api(client, owner, repo)), "repository")
    return string_field(data, "default_branch", "repository")


def commit_for_ref(client: Client, owner: str, repo: str, ref: str) -> tuple[str, str] | None:
    """Return (commit_sha, root_tree_sha); None ONLY when the ref does not exist."""
    url = f"{repo_api(client, owner, repo)}/commits/{encode_path(ref)}"
    try:
        data = json_object(client.json(url), "commit")
    except DownloadError as exc:
        if exc.status == 404:
            return None
        raise  # rate limits, auth and server faults must not masquerade as a miss
    sha = string_field(data, "sha", "commit")
    body = json_object(data.get("commit"), "commit body")
    tree = json_object(body.get("tree"), "commit tree")
    return sha, string_field(tree, "sha", "commit tree")


class TreeCache:
    """Per-tree listings, cached, and NEVER silently truncated."""

    def __init__(self, client: Client, owner: str, repo: str) -> None:
        self.client = client
        self.owner = owner
        self.repo = repo
        self._trees: dict[str, list[TreeEntry]] = {}

    def listing(self, tree_sha: str) -> list[TreeEntry]:
        cached = self._trees.get(tree_sha)
        if cached is not None:
            return cached
        url = f"{repo_api(self.client, self.owner, self.repo)}/git/trees/{encode_path(tree_sha)}"
        data = json_object(self.client.json(url), "tree")
        if data.get("truncated") is True:
            raise RetrievalError(
                f"GitHub returned a TRUNCATED listing for directory tree {tree_sha}. "
                "Refusing to mirror an incomplete folder; narrow the path or retry later.")
        entries = [tree_entry(item) for item in json_list(data.get("tree"), "tree entries")]
        self._trees[tree_sha] = entries
        return entries


def subtree_sha(cache: TreeCache, root_tree: str, path: str, *, max_depth: int) -> str | None:
    """Walk only the path components: O(depth) calls, never the whole repo."""
    if not path:
        return root_tree
    parts = [p for p in path.split("/") if p]
    if len(parts) > max_depth:
        raise LimitExceeded(f"Folder depth exceeds configured limit ({max_depth}).")
    current = root_tree
    for part in parts:
        match = next((e for e in cache.listing(current) if e.path == part and e.kind == "tree"), None)
        if match is None:
            return None
        current = match.sha
    return current


def recursive_subtree(cache: TreeCache, tree_sha: str) -> list[TreeEntry] | None:
    url = (f"{repo_api(cache.client, cache.owner, cache.repo)}"
           f"/git/trees/{encode_path(tree_sha)}?recursive=1")
    data = json_object(cache.client.json(url), "recursive tree")
    if data.get("truncated") is True:
        return None
    return [tree_entry(item) for item in json_list(data.get("tree"), "recursive tree")]


def walk_subtree(cache: TreeCache, tree_sha: str, cfg: Config) -> list[TreeEntry]:
    """Iterative subtree walk used when the recursive listing is truncated."""
    out: list[TreeEntry] = []
    stack: list[tuple[str, str]] = [(tree_sha, "")]
    files = dirs = 0
    while stack:
        cache.client.cfg.deadline.check("tree walk")
        sha, prefix = stack.pop()
        for entry in cache.listing(sha):
            rel = f"{prefix}/{entry.path}" if prefix else entry.path
            if len(PurePosixPath(rel).parts) > cfg.max_depth:
                raise LimitExceeded(f"Folder depth exceeds configured limit ({cfg.max_depth}).")
            if entry.kind == "tree":
                dirs += 1
                if dirs > cfg.max_dirs:
                    raise LimitExceeded(f"Folder contains more than {cfg.max_dirs} directories.")
                out.append(TreeEntry(rel, "tree", entry.sha, 0, entry.mode))
                stack.append((entry.sha, rel))
                continue
            if entry.kind == "blob" and entry.mode != SYMLINK_MODE:
                files += 1
                if files > cfg.max_files:
                    raise LimitExceeded(f"Folder contains more than {cfg.max_files} files.")
            out.append(TreeEntry(rel, entry.kind, entry.sha, entry.size, entry.mode))
    return out


def fetch_folder_entries(cache: TreeCache, tree_sha: str, cfg: Config) -> list[TreeEntry]:
    recursive = recursive_subtree(cache, tree_sha)
    if recursive is None:
        log_event(logging.INFO, "tree_truncated_fallback", tree=tree_sha)
        return walk_subtree(cache, tree_sha, cfg)
    files = dirs = 0
    for entry in recursive:
        if len(PurePosixPath(entry.path).parts) > cfg.max_depth:
            raise LimitExceeded(f"Folder depth exceeds configured limit ({cfg.max_depth}).")
        if entry.kind == "tree":
            dirs += 1
        elif entry.kind == "blob" and entry.mode != SYMLINK_MODE:
            files += 1
    if files > cfg.max_files:
        raise LimitExceeded(f"Folder contains more than {cfg.max_files} files.")
    if dirs > cfg.max_dirs:
        raise LimitExceeded(f"Folder contains more than {cfg.max_dirs} directories.")
    return recursive


def resolve_target(client: Client, owner: str, repo: str, tail: list[str], kind: str, *,
                   cfg: Config, ref_override: str | None = None,
                   path_override: str | None = None) -> RepoTarget:
    """Resolve ref/path without guessing. Ambiguity is a first-class outcome."""
    cache = TreeCache(client, owner, repo)
    if path_override is not None and ref_override is None:
        raise UsageError("--path requires --ref.")

    if ref_override is not None or kind == "root":
        ref = ref_override if ref_override is not None else default_branch(client, owner, repo)
        resolved = commit_for_ref(client, owner, repo, ref)
        if resolved is None:
            raise ResolutionError(f"Ref not found: {safe_log(ref)}")
        sha, tree = resolved
        if path_override is not None:
            path = path_override.strip("/")
        else:
            path = "/".join(tail) if kind != "root" else ""
        subtree = subtree_sha(cache, tree, path, max_depth=cfg.max_depth)
        if subtree is None:
            raise ResolutionError(
                f"Folder not found at ref {safe_log(ref)}: {safe_log(path or '(repository root)')}")
        return RepoTarget(owner, repo, ref, path, sha, tree, subtree)

    matches: list[RepoTarget] = []
    for split in range(len(tail), 0, -1):
        client.cfg.deadline.check("resolution")
        ref, path = "/".join(tail[:split]), "/".join(tail[split:])
        resolved = commit_for_ref(client, owner, repo, ref)
        if resolved is None:
            continue
        sha, tree = resolved
        subtree = subtree_sha(cache, tree, path, max_depth=cfg.max_depth)
        if subtree is None:
            continue
        matches.append(RepoTarget(owner, repo, ref, path, sha, tree, subtree))
        # Shorter candidates are still examined: silently taking the longest
        # match could mirror the wrong folder.
    if not matches:
        raise ResolutionError(
            "Could not resolve the URL ref and folder path. Check the URL; if the branch "
            "name contains slashes, re-run with --ref.")
    if len(matches) > 1:
        raise AmbiguousRefError(
            "Ambiguous URL: multiple ref/folder interpretations exist. Re-run with --ref:",
            [f"--ref {m.ref}  (folder: {m.path or '(repository root)'})" for m in matches])
    return matches[0]


# --------------------------------------------------------------------------- #
# Staging (API tier)                                                           #
# --------------------------------------------------------------------------- #
@dataclass
class StageResult:
    files: int = 0
    directories: int = 0
    bytes: int = 0
    skipped_symlinks: int = 0
    skipped_submodules: int = 0
    lfs_pointers: int = 0
    deduplicated: int = 0


def materialise_path(stage: Path, rel: str, cfg: Config) -> Path:
    safe = safe_relpath(rel)
    if len(safe.parts) > cfg.max_depth:
        raise LimitExceeded(f"Folder depth exceeds configured limit ({cfg.max_depth}).")
    dest = stage.joinpath(*safe.parts)
    dest.parent.mkdir(parents=True, exist_ok=True)
    return dest


def make_empty_dirs(stage: Path, dirs: Iterable[str], cfg: Config) -> int:
    count = 0
    for rel in sorted(set(dirs)):
        safe = safe_relpath(rel)
        if len(safe.parts) > cfg.max_depth:
            raise LimitExceeded(f"Folder depth exceeds configured limit ({cfg.max_depth}).")
        stage.joinpath(*safe.parts).mkdir(parents=True, exist_ok=True)
        count += 1
    if count > cfg.max_dirs:
        raise LimitExceeded(f"Folder contains more than {cfg.max_dirs} directories.")
    return count


def verify_staged_file(entry_path: str, staged: Path, size: int, expected_sha: str) -> None:
    if not expected_sha:
        return
    if HEX_SHA_RE.match(expected_sha) is None:
        log_event(logging.WARNING, "unverifiable_blob_sha", path=entry_path)
        return
    actual = git_blob_sha_file(staged, size, sha256=len(expected_sha) == 64)
    if actual != expected_sha:
        raise IntegrityError(
            f"Integrity check failed for {safe_log(entry_path)}: Git blob hash mismatch.")


def stage_api_folder(client: Client, target: RepoTarget, stage: Path, cfg: Config) -> StageResult:
    cache = TreeCache(client, target.owner, target.repo)
    subtree = target.subtree_sha or subtree_sha(cache, target.tree_sha, target.path,
                                                max_depth=cfg.max_depth)
    if subtree is None:
        raise ResolutionError(
            f"Target folder not found: {safe_log(target.path or '(repository root)')}")
    entries = fetch_folder_entries(cache, subtree, cfg)
    result = StageResult()
    files: list[TreeEntry] = []
    dirs: list[str] = []
    for entry in entries:
        if entry.kind == "tree":
            dirs.append(entry.path)
        elif entry.kind == "commit" or entry.mode == SUBMODULE_MODE:
            result.skipped_submodules += 1
            log_event(logging.WARNING, "skipped_submodule", path=entry.path)
        elif entry.kind == "blob" and entry.mode == SYMLINK_MODE:
            if cfg.symlink_policy == "fail":
                raise DownloadError(
                    f"Symlink entry not supported (--symlink-policy fail): {safe_log(entry.path)}")
            result.skipped_symlinks += 1
            log_event(logging.WARNING, "skipped_symlink", path=entry.path)
        elif entry.kind == "blob":
            files.append(entry)
    if not files:
        raise DownloadError(
            f"No regular files found in the requested folder: "
            f"{safe_log(target.path or '(repository root)')} "
            f"(skipped {result.skipped_symlinks} symlink(s), "
            f"{result.skipped_submodules} submodule(s)).")
    result.directories = make_empty_dirs(stage, dirs, cfg)

    seen: dict[str, tuple[Path, int]] = {}
    for entry in files:
        cfg.deadline.check("download")
        if entry.size > cfg.max_download:
            raise LimitExceeded(f"File exceeds per-download limit: {safe_log(entry.path)}")
        dest = materialise_path(stage, entry.path, cfg)
        cached = seen.get(entry.sha) if entry.sha else None
        if cached is not None and cached[0].exists():
            shutil.copyfile(cached[0], dest)
            size = cached[1]
            result.deduplicated += 1
        else:
            # Tree listings are SUBTREE-relative; raw URLs need the FULL repo path.
            full_path = f"{target.path}/{entry.path}" if target.path else entry.path
            url = (f"{RAW_BASE}/{encode_path(target.owner)}/{encode_path(target.repo)}"
                   f"/{encode_path(target.commit_sha)}/{encode_path(full_path)}")
            size = client.download_to(url, dest, max_size=cfg.max_download)
            if entry.size and size != entry.size:
                raise IntegrityError(
                    f"Size mismatch for {safe_log(entry.path)}: expected {entry.size}, got {size}.")
            verify_staged_file(entry.path, dest, size, entry.sha)
            if entry.sha:
                seen[entry.sha] = (dest, size)
        result.bytes += size
        if result.bytes > cfg.max_extract:
            raise LimitExceeded(f"Folder exceeds extracted-size limit ({cfg.max_extract} bytes).")
        if is_lfs_pointer(dest):
            result.lfs_pointers += 1
            if cfg.lfs_policy == "fail":
                raise DownloadError(
                    f"Git LFS pointer, payload not fetched (--lfs fail): {safe_log(entry.path)}")
            log_event(logging.WARNING, "git_lfs_pointer", path=entry.path,
                      note="pointer committed, payload not fetched")
        os.chmod(dest, 0o755 if entry.mode == EXEC_MODE else 0o644)
        result.files += 1
    return result


# --------------------------------------------------------------------------- #
# Archive tiers                                                                #
# --------------------------------------------------------------------------- #
def archive_urls(target: RepoTarget) -> list[tuple[str, str]]:
    if HEX_SHA_RE.match(target.commit_sha) is None:
        raise DownloadError("Refusing to build archive URLs from an unvalidated commit SHA.")
    owner, repo = encode_path(target.owner), encode_path(target.repo)
    commit = urllib.parse.quote(target.commit_sha, safe="")
    return [("zip", f"{CODELOAD_BASE}/{owner}/{repo}/zip/{commit}"),
            ("tar.gz", f"{CODELOAD_BASE}/{owner}/{repo}/tar.gz/{commit}")]


def archive_root(members: Iterable[str]) -> str:
    roots: set[str] = set()
    for name in members:
        norm, _ = member_views(name)
        head = norm.split("/", 1)[0]
        if head and head not in SPECIAL_ROOTS:
            roots.add(head)
    if len(roots) != 1:
        raise DownloadError(f"Archive has an unexpected root structure: {sorted(roots)[:5]!r}")
    return next(iter(roots))


def copy_bounded(src: IO[bytes], dst: IO[bytes], budget: int, label: str) -> int:
    """Count ACTUAL bytes written; archive headers are untrusted declarations."""
    total = 0
    while True:
        chunk = src.read(CHUNK)
        if not chunk:
            break
        total += len(chunk)
        if total > budget:
            raise LimitExceeded(
                f"Extracted content exceeds size limit while reading {safe_log(label)}")
        dst.write(chunk)
    return total


def eocd_entry_count(archive: Path) -> int | None:
    """Read the ZIP end-of-central-directory record to bound memory BEFORE infolist()."""
    size = archive.stat().st_size
    if size < 22:
        return None
    tail_len = min(size, 65557 + 22)
    with archive.open("rb") as handle:
        handle.seek(size - tail_len)
        tail = handle.read(tail_len)
    idx = tail.rfind(b"PK\x05\x06")
    if idx < 0 or len(tail) - idx < 22:
        return None
    record = struct.unpack("<4s4H2LH", tail[idx:idx + 22])
    if idx + 22 + record[7] != len(tail):
        return None
    total = record[4]
    if total == 0xFFFF:
        return None  # ZIP64: fall back to the (download-bounded) central directory
    return int(total)


def _reject_duplicate(seen: set[str], rel: str) -> None:
    if rel in seen:
        raise DownloadError(f"Archive contains a duplicate entry: {safe_log(rel)}")
    seen.add(rel)


def _handle_non_regular(kind: str, rel: str, cfg: Config, result: StageResult) -> bool:
    """Return True when the entry was skipped; raise when it must be refused."""
    if kind in ("symlink", "hardlink"):
        if cfg.symlink_policy == "fail":
            raise DownloadError(
                f"Archive {kind} not supported (--symlink-policy fail): {safe_log(rel)}")
        result.skipped_symlinks += 1
        log_event(logging.WARNING, "skipped_archive_link", kind=kind, path=rel)
        return True
    raise DownloadError(f"Archive contains a non-regular entry ({kind}): {safe_log(rel)}")


def _finalise_staged(dest: Path, rel: str, executable: bool, cfg: Config,
                     result: StageResult) -> None:
    if is_lfs_pointer(dest):
        result.lfs_pointers += 1
        if cfg.lfs_policy == "fail":
            raise DownloadError(
                f"Git LFS pointer, payload not fetched (--lfs fail): {safe_log(rel)}")
        log_event(logging.WARNING, "git_lfs_pointer", path=rel,
                  note="pointer committed, payload not fetched")
    os.chmod(dest, 0o755 if executable else 0o644)


def extract_zip_target(archive: Path, stage: Path, target: RepoTarget, cfg: Config) -> StageResult:
    result = StageResult()
    cap = cfg.archive_entry_cap
    declared_count = eocd_entry_count(archive)
    if declared_count is not None and declared_count > cap:
        raise LimitExceeded(f"Archive contains too many entries ({declared_count} > {cap}).")
    with zipfile.ZipFile(archive) as zf:
        infos = zf.infolist()
        if len(infos) > cap:
            raise LimitExceeded(f"Archive contains too many entries ({len(infos)} > {cap}).")
        marker = archive_root(i.filename for i in infos)
        if target.path:
            marker += "/" + target.path.strip("/")
        marker += "/"
        selected: list[tuple[zipfile.ZipInfo, str]] = []
        dirs: list[str] = []
        seen: set[str] = set()
        declared = 0
        for info in infos:
            cfg.deadline.check("zip scan")
            norm, original = member_views(info.filename)
            if not norm.startswith(marker):
                continue
            rel = original[len(marker):]
            if not rel:
                continue
            safe_relpath(rel)
            if info.is_dir():
                dirs.append(rel.rstrip("/"))
                continue
            mode = (info.external_attr >> 16) & 0xFFFF
            file_type = stat.S_IFMT(mode) if mode else 0
            if file_type not in (0, stat.S_IFREG):
                kind = "symlink" if file_type == stat.S_IFLNK else "special"
                if _handle_non_regular(kind, rel, cfg, result):
                    continue
            if info.file_size < 0 or info.file_size > cfg.max_extract:
                raise LimitExceeded(f"ZIP entry exceeds extraction limit: {safe_log(rel)}")
            if (cfg.ratio_warn > 0 and info.file_size > RATIO_MIN_SIZE and info.compress_size > 0
                    and info.file_size / info.compress_size > cfg.ratio_warn):
                log_event(logging.WARNING, "high_compression_ratio", path=rel,
                          ratio=f"{info.file_size / info.compress_size:.0f}",
                          note="advisory only; actual bytes are bounded")
            declared += info.file_size
            if declared > cfg.max_extract:
                raise LimitExceeded("ZIP extracted content exceeds size limit.")
            _reject_duplicate(seen, rel)
            selected.append((info, rel))
        if not selected:
            raise DownloadError(
                f"Requested folder not found in ZIP archive: "
                f"{safe_log(target.path or '(repository root)')}")
        if len(selected) > cfg.max_files:
            raise LimitExceeded("ZIP extracted file count exceeds limit.")
        result.directories = make_empty_dirs(stage, dirs, cfg)
        for info, rel in selected:
            cfg.deadline.check("zip extract")
            dest = materialise_path(stage, rel, cfg)
            with zf.open(info) as src, dest.open("wb") as dst:
                result.bytes += copy_bounded(src, dst, cfg.max_extract - result.bytes, rel)
            _finalise_staged(dest, rel, bool((info.external_attr >> 16) & 0o111), cfg, result)
            result.files += 1
    return result


def extract_tar_target(archive: Path, stage: Path, target: RepoTarget, cfg: Config) -> StageResult:
    """Single streaming pass; decompression WORK is bounded, not just output."""
    result = StageResult()
    cap = cfg.archive_entry_cap
    scan_budget = max(cfg.max_extract, ARCHIVE_MAX_EXPANSION * archive.stat().st_size)
    root: str | None = None
    marker = ""
    scanned = entries = declared = 0
    dirs: list[str] = []
    seen: set[str] = set()
    with tarfile.open(archive, "r|gz") as tf:
        for member in tf:
            cfg.deadline.check("tar scan")
            entries += 1
            if entries > cap:
                raise LimitExceeded(f"Archive contains too many entries (> {cap}).")
            scanned += max(0, member.size) + TAR_HEADER_COST
            if scanned > scan_budget:
                raise LimitExceeded(
                    f"Archive expansion exceeds the safe scan budget ({scan_budget} bytes); "
                    "refusing to decompress further.")
            norm, original = member_views(member.name)
            if not norm:
                continue
            head = norm.split("/", 1)[0]
            if head in SPECIAL_ROOTS:
                continue
            if root is None:
                root = head
                marker = root + ("/" + target.path.strip("/") if target.path else "") + "/"
            elif head != root:
                raise DownloadError("Archive has an unexpected root structure.")
            if not norm.startswith(marker):
                continue
            rel = original[len(marker):]
            if not rel:
                continue
            safe_relpath(rel)
            if member.isdir():
                dirs.append(rel.rstrip("/"))
                continue
            if not member.isfile():
                kind = "symlink" if member.issym() else "hardlink" if member.islnk() else "special"
                if _handle_non_regular(kind, rel, cfg, result):
                    continue
            if member.size < 0 or member.size > cfg.max_extract:
                raise LimitExceeded(f"TAR entry exceeds extraction limit: {safe_log(rel)}")
            declared += member.size
            if declared > cfg.max_extract:
                raise LimitExceeded("TAR extracted content exceeds size limit.")
            _reject_duplicate(seen, rel)
            result.files += 1
            if result.files > cfg.max_files:
                raise LimitExceeded("TAR extracted file count exceeds limit.")
            src = tf.extractfile(member)
            if src is None:
                raise DownloadError(f"Unable to read archive member: {safe_log(rel)}")
            dest = materialise_path(stage, rel, cfg)
            with src, dest.open("wb") as dst:
                result.bytes += copy_bounded(src, dst, cfg.max_extract - result.bytes, rel)
            _finalise_staged(dest, rel, bool(member.mode & 0o111), cfg, result)
    if result.files == 0:
        raise DownloadError(
            f"Requested folder not found in TAR archive: "
            f"{safe_log(target.path or '(repository root)')}")
    result.directories = make_empty_dirs(stage, dirs, cfg)
    return result


# --------------------------------------------------------------------------- #
# Destination commit (no-follow, atomic, transactional)                        #
# --------------------------------------------------------------------------- #
_DIR_FD_OK: bool | None = None


def _probe_dir_fd() -> bool:
    """Observe real behaviour instead of trusting os.supports_dir_fd membership."""
    if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        return False
    try:
        with tempfile.TemporaryDirectory(prefix="ghfd-probe-") as tmp:
            fd = os.open(tmp, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            try:
                os.mkdir("d", dir_fd=fd)
                sub = os.open("d", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                try:
                    handle = os.open("a", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                                     0o600, dir_fd=sub)
                    os.close(handle)
                    os.stat("a", dir_fd=sub, follow_symlinks=False)
                    os.chmod("a", 0o644, dir_fd=sub)
                    os.replace("a", "b", src_dir_fd=sub, dst_dir_fd=sub)
                    os.unlink("b", dir_fd=sub)
                finally:
                    os.close(sub)
            finally:
                os.close(fd)
        return True
    except (OSError, NotImplementedError, AttributeError):
        return False


def dir_fd_supported() -> bool:
    global _DIR_FD_OK
    if _DIR_FD_OK is None:
        _DIR_FD_OK = _probe_dir_fd()
    return _DIR_FD_OK


class DirHandle:
    """A directory reference that never follows symlinks when descending.

    POSIX uses directory descriptors (race-free against symlink swaps); other
    platforms fall back to path operations guarded by lstat checks.
    """

    __slots__ = ("fd", "path")

    def __init__(self, fd: int | None, path: Path) -> None:
        self.fd = fd
        self.path = path

    def close(self) -> None:
        if self.fd is not None:
            try:
                os.close(self.fd)
            except OSError:
                pass
            self.fd = None

    def stat(self, name: str) -> os.stat_result | None:
        try:
            if self.fd is None:
                return (self.path / name).lstat()
            return os.stat(name, dir_fd=self.fd, follow_symlinks=False)
        except FileNotFoundError:
            return None

    def mkdir(self, name: str) -> None:
        if self.fd is None:
            (self.path / name).mkdir()
        else:
            os.mkdir(name, dir_fd=self.fd)

    def open_dir(self, name: str) -> DirHandle:
        child = self.path / name
        if self.fd is None:
            return DirHandle(None, child)
        return DirHandle(os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                 dir_fd=self.fd), child)

    def open_read(self, name: str) -> int:
        if self.fd is None:
            return os.open(self.path / name, os.O_RDONLY | os.O_NOFOLLOW)
        return os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=self.fd)

    def create_tmp(self, name: str) -> int:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
        if self.fd is None:
            return os.open(self.path / name, flags, 0o600)
        return os.open(name, flags, 0o600, dir_fd=self.fd)

    def chmod(self, name: str, mode: int) -> None:
        if self.fd is None:
            os.chmod(self.path / name, mode)
        else:
            os.chmod(name, mode, dir_fd=self.fd)

    def replace(self, src: str, dst: str) -> None:
        if self.fd is None:
            os.replace(self.path / src, self.path / dst)
        else:
            os.replace(src, dst, src_dir_fd=self.fd, dst_dir_fd=self.fd)

    def unlink(self, name: str, *, missing_ok: bool = False) -> None:
        try:
            if self.fd is None:
                (self.path / name).unlink()
            else:
                os.unlink(name, dir_fd=self.fd)
        except FileNotFoundError:
            if not missing_ok:
                raise


def open_root(directory: Path, *, allow_symlink: bool) -> DirHandle:
    st = directory.lstat()
    if stat.S_ISLNK(st.st_mode):
        if not allow_symlink:
            raise CommitError(
                f"Destination root is a symlink: {directory}. "
                "Use --allow-destination-symlink to permit this explicitly.")
        st = directory.stat()  # explicitly permitted: follow the root link only
    if not stat.S_ISDIR(st.st_mode):
        raise CommitError(f"Destination is not a directory: {directory}")
    if not dir_fd_supported():
        return DirHandle(None, directory)
    flags = os.O_RDONLY | os.O_DIRECTORY
    if not allow_symlink:
        flags |= os.O_NOFOLLOW
    return DirHandle(os.open(directory, flags), directory)


def descend(root: DirHandle, parts: Sequence[str], created: list[Path]) -> DirHandle:
    """Open (creating if needed) each directory component without following links."""
    current = root
    opened: list[DirHandle] = []
    try:
        for part in parts:
            st = current.stat(part)
            if st is None:
                try:
                    current.mkdir(part)
                except FileExistsError:
                    pass
                else:
                    created.append(current.path / part)
                st = current.stat(part)
            if st is None:
                raise CommitError(f"Cannot create directory: {current.path / part}")
            if stat.S_ISLNK(st.st_mode):
                raise CommitError(f"Refusing to write through symlink: {current.path / part}")
            if not stat.S_ISDIR(st.st_mode):
                raise CommitError(f"Destination conflict: {current.path / part} is not a directory.")
            nxt = current.open_dir(part)
            opened.append(nxt)
            current = nxt
        return current
    except BaseException:
        for handle in opened:
            handle.close()
        raise
    finally:
        for handle in opened[:-1]:
            handle.close()


def write_through(parent: DirHandle, leaf: str, source: Path, mode: int, cfg: Config) -> None:
    tmp = f".ghfd-tmp-{secrets.token_hex(8)}"
    fd = parent.create_tmp(tmp)
    try:
        with os.fdopen(fd, "wb") as out, source.open("rb") as inp:
            shutil.copyfileobj(inp, out, CHUNK)
            out.flush()
            if cfg.fsync:
                os.fsync(out.fileno())
        parent.chmod(tmp, mode)
        parent.replace(tmp, leaf)
    except BaseException:
        parent.unlink(tmp, missing_ok=True)
        raise


def backup_existing(parent: DirHandle, leaf: str, rel: str, backup_root: Path) -> Path:
    target = backup_root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    fd = parent.open_read(leaf)
    with os.fdopen(fd, "rb") as src, target.open("wb") as dst:
        shutil.copyfileobj(src, dst, CHUNK)
    return target


@dataclass
class CommitReport:
    files: int = 0
    directories: int = 0


def commit_tree(stage: Path, destination: Path, cfg: Config) -> CommitReport:
    """Transactional commit; rolls back installed files on ANY interruption."""
    files = sorted(p for p in stage.rglob("*") if p.is_file())
    dirs = sorted(p for p in stage.rglob("*") if p.is_dir())
    report = CommitReport()
    rel_files = [p.relative_to(stage).as_posix() for p in files]
    rel_dirs = [p.relative_to(stage).as_posix() for p in dirs]
    problems = detect_collisions(rel_files, rel_dirs, fold=filesystem_folds_case(destination))
    if problems:
        raise CommitError("Destination filesystem cannot represent this folder faithfully: "
                          + "; ".join(problems[:10]))
    created: list[Path] = []
    installed: list[tuple[str, ...]] = []
    backed_up: list[tuple[tuple[str, ...], Path]] = []

    with ExitStack() as stack:
        root = open_root(destination, allow_symlink=cfg.allow_destination_symlink)
        stack.callback(root.close)
        backup_root = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="ghfd-backup-")))
        try:
            for directory in dirs:
                parts = tuple(PurePosixPath(directory.relative_to(stage).as_posix()).parts)
                handle = descend(root, parts, created)
                if handle is not root:
                    handle.close()
                report.directories += 1
            if cfg.no_overwrite:
                # Fail before mutating anything when the caller forbids overwrites.
                for src in files:
                    parts = tuple(PurePosixPath(src.relative_to(stage).as_posix()).parts)
                    handle = descend(root, parts[:-1], created)
                    try:
                        if handle.stat(parts[-1]) is not None:
                            raise CommitError("File exists and --no-overwrite is set: "
                                              f"{destination / '/'.join(parts)}")
                    finally:
                        if handle is not root:
                            handle.close()
            for src in files:
                cfg.deadline.check("commit")
                rel = src.relative_to(stage).as_posix()
                parts = tuple(PurePosixPath(rel).parts)
                handle = descend(root, parts[:-1], created)
                try:
                    leaf = parts[-1]
                    st = handle.stat(leaf)
                    if st is not None:
                        if stat.S_ISLNK(st.st_mode):
                            raise CommitError(
                                f"Refusing to write through symlink: {destination / rel}")
                        if not stat.S_ISREG(st.st_mode):
                            raise CommitError(
                                f"Destination conflict: {destination / rel} is not a regular file.")
                        if cfg.no_overwrite:
                            raise CommitError(
                                f"File exists and --no-overwrite is set: {destination / rel}")
                        backed_up.append((parts, backup_existing(handle, leaf, rel, backup_root)))
                    write_through(handle, leaf, src, stat.S_IMODE(src.stat().st_mode), cfg)
                    installed.append(parts)
                    report.files += 1
                finally:
                    if handle is not root:
                        handle.close()
        except BaseException:
            _rollback(root, installed, backed_up, created)
            raise
    return report


def _rollback(root: DirHandle, installed: Sequence[tuple[str, ...]],
              backed_up: Sequence[tuple[tuple[str, ...], Path]], created: Sequence[Path]) -> None:
    for parts in reversed(installed):
        try:
            handle = descend(root, parts[:-1], [])
            try:
                handle.unlink(parts[-1], missing_ok=True)
            finally:
                if handle is not root:
                    handle.close()
        except (OSError, DownloadError):
            LOG.exception("event=rollback_unlink_failed path=%s", safe_log("/".join(parts)))
    for parts, backup in reversed(backed_up):
        try:
            handle = descend(root, parts[:-1], [])
            try:
                write_through(handle, parts[-1], backup, stat.S_IMODE(backup.stat().st_mode),
                              Config())
            finally:
                if handle is not root:
                    handle.close()
        except (OSError, DownloadError):
            LOG.exception("event=rollback_restore_failed path=%s", safe_log("/".join(parts)))
    for path in reversed(created):
        try:
            path.rmdir()
        except OSError:
            pass  # non-empty or already gone: never delete user content


# --------------------------------------------------------------------------- #
# Archive retention (atomic; never fails a successful commit)                  #
# --------------------------------------------------------------------------- #
def retention_name(target: RepoTarget, fmt: str) -> str:
    base = re.sub(r"[^A-Za-z0-9._-]+", "-",
                  f"{target.repo}-{target.ref}-{target.commit_sha[:12]}").strip("-") or "repository"
    return base + (".tar.gz" if fmt == "tar.gz" else ".zip")


def retain_archive(archive: Path, destination: Path, name: str, cfg: Config) -> Path | None:
    """Atomic retention into <destination>/.ghfd-archives/ (never collides with content)."""
    with ExitStack() as stack:
        root = open_root(destination, allow_symlink=cfg.allow_destination_symlink)
        stack.callback(root.close)
        handle = descend(root, (RETENTION_DIR,), [])
        try:
            st = handle.stat(name)
            if st is not None:
                if stat.S_ISLNK(st.st_mode):
                    raise CommitError(f"Refusing to retain archive through symlink: {name}")
                if cfg.no_overwrite:
                    log_event(logging.WARNING, "archive_retention_skipped",
                              reason="no_overwrite", path=name)
                    return None
            write_through(handle, name, archive, 0o600, cfg)
        finally:
            if handle is not root:
                handle.close()
    return destination / RETENTION_DIR / name


def safe_retain(archive: Path, destination: Path, name: str, cfg: Config) -> Path | None:
    """Retention is best-effort: it must never turn a successful commit into a failure."""
    try:
        return retain_archive(archive, destination, name, cfg)
    except Exception as exc:  # deliberately broad: logged, never fatal
        log_event(logging.WARNING, "archive_retention_failed", name=name, error=exc)
        return None


def download_with_archive_fallback(
    client: Client, target: RepoTarget, destination: Path, cfg: Config
) -> tuple[StageResult, str, Path | None]:
    errors: list[str] = []
    preserved: list[Path] = []
    for fmt, url in archive_urls(target):
        with tempfile.TemporaryDirectory(prefix="ghfd-archive-") as tmp:
            tmpdir = Path(tmp)
            archive = tmpdir / f"repository.{fmt}"
            try:
                client.download_to(url, archive, max_size=cfg.max_download)
            except DownloadError as exc:
                errors.append(f"{fmt} download: {exc}")
                log_event(logging.WARNING, "archive_download_failed", format=fmt, error=exc)
                continue
            stage = tmpdir / "stage"
            stage.mkdir()
            try:
                if fmt == "zip":
                    result = extract_zip_target(archive, stage, target, cfg)
                else:
                    result = extract_tar_target(archive, stage, target, cfg)
            except DeadlineExceeded:
                raise
            except Exception as exc:
                errors.append(f"{fmt} extraction: {exc}")
                log_event(logging.WARNING, "archive_extract_failed", format=fmt, error=exc)
                saved = safe_retain(archive, destination, retention_name(target, fmt), cfg)
                if saved is not None:
                    preserved.append(saved)
                    log_event(logging.WARNING, "archive_preserved_for_recovery", path=saved)
                continue
            # Commit failures are destination-side: no second format, no retry.
            report = commit_tree(stage, destination, cfg)
            result.files, result.directories = report.files, report.directories
            for old in preserved:
                try:
                    old.unlink(missing_ok=True)
                except OSError:
                    log_event(logging.WARNING, "cleanup_failed", path=old)
            retained = (safe_retain(archive, destination, retention_name(target, fmt), cfg)
                        if cfg.keep_archive else None)
            if retained is not None:
                log_event(logging.INFO, "archive_retained", path=retained)
            return result, fmt, retained
    raise RetrievalError("Archive fallback failed: " + " | ".join(errors))


# --------------------------------------------------------------------------- #
# CLI                                                                          #
# --------------------------------------------------------------------------- #
class JsonLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({"level": record.levelname, "message": record.getMessage()},
                          ensure_ascii=True)


def configure_logging(args: argparse.Namespace) -> None:
    level = logging.DEBUG if args.verbose else logging.WARNING if args.quiet else logging.INFO
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(JsonLogFormatter() if args.log_format == "json"
                         else logging.Formatter("%(levelname)s: %(message)s"))
    LOG.handlers[:] = [handler]
    LOG.setLevel(level)
    LOG.propagate = False


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="github_folder_downloader.py",
        description="Download and mirror a GitHub repository folder without cloning the repository.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=("Exit codes: 0 success, 1 failure, 2 usage/destination error, 3 ambiguous ref, "
                "130 interrupted. Use --json for failure classes."))
    parser.add_argument("github_folder_url", nargs="?", help="HTTPS GitHub folder or repository URL")
    parser.add_argument("destination", nargs="?", help="Local destination directory")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--self-test", action="store_true",
                        help="Run the built-in offline regression suite and exit")
    parser.add_argument("--ref", default=None,
                        help="Pin the ref; the URL tail is then the folder path (no guessing)")
    parser.add_argument("--path", default=None,
                        help="Explicit folder path (requires --ref; '' means repository root)")
    parser.add_argument("--token-env", default="GITHUB_TOKEN",
                        help="Environment variable holding the GitHub token")
    parser.add_argument("--timeout", type=float, default=30.0, help="Per-request timeout (seconds)")
    parser.add_argument("--deadline", type=float, default=DEFAULT_DEADLINE,
                        help="Global wall-clock budget for the whole run (seconds)")
    parser.add_argument("--retries", type=int, default=3,
                        help="Retries AFTER the first attempt (0 = a single attempt)")
    parser.add_argument("--backoff-base", type=float, default=RETRY_BASE_DELAY,
                        help="Exponential backoff base (seconds, jittered, capped)")
    parser.add_argument("--max-download-size", type=int, default=100,
                        help="Per-response / per-file / archive download cap (MiB)")
    parser.add_argument("--max-extracted-size", type=int, default=250,
                        help="Aggregate reconstructed content cap (MiB, all tiers)")
    parser.add_argument("--max-files", type=int, default=DEFAULT_MAX_FILES,
                        help="Maximum regular files to materialise")
    parser.add_argument("--max-dirs", type=int, default=DEFAULT_MAX_DIRS,
                        help="Maximum directories to materialise")
    parser.add_argument("--max-depth", type=int, default=DEFAULT_MAX_DEPTH,
                        help="Maximum path depth")
    parser.add_argument("--max-archive-entries", type=int, default=0,
                        help="Whole-archive entry cap (0 = derive from --max-files)")
    parser.add_argument("--max-compression-ratio", type=int, default=RATIO_WARN_DEFAULT,
                        help="Advisory ZIP ratio warning threshold (0 disables the warning)")
    parser.add_argument("--symlink-policy", choices=("skip", "fail"), default="skip",
                        help="Symlink/hardlink handling, identical in every tier")
    parser.add_argument("--lfs", choices=("warn", "fail"), default="warn",
                        help="Git LFS pointers: warn and materialise, or fail")
    parser.add_argument("--keep-archive", action="store_true",
                        help="Retain the archive in <destination>/.ghfd-archives after success")
    parser.add_argument("--no-overwrite", action="store_true",
                        help="Refuse to overwrite existing destination files")
    parser.add_argument("--allow-destination-symlink", action="store_true",
                        help="Permit the destination ROOT itself to be a symlink")
    parser.add_argument("--fsync", action="store_true",
                        help="fsync each committed file (slower, survives power loss)")
    parser.add_argument("--dry-run", action="store_true", help="Resolve and report only; write nothing")
    parser.add_argument("--json", action="store_true", help="Emit a JSON summary on stdout")
    parser.add_argument("--log-format", choices=("text", "json"), default="text",
                        help="Log format on stderr")
    parser.add_argument("--verbose", action="store_true", help="Debug logging")
    parser.add_argument("--quiet", action="store_true", help="Warnings and errors only")
    return parser


def config_from_args(args: argparse.Namespace) -> Config:
    return Config(
        timeout=float(args.timeout), retries=int(args.retries),
        backoff_base=float(args.backoff_base),
        max_download=int(args.max_download_size) * MIB,
        max_extract=int(args.max_extracted_size) * MIB,
        max_files=int(args.max_files), max_dirs=int(args.max_dirs),
        max_depth=int(args.max_depth), max_archive_entries=int(args.max_archive_entries),
        ratio_warn=int(args.max_compression_ratio),
        symlink_policy=str(args.symlink_policy), lfs_policy=str(args.lfs),
        no_overwrite=bool(args.no_overwrite), keep_archive=bool(args.keep_archive),
        allow_destination_symlink=bool(args.allow_destination_symlink),
        fsync=bool(args.fsync), dry_run=bool(args.dry_run),
        token=os.environ.get(str(args.token_env)) or None,
        deadline=Deadline(float(args.deadline)))


def validate_args(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    positives = {"--timeout": args.timeout, "--deadline": args.deadline,
                 "--max-download-size": args.max_download_size,
                 "--max-extracted-size": args.max_extracted_size,
                 "--max-files": args.max_files, "--max-dirs": args.max_dirs,
                 "--max-depth": args.max_depth}
    for name, value in positives.items():
        if value <= 0:
            parser.error(f"{name} must be positive.")
    if not 0 <= args.retries <= MAX_RETRIES:
        parser.error(f"--retries must be between 0 and {MAX_RETRIES}.")
    if args.backoff_base < 0:
        parser.error("--backoff-base must be non-negative.")
    if args.max_archive_entries < 0:
        parser.error("--max-archive-entries must be non-negative (0 = derive).")
    if args.max_compression_ratio < 0:
        parser.error("--max-compression-ratio must be non-negative (0 disables the warning).")
    if args.path is not None and args.ref is None:
        parser.error("--path requires --ref.")


def summarise_result(summary: dict[str, object], result: StageResult, tier: str,
                     retained: Path | None) -> None:
    summary.update(tier=tier, files=result.files, directories=result.directories,
                   bytes=result.bytes, skipped_symlinks=result.skipped_symlinks,
                   skipped_submodules=result.skipped_submodules,
                   lfs_pointers=result.lfs_pointers, deduplicated=result.deduplicated,
                   retained_archive=str(retained) if retained else None)


def run(args: argparse.Namespace, summary: dict[str, object]) -> int:
    cfg = config_from_args(args)
    client = Client(cfg)
    dest_raw = Path(str(args.destination)).expanduser()
    if dest_raw.is_symlink() and not cfg.allow_destination_symlink:
        raise UsageError(f"Destination is a symlink: {dest_raw}. "
                         "Use --allow-destination-symlink to permit this explicitly.")
    try:
        destination = dest_raw.resolve()
    except OSError as exc:
        raise UsageError(f"Cannot resolve destination {dest_raw}: {exc}") from exc
    if destination.exists() and not destination.is_dir():
        raise UsageError(f"Destination exists but is not a directory: {destination}")
    summary["destination"] = str(destination)

    owner, repo, tail, kind = parse_url(str(args.github_folder_url))
    target = resolve_target(client, owner, repo, tail, kind, cfg=cfg,
                            ref_override=args.ref, path_override=args.path)
    summary.update(owner=target.owner, repo=target.repo, ref=target.ref,
                   path=target.path, commit=target.commit_sha)
    log_event(logging.INFO, "resolved", repo=f"{target.owner}/{target.repo}", ref=target.ref,
              path=target.path or "(repository root)", commit=target.commit_sha[:12])
    if not target.path:
        log_event(logging.WARNING, "whole_repository_requested",
                  note="no folder path given; limits still apply")

    if cfg.dry_run:
        cache = TreeCache(client, target.owner, target.repo)
        entries = fetch_folder_entries(cache, target.subtree_sha, cfg)
        planned = StageResult()
        for entry in entries:
            if entry.kind == "tree":
                planned.directories += 1
            elif entry.kind == "commit" or entry.mode == SUBMODULE_MODE:
                planned.skipped_submodules += 1
            elif entry.kind == "blob" and entry.mode == SYMLINK_MODE:
                planned.skipped_symlinks += 1
            elif entry.kind == "blob":
                planned.files += 1
                planned.bytes += entry.size
        summary.update(tier="dry-run", files=planned.files, directories=planned.directories,
                       bytes=planned.bytes, skipped_symlinks=planned.skipped_symlinks,
                       skipped_submodules=planned.skipped_submodules)
        log_event(logging.INFO, "dry_run", files=planned.files,
                  directories=planned.directories, bytes=planned.bytes)
        return EXIT_OK

    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ghfd-primary-") as tmp:
        stage = Path(tmp) / "stage"
        stage.mkdir()
        try:
            result = stage_api_folder(client, target, stage, cfg)
        except DeadlineExceeded:
            raise
        except DownloadError as exc:
            log_event(logging.WARNING, "primary_failed", error=exc)
        else:
            # Commit is deliberately OUTSIDE the staging handler: a destination
            # conflict must never trigger a whole-repository archive download.
            report = commit_tree(stage, destination, cfg)
            result.files, result.directories = report.files, report.directories
            summarise_result(summary, result, "api", None)
            log_event(logging.INFO, "success", tier="api", files=result.files,
                      bytes=result.bytes, mib=f"{result.bytes / MIB:.2f}")
            return EXIT_OK

    result, fmt, retained = download_with_archive_fallback(client, target, destination, cfg)
    summarise_result(summary, result, fmt, retained)
    log_event(logging.INFO, "success", tier=fmt, files=result.files,
              bytes=result.bytes, mib=f"{result.bytes / MIB:.2f}")
    return EXIT_OK


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    configure_logging(args)
    if args.self_test:
        return run_self_test()
    if not args.github_folder_url or not args.destination:
        parser.error("URL and DESTINATION are required (or use --self-test).")
    validate_args(parser, args)
    started = time.monotonic()
    summary: dict[str, object] = {"ok": False, "exit_code": EXIT_FAILURE, "error_class": None,
                                  "message": None, "version": __version__,
                                  "dry_run": bool(args.dry_run)}
    try:
        code = run(args, summary)
        summary["ok"] = code == EXIT_OK
    except AmbiguousRefError as exc:
        code = EXIT_AMBIGUOUS
        summary["error_class"] = type(exc).__name__
        summary["message"] = str(exc)
        summary["interpretations"] = list(exc.interpretations)
        LOG.error("%s", exc)
        for interpretation in exc.interpretations:
            LOG.error("  possible: %s", safe_log(interpretation))
    except UsageError as exc:
        code = EXIT_USAGE
        summary["error_class"] = type(exc).__name__
        summary["message"] = str(exc)
        LOG.error("%s", exc)
    except DownloadError as exc:
        code = EXIT_FAILURE
        summary["error_class"] = type(exc).__name__
        summary["message"] = str(exc)
        LOG.error("%s", exc)
    except KeyboardInterrupt:
        code = EXIT_INTERRUPTED
        summary["error_class"] = "KeyboardInterrupt"
        summary["message"] = "interrupted"
        LOG.error("Interrupted.")
    except OSError as exc:
        code = EXIT_FAILURE
        summary["error_class"] = type(exc).__name__
        summary["message"] = f"filesystem error: {exc}"
        LOG.error("Filesystem error: %s", safe_log(exc))
    except Exception as exc:  # last resort: always reported, never silent
        code = EXIT_FAILURE
        summary["error_class"] = type(exc).__name__
        summary["message"] = f"unexpected error: {exc}"
        LOG.exception("Unexpected error.")
    summary["exit_code"] = code
    summary["duration_seconds"] = round(time.monotonic() - started, 3)
    if args.json:
        print(json.dumps(summary, ensure_ascii=True, sort_keys=True))
    return code


# --------------------------------------------------------------------------- #
# Built-in offline smoke suite (--self-test). Never touches the network.       #
# Anchors the highest-severity audited defects; extend it when you fix a bug.  #
# --------------------------------------------------------------------------- #
def run_self_test() -> int:
    import email.message
    import io
    import unittest
    from unittest import mock

    mod = sys.modules[__name__]

    class Resp:
        def __init__(self, payload: bytes = b"", headers: dict[str, str] | None = None) -> None:
            self._buf, self.headers = io.BytesIO(payload), headers or {}

        def read(self, size: int = -1) -> bytes:
            return self._buf.read(size)

        def __enter__(self) -> "Resp":
            return self

        def __exit__(self, *exc: object) -> bool:
            return False

    def err(url: str, code: int, headers: dict[str, str] | None = None) -> urllib.error.HTTPError:
        msg = email.message.Message()
        for key, value in (headers or {}).items():
            msg[key] = value
        return urllib.error.HTTPError(url, code, "error", msg, io.BytesIO(b""))

    def zip_of(path: Path, entries: list[tuple[str, bytes]],
               links: list[tuple[str, str]] | None = None) -> Path:
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
            for name, data in entries:
                zf.writestr(name, data)
            for name, link in links or []:
                info = zipfile.ZipInfo(name)
                info.external_attr = (stat.S_IFLNK | 0o777) << 16
                zf.writestr(info, link)
        return path

    def tar_of(path: Path, entries: list[tuple[str, bytes]]) -> Path:
        with tarfile.open(path, "w:gz") as tf:
            for name, data in entries:
                info = tarfile.TarInfo(name)
                info.size = len(data)
                tf.addfile(info, io.BytesIO(data))
        return path

    TARGET = RepoTarget("o", "r", "main", "docs", "a" * 40, "b" * 40, "b" * 40)

    class Smoke(unittest.TestCase):
        def setUp(self) -> None:
            guard = mock.patch.object(mod, "_open_request",
                                      side_effect=AssertionError("self-test is offline"))
            guard.start()
            self.addCleanup(guard.stop)
            self._tmp = tempfile.TemporaryDirectory()
            self.addCleanup(self._tmp.cleanup)
            self.base = Path(self._tmp.name)

        def stage(self, files: dict[str, bytes]) -> Path:
            root = Path(tempfile.mkdtemp(prefix="stage-", dir=self.base))
            for rel, data in files.items():
                dest = root.joinpath(*rel.split("/"))
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
            return root

        def dest(self) -> Path:
            path = self.base / "dest"
            path.mkdir(exist_ok=True)
            return path

        def test_urls_and_paths(self) -> None:
            self.assertEqual(parse_url("https://github.com/o/r/tree/main/docs"),
                             ("o", "r", ["main", "docs"], "tree"))
            self.assertEqual(parse_url("https://github.com/o/r/tree/main"),
                             ("o", "r", ["main"], "tree"))
            self.assertEqual(parse_url("https://github.com/o/r.git/"), ("o", "r", [], "root"))
            for url in ("http://github.com/o/r/tree/main/d", "https://gitlab.com/o/r/tree/main/d",
                        "https://github.com/o/r/blob/main/d.md",
                        "https://u:p@github.com/o/r/tree/main/d",
                        "https://github.com/o/r/tree/main/d?q=1",
                        "https://github.com/o/../tree/main/d",
                        "https://github.com/o/r/tree/main/a%2Fb", "not a url"):
                with self.subTest(url=url), self.assertRaises(DownloadError):
                    parse_url(url)
            for bad in ("", "../x", "/etc/passwd", "a/../b", "C:/x", "..\\x", "\\\\h\\s", "a\x00b"):
                with self.subTest(bad=bad), self.assertRaises(DownloadError):
                    safe_relpath(bad)
            if not IS_WINDOWS:
                self.assertEqual(safe_relpath("a\\b").parts, ("a\\b",))
                self.assertEqual(safe_relpath("a/:x").parts, ("a", ":x"))
            with mock.patch.object(mod, "IS_WINDOWS", True):
                for bad in ("a/:x", "CON.txt", "foo.", "a\\b"):
                    with self.subTest(bad=bad), self.assertRaises(DownloadError):
                        safe_relpath(bad)
            norm, original = member_views("./root/docs/a\\b")
            self.assertEqual((norm, original), ("root/docs/a/b", "root/docs/a\\b"))
            self.assertTrue(detect_collisions(["README.md", "readme.md"], [], fold=True))
            self.assertFalse(detect_collisions(["README.md", "readme.md"], [], fold=False))

        def test_redirects_and_retries(self) -> None:
            handler = SafeRedirectHandler()

            def go(src: str, dst: str) -> urllib.request.Request | None:
                return handler.redirect_request(
                    urllib.request.Request(src, headers={"Authorization": "Bearer T"}),
                    None, 302, "Found", email.message.Message(), dst)

            cross = go("https://codeload.github.com/o/r/zip/x",
                       "https://objects.githubusercontent.com/s?sig=x")
            assert cross is not None
            self.assertIsNone(cross.headers.get("Authorization"))
            same = go("https://api.github.com/a", "https://api.github.com/b")
            assert same is not None
            self.assertEqual(same.headers.get("Authorization"), "Bearer T")
            with self.assertRaises(DownloadError):
                go("https://api.github.com/a", "http://api.github.com/b")
            self.assertTrue(any(isinstance(h, SafeRedirectHandler) for h in get_opener().handlers))
            url = "https://api.github.com/x"
            for effects, cfg, calls, raises in (
                    ([err(url, 500), Resp(b"ok")], Config(), 2, False),
                    ([err(url, 404)], Config(), 1, True),
                    ([err(url, 500)], Config(retries=0), 1, True),
                    ([err(url, 429, {"Retry-After": "3600"})], Config(), 1, True),
                    ([err(url, 403, {"Retry-After": "0"}), Resp(b"ok")], Config(), 2, False),
                    ([ssl.SSLCertVerificationError("bad")], Config(), 1, True)):
                with self.subTest(calls=calls):
                    with mock.patch.object(mod.time, "sleep"), \
                            mock.patch.object(mod, "_open_request", side_effect=effects) as op:
                        if raises:
                            with self.assertRaises(RetrievalError):
                                Client(cfg).read_bytes(url)
                        else:
                            self.assertEqual(Client(cfg).read_bytes(url), b"ok")
                        self.assertEqual(op.call_count, calls)
            with self.assertRaises(DeadlineExceeded):
                Client(Config(deadline=Deadline(-1))).read_bytes(url)

        def test_archives(self) -> None:
            with self.assertRaises(DownloadError):
                extract_zip_target(zip_of(self.base / "a.zip", [("root/other/x", b"x")]),
                                   self.base, TARGET, Config())
            with self.assertRaises(DownloadError):
                extract_zip_target(zip_of(self.base / "b.zip", [("root/docs/../../etc/p", b"x")]),
                                   self.base, TARGET, Config())
            linked = zip_of(self.base / "c.zip", [("root/docs/ok", b"x")], [("root/docs/l", "/etc")])
            res = extract_zip_target(linked, self.base, TARGET, Config())
            self.assertEqual((res.files, res.skipped_symlinks), (1, 1))
            with self.assertRaises(DownloadError):
                extract_zip_target(linked, self.base, TARGET, Config(symlink_policy="fail"))
            if not IS_WINDOWS:
                extract_zip_target(zip_of(self.base / "d.zip", [("root/docs/a\\b", b"x")]),
                                   self.base, TARGET, Config())
                self.assertTrue((self.base / "a\\b").is_file())
                self.assertFalse((self.base / "a" / "b").exists())
                extract_tar_target(tar_of(self.base / "d.tgz", [("root/docs/a\\b", b"x")]),
                                   self.base, TARGET, Config())
                self.assertTrue((self.base / "a\\b").is_file())
            bomb = tar_of(self.base / "f.tgz",
                          [("root/other/big", b"\0" * 200000), ("root/docs/a", b"ok")])
            with self.assertRaises(LimitExceeded) as ctx:
                extract_tar_target(bomb, self.base, TARGET, Config(max_extract=2000))
            self.assertIn("scan budget", str(ctx.exception))
            with self.assertRaises(LimitExceeded):
                extract_zip_target(zip_of(self.base / "e.zip",
                                          [(f"root/docs/f{i}", b"x") for i in range(30)]),
                                   self.base, TARGET, Config(max_archive_entries=10))
            with self.assertRaises(DownloadError):
                archive_urls(RepoTarget("o", "r", "main", "docs", "../../evil", "b" * 40))

        def test_commit_rollback_retention(self) -> None:
            for use_dir_fd in (True, False):
                dest, outside = self.dest(), self.base / f"out{use_dir_fd}"
                outside.mkdir()
                (dest / f"s{use_dir_fd}").symlink_to(outside, target_is_directory=True)
                stage = self.stage({f"s{use_dir_fd}/f.txt": b"x"})
                with mock.patch.object(mod, "_DIR_FD_OK", use_dir_fd):
                    with self.assertRaises(CommitError):
                        commit_tree(stage, dest, Config())
                self.assertFalse((outside / "f.txt").exists())
            dest = self.dest()
            (dest / "existing.txt").write_bytes(b"old")
            stage = self.stage({"existing.txt": b"new", "second.txt": b"second"})
            real_replace, state = DirHandle.replace, {"n": 0}

            def flaky(handle: DirHandle, src: str, dst: str) -> None:
                state["n"] += 1
                if state["n"] == 2:
                    raise KeyboardInterrupt
                real_replace(handle, src, dst)

            with mock.patch.object(DirHandle, "replace", flaky):
                with self.assertRaises(KeyboardInterrupt):
                    commit_tree(stage, dest, Config())
            self.assertEqual((dest / "existing.txt").read_bytes(), b"old")
            self.assertFalse((dest / "second.txt").exists())
            with self.assertRaises(CommitError):
                commit_tree(self.stage({"existing.txt": b"n"}), dest, Config(no_overwrite=True))
            archive = self.base / "repo.zip"
            archive.write_bytes(b"PK")
            saved = retain_archive(archive, dest, "r.zip", Config())
            assert saved is not None
            self.assertEqual(stat.S_IMODE(saved.stat().st_mode), 0o600)
            self.assertIsNone(retain_archive(archive, dest, "r.zip", Config(no_overwrite=True)))
            not_dir = self.base / "file"
            not_dir.write_bytes(b"x")
            self.assertIsNone(safe_retain(archive, not_dir, "r.zip", Config()))

        def test_guards(self) -> None:
            import ast
            import inspect
            tree = ast.parse(inspect.getsource(mod))
            bad_mods = {"subprocess", "pty", "runpy", "importlib", "ctypes"}
            bad_calls = {"exec", "eval", "system", "popen", "spawn", "execv", "execve", "fork"}
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.assertNotIn(alias.name.split(".")[0], bad_mods)
                if isinstance(node, ast.ImportFrom):
                    self.assertNotIn((node.module or "").split(".")[0], bad_mods)
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        self.assertNotIn(node.func.id, bad_calls)
                    if isinstance(node.func, ast.Attribute):
                        self.assertNotIn(node.func.attr, bad_calls)
            self.assertNotIn("\n", safe_log("a\nb"))
            self.assertIn("\\x0a", safe_log("a\nb"))

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Smoke)
    result = unittest.TextTestRunner(verbosity=1, stream=sys.stderr).run(suite)
    return EXIT_OK if result.wasSuccessful() else EXIT_FAILURE


if __name__ == "__main__":
    sys.exit(main())
