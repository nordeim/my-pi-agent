---
name: brutalist-portfolio-nextjs
description: >
  Build, port, or remediate an avant-garde, anti-generic personal portfolio using Next.js 16 App Router
  with a Tactile Brutalism + High-End Editorial design system. Covers the complete architectural lifecycle
  from Vite SPA migration through four remediation phases to production: CSS-first design tokens with
  dual-theme (Night/Day), client-side SPA orchestrator embedded in Next.js, hash-based routing with
  keyboard focus management, lazy-loaded sections with ErrorBoundary + Suspense, optional database with
  graceful null handling, WCAG AAA accessibility (discriminated union API responses, ARIA, reduced motion,
  skip links, focus management), strict TypeScript with noUncheckedIndexedAccess, rate-limited API routes,
  security headers, OG/Twitter metadata + JSON-LD, centralized site configuration, dead code archival
  strategy, and a complete iterative remediation workflow. Use this skill whenever building or porting
  a portfolio, personal site, creative showcase, or any web project that demands distinctive
  brutalist/editorial aesthetics with Next.js. Also use when performing code review remediation,
  type-safety auditing, CSS variable reconciliation, migrating from Vite to Next.js, or implementing
  a phased quality-gate development workflow. Triggers on: portfolio, personal site, brutalist design,
  editorial design, Next.js port, SPA orchestrator, hash routing, dual theme, anti-generic design,
  design system tokens, CSS variable strategy, noUncheckedIndexedAccess, react-error-boundary,
  remediation, type consolidation, Vite migration, Next.js 16, Tailwind v4, discriminated unions,
  rate limiting, WCAG AAA, focus management, dead code archival.
---

# Brutalist Portfolio — Next.js 16 Architectural Blueprint & Remediation Guide

**Version 4.0** — Distilled from 4 remediation phases, 4 code review audits, 17 active components, 15 archived components, and 21 hard-won lessons.

This skill distills the complete architectural knowledge, design system, phased workflow, patterns, anti-patterns, hard-won troubleshooting insights, and remediation methodology from building and remediating "The Engineered Soul" — a personal portfolio ported from a Vite SPA to Next.js 16 App Router with Tactile Brutalism aesthetics, through **four full remediation cycles** that resolved 50+ TypeScript errors, 14 undefined CSS variables, theme system inconsistencies, accessibility gaps, security vulnerabilities, and numerous architectural inconsistencies.

Any agent using this skill can reproduce a similar codebase from scratch, apply the same architectural decisions to a new project, or perform rigorous remediation on an existing Next.js codebase.

---

## Table of Contents

1. [Project Purpose & Design Philosophy](#1-project-purpose--design-philosophy)
2. [Project Execution Phases (Six-Phase Workflow)](#2-project-execution-phases-six-phase-workflow)
3. [Architecture Blueprint](#3-architecture-blueprint)
4. [Design System: Tactile Brutalism + High-End Editorial](#4-design-system-tactile-brutalism--high-end-editorial)
5. [CSS Strategy for Tailwind v4](#5-css-strategy-for-tailwind-v4)
6. [Theme System Design](#6-theme-system-design)
7. [Component Architecture](#7-component-architecture)
8. [Data, Type & Configuration Strategy](#8-data-type--configuration-strategy)
9. [Type Safety: noUncheckedIndexedAccess Deep Dive](#9-type-safety-nouncheckedindexedaccess-deep-dive)
10. [Error Boundary Architecture](#10-error-boundary-architecture)
11. [Hash Routing Design](#11-hash-routing-design)
12. [API Route Design](#12-api-route-design)
13. [Database as Optional Feature](#13-database-as-optional-feature)
14. [Accessibility (WCAG AAA)](#14-accessibility-wcag-aaa)
15. [Security Headers & Metadata](#15-security-headers--metadata)
16. [Dead Code & Archival Strategy](#16-dead-code--archival-strategy)
17. [Build & Verification Pipeline](#17-build--verification-pipeline)
18. [Patterns (11)](#18-patterns)
19. [Anti-Patterns (14)](#19-anti-patterns)
20. [Troubleshooting Guide](#20-troubleshooting-guide)
21. [Remediation Methodology](#21-remediation-methodology)
22. [Remediation History (4 Phases)](#22-remediation-history-4-phases)
23. [Lessons Learnt (21)](#23-lessons-learnt-21)
24. [Outstanding Issues & Recommendations](#24-outstanding-issues--recommendations)
25. [Critical "Never" List](#25-critical-never-list)
26. [File Structure Reference](#26-file-structure-reference)
27. [Type Reference](#27-type-reference)
28. [Version Compatibility Matrix](#28-version-compatibility-matrix)

---

## 1. Project Purpose & Design Philosophy

### What This Project Is

"The Engineered Soul" is a personal portfolio and digital archive for a Creative Technologist. It is not a template, a starter kit, or a generic landing page. It is an **avant-garde digital installation** that deliberately rejects the homogenized "AI slop" aesthetic prevalent in modern web design.

### Anti-Generic Design Philosophy

Every visual decision must earn its place through calculated purpose. The design rejects:

- **Predictable Bootstrap-style grids and card layouts** — Use asymmetric Bento grids, staggered layouts, and deliberate visual tension instead.
- **Safe "Inter/Roboto" pairings without distinctive typographical hierarchy** — Use a three-voice typography system (Cormorant Garamond editorial / DM Sans body / IBM Plex Mono utility) that creates clear visual hierarchy and character.
- **Purple-gradient-on-white cliches** — Use a Night-first palette with warm gold accents (`#e8c547`) or a warm cream Day palette with dark goldenrod accents (`#b8860b`).
- **Rounded corners** — `border-radius: 0` is enforced globally, including scrollbar thumbs. This is non-negotiable.
- **Homogenized "AI slop" aesthetic** — If a design decision could be auto-generated by a template engine, it's wrong for this project.

### The "Why" Factor

Every element must have a reason for existing. If you cannot articulate why a component, color, animation, or layout choice is there — remove it. Whitespace as a structural element is preferred over decorative clutter.

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
- Implement in logical, testable components following the layered architecture (see Section 3).
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

## 3. Architecture Blueprint

### Core Architectural Decision: Client-Side SPA Orchestrator inside Next.js

The portfolio uses a **Client-Side SPA Orchestrator** pattern embedded within the Next.js App Router. This preserves complex animations, hash-based routing, and kinetic interactions from the original Vite SPA while gaining Next.js benefits (metadata API, code splitting via Turbopack, security headers, structured data).

**Why this pattern**: A pure Server Component approach would lose the hash-based routing and interactive state management that makes the portfolio feel like a "digital installation." The orchestrator pattern gives you both worlds — SEO metadata from Server Components, interactive SPA behavior from Client Components.

### Architectural Layers

```
layout.tsx (Server Component)
  ├── Metadata, Viewport (exported as const — works even with client page)
  ├── ThemeScript (inline script, prevents FOUC by reading localStorage before paint)
  ├── Google Fonts (preconnect + <link> in <head>)
  ├── JSON-LD structured data (Person schema)
  └── Skip-to-content link
      └── page.tsx (Client Component — "use client")
          └── ErrorBoundary (react-error-boundary, wraps everything)
              └── dynamic import with ssr: false
                  └── PortfolioApp.tsx (Client Component — orchestrator)
                      ├── AccessibilityProvider (context for reduced motion)
                      ├── Live region for theme change announcements
                      ├── Navigation (eager)
                      ├── HeroKinetic (eager — above fold)
                      ├── Sections (lazy via React.lazy + Suspense)
                      │   ├── BentoGrid (About)
                      │   ├── ProjectsSection > ProjectCard
                      │   ├── SkillsSection
                      │   ├── Timeline (Experience)
                      │   ├── BlogSection
                      │   ├── Terminal (interactive terminal emulator)
                      │   └── ContactSection (submits to /api/contact)
                      └── Footer (lazy)
```

### Key Architectural Rules

1. **`layout.tsx` is a Server Component** — exports `metadata` and `viewport`, contains the FOUC-prevention script (via `ThemeScript`), renders the skip-link. Never add `"use client"` here.
2. **`page.tsx` is a Client Component** — required because it uses `next/dynamic` with `ssr: false`. Uses `react-error-boundary` (NOT the custom `ErrorBoundary`) at the top level. This is a deliberate trade-off: no SSR for the page content, but metadata from `layout.tsx` still works for SEO.
3. **`PortfolioApp.tsx` is the orchestrator** — manages theme state, hash routing, and section composition. All sections are wrapped in a custom class-based `ErrorBoundary` + `Suspense`. **File location: `src/app/PortfolioApp.tsx`, NOT `src/components/PortfolioApp.tsx`** — the App Router co-locates the orchestrator with the route. Do NOT move it.
4. **Above-the-fold content is eager** — `Navigation` and `HeroKinetic` are imported directly (not lazy).
5. **Below-the-fold sections are lazy** — uses `React.lazy()` + `Suspense` for code splitting. Each lazy section also gets a `SectionSkeleton` fallback for loading state.
6. **Dual error boundary system** — `react-error-boundary` at the page level (catches catastrophic failures with a "Try Again" button), custom class-based `ErrorBoundary` per section (isolates failures to individual sections with a "Retry" button).

### API Layer

```
src/app/api/
  ├── contact/route.ts    # POST — validates name/email/message, rate-limited (5 req/min/IP)
  └── health/route.ts     # GET — checks DB connectivity, returns 503 if no DB
```

### Data Layer

All portfolio content is managed as static TypeScript data (not fetched from a CMS). The database is optional and currently only used for the health check endpoint.

```
src/lib/
  ├── types.ts         # CANONICAL type definitions (Project, SiteConfig, ContactApiResponse, etc.)
  ├── projects.ts      # Project entries (imports and re-exports Project from types.ts)
  ├── skills.ts        # Skill categories and items
  ├── timeline.ts      # Career timeline entries
  ├── site-config.ts   # Centralized site configuration (name, email, URLs)
  └── rate-limit.ts    # In-memory sliding window rate limiter
```

---

## 4. Design System: Tactile Brutalism + High-End Editorial

### The 28px Mathematical Grid

All spacing is governed by a 28px unit. This creates a visible structural rhythm that reinforces the brutalist aesthetic. Define the grid as CSS custom properties in the `@theme` block:

```css
@theme {
  --spacing-grid: 28px;
  --spacing-half: 14px;    /* grid / 2 */
  --spacing-quarter: 7px;  /* grid / 4 */
  --spacing-double: 56px;  /* grid * 2 */
}
```

**Gotcha**: If these derived spacing tokens are not defined in `@theme`, components that reference `var(--spacing-half)` etc. will silently get `unset`, causing layout collapse. Every CSS variable used in a component MUST be defined in `@theme` — undefined variables fail silently with no error or warning.

### Typography Hierarchy — Three Voices

Every font choice serves a distinct role. Do not use Inter or Roboto as the body font — that is the "safe default" this design rejects.

| Role | Font | CSS Variable | Tailwind Class | Purpose |
|---|---|---|---|---|
| **Editorial** | Cormorant Garamond | `--font-editorial` / `--font-serif` / `--font-display` | `font-editorial` | Headings, narrative, hero text |
| **Body** | DM Sans | `--font-body` / `--font-sans` | `font-body` | General content, paragraphs |
| **Utility** | IBM Plex Mono | `--font-utility` / `--font-mono` | `font-utility` | Labels, stats, Machine Mode, terminal |

**Why DM Sans instead of Inter**: Inter is the default system-ui stand-in used by every startup landing page. DM Sans provides similar readability with a distinctive geometric character that breaks the "AI slop" pattern.

**Font aliases**: `--font-display` is an alias for `--font-editorial` (both map to Cormorant Garamond). `--font-utility` is an alias for `--font-mono` (both map to IBM Plex Mono). `--font-body` is an alias for `--font-sans` (both map to DM Sans). Define ALL aliases in `@theme` — components may use either name.

### Brutalist Enforcement

Zero border-radius is non-negotiable. Enforce it globally, including on scrollbar thumbs:

```css
* {
  border-radius: 0 !important;
}

::-webkit-scrollbar-thumb {
  border-radius: 0;  /* Must be explicit — browsers default to rounded */
}
```

**Lesson from Remediation 4**: The scrollbar thumb had `border-radius: 3px` which violated the zero-radius rule. Browsers apply their own default border-radius to scrollbar thumbs, so you must explicitly set it to 0.

### Color System: Dual Theme with `--color-` Prefix Convention

Define all design tokens with the `--color-` prefix in the `@theme` block. This convention must be consistent across the entire codebase — mixing naming conventions creates a maintenance nightmare.

**Night theme (default) — dark palette:**
```css
@theme {
  --color-bg: #0a0a0a;
  --color-bg-soft: #111111;
  --color-surface: #1a1a1a;
  --color-border: #222222;
  --color-border-strong: #333333;
  --color-text-primary: #f0ece4;
  --color-text-secondary: #a8a29e;
  --color-text-muted: #918983;           /* Must pass WCAG AA: 5.76:1 on #0a0a0a */
  --color-accent: #e8c547;
  --color-accent-hover: #f0d060;
  --color-accent-muted: #e8c54733;
  --color-text-inverse: #0a0a0a;
  --color-border-subtle: #1a1a1a;
  --color-bg-sunken: #070707;
  --color-bg-elevated: #222222;
  --color-error: #c0392b;
  --color-accent-subtle: #e8c5471a;
}
```

**Day theme overrides via `[data-theme="day"]` selector:**
```css
[data-theme="day"] {
  --color-bg: #f5f0e8;
  --color-bg-soft: #ede8df;
  --color-surface: #e5e0d6;
  --color-border: #d5cfc4;
  --color-border-strong: #b8b0a2;
  --color-text-primary: #1a1612;
  --color-text-secondary: #5c5650;
  --color-text-muted: #6b6560;           /* Must pass WCAG AA: 5.06:1 on #f5f0e8 */
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

**Critical lesson from Remediation 4**: Contrast ratios must be verified in BOTH themes independently. The Night theme needed a lighter muted text (`#918983` = 5.76:1) while the Day theme needed a darker muted text (`#6b6560` = 5.06:1). The same hex value can pass WCAG AA on one background but fail on the other.

**Critical rule**: Use `--color-` prefix consistently. Do NOT introduce shorthand variants like `--border-color`, `--text-primary`, or `--bg-surface`. If archived components need different names, define alias variables in `globals.css` rather than creating a parallel naming system.

### Shadows: Brutal Offsets

Shadows are hard-edged offsets (no blur), reinforcing the brutalist aesthetic. These MUST be defined in `@theme` with day-theme overrides:

```css
@theme {
  --shadow-brutal: 4px 4px 0 0 var(--color-border-strong);
  --shadow-brutal-sm: 2px 2px 0 0 var(--color-border);
}

[data-theme="day"] {
  --shadow-brutal: 4px 4px 0 0 var(--color-border-strong);
  --shadow-brutal-sm: 2px 2px 0 0 var(--color-border);
}
```

**Gotcha**: If `--shadow-brutal` and `--shadow-brutal-sm` are not defined, `box-shadow: var(--shadow-brutal)` silently resolves to `unset` — cards render without shadows and look broken. No error, no warning. Day theme shadows use the same pattern but reference the overridden `--color-border-strong` and `--color-border` values, producing naturally lighter shadows on the cream background.

### Complete Required Design Tokens Table

Every token used by any active component MUST be defined in `@theme` with day-theme overrides where applicable:

| Token | Used By | Day Override |
|---|---|---|
| `--color-bg` | Body, cards, inputs | Yes |
| `--color-bg-soft` | Alternating backgrounds | Yes |
| `--color-surface` | Card surfaces, panels | Yes |
| `--color-border` | Borders, dividers | Yes |
| `--color-border-strong` | Emphasized borders | Yes |
| `--color-text-primary` | Headings, body text | Yes |
| `--color-text-secondary` | Subtitles, descriptions | Yes |
| `--color-text-muted` | Captions, timestamps, hints | Yes (different value!) |
| `--color-accent` | Buttons, links, highlights | Yes |
| `--color-accent-hover` | Button/link hover | Yes |
| `--color-accent-muted` | Selection, subtle accents | Yes |
| `--color-text-inverse` | Accent-on-dark text | Yes |
| `--color-border-subtle` | Subtle dividers | Yes |
| `--color-bg-sunken` | Sunken panels, wells | Yes |
| `--color-bg-elevated` | Elevated panels, modals | Yes |
| `--color-error` | Error messages, borders | Yes |
| `--color-accent-subtle` | Subtle accent backgrounds | Yes |
| `--font-editorial` | Headings | No (alias) |
| `--font-display` | Headings (alias) | No (alias) |
| `--font-body` | Body text | No (alias) |
| `--font-sans` | Body text (alias) | No (alias) |
| `--font-utility` | Labels, stats | No (alias) |
| `--font-mono` | Labels, stats (alias) | No (alias) |
| `--spacing-grid` | All spacing | No |
| `--spacing-double` | Section padding | No |
| `--spacing-half` | Component padding | No |
| `--spacing-quarter` | Fine spacing | No |
| `--transition-fast` | Hover states, transitions | No |
| `--shadow-brutal` | Card shadows | Yes |
| `--shadow-brutal-sm` | Small card shadows | Yes |
| `--z-index-grain` | Grain overlay | No |
| `--z-index-machine` | Machine mode overlay | No |
| `--z-index-skip-link` | Skip link | No |
| `--animate-fade-in` | Entrance animations | No |
| `--animate-fade-up` | Slide-up entrance | No |
| `--animate-slide-in` | Slide-in entrance | No |

---

## 5. CSS Strategy for Tailwind v4

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

## 6. Theme System Design

### Architecture: `data-theme` Attribute on `<html>`

The theme system uses a `data-theme` attribute, toggled between `"day"` and `"night"`. The attribute is set on `document.documentElement` (`<html>`), NOT on `<body>`.

**Do NOT use class-based theme switching** (`theme-night` / `theme-day`). The `data-attribute` approach is more semantic, works with FOUC prevention, and avoids class name collisions.

**Do NOT set `data-theme` on `<body>`** — both `ThemeScript` (initial paint) and `PortfolioApp` (runtime toggle) must target `document.documentElement` consistently. Setting on `<body>` in some places and `<html>` in others means CSS selectors only match some of the time.

### FOUC Prevention Script

Place an inline `<script>` via the `ThemeScript` component in `layout.tsx`'s `<head>` that reads `localStorage` and sets `data-theme` before the first paint:

```tsx
export function ThemeScript() {
  const script = `
    (function() {
      try {
        var stored = localStorage.getItem('theme');
        if (stored === 'night' || stored === 'day') {
          document.documentElement.setAttribute('data-theme', stored);
          return;
        }
        // Respect system preference when no stored value
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

**Why `documentElement`**: The FOUC script runs before React hydration, when `<body>` may not exist yet. Setting on `documentElement` covers the interim. The script also respects the user's OS preference (`prefers-color-scheme`) when no stored value exists.

### Theme Change Handler

In the orchestrator component, handle theme changes with accessibility announcements:

```tsx
const handleThemeChange = useCallback((theme: "day" | "night") => {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("theme", theme);

  // Announce to screen readers
  const announcement = document.getElementById("theme-announcement");
  if (announcement) {
    announcement.textContent = `Switched to ${theme} theme`;
  }
}, []);
```

Include a live region for the announcement:
```tsx
<div id="theme-announcement" aria-live="polite" aria-atomic="true" className="sr-only" />
```

### ThemeSwitch Component

The theme toggle must use `role="switch"` and `aria-checked`:

```tsx
<button
  role="switch"
  aria-checked={currentTheme === "day"}
  aria-label={`Switch to ${currentTheme === "night" ? "day" : "night"} theme`}
  onClick={() => onThemeChange(currentTheme === "night" ? "day" : "night")}
>
  {currentTheme === "night" ? "DAY" : "NIGHT"}
</button>
```

---

## 7. Component Architecture

### Active vs. Archived Classification

Components fall into two categories. Track this explicitly in documentation — assuming all components are wired in causes confusion.

**Active** (17, wired into `PortfolioApp.tsx`):

| Component | Loading | Key Features |
|---|---|---|
| `Navigation` | Eager | Hash links, mobile menu, `aria-current`, ThemeSwitch |
| `HeroKinetic` | Eager | Animated headline, "View Work" CTA, decorative grid lines |
| `SectionBlock` | Eager (imported) | Title h2 with ScrollReveal, content slot |
| `ErrorBoundary` | Eager (imported) | Class-based, per-section isolation, retry button |
| `AccessibilityProvider` | Eager | `prefersReducedMotion` via context |
| `ThemeScript` | Eager (in layout) | FOUC prevention inline script |
| `ThemeSwitch` | Eager (in Navigation) | `role="switch"`, `aria-checked`, DAY/NIGHT |
| `ScrollReveal` | Eager (imported) | IntersectionObserver, respects reduced motion |
| `BentoGrid` | Lazy | 4 bento items (Philosophy, Frontend, Backend, Design) |
| `ProjectsSection` | Lazy | Tag filter, grid, empty state |
| `ProjectCard` | Lazy (via ProjectsSection) | Image, title, description, tech tags, links |
| `SkillsSection` | Lazy | Grouped by category, bordered cards |
| `Timeline` | Lazy | Vertical timeline, date ranges, role/company |
| `BlogSection` | Lazy | "Coming Soon" placeholder |
| `Terminal` | Lazy | Commands: help, about, projects, skills, contact, clear; command history |
| `ContactSection` | Lazy | Client validation, submits to /api/contact, success/error states |
| `Footer` | Lazy | Copyright, GitHub/Email links |

**Archived** (15, in `src/components/_archive/`): AboutFlow, ArchiveSpread, ArchiveItemCard, BentoTile, BrandMark, ClientOnly, CodeRain, ContentBody, DitherOverlay, GrainOverlay, LayoutShell, MachineOverlay, MobileDrawer, SocialIcon, ThemeToggle.

**Why archived components exist**: They may be from an earlier iteration or planned for future integration. They must not be deleted without confirmation, but they must also not be assumed to work — they likely reference undefined CSS variables or Tailwind classes.

### Section Composition Pattern

Each section follows this three-layer wrapping pattern in the orchestrator:

```tsx
<section id="section-id" aria-label="Section Name">
  <ErrorBoundary fallback={<SectionError name="Section Name" />}>
    <Suspense fallback={<SectionSkeleton />}>
      <SectionBlock id="section-content" title="Section Title">
        <SectionComponent />
      </SectionBlock>
    </Suspense>
  </ErrorBoundary>
</section>
```

The three-layer wrapping provides:
1. **ErrorBoundary** — catches runtime errors, shows fallback UI with retry button
2. **Suspense** — shows skeleton while lazy-loaded component loads
3. **SectionBlock** — provides consistent section layout with animated title

### Section Skeleton

```tsx
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
```

### Section Error Fallback

```tsx
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

### Stateless Component Principle

Keep components in `src/components/` as stateless as possible. State management belongs in:
- Custom hooks (`src/hooks/`) for interaction logic
- The orchestrator (`PortfolioApp.tsx`) for app-level state (theme, active section)

---

## 8. Data, Type & Configuration Strategy

### Static TypeScript Data

Content is managed as static TypeScript data, not fetched from a CMS or database. This ensures type safety at build time, zero network requests for content, instant page loads, and easy version control.

Organize data files by domain:
```
src/lib/
  ├── types.ts        — Shared TypeScript interfaces (CANONICAL type definitions)
  ├── projects.ts     — Project entries (imports and re-exports from types.ts)
  ├── skills.ts       — Skill categories and items
  ├── timeline.ts     — Career timeline entries
  ├── site-config.ts  — Centralized site configuration (name, email, URLs)
  └── rate-limit.ts   — In-memory sliding window rate limiter
```

### Type Consolidation Rule

If two files export the same interface name (e.g., `Project` in both `types.ts` and `projects.ts`), they must be compatible or consolidated. The canonical approach: define all shared types in `types.ts`, import them in domain-specific files.

**The consolidated `Project` type** (from Remediation 2):

```typescript
export interface Project {
  id: string;
  title: string;
  description: string;
  role: string;
  period: string;
  category: ProjectCategory;
  tech: readonly string[];    // NOT "tags"
  links: ProjectLink;         // NOT top-level "github"/"live"
  image?: string;
  featured?: boolean;
}

export interface ProjectLink {
  live?: string;
  repo?: string;              // NOT top-level "github"
}

export type ProjectCategory =
  | "full-stack" | "frontend" | "systems"
  | "research" | "tool" | "design" | "other";
```

**Field mapping gotchas** (from actual bugs found and fixed):
| Old Field | New Field | Where it was wrong |
|---|---|---|
| `tags: string[]` | `tech: readonly string[]` | `ProjectCard.tsx` used `project.tags` |
| `github: string` | `links.repo: string` | `ProjectCard.tsx` used `project.github` |
| `live: string` | `links.live: string` | `ProjectCard.tsx` used `project.live` |

**Re-export pattern**: `projects.ts` imports `Project` from `types.ts` and re-exports it, so consumers can import from either location:
```typescript
import type { Project } from "./types";
export type { Project, ProjectCategory, ProjectLink } from "./types";
```

### Centralized Site Configuration

All site-wide constants (name, email, social links, URLs) must be in a single file — `site-config.ts`. This eliminates drift from hardcoding the same values in 4+ components.

```typescript
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
} as const;
```

**Lesson from Remediation 3**: Contact info was scattered across Navigation, Footer, Terminal, and layout.tsx — each hardcoding different values. Creating `site-config.ts` as single source of truth eliminated this drift risk.

### Discriminated Union for API Responses

All API responses must use discriminated unions with a `success` boolean discriminant:

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

**Usage**: TypeScript narrows the type automatically when you check `data.success`:
```typescript
if (data.success) {
  // data.message is accessible here
} else {
  // data.error and data.retryAfter are accessible here
}
```

**Do NOT** access `data.error` without first checking `data.success === false`. **Do NOT** access `data.message` without checking `data.success === true`.

---

## 9. Type Safety: noUncheckedIndexedAccess Deep Dive

### Why This Matters

`noUncheckedIndexedAccess: true` in `tsconfig.json` means array index access returns `T | undefined`, not `T`. This catches real bugs where runtime errors were possible. During Remediation 2, enabling this flag revealed 6+ actual defect sites.

### Common Patterns and Fixes

**1. Array element access in loops:**
```typescript
// WRONG — CHARS[index] might be undefined
const char = CHARS[Math.floor(Math.random() * CHARS.length)];

// CORRECT — provide fallback
const char = CHARS[Math.floor(Math.random() * CHARS.length)] ?? "0";
```

**2. Column/value access in canvas rendering:**
```typescript
// WRONG — columns[i] might be undefined
const y = columns[i] * FONT_SIZE;

// CORRECT — null coalesce
const colValue = columns[i] ?? 0;
const y = colValue * FONT_SIZE;
```

**3. IntersectionObserver callback destructuring:**
```typescript
// WRONG — ([entry]) assumes entries[0] exists
const observer = new IntersectionObserver(([entry]) => { ... });

// CORRECT — safe access
const observer = new IntersectionObserver((entries) => {
  const entry = entries[0];
  if (entry?.isIntersecting) {
    setIsVisible(true);
  }
});
```

**4. Focus management:**
```typescript
// WRONG — focusable[0] might be undefined
focusable[0].focus();

// CORRECT — optional chaining
focusable[0]?.focus();
```

**5. Command history access:**
```typescript
// WRONG — commandHistory[newIndex] might be undefined
setInput(commandHistory[newIndex]);

// CORRECT — null coalesce
setInput(commandHistory[newIndex] ?? "");
```

### Enabling noUncheckedIndexedAccess

Add to `tsconfig.json`:
```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true
  }
}
```

After enabling, run `npx tsc --noEmit` and systematically fix every `Type 'T | undefined' is not assignable to type 'T'` error. The fixes are almost always `?.` or `??` — never type assertions (`as T`).

---

## 10. Error Boundary Architecture

### Dual Error Boundary System

The project uses two complementary error boundary systems:

1. **Page-level: `react-error-boundary`** (in `page.tsx`) — wraps the entire `PortfolioApp`. Catches catastrophic failures. Uses the `FallbackComponent` pattern with a "Try Again" button.

2. **Section-level: Custom class-based `ErrorBoundary`** (in `PortfolioApp.tsx`) — wraps each section individually. Isolates failures so one broken section doesn't take down the whole app. Includes a "Retry" button.

### `react-error-boundary` v4 Type Change

**Critical gotcha**: In `react-error-boundary` v4, `FallbackProps.error` is typed as `unknown`, NOT `Error`. Custom fallback components must type it accordingly:

```typescript
// CORRECT — react-error-boundary v4
function ErrorFallback({
  error,
  resetErrorBoundary,
}: {
  error: unknown;
  resetErrorBoundary: () => void;
}) {
  const message = error instanceof Error ? error.message : "An unknown error occurred";
  // ...
}

// WRONG — TypeScript error in v4
function ErrorFallback({ error }: { error: Error }) {
  // Type 'unknown' is not assignable to type 'Error'
}
```

**Must install**: `npm install react-error-boundary` — this is a required dependency that was missing in the original `package.json`.

---

## 11. Hash Routing Design

### `useRouteHash` Hook

The custom `useRouteHash` hook provides client-side SPA navigation within the Next.js App Router by reading and writing `window.location.hash`.

```typescript
const VALID_SECTIONS = [
  "hero", "about", "projects", "skills",
  "experience", "blog", "terminal", "contact",
] as const;

type Section = (typeof VALID_SECTIONS)[number];

export function useRouteHash(): [string, (section: string) => void] {
  const [activeSection, setActiveSectionState] = useState<string>(getHashFromWindow);

  const setActiveSection = useCallback((section: string) => {
    const clean = section.replace(/^#/, "");
    const valid = VALID_SECTIONS.includes(clean as Section) ? clean : "hero";
    window.location.hash = valid;
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
    function handleHashChange() {
      const hash = window.location.hash.replace("#", "");
      const valid = VALID_SECTIONS.includes(hash as Section) ? hash : "hero";
      setActiveSectionState(valid);
    }
    window.addEventListener("hashchange", handleHashChange);
    return () => window.removeEventListener("hashchange", handleHashChange);
  }, []);

  return [activeSection, setActiveSection];
}
```

**Critical: Returns a tuple, not an object.** Use array destructuring: `const [currentHash, navigateTo] = useRouteHash()`.

### VALID_SECTIONS Must Match Actual Section IDs

The `VALID_SECTIONS` array must exactly match the section IDs rendered in `PortfolioApp.tsx`. A mismatch breaks `aria-current` indicators and active link highlighting silently — no error, just broken navigation state.

### Focus Management for Keyboard Navigation

**Lesson from Remediation 4**: Hash-based routing that scrolls without moving focus creates a trap for keyboard users. After navigation, focus must move to the target section heading using `tabindex="-1"` + `focus()`. Without this, keyboard users are stranded at their previous position while the visual viewport has moved.

The `requestAnimationFrame` wrapper ensures the DOM has updated before attempting to focus.

---

## 12. API Route Design

### Contact API (`/api/contact`)

The contact endpoint follows a layered validation pattern:

1. **Rate limiting** — 5 requests per minute per IP address
2. **JSON parsing** — graceful error for invalid JSON
3. **Type validation** — check body is an object
4. **Field validation** — name (1-100 chars), email (regex), message (10-5000 chars)
5. **Processing** — currently logs to console (TODO: integrate email service)
6. **Response** — typed with `ContactApiResponse` discriminated union

```typescript
export async function POST(request: Request): Promise<Response> {
  // 1. Rate limiting
  const ip = getClientIp(request);
  const limit = await rateLimit(ip, { maxRequests: 5, windowMs: 60_000 });
  if (!limit.success) {
    const body: ContactApiResponse = {
      success: false,
      error: "Too many requests. Please try again later.",
      retryAfter: Math.ceil((limit.retryAfterMs ?? 60_000) / 1000),
    };
    return Response.json(body, {
      status: 429,
      headers: { "Retry-After": String(body.retryAfter) },
    });
  }

  // 2-4. Parse, validate
  // 5. Process (TODO: email service)
  // 6. Return typed response
}
```

### Rate Limiter

The in-memory sliding window rate limiter supports multiple proxy headers:

```typescript
export function getClientIp(request: Request): string {
  return (
    request.headers.get("x-forwarded-for")?.split(",")[0]?.trim() ||
    request.headers.get("x-real-ip") ||
    request.headers.get("cf-connecting-ip") ||
    "127.0.0.1"
  );
}
```

**Limitation**: In-memory only. Tokens don't persist across server instances or restarts. For multi-instance deployments (Vercel, Docker), replace with Redis/Upstash rate limiting.

### Health API (`/api/health`)

Returns database connectivity status. Returns 503 when DB is unavailable. Uses null-safe db access.

---

## 13. Database as Optional Feature

### Graceful Degradation Pattern

The database connection is optional. The app must function fully without `DATABASE_URL`:

```typescript
// src/db/index.ts
function createDb() {
  if (!process.env.DATABASE_URL) return null;
  try {
    const client = postgres(process.env.DATABASE_URL);
    return drizzle(client, { schema });
  } catch {
    console.warn("Failed to connect to database. Features disabled.");
    return null;
  }
}
export const db = createDb();
```

### Null Guard in API Routes

Every API route that uses `db` must guard against null:

```typescript
if (!db) {
  return Response.json({ ok: false, error: "Database not configured" }, { status: 503 });
}
```

### Drizzle Config: Use Environment Variables

**Lesson from Remediation 4**: `drizzle.config.json` had `postgres:postgres` hardcoded in plaintext. Convert to `drizzle.config.ts` reading `DATABASE_URL` from environment:

```typescript
import { defineConfig } from "drizzle-kit";

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) {
  throw new Error("DATABASE_URL environment variable is not set.");
}

export default defineConfig({
  dialect: "postgresql",
  schema: "./src/db/schema.ts",
  dbCredentials: { url: databaseUrl },
});
```

The config throws a clear error if `DATABASE_URL` is missing. This is intentional for Drizzle Kit commands (`push`, `studio`, `generate`). The main application handles a missing database gracefully.

### Environment Variables

| Variable | Purpose | Required |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | No (app runs without DB; Drizzle Kit requires it) |
| `NEXT_PUBLIC_SITE_URL` | Site URL for `metadataBase` in `layout.tsx` | No (defaults to `https://nicholasyun.com`) |

Always create `.env.example` documenting all variables.

---

## 14. Accessibility (WCAG AAA)

### Skip-to-Content Link

Place exactly ONE skip-link in `layout.tsx` (Server Component). Do NOT duplicate it in client components.

```tsx
<a className="skip-link" href="#main-content">Skip to main content</a>
```

Style it to be invisible until focused:
```css
.skip-link { position: absolute; top: -100%; left: 16px; z-index: var(--z-index-skip-link); }
.skip-link:focus { top: 16px; }
```

**Lesson from Remediation 3**: A duplicate skip-link existed in both `layout.tsx` and `PortfolioApp.tsx`. Removed from `PortfolioApp.tsx` — one skip-link is sufficient.

### Focus Styles

High-contrast focus rings for keyboard navigation:
```css
*:focus-visible { outline: 2px solid var(--color-accent); outline-offset: 2px; }
```

### Focus Management After Navigation

After hash-based navigation, move keyboard focus to the target section heading:
```typescript
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
```

**`tabindex="-1"`** allows programmatic focus without adding the element to the tab order. **`preventScroll: true`** prevents the browser from scrolling to the heading (the hash already scrolls there).

### Reduced Motion

Respect `prefers-reduced-motion` for all animations. Use the `useReducedMotion` hook:

```typescript
export function useReducedMotion(): boolean {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(true); // SSR-safe default
  useEffect(() => {
    const mql = window.matchMedia("(prefers-reduced-motion: reduce)");
    setPrefersReducedMotion(mql.matches);
    function handleChange(e: MediaQueryListEvent) { setPrefersReducedMotion(e.matches); }
    mql.addEventListener("change", handleChange);
    return () => mql.removeEventListener("change", handleChange);
  }, []);
  return prefersReducedMotion;
}
```

Also add a CSS fallback:
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

**Lesson from Remediation 4**: `HeroKinetic` and `ScrollReveal` used inline `window.matchMedia` instead of the `useReducedMotion` hook. Updated both to import and use the hook. Any new animation component MUST use this hook.

### AccessibilityProvider vs. useReducedMotion

The project has both an `AccessibilityProvider` (with a `useAccessibility()` context hook) and a standalone `useReducedMotion()` hook. This is a known redundancy — `HeroKinetic` and `ScrollReveal` use the standalone hook while other components could use the context. These two systems should be consolidated. Either:
1. Have all components consume the context hook from `AccessibilityProvider`
2. Remove `AccessibilityProvider` and use the standalone `useReducedMotion` hook everywhere

**Lesson from Remediation 4**: `prefersHighContrast` was defined in `AccessibilityProvider` but never consumed, and no high-contrast color palette existed. Removing it entirely was cleaner than leaving a dead toggle implying non-existent functionality. **Remove half-implemented features entirely rather than leaving dead toggles.**

### ARIA Attributes Checklist

| Component | ARIA | Implementation |
|---|---|---|
| `ThemeSwitch` | `role="switch"`, `aria-checked` | Toggle between day/night |
| `Navigation` | `aria-current="page"` | Active section indicator |
| `Terminal` | `role="log"`, `aria-live="polite"` | Terminal output |
| `ContactSection` | `aria-live` | Form submission feedback |
| All sections | `aria-label` | Section identification |
| Error fallbacks | `role="alert"` | Error announcements |
| Loading skeleton | `aria-hidden="true"` | Hidden from screen readers |
| Page loading | `role="status"`, `aria-live="polite"` | Loading announcement |

### Contrast Ratios

Text-muted colors must be verified in BOTH themes independently. The same hex value can pass WCAG AA on one background but fail on the other.

| Theme | Background | Text-Muted | Ratio | Status |
|---|---|---|---|---|
| Night | `#0a0a0a` | `#918983` | 5.76:1 | WCAG AA Pass |
| Day | `#f5f0e8` | `#6b6560` | 5.06:1 | WCAG AA Pass |

---

## 15. Security Headers & Metadata

### Security Headers in next.config.ts

```typescript
const securityHeaders = [
  { key: "X-Frame-Options", value: "DENY" },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
];

const nextConfig: NextConfig = {
  poweredByHeader: false,
  reactStrictMode: true,
  images: { formats: ["image/avif", "image/webp"] },
  async headers() {
    return [{ source: "/(.*)", headers: securityHeaders }];
  },
};
```

### OG/Twitter Metadata + JSON-LD

Add comprehensive metadata in `layout.tsx` including `openGraph`, `twitter` card, `robots`, and JSON-LD `Person` schema. This works even though `page.tsx` is a Client Component because metadata is exported from the Server Component `layout.tsx`.

```typescript
const structuredData = {
  "@context": "https://schema.org",
  "@type": "Person",
  name: siteConfig.name,
  jobTitle: "Software Engineer & Designer",
  url: siteConfig.url,
  sameAs: [siteConfig.githubUrl, siteConfig.linkedinUrl],
};
```

Use `NEXT_PUBLIC_SITE_URL` environment variable for `metadataBase` with a fallback default.

---

## 16. Dead Code & Archival Strategy

### The Problem

After multiple iterations, ~40% of the codebase may become dormant — components, hooks, and data files that are never imported by any active component. This creates confusion about which code is active, which CSS variables are needed, and which types are important.

### The Solution: `_archive/` Directories

Move dormant code to `_archive/` subdirectories rather than deleting it. This makes it immediately clear what is active vs. dormant, reduces the risk of accidentally importing dead code, and preserves code that may be reintegrated later.

```
src/
  ├── components/
  │   ├── Navigation.tsx          # Active
  │   ├── HeroKinetic.tsx         # Active
  │   └── _archive/               # Dormant components
  │       ├── AboutFlow.tsx
  │       ├── CodeRain.tsx
  │       └── ...
  ├── hooks/
  │   ├── useRouteHash.ts         # Active
  │   ├── useReducedMotion.ts     # Active
  │   └── _archive/
  │       ├── useViewTransitions.ts
  │       └── useWeightedScroll.ts
  └── lib/
      ├── types.ts                # Active
      ├── projects.ts             # Active
      └── _archive/
          ├── data.ts             # Dead code with stale section names
          ├── content.ts
          └── sounds.ts
```

### TypeScript Configuration for Archival

Exclude `_archive` directories from TypeScript compilation:

```json
{
  "compilerOptions": { ... },
  "exclude": ["node_modules", "src/**/_archive"]
}
```

### Archival Rules

1. **Never import from `_archive/` in active code** — archived code may have stale types, undefined CSS variable references, and incorrect data.
2. **Before integrating any archived component**, reconcile its CSS variable names with the `--color-` prefix convention and verify all `var()` references resolve to `@theme` definitions.
3. **Archived components are not guaranteed to work** — they may reference undefined CSS variables, missing Tailwind classes, or stale data structures.
4. **Document the archival** — update AGENTS.md and README.md with the list of archived components and files.

---

## 17. Build & Verification Pipeline

### Commands

| Command | Purpose | Must Pass |
|---|---|---|
| `npm run typecheck` | `tsc --noEmit` | Zero errors |
| `npm run build` | typecheck + `next build` | Zero errors |
| `npm run lint` | ESLint | Zero warnings |
| `npm run dev` | Development server (Turbopack) | Starts successfully |

### Pre-Build Checklist

Before running `npm run build`, verify:

1. `package.json` versions exist on npm (`npm view <pkg> dist-tags`)
2. `globals.css` import order is correct (no `@import url()` after `@import "tailwindcss"`)
3. No `optimizeFonts` in `next.config.ts` (removed in Next.js 16)
4. All `"use client"` directives are present where needed
5. `db` usage includes null guards
6. No unused imports (TS6133)
7. All `var(--*)` references in components have corresponding `@theme` definitions
8. `noUncheckedIndexedAccess` is enabled — all array index access uses `?.` or `??`
9. `react-error-boundary` is installed and `error` prop is typed as `unknown`
10. `useRouteHash` is destructured as a tuple, not an object
11. Scrollbar `border-radius` is explicitly 0
12. Contact API responses use `ContactApiResponse` discriminated union
13. Text-muted contrast ratios pass WCAG AA in BOTH themes
14. All API routes have rate limiting
15. No hardcoded credentials in config files

---

## 18. Patterns

### Pattern 1: CSS Variable Naming Convention

Always use the `--color-` prefix for all color tokens in `@theme`:
- `--color-bg`, `--color-text-primary`, `--color-border`, `--color-accent`
- Day theme overrides in `[data-theme="day"]` selector

### Pattern 2: Lazy Section Loading

```tsx
const SectionComponent = lazy(() => import("@/components/SectionComponent"));
<section id="section" aria-label="Section">
  <ErrorBoundary fallback={<SectionError name="Section" />}>
    <Suspense fallback={<SectionSkeleton />}>
      <SectionComponent />
    </Suspense>
  </ErrorBoundary>
</section>
```

### Pattern 3: Optional Feature Guard

```typescript
if (!feature) { return gracefulFallback(); }
```

Applied to database connections, environment variables, and any feature that depends on external configuration.

### Pattern 4: Accessibility-First Component Design

Every interactive component must:
1. Have an `aria-label` or associated `<label>`
2. Show visible focus indicators (`:focus-visible`)
3. Announce state changes to screen readers (`aria-live`)
4. Respect reduced motion preferences
5. Be keyboard-navigable
6. Manage focus after navigation (hash routing)

### Pattern 5: Section Skeleton for Loading State

```tsx
function SectionSkeleton() {
  return (
    <div aria-hidden="true" style={{ minHeight: "200px", display: "flex", ... }}>
      Loading&hellip;
    </div>
  );
}
```

### Pattern 6: FOUC-Free Theme Initialization

Use `ThemeScript` component with `suppressHydrationWarning` to set theme before React hydration. Target `document.documentElement`, never `<body>`.

### Pattern 7: Type Re-Export for Consumer Convenience

Define types in `types.ts`, re-export from domain files:
```typescript
// types.ts — canonical definition
export interface Project { ... }

// projects.ts — re-export for convenience
import type { Project } from "./types";
export type { Project, ProjectCategory, ProjectLink } from "./types";
```

### Pattern 8: Safe Array Index Access

With `noUncheckedIndexedAccess: true`, always guard array index access:
```typescript
const item = arr[i] ?? defaultValue;   // null coalescing
const result = arr[i]?.method();       // optional chaining
```

### Pattern 9: Discriminated Union for API Responses

```typescript
type ApiResponse = ApiSuccess | ApiError;
// Use a `success` boolean discriminant for TypeScript narrowing
if (data.success) { /* access data.message */ }
else { /* access data.error */ }
```

### Pattern 10: Centralized Configuration

All site-wide constants in a single file, imported everywhere:
```typescript
export const siteConfig = { name, email, url, ... } as const;
```

### Pattern 11: Dead Code Archival

Move dormant code to `_archive/` directories, exclude from TypeScript compilation, document in agent briefings. Never import from `_archive/` in active code.

---

## 19. Anti-Patterns

### Anti-Pattern 1: Object Destructuring on Tuple-Returning Hooks

`useRouteHash` returns `[string, (section: string) => void]`. Using object destructuring (`const { currentHash, navigateTo } = useRouteHash()`) causes a runtime error. Always use array destructuring.

### Anti-Pattern 2: Mixed CSS Variable Naming Conventions

Do NOT use different naming conventions for the same concept:
- `--color-border` (canonical) vs `--border-color` (shorthand)
- `--color-text-primary` (canonical) vs `--text-primary` (shorthand)

### Anti-Pattern 3: Class-Based Theme Switching

Do NOT toggle themes by adding/removing CSS classes. Use `data-theme` attribute on `<html>`.

### Anti-Pattern 4: `optimizeFonts` in next.config.ts

This property was removed in Next.js 16. Font optimization is automatic.

### Anti-Pattern 5: `@import url()` After `@import "tailwindcss"`

The CSS optimizer will reject external font imports placed after the Tailwind import.

### Anti-Pattern 6: Unguarded Database Access

Do NOT assume `db` is always available. The database connection can be `null`.

### Anti-Pattern 7: Duplicate Skip-Links

Do NOT render skip-links in both `layout.tsx` and client components. One skip-link in `layout.tsx` is sufficient.

### Anti-Pattern 8: Duplicate Type Definitions

Do NOT export the same interface name from multiple files with different shapes. Consolidate into a single canonical definition in `types.ts`.

### Anti-Pattern 9: Generic Typography Choices

Do NOT use Inter, Roboto, or system-ui as the primary body font. Choose a distinctive typeface that reinforces the design identity.

### Anti-Pattern 10: Wrong Import Paths for Co-Located Files

`PortfolioApp.tsx` lives in `src/app/`, NOT `src/components/`. Import as `@/app/PortfolioApp`, not `@/components/PortfolioApp`.

### Anti-Pattern 11: Typing `react-error-boundary` Error Prop as `Error`

In v4, `FallbackProps.error` is `unknown`. Type it as `unknown` and use `instanceof Error` guard.

### Anti-Pattern 12: Importing from Dead Code Files

Do NOT import from `src/lib/_archive/data.ts`, `content.ts`, `utils.ts`, `testimonials.ts`, or `sounds.ts` — these are dead code with potentially stale or incorrect data.

### Anti-Pattern 13: Undefined CSS Variables in Components

Every `var(--something)` reference in a component MUST have a corresponding definition in `@theme`. Undefined variables silently resolve to `unset` with no error or warning.

### Anti-Pattern 14: Leaving Half-Implemented Features

Do not leave unused toggles, context values, or configuration options that imply functionality that doesn't exist (e.g., `prefersHighContrast` with no high-contrast palette). Remove them entirely.

---

## 20. Troubleshooting Guide

### Build Errors

| Symptom | Root Cause | Fix |
|---|---|---|
| `npm install` fails with `ETARGET` | Package version doesn't exist on npm | Verify with `npm view <pkg> dist-tags`. Update to the latest available. |
| `optimizeFonts` not in `NextConfig` | Property removed in Next.js 16 | Remove from `next.config.ts` |
| `ssr: false` not allowed in Server Components | `page.tsx` was a Server Component | Add `"use client"` directive |
| CSS `@import url()` warning | Font import after `@import "tailwindcss"` | Move `@import url(...)` to the top of `globals.css` or use `<link>` in layout |
| `db is possibly null` (TS18047) | Database connection is optional | Add `if (!db) { return ... }` guard |
| Unused import (TS6133) | Variable declared but never read | Remove the unused import |
| `Property X does not exist on type [...]` | `noUncheckedIndexedAccess: true` | Use `?.` or `??` for array index access |
| `Type 'unknown' is not assignable to type 'Error'` | `react-error-boundary` v4 | Type as `error: unknown`, guard with `instanceof Error` |
| Cannot find module `react-error-boundary` | Not installed | `npm install react-error-boundary` |
| Cannot find module `@/components/PortfolioApp` | Wrong import path | Import from `@/app/PortfolioApp` |
| Object destructuring on useRouteHash returns undefined | Hook returns tuple, not object | Use `const [currentHash, navigateTo] = useRouteHash()` |
| `tags` does not exist on `Project` | Old field name | Use `tech` (consolidated type) |
| `github`/`live` does not exist on `Project` | Old field names | Use `links.repo`/`links.live` |
| `href`/`label` does not exist on `SocialLink` | Wrong field names | Use `url`/`platform` |

### Visual Issues

| Symptom | Root Cause | Fix |
|---|---|---|
| Component renders with wrong font | Missing `@theme` font family entry | Verify the font variable is in `@theme` |
| Theme toggle doesn't work | Using class-based switching | Change to `data-theme` attribute on `<html>` |
| Flash of wrong theme on load | Missing FOUC prevention script | Add `ThemeScript` to `layout.tsx` `<head>` |
| CSS variables resolve to empty | Variable name mismatch or undefined | Check `globals.css` for exact variable name with `--color-` prefix |
| Missing shadows on cards | `--shadow-brutal` not defined | Add to `@theme` block with day override |
| Broken transitions | `--transition-fast` not defined | Add to `@theme` block |
| Active nav link not highlighted | `VALID_SECTIONS` doesn't match section IDs | Update to match actual section IDs in PortfolioApp |
| Z-index layering broken | Custom z-index tokens not defined | Add `--z-index-*` to `@theme` |
| Scrollbar has rounded thumb | Browser default `border-radius` | Explicitly set `::-webkit-scrollbar-thumb { border-radius: 0; }` |
| Muted text hard to read | Contrast ratio fails WCAG AA | Use different values for Night vs Day themes |
| Keyboard focus stranded after navigation | No focus management on hash change | Add `tabindex="-1"` + `focus()` in `useRouteHash` |

### Version Compatibility

| Package | Verified Working Version | Notes |
|---|---|---|
| `next` | 16.2.9 | `optimizeFonts` removed; `ssr: false` requires `"use client"` |
| `react` | 19.2.7 | Latest stable at time of writing |
| `react-dom` | 19.2.7 | Must match React version |
| `@types/react` | 19.2.17 | Latest available |
| `@types/react-dom` | 19.2.3 | Max available (NOT 19.2.6+) |
| `tailwindcss` | 4.1.17 | CSS-first config, `@import "tailwindcss"` |
| `drizzle-orm` | 0.45.2 | PostgreSQL adapter |
| `typescript` | 5.9.3 | Strict mode + noUncheckedIndexedAccess |
| `react-error-boundary` | 4.x | `FallbackProps.error` is `unknown` |

---

## 21. Remediation Methodology

When applying a remediation (a batch of fixes from a code review or audit), follow this rigorous process:

### Step 1: Deep Reconnaissance

Read ALL documentation files before touching code:
- `CLAUDE.md`, `AGENTS.md`, `README.md` — project constraints and gotchas
- Any code review reports — identified issues and proposed fixes
- Status files — current project state and remediation history
- Existing SKILL files — architectural knowledge

### Step 2: Validate Remediation Proposals Against Actual Codebase

**Critical lesson from Remediation 4**: Remediation reports written without access to the actual codebase may reference ~15 files that don't exist (`ParticleField.tsx`, `CustomCursor.tsx`, `GlitchText.tsx`, etc.). Always validate each proposal against the real file structure before applying changes. Never blindly apply fixes for files that don't exist.

### Step 3: Extract Files from Remediation Report

Remediation reports often embed file contents in markdown code blocks. Extract each file carefully:
- Use the LAST occurrence of each file path (later fixes supersede earlier ones)
- Verify the file path is correct relative to the project root
- Check that the content is complete (not truncated)
- For large remediation files (4000+ lines), use systematic extraction

### Step 4: Verify Package Versions

Before running `npm install`, verify every version in `package.json` against npm:
```bash
npm view <package> dist-tags
```

Remediation reports may specify versions that don't exist. Update to the nearest available version.

### Step 5: Install Dependencies

```bash
npm install
```

Check for missing dependencies that the remediation introduces (e.g., `react-error-boundary`).

### Step 6: Typecheck First

```bash
npx tsc --noEmit
```

Fix all type errors before proceeding to build.

### Step 7: Build and Fix

```bash
npm run build
```

Fix any build errors. Re-run until clean.

### Step 8: Full Codebase Audit

After remediation, perform a comprehensive audit:
- Check for stale references to removed/renamed files
- Verify ALL CSS variable references resolve to `@theme` definitions
- Verify Tailwind class names are defined
- Check for duplicate type definitions
- Verify component integration status
- Verify `VALID_SECTIONS` matches section IDs
- Verify theme target consistency
- Check for dead code
- Verify all dependencies are in `package.json`

### Step 9: Update ALL Documentation

Update README.md, CLAUDE.md, AGENTS.md, and GEMINI.md to reflect the current state.

---

## 22. Remediation History (4 Phases)

### Remediation 1 (Initial Port — Build-Breaking Issues)

| Issue | Resolution |
|---|---|
| `@types/react-dom@^19.2.6` didn't exist on npm | Updated to `^19.2.3` |
| `react@^19.2.6` / `react-dom@^19.2.6` didn't exist | Updated to `^19.2.7` |
| `next@^16.2.6` didn't exist | Updated to `^16.2.9` |
| `optimizeFonts` not in `NextConfig` type | Removed from `next.config.ts` |
| Unused `CodeRain` lazy import (TS6133) | Removed from `PortfolioApp.tsx` |
| `db` possibly null (TS18047) | Added null guard in `/api/health/route.ts` |
| `ssr: false` not allowed in Server Components | Added `"use client"` to `page.tsx` |
| CSS `@import url()` must precede all rules | Moved Google Fonts import before `@import "tailwindcss"` |

### Remediation 2 (Type Consolidation + Strictness)

| Issue | Resolution |
|---|---|
| Duplicate `Project` type across `types.ts` and `projects.ts` | Consolidated into single definition in `types.ts`; `projects.ts` re-exports |
| Missing type exports | Added 7 missing interfaces/types to `types.ts` |
| `noUncheckedIndexedAccess` not enabled | Added to `tsconfig.json`; fixed 6+ array index access patterns |
| `react-error-boundary` not installed | Added as dependency; `page.tsx` uses its `ErrorBoundary` |
| `useRouteHash` returns tuple, not object | Fixed destructuring in `PortfolioApp.tsx` |
| `page.tsx` imported from wrong path | Fixed to `@/app/PortfolioApp` |
| `FallbackProps.error` typed as `Error` | Updated to `unknown` in `ErrorFallback` |
| `ProjectCard` used old field names | Rewrote to use `tech`/`links.repo`/`links.live` |
| Missing `@theme` tokens | Added fonts, z-index, animations |
| Missing day-theme overrides | Added `[data-theme="day"]` color overrides |
| Missing security headers | Added X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy |
| Missing OG/Twitter metadata | Added comprehensive metadata in `layout.tsx` |
| Missing structured data | Added JSON-LD `Person` schema |

### Remediation 3 (Design Tokens, Routing, Architecture)

| Issue | Resolution |
|---|---|
| 14 undefined CSS variables in active components | Defined all in `@theme` with day-theme overrides |
| Day theme incomplete | Added overrides for ALL semantic tokens |
| Hash routing mismatch | Updated `VALID_SECTIONS` to match actual section IDs |
| Theme target inconsistency | Unified on `document.documentElement` in both `ThemeScript` and `PortfolioApp` |
| System preference ignored | Added `prefers-color-scheme` detection |
| Contact info scattered | Created `site-config.ts` as single source of truth |
| Contact form simulated | Replaced with real POST `/api/contact` endpoint |
| No rate limiting | Created `rate-limit.ts` with sliding window algorithm |
| Duplicate skip-link | Removed from `PortfolioApp.tsx` |
| Dead code mixed with active | Moved dormant code to `_archive/` directories |

### Remediation 4 (Accessibility, Security, Type Safety)

| Issue | Resolution |
|---|---|
| Scrollbar `border-radius: 3px` | Changed to `0` in `globals.css` |
| Hardcoded DB credentials | Converted `drizzle.config.json` to `.ts` with env vars |
| No `.env.example` | Created with all variables documented |
| Untyped API responses | Added `ContactApiResponse` discriminated union |
| Unused `prefersHighContrast` | Removed from `AccessibilityProvider` entirely |
| Inline `window.matchMedia` in components | Updated to use `useReducedMotion` hook |
| Text-muted contrast fails WCAG AA | Night: `#918983` (5.76:1); Day: `#6b6560` (5.06:1) |
| No focus management after hash nav | Added `tabindex="-1"` + `focus()` in `useRouteHash` |
| ARIA attributes verified | Already present — `ThemeSwitch`, `Navigation`, `Terminal` |

---

## 23. Lessons Learnt (21)

### 1. Verify npm Versions Before Pinning
Remediation specified versions that didn't exist on npm (`@types/react-dom@^19.2.6`, max was 19.2.3). Just because a version number follows a logical sequence doesn't mean it was published.

### 2. CSS Import Order Is Critical in Tailwind v4
`@import "tailwindcss"` expands to `@layer` rules. External font imports must come before it.

### 3. `optimizeFonts` Is Gone in Next.js 16
Font optimization is automatic. The config key no longer exists.

### 4. `ssr: false` Requires Client Components
In Next.js 16, `next/dynamic` with `ssr: false` cannot be used in Server Components.

### 5. Two Design Token Systems Create Technical Debt
Dormant components use shorthand CSS variable names while `@theme` uses `--color-` prefix. Must reconcile before integration. Moving dormant code to `_archive/` prevents confusion.

### 6. Null-Safe Database Access Is Mandatory
Since `DATABASE_URL` is optional, `db` can be `null`. Always guard.

### 7. `noUncheckedIndexedAccess` Catches Real Bugs
Array index access returning `T | undefined` revealed 6+ places where runtime errors were possible.

### 8. `react-error-boundary` v4 Changed `FallbackProps.error`
From `Error` to `unknown`. Must use `instanceof Error` guard.

### 9. File Location Matters for App Router Imports
`PortfolioApp.tsx` in `src/app/` must be imported as `@/app/PortfolioApp`.

### 10. Undefined CSS Variables Fail Silently
`var(--font-display)` resolving to `unset` produces no error — the style just doesn't apply. Audit all `var()` references against `@theme`.

### 11. Hook Return Types Must Match Destructuring
A hook returning a tuple cannot be destructured with object syntax.

### 12. Type Consolidation Requires Consumer Updates
When consolidating a type, every consumer must be updated to use new field names.

### 13. Remediation Reports May Introduce New Dependencies
Check for new imports after extracting files.

### 14. Hash Routing Section Names Must Match Actual IDs
A mismatch breaks `aria-current` silently.

### 15. Theme Target Consistency Matters
Pick one element (`<html>`) and use it everywhere for `data-theme`.

### 16. Dead Code Creates Maintenance Confusion
~40% of codebase may become dormant. Regular dead code audits and `_archive/` directories are essential.

### 17. Centralize Configuration Early
Scattered hardcoded values create drift risk. Single source of truth (`site-config.ts`) eliminates this.

### 18. Discriminated Unions Prevent Type Errors on API Responses
`ContactApiResponse = ContactApiSuccess | ContactApiError` with `success` discriminant enables safe TypeScript narrowing.

### 19. Contrast Ratios Must Be Verified in Both Themes Independently
The same hex value can pass AA on dark but fail on light. Use different muted text colors for Night vs Day.

### 20. Remove Half-Implemented Features Entirely
Dead toggles implying non-existent functionality (like `prefersHighContrast` with no palette) create confusion. Remove them.

### 21. Focus Management Is Essential for Keyboard Navigation
Hash-based routing that scrolls without moving focus traps keyboard users. Add `tabindex="-1"` + `focus()` after navigation.

---

## 24. Outstanding Issues & Recommendations

| Priority | Issue | Recommendation |
|---|---|---|
| 1 | Contact API logs to console | Integrate email service (Resend, SendGrid) |
| 2 | No error reporting | Integrate Sentry in `error.tsx` and global error boundary |
| 3 | Redundant accessibility systems | Consolidate `useAccessibility()` context vs `useReducedMotion()` hook |
| 4 | Archived CSS variable mismatch | Add aliases in `globals.css` or rewrite to `--color-` prefix |
| 5 | Missing portrait assets | Place webp images in `public/portraits/` |
| 6 | No SSR for SEO | Replace `ssr: false` with `Suspense` boundaries |
| 7 | Analytics table never written to | Implement middleware to track page views or remove unused schema |
| 8 | In-memory rate limiting only | Replace with Redis/Upstash for multi-instance deployments |
| 9 | Blog section is placeholder | Implement blog content or remove the section |
| 10 | Terminal has limited commands | Expand command set (e.g., `experience`, `education`, `download`) |

---

## 25. Critical "Never" List

- **Never** use `border-radius` (unless explicitly requested for a specific non-UI element)
- **Never** use `any` in TypeScript
- **Never** use Vite-specific features like `import.meta.glob`
- **Never** add speculative "AI slop" or safe defaults (rounded cards, Inter-only typography)
- **Never** add `optimizeFonts` to `next.config.ts` (removed in Next.js 16)
- **Never** put `@import url()` after `@import "tailwindcss"` in `globals.css`
- **Never** use class-based theme switching. Use `data-theme` attribute on `<html>`
- **Never** set `data-theme` on `<body>` — always use `document.documentElement` (`<html>`)
- **Never** use `db` from `@/db` without a null guard
- **Never** access array indices without `?.` or `??` (enforced by `noUncheckedIndexedAccess`)
- **Never** import `PortfolioApp` from `@/components/PortfolioApp` — it's at `@/app/PortfolioApp`
- **Never** type `react-error-boundary` fallback `error` prop as `Error` — it's `unknown`
- **Never** import data from `@/lib/_archive/data` — it's dead code with stale section names
- **Never** hardcode site config in components — import from `@/lib/site-config`
- **Never** create an API route without rate limiting — use `rateLimit()` from `@/lib/rate-limit`
- **Never** hardcode credentials in config files — use environment variables
- **Never** access `ContactApiResponse.error` without checking `data.success === false` first
- **Never** trust remediation docs without validating file paths against the actual codebase
- **Never** leave half-implemented features — remove them entirely
- **Never** use object destructuring on `useRouteHash()` — it returns a tuple
- **Never** reference CSS variables that aren't defined in `@theme` — they silently resolve to `unset`

---

## 26. File Structure Reference

The canonical file structure for a project built with this skill:

```
project-root/
├── .env.example                    # Environment variable template
├── next.config.ts                  # Security headers, strict mode, poweredByHeader: false
├── package.json                    # Verified dependency versions
├── tsconfig.json                   # strict: true, noUncheckedIndexedAccess: true, @/ alias
├── drizzle.config.ts               # DB config using env vars (NOT .json with hardcoded creds)
├── eslint.config.mjs
├── postcss.config.mjs
│
├── src/
│   ├── app/
│   │   ├── layout.tsx              # Server Component: metadata, FOUC script, skip-link, JSON-LD
│   │   ├── page.tsx                # Client Component: dynamic import + react-error-boundary
│   │   ├── PortfolioApp.tsx        # Client Component: SPA orchestrator (IN src/app/, NOT src/components/)
│   │   ├── error.tsx               # Next.js error page
│   │   ├── not-found.tsx           # 404 page
│   │   ├── globals.css             # Design tokens (@theme), theme rules, utility classes
│   │   └── api/
│   │       ├── contact/route.ts    # POST — validation + rate limiting + typed response
│   │       └── health/route.ts     # GET — DB health check (null-safe)
│   │
│   ├── components/
│   │   ├── Navigation.tsx          # Active (eager)
│   │   ├── HeroKinetic.tsx         # Active (eager)
│   │   ├── SectionBlock.tsx        # Active
│   │   ├── ErrorBoundary.tsx       # Active (class-based, per-section)
│   │   ├── AccessibilityProvider.tsx # Active
│   │   ├── ThemeScript.tsx         # Active (FOUC prevention)
│   │   ├── ThemeSwitch.tsx         # Active
│   │   ├── ScrollReveal.tsx        # Active
│   │   ├── BentoGrid.tsx           # Active (lazy)
│   │   ├── ProjectsSection.tsx     # Active (lazy)
│   │   ├── ProjectCard.tsx         # Active (via ProjectsSection)
│   │   ├── SkillsSection.tsx       # Active (lazy)
│   │   ├── Timeline.tsx            # Active (lazy)
│   │   ├── ContactSection.tsx      # Active (lazy)
│   │   ├── BlogSection.tsx         # Active (lazy)
│   │   ├── Terminal.tsx            # Active (lazy)
│   │   ├── Footer.tsx              # Active (lazy)
│   │   └── _archive/               # Dormant components (excluded from tsconfig)
│   │       └── ...
│   │
│   ├── hooks/
│   │   ├── useRouteHash.ts         # Hash-based routing (returns tuple!)
│   │   ├── useReducedMotion.ts     # Prefers-reduced-motion detection
│   │   └── _archive/               # Dormant hooks
│   │
│   ├── lib/
│   │   ├── types.ts                # CANONICAL type definitions + ContactApiResponse
│   │   ├── projects.ts             # Project data (re-exports from types.ts)
│   │   ├── skills.ts               # Skill data
│   │   ├── timeline.ts             # Timeline data
│   │   ├── site-config.ts          # Centralized site configuration
│   │   ├── rate-limit.ts           # Sliding window rate limiter + getClientIp
│   │   └── _archive/               # Dormant lib files
│   │
│   └── db/
│       ├── index.ts                # Optional DB connection (null-safe)
│       └── schema.ts               # Drizzle schema
│
├── public/
│   ├── favicon.svg
│   └── portraits/                  # (add portrait assets here)
│
└── docs/                           # Project documentation
```

---

## 27. Type Reference

### Core Types (defined in `src/lib/types.ts`)

```typescript
export interface NavLink {
  label: string;
  href: string;
}

export interface SocialLink {
  platform: string;    // NOT "label"
  url: string;         // NOT "href"
  icon?: string;
}

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

export interface ProjectLink {
  live?: string;
  repo?: string;       // NOT top-level "github"
}

export type ProjectCategory =
  | "full-stack" | "frontend" | "systems"
  | "research" | "tool" | "design" | "other";

export interface Project {
  id: string;
  title: string;
  description: string;
  role: string;
  period: string;
  category: ProjectCategory;
  tech: readonly string[];  // NOT "tags"
  links: ProjectLink;
  image?: string;
  featured?: boolean;
}

// API Response Types
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

### Archived Types (in `types.ts`, only used by archived components)

```typescript
export interface AboutPillar { ... }
export interface ParsedCollectionItem { ... }
export interface Collection { ... }
export interface ParsedPortfolioItem { ... }
export interface MachineOverlayData { ... }
export type SocialIconVariant = "mail" | "linkedin" | "instagram" | "github";
```

---

## 28. Version Compatibility Matrix

| Package | Verified Version | Critical Notes |
|---|---|---|
| `next` | ^16.2.9 | `optimizeFonts` removed; `ssr: false` requires `"use client"` |
| `react` | ^19.2.7 | |
| `react-dom` | ^19.2.7 | Must match React version |
| `@types/react` | ^19.2.17 | |
| `@types/react-dom` | ^19.2.3 | Max available — do NOT specify higher |
| `tailwindcss` | ^4.1.17 | CSS-first config, `@import "tailwindcss"` |
| `drizzle-orm` | ^0.45.2 | PostgreSQL adapter |
| `postgres` | ^3.4.7 | Database driver |
| `typescript` | ^5.9.3 | Strict mode + noUncheckedIndexedAccess |
| `react-error-boundary` | ^6.1.2 | `FallbackProps.error` is `unknown` |

**Always verify versions before pinning**: `npm view <pkg> dist-tags`
