# Accessibility & Compliance (Core Module 6)

> **Source Skills:** web-design-guidelines, avant-garde-design-v4, ui-styling, frontend-design  
> **Purpose:** Meet WCAG AAA + ADA Title II standards with automated auditing

---

## 1. Legal Requirement (April 24, 2026)

**ADA Title II**: All digital content must meet **WCAG 2.1 Level AA** minimum.  
**Best Practice**: Target **WCAG AAA** for mastery and future-proofing.

---

## 2. Web Interface Guidelines Audit (web-design-guidelines)

### 2.1 Audit Workflow
1. **Fetch Latest Guidelines**:
   ```bash
   # Use FetchURL to retrieve latest rules
   # URL: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
   ```
2. **Read Files to Audit**: Specify files/patterns to review
3. **Apply All Rules**: Check against every guideline
4. **Output Findings**: `file:line` format as specified in guidelines

### 2.2 When to Run
- After completing UI implementation
- Before any production deployment
- When user asks: "review my UI", "check accessibility", "audit design"

---

## 3. WCAG AAA Checklist (avant-garde-design-v4)

### 3.1 Mandatory Checks
- [ ] **Images**: Every image has meaningful `alt` text (or `alt=""` if decorative)
- [ ] **Text Size**: Minimum 14px (16px+ recommended)
- [ ] **Color Contrast**:
  - Normal text: 7:1 ratio (AAA)
  - Large text (18px+): 4.5:1 ratio (AAA)
- [ ] **Links**: Descriptive text ("Register for Career Fair" not "Click here")
- [ ] **Touch Targets**: Minimum 44×44px (AAA)
- [ ] **Headings**: Semantic `<h1>`–`<h6>` for structure
- [ ] **Focus States**: Visible on all interactive elements (`focus-visible:ring-2`)
- [ ] **Forms**: Associated `<label>` or `aria-label`
- [ ] **Reduced Motion**: All animations respect `prefers-reduced-motion`

### 3.2 Semantic HTML
| Element | Use For |
|---------|---------|
| `<nav>` | Navigation menus |
| `<main>` | Primary page content |
| `<section>` | Thematic content groups |
| `<article>` | Self-contained content |
| `<aside>` | Complementary content |

---

## 4. Radix UI Accessibility (ui-styling)

### 4.1 Built-In Features
- Automatic ARIA role assignment
- Keyboard navigation (Arrow keys, Escape, Tab)
- Focus trap for modals/overlays
- Screen reader announcements

### 4.2 Checklist for Radix Components
- [ ] Dialog: Focus returns to trigger on close
- [ ] Dropdown: Arrow key navigation, Escape closes
- [ ] Tabs: `aria-selected` for active tab
- [ ] Checkbox/Radio: Proper `role` and `aria-checked`
- [ ] Toast: `aria-live="polite"` for announcements

---

## 5. Reduced Motion (Absolute Requirement)

### 5.1 Implementation
```tsx
"use client";
import { useEffect, useState } from "react";

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

### 5.2 Usage in Animation
```tsx
const prefersReducedMotion = useReducedMotion();
const initial = prefersReducedMotion ? {} : { opacity: 0, y: 30 };

<motion.div
  initial={initial}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: prefersReducedMotion ? 0 : 0.6 }}
>
  Content
</motion.div>
```

### 5.3 Rule
> When `prefers-reduced-motion: reduce`, **disable all animations entirely**—do not just slow them.

---

## 6. Accessibility Anti-Patterns (frontend-design)

| ❌ Don't | ✅ Do |
|----------|-----|
| `<div onClick>` (not keyboard accessible) | `<button type="button">` |
| `autoFocus` without justification | Use sparingly, desktop only |
| Images without `alt` | Always provide meaningful `alt` |
| Form inputs without labels | `<label>` or `aria-label` required |
| Animating `width`/`height` | Use `transform: scale()` |
| `outline-none` without replacement | `outline-hidden` + `focus-visible:ring-*` |
| "Click here" links | Descriptive link text |

---

## 7. OWASP 2025 Security Checklist (nextjs16-tailwind4)

| Category | Checks |
|----------|--------|
| **A01 Broken Access Control** | IDOR, auth checks, SSRF protection |
| **A02 Security Misconfiguration** | Secure headers, no stack traces |
| **A03 Supply Chain** | `npm audit`, lockfile integrity |
| **A04 Cryptographic Failures** | bcrypt for passwords, jose for JWT |
| **A05 Injection** | ORM to prevent SQL injection, XSS sanitization |
| **A06 Insecure Design** | Input validation with Zod |
| **A07 Authentication Failures** | Secure cookies (HttpOnly; SameSite=Strict) |
| **A08 Integrity Failures** | Code signing, dependency verification |
| **A09 Logging & Monitoring** | Failed auth logging |
| **A10 Exceptional Conditions** | Fail-closed, proper error boundaries |

### 7.1 Next.js Security Headers
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

---

## 8. Verification Gates

### 8.1 Pre-Deploy Accessibility Check
- [ ] Lighthouse Accessibility Score ≥ 95
- [ ] No console errors related to ARIA
- [ ] Keyboard-only operation confirmed
- [ ] Screen-reader test (VoiceOver/NVDA)
- [ ] Responsive: mobile, tablet, desktop
- [ ] All animations obey `prefers-reduced-motion`
- [ ] `npm audit` returns no high/critical vulnerabilities

### 8.2 Design Quality Gate
- [ ] Color contrast meets WCAG AAA
- [ ] Touch targets ≥ 44×44px
- [ ] Focus states visible on all interactive elements
- [ ] Forms have associated labels
- [ ] Semantic HTML used throughout

---

## 9. Related References
- [01-philosophy-strategy.md](01-philosophy-strategy.md) → Intentionality, anti-generic
- [05-performance-optimization.md](05-performance-optimization.md) → Performance budgets
- [07-visual-design-motion.md](07-visual-design-motion.md) → Animation, reduced motion
- [08-quality-assurance.md](08-quality-assurance.md) → OWASP, verification gates
