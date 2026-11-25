# Validation report — `solving-a-level-exam-papers`

> **Superseded by revision 3 (2026-11-24):** every finding left open below (V-5…V-14, S-1) is now closed, six further findings (V-15…V-20) were found and closed, and the suite is 97 passed. See [`revalidation_rev3.md`](revalidation_rev3.md). The text below is the revision-2 record and is kept unchanged.

**Date:** 2026-11-24 · **Branch:** `main` · **Initial-pass HEAD:** `ced14ee24305abb837773b1c93e1e73352491a43` · **Revision 2 HEAD:** `1d94f148959498e0ba29d7ee9dac5ccd54168162` (fixes uncommitted)
**Initial pass:** skill subtree clean; probes under `/tmp`; only these two authorised report files were added.
**Revision 2:** fixes applied to five skill files (`scripts/lint_skill.py`, `scripts/safe_expr.py`, `tests/test_cli.py`, `tests/test_safe_expr.py`, `references/tool-safety.md`) and these two reports. No commit or push.
**Verdict:** **PASS — promotable to `Verified` on the High/Medium gate.** All hard gates are green: lint exits 0, pytest is 60/60, the example suite is 7/7, and no High/Medium finding remains open. Ten Low findings remain open and tracked; they do not block promotion.

Evidence labels: **Verified (executed)** · **Confirmed (static)** · **Reported-Verified (external)** · **Refuted**.

---

## 1. Provenance

| Artefact | SHA-256 |
|---|---|
| `SKILL.md` | `ce2cde66bbc65809a296caa2aceb4620bbada403914de0b8f0d6478dbd493327` |
| `assets/checks.example.json` | `18c1a7f6668c01f20c4c662eabb5692c87a7b391a9b7e9510787d7fba42489f2` |
| `scripts/check_math.py` | `5ee3d3f1272795c80b8bf202ded7bd9374745cae9e3eb823dc7b349c4ae3627f` |
| `scripts/extract_pdf.py` | `031d55b3c08a83df67b1f33152f52c433be024e8b28305c180a7309635766356` |
| `scripts/lint_skill.py` | `2133148d274123ee143b864854f3c4c7f3405008cb306e78ddae8cf71ca53fb9` |
| `scripts/safe_expr.py` | `4070049245c4286365f41ac7b56d3211da12285d7e030ab9cefbc97d5b06d13d` |
| `tests/test_cli.py` | `33d565edc57c05869b5e2aae921a05b861f8ce016193f55ee8560d1cd9902490` |
| `tests/test_safe_expr.py` | `e1b33d4b45b561e520773443145c57e0c6eaf2a8e896d076a5cc093f6c88bb40` |
| `samples/2026_Prelim_P1.pdf` | `c5873a178e9538e78e1710d050e29bc25fc969bdfed29767c3948a2d558b57c8` |
| `docs/SKILL_v1.md` | `834d465a909d9d7d99a2345ffbaf61dfc079546b51f3737ce3a3a10be4963a36` |
| `docs/v1_to_v2_updates.md` | `624e13fb4462c926d932f999433e9d39d6d17e9ffdcf74b48c2828cb8bc2081d` |
| `docs/independent_skill_audit_report.json` | `f019b2937810c65432ebb990db1c9bd1031291fe8db70d9cb92ac5bc09144612` |
| `references/tool-safety.md` | `93391f610e994458edb3edfcdf0c8a35d03c9e3a9670694a11537594f65472a2` |

Hashes above are the revision-2 working tree. Changed since the initial pass: `lint_skill.py` (`de58e349…` → `2133148d…`), `safe_expr.py` (`a5138e8f…` → `a596778a…`), `test_cli.py` (`6c9c7dea…` → `33d565ed…`), `test_safe_expr.py` (`54357005…` → `92c468cf…`); `references/tool-safety.md` is new to this table. The initial-pass hashes remain in git history at `ced14ee2`/`1d94f148`.

Environment: Python 3.14.7 · pytest 9.2.0 · sympy 1.14.0 · pdfplumber 0.11.11 (installed on demand via `uv run --with …`; not in the default interpreter).

Two questions are kept separate throughout:
1. **Conformance** — does the shipped package implement what its own docs claim?
2. **Truth** — are those claims correct when executed?

---

## 2. Executed evidence — initial pass (pre-fix)

Kept as audit history: E1 and E2 are the failures that motivated revision 2. Current results are R1–R10 below.

| # | Command | Result |
|---|---|---|
| E1 | `python3 scripts/lint_skill.py .` | **exit 1**; `SKILL.md body: 139 lines`; 7 unsafe-pattern hits, all inside `scripts/lint_skill.py` |
| E2 | `uv run --with pytest --with sympy --with pdfplumber pytest -q tests/` | **1 failed, 29 passed in 7.62s** — `test_lint_passes_package` |
| E3 | `uv run --with sympy python scripts/check_math.py assets/checks.example.json` | **7/7 PASS, exit 0**; `checks_sha256=18c1a7f6… sympy=1.14.0` |
| E4 | `extract_pdf.py samples/2026_Prelim_P1.pdf --out /tmp/…` (run 1) | **exit 0**; 24 pages; manifest written |
| E5 | same command, same `--out` (run 2) | **exit 2**; refuses to overwrite (fail-closed) |
| E6 | same command with `--force` (run 3) | **exit 0** |
| E7 | `extract_pdf.py … --pages abc` | **exit 1** + traceback (`ValueError`, `extract_pdf.py:80`) |
| E8 | `extract_pdf.py … --pages 999` | **exit 3**, `G0 FAILED … pages with no text layer: ALL`, `pages=0` |
| E9 | `safe_expr` probes: `x.__class__`, `x[0]`, `__import__('os')`, `lambda` | all **rejected** (`UnsafeExpression`) |
| E10 | `safe_expr` probes: `eye(1000)`, `zeros(2000,2000)`, `factorial(200000)` | all **accepted** (0.001 s / 0.000 s / 0.463 s) — no size cap |
| E11 | `safe_expr` probe: `2**100000` | **rejected**, but message is `non-finite exponent` (should be “exponent too large”) |
| E12 | `check_math.run_check(..., timeout=0.001)` | **ERROR** — `per-check time limit exceeded` (SIGALRM works) |
| E13 | interval check with `expr: I` / `sqrt(-1)`; zero check with `expr: [1,2]` | each **ERROR**, suite **exit 1** (fail-closed, but a config-class error reports as maths ERROR) |
| E14 | malformed JSON | **exit 2**, `CONFIG ERROR: Expecting property name…` |

### 2a. Re-validation (revision 2, post-fix)

| # | Command / probe | Result |
|---|---|---|
| R1 | `python3 scripts/lint_skill.py .` | **exit 0**; `PASS: structure, frontmatter, links, template and script-safety checks`; body 139 lines |
| R2 | `uv run --with pytest --with sympy --with pdfplumber pytest -q tests/` | **60 passed in 6.72s** (42 safe-expression, 18 CLI; includes all six V-3 tests) |
| R3 | `uv run --with sympy python scripts/check_math.py assets/checks.example.json` | **7/7 PASS, exit 0**; `checks_sha256=18c1a7f6… sympy=1.14.0` |
| R4 | `extract_pdf.py samples/2026_Prelim_P1.pdf --out /tmp/opencode/rv1` | **exit 0**; 24 pages; `manifest.json` written |
| R5 | same command, same `--out` | **exit 2**; `CONFIG ERROR: refusing to overwrite …` |
| R6 | same command with `--force` | **exit 0** |
| R7 | allocation rejection probes: `eye(65)`, `zeros(65,65)`, `ones(65,1)`, `Matrix(65,1,[0])`, `factorial(10001)`, `binomial(10001,2)`, `gamma(10001)`, `diag(eye(64),eye(64))`, `[0]*4097`, `Matrix([0]*65)`, `Matrix([[0]*65]*65)`, `Matrix(64,64,[0]*4097)` | **12/12 rejected** with `UnsafeExpression` and a specific message |
| R8 | allocation acceptance probes: `eye(64)`, `zeros(64,64)`, `ones(64,1)`, `Matrix([[1,2],[3,4]])`, `factorial(1000)`, `binomial(1000,2)`, `gamma(100)`, `diag(1,2,3)`, `[0]*4096`, `Matrix([0]*64)`, `Matrix([[0]*64]*64)`, `Matrix(64,64,[0]*4096)` | **12/12 accepted** |
| R9 | `test_timeout_fails_closed` via R2 | **pass**; `expand((x+1)**900)` at `--timeout 0.01` returns `ERROR` + `time limit` |
| R10 | `test_lint_requires_authorisation_gate` and `test_lint_still_flags_other_scripts` via R2 | **pass**; lint still flags a copied `extract_pdf.py` |
| R11 | `extract_pdf.py … --pages abc` | **exit 1** + traceback — unchanged Low V-8 |

---

## 3. External audit closure (7 findings)

| ID | Sev | Status | Evidence |
|---|---|---|---|
| `SEC-01` arbitrary code via `sympify` | High | **Closed** | `sympify`/`parse_expr` gone; `safe_expr.py` AST whitelist (E9). Unsafe payloads → `ConfigError` → exit 2, no side effect. |
| `GATE-01` empty suite passes | Medium | **Closed** | `MIN_CHECKS_FLOOR=2`, `MAX_CHECKS=200` (`check_math.py:18`); missing/empty/duplicate/malformed → exit 2 (tests + E14). |
| `SAFE-01` unrequested git commit | Medium | **Closed** | `SKILL.md:82–86`: explicit authorisation required; `git status --porcelain` first; stage only the named deliverable; never `git add -A`, never push/amend. |
| `PDF-01` textless PDF fails open | Medium | **Closed** | `NO_TEXT_MIN_CHARS=20`; per-page `NO_TEXT`; `G0 FAILED` + **exit 3** (E8); `test_textless_pdf_exit3` passes. |
| `DATA-01` default overwrite | Medium | **Closed** | `atomic_write` refuses existing target unless `--force` (E5/E6). |
| `PDF-02` noisy flags / truncated stdout | Low | **Partially closed** | Truncation notice + full-report path added; candidate tier retained. False-positive volume unchanged (`343` reported externally; not re-counted). Disclosed in v2 §4.8. |
| `SAMPLE-01` exemplar missing gates | Low | **Closed, residual** | Cover rules verbatim (`model_answer_6_corrected.md:4–7`), fidelity table, and `Handoff — Verified/Deferred` (lines 258–263) present. Residual: Handoff says “Verified: 7/7 exact checks” while §5 says “no CAS … executed” (lines 205, 259); ledger omits the `checks_sha256`/tool-version line mandated by `assets/solution-template.md`. |

---

## 4. Self-finding ledger

| ID | Sev | Status | Finding | Evidence | Minimal fix |
|---|---|---|---|---|---|
| `V-1` | **High** | **Closed** | Linter fails on its own package | **Fixed**: the scan skips `SELF` while still scanning every other script; R1 exit 0, R10 proves a copied `extract_pdf.py` is still flagged. | Applied: self-skip in `lint_skill.py`; guard test added. |
| `V-2` | Low | Accepted by design | Re-run into the same out-dir exits 2 | E5; documented in v2 §4.8 | Keep; optionally add unique run dirs. Not a defect. |
| `V-3` | Medium | **Closed** | Six regression tests named in v2 docs do not exist | **Fixed**: all six exist in `tests/test_cli.py`; R2 green. They guard provenance, complex intervals, timeout, truncation notice, the git-authorisation gate, and other-script scanning. | Applied: six tests added. |
| `V-4` | Medium | **Closed (Option A)** | Residual DoS surface in the “safe” evaluator | **Fixed for allocation vectors**: `MAX_MATRIX_DIM=64`, `MAX_INT_ARG=10_000`, `MAX_SEQ=4096`; R7 rejects 12/12 oversized forms, R8 accepts 12/12 bounded forms. `integrate/limit/solve` remain under the documented trusted-input model plus per-check SIGALRM timeout; no true OOM/hang was induced. | Applied: caps in `safe_expr.py`; `references/tool-safety.md` rule 2 updated. |
| `V-5` | Low | **Open** | “Broken local link” check is vacuous | `SKILL.md` paths are code spans, not `](…)` links; only the hard-coded `REQUIRED` list guards existence | Parse Markdown links, or drop the claim. |
| `V-6` | Low | **Open** | Package contradicts v1 packaging rule | `samples/` (1.1 MB PDF) and `docs/` ship inside the skill; v1 §14 says “keep eval suite outside the skill folder”; v1 §13 says no auxiliary docs | Declare the exception in `SKILL.md`, or move audit artefacts to repo `docs/`. |
| `V-7` | Low | **Open** | Verification playbook lost content | Shipped playbook is 32 lines; v1 had universal checks 1–7, an executable JSON example, SymPy patterns, and a probability row | Restore them compactly; keep v2 suite contract. |
| `V-8` | Low | **Open** | `--pages` accepts garbage → traceback | E7; `extract_pdf.py:80` `int(lo)` uncaught | Use an argparse `type` / catch `ValueError` → exit 2. |
| `V-9` | — | **Refuted** | Hypothesis that textless PDFs still exit 0 | E8 + `test_textless_pdf_exit3` | — |
| `V-10` | Low | **Open** | Wrong rejection message for huge exponents | E11: `UnsafeExpression` subclasses `ValueError`, so its own `except ValueError` rewrites “exponent too large” as “non-finite exponent” | Re-raise `UnsafeExpression` before the generic `ValueError` catch. |
| `V-11` | Low | **Open** | Config-class malformed expressions report as maths ERROR | E13: `expr: [1,2]`, `expr: I` → row `ERROR`, exit 1 | Validate result type/shape and raise `ConfigError` → exit 2. |
| `V-12` | Low | **Open** | `SKILL.md` file tree is incomplete | Tree at `SKILL.md:10–15` omits `samples/` and `docs/` | Add them or move them out. |
| `V-13` | Low | **Open** | v2 promotion commands are partly wrong | PART 5’s `# expect PASS` / `# expect all pass` and PART 6’s “Linter would PASS” are now true (R1/R2); `../../samples/…` still resolves outside the skill | Replace the sample path with `samples/2026_Prelim_P1.pdf` (verified block in §6). |
| `V-14` | Low | **Open** | Distinct `Deduce` obligation dropped | v2 command-word table merges “Hence / Deduce”; `exam-presentation.md` §2 lists only `Hence` | Restore a `Deduce` row. |
| `S-1` | Low | **Open** | Exemplar provenance over-claim | See `SAMPLE-01` residual | Change to “7/7 via `assets/checks.example.json` (executed)” or “hand-checked”; add `checks_sha256`/tool-version line (`N/A — no CAS`). |

Counts: **0 High, 0 Medium, 10 Low open**; 1 accepted-by-design; 1 refuted. V-1, V-3 and V-4 are closed with executed evidence.

---

## 5. Conformance matrix

| Requirement | Status | Note |
|---|---|---|
| `SKILL.md` at skill root; frontmatter `name`/`description` | PASS | name 27 chars, matches dir; description 680 chars |
| Body < 500 lines, progressive disclosure | PASS | 139 lines |
| Supporting files use relative forward-slash paths | PASS | All referenced files exist |
| No auxiliary README/CHANGELOG | PASS | none; `docs/`/`samples/` are the exception (V-6) |
| Scripts deterministic, dependency-light, no network | PASS | stdlib + sympy/pdfplumber only |
| `lint_skill.py` exits 0 | PASS | R1 |
| `pytest` green | PASS | R2: 60 passed |
| Exit-code contract 0/1/2/3 | PASS | E3/E5/E8/E14; usage path still fails (V-8, Low) |
| No arbitrary code execution | PASS | E9 |
| Memory-exhaustion vectors capped | PASS | R7/R8; `MAX_MATRIX_DIM=64`, `MAX_INT_ARG=10_000`, `MAX_SEQ=4096` |
| Empty/malformed suite fails closed | PASS | `MIN_CHECKS_FLOOR=2`, E14 |
| No unrequested git side effects | PASS | `SKILL.md:82–86`, R10 |
| Textless PDF fails closed | PASS | E8 |
| No overwrite without `--force` | PASS | E5/E6/R5/R6 |
| Provenance in ledger | PARTIAL | code emits `checks_sha256`; exemplar omits it (S-1, Low) |
| Q6 regression suite 7/7 | PASS | R3 |
| Eval suite outside skill folder | **FAIL (undocumented, Low)** | `tests/`, `samples/` inside (V-6) |
| File tree complete | **FAIL (Low)** | omits `samples/`, `docs/` (V-12) |

---

## 6. Doc ↔ code contradictions — status after revision 2

1. **Resolved:** PART 5 `# expect PASS` now matches R1.
2. **Resolved:** PART 5 `# expect all pass` now matches R2 (60 passed).
3. **Resolved:** PART 3’s six tests now exist (V-3 closed).
4. **Resolved:** PART 6 “Linter would PASS” now matches R1.
5. **Open (Low V-13):** PART 5’s `../../samples/2026_Prelim_P1.pdf` resolves outside the skill; the sample is at `samples/2026_Prelim_P1.pdf` relative to the skill root.
6. **Open (Low V-6):** v1 §14 “keep eval suite outside the skill folder” vs shipped `tests/` and `samples/`.

Verified command block (from the skill directory):

```bash
python3 scripts/lint_skill.py .                                             # exit 0, PASS
uv run --with pytest --with sympy --with pdfplumber pytest -q tests/        # 60 passed
uv run --with sympy python scripts/check_math.py assets/checks.example.json # 7/7, exit 0
uv run --with pdfplumber python scripts/extract_pdf.py \
  samples/2026_Prelim_P1.pdf --out /tmp/out                                 # exit 0; add --force to rerun
```

---

## 7. Unverified / residual risk

- PDF-02 false-positive rate (`343`) is **Reported-Verified (external)**; not re-counted.
- V-4 allocation caps are **Verified (executed)** for the listed vectors (R7/R8). `integrate/limit/solve` remain timeout-bounded, not argument-capped; a true OOM/hang was not induced.
- The truncation regression uses a generated 45-page blank PDF in `tmp_path`; it verifies the render/truncation path, not extraction quality.
- `test_timeout_fails_closed` depends on SIGALRM and a deliberately expensive expression; it passed in R2 but is inherently timing-sensitive.
- `checks.example.json` mathematics was executed and passes, but the underlying paper/bound-solution correspondence is **Reported-Verified (external)**; page images were not re-read here.
- Repo root has unrelated pre-existing changes (`backup/…`, `settings.json`, submodule). The skill subtree now contains the five fix files plus these two reports; nothing was committed or pushed.

---

## 8. Remediation status (revision 2)

**Applied and verified**

| Item | Status | Evidence |
|---|---|---|
| P0.1 Fix lint self-scan | Done | V-1; R1 exit 0; R10 still flags copied script |
| P0.2 pytest green | Done | R2: 60 passed |
| P1.4 Six regression tests | Done | `tests/test_cli.py`; R2 |
| P2.6 Allocation caps | Done (Option A) | `scripts/safe_expr.py`; R7/R8; `references/tool-safety.md` |
| Re-validation | Done | R1–R11; hashes in §1 |

**Still open (all Low; non-blocking)**

| Item | Status | Finding |
|---|---|---|
| Add `samples/`/`docs/` to the tree or move `docs/` out | Open | V-6 / V-12 |
| Restore playbook checks 1–7 and SymPy patterns | Open | V-7 |
| Reject `--pages` garbage as exit 2 | Open | V-8 |
| Fix huge-exponent message | Open | V-10 |
| Validate result types → `ConfigError` | Open | V-11 |
| Fix v2 sample path; align PART 5/6 | Open | V-13 |
| Restore `Deduce` row | Open | V-14 |
| Fix exemplar provenance line | Open | S-1 |
| Implement or drop the link check | Open | V-5 |

No High/Medium finding remains open. Nothing was committed or pushed.

**Files changed in revision 2:** `scripts/lint_skill.py`, `scripts/safe_expr.py`, `tests/test_cli.py`, `tests/test_safe_expr.py`, `references/tool-safety.md`, `docs/validation_report.md`, `docs/validation_report.json`.
