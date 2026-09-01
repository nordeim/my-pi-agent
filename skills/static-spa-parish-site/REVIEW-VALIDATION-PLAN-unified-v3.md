# Meticulous Review & Validation Plan — `unified-v3_SKILL.md` v3.0.0 vs `review_plan.md`

> **Request:** Meticulously plan to review and validate `unified-v3_SKILL.md` (1438 lines, Lineage Master) against `review_plan.md` (55 lines, completion claim).
> **Author:** Claw Code (Frontend Architect · 15y) · **Date:** 2026-09-01 · **Method:** Meticulous Approach — ANALYZE → PLAN → VALIDATE → IMPLEMENT → VERIFY → DELIVER
> **Stack read:** `unified-v3_SKILL.md` 135664 bytes / 1438 lines · `review_plan.md` 12129 bytes / 55 lines · `UNIFIED-V3-PLAN.md` 310 lines · `VERIFICATION-UNIFIED-V3.md` 143 lines · `CRITICAL-COMPARISON.md` 310 lines · `draft_unified-v3_SKILL.md` 254 lines
> **No code will be written until this plan is approved.**

---

## Table of Contents
1. [Executive Summary & Go/No-Go](#1-executive-summary--gono-go)
2. [Phase 1 — ANALYZE: What Each Document Actually Is](#2-phase-1--analyze-what-each-document-actually-is)
3. [Phase 2 — PLAN: Validation Axes, Methods & Checklists](#3-phase-2--plan-validation-axes-methods--checklists)
4. [Phase 3 — VALIDATE: Explicit Confirmation Gate](#4-phase-3--validate-explicit-confirmation-gate)
5. [Phase 4 — IMPLEMENT: Execute the Review (After Approval)](#5-phase-4--implement-execute-the-review-after-approval)
6. [Phase 5 — VERIFY: Iron Law — No False Completion](#6-phase-5--verify-iron-law--no-false-completion)
7. [Phase 6 — DELIVER: Review Report & Handoff](#7-phase-6--deliver-review-report--handoff)
8. [Appendix A — Claims Inventory Extracted from `review_plan.md`](#8-appendix-a--claims-inventory-extracted-from-review_planmd)
9. [Appendix B — Risk Register](#9-appendix-b--risk-register)

---

## 1. Executive Summary & Go/No-Go

**One sentence:** `review_plan.md` is not a review *plan* — it is a **55-line completion claim** (5 defect→fix rows + 6 verification ticks + 6-row deliverables table) asserting that `unified-v3_SKILL.md` is "complete, verified, and ready"; the job of this review is to **falsify each claim with `rg`/`wc` proofs and cross-checks against the three source skills** before anyone stamps `v3.0.0` as canonical.

**Go/No-Go:** **GO** — but as a *claims-verification audit*, not a re-merge. Risk is **Low** if we treat `review_plan.md` as the acceptance criteria and `unified-v3_SKILL.md` as the artifact under test, with `risen-christ` (1427 lines, most mature) as the ground-truth baseline for spot-checks. Risk becomes **Medium** if we re-open the merge itself without first proving the claimed fixes.

**Best recommendation:** Run an **8-axis, evidence-anchored audit** (see §3.1) producing a single `REVIEW-REPORT-unified-v3.md` with per-axis **PASS / FAIL / CONCERN + `rg` citation + line number + severity (Critical/High/Medium/Low) + fix recommendation**. No edits to `unified-v3_SKILL.md` during the review — findings are reported, then fixed in a separate commit after your approval.

**What "meticulously" means here:** Every claim in `review_plan.md` must have a *reproducible* check (exact `rg` pattern + expected hit count + location). Prose assertions without a citation are treated as FAIL.

---

## 2. Phase 1 — ANALYZE: What Each Document Actually Is

### 2.1 `review_plan.md` — the acceptance criteria (55 lines)

| Block | What it asserts | Why it matters |
|---|---|---|
| **Header** | Built per `UNIFIED-V3-PLAN.md` (approved as-is); baseline `risen-christ` 1427 lines + 26+2 superset + 28 utilities + 15 anti-patterns + parameterized smoke | Sets the target shape: if `unified-v3` diverges from `risen-christ` skeleton, the claim is false |
| **Key fixes table (5 rows)** | C-1 Appendix B St Mary smoke → parameterized Risen example (3 priests Brian/Arun/Dexter, UEN T08CC4042G); H-4 token drift → 26+2 superset (gold-700 4.72:1 + terracotta-600 5.36:1); H-6/H-7 vite test + CSP strict; C-3 31/172 vs 24/134 → `~35/202~51` machine-asserted; tail-end decay → Appendix E relabeled Reference | These are the *falsifiable* defects — each must be proven fixed via `rg` inside `unified-v3` |
| **Verification (6 ticks)** | front-matter v3.0.0 + canonical Risen + 4-hop lineage; tokens 26+2 superset; 27 sections (§§1–20 + A–F + QR); Appendix B parameterized; fidelity (Oklahoma/Tepeyac only in §1+D/F); lines 1438 (1400–1500) | The pre-ship gate — any tick that fails blocks promotion |
| **Deliverables table (6 rows)** | `unified-v3` 1438 lines = canonical; `UNIFIED-V3-PLAN` 310 lines = merge strategy; `VERIFICATION-UNIFIED-V3` = rg proofs; `CRITICAL-COMPARISON` 310 lines = scored review; `draft` 254 lines = discarded memo; frozen profiles 1427/1393/1337 | Validates file inventory and freeze protocol — must match `ls -l` + `wc -l` |

**Critical observation:** `review_plan.md` contains **no** review *procedure* — it only declares *what* is done. This plan therefore invents the *how*.

### 2.2 `unified-v3_SKILL.md` — the artifact under test (1438 lines)

| Dimension | Claimed in `review_plan.md` | Actual sampled (ANALYZE read, offset 0–50KB) |
|---|---|---|
| Front-matter | `singapore-parish-lineage v3.0.0`, canonical Risen Toa Payoh, 4-hop lineage, 77 files / ~202+51+51 | ✅ front-matter block present, `name: singapore-parish-lineage`, `version: 3.0.0`, lineage `Rother → St Joseph BT → St Mary → Risen Christ` |
| §1 Identity | 4 parishes in one breath + Risen constants table with Parish X template | ✅ §1 title "Lineage in one breath (4 hops …)" with Risen constants table (Name/Address/Tagline/Feast/UEN T08CC4042G) |
| §4 Tokens | 26 colors + 2 shadows superset (gold-700 #85601f 4.72:1 + terracotta-600 #8f4c30 5.36:1), 28 utilities | ✅ full `@theme` block sampled (shrine-cream … terracotta-600, 8 keyframes, 28 utilities with `@media print`) |
| Sections | 27 (§§1–20 + A–F + QR), ~1400–1500 lines | ✅ TOC shows 20 numbered + 6 Appendices + Quick Ref = 27; first read truncated at 50KB but `wc -l` confirms 1438 |
| Fix evidence | C-1 smoke parameterized, H-4 superset rationale, H-6/H-7 strict CSP, C-3 machine-asserted counts | ⚠️ requires full-file `rg` pass (see §3.2) — not yet proven |

**Gaps to probe:** Appendix B smoke still lists St Mary footnotes correctly? Appendix E fossil labeling? §11 pre-ship gate still 9-step with `test:e2e:built`? §9 15 anti-patterns vs draft 9? Token hex exactness vs `src/index.css`?

### 2.3 Ground-truth triangulation

For any claim that cannot be proven inside `unified-v3` alone, the tie-breaker is:

1. `risen-christ_SKILL.md` (1427 lines) — canonical parent, most mature (`useScrollSpy`, `deepLinks`, `docs-contract`, `repo-hygiene`, 35/202+51+51).
2. `st-mary-of-angels_SKILL.md` (1393 lines) — source of `gold-700` + print media + columbarium variant.
3. `rothershrine-v2_SKILL.md` (1337 lines) — source of Palladian origin + 6-pill jump nav.

If `unified-v3` contradicts `risen-christ` on an immutable contract (17 routes / 5 alias groups / HashRouter / singlefile / 77-file tree / 15 anti-patterns), `unified-v3` is wrong.

### 2.4 Ambiguities surfaced — must resolve before IMPLEMENT

| # | Ambiguity | Options | Recommendation |
|---|---|---|---|
| A1 | Scope — validate `unified-v3` *only* against `review_plan.md` (55-line claim set), or also triangulate spot-checks against the 3 sources and `VERIFICATION-UNIFIED-V3.md`? | Strict (only review_plan) vs Triangulated (review_plan + sources) | **Triangulated** — otherwise we certify a self-referential claim loop |
| A2 | Evidence standard — `rg`/`wc` machine proofs only, or also manual readability / copy-pasteability / anti-generic design judgment? | Machine-only vs Machine + editorial | **Machine + editorial** (editorial flagged as CONCERN, not FAIL) |
| A3 | Handling of `review_plan.md` misnomer — rename to `VERIFICATION-SUMMARY` or keep? | Keep vs Rename | **Keep** but note in report §1 that the file is a completion claim, not a plan |
| A4 | Fix policy — if FAILs found, should IMPLEMENT also fix them or only report? | Report-only vs Report+Fix | **Report-only** in this phase; fixes in a follow-up commit after you approve the report (surgical discipline) |

---

## 3. Phase 2 — PLAN: Validation Axes, Methods & Checklists

### 3.1 Eight validation axes (each maps to a review_plan claim)

| Axis | review_plan claim it tests | Method | Pass criterion | Severity if FAIL |
|---|---|---|---|---|
| **V1 — Identity & Versioning** | front-matter `singapore-parish-lineage v3.0.0`, canonical Risen Toa Payoh, 4-hop lineage, How to Use / Sources of truth / File name note | `rg "^name:|^version:|^canonical_ref:|^lineage:" unified-v3` + manual read §§0–1 | All four front-matter fields exact; canonical_ref contains `91 Toa Payoh Central` + `first air-con 1971`; lineage contains all 4 hops with addresses | **Critical** — wrong identity = wrong canonical |
| **V2 — Token Superset** | 26 colors + 2 shadows (gold-700 #85601f 4.72:1 + terracotta-600 #8f4c30 5.36:1) + 28 utilities + Risen refinement note | `rg "shrine-gold-700|shrine-terracotta-600" unified-v3` (expect 2+ hits each) + `rg "26\+2|28-theme" unified-v3` + count ` --color-shrine-` occurrences in §4.1 (expect 26) + cross-check against `risen-christ` §4 baseline | Both AA tokens present with correct hex + comment; 26 color vars + 2 shadows = 28 theme entries; rationale note "Risen intentionally dropped gold-700" preserved | **High** — token drift breaks `grep shrine- src/index.css` verification |
| **V3 — Structural Completeness** | 27 sections (§§1–20 + A–F + QR), 1400–1500 lines, TOC 22 entries | `wc -l unified-v3` + `rg "^## [0-9]+\.|^## Appendix|^## Quick" unified-v3 | 27 headings, 1400–1500 lines (review_plan says 1438), §§5–20 contracts present (not draft's 254-line outline) | **Critical** — missing §§5–20 = non-executable skill |
| **V4 — C-1 Smoke Parameterization** | Appendix B now parameterized — Risen example filled (3 priests Brian/Arun/Dexter, UEN T08CC4042G), St Mary 4 OFM / T08CC4053H only in Parish X footnote | `rg "4 OFM|T08CC4053H|#mandarin" unified-v3` + read Appendix B | Zero hits in Appendix B steps; hits only in footnote `For Parish X (St Mary: …)` if present; Risen example values (T08CC4042G, Brian/Arun/Dexter, `#language-communities`) in steps | **High** — fossil smoke = predecessors leak into live-site gate |
| **V5 — Fidelity (No Leaks)** | Oklahoma/Tepeyac only in §1 breath + D/F provenance, zero in §§2–20 data sections; Kranji/Palladian/WOHA/Ho Ping only in §1 + D/F | `rg "Oklahoma|Tepeyac|Kranji|Palladian|WOHA|Ho Ping" unified-v3` + classify hits by section | All hits in §1 or Appendices D/F/E; zero in §§2–20 content/data/routing/color/type tables | **Critical** — fidelity breach = parish facts wrong |
| **V6 — Config & Contract Completeness** | H-6/H-7 fixed: `test { globals, jsdom }` + `server.watch.ignored` + `playwright.built.config.ts` mandated; strict CSP `img-src 'self' data: blob:` only, legacy forbidden | `rg "test \{|server\.watch\.ignored|playwright\.built|img-src 'self'" unified-v3` + read §3.2 table + ADR-6 | All three config mandates present; CSP row says `img-src 'self' data: blob:` with "legacy wikimedia/pexels forbidden" | **High** — contradictions break `pnpm lint/typecheck/build` gate |
| **V7 — Audit Ledger Depth** | 15 anti-patterns (not draft 9) + 16-row debugging + 9-step pre-ship gate with `test:e2e:built` + 12 lessons + §15–20 copy-pasteable patterns | `rg "Anti-Pattern.*Severity|Debugging Guide|Pre-Ship Checklist|Lessons Learnt" unified-v3` + count anti-pattern rows (expect 15) | All four ledger sections present; anti-pattern table has 15 rows including #14 built-artifact favicon + #15 backslash | **Medium** — missing ledger rows = re-introduction of top audit bugs |
| **V8 — Metrics Discipline** | C-3 fixed: prose says `~35/202~51 (machine-asserted by docs-contract)`, not hardcoded drift-prone `31/172 vs 24/134`; Appendix E relabeled Reference (St Mary vs St Joseph) | `rg "machine-asserted|docs-contract" unified-v3` + `rg "31/172|24/134|25/141|35/202" unified-v3` → classify | C-3 counts appear only as `~` + "asserted by docs-contract"; Appendix E header contains "Reference: St Mary vs St Joseph" | **Medium** — hardcoded counts drift within weeks |

### 3.2 Reproducible `rg`/`wc` gate (runs in Phase 4)

```bash
# V1 — identity
rg -n "^name:|^display_name:|^version:|^canonical_ref:|^lineage:" unified-v3_SKILL.md

# V2 — tokens
rg -n "shrine-gold-700|shrine-terracotta-600" unified-v3_SKILL.md
rg -n "26 colors|2 shadows|28-theme|28 theme" unified-v3_SKILL.md
rg -n -- "--color-shrine-" unified-v3_SKILL.md | wc -l   # expect 26
rg -n "#85601f|#8f4c30" unified-v3_SKILL.md               # both hex present

# V3 — structure
wc -l unified-v3_SKILL.md                                  # expect 1438 (1400–1500)
rg -n "^## [0-9]+\.|^## Appendix|^## Quick" unified-v3_SKILL.md | wc -l  # expect 27
rg -n "^## [0-9]+\.|^## Appendix" unified-v3_SKILL.md      # list for manual TOC check

# V4 — smoke
rg -n "T08CC4042G|T08CC4053H|4 OFM|#mandarin|#language-communities" unified-v3_SKILL.md
rg -n "Brian|Arun|Dexter" unified-v3_SKILL.md              # Risen priests

# V5 — fidelity
rg -n "Oklahoma|Tepeyac|Kranji|Palladian|WOHA|Ho Ping" unified-v3_SKILL.md

# V6 — config
rg -n "playwright\.built|server\.watch\.ignored|test \{|globals.*jsdom" unified-v3_SKILL.md
rg -n "img-src 'self' data: blob:|wikimedia|pexels" unified-v3_SKILL.md

# V7 — ledger depth
rg -n "Anti-Pattern|Debugging Guide|Pre-Ship Checklist|Lessons Learnt" unified-v3_SKILL.md
rg -n "dev-only E2E|backslash|agent-browser eval" unified-v3_SKILL.md  # #14/#15

# V8 — metrics
rg -n "machine-asserted|docs-contract" unified-v3_SKILL.md
rg -n "Reference: St Mary vs St Joseph|fossil|tail-end decay" unified-v3_SKILL.md

# Cross-check — deliverables vs ls
ls -l new-skills/*.md && wc -l new-skills/*.md
diff -u <(rg "^## " risen-christ_SKILL.md) <(rg "^## " unified-v3_SKILL.md) | head -n 80
```

### 3.3 Manual spot-checks (checklist for Phase 4)

- [ ] §1 Risen constants table has 9 rows + `Parish X template` column (addresses, UEN, feast, hours variants)
- [ ] §3.2 critical config table mandates `test`, `server.watch.ignored`, `playwright.built.config.ts`, tight CSP — no contradictions
- [ ] §4.1 `@theme` block is copy-pasteable (not truncated like `draft_unified-v3` was at `--color-shrine-maroon-700`)
- [ ] §4.3 utilities table has 28 rows including `@media print` for `reveal`
- [ ] §5.2 77-file inventory (41+35+1) matches `risen-christ` §5.2
- [ ] §5.4 routing contract has 17 Route / 5 alias groups / 7 alias paths table + `resolveHashRedirect` + `scroll-mt-28` note
- [ ] §5.5 component conventions table includes Header modal drawer (role=dialog, aria-modal, focus trap, 44px)
- [ ] §6 `useScrolled` code fence present with `threshold = 12` default + Header `16` nuance
- [ ] §7 10 arrays with counts/shapes + 8 interfaces + `images 11 local` + add-content recipes
- [ ] §9 15 anti-patterns (count rows) — draft had 9, missing #10–15 must be present
- [ ] Appendix B smoke is Risen example (Toa Payoh, 91, 1969–2026) with Parish X footnotes — not Bukit Batok
- [ ] Appendix E header says "Reference: St Mary vs St Joseph … (Generalized via docs-contract)" — fossil preserved but labeled
- [ ] Appendix A ADR-3 says 26+2 superset with both AA steps; ADR-6 forbids `src.orig` in index
- [ ] No `<a href="#id">` advice outside the anti-pattern; Ministries jump nav correctly says `<Link to="/ministries#id">`

### 3.4 Success criteria (all must be green to promote v3.0.0)

| Criterion | Gate |
|---|---|
| All 8 axes PASS (or CONCERN with written rationale) | No Critical/High FAIL remains |
| `rg` gate (§3.2) expectations met | Each `rg` line in the report shows expected vs actual |
| Fidelity zero-leak proven | V5 `rg` hits classified by section, zero in §§2–20 data sections |
| Lines 1438 within 1400–1500 + 27 sections | `wc -l` + heading count cited |
| Cross-check vs `risen-christ` shows no immutable-contract regression | `diff` of §5.4/§9/§11 shows only additive superset, not fork |
| Report is evidence-anchored | Every verdict has a `rg` citation + line number + severity |

---

## 4. Phase 3 — VALIDATE: Explicit Confirmation Gate

**Do not start Phase 4 until you confirm. Reply with one of:**

| Option | What it triggers |
|---|---|
| **`approve plan as-is`** | I run Phase 4 immediately: full 8-axis audit with `rg` proofs → write `REVIEW-REPORT-unified-v3.md` → Phase 5 self-check → Phase 6 handoff. No edits to `unified-v3_SKILL.md`. |
| **`approve with scope tweak`** | Specify `A1–A4` choices (e.g., `A1 strict / A4 report+fix`) — I revise §3.1/§3.2 and re-issue the plan before running. |
| **`expand to include fix pass`** | I produce the report *and* then open a second plan for the fix commit (surgical edits only for FAILs). Two-phase approval preserved. |

**Open questions for you:**
1. Do you want the triangulation spot-checks against `risen-christ`/`st-mary`/`rothershrine` (A1), or strict `review_plan.md` only?
2. Should this review also produce a diff patch for any FAILs, or stay report-only (A4)?

---

## 5. Phase 4 — IMPLEMENT: Execute the Review (After Approval)

*One section per axis, one `rg` per claim, no hand-waving.*

**Step order:**
1. Run the `rg`/`wc` gate (§3.2) — capture stdout verbatim into the report's Evidence appendix.
2. Read `unified-v3_SKILL.md` front-to-back (offset reads to cover all 1438 lines — no 50KB truncation).
3. Score each of the 8 axes: PASS / FAIL / CONCERN + severity + line refs + fix recommendation.
4. Cross-check 3 samples against `risen-christ_SKILL.md`: §4 `@theme` block, §5.4 routing table, §9 anti-patterns 15.
5. Classify fidelity hits (V5) by section — prove zero leaks in §§2–20.
6. Draft the report (no edits to the skill file).

**Anti-generic note:** This is a docs audit — no UI, no purple gradients. Evidence is the design.

---

## 6. Phase 5 — VERIFY: Iron Law — No False Completion

Before delivering the report, self-check:

- [ ] Every `review_plan.md` claim in Appendix A has a corresponding verdict in the report (no orphan claim).
- [ ] Every FAIL/CONCERN has a `rg` citation + line number + severity — no prose-only verdict.
- [ ] `rg` outputs are pasted verbatim (not summarized) in an Evidence appendix.
- [ ] No edit was made to `unified-v3_SKILL.md`, `review_plan.md`, or any `*_SKILL.md` during the review.
- [ ] Report states whether `v3.0.0` is **PROMOTE / PROMOTE WITH FIXES / DO NOT PROMOTE** with explicit blockers.

**Iron Law:** I will not claim "verified and ready" — the report will claim it *only if* all 8 axes are PASS.

---

## 7. Phase 6 — DELIVER: Review Report & Handoff

| Deliverable | Path | Content |
|---|---|---|
| **Review Report** | `new-skills/REVIEW-REPORT-unified-v3.md` | 8-axis scoring + verdict table + per-axis evidence + cross-check diff + blocker list + recommendation (Promote / Promote-with-fixes / Do-not-promote) |
| **Evidence log** | Inside the report (Appendix) | Verbatim `rg`/`wc`/`diff` outputs for reproducibility |
| **No skill edit** | — | Findings become a follow-up fix plan you approve separately |

**Suggested commit (after report approval):**
```bash
git add new-skills/REVIEW-VALIDATION-PLAN-unified-v3.md
git commit -m "docs(plan): add review-validation plan for unified-v3 vs review_plan (8-axis, rg-gated)"
# then after Phase 4:
git add new-skills/REVIEW-REPORT-unified-v3.md
git commit -m "docs(review): 8-axis audit of unified-v3 v3.0.0 vs review_plan — <verdict>"
```

---

## 8. Appendix A — Claims Inventory Extracted from `review_plan.md`

| # | Claim (verbatim or paraphrased) | Where | Falsifier (`rg`) |
|---|---|---|---|
| C-1 | Appendix B now parameterized — Risen example filled: 3 priests (Brian/Arun/Dexter), UEN T08CC4042G | Key fixes row 1 | `rg "T08CC4042G|Brian|Arun|Dexter" unified-v3` must hit in B steps; `rg "4 OFM|T08CC4053H"` must hit only in footnote |
| C-2 | Unified 26+2 superset — gold-700 (St Mary 4.72:1) + terracotta-600 (Risen 5.36:1), with Risen refinement rationale | Row 2 | `rg "gold-700|terracotta-600|26\+2"` |
| C-3 | `test { globals, jsdom }` + `server.watch.ignored` + `playwright.built.config.ts`; `img-src 'self' data: blob:` only, legacy forbidden | Row 3 | `rg "playwright\.built|server\.watch\.ignored|img-src 'self'"` |
| C-4 | Front-matter `~35/202~51` (machine-asserted by docs-contract), prose no longer hardcodes drift-prone counts | Row 4 | `rg "machine-asserted|docs-contract"` |
| C-5 | Appendix E relabeled Reference: St Mary vs St Joseph (Generalized via docs-contract) + §1 lineage breath keeps all 4 hops | Row 5 | `rg "Reference: St Mary vs St Joseph"` |
| V1 | front-matter: singapore-parish-lineage v3.0.0, canonical Risen Toa Payoh, 4-hop lineage ✓ | Verification block | `rg "^name:|^version:|^canonical_ref:|^lineage:"` |
| V2 | tokens: gold-700 + terracotta-600 → 26+2 / 28-theme superset ✓ | Verification block | `rg "shrine-gold-700|shrine-terracotta-600"` |
| V3 | sections: 27 (§§1–20 + A–F + QR) ✓ | Verification block | `rg "^## [0-9]+\.|^## Appendix|^## Quick" | wc -l` |
| V4 | Appendix B: Parameterized — Risen example (smoke) ✓ | Verification block | read Appendix B |
| V5 | fidelity: Oklahoma/Tepeyac only in §1 breath + D/F, 0 in data sections ✓ | Verification block | `rg "Oklahoma|Tepeyac"` classified |
| V6 | lines: 1438 (target 1400–1500) ✓ | Verification block | `wc -l` |

---

## 9. Appendix B — Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Self-referential loop** — `review_plan.md` certifies itself, we re-certify the certificate | High (55-line claim is the only acceptance criteria) | Critical — false promotion | Triangulate 3 samples against `risen-christ` (A1); treat `review_plan.md` as claim set, not proof |
| **50KB truncation hides decay** — initial read was truncated at 50KB/2000 lines | High (already hit in ANALYZE) | High — tail Appendices E/F unread | Offset reads in Phase 4 to cover all 1438 lines; `wc -l` + heading `rg` as gate |
| **Token hex typo** — `gold-700 #85601f` vs `#85601e` passes prose but fails `grep shrine-` | Medium | High — breaks contract | Exact `rg "#85601f|#8f4c30"` + compare against `src/index.css` if repo present |
| **Fidelity mis-classification** — `WOHA` appears in §1 breath (allowed) but reviewer counts it as leak | Medium | Medium — false FAIL | Classify hits by section heading (require section-aware `rg -n` with heading context) |
| **Report-only vs fix creep** — reviewer starts editing `unified-v3` mid-audit | Medium | Medium — surgical discipline break | Phase 4 is read-only; fixes require separate plan you approve (A4) |
| **Scope creep into re-merge** — audit expands into re-doing the 26+2 superset | Low | Medium — adds unverified design debt | Freeze: no new tokens/routes beyond the 8 axes; any new finding becomes a CONCERN, not a silent fix |

---

## Next Step — Awaiting Your Confirmation

Reply **`approve plan as-is`** to run the 8-axis audit now, or specify `A1–A4` scope tweaks (e.g., `A1 strict, A4 report-only`). No file beyond this plan will be written until you validate.
