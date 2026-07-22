# Avant-Garde Component Patterns Library

## 1.0 Navigation Patterns

### 1.1 The "Glass-Morphic" Sticky Header
- **Strategic Goal:** Institutional Clarity + Modern Feel
- **Behavior:** Minimalist bar with subtle blur that doesn't overwhelm content.

```tsx
// src/components/layout/Navbar.tsx
import { cn } from "@/lib/utils";

export const Navbar = ({ className }: { className?: string }) => {
  return (
    <nav className={cn(
      "fixed top-0 z-sticky w-full border-b border-border/40",
      "bg-background/60 backdrop-blur-md backdrop-saturate-150",
      className
    )}>
      <div className="container flex h-16 items-center justify-between">
        <Logo className="w-24" />
        <div className="hidden md:flex items-center gap-8">
          <NavLink href="/courses">Courses</NavLink>
          <NavLink href="/community">Community</NavLink>
          <Button variant="outline" size="sm">Sign In</Button>
          <Button size="sm">Get Started</Button>
        </div>
        <MobileNav className="md:hidden" />
      </div>
    </nav>
  );
};
```

---

## 2.0 Card Patterns

### 2.1 The "Tactile Depth" Feature Card
- **Strategic Goal:** Dynamic Modernism
- **Visual:** Uses subtle shadows and border-shimmers to feel physically reactive.

```tsx
// src/components/ui/FeatureCard.tsx
export const FeatureCard = ({ title, description, icon: Icon }: any) => {
  return (
    <div className="group relative overflow-hidden rounded-2xl border bg-card p-8 transition-all hover:border-brand-500/50 hover:shadow-2xl hover:shadow-brand-500/10">
      <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-brand-500/10 text-brand-500 ring-1 ring-brand-500/20 transition-transform group-hover:scale-110">
        <Icon className="h-6 w-6" />
      </div>
      <h3 className="mb-2 text-xl font-bold">{title}</h3>
      <p className="text-muted-foreground leading-relaxed">{description}</p>
      
      {/* Background Gradient Shimmer */}
      <div className="absolute -right-10 -top-10 h-32 w-32 rounded-full bg-brand-500/5 blur-3xl transition-opacity group-hover:opacity-100" />
    </div>
  );
};
```

---

## 3.0 Section Patterns

### 3.1 The "Vertical Narrative" Hero
- **Strategic Goal:** Rejecting hero-split cliché.
- **Visual:** Large typography that flows vertically, creating a magazine feel.

```tsx
// src/components/sections/Hero.tsx
export const Hero = () => {
  return (
    <section className="relative flex min-h-[90vh] flex-col items-center justify-center overflow-hidden py-24">
      <div className="container relative z-base text-center">
        <span className="mb-6 inline-block rounded-full bg-brand-500/10 px-4 py-1 text-sm font-semibold text-brand-500 uppercase tracking-widest">
          Version 4.0 Launch
        </span>
        <h1 className="mx-auto mb-8 max-w-4xl text-6xl font-black leading-[1.05] tracking-tight sm:text-8xl">
          The <span className="text-brand-500">Intention</span> Behind Every Pixel.
        </h1>
        <p className="mx-auto mb-10 max-w-2xl text-xl text-muted-foreground">
          Expert-led education for designers who refuse to be generic. 
          Build the future of the web with Tailwind v4 and React 19.
        </p>
        <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
          <Button size="lg" className="h-14 px-10 text-lg">Join the Academy</Button>
          <Button size="lg" variant="outline" className="h-14 px-10 text-lg">View Curriculum</Button>
        </div>
      </div>
      
      {/* Avant-Garde Background Decor */}
      <div className="absolute inset-0 -z-behind opacity-20 [mask-image:radial-gradient(ellipse_at_center,black,transparent)]">
        <div className="absolute left-1/2 top-1/2 h-[800px] w-[800px] -translate-x-1/2 -translate-y-1/2 bg-[conic-gradient(from_0deg_at_50%_50%,#f27a1a_0deg,#4f46e5_120deg,#f27a1a_360deg)] blur-[120px]" />
      </div>
    </section>
  );
};
```

---

## 4.0 Form Patterns

### 4.1 The "Search Command" Palette
- **Strategic Goal:** Utility + High-End Feel
- **Visual:** Mimics MacOS Spotlight or Raycast for search.

```tsx
// src/components/ui/CommandPalette.tsx
// Note: Requires cmdk or shadcn command component
export const SearchTrigger = () => {
  return (
    <button className="flex w-64 items-center justify-between rounded-lg border bg-muted/50 px-4 py-2 text-sm text-muted-foreground transition-colors hover:bg-muted focus:outline-none focus:ring-2 focus:ring-brand-500/40">
      <span className="flex items-center gap-2">
        <SearchIcon className="h-4 w-4" />
        Search curriculum...
      </span>
      <kbd className="rounded bg-muted-foreground/10 px-1.5 font-mono text-[10px] font-medium opacity-100">
        ⌘K
      </kbd>
    </button>
  );
};
```

---

## 5.0 Animation Patterns

### 5.1 Staggered Entrance (Motion)
- **Library:** Motion (v12+)

```tsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: { y: 0, opacity: 1, transition: { duration: 0.5, ease: "easeOut" } }
};

// Usage
<motion.div variants={containerVariants} initial="hidden" animate="visible">
  <motion.div variants={itemVariants}>Item 1</motion.div>
  <motion.div variants={itemVariants}>Item 2</motion.div>
</motion.div>
```

---

**See Also:**
- `[14-animation-standards.md](14-animation-standards.md)` - Timing and easing reference
- `[09-color-palettes.md](09-color-palettes.md)` - Palette implementation
