# Audit & Validation Plan — `gpt_v1.md` 

**Mode:** C (Audit). Findings only; no remediation without your approval. Any Critical confirmed mid-audit gets surfaced immediately regardless of scope.

**Material constraint (stated up front):** this session has no code-execution environment, and the script exists only as text embedded in the uploaded Markdown. Therefore the audit is two-track:

- **Track 1 — Static audit:** executable now by full-source inspection; every claim labeled **Reasoned** until executed.
- **Track 2 — Dynamic validation:** a runnable offline harness + exact gate commands. Results stay **Unverifiable** until you run them or a Python runner is made available. The prior document's §15 claims ("compilation verified," "smoke tests passed") are treated as unverified provenance and re-checked, not trusted (Appendix B.1).

---

## Phase 1 — Intake & workspace discipline

| Step | Action | Evidence |
|---|---|---|
| 1.1 | Treat uploaded `.md` as read-only. Extract the code block **verbatim** to `audit/scratch/github_folder_downloader.py` | SHA-256 of extracted file recorded; diff against source block = empty |
| 1.2 | Confirm extraction completeness (no truncation, no HTML-entity corruption from the Markdown) | `python3 -m py_compile audit/scratch/github_folder_downloader.py` |
| 1.3 | Final deliverables (report, harness) live in `audit/report/` and `audit/tests/`; scratch never ships | Directory layout |

## Phase 2 — Toolchain validation (before any gate runs)

```bash
python3 --version          # blueprint targets 3.11+; code needs ≥3.10 for `X | None`
python3 -m pytest --version
ruff --version
mypy --version
```

If absent, provision via package manager only (no hand-edited manifests):

```bash
uv venv audit/.venv && uv pip install --python audit/.venv pytest ruff mypy
```

Runtime is stdlib-only — no production dependencies to vet. License/dependency-health dimension is trivially clean (**Reasoned**).

## Phase 3 — Static audit matrix (hypothesis register)

Full read of the provided source is complete. Below is the targeted hypothesis register driving both tracks — **all entries are Reasoned (code inspection), not confirmed findings.** Locations use function names, not fabricated line numbers. Provisional severity applies *if confirmed*.

| ID | Dimension | Location | Hypothesis | Confirmation method | Prov. severity |
|---|---|---|---|---|---|
| H-01 | Correctness/Security | `stream_to_file`, `request_bytes` | urllib's default redirect handler re-sends `Authorization` cross-host (only content headers are stripped). codeload → signed-storage redirect with a token set ⇒ storage rejects dual auth (**authenticated archive fallback broken**) + PAT exposed to third-party origin | Unit-probe `HTTPRedirectHandler.redirect_request` header retention; mocked 302; optional live dummy-token run | High |
| H-02 | Correctness | `download_blob` | Raw downloads use `target.ref`, not resolved `commit_sha` ⇒ slash-branch raw-URL ambiguity + TOCTOU mixed-commit mirror if branch advances mid-run | Assert constructed URL in mock; code path is deterministic | High |
| H-03 | Error handling | `resolve_target` | `except DownloadError: continue` swallows 403/429/5xx/timeouts as "candidate miss" ⇒ rate limit misreported as "unresolved ref" (violates blueprint §11 matrix) | Mock 403/429 on first candidate; assert surfaced cause | High |
| H-04 | Correctness/Scale | `resolve_target` | Recursive-tree `truncated` ⇒ *every* candidate skipped ⇒ hard abort on large repos; combined with archive size cap, no viable retrieval path | Mock truncated tree response | High |
| H-05 | Performance/Reliability | `resolve_target`, `stage_api_folder`, `fetch_tree` | Full-repo per-directory tree walk (N+1) executed **twice**; walk result in `resolve_target` discarded (dead `found`/`tree` assignment) ⇒ unauth 60 req/hr quota exhausts on modest repos, defeating the primary goal | Count mocked API calls for a 40-dir fixture repo | High |
| H-06 | Testing | whole deliverable | Zero automated tests shipped; blueprint §13 DoD unmet | Inventory | High |
| H-07 | Correctness/Policy | `main`, `download_with_archive_fallback` | Primary `except Exception` conflates staging failures with **commit** failures ⇒ `--no-overwrite` conflict / permission / disk-full triggers pointless full-archive download; archive preserved on *commit* failure (retention table says extraction-failure only) | Mock primary success + pre-existing conflict; observe fallback invocation and preserved files | Medium–High |
| H-08 | Security/DoS | `extract_tar_target` | `r:gz` + `getmembers()` fully decompresses the archive *before* any extracted-size check ⇒ decompression-bomb CPU/time cost within the 100 MiB compressed cap | Timed fixture: ~2 MiB gz → 512 MiB zeros; assert scan cost/behavior | Medium–High |
| H-09 | Security/DoS | `extract_zip_target`, `extract_tar_target` | No cap on **total** archive entries pre-selection (`infolist`/`getmembers`) ⇒ memory exhaustion; blueprint §6B/C entry-count guard missing | Fixture with 100k tiny entries outside target prefix | Medium |
| H-10 | Correctness | `safe_relpath` | Rejects `:` in any component and remaps `\` ⇒ legitimate Linux filenames (e.g. `notes:2024.md`) fail **both** tiers | API fixture + archive fixture containing such names | Medium |
| H-11 | Correctness | `resolve_target` | Two simultaneously valid ref/path interpretations silently resolved longest-first; blueprint §4 requires reporting ambiguity | Mock dual-valid refs | Medium |
| H-12 | Robustness | `resolve_target`, `fetch_tree` | Malformed API payloads (`item["path"]` KeyError; `commit.tree = null` AttributeError) escape the `DownloadError` net ⇒ generic "Unexpected error" crash | Mock malformed JSON variants | Medium |
| H-13 | Data integrity | `download_with_archive_fallback` | Partial/oversize downloads preserved as "manual recovery" archives without partial-marker; stray partial ZIP remains even when TAR.GZ subsequently succeeds | Interrupt mock stream mid-body; inspect destination | Medium |
| H-14 | Reliability | `commit_files` | `except Exception` misses `KeyboardInterrupt` ⇒ rollback skipped, destination left partially committed | Inject KI mid-commit; assert pre-existing files intact | Medium |
| H-15 | Reliability | HTTP layer | No retries/backoff/`Retry-After` anywhere (blueprint §9); one transient 500 on one blob ⇒ disproportionate full-repo fallback | Mock single 500 then 200; observe no retry | Medium |
| H-16 | Correctness | `stage_api_folder` | Aggregate API-tier limit uses `max_download`, ignoring `--max-extracted-size` ⇒ limit semantics diverge from CLI help/blueprint | Boundary test at both limits | Medium |
| H-17 | Integrity | `stage_api_folder`, `sha256_file` | Git blob SHA available but never verified; `sha256_file` is dead code ⇒ blueprint §12E hash comparison unimplemented | Corrupt one mocked blob body; expect undetected acceptance | Medium |
| H-18 | Fidelity | `fetch_tree` | Symlink blobs (mode 120000) materialized as plain text files; submodule (`commit`) entries silently dropped — undisclosed divergence | Fixture tree with mode-120000 blob + commit entry | Low–Medium |
| H-19 | Correctness | `commit_files` | Legit staged file named `.rollback` collides with backup dir ⇒ commit failure on both tiers | Fixture file named `.rollback` | Low |
| H-20 | Consistency | `archive_urls` vs `encode_path` | Owner/repo interpolated unencoded into codeload URLs while API paths are encoded; `stream_to_file` HTTPS check is case-sensitive vs `request_bytes` | Odd-name URL fixtures | Low |
| H-21 | Maintainability | various | Loose typing (`api_json` → Any, `list[dict]`), duplicated HTTP layers, magic numbers (10 MiB, 300, 1024), inconsistent keep-archive naming | `ruff` + `mypy --strict` baseline | Low |

**Positive guards to validate (not presumed findings):** traversal/absolute/UNC/drive-path rejection, symlink/hardlink/FIFO/device rejection, no `extractall`, no execution of content, staging-before-commit, HTTPS-only, token never logged. Adversarial fixtures must *confirm* these hold; a failure becomes a Critical finding.

## Phase 4 — Offline dynamic harness (no network, no real tokens)

Tests assert **observable behavior** — bytes on disk, destination state, exit codes, constructed request URLs — never merely that mocks were called (§10). HTTP mocked at `urllib.request.urlopen`; archives crafted in-test via `zipfile`/`tarfile`; dummy token `TEST-TOKEN-DO-NOT-USE` only.

| Test module | Key cases | Covers |
|---|---|---|
| `test_url_parse.py` | plain/slash-branch/encoded/tag/SHA/root URLs; blob, gist, gitlab, userinfo, query, `..`, malformed | blueprint §12A |
| `test_ref_resolution.py` | dual-valid ambiguity; 403/429/500/timeout on candidate; truncated tree; malformed payloads; API-call budget count | H-03/04/05/11/12 |
| `test_api_stage.py` | URL uses commit SHA; symlink blob; submodule; `:`-filename; per-file/aggregate/extracted limits; corrupt blob integrity; depth/count caps | H-02/10/16/17/18 |
| `test_archive_safety.py` | traversal, absolute, `..\`, UNC, drive, symlink/hardlink/FIFO/device entries (ZIP+TAR); multi-root; missing target; corrupt ZIP/TAR; empty archive; `.rollback` filename | guards, H-10/19 |
| `test_archive_limits.py` | entry-count flood; timed small gzip bomb; oversize member; declared-vs-actual size; ratio behavior | H-08/09 |
| `test_http_policy.py` | redirect header retention probe; HTTPS enforcement (both casings); size-cap mid-stream; partial-download preservation; retry absence | H-01/13/15/20 |
| `test_commit.py` | conflict + rollback; `--no-overwrite` (assert **no** archive fallback triggered); KI mid-commit; unrelated files preserved; dest-is-file; read-only dest | H-07/14, guards |
| `test_cli.py` | exit codes 0/1/2/130; MiB parsing; positive-limit validation; token never in captured logs | blueprint §12E |

Gate commands (exact):

```bash
python3 -m py_compile audit/scratch/github_folder_downloader.py
ruff check audit/scratch/github_folder_downloader.py
ruff format --check audit/scratch/github_folder_downloader.py
mypy --strict audit/scratch/github_folder_downloader.py     # baseline audit, not a pass/fail gate to weaken
python3 -m pytest audit/tests -q
```

Per §10/Appendix B.5: lint/type output on legacy code is **finding material**, never silenced or loosened to force green.

## Phase 5 — Live smoke protocol (opt-in; network-gated)

Run only if network is available; courteous volume, no rate-limit abuse (429 behavior stays mocked). Each result recorded with commit SHA of the source repo for reproducibility.

```bash
# root URL, tiny repo
python3 audit/scratch/github_folder_downloader.py \
  "https://github.com/octocat/Hello-World" /tmp/gh-audit/root --verbose
# nested folder, stable public repo
python3 audit/scratch/github_folder_downloader.py \
  "https://github.com/github/gitignore/tree/main/Global" /tmp/gh-audit/global --verbose
# deterministic fallback trigger: primary fails on file-count cap
python3 audit/scratch/github_folder_downloader.py \
  "https://github.com/github/gitignore/tree/main/Global" /tmp/gh-audit/fallback --max-files 1
```

Slash-branch live resolution needs a repo that actually has one — supply a URL or I'll provision a throwaway fixture repo; I won't assume one exists. Authenticated-redirect behavior (H-01) optionally confirmed with a real least-privilege token you export yourself — never pasted into chat.

## Phase 6 — Blueprint compliance & reporting

- Map every §13 Definition-of-Done item to evidence: **met-by-inspection** (CLI contract, argparse, staging, no-execution, configurable limits, exit codes), **gap** (tests, retries, hash verification, ambiguity reporting, ratio/entry guards, extracted-size semantics), **runtime-TBD** (live retrieval, slash branches, preservation paths).
- Report format per §12: severity counts first → findings ordered by severity → each with location, snippet evidence, impact, concrete fix recommendation, confidence tag. No rewrites.
- **Verification ledger** delivered with the report: what was checked, how (inspection / mock execution / live), result.

## Phase 7 — Delivery & change management

Conditional on a repo + SSH wrapper being available (none is evident in this session — flagged, not assumed):

1. `chore(audit): extract downloader fixture and harness scaffolding`
2. `test(audit): add offline safety, correctness, and policy harness`
3. `docs(audit): severity-classified findings with verification ledger`

Fix commits (Mode B, regression-test-first, e.g. `fix(security): drop authorization header on cross-host redirect`) happen **only after you approve specific findings**. Stop rule: two unconfirmed fix attempts ⇒ systematic isolation, per §11.

---

### Verification ledger (this plan)

| Check | Method | Result |
|---|---|---|
| Full source read (complete, untruncated) | In-context inspection | Done — 21 hypotheses registered, all **Reasoned** |
| Runtime/tooling availability | Session inspection | No runner available — dynamic claims **Unverifiable** here |
| Prior §15 "compiled/smoke-tested" claims | Not re-executed | **Unverifiable**; scheduled for re-verification in Phases 1–4 |
| Embedded-instruction scan of uploaded doc (§9) | Inspection | None found; prior-agent claims treated as data, not authority |

---

# Audit Execution — Track 1 Findings + Track 2 Harness

**Execution status:** no code was executed in this session (no runner available). Every finding below is **Reasoned** (full-source inspection of the provided script). The harness is desk-checked, **not run** — its results are **Unverifiable** until you execute it. The script itself is untouched (Mode C: no remediation without approval).

**Plan deviations (disclosed):** 8 test modules consolidated into 4 + one shared utility; tests written as stdlib `unittest` (pytest-compatible) so Track 2 runs with **zero installs**. Harness tests assert *correct* behavior: a **RED** test confirms the corresponding defect and doubles as the post-fix regression test — no inversion needed later.

---

## Track 1 — Findings Report

**Summary: Critical 0 · High 7 · Medium 11 · Low 4** (22 findings). One new defect (F-10) was discovered during desk-check beyond the approved hypothesis register. Traversal/symlink guards appear sound by inspection; adversarial fixtures must confirm before any Critical is ruled out.

### High

**F-01 (H-01) — Authorization header survives cross-host redirects**
- Location: `request_bytes`, `stream_to_file` — stock `urllib.request.urlopen`, no custom opener.
- Evidence: `headers["Authorization"] = "Bearer " + token` + default redirect handling; urllib's `HTTPRedirectHandler.redirect_request` strips only content headers.
- Impact: codeload archive → presigned-storage redirect re-sends the PAT. Dual auth (query signature + `Authorization`) is rejected by presigned storage → **authenticated archive fallback likely broken**; token also exposed to a third-party origin. Storage-response detail is Assumed pending live check; header retention is testable offline (`test_h01`).
- Fix: custom opener whose redirect handler drops `Authorization` when the host changes (requests-style `rebuild_auth`).
- Confidence: Reasoned.

**F-02 (H-02) — Raw downloads use branch ref, not resolved commit SHA**
- Location: `download_blob`.
- Evidence: `.../{encode_path(target.ref)}/{encode_path(path)}` — `target.commit_sha` is resolved but unused here.
- Impact: slash-branch raw-URL ambiguity; branch advancing mid-run yields a mixed-commit mirror (integrity violation vs blueprint §12E).
- Fix: use `target.commit_sha` in the raw URL (already available; one-line change).
- Confidence: Reasoned.

**F-03 (H-03) — Rate-limit/server errors swallowed during ref resolution**
- Location: `resolve_target`.
- Evidence: `except DownloadError:` → `continue` — 403/429/5xx/timeouts treated as candidate misses.
- Impact: rate limiting misreported as "Could not resolve URL ref and folder path"; violates blueprint §11 failure matrix; operators chase the wrong cause.
- Fix: distinguish 404 (candidate miss) from 403/429/5xx/timeout (abort or surface with cause).
- Confidence: Reasoned.

**F-04 (H-04) — Truncated recursive tree aborts all candidates**
- Location: `resolve_target`.
- Evidence: `if recursive.get("truncated"): continue` — truncation is a repo property, identical for every candidate; the 10 MiB `api_json` cap compounds this.
- Impact: large repos (>~100k entries) cannot resolve at all; combined with the archive size cap, **no viable retrieval path**.
- Fix: verify the target path from the already-fetched non-recursive walk, or use the Contents API for the specific path; don't require an untruncated full recursive listing.
- Confidence: Reasoned.

**F-05 (H-05) — Full-repo N+1 tree walk executed twice; first result discarded**
- Location: `resolve_target` (`tree = fetch_tree(...)` feeds only a dead `found` assignment), `stage_api_folder` (walks from repo root again).
- Evidence: per-directory non-recursive calls; no caching; staging walks the whole repo even for a deep subfolder.
- Impact: ~2×(dirs+1) + blobs + candidates requests; unauthenticated 60 req/hr quota exhausts on modest repos → primary fails → full-repo archive fallback, defeating the primary goal.
- Fix: fetch once, cache, and walk only the target subtree (resolve subtree SHA from the recursive listing or Contents API).
- Confidence: Reasoned.

**F-06 (H-06) — No automated tests delivered**
- Location: deliverable inventory.
- Evidence: single script; blueprint §13 DoD explicitly requires tests; §15 "smoke tests passed" is unverified provenance.
- Impact: release gate unmet; safety-critical extraction logic unguarded against regression.
- Fix: adopt the Track-2 harness below as the regression suite.
- Confidence: Reasoned.

**F-07 (H-07) — Archive fallback triggered by commit/policy failures; archive preserved on commit failure**
- Location: `main` (`except Exception as primary_exc:` wraps staging **and** `commit_files`), `download_with_archive_fallback` (preservation on any exception).
- Evidence: `--no-overwrite` conflict, permission error, or disk-full inside `commit_files` falls through to full-archive download; fallback commit failure then preserves an archive.
- Impact: needless whole-repo downloads for deterministic local failures; retention policy deviates (blueprint: preserve only on *extraction* failure); confusing diagnostics.
- Fix: separate staging errors from commit errors; never fall back on commit/policy failures; preserve only when extraction/validation fails.
- Confidence: Reasoned.

### Medium

**F-08 (H-08) — TAR scan decompresses entire archive before any extracted-size check**
- Location: `extract_tar_target` — `tarfile.open(archive, "r:gz")` + `getmembers()`.
- Evidence: reaching the last header requires decompressing all preceding member payloads; `max_extract` sums only *selected* sizes.
- Impact: decompression-bomb CPU/time amplification within the 100 MiB compressed cap (e.g., 100 MiB gz → tens of GiB scanned).
- Fix: stream `r|gz` with a running total-uncompressed budget, or bound scan work explicitly.
- Confidence: Reasoned.

**F-09 (H-09) — No cap on total archive entries**
- Location: `extract_zip_target` (`zf.infolist()`), `extract_tar_target` (`getmembers()`).
- Evidence: limits apply to *selected* entries only; blueprint §6B/C requires excessive-entry guards.
- Impact: memory/CPU exhaustion from archives with millions of out-of-prefix entries.
- Fix: enforce a total-entry cap during enumeration, before selection.
- Confidence: Reasoned.

**F-10 (H-22, new) — Silent success when target directory is absent from archive**
- Location: `extract_zip_target` / `extract_tar_target` — `return len(selected), total` with no `if not selected` guard; `commit_files` happily commits zero files.
- Evidence: no-match selection returns `(0, 0)` → `main` logs SUCCESS, exit 0.
- Impact: violates "target folder not found → abort"; user receives an empty destination reported as success. Same class: API-tier folders containing only submodules.
- Fix: fail with a clear error when zero files are materialized (or the target prefix is absent).
- Confidence: Reasoned.

**F-11 (H-10) — Legitimate filenames rejected or silently remapped**
- Location: `safe_relpath`.
- Evidence: `path.replace("\\", "/")`; `if any(":" in part ...)`.
- Impact: `notes:2024.md` (valid on Linux/macOS) fails **both** tiers; `a\b.md` (valid Git name on POSIX) is silently written to `a/b.md` — data misplacement. On Windows the `:` rejection is protective; disclose platform semantics rather than failing silently.
- Fix: reject only true traversal/absolute/drive forms; handle backslash literally on POSIX; document Windows-incompatible names with a clear per-file error.
- Confidence: Reasoned.

**F-12 (H-11) — Dual-valid ref/path ambiguity silently resolved longest-first**
- Location: `resolve_target`.
- Evidence: first valid candidate returns immediately; shorter interpretations never examined, no warning.
- Impact: blueprint §4 forbids silent selection when ambiguous; wrong folder mirrored without notice.
- Fix: check remaining candidates when one resolves; report ambiguity (or require disambiguation) when multiple interpretations are valid.
- Confidence: Reasoned.

**F-13 (H-12) — Malformed API payload crashes outside the DownloadError net**
- Location: `resolve_target` / root path.
- Evidence: `(commit_data.get("commit") or {}).get("tree", {}).get("sha")` — `"tree": null` yields `None.get(...)` → `AttributeError`, not caught by `except DownloadError`.
- Impact: generic "Unexpected error" exit instead of an actionable diagnostic. (Desk-check correction: the `item["path"]` KeyError arm of the original hypothesis is **refuted** — `fetch_tree` normalizes entries.)
- Fix: type-validate nested payload fields before access.
- Confidence: Reasoned.

**F-14 (H-13) — Partial downloads preserved as "manual recovery" artifacts**
- Location: `download_with_archive_fallback` — `if archive.exists() and archive.stat().st_size:`.
- Evidence: mid-stream size-cap/network failure leaves partial bytes; preserved unmarked; stray partial ZIP remains even when TAR.GZ subsequently succeeds.
- Impact: destination pollution; corrupt archive presented as recoverable; violates retention policy and clean-output discipline.
- Fix: track download completion; preserve only fully downloaded archives; delete partials.
- Confidence: Reasoned.

**F-15 (H-14) — KeyboardInterrupt mid-commit bypasses rollback**
- Location: `commit_files` — `except Exception:` (KI is `BaseException`).
- Impact: destination left partially committed; blueprint §11 requires retaining previously committed files and clean interruption semantics.
- Fix: roll back in `except BaseException:` (re-raise after), or `try/finally` with a success flag.
- Confidence: Reasoned.

**F-16 (H-15) — No retry/backoff/Retry-After anywhere**
- Location: HTTP layer; `import time` is unused.
- Evidence: blueprint §9 explicitly requires bounded retries for 429/transient 5xx.
- Impact: one transient 500 on one blob fails the entire primary tier → disproportionate full-repo fallback.
- Fix: bounded retries with exponential backoff honoring `Retry-After` for 429/5xx.
- Confidence: Reasoned.

**F-17 (H-16) — API tier ignores `--max-extracted-size`; aggregate cap reuses `max_download`**
- Location: `stage_api_folder` — signature has no `max_extract`; `if total > max_download:`.
- Impact: CLI help ("Maximum extracted folder size") misleads; reconstructed-content limit unenforced on the primary path.
- Fix: apply `max_extract` to aggregate staged bytes; keep `max_download` per-response; document semantics.
- Confidence: Reasoned.

**F-18 (H-17) — No content integrity verification; `sha256_file` dead**
- Location: `stage_api_folder` / `download_blob`; unused `sha256_file`.
- Evidence: Git blob SHA-1 in tree metadata never compared to downloaded bytes; blueprint §12E requires hash comparison.
- Fix: verify `sha1(b"blob %d\0" % n + data)` against `entry["sha"]`; remove or repurpose dead helper.
- Confidence: Reasoned.

### Low

**F-19 (H-18) — Symlink blobs materialized as text; submodules silently dropped** — `fetch_tree` ignores `mode` (120000) and filters out `commit` entries. Safe (no symlinks created) but unfaithful and undisclosed. Fix: skip-with-warning or explicit rejection; document. Reasoned.

**F-20 (H-19) — Staged file named `.rollback` breaks commit** — `backup = stage / ".rollback"; backup.mkdir(exist_ok=True)` raises `FileExistsError` on both tiers. Fix: keep backups outside the staged-content namespace. Reasoned.

**F-21 (H-20) — Encoding/case inconsistencies** — `archive_urls` interpolates owner/repo unencoded (`?`/`#` would split the URL; API paths use `encode_path`); `stream_to_file` HTTPS check is case-sensitive vs `request_bytes`. Fix: encode consistently; normalize scheme case. Reasoned.

**F-22 (H-21) — Maintainability cluster** — unused `time` import; dead first `found` assignment; untyped `api_json` return; duplicated HTTP error handling across two functions; undocumented magic numbers (10 MiB, 1024, 300); keep-archive name `repository-fallback.*` vs blueprint's informative `repo-ref.zip`. Fix: targeted cleanups alongside functional fixes. Reasoned.

---

## Track 2 — Runnable Harness

**Layout** (save these five files; extract the script first):

```
audit/
├── scratch/github_folder_downloader.py   # extracted verbatim, never modified
└── tests/
    ├── ghutil.py
    ├── test_http_and_security.py
    ├── test_resolution_and_api.py
    ├── test_archive_and_commit.py
    └── test_cli_integration.py
```

### Phase 1 — extraction + compile re-check (run from the directory containing the uploaded `.md`)

```bash
mkdir -p audit/scratch audit/tests
python3 - <<'PY'
from pathlib import Path
src = Path("github_folder_downloader_v1.md").read_text(encoding="utf-8")
start = src.index("#!/usr/bin/env python3")
code = src[start:src.index("```", start)].rstrip() + "\n"
Path("audit/scratch/github_folder_downloader.py").write_text(code, encoding="utf-8")
PY
python3 -m py_compile audit/scratch/github_folder_downloader.py
```

If compile fails on HTML entities (`&quot;` etc.), apply `html.unescape` to `code` before writing, then recompile — report which path was needed.

### `audit/tests/ghutil.py`

```python
"""Shared harness utilities. Stdlib only, no network, dummy credentials only."""
from __future__ import annotations

import email.message
import hashlib
import io
import json
import sys
import tarfile
import urllib.error
import urllib.parse
import zipfile
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scratch"))
import github_folder_downloader as gfd  # noqa: E402

API = "https://api.github.com"
RAW = "https://raw.githubusercontent.com"
DUMMY_TOKEN = "TEST-TOKEN-DO-NOT-USE"
SHA = "a" * 40
TREE = "b" * 40


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def make_target(path: str = "docs") -> gfd.RepoTarget:
    return gfd.RepoTarget("o", "r", "main", path, SHA, TREE)


class FakeResponse:
    def __init__(self, body: bytes, headers: dict | None = None):
        self._buf = io.BytesIO(body)
        self.headers = email.message.Message()
        for k, v in (headers or {}).items():
            self.headers[k] = v

    def read(self, n: int = -1) -> bytes:
        return self._buf.read(n)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self._buf.close()
        return False


def http_error(url: str, code: int, body: bytes = b'{"message":"error"}') -> urllib.error.HTTPError:
    return urllib.error.HTTPError(url, code, "err", email.message.Message(), io.BytesIO(body))


class Router:
    """Exact-URL routing for mocked urlopen; records every request. Unknown URL -> 404."""

    def __init__(self):
        self.routes: dict = {}
        self.requests: list = []

    def add(self, url: str, body, headers: dict | None = None):
        self.routes[url] = (body, headers)

    def __call__(self, req, timeout=None):
        url = req.full_url
        self.requests.append((url, dict(req.headers)))
        if url not in self.routes:
            raise http_error(url, 404)
        body, headers = self.routes[url]
        if isinstance(body, int):
            raise http_error(url, body)
        return FakeResponse(body, headers)

    def urls(self) -> list:
        return [u for u, _ in self.requests]

    def patch(self):
        return mock.patch("urllib.request.urlopen", side_effect=self)


def api_repo(router: Router, *, blobs: dict, owner: str = "o", repo: str = "r",
             ref: str = "main", sha: str = SHA, tree_sha: str = TREE,
             modes: dict | None = None, submodules=(), truncated: bool = False,
             raw_override: dict | None = None):
    """Serve commits/{ref}, the full non-recursive tree walk, the recursive tree,
    and raw blobs under both ref and commit SHA. Dirs derived from blob paths."""
    modes = modes or {}
    raw_override = raw_override or {}
    dirs = {""}
    for p in list(blobs) + list(submodules):
        parts = p.split("/")
        for i in range(1, len(parts)):
            dirs.add("/".join(parts[:i]))

    def dsha(d: str) -> str:
        return tree_sha if d == "" else hashlib.sha1(f"{tree_sha}:{d}".encode()).hexdigest()

    children = {d: [] for d in dirs}
    recursive = []
    for d in sorted(dirs - {""}):
        parent = d.rsplit("/", 1)[0] if "/" in d else ""
        entry = {"path": d.split("/")[-1], "type": "tree", "sha": dsha(d), "mode": "040000"}
        children[parent].append(entry)
        recursive.append({**entry, "path": d})
    for p, content in blobs.items():
        parent = p.rsplit("/", 1)[0] if "/" in p else ""
        entry = {"path": p.split("/")[-1], "type": "blob", "sha": git_blob_sha(content),
                 "size": len(content), "mode": modes.get(p, "100644")}
        children[parent].append(entry)
        recursive.append({**entry, "path": p})
    for p in submodules:
        parent = p.rsplit("/", 1)[0] if "/" in p else ""
        entry = {"path": p.split("/")[-1], "type": "commit", "sha": "9" * 40}
        children[parent].append(entry)
        recursive.append({**entry, "path": p})

    base = f"{API}/repos/{owner}/{repo}"
    router.add(f"{base}/commits/{ref}",
               json.dumps({"sha": sha, "commit": {"tree": {"sha": tree_sha}}}).encode())
    for d in dirs:
        router.add(f"{base}/git/trees/{dsha(d)}",
                   json.dumps({"tree": children[d], "truncated": False}).encode())
    router.add(f"{base}/git/trees/{tree_sha}?recursive=1",
               json.dumps({"tree": recursive, "truncated": truncated}).encode())
    for p, content in blobs.items():
        enc = "/".join(urllib.parse.quote(x, safe="") for x in p.split("/"))
        body = raw_override.get(p, content)
        router.add(f"{RAW}/{owner}/{repo}/{ref}/{enc}", body)
        router.add(f"{RAW}/{owner}/{repo}/{sha}/{enc}", body)


def zip_bytes(entries, symlinks=(), compression: int = zipfile.ZIP_DEFLATED) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression) as zf:
        for name, data in entries:
            zf.writestr(name, data)
        for name, target in symlinks:
            zi = zipfile.ZipInfo(name)
            zi.external_attr = 0o120777 << 16
            zf.writestr(zi, target.encode())
    return buf.getvalue()


def targz_bytes(entries) -> bytes:
    """entries: (name, kind, payload); kind in file/dir/sym/lnk/fifo."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        for name, kind, payload in entries:
            ti = tarfile.TarInfo(name)
            if kind == "dir":
                ti.type = tarfile.DIRTYPE
                tf.addfile(ti)
            elif kind == "sym":
                ti.type = tarfile.SYMTYPE
                ti.linkname = payload
                tf.addfile(ti)
            elif kind == "lnk":
                ti.type = tarfile.LNKTYPE
                ti.linkname = payload
                tf.addfile(ti)
            elif kind == "fifo":
                ti.type = tarfile.FIFOTYPE
                tf.addfile(ti)
            else:
                data = payload if isinstance(payload, bytes) else payload.encode()
                ti.size = len(data)
                tf.addfile(ti, io.BytesIO(data))
    return buf.getvalue()
```

### `audit/tests/test_http_and_security.py`

```python
"""H-01, H-15, H-20. RED tests confirm defects; GUARD tests must always pass."""
import email.message
import tempfile
import unittest
import urllib.parse
import urllib.request
from pathlib import Path
from unittest import mock

from ghutil import DUMMY_TOKEN, SHA, FakeResponse, Router, gfd, http_error, make_target


class TestHttp(unittest.TestCase):
    def test_h01_auth_stripped_on_cross_host_redirect(self):
        """RED until F-01 fixed. Failure here = stdlib retains Authorization
        cross-host on this interpreter (defect confirmed)."""
        handler = urllib.request.HTTPRedirectHandler()
        req = urllib.request.Request(
            "https://codeload.github.com/o/r/zip/" + SHA,
            headers={"Authorization": "Bearer " + DUMMY_TOKEN})
        new = handler.redirect_request(
            req, None, 302, "Found", email.message.Message(),
            "https://objects.githubusercontent.com/signed?sig=x")
        self.assertIsNotNone(new)
        self.assertIsNone(new.headers.get("Authorization"),
                          "Authorization forwarded to third-party host")

    def test_h15_bounded_retry_on_transient_500(self):
        """RED until F-16 fixed: expects one retry after a transient 500."""
        url = "https://api.github.com/x"
        with mock.patch("urllib.request.urlopen",
                        side_effect=[http_error(url, 500), FakeResponse(b"ok")]) as m:
            try:
                body = gfd.request_bytes(url, timeout=1)
            except gfd.DownloadError:
                body = None
            self.assertEqual(m.call_count, 2, "no retry attempted")
            self.assertEqual(body, b"ok")

    def test_h20_archive_url_components_encoded(self):
        """RED until F-21 fixed: '?' in repo must not become a query string."""
        t = gfd.RepoTarget("o", "a?b", "main", "", SHA, "b" * 40)
        for _, url in gfd.archive_urls(t):
            self.assertEqual(urllib.parse.urlsplit(url).query, "")

    def test_h20_https_scheme_case_consistent(self):
        """RED until F-21 fixed: stream_to_file must accept uppercase scheme
        like request_bytes does."""
        r = Router()
        r.add("HTTPS://api.github.com/x", b"{}")
        with r.patch(), tempfile.TemporaryDirectory() as tmp:
            gfd.request_bytes("HTTPS://api.github.com/x", timeout=1)  # guard arm
            gfd.stream_to_file("HTTPS://api.github.com/x", Path(tmp) / "a",
                               timeout=1, token=None, max_size=100)

    def test_guard_https_enforced(self):
        """GUARD: plaintext HTTP rejected by both request paths."""
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(gfd.DownloadError):
                gfd.request_bytes("http://api.github.com/x", timeout=1)
            with self.assertRaises(gfd.DownloadError):
                gfd.stream_to_file("http://x/y", Path(tmp) / "a",
                                   timeout=1, token=None, max_size=10)


if __name__ == "__main__":
    unittest.main()
```

### `audit/tests/test_resolution_and_api.py`

```python
"""H-02..H-05, H-10..H-12, H-16..H-18. RED confirms defect; GUARD always green."""
import inspect
import json
import tempfile
import unittest
from pathlib import Path

from ghutil import API, SHA, Router, api_repo, gfd, make_target

RESOLVE = dict(timeout=1, token=None)
STAGE = dict(timeout=1, token=None, max_download=10**6, max_files=100, max_depth=10)


def resolve(r, tail=("main", "docs")):
    with r.patch():
        return gfd.resolve_target("o", "r", list(tail), "tree", **RESOLVE)


class TestResolution(unittest.TestCase):
    def test_h03_rate_limit_surfaced_not_masked(self):
        """RED until F-03 fixed: 403 must appear in the failure, not 'unresolved ref'."""
        r = Router()
        for ref in ("main/docs", "main"):
            r.add(f"{API}/repos/o/r/commits/{ref}", 403)
        with r.patch():
            with self.assertRaises(gfd.DownloadError) as ctx:
                gfd.resolve_target("o", "r", ["main", "docs"], "tree", **RESOLVE)
        self.assertIn("403", str(ctx.exception))

    def test_h04_truncated_tree_still_resolves(self):
        """RED until F-04 fixed: walk already proved 'docs' exists."""
        r = Router()
        api_repo(r, blobs={"docs/a.md": b"a"}, truncated=True)
        t = resolve(r)
        self.assertEqual(t.path, "docs")

    def test_h05_tree_walk_not_duplicated(self):
        """RED until F-05 fixed: 4 dirs -> one walk (<=5 tree calls), not two (8)."""
        r = Router()
        api_repo(r, blobs={"docs/a.md": b"a", "src/b.md": b"b",
                           "src/deep/c.md": b"c", "README.md": b"r"})
        with r.patch():
            t = gfd.resolve_target("o", "r", ["main", "docs"], "tree", **RESOLVE)
            with tempfile.TemporaryDirectory() as tmp:
                gfd.stage_api_folder(t, Path(tmp), **STAGE)
        walks = [u for u in r.urls() if "/git/trees/" in u and "recursive" not in u]
        self.assertLessEqual(len(walks), 5, f"{len(walks)} non-recursive tree calls")

    def test_h02_raw_download_pins_commit_sha(self):
        """RED until F-02 fixed: raw URLs must use the resolved SHA, not 'main'."""
        r = Router()
        api_repo(r, blobs={"docs/a.md": b"a"})
        with r.patch():
            t = gfd.resolve_target("o", "r", ["main", "docs"], "tree", **RESOLVE)
            with tempfile.TemporaryDirectory() as tmp:
                gfd.stage_api_folder(t, Path(tmp), **STAGE)
        raw = [u for u in r.urls() if u.startswith("https://raw.githubusercontent.com")]
        self.assertTrue(raw)
        for u in raw:
            self.assertIn(SHA, u, f"unpinned raw URL: {u}")

    def test_h11_ambiguity_alternatives_examined(self):
        """RED until F-12 fixed: both 'feature/x' + docs and 'feature' + x/docs
        are valid; the shorter interpretation must at least be checked."""
        r = Router()
        api_repo(r, ref="feature/x", blobs={"docs/a.md": b"A"},
                 sha="c" * 40, tree_sha="d" * 40)
        api_repo(r, ref="feature", blobs={"x/docs/a.md": b"B"},
                 sha="e" * 40, tree_sha="f" * 40)
        with r.patch():
            gfd.resolve_target("o", "r", ["feature", "x", "docs"], "tree", **RESOLVE)
        self.assertIn(f"{API}/repos/o/r/commits/feature", r.urls(),
                      "shorter valid interpretation never examined")

    def test_h12_malformed_payload_raises_download_error(self):
        """RED until F-13 fixed: 'tree': null must not escape as AttributeError."""
        r = Router()
        r.add(f"{API}/repos/o/r/commits/main",
              json.dumps({"sha": SHA, "commit": {"tree": None}}).encode())
        with r.patch():
            with self.assertRaises(gfd.DownloadError):
                gfd.resolve_target("o", "r", ["main"], "tree", **RESOLVE)

    def test_h16_extract_limit_applies_to_api_tier(self):
        """RED until F-17 fixed: staging must accept/enforce max_extract."""
        self.assertIn("max_extract", inspect.signature(gfd.stage_api_folder).parameters)


class TestApiStaging(unittest.TestCase):
    def stage(self, r, **kw):
        with r.patch():
            t = gfd.resolve_target("o", "r", ["main", "docs"], "tree", **RESOLVE)
            tmp = tempfile.TemporaryDirectory()
            self.addCleanup(tmp.cleanup)
            stage = Path(tmp.name)
            gfd.stage_api_folder(t, stage, **{**STAGE, **kw})
            return stage

    def test_h10_colon_filename_downloads(self):
        """RED until F-11 fixed: POSIX-legitimate name must materialize."""
        r = Router()
        api_repo(r, blobs={"docs/notes:2024.md": b"x"})
        stage = self.stage(r)
        self.assertTrue((stage / "notes:2024.md").exists())

    def test_h10_backslash_filename_preserved(self):
        """RED until F-11 fixed: 'a\\b.md' must not be remapped to 'a/b.md'."""
        r = Router()
        api_repo(r, blobs={"docs/a\\b.md": b"x"})
        stage = self.stage(r)
        self.assertTrue((stage / "a\\b.md").exists(), "filename silently remapped")
        self.assertFalse((stage / "a" / "b.md").exists())

    def test_h17_corrupted_blob_detected(self):
        """RED until F-18 fixed: metadata sha mismatch must fail."""
        r = Router()
        api_repo(r, blobs={"docs/a.md": b"expected"},
                 raw_override={"docs/a.md": b"corrupted"})
        with self.assertRaises(gfd.DownloadError):
            self.stage(r)

    def test_h18_symlink_blob_not_materialized_as_text(self):
        """RED until F-19 fixed: mode-120000 blob must be skipped/rejected, not
        written as a regular file containing the link target."""
        r = Router()
        api_repo(r, blobs={"docs/link": b"../../secret", "docs/a.md": b"a"},
                 modes={"docs/link": "120000"})
        stage = self.stage(r)
        self.assertFalse((stage / "link").exists())

    def test_h18_submodule_drop_warns(self):
        """RED until F-19 fixed: silently dropping a submodule needs a warning."""
        r = Router()
        api_repo(r, blobs={"docs/a.md": b"a"}, submodules=["docs/vendor"])
        with self.assertLogs(gfd.LOG, level="WARNING"):
            self.stage(r)

    def test_guard_happy_path_structure_and_content(self):
        """GUARD: nested layout and bytes reconstructed exactly."""
        r = Router()
        api_repo(r, blobs={"docs/a.md": b"A", "docs/sub/b.bin": b"\x00\x01B"})
        stage = self.stage(r)
        self.assertEqual((stage / "a.md").read_bytes(), b"A")
        self.assertEqual((stage / "sub" / "b.bin").read_bytes(), b"\x00\x01B")


if __name__ == "__main__":
    unittest.main()
```

### `audit/tests/test_archive_and_commit.py`

```python
"""H-08..H-10, H-13, H-14, H-19, H-22 + permanent safety guards."""
import os
import shutil
import tempfile
import time
import unittest
import zipfile
from pathlib import Path
from unittest import mock

from ghutil import Router, gfd, make_target, targz_bytes, zip_bytes

EXTRACT = dict(max_extract=10**6, max_files=100, max_depth=10)
FALLBACK = dict(timeout=1, token=None, max_download=100_000, max_extract=10**6,
                max_files=100, max_depth=10, keep_archive=False, no_overwrite=False)


class TmpCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name)
        self.archive = self.base / "a.bin"
        self.stage = self.base / "stage"
        self.stage.mkdir()
        self.dest = self.base / "dest"
        self.dest.mkdir()

    def write_zip(self, entries, **kw):
        self.archive.write_bytes(zip_bytes(entries, **kw))

    def write_tar(self, entries):
        self.archive.write_bytes(targz_bytes(entries))


class TestGuards(TmpCase):
    def test_guard_safe_relpath_rejects(self):
        for bad in ("../x", "/etc/passwd", "C:/x", "..\\x", "\\\\h\\s",
                    "a/../../b", "", "a/:x"):
            with self.subTest(bad=bad), self.assertRaises(gfd.DownloadError):
                gfd.safe_relpath(bad)

    def test_guard_zip_traversal_rejected(self):
        self.write_zip([("root/docs/../../evil.txt", b"x")])
        with self.assertRaises(gfd.DownloadError):
            gfd.extract_zip_target(self.archive, self.stage, make_target(), **EXTRACT)
        self.assertEqual(list(self.dest.rglob("*")), [])

    def test_guard_zip_absolute_rejected(self):
        self.write_zip([("root/docs//etc/x", b"x")])
        with self.assertRaises(gfd.DownloadError):
            gfd.extract_zip_target(self.archive, self.stage, make_target(), **EXTRACT)

    def test_guard_zip_symlink_rejected(self):
        self.write_zip([("root/docs/a.md", b"a")], symlinks=[("root/docs/l", "../x")])
        with self.assertRaises(gfd.DownloadError):
            gfd.extract_zip_target(self.archive, self.stage, make_target(), **EXTRACT)

    def test_guard_tar_special_entries_rejected(self):
        for kind, payload in (("sym", "../x"), ("lnk", "root/docs/a.md"), ("fifo", "")):
            with self.subTest(kind=kind):
                self.write_tar([("root/docs/a.md", "file", b"a"),
                                ("root/docs/bad", kind, payload)])
                with self.assertRaises(gfd.DownloadError):
                    gfd.extract_tar_target(self.archive, self.stage, make_target(), **EXTRACT)

    def test_guard_tar_traversal_rejected(self):
        self.write_tar([("root/docs/../../evil", "file", b"x")])
        with self.assertRaises(gfd.DownloadError):
            gfd.extract_tar_target(self.archive, self.stage, make_target(), **EXTRACT)

    def test_guard_multi_root_rejected(self):
        self.write_zip([("a/x", b""), ("b/y", b"")])
        with self.assertRaises(gfd.DownloadError):
            gfd.extract_zip_target(self.archive, self.stage, make_target(), **EXTRACT)

    def test_guard_zip_and_tar_happy_path(self):
        self.write_zip([("root/docs/a.md", b"A"), ("root/docs/s/b.md", b"B")])
        self.assertEqual(gfd.extract_zip_target(self.archive, self.stage, make_target(), **EXTRACT), (2, 2))
        self.assertEqual((self.stage / "s" / "b.md").read_bytes(), b"B")
        self.write_tar([("root/docs/a.md", "file", b"A")])
        self.assertEqual(gfd.extract_tar_target(self.archive, self.stage, make_target(), **EXTRACT), (1, 1))

    def test_guard_rollback_on_oserror(self):
        (self.dest / "a.md").write_bytes(b"OLD")
        (self.stage / "a.md").write_bytes(b"NEW")
        (self.stage / "b.md").write_bytes(b"B")
        real, n = os.replace, [0]

        def flaky(src, dst):
            n[0] += 1
            if n[0] == 2:
                raise OSError("simulated disk failure")
            return real(src, dst)

        with mock.patch("os.replace", side_effect=flaky):
            with self.assertRaises(OSError):
                gfd.commit_files(self.stage, self.dest, no_overwrite=False)
        self.assertEqual((self.dest / "a.md").read_bytes(), b"OLD")
        self.assertEqual(len(list(self.dest.iterdir())), 1)


class TestDefects(TmpCase):
    def test_h22_missing_target_fails_loudly(self):
        """RED until F-10 fixed: absent target must not report (0, 0) success."""
        self.write_zip([("root/other/a.md", b"a")])
        with self.assertRaises(gfd.DownloadError):
            gfd.extract_zip_target(self.archive, self.stage, make_target(), **EXTRACT)

    def test_h08_tar_scan_bounded_by_extract_limit(self):
        """RED until F-08 fixed: 64 MiB of non-selected data must not be
        scanned under a 1 KiB extracted budget. Elapsed printed for evidence."""
        self.write_tar([("root/big.bin", "file", b"\0" * (64 * 1024 * 1024)),
                        ("root/docs/a.md", "file", b"ok")])
        t0 = time.perf_counter()
        try:
            gfd.extract_tar_target(self.archive, self.stage, make_target(),
                                   max_extract=1024, max_files=10, max_depth=10)
            raised = False
        except gfd.DownloadError:
            raised = True
        print(f"\n[H-08 evidence] tar scan elapsed: {time.perf_counter() - t0:.2f}s")
        self.assertTrue(raised, "unbounded decompression scan succeeded")

    def test_h09_total_entry_count_capped(self):
        """RED until F-09 fixed: 20k out-of-prefix entries must be rejected."""
        entries = [(f"root/other/f{i}", b"x") for i in range(20_000)]
        entries.append(("root/docs/a.md", b"ok"))
        self.write_zip(entries, compression=zipfile.ZIP_STORED)
        with self.assertRaises(gfd.DownloadError):
            gfd.extract_zip_target(self.archive, self.stage, make_target(),
                                   max_extract=10**6, max_files=5, max_depth=10)

    def test_h19_rollback_filename_commits(self):
        """RED until F-20 fixed: a repo file named '.rollback' must commit."""
        (self.stage / ".rollback").write_bytes(b"legit content")
        gfd.commit_files(self.stage, self.dest, no_overwrite=False)
        self.assertEqual((self.dest / ".rollback").read_bytes(), b"legit content")

    def test_h14_keyboard_interrupt_rolls_back(self):
        """RED until F-15 fixed: KI mid-commit must leave destination untouched."""
        (self.stage / "a.md").write_bytes(b"A")
        (self.stage / "b.md").write_bytes(b"B")
        real, n = shutil.copyfile, [0]

        def flaky(src, dst):
            n[0] += 1
            if n[0] == 2:
                raise KeyboardInterrupt
            return real(src, dst)

        with mock.patch("shutil.copyfile", side_effect=flaky):
            with self.assertRaises(KeyboardInterrupt):
                gfd.commit_files(self.stage, self.dest, no_overwrite=False)
        self.assertEqual(list(self.dest.iterdir()), [], "partial commit left behind")

    def test_h13_no_partial_archive_preserved_on_tar_success(self):
        """RED until F-14 fixed: oversize partial ZIP must be deleted, not kept."""
        t = make_target()
        urls = dict(gfd.archive_urls(t))
        r = Router()
        r.add(urls["zip"], b"Z" * 200_000)  # exceeds 100k cap mid-stream
        r.add(urls["tar.gz"], targz_bytes([("root/docs/a.md", "file", b"ok")]))
        with r.patch():
            count, size, fmt = gfd.download_with_archive_fallback(t, self.dest, **FALLBACK)
        self.assertEqual(fmt, "tar.gz")
        self.assertEqual((self.dest / "a.md").read_bytes(), b"ok")
        stray = self.dest / "r-main-fallback.zip"
        self.assertFalse(stray.exists(), "partial ZIP preserved as recovery artifact")


if __name__ == "__main__":
    unittest.main()
```

### `audit/tests/test_cli_integration.py`

```python
"""H-07 integration + CLI contract guards (exit codes, token hygiene)."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from ghutil import DUMMY_TOKEN, SHA, Router, api_repo, gfd, zip_bytes

URL = "https://github.com/o/r/tree/main/docs"
ZIP_URL = f"https://codeload.github.com/o/r/zip/{SHA}"


class TestCli(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dest = Path(self._tmp.name) / "dest"

    def run_main(self, router, *extra):
        with router.patch(), self.assertLogs(gfd.LOG, level="INFO") as logs:
            rc = gfd.main([URL, str(self.dest), *extra])
        return rc, logs.output

    def test_h07_no_fallback_on_no_overwrite_conflict(self):
        """RED until F-07 fixed: a policy conflict must not trigger codeload."""
        self.dest.mkdir()
        (self.dest / "a.md").write_bytes(b"OLD")
        r = Router()
        api_repo(r, blobs={"docs/a.md": b"NEW"})
        r.add(ZIP_URL, zip_bytes([("root/docs/a.md", b"NEW")]))
        rc, _ = self.run_main(r, "--no-overwrite")
        self.assertEqual(rc, 1)
        self.assertFalse(any("codeload" in u for u in r.urls()),
                         "needless full-archive download on commit conflict")
        self.assertEqual((self.dest / "a.md").read_bytes(), b"OLD")

    def test_h07_no_archive_preserved_on_commit_failure(self):
        """RED until F-07 fixed: retention policy is extraction-failure only."""
        self.dest.mkdir()
        (self.dest / "a.md").write_bytes(b"OLD")
        r = Router()
        api_repo(r, blobs={"docs/a.md": b"NEW"})
        r.add(ZIP_URL, zip_bytes([("root/docs/a.md", b"NEW")]))
        self.run_main(r, "--no-overwrite")
        self.assertFalse((self.dest / "r-main-fallback.zip").exists(),
                         "archive preserved on commit (not extraction) failure")

    def test_guard_primary_success_no_archive(self):
        """GUARD: happy path uses API/raw only, exit 0, correct bytes."""
        r = Router()
        api_repo(r, blobs={"docs/a.md": b"NEW", "docs/s/b.md": b"B"})
        rc, _ = self.run_main(r)
        self.assertEqual(rc, 0)
        self.assertEqual((self.dest / "a.md").read_bytes(), b"NEW")
        self.assertEqual((self.dest / "s" / "b.md").read_bytes(), b"B")
        self.assertFalse(any("codeload" in u for u in r.urls()))

    def test_guard_token_never_logged(self):
        """GUARD: dummy token must not appear in any log record."""
        r = Router()
        api_repo(r, blobs={"docs/a.md": b"NEW"})
        with mock.patch.dict(os.environ, {"GITHUB_TOKEN": DUMMY_TOKEN}):
            rc, output = self.run_main(r)
        self.assertEqual(rc, 0)
        self.assertFalse(any(DUMMY_TOKEN in line for line in output))

    def test_guard_destination_is_file_exit_2(self):
        f = Path(self._tmp.name) / "file"
        f.write_bytes(b"x")
        self.assertEqual(gfd.main([URL, str(f)]), 2)

    def test_guard_interrupt_exit_130(self):
        r = Router()
        api_repo(r, blobs={"docs/a.md": b"NEW"})
        with mock.patch.object(gfd, "stage_api_folder", side_effect=KeyboardInterrupt):
            rc, _ = self.run_main(r)
        self.assertEqual(rc, 130)

    def test_guard_invalid_limits_exit_2(self):
        with self.assertRaises(SystemExit) as ctx:
            gfd.parse_args([URL, "d", "--max-files", "0"])
        self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
```

### Run commands

```bash
# Track 2 — zero-install (stdlib unittest), Python 3.11+
python3 -m unittest discover -s audit/tests -v

# Optional toolchain + alternate runner / static gates (finding material, never weakened to pass)
uv venv audit/.venv && uv pip install --python audit/.venv pytest ruff mypy
audit/.venv/bin/python -m pytest audit/tests -q
audit/.venv/bin/ruff check audit/scratch/github_folder_downloader.py
audit/.venv/bin/mypy --strict audit/scratch/github_folder_downloader.py
```

**Interpretation rule:** RED-labeled tests assert *correct* behavior — their **failure/error confirms the mapped finding**; a *passing* RED test **refutes** that hypothesis on your interpreter (report it back). GUARD tests must pass now and forever. Predicted outcome (Reasoned, not observed): all GUARDs green; ~19 RED tests failing/erroring across F-01…F-21. Live GitHub behavior (F-01 storage rejection, slash-branch raw resolution) remains Unverifiable until the opt-in smoke protocol runs.

---

## Verification Ledger

| Check | Method | Result |
|---|---|---|
| Full script inspection (all functions) | Static, complete source in context | Done — 22 findings, all **Reasoned** |
| Original hypothesis H-12 (KeyError arm) | Desk-check of `fetch_tree` normalization | **Refuted**; narrowed to `tree: null` AttributeError (F-13) |
| New defect H-22 (empty-success) | Desk-check of selection/return path | Added as F-10, **Reasoned** |
| Harness correctness | Desk-check only | **Unverifiable** until executed; harness bugs possible — send output back |
| py_compile / ruff / mypy / pytest | Not run here | Commands provided; prior §15 compile claim re-checked by Phase 1 |
| Live GitHub smoke | Not performed | **Unverifiable**; opt-in protocol from the approved plan stands |

## Handoff

- **Delivered:** severity-classified findings (no script changes), extraction procedure, 5-file regression-ready harness, exact gate commands.
- **Deferred debt (needs your approval → Mode B, regression-test-first):** F-01…F-22 remediation; live smoke protocol; ruff/mypy baseline triage. Suggested fix order: F-01/F-02 (security/integrity, one-line-ish) → F-03/F-04/F-05 (resolution reliability, shared seam) → F-07/F-10/F-14 (policy) → F-08/F-09 (archive hardening) → remainder.
- **Commit grouping (conditional — no repo/SSH wrapper in this session):** `chore(audit): extract downloader fixture and add offline harness`, `docs(audit): severity-classified findings with verification ledger`; fixes as separate `fix(...)` commits per finding once approved.
- **Next action:** run the two command blocks above and return the unittest output (plus ruff/mypy if provisioned). I'll reconcile predicted vs. observed results, mark confirmed/refuted findings Verified, and queue the approved fixes.

---

# v2 Implementation Plan — Hardened GitHub Folder Downloader

**Mode:** A (Generation), driven by the delivered audit (F-01…F-22). Each remediation is regression-backed: the existing harness's RED tests become the acceptance evidence (red on v1 → green on v2). **Environment constraint unchanged:** no runner in this session — Increment 0 (baseline reproduction) executes first, by you or via an exposed runner; until then all outcome predictions are **Reasoned**, not Verified.

**Deliverable shape (per blueprint §14):** single-file Python 3.11+ stdlib-only utility, `deliverable/github_folder_downloader.py`. v1 stays frozen at `audit/scratch/` as the test baseline. Same harness runs against both via a path override — the before/after ledger is the core evidence artifact.

---

## 1. Acceptance Criteria

1. All 22 findings closed or explicitly deferred with justification (none planned for deferral except live-only checks).
2. Blueprint §13 DoD: all 18 items satisfied, including the two currently unmet (automated tests; hash verification).
3. Full harness green against v2: existing GUARD tests, existing RED tests, and the new-coverage tests below. Zero skipped/weakened assertions.
4. Gates clean without guardrail weakening: `py_compile`, `ruff check`, `mypy --strict`, full test suite.
5. CLI contract preserved (two positionals, all v1 flags, defaults unchanged); additions are additive only (`--ref`, exit code 3).
6. Verification ledger delivered: per-finding Verified/Reasoned status, live-smoke results or Unverifiable flags.

## 2. Design Decisions (stated assumptions — adjustable on approval)

| # | Decision | Recommendation | Rationale / tradeoff |
|---|---|---|---|
| D1 | Ref/path ambiguity (F-12) | **Hard-fail with both interpretations listed**, exit 3; add `--ref REF` to pin the ref (entire URL tail becomes the path) | Blueprint §4 forbids silent selection. Tradeoff: URLs that v1 silently guessed may now fail — correctness over convenience; `--ref` is the documented escape hatch. Cost: bounded extra commits-API calls (≤ tail length) to examine shorter candidates |
| D2 | Filename policy (F-11) | **Platform-aware**: POSIX keeps literal `\` and `:` in components (no remapping); Windows rejects Windows-illegal names with a per-file actionable error. True traversal, absolute, drive-absolute (`X:/…`), and UNC forms rejected on **all** platforms | Fidelity per blueprint ("preserve file names") without weakening traversal defense. Tradeoff: POSIX-faithful trees may be non-portable to Windows — documented, not silently "fixed" |
| D3 | Exit codes | Keep 0/1/2/130; add **3 = ambiguous ref/path** | Additive, meaningful; v1 unreleased so no consumer breakage |
| D4 | Archive entry cap (F-09) | Total entries (selected or not) ≤ `max(1000, 10 × max_files)`; named constant, clear error | Scales with user intent; keeps the 20k-entry/`--max-files 5` regression test meaningful; huge-monorepo fallbacks fail loudly with a preserved archive |
| D5 | TAR scan budget (F-08) | Stream `r\|gz` single-pass; abort when **total decompressed bytes** (skipped + extracted) exceed `max(max_extract, 100 × compressed archive size)` | Bounds bomb amplification while allowing legit ~5–20:1 source archives generous headroom; satisfies blueprint's ratio guard with one mechanism instead of a false-positive-prone per-entry heuristic. Tradeoff: pathological-but-legit >100:1 archives rejected with clear error + archive preserved |

## 3. Target Architecture (single file, typed seams)

- **Errors:** `DownloadError(status: int | None)`; `CommitError(DownloadError)` (never triggers fallback); `AmbiguousRefError(DownloadError)` (carries interpretations, maps to exit 3).
- **HTTP core (deduplicated, F-21/F-22):** one `build_opener()` with a redirect handler that (a) drops `Authorization` on host change, (b) rejects non-HTTPS redirect targets; shared header/error-translation path; `with_retries()` — bounded (3 attempts), exponential backoff + jitter, honors `Retry-After` (capped wait, actionable failure beyond cap), retries only 429/5xx/network/timeout on idempotent GETs. `request_bytes` / `stream_to_file` become thin wrappers; `stream_to_file` deletes partial output on failure.
- **Typed data:** `TreeEntry` dataclass (path, type, sha, size, mode); `api_json` returns `object`, narrowed by validation helpers at the boundary (no `Any` leakage; argparse `Namespace` accessed through one typed accessor — strict mypy without suppressions).
- **Resolution (F-02/03/04/05/12/13):** candidates longest→shortest; 404 = miss, everything else surfaces (rate-limit detected via status + `X-RateLimit-Remaining`, reset time reported). Path verification via root-tree walk down path components (O(depth) calls) to the **subtree SHA**, then one `git/trees/{subtree}?recursive=1`; truncation falls back to a **subtree-scoped** iterative walk (explicit stack — no Python recursion limit), cached per SHA, bounded by `max_files`/`max_depth` during traversal. Raw downloads pinned to `commit_sha`.
- **Primary staging:** `max_extract` enforced on aggregate bytes; per-response `max_download`; git-blob SHA-1 + size verified per file; mode-120000 blobs and `commit` entries skipped **with warnings**; zero-materialized-files → loud failure.
- **Fallback:** encoded codeload URLs; ZIP — entry cap, declared-size pre-checks plus actual-byte counting during copy, zero-guard; TAR — streaming per D5, entry cap, zero-guard; preservation **only** for fully downloaded archives that failed extraction/validation (never commit failures); informative names `{repo}-{ref}.{zip|tar.gz}` for both preserve and `--keep-archive`.
- **Commit:** backups in an isolated sibling tempdir (outside staged-content namespace); `except BaseException` rollback + re-raise; unique tmp names (`.tmp-download-{uuid}`) to avoid cross-run collisions; `CommitError` for conflicts/permissions/disk.
- **main:** staging and commit in separate try blocks — only staging failures fall back.

## 4. Finding → Fix → Evidence Traceability

| F | Severity | Remediation seam | Inc. | Regression evidence |
|---|---|---|---|---|
| 01 | High | Opener redirect handler | 1 | h01 (retargeted, §5) + same-host retention & HTTPS-downgrade tests |
| 02 | High | Raw URL uses `commit_sha` | 2 | h02 |
| 03 | High | Status-classified resolution errors | 2 | h03 + 429/5xx/timeout classification tests |
| 04 | High | Subtree-scoped recursive + scoped walk | 2 | h04 + subtree-truncation test |
| 05 | High | Path-walk + cache + subtree-only fetch | 2 | h05 (≤5 tree calls) + call-budget test |
| 06 | High | Extended harness as DoD suite | 6 | Full green ledger vs v1 red baseline |
| 07 | High | Staging/commit separation; `CommitError` | 5 | h07 ×2 + disk-full/permission no-fallback tests |
| 08 | Med | Streaming TAR + scan budget (D5) | 4 | h08 + budget-boundary tests |
| 09 | Med | Entry cap (D4), both formats | 4 | h09 + TAR entry-flood test |
| 10 | Med | Zero-file guards, both tiers | 3+4 | h22 + API-only-submodule-folder test |
| 11 | Med | Platform-aware `safe_relpath` (D2) | 3 | h10 ×2 + non-ASCII, UNC, drive-absolute tests |
| 12 | Med | Ambiguity detection + `--ref` (D1) | 2 | h11 (revised, §5) + `--ref` pin test + exit-3 test |
| 13 | Med | Boundary payload validation | 2 | h12 + malformed-variant tests |
| 14 | Med | Completion flag; partial cleanup | 4 | h13 + interrupted-stream cleanup test |
| 15 | Med | `BaseException` rollback | 5 | h14 |
| 16 | Med | `with_retries` + `Retry-After` | 1 | h15 + Retry-After/cap/backoff tests (clock patched) |
| 17 | Med | `max_extract` in staging; help text | 3 | h16 + aggregate-limit boundary test |
| 18 | Med | Blob SHA-1 + size verification | 3 | h17 + size-mismatch test |
| 19 | Low | Skip-with-warning (symlinks/submodules) | 3 | h18 ×2 |
| 20 | Low | Isolated backup dir | 5 | h19 |
| 21 | Low | Encoded archive URLs; unified scheme check | 1 | h20 ×2 |
| 22 | Low | Dead code removal, types, constants, naming | 1–6 | ruff/mypy strict + naming tests |

## 5. Harness Revisions (disclosed — strengthening only, never weakening)

1. `ghutil.py`: target path via `GH_DOWNLOADER_PATH` env override (enables v1-red/v2-green dual run); fixtures extended with Contents/root-walk and **subtree** recursive endpoints (new resolution seam needs serving; existing assertions untouched).
2. `h01` retargeted from stdlib's handler to the script's opener handler — stdlib itself never changes, so probing it would stay red forever; assertion intent (cross-host auth stripped) is preserved and strengthened with same-host retention + downgrade-rejection cases.
3. `h11` upgraded to expect `AmbiguousRefError` **and** shorter-candidate examination (v2 contract is stronger than the audit's minimal assertion).
4. Retry tests patch `time.sleep`/jitter for speed and determinism.
5. New module `test_url_parse.py` (blueprint §12A gap in the consolidated audit harness): standard/slash/encoded/tag/SHA/root URLs; blob/gist/gitlab/userinfo/query/`..`/malformed rejection.

## 6. Increments, Gates, and Commit Plan

Each increment: failing test(s) first → implement → targeted tests + `py_compile` + `ruff` + `mypy --strict` → atomic commit. Full suite at I2, I4, I6.

| Inc. | Scope | Conventional Commit (conditional: repo + SSH wrapper unavailable in this session — flagged, not assumed) |
|---|---|---|
| 0 | Extract v1, run harness, record observed red/green baseline ledger (converts audit Reasoned → Verified/refuted) | `chore(audit): record v1 baseline test ledger` |
| 1 | HTTP core: F-01/16/21 (+22 dedup/constants) | `fix(http): strip auth on cross-host redirects, add bounded retries` |
| 2 | Resolution redesign: F-02/03/04/05/12/13, `--ref`, exit 3 | `feat(resolve): subtree-scoped resolution with ambiguity reporting` |
| 3 | Primary staging: F-10a/11/17/18/19 | `fix(stage): verify blob integrity, enforce extract limits, platform-aware paths` |
| 4 | Fallback hardening: F-08/09/10b/14, informative naming | `fix(archive): bounded streaming extraction and policy-correct preservation` |
| 5 | Commit/policy: F-07/15/20 | `fix(commit): isolate commit failures from fallback, roll back on interrupt` |
| 6 | CLI/help/README, dead-code sweep, full gate, pre-mortem, delivery ledger | `feat(cli): add --ref disambiguation; docs: v2 limits and policies` |

## 7. Verification Protocol

```bash
# I0 — baseline (expected: GUARDs green, ~19 RED failing/erroring)
GH_DOWNLOADER_PATH=audit/scratch/github_folder_downloader.py \
  python3 -m unittest discover -s audit/tests -v
# Final gate — v2 (expected: all green)
GH_DOWNLOADER_PATH=deliverable/github_folder_downloader.py \
  python3 -m unittest discover -s audit/tests -v
audit/.venv/bin/ruff check deliverable/github_folder_downloader.py
audit/.venv/bin/mypy --strict deliverable/github_folder_downloader.py
python3 -m py_compile deliverable/github_folder_downloader.py
```

Live smoke (opt-in, network-gated, courteous volume): the three approved scenarios plus (a) forced-fallback via `--max-files 1`, (b) a slash-branch/ambiguity fixture repo (supply a URL or provision a throwaway), (c) authenticated redirect check using **your own** least-privilege token exported locally — never pasted here. F-01's storage-rejection impact stays **Assumed** until (c) runs.

**Pre-mortem (executed at I6, planned handling):**

| Failure mode | Handling |
|---|---|
| Malicious archive (traversal/symlink/bomb/entry flood) | D2/D4/D5 guards + existing rejection suite |
| Rate limit / transient 5xx | Classified errors, bounded retry, `Retry-After` |
| Branch advances mid-run | SHA-pinned raw + archive + blob-hash verification |
| Partial network failure | Retry; partial deletion; completed-only preservation |
| Huge repo / truncated tree | Subtree scoping, scoped walk, limits with clear errors |
| Empty/missing target, submodule-only folder | Zero-file guards, warnings |
| KI / disk-full mid-commit | `BaseException` rollback, isolated backups, unique tmp names |
| Concurrent runs to one destination | Per-file `os.replace` atomicity + unique tmp names; full locking **out of scope**, documented |

## 8. Known Limitations (will be stated in delivery, not hidden)

- Windows filename behavior: Reasoned-only unless a Windows runner is available.
- No directory-level atomic swap (blueprint acknowledges); per-file transactional semantics with rollback.
- Empty Git directories unreconstructable (inherent); destination-local symlink-swap TOCTOU out of scope.
- Live GitHub behavior Unverifiable until smoke runs; single-file constraint keeps the diff large by design.

---

**Ready check:** acceptance criteria inferable ✓; NFRs fixed (3.11+, stdlib, bounded scale) ✓; no new dependencies ✓; D1–D5 are stated assumptions within blueprint latitude, not blockers.

**One question:** approve the plan as specified — including D1 (hard-fail ambiguity + `--ref`), D2 (platform-aware filenames), and D5 (100:1 scan budget) — or adjust any decision before I begin Increment 0/1?

---

# v2 Implementation — Delivered

**Status:** implemented per plan with D1–D5 resolved as recommended. **Nothing was executed** (no runner in this session): the script and harness are desk-checked only — all behavior claims are **Reasoned**, runtime results **Unverifiable** until you run the gates below. First-run failures are expected and welcome; send output back and I'll fix root causes, not symptoms.

**Decisions applied:** D1 hard-fail ambiguity + `--ref` (exit 3) · D2 platform-aware filenames · D3 exit 3 added · D4 entry cap `max(1000, 10×max_files)` · D5 TAR scan budget `max(max_extract, 100×compressed)`.

---

## 1. `deliverable/github_folder_downloader.py`

```python
#!/usr/bin/env python3
"""Download and mirror a GitHub repository folder without cloning the repository.

Usage:
  python github_folder_downloader.py URL DESTINATION
  python github_folder_downloader.py URL DESTINATION --ref feature/x --verbose

Only ordinary files are materialized; downloaded content is never executed.
Exit codes: 0 success, 1 failure, 2 usage/destination error, 3 ambiguous ref, 130 interrupted.
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
USER_AGENT: Final = "github-folder-downloader/2.0 (Python urllib)"
API_BASE: Final = "https://api.github.com"
RAW_BASE: Final = "https://raw.githubusercontent.com"
CODELOAD_BASE: Final = "https://codeload.github.com"
MIB: Final = 1024 * 1024
DEFAULT_MAX_DOWNLOAD: Final = 100 * MIB
DEFAULT_MAX_EXTRACT: Final = 250 * MIB
DEFAULT_MAX_FILES: Final = 5000
DEFAULT_MAX_DEPTH: Final = 100
CHUNK: Final = 64 * 1024
API_JSON_LIMIT: Final = 10 * MIB
ERROR_BODY_LIMIT: Final = 1024
ERROR_DETAIL_LIMIT: Final = 300
RETRY_ATTEMPTS: Final = 3
RETRY_BASE_DELAY: Final = 0.5
RETRY_MAX_DELAY: Final = 8.0
RETRY_AFTER_CAP: Final = 60.0
RETRY_STATUS: Final = frozenset({429, 500, 502, 503, 504})
# Bound decompression work: legitimate source archives compress well under 100:1.
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
T = TypeVar("T")


class DownloadError(Exception):
    """Expected operational failure, optionally carrying an HTTP status."""

    def __init__(self, message: str, *, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status


class CommitError(DownloadError):
    """Destination-side failure. Never triggers archive fallback."""


class AmbiguousRefError(DownloadError):
    """Several ref/folder interpretations of one URL are valid."""

    def __init__(self, message: str, interpretations: Sequence[str]) -> None:
        super().__init__(message)
        self.interpretations = tuple(interpretations)


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

    Structural checks use normalized separators so traversal, absolute, drive and
    UNC forms are rejected on every platform. Materialization keeps the original
    separators: on POSIX a backslash is a legal filename character and must not
    silently become a directory boundary.
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


def _backoff(attempt: int) -> float:
    return min(RETRY_MAX_DELAY, RETRY_BASE_DELAY * (2 ** (attempt - 1))) * (0.5 + random.random() / 2)


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
) -> T:
    """Single HTTP seam: HTTPS-only, bounded retries, credential-safe redirects."""
    ensure_safe_opener()
    if not url.lower().startswith("https://"):
        raise DownloadError("HTTPS is required for network requests.")
    headers = {"User-Agent": USER_AGENT, "Accept": accept}
    if token:
        headers["Authorization"] = "Bearer " + token
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return handle(response)
        except urllib.error.HTTPError as exc:
            status, detail, resp_headers = exc.code, _error_detail(exc), exc.headers
            exc.close()
            if status in RETRY_STATUS and attempt < RETRY_ATTEMPTS:
                hinted = _retry_after_seconds(resp_headers.get("Retry-After") if resp_headers else None)
                if hinted is not None and hinted > RETRY_AFTER_CAP:
                    raise DownloadError(
                        f"HTTP {status} for {url}: server asks to retry after {hinted:.0f}s "
                        f"(cap {RETRY_AFTER_CAP:.0f}s); retry later.",
                        status=status,
                    ) from exc
                delay = hinted if hinted is not None else _backoff(attempt)
                LOG.warning("HTTP %s for %s; retry %d/%d in %.1fs",
                            status, url, attempt + 1, RETRY_ATTEMPTS, delay)
                time.sleep(delay)
                continue
            raise DownloadError(_http_message(url, status, detail, resp_headers), status=status) from exc
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            if attempt < RETRY_ATTEMPTS:
                delay = _backoff(attempt)
                LOG.warning("Network error for %s (%s); retry %d/%d in %.1fs",
                            url, exc, attempt + 1, RETRY_ATTEMPTS, delay)
                time.sleep(delay)
                continue
            raise DownloadError(f"Network error for {url}: {exc}") from exc
    raise DownloadError(f"Request failed after {RETRY_ATTEMPTS} attempts: {url}")


def request_bytes(url: str, *, timeout: float, token: str | None = None,
                  accept: str = "application/vnd.github+json",
                  limit: int | None = None) -> bytes:
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

    return _perform(url, timeout=timeout, token=token, accept=accept, handle=handle)


def stream_to_file(url: str, out: Path, *, timeout: float, token: str | None,
                   max_size: int, accept: str = "application/octet-stream") -> int:
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
        return _perform(url, timeout=timeout, token=token, accept=accept, handle=handle)
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


def api_json(url: str, *, timeout: float, token: str | None) -> object:
    payload = request_bytes(url, timeout=timeout, token=token, limit=API_JSON_LIMIT)
    try:
        result: object = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DownloadError(f"Invalid JSON response from GitHub API: {url}") from exc
    return result


def encode_path(path: str) -> str:
    return "/".join(urllib.parse.quote(part, safe="") for part in path.split("/") if part)


def parse_url(url: str) -> tuple[str, str, list[str], str]:
    """Parse a github.com owner/repo tree URL into owner, repo, tail, kind."""
    try:
        parsed = urllib.parse.urlsplit(url)
    except ValueError as exc:
        raise DownloadError(f"Invalid URL: {exc}") from exc
    if parsed.scheme != "https" or parsed.hostname != "github.com" or parsed.username or parsed.password:
        raise DownloadError("Expected an HTTPS github.com URL.")
    if parsed.query or parsed.fragment:
        raise DownloadError("Query strings and fragments are not supported in folder URLs.")
    parts = [urllib.parse.unquote(p) for p in parsed.path.strip("/").split("/") if p]
    if len(parts) < 2:
        raise DownloadError("URL must include OWNER and REPO.")
    owner, repo = parts[0], parts[1]
    if repo.endswith(".git"):
        repo = repo[:-4]
    if not owner or not repo or any("/" in x or x in (".", "..") for x in (owner, repo)):
        raise DownloadError("Invalid owner or repository name.")
    if len(parts) == 2:
        return owner, repo, [], "root"
    if parts[2] != "tree" or len(parts) < 4:
        raise DownloadError(
            "Expected a folder URL in the form https://github.com/OWNER/REPO/tree/REF/PATH.")
    return owner, repo, parts[3:], "tree"


def get_repo_default_branch(owner: str, repo: str, *, timeout: float, token: str | None) -> str:
    data = _json_object(
        api_json(f"{API_BASE}/repos/{encode_path(owner)}/{encode_path(repo)}", timeout=timeout, token=token),
        "repository")
    return _string_field(data, "default_branch", "repository")


def _commit_for_ref(owner: str, repo: str, ref: str, *, timeout: float,
                    token: str | None) -> tuple[str, str] | None:
    """Return (commit_sha, root_tree_sha); None only when the ref does not exist."""
    url = (f"{API_BASE}/repos/{encode_path(owner)}/{encode_path(repo)}"
           f"/commits/{encode_path(ref)}")
    try:
        data = _json_object(api_json(url, timeout=timeout, token=token), "commit")
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
    _trees: dict[str, list[TreeEntry]] = field(default_factory=dict)

    def listing(self, tree_sha: str) -> list[TreeEntry]:
        cached = self._trees.get(tree_sha)
        if cached is not None:
            return cached
        url = (f"{API_BASE}/repos/{encode_path(self.owner)}/{encode_path(self.repo)}"
               f"/git/trees/{encode_path(tree_sha)}")
        data = _json_object(api_json(url, timeout=self.timeout, token=self.token), "tree")
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
    data = _json_object(api_json(url, timeout=cache.timeout, token=cache.token), "recursive tree")
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
        if entry.kind == "blob":
            files += 1
    if files > max_files:
        raise DownloadError(f"Folder contains more than {max_files} files.")
    return recursive


def resolve_target(owner: str, repo: str, tail: list[str], kind: str, *, timeout: float,
                   token: str | None, ref_override: str | None = None,
                   max_depth: int = DEFAULT_MAX_DEPTH) -> RepoTarget:
    cache = TreeCache(owner, repo, timeout, token)
    if kind == "root" or ref_override:
        ref = ref_override or get_repo_default_branch(owner, repo, timeout=timeout, token=token)
        resolved = _commit_for_ref(owner, repo, ref, timeout=timeout, token=token)
        if resolved is None:
            raise DownloadError(f"Ref not found: {ref}")
        sha, tree = resolved
        path = "/".join(tail) if kind != "root" else ""
        subtree = _subtree_sha(cache, tree, path, max_depth=max_depth)
        if subtree is None:
            raise DownloadError(f"Folder not found at ref {ref}: {path or '(repository root)'}")
        return RepoTarget(owner, repo, ref, path, sha, tree, subtree)

    matches: list[RepoTarget] = []
    for split in range(len(tail), 0, -1):
        ref, path = "/".join(tail[:split]), "/".join(tail[split:])
        resolved = _commit_for_ref(owner, repo, ref, timeout=timeout, token=token)
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
        raise DownloadError(
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


def download_blob(target: RepoTarget, path: str, *, timeout: float, token: str | None,
                  max_size: int) -> bytes:
    # Pin the resolved commit: branch names are mutable and slash-refs are
    # ambiguous on the raw host.
    url = (f"{RAW_BASE}/{encode_path(target.owner)}/{encode_path(target.repo)}"
           f"/{encode_path(target.commit_sha)}/{encode_path(path)}")
    return request_bytes(url, timeout=timeout, token=token,
                         accept="application/octet-stream", limit=max_size)


def _verify_blob(entry: TreeEntry, data: bytes) -> None:
    if entry.size and len(data) != entry.size:
        raise DownloadError(
            f"Size mismatch for {entry.path}: expected {entry.size} bytes, got {len(data)}.")
    if entry.sha and git_blob_sha(data) != entry.sha:
        raise DownloadError(f"Integrity check failed for {entry.path}: Git blob SHA mismatch.")


def stage_api_folder(target: RepoTarget, stage: Path, *, timeout: float, token: str | None,
                     max_download: int, max_files: int, max_depth: int,
                     max_extract: int = DEFAULT_MAX_EXTRACT) -> tuple[int, int]:
    cache = TreeCache(target.owner, target.repo, timeout, token)
    subtree = target.subtree_sha or _subtree_sha(cache, target.tree_sha, target.path, max_depth=max_depth)
    if subtree is None:
        raise DownloadError(f"Target folder not found: {target.path or '(repository root)'}")
    entries = fetch_folder_entries(cache, subtree, max_files=max_files, max_depth=max_depth)
    files: list[TreeEntry] = []
    for entry in entries:
        if entry.kind == "commit":
            LOG.warning("Skipping submodule (not retrieved): %s", entry.path)
        elif entry.kind == "blob" and entry.mode == SYMLINK_MODE:
            LOG.warning("Skipping symlink (not materialized): %s", entry.path)
        elif entry.kind == "blob":
            files.append(entry)
    if not files:
        raise DownloadError(
            f"No regular files found in the requested folder: {target.path or '(repository root)'}")
    total = 0
    for entry in files:
        safe = safe_relpath(entry.path)
        if len(safe.parts) > max_depth:
            raise DownloadError(f"Folder depth exceeds configured limit ({max_depth}).")
        if entry.size > max_download:
            raise DownloadError(f"File exceeds per-download limit: {entry.path}")
        data = download_blob(target, entry.path, timeout=timeout, token=token, max_size=max_download)
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


def extract_zip_target(archive: Path, stage: Path, target: RepoTarget, *,
                       max_extract: int, max_files: int, max_depth: int) -> tuple[int, int]:
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
            if mode and stat.S_IFMT(mode) not in (0, stat.S_IFREG):
                raise DownloadError(f"ZIP contains a non-regular entry: {rel}")
            if info.file_size < 0 or info.file_size > max_extract:
                raise DownloadError(f"ZIP entry exceeds extraction limit: {rel}")
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


def extract_tar_target(archive: Path, stage: Path, target: RepoTarget, *,
                       max_extract: int, max_files: int, max_depth: int) -> tuple[int, int]:
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


def commit_files(stage: Path, destination: Path, *, no_overwrite: bool) -> int:
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
                rel = src.relative_to(stage)
                dst = destination / rel
                if dst.exists():
                    if dst.is_dir():
                        raise CommitError(f"Destination conflict: {dst} is a directory.")
                    if no_overwrite:
                        raise CommitError(f"File exists and --no-overwrite is set: {dst}")
                    backup = backup_root / rel
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


def preserve_archive(archive: Path, destination: Path, name: str) -> Path:
    destination.mkdir(parents=True, exist_ok=True)
    dest = destination / name
    shutil.copyfile(archive, dest)
    return dest


def download_with_archive_fallback(target: RepoTarget, destination: Path, *, timeout: float,
                                   token: str | None, max_download: int, max_extract: int,
                                   max_files: int, max_depth: int, keep_archive: bool,
                                   no_overwrite: bool) -> tuple[int, int, str]:
    errors: list[str] = []
    destination.mkdir(parents=True, exist_ok=True)
    for fmt, url in archive_urls(target):
        with tempfile.TemporaryDirectory(prefix="gh-folder-") as tmp:
            tmpdir = Path(tmp)
            archive = tmpdir / f"repository.{fmt}"
            try:
                stream_to_file(url, archive, timeout=timeout, token=token, max_size=max_download)
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
                        max_files=max_files, max_depth=max_depth)
                else:
                    count, size = extract_tar_target(
                        archive, stage, target, max_extract=max_extract,
                        max_files=max_files, max_depth=max_depth)
            except Exception as exc:
                errors.append(f"{fmt} extraction: {exc}")
                LOG.warning("%s extraction failed: %s", fmt.upper(), exc)
                try:
                    saved = preserve_archive(archive, destination, archive_filename(target, fmt))
                    LOG.warning("Preserved archive for manual recovery: %s", saved)
                except OSError as save_exc:
                    errors.append(f"preservation failed: {save_exc}")
                continue
            # Commit failures are destination-side: no preservation, no second format.
            commit_files(stage, destination, no_overwrite=no_overwrite)
            if keep_archive:
                saved = preserve_archive(archive, destination, archive_filename(target, fmt))
                LOG.info("Retained archive: %s", saved)
            return count, size, fmt
    raise DownloadError("Archive fallback failed: " + " | ".join(errors))


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download and mirror a GitHub repository folder without cloning the repository.")
    parser.add_argument("github_folder_url", help="HTTPS GitHub folder URL, or repository root URL")
    parser.add_argument("destination", help="Local destination directory")
    parser.add_argument("--ref", default=None,
                        help="Pin the branch/tag/commit ref; the whole URL tail is then the folder path")
    parser.add_argument("--timeout", type=float, default=30.0,
                        help="Network operation timeout in seconds (default: 30)")
    parser.add_argument("--max-download-size", type=int, default=100,
                        help="Per-response/archive download cap in MiB (default: 100)")
    parser.add_argument("--max-extracted-size", type=int, default=250,
                        help="Total reconstructed content cap in MiB, both tiers (default: 250)")
    parser.add_argument("--max-files", type=int, default=DEFAULT_MAX_FILES,
                        help=f"Maximum files to materialize (default: {DEFAULT_MAX_FILES})")
    parser.add_argument("--max-depth", type=int, default=DEFAULT_MAX_DEPTH,
                        help=f"Maximum path depth (default: {DEFAULT_MAX_DEPTH})")
    parser.add_argument("--keep-archive", action="store_true",
                        help="Retain the archive even after successful extraction")
    parser.add_argument("--no-overwrite", action="store_true",
                        help="Refuse to overwrite existing destination files")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--token-env", default="GITHUB_TOKEN",
                        help="Environment variable holding the GitHub token (default: GITHUB_TOKEN)")
    args = parser.parse_args(argv)
    if (args.timeout <= 0 or args.max_download_size <= 0 or args.max_extracted_size <= 0
            or args.max_files <= 0 or args.max_depth <= 0):
        parser.error("Timeout and all size/count/depth limits must be positive.")
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(levelname)s: %(message)s")
    ensure_safe_opener()
    timeout: float = float(args.timeout)
    max_download: int = int(args.max_download_size) * MIB
    max_extract: int = int(args.max_extracted_size) * MIB
    max_files: int = int(args.max_files)
    max_depth: int = int(args.max_depth)
    no_overwrite: bool = bool(args.no_overwrite)
    token_env: str = str(args.token_env)
    ref_override: str | None = str(args.ref) if args.ref else None
    destination = Path(str(args.destination)).expanduser().resolve()
    if destination.exists() and not destination.is_dir():
        LOG.error("Destination exists but is not a directory: %s", destination)
        return 2
    token = os.environ.get(token_env) or None
    try:
        owner, repo, tail, kind = parse_url(str(args.github_folder_url))
        target = resolve_target(owner, repo, tail, kind, timeout=timeout, token=token,
                                ref_override=ref_override, max_depth=max_depth)
        LOG.info("Resolved repository=%s/%s ref=%s path=%s commit=%s", target.owner, target.repo,
                 target.ref, target.path or "(repository root)", target.commit_sha[:12])
        destination.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="gh-folder-primary-") as tmp:
            stage = Path(tmp) / "stage"
            stage.mkdir()
            try:
                count, size = stage_api_folder(
                    target, stage, timeout=timeout, token=token, max_download=max_download,
                    max_files=max_files, max_depth=max_depth, max_extract=max_extract)
            except DownloadError as exc:
                LOG.warning("Primary retrieval failed: %s", exc)
            else:
                # Commit is deliberately outside the staging handler: a destination
                # conflict must not trigger a whole-repository archive download.
                commit_files(stage, destination, no_overwrite=no_overwrite)
                LOG.info("SUCCESS: downloaded %d file(s), %.2f MiB using GitHub API/raw retrieval.",
                         count, size / MIB)
                return 0
        count, size, fmt = download_with_archive_fallback(
            target, destination, timeout=timeout, token=token, max_download=max_download,
            max_extract=max_extract, max_files=max_files, max_depth=max_depth,
            keep_archive=bool(args.keep_archive), no_overwrite=no_overwrite)
        LOG.info("SUCCESS: downloaded %d file(s), %.2f MiB using %s archive fallback.",
                 count, size / MIB, fmt)
        return 0
    except AmbiguousRefError as exc:
        LOG.error("%s", exc)
        for interpretation in exc.interpretations:
            LOG.error("  possible: %s", interpretation)
        return 3
    except DownloadError as exc:
        LOG.error("%s", exc)
        return 1
    except KeyboardInterrupt:
        LOG.error("Interrupted.")
        return 130
    except OSError as exc:
        LOG.error("Filesystem error: %s", exc)
        return 1
    except Exception:
        LOG.exception("Unexpected error.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

---

## 2. Harness updates

### 2a. Replace `audit/tests/ghutil.py` header and `api_repo` tree-serving loop

Replace the import bootstrap block with:

```python
import os

_TARGET = os.environ.get("GH_DOWNLOADER_PATH")
_MODULE = (Path(_TARGET).resolve() if _TARGET
           else Path(__file__).resolve().parents[1] / "scratch" / "github_folder_downloader.py")
sys.path.insert(0, str(_MODULE.parent))
import github_folder_downloader as gfd  # noqa: E402
```

Replace the tree-serving loop in `api_repo` with (adds subtree-scoped recursive endpoints; root endpoints unchanged so v1 still runs):

```python
    for d in dirs:
        sha_d = dsha(d)
        router.add(f"{base}/git/trees/{sha_d}",
                   json.dumps({"tree": children[d], "truncated": False}).encode())
        if d:
            scoped = [{**e, "path": e["path"][len(d) + 1:]}
                      for e in recursive if e["path"].startswith(d + "/")]
        else:
            scoped = recursive
        router.add(f"{base}/git/trees/{sha_d}?recursive=1",
                   json.dumps({"tree": scoped, "truncated": truncated}).encode())
```

### 2b. `test_http_and_security.py` — replace `test_h01_*` and `test_h15_*`

```python
    def test_h01_auth_stripped_on_cross_host_redirect(self):
        """RED until F-01 fixed. Targets the script's redirect seam (stdlib never changes)."""
        handler = gfd.SafeRedirectHandler()
        req = urllib.request.Request(
            "https://codeload.github.com/o/r/zip/" + SHA,
            headers={"Authorization": "Bearer " + DUMMY_TOKEN})
        new = handler.redirect_request(
            req, None, 302, "Found", email.message.Message(),
            "https://objects.githubusercontent.com/signed?sig=x")
        self.assertIsNotNone(new)
        self.assertIsNone(new.headers.get("Authorization"))

    def test_guard_same_host_redirect_keeps_auth(self):
        handler = gfd.SafeRedirectHandler()
        req = urllib.request.Request("https://api.github.com/a",
                                     headers={"Authorization": "Bearer " + DUMMY_TOKEN})
        new = handler.redirect_request(req, None, 302, "Found", email.message.Message(),
                                       "https://api.github.com/b")
        self.assertEqual(new.headers.get("Authorization"), "Bearer " + DUMMY_TOKEN)

    def test_h15_bounded_retry_on_transient_500(self):
        url = "https://api.github.com/x"
        with mock.patch("time.sleep"), mock.patch(
                "urllib.request.urlopen",
                side_effect=[http_error(url, 500), FakeResponse(b"ok")]) as m:
            body = gfd.request_bytes(url, timeout=1)
            self.assertEqual(m.call_count, 2)
            self.assertEqual(body, b"ok")
```

### 2c. `test_resolution_and_api.py` — replace `test_h11_*`

```python
    def test_h11_ambiguity_reported(self):
        """RED until F-12 fixed: both interpretations valid -> report, never guess."""
        r = Router()
        api_repo(r, ref="feature/x", blobs={"docs/a.md": b"A"}, sha="c" * 40, tree_sha="d" * 40)
        api_repo(r, ref="feature", blobs={"x/docs/a.md": b"B"}, sha="e" * 40, tree_sha="f" * 40)
        with r.patch():
            with self.assertRaises(gfd.DownloadError) as ctx:
                gfd.resolve_target("o", "r", ["feature", "x", "docs"], "tree", **RESOLVE)
        self.assertIn("ambiguous", str(ctx.exception).lower())
        self.assertIn(f"{API}/repos/o/r/commits/feature", r.urls())
```

### 2d. `test_archive_and_commit.py` — platform-conditional guard (D2)

Replace `test_guard_safe_relpath_rejects` with:

```python
    def test_guard_safe_relpath_rejects(self):
        for bad in ("../x", "/etc/passwd", "C:/x", "..\\x", "\\\\h\\s", "a/../../b", ""):
            with self.subTest(bad=bad), self.assertRaises(gfd.DownloadError):
                gfd.safe_relpath(bad)

    def test_guard_colon_path_platform_policy(self):
        """D2: rejected on Windows, preserved on POSIX (was a blanket rejection in v1)."""
        if os.name == "nt":
            with self.assertRaises(gfd.DownloadError):
                gfd.safe_relpath("a/:x")
        else:
            self.assertEqual(gfd.safe_relpath("a/:x").parts, ("a", ":x"))
```

### 2e. New `audit/tests/test_v2_policies.py`

```python
"""New v2 contracts: --ref, exit 3, Retry-After, HTTPS downgrade, caps, zero-file."""
import email.message
import json
import tempfile
import unittest
import urllib.request
from pathlib import Path
from unittest import mock

from ghutil import API, SHA, FakeResponse, Router, api_repo, gfd, http_error, make_target, targz_bytes, zip_bytes

URL = "https://github.com/o/r/tree/main/docs"


class TestPolicies(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name)

    def test_ref_override_pins_interpretation(self):
        r = Router()
        api_repo(r, ref="feature/x", blobs={"docs/a.md": b"A"}, sha="c" * 40, tree_sha="d" * 40)
        api_repo(r, ref="feature", blobs={"x/docs/a.md": b"B"}, sha="e" * 40, tree_sha="f" * 40)
        with r.patch():
            t = gfd.resolve_target("o", "r", ["x", "docs"], "tree", timeout=1, token=None,
                                   ref_override="feature")
        self.assertEqual((t.ref, t.path), ("feature", "x/docs"))

    def test_ambiguous_url_exits_3(self):
        r = Router()
        api_repo(r, ref="feature/x", blobs={"docs/a.md": b"A"}, sha="c" * 40, tree_sha="d" * 40)
        api_repo(r, ref="feature", blobs={"x/docs/a.md": b"B"}, sha="e" * 40, tree_sha="f" * 40)
        dest = self.base / "d"
        with r.patch(), self.assertLogs(gfd.LOG, level="INFO"):
            rc = gfd.main(["https://github.com/o/r/tree/feature/x/docs", str(dest)])
        self.assertEqual(rc, 3)

    def test_retry_after_cap_refused(self):
        url = "https://api.github.com/x"
        exc = http_error(url, 429)
        exc.headers["Retry-After"] = "3600"
        with mock.patch("time.sleep"), mock.patch("urllib.request.urlopen", side_effect=exc):
            with self.assertRaises(gfd.DownloadError) as ctx:
                gfd.request_bytes(url, timeout=1)
        self.assertIn("retry after", str(ctx.exception).lower())

    def test_https_downgrade_redirect_refused(self):
        handler = gfd.SafeRedirectHandler()
        req = urllib.request.Request("https://api.github.com/a")
        with self.assertRaises(gfd.DownloadError):
            handler.redirect_request(req, None, 302, "Found", email.message.Message(),
                                     "http://api.github.com/b")

    def test_tar_entry_cap(self):
        archive = self.base / "a.tar.gz"
        archive.write_bytes(targz_bytes(
            [(f"root/other/f{i}", "file", b"x") for i in range(1200)]
            + [("root/docs/a.md", "file", b"ok")]))
        with self.assertRaises(gfd.DownloadError):
            gfd.extract_tar_target(archive, self.base, make_target(),
                                   max_extract=10**6, max_files=5, max_depth=10)

    def test_api_zero_file_folder_fails(self):
        r = Router()
        api_repo(r, blobs={"other/a.md": b"a"}, submodules=["docs/vendor"])
        with r.patch():
            t = gfd.resolve_target("o", "r", ["main", "docs"], "tree", timeout=1, token=None)
            with self.assertRaises(gfd.DownloadError):
                gfd.stage_api_folder(t, self.base, timeout=1, token=None,
                                     max_download=10**6, max_files=100, max_depth=10)

    def test_extract_limit_enforced_on_api_tier(self):
        r = Router()
        api_repo(r, blobs={"docs/a.bin": b"x" * 60_000, "docs/b.bin": b"y" * 60_000})
        with r.patch():
            t = gfd.resolve_target("o", "r", ["main", "docs"], "tree", timeout=1, token=None)
            with self.assertRaises(gfd.DownloadError) as ctx:
                gfd.stage_api_folder(t, self.base, timeout=1, token=None, max_download=10**6,
                                     max_files=100, max_depth=10, max_extract=100_000)
        self.assertIn("extracted-size", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
```

### 2f. New `audit/tests/test_url_parse.py`

```python
"""Blueprint §12A URL matrix."""
import unittest
from ghutil import gfd


class TestUrlParse(unittest.TestCase):
    def test_supported_forms(self):
        cases = [
            ("https://github.com/o/r/tree/main/docs", ("o", "r", ["main", "docs"], "tree")),
            ("https://github.com/o/r/tree/feature/x/docs", ("o", "r", ["feature", "x", "docs"], "tree")),
            ("https://github.com/o/r/tree/main/a%20b/c", ("o", "r", ["main", "a b", "c"], "tree")),
            ("https://github.com/o/r/tree/v1.2/docs", ("o", "r", ["v1.2", "docs"], "tree")),
            ("https://github.com/o/r/tree/" + "a" * 40 + "/docs", ("o", "r", ["a" * 40, "docs"], "tree")),
            ("https://github.com/o/r", ("o", "r", [], "root")),
            ("https://github.com/o/r.git/", ("o", "r", [], "root")),
            ("https://github.com/o/r/tree/main/a/b/c", ("o", "r", ["main", "a", "b", "c"], "tree")),
        ]
        for url, expected in cases:
            with self.subTest(url=url):
                self.assertEqual(gfd.parse_url(url), expected)

    def test_rejected_forms(self):
        for url in ("http://github.com/o/r/tree/main/d", "https://gitlab.com/o/r/tree/main/d",
                    "https://github.com/o/r/blob/main/d.md", "https://gist.github.com/o/abc",
                    "https://u:p@github.com/o/r/tree/main/d", "https://github.com/o/r/tree/main/d?q=1",
                    "https://github.com/o/r/tree/main/d#frag", "https://github.com/o",
                    "https://github.com/o/r/tree/main", "https://github.com/../r/tree/main/d",
                    "not a url"):
            with self.subTest(url=url), self.assertRaises(gfd.DownloadError):
                gfd.parse_url(url)


if __name__ == "__main__":
    unittest.main()
```

---

## 3. Verification commands

```bash
# Baseline (v1) — expect GUARDs green, defect tests red
GH_DOWNLOADER_PATH=audit/scratch/github_folder_downloader.py \
  python3 -m unittest discover -s audit/tests -v 2>&1 | tee audit/report/baseline.txt

# v2 — expect all green
GH_DOWNLOADER_PATH=deliverable/github_folder_downloader.py \
  python3 -m unittest discover -s audit/tests -v 2>&1 | tee audit/report/v2.txt

python3 -m py_compile deliverable/github_folder_downloader.py
audit/.venv/bin/ruff check deliverable/github_folder_downloader.py
audit/.venv/bin/mypy --strict deliverable/github_folder_downloader.py
```

## 4. Verification ledger

| Item | Method | Status |
|---|---|---|
| All 22 findings addressed in code | Desk-check against finding list | **Reasoned** |
| v2 compiles / tests pass / lint / types | Not executed here | **Unverifiable** — commands above |
| Harness↔v2 endpoint compatibility | Traced call-by-call (h05 = 1 tree call, h04 scoped walk, h02 SHA-pinned raw) | **Reasoned** |
| Live GitHub behavior (F-01 storage rejection, slash-branch) | Not performed | **Unverifiable** |
| Windows filename policy (D2) | Code path only | **Reasoned**, needs Windows runner |

**Known first-run risks (flagged, not hidden):** `SafeRedirectHandler.redirect_request` annotation must match your typeshed's base signature — if mypy reports an override mismatch, send it and I'll align the signature (no suppression). Harness `FakeResponse` duck-types `HTTPResponse`; runtime fine, not type-gated.

## 5. Handoff

- **Delivered:** v2 script (all 22 fixes), harness deltas (2 new modules, 4 revised tests, fixture/env updates), gate commands.
- **Disclosed harness changes:** h01 retargeted to the script's seam; h11 now demands an ambiguity error; `a/:x` guard made platform-conditional per approved D2; retry tests patch `time.sleep`. No assertion was deleted or weakened.
- **Deferred:** live smoke protocol; Windows verification; ruff/mypy triage; directory-level locking (out of scope, documented).
- **Commit grouping** (no repo/SSH wrapper here): `fix(http)`, `feat(resolve)`, `fix(stage)`, `fix(archive)`, `fix(commit)`, `feat(cli)+docs`, `test(audit)` — one per increment, in that order.
- **Next:** run §3 and paste `v2.txt` plus lint/type output. I'll reconcile predicted vs observed, then fix root causes with the failing test as the regression anchor.
