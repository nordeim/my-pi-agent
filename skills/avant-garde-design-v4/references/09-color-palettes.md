# Strategic Color Palettes (Tailwind v4 Optimized)

## 1.0 Palette Strategy (60-30-10 Rule)
Implement color with intentionality:
- **60% Primary/Background:** Base calm/neutral
- **30% Secondary:** Supporting regions
- **10% Accent:** High-impact CTAs/highlights

---

## 2.0 Institutional Clarity (Trust-Based)
- **Goal:** Reliability, Professionalism, Legacy
- **Example:** iTrust Academy

```css
@theme {
  --color-brand-primary: #F27A1A;           /* Warm, professional orange */
  --color-brand-navy: #1E293B;              /* Deep, reliable navy */
  --color-bg-primary: #FFFFFF;
  --color-bg-subtle: #F8F9FA;
  --color-text-primary: #111827;            /* Near-black for readability */
  --color-text-muted: #6B7280;              /* Gray-500 */
  --color-success: #059669;                 /* Emerald-600 */
}
```

---

## 3.0 Dynamic Modernism (Energy-Based)
- **Goal:** Innovation, FOMO, Forward-thinking
- **Example:** AI Academy

```css
@theme {
  --color-brand-indigo: #4F46E5;           /* Energetic indigo */
  --color-brand-cyan: #06B6D4;             /* High-tech cyan */
  --color-bg-dark: #0F172A;                /* Deep slate for depth */
  --color-bg-glow: #1E293B;
  --color-accent-violet: #7C3AED;
  --color-text-glow: #F1F5F9;
  --color-urgency: #EF4444;                /* High-impact red */
}
```

---

## 4.0 Luxury Premium (Refined/High-End)
- **Goal:** Prestige, Elegance, Exclusive
- **Visual:** High contrast between cream and deep stone, minimal use of gold.

```css
@theme {
  --color-brand-gold: #D4AF37;             /* Sophisticated gold */
  --color-bg-cream: #FDFCF0;               /* Expensive off-white */
  --color-bg-stone: #1C1917;               /* Deep stone-900 */
  --color-text-rich: #1C1917;
  --color-text-stone: #44403C;
  --color-border-premium: #E7E5E4;
}
```

---

## 5.0 Color Psychology Quick Guide

| Color | Psychological Impact | Strategic Use |
|-------|----------------------|---------------|
| **Orange** | Warmth, Energy, Accessibility | Institutional CTAs (friendly) |
| **Navy** | Trust, Authority, Calm | Corporate backgrounds/headers |
| **Indigo** | Creativity, Mystery, High-Tech | Modern product highlights |
| **Cyan** | Precision, Cleanliness, Future | UI accents for tech interfaces |
| **Gold** | Prestige, Quality, Value | Luxury borders/icons |
| **Emerald** | Growth, Success, Security | Trust signals and success states |

---

## 6.0 Accessibility & Contrast Verification
**Target:** WCAG AAA (7:1 for normal text, 4.5:1 for large text)

**High-Contrast Token Pattern:**
```css
@theme {
  /* High contrast for AAA compliance */
  --color-text-body: oklch(0.15 0.02 250);   /* Dark slate */
  --color-text-display: oklch(0.05 0.01 250); /* Near black */
}
```

**Verification Rule:**
Never place white text on a light brand color or black text on a dark brand color without verifying the contrast ratio (WebAIM Contrast Checker).

---

**See Also:**
- `[10-design-directions.md](10-design-directions.md)` - Visual themes
- `[13-patterns-catalog.md](13-patterns-catalog.md)` - Implementation patterns
