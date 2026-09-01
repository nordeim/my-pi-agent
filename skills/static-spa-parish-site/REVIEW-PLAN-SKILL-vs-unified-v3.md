# Meticulous Review Plan — `SKILL.md` (1590 lines, 2026-09-01) vs `unified-v3_SKILL.md` (1438 lines, 2026-08-31)

> **Request:** Meticulously plan to review `SKILL.md` and compare it with `unified-v3_SKILL.md`.
> **Author:** Claw Code (Frontend Architect · 15y) · **Date:** 2026-09-01 · **Method:** Meticulous Approach — ANALYZE → PLAN → VALIDATE → IMPLEMENT → VERIFY → DELIVER
> **No file will be edited until this plan is approved.**

---

## Table of Contents
1. [Executive Summary & Go/No-Go](#1-executive-summary--gono-go)
2. [Phase 1 — ANALYZE: What Each Document Is & Why They Diverge](#2-phase-1--analyze-what-each-document-is--why-they-diverge)
3. [Phase 2 — PLAN: 9-Axis Comparative Review & Methods](#3-phase-2--plan-9-axis-comparative-review--methods)
4. [Phase 3 — VALIDATE: Confirmation Gate](#4-phase-3--validate-confirmation-gate)
5. [Phase 4 — IMPLEMENT: How the Review Will Run (After Approval)](#5-phase-4--implement-how-the-review-will-run-after-approval)
6. [Phase 5 — VERIFY: Iron Law](#6-phase-5--verify-iron-law)
7. [Phase 6 — DELIVER: Report & Recommendation](#7-phase-6--deliver-report--recommendation)
8. [Appendix A — Claims & Deltas Inventory](#8-appendix-a--claims--deltas-inventory)
9. [Appendix B — Risk Register](#9-appendix-b--risk-register)

---

## 1. Executive Summary & Go/No-Go

**One sentence:** `SKILL.md` (1590 lines, `static-spa-parish-site` v3.0.0 + `package_version: 1.4.4`, dated 2026-09-01) is a **one-day-newer, structurally superseding rewrite of `unified-v3_SKILL.md`** (1438 lines, `singapore-parish-lineage` v3.0.0, dated 2026-08-31) that introduces a §0 Volatile Facts Register, a full Appendix G audit ledger (26 findings), and a fossil-sweep protocol — while intentionally **diverging on the token superset** (25+2 vs 26+2) and freezing the appendices differently.

**Go/No-Go:** **GO** — as a *comparative, evidence-anchored review*, not a re-merge. Both files claim v3.0.0 but answer different questions:
- `unified-v3` asks *"how to unify the 3 parish hops into a Lineage Master with the 26+2 palette?"*
- `SKILL.md` asks *"how to stop the lineage docs from fossilizing again?"* (systemic root cause: volatile facts restated 5–8× per doc, appendices copy-forwarded without a previous-parish sweep — Appendix G.2).

The review must therefore **score `SKILL.md` as a candidate canonical**, with `unified-v3` as the *incumbent* and `risen-christ` (1427 lines) as the *ground-truth baseline* for byte-level contracts.

**Best recommendation:** Run a **9-axis diff** (see §3.1) with `rg`/`wc`/`diff` proofs. Do not edit either file during the review. The deliverable will state **which file to promote to canonical and which to freeze as lineage artifact**, with per-axis PASS / CONCERN / FAIL + line citations + `diff` evidence.

---

## 2. Phase 1 — ANALYZE: What Each Document Is & Why They Diverge

### 2.1 Identity

| Field | `SKILL.md` (candidate) | `unified-v3_SKILL.md` (incumbent) | What to test |
|---|---|---|---|
| `name` | `static-spa-parish-site` | `singapore-parish-lineage` | Different framing — both v3.0.0, but SKILL splits `version` (doc axis) vs `package_version: 1.4.4` (repo axis, §0) |
| `display_name` | Parish Site Engineering Skill — Unified v3 | Singapore Parish SPA Lineage — Master Engineering Skill | Unified is lineage-branded; SKILL is parish-site-branded |
| `version` | 3.0.0 (doc axis) + `package_version: 1.4.4` (§0) | 3.0.0 (single axis) | SKILL's split resolves hop-1's triple-version conflict (1.3.0 / 1.1.0 / 1.0.0) — Appendix G #1 |
| `canonical` | Risen Christ, Toa Payoh (91 Toa Payoh Central, 1971 first air-con, Fr Pierre Abrial) — explicit `unified_from: rothershrine + st-mary + risen` + `port_provenance` | Risen Christ, Toa Payoh (same parish, same address/blessing) — `canonical_ref` + `lineage: Rother → St Joseph BT → St Mary → Risen` | Same parish, same stack, same 77 files — framing diff only |
| `lines` | **1590** (+152 vs unified) | **1438** | +152 = §0 (+~30) + Appendix G ledger (+~180) − Appendix D/E/F consolidation (−~60) |
| `date` | 2026-09-01 (one day newer) | 2026-08-31 | SKILL claims to supersede unified — verify by `ls -l` + frontmatter |
| `skeleton` | §§0–20 + Appendices A–G + Quick Ref (29 headings) | §§1–20 + Appendices A–F + Quick Ref (27 headings) | SKILL adds §0 Volatile Facts Register; appendices G is new; D/E/F are consolidated vs unified's split D+E+F |

### 2.2 The systemic divergence (why SKILL is not just "unified + G")

`unified-v3` fixes **5 specific defects** from the draft diagnosis (C-1 smoke, H-4 token drift, H-6/H-7 vite test/CSP, C-3 counts, tail-end decay). `SKILL.md` fixes **the systemic root cause that produced those 5** — and 21 more — as catalogued in Appendix G:

> "Every finding above is an instance of one failure mode: volatile facts restated 5–8× per document + appendices copy-forwarded at each hop without a previous-parish fossil sweep." (SKILL Appendix G.2)

**Structural countermeasure in SKILL that unified lacks:**
1. **§0 Volatile Facts Register** — the *only* section allowed to state a mutable number (16 rows: canonical/package_version/unit/E2E/src/images/build/tokens/utilities/hooks/utils/routes/CSP/src.orig/skills/secrets/data arrays/parish constants/pre-push gate). Every other section references §0 ("see §0") instead of restating.
2. **`as of <date>` labels** for historical snapshots in lineage appendices — only appendices may carry stale numbers, and only when labeled.
3. **Fossil-Sweep Protocol** (Appendix G.4) — 8-step `rg` checklist future ports must run before shipping (register-first, sweep-old-value, previous-parish grep, sum-every-count, reconcile-tree, tracking-audit, rewrite-Appendix-B, gates).

Unified's countermeasure is weaker: front-matter `~35/202 (machine-asserted by docs-contract, not prose)` — correct intent, but other sections still restate counts without a single-source register.

### 2.3 Token & contract deltas (the two intentional non-consensuses)

| Dimension | SKILL.md (2026-09-01) | unified-v3 (2026-08-31) | Which is "right"? |
|---|---|---|---|
| **Palette** | **25 colors + 2 shadows (27 @theme entries)** — terracotta-600 only; gold-700 #85601f is a lineage note ("hop-2 also carried it — re-add if needed") | **26 colors + 2 shadows (28 entries)** — gold-700 + terracotta-600 superset | Both documented. SKILL matches `src/index.css` byte-for-byte (27 entries); unified's 28 is a *future-port* superset. Must verify via `sed -n '/@theme/,/^}/p' | - |
| **Utilities** | **27 utility classes** (each `rise-in-d1..d4` counted individually) + 8 keyframes + `@media print` reveal | **28 utilities** (27 + print counted as separate) | Counting convention diff — must reconcile vs `§0` register vs §4.3 table rows |
| **Hooks/Utils** | 3 hooks + 4 utils (cn/massDay/monogram/deepLinks) — §5.2 tree complete per test harness | 3 hooks + same 4 utils | Parity — but SKILL's §5.2 tree was audited to match test harness (finding #25) |
| **Appendices** | G (26 findings + root cause + fossil-sweep) + D consolidated lineage + E hop-2 validation + F hop-3 diff (corrected) | D (Rother→St Joseph→St Mary) + E (St Mary vs St Joseph) + F (St Mary→Risen) — no G | SKILL adds the ledger that explains *why* unified's 5 fixes were needed |
| **ADR** | **ADR-7 + ADR-8 new** (volatile-facts register + fossil-sweep) beyond 1–6 | ADR 1–6 only | SKILL adds the governance ADRs that make §0 enforceable |

### 2.4 What must not have regressed (immutable contracts — test against `risen-christ` baseline)

- 77 files (41+35+1), 35/202 + 51 E2E (+ 51 built), 397.52 kB singlefile, 8 images all-local, 17 Route / 5 groups / 7 aliases / 9 anchors (`#language-communities` not `#mandarin`), HashRouter + singlefile + `@→src/` + `src.orig` pruned + `repo-hygiene` guard, CSP `'self' data: blob:`, 15 anti-patterns, 16-row debugging, 9-step pre-ship, 12 lessons + L13–L15 new in SKILL.

### 2.5 Ambiguities to resolve before IMPLEMENT

| # | Ambiguity | Options | Recommendation |
|---|---|---|---|
| A1 | **Canonical choice** — should the review *recommend* one file as canonical, or treat both as co-canonical lineage variants? | Single canonical vs Co-canonical | **Single canonical** (the Meticulous Approach requires one source of truth — SKILL.md's §0 makes single-canonical enforceable) |
| A2 | **Token superset verdict** — 25+2 (SKILL, matches `src/index.css`) vs 26+2 (unified, future-proof) — which to bless? | Bless SKILL 25+2 (byte-true) vs Bless unified 26+2 (future) vs Bless SKILL 25+2 + note to re-add gold-700 on demand | **Bless SKILL 25+2 as canonical, unified 26+2 as documented option** — SKILL explicitly says "re-add it deliberately if a text-bearing gold step is needed" (Appendix G #3 resolution) |
| A3 | **Counting convention** — utilities 27 vs 28 (`rise-in-d1..d4` + `@media print`) — which count becomes the contract? | 27 (SKILL §0) vs 28 (unified) | **Defer to SKILL §0 (27 + 8 keyframes)** — it's the only register with a sum-verified breakdown |
| A4 | **Fix policy** — if the review finds FAILs in either file, should the review also patch them? | Report-only vs Report+patch | **Report-only** — findings become a surgical follow-up commit you approve separately (discipline from the 2026-09-01 REVIEW-PLAN) |

---

## 3. Phase 2 — PLAN: 9-Axis Comparative Review & Methods

### 3.1 Nine axes (each maps to a `review_plan.md`-style gate + SKILL's G ledger)

| Axis | Tests | Method (reproducible) | Pass criterion | Severity |
|---|---|---|---|---|
| **V1 — Identity & Versioning** | `name/version/package_version/canonical/unified_from/lineage` | `rg "^name:|^version:|^package_version:|^canonical|^unified_from|^port_provenance" SKILL.md unified-v3_SKILL.md` + `head` frontmatter + `wc -l` | SKILL: `static-spa-parish-site 3.0.0 + package_version 1.4.4` with §0 row; unified: `singapore-parish-lineage 3.0.0` with `~` machine-asserted — both valid, SKILL's split must resolve the triple-version fossil (App G #1) | Critical |
| **V2 — Structural Completeness** | Sections, line counts, TOC | `rg "^## |^0\." SKILL.md unified-v3_SKILL.md | wc -l` + `rg "^## [0-9]+\.|^## Appendix|^## Quick|^## 0\."` counts + `diff <(rg "^##" SKILL) <(rg "^##" unified)` | SKILL 29 headings (§0 + §§1–20 + A–G + QR) / 1590 lines; unified 27 headings / 1438 lines — no section lost; SKILL's §0 + G additive | Critical |
| **V3 — Token & Style Contracts** | Palette, utilities, keyframes, z-index | `sed -n '/@theme/,/^}/p' SKILL.md | rg -c "--color-shrine-"` (expect 25) vs unified (expect 26) + `rg -n "gold-700|terracotta-600"` both files + `rg "z-\[60\]" SKILL.md unified` (SKILL §18 gains rail row) | SKILL 25+2 matches `src/index.css`; unified 26+2 is superset with rationale — both pass if §0/§4.1/§19/ADR-3 are internally consistent | High |
| **V4 — Volatile-Facts Discipline** | Single-source vs restatement | `rg -c "202 tests|51 E2E|397\.52|77 files|25 .*shadows|27 .*utilities|17 Route" SKILL.md unified` + `rg "see §0|machine-asserted|as of" SKILL.md unified` | SKILL: volatile facts stated once (§0) + `as of` in appendices, others reference §0; unified: `~` shorthand but still restates in §§2/3/11 — SKILL's discipline must be the tighter | High |
| **V5 — Smoke & Fidelity** | Appendix B param + no-leak in §§2–20 | `rg "^## Appendix B" -A 120 SKILL.md unified` + `rg "T08CC4042G|T08CC4053H|4 OFM|#language-communities|#mandarin" SKILL.md unified` + `rg "Oklahoma|Tepeyac|Kranji|Palladian|WOHA|Ho Ping" SKILL.md unified` classified by section | Both: B is Risen-filled (91 Toa Payoh, 1969–2026, 3 priests Brian/Arun/Dexter); zero predecessor leaks outside §1/D/E/F/G | High |
| **V6 — Config & Contract Completeness** | vite/eslint/ts/playwright/CSP/src.orig | `rg "playwright\.built|server\.watch\.ignored|test \{|globals|img-src|src\.orig.*forbidden|repo-hygiene" SKILL.md unified` + read §3.2 tables + ADR-6 | Both mandate `test{globals,jsdom}` + `server.watch.ignored` + `playwright.built` + strict `img-src 'self' data: blob:` + pruned `src.orig` + `repo-hygiene` guard — must match `risen-christ` | High |
| **V7 — Audit Ledger Depth** | Anti-patterns, debugging, pre-ship, lessons, fossil-sweep | `rg "^\| [0-9]+ \| \*\*" SKILL.md unified | wc -l` (expect 15) + `rg "Appendix G|Fossil-Sweep|Unification.*Ledger" SKILL.md unified` + `rg "L13|L14|L15" SKILL.md` | Both have 15 anti-patterns; SKILL adds Appendix G (26 findings #1–26 + root cause G.2 + provenance G.3 + fossil-sweep G.4) + L13–L15 + ADR-7/8 | Medium |
| **V8 — Migration Appendices** | D/E/F lineage & validation vs fossil appendices | Read Appendix D (SKILL D.1–D.3 vs unified D) + E (hop-2 validation) + F (hop-3 diff) + `diff` of F tables | SKILL's D is 4-generation consolidated with labeled snapshots (`as of`), E labeled port-day audit + v3 reuse note, F corrected vs round-7 snapshot — unified's D/E/F are the pre-unification split that Appendix G would have consolidated | Medium |
| **V9 — Lineage Invariants** | 77/35/202/51/397.52kB/8 local/17/5/7/9/HashRouter/singlefile/@alias | `rg "77 files|35 files / 202|51 E2E|397\.52|8 files|17 Route|5 groups|HashRouter|singlefile|@→src" SKILL.md unified` vs `risen-christ` | Both preserve all invariants byte-for-byte; any regression vs `risen-christ` is a FAIL | Critical |

### 3.2 Reproducible `rg`/`wc`/`diff` gate (runs in Phase 4 — capture stdout verbatim)

```bash
# V1 — identity
rg -n "^name:|^version:|^package_version:|^canonical|^unified_from|^port_provenance" SKILL.md unified-v3_SKILL.md
head -n 30 SKILL.md; head -n 20 unified-v3_SKILL.md
wc -l SKILL.md unified-v3_SKILL.md

# V2 — structure
rg -n "^## [0-9]+\.|^## Appendix|^## Quick|^## 0\." SKILL.md unified-v3_SKILL.md | wc -l
rg -n "^## [0-9]+\.|^## Appendix|^## Quick|^## 0\." SKILL.md
rg -n "^## [0-9]+\.|^## Appendix|^## Quick" unified-v3_SKILL.md
diff <(rg "^## " SKILL.md) <(rg "^## " unified-v3_SKILL.md) | head -n 80

# V3 — tokens
sed -n '/@theme/,/^}/p' SKILL.md | rg -c -- "--color-shrine-"; echo "SKILL @theme colors"
sed -n '/@theme/,/^}/p' unified-v3_SKILL.md | rg -c -- "--color-shrine-"
rg -n "gold-700|terracotta-600|26 \+ 2|25 \+ 2|26 colors|25 colors" SKILL.md unified-v3_SKILL.md
rg -n "z-\[60\]|z-50|z-\[100\]" SKILL.md unified-v3_SKILL.md | head

# V4 — volatile-facts discipline
rg -n "machine-asserted|see §0|Volatile Facts|as of" SKILL.md | head -n 20
rg -n "machine-asserted|see §0|Volatile Facts|as of" unified-v3_SKILL.md | head -n 20
rg -n "202 tests|51 E2E|397\.52|77 files" SKILL.md | wc -l; rg -n "202 tests|51 E2E|397\.52|77 files" unified-v3_SKILL.md | wc -l

# V5 — smoke & fidelity
rg -n "T08CC4042G|T08CC4053H|4 OFM|#language-communities|#mandarin" SKILL.md unified-v3_SKILL.md
rg -n "Oklahoma|Tepeyac|Kranji|Palladian|WOHA|Ho Ping" SKILL.md unified-v3_SKILL.md

# V6 — config
rg -n "playwright\.built|server\.watch\.ignored|test \{|globals.*jsdom|img-src.*self|src\.orig.*forbidden|repo-hygiene" SKILL.md unified-v3_SKILL.md

# V7 — ledger
rg -n "^\| [0-9]+ \| \*\*" SKILL.md | wc -l; rg -n "^\| [0-9]+ \| \*\*" unified-v3_SKILL.md | wc -l
rg -n "Appendix G|Fossil-Sweep|Unification.*Ledger|L13|L14|L15|ADR-7|ADR-8" SKILL.md | head
rg -n "Appendix G|Fossil-Sweep|Unification.*Ledger" unified-v3_SKILL.md | head

# V8 — appendices diff
sed -n '/## Appendix D/,/## Appendix E/p' SKILL.md | head -n 80
sed -n '/## Appendix D/,/## Appendix E/p' unified-v3_SKILL.md | head -n 40
diff <(sed -n '/## Appendix F/,/## Appendix G/p' SKILL.md | head -n 60) <(sed -n '/## Appendix F/,/## Quick/p' unified-v3_SKILL.md | head -n 60) | head -n 60

# V9 — invariants vs baseline
rg -n "77 files|35 files / 202|51 E2E|397\.52|17 Route|HashRouter|singlefile" SKILL.md unified-v3_SKILL.md risen-christ_SKILL.md | head -n 20
```

### 3.3 Manual spot-checks (Phase 4 checklist)

- [ ] §0 in SKILL is the *only* place stating each mutable number — every other section says "see §0" (not a restated count)
- [ ] `grep shrine- src/index.css → 25 colors + 2 shadows` in SKILL matches `src/index.css` byte-for-byte; unified's 26+2 is a documented superset option, not a drift
- [ ] §4.3 lists 27 utility rows + 8 keyframe rows in both files (unified counts print as 28)
- [ ] §18 in SKILL has the `z-[60]` ScrollProgress rail row that unified's §18 audit flagged as missing in the sources
- [ ] Appendix B in both files is Risen-filled (18 steps + built pass in SKILL; 17 in unified) — not the St Mary fossil
- [ ] Appendix G in SKILL records all 26 findings (#1–26) with per-finding resolution; unified has no G
- [ ] ADR-7 (volatile-facts register) + ADR-8 (fossil-sweep) exist only in SKILL
- [ ] D.1 lineage table in SKILL carries `as of <date>`-labeled snapshots for every hop's test/version count — unified's D/E/F split carries the same but without the single-table trajectory
- [ ] No `<a href="#id">` outside the anti-pattern; Ministries jump nav correctly `<Link to="/ministries#id">` in both

### 3.4 Success criteria (all must be green to recommend a canonical)

| Criterion | Gate |
|---|---|
| All 9 axes scored PASS or CONCERN-with-rationale | No Critical/High FAIL remains unaddressed |
| Every verdict has a `rg` citation + line number + severity | No prose-only verdict |
| `rg` gate (§3.2) outputs pasted verbatim in Evidence appendix | Reproducible |
| Token / route / file invariants vs `risen-christ` baseline show additive superset only — no immutable-contract regression | `diff` vs `risen-christ` cited |
| Report states **PROMOTE SKILL.md / PROMOTE unified-v3 / CO-CANONICAL+FREEZE** with explicit blockers | No ambiguous recommendation |

---

## 4. Phase 3 — VALIDATE: Confirmation Gate

**Reply with one of:**

| Option | What it triggers |
|---|---|
| **`approve plan as-is`** | I run the 9-axis comparative review immediately → write `REVIEW-REPORT-SKILL-vs-unified-v3.md` → Phase 5 self-check → Phase 6 handoff. No edits to either SKILL file. |
| **`approve with scope tweak`** | Specify `A1–A4` choices (e.g., `A2 bless 25+2, A4 report-only`) — I revise §2.5/§3.1 and re-issue before running. |
| **`expand to include fix pass`** | I produce the report *and* then open a second plan for the surgical fix commit (only for FAILs). Two-phase approval preserved. |

**Open questions for you:**
1. Should SKILL.md's §0 Volatile Facts Register become the *mandated* canonical pattern (A1 single-canonical)?
2. Confirm the token verdict you want: bless SKILL's 25+2 as canonical (unified 26+2 noted as option) — A2?

---

## 5. Phase 4 — IMPLEMENT: How the Review Will Run (After Approval)

1. Run the `rg`/`wc`/`diff` gate (§3.2) — capture stdout verbatim.
2. Read both files front-to-back (offset reads to cover 1590 + 1438 lines — no 50KB truncation).
3. Score each of the 9 axes: PASS / FAIL / CONCERN + severity + line refs + fix recommendation + which file is ahead.
4. Classify fidelity hits by section — prove zero leaks outside §1/D/E/F/G in both files.
5. Diff 3 samples vs `risen-christ` baseline: §4 `@theme`, §5.4 routing, §9 anti-patterns 15.
6. Draft the report — no edits to either skill file.

---

## 6. Phase 5 — VERIFY: Iron Law

- [ ] Every `review_plan.md`-style claim in both files has a verdict (no orphan claim).
- [ ] Every FAIL/CONCERN has a `rg` citation + line number + severity + which file is ahead.
- [ ] `rg` outputs pasted verbatim (not summarized) in Evidence appendix.
- [ ] No edit made to `SKILL.md`, `unified-v3_SKILL.md`, or any `*_SKILL.md` during the review.
- [ ] Report states **PROMOTE SKILL.md / PROMOTE unified-v3 / CO-CANONICAL** with explicit blockers.

---

## 7. Phase 6 — DELIVER: Report & Recommendation

| Deliverable | Path | Content |
|---|---|---|
| **Comparative Report** | `new-skills/REVIEW-REPORT-SKILL-vs-unified-v3.md` | 9-axis scoring + head-to-head deltas + `diff` evidence + per-axis winner + overall recommendation (Promote SKILL.md as canonical — or the alternative with blockers) |
| **Evidence log** | Inside the report (Appendix) | Verbatim `rg`/`wc`/`diff` outputs |
| **No skill edit** | — | Findings become a follow-up surgical commit you approve separately |

**Suggested commit after report approval:**
```bash
git add new-skills/REVIEW-PLAN-SKILL-vs-unified-v3.md
git commit -m "docs(plan): add comparative review plan SKILL.md vs unified-v3 (9-axis, rg-gated)"
# then after Phase 4:
git add new-skills/REVIEW-REPORT-SKILL-vs-unified-v3.md
git commit -m "docs(review): 9-axis comparative audit SKILL.md vs unified-v3 — <verdict>"
```

---

## 8. Appendix A — Claims & Deltas Inventory

| # | Dimension | SKILL.md (2026-09-01) | unified-v3 (2026-08-31) | Delta type |
|---|---|---|---|---|
| 1 | `name` | `static-spa-parish-site` | `singapore-parish-lineage` | Framing rename |
| 2 | `version` axis | `3.0.0` (doc) + `package_version 1.4.4` (repo, §0) | `3.0.0` single axis | SKILL splits axes to resolve triple-version fossil |
| 3 | Lines | 1590 | 1438 | +152 = §0+G−consolidation |
| 4 | §0 Register | 16 rows, single source, `see §0` discipline | Front-matter `~` shorthand, no §0 | SKILL's systemic countermeasure; unified has weaker form |
| 5 | Tokens | 25+2 (27 entries) — gold-700 as lineage note | 26+2 (28 entries) — gold-700 + terracotta-600 superset | Intentional divergence — SKILL byte-true to `src/index.css`; unified future-proof |
| 6 | Utilities | 27 + 8 keyframes (counted as 27) | 28 (27 + print) | Counting convention |
| 7 | Appendix B | 18-step Risen smoke + built pass | 17-step Risen smoke (parameterized) | SKILL adds the built-pass step explicitly |
| 8 | Ledger | Appendix G: 26 findings #1–26 + G.2 root cause + G.3 provenance + G.4 fossil-sweep + ADR-7/8 + L13–15 | No G; 5 Key-fixes table in `review_plan.md` style | SKILL's ledger is the audit trail unified's 5 fixes were drawn from |
| 9 | Appendices D/E/F | D consolidated 4-generation (D.1–D.3) + E hop-2 validation (labeled) + F corrected hop-3 diff | D split (Rother→St Joseph→St Mary), E ref, F St Mary→Risen | SKILL consolidates with `as of` labels; unified preserves the split |
| 10 | z-index | §18 includes `z-[60]` ScrollProgress rail row | Same row present (post-audit) | Parity — both fixed the source omission |
| 11 | Invariants | 77 / 35/202 / 51×2 / 397.52kB / 8 local / 17/5/7/9 / HashRouter/singlefile | Same | No regression in either vs `risen-christ` |
| 12 | Outstanding secret | `docs/ssh-key.txt` rotation still outstanding (C-1) | Same (disclosed) | Parity |

---

## 9. Appendix B — Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Framing confusion** — `static-spa-parish-site` vs `singapore-parish-lineage` reads as two products | High | Medium — cannons on different names, same parish | Recommend single `name` in report; SKILL's `static-spa-parish-site` is the cooler, repo-anchored name |
| **Token count false FAIL** — 25 vs 26 flagged as drift when it's a deliberate superset choice | High | High — false FAIL blocks promotion | Classify as CONCERN-with-rationale, not FAIL; cite `src/index.css` byte count as tie-breaker (SKILL wins on byte-truth, unified wins on future-port notes) |
| **50KB truncation hides G ledger** — initial read truncated at 50KB, G ledger lives at tail | High | High — 26 findings unread | Offset reads in Phase 4 to cover tail 1390–1590; `rg "Appendix G"` as gate |
| **Self-referential loop** — SKILL's Appendix G re-audits unified's sources, but unified's `review_plan.md` already claimed completion | Medium | Medium — circular certification | Triangulate both files against `risen-christ` as ground truth, not against each other |
| **Report-only vs fix creep** — reviewer starts editing SKILL/unified mid-audit | Medium | Medium — surgical discipline break | Phase 4 is read-only; fixes in a separate plan you approve (A4) |
| **Utility count false FAIL** — 27 vs 28 from `rise-in-d1..d4` + print convention | Medium | Low — counting pedantry | Note convention in report; both count to the same 27 utility rows + 8 keyframes |

---

## Next Step — Awaiting Your Confirmation

Reply **`approve plan as-is`** to run the 9-axis audit now, or specify `A1–A4` scope tweaks. No file beyond this plan will be written until you validate.
