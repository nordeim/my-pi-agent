# Mobile Navigation: Non-Negotiable Guardrails

## 1.0 The Viewport Core
Ensure your `app/layout.tsx` or `_document.tsx` includes:
```html
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5, viewport-fit=cover">
```
*Note: `viewport-fit=cover` is critical for iPhones with "notches".*

---

## 2.0 Symmetrical Breakpoint Strategy
Avoid "Ghost Menus" by ensuring your desktop and mobile navs share the same breakpoint.

**Pattern:**
```tsx
<nav>
  {/* DESKTOP NAV */}
  <div className="hidden md:flex">...</div>
  
  {/* MOBILE NAV TRIGGER */}
  <div className="md:hidden">...</div>
</nav>
```

---

## 3.0 Touch Targets (The 44px Rule)
Every interactive element MUST be at least 44x44px for WCAG AA (ADA compliance).

```tsx
// ❌ TOO SMALL
<button className="p-1"><MenuIcon /></button>

// ✅ ACCESSIBLE
<button className="p-3 focus-visible:ring-2 focus-visible:ring-brand-500">
  <MenuIcon className="h-6 w-6" />
</button>
```

---

## 4.0 Overlay Positioning & Z-Index
Use a standardized z-index scale to prevent stacking order issues.

```css
@theme {
  --z-overlay: 400;
  --z-modal: 500;
}
```

**Mobile Menu Overlay:**
```tsx
<div className="fixed inset-0 z-overlay bg-background/80 backdrop-blur-sm">
  {/* Menu Content */}
</div>
```

---

## 5.0 Semantic Controls & ARIA
Never use a `<div>` for a menu trigger. Use a `<button>` with ARIA states.

```tsx
const [isOpen, setIsOpen] = useState(false);

return (
  <button 
    type="button"
    aria-expanded={isOpen}
    aria-controls="mobile-menu"
    aria-label="Toggle navigation menu"
    onClick={() => setIsOpen(!isOpen)}
  >
    {isOpen ? <CloseIcon /> : <MenuIcon />}
  </button>
);
```

---

## 6.0 shadcn/ui Implementation (Best Practice)
Leverage the `Sheet` component from shadcn/ui (Radix Dialog primitive) for high-end feel and accessibility.

```tsx
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";

export const MobileNav = () => {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" className="md:hidden">
          <MenuIcon />
        </Button>
      </SheetTrigger>
      <SheetContent side="right" className="w-[300px] sm:w-[400px]">
        {/* Nav Links */}
      </SheetContent>
    </Sheet>
  );
};
```

---

## 7.0 Performance Tip: Body Scroll Lock
When the mobile menu is open, the background content MUST be locked.
*shadcn/Radix handles this automatically.* If building custom, use `useLockBodyScroll`.

---

**See Also:**
- `[08-mobile-nav-debugging.md](08-mobile-nav-debugging.md)` - Fixing common nav issues
- `[11-tech-commitments.md](11-tech-commitments.md)` - Performance standards
