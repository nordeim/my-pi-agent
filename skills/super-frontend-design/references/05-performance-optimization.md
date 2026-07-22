# Performance Optimization (Core Module 5)

> **Source Skills:** nextjs-react-expert, nextjs16-tailwind4, web-frameworks  
> **Purpose:** Achieve production-grade performance with 57 validated Vercel rules

---

## 1. Priority Order (Critical → Low)

```
1️⃣ CRITICAL (Biggest Gains - Do First):
   ├─ Eliminate Waterfalls (each adds 100-500ms+ latency)
   └─ Bundle Size Optimization (affects TTI, LCP)

2️⃣ HIGH (Significant Impact - Do Second):
   └─ Server-Side Performance (faster SSR, streaming)

3️⃣ MEDIUM (Moderate Gains - Do Third):
   ├─ Client-Side Data Fetching (SWR, deduplication)
   ├─ Re-render Optimization (React.memo, useMemo)
   └─ Rendering Performance (virtualization, images)

4️⃣ LOW (Polish - Do Last):
   ├─ JavaScript Micro-optimizations
   └─ Advanced Patterns (useLatest, init-once)
```

---

## 2. CRITICAL: Eliminate Waterfalls (12 Rules)

### 2.1 What is a Waterfall?
Sequential `await` calls that add full network latency per step. Example:
```typescript
// ❌ WATERFALL (3 sequential waits)
const user = await getUser();
const posts = await getPosts(user.id);
const comments = await getComments(posts[0].id);

// ✅ PARALLEL (1 wait total)
const [user, posts, comments] = await Promise.all([
  getUser(),
  getPosts(user.id),
  getComments(posts[0].id), // Note: Still depends, restructure if possible
]);
```

### 2.2 Key Rules
1. **Parallel Data Fetching**: Always use `Promise.all()` for independent calls
2. **Server Components First**: No client-side waterfalls for initial data
3. **Suspense Boundaries**: Wrap data-fetching components to avoid blocking
4. **Preload Critical Data**: Use `<link rel="preload">` for key assets
5. **Avoid Sequential Await**: Never chain awaits for independent operations

### 2.3 Verification
```bash
# Check for sequential awaits in codebase
grep -r "await" src/ --include="*.ts" | grep -A 2 "await"
```

---

## 3. CRITICAL: Bundle Size Optimization (10 Rules)

### 3.1 Budget Targets
| Metric | Institutional | Dynamic | Balanced |
|--------|---------------|---------|----------|
| Initial JS bundle | < 150 KB | < 300 KB | < 200 KB |
| First Contentful Paint | < 1.0s | < 1.5s | < 1.2s |
| Largest Contentful Paint | < 1.5s | < 2.5s | < 2.0s |
| Time to Interactive | < 2.0s | < 3.5s | < 2.5s |

### 3.2 Key Rules
1. **No Barrel Imports**: Avoid `index.ts` re-exports in app code
   ```typescript
   // ❌ BARREL IMPORT
   import { Button, Card } from "@/components/ui";
   // ✅ DIRECT IMPORT
   import { Button } from "@/components/ui/Button";
   import { Card } from "@/components/ui/Card";
   ```
2. **Dynamic Imports**: Lazy load heavy components
   ```tsx
   const HeavyChart = dynamic(() => import("./HeavyChart"), {
     loading: () => <Skeleton />,
     ssr: false,
   });
   ```
3. **Tree-Shaking**: Import single functions, not entire libraries
   ```typescript
   // ❌ WHOLE LIBRARY
   import _ from "lodash";
   // ✅ SINGLE FUNCTION
   import debounce from "lodash/debounce";
   ```
4. **Next.js Image**: Always use `next/image` for optimization
5. **Next.js Font**: Use `next/font/google` for zero-network font loading

### 3.3 Bundle Analysis
```bash
# Install analyzer
npm install @next/bundle-analyzer

# Add to next.config.ts
const withBundleAnalyzer = require("@next/bundle-analyzer")({
  enabled: process.env.ANALYZE === "true",
});
module.exports = withBundleAnalyzer(nextConfig);

# Run analysis
ANALYZE=true npm run build
```

---

## 4. HIGH: Server-Side Performance (10 Rules)

### 4.1 Key Rules
1. **Parallel Server Fetching**: Use `Promise.all()` in Server Components
2. **Streaming SSR**: Use Suspense for slow server operations
3. **API Route Optimization**: No N+1 queries, use ORMs properly
4. **Server Actions**: Use for form mutations (Next.js 16+)
5. **PPR (Partial Prerendering)**: Hybrid static + dynamic pages

### 4.2 PPR Example
```typescript
// next.config.ts
const nextConfig = {
  experimental: { ppr: "incremental" },
};

// App Router page with PPR
export const experimental_ppr = true;
export default async function Page() {
  const staticContent = await getStaticData();
  return (
    <div>
      {staticContent}
      <Suspense fallback={<Skeleton />}>
        <DynamicComponent />
      </Suspense>
    </div>
  );
}
```

---

## 5. MEDIUM: Re-render & Rendering Optimization (15 Rules)

### 5.1 Re-render Rules
1. **React.memo**: Wrap expensive components
2. **useMemo**: Cache expensive computations
3. **useCallback**: Cache event handlers passed to children
4. **React Compiler**: React 19 auto-memoizes (trust it first)
5. **Virtualization**: Use for lists >100 items (`react-window`)

### 5.2 Rendering Rules
1. **Compositor-Only Animations**: Animate only `transform` and `opacity`
2. **Avoid Layout Thrashing**: Batch DOM reads/writes
3. **next/image**: Always provide `width`/`height` to avoid CLS
4. **Skeleton Loaders**: Use instead of spinners for better UX

---

## 6. LOW: JavaScript Micro-optimizations (10 Rules)

### 6.1 Rules
1. **Hoist RegExps**: Move regex to module scope
2. **Cache Property Access**: In hot loops, cache `obj.prop`
3. **Avoid `for...in`**: Use `for...of` or `forEach`
4. **Use `Map`/`Set`**: For frequent lookups vs arrays
5. **Debounce Inputs**: 300-500ms delay for search

---

## 7. Performance Budgets by Quadrant (avant-garde-design-v4)

| Metric | Q1/Q3 (Institutional) | Q2/Q4 (Dynamic) |
|--------|------------------------|------------------|
| Initial JS bundle | < 150 KB | < 300 KB |
| First Contentful Paint | < 1.0s | < 1.5s |
| Cumulative Layout Shift | < 0.05 | < 0.1 |
| Animation Frame Budget | N/A | < 16ms (60fps) |

---

## 8. Performance Review Checklist

**Critical (Must Fix):**
- [ ] No sequential data fetching (waterfalls eliminated)
- [ ] Bundle size < 200KB for main bundle
- [ ] No barrel imports in app code
- [ ] Dynamic imports for large components
- [ ] Parallel data fetching where possible

**High Priority:**
- [ ] Server components used where appropriate
- [ ] API routes optimized (no N+1 queries)
- [ ] Suspense boundaries for data fetching
- [ ] Static generation used where possible

**Medium Priority:**
- [ ] Expensive computations memoized
- [ ] List rendering virtualized (if > 100 items)
- [ ] Images optimized with next/image
- [ ] No unnecessary re-renders

**Low Priority (Polish):**
- [ ] Hot path loops optimized
- [ ] RegExp patterns hoisted
- [ ] Property access cached in loops

---

## 9. Verification Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `react_performance_checker.py` | Automated 57-rule audit | `python scripts/react_performance_checker.py <project_path>` |

---

## 10. Related References
- [02-tech-stack-setup.md](02-tech-stack-setup.md) → Next.js, Tailwind setup
- [04-component-architecture.md](04-component-architecture.md) → Component patterns
- [08-quality-assurance.md](08-quality-assurance.md) → Anti-patterns, verification gates
