# Audit — `markdown-to-web` v4.1.0 (post-fix review)

**Mode C (Audit/Review).** Scope: (1) did v4.1.0 actually implement its 15 claimed Round 3 fixes; (2) did it regress any v4.0.0 fix; (3) how it compares to the earlier five editions. All checks are textual — nothing executed. Contradictions quoted from the text are **Verified (textual)**; behavior claims are **Reasoned**.

---

## 1. Executive summary

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 2 |
| Medium | 4 |
| Low | 6 |
| Informational | 4 |

**Verdict: v4.1.0 is the strongest edition in the corpus — and its headline claim ("all 15 fixed") is overstated.** The three hereditary Critical bugs stay dead, all 35 v4.0.0 fixes survive, and the Part 1 audit layer (findings, count reconciliation, confidence retags) was updated meticulously. But the fix-batch was **front-loaded**: code-level fixes landed in Part 1 and the core `lib/` sections, while the *verification and traceability layers* — tests, skeleton, appendices, closing ledger — were left stale. Fix-application scorecard:

| Status | Findings | Evidence |
|---|---|---|
| **Fully applied (7)** | 22.1, 22.7, 22.8, 22.10, 22.13, 22.14, 22.15 | §14.9 encoded exclusion ✓ · §3.1 rewritten ✓ · §6.1 cascade comment corrected ✓ · CI `wait-on` deleted ✓ · §23 Lessons ✓ · gate V-1 retained ✓ · provenance cites filename+version ✓ |
| **Partial — coherence debt (6)** | 22.2, 22.3, 22.4, 22.5, 22.6, 22.12 | Mechanism/function/guard/amendment written, but contradicting or missing companion sections (§4 below) |
| **Not applied (2)** | 22.9, 22.11 | §8.6 aria-label note absent; §8.4 colon-outside blind spot + fixture absent |

The irony worth naming plainly: v4.1.0 codified **Lesson 10 — "Fix-batches create inconsistencies — re-audit the fixes"** (§23) and then, in the same pass, committed exactly that failure mode six times.

---

## 2. High findings

**V1 — Frontmatter test layer is broken against the F3 implementation** *(Finding 22.3 fix incomplete)*
- **Location:** §14.6 vs §22.5; §5 pipeline
- **Evidence:** §22.5 defines only `parseDocument()` (returns `{ frontmatter, body }`). §14.6's six tests all `import { extractFrontmatter } from "@/lib/frontmatter"` — a function that no longer exists. The promised regression test *"frontmatter block does not render as content"* is nowhere in §14, and §22.5's own docstring points to it: "(regression test: §14.6)". No Part 2 section shows the pipeline consuming `body` (App.tsx wiring is never sketched).
- **Impact:** Gate 3 fails as written for anyone implementing to spec; F3's strip behavior is unverified by construction — the exact gap F3 was created to close.
- **Severity:** High · **Confidence:** Verified (textual)
- **Fix:** Rewrite §14.6 against `parseDocument` (body-strip regression + BOM + CRLF cases); add one pipeline line in §5/§13.2 showing `const { frontmatter, body } = parseDocument(markdown)` with `body` feeding enhance/buildToc/renderer.

**V2 — Ledger and version integrity: the traceability system contradicts itself** 
- **Location:** header comment + §1.4 vs Appendix A + Appendix F + Closing
- **Evidence:**
  - Header: Round 3 fixes "all fixed in this edition (Part 1 §22; **Appendix A**)"; §1.4 claims Appendix A has "**67 rows**" and Appendix F has "**(+6 Round 3 checks)**".
  - Appendix A preamble: "Every finding from Part 1 (**Round 1 + Round 2**)" — contains **zero Round 3 rows**; closing sentence: "All **35 findings (20 Round 1 + 15 Round 2)**… resolved".
  - Appendix F is byte-identical to v4.0.0's — steps 1–7 and the same six Critical-fix checks; no Round 3 checks added.
  - Closing block: "End of `markdown-to-web` **v4.0.0** unified skill specification. Skill version: **4.0.0**" — while the YAML frontmatter says `version: 4.1.0`.
- **Impact:** A document whose §1.0 declares "An audit's arithmetic must survive its own audit" fails that standard in three places: a reader tracing any Round 3 fix through Appendix A finds nothing; the self-version is internally contradictory.
- **Severity:** High · **Confidence:** Verified (textual)
- **Fix:** Add 15 Round 3 rows to Appendix A; update preamble/closing arithmetic (52 resolved in v4.0.0 + 15 in v4.1.0 = 67); set Closing block to v4.1.0; either add the six Appendix F checks (strip, link-heading parity, fenced-`critical`, AAA-on-badge-fixture, `active.ts` wiring, §12.1↔21.8 consistency) or delete the claim.

## 3. Medium findings

**V3 — Template wiring fix landed, but three sections disagree on where theme CSS lives** *(22.2 partial)*
§7.4 ships the excellent `templates/active.ts` mechanism and explicitly states "`src/index.css` contains no template `@theme` import." Yet: §5 skeleton **omits `templates/active.ts`** entirely; the §5 `index.css` annotation reads "Tailwind v4 @import + Google Fonts **+ template @theme import**" (direct contradiction); §6.1 is still titled "Editorial template **`src/index.css`** (full listing)" while §7.4 imports the theme from `templates/editorial/theme.css`. An implementer cannot determine the source of truth. → Add `active.ts` to §5; correct the §5 annotation; retitle §6.1 to the template path.

**V4 — F4/F5 shipped as code without their promised fixtures** *(22.4, 22.5, 22.11 partial)*
`headingText()` (§9.2) and the code-block guard (§8.5) are correct as written, but: no link/image-heading parity fixtures in §9.3/§14.4; no fenced-block-containing-`critical` fixture in §14.8; no colon-outside fixture in §14.3; §9.4 still doesn't disclose residual edge cases (reference-style links, HTML entities). Additionally, the §8.5 guard (`text.includes("\n")`) leaves a residual risk for **single-line, language-less fenced blocks** whose content exactly matches a badge value (mdast code values carry no trailing newline) — undisclosed. Code without fixtures violates this corpus's own rule ("assertion is not verification," Lesson 11).

**V5 — §12.1 contradicts the amended Finding 21.8** *(22.6 partial)*
Amended 21.8 now correctly states "Vite *does* replace `process.env.NODE_ENV` at build time." §12.1's inherited note still says "`process.env.NODE_ENV` is **not** replaced unless `define` is explicitly configured." Same fact, opposite claims, one document. → Correct §12.1 (keep the `import.meta.env.DEV` recommendation on idiom/portability grounds).

**V6 — Confidence retag applied in one place, not two** *(§1.1 amendment half-executed)*
§1.1 declares both 21.1 and 21.13 retagged to Reasoned. Finding 21.1's body shows "Verified → Reasoned" ✓; Finding **21.13's body still reads "Confidence: Verified"** ✗; and the Closing still lists "Tailwind v4 `@theme` semantics" and "github-slugger 2.0.0 package exports" under "**Verified** (from stable external definitions)" ✗ — the very category §1.1 says should be Reasoned (library behavior, not normative definitions). Only the WCAG thresholds belong in that category.

## 4. Low findings

- **V7 (22.9 not applied):** §8.6 has no note that badge semantics are carried by visible text, not the `aria-label` on the generic span.
- **V8 (22.11 not applied + inherited inaccuracy):** `**Tag**:` colon-outside-bold still absent from §8.4 blind spots; and the retained "only first-level bullets are targeted" claim is wrong — `BADGE_LINE_RE`'s `^\s*` matches indented bullets (verified against the regex).
- **V9 (22.12 half-applied):** §14.10 states the core-`lib/` 100% goal but gives no rationale for the 90→80/75 project-wide downgrade from draft_q3.
- **V10 — Gate wording drift:** §10.4 ("No suppressions") and §17 Gate 5 ("color-contrast are gate-failures") were not updated to name the encoded badge exclusion now in §14.9 — the distinction between *encoded exception* and *suppression* is exactly what Finding 22.1 was about.
- **V11 — Script discipline drift:** §15.2 and Appendix D.3 carry divergent script listings (`test:watch`, `build:analyze` only in D.3); §17 Gate 4 cites `npm run test:integration`, which is defined in neither (draft_q3's "no phantom scripts" rule, silently abandoned).
- **V12 — Index staleness:** Appendix B omits the new `ParsedDocument` type, retains a duplicate `TagRegistry` row and a phantom "C.5" cross-reference; Closing retains the stale artifact path `markdown-to-web_SKILL_v4.md`.

## 5. Informational

- **V13 — No regressions (verified across the text):** two-layer theming intact (§6.1); `text-xs` + enumerated exceptions intact (§8.6, §10.1, §10.3); no `dangerouslySetInnerHTML`; fence scanner, slug reservation, collision detection, ErrorBoundary, 250 KB budget all present. All 35 v4.0.0 resolutions survive.
- **V14 — The count reconciliation is a genuine advance:** I re-derived the tallies from the finding text — Round 1 = 5H/8M/6L/18I = 37, Round 2 = 3C/2H/7M/3L = 15, Round 3 = 2H/4M/6L/3I = 15, total 67 — and §1.0's table is **exactly right**. (Which makes the stale "35" arithmetic in Appendix A/Closing — V2 — a self-inflicted wound rather than a hard problem.)
- **V15 — Cross-cutting pattern:** the failure distribution is systematic, not random: every High/Medium finding above lives at the *boundary* between a fixed section and an unfixed companion (test vs. implementation, mechanism vs. skeleton, amendment vs. dependent note, claim vs. appendix). The next pass should be a **coherence sweep keyed to each fix's cross-references**, not another content pass.
- **V16 — Edition comparison verdict:**

| Edition | Standing after v4.1 | Still the best at |
|---|---|---|
| **v4.1.0** | Best base; needs a coherence patch (v4.1.1), not new architecture | Breadth + corrected mechanics + 3-round audit record |
| v4.0.0 | Superseded; its closing boilerplate now partially lives inside v4.1 (see V2) | — |
| draft_q3 | Leanest correct core; per-line still tighter than v4.1 | Pipeline diagram, script single-source discipline, no stale seams |
| draft_z2 | Feature reference only | ErrorReporter in mainline, keyboard-nav test file (v4.1 dropped the planned restoration) |
| v2.1.0 | Preserved as the Round 1 record | Audit format; unsafe as build spec |
| draft_d2 | Parts donor only | Template CSS + 6-week plan (both absorbed) |

## 6. Recommended fix list (v4.1.0 → v4.1.1)

1. **V1:** rewrite §14.6 for `parseDocument`; add strip-regression + BOM + CRLF tests; show `body` consumption in the pipeline.
2. **V2:** 15 Round 3 rows in Appendix A; fix all "35 findings"/"v4.0.0" residue in Appendix A and Closing; add the six Appendix F checks or delete the claim.
3. **V3:** `active.ts` into §5 skeleton; reconcile §5/§6.1/§7.4 theme location.
4. **V4:** add link/image parity fixtures, fenced-`critical` fixture, colon-outside fixture; disclose §9.4 residuals and the §8.5 single-line-fence residual.
5. **V5 + V6:** correct §12.1; complete the 21.13 retag; trim Closing's "Verified (stable definitions)" list to WCAG only.
6. **V7–V12:** the six textual fixes as itemized (each is a one- to three-line edit).
7. Restore the keyboard-navigation smoke test (planned for v4.1, dropped — §14.9/§17 Gate 7).

## 7. Verification ledger

| Check | Method | Result |
|---|---|---|
| All 15 Round 3 fix claims vs Part 2 text | Full-text cross-reference | 7 full / 6 partial / 2 missing — Verified (textual) |
| All 35 v4.0.0 resolutions | Grep-style scan for `@theme`-in-`@media`, 14px claim, `dangerouslySetInnerHTML`, fence scanner, collision detection | No regressions — Verified (textual) |
| §1.0 severity tallies (37/15/15 = 67) | Re-derived from finding text | Correct — Verified (textual) |
| Runtime behavior of every snippet | Not executable here | Unverifiable — Appendix F remains the conversion path |

**Bottom line:** v4.1.0 fixed the right things and broke nothing — but it declared completion one coherence pass early. The v4.1.1 work is small, mechanical, and entirely test/text reconciliation; no architectural change is needed.
