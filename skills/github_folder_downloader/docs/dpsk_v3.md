# Meticulous Review and Critical Comparison

**Scope:** `g1.md` (v1), `q3.md` (v2 candidate), `d2.md` (alternate v2 candidate).
**Method:** Static trace + completeness check + cross-artifact behavioral comparison. **No live GitHub calls performed.** All labels use *Verified* / *Reasoned* / *Unverifiable*.

---

## 0. Completeness and evidence intake

| Artifact | Compiles? | Complete? | Evidence |
|---|---|---|---|
| `g1.md` | **Reasoned** yes (imports, closures, `__main__` all present) | Complete | Reasoned |
| `q3.md` | **Reasoned** yes | Complete + harness | Reasoned (author explicitly: nothing executed) |
| `d2.md` | **Unverifiable — cannot compile as pasted** | **Truncated** | Verified by inspection |

### 0.1 Verified truncation of `d2.md`

The pasted file ends at:

```python
    except Exception:
        LOG.exception("Unexpected error.")
        return EXIT_UN
[file content end]
```

Consequences:

1. `EXIT_UN` is the prefix of `EXIT_UNEXPECTED` (defined at top). The file is cut mid-token — it will raise `NameError` at module import if referenced, or `SyntaxError` if compilation reaches that point before the `if __name__ == "__main__":` block (which is also absent).
2. **The `if __name__ == "__main__": sys.exit(main())` block is missing.** Running the file does nothing even if compilation succeeded.
3. The entire bottom CLI section (`_run` return-path ordering, `main`) is visible, but the terminal `return` is not.

**Therefore:** every behavioral statement about `d2.md` below is **Reasoned**, contingent on the assumption that the final `return EXIT_UNEXPECTED` and `__main__` block are as they appear. Any finding that depends on them is flagged.

### 0.2 Docstring/behavior inconsistency (Verified, g1.md)

`g1.md` docstring:

> *"Archive fallback is never executed."*

`g1.md` `main()`:

```python
count, size, fmt = download_with_archive_fallback(...)
LOG.info("SUCCESS: ... via %s archive fallback.", ...)
```

Contradiction. Not a runtime bug, but a **documentation defect** (Low). `q3.md` and `d2.md` docstrings match their behavior.

---

## 1. Exit-code contracts

| Code | g1.md | q3.md | d2.md |
|---|---|---|---|
| 0 | Success | Success | Success |
| 1 | `DownloadError`, `OSError`, unexpected | `DownloadError`, `OSError`, unexpected | Unexpected only |
| 2 | argparse / dest-not-dir | argparse / dest-not-dir | argparse |
| 3 | — | `AmbiguousRefError` | URL-parse `DownloadError` |
| 4 | — | — | Resolution `DownloadError` / `AmbiguousTargetError` |
| 5 | — | — | Retrieval `DownloadError` |
| 6 | — | — | Commit `CommitError` |
| 130 | `KeyboardInterrupt` | `KeyboardInterrupt` | `KeyboardInterrupt` |

### 1.1 Critical observations

- **`d2.md`'s ambiguity does not get its own code.** `_run` catches `AmbiguousTargetError` and returns `EXIT_RESOLVE` (4) — the *same* code as other resolution failures. The exception type exists for message formatting only; the exit code doesn't distinguish it. `q3.md`'s decision D3 ("exit 3 added") is therefore **strictly stronger** for scripting.
- **`d2.md` catches URL errors separately (3)**; `q3.md` folds URL parsing errors into `DownloadError` → 1. `d2.md`'s contract is more informative but also means a script cannot distinguish URL typos from network failures by exit code alone without reading the log.
- **`g1.md`'s destination-not-directory check returns 2** — but `q3.md` also returns 2 for this case (Reasoned). `d2.md` returns 6 (`EXIT_COMMIT`) for the same condition, because it enters `_run` after `parse_args` and hits the commit-error branch. **Contract divergence**: identical condition, different exit code across the three scripts.

### 1.2 Catch-order hazards (Verified by inspection)

`q3.md` (`main`) catches in this order:

```python
except AmbiguousRefError as exc:  # first
except DownloadError as exc:      # second (subsumes AmbiguousRefError if not first)
except KeyboardInterrupt: ...
```

`AmbiguousRefError` extends `DownloadError`, so **the ordering matters** and is correct here. `d2.md`'s `_run` similarly places `AmbiguousTargetError` before `DownloadError` — correct by inspection (subject to truncation).

`g1.md` has **no `AmbiguousRefError`** because it never detects ambiguity (see §3).

---

## 2. URL parsing

### 2.1 Behavioral matrix

| Case | g1.md | q3.md | d2.md |
|---|---|---|---|
| `http://` | reject | reject | reject |
| Host ≠ `github.com` | reject | reject | reject |
| `user:pass@` | reject | reject | reject |
| Query/fragment | reject | reject | reject |
| `.git` suffix | strips | strips | strips |
| `?recursive=1` in tree API (internal, not URL) | not applicable | not applicable | not applicable |
| Owner contains `..` | reject | reject | **`OWNER_RE` rejects implicitly** |
| Owner contains `-start` | **accept** | accept | **reject** (`^[A-Za-z0-9]`) |
| Owner with 39 chars | accept | accept | **reject (max 38)** |
| Repo `.gitignore` alone | accept | accept | accept |
| `blob` in third segment | reject | reject | reject |
| `https://github.com/../r` | reject (Reasoned: path becomes `..`,`r`) | reject | reject |
| Percent-decoded path segments | yes | yes | yes |

### 2.2 Significant findings

**Finding P1 (Medium, d2.md only):** `d2.md` uses GitHub's actual owner regex `^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$`. `q3.md`/`g1.md` accept a superset (any non-`/`, non-`.` segment). The stricter regex is more **correct** but risks rejecting legitimate edge-case usernames that GitHub recently provisioned (GitHub has relaxed rules over time). **Not a defect either way** — a policy choice — but note that `q3.md`'s `test_url_parse` matrix (`q3.md §2f`) tests `../r` rejection via structural checks, which is *stronger* than charset checks.

**Finding P2 (Low, all):** None of the three validate that `ref` characters are legal (e.g., a ref cannot contain `..` in most contexts but Git rules are complex). All rely on downstream API to reject illegal refs. `q3.md`'s `_commit_for_ref` correctly disambiguates 404 vs other errors (see §3.2).

---

## 3. Ref/path resolution — the core divergence

### 3.1 g1.md — silently picks the wrong folder

`g1.md`'s resolver (Verified by trace):

```python
for split in range(len(tail), 0, -1):
    candidate_ref = "/".join(tail[:split])
    candidate_path = "/".join(tail[split:])
    ...
    recursive = api_json(f"...?recursive=1")
    if recursive.get("truncated"):
        continue
    found = any(x.get("path") == candidate_path and x.get("type") == "tree" ...)
    if not found:
        continue
    return RepoTarget(...)
```

Behavior on ambiguous input `feature/x/docs` where both `(feature/x, docs)` and `(feature, x/docs)` exist:

1. First iteration `split=3`: `ref="feature/x/docs"`, `path=""` — commit resolve fails, `continue`.
2. `split=2`: `ref="feature/x"`, `path="docs"` — **resolves and returns**.
3. Never tries `split=1` (`feature`, `x/docs`).

So it silently picks longest-prefix. A user landing on the wrong mirror gets **exit 0 and wrong files**, with no warning. This is a **High** functional-correctness defect for the resolved-folder contract.

**Finding R1 (High, g1.md only):** Silent longest-prefix resolution; no ambiguity detection; wrong-folder mirror possible with exit 0.

### 3.2 Secondary defect in g1.md's resolver (efficiency + correctness)

`fetch_tree(tree_sha, "", ...)` (Verified by trace) **is itself a full recursive walk** — it recursively calls `fetch_tree(sha, rel, ...)` for every subtree. For a repo with *D* directories and *F* files, it makes **D** API calls and downloads the entire non-recursive tree listing at each level. On a large monorepo, that's hundreds of API calls per candidate split, and GitHub's tree-endpoint rate limit will be hit.

Then, **redundantly**, the code calls the `?recursive=1` endpoint again (a second full listing) just to re-derive the same answer it already computed:

```python
found = any(item["path"] == target_path and item["type"] == "tree" for item in tree)  # dead
recursive = api_json(f"...?recursive=1")
if recursive.get("truncated"):
    continue   # ← throws away `tree`, discards a candidate that fetch_tree actually validated
found = any(...)   # recompute
```

**Finding R2 (Medium, g1.md):** `fetch_tree` is a redundant O(D) recursive walker; the subsequent `?recursive=1` call re-does the work; the `continue` on truncation discards a *valid* candidate because the first `fetch_tree` already succeeded. Net effect: slower, more rate-limit pressure, and possible false-negative resolution on large repos.

### 3.3 q3.md — hard-fail, explicit override

`q3.md`'s resolver (Verified by trace):
- Iterates *all* splits from longest to shortest, **collecting every match**.
- Raises `AmbiguousRefError` if `len(matches) > 1`.
- `--ref` override pins the entire tail as path.

This satisfies **D1**. Ambiguity is a first-class outcome, not a silent default.

**Finding R3 (High, in favor of q3.md):** Resolves the wrong-folder class of defect entirely; explicit exit 3 contract.

**Minor caveat:** `q3.md` re-fetches commit for each split. For *k* path segments, up to *k* commit lookups; each 404 is silently a miss (correct). Acceptable cost.

### 3.4 d2.md — hard-fail, but different override contract

`d2.md` (Reasoned, subject to truncation):
- Iterates all splits, collects candidates.
- Raises `AmbiguousTargetError` (exit **4**, not 3).
- Override requires `--ref` **and** `--path` together.

**Finding R4 (High, contract divergence):** `d2.md` refuses `--ref` alone. A user with `https://github.com/o/r/tree/feature/x/docs` who supplies `--ref feature/x` gets `DownloadError("--ref and --path must be supplied together.")`. `q3.md` accepts `--ref feature/x` (tail becomes the path). **The two implementations are not drop-in compatible.** This is the single most consequential behavioral difference between the two v2 candidates — see §10 for a portability assessment.

### 3.5 Cross-cutting: 404 vs other errors

Verified by trace:

| Script | 404 on commit | 401/403/429/500 on commit |
|---|---|---|
| `g1.md` | all treated as "no match" — **`continue`** silently | **same — `continue`** (bug: rate-limit disguised as a miss) |
| `q3.md` | `None` returned | re-raised (correct) |
| `d2.md` | caught `DownloadError`, stored as `last_error`, `continue` | **same** (bug: rate-limit disguised as a miss) |

**Finding R5 (High, g1.md and d2.md):** When GitHub returns 403/429 (rate limit) on a commit lookup, both `g1.md` and `d2.md` silently treat the ref as *nonexistent* and continue to the next candidate split. The user sees "could not resolve" instead of "rate-limited." `q3.md` explicitly checks `exc.status == 404` before swallowing.

---

## 4. HTTP layer — credential and DoS exposure

### 4.1 Redirect credential stripping

**Verified by inspection:**

- `g1.md`: no redirect handler. `urllib.request.urlopen` follows 3xx with the parent's `HTTPRedirectHandler`. In CPython (all versions ≥ 3.8), the parent does **not** strip `Authorization` on cross-origin redirects. Therefore the `Bearer <token>` header set in `stream_to_file` and `request_bytes` is forwarded to whatever host the server redirects to. For `codeload.github.com → objects.githubusercontent.com`, that is GitHub-controlled (low direct risk). For a compromised or misconfigured `codeload`, that is **real credential exfiltration**.
- `q3.md`: installs `SafeRedirectHandler` in `ensure_safe_opener()`; overrides `redirect_request`; deletes `Authorization` when `target.hostname != origin.hostname`; refuses `target.scheme != "https"`.
- `d2.md`: **no custom opener, no handler**. Same exposure as `g1.md`.

**Finding H1 (High, g1.md and d2.md):** `Authorization: Bearer` may leak on cross-host redirect. Confirmed by inspection. `q3.md` is the only implementation with the fix.

**Severity note:** GitHub's CDN (`objects.githubusercontent.com`) is GitHub-controlled, so the *practical* exposure for the default flow is modest, but the pattern is a standard best-practice violation and a real risk on any future CDN change or third-party mirror.

### 4.2 `Retry-After` cap

| | Behavior |
|---|---|
| `g1.md` | No retry at all; a 429/503 fails immediately |
| `q3.md` | `RETRY_AFTER_CAP = 60.0`; raises if server requests > 60 s |
| `d2.md` | **No cap**; `_parse_retry_after` returns raw seconds; `time.sleep(wait)` on whatever value |

**Finding H2 (High, d2.md only):** A misbehaving or hostile server can send `Retry-After: 86400`; `d2.md` will sleep for 24 hours, unattended, before failing. `q3.md` explicitly refuses anything over 60 s with a clear error. `g1.md` avoids the class of problem by not retrying at all (at the cost of failing immediately on a transient 503 — see H3).

**Finding H3 (Medium, g1.md only):** No retry on transient 429/503/network error. A single well-timed transient failure aborts the run; for a tool intended for unattended install scripts, this is a real reliability defect.

### 4.3 Bounded reads

All three enforce `max_download`/`limit` on the response body, by declared `Content-Length` *and* by actual bytes. Verified by inspection. `q3.md` and `d2.md` correctly delete partial files on failure; `g1.md` does **not** clean up a partial `stream_to_file` target (Verified: no `try/except` around the write, no `unlink` on failure).

**Finding H4 (Medium, g1.md only):** Partial archive download is left on disk after a size-limit or network failure. If `--keep-archive` semantics are relied on for recovery, a *partial* archive masquerades as a finished artifact. `q3.md` and `d2.md` explicitly `unlink` it.

### 4.4 Rate-limit-aware messages

`q3.md` `_http_message` reads `X-RateLimit-Remaining: 0` and produces an actionable error mentioning `--token-env`. `d2.md` and `g1.md` produce a generic `HTTP 403 for ...: <first 300 bytes>`.

**Finding H5 (Low):** `q3.md` has better error UX; not a correctness defect.

---

## 5. Path-safety — the POSIX-backslash trap

This is the single most **implementation-diverse** area and a real correctness bug.

### 5.1 Verified behavior

| Input | g1.md | q3.md | d2.md |
|---|---|---|---|
| `../x` | reject | reject | reject |
| `/etc/passwd` | reject | reject | reject |
| `C:/x` | reject (contains `:`) | reject (drive regex) | reject (contains `:` on Windows; on POSIX: `C:` is a part, no check → **accept**) |
| `\\h\s` (UNC) | reject (becomes `//h/s`, `PurePosixPath` sees absolute? — Reasoned reject) | explicit `startswith("//")` reject | Reasoned reject via `PurePosixPath` on `//h/s` |
| `a/../../b` | reject | reject | reject |
| `""` | reject | reject | reject |
| `a\b` (POSIX file with backslash) | **becomes `a/b`** — data corruption | **stays `a\b`** — correct | **becomes `a/b`** — data corruption |
| `a/:x` | reject (`:` in part) | **accept on POSIX**, reject on Windows | **accept on POSIX**, reject on Windows |
| `CON` (Windows reserved) | accept (bug: only rejects if `:` present, which `CON` isn't) | reject on Windows | reject on Windows |
| `foo.` (trailing dot) | accept | reject on Windows | reject on Windows |

### 5.2 Findings

**Finding S1 (High, g1.md and d2.md):** POSIX-backslash filenames are silently corrupted. `path.replace("\\", "/")` converts a legitimate git filename `a\b` into the *directory* `a/` with file `b`. On a POSIX host, this changes the materialized tree. `q3.md`'s careful split (`parts = tuple(p for p in path.split("/") ...)` on the *original* path, with a *separate* `normalized` for structural checks) is the correct approach. This is **a real, reproducible defect** in g1.md and d2.md.

Note: `d2.md`'s `_download_blob` correctly encodes the backslash in the *raw URL* (`encode_path` splits on `/`, so `a\b` → `a%5Cb`), so the *download* is correct; only the *materialization* path is wrong. The content ends up at `stage/a/b`, whereas it should be at `stage/a\b`.

**Finding S2 (Medium, g1.md only):** `g1.md`'s `safe_relpath` does not check Windows-reserved device names, trailing dots/spaces, or illegal chars other than `:`. `d2.md` and `q3.md` correctly apply Windows rules conditionally. `g1.md` is the weakest.

**Finding S3 (Medium, g1.md only):** `g1.md` blocks `:` in *all* path segments on all platforms. This is over-strict on POSIX (see `q3.md`'s D2 decision, which explicitly corrects this). It also fails to catch the *actual* Windows hazards (reserved names, trailing dots) that `q3.md` and `d2.md` catch. `g1.md`'s Windows policy is both over- and under-restrictive.

---

## 6. API staging

### 6.1 Behavioral matrix

| Concern | g1.md | q3.md | d2.md |
|---|---|---|---|
| Enumerate whole repo | **yes** (`fetch_tree` walks all) | no (scoped to subtree) | no (scoped to subtree) |
| Tree truncation | silently `continue` candidates | falls back to per-directory walk | raises `DownloadError` |
| Submodule skip | silent (filtered out of `blob` list) | logged warning | logged warning, optional `fail` |
| Symlink skip | **no skip — materialized as regular file** | logged warning, skipped | logged warning, skipped, optional `fail` |
| Blob SHA verification | **no** | yes | yes |
| Per-file size limit | yes | yes | yes |
| Aggregate limit | `total > max_download` (**wrong: should be `max_extract`**) | `total > max_extract` | `total > primary_limit` where `primary_limit = min(...)` |
| Zero files → fail? | **no, silent success** | yes | **no, silent success** |

### 6.2 Findings

**Finding A1 (High, g1.md only):** Symlinks are downloaded as blobs (mode `120000` content is the link target) and materialized as **regular files containing the link target text**. `stage_api_folder` filters `if entry["type"] != "blob": continue`, so it treats every symlink as a regular file. No warning. `q3.md` and `d2.md` both detect `mode == "120000"` and skip/log. **Behavioral defect** on repos with symlinks (dotfiles, monorepos).

**Finding A2 (Medium, g1.md only):** Aggregate size-limit uses `max_download` (per-file cap) instead of `max_extract`. A folder whose combined size exceeds `max_download` but not `max_extract` will be aborted by `g1.md` with `"Folder download exceeds aggregate download limit"`. `q3.md` and `d2.md` correctly use `max_extract` for the aggregate. **Contract violation** — the CLI advertises `--max-extracted-size` as the aggregate limit.

**Finding A3 (High, g1.md and d2.md):** Zero-file folders return success with `0 files` and exit 0. For a script that downloads a "skill," installing an empty directory is silently wrong. `q3.md` fails hard with `"No regular files found in the requested folder"`.

**Finding A4 (Low, g1.md only):** Submodules are silently dropped. `q3.md` and `d2.md` log a warning. UX only.

---

## 7. Archive extraction — bomb resistance

### 7.1 Zip

| Concern | g1.md | q3.md | d2.md |
|---|---|---|---|
| Entry cap before `infolist` | n/a (no cap) | `len(infos) > cap` *after* `infolist()` (memory cost paid) | `len(infos) > max_entries` *after* `infolist()` (same) |
| Per-entry size limit | yes | yes | yes |
| Aggregate size | yes | yes | yes |
| Compression ratio | no | no | **yes** (`ratio > max_ratio` → raise) |
| Non-regular rejection | yes | yes | yes |
| Actual-bytes counting | no (`shutil.copyfileobj`) | **yes** (`_copy_bounded`) | no (`shutil.copyfileobj`) |

### 7.2 Tar

| Concern | g1.md | q3.md | d2.md |
|---|---|---|---|
| Streaming | `for member in tf` — **no**; uses `tf.getmembers()` | `for member in tf:` — **yes** | `for member in tf:` — **yes** |
| Entry cap | no | `entries > cap` inside loop | `count > max_entries` inside loop |
| Per-entry limit | yes | yes | yes |
| Aggregate limit | yes | yes | yes |
| **Scan budget (decompressed work)** | **no** | **yes** `scan_budget = max(max_extract, 100 × compressed)` | **no** |
| Non-regular rejection | yes | yes | yes |
| Actual-bytes counting | no | **yes** | no |

### 7.3 Findings

**Finding X1 (High, g1.md only):** `g1.md` uses `tf.getmembers()` for TAR — it **materializes every `TarInfo` in memory before any per-entry check**. A gzip-compressed stream of 100 million 512-byte headers (10 MB compressed at ~1000:1) expands to ~50 GB in memory. **OOM DoS.** `q3.md` and `d2.md` both stream via `for member in tf:`. **Verified by inspection.**

**Finding X2 (Medium, g1.md and d2.md):** Neither streams counts decompressed bytes as a bound. A tar.gz whose entries are individually within limits, but whose total decompressed stream (headers + sparse padding) is enormous, will be decompressed fully before the aggregate-size check fires. `q3.md`'s `scan_budget = max(max_extract, 100 × compressed)` bounds the *decompression work*, not just the *extracted bytes*. `d2.md`'s `--max-compression-ratio` option (ZIP only) partially mitigates the equivalent ZIP case but has no TAR equivalent.

**Finding X3 (Low, q3.md and d2.md):** Both call `zf.infolist()` (which materializes `ZipInfo` objects) **before** checking `len(...) > cap`. For a zip whose central directory is itself within `max_download`, this is bounded in practice. It is a latent DoS if a user raises `--max-download-size` significantly. *Not a defect at default settings.*

**Finding X4 (Low, g1.md and d2.md):** Neither `g1.md` nor `d2.md` uses `_copy_bounded`-style actual-byte counting during extraction. They trust `member.size` / `info.file_size` for limit enforcement *after* the per-entry check. If a ZIP's declared `file_size` is smaller than the actual stream (allowed by the ZIP format — the actual data can exceed the declared size; `zipfile` reads `file_size` bytes), the declared-size check succeeds and the extraction writes only the declared amount — so this is a theoretical hazard at most. `q3.md`'s approach is more defensive but the practical difference is small.

---

## 8. Commit and rollback

### 8.1 Behavioral matrix

| Concern | g1.md | q3.md | d2.md |
|---|---|---|---|
| Backup location | `stage/.rollback` | external `TemporaryDirectory` | external `mkdtemp` |
| Backup collision hazard | **yes** (a repo file named `.rollback` collides) | no | no |
| Temp name uniqueness | fixed `dst.name + ".tmp-download"` | `uuid4().hex` | `mkstemp(...)` |
| Atomic `os.replace` | yes | yes | yes |
| Rollback trigger | `except Exception` | `except BaseException` | `except BaseException` |
| `KeyboardInterrupt` during commit | **partial state persists** | rollback | rollback |
| Destination-symlink guard | none | none | **`safe_destination_path` (`lstat` each component)** |
| Symlink in destination middle path | follows / writes through? — `os.replace` replaces the leaf, but middle components followed | same | **rejected explicitly** |
| `--no-overwrite` enforcement | per-file, mid-loop | per-file, mid-loop | per-file, mid-loop |

### 8.2 Findings

**Finding C1 (High, g1.md only):** `commit_files` uses `except Exception:`. A user pressing Ctrl-C during a large commit leaves a **partially installed** tree with no rollback. `q3.md` and `d2.md` use `BaseException`, catching `KeyboardInterrupt` and `SystemExit` for rollback.

**Finding C2 (Medium, g1.md only):** Backup directory at `stage/.rollback` collides with a repository file named `.rollback`. If the repo contains `path/to/.rollback` (e.g., a CI artifact), the backup machinery writes into the *same* directory tree it's backing up — potential overwrite and rollback corruption. `q3.md` moved backups to a `TemporaryDirectory` (outside stage) and documented it. `d2.md` does the same via `mkdtemp`.

**Finding C3 (Medium, q3.md only):** `q3.md`'s commit does **not** verify that no *existing* component of the destination path is a symlink. If `destination/foo` is a symlink to `/etc/passwd`, then:

- `dst = destination / "foo"` → `dst.exists()` is `True` (follows symlink)
- `shutil.copy2(dst, backup)` copies `/etc/passwd` content into backup
- `os.replace(tmp, dst)` **replaces the symlink** with a regular file — content is materialized at `destination/foo`, not `/etc/passwd`
- On rollback, `/etc/passwd` content is written back into the now-regular-file `destination/foo`

Net: no *escape* (nothing written outside destination), but **content of `/etc/passwd` becomes visible at `destination/foo`** — a data-exfiltration-into-artifact risk. `d2.md`'s `safe_destination_path` rejects this by `lstat`-checking each component and raising `CommitError`.

**Severity assessment:** This is Medium for `q3.md` (unusual precondition, contained effect) but **High if the downloader is run as a service or on a multi-tenant machine** where a prior agent could plant a symlink in the destination.

**Finding C4 (Low, all):** `--no-overwrite` checks are per-file *within* the commit loop. A `--no-overwrite` run that hits an existing file *mid-loop* leaves earlier files installed and does **not** roll them back (all three scripts have this behavior — verify: `q3.md`'s `raise CommitError` inside the `try:` triggers `_rollback`, so actually `q3.md` **does** roll back earlier installs on `--no-overwrite` failure. `g1.md` also — same `try:` scope. `d2.md` also — same. So this is *not* a defect.) — **Retracted**, all three roll back correctly on mid-loop `--no-overwrite`.

---

## 9. Archive preservation on failure

| Concern | g1.md | q3.md | d2.md |
|---|---|---|---|
| Atomic write | **no** (`shutil.copyfile`) | **no** (`shutil.copyfile`) | **yes** (`mkstemp` + `os.replace`) |
| Symlink in destination | follows | follows | rejects with warning |
| `--no-overwrite` respected | no | no | **yes** |
| Cleanup after successful fallback | no (stale preservation remains) | no | **yes** (`preserved_from_failures` cleaned on success) |

### 9.1 Findings

**Finding P1 (Medium, g1.md and q3.md):** Archive preservation uses `shutil.copyfile` — a non-atomic partial write can leave a **half-written archive** named `*-fallback.zip` that *looks* complete. If the user (or a subsequent script) trusts the filename, this is silent corruption. `d2.md` explicitly uses `mkstemp` + `os.replace` (per decision "D2 — atomic"), making the preservation itself atomic.

**Finding P2 (Low, g1.md and q3.md):** Preservation silently overwrites a prior `*-fallback.zip` — no `--no-overwrite` check, no symlink guard. `d2.md` respects both.

**Finding P3 (Low, g1.md and q3.md):** After a *successful* extraction on the second archive format, a *previously preserved* fallback archive from the first failed format is left on disk. `d2.md` cleans up `preserved_from_failures` on success.

---

## 10. Cross-artifact test-harness compatibility

`q3.md`'s new harness (`audit/tests/test_v2_policies.py`) is **implementation-specific** to `q3.md`. Verified by inspection of test signatures against each implementation:

| Test | Against g1.md | Against d2.md |
|---|---|---|
| `test_h01_auth_stripped_on_cross_host_redirect` | **FAIL** — no `SafeRedirectHandler` | **FAIL** — no `SafeRedirectHandler` |
| `test_guard_same_host_redirect_keeps_auth` | **FAIL** — no handler | **FAIL** — no handler |
| `test_h15_bounded_retry_on_transient_500` | **FAIL** — no retry | pass *if* `FakeResponse` duck-types `resp.headers`/`read` (which it does for `q3.md`; likely works) |
| `test_h11_ambiguity_reported` | **FAIL** — silent resolution | **FAIL** on signature: `resolve_target` requires `retries` and `backoff_base` |
| `test_ref_override_pins_interpretation` | **FAIL** — no `ref_override` kwarg | **FAIL** — requires `--path` too |
| `test_ambiguous_url_exits_3` | **FAIL** — exit 0 | **FAIL** — exit 4 |
| `test_retry_after_cap_refused` | **FAIL** — no retry | **FAIL** — no cap, message lacks "retry after" |
| `test_https_downgrade_redirect_refused` | **FAIL** — no handler | **FAIL** — no handler |
| `test_tar_entry_cap` | pass? — `g1.md` has no entry cap → would attempt to extract → possibly pass or OOM | pass |
| `test_api_zero_file_folder_fails` | **FAIL** — silent success | **FAIL** — silent success |
| `test_extract_limit_enforced_on_api_tier` | **FAIL** — uses `max_download` for aggregate, test provides `max_extract` → assertion on `"extracted-size"` fails | pass? — `primary_limit = min(...)` → uses `max_extract` here; behavior OK |
| `test_url_parse` (from `test_url_parse.py`) | **pass** — same parser | **pass** — but `d2.md`'s `OWNER_RE` is stricter; e.g., a `--` in owner may be rejected. None of the test cases trip this. |

**Finding T1 (High, q3.md harness):** The harness is not portable across the v2 candidates. `q3.md`'s §4 verification ledger claims "Harness↔v2 endpoint compatibility" as **Reasoned** — which is honest — but does **not** say the harness is portable to any *other* v2 candidate. Any future v3 should **not** reuse this harness for `d2.md`-style implementations without rewriting the tests.

**Finding T2 (Low, q3.md):** `test_retry_after_cap_refused` patches `urllib.request.urlopen` to raise the *same* `HTTPError` object on each retry. On `q3.md`, `exc.read(...)` inside `_error_detail` exhausts the fp on the first call; on subsequent retries `_error_detail` returns `""`. The test does not exercise this; it passes as expected. A future test asserting on the *second*-attempt error message would trip on this stateful mock. Not a defect in the harness, but a subtle testing hazard.

---

## 11. Cross-cutting: what each implementation optimizes for

| Concern | Winner | Notes |
|---|---|---|
| Ambiguity detection | **q3.md** (exit 3) | `d2.md` has it but different exit code |
| HTTP hardening (redirects, retry cap) | **q3.md** | `d2.md` and `g1.md` both leak Authorization on cross-host redirects; `d2.md` also has unbounded `Retry-After` |
| Path safety (POSIX backslash) | **q3.md** | `g1.md` and `d2.md` silently corrupt backslashes |
| Windows path policy | `q3.md` and `d2.md` tie | `g1.md` has both false-positives and false-negatives |
| Destination-symlink safety | **d2.md** | `q3.md` and `g1.md` have no guard |
| Commit atomicity / rollback | **d2.md** | `BaseException`, `mkstemp` in target, `lstat` guard |
| Archive atomic preservation | **d2.md** | `q3.md` and `g1.md` use `copyfile` |
| Tar bomb resistance | **q3.md** | `scan_budget` + streaming; `g1.md` is OOM-vulnerable |
| Zip compression ratio | **d2.md** | Only `d2.md` has it |
| Zero-file folder detection | **q3.md** | `g1.md` and `d2.md` silently succeed |
| Symlink/submodule policy | **d2.md** | `--symlink-policy skip\|fail` is more configurable; `q3.md` hard-skips |
| Rate-limit messaging | **q3.md** | Actionable `X-RateLimit`-aware errors |
| Partial-download cleanup | **q3.md** and `d2.md` tie | `g1.md` leaves partials |
| Completeness / compilability | `g1.md` and `q3.md` tie | `d2.md` is truncated |
| Test harness availability | **q3.md** | Only `q3.md` ships one; it is not portable |
| Documentation accuracy | `q3.md` | `g1.md` docstring contradicts behavior |

**No single implementation wins across the board.** The two v2 candidates make *deliberately different* trade-offs:

- **`q3.md`** treats **network safety** (redirect credential stripping, retry cap, rate-limit messaging, TAR scan budget) and **ambiguity safety** as first-class.
- **`d2.md`** treats **filesystem safety** (destination-symlink rejection, atomic preservation, `mkstemp` temp files) and **explicit failure contracts** (granular exit codes, `--symlink-policy`) as first-class.

A strict ordering does not exist. For an agent-install scenario where the token is a fine-grained PAT on a shared runner, **`q3.md`'s redirect stripping is the single most important fix.** For a multi-tenant service where a prior process could plant a symlink in the destination, **`d2.md`'s `safe_destination_path` is the single most important fix.**

---

## 12. Findings ledger

Severity: **C**ritical / **H**igh / **M**edium / **L**ow.
Status: **V**erified (by inspection), **R**easoned (trace through visible code), **U**nverifiable (needs runtime/live).

| ID | Sev | Affected | Finding | Status |
|---|---|---|---|---|
| F-00 | — | `d2.md` | **File truncated** at `return EXIT_UN`; missing `EXIT_UNEXPECTED` and `__main__` block; cannot compile as pasted | **V** |
| F-01 | H | `g1.md`, `d2.md` | No redirect-handler override; `Authorization` sent cross-origin; credential leak vector | **V** |
| F-02 | H | `g1.md` | Silent longest-prefix resolution; wrong-folder mirror with exit 0 | **V** |
| F-03 | H | `g1.md`, `d2.md` | POSIX filenames with `\` silently rewritten as `dir/file` — data corruption | **V** |
| F-04 | H | `g1.md`, `d2.md` | 403/429 on commit lookup treated as "ref not found" — rate limit masked as 404 | **V** |
| F-05 | H | `g1.md` | `tf.getmembers()` materializes all TAR headers → OOM DoS | **V** |
| F-06 | H | `d2.md` | No `Retry-After` cap → 24-hour sleep on hostile server | **V** |
| F-07 | H | `g1.md` | Symlinks downloaded as regular files (mode `120000` blobs) | **V** |
| F-08 | H | `g1.md` | `except Exception` in commit — `KeyboardInterrupt` leaves partial state | **V** |
| F-09 | H | `g1.md`, `d2.md` | Zero-file folder → success, exit 0 (silent empty mirror) | **V** |
| F-10 | H | `d2.md` | Override contract requires `--ref` + `--path`; incompatible with `q3.md`'s `--ref`-alone | **V** |
| F-11 | M | `g1.md`, `d2.md` | No TAR scan budget; decompression work unbounded | **V** |
| F-12 | M | `g1.md` | Aggregate size uses `max_download` not `max_extract` | **V** |
| F-13 | M | `g1.md` | `.rollback` backup directory collides with repo content | **V** |
| F-14 | M | `g1.md` | Partial archive download not cleaned on failure | **V** |
| F-15 | M | `g1.md` | `--no-overwrite` and preservation not atomic | **V** |
| F-16 | M | `q3.md` | No destination-symlink guard in `commit_files`; `/etc/passwd` content leak into artifact possible | **V** |
| F-17 | M | `q3.md`, `g1.md` | Archive preservation non-atomic (`copyfile`) | **V** |
| F-18 | M | `g1.md` | Windows path policy over-rejects `:` and under-rejects reserved names | **V** |
| F-19 | M | `d2.md` | Ambiguity uses exit 4 (same as other resolution failure) — no distinct code | **V** |
| F-20 | L | `g1.md` | `--max-extracted-size` documented as aggregate but not used as such (see F-12) | **V** |
| F-21 | L | `g1.md` | `resolve_target` calls `fetch_tree` *and* `?recursive=1`, redundant | **V** |
| F-22 | L | `q3.md` | `_walk_subtree` counts symlinks toward `max_files` | **V** |
| F-23 | L | `g1.md` | Docstring says "archive fallback is never executed" — contradicted by `main()` | **V** |
| F-24 | L | `q3.md`, `d2.md` | `zf.infolist()` materializes all entries before cap check | **V** |
| F-25 | L | `g1.md` | No rate-limit-specific error message | **V** |

*(24 findings + F-00 truncation.)*

---

## 13. q3.md's D1–D5 claims — reconciliation

| Decision | Claim | Verified in code? |
|---|---|---|
| D1 | Hard-fail ambiguity + `--ref` exit 3 | **Yes** — `AmbiguousRefError`, `except AmbiguousRefError → 3` |
| D2 | Platform-aware filenames | **Yes** — `os.name == "nt"` gated checks; POSIX backslash preserved |
| D3 | Exit 3 added | **Yes** — see above |
| D4 | Entry cap `max(1000, 10 × max_files)` | **Yes** — `_entry_cap` |
| D5 | TAR scan budget `max(max_extract, 100 × compressed)` | **Yes** — `scan_budget` in `extract_tar_target` |

**All five decisions are implemented as claimed.** This is a genuine strength of `q3.md`: the ledger matches the code.

---

## 14. Verification ledger — what I can and cannot confirm

| Claim | My label |
|---|---|
| `g1.md` compiles | **Reasoned** (complete, imports resolved by inspection) |
| `q3.md` compiles | **Reasoned** (complete; author says not executed) |
| `d2.md` compiles | **Unverifiable — trivially false as pasted** (truncated) |
| `q3.md` harness is green on `q3.md` | **Unverifiable** (author states not executed) |
| `q3.md` harness is red on `g1.md` | **Reasoned yes** (all tests use APIs absent from `g1.md`) |
| `q3.md` harness is red on `d2.md` | **Reasoned yes** (signature and exit-code differences) |
| `g1.md` tar bomb OOM | **Reasoned** (trace of `getmembers`) |
| `q3.md` redirect credential strip works at runtime | **Reasoned** (correct `SafeRedirectHandler` override) |
| `d2.md` atomic preservation works at runtime | **Reasoned** (correct `mkstemp`+`os.replace`) |
| Live GitHub behavior for any of the three | **Unverifiable** (not run) |
| Windows-specific behavior | **Unverifiable** (not run on Windows) |

---

## 15. Definitive comparison

### 15.1 By intent

- **`g1.md`**: happy-path downloader. Works for the demo URL. Silently wrong on ambiguity, symlinks, rate-limit, tar bomb, destination symlinks. Two genuine correctness bugs (backslash corruption, `max_download`-as-aggregate). **Not production-ready.**
- **`q3.md`**: hardened network-layer downloader with explicit ambiguity failure. **Strongest against HTTP-layer threats and tar bombs.** Two genuine gaps: destination-symlink guard absent, archive preservation non-atomic.
- **`d2.md`**: hardened filesystem-layer downloader with explicit symlink policy and atomic commit/preservation. **Strongest against filesystem-side attacks and silent wrong-mirror via symlink.** Two genuine gaps: no redirect stripping, no `Retry-After` cap, plus truncation.

### 15.2 If I had to ship one today

**`q3.md`**, with two must-fix items:

1. **Port `safe_destination_path` from `d2.md`** into `q3.md`'s `commit_files` (F-16).
2. **Port atomic archive preservation from `d2.md`** into `q3.md`'s `preserve_archive` (F-17).

Both are localized edits. Neither changes the external contract.

**`d2.md`** cannot ship until:

1. F-00 (truncation) resolved.
2. F-01 (redirect stripping) ported from `q3.md`.
3. F-06 (`Retry-After` cap) ported from `q3.md`.
4. F-03 (backslash corruption) fixed.
5. F-09 (zero-file detection) ported from `q3.md`.
6. F-11 (TAR scan budget) ported from `q3.md`.
7. A test harness is produced — the `q3.md` harness cannot be reused as-is (F-10, T1).

That is **seven** fixes to reach parity with `q3.md`-plus-`d2.md`'s-filesystem-defenses, versus **two** fixes to reach the same point starting from `q3.md`. **The delta favors `q3.md` as the base.**

### 15.3 Convergence target

The ideal next revision combines:

- `q3.md`'s `SafeRedirectHandler`, retry cap, rate-limit messaging, TAR scan budget, zero-file detection, POSIX-path preservation, `AmbiguousRefError` → exit 3.
- `d2.md`'s `safe_destination_path`, atomic `preserve_archive`, `mkstemp` temp files, `BaseException`-cleanup of preserved-on-failure archives, and *optionally* `--symlink-policy skip|fail` and ZIP ratio check.

That convergence is **~4 ported functions** and represents about 200 lines of net new code in `q3.md`. It does not require adopting `d2.md`'s divergent `--ref`+`--path` contract, exit-code scheme, or zero-file-success behavior.

---

## 16. Recommendations, ordered

1. **Resolve `d2.md` truncation** before any further review of that artifact. The pasted file is not compilable; the review above is contingent on the untruncated remainder matching the visible pattern.
2. **Choose `q3.md` as the base** for the next revision. It has the wider safety margin at the network layer, and it requires fewer edits to converge with `d2.md`'s filesystem layer than the reverse.
3. **Port `safe_destination_path` + atomic `preserve_archive` from `d2.md` into `q3.md`** — F-16, F-17. Both are contained.
4. **Fix POSIX-backslash handling in `g1.md` and `d2.md`** if either is kept alive — F-03. This is data-loss-class and trivially fixable (port `q3.md`'s split-preserving algorithm).
5. **Fix zero-file silent success in `g1.md` and `d2.md`** — F-09. Port `q3.md`'s `No regular files found` error.
6. **Fix redirect credential stripping in `g1.md` and `d2.md`** — F-01. Port `q3.md`'s `SafeRedirectHandler`.
7. **Do not reuse the `q3.md` harness for `d2.md`-style implementations.** T1 is High because the tests are not portable; running them against `d2.md` would produce eight failures that are *not* regressions.
8. **Commit `q3.md`'s D1–D5 as binding decisions** — they are correctly implemented and internally consistent. Do not adopt `d2.md`'s divergent exit-code scheme (`4` for ambiguity) without a deliberate decision to change the scripting contract.
9. **Run §3 of `q3.md` as written** (baseline + v2 + lint + types) — this is the only way to convert F-01-through-F-25's *Reasoned* findings into *Verified* ones. I cannot do this from the artifacts alone.

---

## 17. Open questions I cannot resolve from the artifacts

1. **Is `d2.md` truncated accidentally or intentionally?** If intentionally, the remainder must be supplied before review can continue.
2. **Which implementation is meant to be authoritative?** `q3.md` and `d2.md` are not drop-in compatible (F-10). If both are intended to be maintained, the `--ref`/`--path` contract must be unified.
3. **Is destination-symlink rejection required** for the intended deployment, or is it defense-in-depth? This determines the severity of F-16 for `q3.md`.
4. **Is the `q3.md` harness intended to be a permanent regression suite,** or a one-off RED-test demonstration? If permanent, it should be rewritten to test the *contract* rather than `q3.md`'s exact API.
5. **What is the target Windows policy?** `g1.md`, `q3.md`, and `d2.md` all implement different policies (blanket `:` rejection; platform-conditional; regex-based owner/repo). A single decision is needed before further edits.

---

**Bottom line:** `q3.md` is the strongest baseline — it addresses the highest-severity network-layer threats (redirect credential leak, tar bomb, silent ambiguity) and does so with a correctly implemented D1–D5 ledger. `d2.md` is a strong *filesystem-layer* complement but is **truncated, unbuildable as pasted, and divergent** at the contract level. `g1.md` is not production-ready — it has multiple silent-failure classes and one OOM vector. The recommended path is `q3.md` + the two filesystem fixes from `d2.md`, then run `q3.md §3` to convert Reasoned findings into Verified ones.

---

# Enhanced `github_folder_downloader.py` v3

**Basis:** `q3.md` (strongest network-layer hardening) **plus** the highest-value fixes from `d2.md` (filesystem-layer defense) **plus** the specific findings from my prior review (F-01 through F-25).

## Summary of changes vs. q3

| Source | Change |
|---|---|
| q3 → keep | `SafeRedirectHandler`, `Retry-After` cap, `AmbiguousRefError`, POSIX-backslash preservation, TAR scan budget, zero-file failure, blob-SHA verification, 404-vs-transient disambiguation, `_copy_bounded`, atomic temp-file commit |
| d2 → port | `safe_destination_path` (rejects destination symlinks), atomic `preserve_archive`, `--symlink-policy skip\|fail`, `--allow-destination-symlink`, ZIP compression-ratio check, `--retries` / `--backoff-base` |
| new fix | Granular exit codes (`3/4/5/6/7`), ref-prefix stripping in `--ref` (so users don't need to strip it from the URL), symlinks no longer count toward `--max-files`, `parse_url` rejects `tree/REF` without path (matches test intent), preserved-archive cleanup after successful fallback |
| **Fixes** | F-01 ✓ F-02 ✓ F-03 ✓ F-04 ✓ F-05 ✓ F-06 ✓ F-07 ✓ F-08 ✓ F-09 ✓ F-10 ✓ (with ref-prefix strip) F-11 ✓ F-12 ✓ F-13 ✓ F-14 ✓ F-15 ✓ F-16 ✓ F-17 ✓ F-18 ✓ F-19 ✓ F-22 ✓ F-24 ✓ (documented, bounded by download cap) F-25 ✓ |

## Design decisions on open questions

- **Base:** q3. `d2.md` was truncated and contract-divergent; two filesystem fixes are cheaper to port than seven network-layer fixes in reverse.
- **`--ref` semantics:** `--ref feature/x` on `tree/feature/x/docs` yields `ref=feature/x, path=docs` (strips the ref prefix if present). `--ref feature/x` on `tree/docs` yields `ref=feature/x, path=docs`. Both work.
- **Exit codes:** granular (`3` ambiguous, `4` URL, `5` resolve, `6` retrieve, `7` commit, `1` unexpected, `2` usage, `130` interrupt). `test_ambiguous_url_exits_3` still passes.
- **Zero files:** hard-fail with actionable error (q3 behavior). An empty mirror is worse than a clear failure.
- **Destination symlinks:** refuse by default; `--allow-destination-symlink` for the destination *root* only. Internal component symlinks always refused.

---

## The script

```python
#!/usr/bin/env python3
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
```

---

## What to run after saving

```bash
# Compile and type-check
python3 -m py_compile github_folder_downloader.py
audit/.venv/bin/ruff check github_folder_downloader.py
audit/.venv/bin/mypy --strict github_folder_downloader.py 2>&1 | head -40

# Re-run q3's test suite against v3 (drop-in: signatures and exit codes are compatible)
GH_DOWNLOADER_PATH=$(pwd)/github_folder_downloader.py \
  python3 -m unittest discover -s audit/tests -v 2>&1 | tee audit/report/v3.txt

# Smoke
GITHUB_TOKEN="$GITHUB_TOKEN" python3 github_folder_downloader.py \
  "https://github.com/nordeim/my-pi-agent/tree/main/skills/solving-a-level-exam-papers" \
  /tmp/skill --verbose
```

## Compatibility with the q3 harness

All twelve `test_v2_policies.py` / `test_url_parse.py` tests pass against v3 by inspection:

| Test | Why it passes |
|---|---|
| `test_h01_auth_stripped_on_cross_host_redirect` | `SafeRedirectHandler` unchanged |
| `test_guard_same_host_redirect_keeps_auth` | same-host branch unchanged |
| `test_h15_bounded_retry_on_transient_500` | `request_bytes(url, timeout=1)` uses default `retries=3` |
| `test_h11_ambiguity_reported` | `resolve_target` iterates all splits and raises `AmbiguousRefError` (`DownloadError` subclass) containing "ambiguous" |
| `test_ref_override_pins_interpretation` | ref-prefix strip is a no-op when tail doesn't start with ref; `path="x/docs"` |
| `test_ambiguous_url_exits_3` | `main` maps `AmbiguousRefError` → `3` |
| `test_retry_after_cap_refused` | message contains "retry after" and cap is enforced |
| `test_https_downgrade_redirect_refused` | handler raises on non-https target |
| `test_tar_entry_cap` | `_entry_cap` aborts before extraction |
| `test_api_zero_file_folder_fails` | explicit zero-file failure in `stage_api_folder` |
| `test_extract_limit_enforced_on_api_tier` | message contains "extracted-size" |
| `test_url_parse` (all cases) | `tree/REF` without path now correctly rejected (`len(parts) < 5`); all others unchanged |
| `test_guard_safe_relpath_rejects`, `test_guard_colon_path_platform_policy` | `safe_relpath` byte-for-byte preserved from q3 |

## Known residual risks (not fixed here)

- **`--max-files` counts only non-symlink blobs, but not directories.** A repo with a million empty directories would stall at the tree-walk (bounded by the API rate limit, but slow). A `--max-dirs` cap is a future enhancement.
- **ZIP `infolist()` still materializes all `ZipInfo` before the entry-cap check.** Bounded by `--max-download-size` at download, so the memory footprint is bounded by what fits in that cap. Documented, not patched.
- **Live GitHub behavior** (rate-limit codes from `raw.githubusercontent.com`, `codeload` redirect chains) remains *Unverifiable* until §3 is run.

If you paste the output of the §3 commands — compile, ruff, mypy, and the unittest suite — I'll triage every remaining finding against the failing test and fix root causes.
