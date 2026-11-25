# Revalidation rev 4 — `solving-a-level-exam-papers` (v2.0.1)

**Date:** 2026-11-25 · **Scope:** post-rev3 probe of `SKILL.md`, scripts, tests, and the validation record; fixes for V-21 … V-25 and the documentation defects D-3 … D-8.
**Verdict:** worktree gates pass and the audited defects are fixed. The repo at `HEAD` still lacks the sample PDF, and the fixes are uncommitted; promotion remains conditional until that is committed.

Evidence labels: **Verified** (executed, output observed) · **Reasoned** (code inspection only) · **Reported** (earlier report, not re-run).

---

## 1. What changed

| Finding | Severity | Fix |
|---|---|---|
| **V-21** strip recipe in `SKILL.md` fails | Low | Replaced the false "delete dirs, re-run linter" instruction with the true packaging contract: the linter is for the full self-verifying package and requires `tests/`. |
| **V-22** unreadable PDF traceback | Low | Wrapped `src.read_bytes()` in `OSError` handling → `CONFIG ERROR`, exit 2; added a regression test. |
| **V-23** ledger broken by `|` / newline | Low | Added `_md_cell()` escaping for ids, notes, kinds, roles and statuses; added a table-integrity test. |
| **V-24** real unlisted package file passes lint | Low | Added a tree-completeness check for every real file under package dirs (excluding hidden/cache paths); added a regression test. |
| **V-25** `--render` writes before overwrite refusal | Medium | Two-phase render: collect NO_TEXT pages, check `pages.txt`, `manifest.json` and all planned `page-*.png` targets, then write. A refused run now has no side effects. |

Tests added: `test_ledger_escapes_pipes_and_newlines`, `test_render_refuses_existing_png_without_force`, `test_unreadable_pdf_exit2`, `test_lint_flags_unlisted_package_file`. Suite grew from **97 to 101 passed**.

## 2. Documentation corrections

| ID | Defect | Correction |
|---|---|---|
| **D-3** | `closedLowRev3` was 14 | Set to **13** (10 rev2 + V-17, V-18, V-20). |
| **D-4** | rev3 said Python 3.11.2 | Corrected to **3.14.7**. |
| **D-5** | `v1_to_v2_updates.md` erratum said 89 passed | Corrected to **97 passed**. |
| **D-6** | `validation_report.md` banner overclaimed closure | Rewritten to point at rev4 and describe rev3 accurately. |
| **D-7** | JSON `revalidationEvidenceRev3` omitted R6 | Added R6. |
| **D-8** | rev3 §6 omitted changed-doc hashes | Added `docs/v1_to_v2_updates.md` and `references/tool-safety.md` rev3 hashes. |
| **H-2** | JSON claimed rev3 while carrying rev2 provenance/conformance | Converted it to an explicit **historical rev3 record** (`status: historical`, `supersededBy: docs/revalidation_rev4.md`), with rev3 hashes, 97-pass conformance, 13 count and R6. |

## 3. Executed verification (final state)

| # | Command | Result |
|---|---|---|
| R1 | `python3 scripts/lint_skill.py .` | exit 0 — PASS (body 149 lines) |
| R2 | `uv run --with pytest --with sympy --with pdfplumber pytest -q tests/` | **101 passed** |
| R3 | `uv run --with sympy python scripts/check_math.py assets/checks.example.json` | 7/7, exit 0, `checks_sha256=18c1a7f6668c01f2…` |
| R4 | `uv run --with pdfplumber python scripts/extract_pdf.py samples/2026_Prelim_P1.pdf --pages 4,16-18 --out /tmp/opencode/o4` | exit 0, 4 pages, `gate_G0: PASS` |
| R5 | bad `--pages` / out-of-range / overwrite refusal / corrupt PDF / missing checks file | exit **2** each; `CONFIG ERROR` or argparse usage; no traceback |
| R6 | playbook patterns (eigenpair, inverse, tangency discriminant, antiderivative) | 4/4 PASS |
| R7 | repo root `pytest -q tests/` | **390 passed, 9 skipped** (current dirty worktree; rev3's 411/8 was a different tree state) |

## 4. Provenance (SHA-256 of the rev4 worktree files)

| File | SHA-256 |
|---|---|
| `SKILL.md` | `2c7946a16c6722b3e1038d1fcb462293c3f525ab8c9657c5e28752e23139bc9d` |
| `assets/checks.example.json` | `18c1a7f6668c01f20c4c662eabb5692c87a7b391a9b7e9510787d7fba42489f2` (unchanged) |
| `scripts/check_math.py` | `01869b6ac41f0073bac8f51d8921d0c0cd902960e138dab88ed6b2819c720428` |
| `scripts/extract_pdf.py` | `ee30a0b706a0314daacb349366fd2c01263016834b1138a558badbb2532ec9a7` |
| `scripts/lint_skill.py` | `e6ee849983b7bc63fa593e6a86611412221bc71448c40f25f8556431903b540f` |
| `scripts/safe_expr.py` | `721c1b6c07d23f6deecc28a9060238e87ba4bcbaada3d71243c241a7cd1d7857` (unchanged) |
| `tests/test_cli.py` | `0ce6305a48eb37f7d0f4ab7b3490443801e357d7a008299d934c46163949e040` |
| `tests/test_safe_expr.py` | `24525a860f7a6822e210d1189d351cb7b2120e4ae4e4dc7da16fb02aa9136477` (unchanged) |
| `samples/2026_Prelim_P1.pdf` | `c5873a178e9538e78e1710d050e29bc25fc969bdfed29767c3948a2d558b57c8` (restored) |
| `docs/v1_to_v2_updates.md` | `ecf3ca6319c40290bf89531e382d4bdc2be56d27cfd72b2754ee9f1d7d65140a` |
| `docs/revalidation_rev3.md` | `40944259d1410a1d466ddf540bcd85eda65e964e3765fbb39adecec9e6bfaab4` |
| `docs/validation_report.md` | `147a64c7c73853cec2926931fcc454497703898a41d000f6baefc506acf04f3d` |
| `docs/validation_report.json` | `44a2537242ee262e340b7cdfd526ebc10b3ff3817e2bf984177f306ea45cdb1e` |
| `references/tool-safety.md` | `540b8960994d0aeb4a4defbdb3216282a206a42aab867b887ea6d796fd73d0d3` |

This report is not self-hashed (a file cannot contain its own SHA-256).

## 5. Residual risk and limits

- **H-1 remains:** `samples/2026_Prelim_P1.pdf` is present and staged in the worktree, but absent at `HEAD` `7c5cc0b8`. A fresh clone still fails lint and two tests. Commit is required; this pass did not commit.
- **V-6 remains a documented exception:** the eval suite lives outside the skill folder. The default package is consistent with that exception; the strip recipe is no longer advertised.
- `integrate`, `limit`, `solve` remain timeout-bounded, not argument-capped; Windows has no `SIGALRM`.
- `test_timeout_fails_closed` is timing-sensitive.
- The root suite reports 390 passed / 9 skipped in the current dirty worktree, not rev3's 411/8. The root checkout includes unrelated pre-existing edits and deletions; the skill-local suite is 101 passed.
- PDF candidate flags remain heuristic; paper/solution correspondence was not re-derived from page images.
- `docs/validation_report.json` is intentionally a historical rev3 record; this file is the current record.

## 6. Hand-off

**Verified:** §3 R1–R7. **Deliverable:** the five fixes, four regression tests, and the corrected validation record. **Not done:** commit or push. Stage named files only after explicit authorisation; do not use `git add -A`.
