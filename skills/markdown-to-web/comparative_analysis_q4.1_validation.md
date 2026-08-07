**1. Validated the Round 4 audit (`comparative_analysis_q4.1.md`):**

I cross-checked every one of the 16 findings against the v4.1.0 source file using targeted grep and read operations. **All 16 findings are accurate.** The audit is devastatingly precise — it identified that v4.1.0 front-loaded code-level fixes while leaving verification/traceability layers stale. The key findings:

- **V1 (High):** §14.6 tests import `extractFrontmatter` — a function that no longer exists. `parseDocument()` replaced it in §22.5 but the tests were never updated. The strip regression test F3 was created to fix is unverified by construction.
- **V2 (High):** Appendix A has zero Round 3 rows despite the header claiming "all fixed in this edition (Appendix A)." The Closing still says "v4.0.0" and "35 findings" while the YAML says `version: 4.1.0`. The self-version is internally contradictory.
- **V3 (Medium):** §7.4 ships `active.ts` but §5 skeleton omits it, §5 annotation contradicts §7.4 on where theme CSS lives, and §6.1 title references the wrong file.
- **V4 (Medium):** F4 (`headingText()`) and F5 (code-block guard) shipped as code without their promised test fixtures.
- **V5 (Medium):** §12.1 says "NODE_ENV is not replaced" while the amended Finding 21.8 says "Vite does replace it" — same fact, opposite claims, one document.
- **V6 (Medium):** Finding 21.13's body still reads "Verified" despite §1.1 declaring it retagged to "Reasoned."

The audit's core insight (V15): "every failure lives at the boundary between a fixed section and an unfixed companion." The irony: v4.1.0 codified Lesson 10 — "Fix-batches create inconsistencies — re-audit the fixes" — and then committed exactly that failure mode six times.

**2. Validated the prior v4.1 plan:**

The `unified_skill_v4.1_IMPLEMENTATION_PLAN.md` was sound but incompletely executed. Its §7 "Final consistency gate" listed 6 checks — every one was violated by the actual v4.1.0 output. The plan itself was correct; its execution was the problem.

**3. Created the v4.1.1 implementation plan:**

The plan locks 5 architectural decisions:
- **v4.1.1 is a coherence patch** (not a new edition) — no new architecture, no new code patterns
- **Version = v4.1.1** (patch, not minor) — 16 mechanical/textual fixes
- **No new Part 1 findings** — the 16 audit findings are implementation defects, not design-level findings; tracked in Appendix A as rows 68–83
- **Coherence sweep keyed to fix cross-references** — per V15's insight, follows each fix's cross-references to every dependent section
- **Target 3,900–4,100 lines** (v4.1.0 + ~138 lines of fixtures/tests/ledger rows)

The plan registers all 16 fixes, provides a section-by-section delta (26 changes across 20 sections), defines 20 quality gates, and specifies a 3-phase implementation order (~1.5 hours total). The key insight from the audit: "The v4.1.1 work is small, mechanical, and entirely test/text reconciliation; no architectural change is needed."

### What you should do next

Review the plan's 7 confirmation items in §IX. Once you confirm, I'll execute the 3-phase coherence sweep and deliver `markdown-to-web_SKILL_v4.1.1.md`. The work is small and mechanical — completing unfinished v4.1.0 fixes, not designing new architecture.
