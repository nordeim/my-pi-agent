# Unified Skill v4.1.0 — Meticulous Implementation Plan

**Date:** 2026-08-07  
**Base:** `markdown-to-web_SKILL_v4.md` (v4.0.0, 3,667 lines) — the most correct and complete prior edition  
**Trigger:** Round 3 self-audit (15 new findings from `comparative_analysis_q4.md`), all validated against the v4.0.0 source  
**Target:** One self-contained skill file, `markdown-to-web_SKILL_v4.1.md`, estimated 3,400–3,800 lines  
**Confidence:** Reasoned (design document; no code execution in this environment)

---

## I. Validation of the Round 3 Audit

### 1.1 Audit document reviewed

`comparative_analysis_q4.md` (199 lines) — a Mode C audit of five skill editions (draft_z2, draft_q3, v2.1.0, draft_d2, v4.0.0). The audit identifies 26 findings (3 Critical, 5 High, 7 Medium, 6 Low, 5 Informational) and ranks v4.0.0 as the most correct edition while surfacing 11 open defects within it.

### 1.2 Validation method

Each Round 3 finding was cross-checked against the v4.0.0 source file (`/home/z/my-project/download/markdown-to-web_SKILL_v4.md`, 3,667 lines) using targeted grep and read operations. The validation confirms:

| Finding | Audit claim | Validation against v4.0.0 source | Verdict |
|---------|-------------|----------------------------------|---------|
| **H4** — AAA gate contradicts exceptions | §14.9 hard-fails `color-contrast` while §10.3 documents badge contrast as accepted exception | **Confirmed.** v4.0.0 line 2645: `["color-contrast", "target-size"].includes(v.id)` — hard-fails ALL color-contrast violations. §10.3 lines 1730–1736 documents 5 badge accent tokens as "AAA ✗ | Exception." The gate would fail on any page containing a badge. | **Valid — must fix** |
| **H5** — Template switching unwritten | §7.4 says "the build system loads the template" with no mechanism | **Confirmed.** v4.0.0 line 1178: "The build system loads the template specified in frontmatter (or the default `editorial`)..." — no Vite plugin, no virtual module, no `active.ts` wiring file exists in the §5 skeleton. | **Valid — must fix** |
| **M1** — Frontmatter never stripped | `extractFrontmatter` returns metadata only; no strip step | **Confirmed.** v4.0.0 line 3288: `export function extractFrontmatter(markdown: string): Frontmatter` — returns `Frontmatter` (metadata object), not `{ frontmatter, body }`. No pipeline step strips the `---…---` block. The frontmatter would render as `<hr><p>title: …</p><hr>`. | **Valid — must fix** |
| **M2** — Slug parity omits linked/image headings | `buildToc` strips backticks only; links/images desync | **Confirmed.** v4.0.0 §9.2 line 2338: `const text = match[2].replace(/`/g, "").trim();` — backticks only. §9.3 fixture list (lines 2360–2370) contains no link or image heading case. | **Valid — must fix** |
| **M3** — Badge misfire on unclassed code blocks | `components.code` treats "no className" as inline; fenced block with no language + content `critical` renders as Badge | **Confirmed.** v4.0.0 §8.5 line 1372: `const isBlock = Boolean(className);` — no single-line check. A fenced block ``` ```\ncritical\n``` ``` with no language and `rehype-highlight` off would match `resolveBadge("critical")`. | **Valid — must fix** |
| **M7 (→22.6)** — Finding 21.8 overstates `process.env` breakage | Vite DOES replace `process.env.NODE_ENV` at build time | **Confirmed as accurate critique.** Vite's `define` config replaces `process.env.NODE_ENV` by default. The v4.0.0 finding 21.8 rationale ("not available in a Vite browser build unless explicitly defined") is inaccurate. The recommendation (`import.meta.env.DEV`) is still correct on idiom/portability grounds. The genuine draft_d2 bug was `process.env.ERROR_REPORTING_ENDPOINT` (Vite exposes only `import.meta.env.VITE_*`). | **Valid — amend rationale** |
| **L1 (→22.7)** — §3.1 "requires LF" contradicts §22.5 CRLF code | §3.1 says LF-only; §22.5 code normalizes CRLF | **Confirmed.** v4.0.0 §22.5 line 3286: "requires LF line endings and no BOM at file start" while line 3290: `markdown.replace(/\r\n/g, "\n")` — code handles CRLF. Internal contradiction. | **Valid — must fix** |
| **L2 (→22.8)** — §6.1 "equal specificity" comment false | `:root:not([data-theme="light"])` is (0,2,0); `[data-theme="dark"]` is (0,1,0) — not equal | **Confirmed.** CSS specificity arithmetic is stable and verifiable. The comment is wrong; behavior is still correct (both branches set identical values). | **Valid — fix comment** |
| **L3 (→22.9)** — `aria-label` on generic span | ARIA 1.2 forbids accessible names on generic elements | **Confirmed as accurate.** ARIA 1.2 does restrict accessible names on generic elements. The visible value + bold label carry semantics. The `aria-label` is belt-and-suspenders used by integration tests (`getByLabelText`). | **Valid — add note, keep attribute** |
| **L4 (→22.11)** — `**Tag**:` colon-outside undocumented | Regex requires colon inside bold; variant not disclosed | **Confirmed.** v4.0.0 §8.4 regex: `\*\*([^*]+):\*\*` — colon must be inside. The variant `**Tag**: value` does not match and is not in the blind-spots list. | **Valid — disclose + add fixture** |
| **L5 (→22.10)** — CI `preview &` + `wait-on` redundant | Playwright `webServer` already boots preview; `wait-on` undeclared | **Confirmed.** v4.0.0 §15.1 CI YAML runs `npm run preview &` and `npx wait-on http://localhost:4173`. `wait-on` is not in devDependencies. `playwright.config.ts` §14.10 line 2825: `webServer: { command: "npm run preview", port: 4173 }` — already boots the server. | **Valid — delete redundant steps** |
| **L6** — Two "v2.0.0" editions; draft_d2 generation artifacts | Provenance ambiguity | **Confirmed.** draft_z2 and draft_d2 both self-version "2.0.0". | **Valid — cite filename + version** |
| **I3** — v4.0.0 tags C1 as "Verified" without execution | Evidence contract self-violation | **Confirmed.** v4.0.0 Finding 21.1 line 359: "Confidence: Verified (Tailwind v4 documentation confirms...)" — no execution. Per the evidence contract, unexecuted claims about library behavior are Reasoned. | **Valid — retag** |
| **I5** — Coverage 90→80 downgrade unexplained | Silent guardrail weakening | **Confirmed.** draft_q3 §12.2 had 90%; v4.0.0 §14.10 has 80/75% with no rationale. | **Valid — add rationale** |
| **H3** — Missing `await` on async `processMarkdown` (draft_d2) | Crash-grade defect in draft_d2 | **Confirmed as a draft_d2-only bug.** v4.0.0 does not use `processMarkdown` (it uses `enhanceMarkdown` + `ReactMarkdown` directly, synchronously). Not a v4.0.0 defect — but worth noting in the ledger as a draft_d2-only finding. | **Valid — historical, not a v4.0.0 defect** |

**Validation verdict: all 15 Round 3 findings are accurate.** The audit is rigorous and its recommendations are sound. The proposed `draft_q4.1.md` implements all 15 correctly.

---

## II. Validation of the Proposed v4.1 Implementation Plan and Draft

### 2.1 Implementation plan reviewed

`unified_skill_v4.1_IMPLEMENTATION_PLAN.md` (146 lines) — proposes 6 decisions (D1–D6), 15 Round 3 findings to absorb, 5 concrete fix specifications (F1–F5), a section-by-section delta, a 5-pass execution strategy, a pre-mortem, and a final consistency gate.

### 2.2 Draft skill reviewed

`draft_q4.1.md` (4,067 lines) — a 5-pass assembled draft implementing the plan. Contains Part 1 (67 findings across 3 rounds), Part 2 §1–§23, Appendices A–F, and a final consistency gate.

### 2.3 Validation of the 6 decisions

| Decision | Plan's choice | Validation | Verdict |
|----------|--------------|------------|---------|
| **D1** — AAA gate vs exceptions | Keep default accents; encode exceptions in axe test via `[data-tag]` exclusion; `target-size` stays global; §10.5 recipe remains opt-in | **Correct.** This makes the gate enforce exactly what §10.3 claims — honest by construction. The alternative (making §10.5 the default) would silently shift the palette and lose the v1.0.1 editorial identity. The `[data-tag]` exclusion is an enumerated exception, not a rule suppression — badges carry `data-tag` by construction (§8.6), and if they ever stop carrying it, the exclusion becomes a no-op and the gate fails closed. | **Adopt** |
| **D2** — Template switching | One wiring file `src/templates/active.ts`; frontmatter `template` becomes advisory with dev-mode warning | **Correct.** Honors draft_q3's rejected-`virtual:`-module decision. Replaces v4.0.0 §7.4's overpromise with a concrete, written mechanism. The wiring file is one line to edit — honest and minimal. The dev-mode mismatch warning is a good safety net. | **Adopt** |
| **D3** — Frontmatter API | `parseDocument()` returns `{ frontmatter, body }`; BOM stripped, CRLF normalized; "LF-only" limitation deleted | **Correct.** Fixes the render artifact (M1) and closes the §3.1/§22.5 contradiction (L1) in one move. The `body` is what feeds `buildToc`/`enhanceMarkdown`/`ReactMarkdown`. | **Adopt** |
| **D4** — Badge text size | Stays `text-xs` (12px); no revival of 14px claim | **Correct.** Already correct in v4.0.0. The 14px claim was an arithmetic error (Finding 21.2). Reasserting explicitly prevents future regression. | **Adopt** |
| **D5** — Coverage thresholds | Keep 80/75 project-wide with explicit rationale; core `lib/` held to 100% goal | **Correct.** Resolves the silent 90→80 downgrade (I5) without pretending layout code is cheaply coverable in jsdom. The rationale (jsdom limits on layout/template components) is accurate. | **Adopt** |
| **D6** — `aria-label` on badge span | Keep, with a one-line note about visible text carrying semantics | **Correct.** Dropping it loses nothing measurable but breaks integration tests that use `getByLabelText`. Adding a role would pollute the document outline. The belt-and-suspenders approach with a documentation note is the right call. | **Adopt** |

### 2.4 Validation of the 5 fix specifications (F1–F5)

| Fix | Plan's specification | Validation | Verdict |
|-----|---------------------|------------|---------|
| **F1** — AAA gate with encoded exceptions | Exclude `[data-tag]` nodes from AAA `color-contrast`; `target-size` stays global | **Correct.** The draft_q4.1 §14.9 implementation uses `.exclude("[data-tag]")` for the contrast run and a separate `.withRules(["target-size"])` run for target size. This is the correct axe-core API usage — `exclude` is a context-level exclusion, not a rule disable. The exclusion fails closed (if `data-tag` is ever dropped from Badge, the exclusion becomes a no-op and the gate fails). | **Adopt** |
| **F2** — Template wiring | `src/templates/active.ts` with CSS side-effect import + re-exports + `TEMPLATE_NAME` | **Correct.** The draft_q4.1 §7.4 implementation is clean: one file, three imports, one constant. `main.tsx` imports `active.ts` (never `theme.css` directly). The dev-mode mismatch warning in `App.tsx` is a good safety net. This replaces the unwritten "build system loads template" promise with written code. | **Adopt** |
| **F3** — `parseDocument` | Returns `{ frontmatter, body }`; strips BOM (`/^\uFEFF/`), normalizes CRLF; `body` feeds all downstream consumers | **Correct.** The draft_q4.1 §22.5 implementation is well-traced. The regex `^---\n([\s\S]*?)\n---\n?` matches the frontmatter block; `normalized.slice(match[0].length).replace(/^\n+/, "")` strips it and leading blank lines. The regression test ("frontmatter block does not leak into the rendered body") is the right fixture. | **Adopt** |
| **F4** — Heading text normalization | `headingText()` applied in hast text order: backticks → images to alt → links to link text → autolinks to URL | **Correct.** The draft_q4.1 §9.2 implementation applies reductions in the correct order (matching how hast contributes text content). The new parity fixtures (`## Heading with [link](https://x.y)` and `## Alt text ![img](i.png)`) are the right test cases. Residual edge cases (HTML entities, footnote refs) are disclosed. | **Adopt** |
| **F5** — Code-block badge guard | `typeof children === "string" && !children.includes("\n")` before `resolveBadge` | **Correct.** The draft_q4.1 §8.5 implementation adds the single-line check to the `components.code` entry. A fenced block with content `critical` has `children = "critical\n"` (or `"critical"` with a trailing newline in some react-markdown versions) — the `!children.includes("\n")` guard prevents misfire. The fixture (fenced block containing exactly `critical` renders as `<code>`, not Badge) is the right test. | **Adopt** |

### 2.5 Validation of the draft_q4.1.md

The draft is a 5-pass assembled document that implements the plan faithfully. Key observations:

**Strengths:**
- All 67 findings (20 R1 + 15 R2 + 15 R3 + 17 appendix/section findings) have dispositions in Appendix A
- The 5 load-bearing fixes (F1–F5) are each backed by regression fixtures
- The evidence contract is self-applied (21.1 and 21.13 retagged from Verified to Reasoned; 21.8 amended in place)
- The §23 Lessons Learnt section is restored from draft_q3 and extended with Round 3 lessons (hereditary error propagation, unwritten machinery, encoded exceptions, disclosed blind spots)
- The Final Consistency Gate (15 checks) is thorough and honest (including the stated length deviation)
- The `package.json` scripts block (§15.2) is the single source of truth — every script cited in CI/pre-ship is defined there

**Issues identified in the draft (to be addressed in the final v4.1.0):**
1. **Length deviation:** The draft acknowledges ~4,900–5,100 lines (well above the 3,200–3,600 target). The plan's quality gate #5 says "Length blowout" mitigation is "unchanged code blocks verbatim, tables compact." The final v4.1.0 should target 3,400–3,800 by condensing where possible without losing load-bearing content. The draft's own Final Consistency Gate honestly states this deviation.
2. **Pass narration:** The draft contains "Pass 1 of 5" / "Pass 2 of 5" narration between sections (lines 1, 571, 633, 3632). These are assembly artifacts and should be removed in the final deliverable.
3. **Trailing URL:** Line 4067 contains a `https://chat.qwen.ai/s/...` URL — an artifact of the drafting environment. Must be removed.
4. **`§16 row 19` duplication:** The draft's §16 has 26 rows. Row 19 is "Claiming AAA because '14px is bigger'" (from v4.0.0's row 13). The plan says "rows 1–18/20–22 numbers unchanged" but the draft appears to have renumbered. The final should verify row numbering consistency.

**Verdict:** The draft is a sound implementation of the plan. The 5 fixes are correct. The issues are editorial (length, narration artifacts, trailing URL), not substantive.

---

## III. Architectural Decisions (Locked for v4.1.0)

### Decision 1: Base = v4.0.0 + Round 3 fixes

v4.1.0 = v4.0.0 (3,667 lines) + 15 Round 3 fixes. No rewrite of load-bearing architecture. The three hereditary Critical bugs (C1–C3) remain dead. The five load-bearing fixes (F1–F5) are applied surgically.

### Decision 2: Version = v4.1.0

Minor version bump (not v5.0.0) because:
- No architectural rewrites (v4.0.0's two-layer tokens, fence scanner, collision detection, backtick-wrapping pipeline all stand)
- 15 fixes, 2 of which are High (gate coherence, template wiring) — significant but not architectural
- The hereditary Critical bugs are already dead in v4.0.0; v4.1.0 fixes self-inflicted defects

### Decision 3: Target length = 3,400–3,800 lines

v4.0.0 was 3,667 lines. v4.1.0 adds:
- +15 Round 3 findings (~120 lines)
- +5 fix code blocks (F1–F5, ~80 lines)
- +5 new test fixtures (~60 lines)
- +§23 Lessons Learnt (~50 lines)
- +6 new anti-pattern rows (~30 lines)
- +3 new debugging rows (~15 lines)
- +6 Appendix F spot-check steps (~30 lines)
- Net additions: ~385 lines

To stay within 3,800: condense the §14 test code (use compact one-liner assertions where possible), condense Appendix E (advanced patterns — already compact in v4.0.0), and remove the Pass narration artifacts from the draft.

### Decision 4: Preserve v4.0.0 structure exactly

All v4.0.0 section numbers (§1–§22, Appendices A–F) are preserved. v4.1.0 adds §23 (Lessons Learnt, restored from draft_q3) after §22. No renumbering — all cross-references from v4.0.0 remain valid.

### Decision 5: Evidence contract self-application

v4.0.0 tagged Findings 21.1 and 21.13 as "Verified" without execution. v4.1.0 retags both to "Reasoned" with an explicit §1.1 note. Finding 21.8's rationale is amended in place. The audit enforces the standard it polices.

### Decision 6: Encode exceptions, never suppress rules

The AAA gate (§14.9) uses `.exclude("[data-tag]")` — a context-level exclusion — rather than disabling the `color-contrast` rule. This is the critical distinction: an enumerated exception (named in §10.3, implemented as a scoped exclusion) vs. a rule suppression (which weakens the gate). The exclusion fails closed if `data-tag` is ever dropped from Badge.

---

## IV. Bug Fix Registry (15 Round 3 findings)

| ID | Severity | Finding | Fix in v4.1.0 |
|----|----------|---------|---------------|
| 22.1 | High | AAA axe gate contradicts §10.3 exceptions | §14.9: `.exclude("[data-tag]")` for contrast; `target-size` global (F1) |
| 22.2 | High | Template switching machinery overpromised | §7.4: `src/templates/active.ts` wiring file; frontmatter `template` advisory with dev-mode warning (F2) |
| 22.3 | Medium | Frontmatter never stripped → renders as `<hr><p>title:…</p>` | §22.5: `parseDocument()` returns `{ frontmatter, body }`; pipeline consumes `body` (F3) |
| 22.4 | Medium | Linked/image headings desync TOC↔rehype-slug | §9.2: `headingText()` normalization (backticks→images→links→autolinks); 2 new parity fixtures (F4) |
| 22.5 | Medium | Badge misfires on unclassed fenced code blocks | §8.5: `text.includes("\n")` guard before `resolveBadge`; fenced-`critical` fixture (F5) |
| 22.6 | Medium | Finding 21.8 overstates `process.env` breakage | §21.8: amended in place — Vite replaces `process.env.NODE_ENV`; genuine bug was `process.env.ERROR_REPORTING_ENDPOINT`; fix stands on idiom/portability |
| 22.7 | Low | §3.1 "requires LF" contradicts §22.5 CRLF code | §3.1: rewritten — CRLF handled, BOM stripped, limitation is flat `key: value` only |
| 22.8 | Low | §6.1 "equal specificity" comment false | §6.1: comment rewritten with correct cascade facts ((0,2,0) vs (0,1,0)) |
| 22.9 | Low | `aria-label` on generic span may not be exposed | §8.6: note added — visible text carries semantics; label is belt-and-suspenders |
| 22.10 | Low | CI `preview &` + `wait-on` redundant and undeclared | §15.1: both steps deleted; Playwright `webServer` is single server owner |
| 22.11 | Low | `**Tag**:` colon-outside-bold undocumented | §8.4: added to disclosed blind spots; fixture asserts pass-through |
| 22.12 | Low | Coverage 90→80 downgrade unexplained | §14.10: rationale added (jsdom limits on layout; core `lib/` 100% goal) |
| 22.13 | Informational | Hereditary error propagation | §23: Lessons Learnt lesson 10 ("audit against first principles, not prior drafts") |
| 22.14 | Informational | `lucide-react@1.28.0` phantom version | §4: Unverified tag + gate V-1 retained; provenance note added |
| 22.15 | Informational | Dual "v2.0.0" provenance ambiguity | Provenance log: cite filename + self-version together |

---

## V. Section-by-Section Delta (v4.0.0 → v4.1.0)

Unchanged sections are carried **verbatim** (no rewrite drift): §1 (except tenet 7 added), §2, §4 (except 22.14 note), §11, §13 (except §13.2 memoization excerpt updated for `parseDocument`), §19, §21 (except 21.8 amended, 21.1/21.13 retagged).

| Section | Change | Lines delta |
|---------|--------|-------------|
| Header/provenance | v4.1.0; merge log adds "Round 3 self-audit, 15 findings" | +5 |
| Part 1 §1.0 | Severity table reconciled (67 total); Round 3 block added; count reconciliation note | +25 |
| Part 1 §1.1 | Confidence note: Round 3 retag amendment (21.1, 21.13 → Reasoned; 21.8 amended) | +8 |
| Part 1 §21.1 | Confidence retagged: ~~Verified~~ → Reasoned (against documented Tailwind v4 semantics) | +2 |
| Part 1 §21.8 | Amended in place: Vite DOES replace `process.env.NODE_ENV`; genuine bug was `ERROR_REPORTING_ENDPOINT` | +6 |
| Part 1 §21.13 | Confidence retagged: ~~Verified~~ → Reasoned (against package-export knowledge) | +2 |
| Part 1 §22 (NEW) | Round 3 findings 22.1–22.15, full evidence-contract format | +120 |
| Part 1 §1.3 | Observations 8 and 9 added (hereditary errors, unwritten machinery) | +8 |
| Part 1 §1.4 | Reuse table: +Round 3 self-audit row; +v4.0.0 base row | +4 |
| §3.1 | Limitations rewritten: CRLF handled, BOM stripped, flat `key: value` only; `template` advisory | +3 |
| §5 skeleton | `templates/active.ts` added; pipeline diagram shows `parseDocument → body` | +8 |
| §6.1 | Specificity comment corrected (R3-8); cascade facts stated | +6 |
| §7.4 | Contract rewritten around `active.ts` (F2); mismatch warning; "why not frontmatter-driven" note | +20 |
| §8.4 | Blind-spot list: colon-outside-bold variant added (R3-11) | +4 |
| §8.5 | F5 guard: `text.includes("\n")` check before `resolveBadge` | +3 |
| §8.6 | D6 note: visible text carries semantics; `aria-label` is belt-and-suspenders | +2 |
| §9.2 | F4: `headingText()` normalization (backticks→images→links→autolinks) | +12 |
| §9.3 | +2 parity fixtures: linked heading, image heading | +15 |
| §10.3 | Exceptions table unchanged; canonical statement added | +2 |
| §10.4 | Gate text cites F1 exclusion mechanics | +4 |
| §13.2 | Memoization excerpt: `parseDocument().body` feeds `enhanceMarkdown`/`buildToc` | +3 |
| §14.3 | +1 fixture: colon-outside-bold pass-through | +5 |
| §14.4 | +2 fixtures: linked heading, image heading | +10 |
| §14.6 | Rewritten: `parseDocument()` API; strip regression; BOM; CRLF | +30 |
| §14.8 | +2 integration tests: fenced-`critical` stays code; frontmatter absent from render | +15 |
| §14.9 | F1: `.exclude("[data-tag]")` for contrast; separate `target-size` run; keyboard nav test restored | +25 |
| §14.10 | D5: coverage rationale added (jsdom limits; core `lib/` 100% goal) | +4 |
| §15.1 | `preview &` / `wait-on` steps deleted (R3-10) | -6 |
| §15.2 | `test:unit` and `test:integration` scripts added (single-source rule); pre-commit uses `test:unit` | +3 |
| §16 | +5 rows: frontmatter-as-content, link-heading desync, code-block badge, AAA-gate-vs-exceptions, frontmatter-auto-switch → 27 rows | +12 |
| §18 | +3 rows: frontmatter visible, badge on code block, anchor mismatch on linked heading → 23 rows | +6 |
| §20 | +v4.0.0 → v4.1.0 delta table | +10 |
| §22.5 | `parseDocument()` full code (F3) — replaces `extractFrontmatter` | +20 |
| §23 (NEW) | Lessons Learnt — restored from draft_q3; +Round 3 lessons (9–13) | +50 |
| App. A | +15 Round 3 ledger rows (67 total) | +18 |
| App. C | Fixture index updated with new counts | +3 |
| App. D | CI without `preview &`/`wait-on` | -3 |
| App. F | +6 spot-check steps (F1–F5 + template wiring) | +18 |
| Closing | Counts updated (67/67); self-check extended; "Reasoned throughout" | +8 |
| **Net** | | **+445** |

**Estimated v4.1.0 length:** 3,667 + 445 ≈ 4,112 lines. Target: condense to 3,400–3,800 by:
- Removing Pass narration artifacts from the draft (-15 lines)
- Condensing §14 test code (compact one-liner assertions where possible, -80 lines)
- Condensing Appendix E (already compact, -10 lines)
- Condensing Part 1 Round 1 findings table (already condensed in v4.0.0, maintain)
- Carrying §11, §12, §13, §19 verbatim from v4.0.0 (no expansion)

---

## VI. Quality Gates for the v4.1.0 Document Itself

Before the document is declared complete, verify:

1. **Every finding (67 across Rounds 1–3) has a disposition in Appendix A.** No orphan fixes.
2. **No `@theme` inside `@media` in v4.1.0 code.** (The three hereditary Critical bugs stay dead.)
3. **No "14px relaxes AAA" claim in v4.1.0 code.** (Appears only as rejected Finding 21.2.)
4. **No `dangerouslySetInnerHTML` in v4.1.0 code.** (Appears only as rejected Finding 21.3.)
5. **`parseDocument()` returns `{ frontmatter, body }`.** Every pipeline consumer takes `body`. §3.1 limitations match §22.5 code.
6. **`headingText()` applied before `slugger.slug()`** in `buildToc`. Link/image fixtures present in §9.3 and §14.4.
7. **`components.code` guard includes `text.includes("\n")`.** Fenced-`critical` fixture present in §14.8.
8. **§14.9 AAA test excludes `[data-tag]` for contrast only.** `target-size` global. §10.3 canonical. §10.4, §17 Gate 5 cite §14.9 mechanics.
9. **`templates/active.ts` written in full (§7.4).** No "build system loads template from frontmatter" promise remains. Frontmatter `template` advisory.
10. **Every script cited in §15.1, §15.3, §17 appears in §15.2.** No phantom scripts.
11. **CI contains no `preview &` / `wait-on`.** Playwright `webServer` is single server owner.
12. **Coverage 80/75 stated with rationale (§14.10).**
13. **Evidence contract self-applied: 21.1/21.13 retagged Reasoned; 21.8 amended; "Reasoned throughout."**
14. **No Pass narration artifacts.** No trailing URLs. No `TODO`/`FIXME`/`XXX`/`TBD`.
15. **Length: 3,400–3,800 lines.** (If exceeding 3,900, condense §14 test code and Appendix E.)
16. **§16 row numbering: rows 1–22 unchanged from v4.0.0.** New rows 23–27 for Round 3 anti-patterns.

---

## VII. Implementation Order (5 Phases)

### Phase 1: Base + Part 1 (Round 3 findings) — ~60 min

1. Copy v4.0.0 front matter; update version to 4.1.0; update provenance comment
2. Update §1.0 executive summary: reconciled severity table (67 total), Round 3 block, count reconciliation note
3. Update §1.1 methodology: Round 3 confidence amendment (21.1/21.13 retag, 21.8 amendment)
4. Carry §1.2 Round 1 findings verbatim from v4.0.0
5. Carry §21 Round 2 findings with retags (21.1, 21.13) and amendment (21.8)
6. Write §22 Round 3 findings (22.1–22.15) in full evidence-contract format
7. Update §1.3 observations (add 8 and 9)
8. Update §1.4 reuse table (add Round 3 + v4.0.0 rows)

### Phase 2: Part 2 §1–§9 (F2–F5 code fixes) — ~75 min

9. §1: add tenet 7 ("No unwritten machinery")
10. §3.1: rewrite limitations (CRLF handled, BOM stripped, flat key:value, template advisory)
11. §5: add `templates/active.ts` to skeleton; update pipeline diagram for `parseDocument → body`
12. §6.1: correct specificity comment
13. §7.4: rewrite contract around `active.ts` (F2); mismatch warning; "why not frontmatter-driven" note
14. §8.4: add colon-outside-bold to blind spots
15. §8.5: add F5 guard (`text.includes("\n")`)
16. §8.6: add D6 note on aria-label
17. §9.2: add `headingText()` normalization (F4)
18. §9.3: add 2 new parity fixtures (linked heading, image heading)

### Phase 3: Part 2 §10–§15 (F1 + tests + CI) — ~75 min

19. §10.3: add canonical statement
20. §10.4: cite F1 exclusion mechanics
21. §13.2: update memoization excerpt for `parseDocument().body`
22. §14.3: add colon-outside fixture
23. §14.4: add linked/image heading fixtures
24. §14.6: rewrite for `parseDocument()` API (F3); strip regression; BOM; CRLF
25. §14.8: add fenced-`critical` and frontmatter-absent integration tests
26. §14.9: rewrite with F1 (`.exclude("[data-tag]")`); restore keyboard nav test
27. §14.10: add coverage rationale (D5)
28. §15.1: delete `preview &` / `wait-on` steps
29. §15.2: add `test:unit` and `test:integration` scripts; update pre-commit

### Phase 4: Part 2 §16–§23 + Closing — ~60 min

30. §16: add 5 new anti-pattern rows (23–27)
31. §18: add 3 new debugging rows
32. §20: add v4.0.0 → v4.1.0 delta table
33. §22.5: replace `extractFrontmatter` with `parseDocument()` (F3)
34. §23 (NEW): Lessons Learnt — restored from draft_q3 + Round 3 lessons
35. Closing: update counts (67/67), self-check, confidence statement

### Phase 5: Appendices A–F + final consistency pass — ~45 min

36. Appendix A: add 15 Round 3 ledger rows (67 total)
37. Appendix C: update fixture index with new counts
38. Appendix D: remove `preview &` / `wait-on` from CI
39. Appendix F: add 6 spot-check steps (F1–F5 + template wiring)
40. Run quality gates (§VI, 16 checks)
41. Grep verification: no `@theme`-in-`@media`, no "14px relaxes", no `dangerouslySetInnerHTML`
42. Line count check (3,400–3,800)
43. Save to `/home/z/my-project/download/markdown-to-web_SKILL_v4.1.md`

**Estimated total:** ~5.5 hours of focused composition.

---

## VIII. Explicit Assumptions

1. The user wants a single markdown file (the corpus convention), not a multi-file project.
2. v4.1.0 replaces v4.0.0; no backward compatibility required beyond Appendix A (correction ledger) and §20 (migration guide).
3. The skill file itself does not need to be buildable or runnable — it is documentation. Code snippets are illustrative but should be syntactically valid TypeScript.
4. The draft_q4.1.md is a sound starting point — v4.1.0 will follow its structure and fixes closely, with editorial cleanup (remove Pass narration, trailing URL; condense to target length).
5. The evidence contract (§21) is preserved verbatim from v1.0.1 and applied to the audit itself (21.1/21.13 retagged, 21.8 amended).
6. English-only skill file (CJK heading support is tested in §14.5).
7. The `defineConfig` helper remains rejected (§3.2); the `MarkdownToWebConfig` type remains in §22.4 for teams that want it.
8. The `ErrorReporter` with external endpoint remains in Appendix E (optional); the `PerformanceMonitor` remains in Appendix E (optional, no gtag).
9. All four source documents (draft_q3, draft_z2, draft_d2, v2.1.0) plus v4.0.0 are treated as prior art. Provenance is documented in the header comment and Closing.

---

## IX. Confirmation Request

**Please confirm the following before I proceed to implementation:**

1. ✅ **Adopt v4.0.0 as base** + 15 Round 3 fixes (no architectural rewrite)?
2. ✅ **Fix all 15 Round 3 findings** per the Bug Fix Registry (2 High, 4 Medium, 6 Low, 3 Informational)?
3. ✅ **Apply the 5 load-bearing fixes (F1–F5)** with regression fixtures?
4. ✅ **Apply the 6 decisions (D1–D6)** as specified?
5. ✅ **Self-apply the evidence contract** (retag 21.1/21.13, amend 21.8)?
6. ✅ **Target 3,400–3,800 lines** (condense from draft_q4.1's ~5,000)?
7. ✅ **Preserve v4.0.0 section numbering** (add §23; no renumbering)?
8. ✅ **Save to `/home/z/my-project/download/markdown-to-web_SKILL_v4.1.md`**?
9. Any **specific additions, removals, or modifications** to the plan above?

Awaiting your go-ahead to begin Phase 1.
