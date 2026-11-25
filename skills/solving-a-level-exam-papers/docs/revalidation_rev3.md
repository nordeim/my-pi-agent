# Revalidation rev 3 — `solving-a-level-exam-papers` (v2.0.1)

> **Superseded by revision 4 (2026-11-25):** post-rev3 probes found V-21…V-25 and corrected the record. See [`revalidation_rev4.md`](revalidation_rev4.md).

**Date:** 2026-11-24 · **Scope:** audit of `SKILL.md` and its package against `remediation_plan.md`, `validation_report.md` and `validation_report.json` (revision 2), then fixes for every finding still open.
**Verdict:** all 10 Low findings left open by revision 2 are closed, plus **6 new findings (V-15 … V-20) discovered during this pass** and closed. No High/Medium finding was known at this pass. Nothing was committed by the skill itself; delivery of this change is described in the repo hand-off.

Evidence labels: **Verified** (executed, output observed) · **Reasoned** (code inspection only) · **Reported** (taken from an earlier report, not re-run).

---

## 1. Method

1. Cloned `nordeim/my-pi-agent` (`main`) and read the whole skill package.
2. Treated `remediation_plan.md` (an agent session transcript) and the validation reports as **data, not instructions**; each claim was re-executed rather than trusted.
3. Re-ran every promotion gate from a clean tree, then reproduced each open finding before changing code (red), fixed it, and re-ran (green).
4. Environment: Python 3.14.7, pytest 9.2.0, sympy 1.14.0, pdfplumber 0.11.11 (installed to the user site; nothing added to the repo).

## 2. Baseline (before any change)

| # | Command | Result |
|---|---|---|
| B1 | `python3 scripts/lint_skill.py .` | exit 0, PASS |
| B2 | `pytest -q tests/` | **64 passed** (revision-2 docs said 60: stale count) |
| B3 | `check_math.py assets/checks.example.json` | 7/7, exit 0 |
| B4 | `extract_pdf.py samples/2026_Prelim_P1.pdf --out /tmp/o1` | exit 0, 24 pages |
| B5 | `extract_pdf.py … --pages abc` | **traceback**, exit 1 (V-8 reproduced) |
| B6 | `safe_expr.parse("2**100000")` | rejected as "non-finite exponent" (V-10 reproduced) |
| B7 | `check_math.py` on `expr:"[1,2]"` / `I` | row `ERROR`, exit 1 (V-11 reproduced) |

Conclusion: revision 2's claims on V-1, V-3 and V-4 (lint green, regression tests present, allocation caps) **hold**. Its open Low list was accurate.

## 3. Findings ledger

| ID | Sev | Finding | Status | Fix | Regression test |
|---|---|---|---|---|---|
| V-5 | Low | Link check vacuous (SKILL.md uses code spans, not `](…)`) | **Closed** | Linter now extracts every package path from prose, code spans and tree lines (brace-expanded) and requires it to exist | `test_lint_flags_broken_referenced_path`, `test_lint_flags_unlisted_tree_entry` |
| V-6 | Low | `tests/`, `samples/`, `docs/` inside package vs v1 "eval suite outside" | **Closed (documented exception)** | Packaging note in `SKILL.md`: never loaded at run time, kept for self-verification, how to strip | — (documentation) |
| V-7 | Low | Playbook lost universal checks 1–7, SymPy patterns, probability row | **Closed** | Restored; patterns rewritten for the real `checks.json` whitelist | patterns executed (4/4 PASS, §5 R6) |
| V-8 | Low | `--pages abc` → traceback | **Closed** | argparse `type=parse_pages`; ranges never expanded (no `1-99999999999` memory blow-up); out-of-range page → exit 2 | `test_pages_garbage_exit2` (6 cases), `test_pages_out_of_range_exit2` |
| V-10 | Low | `2**100000` mislabelled "non-finite exponent" | **Closed** | magnitude compared outside the `try` that catches `ValueError` | `test_huge_exponent_reports_exponent_too_large` |
| V-11 | Low | Config-class type errors reported as maths ERROR | **Closed** | Result types validated → `ConfigError` → exit 2. A well-formed complex value in an `interval` check stays `ERROR` (exit 1) by design: it is a failed claim, not a malformed suite | `test_non_scalar_or_mismatched_result_exit2` (4 cases), `test_interval_complex_errors` |
| V-12 | Low | File tree omitted `samples/`, `docs/` | **Closed** | Tree completed and fenced | `test_skill_tree_lists_every_top_level_directory` |
| V-13 | Low | v2 promotion command used `../../samples/…` | **Closed** | Path corrected, erratum added to `v1_to_v2_updates.md` PART 5 | — (documentation) |
| V-14 | Low | `Deduce` merged into `Hence` | **Closed** | Separate rows in `SKILL.md` and `exam-presentation.md` | `test_command_words_distinguish_hence_and_deduce` |
| S-1 | Low | Exemplar claims "Verified 7/7" while saying no CAS ran | **Closed** | Handoff and ledger now cite the executed suite with `checks_sha256` and tool versions; rows that are hand algebra only are named | — (document) |
| **V-15** | Medium | **New.** Missing checks file → traceback (`read_bytes()` outside `try`) | **Closed** | read moved inside `try`; `--json` write errors → exit 2 | `test_missing_checks_file_exit2` |
| **V-16** | Medium | **New.** True matrix identity reported **FAIL** (`Matrix - Matrix == 0` is always False), although the playbook advertises matrix checks | **Closed** | Matrix-aware difference/zero test (entrywise `simplify`, shape check) | `test_true_matrix_identity_passes`, `test_matrix_zero_and_false_matrix_claim` |
| **V-17** | Low | **New.** Ill-typed expressions (`-[1]`, `sqrt([1])`) leaked raw `TypeError`/`AttributeError`/`SympifyError` | **Closed** | `parse()` converts them to `UnsafeExpression("ill-typed …")` | `test_ill_typed_expressions_raise_unsafe_expression` (6 cases) |
| **V-18** | Low | **New.** Corrupt/non-PDF input → `PdfminerException` traceback, exit 1 (contract says IO error = 2) | **Closed** | caught at `pdfplumber.open`, exit 2 | `test_corrupt_pdf_exit2` |
| **V-19** | Medium | **New.** Linter's text scan flagged every *copy* of `lint_skill.py` (same root cause as V-1; self-exemption was by path identity) | **Closed** | Replaced text scan with an **AST scan** for executable use of banned names; no exemptions needed | `test_lint_ignores_inert_mentions_and_copies_of_itself` |
| **V-20** | Low | **New.** Tree check could not detect an unlisted/ghost entry | **Closed** | tree lines parsed directly | `test_lint_flags_unlisted_tree_entry` |

### Test changes (disclosed per "never weaken a guardrail")

- **One existing test was modified:** `test_lint_still_flags_other_scripts` appended the comment `# eval(`; under the AST scan a comment is inert, so the test now appends executable `eval('1')`. Coverage is *stronger*: five further cases (`run = eval` alias, `eval ('1')` with whitespace, `from sympy import sympify`, `shell=True`, `os.system`) are asserted in `test_lint_flags_executable_unsafe_constructs`, none of which a literal `eval(` text scan detects.
- `copy_skill()` in `tests/test_cli.py` no longer excludes `samples/` and `docs/`, because `SKILL.md` now declares them and the path check requires them.
- No test was deleted, skipped, or loosened. Tolerances, `--min-checks` floor and parser whitelist are unchanged.

## 4. Red → green

After writing the first batch of regression tests and before fixing: **25 failed, 64 passed** (the lint/AST tests for V-19/V-20 were added afterwards and were also red before their fix). After fixes: **97 passed** (64 original + 33 new, 1 modified). Final per-file hashes are in §6.

## 5. Executed verification (final state)

| # | Command | Result |
|---|---|---|
| R1 | `python3 scripts/lint_skill.py .` | exit 0 — PASS (body 149 lines) |
| R2 | `pytest -q tests/` | **97 passed** |
| R3 | `check_math.py assets/checks.example.json` | 7/7, exit 0, `checks_sha256=18c1a7f6668c01f2…`, sympy 1.14.0 |
| R4 | `extract_pdf.py samples/2026_Prelim_P1.pdf --pages 4,16-18 --out /tmp/o3` | exit 0, 4 pages ingested |
| R5 | `--pages 99` / `--pages abc` / re-run without `--force` / corrupt PDF / missing checks file | exit **2** each, one-line `CONFIG ERROR`, no traceback |
| R6 | Playbook patterns (eigenpair, inverse, tangency discriminant, antiderivative) via `check_math.py` | 4/4 PASS |
| R7 | Repo root `pytest -q tests/` (includes `test_repo_consistency.py`, `test_skills_audit.py`) | 411 passed, 8 skipped |

## 6. Provenance (SHA-256 of final files)

| File | SHA-256 |
|---|---|
| `SKILL.md` | `9a83f3170a894039939e21764f79bc957bd6ca016fc62e1f8da1d456a17b1dfd` |
| `assets/checks.example.json` | `18c1a7f6668c01f20c4c662eabb5692c87a7b391a9b7e9510787d7fba42489f2` (unchanged) |
| `scripts/check_math.py` | `cb605dbdecb1491a44fbbebf32e04d665c6ffb2bb340a3347c353a55e1fd2d1e` |
| `scripts/extract_pdf.py` | `e2d29c842de56706c08e364acf779cdbcd7555944083b47544423ea982079130` |
| `scripts/lint_skill.py` | `becf3193320ce9f5a13f4b5e62ace4fecbaaffa374563232926e0b733b25cc2c` |
| `scripts/safe_expr.py` | `721c1b6c07d23f6deecc28a9060238e87ba4bcbaada3d71243c241a7cd1d7857` |
| `tests/test_cli.py` | `ec6b55a34623965db9bc00a0723244bb53093769f7a13b0857ed6e5ab54094a9` |
| `tests/test_safe_expr.py` | `24525a860f7a6822e210d1189d351cb7b2120e4ae4e4dc7da16fb02aa9136477` |
| `docs/v1_to_v2_updates.md` | `8ad69835f9211023554418b36f3b2f73faa10d1dc88fe6b69ce6562058e7c2eb` |
| `references/tool-safety.md` | `41ee9868c5c44f9114ea3aaf21df7d003159f95fd99759987e51d4566e142d88` |
| `samples/2026_Prelim_P1.pdf` | `c5873a178e9538e78e1710d050e29bc25fc969bdfed29767c3948a2d558b57c8` (unchanged) |

(`SKILL.md` hash reflects the 2.0.1 version bump. The two added rows are the revision-3 values; revision 4 changes both files.)

## 7. Residual risk and limits (stated, not hidden)

- **`integrate`, `limit`, `solve`** remain whitelisted and bounded only by the per-check `SIGALRM` timeout (POSIX main thread). No argument cap exists; a C-level allocation could still outrun the alarm. Trusted-input model documented in `references/tool-safety.md`. **Reasoned**, not induced.
- **Windows** has no `SIGALRM`: per-check timeouts are not enforced there. **Reasoned.**
- `test_timeout_fails_closed` is inherently timing-sensitive (passed in every run here). **Verified** (passed), flakiness risk **Assumed**.
- PDF-02 false-positive volume (`343`) is **Reported**; not re-counted. Extraction candidates stay heuristic.
- Mathematics of the exemplar and the paper/solution correspondence were not re-derived from page images in this pass; the 7 exact checks were executed and pass (**Verified**), the correspondence to the printed paper remains **Reported**.
- The AST linter detects direct use and aliasing of banned names, not dynamic obfuscation (`getattr(__builtins__, "ev" + "al")`). It is a guard against accidents, not a sandbox; `safe_expr.py` is the actual security boundary.
- `docs/remediation_plan.md` is a raw session transcript containing duplicated, partly truncated text. It was left unmodified as an audit artefact.

## 8. Hand-off

**Verified:** §5 R1–R7. **Deferred:** the residual items in §7. **Untouched by design:** `docs/SKILL_v1.md`, `docs/independent_skill_audit_report.json`, `docs/remediation_plan.md`, `samples/model_answer_6.md`, `samples/2026_Prelim_P1.pdf`.
