Evidence is complete. Writing the two deliverables now.
# Wrote skills/solving-a-level-exam-papers/docs/validation_report.md
# Validation report — `solving-a-level-exam-papers`

**Date:** 2026-11-24 · **Branch:** `main` · **HEAD:** `ced14ee24305abb837773b1c93e1e73352491a43`
**Skill subtree:** clean before and after validation (probes written under `/tmp`; only `__pycache__` was created and removed).
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

Thought: 21.1s
Now the JSON. Must be valid. Include metadata, summary, findings, externalClosure, conformance, evidence, contradictions, remediation. Keep hashes.

Ensure no trailing commas. Write.
# Wrote skills/solving-a-level-exam-papers/docs/validation_report.json
{
  "schemaVersion": "1.0",
  "report": "validation_report",
  "generatedAt": "2026-11-24",
  "target": {
    "skill": "solving-a-level-exam-papers",
    "path": "skills/solving-a-level-exam-papers",
    "repo": "nordeim/my-pi-agent",
    "branch": "main",
    "head": "ced14ee24305abb837773b1c93e1e73352491a43",
    "skillSubtreeClean": true
  },
  "environment": {
    "python": "3.14.7",
    "pytest": "9.2.0",
    "sympy": "1.14.0",
    "pdfplumber": "0.11.11",
    "installMethod": "uv run --with (on demand; not in default interpreter)"
  },
  "verdict": {
    "promotableToVerified": false,
    "conformance": "FAIL",
    "truthOfClaims": "PARTIAL",
    "summary": "Security and correctness remediation is real and verified, but the promotion gate fails: lint exits 1 and pytest has 1 failure. The v2 promotion doc claims both pass."
  },
  "summary": {
    "openHigh": 1,
    "openMedium": 2,
    "openLow": 10,
    "acceptedByDesign": 1,
    "refuted": 1,
    "externalFindingsClosed": 5,
    "externalFindingsPartial": 1,
    "externalFindingsClosedWithResidual": 1
  },
  "provenance": {
    "sha256": {
      "SKILL.md": "ce2cde66bbc65809a296caa2aceb4620bbada403914de0b8f0d6478dbd493327",
      "assets/checks.example.json": "18c1a7f6668c01f20c4c662eabb5692c87a7b391a9b7e9510787d7fba42489f2",
      "scripts/check_math.py": "5ee3d3f1272795c80b8bf202ded7bd9374745cae9e3eb823dc7b349c4ae3627f",
      "scripts/extract_pdf.py": "031d55b3c08a83df67b1f33152f52c433be024e8b28305c180a7309635766356",
      "scripts/lint_skill.py": "de58e349a92d20dcd5705155e0ab4a36e4159c705c65d5d9986bed788116fa8e",
      "scripts/safe_expr.py": "a5138e8f8c9f287c993d670dee8f0c675afcf21c5aa6a86e95d89fcfb41de3fc",
      "tests/test_cli.py": "6c9c7deab8e130368f2ec97a6cd2257fbc4a0c972ce3782330169012e8625171",
      "tests/test_safe_expr.py": "54357005fab72324c2b3754344a44114315e3ee16aeeca0bb46dde7539e0efe5",
      "samples/2026_Prelim_P1.pdf": "c5873a178e9538e78e1710d050e29bc25fc969bdfed29767c3948a2d558b57c8",
      "docs/SKILL_v1.md": "834d465a909d9d7d99a2345ffbaf61dfc079546b51f3737ce3a3a10be4963a36",
      "docs/v1_to_v2_updates.md": "624e13fb4462c926d932f999433e9d39d6d17e9ffdcf74b48c2828cb8bc2081d",
      "docs/independent_skill_audit_report.json": "f019b2937810c65432ebb990db1c9bd1031291fe8db70d9cb92ac5bc09144612"
    }
  },
  "method": {
    "axes": [
      "conformance: shipped package vs its own documented claims",
      "truth: documented claims when executed"
    ],
    "labels": ["Verified (executed)", "Confirmed (static)", "Reported-Verified (external)", "Refuted"],
    "isolation": "All probes and outputs under /tmp; no skill files modified; no commits or pushes"
  },
  "findings": [
    {
      "id": "V-1",
      "origin": "self",
      "severity": "High",
      "confidence": "Verified (executed)",
      "status": "Open",
      "title": "Linter fails on its own package",
      "location": "scripts/lint_skill.py:16-18",
      "evidence": "`python3 scripts/lint_skill.py .` exits 1 with 7 unsafe-pattern hits, all in lint_skill.py. BANNED at 16-17; ALLOWED_BANNED at 18 excludes only safe_expr.py.",
      "impact": "Hard conformance gate fails; test_lint_passes_package is red; v2 promotion claims PASS.",
      "recommendation": "Skip the linter file itself in the scan (it must contain the patterns), or load the ban list from a data file."
    },
    {
      "id": "V-2",
      "origin": "self",
      "severity": "Low",
      "confidence": "Verified (executed)",
      "status": "Accepted by design",
      "title": "Re-run into same out-dir exits 2",
      "location": "scripts/extract_pdf.py:26-34",
      "evidence": "Run 2 same --out exits 2; --force exits 0. Disclosed in v2 section 4.8.",
      "impact": "Fail-closed; no data loss. UX only.",
      "recommendation": "Keep; optionally add unique run directories."
    },
    {
      "id": "V-3",
      "origin": "self",
      "severity": "Medium",
      "confidence": "Confirmed (static)",
      "status": "Open",
      "title": "Six regression tests named in v2 docs do not exist",
      "location": "tests/test_cli.py; docs/v1_to_v2_updates.md PART 3",
      "evidence": "Absent: test_lint_requires_authorisation_gate, test_report_truncation_notice, test_interval_complex_errors, test_timeout_fails_closed, test_provenance_present, test_force_overwrites.",
      "impact": "Documented QA coverage is overstated; behaviours exist but are unguarded.",
      "recommendation": "Add the tests or remove the claims."
    },
    {
      "id": "V-4",
      "origin": "self",
      "severity": "Medium",
      "confidence": "Confirmed (static) + bounded probes",
      "status": "Open",
      "title": "Residual DoS surface in safe_expr",
      "location": "scripts/safe_expr.py:17-37",
      "evidence": "No dimension cap for Matrix/diag/eye/zeros/ones; no argument cap for factorial/binomial/gamma/integrate/limit/solve. eye(1000), zeros(2000,2000), factorial(200000) accepted. Timeout interrupts Python work (ERROR) but cannot reliably preempt large C-level allocation.",
      "impact": "Model-supplied or adversarial expressions can exhaust memory/CPU.",
      "recommendation": "Cap matrix dimensions and factorial/binomial args; gate or remove integrate/limit/solve; document the trusted-input model."
    },
    {
      "id": "V-5",
      "origin": "self",
      "severity": "Low",
      "confidence": "Confirmed (static)",
      "status": "Open",
      "title": "Broken-local-link check is vacuous",
      "location": "scripts/lint_skill.py",
      "evidence": "SKILL.md paths are code spans, not markdown links; only the hardcoded REQUIRED list guards existence.",
      "impact": "Linter cannot detect broken relative links.",
      "recommendation": "Parse markdown links, or drop the claim."
    },
    {
      "id": "V-6",
      "origin": "self",
      "severity": "Low",
      "confidence": "Confirmed (static)",
      "status": "Open",
      "title": "Packaging contradicts v1 rules",
      "location": "samples/; docs/; docs/SKILL_v1.md sections 13-14",
      "evidence": "samples/ (1.1 MB PDF) and docs/ ship inside the skill; v1 says keep the eval suite outside the skill folder and no auxiliary docs.",
      "impact": "Packaging rule is violated without disclosure.",
      "recommendation": "Declare the exception in SKILL.md, or move audit artefacts to repo docs/."
    },
    {
      "id": "V-7",
      "origin": "self",
      "severity": "Low",
      "confidence": "Confirmed (static)",
      "status": "Open",
      "title": "Verification playbook lost content",
      "location": "references/verification-playbook.md",
      "evidence": "Shipped playbook is 32 lines; v1 had universal checks 1-7, executable JSON example, SymPy patterns, and a probability row.",
      "impact": "Weaker G4 guidance for topics outside the Q6 example.",
      "recommendation": "Restore them compactly while keeping the v2 suite contract."
    },
    {
      "id": "V-8",
      "origin": "self",
      "severity": "Low",
      "confidence": "Verified (executed)",
      "status": "Open",
      "title": "--pages accepts garbage and tracebacks",
      "location": "scripts/extract_pdf.py:80",
      "evidence": "--pages abc exits 1 with an uncaught ValueError traceback instead of exit 2.",
      "impact": "Violates the documented usage/config exit-code contract.",
      "recommendation": "Use an argparse type or catch ValueError and exit 2; reject non-positive and out-of-range pages."
    },
    {
      "id": "V-9",
      "origin": "self",
      "severity": "None",
      "confidence": "Refuted",
      "status": "Refuted",
      "title": "Textless PDF still fails open (hypothesis)",
      "location": "scripts/extract_pdf.py",
      "evidence": "--pages 999 yields pages=0, G0 FAILED, exit 3; test_textless_pdf_exit3 passes.",
      "impact": "No defect.",
      "recommendation": "None."
    },
    {
      "id": "V-10",
      "origin": "self",
      "severity": "Low",
      "confidence": "Verified (executed)",
      "status": "Open",
      "title": "Wrong rejection message for huge exponents",
      "location": "scripts/safe_expr.py",
      "evidence": "2**100000 is rejected as 'non-finite exponent' because UnsafeExpression subclasses ValueError and is caught by its own except ValueError.",
      "impact": "Fails closed, but the message misdiagnoses the cause.",
      "recommendation": "Re-raise UnsafeExpression before the generic ValueError catch."
    },
    {
      "id": "V-11",
      "origin": "self",
      "severity": "Low",
      "confidence": "Verified (executed)",
      "status": "Open",
      "title": "Config-class malformed expressions report as maths ERROR",
      "location": "scripts/check_math.py",
      "evidence": "expr [1,2] and expr I produce ERROR rows and exit 1, not config exit 2.",
      "impact": "Blurs config vs maths failure semantics.",
      "recommendation": "Validate result type (Expr/Matrix) and raise ConfigError."
    },
    {
      "id": "V-12",
      "origin": "self",
      "severity": "Low",
      "confidence": "Confirmed (static)",
      "status": "Open",
      "title": "SKILL.md file tree is incomplete",
      "location": "SKILL.md:10-15",
      "evidence": "Tree omits samples/ and docs/ that ship.",
      "impact": "Manifest does not match package.",
      "recommendation": "Add them, or move docs/ out and document the sample fixture."
    },
    {
      "id": "V-13",
      "origin": "self",
      "severity": "Low",
      "confidence": "Verified (executed)",
      "status": "Open",
      "title": "v2 promotion commands are wrong",
      "location": "docs/v1_to_v2_updates.md PART 5-6",
      "evidence": "'# expect PASS' is false (exit 1); '# expect all pass' is false (1 failed); ../../samples path resolves outside the skill; PART 6 says 'Linter would PASS'.",
      "impact": "A reviewer following the doc cannot reach Verified and will misdiagnose the failure.",
      "recommendation": "Replace with the verified command block and correct paths."
    },
    {
      "id": "V-14",
      "origin": "self",
      "severity": "Low",
      "confidence": "Confirmed (static)",
      "status": "Open",
      "title": "Distinct Deduce obligation dropped",
      "location": "SKILL.md command-word table; references/exam-presentation.md section 2",
      "evidence": "v2 merges 'Hence / Deduce'; v1 had a distinct Deduce row.",
      "impact": "One command-word obligation is no longer explicit.",
      "recommendation": "Restore a Deduce row."
    },
    {
      "id": "S-1",
      "origin": "self",
      "severity": "Low",
      "confidence": "Confirmed (static)",
      "status": "Open",
      "title": "Exemplar provenance over-claim",
      "location": "samples/model_answer_6_corrected.md:205, 258-263",
      "evidence": "Handoff claims 'Verified: 7/7 exact checks' while section 5 says 'no CAS ... executed'; ledger omits checks_sha256/tool version required by the solution template.",
      "impact": "Weakens the exemplar as a conformance reference.",
      "recommendation": "Say '7/7 via assets/checks.example.json (executed)' or 'hand-checked'; add checks_sha256 N/A with reason."
    }
  ],
  "externalClosure": [
    {
      "id": "SEC-01",
      "severity": "High",
      "status": "Closed",
      "evidence": "sympify/parse_expr removed; safe_expr AST whitelist rejects attribute, subscript, dunder, lambda; unsafe payload exits 2 without side effect."
    },
    {
      "id": "GATE-01",
      "severity": "Medium",
      "status": "Closed",
      "evidence": "MIN_CHECKS_FLOOR=2, MAX_CHECKS=200; empty/missing/duplicate/malformed exit 2."
    },
    {
      "id": "SAFE-01",
      "severity": "Medium",
      "status": "Closed",
      "evidence": "SKILL.md:82-86 requires explicit authorisation, git status check, staging only the named deliverable, no add -A, no push/amend."
    },
    {
      "id": "PDF-01",
      "severity": "Medium",
      "status": "Closed",
      "evidence": "NO_TEXT_MIN_CHARS=20; G0 FAILED; exit 3 verified with empty corpus; regression test passes."
    },
    {
      "id": "DATA-01",
      "severity": "Medium",
      "status": "Closed",
      "evidence": "atomic_write refuses overwrite without --force; verified exit 2 then exit 0 with --force."
    },
    {
      "id": "PDF-02",
      "severity": "Low",
      "status": "Partially closed",
      "evidence": "Truncation notice and full-report path added; candidate tier retained; false-positive volume unchanged (343 reported externally, not re-counted)."
    },
    {
      "id": "SAMPLE-01",
      "severity": "Low",
      "status": "Closed with residual",
      "evidence": "Cover rules verbatim, fidelity table, and Verified/Deferred handoff present; residual provenance over-claim (S-1)."
    }
  ],
  "conformance": [
    {"requirement": "SKILL.md at root with frontmatter", "status": "PASS"},
    {"requirement": "Body < 500 lines", "status": "PASS", "note": "139 lines"},
    {"requirement": "Relative forward-slash supporting paths", "status": "PASS"},
    {"requirement": "No auxiliary README/CHANGELOG", "status": "PASS"},
    {"requirement": "Scripts deterministic, dependency-light, no network", "status": "PASS"},
    {"requirement": "lint_skill.py exits 0", "status": "FAIL", "note": "exit 1, V-1"},
    {"requirement": "pytest green", "status": "FAIL", "note": "1 failed, 29 passed"},
    {"requirement": "Exit-code contract", "status": "PASS", "note": "usage path fails, V-8"},
    {"requirement": "No arbitrary code execution", "status": "PASS"},
    {"requirement": "Empty/malformed suite fails closed", "status": "PASS"},
    {"requirement": "No unrequested git side effects", "status": "PASS"},
    {"requirement": "Textless PDF fails closed", "status": "PASS"},
    {"requirement": "No overwrite without --force", "status": "PASS"},
    {"requirement": "Provenance in ledger", "status": "PARTIAL", "note": "code yes; exemplar no"},
    {"requirement": "Q6 suite 7/7", "status": "PASS"},
    {"requirement": "Eval suite outside skill folder", "status": "FAIL", "note": "undocumented; V-6"},
    {"requirement": "File tree complete", "status": "FAIL", "note": "V-12"}
  ],
  "executedEvidence": [
    {"id": "E1", "command": "python3 scripts/lint_skill.py .", "result": "exit 1; body 139; 7 hits in lint_skill.py"},
    {"id": "E2", "command": "pytest -q tests/", "result": "1 failed, 29 passed in 7.62s; test_lint_passes_package"},
    {"id": "E3", "command": "check_math.py assets/checks.example.json", "result": "7/7 PASS exit 0; checks_sha256=18c1a7f6...; sympy 1.14.0"},
    {"id": "E4", "command": "extract_pdf.py sample --out /tmp (run 1)", "result": "exit 0; 24 pages; manifest"},
    {"id": "E5", "command": "same (run 2)", "result": "exit 2; refuses overwrite"},
    {"id": "E6", "command": "same --force (run 3)", "result": "exit 0"},
    {"id": "E7", "command": "extract_pdf.py --pages abc", "result": "exit 1; ValueError traceback at line 80"},
    {"id": "E8", "command": "extract_pdf.py --pages 999", "result": "exit 3; G0 FAILED; pages=0"},
    {"id": "E9", "command": "safe_expr attr/subscript/dunder/lambda", "result": "all rejected"},
    {"id": "E10", "command": "safe_expr eye(1000), zeros(2000,2000), factorial(200000)", "result": "all accepted; no size cap"},
    {"id": "E11", "command": "safe_expr 2**100000", "result": "rejected; message 'non-finite exponent'"},
    {"id": "E12", "command": "check_math.run_check timeout=0.001", "result": "ERROR per-check time limit exceeded"},
    {"id": "E13", "command": "interval expr I; zero expr [1,2]", "result": "ERROR rows; exit 1"},
    {"id": "E14", "command": "check_math malformed JSON", "result": "exit 2 CONFIG ERROR"}
  ],
  "docCodeContradictions": [
    "PART 5 '# expect PASS' false (exit 1)",
    "PART 5 '# expect all pass' false (1 failed)",
    "PART 5 ../../samples path resolves outside the skill",
    "PART 3 names six tests that do not exist",
    "PART 6 'Linter would PASS' false",
    "v1 section 14 'eval suite outside skill folder' vs shipped tests/ and samples/"
  ],
  "unverified": [
    "PDF-02 343 false positives: Reported-Verified (external), not re-counted",
    "V-4 OOM/hang not induced; bounded acceptance probes only",
    "Paper/bound-solution correspondence: Reported-Verified (external)"
  ],
  "remediation": {
    "P0": [
      "Fix lint self-scan; lint exit 0",
      "Re-run pytest; 30 passed"
    ],
    "P1": [
      "Correct PART 5-6 commands, sample path, test list",
      "Add six missing regression tests or delete claims",
      "Fix SKILL.md tree / declare samples+docs exception"
    ],
    "P2": [
      "Cap matrix and factorial/binomial args; gate integrate/limit/solve; fix exponent message",
      "Validate result types to ConfigError",
      "Validate --pages type and range"
    ],
    "P3": [
      "Restore playbook universal checks and SymPy patterns; implement link check or drop",
      "Restore Deduce row; fix exemplar provenance"
    ]
  },
  "sideEffects": {
    "skillFilesModified": false,
    "committed": false,
    "pushed": false,
    "tempArtifacts": "/tmp/val-probes, /tmp/val-oor",
    "cleanup": "removed scripts/__pycache__ and tests/__pycache__"
  }
}

Thought: 4.3s
Validate JSON and check that docs are now untracked (new files) in skill subtree — that's expected deliverables but it means skill subtree no longer clean (two new report files). The report says skill subtree clean before/after validation, but we just wrote reports into docs/, so now untracked. Need to reconcile: reports are authorized deliverables, not skill source edits. Update wording? The md says "Skill subtree: clean before and after validation (probes...)" — now false because we added reports. Need to fix that line: "clean before; only the two authorized report files were added afterwards." Also JSON sideEffects skillFilesModified false is accurate for skill files, but new report files added. Add reportsWritten. Let me update.

Also validate JSON with python json.tool, and check git status.

Fix md line and JSON. Also maybe report path is inside skill docs/ which reinforces V-6 (docs inside skill). Hmm — user authorized reports in docs/. That itself adds to docs/. Note it. Could instead write to repo docs/ outside skill? Prior decision: docs/validation_report.* inside skill docs. The summary says "Reports to be written to docs/validation_report.md and .json (authorized deliverables)". Ambiguous whether repo docs or skill docs. I wrote inside skill docs. That's consistent with existing docs/ location but worsens V-6. Better: keep, but explicitly note they are validation artefacts and optionally should move with the other audit docs. Or move to repo-level docs/? Repo root docs may not exist. Let me check. If repo has docs/, maybe better there. But the audit artifacts live in skill docs/; consistency favors there. Keep and disclose.

Update md provenance line and add "Reports added" in side effects. Then validate.

Also the JSON summary externalFindingsClosed: 5? Count: SEC-01, GATE-01, SAFE-01, PDF-01, DATA-01 = 5 closed; PDF-02 partial 1; SAMPLE-01 closed-with-residual 1. Correct.

Open counts: High 1 (V-1), Medium 2 (V-3,V-4), Low: V-5,V-6,V-7,V-8,V-10,V-11,V-12,V-13,V-14,S-1 = 10. Correct.

Now edit md.
$ cd /home/pete/.pi/agent/skills/solving-a-level-exam-papers && python3 -c "import json;json.load(open('docs/validation_report.json'));print('JSON OK')"
JSON OK
← Edit skills/solving-a-level-exam-papers/docs/validation_report.md
# Validation report — `solving-a-level-exam-papers`# Validation report — `solving-a-level-exam-papers`

**Date:** 2026-11-24 · **Branch:** `main` · **HEAD:** `ced14ee24305abb837773b1c93e1e73352491a43`**Date:** 2026-11-24 · **Branch:** `main` · **HEAD:** `ced14ee24305abb837773b1c93e1e73352491a43`
**Skill subtree:** clean before and after validation (probes written under `/tmp`; only `__pycache__` was created and removed).**Skill subtree:** clean before validation (probes written under `/tmp`; the only transient artefact, `__pycache__`, was removed). Afterwards the only additions are these two authorised report files in `docs/`; no skill source file was modified.
**Verdict:** **NOT promotable to `Verified`.** The v2 security/correctness remediation is real and verified, but the promotion gate fails: `lint_skill.py` exits 1 and `pytest` is red. The v2 promotion doc claims both pass.
**Verdict:** **NOT promotable to `Verified`.** The v2 security/correctness remediation is real and verified, but the promotion gate fails: `lint_skill.py` exits 1 and `pytest` is red. The v2 promotion doc claims both pass.
Evidence labels: **Verified (executed)** · **Confirmed (static)** · **Reported-Verified (external)** · **Refuted**.
Evidence labels: **Verified (executed)** · **Confirmed (static)** · **Reported-Verified (external)** · **Refuted**.

← Edit skills/solving-a-level-exam-papers/docs/validation_report.json
    "Restore Deduce row; fix exemplar provenance"    "Restore Deduce row; fix exemplar provenance"
  ]  ]
},},
"sideEffects": {"sideEffects": {
  "skillFilesModified": false,  "skillSourceFilesModified": false,
  "reportsWritten": [
    "docs/validation_report.md",
    "docs/validation_report.json"
  ],
  "committed": false,  "committed": false,
  "pushed": false,  "pushed": false,
  "tempArtifacts": "/tmp/val-probes, /tmp/val-oor",  "tempArtifacts": "/tmp/val-probes, /tmp/val-oor",
  "cleanup": "removed scripts/__pycache__ and tests/__pycache__"  "cleanup": "removed scripts/__pycache__ and tests/__pycache__"
Thought: 2.0s
Now update todos: P0-P10 statuses. We completed all except maybe P10 delivery. Let me set P0-P9 completed, P10 completed (reports delivered). But the todo list contents from prior summary: P0..P10. We don't have exact names, but can reconstruct reasonable. Mark all completed.

Then final summary to user: verdict, key findings, reports written, no fixes applied, ask whether to apply P0 fixes.

Keep concise (<4 lines? But user asked status; a bit more is fine, still concise). Include file refs. Mention 1 High/2 Medium/10 Low; external closures; docs contradiction. Offer next step.

Let me update todo list.
# Todos
[✓] P0 Freeze provenance (HEAD, clean tree, hashes)
[✓] P1 Run lint and record result
[✓] P2 Verify external audit findings SEC-01..SAMPLE-01
[✓] P3 Verify self-findings V-1..V-9
[✓] P4 Adversarial probes (injection, DoS, timeout, malformed inputs)
[✓] P5 Execute scripts and pytest evidence
[✓] P6 v1-to-v2 delta audit
[✓] P7 Doc-vs-code consistency audit
[✓] P8 Exemplar/template conformance (SAMPLE-01)
[✓] P9 Packaging and conformance matrix
[✓] P10 Write validation_report.md and .json
Thought: 323ms
Final answer. Mention verdict, counts, top blockers, reports paths, no source edits/commits, ask to proceed with P0 fixes. Keep tight.
Validation complete. Reports written to docs/validation_report.md and docs/validation_report.json.
Verdict: not promotable to Verified. The v2 security fixes are real (code-execution, empty-suite, textless-PDF, overwrite, unrequested-commit all closed), but the promotion gate fails:
- High V-1: lint_skill.py scans itself → exit 1 (lint_skill.py:18 allowlist omits itself), so test_lint_passes_package fails (29 passed, 1 failed).
- Medium V-3: six regression tests named in v1_to_v2_updates.md don't exist.
- Medium V-4: safe_expr has no matrix/factorial size caps (eye(1000), zeros(2000,2000), factorial(200000) accepted).
- 10 Low incl. wrong PART 5 commands (# expect PASS, ../../samples/...), --pages abc traceback, incomplete SKILL.md tree, dropped playbook checks, exemplar provenance over-claim.
- V-9 refuted; V-2 accepted by design.
No skill source files changed, nothing committed. Want me to apply the P0 fix (lint self-scan + green pytest) and then the doc corrections?
▣  Build · DeepSeek V4.1 Flash Free · 9m 2s
please meticulously plan to apply targeted fixes for High to Medium severity findings after re-validation
Thought: 20.1s
The user wants a meticulous plan to apply targeted fixes for High to Medium severity findings after re-validation. So they want a plan (not implementation yet). Per AGENTS.md: ANALYZE → PLAN → VALIDATE → IMPLEMENT. They said "please meticulously plan to apply targeted fixes ... after re-validation". So produce a detailed plan, with exact edits, acceptance criteria, ordering, verification commands, risk. Then ask for approval (VALIDATE checkpoint). Don't edit files yet.

Findings High to Medium: V-1 (High), V-3 (Medium), V-4 (Medium). Also external SAMPLE-01 was Low; PDF-02 Low. So only V-1, V-3, V-4 are in scope. But "after re-validation" means plan should include re-validation gates after fixes. Possibly include medium external? All external medium are closed. So scope = V-1, V-3, V-4.

Need to be meticulous: exact files, exact lines, proposed code changes, test additions, commands, acceptance, rollback, risks, what not to touch (Low findings). Also consider whether fixing V-1 via skipping self is correct vs moving BANNED patterns out. Need analyze trade-offs:

V-1 fix options:
A. Skip self in scan (if p.name == Path(__file__).name: continue). Simple, preserves ban list. But a future banned pattern could be added to lint_skill.py unnoticed; that's acceptable because the linter legitimately contains those tokens. Risk: bypass is name-based; if script renamed, breaks. Use p.resolve() == Path(__file__).resolve().
B. Move BANNED patterns to a separate data file (e.g., JSON) so lint_skill.py contains no literal banned tokens; then no skip. More robust but adds a file and read logic; changes packaging/tree. Also eval( etc. might still appear in comments? Move to JSON with escaped strings. More complexity, not needed.
C. Build patterns programmatically ("sym"+"pify(") to avoid literals — hacky, hurts readability.
Recommend A with resolve() and a comment? AGENTS says no comments unless asked; but a brief comment explaining why skip is justified is useful. However "DO NOT ADD ANY COMMENTS unless asked" — avoid comment, or use a constant name SELF = Path(__file__).resolve() and clear code. Could add no comment.

Need inspect lint_skill.py fully to plan exact edit. I have lines 12-40 and know structure; need the scanning loop and return. Let me read full file (48? now 78+ lines per diff, maybe 106). Read it.

V-3 fix: add six tests. Need to inspect test_cli.py to match style/helpers. Read full test_cli.py and test_safe_expr.py. Then design tests:
- test_force_overwrites: run extract twice, second exit 2, third with --force exit 0. Existing test_textless? There may already be helper. 
- test_report_truncation_notice: needs a long report > REPORT_CHARS (4000?) to trigger truncation. Could monkeypatch? Better unit-test the formatting function if exists; else generate PDF? Hard. Inspect extract_pdf for truncation logic/function. If inline, refactor minimally to a function emit_report? That's a code change beyond tests. Alternatively test via a fake report string by calling a helper. Need read full extract_pdf.py.
- test_interval_complex_errors: suite with interval expr I -> exit 1, ERROR row. Easy.
- test_timeout_fails_closed: run_check with tiny timeout -> ERROR. Import check_math. Easy.
- test_provenance_present: run check_math on example, assert "checks_sha256=" and "sympy=" in stdout. Easy.
- test_lint_requires_authorisation_gate: assert "explicit authorisation" (or phrase) in SKILL.md and that G6 contains it. Easy static test.

V-4 fix: add caps in safe_expr. Need design:
- Matrix constructors: Matrix, diag, eye, zeros, ones. Cap rows/cols <= e.g. 64 and total elements <= 4096. But Matrix receives list of lists; diag receives args; eye(n); zeros(r,c). Wrapping each in a validation function.
- factorial/binomial/gamma: cap argument <= 10_000? factorial(200000) took 0.46s and huge int; cap at 10_000 (fast). binomial(n,k) cap n <= 10_000. gamma cap arg <= 10_000.
- integrate/limit/solve: these are the heaviest. Options: remove entirely, or cap? Hard to bound. Since checks for A-level rarely need symbolic integrate/limit/solve; but could be needed. Target fix for Medium: remove integrate, limit, solve from FUNCS, or gate behind explicit allow_heavy flag in suite schema? Simpler: remove and document; but this may break legitimate checks. Alternative: keep but enforce a much shorter timeout for heavy funcs? Timeout is per-check already; SIGALRM works (E12). The OOM risk is matrix allocation, not CPU. For CPU-heavy integrate/limit/solve, timeout handles. So V-4 remediation could be: cap matrix dims + factorial/binomial/gamma; keep integrate/limit/solve under timeout, document. But static finding says no argument cap for them; a plan can justify keeping because timeout covers CPU and no unbounded memory? integrate can allocate huge expressions. Hmm.

Meticulous plan should present options and recommend:
- Caps: MAX_MATRIX_DIM=64, MAX_MATRIX_ELEMS=4096, MAX_INT_ARG=10_000.
- Wrap constructors and factorial/binomial/gamma.
- Keep integrate/limit/solve but add a per-call complexity guard? Not feasible. Recommend keep with documented timeout + trust model, OR remove. I'd recommend keep but document, because removal is a behavioural regression and Medium finding's core is memory blowup via matrix/factorial. However user asked targeted fixes for High-Medium; leaving part of V-4 open may not satisfy. Better: implement caps + remove integrate, limit, solve from whitelist? That's a functional change. A-level further maths checks might use solve for roots; but discriminant and algebra suffice. Hmm.

Alternative: keep solve/integrate/limit but wrap with a pre-check on argument count/size? No.

Could add MAX_NODES already 600; expression size bounded. The cost is internal algorithm, not input size. Timeout covers CPU; memory can still blow. Risk acceptance: document that heavy symbolic ops are timeout-bounded but memory is not fully bounded; treat as trusted input. But then V-4 not fully closed.

Targeted fix to close V-4 robustly: remove the three heavy funcs. But that could break existing checks? Search checks.example.json: uses re, discriminant, asin, sqrt, Rational. No integrate/limit/solve. Tests? test_safe_expr may test allowed funcs; inspect. If none use them, removal is safe for current suite. But skill guidance may tell agents to use solve. Check references for solve( / integrate( usage. If docs mention them, update docs too (but that's beyond High-Medium? still part of fix).

Maybe better: keep integrate, limit, solve but require they appear only in suites marked "trusted": true? Adds schema complexity. Overkill.

Let me inspect code/tests/docs for usage before deciding. Read lint_skill.py full, extract_pdf.py full (truncation/report), test_cli.py full, test_safe_expr.py full, and grep for integrate/limit/solve/solve( in references/assets/tests. Then plan.

Also "after re-validation" could mean: re-run validation after fixes, and only then claim closure. Plan should include a re-validation phase with same E1–E14 probes, plus regression checks, and update validation_report (or write addendum). Should we update the report? Yes, after fixes, update statuses and hashes (new hashes). That's part of plan: regenerate hashes, update report ledger/verdict, re-run E1/E2/E7/E10/E11/E13, ensure Low findings untouched.

Also need to consider docs corrections? User said High to Medium only. V-13 is Low but it's the doc that says expect PASS; after fixing V-1, PART 5 becomes true (lint PASS, pytest all pass) except sample path is still wrong (Low V-13). Hmm, after V-1 fix, # expect PASS becomes true; # expect all pass true; ../../samples still wrong. So PART 5 partially true. Since V-13 is Low, out of scope, but the plan should note that the doc's sample path remains wrong (Low) and is not addressed, or optionally include it as a one-line drive-by? User said targeted High-Medium; avoid scope creep. But leaving a known wrong command after "re-validation" could confuse. Mention as explicitly out of scope, recommend separate Low batch.

Also V-12 tree omission Low; V-6 Low; V-7 Low; V-8 Low; V-10/V-11 Low; S-1 Low; V-14 Low; V-5 Low. Out of scope.

Need to decide whether adding tests for timeout requires importing check_math; test_cli currently may use subprocess only. Read.

Let me read files.
Before proposing edits, I need the exact current code paths for the three in-scope findings (V-1 High, V-3/V-4 Medium).
$ cd /home/pete/.pi/agent/skills/solving-a-level-exam-papers && echo "===== lint_skill.py ====="; nl -ba scripts/lint_skill.py; echo "===== extract_pdf.py (report/truncation) ====="; nl -ba scripts/extract_pdf.py | sed -n '1,20p;95,190p'
===== lint_skill.py =====
     1	#!/usr/bin/env python3
     2	"""Validate skill structure, frontmatter, links, and script safety patterns."""
     3	from __future__ import annotations
     4	import re, sys
     5	from pathlib import Path
     6	
     7	NAME_RX = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
     8	REQUIRED = [
     9	    "references/source-fidelity.md", "references/exam-presentation.md",
…
Click to expand
Thought: 4.4s
V-1 fix: skip self. Line 55-57. Change:
for script in (root / "scripts").glob("*.py"):
    if script.name in ALLOWED_BANNED or script.resolve() == Path(__file__).resolve():
        continue
But ALLOWED_BANNED={"safe_expr.py"} comment says "contains none of these" which is now false? safe_expr contains "eval("? No, AST evaluator named _ev; no eval(. It contains "exec("? no. It contains __import__? no. Actually safe_expr doesn't contain banned tokens; the allowlist comment says "interpreter module: contains none of these" — if it contains none, why allowlist? Maybe because it contains strings like "eval" in docstring? Let me grep. Anyway. The self file must contain them. Use script.resolve() == SELF with SELF = Path(__file__).resolve().

Better design: SELF = Path(__file__).resolve() near top; loop skip if script.resolve() in {SELF} or name in ALLOWED_BANNED. Clean.

Test for V-1: existing test_lint_passes_package will pass. Do we add an explicit test that linter ignores itself but still flags a planted banned token? That would strengthen. But V-3 list includes test_lint_requires_authorisation_gate, not self-skip. Existing test covers PASS. Optionally add test_lint_flags_banned_token_in_other_script to prevent over-broad skip. This is good regression: create temp copy? test_cli probably builds temp skill. Read tests.

V-3 tests: need inspect test_cli.py helpers.

V-4: implement caps. Need inspect safe_expr full to wrap functions. Read safe_expr.py fully. Also grep docs for integrate/limit/solve usage.

Let me read test_cli.py, test_safe_expr.py, safe_expr.py, and grep.
$ cd /home/pete/.pi/agent/skills/solving-a-level-exam-papers && echo "===== test_cli.py ====="; nl -ba tests/test_cli.py; echo "===== test_safe_expr.py ====="; nl -ba tests/test_safe_expr.py
===== test_cli.py =====
     1	import json, subprocess, sys
     2	from pathlib import Path
     3	import pytest
     4	
     5	ROOT = Path(__file__).resolve().parents[1]
     6	SCRIPTS = ROOT / "scripts"
     7	EXAMPLE = json.loads((ROOT / "assets" / "checks.example.json").read_text())
     8	
     9	
…
Click to expand
Thought: 17.1s
Interesting: test_no_overwrite_then_force already covers force (so V-3's "test_force_overwrites" is semantically covered, just differently named). test_textless_pdf_exit3 covers. test_example_suite_passes covers provenance. test_injection covers. So V-3 missing named tests: truncation, interval complex, timeout, lint auth gate. And force/provenance are covered by different names. Plan should acknowledge that, and add only genuinely missing ones (4), while maybe renaming/adding aliases? Don't add duplicate tests. Meticulous: map claims to existing coverage; add 4 tests, not 6; note two claims are covered under different names (so doc claim about names is still wrong, but coverage exists). That reduces unnecessary tests (simplicity). But user asked targeted fixes; adding 4 tests is right.

Wait: test_lint_requires_authorisation_gate is missing; lint itself checks "explicit authorisation" line 69-70, so a test can assert lint rejects a SKILL.md lacking the phrase. That requires building a temp skill copy. Could be a unit test on a temp dir with minimal SKILL.md and required files? Lint requires all REQUIRED files; building temp fixture with all files is heavy. Simpler: assert "explicit authorisation" in (ROOT/"SKILL.md").read_text().lower() — tests the content, not the linter gate. Better: create a temp copy of the skill (shutil.copytree) excluding pycache, mutate SKILL.md to remove phrase, run lint -> exit 1 with message. That's robust and matches name. Cost: copying ~1.2MB sample? copytree includes samples (1.1MB) fine, but tests dir too. Could copy only required files? Lint needs references/assets/scripts/tests; copy whole ROOT except .git/pycache. Simpler: shutil.copytree(ROOT, tmp/"skill", ignore=shutil.ignore_patterns("__pycache__")); 1.2MB, fine. Then replace phrase. Run lint -> 1. Good.

- test_report_truncation_notice: Need >40 lines. Could use a synthetic PDF with many flags? Hard. Better unit-test by importing extract_pdf and calling a helper. Currently truncation is inline lines 123-127. To test without refactor, generate a PDF with many pages? 40+ pages blank -> all NO_TEXT, lines = 1 + 40*? Each page 1 line, flags 0 -> 41 lines > 40; truncation notice triggers. But blank PDF generator makes 1 page. Could generate 45 blank pages by parameterizing blank_pdf. But then no flags; lines = 1 + 45 = 46 > 40 -> notice. That tests truncation. Feasible: extend blank_pdf(path, pages=1) to build N pages. But that's a test-only change; PDF object structure needs kids list. More code. Alternatively generate a PDF with one page containing 60 lines of math-ish text to create flags; requires text content stream with font — harder.

Simplest robust: refactor the report rendering into a pure function render_report(src_name, digest, pages, out, cap=STDOUT_LINE_CAP) -> tuple[list[str], int] or format_report(...) returning (shown, truncated_count). Then test the function directly with synthetic pages. But that's a production code refactor for testability; acceptable and small. However "surgical changes" — adding a function is okay but touches script. Alternative: test via CLI with 45-page blank PDF. That avoids production refactor, but test helper complexity. Which is more meticulous?

A 45-page blank PDF: build catalog/pages with kids array of page objects, each with empty content stream. blank_pdf can be generalized. Lint lines: 1 header + 45 page lines = 46; shown 40; truncated 6. Assert "[OUTPUT TRUNCATED" and "manifest.json" in stdout. Exit 3 (all NO_TEXT). Good. No production change. I prefer this: test-only, no refactor.

But note: --out writes pages.txt/manifest; fine.

- test_interval_complex_errors: suite with 2 checks: base equal + interval expr "I" (or "sqrt(-1)") -> exit 1, "ERROR" in stdout. Easy.

- test_timeout_fails_closed: subprocess CLI with --timeout 0.001 and a check simplify((x+1)**80). Is --timeout a CLI option? Check check_math argparse. I know run_check takes timeout; CLI likely --timeout. Verify. If not, unit import. Let me check check_math CLI lines ~200. Also simplify((x+1)**80) may complete before 1ms? Parsing itself >1ms, so alarm fires. But alarm starts before parse? In run_check, signal.alarm(int(timeout)) where timeout float 0.001 -> int=0 -> alarm(0) cancels! Important: if code does signal.alarm(int(timeout)), 0.001 -> 0 -> no alarm. Need inspect. If it uses signal.setitimer or ceil. E12 used run_check timeout=0.001 and got timeout, so implementation handles float (maybe setitimer). Let me read run_check. If CLI --timeout default 20 int, passing 0.001 maybe type float. Need confirm.

- test_provenance_present already covered by test_example_suite_passes (checks_sha256=). No new test needed; maybe rename? Don't duplicate.
- test_force_overwrites covered by test_no_overwrite_then_force. No new test.
So add 4 tests: truncation, interval complex, timeout, lint auth gate. Update doc claim names to match actual test names (V-13 Low doc, but doc correction is Low; however to make V-3 closure honest, either add tests with claimed names or correct doc). Since V-3 is Medium and about false claims, the fix can be: add the 4 missing behaviours under the exact claimed names, and rename existing two? Renaming tests to match doc is churn. Better: add 4 named tests + correct the doc list to actual names (6 behaviours, 6 tests, names differ for 2). But doc correction is Low V-13; still part of V-3 closure. Plan: add 4 tests with claimed names where missing; for the 2 covered, either add thin aliases (duplicative) or update doc. Choose update doc (no duplicate tests), and note V-3 closes as "all six behaviours tested; two under existing names; doc list corrected."

V-4 design details. Read safe_expr fully and check_math CLI timeout. Also grep docs for funcs.
$ cd /home/pete/.pi/agent/skills/solving-a-level-exam-papers && echo "===== safe_expr.py ====="; nl -ba scripts/safe_expr.py; echo "===== check_math CLI/run_check ====="; nl -ba scripts/check_math.py | sed -n '24,120p;190,260p'
===== safe_expr.py =====
     1	"""Whitelisted AST interpreter for check expressions. No eval/exec/sympify.
     2	
     3	Threat model: checks.json is authored from PDF/user text, which is untrusted.
     4	Only the node types, names and functions below can ever be evaluated.
     5	"""
     6	from __future__ import annotations
     7	import ast
     8	import sympy as sp
     9	
…
Click to expand
Thought: 2.6s
run_check uses setitimer float; good. But note: run_check catches UnsafeExpression before generic; V-10 is in safe_expr's exponent check, separate. Also ConfigError subclass ValueError; except ConfigError first. Good.

Timeout: setitimer then never cancelled on success? Let me see rest (lines 120-190) — likely finally signal.setitimer(0). Need check. If not, alarm may fire during next check; but probably cancelled. Read 120-200.

Also --timeout CLI? Read 190-260 output was blank because file shorter? Let me read 120-200.
$ cd /home/pete/.pi/agent/skills/solving-a-level-exam-papers && nl -ba scripts/check_math.py | sed -n '120,210p'; echo "--- grep heavy funcs in docs/tests/assets ---"; grep -rnE '\b(integrate|limit|solve|eye|zeros|ones|diag|factorial|binomial|gamma)\s*\(' references assets tests SKILL.md | grep -v 'checks.example.json'
120	                "role": c.get("role", "-"), "status": "ERROR", "detail": str(exc)}
   121	    finally:
   122	        if hasattr(signal, "SIGALRM"):
   123	            signal.setitimer(signal.ITIMER_REAL, 0)
   124	
   125	
   126	def main() -> int:
   127	    ap = argparse.ArgumentParser()
   128	    ap.add_argument("checks")
   129	    ap.add_argument("--min-checks", type=int, default=MIN_CHECKS_FLOOR)
…
Click to expand
Thought: 1m 34s
No docs/tests use heavy funcs. So removing integrate/limit/solve is low-risk for current package; but the skill's tool-safety may say whitelist includes them. Let me check tool-safety content for function list. Earlier read but not exact. grep "solve" docs. The grep above covered references, assets, tests, SKILL.md, and found nothing. So no doc mentions them. Good.

But removing integrate, limit, solve reduces capability for checks like "verify integral" or "solve polynomial". For A-level, solve could be useful for roots; but discriminant/factor cover. integrate could verify a definite integral exactly. Removing may be a functional regression. Alternative: keep but bound by a much shorter "heavy" timeout? The per-check timeout already applies. The Medium finding is memory DoS via matrix dims primarily; integrate/limit/solve CPU is bounded by timeout, though memory not. Meticulous approach: quantify and choose.

Could implement a two-tier: cap matrix/factorial (memory), and for integrate/limit/solve, wrap with a complexity guard? Not possible. Could keep them but document that heavy symbolic ops are timeout-bounded and checks are trusted-ish. But threat model says checks authored from PDF/user text = untrusted. Then keeping integrate with no cap is a residual Medium. To close Medium, remove or gate.

Gate option: add suite-level "allow_heavy": true (default false), and only register heavy funcs if allow_heavy. That preserves capability for trusted suites while defaulting untrusted to safe. But schema change + docs + tests. More work, but principled. However targeted fix for Medium; is this over-engineering? AGENTS says simplicity first. 

Simpler: remove integrate, limit, solve from FUNCS. If a check needs them, the user can compute externally and assert equality. The skill is about verifying answers, not performing heavy symbolic integration. diff remains (cheap-ish, can also blow up but less). factor/simplify can also be expensive on large expressions but MAX_NODES/CHARS bound input; expansion blowup possible (e.g., expand((x+1)*1000) but MAX_POW=1000 allows; could allocate huge). Hmm, expand((x+1)**500) creates 501 terms, fine; *1000 -> 1001 terms. Bounded by MAX_POW. simplify on 600 nodes could be slow but timeout.

Memory blowup vectors: Matrix dims (unbounded), factorial/binomial (unbounded output size), gamma (unbounded), 2**1000 bounded by MAX_POW but 2**1000 is 300 digits fine; 1000**1000 3000 digits fine. factorial(10**9) would OOM. So caps on factorial/binomial/gamma + matrix dims are the key. integrate/limit/solve are CPU not memory primarily. Timeout handles CPU (verified). So targeted V-4 fix: caps for memory vectors; keep integrate/limit/solve with timeout; explicitly document residual "CPU-bound heavy functions are timeout-bounded; memory is bounded by caps". That closes the Medium (memory DoS) while acknowledging CPU residual covered by timeout. But the finding text says "no argument cap for integrate/limit/solve" — we can state timeout is the control, tested. Is that acceptable? The user wants targeted fixes for Medium; a defensible closure matrix can say "memory vectors capped; CPU vectors timeout-bounded (E12); documented". 

However integrate can create enormous expressions consuming memory before timeout alarm is delivered (C-level). Sympy integrate is Python-level mostly, signals can interrupt Python bytecode, so timeout works. GMP allocation for factorial is C-level; cap solves. Matrix allocation is C-level; cap solves. Good reasoning: keep heavy funcs because timeout demonstrably interrupts Python-level sympy work; cap the C-level allocation vectors. This is precise and avoids functionality loss.

Caps design:
- MAX_MATRIX_DIM = 64 (64x64 = 4096 entries).
- MAX_MATRIX_ELEMS = 4096 (redundant with dim cap but for diag/Matrix nested).
- MAX_INT_ARG = 10_000 for factorial/binomial/gamma.
Implement wrappers:

def _check_matrix(m):
    m = sp.Matrix(m)
    if m.rows > MAX_MATRIX_DIM or m.cols > MAX_MATRIX_DIM:
        raise UnsafeExpression(...)
    return m
But eye(100000) allocates before wrapper sees it. Need wrap constructors to validate args before calling:
def _eye(rows, cols=None):
    rows = int(rows); cols = int(cols) if cols is not None else rows
    _check_dims(rows, cols)
    return sp.eye(rows, cols)
Similarly zeros/ones. diag(*args) — args already evaluated; a huge diag would require huge list which is bounded by MAX_NODES/CHARS (600 nodes => max ~600 args), fine; but elements could be matrices? diag with matrices; each matrix capped by Matrix wrapper. Could still cap total. Simpler wrap _diag(*args) and check len(args)<=MAX_MATRIX_DIM and total elements. Matrix gets a list of lists already evaluated; nested list length bounded by nodes; but Matrix([[0]*100000]) list comprehension? No comprehensions allowed; literal 100k elements exceeds MAX_NODES. So Matrix literal is bounded by 600 nodes -> ~300 elements. Still cap dims for safety. zeros(2000,2000) needs pre-check. eye(100000) pre-check.

factorial: pre-check arg before call. _int_arg(name, n, cap): require integer, 0 <= n <= cap. factorial of negative? sympy handles; cap abs. binomial(n,k): cap n and k. gamma: cap arg; gamma of huge rational? cap numeric abs <= MAX_INT_ARG.

Use wrappers in FUNCS:
"Matrix": _matrix, "diag": _diag, "eye": _eye, "zeros": _zeros, "ones": _ones,
"factorial": _factorial, "binomial": _binomial, "gamma": _gamma,
Need wrappers accept *args; Matrix can be Matrix(rows, cols, flatlist) too. Handle generically: if 3 args (rows, cols, data) validate dims. But Matrix([[..]]) one arg. Implement:

def _matrix(*args):
    if len(args) == 1:
        m = sp.Matrix(args[0])
    elif len(args) == 3:
        r, c = int(args[0]), int(args[1])
        _check_dims(r, c)
        m = sp.Matrix(r, c, args[2])
    else:
        raise UnsafeExpression("Matrix expects 1 or 3 arguments")
    _check_dims(m.rows, m.cols)
    return m
Careful: int(args0) on sympy Integer works; on Symbol raises TypeError -> catch -> UnsafeExpression. Use helper _dim.

_diag(*args): if any arg is Matrix/list, total; simpler: m = sp.diag(*args) then cap dims; but allocation of diag from 600 args is at most 600x600 = 360k entries (~3MB) okay, but cap after; could allocate 600x600 acceptable. Actually 600 args each scalar -> 600x600 dense = 360k, fine. If args are 64x64 matrices, 600 of them -> huge; but Matrix wrapper caps each at 64x64, diag of 600 blocks = 38400x38400 -> OOM before post-check. Need pre-check block count. _diag: if len(args) > MAX_MATRIX_DIM: reject; compute total dims by summing matrix sizes/lists; if total > MAX_MATRIX_DIM reject before sp.diag. Implement.

_eye(rows, cols=None), _zeros, _ones pre-check.

_factorial(n): _bounded_int(n); call sp.factorial.
_binomial(n,k): both bounded.
_gamma(z): require z.is_number and abs(float(N(z))) <= MAX_INT_ARG; else reject. But gamma(Rational(1,2)) fine. If symbolic -> reject (gamma with symbol could be heavy). This is stricter but okay.

Constants: MAX_MATRIX_DIM=64, MAX_INT_ARG=10_000.

Also fix V-10 while touching safe_expr? It's Low, out of scope. But it's a one-line reorder in the same block; targeted High-Medium only. Avoid scope creep? The plan can mention optional low-severity drive-by but recommend separate. User explicitly said High to Medium; so exclude.

Tests for V-4: add to test_safe_expr.py:
- reject eye(100000), zeros(106, 1), factorial(200000), binomial(200000, 100000), gamma(106), Matrix 1000x1000? Matrix([[0]*1000]) too many nodes; use eye(65) and zeros(65,65) reject at boundary; accept eye(64).
- diag of 65 args reject; diag 64 accept.
- boundary: factorial(10000) accept? 10000! ~35660 digits, fast (~ms). Test accept maybe slow-ish but fine; or test 1000 accept.
- Ensure existing payloads still rejected.
- Ensure existing example still passes (no heavy funcs).

Need ensure caps don't break checks.example.json (uses re, discriminant, asin, sqrt, Rational) — fine.

V-1 test: existing test_lint_passes_package; add test_lint_still_flags_other_scripts to ensure self-skip isn't overbroad. Build temp copy, inject eval( into a copy of extract_pdf.py? Simpler: copy ROOT to tmp (ignore pycache), append \n# eval(\n to scripts/extract_pdf.py, run lint -> exit 1 and "unsafe pattern" in stdout. That's a strong regression. But copying 1.2MB sample; okay. Alternatively create minimal temp skill with required files stubs and one script containing token; but lint also checks template sections/auth/tests. Easier copytree. Add helper copy_skill(tmp_path).

However test runtime increases; acceptable.

V-3 tests:
1. test_interval_complex_errors — CLI, exit 1, "ERROR" in stdout.
2. test_timeout_fails_closed — CLI --timeout 0.001 with a check expression; need suite with >=2 checks and original-condition. Use base equal 1=1 plus a zero check simplify((x+1)**80); assert exit 1 and "time limit exceeded" in stdout. But run_check timeout 0.001: first check also under 1ms? 1=1 fast but setitimer 1ms; could time out the first check randomly -> still exit 1 and message, test passes but not specifically second. Better order: heavy first? Then first check may timeout; still message. Assert message, not which. Flaky? 1ms is tiny; even trivial parse may exceed 1ms, so test reliably errors. But could the process set alarm before parse and signal arrives during json load? Alarm set inside run_check after validate; fine. Use --timeout 0.01 and expression integrate(exp(x**2), (x, 0, 1))? Might finish <10ms. Use simplify((x+1)**200) with timeout 0.001; parsing 200-node expr >1ms likely. E12 proved run_check 0.001 with *80 times out. Use same expression *80. CLI adds process startup but alarm starts after. Good. Assert "per-check time limit exceeded" in stdout (detail printed in ledger). The row status ERROR and detail string appears in ledger? Ledger only prints status, not detail! Ledger columns: id, note, kind, role, result — no detail. So "time limit exceeded" won't appear in stdout unless JSON output. Use --json and read results detail. Or assert exit 1 and "ERROR" in stdout. To specifically prove timeout, use --json out.json and assert detail contains "time limit exceeded". Good.
3. test_report_truncation_notice — 45-page blank PDF, assert "[OUTPUT TRUNCATED" in stdout and "manifest.json" in that notice. Need generalize blank_pdf to n pages. Implement blank_pdf(path, pages=1) building Kids refs and page objects. Careful with object numbering. Simpler: generate 45 separate one-page PDFs? No, one PDF.
   Build:
   - obj1 Catalog -> Pages 2 0 R
   - obj2 Pages -> Kids 3 0 R 5 0 R ... Count N
   - for each page i: page obj, contents obj (empty stream). Objects 3,4 for page1; 5,6 page2...
   - xref accordingly.
   Rewrite blank_pdf to generic. Existing test uses blank_pdf(pdf) default 1 -> still works.
4. test_lint_requires_authorisation_gate — copy skill, remove "explicit authorisation" and "explicit authorization" from SKILL.md (case-insensitive). Use regex replace phrase. Run lint -> exit 1, message "must gate git delivery" in stdout. But removing phrase might break nothing else. Implement replace via re.sub(r"(?i)explicit authori[sz]ation", "approval", text).
   Copy skill includes tests; lint only checks presence. Fine.

test_provenance_present and test_force_overwrites: already covered; update doc list to actual names. Alternatively add aliases with exact names that call existing logic? Duplicative. Plan: doc correction.

But wait: user asked High-Medium fixes; V-3 includes "six tests named in docs don't exist". Fixing by adding 4 + correcting doc for 2 is legitimate. But doc correction also touches Low V-13. It's required to close V-3 honestly. Fine.

Also after V-1 fix, test_lint_passes_package passes. After adding tests, total 34.

Now re-validation plan:
Phase R: re-run E1-E14, plus new tests, plus caps probes, plus full pytest. Update validation_report.md/json:
- new hashes for changed files.
- V-1/V-3/V-4 status Closed; summary counts High 0, Medium 0, Low 10.
- verdict: promotable? If all gates green and Medium closed, yes "Verified" subject to external unverified notes. But be careful: conformance matrix "pytest green" now PASS; lint PASS; V-6 etc. remain Low open. Verdict could be "PASS WITH LOW RESIDUALS" / promotable with known Low debt. 
- Add "revalidation" section with commands/results.
- Do not alter Low findings statuses.
- Update docs/v1_to_v2_updates.md PART 5/6? That's V-13 Low but after fixes PART 5 becomes mostly true except sample path. If we don't fix, re-validation report still flags. Since the goal is promotion, leaving a wrong sample path in the promotion doc undermines "Verified". Hmm. The user said High to Medium; but V-13 is Low and a one-line path fix. Meticulous plan can include an explicit "adjacent one-line doc correction required for consistency" as a dependency of V-3 closure? Actually V-3 closure involves correcting test names in that doc; while editing, fixing sample path is trivial. But scope discipline says only requested severities. Yet the doc correction for test names is in the same file; leaving a known wrong path is odd. I'll propose it as an optional "in-scope doc touch" clearly marked, and ask approval. Since user said "targeted fixes for High to Medium", I should keep optional items separate and not silently include. Plan lists "Out of scope (not doing)" including V-13 except the test-name list needed for V-3; but if we touch the test list, we might as well fix path. Hmm.

Better: V-3 fix = add 4 tests; do NOT edit docs (the doc claim about six names remains a Low doc issue V-13). But then V-3 "six tests named don't exist" still partially true (2 exist under other names, 4 now exist with claimed names). After adding 4, all six claimed behaviours are tested, but only 4 carry claimed names. Is V-3 closed? The finding is "six regression tests named in v2 docs do not exist". Strictly, 2 still don't exist by name. To close, either add 2 aliases or fix doc. Adding 2 thin aliases is duplicative; fixing doc is right. So V-3 closure necessarily includes a doc edit (test list). That doc edit is part of Medium fix, not Low scope creep. Then sample path remains; mention.

Maybe rename existing tests to claimed names instead of aliases:
- test_no_overwrite_then_force -> test_force_overwrites (it covers both no-overwrite and force; name narrower but okay)
- test_example_suite_passes -> test_provenance_present? It covers 7/7 + provenance; losing "example passes" name. Could split: keep example test, add separate test_provenance_present asserting sha/sympy; cheap. That's 5 new tests. Hmm.
Simplest: add 4 missing + add test_provenance_present (small, distinct) + rename force test to test_force_overwrites (or add alias). Then all six names exist. But force test also asserts no-overwrite; renaming loses that signal. Add a separate test_force_overwrites that does the force leg, and keep existing? Duplicate setup. Alternatively rename to test_no_overwrite_then_force_overwrites — doesn't match claim exactly.

Doc correction is cleaner: change PART 3 list to actual test names and coverage mapping. I'll plan that. Then V-3 closes by coverage + accurate doc. Good.

But the user asked "targeted fixes for High to Medium severity findings" — doc test-name correction is part of V-3; acceptable.

Now, V-1 fix also makes PART 5 # expect PASS true. V-3 doc correction fixes test list. Sample path remains wrong (V-13). We'll note as out-of-scope residual; or include a one-line path correction as "required for the promotion block to be executable" — I'd include it because the re-validation acceptance uses the corrected command block; but that's Low. Let me ask via question? The instructions say ask one question at a time, but we need approval of plan. Could present plan with a "Decision needed" item: include the one-line sample-path fix (Low, adjacent) or leave it. Use question tool? The user asked to plan; better present plan and ask for approval, including the optional item. No need for question tool; end with explicit approval request.

Also V-4 caps: need decide exact constants. 64 dims, 10k int arg. Justify: checks.example matrices none; 64 is plenty for exam checks. 10k! is 35660 digits, computes in ~ms; acceptable. factorial(200000) 0.46s and ~1MB; cap 10k.

Test runtime for factorial(10000) maybe ~10ms. Fine.

Implement wrappers carefully with no comments (AGENTS). But docstrings? Existing file has docstrings; adding function names is enough. No comments.

Potential issue: sp.eye(rows, cols) accepts None; wrapper signature def _eye(rows, cols=None). _dim(v):
def _dim(v, name):
    if not isinstance(v, (int, sp.Integer)):
        raise UnsafeExpression(f"{name} must be an integer")
    n = int(v)
    if n < 0 or n > MAX_MATRIX_DIM:
        raise UnsafeExpression(f"{name} exceeds {MAX_MATRIX_DIM}")
    return n
But _ev converts int constants to sp.Integer; fine. isinstance(sp.Integer(3), int) false, so include sp.Integer. Also sympy Float 3.0? reject (good).

_zeros(rows, cols=None): cols default rows; validate both.
_ones same.
_eye same.
_matrix(*args):
- 1 arg: if list of lists; sp.Matrix may raise; validate resulting dims.
- 3 args: validate dims before construct.
_diag(*args):
- if len(args) > MAX_MATRIX_DIM: reject (a 64x64 block max 64 blocks).
- compute total = 0; for a in args: if Matrix/list -> rows/cols; if list -> (len, len of first?) diag treats list as block? sp.diag(*1,2) diagonal scalars. If arg is list, sp.diag flattens? Simpler: construct with sp.diag then check dims; but allocation risk from 64 blocks each 64x64 = 4096x4096 16M entries 128MB — risky but bounded-ish. Pre-check block count and total: treat list/Matrix as block size; scalar as 1. total += size. if total > MAX_MATRIX_DIM reject. Then construct.
- For a list arg of length L, block size L (diag(list) gives LxL). For Matrix, rows (assume square? diag accepts rectangular? use rows+cols maybe). Use max(rows, cols) conservatively.

_factorial(n): _int_arg(n); if n<0 reject? sympy factorial(-1) is zoo/complex; reject negative.
_binomial(n,k): both ints >=0, n<=MAX_INT_ARG, k<=n? binomial allows k>n -> 0; allow k<=MAX_INT_ARG.
_gamma(z): if not z.is_number: reject; try val=abs(float(sp.N(z))); except -> reject; if val>MAX_INT_ARG: reject. But gamma(10000) huge; cap 10000 still huge (factorial 9999) but same as factorial cap; okay. Maybe cap gamma at 1000 to be safe; but consistency 10k. gamma(10000) ~ 10^35659, fine memory. Use MAX_INT_ARG.
- Also factorial of Rational? reject non-integer.

Where to place wrappers: after CONSTS/BINOPS or before FUNCS? FUNCS defined at 17, wrappers need MAX constants and UnsafeExpression. Define constants at 10, helper functions before FUNCS, then reference. Or define FUNCS after wrappers. Cleanest: move FUNCS below helper defs; but that's a bigger diff. Could define wrappers above FUNCS (after class), then FUNCS. That reorders. Or define FUNCS with lambdas calling helpers defined later? Python resolves at call time, so helpers can be defined after FUNCS as long as module fully loaded before parse called. _ev called after import, so names resolved then. We can keep FUNCS at 17 referencing _matrix etc., and define helpers after FUNCS (before _ev). That works and is minimal diff: change 8 entries + insert helper block after FUNCS. But readability: forward references okay in Python.

Alternatively insert helpers before FUNCS and shift. Plan can say "insert helpers between CONSTS and _ev; point FUNCS entries at them". Since FUNCS is above CONSTS, forward refs needed. Fine.

Also det/inv/transpose wrap sp.Matrix(m) on an already-created matrix; no new allocation beyond inverse; inv of 64x64 could be expensive but timeout. inv of symbolic 64x64 could blow memory; cap dims already. Could also cap det/inv input dims to 64 (already matrix created <=64). If user passes list literal <=600 nodes ~300 elements (17x17) okay.

Now, what about Matrix with 1 arg and huge nested list? Node cap 600 limits elements ~300; fine.

Tests for caps:
@pytest.mark.parametrize("src", ["eye(65)", "zeros(65,65)", "ones(65,1)", "factorial(10001)", "binomial(10001,2)", "gamma(10001)", "diag(*[1]*65)"])
But diag(*[1]*65) uses starred arg -> rejected earlier ("starred arguments forbidden"), not cap. To test diag cap, need 65 positional args literal: diag(1,1,...65 times); build string programmatically. Could skip diag test or use diag(eye(64), eye(64)) -> total 128 >64 reject; both eye(64) allowed individually. That tests diag total cap. Good.
Accept tests: eye(64), zeros(64,64) maybe heavy 4096 entries fine; factorial(1000); binomial(1000,2); gamma(100); diag(1,2,3).

Need ensure eye(64) accepted and type Matrix; test shape.

V-1 regression test test_lint_still_flags_other_scripts: copytree, append eval( to extract_pdf.py, run lint -> 1, "unsafe pattern" in stdout. But eval( appended as a bare line is syntax-invalid; lint doesn't compile, just string scan, so fine. Use \n# eval(\n to keep valid-ish. Good.

Copy helper:
def copy_skill(tmp_path):
    dst = tmp_path / "skill"
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns("__pycache__"))
    return dst
Need import shutil, re.

test_lint_requires_authorisation_gate:
dst = copy_skill(tmp_path)
p = dst/"SKILL.md"; t=p.read_text()
p.write_text(re.sub(r"(?i)explicit authori[sz]ation", "approval", t))
r = run("lint_skill.py", dst)
assert r.returncode == 1 and "must gate git delivery" in r.stdout
But lint checks root.name equals frontmatter name. dst name "skill" != "solving-a-level-exam-papers" -> adds name mismatch error too, still exit 1 and message present. Fine, but test could fail if message absent? It's present. To avoid confusion, name dst = ROOT.name: dst = tmp_path / ROOT.name. Do that in copy helper.

test_report_truncation_notice: generalize blank_pdf. Let me design object numbering:
def blank_pdf(path, pages=1):
    kids = " ".join(f"{3+2*i} 0 R" for i in range(pages))
    objs = [
      b"<</Type/Catalog/Pages 2 0 R>>",
      f"<</Type/Pages/Kids[{kids}]/Count {pages}>>".encode(),
    ]
    for i in range(pages):
        objs.append(f"<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]/Resources<<>>/Contents {4+2*i} 0 R>>".encode())
        objs.append(b"<</Length 0>>stream\nendstream\n")
    ...
Object i numbering: obj1 catalog, obj2 pages, page objs 3,5,7..., contents 4,6,8... For i=0: page obj3 contents4; i=1: page5 contents6. kids uses 3+2*i. Correct.
Then write xref as before. offsets appended in order 1..len(objs). Good.

Test:
pdf=tmp_path/"many.pdf"; blank_pdf(pdf, 45)
r=run("extract_pdf.py", pdf, "--out", tmp_path/"o")
assert r.returncode == 3
assert "[OUTPUT TRUNCATED" in r.stdout
Line count: 1 header + 45 page lines = 46; cap 40; truncated 6. Yes. But each page line may add flags; blank text none. Good. Note --render not used.

test_interval_complex_errors:
spec = {"symbols":["x"],"checks":[
 {"id":"O",... equal lhs 1 rhs 1},
 {"id":"C","role":"domain","kind":"interval","note":"complex","expr":"I","lo":"0","hi":"1"}]}
r=run("check_math.py", suite(...)); assert r.returncode==1 and "| C |" in r.stdout and "ERROR" in r.stdout
Careful ledger line format | C | complex | interval | domain | ERROR |. Assert "ERROR" in stdout.

test_timeout_fails_closed:
spec = base + {"id":"T","role":"sanity","kind":"zero","note":"slow","expr":"simplify((x+1)**80)"}
out=tmp_path/"r.json"
r=run("check_math.py", suite(...), "--timeout","0.001","--json",out)
assert r.returncode==1
data=json.loads(out.read_text())
assert any(x["status"]=="ERROR" and "time limit" in x["detail"] for x in data["results"])
But base equal check might also timeout; then both ERROR; assertion still finds T? If alarm fires during first check, T never runs? rows list comprehension: first check raises _Timeout caught -> ERROR row; alarm cancelled; second runs, likely also times out. T likely ERROR with message. But if alarm fires during O, then for T setitimer 0.001 again; fine. Assert any result detail contains "time limit". Could pass even if T passed? If T completes <1ms? *80 simplify unlikely <1ms. To be safer use integrate(exp(x**2), (x, 0, 100))? Might be fast. Use simplify((x+1)**400) — node count 400 <600, pow 400<1000; parsing/simplify >1ms. Use 400. But E12 80 worked. Use *300.
Also ensure --timeout 0.001 accepted (0 < 0.001 <=120). Yes.
Potential flakiness: machine very fast; 1ms is still tiny for sympy import? Import happens before main; alarm starts in run_check. Parsing 300-node AST + sympy simplify >1ms reliably. Good.

test_provenance_present: existing test asserts checks_sha256. To satisfy name, either add:
def test_provenance_present(tmp_path):
    r=run("check_math.py", suite(tmp_path, EXAMPLE))
    assert "checks_sha256=" in r.stdout and "sympy=" in r.stdout
Cheap, distinct. Add it. Then only test_force_overwrites name missing; rename existing test_no_overwrite_then_force? Add separate force test duplicates setup. Better rename to test_force_overwrites and keep assertions; name slightly narrows but covers. Or add alias function calling existing? Pytest functions can't easily call with tmp_path. Rename is fine; it still tests no-overwrite+force. Doc list then exact six names exist. That avoids doc edit for names. But V-13 doc still has sample path wrong; out of scope. And no doc test-list edit needed. Good: add 5 tests (truncation, interval, timeout, lint auth, provenance) + rename 1 = six names. Wait existing force test covers provenance? no. Existing example test covers provenance but name differs; add provenance test. Total new tests: 5, rename 1. Test count 29+5=34 (rename doesn't add). V-3 closed by name + behaviour.

Hmm, but adding test_provenance_present duplicates part of test_example_suite_passes; minor duplication acceptable for claim traceability. Could instead rename example test to test_provenance_present and lose 7/7 assertion name; keep both is fine.

V-4 tests add ~8 parametrized cases; total ~42.

Now V-1 fix + tests: lint will scan test files? No, only scripts/*.py. Good. But test_lint_still_flags_other_scripts appends eval( to a copy; lint's BANNED scan catches; no self issue.

One more: lint ALLOWED_BANNED comment says safe_expr contains none; if safe_expr contains "eval("? grep. grep -n 'eval(' safe_expr.py maybe in docstring "No eval/exec/sympify." — that's "eval/" not "eval(". exec(? docstring "eval/exec/sympify" no paren. So it contains none, making allowlist unnecessary. Could remove ALLOWED_BANNED entirely and rely on self-skip. But leaving it harmless. V-1 plan: add SELF skip; optionally simplify ALLOWED_BANNED? Don't touch unrelated.

Wait: if safe_expr contains none, why allowlist? Maybe to allow future. Leave.

Now scope/risk:
- Modifying scripts changes hashes; update report.
- No behaviour change to example suite.
- Caps may reject legitimate large matrices; document in tool-safety? That's a doc change. Since V-4 fix changes contract, update references/tool-safety.md to state caps. Is tool-safety in scope? It's part of V-4 remediation (document limits). Add one line to "Rules" listing caps. That's a targeted doc change for Medium. Good. Also SKILL.md tool safety summary? It points to reference; no need.
- Tests require sympy/pdfplumber via uv; existing pattern.

Re-validation:
1. python3 scripts/lint_skill.py . -> 0.
2. uv run --with pytest --with sympy --with pdfplumber pytest -q tests/ -> all pass (34? count).
3. check_math example -> 7/7.
4. caps probes -> reject.
5. extract run1/2/3 -> 0/2/0; --pages abc still 1 (Low, out of scope) — re-validation should note unchanged Low.
6. Update report hashes/statuses; add revalidation section; verdict "PASS (High/Medium closed; Low residuals tracked)".
7. Do not commit.

Acceptance criteria explicit:
- V-1: lint exit 0; test_lint_passes_package passes; injected banned token still caught.
- V-3: six named tests exist and pass; full suite green.
- V-4: eye(65), zeros(65,65), factorial(10001), binomial(10001,2), gamma(10001), diag(eye(64),eye(64)) rejected; eye(64), factorial(1000) accepted; example suite unchanged 7/7.

Risk table:
- Over-broad self-skip -> regression test.
- Caps break legitimate checks -> boundary tests + example; document.
- Timeout test flakiness -> use JSON detail and 1ms; if flaky, use monkeypatch/unit? Alternative deterministic: import check_math and call run_check with timeout=1e-9? setitimer minimum resolution; 1e-9 may fire immediately; same. Could unit-test _alarm directly? That only tests raising. CLI test with **300 should be stable.
- Copytree tests slow (~1.2MB) x2; acceptable. Could ignore samples to speed: ignore_patterns("pycache","samples") — lint doesn't require samples. Do that! Then copy is small. Use ignore=("pycache","samples","docs")? lint requires docs? No. tests? lint checks tests/*.py exists; copy tests. Keep tests. Ignore samples/docs to speed. Good.
- Test report truncation 45-page PDF may be slow (~0.2s); fine.

Now, the plan must be presented, then ask for explicit approval (VALIDATE). No edits yet. The user said "please meticulously plan"; so do not implement. Provide plan with phases, file-by-file diffs (described), acceptance, re-validation, risks, out-of-scope, and approval question.

Need also mention estimated effort? AGENTS wants effort/timeline. Provide rough: ~1-2 hours, 6 files + tests + report.

File change list:
1. scripts/lint_skill.py — SELF skip.
2. scripts/safe_expr.py — caps/wrappers.
3. tests/test_safe_expr.py — cap tests.
4. tests/test_cli.py — 5 tests + rename + blank_pdf pages.
5. references/tool-safety.md — document caps (one paragraph/table row).
6. docs/validation_report.md/.json — post-fix update (statuses, hashes, revalidation).
Maybe docs/v1_to_v2_updates.md? Only if renaming tests changes claimed names? We're making names exist, so no doc edit needed. But PART 5 sample path remains wrong (Low). Out of scope. PART 5 # expect PASS becomes true. Good. PART 6 "Linter would PASS" becomes true. So V-13 partially self-heals; sample path remains. Mention.

Wait: test names claimed: test_lint_requires_authorisation_gate (add), test_report_truncation_notice (add), test_interval_complex_errors (add), test_timeout_fails_closed (add), test_provenance_present (add), test_force_overwrites (rename). All six exist. Great, no doc edit for V-3.

But test_lint_requires_authorisation_gate tests lint gate, not SKILL content; good.

test_report_truncation_notice tests stdout truncation, not report file; good.

Now V-4 doc: tool-safety currently says? Need read to place edit accurately. I read earlier but not exact. Let me read tool-safety.md fully (28 lines). Also check SKILL.md tool safety summary line ~? It says "full: references/tool-safety.md". A one-line update in tool-safety "Rules" is enough. Read it before final plan? I can include "add a Limits row" without exact line. Better read to be precise. Also need ensure no contradiction: tool-safety might say "no arbitrary large matrices" already. Let me read.
$ cd /home/pete/.pi/agent/skills/solving-a-level-exam-papers && nl -ba references/tool-safety.md
1	# Tool safety
     2	
     3	## Untrusted input
     4	PDF text, user pastes and model output are **data, never code**. A paper can
     5	carry an injection payload that an agent might copy into `checks.json`.
     6	
     7	## Rules
     8	1. Never call `sympify`, `parse_expr`, `eval`, `exec`, `os.system` or
     9	   `subprocess(..., shell=True)` on such strings. Use `scripts/safe_expr.py`.
    10	2. The interpreter whitelists AST nodes, names and functions; it rejects
…
Click to expand
Thought: 30.7s
Add rule 2 extension: "and caps matrix dimensions and integer-function arguments". Or new rule 7. Minimal: amend rule 2 sentence: "...oversized input, oversized matrices and factorial/binomial/gamma arguments." Good.

Also note rule 5 says "content-hash run directories" but default is content-hash dir out/{stem}-{digest8}; yes.

Now plan. Need be meticulous but concise. Use headings, tables, code snippets. Present exact edits (diff-like), acceptance commands. Then ask approval.

Also mention "after re-validation": Phase 5 re-run all probes and update report; Phase 6 deliver summary. Don't commit.

Potential subtlety: test_lint_requires_authorisation_gate copies skill and removes phrase; lint also checks name matches dir; helper names dir ROOT.name so pass; only auth error. Good. Ignore samples/docs for speed. But lint REQUIRED includes scripts/tests/references/assets; all copied. Good. shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns("__pycache__","samples","docs")) — dst parent tmp; dst name ROOT.name. Good.

test_lint_still_flags_other_scripts: append # eval( to dst/scripts/extract_pdf.py; lint scans all scripts except safe_expr and self; catches. Assert exit 1 + "unsafe pattern" + "extract_pdf.py".

One issue: lint self-skip using Path(__file__).resolve(); when running copied lint from dst, __file__ is dst/scripts/lint_skill.py; skips copied self; good.

V-4 wrappers and test specifics. Provide code sketch:

MAX_MATRIX_DIM, MAX_INT_ARG = 64, 10_000

def _int(v, name, cap):
    if not isinstance(v, (int, sp.Integer)):
        raise UnsafeExpression(f"{name} must be an integer")
    n = int(v)
    if n < 0 or n > cap:
        raise UnsafeExpression(f"{name} must be in 0..{cap}")
    return n

def _dims(rows, cols):
    if rows > MAX_MATRIX_DIM or cols > MAX_MATRIX_DIM:
        raise UnsafeExpression(f"matrix dimensions exceed {MAX_MATRIX_DIM}")
    return rows, cols

def _eye(rows, cols=None):
    r = _int(rows, "eye rows", MAX_MATRIX_DIM)
    c = _int(cols if cols is not None else r, "eye cols", MAX_MATRIX_DIM)
    return sp.eye(r, c)
...
def _matrix(*args):
    if len(args) == 1:
        m = sp.Matrix(args[0])
    elif len(args) == 3:
        r = _int(args[0], "Matrix rows", MAX_MATRIX_DIM)
        c = _int(args[1], "Matrix cols", MAX_MATRIX_DIM)
        m = sp.Matrix(r, c, args[2])
    else:
        raise UnsafeExpression("Matrix expects 1 or 3 arguments")
    _dims(m.rows, m.cols)
    return m
_dims returns tuple unused; fine. _diag:
def _diag(*args):
    if len(args) > MAX_MATRIX_DIM:
        raise UnsafeExpression(...)
    total = 0
    for a in args:
        if isinstance(a, sp.MatrixBase):
            total += max(a.rows, a.cols)
        elif isinstance(a, list):
            total += len(a)
        else:
            total += 1
    if total > MAX_MATRIX_DIM:
        raise UnsafeExpression(...)
    return sp.diag(*args)
Need sp.MatrixBase exists. Or hasattr(a, "rows"). Use getattr(a,"rows",None). Simpler:
r = getattr(a, "rows", None)
total += max(r, getattr(a,"cols",r)) if r else (len(a) if isinstance(a,list) else 1)
Fine.

_factorial(n): _int(n,"factorial",MAX_INT_ARG) then sp.factorial.
_binomial(n,k): both cap.
_gamma(z): 
if not getattr(z, "is_number", False):
    raise UnsafeExpression("gamma requires a numeric argument")
try:
    mag = abs(float(sp.N(z)))
except (TypeError, ValueError, OverflowError):
    raise UnsafeExpression("gamma argument is not finite") from None
if mag > MAX_INT_ARG: raise ...
return sp.gamma(z)
But gamma(10001) rejected; gamma(10000) allowed. Fine.

FUNCS entries updated. Forward refs: helpers defined after FUNCS but before parse; okay. To avoid confusion, place helpers between FUNCS and CONSTS? FUNCS references names at call time, so fine. But _gamma uses sp.N; okay.

Tests:
@pytest.mark.parametrize("src", [
 "eye(65)", "zeros(65,65)", "ones(65,1)",
 "factorial(10001)", "binomial(10001,2)", "gamma(10001)",
 "diag(eye(64), eye(64))",
])
def test_oversized_rejected(src): raises
diag(eye(64), eye(64)): each eye allowed; total 128 >64 -> reject. But eye(64) constructs 4096 entries twice; fine.
Accept:
@pytest.mark.parametrize("src", ["eye(64)","zeros(64,64)","factorial(1000)","binomial(1000,2)","gamma(100)","diag(1,2,3)"])
def test_limits_allow_small(src): parse(...) no raise
zeros(64,64) 4096; fine.

Wait: _int rejects sp.Float; eye(64.0) rejected; good.

Potential: binomial(10001,2) pre-check n cap -> reject before compute. Good.

Now test_cli changes:
- imports add re, shutil.
- blank_pdf(path, pages=1) generic.
- rename test_no_overwrite_then_force -> test_force_overwrites.
- add copy_skill.
- add 5 tests.
- provenance test duplicates; okay.

Count: existing 12 tests +5 =17 test functions; parametrized safe_expr adds 7+6=13 cases + existing 16 cases? Fine.

Re-validation acceptance commands:
python3 scripts/lint_skill.py .                     # PASS, 0
uv run --with pytest --with sympy --with pdfplumber pytest -q tests/  # all pass
uv run --with sympy python scripts/check_math.py assets/checks.example.json  # 7/7, 0
uv run --with sympy python - <<... caps probe ...   # rejects/accepts
uv run --with pdfplumber python scripts/extract_pdf.py samples/... --out /tmp/r1  # 0
... /tmp/r1 again # 2 ; --force # 0
Then update report with new hashes and statuses; add §9 re-validation.

Do we update docs/validation_report.* hashes for changed files and add revalidatedAt? Yes.

Risk: changing safe_expr may break checks.example.json? No heavy funcs; verify.
Risk: MAX_MATRIX_DIM name collision none.
Risk: gamma symbolic checks (e.g., gamma(x)) now rejected; was allowed. This is a behavioural restriction; document in tool-safety. A-level checks unlikely. Mention.

Out of scope: V-5..V-14, S-1, PDF-02 residual, V-13 sample path, V-8 --pages traceback, V-10 message, V-11 exit semantics. Note that after V-1 fix, PART 5 # expect PASS becomes true; sample path remains wrong (Low). Also note lint still scans scripts for eval(; tests aren't scanned (test files contain eval( payload strings? test_cli has "eval('1+1')" in test_safe_expr payloads, but lint only scripts/*.py, so fine).

Wait: test_safe_expr.py contains "eval('1+1')" string; not scanned. Fine.

One more: after V-1 self-skip, does lint still catch BANNED tokens in check_math.py? check_math imports parse, no banned. extract_pdf no. Good.

Could instead add lint_skill.py to ALLOWED_BANNED set: {"safe_expr.py", "lint_skill.py"} — simplest one-line. But name-based skip is less robust than resolve; still fine. Which is more meticulous? ALLOWED_BANNED = {"safe_expr.py", "lint_skill.py"} is a one-line change, but semantically the linter file is exempt because it defines the patterns; comment can explain. Using resolve self-skip is clearer intent. I'll recommend SELF skip + keep allowlist. Exact:
SELF = Path(__file__).resolve()
...
for script in (root / "scripts").glob("*.py"):
    if script.name in ALLOWED_BANNED or script.resolve() == SELF:
        continue
Add SELF after imports or near constants. Minimal.

Test test_lint_still_flags_other_scripts ensures not overbroad.

Now, should we include an explicit test that lint passes after self-skip? Existing. Good.

Plan approval question at end: "Approve this plan (P0/P1/P2) and the one-line tool-safety doc update? I will not touch Low findings or commit." Maybe offer options: approve all, approve code only, adjust caps. Use question tool? The instructions say use question tool for choices. But the user asked for a plan; a simple ask is fine. Could use question with options: "Approve plan", "Approve code-only (skip doc)", "Change caps", "Hold". But question tool is available and suited. However final answer should be concise; a plan is long. Use question tool at end? The system says when asking questions, ask one at a time. The question tool can ask one. But the user may prefer text. I'll end with a direct approval request; no tool needed. Yet "VALIDATE" phase requires explicit confirmation. A question tool would formalize. But it may be overkill; still, user asked plan, so present and ask.

Need ensure not to implement. No edits.

Let me write the plan in markdown. Keep under ~150 lines. Include "What I will not touch".

Detailed phases:
- Phase 0: baseline freeze (already have hashes; re-confirm clean; snapshot new hashes after).
- Phase 1: V-1.
- Phase 2: V-3.
- Phase 3: V-4.
- Phase 4: docs (tool-safety + validation report).
- Phase 5: re-validation gate.
- Phase 6: handoff.

Include exact acceptance and rollback (git diff / restore; no commit).

Effort estimate: ~90–120 min.

Potential issue: user said "after re-validation" — maybe they mean apply fixes only after re-validating? We already validated. Interpret as "plan fixes, then re-validate after". State assumption explicitly: "I read this as: apply fixes, then re-run the full validation gate; if you meant re-validate first, say so." Good—surface ambiguity (AGENTS).

Also mention no network beyond uv cached; tests use uv.

Let me draft.

Need to be careful with "Medium" scope: V-4 residual heavy funcs. Explain decision: cap memory-allocation vectors; keep integrate/limit/solve under per-check timeout (verified E12), document. This closes the memory-DoS Medium; CPU is bounded by timeout. If they want absolute removal, option B. Present as a decision point? Meticulous plan should present trade-off. Maybe recommend A (caps + timeout + doc), note B (remove heavy funcs) if strict. Ask approval for A. This is a real design choice. Include "Decision A (recommended) vs B".

Similarly V-3: add 5 + rename vs add 6 aliases; recommend add 5 + rename.

Now write final response. Ensure concise but complete. Use tables. No emojis.

One more check: test_timeout_fails_closed with --timeout 0.001 and expression simplify((x+1)**300): node count? AST for (x+1)**300: ~6 nodes, fine; MAX_POW 300. Sympy simplify of expanded? It will expand power? simplify((x+1)**300) may be quick (already power form) ~ms. Parsing + simplify likely >1ms. To guarantee, use expand((x+1)**300)? expand creates 301 terms, >1ms; but expression expand((x+1)**300); parse builds Pow then expand; >1ms. Use expand((x+1)**300). Or factor(2**300 - 1)? factor could be slower. Use simplify((x+1)**300) maybe sympy keeps; expand definitely work. But timeout may fire during parse before expand; still ERROR. Good. Test asserts any ERROR detail "time limit". Use expand((x+1)**300).

But expand of **300 creates 301 terms, memory trivial. 1ms alarm likely fires during parse/AST or expand. Reliable.

Alternatively call run_check directly with timeout=0.001 in a unit test (no subprocess), but then no CLI fail-closed proof. CLI is better.

--json path: parent tmp exists; atomic write. Good.

test_report_truncation_notice blank 45 pages: blank_pdf xref offsets; ensure Contents object numbering matches. Write carefully in implementation, not plan.

Also note test runtime: copytree twice ignoring samples/docs; fine.

Now final.
Interpretation
I read “after re-validation” as: apply the fixes, then re-run the full validation gate and update the report — not “re-validate before planning”. If you meant the latter, stop me.
Scope is strictly High + Medium: V-1 (High), V-3 (Medium), V-4 (Medium). No Low findings, no commits.
Phase 0 — Baseline freeze (5 min)
- Record current hashes for every file I will touch; confirm git status --porcelain -- skills/solving-a-level-exam-papers is empty.
- Work on main; no branch, no commit. Rollback = restore the six files from the recorded hashes / git checkout -- <file>.
Phase 1 — V-1 High: linter self-scan (10 min)
File: scripts/lint_skill.py
Edit 1 — add after imports:
SELF = Path(__file__).resolve()
Edit 2 — line 56:
if script.name in ALLOWED_BANNED or script.resolve() == SELF:
    continue
Rationale: the linter must contain the literal banned tokens it searches for; exempt only itself, by resolved path (not name), and keep scanning every other script.
Acceptance
- python3 scripts/lint_skill.py . → exit 0, PASS.
- pytest -q tests/test_cli.py::test_lint_passes_package → pass.
- New guard test: inject eval( into a copied extract_pdf.py; lint must still exit 1 and name that file. This prevents an over-broad skip.
Phase 2 — V-3 Medium: make the six claimed tests real (30 min)
File: tests/test_cli.py (plus shutil, re imports)
Add five tests with the exact claimed names, and rename one existing test:
Claimed name	Action	Behaviour asserted
test_lint_requires_authorisation_gate	add	copy skill, strip “explicit authorisation/authorization” from SKILL.md; lint exits 1 with “must gate git delivery”
test_report_truncation_notice	add	45-page blank PDF → [OUTPUT TRUNCATED and manifest.json in stdout; exit 3
test_interval_complex_errors	add	interval expr: "I" → row ERROR, suite exit 1
test_timeout_fails_closed	add	--timeout 0.001 + expand((x+1)**300), --json → exit 1 and a result with time limit exceeded
test_provenance_present	add	example suite stdout contains checks_sha256= and sympy=
test_force_overwrites	rename test_no_overwrite_then_force	existing no-overwrite + --force assertions unchanged
Supporting test-only changes:
- Generalise blank_pdf(path, pages=1) to build N page/content object pairs and a matching Kids array.
- Add copy_skill(tmp_path) using shutil.copytree(ROOT, tmp_path / ROOT.name, ignore=shutil.ignore_patterns("__pycache__", "samples", "docs")) so the linter-gate tests stay fast.
No duplicate force test; no production refactor for truncation.
Acceptance: all six names exist and pass; pytest -q tests/ green.
Phase 3 — V-4 Medium: bound memory-allocation vectors (35 min)
File: scripts/safe_expr.py
Design choice (recommended A): cap the C-level allocation vectors; keep integrate/limit/solve but rely on the per-check SIGALRM timeout (already verified: E12). This closes the memory-DoS path without removing legitimate symbolic capability. Option B (stricter) is to delete integrate/limit/solve entirely; I recommend A unless you want maximum restriction.
Constants
MAX_MATRIX_DIM, MAX_INT_ARG = 64, 10_000
Wrappers (validate before allocation; point FUNCS at them):
- _int(v, name, cap) — accepts only int/sp.Integer, 0 <= v <= cap; else UnsafeExpression.
- _eye, _zeros, _ones — validate rows/cols before sp.eye/zeros/ones.
- _matrix(*args) — 1-arg form constructs then checks dims; 3-arg (rows, cols, data) validates dims first.
- _diag(*args) — reject >64 blocks; sum block sizes (Matrix rows/cols, list length, scalar 1) and reject total >64 before sp.diag.
- _factorial, _binomial, _gamma — cap arguments at 10_000; gamma requires a numeric argument and finite magnitude.
File: references/tool-safety.md — extend rule 2 with: “caps matrix dimensions (64) and factorial/binomial/gamma arguments (10 000); heavy symbolic functions remain per-check timeout-bounded.”
Tests: tests/test_safe_expr.py
- Reject: eye(65), zeros(65,65), ones(65,1), factorial(10001), binomial(10001,2), gamma(10001), diag(eye(64), eye(64)).
- Accept: eye(64), zeros(64,64), factorial(1000), binomial(1000,2), gamma(100), diag(1,2,3).
- Existing injection/whitelist payloads and assets/checks.example.json must be unchanged.
Acceptance: all cap tests pass; example suite still 7/7, exit 0.
Phase 4 — Re-validation gate (25 min)
Run exactly these, in order:
python3 scripts/lint_skill.py .                                              # 0, PASS
uv run --with pytest --with sympy --with pdfplumber pytest -q tests/         # all pass
uv run --with sympy python scripts/check_math.py assets/checks.example.json  # 7/7, 0
uv run --with pdfplumber python scripts/extract_pdf.py \
  samples/2026_Prelim_P1.pdf --out /tmp/rv1                                  # 0
# same --out again                                                           # 2 (by design)
# same --force                                                               # 0
Then re-run the bounded probes: eye(65) rejected, eye(64) accepted, factorial(10001) rejected, timeout still yields ERROR, --pages abc still tracebacks (Low, unchanged and disclosed).
Update deliverables
- docs/validation_report.md / .json: new SHA-256s; V-1, V-3, V-4 → Closed; summary becomes 0 High / 0 Medium / 10 Low open; add a “Re-validation” section with commands and results; verdict changes to “PASS — High/Medium closed; Low residuals tracked.”
- Do not mark any Low finding closed.
What I will not touch
V-5–V-14, S-1, PDF-02 residual, V-13’s ../../samples/... path, V-8’s --pages traceback, V-10’s message, V-11’s exit semantics. After V-1 the PART 5 # expect PASS claim becomes true; its sample path remains wrong and stays a tracked Low.
Risks and mitigations
Risk	Mitigation
Self-skip is too broad	injected-token regression test
Caps break a legitimate check	boundary accept/reject tests + example suite
Timeout test flaky	1 ms + expand((x+1)**300), assert via JSON detail
Copytree tests slow	ignore samples/, docs/, __pycache__
Report/hashes drift	regenerate hashes immediately after edits; update both reports
Estimated effort: 90–120 minutes. Files changed: 6 (lint_skill.py, safe_expr.py, test_cli.py, test_safe_expr.py, tool-safety.md, validation_report.{md,json}).
Approve this plan (including Option A for V-4 and the one-paragraph tool-safety.md update)?
▣  Build · DeepSeek V4.1 Flash Free · 5m 4s
Approve
Thought: 50.7s
User approved. Now implement per plan. Need to follow meticulously, verify. Let's set todos. Then edit files.

Files:
1. scripts/lint_skill.py — add SELF, skip.
2. tests/test_cli.py — imports re/shutil, blank_pdf pages, rename force test, add 5 tests + copy_skill.
3. scripts/safe_expr.py — caps/wrappers.
4. tests/test_safe_expr.py — cap tests.
5. references/tool-safety.md — rule 2 extension.
6. docs/validation_report.md/.json — update after revalidation with hashes/statuses.

Let's implement carefully.

First read full files again? We have them. Need exact edits.

1. lint_skill.py

Add SELF = Path(__file__).resolve() after ALLOWED_BANNED. Then line 56 condition.

2. safe_expr.py

Current FUNCS lines 17-35. Need wrappers. Plan:

Add constants line 10: MAX_CHARS, MAX_NODES, MAX_POW = 2000, 600, 1000 -> add MAX_MATRIX_DIM, MAX_INT_ARG = 64, 10_000.

Define helpers. Where? After CONSTS/BINOPS? FUNCS references helper names at call time, so can define helpers after FUNCS. But for readability, define helpers before FUNCS. That requires moving FUNCS down or inserting helpers above FUNCS (after class). Let's insert helpers after class UnsafeExpression (line 13-14) and before FUNCS. They use sp, UnsafeExpression, MAX constants. Then FUNCS uses them.

Helper code:

def _int(v, name, cap):
    if not isinstance(v, (int, sp.Integer)):
        raise UnsafeExpression(f"{name} must be an integer")
    n = int(v)
    if n < 0 or n > cap:
        raise UnsafeExpression(f"{name} must be in 0..{cap}")
    return n


def _dims(rows, cols):
    if rows > MAX_MATRIX_DIM or cols > MAX_MATRIX_DIM:
        raise UnsafeExpression(f"matrix dimensions exceed {MAX_MATRIX_DIM}")
    return rows, cols


def _eye(rows, cols=None):
    r = _int(rows, "eye rows", MAX_MATRIX_DIM)
    c = _int(cols if cols is not None else r, "eye cols", MAX_MATRIX_DIM)
    return sp.eye(r, c)


def _zeros(rows, cols=None):
    r = _int(rows, "zeros rows", MAX_MATRIX_DIM)
    c = _int(cols if cols is not None else r, "zeros cols", MAX_MATRIX_DIM)
    return sp.zeros(r, c)


def _ones(rows, cols=None):
    r = _int(rows, "ones rows", MAX_MATRIX_DIM)
    c = _int(cols if cols is not None else r, "ones cols", MAX_MATRIX_DIM)
    return sp.ones(r, c)


def _matrix(*args):
    if len(args) == 1:
        m = sp.Matrix(args[0])
    elif len(args) == 3:
        r = _int(args[0], "Matrix rows", MAX_MATRIX_DIM)
        c = _int(args[1], "Matrix cols", MAX_MATRIX_DIM)
        m = sp.Matrix(r, c, args[2])
    else:
        raise UnsafeExpression("Matrix expects 1 or 3 arguments")
    _dims(m.rows, m.cols)
    return m


def _diag(*args):
    if len(args) > MAX_MATRIX_DIM:
        raise UnsafeExpression(f"diag exceeds {MAX_MATRIX_DIM} blocks")
    total = 0
    for a in args:
        rows = getattr(a, "rows", None)
        if rows is not None:
            total += max(rows, getattr(a, "cols", rows))
        elif isinstance(a, list):
            total += len(a)
        else:
            total += 1
    if total > MAX_MATRIX_DIM:
        raise UnsafeExpression(f"diag dimensions exceed {MAX_MATRIX_DIM}")
    return sp.diag(*args)


def _factorial(n):
    return sp.factorial(_int(n, "factorial", MAX_INT_ARG))


def _binomial(n, k):
    return sp.binomial(_int(n, "binomial n", MAX_INT_ARG),
                       _int(k, "binomial k", MAX_INT_ARG))


def _gamma(z):
    if not getattr(z, "is_number", False):
        raise UnsafeExpression("gamma requires a numeric argument")
    try:
        mag = abs(float(sp.N(z)))
    except (TypeError, ValueError, OverflowError):
        raise UnsafeExpression("gamma argument is not finite") from None
    if mag > MAX_INT_ARG:
        raise UnsafeExpression(f"gamma argument exceeds {MAX_INT_ARG}")
    return sp.gamma(z)

Potential issue: _matrix with 1 arg that is a list of lists containing >64 rows: sp.Matrix constructs (bounded by nodes), then _dims rejects. Fine. sp.Matrix(args[0]) where args0 is a scalar? sp.Matrix(1) creates 1x1; fine.
_diag: sp.diag(*args) with a list arg: diag(1,2) gives 2x2; total len 2. Good. With Matrix 64x64 twice -> total 128 reject.
_int rejects bool? bool is int subclass; bool constants are rejected earlier in _ev (isinstance(node.value, bool)), but sympy True can't be produced. Fine. Could exclude bool explicitly: isinstance(v, bool) reject; not necessary.
_gamma: sp.N(z) for huge integer e.g. gamma(109): is_number true, float(N(109)) fine, mag 1e9 > 10k reject before gamma. Good. For gamma(10001) reject. For gamma(10000) allowed but huge output (~10^35659), fine memory.
sp.N(z) for complex z=I: mag 1, gamma(I) computes; allowed. Fine.
sp.gamma(Rational(1,2)) fine.

FUNCS entries:
- "Matrix": _matrix, "diag": _diag, "eye": eye, "zeros": zeros, "ones": _ones
- "factorial": _factorial, "binomial": binomial, "gamma": gamma
Keep det/inv/transpose lambdas (they construct from existing matrix; no size growth beyond dims).
Keep integrate/limit/solve.

One concern: eye(64) allocates 4096 entries; fine. zeros(64,64) fine.

Also fix V-10? Out of scope. Don't.

3. tests/test_safe_expr.py

Add constants import? No. Add tests after existing.

@pytest.mark.parametrize("src", [
    "eye(65)", "zeros(65,65)", "ones(65,1)",
    "factorial(10001)", "binomial(10001,2)", "gamma(10001)",
    "diag(eye(64), eye(64))",
])
def test_oversized_allocations_rejected(src):
    with pytest.raises(UnsafeExpression):
        parse(src, symbols=("x",))


@pytest.mark.parametrize("src", [
    "eye(64)", "zeros(64,64)", "ones(64,1)",
    "factorial(1000)", "binomial(1000,2)", "gamma(100)",
    "diag(1,2,3)",
])
def test_bounded_allocations_allowed(src):
    parse(src, symbols=("x",))

diag(eye(64), eye(64)): parse args: eye(64) allowed; diag total 128 -> reject. Good. But note eye(64) constructed twice before diag check; 8192 entries, fine.

ones(65,1) reject; accept ones(64,1).
gamma(10001) reject; gamma(100) accept.
factorial(1000) ~2568 digits fast.
binomial(1000,2) fast.
zeros(64,64) fast.

Could test Matrix([[1,2],[3,4]]) still accepted? Existing? Not explicitly; add to allowed maybe. Not necessary but good: "Matrix([[1,2],[3,4]])". Add.
Reject Matrix 65 rows: string with 65 rows would exceed? Matrix([[1]]*65) not allowed (mult). Use eye(65) covers.

4. tests/test_cli.py

Imports: import json, re, shutil, subprocess, sys.

Add:
def copy_skill(tmp_path):
    dst = tmp_path / ROOT.name
    shutil.copytree(ROOT, dst,
                    ignore=shutil.ignore_patterns("__pycache__", "samples", "docs"))
    return dst

blank_pdf generic. Replace lines 88-102.

New blank_pdf:
def blank_pdf(path, pages=1):
    kids = " ".join(f"{3 + 2 * i} 0 R" for i in range(pages))
    objs = [b"<</Type/Catalog/Pages 2 0 R>>",
            f"<</Type/Pages/Kids[{kids}]/Count {pages}>>".encode()]
    for i in range(pages):
        objs.append(f"<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]/Resources<<>>/Contents {4 + 2 * i} 0 R>>".encode())
        objs.append(b"<</Length 0>>stream\nendstream\n")
    out, offsets = bytearray(b"%PDF-1.4\n"), []
    for i, body in enumerate(objs, 1):
        offsets.append(len(out))
        out += f"{i} 0 obj".encode() + body + b"endobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs)+1}\n".encode() + b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += f"trailer<</Size {len(objs)+1}/Root 1 0 R>>\nstartxref\n{xref}\n%%EOF\n".encode()
    path.write_bytes(bytes(out))

Check object numbering: objs list index 1-based:
1 catalog, 2 pages, i=0 page obj3 contents obj4; i=1 page obj5 contents obj6. Kids 3,5,7... correct. Contents {4+2*i} correct.

Rename test:
def test_no_overwrite_then_force(tmp_path): -> def test_force_overwrites(tmp_path):

Add new tests after force test:

def test_provenance_present(tmp_path):
    pytest.importorskip("sympy")
    r = run("check_math.py", suite(tmp_path, EXAMPLE))
    assert r.returncode == 0
    assert "checks_sha256=" in r.stdout and "sympy=" in r.stdout


def test_interval_complex_errors(tmp_path):
    pytest.importorskip("sympy")
    spec = {"symbols": ["x"], "checks": [
        {"id": "O", "role": "original-condition", "kind": "equal",
         "note": "1 = 1", "lhs": "1", "rhs": "1"},
        {"id": "C", "role": "domain", "kind": "interval",
         "note": "complex value", "expr": "I", "lo": "0", "hi": "1"},
    ]}
    r = run("check_math.py", suite(tmp_path, spec))
    assert r.returncode == 1 and "| C |" in r.stdout and "ERROR" in r.stdout


def test_timeout_fails_closed(tmp_path):
    pytest.importorskip("sympy")
    spec = {"symbols": ["x"], "checks": [
        {"id": "O", "role": "original-condition", "kind": "equal",
         "note": "1 = 1", "lhs": "1", "rhs": "1"},
        {"id": "T", "role": "sanity", "kind": "zero",
         "note": "slow expression", "expr": "expand((x+1)**300)"},
    ]}
    out = tmp_path / "results.json"
    r = run("check_math.py", suite(tmp_path, spec), "--timeout", "0.001", "--json", out)
    assert r.returncode == 1
    results = json.loads(out.read_text())["results"]
    assert any(x["status"] == "ERROR" and "time limit" in x["detail"] for x in results)


def test_report_truncation_notice(tmp_path):
    pytest.importorskip("pdfplumber")
    pdf = tmp_path / "many.pdf"
    blank_pdf(pdf, pages=45)
    r = run("extract_pdf.py", pdf, "--out", tmp_path / "o")
    assert r.returncode == 3
    assert "[OUTPUT TRUNCATED" in r.stdout and "manifest.json" in r.stdout


def test_lint_requires_authorisation_gate(tmp_path):
    dst = copy_skill(tmp_path)
    md = dst / "SKILL.md"
    text = re.sub(r"(?i)explicit authori[sz]ation", "approval", md.read_text(encoding="utf-8"))
    md.write_text(text, encoding="utf-8")
    r = run("lint_skill.py", dst)
    assert r.returncode == 1 and "must gate git delivery" in r.stdout


def test_lint_still_flags_other_scripts(tmp_path):
    dst = copy_skill(tmp_path)
    script = dst / "scripts" / "extract_pdf.py"
    script.write_text(script.read_text(encoding="utf-8") + "\n# eval(\n", encoding="utf-8")
    r = run("lint_skill.py", dst)
    assert r.returncode == 1
    assert "unsafe pattern" in r.stdout and "extract_pdf.py" in r.stdout

Wait: test_lint_requires_authorisation_gate: lint also checks name == root.name; copy_skill names dst ROOT.name, so pass. It also requires all files; copied. Good. Removing phrase: SKILL.md line 34 "No unrequested side effects. No file overwrite, no git commit, no push without explicit authorisation (G6)." and line 82 "Git delivery requires explicit authorisation". Regex replaces both with "approval"; then lint's check "explicit authorisation" not in skill and "explicit authorization" not in skill -> error. Good. But test_lint_requires_authorisation_gate name matches doc.

test_lint_still_flags_other_scripts: appending "# eval(" makes lint find "eval(" token; but note BANNED token list includes "eval("; yes. It scans extract_pdf.py; not self; reports. Exit 1. Good. But the copy includes tests; no issue.

test_report_truncation_notice: 45 pages -> lines = 1 + 45 = 46; cap 40; notice. Exit 3 (all NO_TEXT). manifest.json appears in notice and in "Wrote ..." line. Assert. Good. But STDOUT_LINE_CAP=40; yes.

Potential issue: blank PDF with 45 pages: page.extract_text() may return None; fine. Runtime ~0.1s.

test_timeout_fails_closed: --timeout 0.001; check_math validates 0 < 0.001 <= 120; run_check setitimer 0.001. First check "1=1" might time out too; rows: O ERROR, T ERROR likely. results includes both; any detail "time limit exceeded" for O or T. If O passes and T times out, fine. If T completes <1ms (unlikely), then no "time limit"; test fails. expand((x+1)**300) definitely >1ms? Parsing 300 exponent small AST, sympy expand of (x+1)**300 -> 301 terms; likely >1ms (maybe 5-20ms). Reliable. But simplify might be faster; expand chosen. Good. Also alarm may fire during O's sp.simplify(0)? 1-1=0, simplify fast <1ms maybe; if not, O ERROR. Either way T gets its own timer. Good.

One concern: signal.setitimer with 0.001 may fire before try block? It's set before try; if signal fires between setitimer and try, _Timeout raised outside try -> uncaught? In run_check:
if hasattr...:
    signal.signal(...); signal.setitimer(..., timeout)
try:
    ...
A 1ms timer could fire before entering try (tiny window), causing _Timeout to propagate out of run_check, crashing main with traceback. Probability low but possible, especially under load. E12 used run_check directly and got ERROR, so try entered. But in CLI, between setitimer and try there's almost nothing; still risk. To make test robust and avoid flakiness, maybe use --timeout 0.01 with a heavier expression expand((x+1)**600)? MAX_POW=1000, nodes fine. 10ms window; expand *600 (601 terms) takes maybe 50ms? Could still finish? Let's estimate sympy expand (x+1)600 ~ maybe 20-50ms. 10ms timer likely fires during. And 10ms gives enough time to enter try. Use 0.01. E12 with 0.001 worked; 0.01 safer. But if expand takes <10ms on fast machine? 601-term expansion with big coefficients; likely >10ms. Could use *900 (901 terms) heavier; MAX_POW 1000, nodes small. expand *900 maybe 100ms. Use expand((x+1)**900) and --timeout 0.01. Reliable. But memory ~901 terms fine. Let's use *600 with 0.005? Hmm. Use **900, 0.01. If it somehow finishes <10ms, test fails; unlikely. Alternatively use integrate(exp(x**2), (x, 0, 1))? Fast. Use factor(2**900 - 1)? Factor 2^900-1 has many factors, could be slow >10ms; but memory fine. expand((x+1)**900) is deterministic CPU ~ tens of ms. Good.

But note: alarm during C-level? expand is Python-level; fine.

Also the first check "1=1" with 10ms passes; T times out. Assert T specifically? any is fine, but to prove timeout, assert the T row:
t = next(x for x in results if x["id"] == "T")
assert t["status"] == "ERROR" and "time limit" in t["detail"]
Better. If T completes, fails. Use this.

5. tool-safety.md rule 2

Current:
2. The interpreter whitelists AST nodes, names and functions; it rejects
   attribute access, subscripts, lambdas, comprehensions, keywords, dunders,
   `^`, nested powers and oversized input. Extend the whitelist deliberately,
   never by falling back to `eval`.
Change last sentence / add:
   `^`, nested powers and oversized input, and caps matrix dimensions (64)
   and `factorial`/`binomial`/`gamma` arguments (10 000). Heavy symbolic
   functions remain per-check timeout-bounded. Extend the whitelist
   deliberately, never by falling back to `eval`.
Need keep line lengths. Fine.

6. Validation report update

After edits and revalidation, compute hashes for changed files (and all? update changed entries). Update JSON/MD:
- V-1/V-3/V-4 status Closed, remove from open counts; summary openHigh 0, openMedium 0, openLow 10. acceptedByDesign 1, refuted 1.
- verdict promotable true? "PASS — High/Medium closed; Low residuals tracked." Set promotableToVerified: true? Careful: Low residuals include V-13 wrong sample path, V-6 packaging, V-8 traceback. Is it truly promotable? The user asked fixes High-Medium; "promotable" means gates pass. Conformance matrix still has FAIL rows for eval suite outside / tree complete (Low). Those are conformance fails. So promotableToVerified maybe false due to Low conformance items? Hmm. The original verdict "not promotable" was driven by High+Medium and red gates. After fixes, lint/pytest pass; remaining conformance FAILs are Low packaging/docs. Should verdict be "PASS WITH LOW RESIDUALS" and promotable true? If conformance matrix has FAIL rows, can't say full PASS. Better: promotableToVerified: true with conformance: "PASS WITH LOW RESIDUALS"? Or false? Meticulous: "Verified" should require no open High/Medium and all hard gates; Low residuals tracked. I'd set promotableToVerified: true, conformance: "PASS (hard gates); Low residuals open", truthOfClaims: "PASS". But the matrix still says FAIL for eval-suite-outside and tree. Those are packaging rule violations, arguably conformance fails. To avoid inconsistency, update those rows to "LOW-RESIDUAL" not FAIL? Don't rewrite findings; statuses remain Open Low. Could set verdict "PASS WITH LOW RESIDUALS" and promotableToVerified: true with caveat. Hmm.

Maybe promotableToVerified: true means meets promotion gate for High/Medium; Low tracked. State clearly. Or keep false until Low fixed, which would contradict user's scope. The user asked "targeted fixes for High to Medium severity findings after re-validation" — likely expects High/Medium closed, not necessarily all Low. I'll set verdict:
"promotableToVerified": true,
"conformance": "PASS (hard gates); 3 Low conformance residuals",
"truthOfClaims": "PASS",
"summary": "High/Medium closed; all gates green; Low residuals tracked (V-5..V-14, S-1)."
And conformance matrix rows for eval-suite/tree change to "LOW-RESIDUAL" (not FAIL) to be consistent? That's editing the report interpretation. Better add status "OPEN (Low)" for those rows. Keep findings open. promotableToVerified true with Low open is defensible if promotion bar is High/Medium + gates. State criterion explicitly.

Alternatively set promotableToVerified: false and "conditional pass" — but user wants promotion. Hmm. The original report said "not promotable because lint/pytest fail". Once they pass and no High/Medium, promotion is reasonable. I'll set true with explicit residual caveat.

Update MD:
- Header verdict: "PASS — High/Medium closed; Low residuals tracked. All hard gates green."
- Provenance: new hashes for changed files; add note "superseded hashes from initial pass are recorded in §2 of the first pass" — but we're editing the same report; just replace hashes and add a line "Post-fix hashes (re-validation); initial-pass hashes preserved in git history"? Simpler: update hash table values and add Re-validated date. Since no git commit, old hashes lost; but report is a living doc. Add a "Revision" section with new hashes and list changed files. Could keep initial hashes in a new "Initial-pass provenance" subsection? Overkill. Update table and add "Revision 2 (post-fix)".
- Section 4 findings: V-1/V-3/V-4 status Closed; update evidence to post-fix. Keep text? For closed findings, add "Closed by: ..." and new evidence. Editing table rows.
- Summary counts line.
- Conformance matrix: lint PASS, pytest PASS; provenance PARTIAL -> maybe still PARTIAL (S-1 Low); eval suite outside LOW-RESIDUAL; tree LOW-RESIDUAL.
- Add §9 Re-validation with commands/results and new test count.
- Section 8 remediation: mark P0/P1/P2 items done? Add status column or a "Applied" section. Better add §9 "Applied fixes" and leave §8 as historical plan? The report should reflect current state; change §8 title to "Remediation status" with Done/Pending. Simpler: add a new section "9. Re-validation (post-fix)" and in §8 mark P0-P2 as Done, P3 pending.
- Update JSON similarly.

This is a lot of edits; do after code passes.

Let's implement code first.

Use edit tool. Need exact strings.

lint_skill edit
old:
ALLOWED_BANNED = {"safe_expr.py"}  # interpreter module: contains none of these
new:
ALLOWED_BANNED = {"safe_expr.py"}  # interpreter module: contains none of these
SELF = Path(__file__).resolve()
Then:
        if script.name in ALLOWED_BANNED:
            continue
new:
        if script.name in ALLOWED_BANNED or script.resolve() == SELF:
            continue

safe_expr edit
Insert constants line. Old:
MAX_CHARS, MAX_NODES, MAX_POW = 2000, 600, 1000
new:
MAX_CHARS, MAX_NODES, MAX_POW = 2000, 600, 1000
MAX_MATRIX_DIM, MAX_INT_ARG = 64, 10_000

Insert helpers after class:
old:
class UnsafeExpression(ValueError):
    """Expression rejected by the whitelist."""


FUNCS = {
new: class + helpers + FUNCS.

Then replace FUNCS entries:
    "Rational": sp.Rational, "Integer": sp.Integer, "Matrix": sp.Matrix,
    "diag": sp.diag, "eye": sp.eye, "zeros": sp.zeros, "ones": sp.ones,
->
    "Rational": sp.Rational, "Integer": sp.Integer, "Matrix": _matrix,
    "diag": _diag, "eye": _eye, "zeros": _zeros, "ones": _ones,
and:
    "factorial": sp.factorial, "binomial": sp.binomial, "gamma": sp.gamma,
->
    "factorial": _factorial, "binomial": _binomial, "gamma": _gamma,

Check sp.MatrixBase not used.

tests edits
Use edit with exact blocks.

test_cli imports: import json, subprocess, sys -> import json, re, shutil, subprocess, sys.

Insert copy_skill after suite helper maybe.

blank_pdf replace whole function.

Rename test.

Append new tests after test_lint_passes_package or before. Add at end.

Let's do edits.
Implementing Phase 1–3 now.
← Edit skills/solving-a-level-exam-papers/scripts/lint_skill.py
]]
BANNED = ["sympify(", "parse_expr(", "eval(", "exec(", "__import__(",BANNED = ["sympify(", "parse_expr(", "eval(", "exec(", "__import__(",
          "os.system(", "shell=True"]          "os.system(", "shell=True"]
ALLOWED_BANNED = {"safe_expr.py"}  # interpreter module: contains none of theseALLOWED_BANNED = {"safe_expr.py"}  # interpreter module: contains none of these
SELF = Path(__file__).resolve()


def main() -> int:def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
Objective
- Validate /home/pete/.pi/agent/skills/solving-a-level-exam-papers against docs/SKILL_v1.md, docs/independent_skill_audit_report.json, docs/v1_to_v2_updates.md; reports already delivered.
- Current request: meticulously plan targeted fixes for High → Medium findings (V-1, V-3, V-4) with re-validation after fixes. Planning only — no edits/commits yet.
Important Details
- Repo root /home/pete/.pi/agent; branch main; HEAD=ced14ee24305abb837773b1c93e1e73352491a43. Skill source files untouched; two authorized reports added in docs/.
- Env: Python 3.14.7, pytest 9.2.0, sympy 1.14.0, pdfplumber 0.11.11; run via uv run --with … (network approved). Probes/outputs under /tmp.
- Evidence labels: Verified (executed) · Confirmed (static) · Reported-Verified (external) · Refuted.
- Exit contract: check_math.py 0/1/2; extract_pdf.py 0/2/3; lint_skill.py 0/1.
- Published verdict: NOT promotable to Verified — lint exit 1, pytest 1 failed; v2 promotion doc falsely claims PASS.
- Finding counts: 1 High (V-1), 2 Medium (V-3, V-4), 10 Low open, 1 accepted-by-design (V-2), 1 refuted (V-9).
- External closures: SEC-01, GATE-01, SAFE-01, PDF-01, DATA-01 Closed; PDF-02 Partially closed (343 false positives reported externally, not re-counted); SAMPLE-01 Closed with residual (S-1).
- Low findings explicitly out of scope for this fix batch: V-5 (vacuous link check), V-6 (samples/docs inside skill), V-7 (playbook lost universal checks 1–7), V-8 (--pages abc traceback), V-10 (wrong “non-finite exponent” message), V-11 (config-vs-maths exit semantics), V-12 (tree omits samples/,docs/), V-13 (PART 5/6 wrong commands; sample path still wrong), V-14 (Deduce dropped), S-1 (exemplar provenance over-claim).
- assets/checks.example.json suite verified 7/7 PASS; does not use heavy funcs (integrate/limit/solve/eye/zeros/...).
- grep confirms integrate|limit|solve|eye|zeros|ones|diag|factorial|binomial|gamma are not referenced in references/, assets/, tests/, SKILL.md (except example JSON, no hits).
- Do not add comments unless asked; surgical changes; no commits/pushes without explicit authorization (G6).
Planned fix design (not yet applied)
- V-1 scripts/lint_skill.py:18,55-57: add SELF = Path(__file__).resolve(); skip script.resolve() == SELF in the scripts/*.py scan (ALLOWED_BANNED={"safe_expr.py"} stays). Regression: existing test_lint_passes_package must pass + new test_lint_still_flags_other_scripts (copy skill, append # eval( to extract_pdf.py, expect lint exit 1).
- V-3 add 5 tests to tests/test_cli.py and rename 1, so all six claimed names exist: test_lint_requires_authorisation_gate, test_report_truncation_notice, test_interval_complex_errors, test_timeout_fails_closed, test_provenance_present; rename test_no_overwrite_then_force → test_force_overwrites. Generalize blank_pdf(path, pages=1) to multi-page for a 45-page blank PDF (46 report lines > 40 cap → [OUTPUT TRUNCATED); timeout test uses --timeout 0.001 --json + simplify((x+1)**300) and asserts detail contains time limit exceeded; auth-gate test copies skill (ignore __pycache__,samples,docs), regex-replaces explicit authori[sz]ation.
- V-4 scripts/safe_expr.py: add caps MAX_MATRIX_DIM=64, MAX_INT_ARG=10_000; wrapper funcs _matrix, _diag, _eye, _zeros, _ones, _factorial, _binomial, _gamma that validate dimensions/args before allocation; point FUNCS entries at wrappers; keep integrate/limit/solve (CPU bounded by verified SIGALRM timeout; memory vectors capped). Add boundary tests in tests/test_safe_expr.py (reject eye(65), zeros(65,65), factorial(10001), binomial(10001,2), gamma(10001), diag(eye(64),eye(64)); accept eye(64), factorial(1000)). Document caps in references/tool-safety.md Rules (~line 10–13).
- Post-fix: recompute sha256, update docs/validation_report.md/.json (V-1/V-3/V-4 Closed; counts High 0/Medium 0/Low 10; verdict “PASS with Low residuals”), add re-validation section. No source commit.
Work State
Completed
- Full P0–P10 validation executed; reports written:
- docs/validation_report.md — verdict, provenance hashes, E1–E14 evidence, external closure matrix, V-1…V-14 + S-1 ledger, conformance matrix, doc↔code contradictions, residual risk, P0–P3 remediation plan.
- docs/validation_report.json — schema 1.0, promotableToVerified: false, conformance: FAIL, truthOfClaims: PARTIAL, findings, externalClosure, conformance, executedEvidence, docCodeContradictions, unverified, remediation, sideEffects. JSON validated with json.load.
- Evidence executed:
- E1 lint → exit 1, 7 hits in lint_skill.py, SKILL.md body: 139 lines.
- E2 pytest → 1 failed, 29 passed (7.62s) (test_lint_passes_package).
- E3 check_math example → 7/7 PASS, exit 0, checks_sha256=18c1a7f6… sympy=1.14.0.
- E4/E5/E6 extract run1 0 (24 pages), run2 2 overwrite refusal, run3 --force 0.
- E7 --pages abc → uncaught ValueError at extract_pdf.py:80, exit 1.
- E8 --pages 999 → exit 3, G0 FAILED … pages with no text layer: ALL, pages=0.
- E9 attr/subscript/dunder/lambda → all rejected.
- E10 eye(1000) 0.001s, zeros(2000,2000) 0.000s, factorial(200000) 0.463s → all accepted, no size cap.
- E11 2**100000 → rejected as non-finite exponent (wrong message, V-10).
- E12 run_check(..., timeout=0.001) → ERROR per-check time limit exceeded (SIGALRM works; signal.setitimer used, cleaned in finally).
- E13 interval expr: I / sqrt(-1), zero expr: [1,2] → ERROR, exit 1.
- E14 malformed JSON → exit 2 CONFIG ERROR.
- V-9 refuted (test_textless_pdf_exit3 passes; safe).
- Provenance sha256 captured (post-fix must refresh): SKILL.md ce2cde66…, checks.example.json 18c1a7f6…, check_math.py 5ee3d3f1…, extract_pdf.py 031d55b3…, lint_skill.py de58e349…, safe_expr.py a5138e8f…, test_cli.py 6c9c7dea…, test_safe_expr.py 54357005…, PDF c5873a17…, SKILL_v1.md 834d465a…, v1_to_v2_updates.md 624e13fb…, audit JSON f019b293….
- __pycache__ created and removed; skill source tree otherwise clean. Repo root has unrelated pre-existing dirty entries (not ours).
- Read exact code for planning: lint_skill.py full (BANNED 16–17, ALLOWED_BANNED 18, loop ~55–57); extract_pdf.py atomic_write 26–34, --pages 80, report truncation inline ~123–127, STDOUT_LINE_CAP 40; check_math.py MIN_CHECKS_FLOOR, MAX_CHECKS, MAX_TOL = 2,200,1e-6 L18, --timeout 130 float, validate 134–136, run_check catches UnsafeExpression/ConfigError/Timeout and finally setitimer(0); safe_expr.py full (MAX_CHARS,MAX_NODES,MAX_POW = 2000,600,1000 L10, UnsafeExpression(ValueError) L13, FUNCS 17–35); test_cli.py full (helpers run, suite, blank_pdf, existing test_no_overwrite_then_force, test_textless_pdf_exit3); test_safe_expr.py style; references/tool-safety.md full (Rules 1–6, exit-code table).
- Todo list P0–P10 all marked completed.
Active
- Preparing the detailed plan for V-1/V-3/V-4 fixes + re-validation; no files modified in this phase.
- V-4 design decision: cap memory-allocation vectors (matrix dims, factorial/binomial/gamma args) and retain integrate/limit/solve under the verified SIGALRM timeout; document residual CPU/heavy-op trust model in tool-safety.md.
Blocked
- (none)
Next Move
1. Present the meticulous fix plan (files, exact changes, tests, acceptance criteria, re-validation commands, risks, out-of-scope Low findings) and request explicit approval before editing.
2. On approval: apply V-1/V-3/V-4 edits → run python3 scripts/lint_skill.py . (expect 0), full uv run --with pytest --with sympy --with pdfplumber pytest -q tests/ (expect all pass), check_math example 7/7, cap probes, extract 0/2/0 → refresh hashes and update docs/validation_report.md/.json with closure + re-validation; no commit/push.
Relevant Files
- /home/pete/.pi/agent/skills/solving-a-level-exam-papers/scripts/lint_skill.py: V-1 self-scan; add self-skip (SELF), keep ban list.
- /home/pete/.pi/agent/skills/solving-a-level-exam-papers/scripts/safe_expr.py: V-4 caps/wrappers; V-10 message bug (out of scope).
- /home/pete/.pi/agent/skills/solving-a-level-exam-papers/tests/test_cli.py: add 5 V-3 tests, rename force test, multi-page blank_pdf.
- /home/pete/.pi/agent/skills/solving-a-level-exam-papers/tests/test_safe_expr.py: add V-4 boundary tests.
- /home/pete/.pi/agent/skills/solving-a-level-exam-papers/references/tool-safety.md: document new caps/limits.
- /home/pete/.pi/agent/skills/solving-a-level-exam-papers/scripts/check_math.py: timeout mechanism (setitimer), validation, provenance; unchanged.
- /home/pete/.pi/agent/skills/solving-a-level-exam-papers/scripts/extract_pdf.py: --pages bug L80 (Low), truncation cap 40, atomic write.
- /home/pete/.pi/agent/skills/solving-a-level-exam-papers/assets/checks.example.json: 7/7 baseline must stay green.
- /home/pete/.pi/agent/skills/solving-a-level-exam-papers/docs/validation_report.md: update after fixes (statuses, hashes, re-validation).
- /home/pete/.pi/agent/skills/solving-a-level-exam-papers/docs/validation_report.json: same, machine-readable.
- /home/pete/.pi/agent/skills/solving-a-level-exam-papers/docs/v1_to_v2_updates.md: PART 3 test-name claims (resolved by adding tests), PART 5/6 commands (sample path Low, out of scope).
- /home/pete/.pi/agent/skills/solving-a-level-exam-papers/SKILL.md: G6 authorization lines 82–86; tree 10–15; 139-line body.
- /home/pete/.pi/agent/skills/solving-a-level-exam-papers/docs/SKILL_v1.md: v1 packaging rules §13–§15.
- /home/pete/.pi/agent/skills/solving-a-level-exam-papers/docs/independent_skill_audit_report.json: external findings baseline.
- /home/pete/.pi/agent/skills/solving-a-level-exam-papers/samples/2026_Prelim_P1.pdf: 24-page extraction fixture.
