---
name: brutalist-portfolio-nextjs
description: Complete Next.js 16 + React 19 + TypeScript strict brutalist portfolio reference. App Router, Server Components, 16 components, design system with Tailwind v4 CSS-first @theme, 8+ remediation phases, 52 lessons learned. Covers WCAG AAA accessibility, custom hooks, anti-pattern debugging, before/after debugging, mobile nav debugging. Use when building brutalist/avant-garde portfolio sites or reconstructing a production-grade Next.js portfolio from scratch.
---

# Nicholas Yun — The Engineered Soul: Complete Skill Reference (v6)

> **Document Version**: 6.0
> **Last Updated**: 2026-06-23
> **Codebase Status**: Post-Remediation 8 (ThemeSwitch Hydration Fix)
> **License**: MIT
> **Component Count**: 16 active (15 Client + 1 Server Component ThemeScript)

---

## Table of Contents

1. [Project Identity & Design Philosophy](#1-project-identity--design-philosophy)
2. [Project Execution Phases (Six-Phase Workflow)](#2-project-execution-phases-six-phase-workflow)
3. [Tech Stack & Environment](#3-tech-stack--environment)
4. [Bootstrapping & Configuration](#4-bootstrapping--configuration)
5. [The Design System (Code-First)](#5-the-design-system-code-first)
6. [CSS Strategy for Tailwind v4](#6-css-strategy-for-tailwind-v4)
7. [Component Architecture & Patterns](#7-component-architecture--patterns)
8. [Custom Hooks Deep Dive](#8-custom-hooks-deep-dive)
9. [Content Management (Static TypeScript Data)](#9-content-management-static-typescript-data)
10. [Accessibility (WCAG AAA) Implementation](#10-accessibility-wcag-aaa-implementation)
11. [Anti-Patterns & Common Bugs](#11-anti-patterns--common-bugs)
12. [Debugging Guide](#12-debugging-guide)
13. [Pre-Ship Checklist](#13-pre-ship-checklist)
14. [Lessons Learnt & How to Avoid Them (ALL 52)](#14-lessons-learnt--how-to-avoid-them-all-52)
15. [Pitfalls to Avoid](#15-pitfalls-to-avoid)
16. [Best Practices](#16-best-practices)
17. [Coding Patterns](#17-coding-patterns)
18. [Coding Anti-Patterns](#18-coding-anti-patterns)
19. [Responsive Breakpoint Reference](#19-responsive-breakpoint-reference)
20. [Z-Index Layer Map](#20-z-index-layer-map)
21. [Color Reference (Complete)](#21-color-reference-complete)
22. [The Complete TypeScript Interface Reference](#22-the-complete-typescript-interface-reference)

---

## 1. Project Identity & Design Philosophy

### Name
**Nicholas Yun — The Engineered Soul**

### Tagline
Full-Stack Developer · Designer · Engineer

### Design Philosophy: Tactile Brutalism

This portfolio adheres to a **Tactile Brutalism** design philosophy — raw, unapologetic, and deliberately devoid of decorative softness. The aesthetic draws from architectural brutalism: exposed structure, monolithic surfaces, and honest materiality translated to the digital realm.

**Core Tenets:**

1. **No border-radius.** Ever. (Unless explicitly requested by the owner.) Sharp corners are non-negotiable — they signal the brutalist commitment to structural honesty.

2. **Monochromatic with accent.** The Night theme uses near-blacks (#0a0a0a → #333333) with a single gold accent (#e8c547). The Day theme uses warm off-whites (#f5f0e8 → #b8b0a2) with a dark gold accent (#b8860b). Every color earns its place.

3. **Typography as architecture.** Three font families serve distinct purposes:
   - **Cormorant Garamond** (serif/display) — Headlines, editorial voice
   - **DM Sans** (sans/body) — Body text, UI labels
   - **IBM Plex Mono** (monospace/utility) — Nav, labels, metadata, terminal

4. **Brutal shadows.** Offset box-shadows (4px 4px 0 0) that feel structural, not decorative.

5. **Grid as texture.** A 28px grid underpins all spacing. Decorative grid lines appear in the hero section.

6. **Honest interactions.** No skeuomorphic effects. No gradients masquerading as depth. Animations are functional (fade-up, slide-in) not ornamental.

7. **Content-first.** Every element serves the content. No empty decorative sections.

### The "Never" List (from AGENTS.md, expanded)

These are hard rules that must never be violated:

```
Never use border-radius (unless explicitly requested)
Never use any in TypeScript
Never use Vite-specific features like import.meta.glob
Never add speculative "AI slop" or safe defaults
Never add speculative "AI slop" or safe defaults
Never add optimizeFonts to next.config.ts
Never put @import url() after @import "tailwindcss"
Never use class-based theme switching
Never set data-theme on <body>
Never use db without null guard
Never access array indices without ?. or ??
Never import PortfolioApp from @/components/PortfolioApp
Never type react-error-boundary error prop as Error
Never import from @/lib/_archive/data
Never hardcode site config in components
Never create API route without rate limiting
Never hardcode credentials
Never access ContactApiResponse.error without checking success
Never trust remediation docs without validating paths
Never call setState synchronously inside useEffect
Never let _archive/ code trigger ESLint errors
Never use as type casts on unvalidated input
Never expose internal error details in production
Never fall back to shared IP in rate limiting
Never use document.getElementById in React components
Never use grid-column: span 2 without responsive fallback
Never use as const without satisfies
Never leave setInterval without clearInterval
Never allow tsconfig.json include patterns broader than needed
Never let agent instruction files fall out of sync
Never mix license declarations across project files
Never count components without auditing actual files
Never version-control large binary archives
Never reference CSS variables that aren't defined in @theme — they silently resolve to unset
```

---

## 2. Project Execution Phases (Six-Phase Workflow)

Every project follows this disciplined multi-phase sequence. Each phase has explicit deliverables and verification gates. Skipping phases introduces defects that compound exponentially across subsequent phases.

### Phase 1: ANALYZE — Deep Requirement Mining

- Never make surface-level assumptions. Identify explicit requirements, implicit needs, and ambiguities.
- Research existing codebases, documentation, and relevant resources before proposing solutions.
- Explore multiple approaches, evaluating technical feasibility, alignment with project goals, and long-term implications.
- Perform risk assessment: identify dependencies, challenges, and mitigation strategies.
- **For a port**: Audit the source project thoroughly. Catalog every component, interaction, design token, and data structure. Identify what must be preserved faithfully and what can evolve. Map every `import.meta.glob` usage (Vite-specific) to static TypeScript data.
- **For remediation**: Read ALL documentation files (CLAUDE.md, AGENTS.md, README.md, any code review reports, status files, existing SKILL files) before touching code. These contain critical project-specific constraints and gotchas that are not obvious from the code alone. Remediation reports written without codebase access may reference files that don't exist — validate every file path against the actual structure.

### Phase 2: PLAN — Structured Execution Roadmap

- Create a detailed plan with sequential phases, clear objectives, integrated checklists, success criteria, and validation checkpoints.
- Present the plan for explicit user confirmation before writing any code.
- Include estimated effort for each phase.
- **For a port**: Map every source component to its target implementation. Identify which components need redesign vs. faithful port. Plan the content strategy (static TypeScript data vs. CMS vs. markdown files).
- **For remediation**: Identify the full scope of changes — new types, renamed fields, import path corrections, dependency additions, CSS variable definitions — before extracting any files. Cross-reference the remediation report against the current codebase state. List every file that will be modified or created.

### Phase 3: VALIDATE — Explicit Confirmation

- Obtain explicit user approval of the plan.
- Address concerns or modifications to the plan.
- Ensure alignment on all aspects before implementation begins.
- This gate prevents scope creep and ensures the agent and user share the same understanding.

### Phase 4: IMPLEMENT — Modular, Tested, Documented

- Set up environment: dependencies, configurations, prerequisites.
- Implement in logical, testable components following the layered architecture.
- Practice continuous testing: verify each component before integration.
- Follow library-first approach: use existing UI/component libraries (e.g., `react-error-boundary`) when available, apply bespoke styling only to achieve the design vision.
- Track progress against the plan and communicate deviations.
- **Critical for remediation**: After extracting files from a remediation report, verify package versions against npm BEFORE running `npm install`. Remediation reports often specify versions that don't exist on npm. Use `npm view <pkg> dist-tags` to check.
- **Critical for new builds**: Define all CSS variables in `@theme` before building components. Undefined `var()` references fail silently.

### Phase 5: VERIFY — Rigorous QA

- Run typecheck (`npx tsc --noEmit`) — zero errors required.
- Run production build (`npm run build`) — zero errors required.
- Run lint (`npm run lint`) — zero warnings required.
- Review for accessibility: skip links, focus-visible, reduced motion, ARIA attributes, focus management, contrast ratios (in BOTH themes).
- Consider edge cases: missing environment variables, null database connections, empty data arrays, keyboard-only navigation.
- Verify visual fidelity against the design system.
- **After remediation**: Run a full codebase audit — check for stale references to removed/renamed files, verify ALL CSS variable references resolve to `@theme` definitions, verify Tailwind class names are defined, check for duplicate type definitions, verify component integration status (active vs archived), verify `VALID_SECTIONS` matches section IDs, verify theme target consistency.

### Phase 6: DELIVER — Complete Handoff

- Provide clear usage instructions (dev, build, lint, typecheck, DB commands).
- Document challenges encountered and solutions implemented.
- Classify components as "active" (wired into the app) vs. "archived" (in `_archive/` directories, not integrated).
- Update ALL documentation (README.md, CLAUDE.md, AGENTS.md, GEMINI.md) to reflect the current state.
- List outstanding issues and recommendations for future work.
- Create archive of the codebase for repo refresh if needed.
- Append to the work log with a structured summary.

---

## 3. Tech Stack & Environment

### Exact Dependency Versions

**Runtime Dependencies:**

| Package | Version |
|---------|---------|
| next | ^16.2.9 |
| react | ^19.2.7 |
| react-dom | ^19.2.7 |
| drizzle-orm | ^0.45.2 |
| postgres | ^3.4.7 |
| react-error-boundary | ^6.1.2 |

**Dev Dependencies:**

| Package | Version |
|---------|---------|
| tailwindcss | ^4.1.17 |
| @tailwindcss/postcss | ^4.1.17 |
| typescript | ^5.9.3 |
| eslint | ^9.29.0 |
| eslint-config-next | ^16.2.6 |
| drizzle-kit | ^0.31.4 |
| @types/node | ^24.0.3 |
| @types/react | ^19.2.17 |
| @types/react-dom | ^19.2.3 |

### Overrides (package.json)

```json
"overrides": {
  "esbuild": ">=0.25.0",
  "postcss": ">=8.5.10"
}
```

These override transitive dependency versions to patch known vulnerabilities.

### Node.js Requirement

```
"engines": { "node": ">=20.0.0" }
```

### NPM Scripts

```json
{
  "dev": "next dev --turbopack",
  "build": "npm run typecheck && next build",
  "start": "next start",
  "lint": "next lint",
  "typecheck": "tsc --noEmit",
  "db:generate": "drizzle-kit generate",
  "db:migrate": "drizzle-kit migrate",
  "db:studio": "drizzle-kit studio"
}
```

**Key notes:**
- `dev` uses `--turbopack` for fast local development
- `build` runs `typecheck` before `next build` — type errors block production builds
- Database commands are separate — the app runs fine without a database

### react-error-boundary v6.1.2 — Critical Note

From v4 onward, `FallbackProps.error` is typed as `unknown`, NOT `Error`. This was a breaking change that persists through v6. You MUST use a type guard to narrow it:

```typescript
// CORRECT — type guard
function ErrorFallback({ error, resetErrorBoundary }: {
  error: unknown;
  resetErrorBoundary: () => void;
}) {
  const message = error instanceof Error ? error.message : "Unknown error";
  // ...
}

// WRONG — will not compile
function ErrorFallback({ error }: { error: Error }) {
  // TS error: Type 'unknown' is not assignable to type 'Error'
}
```

### Next.js 16 Breaking Changes

1. **`optimizeFonts` is removed.** It was a Next.js 13–15 config option. In Next.js 16, font optimization is automatic. Adding it to `next.config.ts` causes a build error.

2. **App Router is the default.** No Pages Router code exists.

3. **Turbopack is the recommended dev bundler.** Use `next dev --turbopack`.

### Tailwind CSS v4 Notes

1. **Import order is critical.** `@import "tailwindcss"` MUST come before any `@theme` block or custom CSS. Placing `@import url()` (e.g., Google Fonts) before `@import "tailwindcss"` breaks the entire design token system silently.

2. **`@theme` block replaces `tailwind.config.js`.** Design tokens are defined in `globals.css` using the `@theme` directive.

3. **No `tailwind.config.js` or `tailwind.config.ts` file exists.** All configuration is in `globals.css` and `postcss.config.mjs`.

---

## 4. Bootstrapping & Configuration

### Project Structure

```
personal-portfolio-next/
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Server Component — root layout, metadata, ThemeScript
│   │   ├── page.tsx            # "use client" — ErrorBoundary + dynamic PortfolioApp
│   │   ├── PortfolioApp.tsx    # "use client" — main orchestrator (IMPORTANT: in src/app/, NOT src/components/)
│   │   ├── globals.css         # Tailwind v4 @theme + all design tokens
│   │   ├── error.tsx           # "use client" — Next.js error boundary
│   │   ├── not-found.tsx       # Server Component — 404 page
│   │   └── api/
│   │       ├── contact/route.ts   # POST — rate-limited contact form
│   │       └── health/route.ts    # GET — DB health check
│   ├── components/
│   │   ├── ThemeScript.tsx     # Server Component — inline script in <head>
│   │   ├── Navigation.tsx      # "use client" — sticky nav, mobile menu
│   │   ├── HeroKinetic.tsx     # "use client" — hero with staggered animation
│   │   ├── SectionBlock.tsx    # "use client" — reusable section wrapper
│   │   ├── ErrorBoundary.tsx   # "use client" — class-based per-section boundary
│   │   ├── BentoGrid.tsx       # "use client" — auto-fit grid with span-2
│   │   ├── ProjectsSection.tsx # "use client" — tag filtering
│   │   ├── ProjectCard.tsx     # "use client" — project display card
│   │   ├── SkillsSection.tsx   # "use client" — category grouping
│   │   ├── Timeline.tsx        # "use client" — ol with time elements
│   │   ├── BlogSection.tsx     # "use client" — "Coming Soon" placeholder
│   │   ├── Terminal.tsx        # "use client" — interactive CLI
│   │   ├── ContactSection.tsx  # "use client" — form with validation
│   │   ├── Footer.tsx          # "use client" — site config links
│   │   ├── ThemeSwitch.tsx     # "use client" — role="switch"
│   │   ├── ScrollReveal.tsx    # "use client" — IntersectionObserver
│   │   └── _archive/           # Dormant components (excluded from tsconfig, ESLint)
│   ├── hooks/
│   │   ├── useRouteHash.ts     # Hash-based routing with pushState
│   │   ├── useReducedMotion.ts # prefers-reduced-motion detection
│   │   └── _archive/           # Dormant hooks
│   ├── lib/
│   │   ├── types.ts            # All TypeScript interfaces (centralized)
│   │   ├── site-config.ts      # Single source of truth for site data
│   │   ├── projects.ts         # Static project data
│   │   ├── skills.ts           # Static skills data
│   │   ├── timeline.ts         # Static timeline data
│   │   ├── rate-limit.ts       # In-memory rate limiter
│   │   └── _archive/           # Dormant data modules
│   └── db/
│       ├── index.ts            # drizzle + postgres (optional — can be null)
│       └── schema.ts           # analytics table schema
├── public/
│   ├── favicon.svg
│   └── og-image.png
├── next.config.ts
├── tsconfig.json
├── eslint.config.mjs
├── postcss.config.mjs
├── drizzle.config.ts
├── package.json
└── .env.example
```

### tsconfig.json (Exact)

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "react-jsx",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./src/*"] },
    "noUncheckedIndexedAccess": true
  },
  "include": [
    "next-env.d.ts",
    "**/*.ts",
    "**/*.tsx",
    ".next/types/**/*.ts",
    ".next/dev/types/**/*.ts"
  ],
  "exclude": ["node_modules", "skills", "src/**/_archive"]
}
```

**Critical settings:**
- `strict: true` — Full strict mode
- `noUncheckedIndexedAccess: true` — Array/object index access returns `T | undefined`
- `skills` excluded — The 61MB skills directory is not type-checked
- `src/**/_archive` excluded — Dormant code doesn't pollute builds

### ESLint Configuration (Exact)

```javascript
// eslint.config.mjs
import { defineConfig, globalIgnores } from "eslint/config";
import nextCoreWebVitals from "eslint-config-next/core-web-vitals";

export default defineConfig([
  ...nextCoreWebVitals,
  globalIgnores([".next/**", "out/**", "build/**", "next-env.d.ts", "**/_archive/**"]),
]);
```

**Critical notes:**
- `eslint-config-next/core-web-vitals` ALREADY includes `eslint-plugin-jsx-a11y`. Do NOT re-import it separately — doing so causes `ConfigError: Cannot redefine plugin "jsx-a11y"`.
- `_archive/**` is globally ignored — dormant code does not trigger lint errors.

### PostCSS Configuration

```javascript
// postcss.config.mjs
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
```

Tailwind v4 uses the `@tailwindcss/postcss` plugin. There is no separate `autoprefixer` entry — it's built in.

### next.config.ts (Exact)

```typescript
import type { NextConfig } from "next";

const securityHeaders = [
  { key: "X-Frame-Options", value: "DENY" },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
  { key: "Strict-Transport-Security", value: "max-age=63072000; includeSubDomains; preload" },
  {
    key: "Content-Security-Policy",
    value: "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self';",
  },
];

const nextConfig: NextConfig = {
  poweredByHeader: false,
  reactStrictMode: true,
  allowedDevOrigins: ["personal-portfolio-next.jesspete.shop"],
  images: {
    formats: ["image/avif", "image/webp"],
  },
  async headers() {
    return [{ source: "/(.*)", headers: securityHeaders }];
  },
};

export default nextConfig;
```

**Security notes:**
- CSP `script-src` is `'self'` only — NO `'unsafe-eval'`. This is intentional and required for security.
- `'unsafe-inline'` in `style-src` is needed for inline `style={{}}` objects.
- `poweredByHeader: false` removes the `X-Powered-By: Next.js` header.
- HSTS includes `preload` for browser HSTS lists.

### drizzle.config.ts

```typescript
import { defineConfig } from "drizzle-kit";

const databaseUrl = process.env.DATABASE_URL;

if (!databaseUrl) {
  throw new Error(
    "DATABASE_URL environment variable is not set. " +
    "Copy .env.example to .env.local and configure your database connection.",
  );
}

export default defineConfig({
  dialect: "postgresql",
  schema: "./src/db/schema.ts",
  dbCredentials: { url: databaseUrl },
});
```

**Critical:** This reads from `process.env.DATABASE_URL`, NOT from a `.json` file with hardcoded credentials. (The old `drizzle.config.json` was deleted in Remediation 7.)

### .env.example

```
DATABASE_URL=
NEXT_PUBLIC_SITE_URL=
EMAIL_API_KEY=
```

- `DATABASE_URL` — PostgreSQL connection string (optional — app runs without it)
- `NEXT_PUBLIC_SITE_URL` — Used for OG metadata base URL
- `EMAIL_API_KEY` — For future email service integration (Resend, SendGrid, etc.)

---

## 5. The Design System (Code-First)

All design tokens live in `src/app/globals.css` inside the `@theme` block. This is the single source of truth for the visual system. Components reference these tokens via `var(--token-name)` in inline `style={{}}` objects.

### Night Theme (Default) — Color Tokens

```css
@theme {
  /* Base colors */
  --color-bg: #0a0a0a;
  --color-bg-soft: #111111;
  --color-surface: #1a1a1a;
  --color-border: #222222;
  --color-border-strong: #333333;

  /* Text colors */
  --color-text-primary: #f0ece4;
  --color-text-secondary: #a8a29e;
  --color-text-muted: #918983;       /* WCAG AA 5.76:1 against #0a0a0a */

  /* Accent colors */
  --color-accent: #e8c547;
  --color-accent-hover: #f0d060;
  --color-accent-muted: #e8c54733;

  /* Semantic tokens */
  --color-text-inverse: #0a0a0a;
  --color-border-subtle: #1a1a1a;
  --color-bg-sunken: #070707;
  --color-bg-elevated: #222222;
  --color-error: #c0392b;
  --color-accent-subtle: #e8c5471a;
}
```

### Day Theme — Override Tokens

```css
[data-theme="day"] {
  --color-bg: #f5f0e8;
  --color-bg-soft: #ede8df;
  --color-surface: #e5e0d6;
  --color-border: #d5cfc4;
  --color-border-strong: #b8b0a2;

  --color-text-primary: #1a1612;
  --color-text-secondary: #5c5650;
  --color-text-muted: #6b6560;       /* WCAG AA 5.06:1 against #f5f0e8 */

  --color-accent: #b8860b;
  --color-accent-hover: #996f08;
  --color-accent-muted: #b8860b22;

  --color-text-inverse: #f5f0e8;
  --color-border-subtle: #e5e0d6;
  --color-bg-sunken: #ece7dd;
  --color-bg-elevated: #faf6ef;
  --color-error: #a93226;
  --color-accent-subtle: #b8860b1a;
}
```

### Font Families

```css
@theme {
  --font-sans: "DM Sans", system-ui, sans-serif;
  --font-mono: "IBM Plex Mono", "Fira Code", monospace;
  --font-serif: "Cormorant Garamond", "Georgia", serif;

  /* Semantic aliases (prefer these in components) */
  --font-editorial: "Cormorant Garamond", "Georgia", serif;
  --font-utility: "IBM Plex Mono", "Fira Code", monospace;
  --font-body: "DM Sans", system-ui, sans-serif;
  --font-display: "Cormorant Garamond", "Georgia", serif;
}
```

**Font usage rules:**
- `--font-display` / `--font-editorial` — h1, large display text
- `--font-body` / `--font-sans` — paragraphs, body text
- `--font-utility` / `--font-mono` — nav, labels, metadata, terminal

### Spacing Scale

```css
@theme {
  --spacing-grid: 28px;
  --spacing-double: 56px;
  --spacing-half: 14px;
  --spacing-quarter: 7px;
}
```

The 28px grid is the foundation. All padding, margins, and gaps should be multiples or fractions of this base unit.

### Z-Index Scale

```css
@theme {
  --z-index-grain: 50;
  --z-index-machine: 40;
  --z-index-mobile-backdrop: 45;
  --z-index-mobile-drawer: 46;
  --z-index-skip-link: 100;
  --z-index-loader: 60;
}
```

### Transitions

```css
@theme {
  --transition-fast: 150ms ease;
}
```

### Shadows

```css
@theme {
  --shadow-brutal: 4px 4px 0 0 var(--color-border-strong);
  --shadow-brutal-sm: 2px 2px 0 0 var(--color-border);
}
```

The Day theme overrides these to use its own `--color-border-strong` and `--color-border` values.

### Animations

```css
@theme {
  --animate-fade-in: fade-in 0.6s ease forwards;
  --animate-fade-up: fade-up 0.6s ease forwards;
  --animate-slide-in: slide-in 0.4s ease forwards;
}
```

### Keyframes

```css
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slide-in {
  from { opacity: 0; transform: translateX(-20px); }
  to { opacity: 1; transform: translateX(0); }
}
```

### Global CSS Utilities

**Skip Link:**
```css
.skip-link {
  position: absolute;
  top: -100%;
  left: 16px;
  z-index: var(--z-index-skip-link);
  padding: 8px 16px;
  background: var(--color-accent);
  color: var(--color-bg);
  font-family: var(--font-utility);
  font-size: 0.875rem;
  text-decoration: none;
  transition: top 0.2s ease;
}
.skip-link:focus {
  top: 16px;
}
```

**Grid Overlay:**
```css
.grid-overlay {
  position: fixed;
  inset: 0;
  z-index: var(--z-index-grain);
  pointer-events: none;
  background-image:
    linear-gradient(to right, var(--color-border) 1px, transparent 1px),
    linear-gradient(to bottom, var(--color-border) 1px, transparent 1px);
  background-size: var(--spacing-grid) var(--spacing-grid);
  opacity: 0.15;
}
```

**Grain Texture:**
```css
.grain-overlay {
  position: fixed;
  inset: 0;
  z-index: var(--z-index-grain);
  pointer-events: none;
  opacity: 0.03;
  will-change: transform;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
}
```

**Bento Grid Responsive Span:**
```css
.bento-span-2 {
  grid-column: span 2;
}
@media (max-width: 640px) {
  .bento-span-2 {
    grid-column: span 1;
  }
}
```

**Reduced Motion:**
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**Scrollbar:**
```css
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--color-bg); }
::-webkit-scrollbar-thumb { background: var(--color-border-strong); border-radius: 0; }
::-webkit-scrollbar-thumb:hover { background: var(--color-text-muted); }
```

Note: `border-radius: 0` on scrollbar thumb — brutalist consistency.

**Selection:**
```css
::selection {
  background: var(--color-accent-muted);
  color: var(--color-text-primary);
}
```

### The Styling Rule: Inline style={{}} with CSS Variables

**ALL component styling uses inline `style={{}}` objects referencing CSS variables.** Tailwind utility classes are NOT used for component styling. This is a deliberate architectural choice, not an oversight.

```typescript
// CORRECT — inline style with CSS variables
<button style={{
  fontFamily: "var(--font-mono)",
  fontSize: "0.8125rem",
  color: "var(--color-text-primary)",
  border: "2px solid var(--color-border)",
  padding: "var(--spacing-half) var(--spacing-grid)",
  borderRadius: 0,
}}>
  Click
</button>

// WRONG — Tailwind utility classes (not used in this project)
<button className="font-mono text-sm text-primary border-2 p-3.5 rounded-none">
  Click
</button>
```

Tailwind CSS v4 is installed solely for its `@theme` directive and CSS reset. The utility classes are available but intentionally unused in component code.

---

## 6. CSS Strategy for Tailwind v4

### Import Order (Build-Breaking If Wrong)

This is the single most common build failure. The order must be:

```css
@import "tailwindcss";

@theme { ... }
```

**Alternative (if you need external font imports in CSS)**:
```css
@import url("https://fonts.googleapis.com/css2?family=...");
@import "tailwindcss";

@theme { ... }
```

**Why**: Tailwind v4's `@import "tailwindcss"` expands to `@layer base`, `@layer components`, and `@layer utilities`. CSS specification requires `@import` rules to precede all other rules except `@charset` and `@layer` statements. If `@import url(...)` comes after `@import "tailwindcss"`, the CSS optimizer rejects it and the fonts will not load.

**Recommended approach**: Load Google Fonts via `<link>` tags in `layout.tsx` `<head>` with `preconnect`. This avoids the CSS import ordering issue entirely and provides better performance through early resource hints:

```tsx
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=IBM+Plex+Mono:wght@300;400;500;600&display=swap" rel="stylesheet" />
```

### Design Tokens in `@theme`, Not `tailwind.config`

Tailwind v4 uses CSS-first configuration. Define all tokens in the `@theme` block of `globals.css`:

```css
@theme {
  --font-editorial: "Cormorant Garamond", Georgia, serif;
  --font-body: "DM Sans", system-ui, sans-serif;
  --font-mono: "IBM Plex Mono", monospace;
  --color-bg: #0a0a0a;
  --spacing-grid: 28px;
}
```

These become available as Tailwind utilities automatically: `font-editorial`, `bg-bg`, `p-grid`, etc.

### Custom Tailwind Utility Classes

If components need custom utility classes (e.g., `font-utility`, `font-editorial`, `z-grain`), they MUST be defined in the `@theme` block. Undefined classes silently fail — the element renders with browser defaults.

### CSS Variable Naming: The Two-Convention Problem

Active components use `--color-` prefix: `--color-border`, `--color-text-primary`, `--color-bg`. Archived components in `_archive/` directories use shorthand names that do NOT exist in `@theme`: `--border-color`, `--text-primary`, `--bg-surface`, `--bg-primary`, `--bg-elevated`, `--text-secondary`, `--text-muted`, `--border-strong`, `--color-accent-code`, `--color-accent-poetry`.

Before integrating any archived component, either:
1. Define alias variables in `globals.css` (quick fix, adds technical debt)
2. Rewrite the component to use the `--color-` prefix convention (proper fix, eliminates debt)

---

## 7. Component Architecture & Patterns

### Component Inventory (16 Active)

**15 Client Components** (all have `"use client"` directive):

| # | Component | Lines | File | Role |
|---|-----------|-------|------|------|
| 1 | Navigation | 287 | `src/components/Navigation.tsx` | Sticky nav, mobile menu with focus trap, ESC close, aria-current |
| 2 | HeroKinetic | 132 | `src/components/HeroKinetic.tsx` | Staggered fade-up, useReducedMotion, decorative grid lines |
| 3 | SectionBlock | 50 | `src/components/SectionBlock.tsx` | Reusable section wrapper with ScrollReveal + h2 |
| 4 | ErrorBoundary | 91 | `src/components/ErrorBoundary.tsx` | Class component, retry button |
| 5 | BentoGrid | 112 | `src/components/BentoGrid.tsx` | Auto-fit grid with span-2 responsive collapse |
| 6 | ProjectsSection | 99 | `src/components/ProjectsSection.tsx` | Tag filtering with useMemo |
| 7 | ProjectCard | 159 | `src/components/ProjectCard.tsx` | next/image, tech tags, links with aria-labels |
| 8 | SkillsSection | 106 | `src/components/SkillsSection.tsx` | Category grouping via Map |
| 9 | Timeline | 123 | `src/components/Timeline.tsx` | ol with dots, time elements |
| 10 | BlogSection | 35 | `src/components/BlogSection.tsx` | "Coming Soon" placeholder |
| 11 | Terminal | 262 | `src/components/Terminal.tsx` | Interactive CLI, command history, role="log", aria-live |
| 12 | ContactSection | 342 | `src/components/ContactSection.tsx` | Full form validation, fetch /api/contact, aria-invalid |
| 13 | Footer | 67 | `src/components/Footer.tsx` | Site config links, dynamic year |
| 14 | ThemeSwitch | 55 | `src/components/ThemeSwitch.tsx` | role="switch", localStorage + system preference |
| 15 | ScrollReveal | 79 | `src/components/ScrollReveal.tsx` | IntersectionObserver, direction prop, useReducedMotion |

**1 Server Component:**

| # | Component | Lines | File | Role |
|---|-----------|-------|------|------|
| 16 | ThemeScript | 26 | `src/components/ThemeScript.tsx` | Inline script in `<head>`, no FOUC |

### Rendering Architecture

```
layout.tsx (Server Component)
  ├── <html lang="en" suppressHydrationWarning>
  ├── <head>
  │   ├── Google Fonts <link>
  │   ├── ThemeScript (blocking inline script — sets data-theme before paint)
  │   └── LD+JSON structured data
  ├── <body>
  │   ├── Skip link (<a className="skip-link">)
  │   └── children → page.tsx
  │
page.tsx ("use client")
  └── ErrorBoundary (react-error-boundary, page-level)
      └── PortfolioApp (dynamic import, SSR ENABLED)
          ├── <div aria-live="polite"> (announcement ref)
          ├── <header role="banner">
          │   └── Navigation (eager) + ThemeSwitch
          ├── <main id="main-content" role="main">
          │   ├── <section id="hero">
          │   │   └── ErrorBoundary → HeroKinetic (eager)
          │   ├── <section id="about">
          │   │   └── ErrorBoundary → Suspense → SectionBlock → BentoGrid (lazy)
          │   ├── <section id="projects">
          │   │   └── ErrorBoundary → Suspense → SectionBlock → ProjectsSection (lazy) → ProjectCard
          │   ├── <section id="skills">
          │   │   └── ErrorBoundary → Suspense → SectionBlock → SkillsSection (lazy)
          │   ├── <section id="experience">
          │   │   └── ErrorBoundary → Suspense → SectionBlock → Timeline (lazy)
          │   ├── <section id="blog">
          │   │   └── ErrorBoundary → Suspense → SectionBlock → BlogSection (lazy)
          │   ├── <section id="terminal">
          │   │   └── ErrorBoundary → Suspense → Terminal (lazy)
          │   └── <section id="contact">
          │       └── ErrorBoundary → Suspense → SectionBlock → ContactSection (lazy)
          └── <footer role="contentinfo">
              └── Suspense → Footer (lazy)
```

### Loading Strategy

- **Eager (above fold):** Navigation, ThemeSwitch, HeroKinetic
- **Lazy (below fold):** BentoGrid, ProjectsSection, SkillsSection, Timeline, BlogSection, Terminal, ContactSection, Footer
- **Dynamic import:** PortfolioApp via `next/dynamic` (SSR enabled — `ssr: false` was removed in Remediation 7)
- **Lazy via React.lazy():** All below-fold sections use `React.lazy()` + `<Suspense>`

```typescript
// page.tsx — PortfolioApp is dynamically imported
const PortfolioApp = dynamic(() => import("@/app/PortfolioApp"), {
  loading: () => <LoadingSkeleton />,
});

// PortfolioApp.tsx — below-fold sections use React.lazy()
const ProjectsSection = lazy(() => import("@/components/ProjectsSection"));
const SkillsSection = lazy(() => import("@/components/SkillsSection"));
const Timeline = lazy(() => import("@/components/Timeline"));
const ContactSection = lazy(() => import("@/components/ContactSection"));
const BlogSection = lazy(() => import("@/components/BlogSection"));
const Terminal = lazy(() => import("@/components/Terminal"));
const Footer = lazy(() => import("@/components/Footer"));
const BentoGrid = lazy(() => import("@/components/BentoGrid"));
```

### Error Boundary Strategy

Two levels of error boundaries:

1. **Page-level:** `react-error-boundary` wraps PortfolioApp in `page.tsx`. The `FallbackComponent` receives `error: unknown` (NOT `Error`).

2. **Section-level:** Custom `ErrorBoundary` class component wraps each section in `PortfolioApp.tsx`. Provides section-specific error messages and retry buttons.

```typescript
// Section-level error boundary usage
<ErrorBoundary fallback={<SectionError name="Projects" />}>
  <Suspense fallback={<SectionSkeleton />}>
    <SectionBlock id="projects-content" title="Projects">
      <ProjectsSection />
    </SectionBlock>
  </Suspense>
</ErrorBoundary>
```

### Skeleton and Error Fallbacks

```typescript
// SectionSkeleton — loading state
function SectionSkeleton() {
  return (
    <div
      aria-hidden="true"
      style={{
        minHeight: "200px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: "var(--font-mono)",
        fontSize: "0.75rem",
        color: "var(--color-text-muted)",
        letterSpacing: "0.1em",
        textTransform: "uppercase",
      }}
    >
      Loading&hellip;
    </div>
  );
}

// SectionError — error state
function SectionError({ name }: { name: string }) {
  return (
    <div
      role="alert"
      style={{
        padding: "var(--spacing-grid)",
        border: "2px solid var(--color-error, #c0392b)",
        fontFamily: "var(--font-mono)",
        fontSize: "0.8125rem",
      }}
    >
      <p>Failed to load the {name} section.</p>
    </div>
  );
}
```

### PortfolioApp.tsx — The Orchestrator

**Critical location:** `src/app/PortfolioApp.tsx` — NOT `src/components/PortfolioApp.tsx`. Importing from `@/components/PortfolioApp` will fail.

```typescript
// PortfolioApp.tsx — key patterns

export default function PortfolioApp() {
  const [currentHash, navigateTo] = useRouteHash();
  const announcementRef = useRef<HTMLDivElement>(null);

  // Theme initialization is handled by ThemeScript.tsx in <head>.
  // No duplicate useEffect needed here — it was removed to avoid
  // redundant DOM writes and potential hydration mismatches.

  const handleThemeChange = useCallback((theme: "day" | "night") => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);

    // Announce theme change to screen readers via React ref (NOT document.getElementById)
    if (announcementRef.current) {
      announcementRef.current.textContent = `Switched to ${theme} theme`;
    }
  }, []);

  return (
    <>
      <div
        ref={announcementRef}
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      />
      {/* ... sections ... */}
    </>
  );
}
```

**Key decisions:**
- `announcementRef` uses `useRef<HTMLDivElement>(null)` — NOT `document.getElementById()`
- No duplicate theme initialization `useEffect` — ThemeScript handles it in `<head>`
- `handleThemeChange` is memoized with `useCallback`

### ThemeScript — The Single Initialization Point

```typescript
// src/components/ThemeScript.tsx
// This is a SERVER component — it renders an inline <script> in <head>

export function ThemeScript() {
  const script = `
    (function() {
      try {
        var stored = localStorage.getItem('theme');
        if (stored === 'night' || stored === 'day') {
          document.documentElement.setAttribute('data-theme', stored);
          return;
        }
        var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.documentElement.setAttribute('data-theme', prefersDark ? 'night' : 'day');
      } catch (e) {
        document.documentElement.setAttribute('data-theme', 'night');
      }
    })();
  `;

  return (
    <script
      dangerouslySetInnerHTML={{ __html: script }}
      suppressHydrationWarning
    />
  );
}
```

**Why this works:**
1. Runs as a blocking script in `<head>` before any CSS paints — no FOUC
2. Sets `data-theme` on `document.documentElement` (the `<html>` element) — NOT `<body>`, NOT via class
3. Reads `localStorage` first, falls back to `prefers-color-scheme`, then defaults to "night"
4. `suppressHydrationWarning` prevents React hydration mismatch warning
5. `try/catch` handles private browsing where `localStorage` throws

### Navigation Component — Key Patterns

```typescript
// Mobile menu with focus trap
useEffect(() => {
  if (!isMobileMenuOpen || !mobileMenuRef.current) return;

  const focusable = Array.from(
    mobileMenuRef.current.querySelectorAll<HTMLElement>(
      'a[href], button, [tabindex]:not([tabindex="-1"])',
    ),
  );

  if (focusable.length > 0) {
    focusable[0]?.focus();
  }

  // Focus trap: cycle Tab within the mobile menu
  const handleTabKey = (e: globalThis.KeyboardEvent) => {
    if (e.key !== "Tab" || focusable.length === 0) return;

    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last?.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first?.focus();
    }
  };

  document.addEventListener("keydown", handleTabKey);
  return () => document.removeEventListener("keydown", handleTabKey);
}, [isMobileMenuOpen]);

// ESC key closes mobile menu and returns focus to hamburger button
useEffect(() => {
  if (!isMobileMenuOpen) return;

  const handleEscape = (e: globalThis.KeyboardEvent) => {
    if (e.key === "Escape") {
      setIsMobileMenuOpen(false);
      menuButtonRef.current?.focus();
    }
  };

  document.addEventListener("keydown", handleEscape);
  return () => document.removeEventListener("keydown", handleEscape);
}, [isMobileMenuOpen]);
```

### ThemeSwitch Component

**CRITICAL: Two-Pass Render for SSR Safety (Remediation 8)**

`ThemeSwitch` reads `localStorage`/`matchMedia` to determine the current theme. When SSR is enabled (after Remediation 7 removed `ssr: false`), this causes a hydration mismatch because the server cannot access these APIs. The fix uses a two-pass render:

```typescript
"use client";
import { useCallback, useEffect, useState } from "react";

export default function ThemeSwitch({ onThemeChange }: ThemeSwitchProps) {
  /**
   * Two-pass render strategy to avoid hydration mismatch:
   *
   * 1. SSR + first client render: always "day" (safe default)
   * 2. After hydration (useEffect): read actual theme from
   *    ThemeScript.tsx's data-theme attribute and re-render.
   */
  const [theme, setTheme] = useState<"day" | "night">("day");
  const [isHydrated, setIsHydrated] = useState(false);

  useEffect(() => {
    const rafId = requestAnimationFrame(() => {
      const attr = document.documentElement.getAttribute("data-theme");
      if (attr === "night" || attr === "day") {
        setTheme(attr);
      }
      setIsHydrated(true);
    });
    return () => cancelAnimationFrame(rafId);
  }, []);

  const toggleTheme = useCallback(() => {
    setTheme((prev) => {
      const next = prev === "day" ? "night" : "day";
      onThemeChange(next);
      return next;
    });
  }, [onThemeChange]);

  const isNight = theme === "night";

  return (
    <button
      role="switch"
      aria-checked={isNight}
      aria-label={`Switch to ${isNight ? "day" : "night"} theme`}
      onClick={toggleTheme}
      aria-disabled={!isHydrated}
      style={{
        background: "transparent",
        border: "2px solid var(--color-border)",
        padding: "var(--spacing-quarter) var(--spacing-half)",
        cursor: "pointer",
        fontFamily: "var(--font-mono)",
        fontSize: "0.75rem",
        letterSpacing: "0.1em",
        textTransform: "uppercase",
        borderRadius: 0,
        color: "var(--color-text-primary)",
        lineHeight: 1,
        minWidth: "3rem",
        textAlign: "center" as const,
        transition: "background var(--transition-fast), color var(--transition-fast)",
        opacity: isHydrated ? 1 : 0.6, // Visual cue for pre-hydration state
      }}
    >
      {isNight ? "NIGHT" : "DAY"}
    </button>
  );
}
```

**Key patterns:**
- `useState("day")` — SSR-safe default that matches the server render
- `useEffect` + `requestAnimationFrame` — defers state update to next paint, avoiding React 19 `setState-in-effect` ESLint error
- Reads from DOM attribute (set by `ThemeScript.tsx`) instead of `localStorage`/`matchMedia` — ensures server/client agreement
- `aria-disabled` + opacity — visual cue that the component is in pre-hydration state

### ContactSection — Form Validation Pattern

```typescript
// Client-side validation
function validateForm(data: FormData): FormErrors {
  const errors: FormErrors = {};
  if (!data.name.trim()) errors.name = "Name is required.";
  if (!data.email.trim()) {
    errors.email = "Email is required.";
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
    errors.email = "Please enter a valid email address.";
  }
  if (!data.message.trim()) {
    errors.message = "Message is required.";
  } else if (data.message.trim().length < 10) {
    errors.message = "Message must be at least 10 characters.";
  }
  return errors;
}

// Each field has aria-invalid and aria-describedby
<input
  id="contact-name"
  type="text"
  value={formData.name}
  onChange={handleChange("name")}
  aria-invalid={!!errors.name}
  aria-describedby={errors.name ? "name-error" : undefined}
  required
  autoComplete="name"
  disabled={status === "submitting"}
  style={errors.name ? errorInputStyle : inputStyle}
/>
```

### ErrorBoundary (Class Component)

```typescript
// Custom class-based ErrorBoundary for section-level errors
export default class ErrorBoundary extends Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }
  }

  handleRetry = (): void => {
    this.setState({ hasError: false, error: null });
  };

  render(): ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) return this.props.fallback;
      // ... default error UI with Retry button
    }
    return this.props.children;
  }
}
```

---

## 8. Custom Hooks Deep Dive

### useRouteHash — Hash-Based SPA Routing

```typescript
// src/hooks/useRouteHash.ts

import { useState, useEffect, useCallback } from "react";

const VALID_SECTIONS = [
  "hero", "about", "projects", "skills",
  "experience", "blog", "terminal", "contact",
] as const;

type Section = (typeof VALID_SECTIONS)[number];

function getHashFromWindow(): string {
  if (typeof window === "undefined") return "hero";
  const hash = window.location.hash.replace("#", "");
  return VALID_SECTIONS.includes(hash as Section) ? hash : "hero";
}

export function useRouteHash(): [string, (section: string) => void] {
  const [activeSection, setActiveSectionState] = useState<string>(
    getHashFromWindow
  );

  const setActiveSection = useCallback((section: string) => {
    const clean = section.replace(/^#/, "");
    const valid = VALID_SECTIONS.includes(clean as Section)
      ? clean
      : "hero";
    // pushState avoids default browser scroll-to-anchor behaviour
    window.history.pushState(null, "", "#" + valid);
    setActiveSectionState(valid);

    // Move focus to the section heading for keyboard users
    requestAnimationFrame(() => {
      const sectionEl = document.getElementById(valid);
      if (sectionEl) {
        const heading = sectionEl.querySelector("h1, h2, h3");
        if (heading instanceof HTMLElement) {
          heading.setAttribute("tabindex", "-1");
          heading.focus({ preventScroll: true });
        }
      }
    });
  }, []);

  useEffect(() => {
    // popstate fires on back/forward navigation
    function handlePopState() {
      const hash = window.location.hash.replace("#", "");
      const valid = VALID_SECTIONS.includes(hash as Section) ? hash : "hero";
      setActiveSectionState(valid);
    }

    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  return [activeSection, setActiveSection];
}
```

**Critical implementation details:**

1. **Uses `history.pushState`** — NOT `window.location.hash`. Direct hash assignment triggers the browser's default scroll-to-anchor behavior, which conflicts with the SPA layout. `pushState` updates the URL without scrolling.

2. **Listens for `popstate`** — NOT `hashchange`. The `popstate` event fires on browser back/forward navigation. The `hashchange` event is redundant when using `pushState`.

3. **Focus management** — After navigation, focus moves to the section heading with `tabindex="-1"` and `focus({ preventScroll: true })`. This ensures keyboard users don't lose their place.

4. **Returns a tuple** — `[string, (section: string) => void]`, not an object. This matches React convention for simple state-like hooks.

5. **Validation** — Invalid hash values fall back to "hero". The `VALID_SECTIONS` array is the source of truth.

### useReducedMotion — prefers-reduced-motion Detection

```typescript
// src/hooks/useReducedMotion.ts

import { useState, useEffect } from "react";

const SSR_SAFE_DEFAULT = false;

function getPrefersReducedMotion(): boolean {
  if (typeof window === "undefined") return SSR_SAFE_DEFAULT;
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

export function useReducedMotion(): boolean {
  const [prefersReducedMotion, setPrefersReducedMotion] =
    useState(getPrefersReducedMotion);

  useEffect(() => {
    const mql = window.matchMedia("(prefers-reduced-motion: reduce)");

    function handleChange(e: MediaQueryListEvent) {
      setPrefersReducedMotion(e.matches);
    }

    mql.addEventListener("change", handleChange);
    return () => mql.removeEventListener("change", handleChange);
  }, []);

  return prefersReducedMotion;
}
```

**Key patterns:**
- SSR-safe: returns `false` on the server (assumes motion is OK)
- Lazy initializer: `useState(getPrefersReducedMotion)` avoids running on the server
- Live updates: listens for `change` events on the media query list
- Used by HeroKinetic, ScrollReveal, and any component with animations

---

## 9. Content Management (Static TypeScript Data)

All content is stored as typed TypeScript constants in `src/lib/`. No CMS, no MDX, no file-system routing. Data is imported directly by components.

### site-config.ts — Single Source of Truth

```typescript
import type { SiteConfig } from "./types";

export const siteConfig = {
  name: "Nicholas Yun",
  title: "Nicholas Yun — Software Engineer & Designer",
  email: "hello@nicholasyun.com",
  github: "nordeim",
  githubUrl: "https://github.com/nordeim",
  linkedin: "nicholasyun",
  linkedinUrl: "https://linkedin.com/in/nicholasyun",
  location: "New York",
  url: "https://nicholasyun.com",
} as const satisfies SiteConfig;

export function getSocialLinks(): ReadonlyArray<{
  readonly name: string;
  readonly url: string;
}> {
  return [
    { name: "GitHub", url: siteConfig.githubUrl },
    { name: "LinkedIn", url: siteConfig.linkedinUrl },
    { name: "Email", url: `mailto:${siteConfig.email}` },
  ];
}
```

**`as const satisfies SiteConfig`** — This is the critical pattern. `as const` narrows literal types, `satisfies SiteConfig` ensures the object matches the interface. Using `as const` alone would lose the type-checking guarantee. Using `satisfies` alone would widen the types.

### projects.ts, skills.ts, timeline.ts

These files export typed arrays of static data:

- `projects.ts` exports `Project[]` — used by `ProjectsSection` and `ProjectCard`
- `skills.ts` exports `Skill[]` — used by `SkillsSection`
- `timeline.ts` exports `TimelineEntry[]` — used by `Timeline`

All data types are defined in `src/lib/types.ts` and re-exported.

### Database (Optional)

The app runs without a database. The `db` export from `src/db/index.ts` can be `null`:

```typescript
// src/db/index.ts
export const db = createDb(); // Returns null if DATABASE_URL is not set
```

The analytics schema exists but is not actively written to:

```typescript
// src/db/schema.ts
export const analytics = pgTable("analytics", {
  id: uuid("id").primaryKey().defaultRandom(),
  path: text("path").notNull(),
  referrer: text("referrer"),
  userAgent: text("user_agent"),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
});
```

**Any code using `db` MUST include a null guard:**

```typescript
if (!db) {
  return Response.json({ ok: false, error: "Database not configured" }, { status: 503 });
}
```

---

## 10. Accessibility (WCAG AAA) Implementation

### Skip Link

```tsx
// layout.tsx
<a className="skip-link" href="#main-content">
  Skip to main content
</a>
```

The skip link is positioned off-screen until focused, then appears at the top of the page. It targets `#main-content` on the `<main>` element.

### Focus Styles

```css
*:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}
```

All interactive elements show a visible 2px gold outline on keyboard focus.

### Semantic HTML Structure

- `<html lang="en">` — Language declaration
- `<header role="banner">` — Navigation container
- `<main id="main-content" role="main">` — Primary content
- `<footer role="contentinfo">` — Footer
- `<nav aria-label="Main navigation">` — Navigation
- `<section id="..." aria-label="...">` — Each major section
- `<h1>` — Exactly one per page (in HeroKinetic)
- `<h2>` — Section headings (in SectionBlock)

### ARIA Attributes Used

| Component | Attribute | Purpose |
|-----------|-----------|---------|
| Navigation | `aria-label="Main navigation"` | Identifies nav landmark |
| Navigation links | `aria-current="page"` | Active link indicator |
| Mobile menu button | `aria-expanded`, `aria-controls` | Menu state |
| Mobile menu | `role="dialog"`, `aria-modal="true"` | Modal behavior |
| ThemeSwitch | `role="switch"`, `aria-checked` | Toggle semantics |
| ContactSection inputs | `aria-invalid`, `aria-describedby` | Validation state |
| Error messages | `role="alert"` | Live announcements |
| SectionSkeleton | `aria-hidden="true"` | Hidden from AT |
| Loading skeleton | `role="status"`, `aria-live="polite"` | Loading state |
| Terminal | `role="log"`, `aria-live="polite"` | Terminal output |
| Theme announcements | `aria-live="polite"`, `aria-atomic="true"` | Theme change |

### Keyboard Navigation

- **Tab** — Navigates between interactive elements
- **Enter/Space** — Activates nav links and buttons
- **Escape** — Closes mobile menu, returns focus to hamburger button
- **Focus trap** — Mobile menu traps Tab within its bounds
- **Hash navigation** — Focus moves to section heading after navigation

### Reduced Motion

```typescript
const prefersReducedMotion = useReducedMotion();

// In components:
const [isAnimated, setIsAnimated] = useState(prefersReducedMotion);
// When reduced motion is preferred, content appears immediately without animation
```

The global CSS also enforces reduced motion:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Contrast Ratios (Verified)

| Element | Night Theme | Day Theme |
|---------|-------------|-----------|
| text-muted on bg | 5.76:1 (AA) | 5.06:1 (AA) |
| text-primary on bg | ~17:1 (AAA) | ~14:1 (AAA) |
| accent on bg | ~10:1 (AAA) | ~5.5:1 (AA) |

### AccessibilityProvider — REMOVED

The `AccessibilityProvider` component was deleted in Remediation 6. It provided `prefersHighContrast` context which was never used by any component. `useReducedMotion` is the only accessibility hook that remains, and it's implemented as a standalone hook rather than a context provider.

---

## 11. Anti-Patterns & Common Bugs

### Bug: `instanceof Error` Doesn't Reliably Narrow `unknown` in TS Strict

In TypeScript strict mode, `instanceof Error` checks the prototype chain at runtime, but TypeScript's type narrowing doesn't always recognize this for `unknown` values, especially when the error comes from a different realm (iframe, worker) or is wrapped by a library.

```typescript
// UNRELIABLE
catch (err: unknown) {
  if (err instanceof Error) {
    // TypeScript might narrow, but runtime could fail in edge cases
  }
}

// RELIABLE — type guard function
function isErrorLike(err: unknown): err is { message: string } {
  return (
    typeof err === "object" &&
    err !== null &&
    "message" in err &&
    typeof (err as { message: unknown }).message === "string"
  );
}
```

This pattern is used in `error.tsx`:

```typescript
function isErrorLike(err: unknown): err is { message: string } {
  return (
    typeof err === "object" &&
    err !== null &&
    "message" in err &&
    typeof (err as { message: unknown }).message === "string"
  );
}
```

### Bug: `ssr: false` Was a Sledgehammer

The original `dynamic(() => import(...), { ssr: false })` on PortfolioApp was a blunt fix for hydration mismatches. It prevented SSR entirely, losing SEO benefits and initial load performance. The real fix was removing duplicate theme initialization and ensuring ThemeScript runs before hydration.

**Fixed in Remediation 7:** `ssr: false` removed. SSR is now enabled.

### Bug: Duplicate Theme Initialization

Previously, both ThemeScript and a `useEffect` in PortfolioApp tried to set `data-theme` on mount. This caused hydration mismatches because the server-rendered HTML didn't have `data-theme`, but the client-side effect ran before hydration completed.

**Fixed in Remediation 7:** Duplicate `useEffect` removed. ThemeScript is the single initialization point.

### Bug: `window.location.hash` Causes Scroll Jumps

Using `window.location.hash = "#about"` triggers the browser's default scroll-to-anchor behavior, which conflicts with the SPA layout where all sections are on one page.

**Fixed:** `history.pushState` replaces direct hash assignment. The `popstate` event listener handles back/forward navigation.

### Bug: Shared IP Fallback in Rate Limiting

Originally, `getClientIp()` fell back to `"127.0.0.1"` when no IP headers were found. This grouped ALL unknown-origin requests under the same rate limit key — an effective DoS vector.

**Fixed in Remediation 7:** `getClientIp()` returns `null` when IP is unknown. The `rateLimit()` function skips rate limiting when `identifier` is `null`.

### Bug: `document.getElementById` in React

Using `document.getElementById()` in React components bypasses React's reconciliation and can reference stale DOM nodes.

**Fixed in Remediation 7:** `useRef<HTMLDivElement>(null)` replaces `document.getElementById()` for the announcement element.

### Bug: `grid-column: span 2` Without Responsive Fallback

On narrow viewports where only one grid column fits, `span 2` items overflow or create layout issues.

**Fixed:** CSS class `.bento-span-2` collapses to `span 1` at `max-width: 640px`.

### Bug: `as const` Without `satisfies`

Using `as const` alone on `siteConfig` narrows the types to literal values but loses the guarantee that the object matches the `SiteConfig` interface. If a required field is missing, TypeScript won't catch it.

**Fixed in Remediation 7:** `as const satisfies SiteConfig` — both narrow types AND validate structure.

### Bug: `as` Type Casts on Unvalidated Input

Casting `JSON.parse()` results with `as ContactPayload` bypasses TypeScript's safety net. If the actual data doesn't match the interface, you get runtime errors with no compile-time warning.

**Fixed in Remediation 7:** `isContactPayload()` runtime type guard validates the shape before use.

### Bug: `setInterval` Without `clearInterval`

The original rate limiter used `setInterval` for periodic cleanup of stale entries. This interval was never cleared, creating a memory leak in long-running processes.

**Fixed in Remediation 5:** Replaced with lazy cleanup that runs on each rate limit check instead of on a timer.

### Bug: Error Messages Exposed in Production

The original error boundaries and API routes returned full error messages including stack traces in production.

**Fixed in Remediation 7:** Error messages are gated on `NODE_ENV`:

```typescript
const message = process.env.NODE_ENV === "production"
  ? "An unexpected error occurred."
  : error instanceof Error ? error.message : "An unknown error occurred";
```

### Bug: ESLint jsx-a11y Double Import

`eslint-config-next/core-web-vitals` already includes `eslint-plugin-jsx-a11y`. Importing it again causes `ConfigError: Cannot redefine plugin "jsx-a11y"`.

**Fixed in Remediation 5:** Removed the separate jsx-a11y import from `eslint.config.mjs`.

### Bug: `drizzle.config.json` With Hardcoded Credentials

The old `drizzle.config.json` contained hardcoded database credentials in the repository.

**Fixed in Remediation 7:** Replaced with `drizzle.config.ts` that reads from `process.env.DATABASE_URL`. The JSON file was deleted.

---

## 12. Debugging Guide

### Build Failures

**"optimizeFonts is not a valid config option"**
- Remove `optimizeFonts` from `next.config.ts`. It was removed in Next.js 16.

**"Cannot find module '@/components/PortfolioApp'"**
- PortfolioApp is in `src/app/PortfolioApp.tsx`, NOT `src/components/PortfolioApp.tsx`.
- Correct import: `import("@/app/PortfolioApp")`

**Tailwind CSS not applying styles**
- Verify `@import "tailwindcss"` is the FIRST line in `globals.css`.
- Verify `postcss.config.mjs` uses `@tailwindcss/postcss` (not `tailwindcss` directly).

**"Cannot redefine plugin 'jsx-a11y'"**
- Do NOT import `eslint-plugin-jsx-a11y` separately. It's included in `eslint-config-next/core-web-vitals`.

### Hydration Mismatches

**Theme flash on load**
- ThemeScript must be in `<head>` (in `layout.tsx`), not in a client component.
- Verify `<html suppressHydrationWarning>` is present.
- Verify no duplicate theme initialization `useEffect` in PortfolioApp.

**`ssr: false` temptation**
- Do NOT add `ssr: false` to dynamic imports to "fix" hydration mismatches.
- Fix the root cause instead (duplicate initialization, mismatched markup).

### Type Errors

**"Type 'unknown' is not assignable to type 'Error'"**
- `react-error-boundary` v4+ types `FallbackProps.error` as `unknown`.
- Use a type guard or `instanceof Error` check.

**"Object is possibly 'undefined'" with array access**
- `noUncheckedIndexedAccess: true` means `arr[0]` returns `T | undefined`.
- Always use `?.` or `??` with indexed access.

**"Property does not exist on type 'never'"**
- Usually caused by `as const` arrays. Use `(typeof ARRAY)[number]` for the element type.

### Runtime Errors

**"DATABASE_URL is not set"**
- This is expected if you haven't configured the database.
- The app runs fine without it — `db` will be `null`.

**Rate limiting not working**
- Verify reverse proxy sends `x-forwarded-for` headers.
- Without these headers, `getClientIp()` returns `null` and rate limiting is skipped.

**"Message recorded. Email delivery is not yet configured"**
- This is the honest response from the contact API. Email integration is a TODO.
- Check `EMAIL_API_KEY` in `.env.example` for future setup.

### Performance Issues

**Large bundle size**
- Verify below-fold components use `React.lazy()` + `Suspense`.
- Check that `_archive/` is excluded from the build in `tsconfig.json`.

**Slow initial paint**
- ThemeScript must be blocking in `<head>`.
- Google Fonts should use `display=swap` (already in the URL).
- Consider migrating to `next/font/google` to eliminate external font request.

---

## 13. Pre-Ship Checklist

### Before Every Deploy

- [ ] `npm run typecheck` passes with zero errors
- [ ] `npm run lint` passes with zero errors
- [ ] `npm run build` succeeds
- [ ] Both Night and Day themes render correctly
- [ ] Mobile menu opens/closes with keyboard (Tab, Escape)
- [ ] Skip link works (Tab from page start)
- [ ] Contact form validates all fields
- [ ] Contact form submits to `/api/contact`
- [ ] Rate limiting blocks after 5 requests/minute
- [ ] Hash navigation updates URL and focuses section
- [ ] Back/forward browser navigation syncs active section
- [ ] No console errors in production build
- [ ] CSP headers present (check via browser dev tools)
- [ ] No `'unsafe-eval'` in CSP `script-src`
- [ ] `X-Powered-By` header absent
- [ ] OG image loads at `/og-image.png`
- [ ] Structured data (LD+JSON) present in `<head>`
- [ ] `prefers-reduced-motion` disables animations
- [ ] All `aria-label` attributes are meaningful (not "click here")
- [ ] Focus outline visible on all interactive elements
- [ ] No hardcoded credentials in source code
- [ ] Error messages are generic in production (no stack traces)

### Before Major Changes

- [ ] Component count matches (16 active)
- [ ] No dormant code outside `_archive/`
- [ ] `siteConfig` values not duplicated in components
- [ ] Types are imported from `@/lib/types`, not redefined locally
- [ ] `_archive/` is in both `tsconfig.json` exclude and ESLint globalIgnores
- [ ] `skills/` directory is excluded from `tsconfig.json`
- [ ] No `as` type casts on unvalidated input
- [ ] No `document.getElementById` in React components
- [ ] No `setInterval` without cleanup
- [ ] No `ssr: false` on dynamic imports

---

## 14. Lessons Learnt & How to Avoid Them (ALL 52)

### Phase 1: Build-Breaking Issues

**Lesson 1: `instanceof Error` does not reliably narrow `unknown` in TypeScript Strict**
- **What happened:** Error boundaries used `instanceof Error` to narrow `unknown` error types, but TypeScript's strict mode doesn't guarantee this works across all contexts.
- **Fix:** Use explicit type guard functions like `isErrorLike()` that check `typeof`, `"message" in err`, etc.
- **Prevention:** Always write custom type guards for `unknown` error values. Never rely solely on `instanceof`.

**Lesson 2: `eslint-config-next` already bundles `eslint-plugin-jsx-a11y`**
- **What happened:** Adding `eslint-plugin-jsx-a11y` as a separate import caused `ConfigError: Cannot redefine plugin`.
- **Fix:** Use only `eslint-config-next/core-web-vitals` which includes jsx-a11y.
- **Prevention:** Check what plugins your ESLint config already includes before adding more.

**Lesson 3: `useEffect` should not synchronously call `setState`**
- **What happened:** Calling `setState` synchronously inside `useEffect` can cause layout thrashing and unexpected renders.
- **Fix:** Use `requestAnimationFrame` or functional updates. In the hero, animation is triggered via `requestAnimationFrame`.
- **Prevention:** Wrap state updates in effects with `requestAnimationFrame` when they trigger visual changes.

**Lesson 4: `history.pushState` replaces `window.location.hash` but requires `popstate` listener**
- **What happened:** Using `window.location.hash` caused scroll-to-anchor jumps. Switching to `pushState` fixed scrolling but broke back/forward navigation because only `hashchange` was being listened to.
- **Fix:** Use `popstate` event listener (not `hashchange`) with `pushState`.
- **Prevention:** When changing URL behavior, verify all navigation methods (click, back, forward, direct URL).

**Lesson 5: Stable keys for mutable lists (NOT `key={index}`)**
- **What happened:** Using array index as React keys caused incorrect re-ordering when list items changed.
- **Fix:** Use unique, stable identifiers (e.g., `project.id`, `entry.id`) as keys.
- **Prevention:** Always use domain-specific unique IDs as keys. Only use index keys for static, never-reordered lists.

**Lesson 6: Verify npm versions before pinning**
- **What happened:** Some pinned package versions didn't exist on the registry, causing `npm install` failures.
- **Fix:** Check `npm view <package>@<version>` before pinning. Use caret ranges (`^`) for flexibility.
- **Prevention:** Always verify version existence. Prefer caret ranges over exact pins unless there's a known incompatibility.

**Lesson 7: CSS import order is critical in Tailwind v4**
- **What happened:** Placing `@import url()` (Google Fonts) before `@import "tailwindcss"` in `globals.css` broke the entire design token system silently — all CSS variables became undefined.
- **Fix:** `@import "tailwindcss"` MUST be the first line. All other imports come after.
- **Prevention:** In Tailwind v4, always put `@import "tailwindcss"` first. The `@theme` block depends on it.

**Lesson 8: `optimizeFonts` is gone in Next.js 16**
- **What happened:** Adding `optimizeFonts: true` to `next.config.ts` caused a build error because the option was removed.
- **Fix:** Remove the option entirely. Font optimization is automatic in Next.js 16.
- **Prevention:** Check breaking changes when upgrading Next.js major versions. Don't copy config from older projects.

**Lesson 9: `ssr: false` requires `"use client"`**
- **What happened:** Using `ssr: false` in `next/dynamic()` without `"use client"` in the importing file caused errors.
- **Fix:** The page that uses `dynamic()` must have `"use client"` directive.
- **Prevention:** Remember that `ssr: false` is a client-only feature. The importing module must be a Client Component.

**Lesson 10: Two design token systems create technical debt**
- **What happened:** Having CSS variables in both `globals.css` and a JavaScript object created drift — values got out of sync.
- **Fix:** Eliminated the JS token object. All tokens live in `globals.css` `@theme` block only.
- **Prevention:** Single source of truth for design tokens. If you need them in JS, derive from CSS, don't duplicate.

### Phase 2: Type Consolidation

**Lesson 11: Null-safe database access**
- **What happened:** Code assumed `db` was always available, but without `DATABASE_URL`, it's `null`.
- **Fix:** Always guard with `if (!db) { return ... }`.
- **Prevention:** Treat database connections as optional. Always null-check before use.

**Lesson 12: `noUncheckedIndexedAccess` catches real bugs**
- **What happened:** Enabling this tsconfig option revealed multiple places where array access assumed non-undefined values.
- **Fix:** Added `?.` and `??` operators at all indexed access sites.
- **Prevention:** Always enable `noUncheckedIndexedAccess` in new projects. It catches real runtime bugs.

**Lesson 13: `react-error-boundary` v4+ changed `FallbackProps.error` to `unknown`**
- **What happened:** Code typed the error prop as `Error`, but v4 changed it to `unknown`. TypeScript flagged this.
- **Fix:** Accept `error: unknown` and use type guards to narrow.
- **Prevention:** Read changelogs when updating dependencies. This breaking change persists through v6.

**Lesson 14: `PortfolioApp.tsx` location matters (`src/app/` not `src/components/`)**
- **What happened:** Import paths referenced `@/components/PortfolioApp` but the file lives in `src/app/`.
- **Fix:** Import from `@/app/PortfolioApp`. The file must be in the app directory for Next.js routing.
- **Prevention:** Co-locate orchestrator components with their routes. Don't put route-level components in the generic components directory.

**Lesson 15: Undefined CSS variables silently fail**
- **What happened:** Misspelled CSS variable names (e.g., `--color-boder` instead of `--color-border`) rendered as empty strings with no error.
- **Fix:** Double-check variable names against the `@theme` block. Consider a CSS linting rule.
- **Prevention:** Use autocomplete or snippets for CSS variables. Test theme switching after any variable changes.

**Lesson 16: Centralize configuration early (`site-config.ts`)**
- **What happened:** Site name, email, and URLs were hardcoded in multiple components. Changing one required finding and updating all.
- **Fix:** Created `site-config.ts` with `as const satisfies SiteConfig`. All components import from here.
- **Prevention:** Create a centralized config file on day one. Use TypeScript to enforce its shape.

### Phase 3: Design Tokens, Routing, Architecture

**Lesson 17: Theme target must be consistent (`<html>` not `<body>`)**
- **What happened:** Some code set `data-theme` on `<html>`, some on `<body>`. Inconsistent targeting caused partial theme application.
- **Fix:** Always set `data-theme` on `document.documentElement` (the `<html>` element). Never use `<body>` or class-based switching.
- **Prevention:** Document the theme target in the skill file. Enforce with code review.

**Lesson 18: Hash routing section names must match actual IDs**
- **What happened:** `VALID_SECTIONS` array in `useRouteHash` didn't match the `id` attributes on `<section>` elements. Navigation to "about" failed because the section was "about-content".
- **Fix:** Section wrapper IDs and navigation hash IDs are separate. The `<section>` has `id="about"`, the inner div has `id="about-content"`.
- **Prevention:** Keep a mapping of section names to DOM IDs. Test every navigation link.

**Lesson 19: Rate limiting is essential for public API routes**
- **What happened:** The contact API had no rate limiting, making it vulnerable to spam and abuse.
- **Fix:** Implemented in-memory sliding window rate limiter with 5 req/min per IP.
- **Prevention:** Always add rate limiting to public API endpoints. Even a simple in-memory limiter is better than nothing.

**Lesson 20: Archiving dormant code reduces confusion**
- **What happened:** Unused components and data files in the main source tree caused import confusion and bloated the build.
- **Fix:** Moved dormant code to `_archive/` directories. Added these to `tsconfig.json` exclude and ESLint globalIgnores.
- **Prevention:** When removing features, move code to `_archive/` rather than deleting. This preserves history without polluting the active codebase.

### Phase 4: Accessibility, Security, Type Safety

**Lesson 21: Remediation docs may reference non-existent files**
- **What happened:** Remediation instructions referenced files that had been moved, renamed, or deleted in earlier phases. Following the instructions blindly caused errors.
- **Fix:** Always verify file paths before making changes. Use `ls` or file search.
- **Prevention:** Treat remediation docs as guides, not scripts. Validate every path.

**Lesson 22: Discriminated unions prevent type errors on API responses**
- **What happened:** Code accessed `response.error` without first checking `response.success`, causing TypeScript errors because the success shape doesn't have an `error` field.
- **Fix:** Use `ContactApiResponse = ContactApiSuccess | ContactApiError` discriminated union. Always check `success` first.
- **Prevention:** Model API responses as discriminated unions. Never access error fields without checking the discriminant.

**Lesson 23: Contrast ratios must be verified in both themes independently**
- **What happened:** Text that was readable in Night theme was too low-contrast in Day theme, or vice versa.
- **Fix:** Verified WCAG AA contrast ratios (4.5:1 minimum) for both themes. Night: 5.76:1, Day: 5.06:1.
- **Prevention:** Test contrast in BOTH themes after any color change. Use a contrast checker tool.

**Lesson 24: Remove unused features rather than leaving them half-implemented**
- **What happened:** The `AccessibilityProvider` component was imported but never used by any component. It added bundle size and confusion.
- **Fix:** Deleted `AccessibilityProvider` entirely in Remediation 6.
- **Prevention:** If a feature isn't used, remove it. Don't keep it "just in case."

**Lesson 25: Focus management is essential for keyboard navigation**
- **What happened:** After hash navigation, keyboard focus stayed on the clicked link instead of moving to the new section.
- **Fix:** Use `requestAnimationFrame` to find the section heading, set `tabindex="-1"`, and call `focus({ preventScroll: true })`.
- **Prevention:** Always manage focus after programmatic navigation. Test with keyboard only.

**Lesson 26: Never hardcode credentials in config files**
- **What happened:** `drizzle.config.json` contained database connection strings directly in the repository.
- **Fix:** Replaced with `drizzle.config.ts` reading from `process.env.DATABASE_URL`. Deleted the JSON file.
- **Prevention:** Use environment variables for all secrets. Add config files with credentials to `.gitignore`.

### Phase 5: Code Review Fixes

**Lesson 27: `instanceof Error` narrowing is unreliable across realms**
- **What happened:** (Reiteration with additional context) Errors caught in React error boundaries may not be `Error` instances if thrown from async boundaries or native APIs.
- **Fix:** Use structural type guards (`typeof err === "object" && "message" in err`).
- **Prevention:** Always use structural type guards for error handling in boundary code.

**Lesson 28: ESLint plugin duplication causes ConfigError**
- **What happened:** (Reiteration) Re-importing `eslint-plugin-jsx-a11y` alongside `eslint-config-next/core-web-vitals` failed with "Cannot redefine plugin".
- **Fix:** Use only the core-web-vitals config. Document the reason in comments.
- **Prevention:** Audit ESLint configs for plugin duplication. Read the source of extended configs.

**Lesson 29: Synchronous setState in useEffect causes layout thrashing**
- **What happened:** (Reiteration) Setting state synchronously in `useEffect` forces an immediate re-render before the browser has painted, causing visual flickering.
- **Fix:** Wrap in `requestAnimationFrame` or use `useLayoutEffect` only when truly necessary.
- **Prevention:** When an effect triggers visual changes, defer the state update to the next frame.

**Lesson 30: `history.pushState` replaces `location.hash` but requires event listening**
- **What happened:** (Reiteration with emphasis on event choice) Switching from `window.location.hash` to `history.pushState` fixed scroll jumping but broke back/forward because `hashchange` doesn't fire for `pushState`.
- **Fix:** Listen for `popstate` instead of `hashchange`.
- **Prevention:** When using History API, always pair `pushState` with `popstate` listener.

**Lesson 31: Use stable keys for mutable lists**
- **What happened:** (Reiteration) Terminal command history used index keys, causing incorrect rendering when history was modified.
- **Fix:** Used unique command IDs or content-based keys.
- **Prevention:** Never use index as key for lists that can be reordered, filtered, or modified.

**Lesson 32: Prior remediation "fixes" may be incomplete**
- **What happened:** Remediation 5 found issues that Remediations 1–4 claimed to fix but didn't fully address. For example, the CSP still had `'unsafe-eval'` after Remediation 4 said it was removed.
- **Fix:** Always verify each fix independently. Don't trust prior remediation status.
- **Prevention:** Test each fix. Write verification steps in remediation plans.

**Lesson 33: `ssr: false` is a sledgehammer for hydration mismatches**
- **What happened:** Using `ssr: false` on PortfolioApp's dynamic import disabled SSR entirely, losing SEO benefits and increasing time-to-interactive.
- **Fix:** Removed `ssr: false` in Remediation 7. Fixed the root cause (duplicate theme init).
- **Prevention:** Never use `ssr: false` as a quick fix. Find and fix the hydration mismatch root cause.

**Lesson 34: `'unsafe-eval'` in CSP is almost never needed**
- **What happened:** The original CSP included `'unsafe-eval'` in `script-src`, weakening the security posture.
- **Fix:** Removed `'unsafe-eval'`. The app works fine without it.
- **Prevention:** Only add `'unsafe-eval'` if a specific library requires it (e.g., some older templating engines). Modern React/Next.js does not need it.

**Lesson 35: API responses that claim success without delivering are deceptive**
- **What happened:** The contact API returned "Message sent successfully!" even though email delivery was not configured. Users thought their messages were delivered.
- **Fix:** Changed response to "Message recorded. Email delivery is not yet configured — your message has been logged server-side."
- **Prevention:** Never claim an action succeeded if it didn't. Honest error messages build trust.

**Lesson 36: `as` type casts bypass TypeScript's safety net**
- **What happened:** The contact API used `body as ContactPayload` to cast the parsed JSON. If the request body had unexpected fields or missing fields, the cast would silently pass.
- **Fix:** Created `isContactPayload()` runtime type guard that validates the shape before use.
- **Prevention:** Use runtime type guards for all untrusted input. Reserve `as` for cases where you have external proof of the type.

### Phase 6: Full Codebase Alignment

**Lesson 37: Shared IP fallback in rate limiting is a DoS vector**
- **What happened:** `getClientIp()` fell back to `"127.0.0.1"` when no IP headers were found. All requests without proxy headers shared the same rate limit bucket, allowing an attacker to exhaust the limit for all such requests.
- **Fix:** `getClientIp()` returns `null` when IP is unknown. `rateLimit()` skips limiting when identifier is `null`.
- **Prevention:** Never group unknown-origin requests under a shared identifier. It's better to skip rate limiting than to create a shared bucket.

**Lesson 38: `setInterval` without `clearInterval` is a memory leak**
- **What happened:** The rate limiter used `setInterval` for periodic cleanup but never cleared the interval. In serverless environments with cold starts, this accumulated timers.
- **Fix:** Replaced with lazy cleanup that runs on each rate limit check.
- **Prevention:** Always clean up intervals. Or better, use lazy cleanup patterns instead of periodic timers.

**Lesson 39: Duplicate theme initialization causes hydration mismatches**
- **What happened:** Both ThemeScript and a `useEffect` in PortfolioApp set `data-theme` on mount. The `useEffect` ran after hydration, causing a visible flash.
- **Fix:** Removed the duplicate `useEffect`. ThemeScript is now the single initialization point.
- **Prevention:** Document the initialization flow. Ensure only one code path sets initial theme.

**Lesson 40: `document.getElementById` in React should use `useRef`**
- **What happened:** PortfolioApp used `document.getElementById()` to find the announcement element for screen readers. This bypasses React's reconciliation.
- **Fix:** Replaced with `useRef<HTMLDivElement>(null)`.
- **Prevention:** Always use React refs for DOM references in components. Never use `document.getElementById` or `document.querySelector`.

### Phase 7: Critical + High Security & Quality

**Lesson 41: `grid-column: span 2` needs responsive fallback**
- **What happened:** BentoGrid items with `grid-column: span 2` overflowed on narrow viewports where only one column fit.
- **Fix:** Created `.bento-span-2` CSS class that collapses to `span 1` at `max-width: 640px`.
- **Prevention:** Always add responsive fallbacks for multi-column span. Test at narrow widths.

**Lesson 42: `as const` without `satisfies` loses type checking**
- **What happened:** Using `as const` on `siteConfig` narrowed the types but didn't validate that all required fields were present. If a field was missing, TypeScript wouldn't catch it.
- **Fix:** Changed to `as const satisfies SiteConfig` — narrows types AND validates structure.
- **Prevention:** Always pair `as const` with `satisfies` for configuration objects.

**Lesson 43: Error messages must be gated on `NODE_ENV`**
- **What happened:** Error boundaries and API routes exposed internal error details (stack traces, query text) in production.
- **Fix:** All error messages check `process.env.NODE_ENV === "production"` before revealing details.
- **Prevention:** Never expose internal errors in production. Always gate on environment.

**Lesson 44: Centralize type definitions to prevent drift**
- **What happened:** Types were defined in multiple files, leading to inconsistencies (e.g., `NavLink` defined in both `types.ts` and `Navigation.tsx`).
- **Fix:** All shared types live in `src/lib/types.ts`. Components import from there.
- **Prevention:** Define types once, import everywhere. Use re-exports if needed.

**Lesson 45: `tsconfig.json` include patterns must be scoped narrowly**
- **What happened:** Broad include patterns pulled in the `skills/` directory (61MB) and `_archive/` code, slowing type-checking.
- **Fix:** Added `skills` and `src/**/_archive` to `exclude`.
- **Prevention:** Scope include patterns narrowly. Exclude large directories that aren't part of the build.

**Lesson 46: npm overrides can fix transitive dependency vulnerabilities**
- **What happened:** Transitive dependencies (`esbuild`, `postcss`) had known vulnerabilities in their default versions.
- **Fix:** Added `overrides` in `package.json` to enforce minimum versions.
- **Prevention:** Run `npm audit` regularly. Use `overrides` to patch transitive dependencies when maintainers are slow.

**Lesson 47: GEMINI.md must be kept in sync with other agent docs**
- **What happened:** `GEMINI.md` fell out of sync with `CLAUDE.md` and `AGENTS.md`, leading to inconsistent instructions for different AI agents.
- **Fix:** Rewrote `GEMINI.md` to align with the other docs.
- **Prevention:** When updating agent instructions, update ALL instruction files simultaneously.

**Lesson 48: License field consistency matters**
- **What happened:** `package.json` said "MIT" but the README had no license section, and some docs implied proprietary terms.
- **Fix:** Standardized to MIT across all files.
- **Prevention:** Choose a license early and declare it consistently everywhere.

**Lesson 49: `react-error-boundary` v6+ still has `unknown` error type from v4**
- **What happened:** Some documentation claimed the error type reverted to `Error` in v6. It didn't — the `unknown` type from v4 persists.
- **Fix:** Updated documentation to reflect that `error: unknown` is permanent from v4 onward.
- **Prevention:** Verify type changes in the actual library code, not just release notes.

**Lesson 50: Component counts must be audited after each remediation**
- **What happened:** After Remediation 6 deleted `AccessibilityProvider`, the documentation still listed 17 components. The actual count is 16.
- **Fix:** Audited all component files and updated documentation.
- **Prevention:** After any remediation that adds/removes files, recount components and update all documentation.

**Lesson 51: Don't Trust Documentation Over Code**
- **What happened:** After multiple remediation cycles, documentation was consistently out of date. Remediation reports referenced files that had been moved, renamed, or deleted in earlier phases.
- **Fix:** Always verify file paths against the actual codebase before making changes. Use `ls` or file search.
- **Prevention:** Treat documentation as a guide, not a script. Validate every path. Documentation describes what *should* be; the code shows what *is*. Cross-reference every finding against actual file contents before making changes.

**Lesson 52: Remediation Reports May Reference Non-Existent Files**
- **What happened:** Remediation reports written without access to the actual codebase referenced files that don't exist. Following the instructions blindly caused errors.
- **Fix:** Always validate each proposal against the real file structure before applying changes.
- **Prevention:** Read ALL documentation files before touching code. Verify every file path. Never blindly apply fixes for files that don't exist.

---

## 15. Pitfalls to Avoid

### Architecture Pitfalls

1. **Don't put route-level components in `src/components/`** — PortfolioApp belongs in `src/app/`. The dynamic import `import("@/app/PortfolioApp")` will fail if the file is elsewhere.

2. **Don't use `ssr: false` to fix hydration issues** — It's a sledgehammer that loses SSR benefits. Fix the root cause instead (duplicate initialization, mismatched markup).

3. **Don't create two design token systems** — CSS variables in `globals.css` and a JS object will drift. Use one source of truth (CSS).

4. **Don't skip rate limiting on public APIs** — Even a simple in-memory limiter prevents abuse. Production deployments should use Redis/Upstash.

5. **Don't use `document.getElementById` in React components** — Always use `useRef` for DOM references.

### Type Safety Pitfalls

6. **Don't use `as` type casts on unvalidated input** — Use runtime type guards (`isContactPayload()`) instead.

7. **Don't type `react-error-boundary`'s error prop as `Error`** — It's `unknown` from v4 onward.

8. **Don't use `as const` without `satisfies`** — You lose structural validation.

9. **Don't access `ContactApiResponse.error` without checking `success`** — The discriminated union prevents this at compile time, but only if you check the discriminant first.

10. **Don't forget `noUncheckedIndexedAccess`** — Array access returns `T | undefined`. Always handle the undefined case.

### CSS/Styling Pitfalls

11. **Don't put anything before `@import "tailwindcss"`** — In Tailwind v4, this must be the first line of `globals.css`.

12. **Don't use Tailwind utility classes for component styling** — This project uses inline `style={{}}` with CSS variables. Mixing approaches creates confusion.

13. **Don't use `border-radius`** — Brutalist design rule. Zero exceptions unless explicitly requested.

14. **Don't use `grid-column: span 2` without a responsive fallback** — Add a CSS class that collapses at narrow widths.

15. **Don't use class-based theme switching** — Theme is `data-theme` attribute on `<html>`, not a class on `<body>`.

### Security Pitfalls

16. **Don't include `'unsafe-eval'` in CSP `script-src`** — Modern Next.js doesn't need it.

17. **Don't fall back to a shared IP in rate limiting** — Return `null` instead and skip limiting for that request.

18. **Don't hardcode credentials in config files** — Use environment variables. Add config files with secrets to `.gitignore`.

19. **Don't expose internal error details in production** — Gate on `NODE_ENV`.

20. **Don't use `drizzle.config.json`** — Use `drizzle.config.ts` with `process.env.DATABASE_URL`.

### Process Pitfalls

21. **Don't trust remediation docs without validating paths** — Files may have been moved or deleted in prior phases.

22. **Don't let `_archive/` code trigger ESLint errors** — Add `**/_archive/**` to ESLint `globalIgnores`.

23. **Don't let agent instruction files fall out of sync** — Update all docs (CLAUDE.md, GEMINI.md, AGENTS.md) simultaneously.

24. **Don't version-control large binary archives** — Remove `skills-backup.tar.gz` (40MB) and similar files from git.

25. **Don't count components without auditing actual files** — Verify the count after every remediation.

---

## 16. Best Practices

### Architecture Best Practices

1. **Single source of truth for site configuration** — `site-config.ts` with `as const satisfies SiteConfig`. Import everywhere, never hardcode.

2. **Centralized types** — All shared TypeScript interfaces in `src/lib/types.ts`. Components import from here, not redefine locally.

3. **Lazy loading for below-fold content** — Use `React.lazy()` + `<Suspense>` for sections that aren't visible on initial load.

4. **Two-level error boundaries** — Page-level `react-error-boundary` + section-level custom `ErrorBoundary`. Sections fail gracefully without taking down the entire page.

5. **Discriminated unions for API responses** — `ContactApiResponse = ContactApiSuccess | ContactApiError`. Check `success` discriminant before accessing shape-specific fields.

6. **Archive dormant code** — Move to `_archive/` directories. Exclude from `tsconfig.json` and ESLint. This preserves history without polluting the build.

### Accessibility Best Practices

7. **Skip link** — Every page should have a skip link as the first focusable element.

8. **Focus management after navigation** — Move focus to the target section heading. Use `tabindex="-1"` + `focus({ preventScroll: true })`.

9. **ARIA attributes** — Use `role`, `aria-label`, `aria-current`, `aria-invalid`, `aria-describedby`, `aria-expanded`, `aria-controls`, `aria-live` appropriately. Don't over-ARIA — only add what's needed.

10. **Reduced motion support** — Check `prefers-reduced-motion` and disable animations when active. Provide immediate state instead of animated transitions.

11. **Keyboard navigation** — All interactive elements must be keyboard-accessible. Use focus traps for modals. Close on Escape.

### Security Best Practices

12. **Security headers** — Apply to all routes via `next.config.ts` `headers()` function. Include CSP, HSTS, X-Frame-Options, etc.

13. **Rate limiting** — Essential for public API routes. Use sliding window algorithm. Return 429 with `Retry-After` header.

14. **Input validation** — Validate on both client and server. Use runtime type guards on the server. Never trust client-side validation alone.

15. **Body size limits** — Reject oversized payloads before parsing. The contact API uses 10KB limit.

16. **Honest API responses** — Don't claim success when the action wasn't completed. If email isn't configured, say so.

17. **Environment-gated error messages** — Production errors should be generic. Development can show details.

### Performance Best Practices

18. **Inline styles with CSS variables** — Avoids CSS class generation overhead. CSS variables are resolved at paint time.

19. **`will-change` optimization** — Use `will-change: auto` after animation completes to free GPU resources. (See ScrollReveal.)

20. **Image optimization** — Use `next/image` for automatic optimization. Configure `formats: ["image/avif", "image/webp"]` in `next.config.ts`.

21. **Font loading** — Use `display=swap` in Google Fonts URL to prevent FOIT. Consider migrating to `next/font/google` for zero-layout-shift loading.

### Code Quality Best Practices

22. **`as const satisfies`** — Use for configuration objects. Gets both literal types and structural validation.

23. **Runtime type guards** — For all untrusted input (API request bodies, external data). Replace `as` casts.

24. **Null guards for database** — Always check `if (!db)` before using. The database is optional.

25. **Functional state updates** — Use `setErrors(prev => ...)` instead of reading state directly in callbacks. Prevents stale closure bugs.

---

## 17. Coding Patterns

### Pattern: Inline Style Objects with CSS Variables

```typescript
const containerStyle: CSSProperties = {
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  minHeight: "100vh",
  padding: "var(--spacing-double) var(--spacing-grid)",
  position: "relative",
  overflow: "hidden",
};

return <section style={containerStyle}>...</section>;
```

**Why:** This project does NOT use Tailwind utility classes in JSX. All styling is through inline `style={{}}` objects referencing CSS custom properties. This gives type safety, avoids class name collisions, and makes component styling self-contained.

### Pattern: Conditional Style Merging

```typescript
const inputStyle = {
  width: "100%",
  padding: "var(--spacing-half)",
  border: "2px solid var(--color-border)",
  background: "var(--color-surface)",
  // ...
};

const errorInputStyle = {
  ...inputStyle,
  borderColor: "var(--color-error, #c0392b)",
};

// Usage:
<input style={errors.name ? errorInputStyle : inputStyle} />
```

### Pattern: `as const` for Text Content

```typescript
const HEADLINE_LINES = [
  "The Engineered",
  "Soul",
] as const;
```

This creates a readonly tuple type, ensuring the map callback receives literal string types.

### Pattern: Lazy Functional Initializer

```typescript
const [activeSection, setActiveSectionState] = useState<string>(
  getHashFromWindow  // Function reference, not function call
);
```

Passing a function reference to `useState` makes it a lazy initializer — it only runs on the first render, not on every re-render.

### Pattern: useCallback with Functional Update

```typescript
const toggleTheme = useCallback(() => {
  setTheme((prev) => {
    const next = prev === "day" ? "night" : "day";
    onThemeChange(next);
    return next;
  });
}, [onThemeChange]);
```

Using the functional update form of `setTheme` avoids stale closures over the `theme` variable.

### Pattern: Error State with Functional Update

```typescript
const handleChange = useCallback(
  (field: keyof FormData) =>
    (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
      setFormData((prev) => ({ ...prev, [field]: e.target.value }));
      setErrors((prev) => {
        if (prev[field]) {
          return { ...prev, [field]: undefined };
        }
        return prev;
      });
    },
  [],
);
```

Clears the error for a field when the user starts typing, using functional update to avoid stale state.

### Pattern: Discriminated Union for API Responses

```typescript
interface ContactApiSuccess {
  success: true;
  message: string;
}

interface ContactApiError {
  success: false;
  error: string;
  retryAfter?: number;
}

export type ContactApiResponse = ContactApiSuccess | ContactApiError;
```

The `success` field is the discriminant. After checking `if (data.success)`, TypeScript narrows the type to `ContactApiSuccess`. Otherwise, it narrows to `ContactApiError`.

### Pattern: Runtime Type Guard for API Input

```typescript
function isContactPayload(obj: unknown): obj is ContactPayload {
  if (typeof obj !== "object" || obj === null) return false;
  const record = obj as Record<string, unknown>;
  if ("name" in record && typeof record.name !== "string" && record.name !== undefined) return false;
  if ("email" in record && typeof record.email !== "string" && record.email !== undefined) return false;
  if ("message" in record && typeof record.message !== "string" && record.message !== undefined) return false;
  return true;
}
```

This validates the shape of the parsed JSON body before using it as `ContactPayload`. It replaces the unsafe `body as ContactPayload` cast.

### Pattern: Configuration with `as const satisfies`

```typescript
export const siteConfig = {
  name: "Nicholas Yun",
  title: "Nicholas Yun — Software Engineer & Designer",
  email: "hello@nicholasyun.com",
  // ...
} as const satisfies SiteConfig;
```

- `as const` narrows `"Nicholas Yun"` to the literal type (not just `string`)
- `satisfies SiteConfig` validates the object matches the interface
- Together: literal types AND structural validation

### Pattern: Null-Safe Database Access

```typescript
export async function GET() {
  try {
    if (!db) {
      return Response.json(
        { ok: false, error: "Database not configured" },
        { status: 503 }
      );
    }
    await db.execute(sql`select 1`);
    return Response.json({ ok: true });
  } catch {
    return Response.json({ ok: false }, { status: 500 });
  }
}
```

### Pattern: Focus Trap for Modal

```typescript
const handleTabKey = (e: globalThis.KeyboardEvent) => {
  if (e.key !== "Tab" || focusable.length === 0) return;

  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  if (e.shiftKey && document.activeElement === first) {
    e.preventDefault();
    last?.focus();
  } else if (!e.shiftKey && document.activeElement === last) {
    e.preventDefault();
    first?.focus();
  }
};
```

### Pattern: Reduced Motion Check

```typescript
const prefersReducedMotion = useReducedMotion();
const [isAnimated, setIsAnimated] = useState(prefersReducedMotion);

useEffect(() => {
  if (!prefersReducedMotion) {
    const timer = requestAnimationFrame(() => {
      setIsAnimated(true);
    });
    return () => cancelAnimationFrame(timer);
  }
}, [prefersReducedMotion]);
```

When reduced motion is preferred, content appears immediately. Otherwise, animation triggers after mount via `requestAnimationFrame`.

### Pattern: Environment-Gated Error Messages

```typescript
const errorMessage =
  process.env.NODE_ENV === "production"
    ? "An unexpected error occurred. Please try again."
    : typeof error === "string"
      ? error
      : isErrorLike(error)
        ? error.message
        : "An unexpected error occurred. Please try again.";
```

### Pattern: Announcement via React Ref (Not getElementById)

```typescript
const announcementRef = useRef<HTMLDivElement>(null);

const handleThemeChange = useCallback((theme: "day" | "night") => {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("theme", theme);

  if (announcementRef.current) {
    announcementRef.current.textContent = `Switched to ${theme} theme`;
  }
}, []);

// In JSX:
<div
  ref={announcementRef}
  aria-live="polite"
  aria-atomic="true"
  className="sr-only"
/>
```

### Pattern: IntersectionObserver with Cleanup

```typescript
useEffect(() => {
  const el = ref.current;
  if (!el || prefersReducedMotion) return;

  const observer = new IntersectionObserver(
    (entries) => {
      const entry = entries[0];
      if (entry?.isIntersecting) {
        setIsVisible(true);
        observer.unobserve(el);
      }
    },
    { threshold },
  );

  observer.observe(el);

  return () => {
    observer.unobserve(el);
  };
}, [threshold, prefersReducedMotion]);
```

Observer is created, observes, and unobserves on cleanup. `unobserve` is also called when the element intersects (one-shot reveal).

---

## 18. Coding Anti-Patterns

### Anti-Pattern: Using `as` Type Casts on Unvalidated Input

```typescript
// BAD — bypasses TypeScript's safety net
const data = body as ContactPayload;

// GOOD — runtime type guard
if (!isContactPayload(body)) {
  return Response.json({ success: false, error: "Invalid payload" }, { status: 400 });
}
const data = body; // Now safely narrowed
```

### Anti-Pattern: `document.getElementById` in React

```typescript
// BAD — bypasses React's reconciliation
const el = document.getElementById("announcements");
el.textContent = "Switched to night theme";

// GOOD — React ref
const announcementRef = useRef<HTMLDivElement>(null);
if (announcementRef.current) {
  announcementRef.current.textContent = "Switched to night theme";
}
```

### Anti-Pattern: Shared IP Fallback in Rate Limiting

```typescript
// BAD — all unknown-origin requests share the same bucket
const ip = getClientIp(request) || "127.0.0.1";

// GOOD — skip rate limiting when IP is unknown
const ip = getClientIp(request);
if (!ip) {
  return { success: true, remaining: config.maxRequests };
}
```

### Anti-Pattern: `setInterval` Without Cleanup

```typescript
// BAD — memory leak in serverless environments
setInterval(() => {
  cleanupStaleEntries();
}, 300_000);

// GOOD — lazy cleanup on each request
function cleanupStaleEntries(): void {
  const now = Date.now();
  if (now - lastCleanup < CLEANUP_INTERVAL_MS) return;
  lastCleanup = now;
  // ... cleanup logic
}
```

### Anti-Pattern: Duplicate Theme Initialization

```typescript
// BAD — both ThemeScript and useEffect set data-theme
useEffect(() => {
  const stored = localStorage.getItem("theme");
  document.documentElement.setAttribute("data-theme", stored || "night");
}, []);

// GOOD — ThemeScript handles initialization, PortfolioApp only handles changes
const handleThemeChange = useCallback((theme: "day" | "night") => {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("theme", theme);
}, []);
```

### Anti-Pattern: `window.location.hash` for SPA Navigation

```typescript
// BAD — triggers scroll-to-anchor
window.location.hash = "#about";

// GOOD — pushState avoids scroll
window.history.pushState(null, "", "#about");
```

### Anti-Pattern: `as const` Without `satisfies`

```typescript
// BAD — no structural validation
export const siteConfig = {
  name: "Nicholas Yun",
  // What if 'email' is missing? TypeScript won't catch it.
} as const;

// GOOD — validates structure AND narrows types
export const siteConfig = {
  name: "Nicholas Yun",
  email: "hello@nicholasyun.com",
  // ...
} as const satisfies SiteConfig;
```

### Anti-Pattern: `grid-column: span 2` Without Responsive Fallback

```typescript
// BAD — overflows on narrow viewports
style={{ gridColumn: "span 2" }}

// GOOD — CSS class with responsive collapse
className="bento-span-2"
/* CSS: .bento-span-2 { grid-column: span 2; }
   @media (max-width: 640px) { .bento-span-2 { grid-column: span 1; } } */
```

### Anti-Pattern: Class-Based Theme Switching

```typescript
// BAD — theme via CSS class
document.body.classList.add("theme-night");

// GOOD — data-theme attribute on <html>
document.documentElement.setAttribute("data-theme", "night");
```

### Anti-Pattern: Setting `data-theme` on `<body>`

```typescript
// BAD — inconsistent with CSS selectors
document.body.setAttribute("data-theme", "night");

// GOOD — CSS uses [data-theme="day"] on html
document.documentElement.setAttribute("data-theme", "night");
```

### Anti-Pattern: Calling `setState` Synchronously in `useEffect`

```typescript
// BAD — causes synchronous re-render before paint
useEffect(() => {
  setIsAnimated(true);
}, []);

// GOOD — defer to next frame
useEffect(() => {
  const timer = requestAnimationFrame(() => {
    setIsAnimated(true);
  });
  return () => cancelAnimationFrame(timer);
}, []);
```

### Anti-Pattern: Deceptive API Success Messages

```typescript
// BAD — claims success without delivering
return Response.json({ success: true, message: "Message sent successfully!" });

// GOOD — honest about limitations
return Response.json({
  success: true,
  message: "Message recorded. Email delivery is not yet configured — your message has been logged server-side.",
});
```

### Anti-Pattern: Exposing Internal Errors in Production

```typescript
// BAD — leaks implementation details
return Response.json({ error: error.message, stack: error.stack });

// GOOD — generic message in production
const message = process.env.NODE_ENV === "production"
  ? "An unexpected error occurred."
  : error instanceof Error ? error.message : "Unknown error";
```

### Anti-Pattern: Hardcoding Site Config in Components

```typescript
// BAD — scattered configuration
<footer>Email: hello@nicholasyun.com</footer>

// GOOD — centralized config
import { siteConfig } from "@/lib/site-config";
<footer>Email: {siteConfig.email}</footer>
```

### Anti-Pattern: Using `index` as React Key for Mutable Lists

```typescript
// BAD — incorrect re-ordering on mutations
{items.map((item, index) => <Item key={index} />)}

// GOOD — stable unique keys
{items.map((item) => <Item key={item.id} />)}
```

---

## 19. Responsive Breakpoint Reference

### Navigation Breakpoint

```css
@media (max-width: 768px) {
  .nav-links-desktop {
    display: none !important;
  }
  .mobile-menu-button {
    display: block !important;
  }
}
```

- **≤768px:** Desktop nav links hidden, mobile hamburger button shown
- **>768px:** Desktop nav links visible, mobile button hidden

### BentoGrid Span-2 Collapse

```css
.bento-span-2 {
  grid-column: span 2;
}
@media (max-width: 640px) {
  .bento-span-2 {
    grid-column: span 1;
  }
}
```

- **≤640px:** Span-2 items collapse to span 1 (single column)
- **>640px:** Span-2 items occupy two columns

### Grid Layouts

All grid layouts use CSS `auto-fit` with `minmax`:

```typescript
style={{
  display: "grid",
  gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
  gap: "var(--spacing-grid)",
}}
```

This creates responsive grids that automatically adjust column count based on available width.

### Hero Typography

```typescript
fontSize: "clamp(3rem, 10vw, 8rem)"
```

Uses CSS `clamp()` for fluid typography that scales between 3rem and 8rem based on viewport width.

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Summary Table

| Breakpoint | Affects |
|------------|---------|
| ≤640px | BentoGrid span-2 collapse |
| ≤768px | Navigation mobile menu |
| All widths | Auto-fit grids, fluid typography, reduced motion |

---

## 20. Z-Index Layer Map

### Defined Values (from globals.css @theme)

| Token | Value | Purpose |
|-------|-------|---------|
| `--z-index-grain` | 50 | Grain/grid overlay textures |
| `--z-index-machine` | 40 | Machine overlay (archived) |
| `--z-index-mobile-backdrop` | 45 | Mobile menu backdrop |
| `--z-index-mobile-drawer` | 46 | Mobile menu drawer |
| `--z-index-skip-link` | 100 | Skip to content link |
| `--z-index-loader` | 60 | Full-page loader |

### Component-Specific Z-Index Values

| Component | Value | Set In |
|-----------|-------|--------|
| Navigation (sticky) | 100 | Inline style |
| Mobile menu overlay | 99 | Inline style |
| Skip link | `var(--z-index-skip-link)` = 100 | CSS class |

### Layering Order (bottom to top)

```
1. Normal document flow (z-index: auto)
2. Machine overlay (z-index: 40) — archived
3. Mobile backdrop (z-index: 45)
4. Mobile drawer (z-index: 46)
5. Grain/grid overlay (z-index: 50)
6. Full-page loader (z-index: 60)
7. Navigation (z-index: 100)
8. Skip link (z-index: 100)
```

**Note:** Navigation and skip link share z-index: 100. The skip link appears above navigation via CSS positioning (absolute vs sticky) and DOM order.

---

## 21. Color Reference (Complete)

### Night Theme (Default)

| Token | Hex | RGB | Usage |
|-------|-----|-----|-------|
| `--color-bg` | `#0a0a0a` | rgb(10,10,10) | Page background |
| `--color-bg-soft` | `#111111` | rgb(17,17,17) | Card inner background |
| `--color-bg-sunken` | `#070707` | rgb(7,7,7) | Inset/sunken elements |
| `--color-bg-elevated` | `#222222` | rgb(34,34,34) | Elevated surfaces |
| `--color-surface` | `#1a1a1a` | rgb(26,26,26) | Cards, panels |
| `--color-border` | `#222222` | rgb(34,34,34) | Standard borders |
| `--color-border-strong` | `#333333` | rgb(51,51,51) | Emphasized borders, shadow offset |
| `--color-border-subtle` | `#1a1a1a` | rgb(26,26,26) | Subtle dividers |
| `--color-text-primary` | `#f0ece4` | rgb(240,236,228) | Headings, body text |
| `--color-text-secondary` | `#a8a29e` | rgb(168,162,158) | Secondary text, descriptions |
| `--color-text-muted` | `#918983` | rgb(145,137,131) | Muted labels, captions (WCAG AA 5.76:1) |
| `--color-text-inverse` | `#0a0a0a` | rgb(10,10,10) | Text on accent backgrounds |
| `--color-accent` | `#e8c547` | rgb(232,197,71) | Primary accent, active states |
| `--color-accent-hover` | `#f0d060` | rgb(240,208,96) | Accent hover state |
| `--color-accent-muted` | `#e8c54733` | — | Accent with 20% opacity |
| `--color-accent-subtle` | `#e8c5471a` | — | Accent with 10% opacity |
| `--color-error` | `#c0392b` | rgb(192,57,43) | Error states, validation |

### Day Theme

| Token | Hex | RGB | Usage |
|-------|-----|-----|-------|
| `--color-bg` | `#f5f0e8` | rgb(245,240,232) | Page background |
| `--color-bg-soft` | `#ede8df` | rgb(237,232,223) | Card inner background |
| `--color-bg-sunken` | `#ece7dd` | rgb(236,231,221) | Inset/sunken elements |
| `--color-bg-elevated` | `#faf6ef` | rgb(250,246,239) | Elevated surfaces |
| `--color-surface` | `#e5e0d6` | rgb(229,224,214) | Cards, panels |
| `--color-border` | `#d5cfc4` | rgb(213,207,196) | Standard borders |
| `--color-border-strong` | `#b8b0a2` | rgb(184,176,162) | Emphasized borders, shadow offset |
| `--color-border-subtle` | `#e5e0d6` | rgb(229,224,214) | Subtle dividers |
| `--color-text-primary` | `#1a1612` | rgb(26,22,18) | Headings, body text |
| `--color-text-secondary` | `#5c5650` | rgb(92,86,80) | Secondary text, descriptions |
| `--color-text-muted` | `#6b6560` | rgb(107,101,96) | Muted labels, captions (WCAG AA 5.06:1) |
| `--color-text-inverse` | `#f5f0e8` | rgb(245,240,232) | Text on accent backgrounds |
| `--color-accent` | `#b8860b` | rgb(184,134,11) | Primary accent (dark gold) |
| `--color-accent-hover` | `#996f08` | rgb(153,111,8) | Accent hover state |
| `--color-accent-muted` | `#b8860b22` | — | Accent with 13% opacity |
| `--color-accent-subtle` | `#b8860b1a` | — | Accent with 10% opacity |
| `--color-error` | `#a93226` | rgb(169,50,38) | Error states, validation |

### Theme Color Mapping

| Role | Night | Day |
|------|-------|-----|
| Background | #0a0a0a | #f5f0e8 |
| Text | #f0ece4 | #1a1612 |
| Accent | #e8c547 (gold) | #b8860b (dark gold) |
| Error | #c0392b | #a93226 |

### Viewport Meta Theme Color

```typescript
export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: [
    { media: "(prefers-color-scheme: dark)", color: "#0a0a0a" },
    { media: "(prefers-color-scheme: light)", color: "#f5f0e8" },
  ],
};
```

---

## 22. The Complete TypeScript Interface Reference

All types are centralized in `src/lib/types.ts`.

### Navigation Types

```typescript
export interface NavLink {
  label: string;
  href: string;
}
```

Used by: `Navigation.tsx` (note: Navigation also defines a local readonly `NavLink` interface for its own nav links — this is intentional as the navigation links are static and component-scoped).

### Social Link Types

```typescript
export interface SocialLink {
  platform: string;
  url: string;
  icon?: string;
}
```

### Site Configuration

```typescript
export interface SiteConfig {
  name: string;
  title: string;
  email: string;
  github: string;
  githubUrl: string;
  linkedin: string;
  linkedinUrl: string;
  location: string;
  url: string;
}
```

Validated by: `site-config.ts` via `as const satisfies SiteConfig`.

### Project Types

```typescript
export interface ProjectLink {
  live?: string;
  repo?: string;
}

export type ProjectCategory =
  | "full-stack"
  | "frontend"
  | "systems"
  | "research"
  | "tool"
  | "design"
  | "other";

export interface Project {
  id: string;
  title: string;
  description: string;
  role: string;
  period: string;
  category: ProjectCategory;
  tech: readonly string[];
  links: ProjectLink;
  image?: string;
  featured?: boolean;
}
```

Note: `tech` is `readonly string[]` — project tech stacks should not be mutated at runtime.

### About Types

```typescript
export interface AboutPillar {
  title: string;
  paragraphs: readonly string[];
}
```

### Skill Types

```typescript
export interface Skill {
  readonly name: string;
  readonly category: string;
  readonly level?: "beginner" | "intermediate" | "advanced" | "expert";
}
```

All properties are `readonly` — skill data is immutable.

### Timeline Types

```typescript
export interface TimelineEntry {
  readonly id: string;
  readonly role: string;
  readonly company: string;
  readonly startDate: string;
  readonly endDate?: string;
  readonly description?: string;
  readonly tags?: readonly string[];
}
```

- `endDate` is optional — current positions have no end date
- `tags` is `readonly string[]` — skill tags for each position

### Content/Collection Types (Archived)

```typescript
export interface ParsedCollectionItem {
  slug: string;
  title: string;
  description: string;
  category: string;
  status: string;
  medium?: string;
  image?: string;
  body?: string;
  document?: string;
  link?: string;
  linkLabel?: string;
  accent: string;
}

export interface Collection {
  slug: string;
  title: string;
  description: string;
  accent: string;
}

export interface ParsedPortfolioItem {
  slug: string;
  title: string;
  description: string;
  category: string;
  accent: string;
  status: string;
  image?: string;
  medium?: string;
  body?: string;
  link?: string;
  linkLabel?: string;
}
```

These types are still in `types.ts` for backward compatibility but are only used by archived components.

### Machine Overlay Type (Archived)

```typescript
export interface MachineOverlayData {
  buildVersion: string;
  route: string;
  collections: Record<string, number>;
  activeData: unknown;
}
```

### Social Icon Variant

```typescript
export type SocialIconVariant = "mail" | "linkedin" | "instagram" | "github";
```

### API Response Types

```typescript
interface ContactApiSuccess {
  success: true;
  message: string;
}

interface ContactApiError {
  success: false;
  error: string;
  retryAfter?: number;
}

export type ContactApiResponse = ContactApiSuccess | ContactApiError;
```

**Critical usage pattern:**

```typescript
// Always check the discriminant before accessing shape-specific fields
const data: ContactApiResponse = await response.json();

if (data.success) {
  // data.message is available (ContactApiSuccess)
  console.log(data.message);
} else {
  // data.error and data.retryAfter are available (ContactApiError)
  console.error(data.error);
  if (data.retryAfter) {
    console.log(`Retry after ${data.retryAfter}s`);
  }
}
```

### Internal Types (Not Exported)

**ContactPayload (in route.ts):**
```typescript
interface ContactPayload {
  name?: string;
  email?: string;
  message?: string;
}
```

Fields are optional because the type guard validates them — the payload from the client may be missing fields.

**FormData (in ContactSection.tsx):**
```typescript
interface FormData {
  name: string;
  email: string;
  message: string;
}
```

**FormErrors (in ContactSection.tsx):**
```typescript
interface FormErrors {
  name?: string;
  email?: string;
  message?: string;
}
```

**SubmissionStatus (in ContactSection.tsx):**
```typescript
type SubmissionStatus = "idle" | "submitting" | "success" | "error";
```

**ErrorBoundaryProps (in ErrorBoundary.tsx):**
```typescript
interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}
```

**ErrorBoundaryState (in ErrorBoundary.tsx):**
```typescript
interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}
```

**RateLimitConfig (in rate-limit.ts):**
```typescript
interface RateLimitConfig {
  maxRequests: number;
  windowMs: number;
}
```

**RateLimitEntry (in rate-limit.ts):**
```typescript
interface RateLimitEntry {
  tokens: number;
  lastRefill: number;
}
```

**RateLimitResult (in rate-limit.ts):**
```typescript
export interface RateLimitResult {
  success: boolean;
  remaining: number;
  retryAfterMs?: number;
}
```

**ValidationError (in route.ts):**
```typescript
interface ValidationError {
  field: string;
  message: string;
}
```

---

## Appendix A: Remediation History

### Phase 1: Build-Breaking Issues
- npm version verification
- `optimizeFonts` removal from next.config.ts
- `ssr: false` + `"use client"` requirement
- CSS import order (`@import "tailwindcss"` must be first)

### Phase 2: Type Consolidation
- Unified `Project` type in types.ts
- Enabled `noUncheckedIndexedAccess`
- Installed `react-error-boundary` as explicit dependency
- Fixed import paths (PortfolioApp location)

### Phase 3: Design Tokens, Routing, Architecture
- 14 CSS variables in `@theme` block
- Day theme override via `[data-theme="day"]`
- Hash-based routing with `useRouteHash`
- `site-config.ts` with `as const satisfies`
- Rate limiting on `/api/contact`
- `_archive/` directories for dormant code

### Phase 4: Accessibility, Security, Type Safety
- Scrollbar `border-radius: 0`
- `drizzle.config.ts` reads from env (not hardcoded)
- `.env.example` with all required variables
- `ContactApiResponse` discriminated union
- `prefersHighContrast` removal
- `useReducedMotion` implementation
- Contrast ratio verification (both themes)
- Focus management for hash navigation

### Phase 5: Code Review Fixes
- `error.tsx` type guard for `unknown` error
- `not-found.tsx` as Server Component
- Security headers in `next.config.ts`
- Rate limiter proxy header support
- Hero navigation via `onNavigate` prop
- Mobile focus trap in Navigation
- Next.js Image component in ProjectCard
- ContactSection re-render optimization
- Grain overlay pointer-events
- AccessibilityProvider removal
- Terminal keys/spacing/executeCommand fixes
- Body size limit on contact API (10KB)
- `history.pushState` instead of `window.location.hash`
- ESLint jsx-a11y double import fix

### Phase 6: Full Codebase Alignment
- AccessibilityProvider deleted
- `setState` in `useEffect` refactored
- `_archive/` ESLint ignore
- Timeline spacing fixes
- Lesson numbering consistency

### Phase 7: CRITICAL + HIGH Security & Quality
- `drizzle.config.json` deleted (hardcoded credentials)
- `ssr: false` removed (SSR now enabled)
- CSP hardened (removed `'unsafe-eval'`)
- Honest API response (email not configured)
- `isContactPayload` runtime type guard
- `null` IP fallback (not shared 127.0.0.1)
- Lazy import cleanup
- Duplicate theme initialization removed
- `useRef` replaces `getElementById`
- BentoGrid responsive fallback
- `as const satisfies SiteConfig`
- `NODE_ENV` error gating
- `not-found.tsx` semantic HTML (`<main role="main">`)
- Types centralized in `types.ts`
- npm `overrides` for transitive deps
- `skills/` excluded from `tsconfig.json`

### Documentation Alignment Pass
- Component count corrected to 16
- Chinese text translated to English
- License aligned to MIT across all files
- `react-error-boundary` version clarified (v6.1.2, `unknown` error type)
- `GEMINI.md` rewritten

---

## Appendix B: Outstanding Issues

These are known TODOs that have NOT been implemented:

1. **Integrate email service** — `EMAIL_API_KEY` in `.env.example` is a placeholder. Need Resend, SendGrid, or similar.
2. **Add error reporting** — Sentry or similar. Currently only `console.error`.
3. **Reconcile CSS variable naming** — Archived components reference variables that may not exist in the active theme.
4. **Add portrait assets** — Hero section could include a portrait image.
5. ~~**Re-enable SSR**~~ — **DONE** in Remediation 7.
6. **Write to analytics table** — Schema exists but nothing writes to it. Either implement or remove.
7. **Replace in-memory rate limiting** — Current implementation doesn't work in serverless/multi-instance deployments. Use Redis/Upstash.
8. **Generate production-quality OG image** — Current `og-image.png` may be a placeholder.
9. **Migrate Google Fonts to `next/font/google`** — Eliminates external font request and layout shift.
10. **Remove `skills/` directory** — 61MB of skill documentation not needed in the repo.
11. **Clean up legacy documentation** — Multiple remediation and status files in the root.
12. **Update/remove `GEMINI.md`** — Should be kept in sync with other agent docs.
13. **Remove `skills-backup.tar.gz`** — 40MB binary archive should not be version-controlled.

---

## Appendix C: API Routes Reference

### POST /api/contact

**Request:**
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "message": "Hello, I'd like to connect."
}
```

**Validation:**
- `name`: 1–100 characters
- `email`: Valid email regex (`/^[^\s@]+@[^\s@]+\.[^\s@]+$/`)
- `message`: 10–5000 characters

**Rate Limiting:**
- 5 requests per minute per IP
- Returns 429 with `Retry-After` header when exceeded
- Body size limit: 10KB (413 if exceeded)

**Response (success):**
```json
{
  "success": true,
  "message": "Message recorded. Email delivery is not yet configured — your message has been logged server-side."
}
```

**Response (validation error):**
```json
{
  "success": false,
  "error": "Validation failed."
}
```

**Response (rate limited):**
```json
{
  "success": false,
  "error": "Too many requests. Please try again later.",
  "retryAfter": 45
}
```

### GET /api/health

**Response (healthy):**
```json
{ "ok": true }
```

**Response (no database):**
```json
{ "ok": false, "error": "Database not configured" }
```
Status: 503

**Note:** This route uses `export const dynamic = "force-dynamic"` to prevent caching.

---

## Appendix D: Key File Locations Quick Reference

| What | Where |
|------|-------|
| Root layout | `src/app/layout.tsx` |
| Page entry | `src/app/page.tsx` |
| Main orchestrator | `src/app/PortfolioApp.tsx` |
| Design tokens | `src/app/globals.css` |
| All types | `src/lib/types.ts` |
| Site config | `src/lib/site-config.ts` |
| Project data | `src/lib/projects.ts` |
| Skills data | `src/lib/skills.ts` |
| Timeline data | `src/lib/timeline.ts` |
| Rate limiter | `src/lib/rate-limit.ts` |
| Hash routing hook | `src/hooks/useRouteHash.ts` |
| Reduced motion hook | `src/hooks/useReducedMotion.ts` |
| Theme script | `src/components/ThemeScript.tsx` |
| Navigation | `src/components/Navigation.tsx` |
| Contact form | `src/components/ContactSection.tsx` |
| Terminal | `src/components/Terminal.tsx` |
| Next.js config | `next.config.ts` |
| TypeScript config | `tsconfig.json` |
| ESLint config | `eslint.config.mjs` |
| PostCSS config | `postcss.config.mjs` |
| Drizzle config | `drizzle.config.ts` |
| Database client | `src/db/index.ts` |
| Database schema | `src/db/schema.ts` |
| Contact API | `src/app/api/contact/route.ts` |
| Health API | `src/app/api/health/route.ts` |
| Error page | `src/app/error.tsx` |
| 404 page | `src/app/not-found.tsx` |
| Environment template | `.env.example` |

---

*End of SKILL.md v6.0 — The definitive unified reference for "Nicholas Yun — The Engineered Soul" portfolio. Merged from v5 (3210 lines, 8 remediation phases, 50 lessons) and v4 (1895 lines, 4 remediation phases, 22 lessons + Six-Phase Workflow + CSS Strategy + expanded Never List).*
