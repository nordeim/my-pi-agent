# Tailwind CSS v4 Deep Dive

## Overview of v4 Architecture

Tailwind CSS v4 represents a fundamental shift from JavaScript-based configuration to CSS-first configuration. This eliminates the `tailwind.config.js` file entirely and moves all customization into CSS using the `@theme` directive.

### Key Changes

| Aspect | v3 | v4 |
|--------|----|----|
| Configuration | `tailwind.config.js` | CSS `@theme` directive |
| Import | Multiple directives | Single `@import "tailwindcss"` |
| Arbitrary values | `[--var]` syntax | `(--var)` syntax |
| Opacity modifiers | `bg-opacity-*` utilities | `/` syntax (e.g., `bg-red-500/50`) |
| Gradient prefix | `bg-gradient-*` | `bg-linear-*` |

---

## Complete Theme Configuration

### Basic Setup

```css
/* globals.css */
@import "tailwindcss";

@theme {
  /* ============================================
     TYPOGRAPHY
     ============================================ */

  /* Font Families */
  --font-sans: "Inter", system-ui, sans-serif;
  --font-display: "Space Grotesk", "Inter", sans-serif;
  --font-serif: "Instrument Serif", "Georgia", serif;
  --font-mono: "JetBrains Mono", "Fira Code", monospace;

  /* Font Sizes (extending defaults) */
  --text-xxs: 0.625rem;
  --text-10xl: 8rem;

  /* Line Heights */
  --leading-tighter: 1.1;
  --leading-looser: 2;

  /* Letter Spacing */
  --tracking-tighter: -0.04em;
  --tracking-super-tight: -0.06em;

  /* ============================================
     COLORS (OKLCH recommended)
     ============================================ */

  /* Brand Colors */
  --color-brand-50: oklch(0.98 0.02 250);
  --color-brand-100: oklch(0.95 0.03 250);
  --color-brand-200: oklch(0.90 0.05 250);
  --color-brand-300: oklch(0.80 0.08 250);
  --color-brand-400: oklch(0.70 0.10 250);
  --color-brand-500: oklch(0.55 0.12 250);
  --color-brand-600: oklch(0.45 0.15 250);
  --color-brand-700: oklch(0.35 0.12 250);
  --color-brand-800: oklch(0.25 0.08 250);
  --color-brand-900: oklch(0.18 0.05 250);
  --color-brand-950: oklch(0.12 0.03 250);

  /* Semantic Colors */
  --color-success: oklch(0.65 0.2 145);
  --color-warning: oklch(0.75 0.18 80);
  --color-error: oklch(0.6 0.22 25);
  --color-info: oklch(0.65 0.15 230);

  /* ============================================
     SPACING (extending defaults)
     ============================================ */

  --spacing-18: 4.5rem;    /* 72px */
  --spacing-88: 22rem;     /* 352px */

  /* ============================================
     BREAKPOINTS
     ============================================ */

  --breakpoint-xs: 475px;
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
  --breakpoint-3xl: 1920px;

  /* ============================================
     ANIMATIONS
     ============================================ */

  --animate-fade-in: fade-in 0.5s ease-out;
  --animate-float: float 6s ease-in-out infinite;

  @keyframes fade-in {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }

  @keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
  }

  /* ============================================
     Z-INDEX SCALE
     ============================================ */

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
}
```

---

## v3 → v4 Utility Migration

### Removed Utilities (Must Migrate)

| v3 Utility | v4 Replacement | Pattern |
|------------|----------------|---------|
| `bg-opacity-50` | `bg-red-500/50` | Opacity modifiers |
| `text-opacity-50` | `text-white/50` | Opacity modifiers |
| `border-opacity-50` | `border-black/50` | Opacity modifiers |
| `flex-shrink-*` | `shrink-*` | Direct rename |
| `flex-grow-*` | `grow-*` | Direct rename |
| `overflow-ellipsis` | `text-ellipsis` | Direct rename |

### Renamed Utilities

| v3 | v4 | Reason |
|----|----|--------|
| `shadow-sm` | `shadow-xs` | Explicit scale |
| `shadow` | `shadow-sm` | Named values |
| `blur-sm` | `blur-xs` | Explicit scale |
| `blur` | `blur-sm` | Named values |
| `rounded-sm` | `rounded-xs` | Explicit scale |
| `rounded` | `rounded-sm` | Named values |
| `outline-none` | `outline-hidden` | Semantic clarity |
| `ring` | `ring-3` | Explicit width |

### Gradients (Major Change)

| v3 | v4 |
|----|----|
| `bg-gradient-to-r` | `bg-linear-to-r` |
| `bg-gradient-to-r from-red-500` | `bg-linear-to-r from-red-500` |

**New in v4:** `bg-conic-*`, `bg-radial-*`, `bg-linear-45`

### CSS Variable Syntax Changes

```html
<!-- v3: Square brackets for CSS variables -->
<div class="bg-[--brand-color] w-[--custom-width]">

<!-- v4: Parentheses for CSS variables -->
<div class="bg-(--brand-color) w-(--custom-width)">
```

---

## Built-in Features (No Plugins Needed)

| Feature | v3 Required | v4 Support |
|---------|-------------|------------|
| Container Queries | Plugin | Native with `@container` |
| CSS Nesting | Plugin | Native |
| `aspect-ratio` | Plugin | Native |
| `accent-color` | Manual | Native |
| `color-mix()` | Manual | Native |

---

## Custom Utilities

### Creating Custom Utilities

```css
/* Define custom utilities with @utility */

@utility glass-panel {
  @apply bg-white/70 dark:bg-slate-900/70 backdrop-blur-xl
         border border-white/20 dark:border-slate-800/50;
}

@utility container-tight {
  @apply max-w-[1140px] mx-auto px-4 sm:px-6 lg:px-8;
}

@utility text-balance {
  text-wrap: balance;
}

@utility gradient-text {
  @apply bg-clip-text text-transparent bg-gradient-to-r from-brand-500 to-brand-700;
}
```

---

## Performance Benchmarks

| Metric | v3 | v4 | Improvement |
|--------|----|----|-------------|
| Initial build | ~800ms | ~100ms | **8x faster** |
| Incremental rebuild | ~200ms | ~5ms | **40x faster** |
| No-change rebuild | – | – | **182x faster** |

---

## Browser Requirements

| Browser | Minimum Version |
|---------|-----------------|
| Safari | 16.4+ |
| Chrome | 111+ |
| Firefox | 128+ |

**Note:** Projects requiring older browser support must remain on v3.4.

---

**See Also:**
- `[03-tailwind-v4-pitfalls.md](03-tailwind-v4-pitfalls.md)` - Common pitfalls and solutions
- `[SKILL.md](../SKILL.md)` - Main skill file
