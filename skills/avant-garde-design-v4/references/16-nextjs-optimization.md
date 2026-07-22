# Next.js 16.2+ Optimization Reference

## 1.0 Key Enhancements in Next.js 16.2

Next.js 16.2 represents a major leap in developer experience and production performance.

- **🚀 400% Faster Dev Startup:** Using the latest Turbopack (Rust-powered) engine.
- **⚡ 50% Faster Server Component Rendering:** Optimized RSC (React Server Components) reconciliation.
- **🛠 Improved Hydration Diffing:** Clearer indicators of where hydration fails.
- **📦 Native Tailwind v4 Support:** Deep integration via the `@tailwindcss/vite` equivalent plugin.

---

## 2.0 Server Components by Default

Always use Server Components (RSC) unless interactivity is explicitly required.

**RSC Best Practices:**
- Fetch data directly in the component using `await`.
- Keep the component stateless to reduce client bundle size.
- Pass data as props to Client Components.

```tsx
// src/app/courses/page.tsx (Server Component)
export default async function CoursesPage() {
  const courses = await fetchCourses(); // Direct DB fetch
  
  return (
    <main>
      <CourseHeader />
      <CourseList courses={courses} /> {/* Pass to Client if needed */}
    </main>
  );
}
```

---

## 3.0 Image Optimization Strategy

Next.js `Image` component is your primary tool for LCP and CLS.

**Rule of Thumb:**
- **Hero:** Use `priority` and explicit `width`/`height`.
- **Lists:** Use `sizes` to tell the browser which resolution to load.

```tsx
<Image
  src="/hero.avif"
  alt="Avant-Garde Design Header"
  width={1200}
  height={675}
  priority
  className="aspect-video object-cover"
/>
```

---

## 4.0 Font Optimization (`next/font`)

Never use external Google Font `<link>` tags. Use `next/font` for Zero Layout Shift.

```tsx
// src/app/layout.tsx
import { Inter, Space_Grotesk } from 'next/font/google';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });
const spaceGrotesk = Space_Grotesk({ subsets: ['latin'], variable: '--font-display' });

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${inter.variable} ${spaceGrotesk.variable}`}>
      <body>{children}</body>
    </html>
  );
}
```

---

## 5.0 Modern App Router Architecture

Organize your project by domain, not by file type.

```
src/
├── app/                  # Routes, Layouts, Loading states
│   ├── (auth)/           # Route Group for Authentication
│   ├── (main)/           # Primary application routes
│   └── api/              # API Route Handlers
├── components/           # UI Components
│   ├── layout/           # Shared layout components (Navbar, Footer)
│   ├── sections/         # Feature-specific section blocks
│   └── ui/               # shadcn/ui primitives
├── lib/                  # Shared utilities (cn, formatters)
├── hooks/                # Custom React hooks
└── types/                # Shared TypeScript types
```

---

## 6.0 Build Tool Configuration

Ensure `next.config.ts` is optimized for 2026 performance.

```ts
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  experimental: {
    turbo: {
      rules: {
        // Custom Turbopack rules if needed
      }
    }
  },
  images: {
    formats: ['image/avif', 'image/webp'],
    remotePatterns: [
      { protocol: 'https', hostname: 'cdn.brand.com' }
    ]
  },
  typescript: {
    ignoreBuildErrors: false // Enforce strict types
  }
};

export default nextConfig;
```

---

**See Also:**
- `[15-performance-budgets.md](15-performance-budgets.md)` - Metric targets
- `[11-tech-commitments.md](11-tech-commitments.md)` - Tech stack standards
