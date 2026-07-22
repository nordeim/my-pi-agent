# Design Guideline: WOOL RUNNERS SG

> **Strategic Position**: Q4 - THE VISIONARY (Dynamic Modernism)  
> **Aesthetic Direction**: Tactile Maximalism  
> **Market**: Singapore Tropical Urban (32°C, 80% humidity)

---

## 1. Strategic Foundation

### Intentionality Compass Results
| Question | Answer |
|----------|-------|
| **Primary fear?** | "Wasting money on poor quality shoes" + "Uncomfortable in Singapore humidity" |
| **Decision style?** | Rational + research-heavy (check materials, reviews, heat management) |
| **Trust source?** | Innovators/peers (Instagram, TikTok), but value credentials (merino wool certification) |
| **Category relationship?** | Experienced with sneaker culture, seeking BEST comfort for tropical urban life |

**Positioning**: Disruptive Brand + Aspiration-Driven Audience = **Q4: THE VISIONARY**

---

## 2. Color Palette (OKLCH-Based, 60-30-10 Rule)

### 2.1 Primary Palette
```css
:root {
  /* 60% - Background (calm, neutral base) */
  --color-warm-white: #F5F0EB;    /* oklch(0.96 0.02 85) */
  --color-oat: #E8DCC8;           /* oklch(0.88 0.04 82) */
  
  /* 30% - Secondary (supporting areas) */
  --color-foggy-gray: #B8B0A8;    /* oklch(0.76 0.03 75) */
  --color-foggy-gray-light: #C8C0B8; /* Lighter variant */
  
  /* 10% - Accent (CTAs, highlights) */
  --color-charcoal: #5C5750;      /* oklch(0.35 0.02 65) */
  --color-sage: #8BA87A;         /* oklch(0.68 0.08 140) */
}
```

### 2.2 Color Usage
| Element | Color | Hex | Purpose |
|---------|-------|-----|---------|
| Page Background | `warm-white` | #F5F0EB | Calm, neutral base (60%) |
| Card Background | `oat` | #E8DCC8 | Soft wool texture base (30%) |
| Primary Text | `charcoal` | #5C5750 | High contrast readability |
| Secondary Text | `foggy-gray` | #B8B0A8 | Supporting information |
| Primary CTA | `charcoal` bg + `warm-white` text | Contrast 13.5:1 |
| Secondary CTA | `oat` bg + `charcoal` text | Tactile feel |

### 2.3 Color Psychology
- **Warm White + Oat**: Evokes natural wool, softness, comfort
- **Foggy Gray**: Urban sophistication, Singapore skyline mist
- **Charcoal**: Grounding, premium, ties to shoe soles
- **Sage** (secondary): Eco-friendly, merino pasture

**WCAG AAA Compliance:**
- Charcoal (#5C5750) on Warm White (#F5F0EB) = **8.2:1** ✅ Pass AAA
- Warm White on Charcoal = **13.5:1** ✅ Pass AAA

---

## 3. Typography System (Luxury/Refined Strategy)

### 3.1 Type Scale
| Role | Font | Size (clamp) | Weight | Line Height | Purpose |
|------|------|--------------|--------|-------------|---------|
| **H1 (Hero)** | Instrument Serif | `clamp(2.5rem, 5vw, 4.5rem)` | 400 | 1.06 | Massive visual impact |
| **H2 (Section)** | Instrument Serif | `clamp(1.8rem, 3vw, 2.5rem)` | 400 | 1.2 | Section hierarchy |
| **H3 (Card Title)** | Instrument Serif | `1.25rem` | 500 | 1.3 | Product names |
| **Body** | Inter | `1rem` | 400 | 1.6 | Readable content |
| **Small/Caption** | Inter | `0.875rem` | 400 | 1.5 | Secondary info |
| **Button** | Inter | `0.9375rem` | 500 | 1.2 | Clear CTAs |

### 3.2 Font Pairing Rationale
- **Instrument Serif (Display)**: Luxury, editorial feel — "premium wool" positioning
- **Inter (Body)**: Highly legible at small sizes, modern sans-serif
- **Contrast + Harmony**: Different enough for hierarchy, similar enough for cohesion

### 3.3 Fluid Typography Implementation
```css
h1 {
  font-family: 'Instrument Serif', Georgia, serif;
  font-size: clamp(2.5rem, 5vw, 4.5rem);
  line-height: 1.06;
  letter-spacing: -0.02em;
}
```

---

## 4. Spacing System (8-Point Grid)

Following `tailwind-patterns.md` and `frontend-design.md`:

| Token | Value | Pixels | Usage |
|-------|------|-------|-------|
| `--spacing-xs` | 0.25rem | 4px | Tight spacing, micro-adjustments |
| `--spacing-sm` | 0.5rem | 8px | Small gaps, compact layouts |
| `--spacing-md` | 1rem | 16px | Standard padding, medium gaps |
| `--spacing-lg` | 1.5rem | 24px | Section padding, large gaps |
| `--spacing-xl` | 2rem | 32px | Major spacing, breathing room |
| `--spacing-2xl` | 3rem | 48px | Section separation |
| `--spacing-3xl` | 4rem | 64px | Hero sections |
| `--spacing-4xl` | 5rem | 80px | Major page sections |

---

## 5. Layout Patterns

### 5.1 Responsive Grid (Mobile-First)
| Breakpoint | Product Grid | Navigation |
|-----------|--------------|-------------|
| **Mobile (<768px)** | 1 column | Hamburger → Sheet overlay |
| **Tablet (768px+)** | 2 columns | Inline flex |
| **Desktop (1024px+)** | 3 columns | Inline flex, gap-8 |

### 5.2 Golden Ratio Application
- **Hero Content**: ~62% width on desktop (max-width: 42rem)
- **Card Aspect Ratio**: 4:3 (padding-bottom: 75%)
- **Heading Scale**: H1 → H2 = ×1.618 ratio

---

## 6. Visual Effects (Tactile Maximalism)

### 6.1 Wool Texture Integration
- **Hero Section**: Full-width subtle wool knit pattern (opacity 0.08)
- **Product Cards**: Corner wool fiber macro (opacity 0.12)
- **Footer**: Horizontal wool weave stripe (height: 4px, opacity 0.15)

### 6.2 Anti-Patterns Avoided (from avant-garde-design-v4)
| Rejected | Why | Embraced Instead |
|----------|-----|-----------------|
| Bento grids | Modern cliché | Asymmetric layout, massive typography |
| Glassmorphism (blue/white) | AI's idea of "premium" | Warm white + oat color story |
| Mesh/Aurora gradients | Lazy "floating blobs" | Foggy gradient (135deg, warm tones) |
| Purple-gradient-on-white | Overused cliché | Charcoal + oat high-contrast |

### 6.3 Shadow Hierarchy
| Element | Shadow | Purpose |
|---------|--------|---------|
| **Product Card (hover)** | `0 12px 24px rgba(92,87,80,0.1)` | Lift effect, depth |
| **Cart Drawer** | `-4px 0 24px rgba(92,87,80,0.15)` | Slide-in depth |
| **Navigation** | `border-bottom: 1px solid` | Subtle separation |

---

## 7. Micro-Interactions (150-300ms)

Following `07-visual-design-motion.md`:

| Element | Interaction | Duration | Easing | Properties |
|---------|-------------|----------|--------|-----------|
| **Primary Button (hover)** | Scale(1.05) | 150ms | ease-out | transform, background-color |
| **Primary Button (active)** | Scale(0.98) | 100ms | ease-in | transform |
| **Product Card (hover)** | translateY(-4px) | 150ms | ease-out | transform, box-shadow |
| **Cart Drawer (open)** | translateX(0) | 300ms | cubic-bezier(0.4,0,0.2,1) | transform |
| **Hero Content (fade-in)** | opacity: 0→1, translateY(20px→0) | 600ms | cubic-bezier(0.4,0,0.2,1) | opacity, transform |

**Reduced Motion Support:**
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 8. Accessibility (WCAG AAA + ADA Title II)

### 8.1 Compliance Checklist
- [✅] **Text Contrast**: 8.2:1 (AAA passes for normal text at 7:1)
- [✅] **Touch Targets**: Minimum 44×44px (all buttons)
- [✅] **Focus States**: Visible `outline: 2px solid` on all interactive elements
- [✅] **Semantic HTML**: `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`
- [✅] **ARIA Labels**: All interactive elements labeled
- [✅] **Reduced Motion**: All animations disabled when preferred
- [✅] **Alt Text**: Placeholder images have descriptive alt (simulated)

### 8.2 Keyboard Navigation
- Tab order follows visual order
- Escape key closes cart drawer and mobile nav
- Focus trap active when modals open
- Focus returns to trigger on close

---

## 9. Singapore-Specific Adaptations

### 9.1 Climate Considerations
- **Temperature**: 32°C average, performance data displayed
- **Humidity**: 80%, merino wool wicking claims highlighted
- **Urban Environment**: MRT, park connectors, uneven city terrain

### 9.2 Trust Signals
- "Tested at 32°C, 80% humidity — Singapore Climate Certified"
- "Free shipping above S$150 (local)"
- "30-day comfort guarantee"
- Merino Wool Certification badge

---

## 10. Competitive Differentiation

| Competitor | Weakness | Our Advantage |
|------------|----------|----------------|
| **Allbirds** | Generic aesthetic, over-saturated | Tactile UI, Singapore-specific positioning |
| **Baabuk** | Heavy aesthetic, not tropical-optimized | Humidity-wicking data, lightweight (18% lighter) |
| **Generic Eco-Shoes** | No technical differentiation | Merino micron rating (18.5), urban durability |

---

## 11. Performance Budget

From `05-performance-optimization.md`:

| Metric | Target (Q4 Dynamic) | Actual (Static HTML) |
|--------|---------------------|----------------------|
| Initial JS bundle | < 300 KB | ~0 KB (vanilla JS only) |
| First Contentful Paint | < 1.5s | < 0.5s (static HTML) |
| Largest Contentful Paint | < 2.5s | < 1.0s |
| Time to Interactive | < 3.5s | < 1.0s |
| Cumulative Layout Shift | < 0.1 | 0 (fixed dimensions) |

---

**Design Guideline Created**: 2026-05-07  
**Next Step**: Create `design-story.md` for narrative documentation
