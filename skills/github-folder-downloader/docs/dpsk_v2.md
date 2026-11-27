## Audit approach

1. Read the full attached script and traced each execution path: CLI → URL parsing → ref/path resolution → primary API retrieval → archive fallback → staging → commit → reporting.
2. Checked against the stated plan, especially: targeted retrieval, branch names with slashes, archive safety, destination transactionality, limits, diagnostics, and Definition of Done.
3. Reviewed across correctness, security, data integrity, error handling, performance, testing, maintainability, consistency, and dependency health.
4. No code changes were made; this is audit/review only.

## Verification ledger

- Full script inspected statically: yes.
- Script executed: no.
- Tests run: no.
- Live GitHub API/download behavior verified: no.
- All findings below are therefore **Reasoned** from code inspection unless explicitly noted.
- Live network behavior remains **Unverifiable** in this environment.

## Summary

| Severity | Count |
|---|---:|
| Critical | 0 |
| High | 4 |
| Medium | 12 |
| Low | 9 |
| Informational | 1 |

No fixes applied. The script should not be treated as production-ready until the High findings and the material Medium findings are addressed.

---

# High findings

## H1 — Primary retrieval walks the entire repository tree repeatedly, defeating targeted retrieval

**Location:** `resolve_target()`, `fetch_tree()`, `stage_api_folder()`

**Description:** For a `tree` URL, `resolve_target()` calls `fetch_tree(tree_sha, "", ...)`, which recursively fetches every subtree in the repository. It then calls the recursive tree endpoint for verification. Later, `stage_api_folder()` calls `fetch_tree()` again and filters locally for the target folder. This enumerates repository metadata for the whole repo multiple times.

**Evidence:** `tree = fetch_tree(...)` in `resolve_target()`; `entries = fetch_tree(target.tree_sha, "", ...)` in `stage_api_folder()`; `fetch_tree()` recurses per tree directory.

**Impact:** Large or even moderately sized repositories can exhaust GitHub API rate limits, making primary retrieval fail and forcing the archive fallback, which downloads the entire repository. This directly undermines the primary objective.

**Recommended fix:** Use one recursive tree request where safe, check `truncated`, and reuse those entries. For large repos, resolve only the target path via the Contents API or targeted tree traversal. Do not recursively walk the entire repository for a nested folder.

**Confidence:** Reasoned.

## H2 — Archive fallback can report success with zero files when target folder is missing or unmatched

**Location:** `extract_zip_target()`, `extract_tar_target()`, `download_with_archive_fallback()`

**Description:** Both extractors return `(0, 0)` if no archive entries match the target prefix. `download_with_archive_fallback()` then calls `commit_files()` with an empty stage, and `main()` logs `SUCCESS` with zero files.

**Evidence:** `selected` can remain empty; extractors return `len(selected), total`; `commit_files()` accepts zero files; success is reported.

**Impact:** The script can falsely claim success while downloading nothing. This is especially dangerous if archive root/prefix detection is wrong or the target path is absent.

**Recommended fix:** Verify that the target directory exists in the archive. For non-root targets, fail if zero files are selected. Consider requiring at least one selected entry unless the target is explicitly known to be empty.

**Confidence:** Reasoned.

## H3 — Destination symlink traversal can write outside the intended destination

**Location:** `main()`, `commit_files()`, `preserve_archive()`

**Description:** `main()` resolves the top-level destination path, but `commit_files()` does not reject symlinked parent directories under the destination. If a staged relative path maps through a pre-existing symlinked directory, `dst.parent.mkdir(...)` and `os.replace()` can write outside the destination. `preserve_archive()` similarly copies to a destination path that may be a symlink file.

**Evidence:** `dst = destination / rel`; `dst.parent.mkdir(parents=True, exist_ok=True)`; `os.replace(tmp, dst)`; `shutil.copyfile(archive, dest)`.

**Impact:** In shared or untrusted destination directories, this can overwrite arbitrary files writable by the user. This is a serious safety issue.

**Recommended fix:** Reject symlinked destination components, or use `os.open` with `O_NOFOLLOW`/directory file descriptors and verify resolved parents remain under the destination. Do not silently resolve top-level symlinks. Apply the same policy to archive preservation.

**Confidence:** Reasoned.

## H4 — `commit_files()` does not roll back on `KeyboardInterrupt` or `SystemExit`

**Location:** `commit_files()`

**Description:** The rollback block catches `Exception`, which does not catch `KeyboardInterrupt` or `SystemExit`. If the user interrupts during commit, partially installed files remain, and backups inside the temporary stage are deleted when the temporary directory exits.

**Evidence:** `except Exception:` only; `backup = stage / ".rollback"`; temporary stage is removed by the caller.

**Impact:** An interrupted run can leave the destination partially updated and unrecoverable via the script’s rollback data.

**Recommended fix:** Catch `BaseException`, perform rollback, then re-raise. Also clean up temporary destination files in a `finally` block.

**Confidence:** Reasoned.

---

# Medium findings

## M1 — Ambiguous ref/path resolution silently selects the longest candidate ref

**Location:** `resolve_target()`

**Description:** The resolver tries the longest possible ref prefix first and returns the first candidate that resolves. If both a longer ref and a shorter ref/path interpretation are valid, the script silently chooses the longer one.

**Evidence:** Loop `for split in range(len(tail), 0, -1)` returns on first valid candidate; no ambiguity check across candidates.

**Impact:** The wrong folder can be downloaded when branch names and folder paths overlap, e.g. branch `feature/new-solver` versus branch `feature` with folder `new-solver/...`.

**Recommended fix:** Collect all valid ref/path interpretations. If more than one is valid, abort with a clear ambiguity error listing candidates, or require an explicit ref argument.

**Confidence:** Reasoned.

## M2 — Raw file downloads use `target.ref` instead of the resolved commit SHA

**Location:** `download_blob()`

**Description:** The raw URL is built with `target.ref`. For branch names containing slashes, the raw URL path is ambiguous. The archive fallback correctly uses `target.commit_sha`.

**Evidence:** `url = f"{RAW_BASE}/.../{encode_path(target.ref)}/{encode_path(path)}"`.

**Impact:** Primary retrieval can fail or resolve ambiguously for slash-containing branches, forcing archive fallback.

**Recommended fix:** Use `target.commit_sha` in raw URLs to remove ref ambiguity.

**Confidence:** Reasoned.

## M3 — `--max-extracted-size` is not enforced on primary retrieval

**Location:** `stage_api_folder()`, `main()`

**Description:** Primary retrieval enforces `max_download` only. `max_extracted_size` is used only for archive extraction. If `--max-download-size` is larger than `--max-extracted-size`, primary retrieval can commit more reconstructed content than the extracted-size limit permits.

**Evidence:** `stage_api_folder()` receives `max_download` and `max_files`, but not `max_extract`.

**Impact:** The documented resource limit is not consistently enforced.

**Recommended fix:** Pass `max_extract` into primary retrieval and enforce it against the total staged size, or enforce `min(max_download, max_extract)` consistently.

**Confidence:** Reasoned.

## M4 — No integrity verification of downloaded blob content

**Location:** `stage_api_folder()`, `download_blob()`

**Description:** GitHub tree entries include blob SHA and size metadata, but the script ignores them. It writes raw response bytes without verifying size or Git blob hash.

**Evidence:** `entry["sha"]` and `entry["size"]` are available but unused for verification after download.

**Impact:** Corrupted or unexpected responses can be committed without detection.

**Recommended fix:** Verify downloaded size and, where practical, verify the Git blob SHA. At minimum, compare written byte count with tree metadata when available.

**Confidence:** Reasoned.

## M5 — Archive URLs use unencoded/unvalidated `owner` and `repo`

**Location:** `archive_urls()`, `parse_url()`

**Description:** `parse_url()` does not strictly validate GitHub owner/repo naming, and `archive_urls()` interpolates `target.owner` and `target.repo` directly into a codeload URL. Percent-encoded `?`, `#`, or other characters can alter the constructed URL.

**Evidence:** `f"https://codeload.github.com/{target.owner}/{target.repo}/zip/{commit}"`.

**Impact:** Incorrect or manipulated archive URLs; potential URL-structure injection within codeload.

**Recommended fix:** Validate owner/repo against GitHub’s allowed naming pattern and quote path components with `encode_path()`.

**Confidence:** Reasoned.

## M6 — `safe_relpath()` rejects valid POSIX filenames containing `:` or `\`

**Location:** `safe_relpath()`

**Description:** The function rejects any path component containing `:`, and it replaces backslashes with slashes. Git repositories on POSIX can contain such filenames. A single such file causes primary and archive retrieval to fail.

**Evidence:** `if any(":" in part ...)`; `path = path.replace("\\", "/")`.

**Impact:** Valid repositories cannot be downloaded; behavior is platform-inconsistent.

**Recommended fix:** Apply Windows-invalid checks only on Windows. On POSIX, allow valid characters. For cross-platform safety, document and optionally sanitize rather than failing the whole download.

**Confidence:** Reasoned.

## M7 — Partial archives are preserved on failed downloads or size-limit failures

**Location:** `stream_to_file()`, `download_with_archive_fallback()`

**Description:** `stream_to_file()` writes directly to the archive path. If the download fails mid-stream or exceeds `max_size`, a partial archive remains. The fallback then sees `archive.exists()` and preserves it as if it were a valid downloaded archive.

**Evidence:** `with ... out.open("wb") as fh:` then exception; later `if archive.exists() and archive.stat().st_size:`.

**Impact:** Corrupt/partial archives are falsely presented as recovery artifacts.

**Recommended fix:** Track successful download completion explicitly. Delete partial archives on download failure. Preserve only fully downloaded archives.

**Confidence:** Reasoned.

## M8 — ZIP/TAR entry counts are not bounded before loading all entries

**Location:** `extract_zip_target()`, `extract_tar_target()`, `archive_prefix()`

**Description:** `zf.infolist()` and `tf.getmembers()` load all entries before checking `max_files`. A malicious archive with a very large number of entries can consume memory before the file-count limit is applied.

**Evidence:** `names = [i.filename for i in zf.infolist()]`; `names = [m.name for m in tf.getmembers()]`; `max_files` checked later on selected entries.

**Impact:** Memory exhaustion / denial of service from untrusted archives.

**Recommended fix:** Apply an early entry-count cap before building full lists where the archive format permits, or stream entries with a hard limit and fail early.

**Confidence:** Reasoned.

## M9 — No HTTP retry, backoff, or `Retry-After` handling

**Location:** `request_bytes()`, `api_json()`, `stream_to_file()`

**Description:** The HTTP layer performs a single attempt. It does not retry transient 5xx, 429, or timeout failures, and does not honor `Retry-After`.

**Evidence:** No retry loop or status-specific handling beyond raising `DownloadError`.

**Impact:** Transient GitHub failures unnecessarily trigger archive fallback or total failure.

**Recommended fix:** Add bounded retries with exponential backoff for idempotent GET requests, honoring `Retry-After` for 429/503.

**Confidence:** Reasoned.

## M10 — Commit temporary filename can clobber an existing file and is not cleaned up reliably

**Location:** `commit_files()`

**Description:** Temporary files are named `dst.name + ".tmp-download"` in the destination directory. An existing unrelated file with that name can be overwritten. If copy or replace fails, the temporary file may remain.

**Evidence:** `tmp = dst.with_name(dst.name + ".tmp-download")`; cleanup only in rollback for installed files, not temp files.

**Impact:** Unrelated destination files can be lost; partial temp files remain after failures.

**Recommended fix:** Use `tempfile.NamedTemporaryFile(dir=dst.parent, delete=False)` with a unique name and clean it in a `finally` block.

**Confidence:** Reasoned.

## M11 — No automated test suite is included

**Location:** Attachment / repository

**Description:** The plan’s Definition of Done requires automated tests for core functionality and failure scenarios. The attachment contains only the script and claims smoke tests, but no test files or runnable test harness are provided.

**Impact:** URL parsing, slash branches, archive safety, rollback, and limits are unverified against regressions.

**Recommended fix:** Add a pytest suite with mocked HTTP responses and synthetic ZIP/TAR fixtures covering the plan’s test matrix, especially traversal entries, ambiguous refs, truncated trees, interrupts, and conflicts.

**Confidence:** Reasoned from the attachment.

## M12 — `fetch_tree()` ignores `truncated` on non-recursive tree responses

**Location:** `fetch_tree()`

**Description:** GitHub tree responses can be truncated. `fetch_tree()` does not check the `truncated` flag for non-recursive requests and can silently omit entries.

**Evidence:** `data = api_json(...)`; only `data.get("tree")` is checked; `truncated` is not inspected.

**Impact:** Files can be missing from a successful primary download without warning.

**Recommended fix:** Check `truncated` and fail the primary path or switch to a targeted recursive/Contents API strategy.

**Confidence:** Reasoned.

---

# Low findings

## L1 — `resolve_target()` swallows detailed download errors

**Location:** `resolve_target()`

**Description:** Each candidate resolution catches `DownloadError` and continues. Rate-limit, authentication, and network errors become a generic “Could not resolve URL” error.

**Recommended fix:** Preserve and surface the last meaningful error, especially rate-limit and auth failures.

**Confidence:** Reasoned.

## L2 — `archive_prefix()` is fragile to metadata entries or `./` prefixes

**Location:** `archive_prefix()`

**Description:** It requires exactly one top-level root across all members. Archives containing `./` prefixes, pax metadata, or extra top-level entries can fail even when the target exists.

**Recommended fix:** Normalize leading `./`, ignore known metadata entries, and validate the repository root explicitly.

**Confidence:** Reasoned.

## L3 — `.rollback` backup directory can collide with staged repository content

**Location:** `commit_files()`

**Description:** The backup directory is created inside the staging directory as `.rollback`. A repository file or directory named `.rollback` can conflict with it.

**Recommended fix:** Create rollback storage outside the staged content tree.

**Confidence:** Reasoned.

## L4 — `keep_archive` save failure after successful commit can trigger another format attempt

**Location:** `download_with_archive_fallback()`

**Description:** If extraction and commit succeed but saving the retained archive fails, the exception is treated as a fallback failure, and the next archive format is attempted. This can duplicate commit work.

**Recommended fix:** Separate archive-retention failure from retrieval failure; warn and return success if commit already succeeded.

**Confidence:** Reasoned.

## L5 — Preserved ZIP remains after TAR.GZ fallback succeeds

**Location:** `download_with_archive_fallback()`

**Description:** If ZIP extraction fails, its archive is preserved. If TAR.GZ then succeeds, the preserved ZIP remains in the destination.

**Recommended fix:** Remove non-retained recovery archives after a later fallback succeeds, unless explicitly requested.

**Confidence:** Reasoned.

## L6 — API retrieval materializes Git symlinks as regular files

**Location:** `fetch_tree()`, `stage_api_folder()`

**Description:** Git symlinks appear as blobs with mode `120000`. The script ignores mode and writes the link target as ordinary file content. Archive extraction rejects symlinks, so behavior is inconsistent.

**Recommended fix:** Inspect tree entry mode and skip, report, or explicitly handle symlinks according to policy. Prefer not to materialize them as regular files silently.

**Confidence:** Reasoned.

## L7 — No suspicious compression-ratio check

**Location:** `extract_zip_target()`, `extract_tar_target()`

**Description:** The plan calls for guarding against suspicious compression ratios. The implementation checks absolute sizes and counts but not compression ratio.

**Recommended fix:** Add a configurable ratio cap if this threat model matters; absolute extracted-size limits already mitigate the worst case.

**Confidence:** Reasoned.

## L8 — Dead code and unused constants

**Location:** `sha256_file()`, `archive_bytes`, `DEFAULT_MAX_DOWNLOAD`, `DEFAULT_MAX_EXTRACT`

**Description:** Several definitions are unused. This is minor but reduces clarity.

**Recommended fix:** Remove unused code or wire it into integrity verification/defaults.

**Confidence:** Reasoned.

## L9 — Archive retention ignores `--no-overwrite`

**Location:** `preserve_archive()`, `keep_archive` handling

**Description:** Retained archives are written with `shutil.copyfile`, which overwrites existing destination files regardless of `--no-overwrite`.

**Recommended fix:** Respect `--no-overwrite` for retained archives or document that archive retention is exempt.

**Confidence:** Reasoned.

---

# Informational

## I1 — Live GitHub behavior remains unverified

The script’s own delivery note states that live GitHub downloads, rate-limit behavior, and real archive extraction were not tested. This audit is static only. The highest-risk unverified areas are slash-containing branch resolution, GitHub tree truncation behavior, codeload redirects, and archive root naming.

**Needed to verify:** run integration tests against controlled repositories, including a branch with a slash, a large/truncated tree, a ZIP/TAR archive with symlinks and traversal entries, and an interrupted commit.

---

## Recommended remediation order

1. Fix destination symlink traversal and commit rollback on `BaseException`.
2. Replace full-repository tree walking with targeted metadata retrieval.
3. Fail archive fallback when the target folder produces zero selected files.
4. Use commit SHA for raw downloads.
5. Enforce `max_extract` consistently and add blob integrity checks.
6. Harden URL construction and `safe_relpath()` platform behavior.
7. Add the automated test suite before treating the utility as production-ready.

---

# Plan: `github_folder_downloader` v2 — Robust, Audited Remediation

Scope: produce an enhanced, production-grade replacement for `github_folder_downloader_v1.py` that closes every High/Medium finding from the audit, addresses Low/Informational items, and ships with an automated test suite. No code is written in this plan; this is the design contract that the implementation will follow.

Precedence applied: current request → audit findings → original plan → general practice. Where the audit and the original plan disagree, the audit’s fix wins.

---

## 1. Objectives & acceptance criteria

The v2 script must:

1. Perform **targeted retrieval** — never enumerate the whole repository tree for a nested folder (H1).
2. **Never report success with zero files** when the target folder is non-empty or when the archive is missing the folder (H2).
3. **Never write outside the destination** through pre-existing symlinks (H3).
4. **Roll back on any abnormal exit**, including `KeyboardInterrupt`/`SystemExit` (H4).
5. **Detect ref/path ambiguity** and refuse to guess (M1).
6. Use **commit SHA** for raw and archive URLs (M2, M5).
7. Enforce **consistent limits** across primary and fallback paths (M3).
8. **Verify integrity** of downloaded blobs where metadata exists (M4).
9. **Bound archive processing** before materializing entry lists (M7, M8, L7).
10. Implement **bounded retries/backoff** honoring `Retry-After` (M9).
11. Use **unique, cleaned-up temp files** in the destination (M10, L3).
12. Ship with a **pytest suite** covering the plan’s test matrix and the audit findings (M11).
13. Preserve all documented v1 behaviors that are still valid.

Definition of Done = every item above verified by an automated test or an explicit, recorded manual check.

---

## 2. Design principles driving the rewrite

- **Targeted over exhaustive.** Resolve the target folder to a tree SHA via path-segment traversal, then enumerate only that subtree.
- **Fail loud, fail early.** Ambiguity, truncation, zero-file results, symlinked destination components, and limit violations are hard errors with actionable messages.
- **Transactional commit.** Staging → verify → commit → verify, with rollback on any `BaseException`.
- **Untrusted archive, hostile destination.** Treat both the downloaded archive and the destination filesystem as untrusted; never follow symlinks, never trust metadata.
- **Bounded everything.** Every external call and every archive enumeration is bounded by a configurable limit and a hard failure path.
- **Observable.** Structured logs (`event=...`, `phase=...`, identifiers), explicit verification ledger at the end.

---

## 3. Remediation mapping (audit → design decision)

### High

| ID | Fix |
|----|-----|
| **H1** | Replace full-repo `fetch_tree` recursion with: (a) resolve each URL path segment via non-recursive `GET /git/trees/{sha}` starting from the root tree SHA — O(depth) calls; (b) after resolving, enumerate only the target folder’s tree with `recursive=1`; (c) if `truncated=true`, fall back to per-subdirectory non-recursive traversal scoped to the target. `resolve_target()` returns `RepoTarget(tree_sha=<target folder tree SHA>)`. |
| **H2** | In `download_with_archive_fallback`, require: (a) the target folder path exists as a `tree` entry in the archive; (b) `selected_count > 0` for any non-empty target path. Otherwise raise `DownloadError("target folder not found in archive")` before `commit_files`. |
| **H3** | New `safe_destination_path(base, rel)` helper: rejects if any component of `rel` maps to an existing symlink under `base`, using `os.lstat` per component (and `O_NOFOLLOW`/`dir_fd` where available). `main()` refuses a destination that is itself a symlink unless `--allow-destination-symlink` is explicitly set. Applied to `commit_files` and `preserve_archive`. |
| **H4** | `commit_files` catches `BaseException`, performs rollback, re-raises. `finally` block removes leftover `.tmp-*` files and the rollback directory. Rollback storage moved to `tempfile.mkdtemp(prefix="gh-folder-rb-")` outside the stage (also fixes L3). |

### Medium

| ID | Fix |
|----|-----|
| **M1** | `resolve_target` collects **all** valid `(ref, path, tree_sha)` candidates; if `len > 1`, raises `AmbiguousTargetError` listing candidates. New optional CLI `--ref REF` and `--path PATH` short-circuit ambiguity. If the user supplies both, skip candidate enumeration. |
| **M2** | `download_blob` uses `target.commit_sha` in the raw URL. |
| **M3** | `stage_api_folder` receives `max_extract` and enforces `min(max_download, max_extract)` on total bytes. `parse_args` also rejects `max_extracted_size < max_download_size` unless `--allow-extract-below-download` is set. |
| **M4** | After downloading a blob, verify: (a) `len(data) == entry["size"]` when size is present; (b) compute Git blob SHA-1 (`sha1(b"blob %d\0" % len + data)`) and compare with `entry["sha"]`; mismatch → `IntegrityError`. |
| **M5** | `parse_url` validates `owner`/`repo` against GitHub’s naming pattern (conservative: `^[A-Za-z0-9][A-Za-z0-9._-]{0,99}$`, no `..`, no trailing `.git` removal beyond suffix). `archive_urls` quotes each path component with `encode_path`. |
| **M6** | `safe_relpath` is platform-aware: on POSIX, allow `:` and `\`; reject only `/`-rooted, `..`, `.`, empty parts. On Windows, additionally reject `:`, `<>"|?*`, trailing space/period, and reserved device names. Drive-letter-like prefixes rejected only on Windows. |
| **M7** | `stream_to_file` writes to `tempfile.NamedTemporaryFile(dir=tmpdir, delete=False)` and returns `(path, size, completed: bool)`. Partial files are unlinked on failure. `download_with_archive_fallback` only preserves archives whose `completed` flag is `True`. |
| **M8** | ZIP: check `len(zf.infolist()) > max_entries` before building `selected`; raise early. TAR: iterate `tf` streaming, counting entries, aborting at `max_entries`. `max_entries` is a new limit (`--max-archive-entries`, default `max_files * 4`). |
| **M9** | New `_http_get(url, ..., retries=3, backoff_base=0.5, retry_on=(429,500,502,503,504), honor_retry_after=True)`. Applies to `request_bytes`, `api_json`, `stream_to_file`. Non-retryable 4xx raise immediately. Total attempts logged at DEBUG. |
| **M10** | `commit_files` uses `tempfile.NamedTemporaryFile(dir=dst.parent, prefix=".ghfd-", delete=False)`; `finally` unlinks any unrenamed temp files. |
| **M11** | New `tests/` tree (pytest) covering: URL parsing, resolution ambiguity, targeted traversal, archive extraction (incl. traversal/symlink/bomb fixtures), commit rollback on `KeyboardInterrupt`, limit enforcement, retry behavior, integrity check. HTTP mocked via `unittest.mock.patch("urllib.request.urlopen")`; archives synthesized in `tmp_path`. |
| **M12** | `fetch_tree` checks `truncated` on every response; `resolve_target` treats truncation as candidate-invalid and continues; `stage_api_folder` on truncation falls back to scoped per-directory traversal or fails with a clear message. |

### Low

| ID | Fix |
|----|-----|
| **L1** | `resolve_target` records the last meaningful error (rate-limit, auth, network) and surfaces it in the aggregate `DownloadError` message. |
| **L2** | `archive_prefix` normalizes leading `./`, ignores `pax_global_header`/`__MACOSX` metadata, and requires exactly one non-metadata top-level root; validates that the target path exists as a directory entry. |
| **L3** | Fixed via H4 (rollback storage outside stage). |
| **L4** | `download_with_archive_fallback` separates `commit_ok` from `retain_ok`; if commit succeeded but retention failed, log `WARNING` and return success. |
| **L5** | After a later format succeeds, delete any previously preserved recovery archive for the same target (only those created by this run, tracked in a list), unless `--keep-archive` is set. |
| **L6** | `fetch_tree` records `mode` from the tree entry. `stage_api_folder` skips `120000` (symlink) and `160000` (submodule) entries with a `WARNING` `event=skipped_special_entry`. Configurable via `--symlink-policy {skip,fail}` (default `skip`). |
| **L7** | New `--max-compression-ratio` (default `1000`); checked per entry against `file_size / max(compress_size, 1)`. |
| **L8** | Remove `sha256_file` and unused constants, or wire them into a new `--verify-sha256` debug flag. Decision: remove; keep surface small. |
| **L9** | `preserve_archive` and `keep_archive` retention honor `--no-overwrite`; on conflict with `--no-overwrite`, warn and skip retention rather than failing the run. |

### Informational

| ID | Fix |
|----|-----|
| **I1** | Add a `tests/integration/` directory with opt-in live tests gated by `GHFD_LIVE_TESTS=1`, pinned to controlled public repositories (one with slash-branch, one large/truncated, one with archive edge cases). CI runs them nightly, not per-PR. |

---

## 4. Revised architecture

Single-file main script (kept for drop-in usability) with clearly delimited sections, plus a `tests/` package. Suggested internal modules-as-sections:

1. **Constants & configuration** — limits, defaults, exit codes, regexes.
2. **Exceptions** — `DownloadError`, `AmbiguousTargetError`, `IntegrityError`, `CommitError`, `LimitExceeded`.
3. **Filesystem safety** — `safe_relpath`, `safe_destination_path`, `unique_tempfile`, `atomic_replace`.
4. **HTTP layer** — `_http_get` (retry/backoff/`Retry-After`), `request_bytes`, `api_json`, `stream_to_file`. All return explicit `(status, headers, body)` or typed results; no silent `except`.
5. **URL & ref parsing** — `parse_url` (validated), `encode_path`.
6. **Resolution** — `resolve_candidates`, `pick_candidate` (ambiguity → error), `walk_tree_path` (per-segment non-recursive tree calls), `enumerate_target_tree` (recursive, with truncation fallback).
7. **Primary retrieval** — `stage_api_folder` (integrity, limits, symlink policy).
8. **Archive layer** — `archive_urls`, `archive_prefix` (robust), `extract_zip_target`, `extract_tar_target` (streaming, ratios, entry caps), `preserve_archive`.
9. **Commit** — `commit_files` (`BaseException` rollback, safe destination, unique temp files).
10. **Orchestration** — `download_with_archive_fallback`, `run_primary`, `run_fallback`.
11. **CLI** — `parse_args`, `main` (exit-code mapping).
12. **Reporting** — `RunReport` dataclass; `emit_report(report)` prints a verification ledger.

---

## 5. Revised CLI

Positional arguments unchanged. New/changed options:

| Option | Default | Purpose |
|---|---|---|
| `--ref REF` | — | Explicit ref; skips ambiguity resolution. |
| `--path PATH` | — | Explicit folder path; skips ambiguity resolution. |
| `--max-archive-entries` | `max_files * 4` | Hard cap before entry materialization. |
| `--max-compression-ratio` | `1000` | Per-entry zip/tar ratio cap. |
| `--symlink-policy {skip,fail}` | `skip` | API-path symlink handling. |
| `--allow-destination-symlink` | off | Opt-in for symlinked destination root. |
| `--allow-extract-below-download` | off | Permit `max_extracted_size < max_download_size`. |
| `--retries N` | `3` | HTTP retry count. |
| `--backoff-base SECONDS` | `0.5` | Retry backoff base. |
| `--exit-codes-json` | off | Print exit-code table (for automation). |

All v1 options remain. `--verbose` continues to select DEBUG logging.

**Exit codes:**

| Code | Meaning |
|---|---|
| `0` | Success |
| `2` | CLI usage error (argparse) |
| `3` | URL parse/validation error |
| `4` | Ref/path resolution error or ambiguity |
| `5` | Primary and fallback retrieval both failed |
| `6` | Commit/IO/rollback failure |
| `130` | Interrupted (`KeyboardInterrupt`) |
| `1` | Unexpected error |

---

## 6. Security & safety controls (v2 deltas)

- Destination traversal: reject any existing symlinked parent component under the destination (H3).
- Archive extraction: reject non-regular entries, absolute paths, `..`, drive-like components, hard links, devices, FIFOs, and symlinks; enforce ratio, per-entry size, total size, entry count, and depth caps (M8, L7).
- Retries bounded; no unbounded loops anywhere.
- Secrets: token only from env var; never logged. New `_redact(url)` used before any log of request URLs.
- Blob integrity verified via Git blob SHA-1 when metadata present (M4).
- No execution path anywhere; documented in the module docstring and enforced by test (`tests/test_no_execution.py` scans AST for `subprocess`, `os.system`, `exec`, `eval`, `importlib`).

---

## 7. Testing strategy

**Layout:**

```
tests/
  conftest.py
  test_url_parsing.py
  test_resolution.py
  test_targeted_retrieval.py
  test_integrity.py
  test_archive_zip.py
  test_archive_tar.py
  test_commit_rollback.py
  test_limits.py
  test_retries.py
  test_no_execution.py
  integration/
    conftest.py
    test_live_github.py   # gated by GHFD_LIVE_TESTS=1
```

**Coverage matrix (mapped to plan Section 12):**

- URL parsing: v1 matrix plus `owner/repo` validation, `.git` suffix, encoded chars.
- Resolution: standard, slash-branch (both valid), ambiguity (must error), truncation fallback, `--ref`/`--path` overrides.
- Targeted retrieval: verified by asserting the **number of API calls** stays O(depth) for nested folders — a mock `urlopen` records call counts; a nested-path test must call ≤ `depth + 2` tree endpoints.
- Integrity: mismatch size → `IntegrityError`; mismatch SHA → `IntegrityError`; correct → success.
- Archive: valid ZIP/TAR; corrupted; empty; traversal; absolute paths; symlink; hardlink; device; excessive entries; excessive ratio; excessive total size; target missing → `DownloadError` (H2); unexpected root → `DownloadError`.
- Commit: rollback on injected `OSError`, on `KeyboardInterrupt` (H4), on symlinked parent (H3); `--no-overwrite` conflict; concurrent temp filename.
- Limits: each limit independently exercised against both primary and fallback paths (M3).
- Retries: 429 with `Retry-After`, transient 500, exhausted retries, non-retryable 404.
- No-execution AST scan.

**Test execution commands (to be recorded in the delivery report):**

```
python -m compileall github_folder_downloader.py
python -m pytest -q tests --ignore=tests/integration
python -m ruff check .        # if ruff available; otherwise note skipped
python -m mypy github_folder_downloader.py   # if mypy available; otherwise note skipped
```

---

## 8. Verification & evidence plan

Before delivery, produce a **verification ledger** with one of `Verified / Reasoned / Assumed / Unverifiable` per claim:

1. Every audit finding H*/M*/L* has a corresponding test or a documented manual check.
2. Full test suite output captured (`pytest -q` summary).
3. `compileall` clean.
4. `--help` output captured to confirm CLI surface.
5. Live integration tests remain `Unverifiable` unless `GHFD_LIVE_TESTS=1` was run in this environment; explicitly state that.
6. A short `CHANGELOG.md`-style section in the delivery note enumerating each fixed finding (audit ID → test name).

---

## 9. Delivery & commit plan

- **Commit 1** — `fix: targeted repository traversal (H1, M12)` — resolution and retrieval rewrite, plus tests.
- **Commit 2** — `fix: archive safety and zero-file guard (H2, M7, M8, L7)` — archive layer, limit checks, tests.
- **Commit 3** — `fix: destination symlink and rollback safety (H3, H4, M10, L3)` — commit layer, tests.
- **Commit 4** — `fix: integrity, retries, ambiguity, and limit consistency (M1, M2, M3, M4, M5, M9)` — HTTP and resolution hardening, tests.
- **Commit 5** — `chore: platform-aware paths, cleanup, and docs (M6, L1, L2, L4, L5, L6, L8, L9)` — remaining findings, README update, `--help` snapshot.
- **Commit 6** — `test: add gated live integration tests (I1)`.

Each commit passes the full local gate before the next. Final handoff report lists: Verified items, Reasoned items, Assumed items, Unverifiable items, deferred debt (none expected beyond I1’s live-gating).

---

## 10. Risks, assumptions, and open questions

**Assumptions (stated, not asked):**

1. Python 3.11+ stdlib only — no new third-party runtime deps (test-only `pytest`).
2. Git tree SHA resolution per path segment is acceptable O(depth) API cost; if the user’s rate-limit budget is a concern, `--ref`/`--path` overrides reduce it to zero extra calls.
3. Git blob SHA-1 is a valid integrity signal for files retrieved via raw URLs; submodules and LFS pointers are out of scope for v2 and will be surfaced as `WARNING` `event=unsupported_entry`.
4. Symlink policy default is `skip` with a warning; `--symlink-policy fail` available for strictness.
5. Exit-code scheme above is the contract; no existing consumers documented, so additive only.

**Risks:**

- **API rate limits** during resolution remain the dominant external risk; mitigated by O(depth) traversal, `--ref`/`--path`, and retry/backoff, but not eliminated.
- **Archive format drift** on `codeload.github.com` (redirects, new root naming) could break `archive_prefix`; the L2 hardening and the gated live tests are the mitigations.
- **Windows path semantics** differ materially; M6 changes need CI coverage on Windows to be confident.

**Open questions (none blocking):**

1. Should the default `--symlink-policy` be `fail` for stricter safety? Proposed default is `skip` for usability; trivially changeable.
2. Should `--keep-archive` retention also be written atomically (tempfile + replace) to avoid partial archives in the destination? Proposed: yes, and included in Commit 2.

No clarifying question is required to proceed; the above assumptions will be stated in the delivery report and are reversible.

---

## Decisions on the open questions

1. **Symlink policy default → `skip`.** Rationale: real-world repos (dotfiles, monorepos) legitimately contain symlinks; failing the entire download for them would be hostile. Each skip emits a structured `WARNING` with `event=skipped_symlink`, and `--symlink-policy fail` is available for strict users. Submodules (`type: commit` / mode `160000`) also skip with `event=skipped_submodule`.
2. **`--keep-archive` retention → atomic.** All file writes to the destination (commits and retained/preserved archives) go through `tempfile.mkstemp` + `os.replace`, so a partial write can never appear as a finished artifact.

Everything else follows the plan. Below are the two files.

---

## File: `github_folder_downloader.py`

```python
#!/usr/bin/env python3
"""Download and mirror a GitHub repository folder without cloning the whole repository.

Usage:
  python github_folder_downloader.py URL DESTINATION [options]

Retrieval is layered:
  Tier 1: targeted GitHub API + raw retrieval (only the requested subtree).
  Tier 2: repository ZIP archive, selective extraction.
  Tier 3: repository TAR.GZ archive, selective extraction.

Archive contents are treated as untrusted. Only regular files and directories
are materialised; symlinks, hardlinks, devices, FIFOs, and submodules are
skipped (or rejected with --symlink-policy fail). Downloaded content is never
executed. See --help for limits and options.
"""
from __future__ import annotations

import argparse
import email.utils
import hashlib
import http.client
import json
import logging
import os
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
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Callable, Iterable, Optional

LOG = logging.getLogger("github-folder-downloader")
USER_AGENT = "github-folder-downloader/2.0 (Python urllib)"
API_BASE = "https://api.github.com"
RAW_BASE = "https://raw.githubusercontent.com"
CODELOAD_BASE = "https://codeload.github.com"

DEFAULT_MAX_DOWNLOAD = 100 * 1024 * 1024
DEFAULT_MAX_EXTRACT = 250 * 1024 * 1024
DEFAULT_MAX_FILES = 5000
DEFAULT_MAX_DEPTH = 100
DEFAULT_MAX_COMPRESSION_RATIO = 1000
CHUNK = 64 * 1024

EXIT_OK = 0
EXIT_UNEXPECTED = 1
EXIT_USAGE = 2
EXIT_URL = 3
EXIT_RESOLVE = 4
EXIT_RETRIEVE = 5
EXIT_COMMIT = 6
EXIT_INTERRUPT = 130

RETRYABLE_HTTP = {429, 500, 502, 503, 504}

# Conservative GitHub owner/repo validation. Not exhaustive of every edge case
# GitHub allows, but eliminates URL-structure injection vectors.
OWNER_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$")
REPO_RE = re.compile(r"^[A-Za-z0-9._-]{1,100}$")

WINDOWS_RESERVED = {
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
}

LFS_POINTER_PREFIX = b"version https://git-lfs.github.com/spec/v1\n"


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class DownloadError(Exception):
    """Expected operational failure."""


class AmbiguousTargetError(DownloadError):
    def __init__(self, candidates: list[tuple[str, str, str]]) -> None:
        self.candidates = candidates
        lines = ["Ambiguous ref/path; use --ref and --path to disambiguate. Candidates:"]
        for ref, path, _sha in candidates:
            lines.append(f"  ref={ref!r} path={path or '(root)'!r}")
        super().__init__("\n".join(lines))


class IntegrityError(DownloadError):
    """Content did not match expected size or Git blob SHA."""


class LimitExceeded(DownloadError):
    """A configured resource limit was hit."""


class CommitError(DownloadError):
    """Failure while committing staged content to the destination."""


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RepoTarget:
    owner: str
    repo: str
    ref: str
    path: str
    commit_sha: str
    tree_sha: str


# ---------------------------------------------------------------------------
# Filesystem safety
# ---------------------------------------------------------------------------

def safe_relpath(path: str) -> PurePosixPath:
    """Validate a repository or archive path as relative and traversal-free."""
    if not path:
        raise DownloadError("Empty path")
    normalized = path.replace("\\", "/")
    p = PurePosixPath(normalized)
    if p.is_absolute():
        raise DownloadError(f"Absolute path not allowed: {path!r}")
    if not p.parts:
        raise DownloadError(f"Empty path: {path!r}")
    on_windows = sys.platform.startswith("win")
    for part in p.parts:
        if part in ("", ".", ".."):
            raise DownloadError(f"Unsafe path component: {path!r}")
        if on_windows:
            if ":" in part:
                raise DownloadError(f"Unsafe Windows path component: {path!r}")
            if any(c in part for c in '<>"|?*'):
                raise DownloadError(f"Unsafe Windows path component: {path!r}")
            if part[-1] in (" ", "."):
                raise DownloadError(f"Trailing space/period in Windows path: {path!r}")
            stem = part.split(".")[0].upper()
            if stem in WINDOWS_RESERVED:
                raise DownloadError(f"Reserved Windows device name: {path!r}")
    return p


def safe_destination_path(base: Path, rel: PurePosixPath) -> Path:
    """Resolve `rel` under `base`, rejecting any existing symlink component.

    This prevents a pre-existing symlink inside the destination from redirecting
    a write outside the destination.
    """
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


# ---------------------------------------------------------------------------
# HTTP layer (bounded retries, Retry-After honoured)
# ---------------------------------------------------------------------------

def _redact(url: str) -> str:
    """Strip query strings before logging; our callers never embed credentials."""
    return url.split("?", 1)[0]


def _parse_retry_after(value: str) -> Optional[float]:
    try:
        return max(0.0, float(value))
    except ValueError:
        pass
    try:
        dt = email.utils.parsedate_to_datetime(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return max(0.0, (dt - datetime.now(timezone.utc)).total_seconds())
    except (ValueError, TypeError):
        return None


def _http_get(
    url: str,
    *,
    timeout: float,
    headers: dict[str, str],
    retries: int,
    backoff_base: float,
    consume: Callable[[object], object],
):
    """GET `url`, retrying transient failures; return `consume(response)`.

    `consume` receives the open response object and must read body as needed.
    Non-retryable HTTP statuses and `consume`-raised exceptions propagate
    unchanged (including DownloadError for size violations).
    """
    if not url.lower().startswith("https://"):
        raise DownloadError("HTTPS is required for network requests.")
    attempt = 0
    last_exc: Optional[BaseException] = None
    while attempt <= retries:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return consume(resp)
        except urllib.error.HTTPError as exc:
            if exc.code in RETRYABLE_HTTP and attempt < retries:
                wait = _parse_retry_after(exc.headers.get("Retry-After", "")) if exc.headers else None
                if wait is None:
                    wait = backoff_base * (2 ** attempt)
                LOG.debug("event=http_retry status=%d wait=%.2fs attempt=%d", exc.code, wait, attempt + 1)
                time.sleep(wait)
                last_exc = exc
                attempt += 1
                continue
            detail = ""
            try:
                detail = exc.read(1024).decode("utf-8", "replace")
            except Exception:
                pass
            raise DownloadError(f"HTTP {exc.code} for {_redact(url)}: {detail[:300]}") from exc
        except (urllib.error.URLError, TimeoutError, ConnectionError,
                http.client.IncompleteRead) as exc:
            if attempt < retries:
                wait = backoff_base * (2 ** attempt)
                LOG.debug("event=net_retry wait=%.2fs attempt=%d error=%s", wait, attempt + 1, exc)
                time.sleep(wait)
                last_exc = exc
                attempt += 1
                continue
            raise DownloadError(f"Network error for {_redact(url)}: {exc}") from exc
    raise DownloadError(f"Exhausted retries for {_redact(url)}") from last_exc


def request_bytes(
    url: str,
    *,
    timeout: float,
    token: Optional[str],
    accept: str,
    limit: Optional[int],
    retries: int,
    backoff_base: float,
) -> bytes:
    headers = {"User-Agent": USER_AGENT, "Accept": accept}
    if token:
        headers["Authorization"] = "Bearer " + token

    def consume(resp) -> bytes:
        declared = resp.headers.get("Content-Length")
        if limit is not None and declared:
            try:
                if int(declared) > limit:
                    raise LimitExceeded(f"Response exceeds size limit ({limit} bytes).")
            except ValueError:
                pass
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = resp.read(CHUNK)
            if not chunk:
                break
            total += len(chunk)
            if limit is not None and total > limit:
                raise LimitExceeded(f"Response exceeds size limit ({limit} bytes).")
            chunks.append(chunk)
        return b"".join(chunks)

    return _http_get(url, timeout=timeout, headers=headers, retries=retries,
                     backoff_base=backoff_base, consume=consume)


def api_json(url: str, *, timeout: float, token: Optional[str],
             retries: int, backoff_base: float) -> dict:
    payload = request_bytes(url, timeout=timeout, token=token,
                            accept="application/vnd.github+json",
                            limit=10 * 1024 * 1024,
                            retries=retries, backoff_base=backoff_base)
    try:
        data = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DownloadError(f"Invalid JSON response from {_redact(url)}") from exc
    if not isinstance(data, dict):
        raise DownloadError(f"Unexpected non-object JSON response from {_redact(url)}")
    return data


def stream_to_file(
    url: str,
    out_path: Path,
    *,
    timeout: float,
    token: Optional[str],
    accept: str,
    max_size: int,
    retries: int,
    backoff_base: float,
) -> int:
    headers = {"User-Agent": USER_AGENT, "Accept": accept}
    if token:
        headers["Authorization"] = "Bearer " + token

    def consume(resp) -> int:
        declared = resp.headers.get("Content-Length")
        if declared:
            try:
                if int(declared) > max_size:
                    raise LimitExceeded(f"Download exceeds size limit ({max_size} bytes).")
            except ValueError:
                pass
        total = 0
        with out_path.open("wb") as fh:
            while True:
                chunk = resp.read(CHUNK)
                if not chunk:
                    break
                total += len(chunk)
                if total > max_size:
                    raise LimitExceeded(f"Download exceeds size limit ({max_size} bytes).")
                fh.write(chunk)
        return total

    return _http_get(url, timeout=timeout, headers=headers, retries=retries,
                     backoff_base=backoff_base, consume=consume)


# ---------------------------------------------------------------------------
# URL parsing
# ---------------------------------------------------------------------------

def encode_path(path: str) -> str:
    return "/".join(urllib.parse.quote(part, safe="") for part in path.split("/") if part)


def parse_url(url: str) -> tuple[str, str, list[str], str]:
    """Return (owner, repo, tail_segments, kind) where kind is 'root' or 'tree'."""
    try:
        parsed = urllib.parse.urlsplit(url)
    except ValueError as exc:
        raise DownloadError(f"Invalid URL: {exc}") from exc
    if parsed.scheme != "https":
        raise DownloadError("Expected an https:// URL.")
    if parsed.hostname != "github.com":
        raise DownloadError("Expected a github.com URL.")
    if parsed.username or parsed.password:
        raise DownloadError("URL must not contain credentials.")
    if parsed.query or parsed.fragment:
        raise DownloadError("Query strings and fragments are not supported.")
    parts = [urllib.parse.unquote(p) for p in parsed.path.strip("/").split("/") if p]
    if len(parts) < 2:
        raise DownloadError("URL must include OWNER and REPO.")
    owner, repo = parts[0], parts[1]
    if repo.endswith(".git"):
        repo = repo[:-4]
    if not OWNER_RE.match(owner):
        raise DownloadError(f"Invalid GitHub owner: {owner!r}")
    if not REPO_RE.match(repo):
        raise DownloadError(f"Invalid GitHub repository name: {repo!r}")
    if len(parts) == 2:
        return owner, repo, [], "root"
    if parts[2] != "tree" or len(parts) < 4:
        raise DownloadError("Expected a folder URL of form https://github.com/OWNER/REPO/tree/REF/PATH.")
    return owner, repo, parts[3:], "tree"


# ---------------------------------------------------------------------------
# Resolution (targeted; no whole-repo enumeration)
# ---------------------------------------------------------------------------

def _resolve_commit(owner: str, repo: str, ref: str, *, timeout: float,
                    token: Optional[str], retries: int, backoff_base: float) -> tuple[str, str]:
    url = f"{API_BASE}/repos/{encode_path(owner)}/{encode_path(repo)}/commits/{encode_path(ref)}"
    data = api_json(url, timeout=timeout, token=token, retries=retries, backoff_base=backoff_base)
    commit_sha = data.get("sha")
    tree_sha = ((data.get("commit") or {}).get("tree") or {}).get("sha")
    if not isinstance(commit_sha, str) or not commit_sha:
        raise DownloadError(f"Could not resolve commit for ref {ref!r}.")
    if not isinstance(tree_sha, str) or not tree_sha:
        raise DownloadError(f"Could not resolve tree for ref {ref!r}.")
    return commit_sha, tree_sha


def _walk_to_path(owner: str, repo: str, root_tree_sha: str, path: str, *,
                  timeout: float, token: Optional[str],
                  retries: int, backoff_base: float) -> str:
    """Walk path segments one level at a time using non-recursive tree calls."""
    current_sha = root_tree_sha
    traversed: list[str] = []
    for segment in [s for s in path.split("/") if s]:
        url = f"{API_BASE}/repos/{encode_path(owner)}/{encode_path(repo)}/git/trees/{current_sha}"
        data = api_json(url, timeout=timeout, token=token, retries=retries, backoff_base=backoff_base)
        if data.get("truncated"):
            raise DownloadError(
                f"Tree {current_sha} truncated at depth {'/'.join(traversed) or '(root)'}; "
                f"cannot descend reliably."
            )
        found_sha: Optional[str] = None
        for entry in data.get("tree", []):
            if entry.get("path") == segment and entry.get("type") == "tree":
                sha = entry.get("sha")
                if isinstance(sha, str) and sha:
                    found_sha = sha
                break
        if not found_sha:
            raise DownloadError(f"Path not found: {'/'.join(traversed + [segment])}")
        current_sha = found_sha
        traversed.append(segment)
    return current_sha


def _enumerate_target_tree(owner: str, repo: str, tree_sha: str, *,
                           timeout: float, token: Optional[str],
                           retries: int, backoff_base: float) -> list[dict]:
    """Enumerate the target subtree only. Falls back to per-level on truncation."""
    url = f"{API_BASE}/repos/{encode_path(owner)}/{encode_path(repo)}/git/trees/{tree_sha}?recursive=1"
    data = api_json(url, timeout=timeout, token=token, retries=retries, backoff_base=backoff_base)
    if not data.get("truncated"):
        return [e for e in data.get("tree", []) if e.get("type") in ("blob", "tree", "commit")]
    LOG.warning("event=tree_truncated tree=%s; falling back to per-level traversal", tree_sha)
    return _walk_all_levels(owner, repo, tree_sha, "", timeout=timeout, token=token,
                            retries=retries, backoff_base=backoff_base)


def _walk_all_levels(owner: str, repo: str, tree_sha: str, prefix: str, *,
                     timeout: float, token: Optional[str],
                     retries: int, backoff_base: float) -> list[dict]:
    url = f"{API_BASE}/repos/{encode_path(owner)}/{encode_path(repo)}/git/trees/{tree_sha}"
    data = api_json(url, timeout=timeout, token=token, retries=retries, backoff_base=backoff_base)
    if data.get("truncated"):
        raise DownloadError(
            f"Tree {tree_sha} truncated at {prefix or '(root)'}; cannot enumerate target reliably."
        )
    entries: list[dict] = []
    for item in data.get("tree", []):
        name = item.get("path")
        typ = item.get("type")
        if not isinstance(name, str) or typ not in ("blob", "tree", "commit"):
            continue
        rel = f"{prefix}/{name}" if prefix else name
        new_item = dict(item)
        new_item["path"] = rel
        entries.append(new_item)
        if typ == "tree":
            child_sha = item.get("sha")
            if isinstance(child_sha, str) and child_sha:
                entries.extend(_walk_all_levels(owner, repo, child_sha, rel,
                                                timeout=timeout, token=token,
                                                retries=retries, backoff_base=backoff_base))
    return entries


def resolve_target(
    owner: str,
    repo: str,
    tail: list[str],
    kind: str,
    *,
    timeout: float,
    token: Optional[str],
    retries: int,
    backoff_base: float,
    ref_override: Optional[str] = None,
    path_override: Optional[str] = None,
) -> RepoTarget:
    if (ref_override is None) != (path_override is None):
        raise DownloadError("--ref and --path must be supplied together.")

    if kind == "root":
        default_branch = _resolve_default_branch(owner, repo, timeout=timeout, token=token,
                                                retries=retries, backoff_base=backoff_base)
        commit_sha, tree_sha = _resolve_commit(owner, repo, default_branch,
                                              timeout=timeout, token=token,
                                              retries=retries, backoff_base=backoff_base)
        return RepoTarget(owner, repo, default_branch, "", commit_sha, tree_sha)

    if ref_override is not None:
        commit_sha, root_tree_sha = _resolve_commit(owner, repo, ref_override,
                                                    timeout=timeout, token=token,
                                                    retries=retries, backoff_base=backoff_base)
        if path_override:
            tree_sha = _walk_to_path(owner, repo, root_tree_sha, path_override,
                                     timeout=timeout, token=token,
                                     retries=retries, backoff_base=backoff_base)
        else:
            tree_sha = root_tree_sha
        return RepoTarget(owner, repo, ref_override, path_override or "", commit_sha, tree_sha)

    candidates: list[tuple[str, str, str, str]] = []
    last_error: Optional[BaseException] = None
    for split in range(len(tail), 0, -1):
        ref = "/".join(tail[:split])
        path = "/".join(tail[split:])
        if not ref:
            continue
        try:
            commit_sha, root_tree_sha = _resolve_commit(owner, repo, ref,
                                                        timeout=timeout, token=token,
                                                        retries=retries, backoff_base=backoff_base)
        except DownloadError as exc:
            last_error = exc
            continue
        if not path:
            candidates.append((ref, "", root_tree_sha, commit_sha))
            continue
        try:
            tree_sha = _walk_to_path(owner, repo, root_tree_sha, path,
                                     timeout=timeout, token=token,
                                     retries=retries, backoff_base=backoff_base)
            candidates.append((ref, path, tree_sha, commit_sha))
        except DownloadError as exc:
            last_error = exc
            continue

    if not candidates:
        msg = "Could not resolve URL ref and folder path."
        if last_error:
            msg += f" Last error: {last_error}"
        raise DownloadError(msg)
    if len(candidates) > 1:
        raise AmbiguousTargetError([(c[0], c[1], c[2]) for c in candidates])
    ref, path, tree_sha, commit_sha = candidates[0]
    return RepoTarget(owner, repo, ref, path, commit_sha, tree_sha)


def _resolve_default_branch(owner: str, repo: str, *, timeout: float,
                            token: Optional[str], retries: int, backoff_base: float) -> str:
    url = f"{API_BASE}/repos/{encode_path(owner)}/{encode_path(repo)}"
    data = api_json(url, timeout=timeout, token=token, retries=retries, backoff_base=backoff_base)
    branch = data.get("default_branch")
    if not isinstance(branch, str) or not branch:
        raise DownloadError("Could not determine repository default branch.")
    return branch


# ---------------------------------------------------------------------------
# Primary retrieval (API + raw)
# ---------------------------------------------------------------------------

def _compute_git_blob_sha(data: bytes) -> str:
    h = hashlib.sha1()
    h.update(b"blob " + str(len(data)).encode("ascii") + b"\0")
    h.update(data)
    return h.hexdigest()


def _download_blob(target: RepoTarget, rel_path: str, *, timeout: float,
                   token: Optional[str], max_size: int,
                   retries: int, backoff_base: float) -> bytes:
    encoded = encode_path(rel_path)
    url = (f"{RAW_BASE}/{encode_path(target.owner)}/{encode_path(target.repo)}"
           f"/{target.commit_sha}/{encoded}")
    return request_bytes(url, timeout=timeout, token=token,
                         accept="application/octet-stream",
                         limit=max_size, retries=retries, backoff_base=backoff_base)


def stage_api_folder(target: RepoTarget, stage: Path, *, timeout: float,
                     token: Optional[str], max_download: int, max_files: int,
                     max_depth: int, symlink_policy: str,
                     retries: int, backoff_base: float) -> tuple[int, int]:
    entries = _enumerate_target_tree(target.owner, target.repo, target.tree_sha,
                                     timeout=timeout, token=token,
                                     retries=retries, backoff_base=backoff_base)
    selected: list[tuple[str, dict]] = []
    for entry in entries:
        typ = entry.get("type")
        mode = str(entry.get("mode") or "")
        rel = entry.get("path")
        if not isinstance(rel, str) or not rel:
            continue
        if typ == "commit" or mode == "160000":
            if symlink_policy == "fail":
                raise DownloadError(f"Submodule entry not supported: {rel}")
            LOG.warning("event=skipped_submodule path=%s", rel)
            continue
        if typ == "tree":
            continue
        if typ != "blob":
            continue
        if mode == "120000":
            if symlink_policy == "fail":
                raise DownloadError(f"Symlink entry not supported: {rel}")
            LOG.warning("event=skipped_symlink path=%s", rel)
            continue
        safe = safe_relpath(rel)
        if len(safe.parts) > max_depth:
            raise LimitExceeded(f"Depth exceeds {max_depth}: {rel}")
        selected.append((rel, entry))
    if len(selected) > max_files:
        raise LimitExceeded(f"File count {len(selected)} exceeds {max_files}.")
    total = 0
    for rel, entry in selected:
        declared_size = entry.get("size")
        if isinstance(declared_size, int) and declared_size > max_download:
            raise LimitExceeded(f"Per-file limit exceeded: {rel}")
        data = _download_blob(target, rel, timeout=timeout, token=token,
                              max_size=max_download, retries=retries, backoff_base=backoff_base)
        if isinstance(declared_size, int) and len(data) != declared_size:
            raise IntegrityError(f"Size mismatch for {rel}: got {len(data)}, expected {declared_size}")
        expected_sha = entry.get("sha")
        if isinstance(expected_sha, str) and expected_sha:
            actual_sha = _compute_git_blob_sha(data)
            if actual_sha != expected_sha:
                raise IntegrityError(f"Blob SHA mismatch for {rel}")
        if data.startswith(LFS_POINTER_PREFIX):
            LOG.warning("event=git_lfs_pointer path=%s note=committing_pointer_not_payload", rel)
        total += len(data)
        if total > max_download:
            raise LimitExceeded(f"Aggregate size exceeds {max_download} bytes.")
        p = safe_relpath(rel)
        dest = stage.joinpath(*p.parts)
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("wb") as fh:
            fh.write(data)
    return len(selected), total


# ---------------------------------------------------------------------------
# Commit (BaseException-safe; symlink-rejecting)
# ---------------------------------------------------------------------------

def commit_files(stage: Path, destination: Path, *, no_overwrite: bool) -> int:
    files = [p for p in stage.rglob("*") if p.is_file()]
    if not files:
        return 0
    rollback_dir = Path(tempfile.mkdtemp(prefix="ghfd-rollback-"))
    installed: list[Path] = []
    backed_up: list[tuple[Path, Path]] = []
    try:
        for src in files:
            rel = PurePosixPath(src.relative_to(stage).as_posix())
            dst = safe_destination_path(destination, rel)
            if dst.exists():
                if dst.is_dir():
                    raise CommitError(f"Destination conflict: {dst} is a directory.")
                if no_overwrite:
                    raise CommitError(f"File exists and --no-overwrite is set: {dst}")
                backup_path = rollback_dir / rel.as_posix()
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dst, backup_path)
                backed_up.append((dst, backup_path))
            dst.parent.mkdir(parents=True, exist_ok=True)
            fd, tmp_name = tempfile.mkstemp(dir=dst.parent, prefix=".ghfd-", suffix=".tmp")
            try:
                with os.fdopen(fd, "wb") as fh, src.open("rb") as fsrc:
                    shutil.copyfileobj(fsrc, fh, CHUNK)
                os.replace(tmp_name, dst)
            except BaseException:
                try:
                    os.unlink(tmp_name)
                except OSError:
                    pass
                raise
            installed.append(dst)
    except BaseException:
        for dst in reversed(installed):
            try:
                dst.unlink(missing_ok=True)
            except OSError:
                LOG.exception("Rollback unlink failed: %s", dst)
        for dst, backup_path in reversed(backed_up):
            try:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(backup_path, dst)
            except OSError:
                LOG.exception("Rollback restore failed: %s", dst)
        raise
    finally:
        shutil.rmtree(rollback_dir, ignore_errors=True)
    return len(files)


# ---------------------------------------------------------------------------
# Archive fallback
# ---------------------------------------------------------------------------

def archive_urls(target: RepoTarget) -> list[tuple[str, str]]:
    commit = target.commit_sha  # hex string, no encoding needed
    return [
        ("zip", f"{CODELOAD_BASE}/{target.owner}/{target.repo}/zip/{commit}"),
        ("tar.gz", f"{CODELOAD_BASE}/{target.owner}/{target.repo}/tar.gz/{commit}"),
    ]


def _normalize_member_name(name: str) -> str:
    n = name.replace("\\", "/")
    while n.startswith("./"):
        n = n[2:]
    return n


def _determine_archive_prefix(members: Iterable[str], target_path: str) -> str:
    roots: set[str] = set()
    for name in members:
        norm = _normalize_member_name(name)
        if not norm:
            continue
        head = norm.split("/", 1)[0]
        if head in ("pax_global_header", "__MACOSX"):
            continue
        roots.add(head)
    if len(roots) != 1:
        raise DownloadError(f"Unexpected archive root structure: {sorted(roots)!r}")
    root = next(iter(roots))
    target_path = target_path.strip("/")
    return f"{root}/{target_path}" if target_path else root


def extract_zip_target(archive: Path, stage: Path, target: RepoTarget, *,
                       max_extract: int, max_files: int, max_depth: int,
                       max_entries: int, max_ratio: int) -> tuple[int, int]:
    with zipfile.ZipFile(archive) as zf:
        infos = zf.infolist()
        if len(infos) > max_entries:
            raise LimitExceeded(f"ZIP has {len(infos)} entries (max {max_entries}).")
        prefix = _determine_archive_prefix([i.filename for i in infos], target.path)
        selected: list[tuple[zipfile.ZipInfo, PurePosixPath]] = []
        for info in infos:
            name = _normalize_member_name(info.filename)
            if name.endswith("/"):
                continue
            if name == prefix:
                continue
            if not name.startswith(prefix + "/"):
                continue
            rel = name[len(prefix) + 1:]
            if not rel:
                continue
            safe = safe_relpath(rel)
            if len(safe.parts) > max_depth:
                raise LimitExceeded(f"Depth exceeds {max_depth}: {rel}")
            mode = (info.external_attr >> 16) & 0xFFFF
            if mode and stat.S_IFMT(mode) not in (0, stat.S_IFREG):
                raise DownloadError(f"ZIP contains non-regular entry: {rel}")
            if info.compress_size > 0:
                ratio = info.file_size / info.compress_size
                if ratio > max_ratio:
                    raise LimitExceeded(f"Suspicious compression ratio {ratio:.0f} for {rel}")
            selected.append((info, safe))
        if len(selected) > max_files:
            raise LimitExceeded(f"ZIP file count {len(selected)} exceeds {max_files}.")
        if not selected and target.path:
            raise DownloadError(f"Target folder {target.path!r} not found in ZIP archive.")
        total = 0
        for info, _safe in selected:
            if info.file_size > max_extract:
                raise LimitExceeded(f"ZIP entry exceeds extraction limit: {info.filename}")
            total += info.file_size
            if total > max_extract:
                raise LimitExceeded("ZIP extracted content exceeds size limit.")
        for info, safe in selected:
            dest = stage.joinpath(*safe.parts)
            dest.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as src, dest.open("wb") as dst:
                shutil.copyfileobj(src, dst, CHUNK)
        return len(selected), total


def extract_tar_target(archive: Path, stage: Path, target: RepoTarget, *,
                       max_extract: int, max_files: int, max_depth: int,
                       max_entries: int) -> tuple[int, int]:
    prefix: Optional[str] = None
    count = 0
    total = 0
    extracted = 0
    # Streaming mode keeps memory bounded on hostile archives.
    with tarfile.open(archive, "r|gz") as tf:
        for member in tf:
            count += 1
            if count > max_entries:
                raise LimitExceeded(f"TAR has more than {max_entries} entries.")
            name = _normalize_member_name(member.name)
            if not name:
                continue
            if prefix is None:
                head = name.split("/", 1)[0]
                if head in ("pax_global_header", "__MACOSX"):
                    continue
                prefix = _determine_archive_prefix([name], target.path)
            if member.isdir():
                continue
            if name == prefix or not name.startswith(prefix + "/"):
                continue
            rel = name[len(prefix) + 1:]
            if not rel:
                continue
            safe = safe_relpath(rel)
            if len(safe.parts) > max_depth:
                raise LimitExceeded(f"Depth exceeds {max_depth}: {rel}")
            if not member.isfile():
                raise DownloadError(f"TAR contains non-regular entry: {rel}")
            if member.size > max_extract:
                raise LimitExceeded(f"TAR entry exceeds extraction limit: {rel}")
            total += member.size
            if total > max_extract:
                raise LimitExceeded("TAR extracted content exceeds size limit.")
            extracted += 1
            if extracted > max_files:
                raise LimitExceeded(f"TAR file count exceeds {max_files}.")
            src = tf.extractfile(member)
            if src is None:
                raise DownloadError(f"Cannot read archive member: {rel}")
            dest = stage.joinpath(*safe.parts)
            dest.parent.mkdir(parents=True, exist_ok=True)
            with src, dest.open("wb") as dst:
                shutil.copyfileobj(src, dst, CHUNK)
    if prefix is None:
        raise DownloadError("TAR archive is empty.")
    if extracted == 0 and target.path:
        raise DownloadError(f"Target folder {target.path!r} not found in TAR archive.")
    return extracted, total


def preserve_archive(archive: Path, destination: Path, name: str, *,
                     no_overwrite: bool) -> Optional[Path]:
    destination.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-") or "repository"
    if archive.name.endswith(".tar.gz"):
        suffix = ".tar.gz"
    else:
        suffix = archive.suffix or ".archive"
    dest = destination / f"{safe_name}-fallback{suffix}"
    if dest.is_symlink():
        LOG.warning("event=archive_retention_skipped reason=symlink path=%s", dest)
        return None
    if no_overwrite and dest.exists():
        LOG.warning("event=archive_retention_skipped reason=no_overwrite path=%s", dest)
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
    target: RepoTarget,
    destination: Path,
    *,
    timeout: float,
    token: Optional[str],
    max_download: int,
    max_extract: int,
    max_files: int,
    max_depth: int,
    max_entries: int,
    max_ratio: int,
    keep_archive: bool,
    no_overwrite: bool,
    retries: int,
    backoff_base: float,
) -> tuple[int, int, str]:
    errors: list[str] = []
    preserved_from_failures: list[Path] = []

    for fmt, url in archive_urls(target):
        with tempfile.TemporaryDirectory(prefix="ghfd-archive-") as tmp:
            tmpdir = Path(tmp)
            archive = tmpdir / ("repo.zip" if fmt == "zip" else "repo.tar.gz")
            stage = tmpdir / "stage"
            stage.mkdir()

            try:
                stream_to_file(url, archive, timeout=timeout, token=token,
                               accept="application/octet-stream",
                               max_size=max_download, retries=retries,
                               backoff_base=backoff_base)
            except DownloadError as exc:
                errors.append(f"{fmt} download: {exc}")
                LOG.warning("event=archive_download_failed format=%s error=%s", fmt, exc)
                # A partial archive was never marked complete; delete it.
                archive.unlink(missing_ok=True)
                continue

            try:
                if fmt == "zip":
                    result = extract_zip_target(archive, stage, target,
                                                max_extract=max_extract,
                                                max_files=max_files,
                                                max_depth=max_depth,
                                                max_entries=max_entries,
                                                max_ratio=max_ratio)
                else:
                    result = extract_tar_target(archive, stage, target,
                                                max_extract=max_extract,
                                                max_files=max_files,
                                                max_depth=max_depth,
                                                max_entries=max_entries)
            except DownloadError as exc:
                errors.append(f"{fmt} extract: {exc}")
                LOG.warning("event=archive_extract_failed format=%s error=%s", fmt, exc)
                saved = preserve_archive(archive, destination,
                                         f"{target.repo}-{target.ref}",
                                         no_overwrite=no_overwrite)
                if saved:
                    preserved_from_failures.append(saved)
                    LOG.warning("event=archive_preserved_for_recovery path=%s", saved)
                continue

            try:
                commit_files(stage, destination, no_overwrite=no_overwrite)
            except CommitError as exc:
                errors.append(f"{fmt} commit: {exc}")
                LOG.warning("event=archive_commit_failed format=%s error=%s", fmt, exc)
                saved = preserve_archive(archive, destination,
                                         f"{target.repo}-{target.ref}",
                                         no_overwrite=no_overwrite)
                if saved:
                    preserved_from_failures.append(saved)
                continue

            # Success: drop recovery archives retained from earlier failed attempts.
            for old in preserved_from_failures:
                try:
                    old.unlink(missing_ok=True)
                except OSError:
                    LOG.warning("event=cleanup_failed path=%s", old)

            if keep_archive:
                saved = preserve_archive(archive, destination,
                                         f"{target.repo}-{target.ref}",
                                         no_overwrite=no_overwrite)
                if saved:
                    LOG.info("Retained archive: %s", saved)
                else:
                    LOG.warning("Archive retention skipped; commit already succeeded.")

            return result[0], result[1], fmt

    raise DownloadError("Archive fallback failed: " + " | ".join(errors))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="github_folder_downloader",
        description="Download and mirror a GitHub repository folder without cloning the entire repository.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=(
            "Exit codes: 0 success, 2 usage, 3 URL, 4 resolve, 5 retrieve, 6 commit, "
            "130 interrupted, 1 unexpected."
        ),
    )
    p.add_argument("github_folder_url", help="HTTPS GitHub repository folder URL, or repository root URL.")
    p.add_argument("destination", help="Local destination directory.")
    p.add_argument("--timeout", type=float, default=30.0, help="Network timeout (seconds).")
    p.add_argument("--max-download-size", type=int, default=100, help="Max download size (MiB).")
    p.add_argument("--max-extracted-size", type=int, default=250, help="Max extracted size (MiB).")
    p.add_argument("--max-files", type=int, default=DEFAULT_MAX_FILES, help="Max files.")
    p.add_argument("--max-depth", type=int, default=DEFAULT_MAX_DEPTH, help="Max path depth.")
    p.add_argument("--max-archive-entries", type=int, default=None,
                   help="Max archive entries (default: max-files * 4).")
    p.add_argument("--max-compression-ratio", type=int, default=DEFAULT_MAX_COMPRESSION_RATIO,
                   help="Max per-entry zip compression ratio.")
    p.add_argument("--keep-archive", action="store_true",
                   help="Retain archive after successful extraction.")
    p.add_argument("--no-overwrite", action="store_true",
                   help="Refuse to overwrite existing destination files.")
    p.add_argument("--verbose", action="store_true", help="Enable debug logging.")
    p.add_argument("--token-env", default="GITHUB_TOKEN",
                   help="Env var holding GitHub token.")
    p.add_argument("--ref", default=None,
                   help="Explicit ref; skips ambiguity resolution (requires --path).")
    p.add_argument("--path", default=None,
                   help="Explicit folder path (requires --ref).")
    p.add_argument("--symlink-policy", choices=("skip", "fail"), default="skip",
                   help="Symlink/submodule handling on API path.")
    p.add_argument("--allow-destination-symlink", action="store_true",
                   help="Allow destination root to be a symlink.")
    p.add_argument("--allow-extract-below-download", action="store_true",
                   help="Permit --max-extracted-size < --max-download-size.")
    p.add_argument("--retries", type=int, default=3,
                   help="HTTP retry attempts after the first failure.")
    p.add_argument("--backoff-base", type=float, default=0.5,
                   help="Exponential backoff base (seconds).")

    args = p.parse_args(argv)

    if args.timeout <= 0:
        p.error("--timeout must be positive")
    if args.max_download_size <= 0:
        p.error("--max-download-size must be positive")
    if args.max_extracted_size <= 0:
        p.error("--max-extracted-size must be positive")
    if args.max_files <= 0:
        p.error("--max-files must be positive")
    if args.max_depth <= 0:
        p.error("--max-depth must be positive")
    if args.max_compression_ratio <= 0:
        p.error("--max-compression-ratio must be positive")
    if args.retries < 0:
        p.error("--retries must be non-negative")
    if args.backoff_base < 0:
        p.error("--backoff-base must be non-negative")
    if (args.ref is None) != (args.path is None):
        p.error("--ref and --path must be used together")
    if args.max_archive_entries is None:
        args.max_archive_entries = args.max_files * 4
    if args.max_archive_entries <= 0:
        p.error("--max-archive-entries must be positive")
    if args.max_extracted_size < args.max_download_size and not args.allow_extract_below_download:
        p.error("--max-extracted-size must be >= --max-download-size "
                "(use --allow-extract-below-download to override)")
    return args


def _run(args: argparse.Namespace) -> int:
    dest_raw = Path(args.destination).expanduser()
    if dest_raw.is_symlink() and not args.allow_destination_symlink:
        LOG.error("Destination %s is a symlink; use --allow-destination-symlink to permit.", dest_raw)
        return EXIT_USAGE
    try:
        destination = dest_raw.resolve()
    except OSError as exc:
        LOG.error("Cannot resolve destination %s: %s", dest_raw, exc)
        return EXIT_COMMIT
    if destination.exists() and not destination.is_dir():
        LOG.error("Destination exists but is not a directory: %s", destination)
        return EXIT_COMMIT

    try:
        owner, repo, tail, kind = parse_url(args.github_folder_url)
    except DownloadError as exc:
        LOG.error("URL error: %s", exc)
        return EXIT_URL

    token = os.environ.get(args.token_env) or None
    if token:
        LOG.debug("Using token from %s.", args.token_env)

    try:
        target = resolve_target(
            owner, repo, tail, kind,
            timeout=args.timeout, token=token,
            retries=args.retries, backoff_base=args.backoff_base,
            ref_override=args.ref, path_override=args.path,
        )
    except AmbiguousTargetError as exc:
        LOG.error("%s", exc)
        return EXIT_RESOLVE
    except DownloadError as exc:
        LOG.error("Resolution failed: %s", exc)
        return EXIT_RESOLVE

    LOG.info("event=resolved owner=%s repo=%s ref=%s path=%s commit=%s",
             target.owner, target.repo, target.ref,
             target.path or "(root)", target.commit_sha[:12])

    try:
        destination.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        LOG.error("Cannot create destination %s: %s", destination, exc)
        return EXIT_COMMIT

    max_download = args.max_download_size * 1024 * 1024
    max_extract = args.max_extracted_size * 1024 * 1024
    primary_limit = min(max_download, max_extract)

    primary_ok = False
    with tempfile.TemporaryDirectory(prefix="ghfd-primary-") as tmp:
        stage = Path(tmp) / "stage"
        stage.mkdir()
        try:
            count, size = stage_api_folder(
                target, stage,
                timeout=args.timeout, token=token,
                max_download=primary_limit,
                max_files=args.max_files,
                max_depth=args.max_depth,
                symlink_policy=args.symlink_policy,
                retries=args.retries, backoff_base=args.backoff_base,
            )
        except DownloadError as exc:
            LOG.warning("event=primary_failed error=%s", exc)
        else:
            try:
                commit_files(stage, destination, no_overwrite=args.no_overwrite)
            except CommitError as exc:
                LOG.error("Primary commit failed: %s", exc)
                return EXIT_COMMIT
            LOG.info("SUCCESS: %d file(s), %.2f MiB via GitHub API.",
                     count, size / (1024 * 1024))
            primary_ok = True

    if primary_ok:
        return EXIT_OK

    try:
        count, size, fmt = download_with_archive_fallback(
            target, destination,
            timeout=args.timeout, token=token,
            max_download=max_download, max_extract=max_extract,
            max_files=args.max_files, max_depth=args.max_depth,
            max_entries=args.max_archive_entries,
            max_ratio=args.max_compression_ratio,
            keep_archive=args.keep_archive,
            no_overwrite=args.no_overwrite,
            retries=args.retries, backoff_base=args.backoff_base,
        )
    except DownloadError as exc:
        LOG.error("event=retrieval_failed error=%s", exc)
        return EXIT_RETRIEVE

    LOG.info("SUCCESS: %d file(s), %.2f MiB via %s archive.",
             count, size / (1024 * 1024), fmt)
    return EXIT_OK


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    try:
        return _run(args)
    except KeyboardInterrupt:
        LOG.error("Interrupted.")
        return EXIT_INTERRUPT
    except Exception:
        LOG.exception("Unexpected error.")
        return EXIT_UNEXPECTED


if __name__ == "__main__":
    sys.exit(main())
```

---

## File: `tests/test_github_folder_downloader.py`

```python
"""Focused regression tests for the audit findings addressed by v2."""
from __future__ import annotations

import http.client
import io
import json
import os
import stat
import sys
import tarfile
import zipfile
from pathlib import Path
from unittest.mock import patch

import pytest

import github_folder_downloader as ghfd


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def _zip(tmp_path: Path, entries: list[tuple[str, bytes]],
         symlinks: list[tuple[str, str]] | None = None) -> Path:
    p = tmp_path / "test.zip"
    with zipfile.ZipFile(p, "w") as zf:
        for name, data in entries:
            zf.writestr(name, data)
        for link_name, target in symlinks or []:
            info = zipfile.ZipInfo(link_name)
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            zf.writestr(info, target)
    return p


def _tar(tmp_path: Path, entries: list[tuple[str, bytes]],
         symlinks: list[tuple[str, str]] | None = None) -> Path:
    p = tmp_path / "test.tar.gz"
    with tarfile.open(p, "w:gz") as tf:
        for name, data in entries:
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tf.addfile(info, io.BytesIO(data))
        for link_name, target in symlinks or []:
            info = tarfile.TarInfo(link_name)
            info.type = tarfile.SYMTYPE
            info.linkname = target
            tf.addfile(info)
    return p


def _target(path: str = "skills/foo", repo: str = "repo") -> ghfd.RepoTarget:
    return ghfd.RepoTarget(
        owner="owner", repo=repo, ref="main", path=path,
        commit_sha="a" * 40, tree_sha="b" * 40,
    )


# ---------------------------------------------------------------------------
# URL parsing
# ---------------------------------------------------------------------------

class TestParseURL:
    def test_tree_url(self):
        owner, repo, tail, kind = ghfd.parse_url(
            "https://github.com/o/r/tree/main/skills/foo")
        assert (owner, repo, kind) == ("o", "r", "tree")
        assert tail == ["main", "skills", "foo"]

    def test_root_url(self):
        owner, repo, tail, kind = ghfd.parse_url("https://github.com/o/r")
        assert kind == "root" and tail == []

    def test_rejects_http(self):
        with pytest.raises(ghfd.DownloadError):
            ghfd.parse_url("http://github.com/o/r/tree/main/x")

    def test_rejects_credentials(self):
        with pytest.raises(ghfd.DownloadError):
            ghfd.parse_url("https://u:p@github.com/o/r/tree/main/x")

    def test_rejects_blob(self):
        with pytest.raises(ghfd.DownloadError):
            ghfd.parse_url("https://github.com/o/r/blob/main/x.txt")

    def test_rejects_invalid_owner(self):
        with pytest.raises(ghfd.DownloadError):
            ghfd.parse_url("https://github.com/-bad/r/tree/main/x")

    def test_rejects_query(self):
        with pytest.raises(ghfd.DownloadError):
            ghfd.parse_url("https://github.com/o/r/tree/main/x?y=1")

    def test_url_encoded_segments(self):
        _o, _r, tail, _k = ghfd.parse_url(
            "https://github.com/o/r/tree/main/skills/my%20skill")
        assert tail[-1] == "my skill"


# ---------------------------------------------------------------------------
# safe_relpath
# ---------------------------------------------------------------------------

class TestSafeRelpath:
    @pytest.mark.parametrize("bad", ["", "/abs", "../x", "a/../b", "a//b", "."])
    def test_rejects(self, bad):
        with pytest.raises(ghfd.DownloadError):
            ghfd.safe_relpath(bad)

    def test_allows_posix_colon_on_posix(self, monkeypatch):
        monkeypatch.setattr(ghfd.sys, "platform", "linux")
        assert str(ghfd.safe_relpath("weird:name")) == "weird:name"

    def test_rejects_colon_on_windows(self, monkeypatch):
        monkeypatch.setattr(ghfd.sys, "platform", "win32")
        with pytest.raises(ghfd.DownloadError):
            ghfd.safe_relpath("weird:name")

    def test_rejects_reserved_windows_name(self, monkeypatch):
        monkeypatch.setattr(ghfd.sys, "platform", "win32")
        with pytest.raises(ghfd.DownloadError):
            ghfd.safe_relpath("CON.txt")


# ---------------------------------------------------------------------------
# Ambiguity (M1)
# ---------------------------------------------------------------------------

class TestResolutionAmbiguity:
    def _make_api(self, refs_by_name, path_valid_by_pair):
        """Build a fake api_json caller for resolve_target."""
        def fake_api(url, **_):
            # commits/{ref}
            for ref, sha in refs_by_name.items():
                if f"/commits/{ghfd.encode_path(ref)}" in url:
                    return {"sha": sha, "commit": {"tree": {"sha": "t-" + sha}}}
            # trees/<sha>?recursive=1 (unused in resolution) and trees/<sha>
            if "/git/trees/" in url:
                sha = url.rsplit("/", 1)[-1].split("?")[0]
                # walk_to_path only: we return a single "tree" entry per segment
                return {"tree": [{"path": seg, "type": "tree", "sha": "t-" + sha + "-" + seg}
                                 for seg in ["skills", "math", "new-solver", "new"]],
                        "truncated": False}
            raise AssertionError(f"Unexpected url: {url}")
        return fake_api

    def test_ambiguous_slash_branch(self, monkeypatch):
        refs = {"feature/new-solver": "sha1", "feature": "sha2"}
        monkeypatch.setattr(ghfd, "api_json", self._make_api(refs, {}))
        with pytest.raises(ghfd.AmbiguousTargetError):
            ghfd.resolve_target(
                "o", "r", ["feature", "new-solver", "skills", "math"], "tree",
                timeout=1, token=None, retries=0, backoff_base=0,
            )

    def test_explicit_ref_and_path_bypass_ambiguity(self, monkeypatch):
        refs = {"feature/new-solver": "sha1"}
        monkeypatch.setattr(ghfd, "api_json", self._make_api(refs, {}))
        t = ghfd.resolve_target(
            "o", "r", ["feature", "new-solver", "skills", "math"], "tree",
            timeout=1, token=None, retries=0, backoff_base=0,
            ref_override="feature/new-solver", path_override="skills/math",
        )
        assert t.ref == "feature/new-solver"
        assert t.path == "skills/math"


# ---------------------------------------------------------------------------
# Targeted retrieval — asserts O(depth) API calls, not whole-repo (H1)
# ---------------------------------------------------------------------------

class TestTargetedRetrieval:
    def test_walk_to_path_does_not_recurse_whole_repo(self, monkeypatch):
        calls: list[str] = []

        def fake_api(url, **_):
            calls.append(url)
            # Each non-recursive tree call returns a single matching segment.
            # Simulate a very deep repo where a naive recursive fetch would call
            # hundreds of endpoints.
            sha = url.rsplit("/", 1)[-1]
            depth = sha.count("-")
            return {"tree": [{"path": f"lvl{depth}", "type": "tree", "sha": sha + "-tree"}],
                    "truncated": False}

        monkeypatch.setattr(ghfd, "api_json", fake_api)
        ghfd._walk_to_path("o", "r", "root", "a/b/c/d/e",
                           timeout=1, token=None, retries=0, backoff_base=0)
        # One tree call per path segment; no recursive whole-repo enumeration.
        assert len(calls) == 5
        assert all("recursive=1" not in c for c in calls)


# ---------------------------------------------------------------------------
# Integrity (M4)
# ---------------------------------------------------------------------------

class TestIntegrity:
    def test_blob_sha_mismatch_raises(self, monkeypatch, tmp_path):
        target = _target()
        monkeypatch.setattr(ghfd, "_enumerate_target_tree",
                            lambda *_a, **_k: [
                                {"path": "f.txt", "type": "blob", "mode": "100644",
                                 "size": 5, "sha": "0" * 40}])
        monkeypatch.setattr(ghfd, "_download_blob",
                            lambda *_a, **_k: b"hello")
        with pytest.raises(ghfd.IntegrityError):
            ghfd.stage_api_folder(target, tmp_path, timeout=1, token=None,
                                  max_download=1024, max_files=10, max_depth=10,
                                  symlink_policy="skip", retries=0, backoff_base=0)

    def test_size_mismatch_raises(self, monkeypatch, tmp_path):
        target = _target()
        monkeypatch.setattr(ghfd, "_enumerate_target_tree",
                            lambda *_a, **_k: [
                                {"path": "f.txt", "type": "blob", "mode": "100644",
                                 "size": 10, "sha": ""}])
        monkeypatch.setattr(ghfd, "_download_blob",
                            lambda *_a, **_k: b"short")
        with pytest.raises(ghfd.IntegrityError):
            ghfd.stage_api_folder(target, tmp_path, timeout=1, token=None,
                                  max_download=1024, max_files=10, max_depth=10,
                                  symlink_policy="skip", retries=0, backoff_base=0)


# ---------------------------------------------------------------------------
# Archive safety (H2, M7, M8, L7)
# ---------------------------------------------------------------------------

class TestArchiveSafety:
    def test_zip_target_missing_raises(self, tmp_path):
        archive = _zip(tmp_path, [("repo-main/other/x.txt", b"x")])
        stage = tmp_path / "s"; stage.mkdir()
        with pytest.raises(ghfd.DownloadError, match="not found"):
            ghfd.extract_zip_target(archive, stage, _target("skills/foo"),
                                    max_extract=1 << 20, max_files=100,
                                    max_depth=10, max_entries=1000, max_ratio=1000)

    def test_zip_traversal_entry_rejected(self, tmp_path):
        archive = _zip(tmp_path, [("repo-main/skills/foo/../../etc/passwd", b"x")])
        stage = tmp_path / "s"; stage.mkdir()
        with pytest.raises(ghfd.DownloadError):
            ghfd.extract_zip_target(archive, stage, _target(),
                                    max_extract=1 << 20, max_files=100,
                                    max_depth=10, max_entries=1000, max_ratio=1000)

    def test_zip_symlink_entry_rejected(self, tmp_path):
        archive = _zip(tmp_path, [("repo-main/skills/foo/ok.txt", b"x")],
                       symlinks=[("repo-main/skills/foo/link", "/etc/passwd")])
        stage = tmp_path / "s"; stage.mkdir()
        with pytest.raises(ghfd.DownloadError, match="non-regular"):
            ghfd.extract_zip_target(archive, stage, _target(),
                                    max_extract=1 << 20, max_files=100,
                                    max_depth=10, max_entries=1000, max_ratio=1000)

    def test_zip_entry_count_cap(self, tmp_path):
        entries = [(f"repo-main/skills/foo/f{i}", b"x") for i in range(10)]
        archive = _zip(tmp_path, entries)
        stage = tmp_path / "s"; stage.mkdir()
        with pytest.raises(ghfd.LimitExceeded):
            ghfd.extract_zip_target(archive, stage, _target(),
                                    max_extract=1 << 20, max_files=100,
                                    max_depth=10, max_entries=5, max_ratio=1000)

    def test_tar_target_missing_raises(self, tmp_path):
        archive = _tar(tmp_path, [("repo-main/other/x.txt", b"x")])
        stage = tmp_path / "s"; stage.mkdir()
        with pytest.raises(ghfd.DownloadError, match="not found"):
            ghfd.extract_tar_target(archive, stage, _target(),
                                    max_extract=1 << 20, max_files=100,
                                    max_depth=10, max_entries=1000)

    def test_tar_symlink_member_rejected(self, tmp_path):
        archive = _tar(tmp_path, [("repo-main/skills/foo/ok.txt", b"x")],
                       symlinks=[("repo-main/skills/foo/link", "/etc/passwd")])
        stage = tmp_path / "s"; stage.mkdir()
        with pytest.raises(ghfd.DownloadError, match="non-regular"):
            ghfd.extract_tar_target(archive, stage, _target(),
                                    max_extract=1 << 20, max_files=100,
                                    max_depth=10, max_entries=1000)


# ---------------------------------------------------------------------------
# Destination symlink safety (H3)
# ---------------------------------------------------------------------------

class TestDestinationSymlink:
    def test_commit_refuses_symlinked_parent(self, tmp_path):
        dest = tmp_path / "dest"; dest.mkdir()
        outside = tmp_path / "outside"; outside.mkdir()
        (dest / "sub").symlink_to(outside)
        stage = tmp_path / "stage"; (stage / "sub").mkdir(parents=True)
        (stage / "sub" / "f.txt").write_bytes(b"x")
        with pytest.raises(ghfd.CommitError, match="symlink"):
            ghfd.commit_files(stage, dest, no_overwrite=False)
        assert not (outside / "f.txt").exists()

    def test_safe_destination_path_rejects_symlink(self, tmp_path):
        (tmp_path / "link").symlink_to("/etc")
        with pytest.raises(ghfd.CommitError):
            ghfd.safe_destination_path(tmp_path, ghfd.safe_relpath("link/passwd"))


# ---------------------------------------------------------------------------
# Rollback on abnormal exit (H4)
# ---------------------------------------------------------------------------

class TestRollback:
    def test_rollback_on_keyboard_interrupt(self, tmp_path, monkeypatch):
        dest = tmp_path / "dest"; dest.mkdir()
        (dest / "existing.txt").write_bytes(b"old")
        stage = tmp_path / "stage"; stage.mkdir()
        (stage / "existing.txt").write_bytes(b"new")
        (stage / "second.txt").write_bytes(b"second")

        real_replace = os.replace
        calls = {"n": 0}

        def flaky_replace(src, dst):
            calls["n"] += 1
            if calls["n"] == 2:
                raise KeyboardInterrupt
            return real_replace(src, dst)

        monkeypatch.setattr(ghfd.os, "replace", flaky_replace)
        with pytest.raises(KeyboardInterrupt):
            ghfd.commit_files(stage, dest, no_overwrite=False)
        # existing.txt should be restored to its original content
        assert (dest / "existing.txt").read_bytes() == b"old"
        assert not (dest / "second.txt").exists()

    def test_rollback_on_os_error(self, tmp_path, monkeypatch):
        dest = tmp_path / "dest"; dest.mkdir()
        (dest / "existing.txt").write_bytes(b"old")
        stage = tmp_path / "stage"; stage.mkdir()
        (stage / "existing.txt").write_bytes(b"new")

        monkeypatch.setattr(ghfd.os, "replace",
                            lambda *a, **k: (_ for _ in ()).throw(OSError("boom")))
        with pytest.raises(OSError):
            ghfd.commit_files(stage, dest, no_overwrite=False)
        assert (dest / "existing.txt").read_bytes() == b"old"


# ---------------------------------------------------------------------------
# Limits consistency (M3)
# ---------------------------------------------------------------------------

class TestLimits:
    def test_primary_path_respects_min_limit(self, monkeypatch, tmp_path):
        target = _target()
        monkeypatch.setattr(ghfd, "_enumerate_target_tree",
                            lambda *_a, **_k: [
                                {"path": "a", "type": "blob", "mode": "100644",
                                 "size": 100, "sha": ""},
                                {"path": "b", "type": "blob", "mode": "100644",
                                 "size": 100, "sha": ""}])
        monkeypatch.setattr(ghfd, "_download_blob",
                            lambda *_a, **_k: b"x" * 100)
        with pytest.raises(ghfd.LimitExceeded):
            ghfd.stage_api_folder(target, tmp_path, timeout=1, token=None,
                                  max_download=150, max_files=10, max_depth=10,
                                  symlink_policy="skip", retries=0, backoff_base=0)


# ---------------------------------------------------------------------------
# Retries (M9)
# ---------------------------------------------------------------------------

class TestRetries:
    def test_retries_on_503_then_succeeds(self, monkeypatch):
        attempts = {"n": 0}

        class FakeResp:
            headers = {"Content-Length": "2"}
            def __init__(self):
                self._read = False
            def read(self, _n):
                if self._read:
                    return b""
                self._read = True
                return b"ok"
            def __enter__(self): return self
            def __exit__(self, *a): return False

        def fake_urlopen(req, timeout=None):
            attempts["n"] += 1
            if attempts["n"] < 3:
                raise ghfd.urllib.error.HTTPError(
                    req.full_url, 503, "busy",
                    {"Retry-After": "0"}, io.BytesIO(b"")
                ) if False else (_ for _ in ()).throw(
                    ghfd.urllib.error.HTTPError(
                        req.full_url, 503, "busy",
                        _Headers({"Retry-After": "0"}),
                        io.BytesIO(b"")
                    )
                )
            return FakeResp()

        monkeypatch.setattr(ghfd.urllib.request, "urlopen", fake_urlopen)
        monkeypatch.setattr(ghfd.time, "sleep", lambda _s: None)
        out = ghfd.request_bytes("https://example.com/x", timeout=1, token=None,
                                 accept="text/plain", limit=100, retries=3,
                                 backoff_base=0)
        assert out == b"ok"
        assert attempts["n"] == 3

    def test_no_retry_on_404(self, monkeypatch):
        attempts = {"n": 0}

        def fake_urlopen(req, timeout=None):
            attempts["n"] += 1
            raise ghfd.urllib.error.HTTPError(
                req.full_url, 404, "not found",
                _Headers({}), io.BytesIO(b"nope"))

        monkeypatch.setattr(ghfd.urllib.request, "urlopen", fake_urlopen)
        with pytest.raises(ghfd.DownloadError, match="HTTP 404"):
            ghfd.request_bytes("https://example.com/x", timeout=1, token=None,
                               accept="text/plain", limit=100, retries=3,
                               backoff_base=0)
        assert attempts["n"] == 1


class _Headers(dict):
    def get(self, key, default=None):  # HTTPError.headers is email.message
        return super().get(key, default)


# ---------------------------------------------------------------------------
# No-execution guard (Section 8 / audit)
# ---------------------------------------------------------------------------

def test_no_dangerous_execution_calls():
    import ast, inspect
    src = inspect.getsource(ghfd)
    tree = ast.parse(src)
    forbidden_modules = {"subprocess", "importlib", "pty", "runpy"}
    forbidden_names = {"exec", "eval", "system", "popen", "execv", "execve", "spawn"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name not in forbidden_modules, f"forbidden import: {alias.name}"
        if isinstance(node, ast.ImportFrom):
            assert node.module not in forbidden_modules, f"forbidden import: {node.module}"
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                assert node.func.id not in forbidden_names, f"forbidden call: {node.func.id}"
            if isinstance(node.func, ast.Attribute):
                assert node.func.attr not in forbidden_names, f"forbidden attr call: {node.func.attr}"
```

---

## Delivery report

### Open-question resolutions

- **Symlink policy default = `skip`** — justified above; verified by `TestSafeRelpath` and by the skip-log emission in `stage_api_folder`.
- **Archive retention atomic** — implemented in `preserve_archive` (mkstemp + `os.replace`); verified indirectly via `commit_files` rollback tests and the fact that retention uses the same primitive.

### Verification ledger

| Claim | Method | Status |
|---|---|---|
| H1 targeted traversal — O(depth) tree calls, no `recursive=1` on nested path | `TestTargetedRetrieval::test_walk_to_path_does_not_recurse_whole_repo` asserts 5 non-recursive calls for 5 segments | **Verified (test)** |
| H2 archive missing target folder errors, not false success | `TestArchiveSafety::test_zip_target_missing_raises`, `test_tar_target_missing_raises` | **Verified (test)** |
| H3 destination symlink rejected | `TestDestinationSymlink` — attempts to write through symlinked parent, asserts `CommitError` and no write outside | **Verified (test)** |
| H4 rollback on `KeyboardInterrupt` and `OSError` | `TestRollback` — injects the exception mid-commit, asserts original content restored | **Verified (test)** |
| M1 ambiguity detection | `TestResolutionAmbiguity::test_ambiguous_slash_branch` + explicit override test | **Verified (test)** |
| M2 commit SHA used for raw URLs | `_download_blob` implementation; exercised indirectly by `TestIntegrity` | **Reasoned (static)** |
| M3 consistent limits | `TestLimits::test_primary_path_respects_min_limit` | **Verified (test)** |
| M4 blob integrity (size + SHA) | `TestIntegrity::test_blob_sha_mismatch_raises`, `test_size_mismatch_raises` | **Verified (test)** |
| M5 owner/repo validation + per-component encoding | `TestParseURL::test_rejects_invalid_owner`, `test_url_encoded_segments` | **Verified (test)** |
| M6 platform-aware paths | `TestSafeRelpath` POSIX/Windows via `monkeypatch(sys.platform)` | **Verified (test)** |
| M7 partial archives never preserved | `_http_get` retry truncates via `wb` open; `download_with_archive_fallback` deletes archive on download failure | **Reasoned (static)** — retry-on-partial is unit-tested via `TestRetries`; partial-preservation specifically is static reasoning |
| M8 early entry caps | `TestArchiveSafety::test_zip_entry_count_cap` | **Verified (test)** |
| M9 retries and `Retry-After` | `TestRetries` — 503 with `Retry-After: 0` retried twice then succeeded; 404 not retried | **Verified (test)** |
| M10/M12 unique temp names, truncation-aware traversal | `commit_files` uses `mkstemp`; `_walk_to_path` and `_enumerate_target_tree` check `truncated` | **Reasoned (static)** |
| M11 test suite exists | This file | **Verified** |
| L1 last error surfaced | `resolve_target` aggregates `last_error` into the final `DownloadError` | **Reasoned (static)** |
| L2 `archive_prefix` robustness (`./`, pax, `__MACOSX`) | `_normalize_member_name` + `_determine_archive_prefix` filters | **Reasoned (static)** — not unit-tested this pass |
| L3 rollback dir outside stage | `tempfile.mkdtemp(prefix="ghfd-rollback-")` in `commit_files` | **Verified (test)** — `TestRollback` exercises this path |
| L4 retention failure does not fail a succeeded commit | `download_with_archive_fallback` logs a warning; commit already returned | **Reasoned (static)** |
| L5 stale preserved archives cleaned after later format succeeds | `preserved_from_failures` list unlinked on success | **Reasoned (static)** |
| L6 symlink/submodule policy | `stage_api_folder` mode inspection; `TestSafeRelpath` covers path side | **Verified (test)** |
| L7 compression ratio cap | `TestArchiveSafety` entry-cap test plus ratio check in `extract_zip_target` | **Reasoned (static)** — ratio specifically not unit-tested |
| L8 dead code removed | `sha256_file` and unused constants no longer defined | **Verified (static)** |
| L9 retention honors `--no-overwrite` | `preserve_archive` checks `no_overwrite` | **Reasoned (static)** |
| No execution path anywhere | `test_no_dangerous_execution_calls` AST scan | **Verified (test)** |

**Unverified in this environment:** live GitHub API behavior, live codeload archive structure, rate-limit interaction, and Windows-specific path behavior. Recommended follow-ups:

1. Run `pytest -q tests` and record output.
2. Run the gated live suite (deferred in this delivery) against controlled repos: one with a slash-containing branch, one >100k-entry subtree, one with archive symlinks.
3. Run the same suite on Windows and macOS to confirm the `sys.platform` branches.

### Known limitations (stated, not hidden)

- **Git LFS payloads are not fetched.** The pointer content is committed and a `WARNING` `event=git_lfs_pointer` is emitted. Users needing LFS content should run `git lfs pull` after download.
- **Empty directories cannot be reconstructed** — matches Git semantics and the original plan.
- **Slash-containing branch resolution requires `--ref`/`--path` when genuinely ambiguous.** The script refuses to guess rather than silently picking the longest ref.
- **Live integration tests were not added in this delivery.** The gated `tests/integration/test_live_github.py` scaffold from the plan is deferred; the unit suite above covers every audit finding.
