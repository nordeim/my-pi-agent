# Unified Skill v4.1.1 — Meticulous Implementation Plan

**Date:** 2026-08-07  
**Base:** `markdown-to-web_SKILL_v4.1.md` (v4.1.0, 3,886 lines)  
**Trigger:** Round 4 self-audit (`comparative_analysis_q4.1.md`, 16 findings: 0 Critical, 2 High, 4 Medium, 6 Low, 4 Informational), all validated against the v4.1.0 source  
**Target:** One self-contained skill file, `markdown-to-web_SKILL_v4.1.1.md`, estimated 3,900–4,100 lines  
**Confidence:** Reasoned (design document; no code execution in this environment)

---

## I. Validation of the Round 4 Audit

### 1.1 Audit document reviewed

`comparative_analysis_q4.1.md` (108 lines) — a Mode C audit of the v4.1.0 skill. The audit identifies 16 findings (0 Critical, 2 High, 4 Medium, 6 Low, 4 Informational) and concludes that v4.1.0 is the strongest edition in the corpus but "declared completion one coherence pass early." The audit's core insight: v4.1.0 front-loaded code-level fixes while leaving verification/traceability layers (tests, skeleton, appendices, closing ledger) stale.

### 1.2 Validation method

Each Round 4 finding was cross-checked against the v4.1.0 source file (`/home/z/my-project/download/markdown-to-web_SKILL_v4.1.md`, 3,886 lines) using targeted grep and read operations.

| Finding | Audit claim | Validation against v4.1.0 source | Verdict |
|---------|-------------|----------------------------------|---------|
| **V1** — Frontmatter test layer broken | §14.6 tests import `extractFrontmatter` which no longer exists; §22.5 defines `parseDocument` | **Confirmed.** Line 2608: `import { extractFrontmatter } from "@/lib/frontmatter"` — function that no longer exists. §22.5 (line 3427) defines `parseDocument()`. The §14.6 tests are stale, calling a non-existent function. No pipeline line shows `body` consumption. | **Valid — must fix** |
| **V2** — Ledger/version integrity contradictions | Appendix A says "35 findings (20 Round 1 + 15 Round 2)" with zero Round 3 rows; Closing says "v4.0.0" and "Skill version: 4.0.0"; Appendix F is byte-identical to v4.0.0's | **Confirmed.** Line 3604: "All 35 findings (20 Round 1 + 15 Round 2)" — no Round 3 rows. Line 3880: "v4.0.0 unified skill specification." Line 3882: "Skill version: 4.0.0". Appendix F (lines 3761–3802) has no Round 3 checks. The YAML frontmatter says `version: 4.1.0` (line 55). | **Valid — must fix** |
| **V3** — Template wiring disagreement | §7.4 says `index.css` has no template import; §5 skeleton omits `active.ts`; §5 annotation says "+ template @theme import"; §6.1 title says `src/index.css` | **Confirmed.** §7.4 (line 1307): "src/index.css contains no template @theme import." §5 skeleton (line 760): no `active.ts` listed. §5 annotation (line 766): "Tailwind v4 @import + Google Fonts + template @theme import" — direct contradiction. §6.1 title (line 904): "Editorial template `src/index.css` (full listing)" — but §7.4 says theme comes from `templates/editorial/theme.css`. | **Valid — must fix** |
| **V4** — F4/F5 fixtures missing | `headingText()` shipped without link/image parity fixtures; code-block guard shipped without fenced-`critical` fixture; colon-outside fixture absent | **Confirmed.** §9.2 has `headingText()` (line 1684). §9.3 fixture list (lines 1718–1728) contains no link/image heading. §14.4 test cases (lines 2540–2570) have no link/image heading test. §14.8 (lines 2670–2710) has no fenced-`critical` test. §14.3 (lines 2501–2535) has no colon-outside test. | **Valid — must fix** |
| **V5** — §12.1 contradicts amended 21.8 | §12.1 says "process.env.NODE_ENV is not replaced unless define is explicitly configured"; amended 21.8 says "Vite does replace it" | **Confirmed.** Line 2214: "`process.env.NODE_ENV` is not replaced unless `define` is explicitly configured." Finding 21.8 (line 422): "Vite *does* replace `process.env.NODE_ENV` at build time." Direct contradiction within the same document. | **Valid — must fix** |
| **V6** — 21.13 retag half-executed | §1.1 says both 21.1 and 21.13 retagged; 21.1 body shows retag ✓; 21.13 body still says "Verified" | **Confirmed.** Line 137: "21.13 → Reasoned." Line 453: "Confidence: Verified (github-slugger 2.0.0 package exports)" — NOT retagged. Closing line 3811: lists "github-slugger 2.0.0 package exports" under "Verified (from stable external definitions)" — should be Reasoned. | **Valid — must fix** |
| **V7** — 22.9 not applied | §8.6 has no aria-label note | **Confirmed.** Finding 22.9 (line 537): "Keep aria-label and data-tag... document that semantics are carried by visible text." §8.6 Badge component (line 1555): no such note present. | **Valid — must fix** |
| **V8** — 22.11 not applied; "first-level bullets" inaccuracy | Colon-outside absent from §8.4 blind spots; "only first-level bullets" claim is wrong | **Confirmed.** §8.4 blind spots (line 1488): "only first-level bullets are targeted" — but the regex `^\s*` matches indented bullets. Colon-outside variant `**Tag**: value` not in the list. | **Valid — must fix** |
| **V9** — 22.12 half-applied | §14.10 states 100% goal but no rationale for 90→80 downgrade | **Confirmed.** §14.10 (line 2780): mentions 80/75 thresholds. No rationale for the downgrade from draft_q3's 90%. | **Valid — must fix** |
| **V10** — Gate wording drift | §10.4 and §17 Gate 5 not updated to name the encoded badge exclusion | **Confirmed.** §10.4 (line 1860): "No suppressions." §17 Gate 5 (line 2898): "color-contrast are gate-failures" — doesn't name the `[data-tag]` exclusion now in §14.9. | **Valid — must fix** |
| **V11** — Script discipline drift | §15.2 and D.3 diverge; §17 Gate 4 cites `test:integration` not in §15.2 | **Confirmed.** §15.2 (line 3670) has `test` but not `test:integration`. §17 Gate 4 (line 2893): "npm run test:integration" — phantom script. | **Valid — must fix** |
| **V12** — Index staleness | Appendix B omits `ParsedDocument`; duplicate `TagRegistry` row; Closing has stale path | **Confirmed.** Appendix B (line 3618): duplicate `TagRegistry` row. No `ParsedDocument` row. Closing (line 3839): `markdown-to-web_SKILL_v4.md` — stale path. | **Valid — must fix** |
| **V13** — No regressions | All 35 v4.0.0 fixes survive | **Confirmed.** Two-layer theming, text-xs, no dangerouslySetInnerHTML, fence scanner, collision detection, ErrorBoundary, 250 KB budget all present. | **Valid (positive)** |
| **V14** — Count reconciliation correct | §1.0 table tallies are exact | **Confirmed.** 37 + 15 + 15 = 67. | **Valid (positive)** |
| **V15** — Failure pattern systematic | Failures at boundaries between fixed and unfixed sections | **Confirmed.** Every V1–V12 finding is at a boundary. | **Valid (informational)** |
| **V16** — Edition comparison | v4.1.0 best base; needs coherence patch | **Confirmed.** | **Valid (informational)** |

**Validation verdict: all 16 Round 4 findings are accurate.** The audit is devastatingly precise — every finding was confirmed by direct grep/read against the v4.1.0 source. The irony noted in the audit (v4.1.0 codified Lesson 10 "Fix-batches create inconsistencies" and then committed exactly that failure mode six times) is fully validated.

---

## II. Validation of the Proposed v4.1 Implementation Plan

The `unified_skill_v4.1_IMPLEMENTATION_PLAN.md` (146 lines) was the plan that produced v4.1.0. It is **not** a plan for v4.1.1 — it is the prior plan that was executed (incompletely). The audit's V15 finding correctly identifies the systematic failure: the plan's §5 execution strategy specified 5 passes with review checkpoints, but the execution front-loaded code fixes (Passes 1–3) and left the coherence sweep (Pass 5) incomplete. The plan itself was sound; its execution was the problem.

The plan's §7 "Final consistency gate" listed 6 checks — every one of them was violated by the actual v4.1.0 output:
1. "All 50 findings → Appendix A row" → Appendix A has 35 rows, not 50 (V2)
2. "Frontmatter limitations text == parseDocument code behavior" → §14.6 tests call non-existent function (V1)
3. "Axe test assertions == §10.3 exceptions" → §10.4/§17 wording drift (V10)
4. "CI invokes only scripts defined in §15.2" → `test:integration` is phantom (V11)
5. "Confidence statement: Reasoned throughout" → 21.13 still Verified (V6)
6. "No contradictions" → §12.1 contradicts 21.8 (V5)

**Verdict:** The v4.1 plan was correct but incompletely executed. v4.1.1 does not need a new plan with new architecture — it needs a **coherence sweep** that completes the unfinished Pass 5 of the v4.1 plan, plus the 2 findings that were never started (V7, V8).

---

## III. Architectural Decisions (Locked for v4.1.1)

### Decision 1: v4.1.1 is a coherence patch, not a new edition

v4.1.1 = v4.1.0 + 16 coherence fixes. No new architecture, no new code patterns, no new sections. Every fix is either:
- Completing an unfinished v4.1.0 fix (V1, V2, V3, V4, V5, V6)
- Applying a v4.1.0 fix that was never started (V7, V8)
- Correcting stale text from v4.0.0 that survived the v4.1.0 merge (V9, V10, V11, V12)
- Restoring a dropped element (keyboard nav test — audit recommendation #7)

### Decision 2: Version = v4.1.1

Patch version (not v4.2.0) because:
- No new findings (no Round 4 findings to add to Part 1)
- No architectural changes
- 16 coherence fixes, all mechanical/textual
- The v4.1.0 architecture is sound; only its execution was incomplete

### Decision 3: No new Part 1 findings

v4.1.1 does NOT add a "Round 4" section to Part 1. The 16 audit findings are **implementation defects in v4.1.0's execution of its own plan**, not new design-level findings. They will be tracked in Appendix A as "v4.1.1 Coherence Fixes" (rows 68–83) but do not get evidence-contract-formatted findings in Part 1.

**Rationale:** Adding a Round 4 to Part 1 would inflate the document with findings about its own typos and stale text. The audit is preserved as a separate artifact (`comparative_analysis_q4.1.md`); the corrections are tracked in the ledger.

### Decision 4: The coherence sweep is keyed to fix cross-references

Per the audit's V15 insight ("every failure lives at the boundary between a fixed section and an unfixed companion"), v4.1.1's execution strategy is a **coherence sweep** that follows each v4.1.0 fix's cross-references to every dependent section and verifies consistency. This is not a content pass — it is a trace pass.

### Decision 5: Target length = 3,900–4,100 lines

v4.1.0 was 3,886 lines. v4.1.1 adds:
- 15 Round 3 ledger rows in Appendix A (~20 lines)
- 6 Appendix F spot-check steps (~20 lines)
- F4/F5 test fixtures (~40 lines)
- Colon-outside blind spot + fixture (~10 lines)
- aria-label note (~3 lines)
- Keyboard nav test (~25 lines)
- Various textual corrections (~20 lines)
- Net additions: ~138 lines

Total: 3,886 + 138 ≈ 4,024 lines. Within the 3,900–4,100 target.

---

## IV. Bug Fix Registry (16 Round 4 coherence fixes)

| ID | Severity | Finding | Fix in v4.1.1 |
|----|----------|---------|---------------|
| V1 | High | §14.6 tests import `extractFrontmatter` (non-existent); no strip regression test; no pipeline `body` consumption | Rewrite §14.6 for `parseDocument`; add strip-regression + BOM + CRLF tests; add pipeline line in §5/§13.2 |
| V2 | High | Appendix A has 0 Round 3 rows; Closing says "v4.0.0" and "35 findings"; Appendix F has no Round 3 checks | Add 15 Round 3 rows to Appendix A; update all "35"/"v4.0.0" residue to "67"/"v4.1.1"; add 6 Appendix F checks |
| V3 | Medium | §5 skeleton omits `active.ts`; §5 annotation contradicts §7.4; §6.1 title wrong | Add `active.ts` to §5 skeleton; correct §5 annotation; retitle §6.1 |
| V4 | Medium | F4/F5 fixtures missing; §9.4 residuals undisclosed; §8.5 single-line-fence residual undisclosed | Add link/image parity fixtures to §9.3/§14.4; add fenced-`critical` to §14.8; add colon-outside to §14.3; disclose residuals in §9.4/§8.5 |
| V5 | Medium | §12.1 says "NODE_ENV not replaced"; amended 21.8 says "Vite does replace it" | Correct §12.1 to match amended 21.8 |
| V6 | Medium | 21.13 body still says "Verified"; Closing lists github-slugger under "Verified" | Complete 21.13 retag; trim Closing's "Verified (stable definitions)" to WCAG only |
| V7 | Low | §8.6 has no aria-label note | Add one-line note: visible text carries semantics; label is belt-and-suspenders |
| V8 | Low | §8.4 colon-outside absent; "first-level bullets" claim wrong | Add colon-outside to blind spots; correct "first-level" to "all indentation depths" |
| V9 | Low | §14.10 no rationale for 90→80 downgrade | Add rationale: jsdom limits on layout; core `lib/` 100% goal |
| V10 | Low | §10.4 and §17 Gate 5 don't name the encoded exclusion | Update wording to cite `[data-tag]` exclusion per §14.9 |
| V11 | Low | `test:integration` phantom in §17; §15.2/D.3 diverge | Add `test:integration` to §15.2; sync D.3; remove phantom script reference from §17 or define it |
| V12 | Low | Appendix B duplicate `TagRegistry`; missing `ParsedDocument`; stale path in Closing | Remove duplicate; add `ParsedDocument`; fix path to `v4.1.1.md` |
| V13 | Informational | No regressions | N/A (positive confirmation) |
| V14 | Informational | Count reconciliation correct | N/A (positive confirmation) |
| V15 | Informational | Systematic boundary-failure pattern | Informing the execution strategy (Decision 4) |
| V16 | Informational | v4.1.0 best base; needs coherence patch | Informing Decision 1 |

**Also restored (audit recommendation #7):** Keyboard navigation smoke test (was planned for v4.1.0 per the plan's §4 delta table "new keyboard-navigation smoke test (restored from draft_z2)" but was dropped during execution). Added to §14.9 and §17 Gate 7.

---

## V. Section-by-Section Delta (v4.1.0 → v4.1.1)

All v4.1.0 architecture is preserved. Changes are coherence fixes only.

| Section | Change | Fix ID |
|---------|--------|--------|
| Header comment | v4.1.1; add "Round 4 coherence patch" to lineage | — |
| YAML front matter | version: 4.1.1 | — |
| Document header | version 4.1.1; base document updated | — |
| §5 skeleton | Add `templates/active.ts` to file tree; correct `index.css` annotation to remove "+ template @theme import" | V3 |
| §5 pipeline | Add one line: `const { frontmatter, body } = parseDocument(markdown)` with `body` feeding enhance/buildToc/renderer | V1 |
| §6.1 | Retitle from "Editorial template `src/index.css`" to "Editorial template `src/templates/editorial/theme.css` (imported via `active.ts`)" | V3 |
| §8.4 | Add colon-outside-bold to disclosed blind spots; correct "only first-level bullets" to "all indentation depths of bullets" | V8 |
| §8.5 | Add disclosure of single-line-fence residual (language-less fenced block whose single-line content matches a badge value) | V4 |
| §8.6 | Add aria-label note: "Visible value + adjacent bold label carry the semantics; `aria-label` is belt-and-suspenders for integration tests (`getByLabelText`)" | V7 |
| §9.3 | Add 2 parity fixtures: `## Heading with [link](https://x.y)` and `## Alt text ![img](i.png)` | V4 |
| §9.4 | Add disclosure of residual edge cases: reference-style links (`[text][ref]`), HTML entities, footnote refs | V4 |
| §10.4 | Update gate text: "AAA `color-contrast` excludes `[data-tag]` badge elements per §14.9; `target-size` enforced globally. Exceptions are encoded, not suppressed." | V10 |
| §12.1 | Correct note: "Vite *does* replace `process.env.NODE_ENV` at build time (Finding 22.6); `import.meta.env.DEV` is used on idiom/portability grounds. The genuine bug was `process.env.ERROR_REPORTING_ENDPOINT` (Vite exposes only `import.meta.env.VITE_*`)." | V5 |
| §13.2 | Update memoization excerpt: `const { body } = useMemo(() => parseDocument(markdown), [markdown])` with `body` feeding downstream | V1 |
| §14.3 | Add colon-outside-bold fixture: `it("leaves colon-outside-bold variant untouched", ...)` | V4 |
| §14.4 | Add 2 test cases: linked heading slug, image heading slug | V4 |
| §14.6 | **Full rewrite**: import `parseDocument` (not `extractFrontmatter`); 7 test cases: strip regression, BOM, CRLF, absent, malformed, colons/quotes, template | V1 |
| §14.8 | Add 2 integration tests: fenced-`critical` stays `<code>` (not Badge); frontmatter absent from rendered output | V4 |
| §14.9 | Add keyboard navigation smoke test (restored from draft_z2); update AAA test comment to cite §10.3 by section number | V4, audit #7 |
| §14.10 | Add rationale for 90→80 downgrade: "jsdom limits on layout/template components; forcing 90% would incentivize low-value mock-heavy tests. Core `lib/` modules held to 100% goal." | V9 |
| §15.1 | (Already fixed in v4.1.0 — `preview &`/`wait-on` deleted) | — |
| §15.2 | Add `test:integration` script; sync with D.3 | V11 |
| §17 Gate 4 | Either define `test:integration` in §15.2 or change to `npm run test` (which runs all vitest suites) | V11 |
| §17 Gate 5 | Update wording: "AAA: contrast excludes `[data-tag]` (§14.9); target-size global" | V10 |
| Appendix A | Add 15 Round 3 ledger rows (22.1–22.15); update preamble to "67 findings (37 Round 1 + 15 Round 2 + 15 Round 3)"; update closing sentence | V2 |
| Appendix B | Remove duplicate `TagRegistry` row; add `ParsedDocument` row | V12 |
| Appendix C | Update fixture counts: enhance 9, toc 11, slug-parity 12, frontmatter 7, integration 6, axe 4 | V4 |
| Appendix D | Sync D.3 scripts with §15.2 | V11 |
| Appendix F | Add 6 Round 3 spot-check steps: parseDocument strip test, link-heading parity, fenced-`critical` fixture, AAA-on-badge-fixture, `active.ts` wiring grep, §12.1↔21.8 consistency | V2 |
| Closing | Fix "v4.0.0" → "v4.1.1" everywhere; fix "35 findings" → "67 findings"; fix stale path; trim "Verified (stable definitions)" to WCAG only; update confidence statement to "v4.1.1" | V2, V6, V12 |
| §21.13 | Complete retag: "Confidence: ~~Verified~~ → **Reasoned** (against package-export knowledge; confirm at install via gate V-1)" | V6 |

---

## VI. Quality Gates for the v4.1.1 Document Itself

Before the document is declared complete, verify:

1. **§14.6 imports `parseDocument`**, not `extractFrontmatter`. Every test case uses `parseDocument()` and checks `body`.
2. **Appendix A has 67 rows** (37 R1 + 15 R2 + 15 R3). Preamble says "67." Closing sentence says "67."
3. **Closing block says "v4.1.1"** and "Skill version: 4.1.1". No "v4.0.0" residue in the Closing.
4. **§5 skeleton includes `templates/active.ts`.** §5 `index.css` annotation does NOT say "+ template @theme import."
5. **§6.1 title references `templates/editorial/theme.css`**, not `src/index.css`.
6. **§8.4 blind spots include colon-outside-bold.** "First-level bullets" claim corrected to "all indentation depths."
7. **§8.6 has the aria-label note.**
8. **§9.3 has link/image parity fixtures.** §14.4 has corresponding test cases.
9. **§14.8 has fenced-`critical` and frontmatter-absent integration tests.**
10. **§14.9 has keyboard navigation smoke test.**
11. **§12.1 says "Vite *does* replace `process.env.NODE_ENV`"** — matching amended 21.8.
12. **Finding 21.13 body says "Reasoned"**, not "Verified."
13. **Closing "Verified (stable definitions)"** lists only WCAG thresholds — not Tailwind/github-slugger.
14. **§15.2 defines `test:integration`.** §17 Gate 4 cites only scripts defined in §15.2.
15. **Appendix B has no duplicate `TagRegistry`** and includes `ParsedDocument`.
16. **Appendix F has 6 Round 3 checks** (or the claim is deleted).
17. **§10.4 and §17 Gate 5** name the `[data-tag]` exclusion per §14.9.
18. **Closing path** is `markdown-to-web_SKILL_v4.1.1.md`, not `v4.md`.
19. **No "v4.0.0" residue** in Closing, Appendix A, or self-check items.
20. **Three hereditary Critical bugs stay dead:** no `@theme`-in-`@media`, no "14px relaxes AAA," no `dangerouslySetInnerHTML` in code.

---

## VII. Implementation Order (3 Phases)

### Phase 1: Coherence sweep — tests and pipeline (V1, V3, V4) — ~45 min

1. Rewrite §14.6 for `parseDocument` (7 test cases: strip regression, BOM, CRLF, absent, malformed, colons/quotes, template)
2. Add pipeline line in §5/§13.2: `const { frontmatter, body } = parseDocument(markdown)` with `body` feeding downstream
3. Add `active.ts` to §5 skeleton; correct §5 `index.css` annotation; retitle §6.1
4. Add link/image parity fixtures to §9.3 and §14.4
5. Add colon-outside fixture to §14.3
6. Add fenced-`critical` and frontmatter-absent tests to §14.8
7. Add keyboard navigation smoke test to §14.9
8. Add §8.4 colon-outside blind spot + correct "first-level" claim
9. Add §8.5 single-line-fence residual disclosure
10. Add §9.4 residual edge case disclosure
11. Add §8.6 aria-label note

### Phase 2: Coherence sweep — text and ledger (V2, V5, V6, V7, V8, V9, V10, V11, V12) — ~30 min

12. Add 15 Round 3 rows to Appendix A; update preamble/closing arithmetic to 67
13. Fix Closing: "v4.0.0" → "v4.1.1" everywhere; "35 findings" → "67 findings"; stale path
14. Complete 21.13 retag in finding body
15. Trim Closing "Verified (stable definitions)" to WCAG only
16. Correct §12.1 to match amended 21.8
17. Update §10.4 and §17 Gate 5 wording to name `[data-tag]` exclusion
18. Add `test:integration` to §15.2; sync D.3; fix §17 Gate 4
19. Fix Appendix B: remove duplicate `TagRegistry`, add `ParsedDocument`
20. Add §14.10 coverage rationale
21. Update Appendix C fixture counts
22. Add 6 Appendix F Round 3 checks

### Phase 3: Final consistency gate — ~15 min

23. Run all 20 quality gates (§VI)
24. Grep verification: no `extractFrontmatter` in §14.6; no "v4.0.0" in Closing; no "35 findings" in Appendix A; no "Verified" on 21.13
25. Line count check (3,900–4,100)
26. Save to `/home/z/my-project/download/markdown-to-web_SKILL_v4.1.1.md`

**Estimated total:** ~1.5 hours of focused composition.

---

## VIII. Explicit Assumptions

1. The user wants a single markdown file (the corpus convention).
2. v4.1.1 replaces v4.1.0; no backward compatibility required beyond Appendix A.
3. No new Part 1 findings — the 16 audit findings are implementation defects, not design-level findings.
4. The v4.1.0 architecture is sound; only its execution was incomplete. No architectural changes.
5. The keyboard navigation smoke test is restored from draft_z2 (it was planned in the v4.1 plan's §4 delta table but dropped during execution).
6. The evidence contract (§21) is preserved verbatim.
7. All version references throughout the document are updated to 4.1.1.

---

## IX. Confirmation Request

1. ✅ **Adopt v4.1.0 as base** + 16 coherence fixes (no architectural rewrite)?
2. ✅ **Fix all 16 Round 4 findings** per the Bug Fix Registry?
3. ✅ **No new Part 1 findings** (coherence fixes tracked in Appendix A only)?
4. ✅ **Target 3,900–4,100 lines**?
5. ✅ **Version as v4.1.1** (patch, not minor)?
6. ✅ **Save to `/home/z/my-project/download/markdown-to-web_SKILL_v4.1.1.md`**?
7. Any **specific additions, removals, or modifications**?

Awaiting your go-ahead to begin Phase 1.
