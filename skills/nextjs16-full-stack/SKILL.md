---
name: nextjs16-full-stack
description: |
  IRONFORGE Fitness Studio — Brutalist/Raw + Retro-Futuristic Design System & Next.js 16 Full-Stack Engineering Reference
  Production-grade skill for building IRONFORGE Fitness Studio from any AI agent. Covers
  - Avant-garde brutalist/raw design system with neon orange (#FF5400) on pure black (#0a0a0a)
  - Tailwind CSS v4 CSS-first @theme block, custom utilities, and v3→v4 migration rules
  - Anti-generic UI, typography scale (Bebas Neue / Oswald / Archivo / JetBrains Mono), and motion standards
  - Next.js 16 + React 19 App Router, Server Components, and 5-layer architecture (proxy → app → features → domain → lib)
  - Auth.js v5 + Drizzle ORM authentication, SSE streaming, and env validation
  - shadcn/ui + Radix patterns and CVA component variants
  - Accessibility (WCAG AAA) and performance budgets
  - Vitest, Playwright, and brand-token testing
  This skill ensures any coding agent can match to the IRONFORGE fitness-studio project and implement aligned with the master execution plan.
triggers:
  - ironforge
  - fitness-studio
  - brutalist-fitness
  - nextjs-fitness-app
  - neon-orange-design
  - avant-garde-fitness
version: 1.0
---

# Skills Knowledge Base — IRONFORGE Fitness Studio

> Companion document to `Master Execution Plan.md`.
> Distilled from deep reads of 4 critical skills from `~/.pi/agent/skills/` + scaffolding scan of the existing repo.
> Every rule below is enforced during implementation.

---

## 1. Strategic Positioning (from `avant-garde-design-v4`)

**Quadrant:** Q4 — THE VISIONARY (disruptive brand + aspiration-driven audience).
**Design direction:** Brutalist/Raw primary skeleton + Retro-Futuristic accent (neon orange glow + silver chrome).
**Aesthetic:** "FORGED IN IRON." Editorial noir meets industrial telemetry.

### Anti-Generic Checklist (verbatim, must pass all 10)

1. Intentionality — every element earns its place (Why? Only? Without?)
2. Distinctive Hierarchy — large typography is structural, not just size
3. Whitespace as Voice — communicates drama or calm
4. Human Imperfection — intentional roughness signals authorship
5. Tactile Interaction — elements feel physically reactive
6. Radical Color — deviates from SaaS blue/indigo (we use neon orange on pure black)
7. Narrative Flow — page tells a story
8. Typography Soul — fonts chosen for character (Bebas Neue + Oswald + Archivo + JetBrains Mono)
9. Invisible UX — micro-interactions serve the user
10. Strategic Alignment — aesthetic supports the Compass position

### Forbidden (Anti-Generic §1.0)

- Bento grids
- Hero Split (L/R)
- Mesh gradients
- Glassmorphism (blue/white)
- Inter/Roboto default
- Purple/indigo blur
- Predictable card grids

### Quality Gate

Three metrics scored 1–10: **Memorability, Integrity, Craftsmanship.**
**Pass threshold: minimum 24/30 total.**

---

## 2. Color Palette Rules (from `avant-garde-design-v4/09-color-palettes.md`)

### The 60-30-10 Rule

- **60% Primary/Background** — pure black `#0a0a0a`
- **30% Secondary** — dark gray / silver `#141414` / `#C8C8C8`
- **10% Accent** — neon orange `#FF5400` (large text + UI accents only)

### WCAG AAA Contrast (mandatory)

- Normal text: **7:1**
- Large text (18px+): **4.5:1**
- Non-text UI components: **3:1**

**Verified contrasts for IRONFORGE:**

- `#f5f5f5` body on `#0a0a0a` bg = **18.7:1** ✅ AAA
- `#FF5400` accent on `#0a0a0a` bg = **5.34:1** — passes AAA for large text (≥18px) and UI components; **FAILS for small body text** — restrict orange to ≥18px or UI accents only
- `#C8C8C8` silver on `#0a0a0a` bg = **11.4:1** ✅ AAA
- `#6a6a6a` muted on `#0a0a0a` bg = **3.85:1** — fails AAA for normal text; restrict to ≥18px or non-text

### Forbidden Colors (enforced by Vitest brand-token test)

- Any purple/violet (`#7c3aed`, `#a855f7`, `#8b5cf6`)
- Any default Tailwind blue (`#3b82f6`)
- Any default Tailwind `gray-100` through `gray-400` on dark backgrounds
- Amber-100 / amber-200 (too soft)

---

## 3. Typography Scale

| Role           | Family         | Weight | Size (desktop / mobile) | Tracking        | Used for                  |
| -------------- | -------------- | ------ | ----------------------- | --------------- | ------------------------- |
| Display        | Bebas Neue     | 400    | 8.5vw / 14vw            | 0.005em         | Hero headline only        |
| Heading 1      | Oswald         | 600    | 4rem / 2.5rem           | 0.01em          | Section titles            |
| Heading 2      | Oswald         | 500    | 2.25rem / 1.75rem       | 0.02em          | Card titles               |
| Body           | Archivo        | 400    | 1.0625rem / 1rem        | 0               | Paragraphs                |
| Body condensed | Archivo        | 500    | 0.9375rem               | 0.04em          | Coach bios, story quotes  |
| Telemetry      | JetBrains Mono | 400    | 0.6875rem               | 0.2em uppercase | Section markers, counters |
| CTA            | Oswald         | 600    | 0.85rem                 | 0.2em uppercase | Buttons, pills            |

**Line-height:** 1.55 body, 0.85 display, 1.1 headings.
**Width:** Body text blocks must not exceed **80 characters** (WCAG AAA §1.4.8).
**Line spacing:** ≥ **1.5** for body (WCAG AAA §1.4.8).

---

## 4. Tailwind v4 CSS-First Rules (from `nextjs16-tailwind4` + `tailwind-patterns`)

### Single source of truth

- `src/app/globals.css` contains `@import "tailwindcss";` + one `@theme { … }` block.
- **Forbidden:** `tailwind.config.js`, `tailwind.config.ts`, PostCSS plugins from v3, `postcss-import`, `autoprefixer`.

### `@theme` block structure (canonical for IRONFORGE)

```css
@import 'tailwindcss';

@theme {
  /* Colors — OKLCH where possible, hex allowed for pure black */
  --color-bg: #0a0a0a;
  --color-bg-darker: #050505;
  --color-bg-card: #141414;
  --color-bg-card-hover: #1a1a1a;
  --color-fg: #f5f5f5;
  --color-fg-dim: #c0c0c0;
  --color-muted: #6a6a6a;
  --color-accent: #ff5400;
  --color-accent-bright: #ff7a33;
  --color-accent-dim: #b33a00;
  --color-accent-glow: rgba(255, 84, 0, 0.45);
  --color-silver: #c8c8c8;
  --color-silver-dim: #5a5a5a;
  --color-border: #1f1f1f;
  --color-border-light: #2a2a2a;

  /* Typography */
  --font-display: 'Bebas Neue', 'Arial Narrow', sans-serif;
  --font-heading: 'Oswald', 'Inter Tight', sans-serif;
  --font-body: 'Archivo', 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'Geist Mono', monospace;

  /* Motion */
  --ease-premium: cubic-bezier(0.22, 1, 0.36, 1);
  --ease-snap: cubic-bezier(0.16, 1, 0.3, 1);
  --dur-reveal: 900ms;
  --dur-flip: 900ms;
  --dur-sticky: 600ms;

  /* Layout */
  --container-max: 1600px;
  --gutter: 1.5rem;
  --gutter-lg: 2.5rem;

  /* Z-index scale (from avant-garde-design-v4) */
  --z-behind: -1;
  --z-base: 0;
  --z-raised: 10;
  --z-dropdown: 200;
  --z-sticky: 300;
  --z-overlay: 400;
  --z-modal: 500;
  --z-popover: 600;
  --z-tooltip: 700;
  --z-toast: 800;
  --z-max: 999;

  /* Animations */
  --animate-pulse-cta: pulse-cta 2.4s ease-out infinite;
  --animate-marquee: marquee 38s linear infinite;
  --animate-ken-burns: ken-burns 9s ease-out forwards;
  --animate-wave: wave 0.7s ease-in-out infinite;

  @keyframes pulse-cta {
    0%,
    100% {
      box-shadow:
        0 0 0 0 rgba(255, 84, 0, 0.65),
        0 0 40px rgba(255, 84, 0, 0.3);
    }
    50% {
      box-shadow:
        0 0 0 18px rgba(255, 84, 0, 0),
        0 0 40px rgba(255, 84, 0, 0.3);
    }
  }
  @keyframes marquee {
    0% {
      transform: translateX(0);
    }
    100% {
      transform: translateX(-50%);
    }
  }
  @keyframes ken-burns {
    0% {
      transform: scale(1.06) translate(0, 0);
    }
    100% {
      transform: scale(1.2) translate(-3%, -3%);
    }
  }
  @keyframes wave {
    0%,
    100% {
      height: 3px;
    }
    50% {
      height: 16px;
    }
  }
}

/* Base layer */
@layer base {
  * {
    border-color: var(--color-border);
  }
  html {
    scroll-behavior: smooth;
  }
  body {
    background-color: var(--color-bg);
    color: var(--color-fg);
    font-family: var(--font-body);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    overflow-x: hidden;
  }
  h1,
  h2,
  h3 {
    font-family: var(--font-heading);
  }
  ::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }
  ::-webkit-scrollbar-track {
    background: var(--color-bg-darker);
  }
  ::-webkit-scrollbar-thumb {
    background: var(--color-accent-dim);
  }
  ::-webkit-scrollbar-thumb:hover {
    background: var(--color-accent);
  }
}

/* Custom utilities */
@utility text-stroke {
  -webkit-text-stroke: 1.5px var(--color-silver-dim);
  color: transparent;
}
@utility text-stroke-accent {
  -webkit-text-stroke: 1.5px var(--color-accent);
  color: transparent;
}
@utility vertical-text {
  writing-mode: vertical-rl;
  text-orientation: mixed;
}
@utility bg-textured {
  background-color: var(--color-bg);
  background-image:
    radial-gradient(circle at 20% 30%, rgba(255, 84, 0, 0.06) 0%, transparent 40%),
    radial-gradient(circle at 80% 70%, rgba(80, 80, 80, 0.06) 0%, transparent 40%);
}

/* Reduced motion — MANDATORY */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  [data-reveal] {
    opacity: 1 !important;
    transform: none !important;
  }
}
```

### v3 → v4 migration rules (verbatim)

| v3                  | v4               |
| ------------------- | ---------------- |
| `bg-opacity-50`     | `bg-color/50`    |
| `shadow-sm`         | `shadow-xs`      |
| `shadow`            | `shadow-sm`      |
| `blur-sm`           | `blur-xs`        |
| `rounded-sm`        | `rounded-xs`     |
| `bg-gradient-to-r`  | `bg-linear-to-r` |
| `outline-none`      | `outline-hidden` |
| `ring`              | `ring-3`         |
| `flex-shrink-*`     | `shrink-*`       |
| `flex-grow-*`       | `grow-*`         |
| `bg-[--brand]`      | `bg-(--brand)`   |
| `bg-[var(--brand)]` | `bg-(--brand)`   |

### Forbidden Tailwind patterns

- `tailwind.config.ts` present (must delete)
- Missing `@import "tailwindcss";`
- Variable naming mismatch (`--space-8` vs `--spacing-8`)
- Double-wrapped colors (`rgb(var(--color))` when variable is already RGB/OKLCH)
- Dynamic class interpolation (`bg-${color}-500`) — Tailwind purges these; use mapping objects or full class names
- `@apply` in scoped styles without `@reference`
- Relying on gradient reset in dark mode
- Assuming border default color (now `currentColor`)
- `hidden` attribute now overrides display utilities

---

## 5. Motion Standards (from `avant-garde-design-v4/14-animation-standards.md`)

### Three core principles

Every animation must serve: (1) **Feedback** (confirm action), (2) **Context** (show relationships), (3) **Narrative** (guide the eye).

### Duration & Easing Reference (EXACT)

| Type          | Duration | Easing (cubic-bezier) | Use Case                      |
| ------------- | -------- | --------------------- | ----------------------------- |
| Micro         | 150ms    | `(0.4, 0, 0.2, 1)`    | Hover states, toggle icons    |
| Standard      | 300ms    | `(0.4, 0, 0.2, 1)`    | Modals, drawer entry/exit     |
| Dramatic      | 500ms+   | `(0.25, 1, 0.36, 1)`  | Hero entry, major transitions |
| Reveal        | 900ms    | `(0.22, 1, 0.36, 1)`  | Section reveals on scroll     |
| Flip          | 900ms    | `(0.4, 0.2, 0.2, 1)`  | Coach card 3D flip            |
| Sticky snap   | 600ms    | `(0.22, 1, 0.36, 1)`  | Sticky CTA bar slide          |
| Carousel snap | 700ms    | `(0.16, 1, 0.3, 1)`   | Card snap after drag          |

### Performance guardrails (mandatory)

- [ ] **Compositor only:** animate `transform` and `opacity` — never `width`, `height`, `top`, `margin`
- [ ] **No `all`:** list specific properties in transitions
- [ ] **Hardware acceleration:** `will-change: transform` sparingly
- [ ] **60fps:** maintain on average mobile hardware
- [ ] **Pause off-screen:** IntersectionObserver gates all animations
- [ ] **Respect reduced motion:** disable entirely, not just slow

### Stagger config

```tsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.1, delayChildren: 0.3 } },
};
const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: { y: 0, opacity: 1, transition: { duration: 0.5, ease: 'easeOut' } },
};
```

---

## 6. Accessibility (WCAG AAA, from `avant-garde-design-v4/04-accessibility-checklist.md`)

### AAA Requirements (mandatory for IRONFORGE)

- Contrast: **7:1 normal text, 4.5:1 large text**
- Visual presentation: width ≤ 80 chars, NOT justified, line spacing ≥ 1.5
- Touch targets: ≥ **44×44 CSS pixels**
- Reading level: lower secondary education
- No content flashes >3 times per second

### Skip link pattern

```tsx
<a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2">
  Skip to main content
</a>
<main id="main-content">{/* Content */}</main>
```

### Focus ring

```tsx
className =
  'focus-visible:outline-hidden focus-visible:ring-2 focus-visible:ring-[var(--color-accent)] focus-visible:ring-offset-2';
```

### Icon-only button

```tsx
<button
  aria-label="Close dialog"
  className="p-3 focus-visible:ring-2 focus-visible:ring-[var(--color-accent)]"
>
  <XIcon aria-hidden="true" className="h-5 w-5" />
</button>
```

### Form a11y

- Always label inputs: `<label htmlFor="email">…</label><input id="email" />`
- Mark invalid: `aria-invalid={!!fieldState.error}` + `aria-describedby` pointing to error id
- Required fields: visual `*` + `<span className="sr-only">(required)</span>`
- Group related fields with `<fieldset>` + `<legend>`

### Live regions

```tsx
<div aria-live="polite" aria-atomic="true">{message}</div>
<div aria-live="assertive">{error}</div>
```

### `useReducedMotion` hook (verbatim)

```tsx
'use client';
import { useEffect, useState } from 'react';

export function useReducedMotion(): boolean {
  const [reduced, setReduced] = useState(false);
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    const onChange = () => setReduced(mediaQuery.matches);
    onChange();
    mediaQuery.addEventListener('change', onChange);
    return () => mediaQuery.removeEventListener('change', onChange);
  }, []);
  return reduced;
}
```

### Legal

ADA Title II Compliance effective **April 24, 2026** — federal law requires WCAG 2.1 AA. We target AAA.

---

## 7. Mobile Navigation (from `avant-garde-design-v4/07-mobile-navigation.md` + `08-mobile-nav-debugging.md`)

### Viewport meta (verbatim)

```html
<meta
  name="viewport"
  content="width=device-width, initial-scale=1, maximum-scale=5, viewport-fit=cover"
/>
```

### Symmetrical breakpoints (CRITICAL)

Desktop nav `hidden md:flex` paired with mobile trigger `md:hidden`. **Never** use different breakpoints.

### Touch targets

≥ 44×44px. Minimum `p-3 focus-visible:ring-2`.

### Z-index scale

```css
--z-overlay: 400;
--z-modal: 500;
```

Mobile menu overlay: `fixed inset-0 z-overlay bg-background/80 backdrop-blur-sm`.

### Never use `<div>` for menu triggers

Use `<button>` with `aria-expanded`, `aria-controls`, `aria-label`.

### Body scroll lock (mandatory when menu open)

```tsx
useEffect(() => {
  if (isOpen) document.body.style.overflow = 'hidden';
  else document.body.style.overflow = 'unset';
}, [isOpen]);
```

### Use `dvh` not `vh`

Mobile Safari shifts UI bar. Use `min-h-dvh` (Dynamic Viewport Height).

### Debugging taxonomy (8 classes)

| Class               | Symptom                                            | Fix                                             |
| ------------------- | -------------------------------------------------- | ----------------------------------------------- |
| A: Z-Index Abyss    | Button visible but not clickable                   | `isolation: isolate` on parent                  |
| B: Display Mismatch | Menu disappears at 768px but doesn't show at 767px | Symmetrical breakpoints                         |
| C: Prop Drop        | `onClick` doesn't fire                             | Check event propagation, `pointer-events: none` |
| D: Viewport Shift   | Menu height cut off                                | Use `min-h-dvh`                                 |
| E: Focus Lock       | Can't tab through menu                             | Check `aria-hidden` state                       |
| F: Hydration Ghost  | Works in dev, fails in prod                        | Check Server vs Client content                  |
| G: Layout Warp      | Background scrolls                                 | Body scroll lock                                |
| H: Touch Delay      | Feels laggy                                        | Add `passive: true` to listeners                |

---

## 8. Performance Budgets (Q4 THE VISIONARY, from `avant-garde-design-v4/15-performance-budgets.md`)

| Metric                    | Budget                  |
| ------------------------- | ----------------------- |
| Initial JS bundle         | < 250 KB gzipped        |
| First Contentful Paint    | < 1.2s                  |
| Largest Contentful Paint  | < 2.0s                  |
| Time to Interactive       | < 2.5s                  |
| Cumulative Layout Shift   | < 0.1                   |
| Animation Frame Rate      | 60fps                   |
| Lighthouse Performance    | 85–90+                  |
| Lighthouse Accessibility  | WCAG AA (we target AAA) |
| Lighthouse Best Practices | 100                     |
| Lighthouse SEO            | 100                     |

### Lighthouse CI assertions

```js
'categories:performance': ['error', { minScore: 0.9 }],
'categories:accessibility': ['error', { minScore: 1.0 }],
'categories:best-practices': ['error', { minScore: 1.0 }],
'categories:seo': ['error', { minScore: 1.0 }],
'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
```

### Core Web Vitals fixes

- **CLS:** reserve space using `aspect-ratio` + placeholder background
- **LCP:** preload fonts, hero images get `priority` attribute
- **INP:** break up long JS tasks via `requestIdleCallback`; < 200ms interaction latency

---

## 9. 5-Layer Architecture (from `nextjs16-react19-next-auth5-drizzle-orm`)

```
Layer 0  src/proxy.ts            → Edge cookie check, redirect. NO DB. NO logic. Edge runtime.
Layer 1  src/app/                → Route structure, metadata, Suspense. Layouts must NOT fetch data.
Layer 2  src/features/           → UI composition, data binding, mutations
Layer 3  src/features/*/domain/  → Pure business logic. No Next.js or DB runtime imports (import type only)
Layer 4  src/lib/                → Infrastructure: Drizzle, Auth.js, Inngest, R2, Stripe, AI providers.
```

**Golden Rule:** A lower layer may never import from a higher layer. Domain may import types from Infrastructure but never runtime code.

---

## 10. Custom Hooks (verbatim from `nextjs16-react19-next-auth5-drizzle-orm`)

### `useScrolled`

```tsx
'use client';
import { useEffect, useState } from 'react';

export function useScrolled(threshold = 10): boolean {
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > threshold);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, [threshold]);
  return scrolled;
}
```

### `useReveal`

```tsx
'use client';
import { useEffect, useRef, useState } from 'react';

interface UseRevealOptions {
  threshold?: number; // Default 0.15
  rootMargin?: string; // Default '0px 0px -50px 0px'
  once?: boolean; // Default true
}

export function useReveal<T extends HTMLElement = HTMLDivElement>(
  options: UseRevealOptions = {},
): { ref: React.RefObject<T | null>; revealed: boolean } {
  const { threshold = 0.15, rootMargin = '0px 0px -50px 0px', once = true } = options;
  const ref = useRef<T>(null);
  const [revealed, setRevealed] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      (entries) => {
        const [entry] = entries;
        if (!entry) return;
        if (entry.isIntersecting) {
          setRevealed(true);
          if (once) observer.disconnect();
        } else if (!once) {
          setRevealed(false);
        }
      },
      { threshold, rootMargin },
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, [threshold, rootMargin, once]);

  return { ref, revealed };
}
```

### `useReducedMotion` — see §6 above

### `ScrollReveal` component

```tsx
'use client';
export function ScrollReveal({ children, delay = 0, className, as = 'div' }: ScrollRevealProps) {
  const { ref, revealed } = useReveal<HTMLElement>();
  const Tag = as as ElementType;
  return (
    <Tag
      ref={ref}
      data-reveal=""
      data-revealed={revealed ? 'true' : 'false'}
      style={{ '--reveal-delay': `${delay}ms` } as React.CSSProperties}
      className={cn(className)}
    >
      {children}
    </Tag>
  );
}
```

### CSS for `[data-reveal]`

```css
[data-reveal] {
  opacity: 0;
  transform: translateY(20px);
  transition:
    opacity 0.6s ease-out,
    transform 0.6s ease-out;
  transition-delay: var(--reveal-delay, 0s);
}
[data-reveal][data-revealed='true'] {
  opacity: 1;
  transform: translateY(0);
}
```

---

## 11. shadcn/ui + Radix Patterns (from `ui-styling`)

### Component installation

```bash
pnpm dlx shadcn@latest init        # Generates components.json
pnpm dlx shadcn@latest add button card dialog sheet input label textarea
```

### `cn()` helper (mandatory)

```tsx
// src/lib/utils.ts
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
```

### Button with CVA variants

```tsx
const buttonVariants = cva(
  'inline-flex items-center justify-center gap-2 rounded-md text-sm font-medium whitespace-nowrap transition-all outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-accent)] focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-[var(--color-accent)] text-black hover:bg-[var(--color-accent-bright)]',
        destructive: 'bg-red-600 text-white hover:bg-red-700',
        outline: 'border border-[var(--color-border-light)] bg-transparent hover:bg-white/[0.04]',
        secondary: 'bg-[var(--color-silver)] text-black hover:bg-white',
        ghost: 'hover:bg-white/[0.04]',
        link: 'text-[var(--color-accent)] underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 px-3 text-sm',
        lg: 'h-12 px-6 text-lg',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: { variant: 'default', size: 'default' },
  },
);
```

### Wrapping rules

1. Use `React.forwardRef`
2. Spread `...props` last so consumer overrides win
3. Merge classes via `cn(...)` — never string concatenation
4. Use `className` prop as override channel
5. Base classes use semantic tokens, not raw colors

### Never do

- Strip focus indicators (`focus:outline-none` alone)
- Use `<div onClick>` for interactive elements
- Remove Radix ARIA wiring
- Build a Dialog without the Radix primitive
- Use `focus:` for ring styling (always `focus-visible:`)

---

## 12. Auth.js v5 + Drizzle Patterns (from `nextjs16-react19-next-auth5-drizzle-orm`)

### Critical rules

- `trustHost: true` mandatory (prevents P0 production outage with reverse proxies)
- Auth route handler must be `force-dynamic` (prevents prerender failure)
- `verifySession()` throws redirect — wrong for JSON/SSE. API routes use `auth()` → null → 401 JSON
- DrizzleAdapter rejects Proxy-based db — use real Drizzle client
- `postgres()` defers connection until first query — safe to eager instantiate

### Auth-first Server Action pattern

```tsx
'use server';
export async function createProjectAction(input: z.infer<typeof Schema>) {
  const session = await verifySession({ redirectTo: '/create' });
  const userId = session.user?.id;
  if (!userId) return { success: false, code: 'UNAUTHORIZED' };
  const parsed = Schema.safeParse(input);
  if (!parsed.success) return { success: false, code: 'VALIDATION' };
  // Business logic...
}
```

### API route auth pattern

```tsx
export async function GET(req: NextRequest) {
  const session = await auth();
  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  // ...
}
```

### `queries.ts` Boundary pattern

```tsx
// src/features/projects/queries.ts
export async function getProject(projectId: string, userId: string) {
  const [row] = await db
    .select({ ... })
    .from(projects)
    .leftJoin(videos, eq(videos.projectId, projects.id))
    .where(eq(projects.id, projectId))
    .limit(1);
  if (row && row.userId !== userId) return null;
  return row;
}
```

### Domain isolation

```tsx
// src/features/pipeline/domain/analyze-story.ts
// NO Next.js imports, NO DB imports — only types
import type { Project } from '@/lib/db/schema';

export async function analyzeStory(story: string): Promise<AnalysisResult> {
  // Pure business logic — no side effects
}
```

---

## 13. SSE Streaming Pattern (verbatim, from `nextjs16-react19-next-auth5-drizzle-orm`)

### Server: 2s polling with terminal-status close

```typescript
const interval = setInterval(async () => {
  const current = await readProjectProgress(projectId);
  controller.enqueue(encoder.encode(formatSseMessage(current)));
  if (TERMINAL_STATUSES.has(current.status)) {
    controller.close();
    clearInterval(interval);
  }
}, 2000);
```

### Client: exponential backoff (1s → 2s → 4s, max 3 attempts)

```tsx
'use client';
import { useEffect, useState } from 'react';

const MAX_RECONNECT_ATTEMPTS = 3;
const BASE_BACKOFF_MS = 1000;

function backoffDelay(attempt: number): number {
  return BASE_BACKOFF_MS * Math.pow(2, attempt);
}

// Full hook in skills knowledge base — used for booking status, AI asset generation progress
```

### `maxDuration`

```ts
export const maxDuration = 900; // Vercel Pro
```

---

## 14. Env Validation (Zod, from `nextjs16-react19-next-auth5-drizzle-orm`)

### Anti-patterns (mandatory)

- ❌ `process.env.*` direct access — always import `env` from `@/lib/env`
- ❌ Zod `.url()` rejects `postgresql://` — use `.refine()` with postgres scheme check
- ❌ Build fails without env vars — module has build-context fallback (returns placeholders when `NEXT_PHASE === 'phase-production-build'` or `NODE_ENV === 'test'`)

### Verbatim pattern

```typescript
// ❌ WRONG — typos silently return undefined
const apiKey = process.env.OPENAI_APIKEY; // Missing underscore — undefined!

// ✅ CORRECT — Zod-validated env module
import { env } from '@/lib/env';
const apiKey = env.OPENAI_API_KEY; // Typos fail at module load
```

### Format validation example

```typescript
REPLICATE_SDXL_MODEL: z
  .string()
  .regex(/^[a-z0-9-]+\/[a-z0-9-]+:[a-f0-9]{8,}$/, 'Must match owner/model:sha format')
  .default('stability-ai/sdxl:39ed52f2...'),
```

---

## 15. Security Headers (canonical for IRONFORGE)

### `next.config.ts` `headers()` function

```ts
const CSP_POLICY = [
  "default-src 'self'",
  "script-src 'self' 'unsafe-inline'",  // Next.js App Router requires 'unsafe-inline'
  "style-src 'self' 'unsafe-inline'",
  "img-src 'self' data: https:",
  "font-src 'self'",
  "connect-src 'self' https://api.stripe.com https://js.stripe.com",  // Stripe client
  "media-src 'self'",
  "frame-ancestors 'none'",
  "base-uri 'self'",
  "form-action 'self'",
  "object-src 'none'",
].join('; ');

async headers() {
  return [{
    source: '/(.*)',
    headers: [
      { key: 'X-Frame-Options', value: 'DENY' },
      { key: 'X-Content-Type-Options', value: 'nosniff' },
      { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
      { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
      { key: 'Content-Security-Policy', value: CSP_POLICY },
      { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
    ],
  }];
}
```

**Note:** `'unsafe-eval'` (currently in the cloned `next.config.ts`) is removed — not needed for production Next.js 16.

---

## 16. Testing Patterns (from `nextjs16-react19-next-auth5-drizzle-orm`)

### Vitest anti-patterns

- ❌ `vi.mock('module', () => ({ x: mockFn }))` where `mockFn` is hoisted — use `vi.hoisted()`
- ❌ Arrow function mock constructors — use `class` syntax
- ❌ JSX in `.test.ts` files — rename to `.test.tsx`
- ❌ Direct `process.env.NODE_ENV = 'test'` — use `vi.stubEnv('NODE_ENV', 'test')`
- ❌ Source-reading tests without stripping comments — `src.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*$/gm, '')`

### `vi.hoisted()` pattern

```typescript
const { mockFn } = vi.hoisted(() => ({ mockFn: vi.fn() }));
vi.mock('module', () => ({ x: mockFn }));
```

### `class` syntax for SDK mocks

```typescript
vi.mock('@aws-sdk/client-s3', () => {
  class MockS3Client {
    send = vi.fn();
  }
  return { S3Client: MockS3Client };
});
```

### Brand-token test pattern

```typescript
// src/tests/unit/brand-tokens.test.ts
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const globalsCss = readFileSync(resolve(__dirname, '../../app/globals.css'), 'utf-8');
const stripped = globalsCss.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*$/gm, '');

const FORBIDDEN_COLORS = ['#7c3aed', '#a855f7', '#8b5cf6', '#3b82f6'];

describe('brand tokens', () => {
  FORBIDDEN_COLORS.forEach((color) => {
    it(`rejects forbidden color ${color}`, () => {
      expect(stripped).not.toContain(color);
    });
  });

  it('defines --color-fg with WCAG AAA contrast on --color-bg', () => {
    expect(stripped).toContain('--color-fg: #f5f5f5');
    expect(stripped).toContain('--color-bg: #0a0a0a');
  });
});
```

### Test factory pattern

```typescript
// src/tests/unit/factories/coach.ts
import type { Coach } from '@/lib/db/schema';

export function getMockCoach(overrides: Partial<Coach> = {}): Coach {
  return {
    id: '00000000-0000-0000-0000-000000000001',
    slug: 'marcus-steel',
    name: 'Marcus Steel',
    title: 'Head of Strength',
    bio: '...',
    certifications: ['NSCA-CSCS', 'FRC'],
    specialties: ['Hypertrophy', 'Powerlifting'],
    signatureWorkout: 'Conjugate Max Effort',
    portraitKey: 'coaches/marcus.jpg',
    yearsExp: 12,
    order: 0,
    published: true,
    createdAt: new Date('2024-01-01'),
    updatedAt: new Date('2024-01-01'),
    ...overrides,
  };
}
```

### Quality gate (run before every commit)

```bash
pnpm lint && pnpm typecheck && pnpm test && pnpm build
```

---

## 17. T0–T8 Lessons (from `nextjs16-react19-next-auth5-drizzle-orm` Remediation Sprint 2)

| ID  | Lesson                                                                                                                                              |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| T0  | `pnpm-workspace.yaml` requires `packages: ['.']` field even for single-package repos (pnpm 9+)                                                      |
| T1  | Client components must NEVER import `@/lib/storage/r2` at module level — env validation crashes browser. Server Component signs URL, passes as prop |
| T2  | `trustHost: true` mandatory for reverse-proxy Auth.js v5 deployments                                                                                |
| T3  | `OPENAI_API_KEY.startsWith('sk-')` is NOT too strict — `sk-proj-*`, `sk-svcacct-*`, `sk-admin-*` all start with `sk-`                               |
| T4  | Hardcoded third-party model IDs are an operational liability — move to env vars with format validation                                              |
| T5  | Silent fail-open policies are dangerous — add `moderationSkipped` field + `console.warn` for observability                                          |
| T6  | SSE on Vercel needs both server-side (`maxDuration: 900`) and client-side (exponential backoff) resilience                                          |
| T7  | `putObject` needs a size guard — `MAX_PUT_OBJECT_BYTES = 500 MB` fails fast instead of OOM                                                          |
| T8  | CI should run full quality gate — `lint-staged` only checks staged files                                                                            |

---

## 18. Configuration Files (canonical templates)

### `tsconfig.json` — already correct in cloned repo

- `strict: true`, `noUncheckedIndexedAccess: true`, `noImplicitOverride: true`
- `noUnusedLocals: true`, `noUnusedParameters: true`, `verbatimModuleSyntax: true`
- `paths: { "@/*": ["./src/*"] }`
- `exclude: ["node_modules", "skills", "docs"]`

### `eslint.config.mjs` — already correct, but tighten

- Change `react-hooks/exhaustive-deps: 'warn'` → `'error'`
- Add `no-restricted-imports` rule to enforce 5-layer architecture (domain purity)

### `postcss.config.mjs` — already correct

```js
const config = { plugins: { '@tailwindcss/postcss': {} } };
export default config;
```

### `pnpm-workspace.yaml` (MISSING — must create)

```yaml
packages:
  - '.'
allowBuilds:
  esbuild: true
  sharp: true
onlyBuiltDependencies:
  - sharp
  - esbuild
```

### `.gitignore` — FIX REQUIRED

Current line `#.env*` is commented out — uncomment:

```gitignore
.env*
!.env.example
```

---

## 19. Existing Scaffolding Audit (from scan)

### Present and correct

- `package.json` — all dependencies declared, engines pinned
- `tsconfig.json` — strict, paths configured
- `eslint.config.mjs` — flat config, plugins loaded
- `postcss.config.mjs` — Tailwind v4
- `vitest.config.ts` — jsdom, alias, coverage
- `playwright.config.ts` — Chromium, projects defined
- `drizzle.config.ts` — postgresql, schema path
- `.gitignore` — has env leak bug

### Missing (must create)

- `src/app/layout.tsx`, `src/app/page.tsx`, `src/app/globals.css`
- `src/lib/utils.ts` (cn helper)
- `src/lib/env.ts` (Zod validation)
- `src/lib/db/schema/index.ts`, `src/lib/db/client.ts`, `src/lib/db/seed.ts`
- `src/tests/setup.ts`
- `src/tests/unit/`, `src/tests/e2e/`
- `src/auth.ts`, `src/app/api/auth/[...nextauth]/route.ts`
- `src/inngest/client.ts`, `src/app/api/inngest/route.ts`
- `src/lib/{bcrypt,stripe,replicate,upstash}.ts`
- `src/components/ui/` (shadcn primitives)
- `public/` (favicon, og, fonts)
- `.env.example`, `.env.local`
- `.husky/pre-commit`
- `.prettierrc.json`
- `.editorconfig`, `.nvmrc`, `.npmrc`
- `.github/workflows/ci.yml`
- `pnpm-workspace.yaml`
- `components.json` (shadcn config)

### Bugs to fix

1. `next.config.ts` — comments say "StoryIntoVideo" (lines 4, 14) — rebrand
2. `playwright-live.config.ts` — `baseURL: 'https://storyintovideo.jesspete.shop'` — rebrand
3. `playwright.config.ts` — project testMatch patterns reference StoryIntoVideo specs — rename
4. `.gitignore` — `#.env*` commented out → uncomment
5. `next.config.ts` CSP — remove `'unsafe-eval'` from `script-src`
6. `next.config.ts` — add `connect-src https://api.stripe.com https://js.stripe.com`
7. `drizzle.config.ts` — `import 'dotenv/config'` redundant with dotenv-cli wrapping — keep but document

---

## 20. Skill Load Status

| Skill                                     | Read?                   | Knowledge captured?                     |
| ----------------------------------------- | ----------------------- | --------------------------------------- |
| `avant-garde-design-v4`                   | ✅ Full + 16 references | §1–8, §10, §15                          |
| `nextjs16-tailwind4`                      | ✅ Full                 | §2, §4, §5                              |
| `tailwind-patterns`                       | ✅ Full                 | §4                                      |
| `ui-styling`                              | ✅ Full + 7 references  | §11                                     |
| `nextjs16-react19-next-auth5-drizzle-orm` | ✅ Full (2693 lines)    | §9, §10, §12, §13, §14, §16, §17        |
| `frontend-design`                         | ⏳ Pending              | Will load in Phase 3 (animations)       |
| `frontend-ui-engineering`                 | ⏳ Pending              | Will load in Phase 4 (components)       |
| `security-and-hardening`                  | ⏳ Pending              | Will load in Phase 9 (auth + admin)     |
| `vulnerability-scanner`                   | ⏳ Pending              | Will load in Phase 10 (security QA)     |
| `code-quality-standards`                  | ⏳ Pending              | Will load in Phase 10 (Six-Axis review) |
| `nextjs-react-expert`                     | ⏳ Pending              | Will load in Phase 10 (performance)     |
| `testing-patterns`                        | ⏳ Pending              | Will load in Phase 5 (test factory)     |
| `webapp-testing-journey`                  | ⏳ Pending              | Will load in Phase 10 (E2E)             |
| `web-frameworks`                          | ⏳ Pending              | Will load in Phase 2 (App Router)       |
| `super-frontend-design`                   | ⏳ Pending              | Will load in Phase 4 (master reference) |
| `ui-ux-pro-max`                           | ⏳ Pending              | Will load in Phase 4 (UI specs)         |
| `visual-design-foundations`               | ⏳ Pending              | Will load in Phase 1 (typography)       |

---

_End of Skills Knowledge Base v1.0. Live document — updated as new skills are loaded per phase._
