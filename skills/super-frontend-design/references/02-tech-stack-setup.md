# Tech Stack & Setup (Core Module 2)

> **Source Skills:** nextjs16-tailwind4, frontend-development, web-frameworks  
> **Purpose:** Initialize production-grade frontend projects with validated modern stacks

---

## 1. Recommended Stack (2026 Validated)

```yaml
Core Framework:
  next: 16.1.4+ (App Router, Server Components, Turbopack, PPR)
  react: 19.2.3+ (React Compiler enabled)
  typescript: 5.9+ (Strict Mode, no `any` types)

Styling & UI:
  tailwindcss: 4.1.18+ (CSS-first, @theme directive, Oxide engine)
  @tailwindcss/vite: 4.1.18+ (Vite plugin, 10x faster builds)
  @tailwindcss/postcss: 4.1.18+ (Legacy PostCSS support)
  radix-ui primitives: Latest (Accessible headless components)
  shadcn/ui: 2.x (Tailwind v4 compatible)
  framer-motion: 12.29.0+ (Animations, respect reduced motion)
  class-variance-authority: Latest (Component variants)
  tailwind-merge: ^3 (Class deduplication)
  clsx: ^2 (Conditional classes)

Forms & Validation:
  react-hook-form: 7.x
  zod: 3.x
  @hookform/resolvers: 5.x

Backend / Data (Optional):
  prisma: 6.x
  bcryptjs: 2.x
  jose: 5.x (JWT handling)

Monorepo (Optional):
  turbo: Latest (Turborepo for multi-app workspaces)
  remixicon: Latest (3100+ SVG icons, outlined/filled styles)

Development:
  eslint: 9.x (Flat config)
  prettier: 3.x + prettier-plugin-tailwindcss
  vitest: 2.x (Unit testing)
  playwright: 1.x (E2E testing)
  lighthouse-ci: Latest (Performance monitoring)
```

---

## 2. Project Initialization

### 2.1 Single Next.js Application
```bash
# Create Next.js project (App Router + TypeScript)
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
cd my-app

# Install Tailwind v4 + shadcn/ui
npm uninstall tailwindcss postcss-import autoprefixer # Remove v3 remnants
npm install tailwindcss@latest @tailwindcss/vite @tailwindcss/postcss
npx shadcn@latest init # Configure with Tailwind v4, TypeScript

# Install RemixIcon (optional)
npm install remixicon

# Start dev server
npm run dev
```

### 2.2 Turborepo Monorepo (Multi-App)
```bash
# Create Turborepo
npx create-turbo@latest my-monorepo
cd my-monorepo

# Structure:
# apps/web/          → Customer-facing Next.js app
# apps/admin/        → Admin dashboard Next.js app
# apps/docs/         → Documentation site
# packages/ui/       → Shared components (shadcn/ui + RemixIcon)
# packages/config/   → Shared ESLint/TypeScript configs
# packages/types/    → Shared TypeScript types
# turbo.json         → Build pipeline

# Configure Next.js apps in apps/ with shared packages
# Install remixicon in shared UI package
npm install remixicon --workspace=packages/ui

# Run all apps
npm run dev

# Build all packages
npm run build
```

---

## 3. Tailwind v4 CSS-First Configuration

### 3.1 Critical: No `tailwind.config.js`
All theme tokens live in CSS via `@theme` directive:

```css
/* src/app/globals.css */
@import "tailwindcss";

@theme {
  /* Color Palette (OKLCH for wide gamut) */
  --color-void: #050506;
  --color-void-light: oklch(0.13 0.01 240);
  --color-aurora-cyan: oklch(0.87 0.16 184);
  --color-champagne: oklch(0.85 0.07 84);
  --color-champagne-dark: oklch(0.67 0.06 76);

  /* Typography */
  --font-sans: "Geist", "Inter", system-ui, sans-serif;
  --font-serif: "Instrument Serif", "Georgia", serif;

  /* Spacing (dynamic values allowed) */
  --spacing-18: 4.5rem;
  --spacing-88: 22rem;

  /* Animations */
  --animate-aurora-slow: aurora-slow 20s ease-in-out infinite;
  @keyframes aurora-slow {
    0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.8; }
    33% { transform: translate(30%, 20%) scale(1.1); opacity: 0.6; }
    66% { transform: translate(-20%, 30%) scale(0.9); opacity: 0.7; }
  }
}

@layer base {
  * { border-color: currentColor; }
  html { scroll-behavior: smooth; }
  body {
    background-color: var(--color-void);
    color: var(--color-slate-100);
    font-family: var(--font-sans);
    -webkit-font-smoothing: antialiased;
  }
  h1, h2, h3, h4, h5, h6 { font-family: var(--font-serif); }
}

@utility glass-panel {
  background-color: oklch(0.13 0.01 240 / 0.3);
  backdrop-filter: blur(12px);
  border: 1px solid oklch(0.2 0.01 240 / 0.5);
}
```

### 3.2 Vite Configuration (Recommended)
```javascript
// vite.config.ts
import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [tailwindcss(), react()],
});
```

### 3.3 PostCSS Legacy Configuration
```javascript
// postcss.config.mjs
export default { plugins: ["@tailwindcss/postcss"] };
```

---

## 4. Directory Structure

### 4.1 Single Next.js App
```
project-root/
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Root layout, fonts, metadata
│   │   ├── page.tsx            # Home page
│   │   ├── globals.css         # Tailwind v4 theme + tokens
│   │   └── (routes)/           # Route groups
│   ├── components/
│   │   ├── layout/             # Navbar, Footer, Shell
│   │   ├── sections/           # Hero, Features, Pricing
│   │   └── ui/                 # shadcn primitives + custom variants
│   ├── lib/
│   │   ├── utils.ts            # cn(), formatters, helpers
│   │   └── hooks/              # useReducedMotion, useScrollSpy
│   ├── data/                   # Static content (nav items, features)
│   └── types/                  # Global TypeScript types
├── public/                     # Static assets
├── next.config.ts
├── tsconfig.json
└── package.json
```

### 4.2 Turborepo Monorepo
```
my-monorepo/
├── apps/
│   ├── web/              # Customer Next.js app
│   ├── admin/            # Admin Next.js app
│   └── docs/             # Documentation site
├── packages/
│   ├── ui/               # Shared UI (shadcn + RemixIcon)
│   ├── api-client/       # Shared API client
│   ├── config/           # ESLint, TypeScript configs
│   └── types/            # Shared types
├── turbo.json            # Build pipeline
└── package.json
```

**turbo.json pipeline:**
```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**", "dist/**"]
    },
    "dev": { "cache": false, "persistent": true },
    "lint": {},
    "test": { "dependsOn": ["build"] }
  }
}
```

---

## 5. React/TypeScript Patterns (frontend-development)

### 5.1 Import Aliases
| Alias | Resolves To | Example |
|-------|-------------|---------|
| `@/` | `src/` | `import { apiClient } from '@/lib/apiClient'` |
| `~types` | `src/types` | `import type { User } from '~types/user'` |
| `~components` | `src/components` | `import { Button } from '~components/Button'` |
| `~features` | `src/features` | `import { authApi } from '~features/auth'` |

### 5.2 Component Checklist
- [ ] Use `React.FC<Props>` with TypeScript
- [ ] Lazy load heavy components: `React.lazy(() => import())`
- [ ] Wrap in `<SuspenseLoader>` for loading states
- [ ] Use `useSuspenseQuery` for data fetching
- [ ] Use `useCallback` for event handlers passed to children
- [ ] Default export at bottom
- [ ] No early returns with loading spinners
- [ ] Use `useMuiSnackbar` for user notifications (if MUI)

### 5.3 Feature-Based Organization
```
src/features/my-feature/
├── api/          # API service layer
├── components/   # Feature components
├── hooks/        # Custom hooks
├── helpers/      # Utility functions
├── types/        # TypeScript types
└── index.ts      # Public exports
```

---

## 6. RemixIcon Integration (web-frameworks)

### 6.1 Webfont Usage
```tsx
// In layout.tsx
import 'remixicon/fonts/remixicon.css';

// In components
<i className="ri-home-line ri-2x"></i>
<i className="ri-search-fill"></i>
```

### 6.2 React Component Usage
```tsx
import { RiHomeLine, RiSearchFill } from "@remixicon/react";

<RiHomeLine size={24} />
<RiSearchFill size={32} color="var(--color-champagne)" />
```

---

## 7. Verification Checklist
- [ ] Tailwind v4 installed (no `tailwind.config.js` present)
- [ ] `@theme` directive in `globals.css` with project tokens
- [ ] TypeScript strict mode enabled
- [ ] shadcn/ui initialized with Tailwind v4
- [ ] All imports use aliases (`@/`, `~types`, etc.)
- [ ] RemixIcon installed (if using)
- [ ] Turborepo pipeline configured (if monorepo)

---

## 8. Related References
- [03-design-system.md](03-design-system.md) → Typography, color, spacing
- [04-component-architecture.md](04-component-architecture.md) → shadcn/ui, MUI patterns
- [05-performance-optimization.md](05-performance-optimization.md) → Bundle, waterfalls
