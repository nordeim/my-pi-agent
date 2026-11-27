# Audit Plan & Critical Comparison — three artifacts, two incompatible "v2"s

**Mode:** audit (findings only; no rewrites performed or proposed as code).
**Evidence posture:** no runner in this session — nothing was compiled, linted, or executed. Every finding below is **Reasoned (static trace)** or **Assumed**, never *Verified*. Where I contradict a document's own "Verified" claim, I give the exact trace so you can falsify me by running it.

---

## 1. Artifact inventory (what I actually have)

| ID | File | Content | Self-claimed status | Runnable as delivered? |
|---|---|---|---|---|
| **V1** | `g1.md` | v1 script + usage guide | compiled + 5 smoke tests passed; live behavior unverified | Script yes; smoke tests **not attached** |
| **Q3** | `q3.md` | v2 script + **harness deltas** + gate commands + ledger | desk-checked only; all behavior *Reasoned*, runtime *Unverifiable* | **No** — deltas against unattached `audit/tests/ghutil.py`, `test_http_and_security.py`, `test_resolution_and_api.py`, `test_archive_and_commit.py` |
| **D2** | `d2.md` | v2 script + self-contained pytest suite + ledger | ~14 rows marked **"Verified (test)"** | Suite is self-contained, but **no execution transcript attached** |

**Blocker B-1 (High, process):** Q3's harness cannot be reconstructed from these three files. `Router`, `api_repo`, `FakeResponse`, `http_error`, `make_target`, `zip_bytes`, `targz_bytes`, `SHA`, `DUMMY_TOKEN`, `RESOLVE` are referenced but undefined here. The differential (baseline-RED → v2-GREEN) design is excellent but unexecutable until the baseline harness is supplied.

**Blocker B-2 (High, process):** D2's ledger asserts test-level verification with no output. Under your evidence rule those rows are **Unverifiable**, and two of them are statically falsifiable (§5).

---

## 2. Review plan (meticulous, ordered, with exit criteria)

### Phase A — Normalize & freeze
1. Extract three scripts to `audit/scratch/v1.py`, `deliverable/q3.py`, `deliverable/d2.py`; record SHA-256 of each so findings are pinned to bytes, not to chat text.
2. Pin toolchain: Python 3.12 **and** 3.13 matrix, `uv`-managed venv, `ruff`, `mypy --strict`, `pytest`. Record exact `mypy`/typeshed versions (Q3's redirect-override signature risk is typeshed-version-sensitive).
3. **Exit:** reproducible environment lock; no hand-edited manifests.

### Phase B — Static subsystem review (same 9 lenses on all three)
| # | Subsystem | Specific questions |
|---|---|---|
| 1 | URL parsing | owner/repo charset, `.`/`..`, `%2F` decode-then-validate order, credentials/query/fragment, `.git` strip |
| 2 | Ref/path resolution | ambiguity policy, 404-vs-403 discrimination, O(depth) vs whole-repo, `truncated` handling **at every tier**, `--ref` semantics incl. root URLs |
| 3 | HTTP seam | HTTPS enforcement, redirect credential scope, retry classes, Retry-After parsing/cap, jitter, partial-body exceptions (`IncompleteRead`, `SSLError`) |
| 4 | Integrity | commit pinning, blob size + SHA, declared-vs-actual byte accounting |
| 5 | Path safety | traversal/absolute/drive/UNC/NUL, POSIX backslash policy, Windows reserved/illegal/trailing, case-insensitive collisions |
| 6 | Archive tiers | entry caps, whole-archive **decompression scan budget**, non-regular members, prefix/root robustness, streaming vs `getmembers()` |
| 7 | Destination commit | symlink traversal (root + intermediate), temp-file uniqueness/mode, atomicity, `BaseException` rollback, backup namespace, `--no-overwrite` scope |
| 8 | Retention & fallback | partial-archive survival, atomic retention, retention honoring `--no-overwrite`, commit-failure isolation, post-success retention failure |
| 9 | CLI/observability | exit-code taxonomy, zero-file success, limit cross-validation, log injection, structured events |

**Exit:** one finding record per defect: ID, locus, trace, impact, severity, falsification test.

### Phase C — Harness & ledger credibility audit
For **every** ledger row in Q3 and D2: does a named test exist, does it exercise the claimed behavior, and can it pass by static trace? Reclassify to Verified/Reasoned/Assumed/Unverifiable. **Exit:** corrected ledger with observed-vs-claimed deltas.

### Phase D — Execution (converts Reasoned → Verified)
```bash
uv venv && uv pip install pytest ruff mypy
uv run python -m py_compile deliverable/q3.py deliverable/d2.py
uv run ruff check deliverable/          # no rule disabling, no noqa additions
uv run mypy --strict deliverable/q3.py
uv run mypy --strict deliverable/d2.py
uv run pytest -q tests                  # D2 suite
GH_DOWNLOADER_PATH=audit/scratch/v1.py uv run python -m unittest discover -s audit/tests -v | tee audit/report/baseline.txt
GH_DOWNLOADER_PATH=deliverable/q3.py  uv run python -m unittest discover -s audit/tests -v | tee audit/report/q3.txt
```
**Exit:** baseline shows defect-tests RED and guards GREEN; Q3 shows all GREEN; D2 reconciled against §5 predictions.

### Phase E — Adversarial fixtures (new regression anchors, one per finding)
Symlinked destination parent; truncated **non-recursive** tree; zero-regular-file folder (submodule-only); symlink inside target subtree in archive tier; 1000:1 legitimate ZIP entry; small gzip with huge non-selected TAR members; `Retry-After: 3600` and `inf`; cross-host redirect with `Authorization`; `--ref` on a root URL; repo named `..`; case-colliding filenames; mode `100755` file; LFS pointer.

### Phase F — Platform & live matrix (gated, opt-in)
Windows + macOS for path/symlink branches; live smoke against controlled repos (slash branch, >100k-entry subtree, symlink repo, LFS repo). **Exit:** severity-classified report + handoff with verified results and deferred debt.

---

## 3. Head-to-head capability matrix

| Control | V1 | Q3 | D2 |
|---|---|---|---|
| Redirect credential scoping + HTTPS-downgrade refusal | ✗ | **✓** | **✗ (unfixed)** |
| Bounded retries / jitter / Retry-After **cap** | ✗ / ✗ / ✗ | ✓ / ✓ / ✓ | ✓ / ✗ / **✗ (unbounded sleep)** |
| `IncompleteRead` retried | ✗ | ✗ | ✓ |
| 404-only ref miss (403/401 not masked) | ✗ | **✓** | ✗ (surfaces `last_error` only) |
| O(depth) path walk, subtree-scoped enumeration | ✗ (whole repo, twice) | ✓ | ✓ |
| `truncated` check: recursive / **per-directory** | ✗ / ✗ | ✓ / **✗** | ✓ / ✓ |
| Ambiguity → hard fail + exit code | ✗ (silent longest) | ✓ (exit 3) | ✓ (exit 4) |
| `--ref` honored on **root** URL | n/a | **✓** | **✗ (silently ignored)** |
| Commit-SHA-pinned raw URLs | ✗ (ref) | ✓ | ✓ |
| Blob size + SHA verification | ✗ | ✓ | ✓ |
| Aggregate cap enforced on API tier | ✗ (wrong cap) | ✓ (`max_extract`) | ✓ (via `min()` in CLI only) |
| Zero-file folder → error | ✗ | **✓** | **✗ (SUCCESS, 0 files)** |
| TAR streaming + entry cap + **scan budget** | ✗ / ✗ / ✗ | ✓ / ✓ / **✓** | ✓ / ✓ / **✗** |
| Actual-byte (not declared) accounting | ✗ | **✓** | ✗ |
| ZIP ratio heuristic | ✗ | ✗ (not needed) | ✓ (**false-positives**) |
| Destination **symlink** refusal | ✗ | **✗** | **✓** (`lstat`, best-effort) |
| Unique temp names / atomic replace | ✗ / ✓ | ✓ (uuid) / ✓ | ✓ (`mkstemp`) / ✓ |
| `BaseException` rollback, backups outside stage | ✗ / ✗ | ✓ / ✓ | ✓ / ✓ |
| Atomic retention honoring `--no-overwrite` | ✗ | **✗** | **✓** |
| Commit failure isolated from fallback | ✗ | **✓** | ✗ (re-downloads TAR) |
| Structured `event=` logging | ✗ | ✗ | **✓** |
| Typed JSON schema validation | ✗ | **✓ (every field)** | partial (`dict` only) |
| LFS pointer warning | ✗ | ✗ | ✓ |
| Exec-bit / mode preservation | ✗ | ✗ | ✗ (worse: files land 0600) |
| `mypy --strict` plausible | ✗ | plausible (1 disclosed risk) | **✗ (certain violations)** |
| Ledger honesty | honest | **honest** | **overclaimed** |

---

## 4. Findings — severity classified

### High

| ID | Artifact / locus | Trace | Impact |
|---|---|---|---|
| **D2-H1** | `_http_get` (no redirect handler anywhere) | Plain `urlopen` → stdlib `HTTPRedirectHandler.redirect_request` copies all non-content headers, incl. `Authorization`, to the new origin; no scheme check | Token exfiltration to redirect target; HTTPS→HTTP downgrade permitted; also breaks signed-URL archive fetches ("only one auth mechanism"). **The headline F-01/H-01 finding is unfixed in D2.** |
| **Q3-H1** | `commit_files` | `dst = destination / rel`; `dst.parent.mkdir(exist_ok=True)` succeeds through a pre-existing symlinked directory; no `lstat`/no-follow | Arbitrary write **outside** destination (dotfiles/`$HOME` mirroring). D2 fixed this; Q3 did not. |
| **Q3-H2** | `TreeCache.listing` | Reads `data["tree"]`, never checks `data.get("truncated")`; used by `_subtree_sha` and `_walk_subtree` | **Silent partial mirror reported as SUCCESS** on a truncated single-directory listing. D2 checks it in both walkers. |
| **D2-H2** | `resolve_target`, `if kind == "root":` branch | Returns default branch **before** consulting `ref_override`/`path_override` | `--ref v1 --path ""` on a root URL silently downloads the default branch. Wrong-version install, no warning. |
| **D2-H3** | `stage_api_folder` / `commit_files` | All-symlink or submodule-only folder → `selected == []` → `(0, 0)`; `commit_files` returns 0; `_run` logs SUCCESS → exit 0 | False success on an empty install. Q3 explicitly errors. |
| **P-H1** | D2 ledger | §5 traces | Verification claims contradicted by static analysis; gates cannot be trusted as reported. |
| **P-H2** | Q3 delivery | Missing `ghutil.py` + 3 test modules | Delivered gates unrunnable; RED→GREEN differential unprovable. |

### Medium

| ID | Artifact | Finding |
|---|---|---|
| D2-M1 | `_http_get` | `time.sleep(wait)` with server-supplied `Retry-After`, **uncapped** (`inf` → `OverflowError`); no jitter → hang / thundering herd. Q3 caps at 60 s and refuses. |
| D2-M2 | `extract_tar_target` | No whole-archive scan budget; non-selected members' bytes are decompressed/skipped without accounting → small gzip, enormous expansion. Q3's D5 budget fixes exactly this. |
| D2-M3 | `resolve_target` | Blanket `except DownloadError` per candidate → 403/401/5xx treated as ref-miss; with `retries=3` this burns 4 requests × N candidates against an already-exhausted quota. |
| D2-M4 | `REPO_RE = ^[A-Za-z0-9._-]{1,100}$` | Accepts `.` and `..` as repo → `https://api.github.com/repos/o/../commits/main` sent with bearer token. V1 and Q3 both reject `.`/`..` explicitly. **Regression.** |
| D2-M5 | `archive_urls` | `commit_sha` interpolated **unencoded/unvalidated** (no 40-hex check). Q3 quotes it. |
| D2-M6 | `extract_zip_target` ratio cap (default 1000) | A 1 MiB zero-filled or highly repetitive legitimate file exceeds 1000:1 → ZIP tier refuses, TAR tier (no ratio check) accepts → tier-dependent behavior + spurious failure. |
| D2-M7 | `download_with_archive_fallback` | `CommitError` → preserve + **continue to TAR** → deterministic destination conflict re-downloads the whole repo. |
| D2-M8 | typing | `_http_get(consume: Callable[[object], object])` returned from functions declared `-> bytes` / `-> int`; unannotated `consume(resp)`; bare `dict` return under `--disallow-any-generics` → **`mypy --strict` cannot pass** without real generics (Q3's `_perform[T]` is the correct pattern). |
| Q3-M1 | `extract_*_target` | Prefix/`rel` computed from `name.replace("\\","/")`, so a legal POSIX filename `a\b` becomes directory `a/b` in archive tiers but stays a file in the API tier → **tier-divergent trees**, contradicting the stated D2 policy. |
| Q3-M2 | `preserve_archive` | Non-atomic `shutil.copyfile` to final name; ignores `--no-overwrite`; name `repo-ref.zip` can **clobber a just-committed repo file**. D2 fixed all three. |
| Q3-M3 | `download_with_archive_fallback`, `if keep_archive:` | `preserve_archive` unguarded → `OSError` after a successful commit → exit 1 "Filesystem error" despite files installed. **D2 has the identical bug** while its ledger claims L4 is handled. |
| Q3-M4 | `_perform` except clauses | `http.client.IncompleteRead` and `ssl.SSLError` during body read are not retried → escape as "Unexpected error". D2 catches `IncompleteRead`. |
| Q3-M5 | `_walk_subtree` | `max_files` counts blobs only; directory count and `TreeCache` growth unbounded. |
| SH-M1 | both | Symlink policy is **skip** on API tier but **hard-fail** inside the target prefix in archive tiers → for any repo with a symlink in the target folder, fallback is unusable. D2's docstring claims skip-or-`fail` uniformly. |
| SH-M2 | both | Git mode `100755` ignored → installed scripts non-executable. D2 additionally lands files at `0600` (`mkstemp`). Directly harms the stated AI-skill-installation use case. |
| SH-M3 | both | LFS payloads never fetched; Q3 doesn't even warn → silent pointer files. |
| SH-M4 | both | No case-insensitive / Unicode-normalization collision detection → silent overwrite on Windows/macOS. |
| SH-M5 | both | Per-operation timeout only; no global wall-clock deadline → 5000 files × 30 s can run for hours. |
| SH-M6 | both | 403 **secondary** rate limits (Retry-After present, `X-RateLimit-Remaining` > 0) are non-retryable → hard failure instead of honoring the hint. |

### Low / Info
- **Q3-L1** `ensure_safe_opener()` mutates process-global `urllib` state on import-driven use; flag is not thread-safe.
- **Q3-L2** entry cap counts **whole-repo** entries, so `--max-files 5` makes archive fallback fail on any normal repo (intentional per its own test, but a usability cliff worth documenting).
- **Q3-L3** ambiguity scan always issues N commit lookups (quota cost of correctness — disclosed, accepted).
- **Q3-L4 / D2-L1** rollback never removes directories it created; second `KeyboardInterrupt` during rollback aborts recovery.
- **D2-L2** `dest_raw.is_symlink()` refusal rejects `/tmp`/`/var` themselves on macOS (flag exists; default friction).
- **D2-L3** `--symlink-policy fail` also governs submodules — name/semantics mismatch.
- **D2-L4** `safe_relpath` returns the **normalized** path (POSIX backslash→directory, V1 behavior retained) and does not reject `NUL`; Q3 rejects NUL and preserves separators.
- **SH-L1** both log unsanitized paths (`%s` / `path=%s`); a POSIX filename containing `\n` enables log forging — more consequential in D2's `key=value` format.
- **SH-L2** neither sends `X-GitHub-Api-Version`; neither dedupes identical blob SHAs; neither fsyncs; duplicate archive member names silently overwrite.
- **SH-I1 (strength, both)** neither uses `extractall`/`extract` → no `tarfile` filter CVE surface; both refuse non-regular members rather than materializing them.

---

## 5. Ledger & harness credibility audit (the decisive difference)

**Two D2 tests cannot pass as written** — static trace, falsifiable by running `pytest`:

1. `TestSafeRelpath.test_rejects["a//b"]` — `PurePosixPath("a//b").parts == ("a","b")`; no part is `""`, `"."`, `".."`; `safe_relpath` **returns** a path. `pytest.raises` fails. → ledger row **M6 "Verified (test)"** is falsified.
2. `TestTargetedRetrieval.test_walk_to_path_does_not_recurse_whole_repo` — the fake returns `{"path": "lvl0"}` while `_walk_to_path` searches for segment `"a"` → `raise DownloadError("Path not found: a")`, uncaught (no `pytest.raises`). → ledger row **H1 "Verified (test)"** is falsified.

**Falsifiable prediction (Reasoned):** on Linux, D2's suite collects **36 tests → 34 pass, 2 fail** (the two above). On Windows add 2 errors from unguarded `symlink_to` in `TestDestinationSymlink`. If your observed counts differ, my trace is wrong and I'll correct it.

**Mis-attributed "Verified (test)" rows in D2:**
- **L6 symlink/submodule policy** → cited `TestSafeRelpath`, which tests *path validation*, not policy. No test exercises `--symlink-policy` or the skip warnings.
- **M3 consistent limits** → the test exercises aggregate `max_download`; the actual `min(max_download, max_extract)` in `_run` and the `--allow-extract-below-download` gate are **untested**.
- **L3 rollback dir outside stage** → `TestRollback` passes through it but asserts nothing about location.
- **L4 retention failure does not fail a succeeded commit** → statically **false** (D2-M3/Q3-M3 above).
- **M5 owner/repo validation** → incomplete: repo `..` accepted (D2-M4).
- **L7 ratio cap**, **M7 partial preservation**, **M2 SHA pinning** → correctly self-labeled *Reasoned (static)*.

**D2 test-quality defects:** `raise X if False else (_ for _ in ()).throw(X)` dead construct in `TestRetries`; `_Headers` defined after use; unused imports (`json`, `http.client`) → `ruff F401` if tests are linted; `TestResolutionAmbiguity`'s fake matches refs by **substring**, so `feature/new-solver/skills/math` also "resolves" — it produces 4 candidates and passes for the wrong reason (it would pass even if resolution always raised ambiguity).

**Q3 harness gaps (its ledger is honest, its guard coverage is not complete):**
- `test_h01` retargeted to `SafeRedirectHandler` is legitimate and disclosed — but **no test asserts the handler is actually installed/used** by `urlopen`. The test stays green even if `ensure_safe_opener()` is never called. Add an opener-installation assertion or a loopback-HTTPS redirect test.
- `test_api_zero_file_folder_fails` calls `api_repo(..., submodules=[...])`; that kwarg is **not** in the published deltas → predicted first-run `TypeError` unless baseline `ghutil` already supports it (**Assumed**).
- `main()` inside tests installs a global opener and calls `logging.basicConfig` → cross-test side effects.
- Q3's disclosed `mypy` override-signature risk remains **Unverifiable** until typeshed version is pinned.

**Harness portability:** the two v2s are **not** drop-in interchangeable. `RepoTarget` (Q3 adds `subtree_sha`), `stage_api_folder` (D2 adds `symlink_policy`, drops `max_extract`), `extract_zip_target` (D2 adds `max_entries`/`max_ratio`), every HTTP function (D2 requires `retries`/`backoff_base`), exception names (`AmbiguousRefError` vs `AmbiguousTargetError`; `IntegrityError`/`LimitExceeded` only in D2), and **exit code 3 means "ambiguous ref" in Q3 but "URL error" in D2**. Neither harness can gate the other script without an adapter layer.

---

## 6. Verdict against your priority order

| Axis | Winner | Basis |
|---|---|---|
| Correctness / safety | **Q3**, narrowly | Q3: zero-file failure, `--ref` on root, 404-only miss, actual-byte accounting, TAR scan budget, NUL rejection. D2 counters with destination-symlink refusal and per-directory truncation checks. Both have one High data-integrity hole (Q3-H2 vs D2-H2/H3). |
| Security | **Q3**, decisively | D2 leaves the credential-leak/downgrade seam completely unfixed (D2-H1) and regresses on repo `..` and unencoded SHA. |
| Reliability | **Q3** | Capped Retry-After + jitter + strict error-class discrimination vs D2's unbounded sleep, masked 403s, and duplicate archive download on commit conflict. D2 wins only on `IncompleteRead`. |
| Maintainability | **Q3** | Typed generic HTTP seam, `Final`, validated JSON, `--strict`-plausible. D2 cannot pass `--strict` without real typing work. |
| Performance | tie | Both O(depth + files); D2 avoids one re-walk, Q3 bounds decompression work. |
| Style / observability | **D2** | Structured `event=` logs, richer exit taxonomy, `--symlink-policy`, `ArgumentDefaultsHelpFormatter`. |
| Evidence integrity | **Q3**, decisively | Honest *Unverifiable* ledger vs D2's falsifiable *Verified* rows. |

**Recommendation (proposal only — no code changed):** adopt **Q3 as the base**, then port six D2 controls as separate, test-anchored increments: (1) no-follow destination commit, (2) per-directory `truncated` refusal, (3) atomic retention honoring `--no-overwrite` + post-success retention failure isolation, (4) `mkstemp` temp files, (5) `IncompleteRead`/`SSLError` retry classes, (6) structured `event=` logging + LFS pointer warning. Do **not** port D2's ratio heuristic or its `--ref`/`--path` pairing.

---

## 7. Decision points I need from you before any implementation

| # | Decision | My recommendation |
|---|---|---|
| D-1 | Base script | Q3 |
| D-2 | Exit-code taxonomy | Keep Q3's `0/1/2/3/130`; add `6` for commit only if you want D2's granularity (breaking change for any wrapper) |
| D-3 | Symlink policy | Unify: **skip + warn in both tiers**, `--symlink-policy fail` for strict; never hard-fail archive tier by default (SH-M1) |
| D-4 | Exec bit | Honor mode `100755` → `0755`; commit files `0644`-equivalent, not `0600` (SH-M2) |
| D-5 | LFS | Warn + non-zero advisory flag, or `--lfs fail`; do not silently install pointers |
| D-6 | Case collisions | Detect and fail with a report on case-insensitive targets |
| D-7 | Harness | Supply baseline `audit/tests/*` (unblocks B-1); add an adapter or keep D2's suite as a separate ported set |

---

## 8. Handoff

**Delivered now:** review plan (Phases A–F with exit criteria), 3-artifact inventory, 30-row capability matrix, **7 High / 18 Medium / 12 Low-Info** findings with loci and traces, ledger credibility audit with two falsifiable test-failure predictions, priority-ordered verdict, gated decision list.

**Verification ledger for *this* review**

| Claim | Method | Status |
|---|---|---|
| All findings above | Static reading of the three attached files | **Reasoned** |
| D2 `a//b` and `_walk_to_path` tests fail | Line-by-line trace of `safe_relpath` / `_walk_to_path` vs fixtures | **Reasoned** (high confidence; falsify with `pytest -q`) |
| 36 tests / 34 pass / 2 fail prediction | Manual collection count | **Reasoned** |
| Q3 `mypy --strict` outcome | Typeshed version unknown | **Unverifiable** |
| `ghutil` internals, `submodules` kwarg support | File not attached | **Assumed** |
| Live GitHub redirect/rate-limit/LFS behavior | Not performed | **Unverifiable** |
| Anything compiles, passes, or is secure | Nothing executed in this session | **Unverifiable** |

**Deferred debt:** execution of all gates; Windows/macOS matrix; live smoke protocol; harness reconstruction; directory-level locking; global deadline; LFS retrieval; resume/Range; concurrency.

**Proposed commit grouping once you approve D-1…D-7** (atomic, Conventional, to `main`, pushed via your SSH wrapper when a repo is available): `fix(security): no-follow destination commit` · `fix(api): refuse truncated per-directory listings` · `fix(io): atomic retention honoring --no-overwrite` · `fix(http): retry incomplete/SSL body failures` · `feat(policy): unified symlink handling + exec bit` · `feat(obs): structured events, LFS warning` · `test(audit): regression anchors + ledger reconciliation` — each preceded by its RED anchor.

Next concrete step: paste `audit/tests/ghutil.py` (and the three revised modules) plus the `pytest`/`ruff`/`mypy` output. I'll reconcile predicted vs observed, correct any trace of mine that's wrong, and fix root causes with the failing test as the anchor.

---

# Cross-Review: Alternative Analysis + Its `v3` Script vs. My Audit

**Mode:** audit of an audit (no rewrites performed). **Nothing executed this session** — every claim below is **Reasoned (static trace)** unless marked otherwise. Where I contradict the alternative, I give the trace so you can falsify me by running it.

**Bottom line:** the alternative is a competent second opinion with roughly 60% overlap with mine, **two findings I missed** (credit given below), but it contains **one Critical intake error that invalidates its top finding and its gating recommendation**, ~8 verifiable technical errors, and it **misses the entire evidence-credibility audit**. Its delivered `v3` script then **repeats the exact failure mode both reviews exist to prevent**: it asserts "all twelve tests pass by inspection" and marks 22 findings ✓ with **zero new tests** and at least one **guaranteed-failure CLI path**. Do not adopt `v3` as delivered.

---

## 1. Critical: the truncation finding (F-00) is an intake artifact, not a defect in `d2.md`

The alternative's #1 finding, its "cannot ship" gate, its recommendation #1, and its open question #1 all rest on `d2.md` ending at `return EXIT_UN`.

**In the copy supplied to me, `d2.md` is complete.** Its tail reads:

```python
    except Exception:
        LOG.exception("Unexpected error.")
        return EXIT_UNEXPECTED
if __name__ == "__main__":
    sys.exit(main())
```

…followed by the full `tests/test_github_folder_downloader.py`, the delivery report, and the verification ledger. `EXIT_UNEXPECTED` is defined at the top and referenced intact; the `__main__` guard is present.

**Two independent errors compound here:**

| # | Claim | Correction |
|---|---|---|
| 1 | "`d2.md` is truncated — **Verified by inspection**" | Their intake was truncated, not the artifact. Labeling a *reader-side* defect **Verified** against the source is precisely the ledger failure mode this review is supposed to catch. |
| 2 | "It will raise `NameError` at import, or `SyntaxError` if compilation reaches that point" | Even for a copy truncated at `return EXIT_UN`, **`py_compile` succeeds** — that is a syntactically complete `return` with a name expression. `EXIT_UN` would only `NameError` *when that except branch executes*, never at import. The compile claim is wrong on its own terms. |

**Severity: Critical (process).** It produced a false blocker, mis-ordered the remediation plan ("resolve truncation before any further review"), and consumed an open question. It also silently removed `d2`'s test suite from their field of view — see §3.

---

## 2. Scorecard

| Category | Count | Notes |
|---|---|---|
| Findings we agree on | ~15 | Redirect leak, retry cap, 403-masking, zero-file success, TAR `getmembers()` OOM, `.rollback` collision, `BaseException` rollback, backslash corruption (g1/d2), aggregate-limit misuse, non-atomic preservation, harness non-portability |
| **They found, I missed** | **2** | F-22 symlink counting toward `--max-files`; the `tree/REF` parser/test mismatch (surfaced only in their v3 change list) |
| **I found, they missed** | **14** | incl. 2 High + the entire ledger/harness credibility audit |
| Verifiable errors in their analysis | 8 | §4 below |
| New defects in their `v3` | 14 | §6 below |

---

## 3. What they missed (highest-value deltas)

| ID | Sev | Missed finding | Why it matters |
|---|---|---|---|
| **M-1** | **High** | **`d2`'s verification ledger is falsifiable.** `TestSafeRelpath.test_rejects["a//b"]` cannot pass (`PurePosixPath("a//b").parts == ("a","b")` → no rejection). `TestTargetedRetrieval.test_walk_to_path_does_not_recurse_whole_repo` cannot pass (fake returns `path="lvl0"`, walker seeks `"a"` → uncaught `DownloadError`). Rows L6/M3/H1 attribute "Verified (test)" to tests that don't exercise the claim. | They never opened `d2`'s suite. Their §11 table states *"Test harness availability — only `q3` ships one"* — **factually false**; `d2` ships ~36 tests. |
| **M-2** | **High** | **`q3.TreeCache.listing` never checks `truncated`** on non-recursive listings, used by `_subtree_sha` and `_walk_subtree`. | Silent partial mirror reported as SUCCESS. Their §6.1 matrix lists "falls back to per-directory walk" as a `q3` *strength* without checking the walk itself. **`v3` does not fix this.** |
| **M-3** | **High** | **`d2` silently ignores `--ref`/`--path` for root URLs** (`if kind == "root":` returns default branch before consulting overrides). | Wrong-version install, no warning. `v3` fixes it incidentally; they never named it. |
| **M-4** | **High** | **`q3`'s harness is not runnable as delivered** — `ghutil.py` (`Router`, `api_repo`, `FakeResponse`, `http_error`, `make_target`, `targz_bytes`, `SHA`, `RESOLVE`…) is referenced but not attached; only deltas are. | Their §0 calls `q3` "Complete + harness"; their recommendation #9 ("run §3 as written") is **not executable**. |
| **M-5** | Medium | **`q3`'s archive tiers normalize backslashes** (`name.replace("\\","/")` → `rel` → materialize), so `a\b` becomes `a/b` there too. | Their F-03 matrix says `q3` "stays `a\b` — correct". True only for the API tier. **`v3`'s "F-03 ✓" is false for both archive tiers.** |
| **M-6** | Medium | `d2` `REPO_RE = ^[A-Za-z0-9._-]{1,100}$` **accepts `..`** → `https://api.github.com/repos/o/../commits/main` sent with bearer token. | Their §2.1 checks owner `..` only. |
| **M-7** | Medium | `d2` interpolates `commit_sha` **unencoded/unvalidated** into codeload URLs. | `q3` quotes it. |
| **M-8** | Medium | **`d2` cannot pass `mypy --strict`** (`Callable[[object], object]` returned as `bytes`/`int`; unannotated `consume(resp)`; bare `dict`). | No type-gate assessment of `d2` anywhere in their review. |
| **M-9** | Medium | **Retention failure after a successful commit → non-zero exit** (both `q3` and `d2`; `d2`'s ledger row L4 claims otherwise). | `v3` makes this *worse* — see V3-M1. |
| **M-10** | Medium | `d2` re-downloads the full TAR after a deterministic **commit** failure. | Wasted bandwidth on `--no-overwrite` conflicts. |
| **M-11** | Medium | `d2`'s ZIP ratio cap **false-positives on legitimate files** (deflate on zeros ≈ 1030:1 > default 1000). | They list the ratio cap as an unqualified `d2` **win**. |
| **M-12** | Medium | Shared: **exec bit (`100755`) dropped**, **LFS pointers committed**, case-insensitive collisions, 403 *secondary* rate limits, no global deadline. | Directly harms the stated skill-installation use case. `v3` **drops `d2`'s LFS warning** — a regression. |
| **M-13** | Low | Log forging via unsanitized paths; global `install_opener` side effects; no test asserts the safe opener is actually installed. | — |
| **M-14** | High | **`q3`'s own harness contains a statically-failing test** — see §5. | Neither review flagged it; their `v3` silently "fixed" the script instead of raising it as a decision. |

---

## 4. Verifiable errors in the alternative's analysis

| ID | Their claim | Trace / correction | Label |
|---|---|---|---|
| **E-1** | `d2` owner regex rejects 39 chars ("max 38") | `^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$` → max = 1+37+1 = **39**. 39 is accepted; 40 rejected. Matches GitHub's real limit. | Reasoned |
| **E-2** | F-16: "**no escape** (nothing written outside destination)" | They analyzed only the **leaf**-symlink case (and left the middle-path row in §8.1 with a literal "?"). The escape is via **parent** components: `dest/sub → /outside`; `dst.parent.mkdir(parents=True, exist_ok=True)` succeeds through the symlink; `copyfile` + `os.replace` land at `/outside/f.txt`. **Severity is High, not Medium.** | Reasoned |
| **E-3** | "`d2`'s granular codes mean a script *cannot* distinguish URL typos from network failures" | Inverted. `d2` gives URL=3, retrieve=5 → **distinguishable**. It is `q3` (both → 1) that cannot. | Reasoned |
| **E-4** | §10: `test_h15`, `test_tar_entry_cap`, `test_extract_limit_enforced_on_api_tier` "pass" against `d2` | All three **`TypeError` on signature**: `d2.request_bytes` requires `token/accept/limit/retries/backoff_base`; `extract_tar_target` requires `max_entries`; `stage_api_folder` has no `max_extract` and requires `symlink_policy/retries/backoff_base`. Their table **understates** incompatibility while claiming "verified by inspection of test signatures". | Reasoned |
| **E-5** | X1: "100M headers, 10 MB compressed at ~1000:1 → ~50 GB" | Internally inconsistent (that is ~5000:1). gzip's ceiling is ≈1032:1, so the 100 MiB download cap bounds the stream at ≈103 GB; `TarInfo` overhead makes OOM occur far earlier. **Class correct, arithmetic wrong.** They also miss that `g1` calls `getmembers()` **twice** and that `r:gz` + `extractfile` seeking re-decompresses from the start (quadratic). | Reasoned |
| **E-6** | "`q3`'s ledger matches the code" (§13) | Contradicted by their own F-16/F-17: `q3` claims "all 22 findings addressed" yet ships no destination-symlink guard and non-atomic retention. D1–D5 match; the global claim does not. | Reasoned |
| **E-7** | "Two fixes vs seven… **neither changes the external contract**" | Porting `safe_destination_path` **does** change behavior: runs into symlinked destinations that previously succeeded now fail. Their own `v3` ships ~10 changes, not 2, and still omits M-2 and M-5. | Reasoned |
| **E-8** | Finding IDs **P1/P2 used twice** (§2.2 owner regex vs §9 preservation); C4 published then retracted inline | Traceability defect in a document intended to drive commits and regression anchors. | Verified (structural) |

**Label discipline:** they mark ~24 static traces **"V — Verified (by inspection)"**, then label the *same class* of claim **"Reasoned"** in §14. Under your evidence rule, static reading is **Reasoned**; *Verified* requires execution. This is the same inflation they'd have caught in `d2` had they read its suite.

---

## 5. Credit where due — and a new finding it surfaced

**Two genuine catches I missed:**

1. **F-22** — `q3` counts symlinks toward `--max-files` in both `_walk_subtree` and `fetch_folder_entries`, then filters them out at materialization. A folder of 5000 symlinks + 1 file fails the cap. Real Low/Medium; `v3` fixes it correctly in both paths.
2. **NEW-1 (High, `q3` harness):** their v3 change list notes "`parse_url` rejects `tree/REF` without path (matches test intent)". Following that thread: `q3.parse_url` uses `len(parts) < 4`, so `https://github.com/o/r/tree/main` → `parts = ["o","r","tree","main"]` (len 4) → **accepted**. But `q3`'s own `test_url_parse.test_rejected_forms` asserts it raises. **That test fails against `q3` — and against `g1`.** Their §10 nonetheless reports `test_url_parse` as "pass" against `g1`.

This is the **third statically-failing test** across the two v2 deliveries (alongside `d2`'s two). It materially strengthens the credibility audit: **neither v2's "all green" expectation survives static analysis.**

**Also better in theirs:** the deployment-context framing (shared-runner PAT → redirect stripping dominates; multi-tenant host → destination-symlink guard dominates) is a sharper decision lens than a single linear ranking; the exit-code matrix is cleaner; and their X4 downgrade (stdlib bounds reads by declared size) is correctly calibrated.

---

## 6. Audit of the delivered `v3` script

Claimed: *"drop-in: signatures and exit codes are compatible"*, *"All twelve tests pass against v3 by inspection"*, 22 findings ✓. **Signatures are indeed compatible** (defaults added, `subtree_sha` retained) — credit. The rest does not hold.

| ID | Sev | Finding | Trace |
|---|---|---|---|
| **V3-H1** | **High** | **`--retries 0` makes zero HTTP requests and always fails.** | `parse_args` rejects only `< 0`; `_perform` loops `range(1, retries+1)` → `range(1,1)` empty → falls through to `raise DownloadError("Request failed after 0 attempts")`. First API call fails; exit 1. Help text says "retry attempts per request", implying 0 = one attempt. **New defect, introduced by v3, catchable by one smoke test.** |
| **V3-H2** | **High** | **~10 behavior changes shipped with zero new tests**; compatibility asserted "by inspection". | Ref-prefix stripping, archive symlink policy, ratio gate, `--retries`/`--backoff-base`, exit-code remap, `parse_url` tightening, symlink counting, preserved-archive cleanup — **none** has a regression anchor. Also: `test_v2_policies` (7) + `test_url_parse` (2) = **9** methods, not "twelve". |
| **V3-H3** | **High** | **"F-03 ✓" is false for archive tiers.** | Both extractors still do `name.replace("\\","/")` before slicing `rel`; `safe_relpath`'s separator preservation is bypassed. POSIX `a\b` still becomes `a/b` via ZIP/TAR. |
| **V3-H4** | **High** | **Per-directory truncation still unchecked** (M-2). | `TreeCache.listing` unchanged → silent partial mirror persists. |
| **V3-M1** | Medium | **`preserve_archive` now raises `CommitError`, which escapes `except OSError`.** | (a) In the extraction-failure handler → aborts the whole fallback, **TAR never attempted**. (b) After a successful commit (`keep_archive`) → propagates → `main` → **exit 7 "commit error" despite files installed**. v3 *worsens* M-9. |
| **V3-M2** | Medium | Ratio gate still false-positives; ZIP-only. | `COMPRESSION_RATIO_MIN_SIZE = 1 MiB` exempts small files (good), but deflate on zeros is ≈1030:1 at **any** size → a legitimate >1 MiB zero-filled/sparse fixture still trips 1000:1, ZIP fails, TAR (no ratio check) succeeds → tier divergence + two full downloads + a spurious `-fallback.zip`. |
| **V3-M3** | Medium | **Exit-code contract broken while claiming compatibility.** | `OSError` 1→**7**, URL 1→**4**, resolve 1→**5**, retrieve 1→**6**. Meanwhile bare `DownloadError` (integrity failure, size caps, unsafe paths) still → **1**, documented as "unexpected error". Granular taxonomy applied inconsistently. |
| **V3-M4** | Medium | **Ref-prefix stripping is a new silent interpretation heuristic.** | `if tail[:len(ref_parts)] == ref_parts: strip`. Defensible, but it is exactly the "guess the user's intent" class D1 forbade, it changes `q3`'s documented "whole tail is the path" contract, and it has **no test**. |
| **V3-M5** | Medium | `parse_url` tightening rejects a **valid GitHub URL form**. | `https://github.com/o/r/tree/main` is a real browse URL. v3 now requires `len(parts) >= 5`. This resolves NEW-1 by changing the *script* to match the test — a legitimate choice, but it is a **user-facing decision** that was made silently. |
| **V3-L1** | Low | **Malformed retention filenames.** | `archive_filename()` → `"r-main.zip"`, then `preserve_archive` appends → **`r-main.zip-fallback.zip`** / `r-main.tar.gz-fallback.tar.gz`. Classic un-traced port composition. |
| **V3-L2** | Low | `allow_root_symlink` is inert; TOCTOU remains. | `_run` passes `dest_raw.resolve()`, so `destination.is_symlink()` is always False. `lstat`-then-`mkdir`-then-`replace` is still raceable (no `O_NOFOLLOW`/`dir_fd`). |
| **V3-L3** | Low | `RemoteDisconnected` is redundant (already ⊂ `ConnectionResetError` ⊂ `ConnectionError`); **`ssl.SSLError` during body read still uncaught**. | |
| **V3-L4** | Low | **LFS warning dropped** (regression vs `d2`); exec bit still lost; retained archives land `0600` via `mkstemp`. | |
| **V3-L5** | Low | **Known `mypy` risk not re-disclosed.** `q3` explicitly flagged the `redirect_request` override/typeshed risk; v3 inherits it and adds a likely `_http_message(..., HTTPMessage)` vs `Mapping[str,str]` mismatch, while asserting cleanliness. **Evidence-honesty regression relative to `q3`.** | Assumed (typeshed-version dependent) |

---

## 7. Reconciled position

**Where both reviews converge (high confidence):** `q3` is the correct base; `d2` is the correct source of filesystem controls; `g1` is not production-ready; the `q3` harness is not portable to `d2`; D1–D5 are implemented as claimed.

**Where I hold my position against the alternative:**
- `d2` is **complete**; its blocker is **ledger credibility**, not truncation.
- Destination-symlink write-through in `q3` is **High** (parent-component escape), not Medium.
- `q3` is **not** fully backslash-safe (archive tiers).
- The remediation delta is **not** "2 vs 7"; both bases need ~8–10 anchored changes, and **neither** review's fix list is complete without M-2, M-5, M-9, M-12.

**Recommendation:** keep `q3` as base. Treat the alternative's `v3` as a **design sketch, not a deliverable** — it must be re-derived as atomic, test-anchored increments. Adopt from it: symlink-count exclusion (F-22), archive-tier symlink skip, the ratio **min-size gate concept** (with a corrected default), preserved-archive cleanup, and the `--ref`-on-root-URL handling. Reject as delivered: `--retries 0`, the exit-code remap, ref-prefix stripping, `parse_url` tightening, and the ✓-without-evidence ledger.

**Decisions I need before any code changes** (adds to my earlier D-1…D-7):

| # | Decision | Recommendation |
|---|---|---|
| D-8 | `tree/REF` (no path): accept as whole-repo-at-ref, or reject? | **Accept**; fix `q3`'s test instead of the script. Rejecting a valid GitHub URL to satisfy a test is the tail wagging the dog. |
| D-9 | Exit-code taxonomy | Keep `q3`'s `0/1/2/3/130`; any remap is a versioned breaking change with wrapper migration notes. |
| D-10 | `--retries` semantics | Define as *total attempts*, minimum 1; reject 0 at parse time. |
| D-11 | Ratio cap | Keep only as an **advisory warning**, or default ≥ 2000 with a min-size gate; never a hard tier-divergent failure. |
| D-12 | Ref-prefix stripping | Drop it, or make it explicit (`--ref` + documented tail semantics) with tests for both branches. |

---

## 8. Falsifiable predictions for the gate run

Run these and reconcile against my predictions; any mismatch falsifies my trace and I'll correct it.

```bash
uv venv && uv pip install pytest ruff mypy
uv run pytest -q tests                       # d2 suite
uv run python -m unittest discover -s audit/tests -v   # q3 suite (needs ghutil.py first)
uv run mypy --strict deliverable/q3.py deliverable/d2.py
```

| Prediction | Expected observation |
|---|---|
| `d2` suite on Linux | **36 collected → 34 pass, 2 fail** (`a//b`, `_walk_to_path`) |
| `q3` `test_url_parse.test_rejected_forms` | **FAIL** on the `tree/main` subTest (NEW-1) |
| `q3` suite as delivered | **Cannot run** — `ghutil` symbols undefined (M-4); `api_repo(..., submodules=...)` likely `TypeError` (Assumed) |
| `d2` under `mypy --strict` | Multiple errors at `_http_get` return sites and unannotated `consume` |
| `v3 --retries 0` | Immediate failure, message `"Request failed after 0 attempts"`, exit 1 |

---

## 9. Verification ledger for this review

| Claim | Method | Status |
|---|---|---|
| `d2.md` is complete in the supplied copy | Direct read of artifact tail | **Verified (artifact inspection)** |
| All technical corrections E-1…E-8, M-1…M-14, V3-H1…V3-L5 | Line-by-line static trace | **Reasoned** |
| `--retries 0` failure; `a//b`; `_walk_to_path`; `tree/main` | Deterministic control/data-flow trace | **Reasoned** (high confidence; falsify by running) |
| Test counts (36 / 9) | Manual collection | **Reasoned** |
| `v3` `mypy --strict` outcome | typeshed version unknown | **Unverifiable** |
| Anything compiles, passes, or is secure | Nothing executed this session | **Unverifiable** |

**Deferred debt:** execution of all gates; `ghutil.py` reconstruction; Windows/macOS matrix; live smoke; exec-bit/LFS/case-collision/deadline controls; TOCTOU-hardened commit.

**Next step:** supply `audit/tests/ghutil.py` + the three revised modules and the gate output. I'll reconcile predicted vs observed, correct any trace of mine that's wrong, and land each fix as an atomic Conventional Commit preceded by its RED anchor — no guardrail weakening, no ✓ without evidence.

---

I'll plan this properly, then build and **actually execute** the script and its regression suite before delivering. Let me start by checking the environment.
The sandbox is stateless between calls, so I'll build, compile and execute the entire deliverable in a single run.
# Plan → Build → Verify → Deliver

**Mode:** generation (audit findings applied). **Workflow:** analyze → plan → validate → implement → verify → deliver. Everything below labelled *Verified* was **actually executed** in a Python 3.10.9 sandbox.

## 1. Execution plan (followed)

| Phase | Action | Exit criterion |
|---|---|---|
| Analyze | Merge my audit + the alternative's valid findings into one fix list | 30 defects, 3 shared gaps |
| Plan | Resolve D‑1…D‑12 by priority: correctness/safety → security → reliability → maintainability → performance → style | no silent guessing anywhere |
| Validate | Write a RED anchor per defect **before** the fix | anchor fails on old behaviour |
| Implement | Single file, stdlib only, `Config` object + `Client` seam (no 12‑arg call chains) | compiles |
| Verify | `py_compile`, embedded offline suite, CLI exit‑code probes | observed green |
| Deliver | Script + ledger + deferred debt | no unverified "works" claims |

## 2. Decisions I made on the open questions

| # | Decision | Rationale |
|---|---|---|
| D‑1 | Base = q3 architecture, rebuilt around `Config`/`Client` | typed, one HTTP seam |
| D‑2 | Symlinks/hardlinks **skip+warn in every tier**; `--symlink-policy fail`; devices/FIFOs always refused; submodules always skip+warn | kills the tier divergence |
| D‑3 | Exec bit honoured (`100755`→`0755`, else `0644`); archives retained `0600` | skills need executable scripts |
| D‑4 | `--lfs warn\|fail` (default warn, counted in summary) | no silent pointers |
| D‑5 | Case/NFC collision detection via a real FS probe → fail closed | no silent overwrite on macOS/Windows |
| D‑6 | Empty Git trees recreated | faithful mirror |
| D‑7 | Exit codes stay **0/1/2/3/130**; `--json` gives `error_class` | no breaking remap, still machine‑readable |
| D‑8 | `…/tree/REF` (no path) **accepted** | it is a real GitHub URL; fix the test, not the script |
| D‑9 | `--ref` alone works (tail = path); `--path` requires `--ref`; **no prefix‑stripping heuristic** | no guessing |
| D‑10 | `--retries N` = retries *after* the first attempt; `0` valid → exactly 1 attempt | fixes v3's guaranteed‑failure path |
| D‑11 | Compression ratio = **advisory warning only** | actual bytes are bounded; avoids false rejections |
| D‑12 | Retention: atomic, into `.ghfd-archives/`, honours `--no-overwrite`, **never fails a successful commit** | fixes both prior bugs |

**New defect found by execution (present in g1, q3 *and* d2, missed by both reviews):** tree listings are **subtree‑relative**, but all three built raw URLs from `entry.path` alone → every file in a nested folder 404s and silently falls back to a whole‑repo archive. Fixed: `full_path = target.path + "/" + entry.path`.

Also fixed vs. both v2s: per‑directory `truncated` refusal, archive‑tier backslash preservation (index‑aligned `member_views`), `O_NOFOLLOW`+`dir_fd` commit (with lstat fallback), global `--deadline`, secondary‑rate‑limit 403 retry, `IncompleteRead`/`SSLError` retry (cert errors never retried), ZIP EOCD entry cap before `infolist()`, TAR scan budget incl. header cost, blob dedupe, streaming downloads (no 100 MiB memory spike), private opener (no global urllib mutation), log‑injection neutralisation, `--dry-run`, `--max-dirs`.

## 3. Verification ledger (observed, not asserted)

| Claim | Method | Status |
|---|---|---|
| Compiles | `py_compile` on the delivered file | **Verified** (exit 0) |
| Embedded suite green | `--self-test --quiet` → `Ran 5 tests … OK` (many subTests) | **Verified** (exit 0) |
| Full 78‑test suite green on this exact production code | executed during development | **Verified** (exit 0) |
| `--version` → `3.1.0`; no args → 2; `--path` w/o `--ref` → 2; bad URL → 1 + `"error_class":"URLParseError"` | CLI probes | **Verified** |
| Symlink escape blocked with **and** without `dir_fd`; rollback on `KeyboardInterrupt`/`OSError`; TAR scan budget; backslash filenames; retention non‑fatal | suite assertions | **Verified** |
| Artifact identity | 2121 lines, 94 305 bytes, SHA‑256 `957484af0bfaf1ff…ada884e3fa` | **Verified** |
| `ruff` / `mypy --strict` | not installable (no network) | **Unverifiable** — no lint/type claim made, no rules disabled |
| Live GitHub, Windows/macOS, LFS payload fetch | not performed | **Unverifiable / deferred** |

Three bugs were caught *by running*, not by reading: the raw‑path defect, `open_root` rejecting an explicitly permitted root symlink, and a fixture error. That is why the suite ships inside the file.

## 4. The deliverable

```python
#!/usr/bin/env python3
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
```

## 5. Run it

```bash
python3 github_folder_downloader.py --self-test          # offline gates, exit 0 expected
python3 github_folder_downloader.py \
  "https://github.com/nordeim/my-pi-agent/tree/main/skills/solving-a-level-exam-papers" \
  /tmp/skill --dry-run --json                            # plan only, writes nothing
GITHUB_TOKEN=… python3 github_folder_downloader.py URL /tmp/skill --json --no-overwrite
```

**Deferred debt (not claimed as done):** `ruff`/`mypy --strict` gates (no network in the sandbox — run `uv pip install ruff mypy` then `uv run mypy --strict github_folder_downloader.py`; the `redirect_request` override signature is the known typeshed‑sensitive spot, fix the signature, never suppress); live GitHub smoke (slash branch, >100k subtree, LFS repo, symlink repo); Windows/macOS runners; LFS payload retrieval; parallel downloads; resume/Range; directory‑level locking.

**Commit grouping when you have the repo** (atomic, Conventional, to `main` via your SSH wrapper): `fix(api): use full repo path for raw retrieval` · `fix(api): refuse truncated directory listings` · `fix(security): no-follow destination commit` · `fix(archive): preserve POSIX backslash filenames in all tiers` · `feat(cli): deadline, dry-run, json summary` · `test: embedded offline regression anchors`.
