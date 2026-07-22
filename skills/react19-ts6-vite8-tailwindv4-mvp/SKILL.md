---
name: react19-ts6-vite8-tailwindv4-mvp
description: >
  MVP/production React 19 + TypeScript 6 strict + Vite 8 (Rolldown) + Tailwind CSS v4 CSS-first @theme. File-based routing, pnpm, Vitest + Playwright E2E. Covers complete lifecycle from scaffold to shipping tested, type-safe, WCAG AAA, production-grade code. Use when building new greenfield web apps with modern React + Vite + Tailwind v4.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, SearchWeb, FetchURL
license: MIT
version: 3.0.0
---

# React 19 + TypeScript 6 + Vite 8 MVP — Production-Ready Web App Skill

Use when building a new MVP or production web application using modern React, TypeScript strict mode, Vite 8 (Rolldown), Tailwind CSS v4, and file-based routing. Covers the complete lifecycle from `npm init` to shipping tested, type-safe, production-grade code.

> 🎯 **One-Shot Prevention:** Every section in this skill was extracted from real-world remediation cycles (see §26). Skipping any section that seems "obvious" or "optional" creates rework. Follow the full checklist in §25 before claiming completion — it prevents the 15 most common "works but isn't production-ready" gaps.

## Skill Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| Framework | React | ^19.2 | Concurrent features, `useActionState`, `useOptimistic` |
| Language | TypeScript | ^6.0 | Strict, `erasableSyntaxOnly`, no `any` |
| Build Tool | Vite | ^8.0 | Rolldown engine, HMR, production bundling |
| Styling | Tailwind CSS | ^4.2 | CSS-first `@theme inline`, no config file |
| Router | TanStack Router | ^1.169 | File-based, type-safe routing |
| State | Zustand | ^5.0 | Lightweight, `persist` middleware |
| Validation | Zod | ^4.4+ | Runtime schema validation at boundaries |
| UI Primitives | shadcn/ui | Latest | Accessible component base |
| Icons | Lucide React | ^0.563 | SVG icon set |
| Testing | Vitest | ^4.1 | Unit + behavioral testing (jsdom) |
| Testing | Testing Library | ^16.3 | React component testing |
| Utilities | clsx + tailwind-merge | Latest | Conditional class composition |

---

## 1. Bootstrap New Project

**Step 1: Scaffold**
```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
```

**Step 2: Install core dependencies**
```bash
npm install react@^19.2 react-dom@^19.2 zustand@^5.0 @tanstack/react-router@^1.169 clsx tailwind-merge lucide-react@^0.563
```

**Step 3: Install dev dependencies** (`--legacy-peer-deps` for Vite 8 compatibility)
```bash
npm install --legacy-peer-deps -D \
  typescript@^6.0 vite@^8.0 @vitejs/plugin-react@^4.0 \
  tailwindcss@^4.2 @tailwindcss/vite@^4.2 vitest@^4.1 @testing-library/react@^16.3 \
  @testing-library/jest-dom@^6.0 jsdom @types/react@^19.0 @types/react-dom@^19.0 \
  @tanstack/router-plugin@^1.169
```
> **Note:** React 19 still relies on DefinitelyTyped for TypeScript declarations. `@types/react` and `@types/react-dom` are required. Dependabot PRs across GitHub consistently bump `@types/react` alongside React 19 upgrades to 19.1.1 in July 2025, confirming the types package remains essential.

**Step 4: Verify**
```bash
npx tsc --version      # >= 6.0
npm run build          # Should succeed
npx vitest run         # Exits 0 (0 tests found = environment confirmed)
```

---

## 2. TypeScript Configuration (Non-Negotiable)

`tsconfig.json`
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "useDefineForClassFields": true,
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "erasableSyntaxOnly": true,
    "verbatimModuleSyntax": true,
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"],
      "@hooks/*": ["./src/hooks/*"],
      "@lib/*": ["./src/lib/*"],
      "@routes/*": ["./src/routes/*"],
      "@stores/*": ["./src/stores/*"],
      "@shared/*": ["./src/components/shared/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

<details>
<summary>📄 tsconfig.node.json (Vite Config Types)</summary>

```json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
```
</details>

**CRITICAL RULES**
| Rule | Rationale |
|---|---|
| No `any` | Use `unknown` or proper types. `strict: true` enforces. |
| No `enum` | `erasableSyntaxOnly` rejects. Use union types. |
| No `namespace` | Same rejection. Use ES modules. |
| No `baseUrl` | Deprecated in TS 6.0. Use `"./"` prefix in `paths`. |
| `@shared/*` optional | Only if you have a `src/components/shared/` directory. Remove if empty. |
| No unused vars | `noUnusedLocals`, `noUnusedParameters`. Build will fail. |
| Explicit types | Use `import type` for type-only imports. Example: `import type { UIState } from '@stores/ui'` |

---

## 3. Tailwind CSS v4 Configuration

`src/globals.css` — CSS-First, No `tailwind.config.js`

```css
@import "tailwindcss";

@theme inline {
  /* Semantic Color Tokens (Replace hex values with your brand palette) */
  --color-primary: #C4A882;
  --color-primary-hover: #B09570;
  --color-surface: #FAF8F5;
  --color-surface-muted: #EDE8DF;
  --color-text-primary: #3D3832;
  --color-text-muted: #7A7268;
  --color-border: #D5CFC4;

  /* Typography */
  /* Tip: Pair a serif display font for headings with a sans-serif body font to establish brand hierarchy. */
  --font-heading: 'Inter', system-ui, sans-serif;
  --font-body: 'Inter', system-ui, sans-serif;

  /* Spacing Scale (semantic names, not px) */
  --spacing-1: 4px;
  --spacing-2: 8px;
  --spacing-3: 16px;
  --spacing-4: 24px;

  /* Z-Index Tokens */
  --z-base: 0;
  --z-raised: 10;
  --z-sticky: 100;
  --z-overlay: 200;
  --z-panel: 300;
  --z-modal: 400;
  --z-toast: 500;

  /* Custom Animations */
  --animate-fade-in-up: fade-in-up 800ms ease-out forwards;

  @keyframes fade-in-up {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
  }
}

@layer base {
  html { scroll-behavior: smooth; }
  body {
    font-family: var(--font-body);
    color: var(--color-text-primary);
    background-color: var(--color-surface);
  }
  :focus-visible {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
  }
}

@layer utilities {
  .container-custom {
    width: 100%;
    max-width: 1280px;
    margin-inline: auto;
    padding-inline: 24px;
  }
}

/* Reduced Motion (Aligns with WCAG 2.3.3 — Animation from Interactions) */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Tailwind v4 Rules**
- No `tailwind.config.js` — all configuration lives in `globals.css`
- **ZERO raw hex in `className`**. All colors via `@theme` tokens. `text-wool-900`, not `text-[#3D3835]`.
- Every `--color-*` token defined in `@theme` must have at least one UI consumer. Orphaned tokens defeats the design system.
- **Reuse layout utilities via `@layer utilities`**. If 14 files repeat `container mx-auto max-w-[1280px] px-6`, register `.container-custom` once and use it everywhere.
- Mobile-first: `sm:`, `md:`, `lg:`
- Custom `@keyframes` inside `@theme inline`
- Complex classes in `@layer utilities`
- Font utilities in `@layer utilities` (`.font-display`), never inline font-family strings

> **🎨 Brand Token Mapping:** Replace the semantic hex values above with your design system. Keep the `--color-*` naming convention to maintain component portability across projects.

---

## 4. Negative Value Gotcha (Tailwind v4)

```tsx
/* ❌ WRONG: Tailwind v4 silently ignores this */
className="absolute bottom--24 left--24"
/* Element gets NO positioning. Result: sits at default position. */

/* ✅ CORRECT: Single hyphen prefix for negative values */
className="absolute -bottom-24 -left-24"
```
**Rule:** Tailwind v4 does NOT parse `bottom--24` as negative. Double hyphen is a literal token, not negation. Always use single hyphen prefix (`-bottom-24`).

---

## 5. Vite 8 Configuration

`vite.config.ts` — Unified Config (Vite + Vitest) with Function-form `manualChunks`

```ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import { tanstackRouter } from '@tanstack/router-plugin/vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    tanstackRouter({ target: 'react', autoCodeSplitting: true }),
    tailwindcss(),
    react()
  ],
  resolve: {
    alias: {
      '@': '/src',
      '@components': '/src/components',
      '@hooks': '/src/hooks',
      '@lib': '/src/lib',
      '@routes': '/src/routes',
      '@stores': '/src/stores',
      '@shared': '/src/components/shared'
    }
  },
  // ⚠️ CRITICAL: Vite 8 / Rolldown requires FUNCTION FORM
  build: {
    manualChunks: (id: string) => {
      if (id.includes('react')) return 'react-vendor'
      if (id.includes('tanstack')) return 'router-vendor'
      if (id.includes('lucide')) return 'lucide'
    }
  },
  // Vitest configuration (unified approach)
  test: {
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts'
    // Note: globals: true is omitted. Explicit imports (describe, it, expect) are preferred per Vitest ESLint best practices.
  }
})
```
> **🔧 Plugin Export Name:** The official TanStack Router Vite plugin uses the named export `tanstackRouter` (lowercase). The old `TanStackRouterVite` name was deprecated and removed. Using the old name produces `Module has no exported member 'TanStackRouterVite'`.

**Vite 8 Key Gotchas**
- `manualChunks` must be a **FUNCTION**, not an object
- `--legacy-peer-deps` required for dependency installation
- Using `vitest/config` enables the `test` property without type errors
- `@babel/plugin-react-compiler` post-stable — optional for now

---

## 6. TanStack Router — File-Based Routing

**Route File Convention**
```
src/routes/
├── __root.tsx         # Root layout (Navbar, Footer, Overlays)
├── index.tsx          # / (Home)
├── about.tsx          # /about
├── features.index.tsx # /features
├── features.$id.tsx   # /features/:id
├── $.tsx              # Catch-all 404 route
└── dashboard.tsx      # /dashboard
```
After **EVERY** route change, run:
```bash
npx tsr generate
```
> **404 Handling:** Create `src/routes/$.tsx` for unmatched paths. TanStack Router will automatically throw a not-found error when a path doesn't match any known route pattern, and the `CatchNotFound` component (or a catch-all route) handles it. Regenerate the route tree after adding it.

**Root Layout Pattern**
```tsx
import { createRootRoute, Outlet } from '@tanstack/react-router'
import { Navbar } from '@components/layout/Navbar'
import { Footer } from '@components/layout/Footer'
import { ModalOverlay } from '@shared/ModalOverlay'
import { SlidePanel } from '@shared/SlidePanel'

export const Route = createRootRoute({ component: RootComponent })

function RootComponent() {
  return (
    <>
      <Navbar />
      {/* Sync pt value with Navbar height. Use CSS var for single source of truth. */}
      <main className="min-h-screen pt-[var(--navbar-height,72px)]">
        <Outlet />
      </main>
      <Footer />
      <ModalOverlay />
      <SlidePanel />          {/* Z-index: --z-panel (300) */}
    </>
  )
}
```

**Navigation**
```tsx
// ✅ CORRECT
<Link to="/features/$id" params={{ id: feature.id }}>

// ❌ WRONG (string interpolation for route params)
<Link to={`/features/${feature.id}`}>
```

---

## 7. Zustand State Management

**Pattern:** Flat Stores, Selector Subscriptions, Persist Middleware

```ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface UIState {
  isPanelOpen: boolean
  toasts: { id: string; message: string; type: 'success' | 'error' }[]
  openPanel: () => void
  closePanel: () => void
  addToast: (message: string, type: 'success' | 'error') => void
}

export const useUIStore = create<UIState>()(
  persist(
    (set, get) => ({
      isPanelOpen: false,
      toasts: [],
      openPanel: () => set({ isPanelOpen: true }),
      closePanel: () => set({ isPanelOpen: false }),
      addToast: (message, type) => set((state) => ({
        // jsdom-safe ID generation (crypto.randomUUID() is unavailable in test env)
        // Vitest JSDOM: window.crypto.randomUUID() throws TypeError. Polyfill via setupFiles
        // or use this deterministic fallback.
        toasts: [...state.toasts, { id: `${Date.now()}-${Math.random().toString(36).slice(2)}`, message, type }]
      }))
    }),
    {
      name: 'app-ui-state',
      // CRITICAL: Ephemeral UI state (toasts, isOpen) must NEVER be persisted.
      // Only persist domain data (cart, auth, preferences).
      partialize: () => ({})
    }
  )
)
```

**Zustand Rules (Critical)**
| Rule | Example |
|---|---|
| ✅ Selector in JSX | `const isOpen = useUIStore(s => s.isPanelOpen)` |
| ❌ `.getState()` in JSX | `useUIStore.getState().isPanelOpen` (stale, no re-renders) |
| ✅ Persist data only | `partialize: (s) => ({ preferences: s.preferences })` |
| ❌ Persist UI state | Never persist `isOpen`, `isLoading`, `toasts`, etc. |

**Store-to-Store Calls (Internal OK)**
```ts
// OK inside store logic (not JSX)
submitForm: async (data) => {
  set({ isLoading: true })
  await api.save(data)
  useUIStore.getState().addToast('Saved!', 'success')  // ✅ Store-to-store
  set({ isLoading: false })
}
```

> **🔄 Domain Adaptation:** Swap `UIState` with domain-specific stores (`useCartStore`, `useAuthStore`, etc.) as needed. Keep the flat structure and `partialize` discipline.

---

## 8. React 19 — Modern Hook Patterns

**`useActionState` for Forms**
```tsx
import { useActionState } from 'react'
import { newsletterSchema } from '@lib/schemas'

const [state, formAction, isPending] = useActionState(
  async (_prev, formData: FormData) => {
    const data = Object.fromEntries(formData) as Record<string, string>
    const result = newsletterSchema.safeParse({ email: data.email })
    if (!result.success) {
      return { message: result.error.issues[0].message, type: 'error' as const }
    }
    await new Promise(r => setTimeout(r, 1000))  // Simulate API call
    return { message: 'Subscribed!', type: 'success' as const }
  },
  { message: '', type: 'idle' as const }
)
```

> **🔐 Validation at Boundaries:** Always validate at form submission, API input, or any system boundary. Internal code should trust typed contracts. Never do inline manual checks like `if (!email?.includes('@'))` — use a schema library.

// Use action prop (React 19 feature, not onSubmit for API calls)
<form action={formAction}>
  <input name="email" placeholder="Email" />
  <button disabled={isPending}>
    {isPending ? 'Subscribing...' : 'Subscribe'}
  </button>
  {state.type !== 'idle' && (
    <p className={state.type === 'error' ? 'text-red-500' : 'text-green-500'}>
      {state.message}
    </p>
  )}
</form>
```

**`useOptimistic` for UI Feedback (e.g. Add-to-Cart)**
```tsx
import { useOptimistic, startTransition } from 'react'

const [isAdding, setIsAdding] = useOptimistic(false)

// ✅ CORRECT: setter must be called inside startTransition (React 19 Action)
// If addItem() throws, React reverts the optimistic state automatically.
const handleAddToCart = () => {
  startTransition(async () => {
    setIsAdding(true)
    await addItem({ productId, color, size, qty: 1 })  // Simulated API
    addToast('Added to cart', 'success')
    setIsAdding(false)
    openCart()
  })
}

// In JSX: disabled={isAdding} + loading spinner
<Button isLoading={isAdding} onClick={handleAddToCart}>Add to Cart</Button>
```

---

## 9. Form Validation with Zod at System Boundaries

Validation belongs at the edges — form submission, API calls, URL params. Internal code trusts typed contracts. Install `zod` and define schemas in a central file.

### Installation
```bash
npm install zod@^4.4  # Zod v4 — note the API change from v3
```

### Schema Definitions
```ts
// src/lib/schemas.ts
import { z } from 'zod'

export const newsletterSchema = z.object({
  email: z.string().min(1, 'Email is required').email('Invalid email.'),
})

export const checkoutSchema = z.object({
  fullName: z.string().min(2).max(100),
  email: z.string().email(),
  address: z.string().min(5),
  city: z.string().min(1),
  postalCode: z.string().regex(/^\d{3,6}$/, 'Valid postal code required.'),
})

export type NewsletterInput = z.infer<typeof newsletterSchema>
export type CheckoutInput = z.infer<typeof checkoutSchema>
```

### Usage in `useActionState`
```tsx
import { checkoutSchema } from '@lib/schemas'

const [state, formAction] = useActionState<CheckoutState, FormData>(
  async (_prev, formData) => {
    const data = Object.fromEntries(formData) as Record<string, string>
    const result = checkoutSchema.safeParse(data)  // ✅ Schema-driven, not manual
    if (!result.success) {
      return { step: 'shipping', error: result.error.issues[0].message }
    }
    await submitOrder(data)
    return { step: 'confirmation', error: '' }
  },
  { step: 'shipping', error: '' }
)
```

**⚠️ Zod v4 Breaking Change:**
```ts
// ❌ WRONG (v3 API)
result.error.errors[0].message
// ✅ CORRECT (v4 API)
result.error.issues[0].message   // v4 uses `issues[]`, not `errors[]`
```

---

## 10. Typed Service Layer (Repository Pattern)

Decouple data access from consumers. Define a typed interface, then swap implementations (in-memory → API) without touching consumer code.

```ts
// src/services/products.ts
import { products as catalog } from '@lib/products'
import type { Product } from '@/types/product'

export interface ProductService {
  getAll(): readonly Product[]
  getBySlug(slug: string): Product | undefined
  sort(list: readonly Product[], by: SortOption): readonly Product[]
}

const productService: ProductService = {
  getAll: () => catalog,
  getBySlug: (slug) => catalog.find(p => p.slug === slug),
  sort: (list, by) => [...list].sort((a, b) => /* ... */),
}

export { productService }
```

**Why this matters:** When you switch from `catalog` (in-memory) to `fetch('/api/products')`, only `products.ts` changes. Every route, component, and test stays intact.

---

## 11. Barrel Exports for Clean Boundaries

Use `index.ts` barrel files at directory roots to prevent deep-path coupling and keep imports stable during refactors.

```ts
// src/components/index.ts
export { Button } from './ui/button'
export { CartSlidePanel } from './cart/CartSlidePanel'
export { NewsletterSection } from './sections/NewsletterSection'
export { ErrorBoundary } from './shared/ErrorBoundary'

// src/lib/index.ts
export { cn } from './utils'
export { formatPrice } from './format'
export { newsletterSchema, checkoutSchema } from './schemas'

// Consumer (clean, refactor-proof)
import { Button, CartSlidePanel } from '@/components'
import { newsletterSchema } from '@/lib'
```

**Note:** Barrel files are for *public* module boundaries. Keep internal ad-hoc imports within the same directory.

---

## 12. `inert` and Boolean Props (TS2322 Trap)

```tsx
// ❌ WRONG: `inert` is a BOOLEAN React prop, not a string
<aside inert={isOpen ? undefined : 'true'} />  // TS2322 error

// ✅ CORRECT: Boolean expression or omitted when false
<aside inert={!isOpen} />

// Rule: inert, contentEditable, autoFocus, readOnly are ALL boolean props.
// Never pass a string value.
```

---

## 13. Testing — TDD with Vitest + jsdom

**Test Setup**
If using the unified config in §5, the `test` block is already defined. If you prefer a separate config, create `vitest.config.ts`:
```ts
import { defineConfig } from 'vitest/config'
export default defineConfig({
  test: {
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts'
  }
})
```

**Setup file (`src/test/setup.ts`)**
```ts
import '@testing-library/jest-dom/vitest'
```
> **Note:** The `/vitest` subpath import is the officially recommended approach for Vitest integration. Testing Library docs specify: `import '@testing-library/jest-dom/vitest'`. The bare `@testing-library/jest-dom` import is the Jest-compatible path that may not register matchers correctly in Vitest.

**TanStack Router `Link` Mocking**
```ts
vi.mock('@tanstack/react-router', () => ({
  Link: ({ children, ...props }: { children: React.ReactNode } & Record<string, unknown>) => (
    <a {...props}>{children}</a>
  )
}))
```

**React 19 Async State Updates in Tests**
```tsx
import { act, render, screen } from '@testing-library/react'

// ❌ WRONG: State updates outside fireEvent need act()
useUIStore.getState().openPanel()
expect(screen.getByRole('dialog')).toHaveClass('translate-x-0')  // FAILS

// ✅ CORRECT: Wrap store mutations in act() so DOM flushes
await act(async () => {
  useUIStore.getState().openPanel()
})
```

**TDD Template**
```ts
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, fireEvent, act } from '@testing-library/react'
import { useUIStore } from '@stores/ui'

describe('MyComponent', () => {
  beforeEach(() => {
    // Reset store before each test
    useUIStore.getState().closePanel()
  })

  it('renders empty state', () => {
    render(<MyComponent />)
    expect(screen.getByText('Empty')).toBeDefined()
  })

  it('updates on user action', async () => {
    render(<MyComponent />)
    const btn = screen.getByLabelText('Action')
    fireEvent.click(btn)
    expect(screen.getByText('Updated')).toBeDefined()
  })
})
```

**Guarding Console Output in Tests**
When testing ErrorBoundary or any component that throws internally, React logs to `stderr`. Suppress it with a scoped spy — never at module scope (that leaks across test files).

```ts
// ✅ CORRECT: Scoped to describe block
describe('ErrorBoundary', () => {
  let consoleSpy: ReturnType<typeof vi.spyOn>

  beforeAll(() => {
    consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
  })

  afterAll(() => {
    consoleSpy.mockRestore()
  })

  it('renders fallback on error', () => {
    render(<ErrorBoundary><Throws /></ErrorBoundary>)
    expect(screen.getByText('Something went wrong')).toBeInTheDocument()
  })
})
```

**Testing Standards**
- Behavior-driven: Test user actions, not implementation
- Factory pattern: `getMockData(overrides)` for test data
- Time-dependent: Use `vi.useFakeTimers()` / `vi.useRealTimers()`
- No placeholders: No `expect(true).toBe(true)`

---

## 14. Component Design Patterns

**`cn()` Utility Implementation**
Create `src/lib/utils.ts`:
```ts
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

**shadcn/ui + Tailwind Override**
```tsx
import { Button } from '@components/ui/button'

<Button size="lg" className="bg-[var(--color-primary)] hover:bg-[var(--color-primary-hover)] text-white">
  Custom styled
</Button>
```

**Early Returns (Anti-Nesting)**
```tsx
// ✅ CORRECT
export function DataPanel() {
  if (count === 0) return <EmptyState />
  return <DataList />   
}

// ❌ WRONG (deep nesting)
export function DataPanel() {
  return (
    <div>
      {count === 0 ? (
        <div><p>...</p></div>
      ) : (
        <div>{items.map(...)}</div>
      )}
    </div>
  )
}
```

**`cn()` Helper for Conditional Classes**
```tsx
import { cn } from '@lib/utils'

className={cn(
  'fixed inset-y-0 right-0 transition-transform duration-300',
  isOpen ? 'translate-x-0' : 'translate-x-full'
)}
```

---

## 15. Build & QA Pipeline

**Commands**
```bash
npx tsc --noEmit       # TypeScript type check — ⬅️ ALWAYS RUN THIS FIRST
npm run build          # TypeScript check + Vite build (< 1s via Rolldown)
npx vitest run         # CI: run tests once
npm test               # Vitest watch mode
```

> ⚠️ **CRITICAL: Always run `npx tsc --noEmit` BEFORE `npx vitest run`.**
> TypeScript errors often cause cryptic test failures or misleading stack traces. A clean type check first prevents hours wasted debugging red herrings.

**Success Criteria**
| Metric | Target |
|---|---|
| `npm run build` | `< 1s` |
| `npx vitest run` | All tests pass |
| `npx tsc --noEmit` | Zero errors |

**CI/CD Stages**
1. `npm install --legacy-peer-deps`
2. `npx tsc --noEmit`
3. `npx vitest run`
4. `npm run build`

---

## 16. Common Gotchas Summary

| Gotcha | Fix |
|---|---|
| `manualChunks` object form | Must be a function in Vite 8 |
| `baseUrl` deprecated | Remove, use `"./"` in `paths` |
| `bottom--24` invalid | Use `-bottom-24` (single hyphen) |
| `inert` as string | Must be boolean |
| `getState()` in JSX | Use selector `useStore(s => s.x)` |
| TanStack `Link` in tests | Mock with `vi.mock('@tanstack/react-router')` |
| State updates in tests | Wrap in `act()` |
| Toast auto-remove | Use `vi.useFakeTimers()` / `vi.advanceTimersByTime()`. Example: `vi.advanceTimersByTime(3000); expect(toast).not.toBeInTheDocument()` |
| **Zod v4 `error.issues`** | Use `result.error.issues[0].message` (not `errors[]`) |
| **`useActionState` generics** | Must pass `<State, FormData>` when using 2-arg form |
| **Font-family inline in className** | Use `@layer utilities` (`.font-display`) — never `font-["..."]` |
| **`routeTree.gen.ts` missing** | Run `npx tsr generate` after every route change |
| **`bg-gradient-to-*` in v4** | Use `bg-linear-to-*` |
| **`outline-none` in v4** | Use `outline-hidden` |
| **`flex-shrink-0` in v4** | Use `shrink-0` |
| **Raw hex in `className`** | Replace with `@theme` utility (e.g. `text-wool-900`) |
| **`max-w-[1280px] px-6` inlined everywhere** | Register `.container-custom` in `@layer utilities` |
| **Orphaned `@theme` color** | Defined in `globals.css` but never consumed in UI |

---

## 17. Project File Structure (Reference)

```
src/
├── main.tsx              # Entry + ErrorBoundary wrapper
├── globals.css           # Tailwind v4 @theme inline
├── components/
│   ├── ui/               # shadcn primitives (Button, Card, Input, Badge)
│   ├── layout/           # Navbar, Footer
│   ├── sections/         # Hero, TrustBar, FeatureGrid, Newsletter
│   ├── shared/           # ModalOverlay, SlidePanel, SkipLink, ErrorBoundary
│   └── index.ts          # Barrel exports
├── hooks/                # Custom hooks (useThrottledScroll, useFocusTrap)
│   └── index.ts          # Barrel exports
├── services/             # Typed service layer contracts
│   └── products.ts       # ProductService interface + impl
├── stores/               # Zustand (.ts), persist middleware
├── routes/               # TanStack file-based routing
│   ├── __root.tsx        # Root layout + overlays
│   ├── index.tsx         # Home
│   ├── about.tsx
│   ├── features.index.tsx
│   └── $.tsx             # Catch-all 404
├── types/                # Recommended — delete when empty (auto-audit will flag)
├── lib/                  # Utilities (cn helper, formatters, schemas)
│   ├── utils.ts
│   ├── format.ts
│   ├── schemas.ts        # Zod validation schemas
│   └── index.ts          # Barrel exports
├── vitest.config.ts      # (Optional if using unified vite.config.ts)
└── test/                 # Vitest (jsdom, setup.ts, *.test.ts)
```

---

## 18. Anti-Pattern Reference Card

| # | Anti-Pattern | Fix |
|---|---|---|
| 1 | `getState()` in JSX | Selector subscription |
| 2 | Stubbed test `expect(true).toBe(true)` | Implement real assertions |
| 3 | Non-functional input | `useActionState` + `disabled` |
| 4 | Undefined CSS class | Define in `@theme inline` |
| 5 | Deprecated `baseUrl` | Remove, use relative `paths` |
| 6 | Double-hyphen negatives | Single hyphen prefix |
| 7 | `inert` as string | Boolean expression |
| 8 | Persisting `isOpen` / UI state | `partialize` to data only |
| 9 | `return null` on overlay close | Keep in DOM, toggle `opacity` |
| 10 | Building custom components instead of using shadcn | Use shadcn primitives |
| 11 | `interface Props` / `interface State` | Prefix with component name: `ErrorBoundaryProps` |
| 12 | Raw data + functions without contract | Define typed `ProductService` interface |
| 13 | Manual form validation in action | Use Zod `safeParse()` + `Object.fromEntries(formData)` |
| 14 | `font-["..."]` in className | Use CSS `@layer utilities` (`.font-display`) |
| 15 | Deep relative path imports | Add barrel `index.ts` at directory root |
| 16 | **Tailwind v3 utilities in v4** (`bg-gradient-to-*`, `outline-none`, `flex-shrink-0`) | Use `bg-linear-to-*`, `outline-hidden`, `shrink-0` |
| 17 | **Raw hex in `className`** (`text-[#3D3835]`) | Use `@theme` token utilities (`text-wool-900`) |
| 18 | **Orphaned `@theme` tokens** | Verify every `--color-*` has at least one UI consumer |
| 19 | **Repeated container pattern** (`container mx-auto max-w-[1280px] px-6` ×14 files) | Register `.container-custom` in `@layer utilities` and consume in all layout sections |

---

## 19. Custom Hooks (Advanced)

**`useThrottledScroll` — Performance-First Scroll**
Throttle `window.addEventListener('scroll')` to prevent 60fps re-renders. Uses the latest-ref pattern to avoid effect teardown on every render.

```ts
import { useEffect, useRef } from 'react'

export function useThrottledScroll(callback: (scrollY: number) => void, delay = 100) {
  const callbackRef = useRef(callback)
  callbackRef.current = callback

  const rafId = useRef<number | null>(null)
  const timeoutId = useRef<ReturnType<typeof setTimeout> | null>(null)
  const lastScrollY = useRef<number>(0)

  useEffect(() => {
    const handleScroll = () => {
      lastScrollY.current = window.scrollY
      if (rafId.current !== null) return

      rafId.current = requestAnimationFrame(() => {
        rafId.current = null
        if (timeoutId.current) return
        timeoutId.current = setTimeout(() => {
          timeoutId.current = null
          callbackRef.current(lastScrollY.current)
        }, delay)
      })
    }

    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => {
      window.removeEventListener('scroll', handleScroll)
      if (rafId.current) cancelAnimationFrame(rafId.current)
      if (timeoutId.current) clearTimeout(timeoutId.current)
    }
  }, [delay]) // Stable dependency array prevents re-subscription
}
```
**Critical:** Do NOT use raw `window.addEventListener('scroll')` with `useState` — it triggers re-renders at 60fps.

**`useFocusTrap` — Keyboard Accessibility**
Trap `Tab` key within modals, mobile menus, drawers. No new dependencies needed.

```ts
import { useEffect } from 'react'

export function useFocusTrap(
  isActive: boolean,
  containerRef: React.RefObject<HTMLElement | null>,
  triggerRef?: React.RefObject<HTMLElement | null>
) {
  useEffect(() => {
    if (!isActive || !containerRef.current) return

    const savedTrigger = triggerRef?.current ?? (document.activeElement as HTMLElement)
    const container = containerRef.current

    const getFocusable = (): HTMLElement[] => {
      const candidates = container.querySelectorAll<HTMLElement>(
        'a[href], button, input, textarea, select, [tabindex]:not([tabindex="-1"])'
      )
      return Array.from(candidates).filter(
        (el) => !el.hasAttribute('disabled') && el.offsetParent !== null
      )
    }

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key !== 'Tab' || !container) return
      const focusable = getFocusable()
      if (focusable.length === 0) { e.preventDefault(); return }
      const first = focusable[0], last = focusable[focusable.length - 1]
      const active = document.activeElement as HTMLElement
      if (e.shiftKey) {
        if (active === first || !focusable.includes(active)) {
          e.preventDefault(); last.focus()
        }
      } else {
        if (active === last || !focusable.includes(active)) {
          e.preventDefault(); first.focus()
        }
      }
    }

    const first = getFocusable()[0]
    if (first) first.focus()
    document.addEventListener('keydown', handleKeyDown)
    return () => {
      document.removeEventListener('keydown', handleKeyDown)
      savedTrigger?.focus()
    }
  }, [isActive, containerRef, triggerRef])
}
```
**Why manual and not `react-focus-lock`:** This keeps your bundle lean. For complex cases (iframes, portals), use `react-focus-lock`.

---

## 20. Testing Gotchas (Advanced)

**`requestAnimationFrame` in jsdom**
jsdom does not implement `requestAnimationFrame`. Mock it:
```ts
beforeEach(() => {
  vi.useFakeTimers({ shouldAdvanceTime: true })
  vi.stubGlobal('requestAnimationFrame', (cb: FrameRequestCallback) => {
    return window.setTimeout(cb, 16) as unknown as number
  })
  vi.stubGlobal('cancelAnimationFrame', (id: number) => {
    window.clearTimeout(id)
  })
})

afterEach(() => {
  vi.unstubAllGlobals()
  vi.useRealTimers()
})
```

**Throttled Scroll in Tests**
```ts
it('fires callback after rAF + throttle delay', () => {
  const callback = vi.fn()
  renderHook(() => useThrottledScroll(callback, 100))

  window.dispatchEvent(new Event('scroll'))
  expect(callback).not.toHaveBeenCalled()

  vi.advanceTimersByTime(120) // 16ms rAF + 100ms throttle + buffer
  expect(callback).toHaveBeenCalledTimes(1)
})
```

**ErrorBoundary Test — Console Error Spy**
```ts
describe('ErrorBoundary', () => {
  let consoleSpy: ReturnType<typeof vi.spyOn>

  beforeAll(() => {
    consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
  })

  afterAll(() => {
    consoleSpy.mockRestore()
  })

  it('renders fallback on error', () => {
    render(<ErrorBoundary><Boom /></ErrorBoundary>)
    expect(screen.getByText('Something went wrong')).toBeInTheDocument()
  })
})
```
**CRITICAL:** Define `consoleSpy` inside `beforeAll`/`afterAll`, **NOT** at module scope. Module-scope spies leak across test files.

---

## 21. Accessibility (WCAG 2.1 AA)

**Skip-to-Content Link (WCAG 2.4.1)**
Every production app must have a skip link:
```tsx
// src/components/shared/SkipLink.tsx
export function SkipLink() {
  return (
    <a
      href="#main-content"
      className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-[200] focus:bg-[var(--color-surface)] focus:text-[var(--color-text-primary)] focus:px-4 focus:py-2 focus:rounded-md focus:shadow-lg"
    >
      Skip to main content
    </a>
  )
}

// In __root.tsx: <SkipLink /> before <Navbar />
// In __root.tsx: <main id="main-content"> wrapping <Outlet />
```

**Roving Tabindex for Tabs**
```tsx
import { useId } from 'react'

// 💡 React 19 Tip: Use `useId()` to generate stable aria-controls/id pairs without hydration mismatches.
const tabGroupId = useId()

<button
  role="tab"
  tabIndex={activeTab === tab.id ? 0 : -1}
  aria-selected={activeTab === tab.id}
  aria-controls={`${tabGroupId}-panel-${tab.id}`}
  id={`${tabGroupId}-tab-${tab.id}`}
  onKeyDown={(e) => {
    if (e.key === 'ArrowRight') { /* focus next */ }
    if (e.key === 'ArrowLeft') { /* focus prev */ }
    if (e.key === 'Home') { /* focus first */ }
    if (e.key === 'End') { /* focus last */ }
  }}
>
  {tab.label}
</button>

<div role="tabpanel" id={`${tabGroupId}-panel-${tab.id}`} aria-labelledby={`${tabGroupId}-tab-${tab.id}`} tabIndex={0}>
  {/* tab content */}
</div>
```

**Verification:** Run `axe-core` or Lighthouse accessibility audit pre-ship. Ensure all interactive elements have visible `:focus-visible` states. *(Note: `prefers-reduced-motion` handling in §3 aligns with WCAG 2.3.3)*

---

## 22. Security & SEO Essentials

**Content Security Policy (CSP)**
Add to `index.html` `<head>`:
```html
<!-- Production: Keep as single line. Inject via build tool for dynamic nonces. -->
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' https:; connect-src 'self';">
```
> **⚠️ Production Requirement:** Replace `'unsafe-inline'` with CSP nonces or hashes before shipping. `'unsafe-inline'` is only acceptable for dev/font loading. `https:` in `img-src` allows any secure origin; tighten to specific CDN domains in production. Adjust `script-src`/`connect-src` per analytics/payment SDKs.

**Open Graph / Twitter Card**
```html
<meta property="og:title" content="..." />
<meta property="og:description" content="..." />
<meta property="og:type" content="website" />
<meta property="og:image" content="/og-image.jpg" />
<meta name="twitter:card" content="summary_large_image" />
```

**External Links**
```html
<!-- Always add rel="noopener noreferrer" to external links -->
<a href="..." rel="noopener noreferrer" target="_blank">External</a>
```

---

## 23. Dead Code Prevention

**CSS Token Audit (Tailwind v4)**
```bash
# Find unused @theme tokens
grep -r "ivory-500" src/ || echo "Token is unused — safe to remove"

# Find unused @keyframes
grep -r "slide-in-left" src/ || echo "Animation unused — remove from globals.css"
```

**TypeScript `noUnusedLocals` + Dead Imports**
Already enforced by `tsconfig.json`. But check path aliases when deleting files:

**Path Alias Cleanup Checklist**
When deleting a file (e.g., `src/types/index.ts`):
1. Delete the file: `rm src/types/index.ts`
2. Remove from `tsconfig.json` paths
3. Remove from `vite.config.ts` `resolve.alias`
4. If you use a **separate** `vitest.config.ts` (not the unified approach in §5), remove from its `resolve.alias` too
5. Run `npx tsc --noEmit` to confirm

> 💡 **Unified vs Separate:** With the unified `vite.config.ts` approach (§5), steps 2 and 3 are the only ones needed. The unified config handles both Vite and Vitest aliases.

---

## 24. Removable Dead Code Checklist (Auto-Audit)

Run this after any major refactoring.

> **⚠️ Cross-Platform Note:** This script requires Bash (macOS/Linux/WSL/Git Bash). For Windows native, use the Node.js `fs`/`glob` alternative or run via WSL.
> **⚠️ Heuristic Warning:** The orphaned file detection uses `grep` and may falsely flag `*.test.ts` or barrel files. Always verify before deleting.

```bash
#!/usr/bin/env bash
echo "=== Dead Code Audit ==="

# Unused path aliases (matches double-quoted JSON keys)
echo "Checking path aliases..."
grep -o '"@[a-z-]*"' tsconfig.json | tr -d '"' | sort -u
grep -r "from '@types/" src/ || echo "⚠️ @types alias unused — remove from tsconfig, vite, vitest"

# Unused CSS tokens in globals.css
echo "Checking for unused CSS tokens..."
grep -o "var(--[a-z-]*[0-9]*)" src/globals.css | while read -r token; do
  var=$(echo "$token" | sed 's/var(//;s/)//;s/--//')
  if ! grep -r "$var" src/components/ src/routes/ src/main.tsx >/dev/null; then
    echo "  ⚠️ Unused: $token"
  fi
done

# Unused @keyframes
echo "Checking for unused @keyframes..."
grep "@keyframes" src/globals.css | while read -r line; do
  name=$(echo "$line" | sed 's/@keyframes //')
  if ! grep -r "$name" src/components/ src/routes/ src/main.tsx >/dev/null; then
    echo "  ⚠️ Unused @keyframes: $name"
  fi
done

# Files with no imports
echo "Checking for orphaned files..."
find src \( -name "*.ts" -o -name "*.tsx" \) | while read -r file; do
  basename=$(basename "$file" | sed 's/\..*//')
  # Skip index files to avoid false positives from barrel imports
  if [ "$basename" = "index" ]; then continue; fi
  if ! grep -r "from.*$basename" src/ >/dev/null 2>&1; then
    echo "  ⚠️ Orphaned: $file"
  fi
done

echo "=== Audit Complete ==="
```

---

## 25. Pre-Ship Hardening Checklist

Derived from real-world remediation cycles. Verify all items before production deployment.

### 🚀 Performance
- [ ] Scroll listeners use `useThrottledScroll` (rAF + throttle)
- [ ] No raw `useState` tied to `window.scroll` or `resize`
- [ ] `manualChunks` uses function form in `vite.config.ts`
- [ ] Build time `< 1s`, bundle size audited

### ♿ Accessibility (WCAG 2.1 AA)
- [ ] `<SkipLink />` present and functional
- [ ] All modals/drawers use `useFocusTrap`
- [ ] Tabs implement roving `tabIndex` + arrow key navigation
- [ ] Decorative SVGs have `aria-hidden="true"` or `role="presentation"`
- [ ] `:focus-visible` outlines match design tokens
- [ ] Lighthouse/axe-core score ≥ 95

### 🔒 Security & SEO
- [ ] CSP meta tag configured in `index.html`
- [ ] OG/Twitter meta tags populated
- [ ] All `target="_blank"` links include `rel="noopener noreferrer"`
- [ ] No hardcoded secrets or API keys in client bundle

### 🧪 Testing
- [ ] `requestAnimationFrame` mocked in jsdom setup
- [ ] `consoleSpy` scoped to `beforeAll`/`afterAll` (no module leaks)
- [ ] Timer advancement matches `rAF + throttle + buffer` matrix
- [ ] All store mutations wrapped in `act()` during tests
- [ ] 100% test pass rate, zero skipped tests

### 🧹 Validation & Code Quality
- [ ] All form inputs validated with Zod at system boundaries
- [ ] Typed service interfaces (`ProductService`) for all data access
- [ ] Barrel `index.ts` files exist at `components/`, `lib/`, `hooks/` roots
- [ ] No generic `Props` / `State` — component-name-prefixed interfaces only
- [ ] No inline font-family in className strings (use `@layer utilities`)
- [ ] **No raw hex in `className`** (enforced by `validate-colors.sh`)
- [ ] Dead CSS tokens & `@keyframes` purged
- [ ] Orphaned files & unused path aliases removed
- [ ] `tsconfig.json`, `vite.config.ts`, `vitest.config.ts` aliases synced
- [ ] No `any`, `enum`, or `namespace` in codebase
- [ ] Version bumped, changelog updated

---

## 27. CI Validation Scripts

Add to `package.json` scripts:
```json
{
  "scripts": {
    "validate:colors": "bash scripts/validate-colors.sh",
    "validate:tw": "bash scripts/validate-deprecated-twind.sh",
    "validate:all": "npm run validate:colors && npm run validate:tw"
  }
}
```

### `scripts/validate-colors.sh`
```bash
#!/bin/bash
if grep -rEn 'text-\[#[0-9A-Fa-f]{3,6}\]|bg-\[#[0-9A-Fa-f]{3,6}\]|border-\[#[0-9A-Fa-f]{3,6}\]' src/; then
  echo "❌ Raw hex colors found in className. Use @theme tokens instead."
  exit 1
fi
echo "✅ No raw hex colors in className."
```

### `scripts/validate-deprecated-twind.sh`
```bash
#!/bin/bash
if grep -rEn 'bg-gradient-to-(r|l|t|b)|outline-none[^-]|flex-shrink-0' src/; then
  echo "❌ Deprecated Tailwind v3 utilities found. Update to v4 names."
  exit 1
fi
echo "✅ No deprecated Tailwind v3 utilities."
```

---

## 26. Remediation Round Reference (Real-World)

Derived from actual production remediation cycles. Every item below was a real bug or gap that slipped through code review.

| # | Issue | Fix | Prevention |
|---|---|---|---|
| 1 | `src/types/index.ts` empty with comment | Delete + remove path alias | Auto-audit script (§24) |
| 2 | `--color-ivory-500` defined but unused | Remove from `globals.css` | CSS token grep (§23) |
| 3 | `@keyframes slide-in-left` unused | Remove from `globals.css` | CSS keyframe grep (§23) |
| 4 | Custom hook duplicated by component's built-in logic | Delete (component handles logic internally) | Orphan/duplicate file detection |
| 5 | Toast `timeoutId` not cleared on rapid calls | Module-level `timeoutId` + `clearTimeout` | State management audit |
| 6 | `consoleSpy` at module scope in tests | Move to `beforeAll`/`afterAll` (§13) | Testing best practice |
| 7 | Scroll events unthrottled causing jank | `useThrottledScroll` hook (§19) | Performance audit |
| 8 | No focus trap in mobile menu | `useFocusTrap` hook (§19) | Accessibility audit |
| 9 | No skip-to-content link | Add `SkipLink` component (§21) | WCAG 2.4.1 checklist |
| 10 | No 404 / not-found route | Add `$.tsx` catch-all (§6) | Route coverage audit |
| 11 | No CSP in `index.html` | Add `<meta http-equiv="Content-Security-Policy">` (§22) | Security checklist |
| 12 | No OG/Twitter meta | Add Open Graph + Twitter Card (§22) | SEO checklist |
| 13 | Decorative SVGs not screen-reader friendly | Add `aria-hidden="true"` / `role="presentation"` | Accessibility audit |
| 14 | `requestAnimationFrame` fails in jsdom tests | `vi.stubGlobal('requestAnimationFrame', ...)` (§20) | jsdom awareness |
| 15 | Throttled scroll tests hang | `vi.useFakeTimers({ shouldAdvanceTime: true })` (§20) | Testing best practice |
| 16 | Generic `interface Props` / `interface State` | Rename to `ErrorBoundaryProps`, `ErrorBoundaryState` (§18) | Component naming |
| 17 | Zod v3 `error.errors[]` used on v4 | Use `error.issues[0].message` (§9) | Schema library API |
| 18 | Missing `useActionState<State, FormData>` generic | Pass both type params (§8) | React 19 types |
| 19 | `font-["...",serif]` in className breaks parser | Use `@layer utilities` (§11) | Tailwind + JSX |
| 20 | Raw data functions without typed contract | Define `ProductService` interface (§10) | Architecture |
| 21 | Deep relative imports across modules | Add barrel `index.ts` exports (§11) | Module boundaries |
| 22 | Manual `FormData` field checking in action | Use Zod `safeParse(Object.fromEntries(formData))` (§9) | Validation |
| 23 | Tailwind v3 → v4 utility rename silent fail | Audit: `bg-gradient-to-*` → `bg-linear-to-*`, `outline-none` → `outline-hidden`, `flex-shrink-0` → `shrink-0` | Tailwind v4 |
| 24 | `@theme` tokens defined but never consumed | Ensure every `--color-*` has a UI consumer; use `scripts/validate-colors.sh` | Design system |
| 25 | Container layout (`max-w-[1280px] px-6`) inlined in 14 components | Register `.container-custom` in `@layer utilities`; consume it everywhere | Layout DRY |
| 26 | Add-to-cart without `useOptimistic` | Use `useOptimistic` + `startTransition` for optimistic mutations (§8) | React 19 |
| 27 | Raw hex in `className` (e.g. `text-[#3D3835]`) | Replace with `@theme` utility (e.g. `text-wool-900`); use `scripts/validate-colors.sh` | Tailwind v4 |

**Test evolution from a real project:** 15 tests (4 files) → 49 tests (10 files) — **+240% coverage** after addressing the issues above.

---

### 🛡️ ErrorBoundary Reference Implementation
```tsx
import React from 'react'

interface ErrorBoundaryProps {
  children: React.ReactNode
  fallback?: React.ReactNode
}

interface ErrorBoundaryState {
  hasError: boolean
}

export class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(): ErrorBoundaryState {
    return { hasError: true }
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error('ErrorBoundary caught:', error, info)
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? <div className="p-8 text-center">Something went wrong.</div>
    }
    return this.props.children
  }
}
```

---

Built from production-grade React 19 / TypeScript 6 / Vite 8 / Tailwind v4 MVPs. Shipped with zero TypeScript errors, behavioral test coverage, and WCAG 2.1 AA verification.
