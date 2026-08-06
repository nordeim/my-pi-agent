# markdown-to-web — Project Skill

> **Purpose:** Enable any future agent to understand, maintain, extend, or rebuild this general‑purpose, configurable Markdown‑to‑web rendering system without rediscovering its architecture, configuration contract, or accessibility requirements.
>
> **When to use:** For any project that needs to turn a Markdown document (or a set of documents) into a responsive, accessible, single‑file web page with a table of contents, syntax highlighting, custom badges, and theme customisation.
>
> **Output of this skill:** This document (`markdown-to-web-SKILL.md`) and the accompanying source code repository.

---

## 1. Project Identity & Design Philosophy

**One‑sentence description:** A zero‑backend, single‑file HTML generator that renders any Markdown document as a polished, accessible, configurable web page, with automatic TOC, syntax highlighting, image embedding, and a theme system driven entirely by a configuration object.

**Design thesis:** *Content is the source of truth; configuration drives presentation.* The Markdown file is the only content source; all visual and behavioural customisation is declared in a single config file. The renderer uses `react-markdown` with a suite of plugins; the build system inlines everything into a portable `index.html`. The UI is accessible (WCAG 2.2 AA), responsive, and free of generic aesthetics.

**Non‑negotiable principles:**
- **Configurable, not hard‑coded** – Every design token, TOC depth, badge pattern, and feature toggle is defined in a configuration object, not buried in code.
- **Single‑file output** – The final artifact is one self‑contained `index.html` with all CSS/JS inlined (via `vite‑plugin‑singlefile`). No external assets required at runtime (except for fonts, which are loaded via CSS `@import` by default – but can be inlined or replaced).
- **Evidence‑based reporting** – The original badge system is generalised: users can define their own severity/confidence patterns with CSS classes, keeping the same honesty‑first philosophy.
- **Accessibility first** – Skip‑to‑content, focus indicators, keyboard navigation, semantic HTML, `prefers‑reduced‑motion`, and sufficient colour contrast are built in.
- **Tested and maintainable** – Unit, integration, and accessibility tests protect against regressions; strict TypeScript and linting enforce code quality.

**Anti‑generic mandate (explicitly avoided):** The default theme is neutral and editorial, but the system is designed so that a user can create their own visual identity – no purple gradients, no Bootstrap card grids, no Inter/Roboto safety unless they choose it.

---

## 2. Tech Stack & Environment

| Layer | Technology | Version | Critical Note |
|-------|------------|---------|---------------|
| Framework | React | 19.2.6 | Strict TypeScript; functional components only; no class components. |
| Build | Vite | 7.3.2 | `vite‑plugin‑singlefile` for one‑file output; `?raw` imports for Markdown. |
| Styling | Tailwind CSS | 4.1.17 | CSS‑first `@theme` in `src/styles/theme.css`; no `tailwind.config.js`. |
| Markdown | react‑markdown | 10.1.0 | `remark‑gfm` (tables, strikethrough, task lists) + `rehype‑slug` (heading anchors). |
| Slug generation | github‑slugger | 2.0.0 | Must stay in sync with `rehype‑slug` (both use the same algorithm). |
| Syntax highlighting | highlight.js | 11.11.1 | Light/dark themes; extensible via CSS. |
| Icons | lucide‑react | 1.28.0 | Menu, X, ExternalLink, Sun, Moon (minimal set). |
| Testing | Vitest + React Testing Library + axe‑core | – | Unit, integration, and accessibility tests. |
| Linting | ESLint 9 + plugin‑react‑hooks + plugin‑jsx‑a11y | – | Enforce best practices and accessibility rules. |
| Formatting | Prettier 3.x | – | Consistent code style. |
| Packaging | vite‑plugin‑singlefile | 2.3.0 | Inlines all assets into `dist/index.html`. |
| Package Manager | pnpm (or npm) | – | pnpm recommended for speed and disk efficiency. |
| Node | – | ≥20.19 or ≥22.12 | Required by Vite 7. |

**Verification:** `cat package.json` → all dependencies match the versions above. Use `pnpm list` to confirm.

---

## 3. Configuration System

The entire behaviour of the application is driven by a single configuration file, conventionally named `markdown‑to‑web.config.ts` (or `.js`), placed in the project root. This file exports a default object conforming to the `MarkdownToWebConfig` interface.

### 3.1 Configuration Schema (TypeScript)

```typescript
// types/config.ts

export interface MarkdownToWebConfig {
  /** The Markdown content – either a string or a file path (resolved relative to config) */
  markdown: string;          // path or content

  /** Table of Contents settings */
  toc: {
    /** Heading levels to include, e.g., [1,2,3] for H1–H3; default [2,3] */
    levels?: (1|2|3|4|5|6)[];
    /** Maximum nesting depth; default 3 */
    maxDepth?: number;
    /** Exclude headings matching this regex (applied to text) */
    excludePattern?: RegExp;
  };

  /** Theme customisation */
  theme: {
    /** Custom colours – maps to CSS custom properties */
    colors?: {
      primary?: string;       // e.g., '#0e7c86'
      background?: string;    // page background
      text?: string;          // default text colour
      // ... any other variables
    };
    /** Font families – for display, body, mono */
    fonts?: {
      display?: string;       // e.g., 'Source Serif 4'
      body?: string;          // e.g., 'Inter'
      mono?: string;          // e.g., 'JetBrains Mono'
    };
    /** Dark mode: 'auto' (follows system), true (always dark), false (always light) */
    darkMode?: 'auto' | true | false;
    /** Custom CSS overrides (string of raw CSS) */
    customCSS?: string;
  };

  /** Badge / inline‑code styling patterns */
  badges: {
    /** Array of pattern objects – first match wins */
    patterns: Array<{
      /** Regex to match the inline code content; capture groups for values */
      regex: RegExp;
      /** Map of value -> Tailwind class string (or CSS classes) */
      styleMap: Record<string, string>;
    }>;
    /** Default class if no pattern matches */
    defaultClass?: string;
  };

  /** Image handling */
  images: {
    /** Embed images as base64 data URIs (true) or link them as‑is (false) */
    embed?: boolean;
    /** Maximum size in kilobytes to embed; larger images are linked */
    maxSizeKb?: number;
  };

  /** Accessibility overrides */
  accessibility?: {
    /** Touch target size minimum: '44px' (AAA) or '36px' (AA); default '44px' */
    touchTarget?: '44px' | '36px';
    /** Enable reduced motion support; default true */
    reducedMotion?: boolean;
  };

  /** Output settings */
  output?: {
    /** Output filename, default 'index.html' */
    filename?: string;
  };
}
```

### 3.2 Default Configuration (merged)

The system ships with a sensible default configuration that mimics the original report style. The user only needs to override what they want to change.

```typescript
// src/lib/defaultConfig.ts

export const defaultConfig: MarkdownToWebConfig = {
  markdown: './src/content/report.md',  // placeholder
  toc: {
    levels: [2, 3],
    maxDepth: 2,
  },
  theme: {
    colors: {
      primary: '#0e7c86',
      background: '#fbfaf7',
      text: '#0f1e1c',
    },
    fonts: {
      display: '"Source Serif 4", ui-serif, Georgia, serif',
      body: '"Inter", ui-sans-serif, system-ui, sans-serif',
      mono: '"JetBrains Mono", ui-monospace, monospace',
    },
    darkMode: 'auto',
    customCSS: '',
  },
  badges: {
    patterns: [
      {
        regex: /^\s*-\s*\*\*(Severity|Confidence):\*\*\s+(.+)$/im,
        styleMap: {
          critical: 'bg-red-50 text-red-700 ring-red-200',
          high: 'bg-amber-50 text-amber-700 ring-amber-200',
          medium: 'bg-yellow-50 text-yellow-700 ring-yellow-200',
          low: 'bg-lime-50 text-lime-700 ring-lime-200',
          informational: 'bg-blue-50 text-blue-700 ring-blue-200',
          verified: 'bg-teal-50 text-teal-700 ring-teal-200',
          reasoned: 'bg-violet-50 text-violet-700 ring-violet-200',
          assumed: 'bg-orange-50 text-orange-700 ring-orange-200',
          unverifiable: 'bg-stone-100 text-stone-600 ring-stone-300',
        },
      },
    ],
    defaultClass: 'bg-gray-100 text-gray-700',
  },
  images: {
    embed: true,
    maxSizeKb: 200,
  },
  accessibility: {
    touchTarget: '44px',
    reducedMotion: true,
  },
  output: {
    filename: 'index.html',
  },
};
```

### 3.3 Loading the Configuration

At build time, Vite loads the user config and merges it with defaults. The resulting configuration is injected into the React app via a global `__CONFIG__` variable or by importing a generated config module. The exact mechanism is handled by a Vite plugin that reads the config file and creates a virtual module `virtual:config` that exports the merged config.

---

## 4. Bootstrapping & Commands

### 4.1 Setup

```bash
# Clone the repository
git clone <repo-url> markdown-to-web
cd markdown-to-web

# Install dependencies (using pnpm recommended)
pnpm install

# Place your Markdown file and config (e.g., markdown-to-web.config.ts)
# Edit the config to point to your markdown file.
```

### 4.2 Commands

| Command | Description |
|---------|-------------|
| `pnpm dev` | Start Vite dev server with hot reload. |
| `pnpm build` | Build the production single‑file HTML in `dist/`. |
| `pnpm preview` | Preview the built file locally. |
| `pnpm test` | Run all tests (Vitest). |
| `pnpm test:ui` | Run tests with UI. |
| `pnpm lint` | Run ESLint. |
| `pnpm format` | Run Prettier. |
| `pnpm tsc` | Typecheck without emitting. |

### 4.3 Configuration File

Create a `markdown-to-web.config.ts` in the project root:

```typescript
import { defineConfig } from 'markdown-to-web';

export default defineConfig({
  markdown: './my-document.md',
  toc: { levels: [2, 3, 4] },
  theme: {
    colors: { primary: '#2b6f9b', background: '#ffffff' },
    darkMode: false,
  },
  badges: {
    patterns: [
      {
        regex: /-\s*\*\*Status:\*\*\s+(\w+)/i,
        styleMap: {
          pass: 'bg-green-50 text-green-700',
          fail: 'bg-red-50 text-red-700',
          warn: 'bg-yellow-50 text-yellow-700',
        },
      },
    ],
  },
});
```

The `defineConfig` helper provides type safety and autocompletion.

---

## 5. The Design System (Code-First)

### 5.1 CSS Variables

All design tokens are exposed as CSS custom properties, defined in `src/styles/theme.css`. They are derived from the merged configuration.

```css
/* src/styles/theme.css (generated) */
:root {
  --color-primary: #0e7c86;
  --color-background: #fbfaf7;
  --color-text: #0f1e1c;
  --color-ink-950: #0b1615;     /* derived from primary, etc. */
  --font-display: "Source Serif 4", ui-serif, Georgia, serif;
  --font-body: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;
  --touch-target-min: 44px;
  /* ... more variables */
}

[data-theme="dark"] {
  --color-background: #0f1e1c;
  --color-text: #fbfaf7;
  /* ... dark overrides */
}
```

### 5.2 Tailwind `@theme` Integration

Tailwind v4 uses the `@theme` directive to generate utilities from CSS variables. In `src/styles/theme.css` we include:

```css
@theme {
  --font-display: var(--font-display);
  --font-body: var(--font-body);
  --font-mono: var(--font-mono);
  --color-primary: var(--color-primary);
  /* ... */
}
```

This creates Tailwind classes like `font-display`, `text-primary`, `bg-background`, etc., without a separate configuration file.

### 5.3 Typography Hierarchy (Default)

| Role | Font Variable | Weight | Size (mobile) | Size (sm+) | Tracking | Color |
|------|---------------|--------|---------------|------------|----------|-------|
| H1 | `--font-display` | 600 | `text-3xl` | `sm:text-4xl` | normal | `text` |
| H2 | `--font-display` | 600 | `text-2xl` | `sm:text-[1.75rem]` | normal | `text` |
| H3 | `--font-display` | 600 | `text-xl` | – | normal | `text` |
| Body | `--font-body` | 400 | base (16px) | – | normal | `text` |
| Meta | `--font-mono` | 500/600 | `text-xs` | – | `tracking-widest` | `primary` |
| Badge | `--font-body` | 600 | `text-xs` | – | `tracking-wide uppercase` | per‑style |

All these can be overridden via the config theme or custom CSS.

### 5.4 Keyframes & Animations

Minimal animations: smooth scroll, fade‑in for drawer, and hover transitions. All defined in `src/styles/base.css`:

```css
html { scroll-behavior: smooth; }
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
}
```

No custom keyframes unless configured.

---

## 6. Component Architecture & Patterns

### 6.1 File Structure

```
src/
├── main.tsx                     # Entry: StrictMode + createRoot
├── App.tsx                      # Layout, TOC, drawer state, theme provider
├── components/
│   ├── MarkdownRenderer.tsx     # ReactMarkdown with custom renderers
│   ├── TableOfContents.tsx      # Recursive TOC nav (sidebar + drawer)
│   ├── SyntaxHighlighter.tsx    # Code block wrapper with highlight.js
│   ├── StatusBadge.tsx          # Generic badge renderer from config patterns
│   └── ThemeToggle.tsx          # Light/dark mode switch
├── lib/
│   ├── config.ts                # Load and merge config (build‑time)
│   ├── toc.ts                   # TOC extraction (configurable levels)
│   ├── enhance.ts               # Preprocessor for badge patterns
│   └── images.ts                # Image embedding utilities
├── styles/
│   ├── theme.css                # CSS variables + @theme (generated)
│   ├── base.css                 # Global styles, reset, accessibility
│   └── highlight.css            # Syntax highlighting themes
├── utils/
│   └── cn.ts                    # clsx + tailwind-merge
├── types/
│   └── index.ts                 # Shared TypeScript interfaces
└── content/                     # (Optional) Default markdown location
    └── example.md
```

### 6.2 Data Flow

```
markdown-to-web.config.ts
         │
         ├─► merged with defaultConfig ──► config object
         │
         ├─► markdown file (via ?raw) ────► markdown string
         │
         ├─► buildToc(config.toc) ────────► TocItem[] ──► TableOfContents
         │
         └─► enhanceMarkdown(markdown, config.badges) ──► processed markdown
                  │
                  └─► ReactMarkdown (remark-gfm + rehype-slug)
                           │
                           ├─► custom renderers (h1–h6, p, a, img, pre, code, table, etc.)
                           │
                           ├─► code inline ──► StatusBadge (config‑driven)
                           │
                           └─► pre/code ────► SyntaxHighlighter (highlight.js)
```

### 6.3 Key Components

**`App.tsx`** – Layout and state:
- `useState(false)` for mobile drawer
- `useMemo` for TOC and processed markdown (based on config)
- Injects theme variables and class (`[data-theme]`)
- Header (sticky), sidebar (desktop), drawer (mobile), main content

**`MarkdownRenderer.tsx`** – Renderer factory:
- Accepts `markdown` and `config` as props
- Builds a `components` map using ReactMarkdown's `components` prop
- Inline code is passed to `StatusBadge` with the config's badge patterns
- Images use the custom `img` renderer (embed or link)
- Code blocks use `SyntaxHighlighter`

**`TableOfContents.tsx`** – Recursive nav:
- Uses `TocItem` tree from `buildToc`
- `onNavigate` callback to close drawer on mobile
- No internal state; fully controlled

**`StatusBadge.tsx`** – Config‑aware:
- Receives `children` (the inline code text) and `badgeConfig`
- Iterates over `patterns`, matches via regex, applies corresponding `styleMap`
- Falls back to `defaultClass`

**`SyntaxHighlighter.tsx`** – Highlight.js integration:
- Uses `highlight.js` with the `className` to detect language
- Renders a `pre` with `hljs` class and highlighted HTML

**`ThemeToggle.tsx`** – Light/dark switch:
- Uses `useState` to track current theme (light/dark)
- Toggles `data-theme` attribute on `<html>`
- Persists preference in `localStorage`

---

## 7. Custom Hooks

The application defines a few custom hooks to encapsulate logic:

| Hook | File | Purpose |
|------|------|---------|
| `useTheme` | `hooks/useTheme.ts` | Manages theme state, persists to localStorage, detects system preference. |
| `useConfig` | `hooks/useConfig.ts` | Returns the merged configuration (provided via context). |
| `useToc` | `hooks/useToc.ts` | Builds TOC from markdown and config; memoized. |
| `useDrawer` | `hooks/useDrawer.ts` | Handles mobile drawer open/close with keyboard and focus trapping. |

---

## 8. Content Management & Data Ingestion

### 8.1 Markdown Source

The Markdown content is supplied via the config’s `markdown` property. It can be a **file path** (resolved relative to the config file) or a **direct string** (for small snippets). At build time, Vite’s `?raw` import reads the file if it is a path, or the string is used directly.

### 8.2 Images

Images referenced in Markdown (`![](path)`) are processed by the custom `img` renderer:
- If `embed` is `true` and the image size ≤ `maxSizeKb`, the image is read from disk, encoded as base64, and injected as a `data:image/...` URI.
- Otherwise, the original `src` is used (relative to the output HTML). This allows linking to external or larger images.
- The `alt` text is passed through.

### 8.3 Badge Patterns

The badge system uses a list of patterns; each pattern is a regex and a `styleMap`. The `enhance` preprocessor scans the Markdown for lines that match any pattern and wraps the captured value in a custom HTML element (e.g., `<span data-badge="value">`) or a code block with a class. The `StatusBadge` component then applies the corresponding CSS class.

Alternative approach: use a unified processing step that transforms the Markdown before rendering, adding specific inline code blocks with classes. We chose the preprocessor approach for simplicity and performance.

### 8.4 TOC Generation

`buildToc` extracts headings based on the configured `levels`. It uses `github-slugger` to generate slugs that match `rehype-slug`. The output is a tree of `TocItem` nodes with `level`, `text`, `slug`, and `children`.

---

## 9. Accessibility (WCAG 2.2 AA) Implementation

| Feature | Implementation |
|---------|----------------|
| Skip‑to‑content | `<a href="#main-content" class="sr-only focus:not-sr-only">` |
| Focus visible | `:focus-visible` styles on all interactive elements. |
| Touch targets | Minimum size configurable (default 44px) via CSS variable `--touch-target-min`. |
| Reduced motion | CSS media query disables smooth scrolling; configurable toggle. |
| Heading hierarchy | H1–H6 used logically; no skipped levels. |
| Anchor offset | `scroll-mt-24` on headings compensates for sticky header. |
| ARIA labels | Landmarks: `header`, `main`, `aside`, `nav`, `footer`; `aria-label` for navigation and drawer. |
| Keyboard navigation | Full keyboard support: Tab, Enter, Space, Escape (for drawer). |
| Color contrast | Default theme meets WCAG AAA for text/background (≥7:1). Badge text contrasts checked against background; user must ensure custom colours pass. |
| Dark mode | All colors invert appropriately; contrast maintained. |
| Focus trapping | Drawer traps focus when open; returns focus to trigger on close. |

**Testing:** Automated axe‑core tests in CI; manual testing with screen readers (NVDA, VoiceOver) and keyboard.

---

## 10. Anti-Patterns & Common Bugs

| # | Anti-Pattern | Symptom | Root Cause | Fix |
|---|--------------|---------|------------|-----|
| 1 | Badge regex too broad | Inline code incorrectly styled | Regex matches unintended content | Make regex more specific; test with sample content. |
| 2 | Slug mismatch | TOC links jump to wrong heading | `github-slugger` version differs from `rehype-slug` | Use the same version; verify in tests. |
| 3 | Image embedding fails | Image doesn't appear | Path is relative to config file, not Markdown | Use absolute or resolve correctly; document that paths are relative to config. |
| 4 | Dark mode not applied | Theme toggle doesn't change colors | CSS variables not overridden in `[data-theme="dark"]` | Ensure all color variables have dark counterparts. |
| 5 | Touch target too small (AA) | User fails WCAG AAA | Config sets `touchTarget: '36px'` | Set default to 44px; document the tradeoff. |
| 6 | Fonts not loading offline | Text uses fallback fonts | Google Fonts `@import` requires network | Provide option to inline fonts or use system fonts. |

---

## 11. Debugging Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Build fails with `Cannot find module` | Config file not found or syntax error | Check filename and path; ensure it exports default. |
| TOC is empty | No headings at configured levels | Adjust `toc.levels` or add headings. |
| Badge not styled | Regex not matching | Test regex with your Markdown; use online regex tester. |
| Images not embedded | Image size exceeds `maxSizeKb` or path incorrect | Increase limit or correct path. |
| Syntax highlighting missing | Code block language not specified or not supported | Add language (` ```js `); verify highlight.js supports it. |
| Theme toggle not persistent | localStorage blocked or not used | Fallback to system preference; document. |
| Drawer doesn't close on navigation | `onNavigate` not passed to TOC links | Ensure `TableOfContents` receives `onNavigate` from `App`. |

---

## 12. Pre-Ship Checklist

**Mandatory verification gate (run in order):**

```bash
# 1. Typecheck
pnpm tsc --noEmit

# 2. Lint
pnpm lint

# 3. Test (unit + integration + accessibility)
pnpm test

# 4. Build production
pnpm build

# 5. Smoke test the build
pnpm preview
# Open in browser; verify:
# - TOC shows correct headings
# - Badges styled according to config
# - Code blocks highlighted
# - Images appear (embedded or linked)
# - Theme toggle works (light/dark)
# - Responsive (sidebar on desktop, drawer on mobile)
# - Keyboard navigation works
# - Skip link works
# - No console errors
```

**No deploy gate** – the skill is ready for consumption.

---

## 13. Lessons Learnt (From Original)

1. **Config matters** – Hard‑coding design decisions led to a single‑purpose tool. Generalising required a complete re‑architecture around a config object, but it paid off.
2. **Slugs must be deterministic** – `github-slugger` and `rehype-slug` must use the same algorithm. We now lock versions and test.
3. **Preprocessing is powerful** – The badge system is a classic case where the renderer lacks context; preprocessing at the string level is simpler and more reliable than trying to infer from the AST.
4. **Accessibility is a process** – It’s not a one‑time fix; continuous testing with axe and manual checks is essential.
5. **Image embedding tradeoffs** – Base64 increases HTML size; a configurable limit is the right balance.
6. **Documentation is the product** – A skill is only as good as its documentation; we invested heavily in this document.

---

## 14. Pitfalls to Avoid

| Area | Don't Do This | Do This Instead |
|------|---------------|-----------------|
| Badges | Write custom parsing in the component | Use a preprocessor and a generic `StatusBadge`. |
| TOC | Hardcode heading levels | Use configurable `levels` and `maxDepth`. |
| Styling | Use arbitrary Tailwind values (`text-[#abc]`) | Use CSS variables from the theme system. |
| Images | Assume all images are in the same directory | Resolve paths relative to config; document. |
| Accessibility | Forget focus trapping in drawer | Implement with `useEffect` and `focus‑trap` library or custom logic. |
| Testing | Only test the happy path | Test edge cases: empty markdown, no headings, malformed badges. |
| Config | Overcomplicate with many options | Provide sensible defaults; document each option with examples. |

---

## 15. Best Practices

**Code Organisation:**
- One component per file; colocate types.
- Pure functions in `lib/` have no side effects.
- Use path alias `@/*` → `src/*`.

**TypeScript:**
- `strict: true`; `any` prohibited; use `unknown` when necessary.
- Interface for objects; type for unions.
- Exhaustive checking for config switches.

**React:**
- Functional components + hooks; no HOCs.
- Memoize expensive computations (`useMemo`, `useCallback`).
- Use `React.memo` for pure components.

**Tailwind v4:**
- CSS‑first: all tokens in `@theme`; no `tailwind.config.js`.
- Use semantic classes (e.g., `text-primary`) over hardcoded values.

**Testing:**
- Unit tests: pure functions, utilities.
- Integration: render full page with mock config, assert DOM output.
- Accessibility: axe‑core on every render.

**Documentation:**
- Keep the skill document up‑to‑date with code changes.
- Include examples for every configuration option.
- Provide a quickstart for first‑time users.

---

## 16. Coding Patterns

### Pattern: Config‑Driven Preprocessor

```typescript
// src/lib/enhance.ts
export function enhanceMarkdown(markdown: string, badgeConfig: BadgeConfig): string {
  let result = markdown;
  for (const pattern of badgeConfig.patterns) {
    result = result.replace(pattern.regex, (match, ...groups) => {
      // groups contain captured values; wrap with custom HTML
      return `<span data-badge="${groups[0]}">${groups[0]}</span>`;
    });
  }
  return result;
}
```

**Why:** The renderer lacks context; preprocessing at string level allows fine‑grained control.

### Pattern: Recursive TOC Generation

```typescript
// src/lib/toc.ts
export function buildToc(markdown: string, levels: number[]): TocItem[] {
  const slugger = new GithubSlugger();
  const lines = markdown.split('\n');
  const stack: TocItem[] = [];
  const root: TocItem[] = [];
  let currentParent = root;

  for (const line of lines) {
    const match = line.match(/^(#{1,6})\s+(.+)/);
    if (!match) continue;
    const level = match[1].length;
    if (!levels.includes(level)) continue;
    const text = match[2].replace(/`/g, '');
    const slug = slugger.slug(text);
    const item: TocItem = { level, text, slug, children: [] };
    // ... stack logic to nest
  }
  return root;
}
```

**Why:** Single source of truth for TOC; configurable levels; slug consistency.

### Pattern: Renderer Factory

```typescript
// src/components/MarkdownRenderer.tsx
export function MarkdownRenderer({ markdown, config }: Props) {
  const components = useMemo(() => ({
    code: ({ children, className, ...props }) => {
      const isInline = !className;
      if (isInline) {
        return <StatusBadge value={String(children)} config={config.badges} />;
      }
      return <SyntaxHighlighter language={className?.replace('language-', '')}>{children}</SyntaxHighlighter>;
    },
    img: ({ src, alt }) => <CustomImage src={src} alt={alt} config={config.images} />,
    // ... other elements
  }), [config]);

  return <ReactMarkdown components={components} remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeSlug]}>{markdown}</ReactMarkdown>;
}
```

**Why:** All rendering logic centralized; easily extensible.

---

## 17. Coding Anti-Patterns

| Anti-Pattern | Example (Don't) | Correct |
|--------------|-----------------|---------|
| Hardcoded colours | `className="text-blue-600"` | Use `text-primary` (from theme). |
| Ignoring config | `if (level === 2)` | Use `if (config.toc.levels.includes(level))`. |
| Direct DOM manipulation | `document.querySelector('#drawer').classList.toggle()` | Use React state and conditional rendering. |
| Inline styles for theming | `style={{ color: '#0e7c86' }}` | Use CSS variables and Tailwind classes. |
| Not handling empty states | TOC fails when no headings | Return empty array; render nothing. |
| Mutating config | `config.badges.patterns.push(newPattern)` | Use immutable merge; treat config as read‑only. |

---

## 18. Responsive Breakpoint Reference

**Tailwind defaults (no custom config):**
- `sm`: 640px
- `md`: 768px (used sparingly)
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px

**Actual usage in the default theme:**
- `sm:` – Adjust padding, font sizes, show desktop nav.
- `lg:` – Show sidebar, hide drawer toggle.
- No `md:`/`xl:`/`2xl:` except where needed.

Custom breakpoints can be added via the theme's custom CSS.

---

## 19. Z-Index Layer Map

| z-index | Element | Purpose |
|---------|---------|---------|
| `z-50` | Skip‑to‑content (focused), mobile drawer overlay + panel | Topmost |
| `z-40` | Sticky header | Above content, below drawer |
| `z-30` | Drawer backdrop | – |
| default | Main content, sidebar | Normal flow |

---

## 20. Color Reference (Default Theme)

| Token | Hex | Tailwind Class | Usage |
|-------|-----|----------------|-------|
| `primary` | `#0e7c86` | `text-primary`, `bg-primary` | Accents, links, buttons |
| `background` | `#fbfaf7` | `bg-background` | Page background |
| `text` | `#0f1e1c` | `text-text` | Body text |
| `ink-950` | `#0b1615` | – | Dark surfaces |
| `ink-900` | `#0f1e1c` | – | Headings |
| `paper-50` | `#fbfaf7` | – | Background (same as `background`) |
| `paper-100` | `#f4f2ec` | – | Lighter backgrounds |
| `paper-200` | `#e9e5da` | – | Borders |

All tokens are derived from the config's `colors` object. The default maps to the original report palette for continuity.

---

## 21. Complete TypeScript Interface Reference

### `MarkdownToWebConfig` (defined above in Section 3.1)

### `TocItem`
```typescript
export interface TocItem {
  level: number;          // 1–6
  text: string;
  slug: string;
  children: TocItem[];
}
```

### `BadgeConfig`
```typescript
export interface BadgeConfig {
  patterns: Array<{
    regex: RegExp;
    styleMap: Record<string, string>;
  }>;
  defaultClass?: string;
}
```

### `ImageConfig`
```typescript
export interface ImageConfig {
  embed?: boolean;
  maxSizeKb?: number;
}
```

### `ThemeConfig`
```typescript
export interface ThemeConfig {
  colors?: Record<string, string>;
  fonts?: {
    display?: string;
    body?: string;
    mono?: string;
  };
  darkMode?: 'auto' | boolean;
  customCSS?: string;
}
```

### `AccessibilityConfig`
```typescript
export interface AccessibilityConfig {
  touchTarget?: '44px' | '36px';
  reducedMotion?: boolean;
}
```

---

## Appendices

### Appendix A: Migration from `react-markdown-report`

If you are migrating from the original single‑purpose report skill, follow these steps:

1. Copy your Markdown content to the new project's `src/content/` (or wherever you like).
2. Create a `markdown-to-web.config.ts` that replicates your old design:
   - Set `toc.levels` to `[2,3]` (the original only used H2/H3).
   - Set `theme.colors` to match the old palette (`ink-950`, `paper-50`, etc.).
   - Set `badges.patterns` to include the default `Severity/Confidence` pattern (provided in the default config).
   - Optionally, set `images.embed: true` if you had images.
3. Run `pnpm build` and verify the output matches the old report visually.
4. The new system includes dark mode, syntax highlighting, and more, but you can disable them via config if needed.

### Appendix B: Custom CSS Example

To add custom CSS, use the `theme.customCSS` property:

```typescript
export default defineConfig({
  // ...
  theme: {
    customCSS: `
      h1 { letter-spacing: -0.02em; }
      .badge { border-radius: 9999px; }
      @media (max-width: 640px) {
        .sidebar { display: none; }
      }
    `,
  },
});
```

### Appendix C: Build Output

- `dist/index.html` – the single file, fully self‑contained (except fonts, which are loaded via `@import`; you can inline them by using a custom font loader or base64 fonts).
- The file is minified and optimised by Vite.

### Appendix D: Extending the Skill

To add new features (e.g., custom remark plugins, new syntax highlighting themes, additional UI components), follow the standard React/Vite development flow:

1. Add the dependency.
2. Update the relevant component or pipeline.
3. Update the configuration schema and default config.
4. Write tests.
5. Update this skill document.

---

**Skill version:** `1.0.0`  
**Generated:** 2026-08-06  
**Scope:** Full general‑purpose Markdown‑to‑web rendering system, configurable, accessible, and production‑ready.
