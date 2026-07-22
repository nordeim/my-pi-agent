# Visual Design & Motion (Core Module 7)

> **Source Skills:** aesthetic, avant-garde-design-v4, frontend-design  
> **Purpose:** Create memorable, performant, accessible visual experiences

---

## 1. Four-Stage Aesthetic Framework (aesthetic)

### 1.1 BEAUTIFUL (Aesthetic Principles)
Study high-quality designs (Dribbble, Mobbin, Behance) to extract:
- Design style (Minimalism, Glassmorphism, Neo-brutalism)
- Layout structure & grid systems
- Typography system & hierarchy (predict font names/sizes)
- Color palette with hex codes
- Visual hierarchy techniques
- Micro-interactions
- Aesthetic quality rating (1-10)

**Workflow: Capture & Analyze Inspiration**
1. Browse inspiration sites
2. Use `chrome-devtools` skill to capture full-screen screenshots
3. Use `ai-multimodal` skill to analyze:
   - Design style, layout, typography, colors
   - Visual hierarchy, components, micro-interactions
4. Document findings in `project/docs/design-guideline.md`

### 1.2 RIGHT (Functionality)
Beautiful designs lacking usability are worthless:
- Validate with WCAG accessibility standards
- Ensure responsive breakpoints logical
- Implement loading/error states
- Test keyboard navigation

### 1.3 SATISFYING (Micro-Interactions)
Incorporate subtle animations:
- **Duration**: 150ms (micro), 300ms (standard), 500ms (dramatic)
- **Easing**: `cubic-bezier(0.4, 0, 0.2, 1)` (ease-out for entry)
- **Stagger**: 50ms delay between sequential elements
- **Properties**: Only `transform` and `opacity` (compositor-only)

### 1.4 PEAK (Storytelling)
Elevate with narrative elements:
- Parallax effects (performance-permitting)
- Particle systems (WebGL only for Q4 Dynamic Modernism)
- Thematic consistency across sections
- Restraint: "too much of anything isn't good"

**Workflow: Generate & Iterate Design Images**
1. Define prompt with style, colors, typography, audience
2. Use `ai-multimodal` to generate design images (Gemini API)
3. Analyze output, evaluate aesthetic quality (score ≥7/10)
4. Iterate until standards met
5. Document in `project/docs/design-story.md`

---

## 2. Animation Principles (frontend-design + avant-garde-design-v4)

### 2.1 Timing Guidelines
| Distance/Size | Duration | Context |
|---------------|----------|---------|
| Small micro-interaction | 150ms | Button hover, toggle switch |
| Standard transition | 300ms | Modal open, content fade |
| Large/slow animation | 500ms | Hero section entrance |
| Dramatic effect | 800ms | Page transition, hero reveal |

### 2.2 Easing Selection
| Action | Easing | Why |
|--------|--------|-----|
| Entering | Ease-out | Decelerate, settle in |
| Leaving | Ease-in | Accelerate, exit |
| Emphasis | Ease-in-out | Smooth, deliberate |
| Playful | Bounce | Fun, energetic |

### 2.3 Performance Rules
1. **Compositor-Only**: Animate only `transform` and `opacity`
2. **Reduced Motion**: Disable all animations when `prefers-reduced-motion: reduce`
3. **Test on Low-End**: Verify 60fps on mid-range mobile devices
4. **Avoid Layout Properties**: Never animate `width`, `height`, `margin`, `padding`

---

## 3. Micro-Interaction Patterns (avant-garde-design-v4)

### 3.1 Button Hover
```css
button {
  transition: transform 150ms ease-out, background-color 150ms ease-out;
}
button:hover {
  transform: scale(1.05);
}
button:active {
  transform: scale(0.98);
}
```

### 3.2 Form Focus
```css
input:focus-visible {
  outline: 2px solid var(--color-champagne);
  outline-offset: 2px;
  transition: outline-offset 150ms ease-out;
}
```

### 3.3 Page Entrance (Framer Motion)
```tsx
<motion.div
  initial={{ opacity: 0, y: 30 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.6, ease: [0.4, 0, 0.2, 1] }}
>
  Content
</motion.div>
```

---

## 4. Aesthetic Direction Selection (avant-garde-design-v4)

Choose ONE direction and execute with precision:

| Direction | Characteristics | When to Use | Keywords |
|-----------|-----------------|-------------|----------|
| **Brutally Minimal** | Extreme whitespace, single focal point | Luxury brands, portfolios | Calm, focused, editorial |
| **Maximalist Chaos** | Layered textures, bold typography | Creative agencies, art | Rich, dense, energetic |
| **Retro-Futuristic** | Neon, chrome, geometric patterns | Tech products, gaming | Neon, chrome, sci-fi |
| **Organic/Natural** | Soft curves, earthy tones, fluid shapes | Wellness, sustainability | Earthy, soft, flowing |
| **Luxury/Refined** | Serif fonts, gold accents, subtle gradients | Premium services, fashion | Elegant, restrained, premium |
| **Editorial/Magazine** | Asymmetric layouts, oversized headlines | Media, publishing | Dynamic, typographic, bold |
| **Brutalist/Raw** | Exposed structure, monospace, high contrast | Developer tools, portfolios | Raw, honest, functional |
| **Tactile Maximalism** | "Squishy" buttons, glass-like elements | Web3, DeFi, NFT | Tangible, reactive, immersive |

---

## 5. Visual Effects Principles (frontend-design)

### 5.1 Glassmorphism (Use Radically or Not At All)
```
Key properties:
├── Semi-transparent background
├── Backdrop blur (12px+)
├── Subtle border for definition
└── ⚠️ WARNING: Standard blue/white glassmorphism is a modern cliché.
```

### 5.2 Shadow Hierarchy
```
Elevation concept:
├── Higher elements = larger shadows
├── Y-offset > X-offset (light from above)
├── Multiple layers = more realistic
└── Dark mode: may need glow instead of shadow
```

### 5.3 Gradient Usage
```
Harmonious gradients:
├── Adjacent colors on wheel (analogous)
├── OR same hue, different lightness
├── Avoid harsh complementary pairs
├── 🚫 NO Mesh/Aurora Gradients (floating blobs)
└── VARY from project to project radically
```

---

## 6. Typography as Visual Hierarchy (frontend-design + avant-garde-design-v4)

### 6.1 Squint Test
> If you squint at your design and can't tell the hierarchy, redesign it.

### 6.2 Fluid Typography
```css
/* Use clamp() for responsive headings */
h1 {
  font-size: clamp(2.5rem, 5vw, 4.5rem);
  line-height: 1.0-1.06;
  letter-spacing: -0.02em to -0.04em;
}
```

### 6.3 Typography Pairing Rules
```
Contrast + Harmony:
├── DIFFERENT enough for hierarchy
├── SIMILAR enough for cohesion
└── Usually: display + neutral, or serif + sans
```

---

## 7. Mobile Navigation Patterns (avant-garde-design-v4)

### 7.1 Symmetrical Breakpoint Logic
```tsx
{/* Desktop */}
<nav className="hidden md:flex items-center gap-8">...</nav>

{/* Mobile trigger */}
<button className="md:hidden" aria-label="Open menu">Menu</button>
```

### 7.2 shadcn Sheet Mobile Nav (Complete)
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

### 7.3 Mobile Nav Failure Taxonomy
| Class | Symptom | Fix |
|-------|---------|-----|
| **A** | No nav on mobile | Add mobile trigger + overlay |
| **B** | Hidden by opacity/visibility | Verify JS toggle & CSS open state |
| **C** | Clipped top items | Overlay `position: fixed`; `overflow-y: auto` |
| **D** | Behind another layer | Use z-index scale (--z-overlay: 400) |
| **E** | Breakpoint mismatch | Check viewport meta + breakpoint values |
| **F** | JS error/selector miss | Guard querySelectors; check console |
| **G** | Keyboard unreachable | Use real `<button>`, focus management |
| **H** | Click-outside race condition | Exclude trigger from outside-click handler |

---

## 8. Verification Checklist

**Visual Design:**
- [ ] Distinctive aesthetic direction (not generic)
- [ ] Intentional whitespace usage (structural, not empty)
- [ ] Typography hierarchy clear (squint test passes)
- [ ] Color contrast meets WCAG AAA
- [ ] Micro-interactions are satisfying (150-300ms)

**Motion:**
- [ ] Animations respect `prefers-reduced-motion`
- [ ] Only `transform` and `opacity` animated
- [ ] 60fps on mid-range mobile devices
- [ ] Reduced motion disables animations entirely

**Mobile:**
- [ ] Navigation works on all screen sizes
- [ ] Touch targets ≥44×44px
- [ ] No clipped content on small screens
- [ ] Breakpoint logic symmetrical (`hidden md:flex` / `md:hidden`)

---

## 9. Related References
- [01-philosophy-strategy.md](01-philosophy-strategy.md) → Anti-generic, positioning
- [03-design-system.md](03-design-system.md) → Typography, color
- [06-accessibility-compliance.md](06-accessibility-compliance.md) → WCAG, reduced motion
- [08-quality-assurance.md](08-quality-assurance.md) → Anti-patterns, verification
