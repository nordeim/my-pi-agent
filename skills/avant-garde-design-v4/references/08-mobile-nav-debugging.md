# Mobile Navigation Debugging Playbook

## 1.0 Root Cause Taxonomy (Classes A-H)

Identify your issue by matching it to a class:

| Class | Symptom | Primary Root Cause |
|-------|---------|--------------------|
| **A: Z-Index Abyss** | Button is visible but not clickable | Hidden under another transparent layer or stacking context issue. |
| **B: Display Mismatch** | Menu disappears at 768px but doesn't show at 767px | Asymmetrical breakpoint classes (`hidden md:flex` vs `flex sm:hidden`). |
| **C: Prop Drop** | `onClick` doesn't fire | Event propagation blocked or `pointer-events: none` on parent. |
| **D: Viewport Shift** | Menu height is cut off or shifts on scroll | Using `vh` instead of `svh` or `dvh` on mobile viewports. |
| **E: Focus Lock** | Can't tab through menu | `aria-hidden` state or focus-trap failure in custom modals. |
| **F: Hydration Ghost** | Menu works on dev but fails on prod | Hydration mismatch between Server and Client states. |
| **G: Layout Warp** | Content behind menu is scrollable | `body-scroll-lock` not active or improperly applied. |
| **H: Touch Delay** | Nav feels "laggy" on physical device | `passive: true` missing on listeners or heavy CSS filters. |

---

## 2.0 Diagnostic Decision Tree

**Step 1: The "Inspect" Test**
- Inspect the element in Chrome DevTools using "Mobile Mode".
- *Result:* If the inspector highlights a different element when you click the menu, you have a **Class A (Z-Index)** issue.

**Step 2: The "Force" Test**
- Manually toggle the menu state in your React DevTools.
- *Result:* If the UI updates correctly, your **Class C (Prop Drop)** is the issue—the button isn't communicating with the state.

**Step 3: The "Color" Test**
- Add `bg-red-500` to your mobile nav container.
- *Result:* If the red block is visible at all sizes, you have a **Class B (Display Mismatch)**—your hidden/flex logic is flawed.

**Step 4: The "Scroll" Test**
- Open the menu and try to scroll the background.
- *Result:* If it scrolls, you have a **Class G (Layout Warp)**—body lock is failing.

---

## 3.0 Anti-Patterns to Avoid

- **❌ Avoid `100vh`:** Mobile browsers (Safari) have a shifting UI bar. Use `min-h-dvh` (Dynamic Viewport Height) in v4.
- **❌ Avoid `onClick` on `<div>`:** Mobile browsers sometimes delay these events. Use `<button>`.
- **❌ Avoid Fixed Positioning on Inputs:** Can cause the "Keyboard Warp" where the UI jumps when the keyboard opens.

---

## 4.0 Common Fixes (Quick Reference)

**Fix Class A (Z-Index):**
Add `isolation: isolate` to the parent container to create a clean stacking context.

**Fix Class D (Viewport Shift):**
```css
/* Tailwind v4 */
.mobile-menu {
  @apply fixed inset-0 min-h-dvh w-full;
}
```

**Fix Class G (Body Lock):**
```tsx
useEffect(() => {
  if (isOpen) document.body.style.overflow = 'hidden';
  else document.body.style.overflow = 'unset';
}, [isOpen]);
```

---

## 5.0 Verification Checklist

- [ ] Tested on Chrome Mobile Simulator (iOS & Android modes)
- [ ] Tested on Physical Device (Safari & Chrome)
- [ ] Keyboard navigation (Tab/Enter) verified
- [ ] Orientation change (Portrait to Landscape) doesn't break layout
- [ ] "Notch" areas respected using `safe-area-inset`

---

**See Also:**
- `[07-mobile-navigation.md](07-mobile-navigation.md)` - Implementation standards
- `[06-debugging-playbook.md](06-debugging-playbook.md)` - General debugging
