# Plan — `markdown-to-web` v4.1.0 (unified, corrected skill)

**Mode A (Generation), planning phase.** Base: `SKILL.md` v4.0.0 (technically soundest edition), carrying forward all 35 resolved findings and fixing the 15 issues my audit surfaced. Target: one self-contained skill file, `markdown-to-web_SKILL_v4.1.md`, estimated 3,200–3,600 lines. Nothing executed — all design claims tagged per the skill's own evidence contract.

---

## 1. Decisions (made, not offered)

| # | Decision | Choice | Rationale |
|---|---|---|---|
| D1 | AAA gate vs badge exceptions (R3-1) | Keep default accents; encode the enumerated exceptions **in the axe test** via `[data-tag]` node exclusion; `target-size` stays globally enforced; §10.5 recipe remains the opt-in path to true AAA | Preserves v1.0.1 editorial identity; the gate then enforces *exactly what §10.3 claims* — honest by construction. Making §10.5 the default would silently shift the palette |
| D2 | Template switching (R3-2) | One wiring file `src/templates/active.ts` (one-line edit to switch). Frontmatter `template` becomes **advisory metadata**, validated with a dev-mode warning on mismatch | Honors draft_q3's rejected-`virtual:`-module decision; replaces v4.0.0 §7.4's overpromise with a concrete, written mechanism |
| D3 | Frontmatter API (R3-3) | `parseDocument()` returns `{ frontmatter, body }`; pipeline consumes `body`; BOM stripped, CRLF normalized — the "LF-only" limitation is deleted, not just reworded | Fixes the render artifact and closes the §3.1/§22.5 contradiction in one move |
| D4 | Badge text size | Stays `text-xs` (12px); no revival of the 14px claim | Already correct in v4.0.0; reasserted explicitly in §8.6 |
| D5 | Coverage thresholds | Keep 80/75 project-wide, add explicit rationale (jsdom limits on layout/template components; core `lib/` held to 100% goal) | Resolves the silent 90→80 downgrade (R3-12) without pretending layout code is cheaply coverable |
| D6 | `aria-label` on badge span (R3-9) | Keep, with a one-line note: visible value + adjacent bold label carry the semantics; the label is belt-and-suspenders | Dropping it loses nothing measurable; adding a role pollutes the document outline |

## 2. Round 3 findings to be absorbed into Part 1 (15 new)

| ID | Severity | Finding | Fix lands in |
|---|---|---|---|
| R3-1 | High | AAA axe test hard-fails on its own documented badge exceptions | §10.4, §14.9 |
| R3-2 | High | "Build system loads template from frontmatter" — unwritten machinery | §7.4, §5 skeleton |
| R3-3 | Medium | Frontmatter block never stripped → renders as `<hr><p>title:…</p>` | §22.5, §5 pipeline, §14.6 |
| R3-4 | Medium | Headings with links/images desync TOC↔`rehype-slug` slugs | §9.2, §9.3 fixtures |
| R3-5 | Medium | Unfenced-class code block whose text matches a badge value renders as Badge | §8.5, §14.3 |
| R3-6 | Medium | Finding 21.8 overstates breakage (Vite *does* replace `process.env.NODE_ENV`) | Part 1 §21.8 reworded: fix = idiom/portability, not "unavailable" |
| R3-7 | Low | §3.1 "requires LF" contradicts §22.5's CRLF normalization | §3.1 |
| R3-8 | Low | §6.1 "equal specificity" comment false ((0,2,0) vs (0,1,0)) | §6.1 |
| R3-9 | Low | `aria-label` on generic span may not be exposed by AT | §8.6 note (D6) |
| R3-10 | Low | CI `preview &` + `npx wait-on` redundant (Playwright `webServer` suffices) and undeclared dep | §15.1 |
| R3-11 | Low | `**Tag**:` (colon outside bold) silently unmatched — undisclosed | §8.4 blind spots |
| R3-12 | Low | Coverage 90→80 downgrade unexplained | §14.10 (D5) |
| R3-13 | Informational | Hereditary error propagation: audits that diff drafts instead of first principles propagate bugs | New §23 Lessons |
| R3-14 | Informational | `lucide-react@1.28.0` almost certainly phantom (0.x line); gate V-1 stands | §4 note + provenance |
| R3-15 | Informational | Two editions self-versioned "2.0.0" — provenance ambiguity | Provenance log |

**Corpus totals in v4.1.0: 50 findings (20 R1 + 15 R2 + 15 R3), all with a fix or explicit disposition in Appendix A.**

## 3. Concrete specifications for the five load-bearing fixes

**F1 — AAA gate with encoded exceptions (§14.9):**
```ts
test("AAA advisory: contrast (excluding documented badge exceptions) + target size", async ({ page }) => {
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2aaa", "wcag21aaa", "wcag22aaa"]).analyze();
  // §10.3 exception: badge chips fail AAA contrast by documented design.
  const contrast = results.violations.find((v) => v.id === "color-contrast");
  const nonBadge = contrast?.nodes.filter(
    (n) => !n.target.flat().some((sel) => String(sel).includes("[data-tag]")),
  ) ?? [];
  expect(nonBadge).toEqual([]);                              // AAA contrast everywhere else
  expect(results.violations.find((v) => v.id === "target-size")?.nodes ?? []).toEqual([]); // global
});
```

**F2 — Template wiring (D2):**
```ts
// src/templates/active.ts — THE single place to edit when switching templates.
import "@/templates/editorial/theme.css";
export { EDITORIAL_TAGS as TAGS } from "@/templates/editorial/tags";
export { EditorialLayout as TemplateLayout } from "@/templates/editorial/layout";
export const TEMPLATE_NAME = "editorial" as const;
```
`main.tsx` imports `active.ts` (never `theme.css` directly); `App.tsx` dev-warns when `frontmatter.template !== TEMPLATE_NAME`. §7.4 contract rewritten around this.

**F3 — `parseDocument` (D3):** returns `{ frontmatter, body }`; strips BOM (`/^\uFEFF/`), normalizes CRLF; `body` feeds `buildToc` / `enhanceMarkdown` / `ReactMarkdown`. Regression test: "frontmatter block does not render as content."

**F4 — Heading text normalization in `toc.ts` (R3-4):** applied in the same order hast contributes text:
```ts
const headingText = (raw: string) => raw
  .replace(/`/g, "")
  .replace(/!\[([^\]]*)\]\([^)]*\)/g, "$1")  // image → alt text
  .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1")   // link → link text
  .replace(/<(https?:\/\/[^>]+)>/g, "$1")    // autolink → URL
  .trim();
```
New parity fixtures: `## Heading with [link](https://x.y)`, `## Alt text ![img](i.png)`.

**F5 — Code-block badge guard (R3-5):**
```tsx
code: ({ className, children }: ComponentPropsWithoutRef<"code">) => {
  const text = typeof children === "string" ? children : "";
  if (Boolean(className) || text.includes("\n")) return <code className={className}>{children}</code>;
  const badge = resolveBadge(registry, text);
  ...
```
Fixture: fenced block containing exactly `critical` renders as `<code>`, not Badge.

## 4. Section-by-section delta (vs v4.0.0)

Unchanged sections are carried **verbatim** (no rewrite drift): §1, §2, §4 (plus R3-14 note), §11, §13, §19, §21.

| Section | Change |
|---|---|
| Header/provenance | v4.1.0; merge log adds "Round 3 self-audit, 15 findings" |
| Part 1 §1.0/§1.2 | Severity table + Round 3 block (R3-1…R3-15); 21.8 reworded (R3-6) |
| §3.1 | Limitations rewritten: BOM/CRLF handled; flat-`key:value` only; `template` advisory (D2) |
| §5 skeleton | `templates/active.ts` added; pipeline diagram shows `parseDocument → body` |
| §6.1 | Specificity comment corrected (R3-8) |
| §7.4 | Contract rewritten around `active.ts` (F2); mismatch warning |
| §8.4 | Blind-spot list + `**Tag**:` colon-outside (R3-11) |
| §8.5/§8.6 | F5 guard; D6 note; badge-size rationale preserved |
| §9.2/§9.3 | F4 normalization + 2 new parity fixtures |
| §10.3/§10.4 | Exceptions table unchanged; gate text now cites the F1 exclusion mechanics |
| §14 | §14.3 +2 fixtures (colon-outside, fenced `critical`); §14.6 +strip regression +BOM/CRLF cases; §14.4 +link/image fixtures; §14.9 = F1; new keyboard-navigation smoke test (restored from draft_z2); §14.10 D5 rationale |
| §15.1 | `preview &` / `wait-on` steps deleted — Playwright `webServer` boots the preview (R3-10) |
| §16 | 5 new anti-pattern rows (frontmatter-as-content, link-in-heading desync, code-block badge, AAA-gate-vs-exceptions, frontmatter-auto-switch expectation) → 27 rows |
| §18 | +3 debugging rows (frontmatter visible; badge on code block; anchor mismatch on linked heading) |
| §20 | + v4.0.0 → v4.1.0 delta table |
| §22.5 | `parseDocument` full code (F3) |
| §23 (new) | Lessons Learnt — restores draft_q3's section; adds R3-13 hereditary-error lesson |
| App. A | +15 Round 3 ledger rows (50 total) |
| App. C | Fixture index with new counts |
| App. D | CI without preview/wait-on |
| App. F | +4 spot-check steps: grep frontmatter strip test, link-in-heading parity, fenced-`critical` fixture, axe gate on a badge-bearing fixture |
| Closing | Counts, self-check list extended (no R3 regressions), "Reasoned throughout" |

## 5. Execution strategy (incremental, per large-output discipline)

| Pass | Content | Review checkpoint |
|---|---|---|
| 1 | Frontmatter + Part 1 (R1 preserved verbatim, R2 corrected, R3 new) | Every R3 finding has severity/confidence/fix-reference |
| 2 | Part 2 §1–§9 (all F2–F5 code fixes) | Grep: no raw line regex outside `scanLines`; `parseDocument` used everywhere |
| 3 | Part 2 §10–§15 (F1 + tests + CI) | Axe test logic matches §10.3 exceptions exactly; no phantom scripts vs §15.2 table |
| 4 | Part 2 §16–§23 + Closing | Row counts consistent (27 anti-patterns, 23 debugging, 50-finding ledger) |
| 5 | Appendices A–F + final consistency pass | The §7 checklist below |

## 6. Pre-mortem (top failure modes of the merge itself)

1. **Regression by copy** — stale v4.0.0 snippet reused during merge (old axe test, old `toc.ts`). *Mitigation:* Appendix A ledger + final grep gate (§7).
2. **New self-contradiction** — exceptions table vs gate wording drift apart again. *Mitigation:* single canonical statement in §10.3; §14.9 cites it by section number.
3. **Rewrite drift in untouched sections.** *Mitigation:* verbatim carry-forward rule; only sections in §4's delta table are rewritten.
4. **Script-table desync** (phantom npm scripts in CI). *Mitigation:* every `npm run X` in §15.1/D cross-checked against the §15.2 scripts block — draft_q3's single-source rule.
5. **Length blowout.** *Mitigation:* unchanged code blocks verbatim, tables compact; target band 3,200–3,600 lines.

## 7. Final consistency gate (before delivery)

- `@theme` appears only top-level (never inside `@media`); no "14px relaxes AAA"; no `dangerouslySetInnerHTML` — the three hereditary bugs stay dead.
- All 50 findings → Appendix A row; no orphan fixes.
- Frontmatter limitations text == `parseDocument` code behavior.
- Axe test assertions == §10.3 exceptions, token-for-token.
- CI invokes only scripts defined in §15.2.
- Confidence statement: "Reasoned throughout"; no execution claims.

**Assumption stated:** deliverable is a single self-contained Markdown skill file (corpus convention), no runtime validation possible here — Appendix F remains the path for the user to convert Reasoned → Verified.
