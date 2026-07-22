# Tailwind CSS v4 Common Pitfalls & Migration Guide

## 1.0 The "Zombie Config" Problem

**Pitfall:** Keeping `tailwind.config.js` and expecting v4 to respect it.
**Reality:** v4 is CSS-first. While there is a compatibility layer, it is significantly slower and may be removed in future versions.

**Solution:** Migrate all configurations to the `@theme` block in your CSS.

```css
/* ❌ AVOID */
@import "tailwindcss";
/* relying on tailwind.config.js */

/* ✅ EMBRACE */
@import "tailwindcss";

@theme {
  --color-brand: #f27a1a;
}
```

---

## 2.0 @apply Breaking Changes

**Pitfall:** Using `@apply` with complex, nested, or state-dependent utilities.
**Reality:** v4's compiler is more strict about what can be applied.

**Common Failure:**
```css
/* ❌ FAILS in v4 */
.my-class {
  @apply hover:bg-red-500/50 transition-all duration-300;
}
```

**Solution:** Move complex logic to a `@utility` or use standard CSS nesting.

```css
/* ✅ BETTER */
@utility my-class {
  @apply transition-all duration-300;
  
  &:hover {
    background-color: oklch(0.63 0.26 25 / 0.5);
  }
}
```

---

## 3.0 @source and Content Detection

**Pitfall:** v4 failing to detect classes in monorepos or non-standard file extensions.
**Reality:** v4's auto-detection is powerful but relies on the `@source` directive for specific paths.

**Solution:** Explicitly define your source paths if classes aren't appearing.

```css
@import "tailwindcss";
@source "../../packages/ui/src/**/*.tsx";
@source "../other-app/src/**/*.vue";
```

---

## 4.0 Arbitrary Value Syntax

**Pitfall:** Using v3 square bracket syntax `bg-[#000]` for CSS variables.
**Reality:** v4 introduces a more natural parenthesis syntax for variables.

| v3 Syntax | v4 Syntax |
|-----------|-----------|
| `w-[--my-width]` | `w-(--my-my-width)` |
| `bg-[var(--brand)]` | `bg-(--brand)` |

**Note:** v4 still supports `[]` for literal values like `top-[13px]`, but `()` is preferred for variables.

---

## 5.0 OKLCH Rendering vs. RGB/HEX

**Pitfall:** Unexpected color shifts when using opacity modifiers.
**Reality:** v4 defaults to OKLCH for internal color calculations, which maintains perceived lightness better than RGB.

**The "Grayish" Problem:** When mixing a HEX color with 50% opacity in v4, it might look slightly different than in v3 because the interpolation happens in OKLCH space.

---

## 6.0 Build Time Regressions

**Pitfall:** Using too many complex `@apply` rules or legacy plugins.
**Reality:** v4 is built on the Rust-powered Oxide engine. If your build is slow (>200ms for incremental), you likely have a legacy bottleneck.

**Checklist:**
1. Remove all `postcss` plugins that Tailwind now handles natively (nesting, autoprefixer).
2. Remove `tailwind.config.js` completely.
3. Check for circular `@import` references.

---

## 7.0 Gradient Variables Incompatibility

**Pitfall:** Passing variable names to gradients in a way that worked in v3 but fails in v4.
**Reality:** v4 gradients (`bg-linear-to-r`) expect specific token formats.

```css
/* ❌ AVOID */
.gradient {
  --start: red;
  --end: blue;
  @apply bg-gradient-to-r from-[var(--start)] to-[var(--end)];
}

/* ✅ EMBRACE (Native v4 syntax) */
@theme {
  --color-grad-start: red;
  --color-grad-end: blue;
}

.gradient {
  @apply bg-linear-to-r from-grad-start to-grad-end;
}
```

---

## 8.0 Quick Migration Checklist

- [ ] Update `@tailwindcss/vite` or `@tailwindcss/postcss` to v4.
- [ ] Replace `@tailwind base/components/utilities` with `@import "tailwindcss"`.
- [ ] Port `theme.extend` from `tailwind.config.js` to `@theme` block.
- [ ] Replace `bg-gradient-*` with `bg-linear-*`.
- [ ] Update arbitrary variable syntax from `[]` to `()`.
- [ ] Remove legacy plugins (forms, typography, aspect-ratio) as they are now built-in or handled differently.
- [ ] Verify OKLCH color contrast in dark mode.

---

**See Also:**
- `[02-tailwind-v4-deep-dive.md](02-tailwind-v4-deep-dive.md)` - Core configuration guide
- `[06-debugging-playbook.md](06-debugging-playbook.md)` - Visual debugging protocols
