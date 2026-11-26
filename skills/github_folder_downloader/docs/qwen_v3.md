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


