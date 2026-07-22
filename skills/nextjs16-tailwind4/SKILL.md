---
name: nextjs16-tailwind4
description: Luxury-grade Next.js 16 + React 19 + TypeScript strict with Tailwind CSS v4 CSS-first @theme, Radix UI (shadcn), and Framer Motion. Covers App Router, Server Components, avant-garde anti-generic UI design, OWASP 2025 security audits, Core Web Vitals performance optimization, WCAG AAA accessibility, mobile navigation debugging, and code review for high-end production web experiences.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, SearchWeb, FetchURL or similar tools available to you
---

# Next.js + Tailwind CSS v4 Luxury Web Development

> **Stack**: Next.js 16.1.4+ • React 19.2.3+ • Tailwind CSS v4.1.18+ • TypeScript 5.9+ • Radix UI (shadcn) • Framer Motion 12.29.0+
> **Philosophy**: Avant-Garde UI Design • Intentional Minimalism • Anti‑Generic • WCAG AAA

---

## When to Use This Skill

- Building Next.js applications with Tailwind CSS v4’s CSS‑first architecture
- Creating luxury, high‑end, or conceptually distinctive web experiences
- Implementing shadcn/ui components with custom, branded styling
- Adding Framer Motion animations while respecting accessibility constraints
- Conducting deep code reviews for React/Next.js/TypeScript projects
- Performing full‑stack security audits with an OWASP 2025 lens
- Optimising performance for production‑grade deployments
- Debugging Tailwind v4 visual discrepancies and mobile navigation failures

---

## 1. Project Architecture

### 1.1 Tech Stack Overview

```yaml
Core:
  next: 16.1.4+ (App Router, Server Components, Turbopack)
  react: 19.2.3+
  typescript: 5.9+ (strictest possible config)

Styling & UI:
  tailwindcss: 4.1.18+            # CSS-first, no tailwind.config.*
  @tailwindcss/vite: 4.1.18+      # Vite plugin (superior performance)
  @tailwindcss/postcss: 4.1.18+   # PostCSS plugin (legacy)
  radix-ui primitives              # Accessible headless components
  shadcn/ui: 2.x                   # Tailwind v4 compatible
  framer-motion: 12.29.0+
  class-variance-authority: latest
  tailwind-merge: ^3
  clsx: ^2

Forms & Validation:
  react-hook-form: 7.x
  zod: 3.x
  @hookform/resolvers: 5.x

Backend / Data (optional):
  prisma: 6.x
  bcryptjs: 2.x
  jose: 5.x

Development:
  eslint: 9.x with flat config
  prettier: 3.x + prettier-plugin-tailwindcss
  vitest: 2.x
  playwright: 1.x
```

### 1.2 Directory Structure

```
project-root/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx          # Root layout, fonts, metadata
│   │   ├── page.tsx            # Home page composition
│   │   ├── globals.css         # Tailwind v4 theme + tokens
│   │   └── (routes)/           # Route groups
│   │
│   ├── components/
│   │   ├── layout/             # Navbar, Footer, Shell, MobileNavigation
│   │   ├── sections/           # Hero, Features, Showcase, etc.
│   │   └── ui/                 # shadcn primitives (Button, Input, Card, Sheet, …)
│   │
│   ├── lib/
│   │   ├── utils.ts            # cn(), formatters, helpers
│   │   └── hooks/              # useScrollSpy, useReducedMotion, etc.
│   │
│   ├── data/                   # Static content (destinations, collections)
│   └── types/                  # Global TypeScript types
│
├── public/                     # Static assets (images, fonts)
├── docs/                       # Design decisions, guidelines
├── prisma/                     # Database schema (if using)
├── next.config.ts              # Next.js configuration
├── tsconfig.json               # Strict TypeScript config
└── package.json
```

---

## 2. Tailwind CSS v4 CSS‑First Configuration

### 2.1 The CSS‑First Paradigm

**No `tailwind.config.js` or `tailwind.config.ts`.** Tailwind v4 is configured entirely inside your CSS entry point. All theme tokens, custom animations, and utilities live within the `@theme` directive.

```css
/* src/app/globals.css */
@import "tailwindcss";

/* ============================================
   THEME CONFIGURATION
   ============================================ */

@theme {
  /* ── Color Palette ── */
  --color-void: #050506;
  --color-void-light: oklch(0.13 0.01 240);
  --color-aurora-cyan: oklch(0.87 0.16 184);
  --color-aurora-purple: oklch(0.53 0.21 283);
  --color-aurora-magenta: oklch(0.68 0.24 351);
  --color-champagne: oklch(0.85 0.07 84);
  --color-champagne-dark: oklch(0.67 0.06 76);

  /* ── Typography ── */
  --font-sans: "Geist", "Inter", system-ui, sans-serif;
  --font-serif: "Instrument Serif", "Georgia", serif;

  /* ── Extended Spacing (dynamic values are unlimited) ── */
  --spacing-18: 4.5rem;
  --spacing-88: 22rem;

  /* ── Keyframes & Animations ── */
  --animate-aurora-slow: aurora-slow 20s ease-in-out infinite;
  --animate-float-slow: float-slow 25s ease-in-out infinite;

  @keyframes aurora-slow {
    0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.8; }
    33% { transform: translate(30%, 20%) scale(1.1); opacity: 0.6; }
    66% { transform: translate(-20%, 30%) scale(0.9); opacity: 0.7; }
  }

  @keyframes float-slow {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(5deg); }
  }
}

/* ============================================
   BASE STYLES
   ============================================ */

@layer base {
  * {
    border-color: currentColor;
  }
  html {
    scroll-behavior: smooth;
  }
  body {
    background-color: var(--color-void);
    color: var(--color-slate-100);
    font-family: var(--font-sans);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
  h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-serif);
  }
}

/* ============================================
   CUSTOM UTILITIES
   ============================================ */

@utility text-balance {
  text-wrap: balance;
}

@utility glass-panel {
  background-color: oklch(0.13 0.01 240 / 0.3);
  backdrop-filter: blur(12px);
  border: 1px solid oklch(0.2 0.01 240 / 0.5);
}

@utility aurora-gradient {
  background: linear-gradient(
    135deg,
    var(--color-aurora-cyan) 0%,
    var(--color-aurora-purple) 50%,
    var(--color-aurora-magenta) 100%
  );
}
```

### 2.2 Installation & Build Tools

**Remove v3 remnants, install v4:**

```bash
npm uninstall tailwindcss postcss-import autoprefixer
npm install tailwindcss@latest @tailwindcss/vite   # Vite (recommended)
# Or if using PostCSS:
npm install tailwindcss@latest @tailwindcss/postcss
```

**Vite configuration (recommended, superior performance):**

```javascript
// vite.config.js
import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [tailwindcss()],
});
```

**PostCSS legacy configuration:**

```javascript
// postcss.config.mjs
export default {
  plugins: ["@tailwindcss/postcss"],
};
```

### 2.3 Critical v3 → v4 Migration Map

All `bg-opacity-*`, `text-opacity-*` etc. are gone; use opacity modifiers directly (e.g., `bg-red-500/50`).  
Gradient names changed from `bg-gradient-to-*` to `bg-linear-to-*`.  
Shadow/Blur/Rounded scales are now explicit: `shadow-sm` → `shadow-xs`, `shadow` → `shadow-sm`, etc.  

**Complete reference table (the most common transformations):**

| v3 Utility | v4 Replacement | Notes |
|------------|----------------|-------|
| `bg-opacity-50` | `bg-color/50` | Opacity modifier |
| `text-opacity-75` | `text-color/75` | |
| `shadow-sm` | `shadow-xs` | Explicit scale |
| `shadow` | `shadow-sm` | |
| `blur-sm` | `blur-xs` | |
| `blur` | `blur-sm` | |
| `rounded-sm` | `rounded-xs` | |
| `rounded` | `rounded-sm` | |
| `bg-gradient-to-r` | `bg-linear-to-r` | New gradient type |
| `bg-gradient-to-br` | `bg-linear-to-br` | |
| `outline-none` | `outline-hidden` | Semantic clarity |
| `ring` | `ring-3` | Must specify width |
| `flex-shrink-*` | `shrink-*` | Shortened |
| `flex-grow-*` | `grow-*` | Shortened |
| `overflow-ellipsis` | `text-ellipsis` | Renamed |

**CSS variable syntax evolved:**

```html
<!-- v3: square brackets -->
<div class="bg-[--brand]"></div>

<!-- v4: parentheses for CSS variables -->
<div class="bg-(--brand)"></div>
```

**Variant stacking now left‑to‑right (v4 behaviour):**
```html
<!-- v3: first:*:pt-0 -->
<!-- v4: *:first:pt-0 -->
<ul class="py-4 *:first:pt-0 *:last:pb-0">
  <li>...</li>
  <li>...</li>
</ul>
```

**`@layer utilities` is replaced by `@utility`:**
```css
@utility tab-4 {
  tab-size: 4;
}
```

### 2.4 Advanced v4 Capabilities (Luxury‑Grade Enhancements)

- **Container Queries**: Built‑in `@container` and `@sm:`, `@max-md:`, etc.  
  Enables truly component‑driven responsive behaviour, perfect for editorial layouts.
- **Dynamic values**: Any number becomes a spacing/column/grid value (`w-17`, `grid-cols-15`).
- **Data attribute variants**: `data-current:opacity-100` for state‑driven styling without JavaScript.
- **OKLCH color space**: Provides wider gamut and perceptually uniform gradients; use `oklch(...)` for all brand tokens.
- **Gradient interpolation modifiers**: `bg-linear-to-r/oklch` for smooth, vibrant gradients.
- **Inset shadows & rings**: `inset-shadow-*`, `inset-ring-*` add depth while maintaining minimalism.

### 2.5 Avoiding Common V4 Pitfalls

- **No `@apply` in scoped styles without `@reference`**: In CSS Modules or SFC, you may need `@reference "../../app.css";` before `@apply`.
- **@source scanning**: Explicitly limit scanning scope for monorepos and `node_modules` to prevent build slowdown.
- **Gradient persistence**: v4 gradients don’t reset automatically on dark mode; use `dark:via-none`, etc.
- **Border default color** is now `currentColor`; explicitly set `border-gray-200` if needed.
- **Hidden attribute priority**: `hidden` attribute now overrides display utilities. Remove it to show.

---

## 3. Component Patterns

### 3.1 UI Primitive (shadcn‑style, React 19 ready)

```tsx
// src/components/ui/Button.tsx
import { forwardRef, type ButtonHTMLAttributes } from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-lg font-medium transition-colors focus-visible:outline-hidden focus-visible:ring-2 focus-visible:ring-champagne disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-champagne text-void hover:bg-champagne-dark",
        outline: "border border-slate-700 bg-transparent hover:bg-slate-800",
        ghost: "hover:bg-slate-800",
        link: "underline-offset-4 hover:underline text-champagne",
        luxury: "glass-panel text-white hover:bg-void-light shadow-xs",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-8 px-3 text-sm",
        lg: "h-12 px-6 text-lg",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
);

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  loading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, loading, children, ...props }, ref) => (
    <button
      ref={ref}
      className={cn(buttonVariants({ variant, size }), className)}
      disabled={props.disabled || loading}
      {...props}
    >
      {loading && (
        <span className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
      )}
      {children}
    </button>
  )
);

Button.displayName = "Button";
```

### 3.2 Luxury Section with Motion & Reduced Motion

```tsx
"use client";

import { motion } from "framer-motion";
import { useReducedMotion } from "@/lib/hooks/useReducedMotion";
import { Button } from "@/components/ui/Button";

export function Hero() {
  const prefersReducedMotion = useReducedMotion();
  const initial = prefersReducedMotion ? {} : { opacity: 0, scale: 0.95, y: 30 };

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Aurora background */}
      <motion.div
        initial={initial}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 1.2, ease: [0.0, 0.0, 0.2, 1] }}
        className="absolute inset-0 aurora-gradient opacity-15 blur-3xl"
      />
      <div className="relative z-10 container mx-auto px-4 text-center">
        <motion.h1
          initial={initial}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="text-5xl md:text-7xl lg:text-8xl font-serif text-white mb-6"
        >
          Beyond First Class
        </motion.h1>
        <motion.p
          initial={initial}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="text-xl text-slate-400 max-w-2xl mx-auto mb-8"
        >
          Curated journeys for those who refuse the ordinary.
        </motion.p>
        <motion.div
          initial={initial}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
        >
          <Button variant="luxury" size="lg">Begin Your Journey</Button>
        </motion.div>
      </div>
    </section>
  );
}
```

### 3.3 Form Component (React Hook Form + Zod)

```tsx
// src/components/ui/Input.tsx
import { forwardRef, type InputHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, ...props }, ref) => (
    <div className="space-y-2">
      {label && (
        <label className="text-sm font-medium text-slate-300">
          {label}
          {props.required && <span className="text-aurora-magenta ml-1">*</span>}
        </label>
      )}
      <input
        ref={ref}
        className={cn(
          "flex h-10 w-full rounded-lg border border-slate-700 bg-slate-900/50 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:outline-hidden focus:ring-2 focus:ring-champagne",
          error && "border-aurora-magenta focus:ring-aurora-magenta",
          className
        )}
        {...props}
      />
      {error && <p className="text-sm text-aurora-magenta">{error}</p>}
    </div>
  )
);

Input.displayName = "Input";
```

### 3.4 useReducedMotion Hook

```tsx
// src/lib/hooks/useReducedMotion.ts
import { useState, useEffect } from "react";

export function useReducedMotion(): boolean {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    const mql = window.matchMedia("(prefers-reduced-motion: reduce)");
    setPrefersReducedMotion(mql.matches);

    const handler = (e: MediaQueryListEvent) => setPrefersReducedMotion(e.matches);
    mql.addEventListener("change", handler);
    return () => mql.removeEventListener("change", handler);
  }, []);

  return prefersReducedMotion;
}
```

---

## 4. Avant‑Garde Design Principles (Luxury‑Focused)

### 4.1 Anti‑Generic Philosophy

Every interface must have a **distinctive conceptual core**. Reject:
- Bootstrap‑style predictable grids
- "Inter + purple gradient" clichés
- Card‑heavy, AI‑generated monotony
- Homogenised "startup aesthetic"

### 4.2 Bold Aesthetic Directions

Choose (or invent) a clear visual identity:

| Direction | Characteristics |
|-----------|----------------|
| Brutally Minimal | Extreme whitespace, single focal point |
| Maximalist Chaos | Layered textures, bold typographic clashes |
| Retro‑Futuristic | Neon, chrome, geometric patterns |
| Organic / Natural | Soft curves, earthy tones, fluid shapes |
| **Luxury / Refined** | Serif fonts, champagne accents, subtle gradients |
| Editorial / Magazine | Asymmetric layouts, oversized headlines |
| Brutalist / Raw | Exposed structure, monospace, high contrast |
| Art Deco / Geometric | Symmetry, gold/black, stepped forms |

### 4.3 Intentional Minimalism

- Whitespace is structural, not a lack of content.
- Every element must justify its existence.
- Typography hierarchy alone should tell the story.

### 4.4 Multi‑Dimensional Analysis

Every design decision is weighed against:
1. **Psychological** – Does it evoke the desired mood?
2. **Technical** – Does it cause repaints/reflows?
3. **Accessibility** – AAA? Keyboard/screen-reader?
4. **Scalability** – Will this design survive content growth?

### 4.5 Animation Micro‑Guide

```typescript
const DURATION = { instant: 0, fast: 150, normal: 300, slow: 500, dramatic: 800 };
const EASING = {
  entrance: [0.0, 0.0, 0.2, 1],   // decelerate
  exit: [0.4, 0.0, 1.0, 1.0],      // accelerate
  standard: [0.4, 0.0, 0.2, 1],    // symmetric
};
const STAGGER = 50; // ms
```

---

## 5. Code Review Protocol

### 5.1 Pre‑Review Gate

```bash
npx tsc --noEmit && npm run lint && npm test && npm run build
```

### 5.2 Checklist (Critical → Medium)

**Critical**
- [ ] No `any` – use `unknown` or proper types
- [ ] All animations guarded by `useReducedMotion`
- [ ] Focus rings on all interactive elements
- [ ] ARIA labels, semantic HTML
- [ ] Form validation with Zod schemas
- [ ] XSS prevention (no unsanitised `dangerouslySetInnerHTML`)
- [ ] No memory leaks (`useEffect` cleanup)

**High Priority**
- [ ] TypeScript strict mode, `interface` over `type` unless union
- [ ] Early returns, avoid deep nesting
- [ ] Loading & error states everywhere
- [ ] React keys properly used

**Medium**
- [ ] Composition over inheritance
- [ ] Memoisation where beneficial (but trust React Compiler)
- [ ] `next/image` for all static images
- [ ] Semantic HTML (`<nav>`, `<main>`, `<section>`)

### 5.3 Response Flow
```
READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT
```
No performative agreement. YAGNI: grep for usage before adding “proper” features.

---

## 6. Security Audit Protocol (OWASP Top 10 2025)

### 6.1 Checklist

| Category | Checks |
|----------|--------|
| **A01 Broken Access Control** | IDOR, auth checks, SSRF protection, Server Action guards |
| **A02 Security Misconfiguration** | Secure headers, no default creds, no stack traces exposed |
| **A03 Supply Chain** | `npm audit`, lockfile integrity, SBOM |
| **A04 Cryptographic Failures** | bcrypt for passwords, jose for JWT, no hardcoded secrets |
| **A05 Injection** | ORM to prevent SQL injection, XSS via sanitisation |
| **A06 Insecure Design** | Input validation with Zod, business logic reviews |
| **A07 Authentication Failures** | Session management, secure cookies (HttpOnly; SameSite=Strict) |
| **A08 Integrity Failures** | Code signing, dependency verification |
| **A09 Logging & Monitoring** | Failed auth logging, security events |
| **A10 Exceptional Conditions** | Fail‑closed, proper error boundaries |

### 6.2 Next.js Security Headers

```typescript
// next.config.ts
const nextConfig = {
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          { key: "X-Frame-Options", value: "DENY" },
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
          { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
        ],
      },
    ];
  },
};
```

### 6.3 High‑Risk Code Patterns

```typescript
// ❌ NEVER
eval(userInput); new Function(userInput);
"SELECT * FROM users WHERE id = " + userId;
fs.readFile(`./uploads/${userInput}`);  // path traversal

// ✅ ALWAYS validate and sanitise external data
```

---

## 7. Performance Optimisation (Modern Next.js)

### 7.1 Eliminate Waterfalls

```typescript
// ✅ Parallel
const [user, posts] = await Promise.all([getUser(), getPosts()]);
```

### 7.2 Server Components First

Keep components server‑side unless they need hooks, interaction, or browser APIs. Use `"use client"` only at the leaves.

### 7.3 Dynamic Imports for Heavy Lifting

```tsx
const HeavyChart = dynamic(() => import("./HeavyChart"), {
  loading: () => <Skeleton />,
  ssr: false,
});
```

### 7.4 Bundle Size & Imports

- Avoid barrel files (direct imports: `@/components/ui/Button`).
- Use `@next/bundle-analyzer` to inspect.

### 7.5 Image & Font Optimisation

```tsx
<Image src="/hero.jpg" alt="..." width={1200} height={600} priority className="object-cover" />
```
Load fonts with `next/font/google` and the `variable` strategy (see globals.css).

### 7.6 React Compiler & PPR

React 19 ships the compiler; most manual memoisation is now automatic. Next.js Partial Prerendering (PPR) can be enabled for hybrid static/dynamic pages.

---

## 8. Accessibility (WCAG AAA)

### 8.1 Semantic & Focus

- Use `<nav>`, `<main>`, `<section>` with `aria-labelledby`.
- Visible focus rings: `focus-visible:ring-2 focus-visible:ring-champagne`.
- Icon buttons must have `aria-label`.

### 8.2 Contrast (AAA)

- Normal text: 7:1 ratio.
- Large text (18px+): 4.5:1.
- Use OKLCH with adequate lightness for luxury palettes.

### 8.3 Reduced Motion – Absolute Requirement

All animations must check `prefers-reduced-motion`.  
When set to `reduce`, animations should be **disabled entirely**, not just slowed.

---

## 9. Mobile Navigation Patterns (Production‑Grade)

Luxury interfaces demand flawless mobile navigation. Use the following battle‑tested patterns and never fall into the common failure classes.

### 9.1 Symmetrical Breakpoint Logic

```tsx
{/* Desktop */}
<nav className="hidden md:flex items-center gap-8">...</nav>

{/* Mobile trigger */}
<button className="md:hidden" aria-label="Open menu">Menu</button>
```

### 9.2 shadcn Sheet Mobile Nav (Complete)

```tsx
"use client";
import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { Sheet, SheetClose, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/Sheet";
import { NAV_ITEMS } from "@/data/navItems";

export function MobileNavSheet() {
  const [open, setOpen] = React.useState(false);
  const pathname = usePathname();

  React.useEffect(() => { setOpen(false); }, [pathname]);

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" className="md:hidden" aria-label="Open navigation">
          <span className="sr-only">Menu</span>
          <span className="text-2xl leading-none">≡</span>
        </Button>
      </SheetTrigger>
      <SheetContent side="right" className="p-0 w-[300px]">
        <SheetHeader className="border-b border-slate-800 p-6">
          <SheetTitle className="text-white font-serif">Menu</SheetTitle>
        </SheetHeader>
        <nav className="flex flex-col gap-2 p-6">
          {NAV_ITEMS.map(item => (
            <SheetClose key={item.href} asChild>
              <Link href={item.href} className="text-lg font-medium rounded-lg px-3 py-2 hover:bg-slate-800 transition-colors focus-visible:ring-2 focus-visible:ring-champagne">
                {item.label}
              </Link>
            </SheetClose>
          ))}
        </nav>
      </SheetContent>
    </Sheet>
  );
}
```

### 9.3 Root‑Cause Failure Taxonomy (Diagnose Instantly)

| Class | Symptom | Fix |
|-------|---------|-----|
| **A** | No nav on mobile | Add mobile trigger + overlay |
| **B** | Hidden by opacity/visibility | Verify JS toggle & CSS open state |
| **C** | Clipped top items | Overlay must be `position: fixed`; allow `overflow-y: auto` |
| **D** | Behind another layer | Use the z‑index scale (base‑modal) |
| **E** | Breakpoint mismatch | Check viewport meta and breakpoint values |
| **F** | JS error or selector miss | Guard querySelectors; check console |
| **G** | Keyboard unreachable | Use real `<button>`, focus management |
| **H** | Click‑outside race condition | Exclude trigger from outside‑click handler |

### 9.4 Mandatory Accessibility for Overlays

- **Focus trap** when open.
- **Escape** closes.
- **Scroll lock** on body.
- **Focus returns** to trigger on close.

---

## 10. Visual Debugging Playbook (Tailwind v4)

The “flat” or “minimal” look often signals a build or configuration failure.

### 10.1 Top Causes & Immediate Fixes

1. **Legacy `tailwind.config.ts` present** → Rename or delete. All tokens must be in CSS.
2. **Missing `@import "tailwindcss";`** → No utilities generated.
3. **Variable naming mismatch** → `var(--space-8)` vs `var(--spacing-8)`. Use global search.
4. **Double‑wrapped colors** → `rgb(var(--color))` when the variable already is an RGB/OKLCH value → invalid.
5. **Invalid HTML nesting (SVG/React Hydration)** → `<div>` inside `<svg>` → replace with `<g>`.
6. **Dynamic class concatenation** → Tailwind can’t statically analyse; use full class strings or `@utility`.
7. **Production‑only disappearance** → Check `@source` directives, purge not catching dynamic classes.

### 10.2 Diagnostic Decision Tree

```
Nav present in DOM? → No → Class A (missing trigger)
↓ Yes
Computed display:none? → Yes → media query hiding without fallback
↓
Off‑screen or clipped? → Yes → overflow hidden or transform
↓
Behind another layer? → Yes → z‑index / stacking context
↓
JS state not toggling? → Yes → Class F/H
↓
Production only? → Purge/dynamic class issue.
```

---

## 11. Verification Gates

### 11.1 Pre‑Commit

```bash
npx tsc --noEmit && npm run lint && npm test && npm run build
```

### 11.2 Pre‑Deploy

- [ ] Lighthouse > 90 (Performance, Accessibility)
- [ ] No console errors
- [ ] Keyboard‑only operation confirmed
- [ ] Screen‑reader test (VoiceOver/NVDA)
- [ ] Responsive: mobile, tablet, desktop, small‑height
- [ ] All animations obey `prefers-reduced-motion`
- [ ] `npm audit` returns no high/critical
- [ ] Production build validated (`grep` for expected utilities in CSS)

### 11.3 Design Quality Gate

- [ ] Distinctive aesthetic (immediately recognisable)
- [ ] Intentional whitespace
- [ ] Typographic hierarchy is clear without colour
- [ ] Micro‑interactions feel luxurious (150–300 ms)

---

## 12. Project‑Specific Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Components | PascalCase | `Hero.tsx`, `Button.tsx` |
| Hooks | `useCamelCase` | `useScrollSpy.ts` |
| Utils | camelCase | `cn.ts`, `formatCurrency.ts` |
| Constants | SCREAMING_SNAKE | `NAV_ITEMS` |
| Types | PascalCase | `UserProfile` |
| Files | kebab‑case | `concierge-form.tsx` |

Import order: React/Next → Third‑party → Absolute (`@/`) → Relative.

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| aesthetic | Deep design analysis, inspiration workflows |
| code‑review | Detailed feedback handling |
| vulnerability‑scanner | Threat modelling, deep SAST |
| nextjs‑react‑expert | Advanced performance tuning |
| tailwind‑patterns | Utility composition patterns |
| ui‑styling | shadcn/ui guidance |

> **Luxury is in the details.** Every pixel and every line of code must reflect intention, refinement, and a relentless rejection of the generic.
