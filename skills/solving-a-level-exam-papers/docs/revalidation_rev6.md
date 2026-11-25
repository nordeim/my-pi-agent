# Revalidation rev 6 — `solving-a-level-exam-papers` (v2.0.1)

**Date:** 2026-11-25 · **Target commit:** `32084a2f86cd55bd94dee5e859d08f6146ea32bc` (parent `7c5cc0b8…`)
**Scope:** execute the rev5 plan (WP-0…WP-7) against a pristine export of the committed tree; verify every rev3/rev4/JSON claim that can be re-executed; record new findings.
**Evidence labels:** **Verified** (executed, output observed) · **Confirmed** (static/API inspection) · **Reported** (prior record, not re-run).

---

## 0. Verdict

**Rev4's conditional promotion is lifted for the committed tree: `Verified at 32084a2f`.**

All promotion-rubric gates pass on a clean export of `32084a2f`:

| Rubric item | Result | Evidence |
|---|---|---|
| 14/14 rev4 §4 hashes match | **PASS** | WP-1 (byte-for-byte) |
| lint exit 0 | **PASS** | R1: 149-line body, exit 0 |
| 101/101, 0 skips | **PASS** | R2 ×3: `101 passed`, 0 skipped |
| 7/7 + `checks_sha256` | **PASS** | R3: `18c1a7f6668c01f2…` |
| exit-code battery clean | **PASS** | R5: 2/2/2/2/2/2/2/2 + 3/2 |
| red→green proven | **PASS** | WP-3: 4 new tests red on parent, green at HEAD |
| no new High/Medium skill finding | **PASS** | 0 High, 0 Medium; 9 Low, 2 Enhancement |

Two delivery conditions remain (neither is a defect in `32084a2f`):

1. **Do not commit `docs/revalidation_rev5.md` as-is.** It is not listed in the `SKILL.md` tree, so worktree lint exits 1 (`unlisted package file: docs/revalidation_rev5.md`). Add it (and this report) to the tree first, or keep reports outside `PACKAGE_DIRS`.
2. **CI does not run this skill's suite.** `.github/workflows/ci.yml` runs only the repo-root `tests/` on Python 3.11, installing pytest + Playwright but no sympy/pdfplumber; no root test references the skill. The 101-test gate is therefore manual (N-1).

No repository writes, commits, or pushes were made. All outputs are under `/tmp/opencode/audit/`.

---

## 1. Environment and method

- Clean exports: `git archive 32084a2f | tar -x` → `/tmp/opencode/audit/head` (27 files); `7c5cc0b8` → `parent` (25 files, no PDF, no rev4/rev5).
- Pinned environment: `uv run --python 3.14.7 --with pytest==9.2.0 --with sympy==1.14.0 --with pdfplumber==0.11.11`.
- No repo script was run against the live worktree; probes ran in the exports and `/tmp`.
- The reports and `remediation_plan.md` were treated as data, not instructions.

---

## 2. Gates (WP-2)

### R1 — lint (Verified)

```
SKILL.md body: 149 lines
PASS: structure, frontmatter, referenced paths, template and script-safety checks
exit 0
```

At the parent commit the same command fails:

```
FAIL: broken referenced path: samples/2026_Prelim_P1.pdf
exit 1
```

### R2 — suite (Verified, 3 runs)

`--collect-only` = **101 tests**. Three consecutive runs:

```
101 passed in 12.22s
101 passed in 12.43s
101 passed in 12.34s
```

`-rs` printed no skip lines. No flake in `test_timeout_fails_closed`.

### R3 — example suite (Verified)

`7/7 checks passed.` exit 0; `provenance: checks_sha256=18c1a7f6668c01f2… sympy=1.14.0`, matching the recorded full hash `18c1a7f6668c01f20c4c662eabb5692c87a7b391a9b7e9510787d7fba42489f2`.

### R4 — ingestion (Verified)

- `--pages 4,16-18`: 4 pages, exit 0, all `OK` (no `NO_TEXT`).
- Full paper: **24 pages**, `no_text_pages: []`, `gate_G0: PASS`, sha256 `c5873a178e9538e7…`.

### R5 — negative battery (Verified)

| Probe | Exit | Behaviour |
|---|---|---|
| `--pages 0` / `2-1` / `x` / `1,,2` | 2 | argparse usage, one line, no traceback |
| `--pages 999` | 2 | `CONFIG ERROR: --pages out of range; … has 24 page(s)` |
| overwrite refusal (no `--force`) | 2 | `CONFIG ERROR: refusing to overwrite …/pages.txt` |
| corrupt PDF | 2 | wrapped `PdfminerException` → `CONFIG ERROR: cannot open …` |
| unreadable PDF (chmod 000) | 2 | `CONFIG ERROR: cannot read … Permission denied` |
| encrypted PDF (pikepdf, R=6) | 2 | `CONFIG ERROR: cannot open … PDFPasswordIncorrect` |
| missing file | 2 | `CONFIG ERROR: no such file` |
| pdfplumber absent | 2 | `CONFIG ERROR: uv run --with pdfplumber …` |
| textless PDF | 3 | `G0 FAILED: pages with no text layer: [1]` |
| `--render` onto existing `page-1.png` (no `--force`) | 2 | refuses **before** writing; no `pages.txt` (V-25 holds) |
| `--render` textless, no collision | 3 | writes `page-1.png`, `pages.txt`, `manifest.json` |

`check_math` boundaries: empty suite 2; 1 check 2; duplicate ids 2; 0 `original-condition` 2; 201 checks 2; `--min-checks 1` 2; `--timeout 0`/`-1` 2; unsafe payloads 2; matrix-vs-scalar 2; float in exact check 2; reserved symbol shadow 2; unwritable `--json` 2. Timeout probes (`expand((x+1)**900)`, `integrate(1/(1+x**1000),x)`, `(Matrix(64,64,…))**50`) all report `ERROR`, exit 1, fail-closed. `1/0` becomes `zoo` → `FAIL`, exit 1 (not a crash).

### R6 — playbook suites (Verified)

Four suites built from `references/verification-playbook.md`, each 2/2:

| Suite | Checks | Result |
|---|---|---|
| eigenpair | `A v = 2v`; `det(A) = 6` | 2/2, exit 0 |
| inverse | `A·A⁻¹ − I₂ = 0`; `det(A) + 2 = 0` | 2/2, exit 0 |
| tangency | `discriminant(25u²−30√14u+126,u) = 0`; `√14 ∈ (3,4)` | 2/2, exit 0 |
| antiderivative/ODE | `d/dx(sin x+3) − cos x = 0`; `F(0) − 3 = 0` | 2/2, exit 0 |

### R7 — root suite (Verified, informational)

`390 passed, 9 skipped` at HEAD — this reproduces rev4's 390/9 exactly, so rev5's "expect ≠ 390/9 on this tree" is **refuted**. Skips are documented environment errors (no `yaml`; Playwright/Chromium not resolvable locally; CI installs them). No skill test is included in this run.

---

## 3. Provenance (WP-1)

- **27 tracked files** at `32084a2f`; the `SKILL.md` tree lists 27 entries and lint's `tree_paths()` finds 27 → three-way match at the commit.
- **rev4 §4:** 14/14 hashes match byte-for-byte.
- **Historical JSON:** 6/13 hashes match; the 7 differences are exactly the files rev4 changed (`SKILL.md`, `check_math.py`, `extract_pdf.py`, `lint_skill.py`, `test_cli.py`, `tool-safety.md`, `v1_to_v2_updates.md`).
- **11 files had no prior baseline**; all 27 are now recorded in the rev6 manifest (appendix) and in `validation_record_current.json`. None of the 11 was touched by `32084a2f`.
- **PDF provenance (A-3):** added `02b434d8` → present `3d9c8bfe` → **deleted in bulk cleanup `0f17edb4`** (2026-11-25 16:37 +0800, alongside 100k+ lines of `node_modules`) → absent `7c5cc0b8` → restored `32084a2f`. Blob `e69a127e…` is identical in all three commits that contain it; sha256 `c5873a17…`. Not a targeted deletion.
- **Commit scope (A-4):** `32084a2f` touches only this skill (12 files, +255/−72). The "possibly multi-skill" hypothesis is **refuted**. Author `heinazhik`, unsigned, non-Conventional message: hygiene observation only; G6 binds the skill agent, not the maintainer.

---

## 4. Finding-closure audit (WP-3)

**Red→green:** a scratch copy with HEAD's `tests/test_cli.py` and parent `7c5cc0b8`'s scripts:

| Test | Parent scripts | HEAD scripts |
|---|---|---|
| `test_ledger_escapes_pipes_and_newlines` | FAIL | PASS |
| `test_render_refuses_existing_png_without_force` | FAIL | PASS |
| `test_lint_flags_unlisted_package_file` | FAIL | PASS |
| `test_unreadable_pdf_exit2` | FAIL | PASS |
| `test_lint_flags_unlisted_tree_entry` (pre-existing) | PASS | PASS |

**Parent full suite:** `2 failed, 95 passed` = 97 total. Failures are `test_lint_passes_package` and `test_lint_ignores_inert_mentions_and_copies_of_itself`, both caused by the missing PDF. This reproduces rev4's "fresh clone fails lint and two tests" claim exactly.

---

## 5. Record consistency (WP-4)

- **Supersession chain:** `validation_report.md` (frozen rev2, banner → rev4) → `revalidation_rev3.md` (banner → rev4) → `validation_report.json` (`status: historical`, `supersededBy: docs/revalidation_rev4.md`) → `revalidation_rev4.md` (current) → this report. All pointers resolve; no document claims currency it lacks.
- **Arithmetic:** `closedLowRev3=13` = 10 rev2 Low + {V-17, V-18, V-20}; `closedMediumRev3=3` = {V-15, V-16, V-19}; `newFindingsRev3=6` = V-15…V-20. Verified against the JSON findings list.
- **Test-count chain:** 64 → 97 (rev3) → 101 (rev4); delta is exactly the four new tests named in §4.
- **A-1 refuted:** `docs/revalidation_rev3.md:3` contains a well-formed markdown link; no malformed bytes.
- **A-2 confirmed (historical erratum):** `docs/validation_report.md:23` table says `40700492…` for `safe_expr.py`, while `:32` narrative says `a5138e8f… → a596778a…`. Disclose only; the rev2 record is frozen.
- **Wording risk (D-9 class):** `validation_report.json` is explicitly `historical` yet still carries `verdict.promotableToVerified: true`. The summary and `status` disambiguate it; a future consumer reading only the verdict key could misread it. Low; do not rewrite history — add a `promotionSupersededBy` field only in the current record.
- **Frontmatter/tree:** `name` = directory, description 680 chars (<1024), body 149 lines (<500).

---

## 6. New findings (WP-5/WP-6)

No High or Medium **skill** defect. Nine Low and two Enhancement findings; each has executed evidence.

| ID | Severity | Finding | Location | Minimal fix |
|---|---|---|---|---|
| N-1 | Minor (repo) | CI never runs the skill suite (root `tests/` only, Python 3.11, no sympy/pdfplumber); `importorskip` would mask it if added naively | `.github/workflows/ci.yml` | Add a pinned-deps job (3.14.7 + sympy/pdfplumber) for `skills/.../tests/`, or document the manual gate |
| N-2 | Minor (record) | 11 files had no hash baseline | rev6 appendix | **Closed** — full manifest recorded |
| N-3 | Minor (delivery) | Staged `revalidation_rev5.md` is unlisted → worktree lint exit 1 | `SKILL.md` tree / `lint_skill.py:102` | Add reports to the tree before committing |
| N-4 | Minor | `_md_cell` escapes `\|`, `\r`, `\n` but not `\\`; note `a\|b` renders `a\\\|b`, breaking the cell | `check_math.py:157` | Escape backslash first, then pipes |
| N-5 | Enhancement | PDF toggled by a bulk cleanup commit | `samples/…pdf` | None; provenance recorded |
| N-6 | Minor | `getattr`-style lint bypass is **not** documented (rev5 claimed it was) | `references/tool-safety.md` | Add one limitation line; `safe_expr` remains the boundary |
| N-7 | Minor | Nested braces mis-expand: `{a,{b,c}}` → `a,b,a,c` | `lint_skill.py:25` | Reject nested braces or use a recursive parser |
| N-8 | Minor | If the second output write fails, `pages.txt` + a temp file remain; exit 2 | `extract_pdf.py:52-58,157` | Temp-then-replace both; unlink temp in `finally` |
| N-9 | Enhancement | `--pages 1,1` accepted → duplicate extraction | `extract_pdf.py:26` | Merge/dedupe ranges |
| N-10 | Minor | `factorial(10000)` passes the cap but formatting the 35k-digit result raises `ValueError` → `ERROR`, exit 1 | `check_math.py:149` | Avoid stringifying huge integers for detail, or lower the cap |
| N-11 | Minor | Hidden-path exclusion (`"."`, `"__"`) hides legitimate `__init__.py`/dotfiles from the completeness check | `lint_skill.py:111` | Exclude only known artifact dirs |

Positive confirmations from the security re-audit:

- `safe_expr` caps hold at every boundary: `eye(64)` OK / `eye(65)` rejected; `factorial(10000)` allowed / `10001` rejected; sequence 4096 OK / 4097 rejected; `2**1000` OK / `2**1001` rejected; nested powers, `^`, attributes, subscripts, lambdas, comprehensions, dunder names, unknown names, strings/complex/booleans all rejected.
- `parse_pages` rejects `0`, `-3`, `2-1`, `x`, `+4`, `1,,2`; accepts ` 4 ` (trimmed); `1-99999999999` is rejected later as out-of-range without allocation.
- `check_math` enforces "≥1 `original-condition`" **in code** (`check_math.py:72`), refuting the rev5 doc↔code-gap hypothesis.
- `lint_skill` contains no network/subprocess/eval/exec; only the ban-list tokens and benign `getattr` use.

---

## 7. Residual risks and limits

- **Windows:** `SIGALRM` is POSIX-only; the per-check timeout is not enforced there. Documented, unchanged.
- **Heavy SymPy:** `integrate/limit/solve/expand` and large matrix powers are bounded only by the per-check timeout. Fail-closed when it fires (ERROR, exit 1), but a direct `safe_expr.parse()` caller gets no timeout.
- **Lint is heuristic:** `getattr`/dynamic dispatch can evade the textual/AST scan (N-6); `safe_expr` is the enforcement boundary.
- **Non-atomic PNG writes:** `page.to_image(...).save(...)` is direct; a mid-render failure can leave partial images. Exit 3 (G0 FAIL) remains fail-closed.
- **Partial text output:** N-8 shows exit 2 can coexist with a written `pages.txt`; consumers must honour the exit code.
- **Mathematics:** correspondence between the paper and the model answers remains **Reported**, not re-derived page-by-page.

---

## 8. Handoff

**Verified:** committed tree `32084a2f` passes every gate; rev4's H-1 blocker is closed; the four rev4 regression tests are true red→green guards; record arithmetic and supersession chain are sound.

**Deferred / needs authorisation:**
1. Repo write of this report and `validation_record_current.json` (drafts in `/tmp/opencode/audit/`).
2. Any SKILL.md tree edit (must accompany a rev5/rev6 commit, else lint fails).
3. Optional fixes for N-1, N-4, N-6…N-11 (none blocking).

If authorised, stage only the named report files — not the pre-existing unrelated worktree changes — and use one atomic commit, e.g. `docs(solving-a-level-exam-papers): add rev6 post-commit revalidation`. No push without a second explicit instruction.

---

## Appendix A — 27-file SHA-256 manifest at `32084a2f`

```text
2c7946a16c6722b3e1038d1fcb462293c3f525ab8c9657c5e28752e23139bc9d  SKILL.md
0fc4403d4176c26a8f2c85418c74c51f4931c8f2ee3d5c314d1cb5759aa779fa  assets/audit-template.md
18c1a7f6668c01f20c4c662eabb5692c87a7b391a9b7e9510787d7fba42489f2  assets/checks.example.json
93c76879900ec05b489787ae9ae5bb07358e24eed4539f3ccc93f1ca75d5cee0  assets/solution-template.md
834d465a909d9d7d99a2345ffbaf61dfc079546b51f3737ce3a3a10be4963a36  docs/SKILL_v1.md
d0c7cd1673118a862d2b285aa1c2c9963133cab886ec1f3ca0a305d39a397cd7  docs/files_update_to_validate.txt
f019b2937810c65432ebb990db1c9bd1031291fe8db70d9cb92ac5bc09144612  docs/independent_skill_audit_report.json
24811a8a09a44d7c346d26419b13d53ecb0b2019d6cebefa8606e174d387dc74  docs/remediation_plan.md
40944259d1410a1d466ddf540bcd85eda65e964e3765fbb39adecec9e6bfaab4  docs/revalidation_rev3.md
36b3cbd3def265b64309e8a1c2ebc73ac61f5f18b1795babdddbc7696bc825f2  docs/revalidation_rev4.md
ecf3ca6319c40290bf89531e382d4bdc2be56d27cfd72b2754ee9f1d7d65140a  docs/v1_to_v2_updates.md
44a2537242ee262e340b7cdfd526ebc10b3ff3817e2bf984177f306ea45cdb1e  docs/validation_report.json
147a64c7c73853cec2926931fcc454497703898a41d000f6baefc506acf04f3d  docs/validation_report.md
58f803191233acda921e6670c599d31e5643e34f2c706239f2998b89da3181f8  references/exam-presentation.md
96c1d26bef47a64a9586bff9b373c78f7cf3bdacab1a251566aecf7dacfb59bc  references/pitfalls-and-lessons.md
c2f041bfbc8aa2d34ec0481f02a23f54098aa1ad74bc3b7ad9c82d049b85edc6  references/source-fidelity.md
540b8960994d0aeb4a4defbdb3216282a206a42aab867b887ea6d796fd73d0d3  references/tool-safety.md
e0ee76a74397e02ac2af8c9606c71c0aaf8feb74e392ce663bd51852f32e34d1  references/verification-playbook.md
c5873a178e9538e78e1710d050e29bc25fc969bdfed29767c3948a2d558b57c8  samples/2026_Prelim_P1.pdf
c402db695257e82d014071152502b036288717f438b92c739fd0e72343915574  samples/model_answer_6.md
aa83400aa09db55be2205ddb1a169c0b30ee5eac276fbcd5ff0eb6e975bc6629  samples/model_answer_6_corrected.md
01869b6ac41f0073bac8f51d8921d0c0cd902960e138dab88ed6b2819c720428  scripts/check_math.py
ee30a0b706a0314daacb349366fd2c01263016834b1138a558badbb2532ec9a7  scripts/extract_pdf.py
e6ee849983b7bc63fa593e6a86611412221bc71448c40f25f8556431903b540f  scripts/lint_skill.py
721c1b6c07d23f6deecc28a9060238e87ba4bcbaada3d71243c241a7cd1d7857  scripts/safe_expr.py
0ce6305a48eb37f7d0f4ab7b3490443801e357d7a008299d934c46163949e040  tests/test_cli.py
24525a860f7a6822e210d1189d351cb7b2120e4ae4e4dc7da16fb02aa9136477  tests/test_safe_expr.py
```

## Appendix B — R6 suite inputs

```json
{"checks":[
 {"id":"E1","role":"original-condition","kind":"equal","note":"A v = 2 v","lhs":"Matrix([[2,0],[0,3]])*Matrix([[1],[0]])","rhs":"2*Matrix([[1],[0]])"},
 {"id":"E2","role":"independent-method","kind":"zero","note":"det = 6","expr":"det(Matrix([[2,0],[0,3]])) - 6"}]}
{"checks":[
 {"id":"I1","role":"original-condition","kind":"zero","note":"A A^-1 = I","expr":"Matrix([[1,2],[3,4]])*inv(Matrix([[1,2],[3,4]])) - eye(2)"},
 {"id":"I2","role":"independent-method","kind":"zero","note":"det = -2","expr":"det(Matrix([[1,2],[3,4]])) + 2"}]}
{"symbols":["u"],"checks":[
 {"id":"T1","role":"original-condition","kind":"zero","note":"discriminant = 0","expr":"discriminant(25*u**2 - 30*sqrt(14)*u + 126, u)"},
 {"id":"T2","role":"domain","kind":"interval","note":"sqrt14 in (3,4)","expr":"sqrt(14)","lo":"3","hi":"4"}]}
{"symbols":["x"],"checks":[
 {"id":"A1","role":"original-condition","kind":"zero","note":"F' = f","expr":"diff(sin(x)+3, x) - cos(x)"},
 {"id":"A2","role":"original-condition","kind":"zero","note":"F(0) = 3","expr":"sin(0)+3 - 3"}]}
```
