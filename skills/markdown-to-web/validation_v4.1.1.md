Validation Report: markdown-to-web_SKILL_v4.1.1.md 
 
Executive Summary 
 
Verdict: ✅ PASS — All 16 Round 4 coherence fixes correctly applied. No regressions detected. v4.1.1 is a clean coherence patch over v4.1.0. 
 
┌─────────────────────────────────────┬──────────────────────────────────────────┐ 
│ Metric                              │ Value                                    │ 
├─────────────────────────────────────┼──────────────────────────────────────────┤ 
│ v4.1.0 line count                   │ 3,886                                    │ 
├─────────────────────────────────────┼──────────────────────────────────────────┤ 
│ v4.1.1 line count                   │ 3,962                                    │ 
├─────────────────────────────────────┼──────────────────────────────────────────┤ 
│ Net change                          │ +76 lines (176 additions, 100 deletions) │ 
├─────────────────────────────────────┼──────────────────────────────────────────┤ 
│ Target range (per plan)             │ 3,900–4,100                              │ 
├─────────────────────────────────────┼──────────────────────────────────────────┤ 
│ Within target                       │ ✅ Yes                                   │ 
├─────────────────────────────────────┼──────────────────────────────────────────┤ 
│ 16 fixes verified                   │ 16/16                                    │ 
├─────────────────────────────────────┼──────────────────────────────────────────┤ 
│ Regressions detected                │ 0                                        │ 
├─────────────────────────────────────┼──────────────────────────────────────────┤ 
│ Hereditary Critical bugs still dead │ 3/3                                      │ 
└─────────────────────────────────────┴──────────────────────────────────────────┘ 
 
──────────────────────────────────────────────────────────────────────────────── 
 
Fix-by-Fix Verification 
 
### V1 (HIGH) — §14.6 tests rewritten for parseDocument ✅ 
 
┌───────────────────────────────────────────────────────────────────────────────────────┬───────────────────────────────────────────────────────┐ 
│ Check                                                                                 │ Result                                                │ 
├───────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────┤ 
│ §14.6 heading references parseDocument() not extractFrontmatter()                     │ ✅ Line 2606: "The API under test is parseDocument()" │ 
├───────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────┤ 
│ Import is parseDocument from @/lib/frontmatter                                        │ ✅ Line 2611                                          │ 
├───────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────┤ 
│ 7 test cases: strip regression, BOM, CRLF, absent, malformed, colons/quotes, template │ ✅ All present (lines 2614–2656)                      │ 
├───────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────┤ 
│ No extractFrontmatter in test code                                                    │ ✅ Only in historical Finding descriptions            │ 
├───────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────┤ 
│ Pipeline body consumption in §5/§13.2                                                 │ ✅ Confirmed                                          │ 
└───────────────────────────────────────────────────────────────────────────────────────┴───────────────────────────────────────────────────────┘ 
 
### V2 (HIGH) — Appendix A ledger + Closing version ✅ 
 
┌──────────────────────────────────────────────────────────┬─────────────────────┐ 
│ Check                                                    │ Result              │ 
├──────────────────────────────────────────────────────────┼─────────────────────┤ 
│ "All 67 findings (37 Round 1 + 15 Round 2 + 15 Round 3)" │ ✅ Line 3644        │ 
├──────────────────────────────────────────────────────────┼─────────────────────┤ 
│ No "35 findings" residue                                 │ ✅ 0 exact matches  │ 
├──────────────────────────────────────────────────────────┼─────────────────────┤ 
│ Closing says "v4.1.1"                                    │ ✅ Lines 3956, 3958 │ 
├──────────────────────────────────────────────────────────┼─────────────────────┤ 
│ "Skill version: 4.1.1"                                   │ ✅ Line 3958        │ 
├──────────────────────────────────────────────────────────┼─────────────────────┤ 
│ Appendix A has 15 Round 3 rows (22.1–22.15)              │ ✅ Lines 3646–3664  │ 
├──────────────────────────────────────────────────────────┼─────────────────────┤ 
│ 6 Appendix F Round 3 checks added                        │ ✅ Lines 3866–3873  │ 
└──────────────────────────────────────────────────────────┴─────────────────────┘ 
 
### V3 (MEDIUM) — Template wiring coherence ✅ 
 
┌───────────────────────────────────────────────────────────────────────────┬───────────────────────────────────┐ 
│ Check                                                                     │ Result                            │ 
├───────────────────────────────────────────────────────────────────────────┼───────────────────────────────────┤ 
│ active.ts in §5 skeleton                                                  │ ✅ Line 806, 12 occurrences total │ 
├───────────────────────────────────────────────────────────────────────────┼───────────────────────────────────┤ 
│ §5 index.css annotation says "NO template @theme — arrives via active.ts" │ ✅ Line 805                       │ 
├───────────────────────────────────────────────────────────────────────────┼───────────────────────────────────┤ 
│ No "template @theme import" in §5 annotation                              │ ✅ 0 matches                      │ 
├───────────────────────────────────────────────────────────────────────────┼───────────────────────────────────┤ 
│ §6.1 title references src/templates/editorial/theme.css                   │ ✅                                │ 
├───────────────────────────────────────────────────────────────────────────┼───────────────────────────────────┤ 
│ §5 annotation does not contradict §7.4                                    │ ✅ Consistent                     │ 
└───────────────────────────────────────────────────────────────────────────┴───────────────────────────────────┘ 
 
### V4 (MEDIUM) — F4/F5 fixtures + residuals ✅ 
 
┌─────────────────────────────────────────────────────────────────────────────────────┬────────────────────┐ 
│ Check                                                                               │ Result             │ 
├─────────────────────────────────────────────────────────────────────────────────────┼────────────────────┤ 
│ headingText() function with backtick → image → link → autolink normalization        │ ✅ Lines 1690–1697 │ 
├─────────────────────────────────────────────────────────────────────────────────────┼────────────────────┤ 
│ Applied before slugger.slug() in buildToc                                           │ ✅ Line 1710       │ 
├─────────────────────────────────────────────────────────────────────────────────────┼────────────────────┤ 
│ Colon-outside blind spot in §8.4                                                    │ ✅ Line 1482       │ 
├─────────────────────────────────────────────────────────────────────────────────────┼────────────────────┤ 
│ "All indentation depths" correction in §8.4                                         │ ✅ Line 1481       │ 
├─────────────────────────────────────────────────────────────────────────────────────┼────────────────────┤ 
│ Appendix C fixture counts updated (enhance 9, toc 11, frontmatter 7, integration 6) │ ✅ Lines 3696–3701 │ 
├─────────────────────────────────────────────────────────────────────────────────────┼────────────────────┤ 
│ §14.4 linked/image heading tests documented                                         │ ✅ Line 3697       │ 
└─────────────────────────────────────────────────────────────────────────────────────┴────────────────────┘ 
 
### V5 (MEDIUM) — §12.1 NODE_ENV contradiction resolved ✅ 
 
┌─────────────────────────────────────────────────────┬────────────────────────────┐ 
│ Check                                               │ Result                     │ 
├─────────────────────────────────────────────────────┼────────────────────────────┤ 
│ §12.1 says "Vite does replace process.env.NODE_ENV" │ ✅ Line 2213               │ 
├─────────────────────────────────────────────────────┼────────────────────────────┤ 
│ Matches amended Finding 21.8                        │ ✅ Both say the same thing │ 
├─────────────────────────────────────────────────────┼────────────────────────────┤ 
│ No "not replaced unless define" residue             │ ✅ Confirmed               │ 
└─────────────────────────────────────────────────────┴────────────────────────────┘ 
 
### V6 (MEDIUM) — 21.13 retag completed ✅ 
 
┌──────────────────────────────────────────────┬────────────────────────────────┐ 
│ Check                                        │ Result                         │ 
├──────────────────────────────────────────────┼────────────────────────────────┤ 
│ Finding 21.13 body retagged to "Reasoned"    │ ✅ ~~Verified~~ → **Reasoned** │ 
├──────────────────────────────────────────────┼────────────────────────────────┤ 
│ Closing "Verified" list trimmed to WCAG only │ ✅                             │ 
└──────────────────────────────────────────────┴────────────────────────────────┘ 
 
### V7 (LOW) — §8.6 aria-label note ✅ 
 
┌────────────────────────────────────┬──────────────────┐ 
│ Check                              │ Result           │ 
├────────────────────────────────────┼──────────────────┤ 
│ "belt-and-suspenders" note in §8.6 │ ✅ 2 occurrences │ 
└────────────────────────────────────┴──────────────────┘ 
 
### V8 (LOW) — §8.4 blind spots corrected ✅ 
 
┌──────────────────────────────────────────────────────┬──────────────┐ 
│ Check                                                │ Result       │ 
├──────────────────────────────────────────────────────┼──────────────┤ 
│ "All indentation depths" (not "first-level bullets") │ ✅ Line 1481 │ 
├──────────────────────────────────────────────────────┼──────────────┤ 
│ Colon-outside-bold added to blind spots              │ ✅ Line 1482 │ 
└──────────────────────────────────────────────────────┴──────────────┘ 
 
### V9 (LOW) — §14.10 coverage rationale ✅ 
 
┌────────────────────────────────────────────────────────┬──────────────┐ 
│ Check                                                  │ Result       │ 
├────────────────────────────────────────────────────────┼──────────────┤ 
│ "jsdom limits on layout/template components" rationale │ ✅ Line 2900 │ 
├────────────────────────────────────────────────────────┼──────────────┤ 
│ Core lib/ 100% goal stated                             │ ✅ Line 2900 │ 
└────────────────────────────────────────────────────────┴──────────────┘ 
 
### V10 (LOW) — Gate wording names [data-tag] exclusion ✅ 
 
┌─────────────────────────────────────────────────────────┬──────────────┐ 
│ Check                                                   │ Result       │ 
├─────────────────────────────────────────────────────────┼──────────────┤ 
│ §10.4: "enforced except on [data-tag] badge elements"   │ ✅ Line 1898 │ 
├─────────────────────────────────────────────────────────┼──────────────┤ 
│ §17 Gate 5: "color-contrast enforced except [data-tag]" │ ✅ Line 3105 │ 
└─────────────────────────────────────────────────────────┴──────────────┘ 
 
### V11 (LOW) — test:integration defined ✅ 
 
┌─────────────────────────────────┬──────────────────┐ 
│ Check                           │ Result           │ 
├─────────────────────────────────┼──────────────────┤ 
│ test:integration script present │ ✅ 4 occurrences │ 
├─────────────────────────────────┼──────────────────┤ 
│ §17 Gate 4 no longer phantom    │ ✅               │ 
└─────────────────────────────────┴──────────────────┘ 
 
### V12 (LOW) — Appendix B + Closing path ✅ 
 
┌──────────────────────────────┬──────────────┐ 
│ Check                        │ Result       │ 
├──────────────────────────────┼──────────────┤ 
│ ParsedDocument in Appendix B │ ✅ Line 3683 │ 
├──────────────────────────────┼──────────────┤ 
│ No duplicate TagRegistry row │ ✅ Clean     │ 
├──────────────────────────────┼──────────────┤ 
│ Closing path corrected       │ ✅           │ 
└──────────────────────────────┴──────────────┘ 
 
### V13–V16 (Informational) — Positive confirmations ✅ 
 
┌───────────────────────────────────────────────┬──────────────┐ 
│ Check                                         │ Result       │ 
├───────────────────────────────────────────────┼──────────────┤ 
│ No regressions to 35 v4.0.0 fixes             │ ✅ Confirmed │ 
├───────────────────────────────────────────────┼──────────────┤ 
│ Count reconciliation correct (37+15+15=67)    │ ✅           │ 
├───────────────────────────────────────────────┼──────────────┤ 
│ Systematic boundary-failure pattern addressed │ ✅           │ 
└───────────────────────────────────────────────┴──────────────┘ 
 
### Bonus: Keyboard navigation smoke test ✅ 
 
┌────────────────────────┬──────────────────┐ 
│ Check                  │ Result           │ 
├────────────────────────┼──────────────────┤ 
│ Restored from draft_z2 │ ✅ 2 occurrences │ 
└────────────────────────┴──────────────────┘ 
 
──────────────────────────────────────────────────────────────────────────────── 
 
Regression Analysis 
 
### Three Hereditary Critical Bugs — Still Dead ✅ 
 
┌─────────────────────────┬───────────────┬────────────────────────────────────────────────────────────────────────────────┐ 
│ Bug                     │ v4.1.1 status │ Evidence                                                                       │ 
├─────────────────────────┼───────────────┼────────────────────────────────────────────────────────────────────────────────┤ 
│ @theme-in-@media        │ Dead          │ @theme inline (19 occ, correct); @theme { (1 occ, in 21.1 rejection text only) │ 
├─────────────────────────┼───────────────┼────────────────────────────────────────────────────────────────────────────────┤ 
│ WCAG 14px arithmetic    │ Dead          │ "14px relaxes" (10 occ, all in rejection/finding text only)                    │ 
├─────────────────────────┼───────────────┼────────────────────────────────────────────────────────────────────────────────┤ 
│ dangerouslySetInnerHTML │ Dead          │ 20 occ, all in rejection/finding text only; none in code/pipeline              │ 
└─────────────────────────┴───────────────┴────────────────────────────────────────────────────────────────────────────────┘ 
 
### v4.1.0 Architecture — Fully Preserved ✅ 
 
┌────────────────────────────────────────┬──────────────────────────────────────────┐ 
│ Element                                │ Status                                   │ 
├────────────────────────────────────────┼──────────────────────────────────────────┤ 
│ Two-layer token pattern (§6.1)         │ Preserved — 19 @theme inline occurrences │ 
├────────────────────────────────────────┼──────────────────────────────────────────┤ 
│ Fence-aware scanner (fence.ts)         │ Preserved                                │ 
├────────────────────────────────────────┼──────────────────────────────────────────┤ 
│ Collision detection (validateRegistry) │ Preserved                                │ 
├────────────────────────────────────────┼──────────────────────────────────────────┤ 
│ Backtick-wrapping pipeline (§8.5)      │ Preserved                                │ 
├────────────────────────────────────────┼──────────────────────────────────────────┤ 
│ ErrorBoundary + ErrorFallback          │ Preserved                                │ 
├────────────────────────────────────────┼──────────────────────────────────────────┤ 
│ 250 KB bundle budget                   │ Preserved                                │ 
├────────────────────────────────────────┼──────────────────────────────────────────┤ 
│ All 35 Round 1+2 fixes                 │ Preserved                                │ 
├────────────────────────────────────────┼──────────────────────────────────────────┤ 
│ All 5 Round 3 headline fixes (F1–F5)   │ Preserved                                │ 
└────────────────────────────────────────┴──────────────────────────────────────────┘ 
 
### Diffs Are Surgical ✅ 
 
The 176 additions / 100 deletions are almost entirely: 
- New test cases in §14.6 
- New ledger rows in Appendix A 
- New Appendix F checks 
- Small textual corrections (blind spots, rationales, notes) 
- Version bumps 
 
No section was rewritten wholesale. No architectural mechanism was added, removed, or redesigned. 
 
──────────────────────────────────────────────────────────────────────────────── 
 
Alignment with Source Documents 
 
### Against comparative_analysis_q4.1_validation.md ✅ 
 
All 16 audit findings (V1–V16) are addressed. The audit's core insight — "every failure lives at the boundary between a fixed section and an unfixed companion" — is vindicated: each fix targets a specific boundary (§14.6↔§22.5, 
Appendix A↔Closing, §5↔§7.4, §8.4↔§14.3, §12.1↔§21.8, §10.4↔§14.9, etc.). 
 
### Against unified_skill_v4.1.1_IMPLEMENTATION_PLAN.md ✅ 
 
┌───────────────────────────────────────┬─────────────────────────┐ 
│ Plan item                             │ Delivered               │ 
├───────────────────────────────────────┼─────────────────────────┤ 
│ 5 architectural decisions locked      │ ✅ All followed         │ 
├───────────────────────────────────────┼─────────────────────────┤ 
│ 16-fix Bug Fix Registry               │ ✅ All 16 applied       │ 
├───────────────────────────────────────┼─────────────────────────┤ 
│ Section-by-section delta (26 changes) │ ✅ All present          │ 
├───────────────────────────────────────┼─────────────────────────┤ 
│ 20 quality gates (§VI)                │ ✅ All pass             │ 
├───────────────────────────────────────┼─────────────────────────┤ 
│ Target 3,900–4,100 lines              │ ✅ 3,962 lines          │ 
├───────────────────────────────────────┼─────────────────────────┤ 
│ 3-phase implementation order          │ ✅ Evident in structure │ 
└───────────────────────────────────────┴─────────────────────────┘ 
 
### Against markdown-to-web_SKILL_v4.1.md (no regressions) ✅ 
 
┌──────────────────────────────┬─────────────────────────────────────┐ 
│ v4.1.0 feature               │ Regressed?                          │ 
├──────────────────────────────┼─────────────────────────────────────┤ 
│ parseDocument() pipeline     │ No — enhanced, not replaced         │ 
├──────────────────────────────┼─────────────────────────────────────┤ 
│ active.ts wiring file        │ No — now correctly referenced in §5 │ 
├──────────────────────────────┼─────────────────────────────────────┤ 
│ AAA gate encoding [data-tag] │ No — §10.4/§17 wording improved     │ 
├──────────────────────────────┼─────────────────────────────────────┤ 
│ Frontmatter strip test       │ No — §14.6 rewritten correctly      │ 
├──────────────────────────────┼─────────────────────────────────────┤ 
│ headingText() normalization  │ No — fixtures added                 │ 
├──────────────────────────────┼─────────────────────────────────────┤ 
│ All Round 1–3 findings       │ No — all preserved                  │ 
└──────────────────────────────┴─────────────────────────────────────┘ 
 
──────────────────────────────────────────────────────────────────────────────── 
 
Minor Observations (non-blocking, pre-existing) 
 
1. generate-color-ref.mjs still reads src/index.css (line 1067) — this is a pre-existing pattern from v4.1.0, not a new regression. The editorial theme is now at templates/editorial/theme.css but the script path wasn't updated. This 
   is a documentation-level script path, not a load-bearing mechanism. It is outside the scope of the 16 coherence fixes and was not flagged by the Round 4 audit. 
 
2. extractFrontmatter name appears 4× in Part 1 (lines 482, 512, 3158, 3940) — these are all in finding descriptions documenting the v4.0.0 API that was replaced. This is correct: the finding text must name the old function to 
   describe the bug. Not a regression. 
 
──────────────────────────────────────────────────────────────────────────────── 
 
Conclusion 
 
markdown-to-web_SKILL_v4.1.1.md is a clean, surgical coherence patch that: 
 
1. ✅ Correctly applies all 16 Round 4 fixes from the validated audit 
2. ✅ Aligns with the v4.1.1 implementation plan's architecture and scope 
3. ✅ Introduces zero regressions against v4.1.0 
4. ✅ Keeps all three hereditary Critical bugs dead 
5. ✅ Maintains internal consistency across all cross-referenced sections (Closing, Appendix A, §5 skeleton, §14.6 tests, §10.4 gate, §17 gates) 
6. ✅ Hits the target length (3,962 lines, within 3,900–4,100) 
7. ✅ Passes all 20 quality gates defined in the plan 
 
The document is validation-complete against the three reference files. No further coherence work is needed at this scope. The remaining item (generate-color-ref.mjs path) is a pre-existing v4.1.0 minor inconsistency, not a v4.1.1 
regression.

---

Let me first locate every instance of the inconsistency in v4.1.1 to scope the surgical fix precisely. 

 
rg "generate-color-ref|readFileSync\("src/index\.css"|src/index\.css" in /home/pete/.pi/agent/skills/markdown-to-web/markdown-to-web_SKILL_v4.1.1.md ctx=3 
60 output lines 
 

Thinking... 

Now I have the complete picture. Let me analyze what needs to change and what must be preserved. 
 
Analysis 
 
The inconsistency: generate-color-ref.mjs reads src/index.css, but in v4.1.1 the editorial theme's :root {} block (the Layer-1 variables the script parses) lives in src/templates/editorial/theme.css (full listing in §6.1). The 
script's regex /:root\s*{([^}]*)}/ correctly captures light-mode variables — it just points at the wrong file. 
 
Lines that need changing (2): 
 
┌──────┬───────────────────────────────────────────────────────┬────────────────────────────┐ 
│ Line │ Current                                               │ Issue                      │ 
├──────┼───────────────────────────────────────────────────────┼────────────────────────────┤ 
│ 1062 │ ...parses the Layer-1 variables in `src/index.css`... │ Prose points to stale path │ 
├──────┼───────────────────────────────────────────────────────┼────────────────────────────┤ 
│ 1067 │ const css = readFileSync("src/index.css", "utf8");    │ Code points to stale path  │ 
└──────┴───────────────────────────────────────────────────────┴────────────────────────────┘ 
 
Lines that must NOT change (verified correct): 
 
┌────────────┬────────────────────────────────────────────────────┬─────────────────────────────────────────────────────────────────┐ 
│ Line       │ Content                                            │ Why preserve                                                    │ 
├────────────┼────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────┤ 
│ 473        │ Finding 22.2 description of v4.0.0 behavior        │ Historical finding text                                         │ 
├────────────┼────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────┤ 
│ 851        │ §5 skeleton annotation                             │ No file path mentioned                                          │ 
├────────────┼────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────┤ 
│ 1304       │ "src/index.css contains no template @theme import" │ Factually correct — index.css has base styles only              │ 
├────────────┼────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────┤ 
│ 1991       │ "Google Fonts @import is in src/index.css"         │ Factually correct — fonts are in base index.css                 │ 
├────────────┼────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────┤ 
│ 3859, 3901 │ Appendix F spot-checks                             │ Runtime verification instructions with dist/index.html fallback │ 
└────────────┴────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────────────┘ 
 
Regex correctness check: The script's /:root\s*{([^}]*)}/ correctly matches only the light-mode :root block (the :root:not([data-theme="light"]) dark-mode block has :not(...) between :root and {, so it won't match). No regex change 
needed. 
 
──────────────────────────────────────────────────────────────────────────────── 
 
Surgical Edit Plan 
 
Exactly 2 edits, touching §6.3 only: 
 
Edit 1 — Line 1062 (prose): 
 
``` 
  old: ...parses the Layer-1 variables in `src/index.css` and emits... 
  new: ...parses the Layer-1 variables in `src/templates/editorial/theme.css` (imported via `active.ts`) and emits... 
``` 
 
Edit 2 — Line 1067 (code): 
 
``` 
  old: const css = readFileSync("src/index.css", "utf8"); 
  new: const css = readFileSync("src/templates/editorial/theme.css", "utf8"); 
``` 
 
Scope guard: No other lines change. The §5 skeleton annotation, §7.4 wiring rules, §11.1 font caveat, and Appendix F spot-checks are all correct as-is. 
 
Verification after edit: 
1. Grep for readFileSync — exactly 1 match, pointing to templates/editorial/theme.css 
2. Grep for generate-color-ref — all references consistent 
3. Confirm lines 473, 1304, 1991 untouched 
4. Line count: +2 lines (net, due to slightly longer path string) 
 
---

Edit Complete — Verified ✅ 
 
### What changed (2 edits, §6.3 only) 
 
┌───┬──────┬───────────────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────┐ 
│ # │ Line │ Before                                                │ After                                                                                                │ 
├───┼──────┼───────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────┤ 
│ 1 │ 1062 │ ...parses the Layer-1 variables in `src/index.css`... │ ...parses the Layer-1 variables in `src/templates/editorial/theme.css` (imported via `active.ts`)... │ 
├───┼──────┼───────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────┤ 
│ 2 │ 1067 │ readFileSync("src/index.css", "utf8")                 │ readFileSync("src/templates/editorial/theme.css", "utf8")                                            │ 
└───┴──────┴───────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────┘ 
 
### What was preserved (verified untouched) 
 
┌──────┬────────────────────────────────────────────────────────────────────┬────────────────────────────────────────────────────────┐ 
│ Line │ Content                                                            │ Why                                                    │ 
├──────┼────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤ 
│ 473  │ Finding 22.2: "src/index.css statically imports exactly one theme" │ Historical finding text describing v4.0.0              │ 
├──────┼────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤ 
│ 1304 │ "src/index.css contains no template @theme import"                 │ Factually correct — base index.css has no template CSS │ 
├──────┼────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤ 
│ 1991 │ "Google Fonts @import is in src/index.css"                         │ Factually correct — fonts are in base index.css        │ 
└──────┴────────────────────────────────────────────────────────────────────┴────────────────────────────────────────────────────────┘ 
 
### Verification results 
 
- ✅ No src/index.css remains in the color-ref context 
- ✅ Both color-ref path references now consistently point to src/templates/editorial/theme.css 
- ✅ The readFileSync in the bundle-size test (line 2387, different script) was not touched 
- ✅ Line count: 3962 (no structural change — purely in-place text replacement) 
- ✅ The script's regex (/:root\s*{([^}]*)}/) remains correct — it captures the light-mode :root block in the editorial theme CSS, and the :root:not([data-theme="light"]) dark-mode block won't match (:not(...) sits between :root and 
  {) 
 
The pre-existing v4.1.0 inconsistency is now resolved. The generate-color-ref.mjs script reads from the same file that §6.1 lists as the editorial template's full CSS, and the prose description matches the code.

