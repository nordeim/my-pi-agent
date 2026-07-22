# Design System (Core Module 3)

> **Source Skills:** tailwind-patterns, frontend-design, avant-garde-design-v4  
> **Purpose:** Define cohesive typography, color, spacing, and responsive systems

---

## 1. Tailwind v4 CSS-First Foundation (tailwind-patterns)

### 1.1 Core Concepts
| Concept | Description |
|---------|-------------|
| **CSS-first** | Configuration in CSS, not JavaScript |
| **Oxide Engine** | Rust-based compiler, 10x faster builds |
| **Native Nesting** | CSS nesting without PostCSS |
| **CSS Variables** | All tokens exposed as `--*` vars |

### 1.2 Theme Definition (In `globals.css`)
```css
@theme {
  /* Colors - Semantic OKLCH (perceptually uniform) */
  --color-primary: oklch(0.7 0.15 250);
  --color-surface: oklch(0.98 0 0);
  --color-surface-dark: oklch(0.15 0 0);
  
  /* Spacing Scale (dynamic values allowed) */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 2rem;
  --spacing-18: 4.5rem; /* Custom dynamic value */
  
  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --font-serif: 'Instrument Serif', Georgia, serif;
}
```

### 1.3 v3 → v4 Migration Map
| v3 Utility | v4 Replacement | Notes |
|------------|----------------|-------|
| `bg-opacity-50` | `bg-color/50` | Opacity modifier |
| `shadow-sm` | `shadow-xs` | Explicit scale |
| `blur-sm` | `blur-xs` | |
| `bg-gradient-to-r` | `bg-linear-to-r` | New gradient type |
| `outline-none` | `outline-hidden` | Semantic clarity |
| `ring` | `ring-3` | Must specify width |

---

## 2. Color System

### 2.1 60-30-10 Rule (frontend-design)
```
60% → Primary/Background (calm, neutral base)
30% → Secondary (supporting areas)
10% → Accent (CTAs, highlights, attention)
```

### 2.2 Color Psychology (frontend-design)
| If You Need... | Consider Hues | Avoid |
|----------------|---------------|-------|
| Trust, calm | Blue family | Aggressive reds |
| Growth, nature | Green family | Industrial grays |
| Energy, urgency | Orange, red | Passive blues |
| Luxury, creativity | Deep Teal, Gold, Emerald | Cheap-feeling brights |
| Clean, minimal | Neutrals | Overwhelming color |

### 2.3 OKLCH vs RGB/HSL (tailwind-patterns)
| Format | Advantage |
|--------|-----------|
| **OKLCH** | Perceptually uniform, wider gamut, better gradients |
| **HSL** | Intuitive hue/saturation |
| **RGB** | Legacy compatibility |

### 2.4 Institutional vs Dynamic Palette (avant-garde-design-v4)

**Institutional Clarity (Trust-Based):**
```css
@theme {
  --color-primary: #F27A1A;                    /* Warm orange */
  --color-primary-subtle: rgba(242, 122, 26, 0.08);
  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #F8F9FA;
  --color-text-primary: #111827;                /* Near-black */
  --color-text-secondary: #6B7280;              /* Gray */
}
```

**Dynamic Modernism (Desire-Based):**
```css
@theme {
  --color-primary: #4F46E5;                    /* Indigo */
  --color-bg-primary: #FAFAF9;                  /* Warm off-white */
  --color-bg-dark: #1E293B;                     /* Slate-800 */
  --color-accent-cyan: #06B6D4;
  --color-accent-emerald: #10B981;
  --color-urgency: #EF4444;
}
```

---

## 3. Typography System

### 3.1 Scale Selection (frontend-design)
| Content Type | Scale Ratio | Feel |
|--------------|-------------|------|
| Dense UI | 1.125-1.2 | Compact, efficient |
| General web | 1.25 | Balanced (most common) |
| Editorial | 1.333 | Readable, spacious |
| Hero/display | 1.5-1.618 | Dramatic impact |

### 3.2 Pairing Concept (frontend-design)
```
Contrast + Harmony:
├── DIFFERENT enough for hierarchy
├── SIMILAR enough for cohesion
└── Usually: display + neutral, or serif + sans
```

### 3.3 Typography Systems by Strategy (avant-garde-design-v4)
| Strategy | Display Font | Body Font | H1 Scale |
|----------|-------------|-----------|----------|
| Single Family (Institutional) | DM Sans | DM Sans | 60-72px |
| Expressive (Dynamic) | Space Grotesk | Inter | 64-77px |
| Luxury/Refined | Instrument Serif | Inter | 60-72px |
| Editorial/Magazine | Playfair Display | Source Sans | 64-80px |
| Developer/Brutalist | JetBrains Mono | Inter | 56-68px |

### 3.4 Readability Rules (frontend-design)
- **Line length**: 45-75 characters optimal
- **Line height**: 1.4-1.6 for body text
- **Contrast**: WCAG AA minimum (4.5:1 normal text)
- **Size**: 16px+ for body on web
- **Fluid type**: `clamp(2.5rem, 5vw, 4.5rem)` for responsive headings

---

## 4. Spacing & Layout

### 4.1 8-Point Grid (frontend-design)
```
All spacing in multiples of 8:
├── Tight: 4px (half-step)
├── Small: 8px
├── Medium: 16px
├── Large: 24px, 32px
├── XL: 48px, 64px, 80px
```

### 4.2 Golden Ratio (φ = 1.618) (frontend-design)
```
Use for proportional harmony:
├── Content : Sidebar = ~62% : 38%
├── Heading size = previous × 1.618
├── Spacing: sm → md → lg (each × 1.618)
```

### 4.3 Modern Layout Patterns (tailwind-patterns)
| Pattern | Classes |
|---------|---------|
| Center (both axes) | `flex items-center justify-center` |
| Vertical stack | `flex flex-col gap-4` |
| Space between | `flex justify-between items-center` |
| Auto-fit responsive grid | `grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))]` |
| Asymmetric (Bento) | `grid grid-cols-3 grid-rows-2` with spans |

> **Note:** Prefer asymmetric/Bento layouts over symmetric 3-column grids.

---

## 5. Container Queries (tailwind-patterns)

### 5.1 Breakpoint vs Container
| Type | Responds To |
|------|-------------|
| **Breakpoint** (`md:`) | Viewport width |
| **Container** (`@container`) | Parent element width |

### 5.2 Usage
| Pattern | Classes |
|---------|---------|
| Define container | `@container` on parent |
| Container breakpoint | `@sm:`, `@md:`, `@lg:` on children |
| Named containers | `@container/card` for specificity |

### 5.3 When to Use
| Scenario | Use |
|----------|-----|
| Page-level layouts | Viewport breakpoints |
| Component-level responsive | Container queries |
| Reusable components | Container queries (context-independent) |

---

## 6. Dark Mode (tailwind-patterns)

### 6.1 Configuration Strategies
| Method | Behavior | Use When |
|--------|----------|----------|
| `class` | `.dark` class toggles | Manual theme switcher |
| `media` | Follows system preference | No user control |
| `selector` | Custom selector (v4) | Complex theming |

### 6.2 Pattern
| Element | Light | Dark |
|---------|-------|------|
| Background | `bg-white` | `dark:bg-zinc-900` |
| Text | `text-zinc-900` | `dark:text-zinc-100` |
| Borders | `border-zinc-200` | `dark:border-zinc-700` |

---

## 7. Z-Index Scale (avant-garde-design-v4)
```css
@theme {
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

## 8. Verification Checklist
- [ ] `@theme` directive in `globals.css` with project tokens
- [ ] Color palette uses OKLCH for perceptual uniformity
- [ ] Typography pairing matches strategic positioning (Q1-Q4)
- [ ] Spacing follows 8-point grid or Golden Ratio
- [ ] Container queries used for reusable components
- [ ] Dark mode configured (if required)
- [ ] Z-index scale defined for consistent layering

---

## 9. Related References
- [01-philosophy-strategy.md](01-philosophy-strategy.md) → Anti-generic, positioning
- [04-component-architecture.md](04-component-architecture.md) → shadcn/ui, MUI patterns
- [07-visual-design-motion.md](07-visual-design-motion.md) → Animation, effects
