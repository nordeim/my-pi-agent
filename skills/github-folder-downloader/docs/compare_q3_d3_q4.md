# Comparative Audit — `github_folder_downloader.py` (q3 v2 → d3 v3 → q4 v3.1)

**Mode:** audit (comparative review). **Workflow:** analyze → plan → validate → implement → verify → deliver. Per your spec, this delivers severity-classified findings and a comparison — **no rewrites**.

**Evidence posture (binding for everything below):** there is no code runner in this session. I have executed nothing. Every finding is **Reasoned** (static read of the attached source) or **Assumed** (fixture-/platform-dependent). The "Verified" labels inside q4.md are *author claims*, not reviewer-verified facts; I audit their reproducibility in §5. Nothing here is Verified by me.

---

## 1. The review plan (meticulous, phase-gated)

| Phase | Action | Inputs | Exit criterion |
|---|---|---|---|
| **0 Scope** | Freeze artifacts; compute full SHA-256 of each script; extract exact CLI/exit-code/function-seam contracts | 3 attached sources | Contracts tabulated; no drift between doc prose and code |
| **1 Analyze** | Lineage trace (q3→d3→q4); threat model: ① malicious repo content (paths, symlinks, blobs) ② malicious archive metadata (sizes, ratios, entry counts, dup names) ③ local attacker (destination symlink swap races) ④ hostile network (TLS downgrade, redirect credential leak, slow-loris) ⑤ GitHub API anomalies (truncation, 403 secondary limits, 404-vs-transient) ⑥ operator error (retry/limit footguns) | Source + threat model | Every trust boundary has ≥1 finding or an explicit "checked, clean" |
| **2 Plan** | Severity rubric ordered per your priority: correctness/safety → security → reliability → maintainability → performance → style. Flag **contract decisions needing your sign-off** (never silently resolved) | Findings draft | Rubric applied; decision list produced |
| **3 Validate** | One RED regression anchor per finding *before* any fix; enumerate harness changes that alter assertions (these require your approval — changing a test to match a corrected spec is legitimate only when disclosed, never to pass a gate) | q3 harness + deltas | Anchor list complete; no assertion weakened |
| **4 Implement** | *N/A in audit mode.* Fixes only on request, as atomic Conventional Commits to `main` via your SSH wrapper | — | — |
| **5 Verify** | Gates: `py_compile` → `ruff` → `mypy --strict` → q3 harness (`GH_DOWNLOADER_PATH`) → q4 `--self-test` → live smoke (slash-branch, LFS, symlink repo, >100k subtree, bad-cert host) → Windows/macOS runners. Reproduce author claims: re-run embedded suite; demand the unshipped 78-test suite; full artifact hash | Runner environment | Each claim promoted Reasoned→Verified only on observed exit 0 |
| **6 Deliver** | Severity findings + head-to-head matrix + claims audit + verification ledger + deferred debt + decision sign-offs | All above | No unverified "works/secure" claims |

**Executed now:** Phases 0–2 and the static desk-check portion of Phase 3 (anchor *names* only). Phases 5's execution gates are pending — commands in §7.

---

## 2. Master findings table (static desk-check)

Status: **P** = present, **F** = fixed, **~** = partial/mitigated, **—** = n/a. Severity: **C**ritical / **H**igh / **M**edium / **L**ow / **I**nfo.

| ID | Sev | Finding (component) | q3 | d3 | q4 |
|---|---|---|---|---|---|
| SH-01 | **H** | **Raw URL built from subtree-relative `entry.path`** (`download_blob`/`stage_api_folder`). GitHub tree listings are subtree-relative; raw needs `target.path + "/" + entry.path`. Every *folder* request 404s on Tier 1 → silent whole-repo archive fallback; hard failure when repo archive > `--max-download-size` even if the folder is tiny. Breaks the tool's core "targeted subtree" promise. | P | P | F (`full_path`) |
| SH-02 | **H** | **Per-directory `truncated` flag ignored** in `TreeCache.listing`. Recursive truncation is handled (walk fallback), but a truncated *single-directory* listing silently mirrors an incomplete folder. q4 fail-closed. | P | P | F |
| SH-03 | **H→L** | **Destination symlink traversal.** q3: no checks; parent-dir symlinks redirect writes outside the tree. d3: `safe_destination_path` lstat loop — correct intent, **TOCTOU window** between check and `mkdir`/`copyfile`/`replace`. q4: `dir_fd` + `O_NOFOLLOW` descent (race-free POSIX); lstat fallback elsewhere retains d3's race (documented). | P | ~ | ~ |
| SH-04 | **M** | **Archive tiers normalize `\`→`/` before slicing `rel`** → POSIX backslash filenames silently become nested dirs in fallback tiers. d3's summary claims "POSIX-backslash preservation" — true for `safe_relpath`/API tier only, **not** ZIP/TAR. q4 `member_views` keeps index-aligned original view. | P | P (claim overstated) | F |
| SH-05 | **M** | **Fidelity losses:** exec bit dropped (breaks executable skill scripts — the smoke target is a skills folder); empty Git dirs dropped in all tiers; LFS pointers materialized as content with no warning; case/NFC collisions silently overwrite during staging on macOS/Windows temp FS. | P | P | F (exec, dirs, `--lfs`, collision probe) |
| SH-06 | **M** | **No global wall-clock budget.** 5000 files × 30 s timeout × retries × slow-loris ⇒ unbounded runtime. | P | P | F (`--deadline`, default 900 s) |
| SH-07 | **L** | **403 secondary rate limit not retried** (not in `RETRY_STATUS`; `Retry-After` on 403 ignored) → spurious hard failure on GitHub's common transient throttle. | P | P | F |
| SH-08 | **L** | **Global `urllib` opener mutation** (`install_opener`) — side effect on any embedding process/test harness. | P | P | F (private opener + lock, TLS ≥1.2) |
| SH-09 | **L** | Redirect origin check ignores **port** (same host, different port keeps `Authorization`); `Retry-After: nan` → `max(0.0, nan)` → 0 s hot retry; repo/path names with control chars enable **log injection**. | P | P | F (host+port, NaN/∞ guard, `safe_log`) |
| SH-10 | **I** | Integrity is SHA-1-only → future SHA-256 repos fail closed (safe but unusable); q4 supports both. `commit_sha` unvalidated before URL construction (q4 `HEX_SHA_RE` refuses). | P | P | F |

### d3-only

| ID | Sev | Finding |
|---|---|---|
| D3-01 | **M** | `--retries 0` passes validation but `range(1, 0+1)` is empty → **guaranteed failure with zero requests**. Also no upper cap (unbounded retry loop). q4: retries-after-first semantics, `0` = one attempt, cap 10. |
| D3-02 | **M** | `--keep-archive` retention runs **after successful commit**; `preserve_archive` raising `CommitError`/`OSError` propagates → exit 7 despite a complete mirror. q4 `safe_retain` is non-fatal by design (D-12). |
| D3-03 | **L** | Extraction-failure preservation catches only `OSError`; a symlink-blocked `preserve_archive` raises `CommitError` → aborts the whole fallback instead of trying TAR.GZ. |
| D3-04 | **L** | ZIP compression-ratio **hard reject** (>1000:1 above 1 MiB) false-rejects legitimate highly-compressible files → unnecessary tier fallback; TAR rescues, but if TAR also fails the run dies on a benign file. q4: advisory warning (bytes already bounded). |
| D3-05 | **I** | `--ref` prefix-strip heuristic can silently select the wrong folder when the folder path legitimately starts with the ref name (e.g. `--ref a` on `tree/a/a` meaning folder `a/a`). q4 D-9 refuses to guess (`--path` explicit). Both are documented; q4 is the safer default. |
| D3-06 | **M** | **Claim audit:** "all twelve tests pass by inspection" is likely false — `test_extract_limit_enforced_on_api_tier` stages `docs/*.bin` via Tier 1 and hits SH-01 (404 message, not "extracted-size"). *Assumed*: depends on the unshipped `ghutil` raw-URL fixture; if it serves subtree-relative raw paths, the fixture itself encodes the bug. |

### q3-only (superseded baseline)

| ID | Sev | Finding |
|---|---|---|
| Q3-01 | **H** | `preserve_archive`: non-atomic `shutil.copyfile`, **follows a pre-planted destination symlink** (writes archive bytes through it), ignores `--no-overwrite`. |
| Q3-02 | **M** | No destination-root symlink refusal; `resolve()` silently follows it. No `--symlink-policy`: API tier skips symlinks but archive tiers **reject** them → tier divergence (a symlink repo succeeds on Tier 1, dies on fallback). |
| Q3-03 | **L** | `IncompleteRead`/`RemoteDisconnected` not retried; symlinks count toward `--max-files` in the walk; URL/resolve/retrieve errors all collapse to exit 1. |

### q4-only (the comparison must cut both ways)

| ID | Sev | Finding |
|---|---|---|
| Q4-01 | **L** | **The "cert errors never retried" guard is likely ineffective on the real path.** `urllib`'s `HTTPSHandler.do_open` wraps `OSError` (incl. `SSLCertVerificationError`) in `URLError`, so the dedicated `except ssl.SSLCertVerificationError` clause is bypassed and the `URLError` clause retries. The self-test patches `_open_request` with a *bare* exception → green test, unexercised production path. Fix direction: inspect `exc.reason`. Fails closed either way (wasteful, not insecure). **Reasoned** — confirm with a bad-cert local TLS server. |
| Q4-02 | **L** | Rollback restore uses a fresh `Config()` (ignores caller `fsync`/deadline); `filesystem_folds_case` probes **case only** (misses NFC/NFD-only collisions on case-sensitive APFS) and falls back to `IS_WINDOWS` on probe failure. |
| Q4-03 | **L** | Archive-tier `make_empty_dirs` creates directories *before* the `max_dirs` check (bounded by entry cap, but up to ~500k `mkdir`s before refusal); `KeyboardInterrupt` during post-commit retention exits 130 despite a complete mirror. |
| Q4-04 | **I** | `.ghfd-archives/` and transient probe files pollute the "faithful mirror" (documented); ~2–3× the code surface of d3 ⇒ larger audit surface; `ruff`/`mypy --strict` still unrun (disclosed). |
| Q4-05 | **I** | **Reproducibility gap:** the "full 78-test suite green" claim is not reproducible from the deliverable (only the 5-test smoke ships); artifact SHA-256 is truncated mid-hash. |

---

## 3. Contract divergences (require your sign-off — not silently resolvable)

| Contract | q3 | d3 | q4 | Note |
|---|---|---|---|---|
| Exit codes | 0/1/2/3/130 | **0/1/2/3/4/5/6/7/130** (granular) | 0/1/2/3/130 + `--json error_class` | d3 breaks any consumer keyed on 1; q4 preserves codes, adds machine detail. Pick one. |
| `…/tree/REF` (no path) | rejected | rejected ("matches test intent") | **accepted** (D-8: real GitHub URL; change the test) | q4 is correct per GitHub semantics, but altering `test_url_parse` is a **contract change needing your approval** — legitimate only because the old test encoded a wrong spec, and it is disclosed. |
| `--ref` semantics | tail = path | **prefix-strip heuristic** | tail = path; `--path` requires `--ref`; no guessing | d3 convenience vs q4 explicitness (D3-05 edge). |
| q3-harness drop-in | baseline | **claimed compatible** (signatures preserved) — but see D3-06 | **not drop-in** (`Config`/`Client` seams, `parse_url`, `_entry_cap` removed); disclosed | d3's compatibility claim is partly overconfident; q4's incompatibility is honest. |
| Ratio policy | none | hard reject | advisory warn | Defense-in-depth vs false-rejection tradeoff. |
| Retention location | dest root, non-atomic | dest root `-fallback`, atomic | `.ghfd-archives/`, atomic, non-fatal | q4 namespaced; all pollute mirror somewhat. |

---

## 4. Head-to-head verdict (ordered per your priority)

| Dimension | Winner | Basis |
|---|---|---|
| Correctness/safety | **q4** | SH-01/02 are core-function defects present in *both* q3 and d3; q4 alone fixes them. d3's "passes by inspection" cannot survive SH-01 on a faithful fixture. |
| Security | **q4** | Race-free POSIX commit, private opener, origin port, SHA validation, log neutralization. d3 is a solid second (lstat checks, atomic retention); q3 has Q3-01/02. Residual: Q4-01, non-POSIX TOCTOU. |
| Reliability | **q4** | Deadline, retry semantics + cap, secondary-403, truncation refusal, non-fatal retention. d3 has D3-01/02 footguns. |
| Maintainability | **q4 (structure) / d3 (size)** | `Config`/`Client` seams vs 12-arg chains; but q4 is ~2–3× larger and its full suite isn't shipped. |
| Performance | **q4** | Streaming blobs (no ~2×100 MiB buffering), EOCD pre-cap, dedupe, header-cost scan budget. |
| Evidence quality | **q3 (honesty) / q4 (execution, partial)** | q3 explicitly labels everything unexecuted. q4 actually ran gates but two claims are non-reproducible from the artifact, and Q4-01 shows a green test that misses the real path. d3's inspection claim is the weakest. |

**Recommendation (conditional):** adopt **q4 as the base**, *gated* on §7 execution — it leads on every priority axis that matters, and its unique defects are Low/Info. Keep **d3** only if granular exit codes or harness drop-in are hard requirements, and then SH-01/02 + D3-01/02 must be fixed first. **q3** is superseded; retain solely as the harness baseline. No adoption claim is made until the gates are observed green.

---

## 5. Author-claims audit

| Claim (source) | Reviewer status |
|---|---|
| q3: "nothing executed; desk-checked only" | Consistent posture; all its behavior claims remain **Unverifiable** until run. |
| d3: "twelve tests pass by inspection" | **Likely false** for ≥1 test (D3-06, SH-01); fixture-dependent → **Assumed**. |
| d3: "POSIX-backslash preservation" | **Overstated** — API tier only (SH-04). |
| q4: self-test/CLI probes "Verified" | Plausible, **re-runnable** (suite ships) — but **Unverifiable by me** here. |
| q4: "78-test suite green", artifact SHA | **Unverifiable** — suite not shipped; hash truncated (Q4-05). |
| q4: "cert errors never retried" | **Contested** (Q4-01) — test exercises a path production doesn't take. |
| All: ruff/mypy/live/Windows/macOS | **Unverifiable** (disclosed in all three ledgers). |

---

## 6. Verification ledger (this review)

| Claim | Method | Status |
|---|---|---|
| All findings SH/D3/Q3/Q4 | Line-by-line static read of attached source | **Reasoned** |
| SH-01/02 GitHub API semantics; D3-06 fixture outcome | API docs knowledge; `ghutil` raw loop not attached | **Assumed** |
| Q4-01 URLError wrapping | `urllib` source knowledge; not executed | **Reasoned** (high confidence) |
| Any runtime/pass/secure claim | No runner in session | **Unverifiable** — none made |

---

## 7. Next actions (converts Reasoned → Verified; no rewrites performed)

**Gates, in order:**
```bash
python3 -m py_compile github_folder_downloader.py
uv pip install ruff mypy && uv run ruff check github_folder_downloader.py \
  && uv run mypy --strict github_folder_downloader.py     # fix the redirect_request override signature; never suppress
GH_DOWNLOADER_PATH=$(pwd)/github_folder_downloader.py \
  python3 -m unittest discover -s audit/tests -v          # expect d3 RED on SH-01; q4 needs disclosed contract updates
python3 github_folder_downloader.py --self-test           # q4 only
sha256sum github_folder_downloader.py                     # full identity, replace truncated hash
# live: slash-branch, LFS repo, symlink repo, >100k subtree, bad-cert host, --dry-run --json
```

**RED anchors to add before any fix (names only):** `test_raw_url_uses_full_repo_path`, `test_directory_listing_truncated_refused`, `test_retries_zero_single_attempt`, `test_keep_archive_failure_nonfatal`, `test_preserve_symlink_continues_fallback`, `test_cert_error_not_retried_via_urlerror_reason`, `test_archive_backslash_preserved_all_tiers`, `test_exec_bit_and_empty_dirs`, `test_case_collision_fails_closed`, `test_deadline_enforced`, `test_secondary_403_retried`.

**Decisions awaiting your sign-off:** exit-code contract (granular vs stable+JSON) · `tree/REF` acceptance (approves the `test_url_parse` change) · `--ref` strip vs explicit `--path` · ratio hard-reject vs advisory · retention location.

**Deferred debt:** live/Windows/macOS verification; q4's unshipped 78-test suite; non-POSIX commit race; NFC/NFD probe; LFS payload fetch; parallelism/resume; directory locking. On request, fixes ship as atomic Conventional Commits to `main` via your SSH wrapper, one RED anchor per commit.
