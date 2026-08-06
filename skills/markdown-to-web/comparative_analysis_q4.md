# Audit — `markdown-to-web` skill corpus (5 versions)

**Mode C (Audit/Review).** Findings are ordered by severity, tagged per the corpus's own evidence contract. Nothing was executed in this environment; all runtime-behavior claims are **Reasoned**, textual contradictions are **Verified (textual)**.

---

## 1. Executive summary

| Severity | Count | Status |
|---|---|---|
| Critical | 3 | All fixed/rejected in `draft_q3` + `SKILL.md v4`; **open** in `draft_z2`, `v2.1.0`, `draft_d2` |
| High | 5 | 3 historical (fixed in v4); **2 open in v4.0.0 itself** |
| Medium | 7 | 3 historical; **4 open in v4.0.0** |
| Low | 6 | mostly open |
| Informational | 5 | — |

**Verdict ranking** (fitness as a build spec):

1. **`SKILL.md` v4.0.0** — most correct *and* most complete; the only edition that fixes all three critical hereditary bugs. Still carries ~5 uncaught defects (§4 below).
2. **`draft_q3` v3.0.0** — leanest *correct* core; the best 10-minute path to a working build. Gaps: templates B/C are contracts-only, no performance-budget section.
3. **`draft_z2` v2.0.0** — broadest feature spec (ErrorReporter, 3 font strategies, perf budgets), but carries two critical hereditary bugs. Use as a feature reference, not a base.
4. **`markdown-to-web_SKILL.md` v2.1.0** — the best *audit artifact* (Part 1 methodology is the corpus's crown jewel); unsafe as a build spec because it inherits the critical bugs it was supposed to supersede.
5. **`draft_d2` v2.0.0** — rejected as a base (security + architecture defects); useful only as a parts donor (technical/minimal template CSS, 6-week migration plan).

**Meta-observation:** the corpus demonstrates hereditary error propagation. The `@theme`-in-`@media` bug and the WCAG-14px arithmetic error survived **three** successive "audits" because each edition diffed against the previous draft instead of re-deriving from first principles (Tailwind v4 semantics, WCAG definitions). Only `draft_q3` broke the chain.

---

## 2. Corpus map

| Doc | Self-version | Base | Distinguishing contribution | Distinguishing defect |
|---|---|---|---|---|
| `draft_z2.md` | 2.0.0 | draft_z | Full test code, CI YAML, 250 KB budget, 3 font strategies, ErrorReporter | `@theme`-in-`@media`; WCAG 14px error; fence-blind regex |
| `draft_q3.md` | 3.0.0 | v1.0.1+k/d/q2/z | Two-layer tokens, `fence.ts`, slug reservation, collision detection, correct WCAG math, gate V-1 | Frontmatter LF-only; templates B/C contracts-only |
| `markdown-to-web_SKILL.md` | 2.1.0 | draft_z | Part 1 validation review (20 findings), cross-reference table, Appendix fixtures | Inherits both critical bugs; `gray-matter` listed but never wired |
| `draft_d2.md` | 2.0.0 | — | Full technical/minimal `theme.css`, scroll-spy TOC code, 6-week migration plan | `dangerouslySetInnerHTML`; disconnected AST processor; async misuse; false "Verified" |
| `SKILL.md` | 4.0.0 | draft_q3 | Unifies everything; fixes all 3 critical bugs; Round-2 findings (15) | New contradictions introduced by the fixes (§4) |

---

## 3. Confirmed defects by severity

### Critical

**C1 — `@theme` nested inside `@media (prefers-color-scheme: dark)`**
- **Location:** `draft_z2` §6.1; `v2.1.0` §6; `draft_d2` §5.1–5.4
- **Evidence:** `@media (prefers-color-scheme: dark) { @theme { --color-ink-950: … } }`
- **Impact:** `@theme` is a build-time, top-level Tailwind v4 directive; nesting it in a media query is undocumented and does not generate dark utilities → dark mode silently dead in all three editions.
- **Severity:** Critical · **Confidence:** Reasoned (Tailwind v4 semantics; not executed here — note `SKILL.md` tags this "Verified", which overclaims per its own contract, see I3)
- **Fix:** Two-layer pattern (`:root` runtime vars flipped by media/`[data-theme]` + `@theme inline` bridge). **Fixed in `draft_q3` §4.1 and `SKILL.md` §6.1.** Alternative equally-valid fix: plain `@theme` + override the *generated* `--color-*` variables under the dark selector.

**C2 — WCAG "14px relaxes the AAA threshold to 4.5:1"**
- **Location:** `draft_z2` §8.4/§10; `v2.1.0` §8; `draft_d2` §8.4
- **Evidence:** "Badge text is now `text-sm` (14 px)… At 14 px, the WCAG AAA threshold relaxes to 4.5:1."
- **Impact:** False. WCAG large text is ≥18pt (24px) or ≥14pt **bold** (≈18.66px). 14px normal text still requires 7:1 at AAA. Ships low-contrast badges labelled AAA-compliant.
- **Severity:** Critical · **Confidence:** Verified (against stable WCAG 2.x definitions)
- **Fix:** Enumerate the exception + high-contrast recipe. **Fixed in `draft_q3` §9.3/§9.5 and `SKILL.md` §10.3/§10.5** — but the fix introduced a new contradiction, see **N1**.

**C3 — `dangerouslySetInnerHTML` markdown rendering**
- **Location:** `draft_d2` §14.2 — `return <div dangerouslySetInnerHTML={{ __html: html }} />;`
- **Impact:** XSS surface; defeats react-markdown's component map; contradicts draft_d2's own §11 pipeline claims.
- **Severity:** Critical · **Confidence:** Verified (textual)
- **Fix:** Backtick-wrapping → `components.code` → `Badge`. **Rejected in `draft_q3`/`SKILL.md` (§16 anti-pattern #10).**

### High

**H1 — Fence-blind `buildToc`/`enhanceMarkdown`** (`draft_z2`, `v2.1.0`, `draft_d2`)
`## comment` inside a code fence enters the TOC and consumes a slug counter, desyncing with `rehype-slug`. **Fixed** via `fence.ts`/`scanLines` in `draft_q3` §8.1 / `SKILL.md` §9.1 (scanner logic hand-traces correctly against a CommonMark subset; 4-space indented code blocks remain unhandled — disclosed, acceptable).

**H2 — AST badge processor disconnected from the Badge component** (`draft_d2` §11.3)
`processBadges` writes `data-badge-*` to `listItem.hProperties`; nothing consumes them; `Badge` expects props. Badges never render. **Fixed** by rejecting the approach.

**H3 — Missing `await` on async `processMarkdown`** (`draft_d2` §14.2) — **not caught by any edition's audit**
§11.2 declares `export async function processMarkdown(...): Promise<ProcessingResult>`; §14.2 does `const result = processMarkdown(...); setHtml(result.html);`. `result` is a Promise → `result.html` is `undefined` → blank render, and the `try/catch` cannot catch the rejection. `draft_q3`'s ledger flags "async misuse" generically (Q4) but never this instance.
- **Severity:** High (crash-grade defect in the common path) · **Confidence:** Verified (textual)

**H4 — AAA axe gate contradicts the enumerated badge exceptions** — **OPEN in `draft_q3` §12.3 and `SKILL.md` §14.9/§17**
§10.3 documents badge text failing AAA contrast (≈4.8–6.9:1 < 7:1) as accepted exceptions, while §14.9 hard-fails the AAA run on `color-contrast`:
```ts
const enforced = results.violations.filter(v => ["color-contrast","target-size"].includes(v.id));
expect(enforced).toEqual([]);
```
As written, the gate fails by design on every page containing a badge — or the exceptions table is false. (In `draft_z2` the same test was *internally consistent* because the 14px arithmetic "explained away" the failures — a consistent test built on a false premise; `draft_q3` corrected the premise but not the test.)
- **Severity:** High (a core gate is unshippable as specified) · **Confidence:** Verified (textual contradiction)
- **Fix:** scope the AAA contrast assertion to exclude badge elements (axe `rules` options / `reviewOnFail` per selector, e.g. exclude `[data-tag]`), or adopt §10.5 high-contrast accents as default and delete the exceptions. Recommendation: keep exceptions as defaults, encode the exclusion in the test, offer §10.5 as the opt-in path to genuine AAA.

**H5 — Template-selection machinery unspecified** — **OPEN in `SKILL.md` §7.4, `v2.1.0` §7**
"The build system loads the template specified in frontmatter" implies build-time reading of a `?raw` markdown file's frontmatter — a Vite plugin/virtual module that no edition writes. Meanwhile `src/index.css` statically imports exactly one `theme.css`, and no edition shows how per-template CSS is switched. `draft_d2`'s runtime `loadTemplate()` registry is the only concrete mechanism, but it doesn't solve CSS bundling either.
- **Severity:** High (a non-negotiable design rule — "templates are swappable" — rests on unwritten machinery) · **Confidence:** Reasoned
- **Fix:** spec the mechanism honestly: (a) build-time env/config flag selecting a generated `src/templates/active.ts` + CSS import, or (b) bundle all three Layer-1 variable sets and scope them under `[data-template=…]`, switching at runtime.

### Medium

**M1 — Frontmatter is never stripped from the rendered markdown** — **OPEN in all five editions**
Every edition's `extractFrontmatter()` returns metadata only; none returns or derives the remaining body, and no pipeline step strips the `---…---` block before `enhance`/`buildToc`/`ReactMarkdown`. Result: the frontmatter renders as `<hr><p>title: …</p><hr>` at the top of every document.
- **Severity:** Medium (visible artifact on every build) · **Confidence:** Reasoned
- **Fix:** return `{ frontmatter, body }`; feed `body` downstream; add a regression test ("frontmatter block does not render as content").

**M2 — Slug parity fixtures omit headings containing links/images** — open in all editions
TOC regex captures `Heading [link](https://x)`; `github-slugger` yields `heading-linkurl`, while `rehype-slug` hashes hast text `Heading link` → `heading-link`. Links in headings are common in docs. Only backtick-stripping is handled.
- **Severity:** Medium · **Confidence:** Reasoned
- **Fix:** in `toc.ts`, strip link/image syntax before slugging (`text.replace(/\[([^\]]*)\]\([^)]*\)/g, "$1")`, matching hast text contribution); add fixtures; disclose remaining edge cases (HTML entities, footnote refs).

**M3 — Badge misdetection in unfenced-class code blocks** — open in `draft_q3`, `SKILL.md`, `draft_z2`
`components.code` treats "no `className`" as inline. A fenced block with no language (and no `rehype-highlight`) has no className; if its content is exactly `critical`, `resolveBadge` matches and renders a Badge instead of a code block.
- **Severity:** Medium · **Confidence:** Reasoned
- **Fix:** additionally require `typeof children === "string" && !children.includes("\n")` before badge resolution; add fixture.

**M4 — No registry collision detection** (`draft_z2`, `v2.1.0`, `draft_d2`)
Cross-category first-match-wins resolution renders ambiguously when two tags share a value. **Fixed** by `validateRegistry()` fail-fast in `draft_q3`/`SKILL.md` — the correct design, since the `code` element carries no parent context, so value-only resolution *requires* global uniqueness.

**M5 — `draft_d2` epistemic + budget defects**
Self-tags "Confidence: Verified" with zero execution (violates the corpus's founding contract); 150 KB gzipped budget is unachievable with React 19 + react-markdown + micromark/GFM stack (~160–225 KB realistic); `window.gtag` hardcoded in `PerformanceMonitor`. **Fixed/rejected in v4** (250 KB budget, no gtag, "Reasoned throughout").

**M6 — `draft_z2` IntersectionObserver misses grandchildren**
Observes `toc` items and `item.children` but not H4 grandchildren → H4 sections never highlight. **Fixed** by `flattenToc` in `draft_q3`/`SKILL.md` §9.5.

**M7 — `SKILL.md` Finding 21.8 rationale overstates breakage**
Claims `process.env.NODE_ENV` is unavailable in Vite browser builds; Vite does replace `process.env.NODE_ENV` at build time (documented compat behavior). The *recommendation* (`import.meta.env.DEV`) is right, and draft_d2's `process.env.ERROR_REPORTING_ENDPOINT` genuinely never resolves (Vite exposes only `import.meta.env.VITE_*`) — but the finding's "Verified it breaks" framing is inaccurate.
- **Severity:** Medium (audit credibility) · **Confidence:** Reasoned

### Low

- **L1** `SKILL.md` §3.1 claims frontmatter "requires LF line endings" while §22.5's code normalizes CRLF — internal contradiction (BOM limitation is real; LF-only is not).
- **L2** `SKILL.md` §6.1 comment "after `:root` so equal specificity resolves by order" is wrong: `:root:not([data-theme="light"])` is (0,2,0) vs `[data-theme="dark"]` (0,1,0). Behavior is still correct (both branches set identical values), but the rationale is false.
- **L3** `aria-label` on a plain `<span>` badge (all editions): ARIA 1.2 forbids accessible names on generic elements; AT may ignore it. The visible value + adjacent bold label already convey meaning — either drop the attribute or give the span a name-permitting role.
- **L4** `SKILL.md` §8.4 docs say "only first-level bullets are targeted" but the regex (`^\s*…`) matches indented bullets; the real blind spots are blockquotes and `**Tag**:` (colon outside the bold) — the latter is never disclosed anywhere.
- **L5** `wait-on` used via `npx` in CI but absent from devDependencies; also redundant — `playwright.config.ts`'s `webServer` already boots the preview server for the a11y gate.
- **L6** Two documents self-version "2.0.0" (`draft_z2`, `draft_d2`); `draft_d2`'s skeleton contains generation artifacts (`editor ial/`, `co mponents.tsx`, `useToc.t s`) — evidence of an unreviewed pass.

### Informational

- **I1** `draft_q3`'s "single source of truth for npm scripts — no section may cite a script not listed in §3.1" is the best CI-hygiene rule in the corpus; v4 preserves it.
- **I2** `v2.1.0`'s Part 1 format (Location/Evidence/Impact/Severity/Confidence/Fix + cross-reference table proving every finding has a fix) is the corpus's most reusable artifact.
- **I3** Three editions violated the evidence contract (`draft_d2` "Verified", earlier q-line drafts "Production-Ready"); `SKILL.md` tags C1 as "Verified" without execution — a mild self-violation of the same rule it enforces.
- **I4** `lucide-react@1.28.0` is almost certainly a phantom version (the package has shipped a 0.x line for years). Inherited from v1.0.1; only `draft_q3`/`SKILL.md` tag it **Unverified** + gate V-1. Every other edition pins it as fact.
- **I5** Coverage thresholds silently dropped 90% (`draft_q3`) → 80/75% (`SKILL.md`) with no rationale; minor, but the corpus's own discipline demands such changes be stated.

---

## 4. Completeness matrix (dimension × version)

✓ complete & correct · ◐ partial/disclosed-gap · ✗ absent or wrong

| Dimension | z2 | q3 | v2.1.0 | d2 | **v4** |
|---|---|---|---|---|---|
| Version discipline / gate V-1 | ✓ | ✓ (best) | ✓ | ◐ | ✓ |
| Theming correctness (dark mode) | ✗ | ✓ | ✗ | ✗ | ✓ |
| WCAG honesty & arithmetic | ✗ | ✓ | ✗ | ✗ | ✓ |
| Fence-awareness | ✗ | ✓ | ✗ | ✗ | ✓ |
| Slug parity (test + reservation) | ◐ | ✓ | ◐ | ◐ | ✓ (but M2) |
| Tag registry (data, warnings, collisions) | ◐ | ✓ | ◐ | ◐ | ✓ |
| Templates (3, with CSS) | ✓ | ◐ | ✓ | ✓ | ✓ |
| Template *switching mechanism* | ◐ | ◐ | ◐ | ◐ | ◐ (H5) |
| Frontmatter (parse **and strip**) | ◐ | ◐ | ◐ | ◐ | ◐ (M1) |
| Error handling | ✓✓ | ✓ | ◐ | ✗ | ✓ |
| Fonts/offline (3 strategies) | ✓ | ◐ | ✓ | ◐ | ✓ |
| Tests (in-tree, runnable) | ✓ | ✓ | ✓ | ◐ | ✓ (most complete) |
| A11y gate coherence | ◐ | ✗ (H4) | ◐ | ◐ | ✗ (H4) |
| Performance budgets | ✓ | ✗ (absent) | ◐ | ✗ (150 KB) | ✓ |
| CI/CD | ✓ | ✓ | ✓ | ✓ | ✓ |
| Audit provenance / ledger | ◐ | ✓ | ✓✓ | ✗ | ✓✓ |
| Evidence-contract self-application | ✓ | ✓ | ✓ | ✗ | ✓ (but I3) |
| Migration guidance | ✓ | ✓ | ✓ | ✓✓ | ✓✓ |

---

## 5. Effectiveness assessment

- **`SKILL.md` v4.0.0** — Correct on every load-bearing mechanism (theming, fences, slugs, badges, a11y math) and complete on paper. Its residual risk is *self-inflicted*: fixing C2 broke the AAA gate (H4), and the merge inherited the frontmatter-strip gap (M1). Ship-ready after the §6 fix list.
- **`draft_q3` v3.0.0** — Highest correctness-per-line; the spot-check appendix (F) makes it the fastest verifiable path. Missing: perf budgets, full B/C template CSS, H4's gate coherence.
- **`draft_z2` v2.0.0** — Best feature catalogue (ErrorReporter, visual/keyboard test sketches, self-hosted fonts, Lighthouse). As a spec it would produce broken dark mode and a suite asserting false contrast claims — mine it for sections, never build from it.
- **`v2.1.0`** — Read Part 1 as the canonical audit record; do not implement Part 2.
- **`draft_d2` v2.0.0** — Salvage only §5.3/§5.4 template CSS (after the `@theme` fix v4 already applied) and the 6-week migration plan.

---

## 6. Recommended fix list for v4.0.0 → v4.1.0

1. **H4:** reconcile the AAA axe test with §10.3 — exclude `[data-tag]` elements from the AAA `color-contrast` enforcement (or adopt §10.5 accents by default); state the choice in §10.3 and §14.9 together.
2. **M1:** `extractFrontmatter` returns `{ frontmatter, body }`; pipeline consumes `body`; add regression test.
3. **H5:** replace "the build system loads the template from frontmatter" with a concrete mechanism (build-time flag → generated `active.ts`, or runtime `[data-template]` scoping of Layer-1 variable sets).
4. **M2:** strip link/image markup in `toc.ts` before slugging; add `## Heading [link](url)` and `## ![alt](img)` fixtures to the parity test.
5. **M3:** guard badge resolution with the single-line string check; add the `critical`-code-block fixture.
6. **L1/L2/L4/L5:** align the frontmatter limitation text with the code, correct the specificity comment, disclose the `**Tag**:` (colon-outside) non-match, drop the redundant `preview &`/`wait-on` CI step (Playwright's `webServer` suffices).
7. **I3:** retag C1-class claims "Reasoned (against documented Tailwind v4 semantics)" — the audit should model its own contract.

---

## 7. Verification ledger

| Check | Method | Result |
|---|---|---|
| All quoted defects (C1–C3, H1–H3, M1–M7, L1–L6) | Full-text read of all five files | Verified (textual) |
| Tailwind v4 `@theme`-in-`@media` invalidity, WCAG large-text thresholds, slug behavior, Vite env semantics | Inference against stable external definitions | Reasoned — no toolchain executed here |
| Internal contradictions (H4, L1, L2) | Cross-section comparison within single files | Verified (textual) |
| Runtime behavior of every snippet | Not executable in this environment | Unverifiable — verify via `SKILL.md` Appendix F spot-check (10 min) |

**What would upgrade this audit:** running the Appendix F spot-check (scaffold → vitest suites → grep for `@theme` inside `@media` → offline build) against v4.0.0; the H4 gate conflict and M1 strip gap would then surface as executable failing tests rather than textual findings.
