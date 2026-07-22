# Visual & Technical Debugging Playbook

## 1.0 The 6-Step Visual Debugging Protocol

When an element isn't rendering as expected, follow this decision tree:

**Step 1: Presence Check**
- Is the element in the DOM?
- *Check:* Use DevTools "Elements" panel.
- *If NO:* Component logic is failing (conditional rendering, props issues).

**Step 2: Visibility Check**
- Is it hidden by CSS?
- *Check:* `display: none`, `visibility: hidden`, `opacity: 0`, `height/width: 0`.
- *Check:* Is it being clipped by `overflow: hidden` on a parent?

**Step 3: Stacking Context Check**
- Is it behind another element?
- *Check:* `z-index`, `isolation: isolate`, or natural DOM order.
- *Tip:* Use "Layers" panel in Chrome DevTools.

**Step 4: Layout & Position Check**
- Is it off-screen?
- *Check:* `position: absolute/fixed`, `transform: translate`, `top/left` coordinates.
- *Check:* Is the parent `relative`?

**Step 5: Tailwind v4 Variable Check**
- Is the CSS variable resolving?
- *Check:* Computed style in DevTools. If you see `var(--color-brand)`, click the variable name to see if it's actually defined in the `:root` or `@theme`.

**Step 6: JS State Check**
- Is a state change failing to trigger the UI update?
- *Check:* React DevTools "Components" panel. Check state and props.

---

## 2.0 Tailwind v4 Specific Debugging

### 2.1 Oxide Engine Issues
If classes aren't appearing in the final CSS:
1. **Source Pattern:** Check your `@source` directives. Are the files actually being scanned?
2. **Dynamic Classes:** Are you using string interpolation? `bg-${color}-500` is **forbidden** in v4. Use a mapping object or full class names.

### 2.2 Variable Resolution Failures
If `bg-(--brand)` isn't working:
- Ensure the variable is defined within a `@theme` block or standard CSS `:root`.
- In v4, variables MUST have the `--` prefix to be used with the parenthesis syntax.

---

## 3.0 Animation Debugging

### 3.1 Detecting "Jank"
- Use the "Performance" tab in DevTools.
- Look for **Red Frames** or "Long Tasks" (>50ms).
- **Audit:** Are you animating `width`, `height`, `top`, or `margin`? 
- **Fix:** ONLY animate `transform` and `opacity`.

### 3.2 Motion/Framer Motion Debugging
- Use `layoutId` only when necessary (high performance cost).
- Check `initial` vs `animate` props.
- **Reduced Motion:** If animations aren't firing, check your OS settings or `useReducedMotion` hook implementation.

---

## 4.0 React & Next.js Debugging

### 4.1 Hydration Mismatches
- **Symptom:** "Text content did not match" warning in console.
- **Cause:** Differing content between Server and Client (e.g., `Date.now()`, `window.innerWidth`, randomized IDs).
- **Fix:** Use `useEffect` for client-only data or `suppressHydrationWarning`.

### 4.2 Server Component Boundaries
- **Symptom:** "Event handlers cannot be passed to Client Component props" or similar.
- **Cause:** Trying to use `onClick` in a Server Component.
- **Fix:** Add `"use client"` directive to the component that needs interactivity.

---

## 5.0 Performance Debugging (2026 Standards)

### 5.1 Cumulative Layout Shift (CLS)
- **Symptom:** Content jumps as images load.
- **Fix:** Always provide `width` and `height` to images (even if using `layout="responsive"`). Use `aspect-ratio` in CSS/Tailwind.

### 5.2 LCP (Largest Contentful Paint)
- **Check:** Is your hero image being lazy-loaded?
- **Fix:** Use `priority` attribute on hero images in Next.js. Preload critical fonts.

---

## 6.0 The "Nuclear Option" Debugging Tool
Add this to your `globals.css` to visualize layout issues instantly:

```css
@utility debug-layout {
  * { outline: 1px solid red !important; }
  * * { outline: 1px solid green !important; }
  * * * { outline: 1px solid blue !important; }
}
```

---

**See Also:**
- `[15-performance-budgets.md](15-performance-budgets.md)` - Metric targets
- `[08-mobile-nav-debugging.md](08-mobile-nav-debugging.md)` - Mobile-specific issues
