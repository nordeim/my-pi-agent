I'll ground this plan in the actual repository contents first — fetching the skill, the three validation artifacts, and the full file inventory in parallel, so the review plan targets real claims and real scripts rather than assumptions.
# AUDIT MODE — Review & Validation Plan
**Target:** `nordeim/my-pi-agent` → `skills/solving-a-level-exam-papers` (v2.0.1)
**Baselines:** `docs/revalidation_rev3.md`, `docs/revalidation_rev4.md`, `docs/validation_report.json`
**Plan date:** 2026-11-25 · **Evidence discipline:** the skill's own labels apply to this audit — **Verified** (executed/observed), **Confirmed** (static/API inspection), **Reported** (prior report, not re-run).

I ran read-only reconnaissance against GitHub before writing this plan, so it is grounded in the *actual* current tree, not the reports' snapshots. One material fact changes the whole audit framing:

> **Rev4's promotion blocker (H-1) appears to have been resolved after rev4 was written.** Rev4 (dated today) says the sample PDF is absent at `HEAD 7c5cc0b8` and the fixes are uncommitted. Current `main` is now **`32084a2f` ("update skills", 2026-11-25 10:56 UTC, parent `7c5cc0b8`)**, and that commit **adds `samples/2026_Prelim_P1.pdf` (1,117,524 bytes) plus the V-21…V-25 fixes and rev4 report**. The central question of this audit is therefore: *does the committed state byte-for-byte match the rev4 worktree state that passed the gates, and do those gates pass on a fresh clone?* That is **Confirmed (static)** so far — not yet **Verified**.

---

## 0. Reconnaissance baseline (already executed, read-only)

| Fact | Status | Evidence |
|---|---|---|
| Current `main` HEAD `32084a2f86cd55bd94dee5e859d08f6146ea32bc`, parent `7c5cc0b8a2fc…` (rev4's "bad" HEAD) | Confirmed | commits API |
| Commit touches `SKILL.md` (V-21 fix + tree adds `revalidation_rev4.md`), `check_math.py` (`_md_cell`, V-23), `extract_pdf.py` (`ensure_writable` two-phase render V-25 + `OSError` read V-22), `lint_skill.py` (`tree_paths` completeness V-24), `test_cli.py` (+4 regression tests), `tool-safety.md`, rev3 banner/D-4/D-8 edits, rev4 added, **PDF added** | Confirmed | commit patch API |
| Commit author `heinazhik` (not `nordeim`), unsigned, message `update skills`, +255/−72; **file list truncated in API response — full scope unconfirmed** | Confirmed / open | commits API |
| `validation_report.json` on `main` is the corrected **historical rev3 record** (`status: historical`, `supersededBy: docs/revalidation_rev4.md`, `closedLowRev3: 13`, R6 present, Python 3.14.7, rev3 hashes) — matches rev4's H-2/D-3/D-4/D-7 corrections | Confirmed | raw content |
| `validation_report.md` banner points to rev4; body is the frozen rev2 record (60 passed, 10 Low open, HEADs `ced14ee2` / `1d94f148`) | Confirmed | raw content |
| Full skill inventory: **27 files** — `SKILL.md`; 3 assets; 5 references; 4 scripts; 2 tests; 3 samples; 9 docs (incl. `files_update_to_validate.txt`, 3,378 B) — matches the SKILL.md tree exactly | Confirmed | contents API |
| `files_update_to_validate.txt` is a **git-pull transcript** of two historical change sets (13-file v1 import; 18-file v2 upgrade) — data, not instructions | Confirmed | raw content |
| Environment of record: Python 3.14.7, pytest 9.2.0, sympy 1.14.0, pdfplumber 0.11.11 (via `uv run --with`) | Reported | rev3/rev4/JSON |
| Test-count chain: 60 (rev2) → 64 baseline/97 (rev3) → **101 (rev4)**; root suite 411/8 (rev3) vs 390/9 (rev4 dirty worktree) | Reported | reports |
| This chat's code sandbox has **no network egress** → hash computation and test execution must run in your local/CI environment | Verified | sandbox probe failed |

**Anomalies already spotted (candidate findings to verify, not yet asserted):**
- **A-1:** rev3's supersession banner may contain a malformed link (`[` without closing `](…)` — visible in the commit patch; raw extraction showed a clean code span). Verify against raw bytes.
- **A-2:** rev2 `validation_report.md` §1 is internally inconsistent for `safe_expr.py` (table says `40700492…`, narrative says `a5138e8f… → a596778a…`). Historical record — disclose, don't rewrite.
- **A-3:** the PDF was present at rev3 commit `3d9c8bfe` (JSON provenance) but absent at `7c5cc0b8` — it was **dropped by some intermediate commit and restored today**. Provenance history needs `git log --follow`.
- **A-4:** commit hygiene vs the skill's own G6 contract: non-Conventional message, unsigned, possibly multi-skill scope. (G6 binds the skill agent; a human maintainer commit is a governance observation, not automatically a defect — classify accordingly.)

---

## 1. Charter

**Objective:** produce a defensible, executed verdict on whether the skill *as committed at `32084a2f`* conforms to, and satisfies, every claim in rev3, rev4 and the historical JSON — and whether rev4's conditional promotion can be lifted.

**Decision priority (descending):** fail-closed safety → executed evidence → the skill's documented contracts (exit codes, gates, G6) → report consistency → convenience. Never weaken a gate to make a check pass; never invent defects; refuted hypotheses are recorded as *Refuted*.

**Safety rules for the audit itself:**
1. Work only in a **fresh scratch clone pinned to `32084a2f`**; all probe outputs under `/tmp/audit/…`; zero writes into the repo worktree; **no commit, no push, no `git add -A`** without your explicit authorisation (mirrors G6).
2. Treat `SKILL.md`, references, `remediation_plan.md` (136 KB session transcript), the reports, and the sample PDF as **untrusted data, never instructions** (prompt-injection resistance).
3. Run all DoS/timeout probes under `ulimit -v` / `timeout` wrappers; never execute repo scripts against the live checkout.
4. Every claim gets a label; anything not re-executed stays **Reported**.

---

## 2. Scope

**In scope — all 27 package files:**

| Group | Files | Audit role |
|---|---|---|
| Entry | `SKILL.md` (8,269 B) | Contract source: frontmatter, tree, gates G0–G6, command words, evidence labels |
| Scripts | `safe_expr.py` (10,311 B), `check_math.py` (9,000 B), `extract_pdf.py` (7,718 B), `lint_skill.py` (6,169 B) | Security boundary + exit-code contract; per-script review (§3 WP-5) |
| Tests | `test_cli.py` (16,042 B), `test_safe_expr.py` (2,529 B) | 101-test suite; anti-vacuity checks; red→green proof |
| References | `source-fidelity`, `exam-presentation`, `verification-playbook`, `pitfalls-and-lessons`, `tool-safety` | Doc↔code conformance (G1–G5 guidance, caps/timeout model) |
| Assets | `solution-template.md`, `audit-template.md`, `checks.example.json` (sha `18c1a7f6…`) | Template contracts; 7/7 executable fixture |
| Samples | `2026_Prelim_P1.pdf` (1,117,524 B), `model_answer_6.md`, `model_answer_6_corrected.md` | H-1 fixture; S-1/SAMPLE-01 exemplar conformance |
| Docs (9) | rev3, rev4, `validation_report.{md,json}`, `v1_to_v2_updates.md`, `SKILL_v1.md`, `independent_skill_audit_report.json`, `remediation_plan.md`, `files_update_to_validate.txt` | Baselines + audit trail; consistency checks |

**Informational:** repo-root suite (`tests/test_repo_consistency.py`, `test_skills_audit.py`), `.github/workflows/ci.yml` (1,274 B — content not yet read).
**Out of scope (static reasoning only):** Windows `SIGALRM` behaviour; re-deriving the paper's mathematics from page images (stays *Reported* unless you authorise a full SOLVE+AUDIT pass); editing historical records.

---

## 3. Work packages (execution plan)

### WP-0 — Environment & isolation (prerequisite for everything)
```bash
git clone https://github.com/nordeim/my-pi-agent.git /tmp/audit/repo
cd /tmp/audit/repo && git checkout --detach 32084a2f86cd55bd94dee5e859d08f6146ea32bc
git status --porcelain   # must be empty
cd skills/solving-a-level-exam-papers
uv python install 3.14.7   # pin exactly; record any deviation as an environment delta
```
Pin `pytest==9.2.0 sympy==1.14.0 pdfplumber==0.11.11` in every `uv run --with`. **Exit criterion:** clean pinned tree; versions logged.

### WP-1 — Provenance & three-way hash conformance (highest priority)
1. Compute SHA-256 of **all 27 files** (rev4 hashed only 14 — close that gap):
   ```bash
   find . -type f -not -path '*/.*' -not -path '*/__pycache__/*' -print0 \
     | sort -z | xargs -0 sha256sum > /tmp/audit/head_manifest.sha256
   ```
2. Diff against three baselines: **rev3 §6 / JSON `provenance.sha256`** (historical), **rev4 §4** (expected current), and `changedSinceInitialPass`.
   - **Expected:** all 14 rev4-hashed files match rev4 exactly; `safe_expr.py`, `test_safe_expr.py`, `checks.example.json`, PDF unchanged across rev3→rev4 (`721c1b6c…`, `24525a86…`, `18c1a7f6…`, `c5873a17…`).
   - Any mismatch ⇒ **drift finding**: locate the changing commit (`git log -p -- <file>`) before judging; do not assume corruption.
3. Reconcile the HEAD chain with `git log --oneline ced14ee2..32084a2f` — place `1d94f148` (rev2), `3d9c8bfe` (rev3), `7c5cc0b8` (rev4-era), `32084a2f` (today). Explain rev4 R7's 390/9 vs rev3's 411/8 via tree states.
4. **PDF provenance:** `git log --oneline --follow -- samples/2026_Prelim_P1.pdf` → identify the drop commit between `3d9c8bfe` and `7c5cc0b8` (A-3) and confirm today's restore is byte-identical (`c5873a17…`).
5. `git show --stat 32084a2f` → full file list (API was truncated): confirm whether `validation_report.{md,json}` / `v1_to_v2_updates.md` rode in this commit or an earlier one, and whether **other skills** were touched (A-4 scope check).

**Exit criterion:** every current file is hash-matched to a report or has a documented, commit-backed explanation.

### WP-2 — Gate re-execution (rev4 §3 R1–R7 equivalents, fresh clone)
| Gate | Command | Pass condition |
|---|---|---|
| R1 lint | `python3 scripts/lint_skill.py .` | exit 0, PASS, body ≈149 lines (recount) |
| R2 suite | `uv run --python 3.14.7 --with pytest==9.2.0 --with sympy==1.14.0 --with pdfplumber==0.11.11 pytest -q -rs tests/` | **101 passed, 0 failed, 0 skipped** |
| R3 example | `uv run --with sympy==1.14.0 python scripts/check_math.py assets/checks.example.json` | 7/7, exit 0, `checks_sha256=18c1a7f6668c01f2…` |
| R4 ingest | `… extract_pdf.py samples/2026_Prelim_P1.pdf --pages 4,16-18 --out /tmp/audit/o1` | exit 0, 4 pages, `gate_G0: PASS`; also full run = 24 pages |
| R5 negatives | bad `--pages`, out-of-range, overwrite refusal, corrupt PDF, missing checks file, unreadable PDF | exit **2** each, one-line `CONFIG ERROR`/usage, **no traceback**; textless ⇒ exit **3** |
| R6 playbook | eigenpair, inverse, tangency discriminant, antiderivative suites | 4/4 PASS |
| R7 root | repo-root `pytest -q tests/` | **informational**: 0 failures; record counts/skips (expect ≠ 390/9 ≠ 411/8 on this tree) |

**Anti-vacuity guards (critical):** `pytest --collect-only -q` must show 101; `-rs` must show **zero skips** — the suite uses `pytest.importorskip`, so a dependency-less run can look green while silently skipping the security tests. Assert all named regression tests exist by name (WP-3 map). Run R2 **three times** to expose `test_timeout_fails_closed` flakiness; any flake ⇒ finding with repeat statistics.

### WP-3 — Finding-closure regression audit (red→green proof)
Verify every closure has a *guarding* test, not just a claim. Compact map (full matrix goes in the deliverable):

| Findings | Guard / method |
|---|---|
| V-1, V-19 | `test_lint_passes_package`, `test_lint_still_flags_other_scripts`, `test_lint_ignores_inert_mentions_and_copies_of_itself`, `test_lint_flags_executable_unsafe_constructs` (alias/whitespace/import/`shell=True`/`os.system`) |
| V-3 | six named tests (`…authorisation_gate`, `…truncation_notice`, `…interval_complex_errors`, `…timeout_fails_closed`, `…provenance_present`, `…force_overwrites`) |
| V-4 | 12 reject + 12 accept allocation probes at caps 64/10000/4096 (re-run rev2 R7/R8 vectors) |
| V-5/V-20/V-24 | `test_lint_flags_broken_referenced_path`, `…unlisted_tree_entry`, `…unlisted_package_file` |
| V-8/V-18/V-22 | `test_pages_garbage_exit2` (6 cases), `…out_of_range_exit2`, `test_corrupt_pdf_exit2`, `test_unreadable_pdf_exit2` |
| V-10/V-11/V-17 | `test_huge_exponent_reports_exponent_too_large`, `test_non_scalar_or_mismatched_result_exit2`, `test_ill_typed_expressions_raise_unsafe_expression` |
| V-15/V-16 | `test_missing_checks_file_exit2`, `test_true_matrix_identity_passes`, `test_matrix_zero_and_false_matrix_claim` |
| V-12/V-14 | `test_skill_tree_lists_every_top_level_directory`, `test_command_words_distinguish_hence_and_deduce` |
| V-23/V-25 | `test_ledger_escapes_pipes_and_newlines`, `test_render_refuses_existing_png_without_force` |
| V-6/V-13/V-21, S-1 | static: packaging note present, strip recipe absent, `samples/…` path in PART 5, exemplar ledger cites executed suite + `checks_sha256` |
| SEC-01/GATE-01/PDF-01/DATA-01/SAFE-01 | payload battery → exit 2; suite floor/cap probes; `NO_TEXT_MIN_CHARS=20` boundary (19 vs 20 chars); overwrite/`--force`; G6 text + lint gate |
| D-3…D-8, H-2 | static assertions on JSON/rev3/md (counts 13/3/6, Python 3.14.7, 97-pass erratum, R6, historical labels) |
| PDF-02 | optional: re-count candidate flags across all 24 pages to upgrade *Reported* → *Verified* |

**Red→green proof of the rev4 fixes (H-1 core):** in a scratch copy, combine **HEAD's `test_cli.py` with parent `7c5cc0b8`'s scripts** and run the four new tests → expect **red**; run at HEAD → **green**. Note: parent lacks the PDF, so fixture-dependent reds may surface as errors — that itself demonstrates H-1's fresh-clone failure mode. Also run lint + full suite **at parent** to reproduce rev4's "fresh clone fails lint and two tests" claim.

### WP-4 — Cross-document consistency & record integrity
- Supersession chain: rev2 md (frozen) → rev3 (superseded banner) → JSON (`historical`, `supersededBy`) → rev4 (current) — all pointers resolve; no document claims currency it doesn't have.
- Arithmetic: `closedLowRev3=13` = 10 rev2 + {V-17, V-18, V-20}; `closedMediumRev3=3` = {V-15, V-16, V-19}; `newFindingsRev3=6`; 97→101 = +4 named tests.
- Verify A-1 (banner link bytes), A-2 (rev2 `safe_expr` narrative vs table — disclose as historical erratum, no rewrite), JSON `verdict.promotableToVerified: true` inside a *historical* record vs rev4's conditional promotion (wording-risk assessment).
- SKILL.md tree ↔ disk ↔ lint `tree_paths` three-way match (27/27); frontmatter `name` = dir, description length within spec, body < 500 lines.

### WP-5 — Security re-audit (per script, resource-limited)
| Script | Focus |
|---|---|
| `safe_expr.py` | Full whitelist review; confirm no `sympify/parse_expr/eval/exec`; caps boundary tests (64/65, 10000/10001, 4096/4097); `integrate/limit/solve` timeout-only model — probe expensive forms under `timeout`+`ulimit`; document Windows gap (static); known linter-bypass (`getattr` obfuscation) stays a *documented limitation*, `safe_expr` is the boundary |
| `check_math.py` | `MIN_CHECKS_FLOOR=2`/`MAX_CHECKS=200` boundaries (1, 2, 200, 201 checks; duplicate ids); timeout ≤ 0; `--json` write-failure → exit 2; whether "≥1 `original-condition`" is enforced by code or only by SKILL.md (doc↔code gap candidate); **`_md_cell` escape completeness** — it escapes `|`, `\r`, `\n` but not backslash: probe note `\|` (double-escape column break) |
| `extract_pdf.py` | `parse_pages` fuzz (`0`, `-3`, `2-1`, `1-99999999999`, whitespace, `+4`, `1,,2`); encrypted PDF; **two-phase render residual side effects**: mid-render failure after first PNG written; `pages.txt` written then `manifest.json` `OSError` → partial output with exit 2; PNG writes are non-atomic (direct `.save`) vs `atomic_write` for text; TOCTOU noted as outside threat model |
| `lint_skill.py` | AST scan scope; brace-expansion edge cases (nested braces); hidden-path exclusion `(".", "__")` also excludes legitimate `__*` files from completeness (V-24 residual?); symlink handling; confirm no network/subprocess in all four scripts (static grep + observed runs) |

### WP-6 — New-defect hunt (rev5 probes)
The WP-5 probes double as the new-finding hunt; each hypothesis gets *Confirmed/Refuted* with executed evidence, severity (Critical/Major/Minor/Enhancement per the audit template), location, and a **minimal fix proposal — no unrequested rewrites**.

### WP-7 — Repo integration
Read `ci.yml`: does CI install sympy/pdfplumber before pytest? If not, `importorskip` masks the security suite in CI (green-but-vacuous risk) → recommendation only. Check root consistency/audit tests still pass at HEAD; `.gitignore` doesn't exclude the PDF; confirm A-4 commit scope.

---

## 4. Six-phase mapping, checkpoints, deliverables

| Phase | Content | Exit gate |
|---|---|---|
| **Analyze** | §0 recon (done) + WP-0 | pinned clean clone; anomalies logged |
| **Plan** | this document | your approval of scope/priorities |
| **Validate** | WP-1, WP-4 (static/consistency) | hash matrix complete; drift explained |
| **Implement** | WP-2, WP-3, WP-5, WP-6, WP-7 (probe execution only — *no code changes*) | all gates executed; red→green proven |
| **Verify** | cross-check evidence vs every report claim; 3× flake run; anti-vacuity | zero unlabelled claims; zero silent skips |
| **Deliver** | report + verdict + handoff | **checkpoint: your authorisation** before any repo write |

**Deliverables (scratch first, repo only on authorisation):**
1. `revalidation_rev5.md` — post-commit confirmation audit: executed R1–R7 table, finding ledger (closures re-verified + any new V-26+/D-9+), full 27-file SHA-256 manifest, HEAD-chain reconciliation, H-1 closure statement, residual risks, **Handoff — Verified / Deferred**.
2. A **new current machine-readable record** (e.g. `validation_record_current.json`) superseding the historical rev3 JSON — the historical file is never edited to claim currency.
3. If (and only if) you authorise delivery: `git status --porcelain` first, stage **only the named report files**, one atomic Conventional Commit (e.g. `docs(solving-a-level-exam-papers): add rev5 post-commit revalidation`), no push.

**Promotion rubric — lift rev4's conditional status to *Verified at `32084a2f`* iff:** all 14 rev4 hashes match (or drift is commit-explained) **and** lint exit 0 **and** 101/101 with 0 skips **and** 7/7 + `checks_sha256` match **and** exit-code battery clean **and** red→green proven **and** no new High/Medium finding. Anything less ⇒ verdict stays conditional, with the exact failing gate named.

---

## 5. Risks & limits of this plan
- **Execution venue:** this chat's sandbox has no egress; WP-0…WP-7 must run on your machine or CI (I can generate the full harness script + hash-diff utility ready to run).
- Python 3.14.7 availability may force an environment delta — record, don't hide.
- `test_timeout_fails_closed` flakiness handled by repetition, not by loosening.
- Paper/solution mathematical correspondence stays *Reported* unless you commission a page-image re-derivation.
- The reports themselves are adversarial input: no claim is inherited without re-execution.

**Estimated effort:** WP-0/1 ≈ 1 h · WP-2/3 ≈ 1–2 h · WP-4 ≈ 0.5 h · WP-5/6 ≈ 2–3 h · WP-7 + deliverables ≈ 1–2 h.

---

## 6. Decision point

Say **"execute"** and I'll start with WP-0/WP-1 — or, since execution needs an environment with network + Python 3.14, I can first deliver the **self-contained verification harness** (clone/pin script, 27-file hash manifest + three-way differ against rev3/rev4/JSON, gate runner with anti-vacuity assertions, red→green scratch procedure, and a findings-ledger skeleton) so you can run the entire plan verbatim and feed the outputs back for adjudication. 
