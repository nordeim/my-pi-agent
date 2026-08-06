### §16 Anti-Patterns & Pitfalls

Twenty-two rows pairing an anti-pattern with its symptom, root cause, and fix. Merged from draft_q3's 15 rows and draft_z2's 7 unique rows. Each row is cross-referenced to the finding it addresses (where applicable).

| # | Anti-pattern | Symptom | Root cause | Fix |
|---|---|---|---|---|
| 1 | Badge renders as plain `<code>` | Gray monospace, no color | Value not wrapped by `enhance.ts` (unregistered tag/value, blockquote, or inside fence) | Check `enhance.ts` warnings; use exact bullet syntax; register the tag *(Finding 7.2)* |
| 2 | Heading missing from TOC | Section absent from nav | Level > `maxDepth`, or heading inside a code fence | Adjust depth; move heading out of fence *(Finding 7.3)* |
| 3 | TOC anchor mismatch | Jumps to wrong heading or top | Slug desync (versions drifted, setext heading, hand-edited id) | Run `slug-parity.test.ts`; pin both versions; ATX only *(Finding 2.2)* |
| 4 | Typecheck fails on unused imports | `tsc` errors | Strict `noUnusedLocals` | Delete the import — treat as an architectural signal *(Finding 21.13)* |
| 5 | Fonts render as fallbacks | System fonts | Network blocked; default build uses CDN fonts | Use `npm run build:offline` *(Finding 3.2)* |
| 6 | Code blocks not highlighted | Plain `<pre>` | `rehype-highlight` opt-in not wired | Add plugin + highlight.js CSS import *(§19.4)* |
| 7 | `import { slug } from "github-slugger"` | Build error | No named export exists; default class only | `import GithubSlugger from "github-slugger"` *(Finding 21.13)* |
| 8 | Error boundary everywhere | Error UI for minor issues | Over-broad boundaries | One root boundary; defensive checks in pure code *(Finding 21.15)* |
| 9 | Injecting raw HTML into markdown | Badges/markup silently vanish | react-markdown drops raw HTML without `rehype-raw` | Wrap values as code spans via `enhance.ts` — the supported path *(Finding 21.4)* |
| 10 | Rendering via `dangerouslySetInnerHTML` | XSS surface, dual pipelines | HTML-string architecture | Use the components map (§8.5); if you must serialize, `rehype-sanitize` is mandatory *(Finding 21.3 — Critical)* |
| 11 | Badge classes in runtime config strings | Unstyled badges, no error | Tailwind can't see classes it didn't scan | Keep classes in source files (§8.6); registry carries accent *numbers*, not class strings |
| 12 | `@theme` inside `@media` | Dark mode silently dead | `@theme` is build-time, top-level only | Variable-flip pattern (§6.1) — Layer 1 `:root` + Layer 2 `@theme inline` *(Finding 21.1 — Critical)* |
| 13 | Claiming AAA because "14px is bigger" | Conformance overclaim | Large text is ≥18pt / ≥14pt-bold; 14px ≠ large | §10.3 exceptions or §10.5 high-contrast recipe *(Finding 21.2 — Critical)* |
| 14 | Fence-blind line regexes | Fenced `## comment` in TOC; slug counters desync | Regex can't see fence state | Always go through `scanLines` (§9.1) *(Finding 21.5)* |
| 15 | Duplicate badge values across tags | Ambiguous render | Collision in registry | `loadRegistry` throws — rename one value *(Finding 21.6)* |
| 16 | Hardcoded tag keys in components | Badge doesn't render | `if (tag === 'critical')` hardcoded | Use `TagRegistry` lookup; tags are data *(Finding 7.1)* |
| 17 | Hand-write heading `id`s | TOC links break | Manual ids diverge from `rehype-slug` output | Let `rehype-slug` derive; TOC matches via shared slugger |
| 18 | Use setext headings | TOC desync | `Title\n=====` invisible to line extractor | ATX only (§9.4) |
| 19 | Nest `@theme` in `@media` (duplicate of #12) | Dark mode dead | Same as #12 | Same as #12 — kept for emphasis |
| 20 | Claim offline support for default build | Fonts fail from `file://` | Online build = CDN fonts | Online build = CDN, documented; offline = `build:offline` *(Finding 3.2)* |
| 21 | Skip gates to ship | Defects reach production | Time pressure | State the debt; never weaken a gate *(Finding 11.1)* |
| 22 | Copy version numbers between documents | Version drift | Memory/document copying | `npm ls --depth=0` is the only source of truth *(Finding 2.1)* |

### §17 Pre-Ship Checklist

**Mandatory verification gate, run in order.** No gate may be skipped, weakened, or made non-blocking to ship. A green gate achieved by disabling a check is not a pass — state the debt instead.

```bash
# Gate 1: Typecheck (strict, noUnusedLocals/Parameters)
npm run typecheck                    # tsc --noEmit

# Gate 2: Lint (ESLint + Prettier + markdownlint, zero-warning policy)
npm run lint && npm run lint:format && npm run lint:markdown

# Gate 3: Unit tests (enhance, toc, frontmatter, fence, tags, slug-parity + coverage)
npm run test -- --coverage           # MUST include slug-parity.test.ts

# Gate 4: Integration tests (MarkdownRenderer rendering)
npm run test:integration             # (folded into Gate 3 if vitest runs all tests)

# Gate 5: Accessibility (axe-core via Playwright, light + dark)
npm run a11y                         # AA: zero violations (gate-failure)
                                    # AAA: target-size + color-contrast are gate-failures; others are warnings
                                    # Runs in both light and dark modes

# Gate 6: Production build + bundle size
npm run build                        # online: dist/index.html with CDN fonts
npm run build:offline                # offline: dist/index.html with fonts inlined as base64
npm run test:bundle-size             # < 250 KB gzipped (§13.1)

# Gate 7: Smoke test the build
npm run preview
# Open http://localhost:4173/ and verify:
#   - Header renders with title (from frontmatter or first H1)
#   - Desktop sidebar + mobile drawer (resize < 1024px); drawer closes on Escape
#   - Badges colored; TOC links jump correctly; active section highlights
#   - Theme toggle cycles light/dark/system and persists across reload
#   - Tab through page; focus rings visible on all interactive elements
#   - DevTools → Lighthouse → Run; score ≥ 95 in all categories

# Gate 8: Verify dependency versions (gate V-1)
npm run versions:check               # npm ls --depth=0; compare against §4 table
                                     # lucide-react: confirm resolved version, correct §4 if it differs

# Verify artifact is self-contained:
#   Online build: open dist/index.html WITH network → fonts load, no console errors
#   Offline build: open dist/index.html WITHOUT network → fonts still render
```

**All eight gates must pass.** Suppressing a failure (loosening lint rules, skipping tests, weakening type checks, disabling a11y rules) to make a gate pass is forbidden.

### §18 Debugging Guide

Twenty rows mapping common symptoms to causes and fixes. Merged from draft_z2's 14 rows and draft_q3's 6 unique rows.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Build fails with `vite-plugin-singlefile` error | Version/config mismatch | Verify `viteSingleFile()` in plugins; gate V-1 |
| TOC anchor doesn't scroll | Missing `id` or `scroll-mt-24` | Check heading components; `rehypeSlug` present |
| TOC anchor wrong target | Slug desync | §16 row 3 |
| Badge wrong color | Registry accent mapping | Inspect `tags.ts`; check `enhance.ts` warnings |
| Startup error "badge value collision" | Two tags share a value | Rename one value; collision detection is intentional *(Finding 21.6)* |
| Dark mode doesn't apply | `data-theme` not set, or `@theme` nested in media | Inspect `<html data-theme>`; verify §6.1 structure (no `@theme` inside `@media`) *(Finding 21.1)* |
| Dark mode flickers on load | Theme applied after first paint | Set `data-theme` from a tiny inline script in `index.html` before the bundle |
| Theme toggle doesn't persist | Storage unavailable | Check `theme-storage.ts` try/catch path (§6.6); sandboxed contexts fall back to system *(Finding 21.11)* |
| Active section never highlights | Observer watching top level only | Use `flattenToc` (§9.5) |
| `lucide-react` install fails | Pinned version may not exist | Gate V-1; install current 0.x, update §4 table |
| Offline build huge | Full variable fonts inlined | Subset with `pyftsubset` |
| Offline fonts still missing | Recipe unverified in your environment | Appendix F step 6; file an issue against §11.3 |
| Tests fail only in CI | `npm ci` vs local drift | Reproduce with `rm -rf node_modules && npm ci` |
| `enhance.ts` warnings in build log | Unknown tag value in content | Fix the markdown or extend the registry |
| Build warning: Cannot find module @fontsource/... | Offline build deps not installed | `npm install @fontsource-variable/source-serif-4 @fontsource-variable/inter @fontsource/jetbrains-mono` |
| Test failure: `use(undefined)` throws in unified pipeline | Conditional plugin passed as `undefined` | Use conditional spread: `...(condition ? [plugin] : [])` |
| `extractFrontmatter` returns empty on Windows-authored file | CRLF line endings not handled | Verify `frontmatter.ts` regex uses `\r?\n` or normalizes `\r\n` to `\n` first |
| CI fails on bundle size | Bundle > 250 KB gzipped | Run `npm run build:analyze`; identify the largest chunks; consider lazy-loading `MarkdownRenderer` for very large documents *(Finding 21.9)* |
| `npm ls --depth=0` shows version drift | Dependency installed at wrong version | Run `npm install <pkg>@<exact-version>` to pin; never use `^` or `~` for skill-pinned deps *(Finding 2.1)* |
| Fenced headings appear in TOC | `scanLines()` not wired into `buildToc` | Verify `buildToc` imports and uses `scanLines` (§9.2) *(Finding 21.5)* |

#### 18.1 Debugging tools

```bash
# Enable debug logging
DEBUG="markdown:*" npm run dev

# Bundle analyzer (visualize what's in dist/index.html)
npm run build:analyze
# Opens a treemap visualization in the browser

# Run a single test file
npx vitest run tests/unit/slug-parity.test.ts

# Run axe against the dev server
npx @axe-core/cli http://localhost:5173/

# Inspect the built HTML
# The dist/index.html is a single file — open it in a text editor to inspect
# the inlined CSS and JS. Search for "data-tag" to find badge markup.
```

### §19 Extending the Skill

#### 19.1 Adding a new template

1. Create `src/templates/<name>/` with `theme.css`, `components.tsx`, `layout.tsx`, and `tags.json`.
2. `theme.css` must define all Layer-1 variables (`:root` + `@media` + `[data-theme]`) and Layer-2 `@theme inline` bridge per §6.1 — **never nest `@theme` inside `@media`** (§16 anti-pattern #12).
3. `components.tsx` exports a partial `ComponentsMap` that merges with the default map in `MarkdownRenderer.tsx`.
4. `layout.tsx` exports a React component receiving `TemplateLayoutProps` (§22.1).
5. Add the template name to the `TemplateName` union type in `src/types/template.ts`.
6. Add a default `tags.json` if the template introduces new tag semantics (or copy the editorial default).
7. Document the template in §7 of this skill file.
8. Add a fixture document and an axe test for the new template in `tests/`.

#### 19.2 Adding a new tag

1. Add the tag to `tags.json` (or a document-local `tags.json`).
2. Define allowed values and accent steps (1–5). Values MUST be lowercase (§8.3 validation).
3. Run `npm run test` — the `tags.test.ts` suite should pick up the new tag automatically. **Verify no collision** — if the same value exists in another tag, `loadRegistry` will throw (§16 anti-pattern #15).
4. If the tag should appear in the TOC or header metadata, extend `layout.tsx` to extract it from the frontmatter or markdown.

Example: adding a `Motion` tag for a legal document:

```json
{
  "Motion": {
    "name": "Motion",
    "values": {
      "granted":  { "accent": 4 },
      "denied":   { "accent": 1 },
      "pending":  { "accent": 3 }
    }
  }
}
```

Markdown usage:
```markdown
- **Motion:** granted
```

#### 19.3 Adding a markdown extension (footnotes, math, mermaid)

1. Install the remark/rehype plugin: `npm install remark-footnotes`.
2. Add to `MarkdownRenderer.tsx`'s `remarkPlugins` (or `rehypePlugins`) array.
3. Add a component override in the components map for any new HTML element the plugin emits (e.g., `<sup>` for footnotes, `<div class="math">` for KaTeX).
4. Add a fixture to `tests/integration/` verifying the extension renders.
5. Document the opt-in flag in §3 (Inputs Contract).
6. Re-run the slug-parity test — some remark plugins can interfere with `rehype-slug` if they transform headings.

**AST-based TOC (only if setext support becomes mandatory):** If a document type requires setext heading support (§9.4 limitation), migrate extraction to the AST via `unist-util-visit`. This is the one place AST parsing earns its complexity — it is documented here as the extension path, not implemented in the base skill.

#### 19.4 Adding syntax highlighting

1. `npm install rehype-highlight highlight.js`.
2. Add `rehypeHighlight` to `MarkdownRenderer.tsx`'s `rehypePlugins` (conditionally, based on the `syntaxHighlighting` config flag).
3. Import a highlight.js CSS theme in `index.css` (or define one in `@theme`):

```css
/* In index.css — minimal highlight.js theme using @theme tokens */
.hljs { background: var(--color-paper-100); color: var(--color-ink-900); }
.hljs-keyword { color: var(--color-accent-1); }
.hljs-string  { color: var(--color-accent-4); }
.hljs-comment { color: var(--color-ink-700); font-style: italic; }
.hljs-number  { color: var(--color-accent-3); }
/* ... etc. Define styles for every highlight.js token class you need. */
```

4. Add a "copy code" button component for `<pre>` blocks (optional but recommended for technical docs template).
5. Add ~30 KB to the bundle budget estimate (still within 250 KB).

#### 19.5 Adding search functionality (technical docs template)

For the technical docs template (§7.2), a client-side search can be added:

1. Build a search index at build time from the markdown content (headings + paragraphs).
2. Use a lightweight search library like `lunr` or `flexsearch`.
3. Add a search input in the header with cmd-K shortcut at `z-30` (§6.5).
4. Display results in a dropdown; clicking a result scrolls to the heading.
5. This is out of scope for the default skill but documented as an extension point (Appendix E.3).

#### 19.6 Adding a fourth framework adapter (NOT recommended)

The skill is React-only by design. Adding Vue or Svelte adapters was attempted in draft_q2 and rejected as over-engineering. The core value of the skill is the markdown pipeline + design system, both of which are framework-specific at the rendering layer. If a Vue or Svelte user needs this functionality, they should adapt the patterns (especially `enhance.ts`, `toc.ts`, `fence.ts`, `slug-parity.test.ts`, and the two-layer token system) to their framework — the patterns are transferable even if the code is not.

### §20 Migration Guide

#### 20.1 From `react-markdown-report` v1.0.1

| v1.0.1 | v4.0.0 | Action |
|--------|--------|--------|
| `comparative-analysis.md` | `src/content/document.md` | Rename; becomes the editorial fixture |
| `StatusBadge`, 9 hardcoded keys | `Badge` + tag registry | Move keys to editorial `tags.json` |
| `enhanceReportMarkdown` (two keys, `-` only, fence-blind) | `enhanceMarkdown` (any registered tag, all bullets, fence-aware, warnings) | Replace |
| `buildToc` H2/H3, fence-blind | `buildToc` H2–H4, fence-aware, slug reservation | Replace; `maxDepth: 3` for exact v1 parity |
| Severity tokens in `@theme` | accent-1..5 scale | Map old names via registry |
| Google Fonts only | + self-hosted + offline recipe | Optional (§11) |
| No reduced-motion / focus-visible / 44px targets | All three in base styles + gate | Apply §6.1, §10.2 |
| Badge text `text-xs` (12px, 4.76:1, fails AAA) | Stays `text-xs`; AAA handled by §10.3/§10.5 | No size change — the "14px relaxes AAA" rationale is false *(Finding 21.2)* |
| Pre-ship: `tsc && build` | Eight gates | §17 |
| No tests | vitest + Playwright/axe in-tree | §14 |
| `cn.ts` dead | Wired into `Badge`/templates | Done by construction *(Finding 5.1)* |
| No ErrorBoundary | ErrorBoundary at root + ErrorFallback | §12 *(Finding 21.15)* |
| No dark mode | Two-layer token pattern (Layer 1 `:root` + Layer 2 `@theme inline`) | §6.1 *(Finding 21.1)* — NOT `@theme`-in-`@media` |

#### 20.2 From the drafts

- **draft_k:** adopt structure wholesale; fix badge resolution (§8.3 — cross-category + collision detection); add gates (§17); make `enhance.ts` fence-aware; drop AAA headline.
- **draft_d:** keep honesty (AA baseline) and dark-mode mechanics (now §6.1, NOT draft_d2's `@theme`-in-`@media`); **delete** `defineConfig`/`virtual:config`, raw-HTML badge pattern, `dangerouslySetInnerHTML`, AST badge processor.
- **draft_q2:** keep as standards annex (test pyramid, CI skeleton, dependency criteria, ErrorBoundary contract); **do not copy** TOC extractor, `.use(undefined)` pipeline, async misuse, `PerformanceMonitor` with gtag, "Production-Ready" status. Downscope: one framework, one file.
- **draft_z:** keep audit discipline, tag registry, offline recipe, axe gate, evidence ledger; **apply three corrections** — dark mode per §6.1, badge contrast per §10.3/§10.5, parity test per §9.3; add `ErrorBoundary`.
- **draft_q3 (BASE):** adopt wholesale — two-layer token pattern, fence-aware scanner, collision detection, correct WCAG arithmetic, high-contrast recipe, honest lucide tag + gate V-1, dark-mode axe test, correction ledger, adopter spot-check. Merge full test code from draft_z2, full template CSS from draft_d2 (after @theme fix), Part 1 validation review from v2.1.0.

#### 20.3 6-week phased migration plan

For teams migrating from v1.0.1 in a structured rollout:

**Week 1 — Add Tests:** Install vitest + @testing-library/react + @axe-core/playwright. Add unit tests for `enhance.ts`, `toc.ts`, `fence.ts`, `tags.ts`. Add slug-parity test (§9.3 — the single most important verification). Add integration + a11y tests (both light and dark modes).

**Week 2 — Fix Accessibility:** Add `prefers-reduced-motion` support. Increase touch targets to 44px (`p-2.5` + icon, or `min-w-11 min-h-11`). Add global `:focus-visible` styles. Add skip-to-content link. **Do NOT change badge text to 14px** — the "14px relaxes AAA" claim is false (Finding 21.2). Instead, enumerate the AAA exception (§10.3) and optionally apply the high-contrast recipe (§10.5).

**Week 3 — Design Token Consistency:** Migrate to the two-layer token pattern (§6.1): Layer 1 `:root` runtime variables + Layer 2 `@theme inline` bridge. Move badge colors to accent scale. Update `Badge` component. Remove hardcoded colors. **Verify no `@theme` appears inside `@media`** (Finding 21.1).

**Week 4 — Generalize Badge System:** Replace `StatusBadge` with `Badge` + tag registry (§8). Add `tags.json` for editorial template. Update `enhance.ts` for any registered tag, all bullet styles, fence-aware. Add `validateRegistry()` with collision detection (§8.3).

**Week 5 — Offline Font Strategy:** Install `@fontsource` packages. Add conditional font imports in `main.tsx` (§11.3). Add `build:offline` script. Test offline build by opening `dist/index.html` with network disabled.

**Week 6 — CI/CD:** Set up GitHub Actions (§15.1). Add 8-gate quality gate script (§15.3). Add Lighthouse CI (§15.4). Add pre-commit hooks (§15.2). Add deployment automation to GitHub Pages.

#### 20.4 Quick-start migration procedure (10 steps)

For teams that want to migrate faster than 6 weeks:

1. **Backup:** `cp -r react-markdown-report react-markdown-report-v1.0.1-backup`
2. **Rename:** `git mv src/content/comparative-analysis.md src/content/document.md`
3. **Add v4.0.0 skeleton** from §5 (or `git init` new project, copy content file)
4. **Install dependencies** per §5.1 bootstrap commands
5. **Copy editorial template** from §6.1 and §7.1 — preserves v1.0.1 visual identity
6. **Copy tag registry** from §8.2 — 9 v1.0.1 keys map directly to accent steps 1–5
7. **Run slug-parity test** — the single most important verification: `npx vitest run tests/unit/slug-parity.test.ts`
8. **Run full pre-ship gate** (§17) — all 8 gates must pass
9. **Visually compare** v4.0.0 output to v1.0.1 — should be pixel-similar for editorial template
10. **Commit:** `feat: migrate from v1.0.1 to v4.0.0 (generalized, accessible, offline-capable, two-layer theming, fence-aware TOC, collision-detecting registry)`

### §21 Evidence Contract

Preserved verbatim from v1.0.1 §12. This is the skill's signature quality marker — every claim about the rendered output (or about the skill itself) must carry an evidence tag.

| Tag | Meaning | When to use | Example |
|-----|---------|-------------|---------|
| **Verified** | Executed and observed directly | After running `npm run a11y`, `npm run test`, or manual DevTools inspection | "The slug-parity test passes for all 16 fixtures" (after running `vitest`) |
| **Reasoned** | Logical inference from code, not executed | "Based on the `@theme` tokens, the contrast ratio is X:1" (without running a contrast checker) | "The 12px badge text fails AAA because accent-1 on red-50 is ≈5.9:1, below the 7:1 normal-text threshold" |
| **Assumed** | Based on a stated assumption | "Assuming the user opens the file in Chrome 120+" | "Assuming `@fontsource` packages resolve font files via Vite's asset pipeline as documented" |
| **Unverifiable** | Environment does not allow verification | "Mobile Safari behavior cannot be tested in this environment" | "iOS Safari rendering of `scroll-mt-24` cannot be verified without a device" |

**Rules:**

1. **Never upgrade a tag.** If a claim is Reasoned, do not present it as Verified. If it is Assumed, do not present it as Reasoned. The skill's credibility depends on this honesty.
2. **When in doubt, downgrade.** If you are not sure whether something was executed, tag it Reasoned.
3. **State what would be needed to verify.** "Reasoned — would need to run `npm run build:offline` and open the result from `file://` to verify fonts render."
4. **Apply the contract to the skill file itself.** The skill file makes claims about the system it describes. Those claims must be tagged. See the Closing for this skill file's own confidence statement.

**This contract is applied to v4.0.0 itself.** Every non-trivial claim in this document is implicitly tagged. Where a claim is verified (e.g., "v1.0.1's regex is `/^(\s*-\s*\*\*(?:Severity|Confidence):\*\*)\s+(.+)$/gm`" — Verified, quoted from the source), the source is named. Where a claim is reasoned (e.g., "the accent-1 through accent-5 pairs are ≈5.9–6.9:1 on their chip backgrounds" — Reasoned, based on the token hex values in §6.1 and WCAG relative-luminance formula), the reasoning is given. Where a claim is assumed or unverifiable (e.g., "@fontsource inline behavior in the offline build" — Assumed, requires runtime validation), the assumption is stated.

**Closing principle:** *If you cannot verify a claim, say so. A documented "Assumed" is more valuable than an undocumented "Verified."* This contract is the durable pattern preserved from v1.0.1 — every other module in v4.0.0 is in service of it.

### §22 TypeScript Reference

Complete TypeScript type definitions for the skill. These are the source of truth — if the code drifts from these definitions, the code is wrong, not the types.

#### 22.1 `src/types/template.ts`

```typescript
import type { ReactNode, FC, ComponentPropsWithoutRef } from "react";
import type { TagRegistry } from "./tag";
import type { TocItem } from "./toc";

export type TemplateName = "editorial" | "technical" | "minimal";

export interface TemplateLayoutProps {
  title: string;
  subtitle?: string;
  author?: string;
  date?: string;
  readingTime?: string;
  toc: TocItem[];
  activeSlug?: string;
  markdown: string;
  children: ReactNode;
}

export type ComponentsMap = {
  h1: FC<ComponentPropsWithoutRef<"h1">>;
  h2: FC<ComponentPropsWithoutRef<"h2">>;
  h3: FC<ComponentPropsWithoutRef<"h3">>;
  h4: FC<ComponentPropsWithoutRef<"h4">>;
  p: FC<ComponentPropsWithoutRef<"p">>;
  a: FC<ComponentPropsWithoutRef<"a">>;
  strong: FC<ComponentPropsWithoutRef<"strong">>;
  em: FC<ComponentPropsWithoutRef<"em">>;
  ul: FC<ComponentPropsWithoutRef<"ul">>;
  ol: FC<ComponentPropsWithoutRef<"ol">>;
  li: FC<ComponentPropsWithoutRef<"li">>;
  hr: FC<ComponentPropsWithoutRef<"hr">>;
  blockquote: FC<ComponentPropsWithoutRef<"blockquote">>;
  code: FC<ComponentPropsWithoutRef<"code">>;
  pre: FC<ComponentPropsWithoutRef<"pre">>;
  table: FC<ComponentPropsWithoutRef<"table">>;
  thead: FC<ComponentPropsWithoutRef<"thead">>;
  tbody: FC<ComponentPropsWithoutRef<"tbody">>;
  tr: FC<ComponentPropsWithoutRef<"tr">>;
  th: FC<ComponentPropsWithoutRef<"th">>;
  td: FC<ComponentPropsWithoutRef<"td">>;
};

export interface TemplateConfig {
  name: TemplateName;
  themeCss: string;                    // path to theme.css
  components: Partial<ComponentsMap>;   // overrides for default component map
  layout: FC<TemplateLayoutProps>;
  defaultTags: TagRegistry;             // loaded from tags.json
  tocMaxDepth: 2 | 3 | 4;
  offlineFonts: boolean;                // template-specific font strategy
}
```

#### 22.2 `src/types/tag.ts`

```typescript
export interface TagValueDefinition {
  /** Accent step 1–5, mapped to --color-accent-1 through --color-accent-5 in @theme. */
  accent: 1 | 2 | 3 | 4 | 5;
  /** Optional label override; defaults to the value, capitalized. */
  label?: string;
}

export interface TagDefinition {
  /** The tag name as it appears in markdown, e.g. "Severity", "Status". Case-sensitive. */
  name: string;
  /** The allowed values, each mapped to an accent step. Keys MUST be lowercase. */
  values: Record<string, TagValueDefinition>;
}

export type TagRegistry = Record<string, TagDefinition>;

/** Returned by resolveBadge() — the resolved badge to render. */
export interface ResolvedBadge {
  tag: string;                        // canonical tag name
  value: string;                      // normalized lowercase key
  label: string;                      // display label
  accent: 1 | 2 | 3 | 4 | 5;
}
```

#### 22.3 `src/types/toc.ts`

```typescript
export interface TocItem {
  level: 2 | 3 | 4;
  text: string;
  slug: string;
  children: TocItem[];
}
```

#### 22.4 `src/types/config.ts`

```typescript
import type { TagRegistry } from "./tag";
import type { TemplateName } from "./template";

export interface MarkdownToWebConfig {
  /** Path to the markdown file (relative to project root) */
  markdown: string;
  /** Template name; defaults to "editorial" */
  template?: TemplateName;
  /** Tag registry override; defaults to template's defaultTags */
  tags?: TagRegistry;
  /** TOC maximum depth; defaults to template's tocMaxDepth */
  tocMaxDepth?: 2 | 3 | 4;
  /** Inline fonts as base64 for offline use; defaults to template's offlineFonts */
  offlineFonts?: boolean;
  /** Enable rehype-highlight for code blocks; defaults to false */
  syntaxHighlighting?: boolean;
  /** Error reporting endpoint (optional); if unset, errors are logged but not sent */
  errorReportingEndpoint?: string;
}

// NOTE: v4.0.0 does NOT ship a `defineConfig` helper. The configuration surface is
// deliberately small (frontmatter + template + tags — §3.2). The `MarkdownToWebConfig`
// type is provided for teams that want to build their own config helper, but the base
// skill does not provide one. (draft_d's defineConfig was rejected — Finding 21.4 cousin.)
```

#### 22.5 `src/lib/frontmatter.ts`

```typescript
export interface Frontmatter {
  title?: string;
  subtitle?: string;
  author?: string;
  date?: string;
  template?: string;
  [key: string]: string | undefined;
}

/**
 * Extracts YAML frontmatter from the top of a markdown file.
 * Returns an empty object if no frontmatter is present or if parsing fails.
 * CRLF-safe: normalizes \r\n to \n before parsing.
 *
 * Known limitations (disclosed, by design): flat `key: value` only; no nested YAML,
 * arrays, or multiline values; requires LF line endings and no BOM at file start.
 */
export function extractFrontmatter(markdown: string): Frontmatter {
  // Normalize line endings
  const normalized = markdown.replace(/\r\n/g, "\n");
  const match = normalized.match(/^---\n([\s\S]*?)\n---\n/);
  if (!match) return {};

  const lines = match[1].split("\n");
  const out: Frontmatter = {};
  for (const line of lines) {
    const [key, ...rest] = line.split(":");
    if (key && rest.length > 0) {
      out[key.trim()] = rest.join(":").trim().replace(/^["']|["']$/g, "");
    }
  }
  return out;
}
```

#### 22.6 Additional named types

- `EnhanceResult` (§8.4): `{ enhanced: string; warnings: string[] }`
- `MarkdownRegion` (§9.1): `{ line: string; lineNumber: number; insideFence: boolean }`

#### 22.7 Component props summary

| Component | Props |
|-----------|-------|
| `App` | None (default export, reads markdown via `?raw` import) |
| `MarkdownRenderer` | `{ markdown: string; registry: TagRegistry }` |
| `TableOfContents` | `{ items: TocItem[]; activeSlug?: string; onNavigate?: () => void }` |
| `Badge` | `{ tag: string; value: string; accent: 1 \| 2 \| 3 \| 4 \| 5 }` |
| `ErrorBoundary` | `{ children: ReactNode; fallback?: ReactNode \| ((error, errorInfo) => ReactNode); onError?: (error, errorInfo) => void }` |
| `ErrorFallback` | `{ error?: Error \| null }` |
| `SkipLink` | `{ targetId?: string }` (default: `"content"`) |
| `ThemeToggle` | `{ theme: "light" \| "dark" \| "system"; onChange: (theme) => void }` |

---
