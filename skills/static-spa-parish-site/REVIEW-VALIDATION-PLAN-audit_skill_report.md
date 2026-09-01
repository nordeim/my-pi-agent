# Meticulous Validation Plan — `audit_skill_report.md` (296 lines, 2026-09-01) vs Its Referenced Sources

> **Request:** Meticulously plan to review `audit_skill_report.md` and validate every finding and recommendation against the files it cites.
> **Author:** Claw Code (Frontend Architect · 15y) · **Date:** 2026-09-01 · **Method:** Meticulous Approach — ANALYZE → PLAN → VALIDATE → IMPLEMENT → VERIFY → DELIVER
> **Mode:** C (Audit-of-the-auditor) — read-only discipline. No SKILL file, plan file, or the audit report itself is edited until this validation report is delivered and a fix pass is separately approved.
> **Baseline rule from the audit itself:** document-internal claims are **Verified at text level** (`rg` against attached content) or **Reasoned**; repo-state claims (`src/index.css` byte counts, built-output `397.52 kB`, harness green) are **Unverifiable** in a docs-only environment and must be labeled as such with the exact command that would verify them.

---

## Table of Contents

1. [Executive Summary & Go/No-Go](#1-executive-summary--gono-go)
2. [Phase 1 — ANALYZE: What the Audit Report Is, What It Claims, and Where It Can Be Wrong](#2-phase-1--analyze-what-the-audit-report-is-what-it-claims-and-where-it-can-be-wrong)
3. [Phase 2 — PLAN: 10-Axis Validation Matrix & Reproducible Methods](#3-phase-2--plan-10-axis-validation-matrix--reproducible-methods)
4. [Phase 3 — VALIDATE: Confirmation Gate](#4-phase-3--validate-confirmation-gate)
5. [Phase 4 — IMPLEMENT: How the Validation Will Run (After Approval)](#5-phase-4--implement-how-the-validation-will-run-after-approval)
6. [Phase 5 — VERIFY: Iron Law](#6-phase-5--verify-iron-law)
7. [Phase 6 — DELIVER: Report & Recommendation](#7-phase-6--deliver-report--recommendation)
8. [Appendix A — Claim Inventory to Validate (34 candidate findings + 5 plan deltas + recommendations)](#8-appendix-a--claim-inventory-to-validate)
9. [Appendix B — Evidence Map (which file proves or refutes each claim)](#9-appendix-b--evidence-map)
10. [Appendix C — Risk Register](#10-appendix-c--risk-register)

---

## 1. Executive Summary & Go/No-Go

**One sentence:** `audit_skill_report.md` is a *plan to produce a report* that already embeds **34 candidate findings** (15 unified-v3 fossils U-1..U-15 + 6 rothershrine era fossils R-1..R-6 + 5 SKILL auditor-self findings S-1..S-5 + 8 plan-fidelity deltas P-1..P-3/D-1..D-5), two High-severity **auditor-self contradictions** (S-1 `hours 6 keys` vs its own verbatim 7 keys; S-2 `mass 11 keys` vs its own verbatim 9 keys), a full 11-axis method with a reproducible `rg`/`wc`/`diff`/`sed` gate, and a *conditional-promotion* recommendation (`SKILL.md` canonical contingent on fixing S-1/S-2); the validation must therefore answer (a) is each of the 34 findings reproducible in the cited source text, (b) is each severity correctly calibrated, (c) do the two plan documents (`UNIFIED-V3-PLAN.md`, `REVIEW-PLAN-SKILL-vs-unified-v3.md`) contain the errors P-1/P-2 the audit attributes to them, and (d) does the conditional-promotion thesis survive the auditor's own §0 errors — with every verdict carrying a `rg` citation and a **Verified / Reasoned / Unverifiable** label.

**Go/No-Go: GO.** A 5-minute spot-check has already **confirmed** the audit's two decisive claims at text level:

- **S-1 confirmed:** `SKILL.md` §0 says `hours 6 keys` (line 55, 354, 530) while `§1` enumerates 7 names (`gates`, `mainChurch`, `chapel`, `reception`, `parishOffice`, `mediaCentre`, `adorationRoom`) and `§20.3` verbatim `site.hours` defines **7** keys (`gates`, `mainChurch`, `chapel`, `reception`, `parishOffice`, `mediaCentre`, `adorationRoom`) — see `sed -n '1192,1200p' SKILL.md`. The hypothesis (hop-3 diff computed `7 − columbarium = 6` forgetting `mediaCentre` replaced it) is plausible.
- **S-2 confirmed:** `SKILL.md` §0 says `mass 11 keys` while `§20.3` verbatim `site.mass` defines **9** keys (`weekdayMorning`, `weekdayEvening`, `saturday`, `sunday`, `confession`, `adoration`, `secondCollection`, `note`, `monthly`) — `sed -n '1201,1211p' SKILL.md` counts 9; even if `sunday[5]` were expanded to 5, that is array length, not object keys. No document-internal derivation for `11`.

Which means the audit's sharpest thesis — *the single-source-of-truth register violates its own contract* — is not speculation; it is where the validation report's verdict will be decided. The remaining 32 findings must be checked with identical rigor.

**Recommendation preview (to be confirmed or overturned by evidence):** The audit's **method is sound, its conditional-promotion stance is defensible, and S-1/S-2 deserve to remain High** — but the validation must still re-verify every U/R/P/D row, reconcile the two token-counting conventions (25+2 SKILL byte-true vs 26+2 unified superset), confirm whether `REVIEW-PLAN App A #10`'s `z-[60]` claim is indeed false (it is on current read: `rg -n "z-\[60\]" unified-v3` shows zero §18 row, only `Layout.tsx`/`ScrollProgress.tsx` refs), and decide whether any finding severity should be downgraded or reclassified before the audit becomes a fix plan.

**Environment caveat (honesty):** This workspace **does have** a shell and the `new-skills/` docs, but **no `src/` repo**. All `src/index.css` / `dist/index.html` / `pnpm test` / `find src | wc -l` claims are therefore **Unverifiable** here and will be labeled as such with the exact command that would verify them in the repo root, exactly as the audit itself demands in its §5.2 caveat.

---

## 2. Phase 1 — ANALYZE: What the Audit Report Is, What It Claims, and Where It Can Be Wrong

### 2.1 What the audit report is

| Property | Value |
|---|---|
| File | `audit_skill_report.md` — 296 lines, 2026-09-01 |
| Genre | **Plan to produce a report** that already embeds a full pre-read inventory (not the report itself) |
| Lineage it governs | `rothershrine-v2_SKILL.md` (hop-1 fossil, v1.3.0) → `unified-v3_SKILL.md` (Lineage Master v3.0.0, 2026-08-31) → `SKILL.md` (unified v3.0.0 + `package_version: 1.4.4`, 2026-09-01) + `UNIFIED-V3-PLAN.md` + `REVIEW-PLAN-SKILL-vs-unified-v3.md` |
| Thesis | Two live cannons both claim single-source-of-truth; `SKILL.md` wins the architecture argument but carries two High internal contradictions in §0, so promotion must be conditional on a same-commit §0 fix |
| Method already proposed | 11-axis matrix V1–V11, count-trajectory matrix, reproducible `rg`/`wc`/`diff`/`sed` gate (§3.2), manual spot-checks, success criteria, severity taxonomy, confidence labels (V/P) |

### 2.2 What must be validated (three layers)

| Layer | Audit's claim family | This validation's job |
|---|---|---|
| **L1 — Factual accuracy** | 34 candidate findings U-1..U-15 / R-1..R-6 / S-1..S-5 / P-1..P-3 / D-1..D-5 each pin a file + line + severity + G# + confidence | Re-run every `rg` citation against the **actual files on disk**; mark each **Confirmed / Refuted / Reclassified** with a verbatim `rg -n` citation + line number |
| **L2 — Severity & taxonomy calibration** | High/Med/Low per §12; Critical axis gating in §3.1 | Check whether each severity matches the taxonomy definition and whether any High should be Critical (or vice-versa); flag under-/over-severity |
| **L3 — Recommendation soundness** | "Promote `SKILL.md` as canonical **conditionally** (block on S-1/S-2), freeze `unified-v3` as superset, `rothershrine-v2` as origin" | Test the logic: does the evidence support conditional-promotion over the alternatives (promote unified-v3, co-canonical, no promotion); are blockers necessary and sufficient; what would change the verdict |

### 2.3 Pre-read spot-checks (seeds for Appendix A; confidence labeled now, evidence in Phase 4)

| # | Audit claim | Spot-check result | Confidence |
|---|---|---|---|
| S-1 | SKILL §0 `hours 6 keys` vs §20.3 verbatim 7 | **Confirmed** — `rg -n "hours 6 keys" SKILL.md` hits 3 lines; `sed -n '1192,1200p'` counts 7 keys; §1 lists 7 names while saying "6 keys" | **V** (text) |
| S-2 | SKILL §0 `mass 11 keys` vs §20.3 verbatim 9 | **Confirmed** — `rg -n "mass 11 keys" SKILL.md` hits 55,1578,530; `sed -n '1201,1211p'` counts 9 keys; no derivation for 11 | **V** |
| S-4 | SKILL sum claims verify (202 via 35-term sum; 51 via 8 specs; §4.1 25 colors; §4.3 27 rows) | **Likely confirmed** — audit says it re-summed 35-term `4+3+16+5+…+13+6=202` and `11+8+4+4+7+6+8+3=51`; needs arithmetic re-sum in Phase 4 | P |
| P-1 | REVIEW-PLAN App A #10 claims unified-v3 §18 has `z-[60]` row — audit says false | **Confirmed on current read** — `rg -n "z-\[60\]" unified-v3` returns only `Layout.tsx`/`ScrollProgress.tsx` refs, **zero** §18 `| z-[60] |` row; `rg -n "^\|.*z-\[60"` unified-v3 returns 0; SKILL.md §18 does have the row (`| Rail | z-[60] |`) | V |
| P-2 | REVIEW-PLAN §2.2 "§0 … (16 rows)" vs actual 19 rows | Needs `rg -c "^\|"` on SKILL §0 table to confirm 19 | P |
| U-1 | unified-v3 §6 "Two hooks" vs §2/§11 `useScrollSpy (6)` + 3 hooks in Quick Ref | Likely confirmed — `rg -n "Two hooks|Three hooks"` shows unified-v3 `Two hooks` while SKILL.md says `Three hooks`; but needs tree + test-list cross-check | P |
| U-4 | unified-v3 §18 no `z-[60]` row | **Confirmed** as above (zero §18 row) | V |
| Token divergence | 25+2 (SKILL byte-true) vs 26+2 (unified superset) flagged as CONCERN not FAIL | Sound classification — but needs `sed -n '/@theme/,/^}/p' f | rg -c "--color-shrine-"` execution to confirm 25/26/24 actuals | P |

*All other U/R/P/D rows are **P** until Phase 4 runs the gate.*

### 2.4 Where the audit report itself could be wrong (risk hypotheses to test)

1. **Under-counting S-1/S-2 root cause** — audit hypothesizes `7 − columbarium = 6` forgetting replacement; validation must check whether any other `hours` key (e.g., `bookshop`) explains the `6` in an earlier hop, to ensure the fix recommendation (change §0 to 7) is the right repair vs restoring `bookshop`.
2. **Severity over-escalation** — S-1/S-2 are High; should either be **Critical** (single-source register error violates ADR-7) or downgraded to Medium if the verbatim block is considered the true source. Validate against the audit's own §12 taxonomy definition.
3. **CONCERN vs FAIL boundary for tokens** — audit correctly says 25+2 vs 26+2 is CONCERN-by-design, not FAIL; but `unified-v3` §4.3 claiming "28 utilities / 8 keyframes" while listing only 6 keyframes would be a FAIL if that text exists — needs row count.
4. **REVIEW-PLAN error propagation** — audit already found P-1/P-2, but there may be additional errors in the two plans (line counts `wc -l 1590/1438`, decision letters) that the audit did not flag.
5. **Missing findings** — audit lists 34 candidates, but Appendix G in SKILL has 26 findings; U-14 (`playwright.built` include 4 vs 5) is marked new — there may be additional G gaps the audit missed, or false positives among G's 26 on unattached sources (`st-mary`, `risen-christ` when file not available — but in this env they *are* available).

---

## 3. Phase 2 — PLAN: 10-Axis Validation Matrix & Reproducible Methods

Axes V1–V11 validate the audit's own eleven axes; V12–V13 are new auditor-of-the-auditor checks.

### 3.1 Axis matrix

| Axis | What it validates in the audit report | Method (reproducible — outputs pasted verbatim in the validation report) | Pass criterion | Severity |
|---|---|---|---|---|
| **A1 — Audit self-consistency** | Does `audit_skill_report.md` contradict itself (line counts, heading counts, count-trajectory cells, appendix numbering)? | `wc -l` all 5 files; `rg -n "^## |^# " audit_skill_report.md \| wc -l`; cross-check audit §1.3 `S-1/S-2` counts vs Appendix A S-1/S-2 vs §3.3 matrix `hours 6/7 / mass 11/9` cells; `rg -n "34 candidate|26 findings|15.*U-" audit_skill_report.md` | All internal numbers agree; no § reference points at a non-existent §; `S-1`/`S-2` appear identically in executive summary, §2.4, Appendix A, and §3.3 matrix | High |
| **A2 — Claim veracity: unified-v3 fossils U-1..U-15** | Each U claim (a) exists in the named source file and (b) is correctly quoted | Re-run the audit's §3.2 Block V1–V7 `rg` citations verbatim against `unified-v3_SKILL.md` + `risen-christ_SKILL.md` + `st-mary-of-angels_SKILL.md` (see §3.2 gate below); for U-10 also `rg -c "^\| [0-9]+ \|"` on §4.3 + `sed -n '/@theme/,/^}/p' \| rg -c "--color-shrine-"` + keyframe list | Every U finding confirmed with `rg -n` line hit; any claim with no hit = **Refuted**; any hit with wrong quote = **Reclassified** (wrong file/line/severity) | Critical |
| **A3 — Claim veracity: rothershrine era fossils R-1..R-6** | Each R claim reproduces in `rothershrine-v2_SKILL.md` | `rg -n "^version:|^package_version:|1\.3\.0|1\.1\.0|1\.0\.0" rothershrine-v2`; `rg -n "45 files|52 files|Two hooks|useScrolled"`; `sed -n '/@theme/,/^}/p' \| rg -c` for 24 colors | All R findings confirmed; R-6 redirect-stub PASS confirmed via `rg -n "Redirect stub|Frozen since"` | Medium |
| **A4 — Claim veracity: auditor-self findings S-1..S-5** | S-1/S-2 (§0 vs §20.3 verbatim) + S-3 round heading + S-4 arithmetic + S-5 ledger completeness | **S-1:** `rg -n "hours 6 keys" SKILL.md` + `sed -n '1192,1200p' SKILL.md \| rg -c "^\s*(gates\|mainChurch\|chapel\|reception\|parishOffice\|mediaCentre\|adorationRoom):"` (expect 7) + §1 row count. **S-2:** `rg -n "mass 11 keys" SKILL.md` + `sed -n '1201,1211p' \| rg -c "^\s*(weekday\|saturday\|sunday\|confession\|adoration\|secondCollection\|note\|monthly):"` (expect 9) + arithmetic `11 − 9 = 2` unexplained. **S-3:** `rg -n "current reality.*round" SKILL.md`. **S-4:** re-sum `4+3+16+5+7+10+8+5+7+7+11+3+6+6+17+7+2+5+3+6+6+4+3+2+3+6+3+2+2+2+4+6+2+13+6` via `python3 -c "print(sum([...]))"` (expect 202) + `11+8+4+4+7+6+8+3` (expect 51) + `rg -c "^\| [0-9]+ \|"` §4.3 (expect 27) + `rg -c "\| z-\[60"` §18 (expect 1) | S-1/S-2 **Confirmed** with dual evidence (§0 text + §20.3 verbatim block + §1 enumeration); S-3 confirmed as Low; S-4 PASS confirmed via arithmetic; S-5 **Grounded** (every G row located) | Critical |
| **A5 — Claim veracity: plan errors P-1..P-3 / D-1..D-5** | P-1/P-2 (errors *inside* REVIEW-PLAN) + D-1..D-5 (UNIFIED-V3-PLAN promise → unified-v3 deliverable gaps) | **P-1:** `rg -n "z-\[60\]\|z-50" REVIEW-PLAN-SKILL-vs-unified-v3.md` + `rg -n "z-\[60\]\|^\|.*Rail" unified-v3_SKILL.md` + `rg -n "^\|.*z-\[60"` unified-v3 (expect 0). **P-2:** `sed -n '/Volatile Facts Register/,/^$/p' SKILL.md \| rg -c "^\|"` vs REVIEW-PLAN's "16 rows" claim + `rg -n "16 rows" REVIEW-PLAN`. **D-1:** `rg -n "Two hooks|Three hooks" unified-v3_SKILL.md` + `UNIFIED-V3-PLAN.md` §3.2 "3 hooks" promise. **D-2:** `rg -n "useScrollSpy|monogram|deepLinks" unified-v3_SKILL.md`. **D-3:** `rg -n "16/92\+35" unified-v3` + `UNIFIED-V3-PLAN.md` D. | Each P/D confirmed/refuted with paired citations (promise line + delivered line); P-1 currently **Confirmed** (unified-v3 has no §18 rail row) | High |
| **A6 — Token & utility register reconciliation** | Audit §3.3 token cells (24+2 → 26+2 → 25+2) + §3.1 V3 utility/keyframe row counts (27/28, 8 vs 6) | For each SKILL/unified/rothershrine: `sed -n '/@theme {/,/^}/p' file \| rg -c -- "--color-shrine-"` (expect 25 / 26 / 24); `rg -n "gold-700|terracotta-600" file`; `rg -c "^\| [0-9]+ \|" file` (§4.3 rows → expect 27/27/~18); `rg -n "drawer-item-in\|page-in\|card-tint\|img-zoom\|bg-gold-bloom" unified-v3` + keyframe prose list vs §0 claim | All three `@theme` counts match audit's trajectory; SKILL 25+2 confirmed byte-true; unified 26+2 superset confirmed; utility/keyframe mismatches confirmed as CONCERN or FAIL per audit's classification | High |
| **A7 — Count-trajectory matrix completeness** | Audit §3.3 matrix row for every volatile fact × every generation (package version, unit tests, E2E, src files, tokens, hours keys, mass keys, hooks) | Rebuild matrix from `rg` outputs: `rg -n "package\.json.*version|1\.3\.0|1\.4\.4|3\.0\.0"` all files; `rg -n "16 files / 92|35 files / 202|32 files / 184"` all files; `rg -n "51 E2E|35 E2E|27 E2E"`; `rg -n "45 files|52 files|77 files"`; `rg -n "hours.*keys|mass.*keys"`; `rg -n "Two hooks|Three hooks"` | No cell "unknown" without stated reason; every cell has a file+line citation; `mass 11` cell marked **Refuted** if verbatim proves 9 is the repo truth | High |
| **A8 — Parish fidelity & leak classification (V5 validation)** | Audit V5: predecessor facts (Oklahoma/Tepeyac, 620 Upper BT, Bukit Batok, `#mandarin`, T08CC4043C/4053H, 4 OFM) outside lineage appendices are leaks | Re-run `rg -n "Oklahoma\|Tepeyac\|620 Upper\|Bukit Batok\|#mandarin\|T08CC4053H\|T08CC4043C\|4 OFM\|Portiuncula" SKILL.md` and classify each hit by section (`rg -n` + manual section bucket: §1/Appendix D/E/F/G vs §§2–20/Quick Ref) | Zero hits outside §1/D/E/F/G in SKILL.md; unified-v3 Parish-X template rows correctly scored as intentional, not leaks; rothershrine era-correct hits confirmed | High |
| **A9 — Config & contract completeness (V6 validation)** | Audit V6: vite test block, `server.watch.ignored`, `playwright.built`, tsconfig 5-entry include, CSP pair contradiction, `src.orig` policy, ssh-key advisory | `rg -n "playwright\.built\|server\.watch\.ignored\|img-src\|repo-hygiene\|src\.orig" SKILL.md unified-v3`; `rg -n "img-src\|wikimedia\|pexels" unified-v3 \| head`; `rg -n "include.*playwright\.built" unified-v3 SKILL.md` | CSP self-contradiction in unified-v3 confirmed: §3.2 "no wikimedia/pexels allowlist" vs §5.5/§9#13 "legacy allowlist retained" — cite both lines; include 4 vs 5 fossil confirmed | High |
| **A10 — Recommendation soundness & severity calibration** | Conditional promotion (SKILL canonical contingent on S-1/S-2 fix) vs alternatives; High vs Critical vs Medium labels per audit §12 taxonomy | Map audit §12 taxonomy definitions onto each Appendix A row; test whether S-1/S-2 meet Critical ("single source of truth with wrong numbers in the register violates ADR-7"); test whether 25+2 vs 26+2 CONCERN is correct vs false FAIL; evaluate alternative: what evidence would flip to "promote unified-v3" or "co-canonical" | Severity re-grades proposed explicitly (e.g., S-1 S-2 High → Critical if ADR-7 is taken literally, else High stands); recommendation upheld, qualified, or overturned with evidence; blockers listed as necessary and sufficient; no ambiguous "either is fine" | Critical |

### 3.2 Reproducible command gate (executed in IMPLEMENT; outputs pasted verbatim into the validation report)

```bash
# — Gate 0: file inventory & line counts (audit §1.3 + §V1)
wc -l SKILL.md unified-v3_SKILL.md rothershrine-v2_SKILL.md risen-christ_SKILL.md st-mary-of-angels_SKILL.md \
      REVIEW-PLAN-SKILL-vs-unified-v3.md UNIFIED-V3-PLAN.md audit_skill_report.md
rg -n "^name:|^display_name:|^version:|^package_version:|^last_updated:|^canonical" \
      SKILL.md unified-v3_SKILL.md rothershrine-v2_SKILL.md risen-christ_SKILL.md st-mary-of-angels_SKILL.md | head -n 40

# — Gate A4 (auditor-self): S-1 / S-2 — the decisive axis
rg -n "hours 6 keys|mass 11 keys" SKILL.md unified-v3_SKILL.md risen-christ_SKILL.md
sed -n '1192,1211p' SKILL.md                          # verbatim site.hours + site.mass (7 + 9 keys)
rg -n "hours 6 keys|hours 7 keys|mass 11 keys|mass 9 keys" SKILL.md risen-christ_SKILL.md unified-v3_SKILL.md
python3 -c "print(sum([4,3,16,5,7,10,8,5,7,7,11,3,6,6,17,7,2,5,3,6,6,4,3,2,3,6,3,2,2,2,4,6,2,13,6]))"  # expect 202
python3 -c "print(11+8+4+4+7+6+8+3)"                  # expect 51 (8 E2E specs)

# — Gate A2/A3: unified-v3 fossils U-1..U-15 + rothershrine R-1..R-6
rg -n "Two hooks|Three hooks" SKILL.md unified-v3_SKILL.md rothershrine-v2_SKILL.md risen-christ_SKILL.md
rg -n "32 files / 184|35 files / 202|16 files / 92|11 files / 67|9/53|25 files/142|25 files / 141" \
      SKILL.md unified-v3_SKILL.md rothershrine-v2_SKILL.md risen-christ_SKILL.md st-mary-of-angels_SKILL.md
rg -n "z-\[60\]|z-50|z-\[100\]" SKILL.md unified-v3_SKILL.md risen-christ_SKILL.md
rg -n "^\|.*z-\[60\]" SKILL.md unified-v3_SKILL.md   # expect SKILL 1, unified 0
rg -n "SafeImage.tsx// src|// src/components/SafeImage" unified-v3_SKILL.md SKILL.md
rg -n "fetchPriority" unified-v3_SKILL.md SKILL.md risen-christ_SKILL.md
rg -n "src\.orig.*inert|src\.orig.*forbidden|repo-hygiene" SKILL.md unified-v3_SKILL.md rothershrine-v2_SKILL.md
rg -n "skills/.*live only|skills/.*git history.*c774ed9" unified-v3_SKILL.md SKILL.md

# — Gate A6: tokens & utilities (§4.3 + @theme + keyframes)
for f in SKILL.md unified-v3_SKILL.md rothershrine-v2_SKILL.md risen-christ_SKILL.md st-mary-of-angels_SKILL.md; do
  echo "== $f"; sed -n '/@theme {/,/^}/p' "$f" | rg -c -- "--color-shrine-"; done   # expect 25 / 26 / 24 / 25 / 25
rg -n "gold-700|terracotta-600|gold-300|terracotta-500" SKILL.md unified-v3_SKILL.md rothershrine-v2_SKILL.md st-mary-of-angels_SKILL.md | head -n 30
rg -n "drawer-item-in|page-in|card-tint|img-zoom|bg-gold-bloom" unified-v3_SKILL.md SKILL.md risen-christ_SKILL.md
rg -c "^\| [0-9]+ \|" SKILL.md unified-v3_SKILL.md rothershrine-v2_SKILL.md  # §4.3 numbered rows → SKILL 27, unified ?, rother ?
rg -n "gold-rule-draw|hero-ken-burns|rise-in|menu-in|drawer-in|halo-pulse|drawer-item-in|page-in" SKILL.md unified-v3_SKILL.md | head -n 40

# — Gate A5: plan errors P-1/P-2 + promise→deliverable D-1..D-5
rg -n "z-\[60\]" REVIEW-PLAN-SKILL-vs-unified-v3.md         # P-1: what the review plan claims about unified-v3
rg -n "16 rows|19 rows|19.*rows" REVIEW-PLAN-SKILL-vs-unified-v3.md audit_skill_report.md
rg -n "Appendix A.*#10|Parity|Same row present" REVIEW-PLAN-SKILL-vs-unified-v3.md
rg -n "Three hooks|3 hooks|useScrollSpy.*tie-break" UNIFIED-V3-PLAN.md | head -n 20
rg -n "16/92\+35|hours 6 keys|columbarium" unified-v3_SKILL.md | head -n 20
rg -n "playwright\.built|server\.watch\.ignored|img-src.*self|as of" SKILL.md unified-v3_SKILL.md REVIEW-PLAN-SKILL-vs-unified-v3.md | head -n 30

# — Gate A8/A9: leaks + CSP self-contradiction + include fossil
rg -n "Oklahoma|Tepeyac|620 Upper|Bukit Batok|#mandarin|T08CC4053H|T08CC4043C|4 OFM|Portiuncula|WOHA|Palladian" \
      SKILL.md unified-v3_SKILL.md | head -n 40
rg -n "img-src|wikimedia|pexels" unified-v3_SKILL.md SKILL.md risen-christ_SKILL.md | head -n 30
rg -n 'include.*playwright\.built|include.*\[.*src' unified-v3_SKILL.md SKILL.md | head -n 20
rg -n "17 Route|5 alias|7 alias|HashRouter|singlefile|twMerge\(clsx|resolveAnchor|preventDefault" \
      SKILL.md unified-v3_SKILL.md risen-christ_SKILL.md | head -n 30

# — Gate A1: audit self-consistency (structure + counts)
rg -n "^## |^# " audit_skill_report.md | head -n 60
rg -n "S-1|S-2|U-14|P-1|D-1|34 candidate|26 findings" audit_skill_report.md | head -n 40
diff <(rg -n "^## " SKILL.md | sed 's/^[0-9]*://') <(rg -n "^## " unified-v3_SKILL.md | sed 's/^[0-9]*://') | head -n 60
```

*Every gate's stdout is pasted verbatim into the validation report's Evidence appendix — no summarization, no "green" without output. Repo-dependent claims (`grep shrine- src/index.css`, `find src | wc -l`, `pnpm test`, `dist/index.html` byte count) get an explicit **Unverifiable** label plus the exact repo-root command that would verify them.*

### 3.3 Manual spot-check checklist (Phase 4 — each checked as Confirmed / Refuted / Reclassified)

- [ ] **S-1 hours** — `SKILL.md` §0 `hours 6 keys` vs §1 enumeration (7 names) vs §20.3 verbatim (7 keys) — reconcile and count `gates/mainChurch/chapel/reception/parishOffice/mediaCentre/adorationRoom`
- [ ] **S-2 mass** — `SKILL.md` §0 `mass 11 keys` vs §20.3 verbatim (9 keys: `weekdayMorning/weekdayEvening/saturday/sunday/confession/adoration/secondCollection/note/monthly`) — confirm 9, explain where 11 came from, recommend fix (9 is the verbatim truth; 11 has no derivation)
- [ ] **S-3/S-4/S-5** — round heading vs §0 date; 35-term sum = 202 / 8-spec sum = 51 / §4.1 25 colors / §4.3 27 rows / §19 25 rows arithmetic
- [ ] **U ledger (15 rows)** — each: locate fossil in unified-v3 at cited §/line, verify resolution present in SKILL.md §/line, check severity vs audit §12
- [ ] **R ledger (6 rows)** — each: locate era fossil in rothershrine-v2, confirm freeze note intact, check triple-version 1.3.0/1.1.0/1.0.0
- [ ] **P-1/P-2** — REVIEW-PLAN App A #10 `z-[60]` row claim vs unified-v3 §18 actual (no row); REVIEW-PLAN "16 rows" vs SKILL §0 actual row count
- [ ] **D-1..D-5** — UNIFIED-V3-PLAN promise lines vs unified-v3 delivered lines (3-hook §6, full tree, App E fossil replacement, line-count 1400–1500, `~` discipline)
- [ ] **Tokens & utilities** — `@theme` byte counts 24/25/26 per file; §4.3 row counts; 28-as-27 convention; 6-vs-8 keyframes; `z-[60]` rail row presence only in SKILL
- [ ] **Leaks** — every `Oklahoma/Tepeyac/620 Upper/Bukit Batok/#mandarin/T08CC4043C/4053H/4 OFM` hit classified by section; Parish-X template rows correctly excluded
- [ ] **Config** — `playwright.built`/`server.watch.ignored`/5-entry include/CSP contradiction/src.orig policy/ssh-key advisory — both files' rows checked
- [ ] **Count-trajectory matrix** — every audit §3.3 cell re-derived from `rg` and verbatim counts; `mass 11` flagged as matrix error if verbatim is 9
- [ ] **Recommendation logic** — does the evidence actually support conditional-promotion of SKILL.md over the alternatives; are S-1/S-2 sufficient blockers; would any single refutation flip the verdict

### 3.4 Success criteria (all must be green to publish the validation report)

| Criterion | Gate |
|---|---|
| All 10 axes scored **PASS / CONCERN-with-rationale / FAIL** with `rg` citation + file + line + severity delta | No Critical/High FAIL left unaddressed or mislabeled |
| Count-trajectory matrix complete — every volatile fact × all 3 generations — no cell "unknown" without a stated reason | No orphan hypotheses |
| Every Appendix A candidate finding (34 rows) resolved: **Confirmed / Refuted / Reclassified** with evidence | Zero orphan rows |
| Audit's Honesty caveat honored — every repo-dependent claim labeled **Unverifiable + command**; every arithmetic claim labeled **Verified** | No "green" without output |
| Validation states **Uphold / Qualify / Overturn** on the audit's conditional-promotion verdict with explicit blockers | No ambiguous recommendation |
| No edit made to any of the 7 files during validation | Read-only |

---

## 4. Phase 3 — VALIDATE: Confirmation Gate

Reply with one of:

| Option | What it triggers |
|---|---|
| **`approve plan as-is`** | I run the 10-axis validation immediately → write `REVIEW-VALIDATION-REPORT-audit_skill_report.md` → VERIFY self-check → handoff. No edits to any SKILL/plan/audit file. |
| **`approve with scope tweak`** | Specify `A1–A5` choices (e.g., "downgrade S-1/S-2 to Medium", "add st-mary vs risen interface diff", "treat 25+2/26+2 as FAIL not CONCERN"); I revise this plan and re-issue before running. |
| **`expand to fix pass`** | I produce the validation report *and then* open a second plan for surgical fixes — first in `SKILL.md` §0 (S-1/S-2 → 7/9 keys plus every §7/§20/QR restatement), then in whichever file the validation confirms as FAIL. Two-phase approval preserved — report first, edits second. |

**Open questions:**

| # | Question | My recommendation |
|---|---|---|
| Q1 | Should S-1/S-2 remain **High** or be escalated to **Critical**? A §0 register that states wrong numbers for the very facts it is defined to be the single source of (ADR-7) arguably violates the governance contract more severely than any fossil it catalogs. | Keep **High** in this validation pass but note **Critical-if-ADR-7-is-literal** as a qualified alternative — the validation report will state both and let the fix-pass decision escalate if desired. |
| Q2 | If the validation confirms S-1 = 7 and S-2 = 9, should the fix be `hours 7 keys / mass 9 keys` in §0 alone, or also hunt every restatement (§7, §5.2, §20, QR) for stale `6/11` copies via G.4? | Both — §0 fix **plus** a G.4 sweep (`rg -n "hours 6 keys|mass 11 keys" SKILL.md`) in the same commit; the validation report will list every restatement line that must move with §0. |
| Q3 | Token verdict: the audit says bless 25+2 (SKILL, byte-true) vs 26+2 (unified superset) as CONCERN-by-design. Should the validation treat that classification as PASS, or re-open it as FAIL if `sed` proves a mismatch? | **Defer to evidence**: `sed` on `@theme` is the tie-breaker. If `src/index.css` were available, byte truth wins; in docs-only, both classifications stand as CONCERN with the audit's rationale upheld. |
| Q4 | Should `risen-christ_SKILL.md` and `st-mary-of-angels_SKILL.md` be treated as ground-truth baselines for this validation, or just as two more lineage members? | **Baselines for V9 lineage invariants** — the audit's V9 already does this; the validation re-uses them to test whether the audit's invariant claims reproduce. |
| Q5 | Fix policy if the validation finds FAILs in the audit report itself (e.g., a U row with no `rg` hit, or a mis-counted §0 row total)? | Report-only in this pass (Mode C discipline). Audit-report corrections become a follow-up commit approved separately — the same discipline the audit imposes on the SKILL files. |

---

## 5. Phase 4 — IMPLEMENT: How the Validation Will Run (After Approval)

1. Execute command gate §3.2 — capture stdout verbatim (or hand the exact commands off if execution is unavailable; nothing is asserted green without output).
2. Read all seven files front-to-back with offset reads (no 50 KB truncation — the G ledger, Appendix F tail, and verbatim `site.ts` live at the tail; `wc -l` already confirms `SKILL.md` 1780 / `unified-v3` 1438 / `rothershrine` 1337 / `risen` 1427 / `st-mary` 1393 / `audit` 296).
3. Score A1–A10; fill the count-trajectory matrix (§3.3) with file+line citations.
4. Confirm / refute / reclassify all 34 Appendix A candidate findings + 5 plan deltas; classify V8 leaks by section bucket.
5. Diff the immutable contracts (A9 lineage invariants: §4 `@theme`, §5.4 routing, §9 anti-patterns, §15 patterns) across the 3 generations to test whether the audit's "no regression" claims reproduce.
6. Adjudicate intentional divergences (25+2 vs 26+2; 27 vs 28 utilities; 6 vs 8 keyframes) as CONCERN-with-rationale, not FAIL, with `sed`/`rg -c` as tie-breakers.
7. Draft the validation report — **no edits to any SKILL, plan, or audit file.**

---

## 6. Phase 5 — VERIFY: Iron Law

- [ ] Every axis A1–A10 has a verdict + evidence citation (file + `rg -n` line) + severity delta + which file/claim is ahead.
- [ ] Every Appendix A row (34 + 5) resolved: Confirmed / Refuted / Reclassified (with corrected line/severity/file if reclassified).
- [ ] Command outputs pasted verbatim in Evidence appendix (or exact commands handed off with the reason, labeled Unverifiable).
- [ ] No edit made to any of the 7 files.
- [ ] Validation states **Uphold / Qualify / Overturn** on the audit's conditional-promotion recommendation with explicit blockers.
- [ ] Repo-dependent claims labeled Unverifiable with the exact command; arithmetic claims labeled Verified with re-sum.

---

## 7. Phase 6 — DELIVER: Report & Recommendation

| Deliverable | Path | Content |
|---|---|---|
| **Validation report** | `REVIEW-VALIDATION-REPORT-audit_skill_report.md` | 10-axis scoring; count-trajectory matrix re-derived; confirmed fossil inventory (per file, severity-ordered); per-claim Confirmed/Refuted/Reclassified ledger; head-to-head deltas; recommendation verdict on the audit's conditional-promotion thesis (Uphold / Qualify / Overturn) + blockers |
| **Evidence appendix** | Inside the report | Verbatim `rg`/`wc`/`diff`/`sed`/`python3` outputs |
| **Fix plan (only if `expand to fix pass`)** | Separate approval | Surgical set: `SKILL.md` §0 S-1/S-2 (hours 6→7, mass 11→9) + every restatement line found by `rg -n "hours 6 keys|mass 11 keys"`, plus any other confirmed FAILs det... | 
| **No SKILL edit** | — | Findings become a surgical follow-up commit approved separately |

Suggested commits (docs-only, read-only until report delivery):

```bash
# this plan
git add new-skills/REVIEW-VALIDATION-PLAN-audit_skill_report.md
git commit -m "docs(plan): add validation plan for audit_skill_report.md — 10-axis audit-of-the-auditor, rg-gated"

# after Phase 4 (no file edit)
git add new-skills/REVIEW-VALIDATION-REPORT-audit_skill_report.md
git commit -m "docs(validation): 10-axis validation of audit_skill_report.md — <verdict: uphold|qualify|overturn>"
```

---

## 8. Appendix A — Claim Inventory to Validate (the 34 + 5 the audit already catalogs, plus where to look)

*Severity and confidence per audit §12 taxonomy. This validation re-derives each from the source text; a row with no `rg` hit is **Refuted**, a row with a hit but wrong ± is **Reclassified**.*

### A.1 Unified-v3 fossils U-1..U-15 (audit §8.1 — mostly pre-cataloged by SKILL App G)

| # | Audit location | Audit finding | Where to `rg` | Expected hit | Severity |
|---|---|---|---|---|---|
| U-1 | unified §6 | "Status: **Two hooks**" while §2/§11 list `hooks/useScrollSpy (6 tests)` and Quick Ref lists 3 hooks | `rg -n "Two hooks|Three hooks|useScrollSpy" unified-v3` | `Two hooks` at §6 + `useScrollSpy (6)` at §2/§11 + 3-hook QR | High |
| U-2 | unified §5.2 tree | Missing `hooks/useScrollSpy.ts`, `utils/monogram.ts`, `utils/deepLinks.ts` despite test list naming them | `rg -n "useScrollSpy|monogram|deepLinks" unified-v3` §5.2 tree block | Expect 0 hits in tree, ≥1 in test list | High |
| U-3 | unified §10 | "should be **32 files / 184 tests**" vs 35/202 everywhere else | `rg -n "32 files / 184|35 files / 202" unified-v3 SKILL.md` | unified §10 row = 32/184; SKILL §10 = 35/202 (§0) | High |
| U-4 | unified §18 | No `z-[60]` ScrollProgress row, though §5.2/§5.5 specify it; conflict rule ignores the rail | `rg -n "^\|.*z-\[60" unified-v3 SKILL.md` | SKILL 1, unified 0 | Med |
| U-5 | unified §20.3 | Duplicated `// src/components/SafeImage.tsx` comment; `SafeImageProps` lacks `fetchPriority` that §5.5 documents | `rg -n "SafeImage.tsx// src|fetchPriority" unified-v3 SKILL.md` | unified has dupe comment + no fetchPriority; SKILL has single + fetchPriority? | Med |
| U-6 | unified App C | "harness is green (**25 files/142 + 48 E2E**)" vs 35/202+51 | `rg -n "25 files/142|48 E2E|35 files / 202" unified-v3` App C/E | App C = 25/142+48 vs §2 = 35/202 | Med |
| U-7 | unified App F | Round-7-era snapshot: package **1.3.0**, **32/179+48** tests, St Mary tokens "**24+2**" (St Mary round-7 was 26+2) | `rg -n "1\.3\.0|32/179|24\+2|26\+2" unified-v3` App F + `st-mary` @theme | F says 1.3.0/32-179+48/24+2; cross-check st-mary | Med |
| U-8 | unified §13 | "`src.orig/` … inert guards" vs §2/Quick Ref (pruned round-12 + `repo-hygiene` guard) | `rg -n "src\.orig.*inert|src\.orig.*pruned|repo-hygiene" unified-v3 SKILL.md` | unified §13 says inert, §2 says pruned+guard | High |
| U-9 | unified §14 | `skills/` "live only in git history at `c774ed9`" vs §2 (re-added in full, `0be0fe8`) | `rg -n "c774ed9|0be0fe8|skills.*live only" unified-v3 SKILL.md` | unified §14 stale, SKILL §2 corrected | Med |
| U-10 | unified §4.3 | Keyframes prose lists **6** vs "8" claim; utility table lacks `drawer-item-in`/`page-in`/`card-tint`/`img-zoom`/`bg-gold-bloom` vs its own 27+8 claim | `rg -c "^\| [0-9]+ \|" unified-v3 SKILL.md` + `rg -n "drawer-item-in|page-in|card-tint|img-zoom|bg-gold-bloom" unified-v3` + keyframe `rg` | unified has fewer rows / missing utils | High |
| U-11 | unified §5.2 comments | "images export (11 keys, **3 CDN**)", "hours(**5**)", "mass(**7**)" vs §7 (all-local, 7 hours keys, 9+ mass keys) | `rg -n "11 keys.*3 CDN|hours\(5\)|mass\(7\)" unified-v3 SKILL.md` | Comments stale vs §7 all-local + hours 6/7 + mass 9/11 | Med |
| U-12 | unified §12 L9/L10 | CDN-era "CSP extended to upload.wikimedia.org"; "Rewritten to Bukit Batok St Mary … 35 green (2026-08-28)" | `rg -n "wikimedia|Bukit Batok.*35 green" unified-v3` | Stale CDN + stale date | Low |
| U-13 | unified §3.2 vs §5.5/§9#13 | CSP self-contradiction: "no wikimedia/pexels allowlist" vs "legacy allowlist retained" | `rg -n "img-src|wikimedia|pexels" unified-v3 \| head -20` | Both lines present, contradictory | Med |
| U-14 | unified §10/§13 | tsconfig include lists **4 entries** vs §3.2's 5 (missing `playwright.built.config.ts`) | `rg -n "include.*\[.*playwright\.built|include.*\[.*src" unified-v3 SKILL.md` | unified 4, SKILL 5 | Low |
| U-15 | unified App D.4 | "Do not delete it" vs Quick Ref "removed from tree + index" | `rg -n "Do not delete|removed from tree" unified-v3 SKILL.md` | Opposite instructions | Med |

### A.2 Rothershrine era fossils R-1..R-6 (audit §8.2 — catalog, don't fix; file is a frozen stub)

| # | Audit location | Audit finding | Where to `rg` | Expected hit |
|---|---|---|---|---|
| R-1 | rothershrine fm/§2/App D | Triple version: **1.3.0** (fm) / **1.1.0** (§2) / **1.0.0** (App D) | `rg -n "^version:|1\.3\.0|1\.1\.0|1\.0\.0" rothershrine-v2` | 3 versions |
| R-2 | rothershrine §5.2 | Heading "**45 files** (33+11+1)" vs counts line "**52** (35+16+1)" | `rg -n "45 files|52 files" rothershrine-v2` | Both in §5.2 |
| R-3 | rothershrine §11 | Three count generations in one section: 11/67+27 → 9/53+22 → 16/92+35; E2E 27↔35↔22 | `rg -n "11/67|9/53|16/92|27 E2E|35 E2E|22 E2E" rothershrine-v2` | 3 generations |
| R-4 | rothershrine §6/§5.2 | "Two hooks" but tree lists only `useScrolled.ts`; `useScrollProgress` proven by test list, absent from tree | `rg -n "Two hooks|useScrolled|useScrollProgress|useScrollSpy" rothershrine-v2` | Two hooks text, one in tree |
| R-5 | rothershrine §3.2/QR/§4.3 | Utilities "**24**" vs "**22** + 6 keyframes" vs ~17 table rows | `rg -c "^\| [0-9]+ \|" rothershrine-v2` + `rg -n "24 utilities|22.*keyframe" rothershrine-v2` | Inconsistent |
| R-6 | rothershrine file-name note | Redirect-stub freeze instruction present (PASS) | `rg -n "Redirect stub|do not edit" rothershrine-v2` | PASS |

### A.3 Auditor-self findings S-1..S-5 (audit §8.3 — the decisive set; auditing the auditor)

| # | Audit location | Audit finding | Where to `rg` | Expected hit |
|---|---|---|---|---|
| **S-1** | SKILL §0+§1 vs §20.3 | Register says "hours **6 keys**"; §1 enumerates 7 names; §20.3 verbatim defines **7** (`gates/mainChurch/chapel/reception/parishOffice/mediaCentre/adorationRoom`) | `rg -n "hours 6 keys" SKILL.md` (3 hits) + `sed -n '1192,1200p' SKILL.md` (count 7) | **Audit confirmed on spot-check** — validation re-proves with dual evidence |
| **S-2** | SKILL §0+§7.1 vs §20.3 | Register says "mass **11 keys**"; verbatim `mass` defines **9** (`weekdayMorning/weekdayEvening/saturday/sunday/confession/adoration/secondCollection/note/monthly`) | `rg -n "mass 11 keys" SKILL.md` + `sed -n '1201,1211p'` (count 9) | **Audit confirmed** — no derivation for 11 |
| S-3 | SKILL §2 heading | "current reality (2026-08-31, **round-6** verified)" vs §0 "as of … **round-12**" | `rg -n "current reality.*round|as of.*round" SKILL.md` | Consistent or Low fossil |
| S-4 | SKILL §0 sums | 35-term unit breakdown → 202; E2E 11+8+4+4+7+6+8+3 = 51; §4.1 = 25 colors; §4.3 = 27 rows | `python3 -c "print(sum([...]))"` + `rg -c "^\| [0-9]+ \|" SKILL.md §4.3` + `rg -c "--color-shrine-" SKILL.md` @theme | PASS |
| S-5 | SKILL App G | All 26 claimed resolutions must be located in SKILL body | `rg -n "Appendix G\|Fossil-Sweep\|ADR-7\|L13" SKILL.md` + per-finding G row → body line | Method step |

### A.4 Plan errors P-1..P-3 / D-1..D-5 (audit §8.4 — audit targets the two plans themselves per Q4)

| # | Audit location | Audit finding | Where to `rg` |
|---|---|---|---|
| P-1 | REVIEW-PLAN App A #10 | Claims unified-v3 §18 "Same row present (post-audit) — Parity"; unified-v3 §18 has **no** `z-[60]` row | `rg -n "z-\[60\]\|Same row present\|Parity" REVIEW-PLAN unified-v3` |
| P-2 | REVIEW-PLAN §2.2 | "§0 … (16 rows)"; actual §0 table has **19 rows** (parenthetical lists 18) | `rg -n "16 rows" REVIEW-PLAN` + `rg -c "^\|.*\|" SKILL.md` §0 |
| P-3 | REVIEW-PLAN §2.1 | Line counts 1590/1438 | `wc -l SKILL.md unified-v3` vs claim |
| D-1 | UNIFIED-V3-PLAN §3.2 → unified §6 | Plan promised "3 hooks fences … `useScrollSpy` tie-break"; delivered "**Two hooks**" | `rg -n "3 hooks|Two hooks|useScrollSpy" UNIFIED-V3-PLAN.md unified-v3` |
| D-2 | UNIFIED-V3-PLAN §3.2 → unified §5.2 | Missing 3 files (U-2) — full tree promised | `rg -n "useScrollSpy|monogram|deepLinks" UNIFIED-V3-PLAN.md unified-v3` |
| D-3 | UNIFIED-V3-PLAN §2.4 C-2 → unified App E | Plan: "replace fossil" `16/92+35`; still carries it (labeled "at time of audit") | `rg -n "16/92" unified-v3` + `rg -n "C-2|replace fossil" UNIFIED-V3-PLAN.md` |
| D-4 | UNIFIED-V3-PLAN §3.1 → unified length | Promised 1400–1500 lines | `wc -l unified-v3` → 1438 (PASS, within range) |
| D-5 | UNIFIED-V3-PLAN decision C → unified practice | `~` shorthand + prose restatements quantified | `rg -n "machine-asserted|~35/202" unified-v3` |

*P-3/D-4 are expected PASS (line counts are now `SKILL 1780 / unified 1438 / rother 1337 / risen 1427 / st-mary 1393` — the audit's 1590 figure is stale; the validation will note the drift as a reclassification, not a refutation of the method).*

---

## 9. Appendix B — Evidence Map (which file proves or refutes each audit claim)

| Audit claim family | Primary evidence file(s) | Supporting file(s) | Ground-truth baseline (if needed) |
|---|---|---|---|
| S-1/S-2 (auditor §0 vs verbatim) | `SKILL.md` — §0 table + §1 parish constants + §20.3 `site as const` verbatim (lines 1192–1211) + §5.2 site.ts comment | `risen-christ_SKILL.md` same verbatim block (identical 7+9) | Repo `src/data/site.ts` would be the byte tie-breaker — **Unverifiable** here |
| S-4 sums | `SKILL.md` §0 breakdown string + §4.1 tokens + §4.3 rows | `python3` re-sum | — |
| U-1..U-15 | `unified-v3_SKILL.md` — §§6/5.2/10/18/20.3/App C/F + §3.2/§13/§14/§4.3/§5.2 comments/§12 | Cross-check `SKILL.md` resolution at cited § + `risen-christ` / `st-mary` for era values | `risen-christ` 25 colors baseline; `st-mary` gold-700 baseline |
| R-1..R-6 | `rothershrine-v2_SKILL.md` — fm/§2/App D + §§5.2/6/3.2/QR | `st-mary-of-angels_SKILL.md` for 24→25→26 token trajectory context | — |
| P-1/P-2/P-3 | `REVIEW-PLAN-SKILL-vs-unified-v3.md` — §2.2 + Appendix A #10 | `SKILL.md` §0 actual rows + `unified-v3_SKILL.md` §18 actual rows | — |
| D-1..D-5 | `UNIFIED-V3-PLAN.md` — §3.2 decisions A–F + §2.4 C-2 + §3.1 line target | `unified-v3_SKILL.md` delivered §§6/5.2/10/18/App E | — |
| Token/utility 25+2 vs 26+2, 27 vs 28, 6 vs 8 keyframes | All SKILL files — `sed -n '/@theme/,/^}/p' \| rg -c "--color-shrine-"` + `rg -c "^\| [0-9]+ \|"` + keyframe lists | `src/index.css` byte truth — **Unverifiable** (no repo) — labeled as such | — |
| Leaks (V5) | All SKILL files — `rg "Oklahoma|Tepeyac|620 Upper|Bukit Batok|#mandarin|T08CC...` | Section-classification pass | — |
| Config (V6) | All SKILL files — `rg "playwright.built|server.watch.ignored|img-src|include"` | — | — |
| Invariants (V9) | `risen-christ_SKILL.md` — 77/35/202/51/397.52/17/5/7/9/HashRouter/singlefile | `st-mary` + `rothershrine` for trajectory | — |

---

## 10. Appendix C — Risk Register

| Risk | Likelihood | Impact | Mitigation in this validation |
|---|---|---|---|
| **S-1/S-2 get buried as "low count pedantry"** | High | High — the canonical doc's register is wrong | A4 is a Critical axis; validation verdict makes §0 fix a promotion *blocker*, not a footnote, and lists every restatement line that must move |
| **Token count false-FAIL** (25 vs 26 flagged as drift when it's deliberate) | High | High — blocks a correct promotion | Classify as CONCERN-with-rationale in A6, not FAIL; `sed` byte count is the tie-breaker when repo is available; both designs documented |
| **No `src/` repo → count claims unverifiable** | Certain | Medium | Every such claim labeled **Unverifiable + exact command** (`grep shrine- src/index.css`, `find src | wc -l`, `pnpm test`); document-internal claims labeled **Verified at text level** |
| **50 KB truncation hides the G ledger / verbatim tail** | High | High — 26 findings unread | Offset reads in Phase 4 (`sed -n '1192,1211p'`, `sed -n '1400,1800p'`) + `rg "Appendix G"` gate; `wc -l` proves SKILL is 1780 lines, not the audit's stale 1590 |
| **REVIEW-PLAN's own errors propagate into validation (P-1)** | Medium | Medium | This plan supersedes affected deltas; App A #10 explicitly corrected before A5 runs |
| **Scope creep into editing** | Medium | Medium | Iron law: read-only; fixes gated behind second approval (`expand to fix pass`) — same discipline the audit imposes |
| **Reviewer fatigue at 3×1400-line corpus + audit report** | Medium | Low | Appendix A inventory + count-trajectory matrix + `rg` gate focus reading; tails read via offset passes |
| **Stale line-count claims in the audit** (audit says SKILL 1590, actual 1780; says REVIEW-PLAN 16 rows, actual 19) | Medium | Low — reclassification, not refutation | A1 self-consistency axis explicitly re-derives `wc -l` and `rg -c "^\|"` to reclassify without overturning the method |

---

## Next Step — Awaiting Your Confirmation (VALIDATE)

Reply **`approve plan as-is`** to run the 10-axis validation now → `REVIEW-VALIDATION-REPORT-audit_skill_report.md` → self-check → handoff. **No file beyond this plan will be written until you validate.**

Alternatives: **`approve with scope tweak`** (specify A1–A10 / Q1–Q5 tweaks) or **`expand to fix pass`** (report now + surgical fix plan after).

*Pre-staged evidence on this read (text-level Verified): S-1 hours 7 vs 6 **Confirmed**, S-2 mass 9 vs 11 **Confirmed**, P-1 REVIEW-PLAN App A #10 `z-[60]` **Confirmed false** (unified-v3 has zero §18 rail row), U-4 no `z-[60]` **Confirmed**. All other U/R/P/D/S rows remain **Pending** until the full `rg` gate runs in Phase 4.*

