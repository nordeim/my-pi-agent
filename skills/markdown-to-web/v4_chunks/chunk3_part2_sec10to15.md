### §10 Accessibility (WCAG 2.2 AA + AAA Aspirational)

The headline conformance claim is **WCAG 2.2 AA + AAA aspirational, with documented exceptions**. AA is the gate (zero violations); AAA is the target where feasible, with `target-size` and `color-contrast` as gate-failures and other AAA criteria as warnings. v1.0.1 claimed "WCAG AAA" while self-documenting multiple AAA failures — that contradiction is resolved here by claiming only what is verified.

#### 10.1 Posture (the honesty fix — fixes Findings 8.1 and 21.2)

**Claim: WCAG 2.2 AA, enforced by an automated axe gate. AAA where feasible; every exception is enumerated in §10.3.** This document never states "WCAG AAA" as a headline, and it explicitly rejects the arithmetic error that appeared in draft_z, draft_z2, draft_d2, and v2.1.0 ("14px relaxes the AAA threshold") — WCAG large text is ≥18pt (24px) or ≥14pt bold (≈18.66px); no font size used here qualifies, so normal-text thresholds apply everywhere (Verified — stable WCAG definitions).

#### 10.2 Implementation matrix

| Feature | Implementation | Verification |
|---------|----------------|--------------|
| Skip-to-content | `<a href="#content">` with `sr-only focus:not-sr-only focus:z-50` | Manual: Tab → Enter → focus lands on `#content` |
| Focus visible | Global `:focus-visible` ring (§6.1), all interactive elements | axe `focus-order-semantics`; manual Tab pass |
| Heading hierarchy | H1 → H2 → H3 → H4, no skipped levels | axe `heading-order` |
| Anchor offset | `scroll-mt-24` on H2–H4 | Manual TOC click |
| Reduced motion | `prefers-reduced-motion` guard in base styles | Manual OS setting check |
| Touch targets | All interactive elements ≥ 44×44px (`min-w-11 min-h-11` or `p-2.5` + icon) | axe check `target-size` (gate-failure) |
| ARIA | `aria-label` on nav/drawer/toggle; `aria-hidden` on decorative icons; `role="alert"` on error fallback | axe check `aria-valid-attr`, `button-name` |
| Landmarks | `header`, `main`, `aside`, `nav`, `article`, `footer` | axe check `region` |
| Color isn't sole indicator | Badges carry text + tint | Deuteranopia simulation |
| Keyboard | Full Tab/Shift+Tab/Escape operability; drawer closes on Escape | Manual |
| Language | `<html lang>` set from frontmatter or `en` default | axe check `html-has-lang` |
| Contrast (body) | ink-900 on paper-50 ≈ 16.4:1 (lineage-computed) — AAA ✓ | axe `color-contrast` |
| Live regions | Error announcements use `role="alert"`; loading uses `aria-live="polite"` | axe check `aria-live` |

#### 10.3 Enumerated AAA exceptions (AA guaranteed, AAA not claimed)

| Item | Contrast (computed, Reasoned) | AA (4.5:1) | AAA (7:1) | Disposition |
|------|-------------------------------|------------|----------|-------------|
| Badge text, accent-1 on red-50 | ≈5.9:1 | ✓ | ✗ | Exception; upgrade via §10.5 |
| Badge text, accent-2 on amber-50 | ≈4.8:1 | ✓ | ✗ | Exception; upgrade via §10.5 |
| Badge text, accent-3 on yellow-50 | ≈4.8:1 | ✓ | ✗ | Exception; upgrade via §10.5 |
| Badge text, accent-4 on lime-50 | ≈6.9:1 | ✓ | ✗ | Exception; upgrade via §10.5 |
| Badge text, accent-5 on blue-50 | ≈6.3:1 | ✓ | ✗ | Exception; upgrade via §10.5 |
| Meta labels, teal-700 on paper-50 | ≈6.6:1 | ✓ | ✗ | Exception; use ink-800 if AAA required |

Everything else targets AAA. Dark-mode pairs (e.g., teal-600-dark `#2ba8b3` on `#0b1615` ≈6.5:1) pass AA and are axe-checked in dark mode via `[data-theme="dark"]` before the run (§10.6).

#### 10.4 The gate

Pre-ship command `npm run a11y` runs `tests/accessibility/axe.test.ts` (§14.9): **AA violations fail the build; AAA violations are advisory except contrast and target-size.** No suppressions.

#### 10.5 High-contrast badge recipe (opt-in AAA badges)

Swap Layer-1 accent variables for these (computed ≈8.5–9.2:1 on the standard chips — Reasoned; re-verify with the axe gate after applying). This is the **correct** path to AAA badge contrast — not the false "14px relaxes AAA" claim:

```css
:root {
  --accent-1: #7f1d1d;   /* ≈9.1:1 on red-50 */
  --accent-2: #78350f;   /* ≈8.8:1 on amber-50 */
  --accent-3: #713f12;   /* ≈8.5:1 on yellow-50 */
  --accent-4: #365314;   /* ≈8.5:1 on lime-50 */
  --accent-5: #1e40af;   /* ≈8.1:1 on blue-50 */
}
```

#### 10.6 Dark-mode axe test

The axe gate runs in both light and dark modes (sets `[data-theme="dark"]` before the run) — ensures dark-mode token overrides maintain AA.

#### 10.7 Implementation code snippets

**`src/components/SkipLink.tsx`:**

```typescript
export function SkipLink({ targetId = "content" }: { targetId?: string }) {
  return (
    <a
      href={`#${targetId}`}
      className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-teal-600 focus:text-white focus:rounded focus:shadow-lg"
    >
      Skip to main content
    </a>
  );
}
```

**Touch target CSS pattern** (all buttons/links in headers, drawers, theme toggle):

```typescript
<button
  className="min-w-11 min-h-11 p-2.5 inline-flex items-center justify-center"
  aria-label="Toggle navigation menu"
>
  <MenuIcon className="w-5 h-5" aria-hidden="true" />
</button>
```

#### 10.8 Concrete AAA fixes over v1.0.1

| v1.0.1 gap | v4.0.0 fix |
|------------|------------|
| Touch targets 32–36 px (`p-1.5`) | Touch targets ≥ 44 px (`p-2.5` + icon, or `min-w-11 min-h-11`) |
| Badge text 12 px (4.76:1, fails AAA) — "fixed" via false 14px claim | Badge text stays 12px; AAA handled honestly via §10.3 exceptions or §10.5 high-contrast recipe |
| No `prefers-reduced-motion` | `@media (prefers-reduced-motion: reduce)` disables smooth scroll + animations |
| Browser default focus outline only | Global `:focus-visible` style with 2px teal outline |
| No axe in CI | `npm run a11y` runs `@axe-core/playwright` against the built dist, in both light and dark modes |

### §11 Build & Deploy Recipes

v1.0.1's central pain point was the "single-file portability" half-promise: `vite-plugin-singlefile` inlined JS and CSS but not the Google Fonts `@import`, so the artifact didn't actually work offline. v4.0.0 resolves this with three font strategies (CDN `@import`, self-hosted `@font-face`, `@fontsource` base64 inlining) and four deploy recipes.

#### 11.1 Recipe A — Default single-file build (CDN fonts)

```bash
npm run build
# Output: dist/index.html (JS/CSS inlined; fonts load from Google Fonts CDN)
# Size: ~250-400 KB
# Deploy: any static host (GitHub Pages, Netlify, Vercel, S3, nginx)
```

**`vite.config.ts`:**

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { viteSingleFile } from "vite-plugin-singlefile";
import { resolve } from "path";

export default defineConfig({
  plugins: [react(), tailwindcss(), viteSingleFile()],
  resolve: { alias: { "@": resolve(__dirname, "src") } },
  build: {
    target: "es2022",
    cssCodeSplit: false,
    rollupOptions: {
      output: { inlineDynamicImports: true },
    },
  },
});
```

The online build's Google Fonts `@import` is in `src/index.css` (§6.1). **Caveat:** `@import` must come *before* `@import "tailwindcss"` per CSS spec. The `@import` will fail from `file://` (CORS) — use Recipe C (offline) for `file://` viewing.

#### 11.2 Recipe B — Self-hosted `@font-face` (alternative online build)

Self-host the font files in `public/fonts/` and declare `@font-face` rules. This avoids the Google Fonts CDN dependency but still requires the font files to be served alongside the HTML. Replace the Google Fonts `@import` in `src/templates/editorial/theme.css` with:

```css
/* One @font-face per family/weight combo needed (Inter 400/600, Source Serif 4 400/600, JetBrains Mono 400) */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;  /* repeat for 600 */
  font-display: swap;
  src: url('/fonts/inter-v12-latin-400.woff2') format('woff2');
}
/* ... repeat the @font-face block for each family/weight: Source Serif 4 (400, 600), JetBrains Mono (400) ... */

@import "tailwindcss";
/* ... Layer 1 + Layer 2 per §6.1 ... */
```

**Preload hints in `index.html`** (add one `<link rel="preload">` per font file):

```html
<link rel="preload" href="/fonts/inter-v12-latin-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/source-serif-4-v3-latin-400.woff2" as="font" type="font/woff2" crossorigin>
```

**Caveat:** With `vite-plugin-singlefile`, the `@font-face` URLs reference `/fonts/...` which won't be inlined — the single-file artifact will still need the font files alongside it. For true single-file portability, use Recipe C.

#### 11.3 Recipe C — `@fontsource` base64 inlining (offline build)

```bash
npm run build:offline
# Runs: node scripts/build-offline.mjs
# Output: dist/index.html (JS/CSS/fonts all inlined as base64)
# Size: ~2-4 MB (depending on font subset)
# Deploy: any static host, USB stick, file://, air-gapped environment
```

**`scripts/build-offline.mjs`:**

```javascript
// scripts/build-offline.mjs
// Sketch — requires runtime validation with actual @fontsource packages.
// The @fontsource packages ship font files in node_modules.
// Vite's `assetsInlineLimit` setting (set very high) inlines them as base64.
import { build } from "vite";
import { viteSingleFile } from "vite-plugin-singlefile";

process.env.VITE_OFFLINE_FONTS = "true";

await build({
  plugins: [viteSingleFile()],
  define: { "import.meta.env.VITE_OFFLINE_FONTS": JSON.stringify("true") },
  build: {
    target: "es2022",
    cssCodeSplit: false,
    assetsInlineLimit: 100 * 1024 * 1024,  // 100 MB — inline everything
    rollupOptions: { output: { inlineDynamicImports: true } },
  },
});

console.log("Offline build complete: dist/index.html (fonts inlined as base64)");
```

**`src/main.tsx` (conditional font import):**

```typescript
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import { ErrorBoundary } from "./components/ErrorBoundary";
import "./index.css";

// Conditional font import — only loads @fontsource packages in offline mode.
// In online mode, fonts load via Google Fonts @import in index.css.
// Top-level await requires es2022 target (set in vite.config.ts).
if (import.meta.env.VITE_OFFLINE_FONTS === "true") {
  await import("@fontsource-variable/source-serif-4");
  await import("@fontsource-variable/inter");
  await import("@fontsource/jetbrains-mono");
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </StrictMode>,
);
```

**Known unknowns (Assumed — verify per Appendix F before relying on this):**
1. Confirm `@fontsource` packages resolve the font files via Vite's asset pipeline.
2. Confirm `assetsInlineLimit: 100MB` causes base64 inlining (not just URL copying).
3. Confirm the resulting `dist/index.html` renders fonts correctly when opened from `file://` with no network.
4. If the offline build exceeds 5 MB, subset fonts to only the glyphs used (e.g., `pyftsubset` from `fonttools`).

#### 11.4 Recipe D — GitHub Pages deployment

```bash
# 1. Set base in vite.config.ts
# base: "/<repo-name>/"

# 2. Build
npm run build

# 3. Deploy (using gh-pages or actions/upload-pages-artifact)
npx gh-pages -d dist
```

For GitHub Actions deployment, see Appendix D's CI workflow — it uses `actions/upload-pages-artifact` + `actions/deploy-pages` for native GitHub Pages deployment without third-party tokens.

#### 11.5 Recipe E — Local `file://` viewing

The default build works from `file://` because `vite-plugin-singlefile` removes all `<script type="module" src="...">` and `<link rel="stylesheet" href="...">` references — everything is inlined into one HTML file.

```bash
npm run build
open dist/index.html        # macOS
xdg-open dist/index.html    # Linux
start dist/index.html       # Windows
```

**Caveat:** The online build's Google Fonts `@import` will fail from `file://` (CORS restriction). For `file://` viewing, use Recipe C (offline build) which inlines fonts as base64.

#### 11.6 System font fallbacks

All three strategies use the same fallback chain in `@theme inline`:

```css
--font-serif: "Source Serif 4", ui-serif, Georgia, serif;
--font-sans: "Inter", ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
--font-mono: "JetBrains Mono", ui-monospace, "Cascadia Code", "Source Code Pro", Menlo, Consolas, monospace;
```

If a web font fails to load (network blocked, font file missing), the browser falls back to a similar system font. The design will degrade gracefully — not pixel-identical, but readable and functional.

#### 11.7 Offline verification test

```typescript
// tests/e2e/offline.test.ts
import { test, expect } from "@playwright/test";

test("offline build works without network", async ({ page, context }) => {
  // Build the offline variant first: npm run build:offline
  await page.goto("http://localhost:4173/");  // serve dist/ via `npm run preview`
  await page.waitForLoadState("networkidle");
  await context.setOffline(true);  // go offline
  await page.reload();
  // Verify fonts still render (not falling back to system fonts)
  const bodyFont = await page.locator("body").evaluate((el) => getComputedStyle(el).fontFamily);
  expect(bodyFont).toMatch(/Source Serif 4|Inter/);
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
});
```

#### 11.8 Images

Local images referenced from markdown are resolved by Vite relative to the importing module — for `?raw` markdown, place images in `src/assets/` and reference by root-absolute path, or accept that only remote URLs are zero-config. Base64-embedding images inflates the single file quickly; embed only small images, link large ones. Documented limitation, not a configured feature.

#### 11.9 Size comparison

| Build mode | Approximate size | Use case |
|------------|------------------|----------|
| Online (Recipe A) | 250–400 KB | Default — works anywhere with internet |
| Self-hosted (Recipe B) | 250–400 KB HTML + ~150 KB font files | Production without CDN dependency |
| Offline (Recipe C) | 2–4 MB | Air-gapped, USB, archival, `file://` without internet |

### §12 Error Handling & Resilience

Errors are inevitable. The skill handles them at three layers: (1) build-time warnings from the preprocessor, (2) React error boundaries catching render failures, and (3) a structured error reporter for production observability (optional, Appendix E). The architecture avoids `dangerouslySetInnerHTML` entirely *(fixes Finding 21.3)* — react-markdown's component map renders Markdown as React elements, so a malformed markdown file produces a React render error (caught by the boundary) rather than an XSS surface.

#### 12.1 Error boundary (fixes Finding 21.15)

```typescript
// src/components/ErrorBoundary.tsx
import React from "react";
import type { ErrorInfo, ReactNode } from "react";
import { ErrorFallback } from "./ErrorFallback";

interface BoundaryProps {
  children: ReactNode;
  fallback?: ReactNode | ((error: Error, errorInfo: ErrorInfo) => ReactNode);
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}
interface BoundaryState {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends React.Component<BoundaryProps, BoundaryState> {
  state: BoundaryState = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): BoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    this.props.onError?.(error, errorInfo);
    // Note: ErrorReporter is optional (Appendix E). Base skill logs to console in dev only.
    if (import.meta.env.DEV) {
      console.error("ErrorBoundary caught an error:", error, errorInfo);
    }
  }

  render(): ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) {
        if (typeof this.props.fallback === "function") {
          return this.props.fallback(this.state.error!, {} as ErrorInfo);
        }
        return this.props.fallback;
      }
      return <ErrorFallback error={this.state.error} />;
    }
    return this.props.children;
  }
}
```

**Note:** v4.0.0 uses `import.meta.env.DEV` (Vite idiom) — NOT `process.env.NODE_ENV` (Finding 21.8). Vite replaces `import.meta.env.DEV` at build time; `process.env.NODE_ENV` is not replaced unless `define` is explicitly configured.

Placement: `main.tsx` wraps `<App />` (see §11.3's `main.tsx` listing). Keep it at the root only; use defensive checks (not nested boundaries) in pure functions.

#### 12.2 Error fallback UI

```typescript
// src/components/ErrorFallback.tsx
export function ErrorFallback({ error }: { error: Error | null }) {
  return (
    <div
      role="alert"
      aria-live="assertive"
      className="mx-auto my-16 max-w-xl rounded-lg border border-paper-200 bg-paper-100 p-6"
    >
      <h2 className="font-serif text-xl font-semibold text-ink-900">
        This document couldn't be rendered
      </h2>
      <p className="mt-2 text-sm text-ink-700">
        The content failed to render. Try reloading; if the problem persists, the
        markdown source may be malformed.
      </p>
      {import.meta.env.DEV && error && (
        <pre className="mt-4 overflow-auto rounded bg-ink-950 p-3 text-xs text-paper-100 whitespace-pre-wrap">
          {error.message}
          {error.stack && `\n\n${error.stack}`}
        </pre>
      )}
      <button
        type="button"
        onClick={() => window.location.reload()}
        className="mt-4 min-h-11 min-w-11 rounded-md bg-teal-700 px-4 py-2 text-sm font-semibold text-white"
      >
        Reload page
      </button>
    </div>
  );
}
```

#### 12.3 Error reporter (optional — Appendix E)

The `ErrorReporter` class with external endpoint is moved to Appendix E as optional. The base skill ships with `ErrorBoundary` + `ErrorFallback` only. If a deployment needs error reporting (Sentry, Datadog, custom endpoint), extend `ErrorBoundary.componentDidCatch` with a `fetch` call to `import.meta.env.VITE_ERROR_REPORTING_ENDPOINT`. See Appendix E.4 for the full implementation.

#### 12.4 Malformed markdown handling

| Scenario | Behavior |
|----------|----------|
| Unclosed code fence | react-markdown renders remainder as code — no crash; fence scanner treats rest as fenced (matches CommonMark) |
| Broken table | Renders as plain text — no crash |
| Invalid frontmatter | Ignored; document renders with fallback title |
| Unknown badge value | Build-time warning; line renders unstyled — no crash |
| Colliding tag registry | Startup error naming both tags — fails fast, never renders ambiguously |
| Empty markdown | `buildToc` → `[]`; renderer shows empty article — no crash |
| Markdown with no headings | `buildToc` → `[]`; sidebar/drawer renders "No sections" message — no crash |

#### 12.5 What NOT to do (architectural)

**Do not use `dangerouslySetInnerHTML`** to render markdown output. This was a defect in draft_d2 (Finding 21.3). react-markdown's component map exists to render Markdown as React elements — serializing to HTML and using `dangerouslySetInnerHTML` discards the benefits (type safety, accessibility attributes, reconciliation) and creates an XSS surface even with sanitization. If raw HTML pass-through is genuinely needed, use `rehype-raw` paired with `rehype-sanitize` and document the security implications explicitly. The default skill does not enable this path.

#### 12.6 Nested error boundaries (anti-pattern)

**Do not nest error boundaries.** One root boundary is sufficient. Use defensive checks (e.g., `try/catch` around pure functions, optional chaining for nullable values) in pure code rather than wrapping every component in its own boundary. Over-broad boundaries mask errors and make debugging harder (§16 anti-pattern #8).

### §13 Performance Optimization & Budgets

Performance budgets are explicit and enforced in CI (§15). The budgets below are realistic, not aspirational — they account for React 19, react-markdown, the remark/rehype ecosystem, and the application code. v1.0.1 had no performance budgets; draft_d2 had a 150 KB gzipped budget that was unrealistically low and would have forced feature cuts (Finding 21.9). v4.0.0 sets the budget at 250 KB gzipped, which is achievable without sacrificing functionality.

#### 13.1 Performance budgets

| Metric | Budget | Measurement | Gate |
|--------|--------|-------------|------|
| Bundle size (gzipped) | < 250 KB | `rollup-plugin-visualizer` | CI failure |
| Bundle size (raw) | < 800 KB | `rollup-plugin-visualizer` | Warning |
| First Contentful Paint | < 1.5 s | Lighthouse CI | CI failure if > 2.5 s |
| Time to Interactive | < 3 s | Lighthouse CI | CI failure if > 4 s |
| Largest Contentful Paint | < 2.5 s | Lighthouse CI | CI failure if > 4 s |
| Cumulative Layout Shift | < 0.1 | Lighthouse CI | CI failure if > 0.25 |
| Markdown parsing (1000 lines) | < 100 ms | Custom benchmark | CI failure |
| Markdown parsing (5000 lines) | < 500 ms | Custom benchmark | CI failure |
| TOC extraction (100 headings) | < 50 ms | Custom benchmark | CI failure |

**Bundle composition (estimated, Reasoned — not Verified):**
- React 19 + react-dom: ~45 KB gzipped
- react-markdown + remark-parse + remark-gfm + remark-rehype + rehype-slug: ~80–120 KB gzipped
- lucide-react (tree-shaken to 6 icons): ~5 KB gzipped
- clsx + tailwind-merge: ~3 KB gzipped
- Application code (components, lib, templates): ~30–50 KB gzipped
- **Total estimated: ~160–225 KB gzipped** (within the 250 KB budget)

If `syntaxHighlighting: true` is enabled, add ~30 KB gzipped for `rehype-highlight` + highlight.js common languages. If `rehype-raw` + `rehype-sanitize` are enabled, add ~25 KB gzipped. Both still fit within the 250 KB budget.

#### 13.2 Optimization techniques

**Memoization (fixes Finding 5.2):**

```typescript
// src/components/MarkdownRenderer.tsx
import { useMemo } from "react";
import { enhanceMarkdown } from "@/lib/enhance";
import { buildToc } from "@/lib/toc";

export function MarkdownRenderer({ markdown, registry }: Props) {
  // Memoize the enhanced markdown (regex preprocessing + fence scan)
  const enhanced = useMemo(
    () => enhanceMarkdown(markdown, registry),
    [markdown, registry],
  );

  // Memoize the TOC
  const toc = useMemo(
    () => buildToc(enhanced.enhanced),
    [enhanced.enhanced],
  );

  // Memoize the components map (stable reference unless registry changes)
  const components = useMemo(
    () => buildComponentsMap(registry),
    [registry],
  );

  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypeSlug]}
      components={components}
    >
      {enhanced.enhanced}
    </ReactMarkdown>
  );
}
```

**Code splitting (only for very large documents):**

For documents > 50,000 words, consider lazy-loading the `MarkdownRenderer` component. For typical documents (1,000–10,000 words), the parsing time is < 100 ms and lazy loading adds unnecessary overhead.

```typescript
// Only for very large documents
const MarkdownRenderer = lazy(() => import("./components/MarkdownRenderer"));

<Suspense fallback={<LoadingSpinner />}>
  <MarkdownRenderer markdown={content} registry={registry} />
</Suspense>
```

**Virtual scrolling (only for extreme cases):**

For documents > 100,000 words, consider virtual scrolling with `@tanstack/react-virtual`. This is out of scope for the default skill but documented as an extension point (Appendix E.2).

#### 13.3 No `gtag` hardcoding (fixes Finding 21.10)

v4.0.0 does NOT hardcode `window.gtag` calls. The `PerformanceMonitor` class (Appendix E.5, optional) logs to console in dev and exposes a hook for production reporting. The deploying team wires their analytics provider of choice.

#### 13.4 Performance test examples

```typescript
// tests/performance/bundle-size.test.ts
import { describe, it, expect } from "vitest";
import { readFileSync, existsSync } from "fs";
import { join } from "path";
import { gzipSync } from "zlib";

describe("Bundle Size", () => {
  it("main bundle is under 250KB gzipped", () => {
    const distPath = join(process.cwd(), "dist", "index.html");
    if (!existsSync(distPath)) {
      throw new Error("dist/index.html not found. Run `npm run build` first.");
    }

    const content = readFileSync(distPath);
    const gzipped = gzipSync(content);

    expect(gzipped.length).toBeLessThan(250 * 1024);  // 250 KB
  });
});

// tests/performance/parsing-speed.test.ts
import { describe, it, expect } from "vitest";
import { buildToc } from "@/lib/toc";
import { enhanceMarkdown } from "@/lib/enhance";
import type { TagRegistry } from "@/types/tag";

function generateLargeMarkdown(lines: number): string {
  const sections: string[] = [];
  for (let i = 0; i < lines / 10; i++) {
    sections.push(`
## Section ${i}

This is paragraph ${i} with some content.

- **Severity:** critical
- **Confidence:** verified

### Subsection ${i}.1

More content here.
    `);
  }
  return sections.join("\n");
}

describe("Parsing Performance", () => {
  const registry: TagRegistry = {
    Severity: {
      name: "Severity",
      values: {
        critical: { accent: 1 },
        high: { accent: 2 },
        medium: { accent: 3 },
        low: { accent: 4 },
        informational: { accent: 5 },
      },
    },
  };

  it("parses 1000 lines in under 100ms", () => {
    const markdown = generateLargeMarkdown(1000);
    const start = performance.now();
    enhanceMarkdown(markdown, registry);
    buildToc(markdown);
    const duration = performance.now() - start;
    expect(duration).toBeLessThan(100);
  });

  it("parses 5000 lines in under 500ms", () => {
    const markdown = generateLargeMarkdown(5000);
    const start = performance.now();
    enhanceMarkdown(markdown, registry);
    buildToc(markdown);
    const duration = performance.now() - start;
    expect(duration).toBeLessThan(500);
  });
});
```

### §14 Testing Strategy

The test pyramid is: 70% unit tests, 20% integration tests, 10% visual/end-to-end tests. The single most important test is `slug-parity.test.ts` (§9.3) — it verifies that `github-slugger` (used by `buildToc`) and `rehype-slug` (used by react-markdown) produce identical slugs. If this test fails, every TOC link in every rendered document is broken. v1.0.1 had no tests at all; v4.0.0 ships the full pyramid.

#### 14.1 Test pyramid

```
           /\
          /  \         Visual Regression (10%)
         /----\        - Screenshot comparisons
        /      \       - Cross-browser rendering
       /--------\
      /   E2E    \     End-to-End (10%)
     /------------\    - Full user workflows
    /  Integration \   20% - Navigation, TOC, badges
   /----------------\
  /    Unit Tests    \  70% - Pure functions, components
 /--------------------\ - enhance, toc, frontmatter, fence, tags, slug-parity
/______________________\
```

#### 14.2 Unit tests — `fence.test.ts` (NEW — fixes Finding 21.5)

```typescript
// tests/unit/fence.test.ts
import { describe, it, expect } from "vitest";
import { scanLines } from "@/lib/fence";

const flags = (md: string) => scanLines(md).map((r) => r.insideFence);

describe("scanLines fence tracking", () => {
  it("marks fence delimiters and body as inside", () => {
    expect(flags("before\n```\ninside\n```\nafter")).toEqual([false, true, true, true, false]);
  });
  it("handles tilde fences and longer closing markers", () => {
    expect(flags("~~~\nx\n~~~~\nafter")).toEqual([true, true, true, false]);
  });
  it("unclosed fence extends to end of document", () => {
    expect(flags("```\nstill\nstill")).toEqual([true, true, true]);
  });
  it("does not close a backtick fence with tildes", () => {
    expect(flags("```\n~~~\nx\n```")).toEqual([true, true, true, true]);
  });
  it("requires closing fence at least as long", () => {
    expect(flags("````\nx\n```\ny\n````")).toEqual([true, true, true, true, true]);
  });
});
```

#### 14.3 Unit tests — `enhance.test.ts`

8 test cases covering bullet styles, multiple matches, CRLF, warnings, case sensitivity, fence-aware, and blockquote blind spot:

```typescript
// tests/unit/enhance.test.ts
import { describe, it, expect } from "vitest";
import { enhanceMarkdown } from "@/lib/enhance";
import type { TagRegistry } from "@/types/tag";

const REGISTRY: TagRegistry = {
  Severity: { name: "Severity", values: { critical: { accent: 1 }, low: { accent: 4 } } },
  Status:   { name: "Status",   values: { done: { accent: 4 } } },
};

describe("enhanceMarkdown", () => {
  it("wraps registered values in backticks", () => {
    expect(enhanceMarkdown("- **Severity:** critical", REGISTRY).enhanced).toBe("- **Severity:** `critical`");
  });
  it("accepts *, +, and ordered bullets", () => {
    for (const bullet of ["* ", "+ ", "1. ", "2) "]) {
      expect(enhanceMarkdown(`${bullet}**Severity:** low`, REGISTRY).enhanced).toContain("`low`");
    }
  });
  it("matches tags case-insensitively, outputs canonical case", () => {
    expect(enhanceMarkdown("- **severity:** critical", REGISTRY).enhanced).toBe("- **Severity:** `critical`");
  });
  it("leaves fenced badge lines untouched", () => {
    const md = "```\n- **Severity:** critical\n```";
    expect(enhanceMarkdown(md, REGISTRY).enhanced).toBe(md);
  });
  it("leaves blockquoted badges untouched (documented blind spot)", () => {
    const md = "> - **Severity:** critical";
    expect(enhanceMarkdown(md, REGISTRY).enhanced).toBe(md);
  });
  it("warns on unknown values and leaves the line unchanged", () => {
    const { enhanced, warnings } = enhanceMarkdown("- **Severity:** catastrophic", REGISTRY);
    expect(enhanced).toBe("- **Severity:** catastrophic");
    expect(warnings[0]).toContain("catastrophic");
  });
  it("leaves unregistered bold bullets unchanged without warning", () => {
    const md = "- **Note:** just text";
    expect(enhanceMarkdown(md, REGISTRY)).toEqual({ enhanced: md, warnings: [] });
  });
  it("transforms all matching lines in a document", () => {
    const md = "## F1\n- **Severity:** critical\n- **Status:** done\n## F2\n- **Severity:** low";
    const { enhanced } = enhanceMarkdown(md, REGISTRY);
    expect(enhanced).toContain("`critical`"); expect(enhanced).toContain("`done`"); expect(enhanced).toContain("`low`");
  });
});
```

#### 14.4 Unit tests — `toc.test.ts`

9 test cases covering nesting, level jumps (the q2 regression case), orphans, fenced headings, maxDepth with slug reservation, empty markdown, backtick stripping, repeated headings, CJK:

```typescript
// tests/unit/toc.test.ts
import { describe, it, expect } from "vitest";
import { buildToc } from "@/lib/toc";

describe("buildToc", () => {
  it("nests H3 under H2 and H4 under H3", () => {
    expect(buildToc("## A\n### B\n#### C\n", 4)[0].children[0].children[0].slug).toBe("c");
  });
  it("re-nests an H2 after deeper levels (the q2 regression case)", () => {
    const toc = buildToc("## A\n### B\n## C\n", 4);
    expect(toc.map((t) => t.slug)).toEqual(["a", "c"]); expect(toc[1].children).toEqual([]);
  });
  it("promotes orphan headings to top level", () => {
    expect(buildToc("### Orphan\n## Real\n", 4).map((t) => t.slug)).toEqual(["orphan", "real"]);
  });
  it("ignores fenced headings", () => {
    expect(buildToc("```\n## Hidden\n```\n## Visible\n", 4).map((t) => t.slug)).toEqual(["visible"]);
  });
  it("respects maxDepth but still reserves slugs", () => {
    expect(buildToc("## A\n#### Deep\n## A\n", 3).map((t) => t.slug)).toEqual(["a", "a-1"]);
  });
  it("returns [] for empty markdown", () => { expect(buildToc("", 4)).toEqual([]); });
  it("strips backticks from heading text", () => {
    const toc = buildToc("## `Code` in Heading");
    expect(toc[0].text).toBe("Code in Heading"); expect(toc[0].slug).toBe("code-in-heading");
  });
  it("handles repeated headings (github-slugger dedup)", () => {
    const toc = buildToc("## Section\n## Section");
    expect(toc[0].slug).toBe("section"); expect(toc[1].slug).toBe("section-1");
  });
  it("handles CJK headings", () => {
    const toc = buildToc("## 中文标题");
    expect(toc[0].text).toBe("中文标题"); expect(toc[0].slug).toBeTruthy();
  });
});
```

#### 14.5 Unit tests — `slug-parity.test.ts`

See §9.3 for the full file. The test verifies:
- 7 fixture headings (simple, emoji, CJK, CamelCase, snake_case, kebab-case, leading whitespace)
- Headings with inline code (TOC strips backticks)
- Cross-level dedup counters (`# Dup` → `## Dup` → `## Dup`)
- Fenced headings consume no slugs

#### 14.6 Unit tests — `frontmatter.test.ts`

6 test cases covering extraction, absent, malformed, values with colons, quote stripping, template extraction:

```typescript
// tests/unit/frontmatter.test.ts
import { describe, it, expect } from "vitest";
import { extractFrontmatter } from "@/lib/frontmatter";

describe("extractFrontmatter", () => {
  it("extracts title, subtitle, author, date", () => {
    const fm = extractFrontmatter(`---
title: "My Document"
subtitle: "A subtitle"
author: "Jane Doe"
date: "2026-08-06"
---

# Body`);
    expect(fm).toMatchObject({ title: "My Document", subtitle: "A subtitle", author: "Jane Doe", date: "2026-08-06" });
  });
  it("returns empty object when no frontmatter", () => {
    expect(extractFrontmatter("# Just a document")).toEqual({});
  });
  it("returns empty object on malformed frontmatter", () => {
    expect(extractFrontmatter(`---
this is not valid yaml
---

# Body`)).toEqual({});
  });
  it("handles values with colons", () => {
    expect(extractFrontmatter(`---
title: "Title: with colon"
---

# Body`).title).toBe("Title: with colon");
  });
  it("strips surrounding quotes", () => {
    const fm = extractFrontmatter(`---
title: "Quoted"
author: 'Single'
---

# Body`);
    expect(fm.title).toBe("Quoted"); expect(fm.author).toBe("Single");
  });
  it("extracts template", () => {
    expect(extractFrontmatter(`---
template: "technical"
---

# Body`).template).toBe("technical");
  });
});
```

#### 14.7 Unit tests — `tags.test.ts` (NEW — fixes Finding 21.6)

6 test cases covering clean registry, collision detection, uppercase rejection, out-of-range accent, resolver, label capitalization:

```typescript
// tests/unit/tags.test.ts
import { describe, it, expect } from "vitest";
import { loadRegistry, resolveBadge, validateRegistry } from "@/lib/tags";
import type { TagRegistry } from "@/types/tag";

const OK: TagRegistry = {
  Severity: { name: "Severity", values: { critical: { accent: 1 } } },
  Confidence: { name: "Confidence", values: { verified: { accent: 1 } } },
};

describe("registry validation", () => {
  it("accepts a clean registry", () => {
    expect(validateRegistry(OK)).toEqual([]); expect(() => loadRegistry(OK)).not.toThrow();
  });
  it("detects cross-category value collisions", () => {
    const bad: TagRegistry = {
      Status: { name: "Status", values: { draft: { accent: 3 } } },
      Priority: { name: "Priority", values: { draft: { accent: 2 } } },
    };
    const errors = validateRegistry(bad);
    expect(errors.some((e) => e.includes("collision") && e.includes("Status") && e.includes("Priority"))).toBe(true);
    expect(() => loadRegistry(bad)).toThrow(/collision/);
  });
  it("rejects uppercase-registered values and out-of-range accents", () => {
    const bad: TagRegistry = { S: { name: "S", values: { Critical: { accent: 1 }, ok: { accent: 9 as 1 } } } };
    expect(validateRegistry(bad)).toHaveLength(2);
  });
});

describe("resolveBadge", () => {
  it("resolves across categories from value alone", () => {
    expect(resolveBadge(OK, "verified")?.tag).toBe("Confidence");
    expect(resolveBadge(OK, "  CRITICAL  ")?.tag).toBe("Severity");
  });
  it("returns null for unknown or empty values", () => {
    expect(resolveBadge(OK, "nope")).toBeNull(); expect(resolveBadge(OK, "   ")).toBeNull();
  });
  it("capitalizes default labels", () => {
    expect(resolveBadge(OK, "critical")?.label).toBe("Critical");
  });
});
```

#### 14.8 Integration tests

```typescript
// tests/integration/markdown-rendering.test.tsx
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { MarkdownRenderer } from "@/components/MarkdownRenderer";
import type { TagRegistry } from "@/types/tag";

const registry: TagRegistry = {
  Severity: {
    name: "Severity",
    values: {
      critical: { accent: 1 },
      high: { accent: 2 },
      verified: { accent: 1 },
    },
  },
  Confidence: {
    name: "Confidence",
    values: { verified: { accent: 1 } },
  },
};

describe("MarkdownRenderer integration", () => {
  it("renders markdown with badges", () => {
    const md = `
## Security Finding

This is a critical issue.

- **Severity:** critical
- **Confidence:** verified
    `;

    render(<MarkdownRenderer markdown={md} registry={registry} />);

    // Heading rendered
    expect(screen.getByRole("heading", { level: 2, name: "Security Finding" }))
      .toBeInTheDocument();

    // Badges rendered with correct aria-labels
    expect(screen.getByLabelText("Severity: Critical")).toBeInTheDocument();
    expect(screen.getByLabelText("Confidence: Verified")).toBeInTheDocument();
  });

  it("renders external links with target=_blank", () => {
    const md = "[Example](https://example.com)";
    render(<MarkdownRenderer markdown={md} registry={registry} />);
    const link = screen.getByRole("link", { name: "Example" });
    expect(link).toHaveAttribute("target", "_blank");
    expect(link).toHaveAttribute("rel", "noopener noreferrer");
  });

  it("renders tables with GFM", () => {
    const md = `
| Col1 | Col2 |
|------|------|
| A    | B    |
    `;
    render(<MarkdownRenderer markdown={md} registry={registry} />);
    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.getByRole("columnheader", { name: "Col1" })).toBeInTheDocument();
  });

  it("handles malformed markdown without crashing", () => {
    const md = "## Valid\n\n```\nUnclosed code block";
    render(<MarkdownRenderer markdown={md} registry={registry} />);
    expect(screen.getByRole("heading", { level: 2, name: "Valid" }))
      .toBeInTheDocument();
  });
});
```

#### 14.9 Accessibility tests (fixes Finding 8.3)

```typescript
// tests/accessibility/axe.test.ts
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("document passes WCAG 2.2 AA (hard gate)", async ({ page }) => {
  await page.goto("/");
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag22aa"])
    .analyze();
  expect(results.violations).toEqual([]);
});

test("AAA advisory: contrast and target size must still pass", async ({ page }) => {
  await page.goto("/");
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2aaa", "wcag21aaa", "wcag22aaa"])
    .analyze();
  const enforced = results.violations.filter((v) =>
    ["color-contrast", "target-size"].includes(v.id),
  );
  expect(enforced).toEqual([]);
});

test("dark mode passes AA", async ({ page }) => {
  await page.goto("/");
  await page.evaluate(() => document.documentElement.setAttribute("data-theme", "dark"));
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag22aa"])
    .analyze();
  expect(results.violations).toEqual([]);
});
```

#### 14.10 Test configuration

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import { resolve } from "node:path";

export default defineConfig({
  plugins: [react()],
  resolve: { alias: { "@": resolve(__dirname, "src") } },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./tests/setup.ts"],
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: ["node_modules/", "tests/", "**/*.d.ts", "**/*.config.*", "scripts/"],
      thresholds: { lines: 80, functions: 80, branches: 75, statements: 80 },
    },
  },
});

// tests/setup.ts
import "@testing-library/jest-dom";

// playwright.config.ts
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/accessibility",
  webServer: { command: "npm run preview", port: 4173, reuseExistingServer: false },
});
```

**Coverage statement:** 80% lines/functions, 75% branches project-wide. Core `lib/` modules (fence, toc, enhance, tags) carry a **goal** of 100% — stated as an aspiration enforced by review, not mislabeled as a verified fact.

### §15 CI/CD & Quality Gates

The CI pipeline runs all quality gates on every push and pull request. The pipeline is matrix-tested across Node 20 and Node 22 (the two LTS versions supported by Vite 7). Deployment to GitHub Pages is automated on merge to `main`.

#### 15.1 GitHub Actions workflow

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push: { branches: [main] }
  pull_request: { branches: [main] }
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
jobs:
  quality:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        node-version: [20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "${{ matrix.node-version }}", cache: npm }
      - run: npm ci
      - run: npm run versions:check        # Gate 8 / V-1
      - run: npm run lint                  # Gate 2 (eslint + prettier + markdownlint)
      - run: npm run lint:format
      - run: npm run lint:markdown
      - run: npm run typecheck             # Gate 1
      - run: npm run test -- --coverage    # Gate 3 (unit + integration + slug-parity)
      - if: matrix.node-version == 22
        uses: codecov/codecov-action@v4
        with: { files: ./coverage/coverage-final.json, fail_ci_if_error: false }
      - run: npm run build                 # Gate 6 (online)
      - run: npm run build:offline         # Gate 6 (offline)
      - run: npm run test:bundle-size      # Gate 6 (250 KB gzipped)
      - run: npx playwright install --with-deps chromium
      - run: npm run preview &             # Gate 5 (a11y — needs preview server)
      - run: npx wait-on http://localhost:4173
      - run: npm run a11y
      - run: npm audit --audit-level=critical
      - if: always()
        uses: actions/upload-artifact@v4
        with: { name: dist-node-${{ matrix.node-version }}, path: dist/, retention-days: 7 }
  deploy:
    needs: quality
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: |
          npm ci
          npm run build
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with: { path: dist }
      - id: deployment
        uses: actions/deploy-pages@v4
```

#### 15.2 Pre-commit hooks

```json
// package.json (scripts + lint-staged excerpt)
{
  "scripts": {
    "prepare": "husky",
    "dev": "vite",
    "typecheck": "tsc --noEmit",
    "lint": "eslint . --max-warnings 0",
    "lint:format": "prettier --check .",
    "lint:markdown": "markdownlint-cli2",
    "test": "vitest run",
    "a11y": "playwright test",
    "build": "vite build",
    "build:offline": "node scripts/build-offline.mjs",
    "preview": "vite preview",
    "versions:check": "npm ls --depth=0",
    "test:bundle-size": "vitest run tests/performance/bundle-size.test.ts"
  },
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{md,markdown}": ["markdownlint-cli2 --fix", "prettier --write"],
    "*.{json,yml,yaml}": ["prettier --write"]
  }
}
```

```bash
# .husky/pre-commit — runs lint-staged, typecheck, and unit tests
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"
npx lint-staged && npm run typecheck && npm run test
```

**Order matters:** `eslint --fix` runs first, then `prettier --write` reformats the autofixed output. This avoids drift between the linter's fixed point and the formatter's fixed point.

#### 15.3 Quality gate script

```bash
#!/bin/bash
# scripts/quality-gate.sh — runs all 8 pre-ship gates in order. Exits non-zero on first failure.
set -e
echo "1. Typecheck...";      npm run typecheck
echo "2. Lint...";           npm run lint && npm run lint:format && npm run lint:markdown
echo "3. Unit tests...";     npm run test -- --coverage
echo "4. A11y tests...";     npm run a11y
echo "5. Build (online)..."; npm run build
echo "6. Build (offline)..."; npm run build:offline
echo "7. Bundle size...";    npm run test:bundle-size
echo "8. Verify deps...";    npm run versions:check
echo ""; echo "All 8 quality gates passed."
```

#### 15.4 Lighthouse CI configuration

```yaml
# lighthouserc.yml
ci:
  collect:
    url: [http://localhost:4173/]
    numberOfRuns: 3
  assert:
    preset: lighthouse:no-pwa
    assertions:
      categories:performance: ["warn", { "minScore": 0.9 }]
      categories:accessibility: ["error", { "minScore": 0.95 }]
      categories:best-practices: ["error", { "minScore": 0.95 }]
      categories:seo: ["warn", { "minScore": 0.9 }]
  upload:
    target: temporary-public-storage
```

#### 15.5 Dropped from draft_q2

- **Visual regression tests** — require screenshot baseline management; out of scope for base skill (Appendix E).
- **Coverage upload (codecov)** — nice-to-have; `fail_ci_if_error: false` makes it informational.
- **Multi-framework matrix** — React-only by design (§1).

---
