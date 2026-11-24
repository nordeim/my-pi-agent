# Validation report — `solving-a-level-exam-papers`

**Date:** 2026-11-24 · **Branch:** `main` · **HEAD:** `ced14ee24305abb837773b1c93e1e73352491a43`
**Skill subtree:** clean before validation (probes written under `/tmp`; the only transient artefact, `__pycache__`, was removed). Afterwards the only additions are these two authorised report files in `docs/`; no skill source file was modified.
**Verdict:** **NOT promotable to `Verified`.** The v2 security/correctness remediation is real and verified, but the promotion gate fails: `lint_skill.py` exits 1 and `pytest` is red. The v2 promotion doc claims both pass.

Evidence labels: **Verified (executed)** · **Confirmed (static)** · **Reported-Verified (external)** · **Refuted**.

---

## 1. Provenance

| Artefact | SHA-256 |
|---|---|
| `SKILL.md` | `ce2cde66bbc65809a296caa2aceb4620bbada403914de0b8f0d6478dbd493327` |
| `assets/checks.example.json` | `18c1a7f6668c01f20c4c662eabb5692c87a7b391a9b7e9510787d7fba42489f2` |
| `scripts/check_math.py` | `5ee3d3f1272795c80b8bf202ded7bd9374745cae9e3eb823dc7b349c4ae3627f` |
| `scripts/extract_pdf.py` | `031d55b3c08a83df67b1f33152f52c433be024e8b28305c180a7309635766356` |
| `scripts/lint_skill.py` | `de58e349a92d20dcd5705155e0ab4a36e4159c705c65d5d9986bed788116fa8e` |
| `scripts/safe_expr.py` | `a5138e8f8c9f287c993d670dee8f0c675afcf21c5aa6a86e95d89fcfb41de3fc` |
| `tests/test_cli.py` | `6c9c7deab8e130368f2ec97a6cd2257fbc4a0c972ce3782330169012e8625171` |
| `tests/test_safe_expr.py` | `54357005fab72324c2b3754344a44114315e3ee16aeeca0bb46dde7539e0efe5` |
| `samples/2026_Prelim_P1.pdf` | `c5873a178e9538e78e1710d050e29bc25fc969bdfed29767c3948a2d558b57c8` |
| `docs/SKILL_v1.md` | `834d465a909d9d7d99a2345ffbaf61dfc079546b51f3737ce3a3a10be4963a36` |
| `docs/v1_to_v2_updates.md` | `624e13fb4462c926d932f999433e9d39d6d17e9ffdcf74b48c2828cb8bc2081d` |
| `docs/independent_skill_audit_report.json` | `f019b2937810c65432ebb990db1c9bd1031291fe8db70d9cb92ac5bc09144612` |

Environment: Python 3.14.7 · pytest 9.2.0 · sympy 1.14.0 · pdfplumber 0.11.11 (installed on demand via `uv run --with …`; not in the default interpreter).

Two questions are kept separate throughout:
1. **Conformance** — does the shipped package implement what its own docs claim?
2. **Truth** — are those claims correct when executed?

---

## 2. Executed evidence

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
| `V-1` | **High** | **Open** | Linter fails on its own package | E1: `BANNED` at `lint_skill.py:16–17`; `ALLOWED_BANNED={"safe_expr.py"}` at line 18 does not exclude `lint_skill.py` | Skip the linter file itself in the scan (it must contain the patterns), or load the ban list from data. |
| `V-2` | Low | Accepted by design | Re-run into the same out-dir exits 2 | E5; documented in v2 §4.8 | Keep; optionally add unique run dirs. Not a defect. |
| `V-3` | Medium | **Open** | Six regression tests named in v2 docs do not exist | Absent: `test_lint_requires_authorisation_gate`, `test_report_truncation_notice`, `test_interval_complex_errors`, `test_timeout_fails_closed`, `test_provenance_present`, `test_force_overwrites` | Add the tests (behaviour exists; E6/E8/E12/E13 prove it) or remove the claims. |
| `V-4` | Medium | **Open** | Residual DoS surface in the “safe” evaluator | `safe_expr.py:17–37` exposes `Matrix/diag/eye/zeros/ones` with no dimension cap and `factorial/binomial/gamma/integrate/limit/solve` with no argument cap; E10. Timeout works (E12) but cannot preempt a large C-level allocation reliably | Cap matrix dimensions and factorial/binomial arguments; gate/remove `integrate/limit/solve`; document the trusted-input model. |
| `V-5` | Low | **Open** | “Broken local link” check is vacuous | `SKILL.md` paths are code spans, not `](…)` links; only the hard-coded `REQUIRED` list guards existence | Parse Markdown links, or drop the claim. |
| `V-6` | Low | **Open** | Package contradicts v1 packaging rule | `samples/` (1.1 MB PDF) and `docs/` ship inside the skill; v1 §14 says “keep eval suite outside the skill folder”; v1 §13 says no auxiliary docs | Declare the exception in `SKILL.md`, or move audit artefacts to repo `docs/`. |
| `V-7` | Low | **Open** | Verification playbook lost content | Shipped playbook is 32 lines; v1 had universal checks 1–7, an executable JSON example, SymPy patterns, and a probability row | Restore them compactly; keep v2 suite contract. |
| `V-8` | Low | **Open** | `--pages` accepts garbage → traceback | E7; `extract_pdf.py:80` `int(lo)` uncaught | Use an argparse `type` / catch `ValueError` → exit 2. |
| `V-9` | — | **Refuted** | Hypothesis that textless PDFs still exit 0 | E8 + `test_textless_pdf_exit3` | — |
| `V-10` | Low | **Open** | Wrong rejection message for huge exponents | E11: `UnsafeExpression` subclasses `ValueError`, so its own `except ValueError` rewrites “exponent too large” as “non-finite exponent” | Re-raise `UnsafeExpression` before the generic `ValueError` catch. |
| `V-11` | Low | **Open** | Config-class malformed expressions report as maths ERROR | E13: `expr: [1,2]`, `expr: I` → row `ERROR`, exit 1 | Validate result type/shape and raise `ConfigError` → exit 2. |
| `V-12` | Low | **Open** | `SKILL.md` file tree is incomplete | Tree at `SKILL.md:10–15` omits `samples/` and `docs/` | Add them or move them out. |
| `V-13` | Low | **Open** | v2 promotion commands are wrong | `v1_to_v2_updates.md` PART 5: `# expect PASS` (E1 says 1), `# expect all pass` (E2 says 1 failed), `../../samples/…` resolves outside the skill; PART 6 “Linter would PASS” | Replace with the verified command block in §6. |
| `V-14` | Low | **Open** | Distinct `Deduce` obligation dropped | v2 command-word table merges “Hence / Deduce”; `exam-presentation.md` §2 lists only `Hence` | Restore a `Deduce` row. |
| `S-1` | Low | **Open** | Exemplar provenance over-claim | See `SAMPLE-01` residual | Change to “7/7 via `assets/checks.example.json` (executed)” or “hand-checked”; add `checks_sha256`/tool-version line (`N/A — no CAS`). |

Counts: **1 High, 2 Medium, 10 Low open**; 1 accepted-by-design; 1 refuted.

---

## 5. Conformance matrix

| Requirement | Status | Note |
|---|---|---|
| `SKILL.md` at skill root; frontmatter `name`/`description` | PASS | name 27 chars, matches dir; description 680 chars |
| Body < 500 lines, progressive disclosure | PASS | 139 lines |
| Supporting files use relative forward-slash paths | PASS | All referenced files exist |
| No auxiliary README/CHANGELOG | PASS | none; `docs/`/`samples/` are the exception (V-6) |
| Scripts deterministic, dependency-light, no network | PASS | stdlib + sympy/pdfplumber only |
| `lint_skill.py` exits 0 | **FAIL** | E1 (V-1) |
| `pytest` green | **FAIL** | E2 |
| Exit-code contract 0/1/2/3 | PASS | E3/E5/E8/E14; usage path fails (V-8) |
| No arbitrary code execution | PASS | E9 |
| Empty/malformed suite fails closed | PASS | `MIN_CHECKS_FLOOR=2`, E14 |
| No unrequested git side effects | PASS | `SKILL.md:82–86` |
| Textless PDF fails closed | PASS | E8 |
| No overwrite without `--force` | PASS | E5/E6 |
| Provenance in ledger | PARTIAL | code emits `checks_sha256`; exemplar omits it (S-1) |
| Q6 regression suite 7/7 | PASS | E3 |
| Eval suite outside skill folder | **FAIL (undocumented)** | `tests/`, `samples/` inside (V-6) |
| File tree complete | **FAIL** | omits `samples/`, `docs/` (V-12) |

---

## 6. Doc ↔ code contradictions

1. `docs/v1_to_v2_updates.md` PART 5 (`# expect PASS`, `# expect all pass`) is false against E1/E2. v1 §15 correctly labelled lint as “Unverifiable here”; v2 upgraded it to an expectation without execution.
2. `extract_pdf.py ../../samples/2026_Prelim_P1.pdf` in PART 5 resolves to `/home/pete/.pi/agent/samples/…`; the sample is at `skills/solving-a-level-exam-papers/samples/…`.
3. PART 3 names six tests that do not exist (V-3).
4. PART 6 row “Linter would PASS” contradicts E1.
5. v1 §14 “keep eval suite outside the skill folder” vs shipped `tests/` and `samples/`.

Verified replacement command block (from the skill directory):

```bash
python3 scripts/lint_skill.py .                                             # 0 after V-1 fix
uv run --with pytest --with sympy --with pdfplumber pytest -q tests/        # all pass after V-1
uv run --with sympy python scripts/check_math.py assets/checks.example.json # 7/7, 0
uv run --with pdfplumber python scripts/extract_pdf.py \
  samples/2026_Prelim_P1.pdf --out /tmp/out                                 # 0
```

---

## 7. Unverified / residual risk

- PDF-02 false-positive rate (`343`) is **Reported-Verified (external)**; not re-counted.
- V-4 is **Confirmed (static)** plus bounded acceptance probes (E10). A true OOM/hang was not induced.
- `checks.example.json` mathematics was executed and passes, but the underlying paper/bound-solution correspondence is **Reported-Verified (external)**; page images were not re-read here.
- Repo root has unrelated pre-existing changes (`backup/…`, `settings.json`, submodule); the skill subtree itself is clean and was not touched.

---

## 8. Remediation plan (ordered)

**P0 — unblock promotion**
1. Fix `lint_skill.py` self-scan (skip own file). Acceptance: E1 → exit 0.
2. Re-run E2; `test_lint_passes_package` must pass. Acceptance: 30 passed.

**P1 — make the docs true**
3. Replace PART 5/6 commands with the verified block above; fix the sample path; correct the test list.
4. Add the six missing regression tests (or delete the claims).
5. Add `samples/` and `docs/` to the `SKILL.md` tree, or move `docs/` out and document the sample fixture.

**P2 — harden the evaluator**
6. Cap matrix dimensions and factorial/binomial args; gate/remove `integrate/limit/solve`; re-raise `UnsafeExpression` before `except ValueError` (V-10).
7. Validate result types (`Expr`/`Matrix`) → `ConfigError` exit 2 (V-11).
8. Validate `--pages` with an argparse type and page-range check (V-8/V-15).

**P3 — restore fidelity**
9. Restore playbook universal checks 1–7 and SymPy patterns (V-7); implement the link check or drop it (V-5).
10. Restore the `Deduce` row (V-14); fix exemplar provenance (S-1).

No fixes were applied in this validation pass. Nothing was committed or pushed.
