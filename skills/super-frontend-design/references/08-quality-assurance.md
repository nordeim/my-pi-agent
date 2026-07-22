# Quality Assurance (Core Module 8)

> **Source Skills:** All 10 top frontend skills  
> **Purpose:** End-to-end validation, security, anti-patterns, and delivery readiness

---

## 1. Meticulous Approach SOP (6-Phase Workflow)

### Phase 1: ANALYZE (Deep Requirement Mining)
**Deliverables:**
- Strategic Brief (1 page): Quadrant position, audience psychographics, emotional goals
- Content Audit: Inventory all content types, prioritize hierarchy
- Competitive Matrix: 3-5 competitor screenshots with differentiation opportunities
- Technical Constraints: Browser support, performance budget, accessibility requirements

**Checklist:**
- [ ] Intentionality Compass completed
- [ ] Strategic Positioning Matrix quadrant identified
- [ ] Anti-Generic Litmus Test passed for core concept
- [ ] Accessibility requirements defined (AA vs AAA)
- [ ] Performance budget established

---

### Phase 2: PLAN (Structured Execution Roadmap)
**Deliverables:**
1. Component Architecture: Tree diagram (Server vs Client)
2. File Structure: Next.js + shadcn layout
3. Animation Strategy: Which elements animate, reduced motion compliance
4. Data Flow Map: Server/Client boundary

**Decision Points:**
- Navigation: Inline vs Hamburger (Sheet overlay)
- Color: Single accent (Institutional) vs Multi-accent (Dynamic)
- Typography: Single family vs Two-family system

---

### Phase 3: VALIDATE (Explicit Confirmation Checkpoint)
**Review Agenda:**
1. Present Intentionality Compass positioning
2. Show 3 style tiles (mood boards) with color/typography swatches
3. Review component hierarchy diagram
4. Confirm accessibility target (AA vs AAA)
5. Verify performance budget feasibility

**Sign-off Required:**
- [ ] Strategic positioning approved
- [ ] Color palette contrast ratios verified (WebAIM)
- [ ] Component architecture reviewed
- [ ] Animation complexity approved
- [ ] Mobile navigation pattern confirmed

---

### Phase 4: IMPLEMENT (Modular, Tested Builds)
**Sub-phases:**
1. **4.1 Foundation**: Configure Tailwind v4 theme, set up fonts, implement base layout
2. **4.2 Components**: Use shadcn/ui + Radix (library discipline: don't rebuild from scratch)
3. **4.3 Sections**: Hero, Features, Pricing with intentional whitespace
4. **4.4 Responsive**: Mobile-first, symmetrical breakpoints, touch targets ≥44×44px
5. **4.5 Animation**: 150-300ms duration, compositor-only properties, respect `prefers-reduced-motion`

**Verification per sub-phase:**
- [ ] Theme variables render correctly in DevTools
- [ ] Components use library primitives (no custom rebuilds)
- [ ] Whitespace is structural, not empty
- [ ] All breakpoints tested (mobile, tablet, desktop)
- [ ] Animations disabled when reduced motion enabled

---

### Phase 5: VERIFY (Rigorous QA)
1. **5.1 Visual Debugging** (see Section 5)
2. **5.2 Mobile Navigation** (7.3 in 07-visual-design-motion.md)
3. **5.3 Accessibility Audit** (see 06-accessibility-compliance.md)
4. **5.4 Performance Verification** (see 05-performance-optimization.md)
5. **5.5 Security Scan** (OWASP 2025, see Section 3)

---

### Phase 6: DELIVER (Complete Handoff)
**Deliverables:**
1. **Source Code**: Git repo with clean commit history
2. **Design Documentation**:
   - `docs/design-guideline.md` (strategy + decisions)
   - `docs/design-story.md` (narrative + emotions)
3. **Runbook**: Environment setup, build commands, deployment notes
4. **Quality Report**:
   - Lighthouse scores (≥90 Performance, ≥95 Accessibility)
   - Accessibility audit results (WCAG AAA)
   - Security scan results (no high/critical vulnerabilities)
5. **Knowledge Transfer**: Architecture decisions, extension points, maintenance notes

---

## 2. Pre-Commit Verification Gate

```bash
# Run in order before every commit
npx tsc --noEmit && npm run lint && npm test && npm run build
```

---

## 3. OWASP 2025 Security Checklist (nextjs16-tailwind4)

| Category | Checks |
|----------|--------|
| **A01 Broken Access Control** | IDOR, auth checks, SSRF protection, Server Action guards |
| **A02 Security Misconfiguration** | Secure headers, no default creds, no stack traces exposed |
| **A03 Supply Chain** | `npm audit`, lockfile integrity, SBOM |
| **A04 Cryptographic Failures** | bcrypt for passwords, jose for JWT, no hardcoded secrets |
| **A05 Injection** | ORM to prevent SQL injection, XSS via sanitization |
| **A06 Insecure Design** | Input validation with Zod, business logic reviews |
| **A07 Authentication Failures** | Session management, secure cookies (HttpOnly; SameSite=Strict) |
| **A08 Integrity Failures** | Code signing, dependency verification |
| **A09 Logging & Monitoring** | Failed auth logging, security events |
| **A10 Exceptional Conditions** | Fail-closed, proper error boundaries |

**Next.js Security Headers** (add to `next.config.ts`):
```typescript
async headers() {
  return [{ source: "/(.*)", headers: [
    { key: "X-Frame-Options", value: "DENY" },
    { key: "X-Content-Type-Options", value: "nosniff" },
    { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
    { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
  ]}];
}
```

---

## 4. Design Quality Gate

Before marking UI work complete:
- [ ] Distinctive aesthetic (immediately recognisable, not generic)
- [ ] Intentional whitespace (structural, not empty)
- [ ] Typography hierarchy clear without colour (squint test passes)
- [ ] Micro-interactions satisfying (150-300ms)
- [ ] Every element justified (Why? Only? Without? test)
- [ ] Color contrast meets WCAG AAA
- [ ] Animations respect `prefers-reduced-motion`

---

## 5. Visual Debugging Protocol (avant-garde-design-v4)

```
Step 1: Is element present in DOM?
├─ NO → Component not rendering (check conditional logic, props)
└─ YES → Continue

Step 2: Is it hidden by computed CSS?
├─ YES → Check display, visibility, opacity, width/height
└─ NO → Continue

Step 3: Is it off-screen or clipped?
├─ YES → Check position, transform, overflow on ancestors
└─ NO → Continue

Step 4: Is it behind another layer?
├─ YES → Check z-index, stacking contexts (use --z-* scale)
└─ NO → Continue

Step 5: Is JS failing to toggle state?
├─ YES → Check console, event listeners, state management
└─ NO → Continue

Step 6: Production-only disappearance?
└─ Check dynamic class strings, purge configuration (Tailwind v4: @source directive)
```

---

## 6. Anti-Pattern Catalog (Combined from All Skills)

### 6.1 Design Anti-Patterns (2026 Edition)
| Anti-Pattern | Why It Fails | Correct Approach |
|--------------|--------------|------------------|
| **Bento grids** | Modern cliché, every AI design | Question grid necessity; use asymmetry |
| **Purple-gradient-on-white** | Overused, AI-generated look | Unexpected color combinations |
| **Glassmorphism (blue/white)** | AI's idea of "premium" | Intentional color stories, solid surfaces |
| **Stock photography** | Generic, inauthentic | Custom illustrations or conceptual imagery |
| **"Click here" links** | Useless for screen readers | Descriptive link text |
| **Images of text** | Not readable, not resizable | Real text with proper styling |
| **Infinite scroll without end** | No rest, overwhelming | Provide natural endpoints |

### 6.2 Technical Anti-Patterns
| Anti-Pattern | Why It Fails | Correct Approach |
|--------------|--------------|------------------|
| `tailwind.config.js` in v4 | v4 uses CSS-first | Use `@theme` directive in globals.css |
| `outline-none` without replacement | Accessibility failure | `outline-hidden` + `focus-visible:ring-*` |
| `<div onClick>` | Not keyboard accessible | `<button type="button">` |
| `transition: all` | Performance issue | List specific properties |
| Dynamic class strings | Purged in production | Use static class strings |
| `autoFocus` without justification | UX disruption on mobile | Use sparingly, desktop only |
| Images without dimensions | Layout shift (CLS) | Explicit `width` and `height` |
| Form inputs without labels | Accessibility failure | `<label>` or `aria-label` required |
| Animating `width`/`height` | Poor performance, repaints | Use `scale` transform |
| Barrel imports (`index.ts` re-exports) | Bundle bloat | Direct imports from component files |
| Sequential `await` for independent calls | Waterfalls (100-500ms+ per step) | Use `Promise.all()` |

---

## 7. Code Quality Gates

- [ ] No `any` types (use `unknown` with type guards)
- [ ] Proper error boundaries for Client Components
- [ ] Loading states for async operations
- [ ] Error states with user-friendly messages
- [ ] Disabled buttons during form submission
- [ ] `useEffect` cleanup functions where needed
- [ ] Memoization for expensive calculations (`useMemo`, `useCallback`)
- [ ] Explicit TypeScript return types on functions
- [ ] Type imports: `import type { User } from "~types/user"`

---

## 8. Pre-Deploy Verification Checklist

### Critical (Must Pass)
- [ ] Lighthouse Performance ≥ 90
- [ ] Lighthouse Accessibility ≥ 95
- [ ] No console errors
- [ ] Keyboard-only operation confirmed
- [ ] Screen-reader test (VoiceOver/NVDA)
- [ ] Responsive: mobile, tablet, desktop, small-height
- [ ] All animations obey `prefers-reduced-motion`
- [ ] `npm audit` returns no high/critical vulnerabilities
- [ ] Production build validated (`grep` for expected utilities in CSS)

### High Priority
- [ ] Strategic positioning approved
- [ ] Distinctive aesthetic (not generic)
- [ ] Color contrast meets WCAG AAA
- [ ] Micro-interactions 150-300ms
- [ ] Mobile navigation fully functional

---

## 9. Delivery Handoff Checklist

- [ ] Source code with clean commit history
- [ ] `docs/design-guideline.md` (strategy decisions)
- [ ] `docs/design-story.md` (narrative + emotions)
- [ ] Runbook (setup, build, deploy commands)
- [ ] Lighthouse report (Performance, Accessibility)
- [ ] Accessibility audit report (WCAG AAA)
- [ ] Security scan report (OWASP 2025)
- [ ] Browser testing matrix (Chrome, Firefox, Safari, Edge)
- [ ] Knowledge transfer notes (architecture decisions)

---

## 10. Related References
- [01-philosophy-strategy.md](01-philosophy-strategy.md) → Anti-generic, positioning
- [02-tech-stack-setup.md](02-tech-stack-setup.md) → Next.js, Tailwind setup
- [03-design-system.md](03-design-system.md) → Typography, color
- [04-component-architecture.md](04-component-architecture.md) → shadcn/ui, MUI
- [05-performance-optimization.md](05-performance-optimization.md) → 57 Vercel rules
- [06-accessibility-compliance.md](06-accessibility-compliance.md) → WCAG, ADA
- [07-visual-design-motion.md](07-visual-design-motion.md) → Animation, effects
