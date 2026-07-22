# Technical Commitments & Performance Standards

## 1.0 Strategic Commitment Matrix

Based on your quadrant in the Strategic Positioning Matrix, you MUST adhere to these minimum technical standards:

| Quadrant | Lighthouse Target | Accessibility | Animation Budget |
|----------|-------------------|---------------|------------------|
| **Q1: THE GUARDIAN** | 98-100 | WCAG AAA | Minimal (Micro-interactions only) |
| **Q2: LEGACY INNOVATOR** | 90+ | WCAG AA | Balanced (Scroll reveals) |
| **Q3: TRUSTWORTHY UPSTART** | 95+ | WCAG AAA | Strategic (Trust signals) |
| **Q4: THE VISIONARY** | 85-90+ | WCAG AA | High (Experiential/Tactile) |

---

## 2.0 Performance Budgets by Quadrant

Measure these metrics during every development phase.

| Metric | Institutional (Q1/Q3) | Dynamic (Q2/Q4) | Balanced |
|--------|---------------|---------|----------|
| **Initial JS bundle** | < 120 KB | < 250 KB | < 180 KB |
| **First Contentful Paint** | < 0.8s | < 1.2s | < 1.0s |
| **Largest Contentful Paint** | < 1.2s | < 2.0s | < 1.5s |
| **Time to Interactive** | < 1.5s | < 2.5s | < 2.0s |
| **Cumulative Layout Shift** | < 0.05 | < 0.1 | < 0.05 |
| **Animation Frame Rate** | N/A | 60fps | 60fps |

---

## 3.0 Technology Stack by Position

### 3.1 Q1/Q3 (Institutional Clarity)
- **Framework:** Next.js 16.2+ (Static Export if possible).
- **Styling:** Tailwind v4 (CSS-first, no JS config).
- **Rendering:** 90% Server Components.
- **Components:** shadcn/ui primitives with minimal custom logic.

### 3.2 Q2/Q4 (Dynamic Modernism)
- **Framework:** Next.js 16.2+ (App Router).
- **Styling:** Tailwind v4 + OKLCH color space.
- **Animation:** Motion (v12+) or GSAP for complex timelines.
- **Components:** Bespoke-styled shadcn wrappers with custom tactile physics.

---

## 4.0 Component Library Standards

**CRITICAL RULE:** Do not rebuild what the library provides.
1. **shadcn/ui (Radix):** Use for all accessible primitives (Modals, Tabs, Sheet).
2. **Base UI:** Use for "headless" unstyled primitives requiring 100% custom styling.
3. **Custom Primitives:** Only permitted if the requirement is outside the scope of accessible library patterns (e.g., custom 3D interactions).

---

## 5.0 Security & Safety Checklist (2026 Edition)

- [ ] **Secret Detection:** No API keys or `.env` variables committed.
- [ ] **Content Security Policy (CSP):** Configured via `next.config.ts`.
- [ ] **Sanitization:** All user-generated content sanitized before rendering.
- [ ] **Dependency Audit:** Run `npm audit` weekly.
- [ ] **Form Safety:** All forms use Zod validation and CSRF protection.

---

**See Also:**
- `[15-performance-budgets.md](15-performance-budgets.md)` - Implementation details
- `[16-nextjs-optimization.md](16-nextjs-optimization.md)` - Optimization techniques
