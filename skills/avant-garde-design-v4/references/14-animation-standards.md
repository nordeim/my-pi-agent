# Animation & Motion Standards (2026)

## 1.0 Core Principles
Every animation MUST serve a purpose:
1. **Feedback:** Confirm user action (e.g., button press).
2. **Context:** Show relationship between elements (e.g., expanding list).
3. **Narrative:** Guide the eye through the story (e.g., scroll reveal).

---

## 2.0 Duration & Easing Reference

Standardize timing to create a cohesive experience.

| Type | Duration | Easing (Cubic Bezier) | Use Case |
|------|----------|------------------------|----------|
| **Micro** | 150ms | `(0.4, 0, 0.2, 1)` | Hover states, toggle icons |
| **Standard** | 300ms | `(0.4, 0, 0.2, 1)` | Modals, drawer entry/exit |
| **Dramatic** | 500ms+ | `(0.25, 0.1, 0.25, 1)` | Hero entry, major transitions |

---

## 3.0 Layout Animations (Motion v12+)
Use `layout` prop for seamless transitions between states without jank.

```tsx
<motion.div
  layout
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 0.3 }}
>
  {/* Content that changes size or position */}
</motion.div>
```

---

## 4.0 Staggered List Animation
- **Goal:** Create a sense of flow and quality.

```tsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.3
    }
  }
}

const item = {
  hidden: { y: 20, opacity: 0 },
  show: { y: 0, opacity: 1, transition: { duration: 0.5, ease: "easeOut" } }
}

// Usage
<motion.ul variants={container} initial="hidden" animate="show">
  <motion.li variants={item} />
  <motion.li variants={item} />
</motion.ul>
```

---

## 5.0 Motion Sensitivity & Reduced Motion
**Mandatory Compliance:** ADA Title II / WCAG 2.1 AA.

### 5.1 CSS Standard
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### 5.2 Motion (React) Implementation
```tsx
import { useReducedMotion } from 'framer-motion';

const prefersReducedMotion = useReducedMotion();

<motion.div
  animate={{ x: prefersReducedMotion ? 0 : 100 }}
  transition={{ duration: prefersReducedMotion ? 0 : 0.5 }}
/>
```

---

## 6.0 Animation Performance Guardrails

- [ ] **Compositor Only:** Only animate `transform` and `opacity`.
- [ ] **Avoid `all`:** List specific properties in transitions (e.g., `transition: opacity 0.3s`).
- [ ] **Hardware Acceleration:** Use `translateZ(0)` or `will-change: transform` sparingly.
- [ ] **FPS Check:** Animations must maintain 60fps on average mobile hardware.

---

**See Also:**
- `[15-performance-budgets.md](15-performance-budgets.md)` - Frame budgets
- `[05-component-patterns.md](05-component-patterns.md)` - Implementation patterns
