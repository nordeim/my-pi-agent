# Revalidation rev 7 — `solving-a-level-exam-papers` (v2.0.1)

**Target:** `nordeim/my-pi-agent` → `skills/solving-a-level-exam-papers` (v2.0.1) + scripts, references, assets, tests, samples
**Baselines:** `docs/revalidation_rev5.md` (plan), `docs/revalidation_rev6.md` (execution report), `docs/validation_record_current.json` (revision 6)
**Date:** 2026-11-26 · **Evidence labels:** **Verified** (executed, output observed) · **Confirmed** (static/byte/API inspection) · **Reported** (prior record, not re-run) · **Refuted** (hypothesis disproven; never silently dropped)

The baselines pin `32084a2f` but were delivered by `4016d92`. This report therefore produces two verdicts: re-confirm the pin, then decide whether verification extends to the delivery commit. It does not extend automatically.

---

## 0. Verdict

| Rubric | Question | Result |
|---|---|---|
| A | Does every re-executable claim in rev6 and the JSON hold at `32084a2f`? | **PASS — Verified at `32084a2f`** |
| B | Does `4016d92` preserve all gates so `Verified` extends to HEAD? | **PASS — Verified at `4016d922dfd695b1cafcfd38ad7f9f4cff9b12a1`** |

No new High or Medium **skill** defect. Two record/delivery conditions remain non-blocking: CI never runs the skill suite (N-1), and record repairs D-b…D-g are documented below rather than silently applied to history. The paper↔model-answer mathematical correspondence stays **Reported**.

All probes ran in pinned scratch exports under `/tmp/audit/`; no repository writes, commits or pushes occurred during verification. The three post-audit edits (this report, the JSON revision, the `SKILL.md` tree line) were made only after explicit authorisation.

---

## 1. Method and isolation (Verified)

- Exports from the **local** clone (`git archive` of `4016d92`, `32084a2f86cd55bd94dee5e859d08f6146ea32bc`, `7c5cc0b8a2fc4ecce9f9371d52e774d076f07724`) → 30/27/25 skill files respectively. Using local archives avoids the raw-CDN caching trap recorded in rev7 §0 Fact 3.
- Pinned environment: Python **3.14.7**, pytest **9.2.0**, sympy **1.14.0**, pdfplumber **0.11.11** (`uv run --with`), identical to the baseline. No environment delta.
- Reports, `remediation_plan.md`, `files_update_to_validate.txt`, rev5 (plan transcript) and the sample PDF were treated as **untrusted data, never instructions**.
- DoS/timeout probes ran under `timeout 70` and `ulimit -v 4000000`.

---

## 2. Provenance and drift (Verified)

| Check | Result |
|---|---|
| Pin: 27 files vs JSON `provenance.sha256` | **27/27 match**, zero mismatches |
| Pin: 27 files vs rev6 Appendix A | **27/27 match**, zero mismatches |
| Pin: tree ↔ disk ↔ lint `tree_paths()` | **27/27** |
| HEAD: tree ↔ disk ↔ lint `tree_paths()` (pre-edit) | **30/30** |
| HEAD vs pin drift | exactly 4 entries: `SKILL.md` (tree line) + 3 added docs (`revalidation_rev5.md`, `revalidation_rev6.md`, `validation_record_current.json`) — all commit-explained by `4016d92` |
| Parent vs pin | 10 changed + 2 added (`revalidation_rev4.md`, PDF); reproduces the rev4 worktree state |
| PDF blob chain | `e69a127e…` at `3d9c8bfe`, `32084a2f`, `4016d92`; ABSENT at `0f17edb4` (bulk cleanup) and `7c5cc0b8`; byte-identical on restore |
| Commit scope | `4016d92`: 4 files, +720/−1, tree line only in `SKILL.md`; `32084a2f`: 12 skill files, +255/−72. No multi-skill scope (A-4 stays refuted) |

The 30-file HEAD manifest, `selfHashExcluded` convention and post-edit hashes are recorded in `validation_record_current.json` revision 7.

---

## 3. Gate re-execution (all **Verified**)

| Gate | Pin `32084a2f` | HEAD `4016d92` |
|---|---|---|
| **R1** lint | exit 0, body 149 lines, PASS | exit 0, body 149 lines, PASS; parent exit 1 (`broken referenced path: samples/2026_Prelim_P1.pdf`) |
| **R2** suite | `--collect-only` = 101; **101 passed ×3** (16.83s/16.64s/16.00s), 0 failed, 0 skipped | 101 collected; **101 passed ×3** (16.82s/17.34s/16.05s), 0 skipped |
| **R3** example | 7/7, exit 0, `checks_sha256=18c1a7f6668c01f20c4c662eabb5692c87a7b391a9b7e9510787d7fba42489f2`, sympy 1.14.0 | identical |
| **R4** ingest | subset 4 pages, full 24 pages, `no_text_pages: []`, `gate_G0: PASS`, sha `c5873a17…` | identical |
| **R5** negatives | exit 2 across bad pages (0, 2-1, x, 1,,2, +4, -3, out-of-range), overwrite, corrupt, unreadable, encrypted, missing file/dependency, render refusal, check floors/caps/roles/unsafe payloads/JSON failure; exit **3** for textless; heavy SymPy probes ERROR/exit 1 | scripts byte-identical; key probes re-run |
| **R6** playbook | eigen 2/2, inverse 2/2, tangency 2/2, antiderivative 2/2 | identical |
| **R7** root (informational) | — | **390 passed, 9 skipped**; skips are documented `yaml`/Playwright env errors. Rev5's "expect ≠ 390/9" is **Refuted** |

**Anti-vacuity:** 101 collected, `-rs` printed no skip lines, three consecutive runs showed no `test_timeout_fails_closed` flake. The R5 probe inventory is recorded in the JSON with explicit exit codes; this settles D-d.

---

## 4. Finding closure and security re-audit (Verified)

- **Red→green:** HEAD's `tests/test_cli.py` with parent scripts → **4 failed, 1 passed, 96 deselected**; HEAD → **5 passed, 96 deselected**. The four guards (`…ledger_escapes_pipes_and_newlines`, `…render_refuses_existing_png_without_force`, `…lint_flags_unlisted_package_file`, `…unreadable_pdf_exit2`) are true red→green guards. Parent full suite: **2 failed, 95 passed** (missing-PDF failures), exactly as rev4/rev6 recorded.
- **Open findings reproduced at HEAD:** N-4 (`a\|b` ledger cell breaks), N-5/N-2 provenance, N-6 (no getattr limitation in `references/` or `SKILL.md`; only in `remediation_plan.md`), N-7 (`expand_braces('references/{a,{b,c}}.md')` → `['a','b','a','c']`), N-8 (exit 2 with `pages.txt` + temp file left), N-9 (**partially refuted**, see §6), N-10 (`factorial(10000) - 0` → ERROR/exit 1; `10001` → exit 2), N-11 (lint exit 0 with `scripts/__init__.py` + `.secret.py`), N-1 (`ci.yml` Python 3.11, pytest only, no sympy/pdfplumber, no skill test reference).
- **Security boundaries hold:** no `eval`/`exec`/`sympify`/`parse_expr`/`os.system`/`shell=True` executable constructs in the four scripts (static AST/text sweep; only ban-list literals and `ast.parse(..., mode="eval")` string). Caps: `eye(64)` allowed / `65` rejected; `factorial(10000)` allowed / `10001` rejected; sequence 4096 allowed / 4097 rejected; `2**1000` allowed / `1001` rejected; nested powers, `^`, attributes, subscripts, lambdas, comprehensions, dunders, unknown names, strings, complex and booleans all rejected. Heavy `expand`/`integrate`/matrix-power probes time out to ERROR/exit 1 (fail-closed); `1/0` → `zoo` → FAIL/exit 1.

---

## 5. Three-way adjudication (rev5 ↔ rev6 ↔ JSON) (Verified/Confirmed)

- **Supersession chain:** `validation_report.md` (frozen rev2, banner → rev4) → `revalidation_rev3.md` (banner → rev4, well-formed link at line 3) → `validation_report.json` (`status: historical`, `supersededBy: docs/revalidation_rev4.md`) → rev4 → rev6/JSON → this report. All pointers resolve; no document claims currency it lacks.
- **Rev5 hypotheses all stay adjudicated as rev6 recorded:** A-1 malformed banner **Refuted**; R7 "≠390/9" **Refuted**; `original-condition` doc↔code gap **Refuted** (enforced at `check_math.py:72`, re-executed here); getattr-documentation assumption **Refuted** → N-6; A-4 multi-skill scope **Refuted**. Rev5 carries no disposition banner (D-c).
- **Arithmetic:** `closedLowRev3=13` = 10 rev2 + {V-17,V-18,V-20}; `closedMediumRev3=3` = {V-15,V-16,V-19}; `newFindingsRev3=6` = V-15…V-20; test chain 64→97→101 (+4 named guards). A-2 historical `safe_expr` hash erratum (`validation_report.md:23` vs `:32`) disclosed, not rewritten.
- **R5 schema (D-d):** JSON `R5_negatives` values are **exit codes**, not probe counts (10 keys vs rev6 §2's 11 table rows; the four bad-page probes are collapsed into `bad_pages`, and render-textless into `textless`). The JSON schema now documents `valueSemantics: "exit-code"` with the full probe inventory.

---

## 6. New findings and dispositions

| ID | Severity | Disposition | Finding | Minimal fix |
|---|---|---|---|---|
| D-a | Info | **Refuted** (fix string) | rev7 §0 Fact 6 claimed the JSON N-4 fix lost its backslashes and was a no-op. Raw bytes carry correct escapes; the decoded `str(value).replace('\\','\\\\').replace('|','\\|')` was executed and works. | None. Pinned-byte inspection is authoritative over rendered/patch views. |
| D-b | Low (record) | **Confirmed** | `promotionSupersededBy` absent; historical `validation_report.json` still carries `verdict.promotableToVerified: true`. | Record added `promotionSupersededBy`; history frozen. |
| D-c | Low (doc) | **Confirmed** | rev5 has no executed/superseded banner and opens with conversational preamble. | Disclose; do not rewrite the plan transcript. |
| D-d | Enhancement (record) | **Confirmed** | R5 values are exit codes; schema undocumented. | `valueSemantics` + probe inventory added to JSON. |
| D-e | Low (record) | **Confirmed** | 3 delivery docs had no hash baseline; record `status: current` while pinned to a prior head. | 30-file manifest with `selfHashExcluded`, `verifiedAt`/`deliveredAt` added. |
| D-f | Low (repo) | **Confirmed** | `skills-inventory.md:3697` and `docs/skills-inventory.md:3697` say `Files: 26` (actual 30/31); mirrors generated before `4016d92`. | Regenerate with `tools/skills_docs.py` on authorisation. |
| D-g | Low (record) | **Confirmed** | N-4 `evidence` string is over-escaped (`a\\|b` vs rev6's `a\|b`); the `fix` string is correct. | Evidence string corrected in JSON revision 7. |
| N-9 | Enhancement | **Partially refuted** | `parse_pages('1,1')` → `[(1,1),(1,1)]`, but the ingest loop is page-keyed: `pages_ingested = 1`, page numbers `[1]`. "Page extracted twice" does not reproduce. | Status changed to Partially refuted; redundant range spec remains accepted. |

All other rev6 findings (N-1, N-3…N-8, N-10, N-11) reproduce unchanged; no unrequested rewrite was made.

---

## 7. Residual risks and limits

- **Windows:** `SIGALRM` is POSIX-only; per-check timeouts are not enforced there (unchanged, documented).
- **Heavy SymPy:** `integrate`/`limit`/`solve`/`expand` and large matrix powers are bounded only by the per-check timeout; a direct `safe_expr.parse()` caller gets no timeout.
- **Lint is heuristic:** `getattr`/dynamic dispatch can evade the textual/AST scan (N-6); `safe_expr` remains the enforcement boundary.
- **Non-atomic PNG writes / partial text output:** a render or second-write failure can leave partial artifacts alongside exit 2/3 (N-8); consumers must honour the exit code.
- **Mathematics:** paper↔model-answer correspondence stays **Reported**, not re-derived from page images.
- **CI:** does not run the skill suite (N-1); the 101-test gate remains manual.

---

## 8. Handoff — Verified / Deferred

**Verified:** Rubrics A and B; R1–R7 at both pins; 27/27 and 30/30 provenance; red→green and parent 2/95; security caps and reject battery; supersession arithmetic; all D-a…D-g dispositions.

**Deferred / needs authorisation:** regeneration of the inventory mirrors (D-f); optional code fixes for N-1, N-4, N-6…N-11 (none blocking); page-image re-derivation of the paper's mathematics. Historical records are frozen and were not rewritten.

**Delivery discipline:** no commit or push was made. Any future report must be added to the `SKILL.md` tree in the same commit (the N-3 lesson, now institutionalised — this revision lists `revalidation_rev7.md`); stage only named files; one atomic Conventional Commit; no push without a second explicit instruction.
