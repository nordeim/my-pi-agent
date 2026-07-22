# Component Architecture (Core Module 4)

> **Source Skills:** ui-styling, frontend-development, web-frameworks  
> **Purpose:** Build accessible, reusable, maintainable UI components

---

## 1. UI Layer: shadcn/ui + Radix UI (ui-styling)

### 1.1 Core Principles
- **Accessible primitives**: Built on Radix UI headless components
- **Copy-paste distribution**: Components live in your codebase (full control)
- **TypeScript-first**: Full type safety
- **Composable**: Build complex UIs from simple primitives

### 1.2 Installation & Usage
```bash
# Initialize shadcn/ui (Tailwind v4 compatible)
npx shadcn@latest init

# Add components
npx shadcn@latest add button card dialog form input
```

### 1.3 Example: Button Component (shadcn-style)
```tsx
// src/components/ui/Button.tsx
import { forwardRef, type ButtonHTMLAttributes } from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-lg font-medium transition-colors focus-visible:outline-hidden focus-visible:ring-2 focus-visible:ring-champagne disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-champagne text-void hover:bg-champagne-dark",
        outline: "border border-slate-700 bg-transparent hover:bg-slate-800",
        ghost: "hover:bg-slate-800",
        luxury: "glass-panel text-white hover:bg-void-light shadow-xs",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-8 px-3 text-sm",
        lg: "h-12 px-6 text-lg",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
);

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  loading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, loading, children, ...props }, ref) => (
    <button
      ref={ref}
      className={cn(buttonVariants({ variant, size }), className)}
      disabled={props.disabled || loading}
      {...props}
    >
      {loading && (
        <span className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
      )}
      {children}
    </button>
  )
);

Button.displayName = "Button";
```

### 1.4 Accessible Components Checklist
- [ ] Dialog/Modal: Focus trap, Escape to close, scroll lock
- [ ] Dropdown: Keyboard navigation (Arrow keys), ARIA roles
- [ ] Form inputs: Associated `<label>` or `aria-label`
- [ ] Icon buttons: `aria-label` for screen readers
- [ ] Navigation: Semantic `<nav>`, focus management

---

## 2. Next.js App Router Patterns (web-frameworks)

### 2.1 Server vs Client Components
| Type | When to Use | Directive |
|------|-------------|-----------|
| **Server Component** | Static content, data fetching, no interactivity | Default (no directive) |
| **Client Component** | Hooks, event handlers, browser APIs | `"use client"` at top |

### 2.2 Data Fetching (Server Components)
```tsx
// app/posts/[slug]/page.tsx
import { notFound } from 'next/navigation';

// Static generation at build time
export async function generateStaticParams() {
  const posts = await getPosts();
  return posts.map(post => ({ slug: post.slug }));
}

// Revalidate every hour
async function getPost(slug: string) {
  const res = await fetch(`https://api.example.com/posts/${slug}`, {
    next: { revalidate: 3600 }
  });
  if (!res.ok) return null;
  return res.json();
}

export default async function Post({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug);
  if (!post) notFound();
  return <article>{post.content}</article>;
}
```

### 2.3 Dynamic Imports (Client Components)
```tsx
import dynamic from "next/dynamic";
const HeavyChart = dynamic(() => import("./HeavyChart"), {
  loading: () => <Skeleton />,
  ssr: false,
});
```

---

## 3. Feature-Based Organization (frontend-development)

### 3.1 Directory Structure
```
src/features/my-feature/
├── api/          # API service layer (axios/fetch)
│   └── myFeatureApi.ts
├── components/   # Feature-specific components
│   ├── MyFeature.tsx
│   └── SubComponent.tsx
├── hooks/        # Custom hooks
│   ├── useMyFeature.ts
│   └── useSuspenseMyFeature.ts
├── helpers/      # Utility functions
│   └── myFeatureHelpers.ts
├── types/        # TypeScript types
│   └── index.ts
└── index.ts      # Public exports
```

### 3.2 API Service Layer Example
```typescript
// src/features/auth/api/authApi.ts
import { apiClient } from "@/lib/apiClient";

export const authApi = {
  login: (email: string, password: string) =>
    apiClient.post("/auth/login", { email, password }),
  logout: () => apiClient.post("/auth/logout"),
  getProfile: () => apiClient.get("/auth/profile"),
};
```

### 3.3 Component Pattern (React.FC + TypeScript)
```tsx
import React, { useState, useCallback } from "react";
import { Box, Paper } from "@mui/material";
import { useSuspenseQuery } from "@tanstack/react-query";
import { featureApi } from "../api/featureApi";
import type { FeatureData } from "~types/feature";

interface MyComponentProps {
  id: number;
  onAction?: () => void;
}

export const MyComponent: React.FC<MyComponentProps> = ({ id, onAction }) => {
  const [state, setState] = useState<string>("");
  const { data } = useSuspenseQuery({
    queryKey: ["feature", id],
    queryFn: () => featureApi.getFeature(id),
  });

  const handleAction = useCallback(() => {
    setState("updated");
    onAction?.();
  }, [onAction]);

  return (
    <Box sx={{ p: 2 }}>
      <Paper sx={{ p: 3 }}>{/* Content */}</Paper>
    </Box>
  );
};

export default MyComponent;
```

---

## 4. MUI v7 Styling (frontend-development)

### 4.1 Inline vs Separate Styles
| Style Lines | Approach |
|-------------|-----------|
| <100 lines | Inline `const styles: Record<string, SxProps<Theme>>` |
| >100 lines | Separate `.styles.ts` file |

### 4.2 MUI v7 Grid Syntax
```tsx
{/* ✅ v7 syntax */}
<Grid size={{ xs: 12, md: 6 }}>Content</Grid>

{/* ❌ Old syntax */}
<Grid xs={12} md={6}>Content</Grid>
```

### 4.3 sx Prop Type Safety
```tsx
import { Box } from "@mui/material";
import type { SxProps, Theme } from "@mui/material";

const styles: Record<string, SxProps<Theme>> = {
  container: { p: 2, bgcolor: "background.paper" },
};

<Box sx={styles.container}>Content</Box>;
```

---

## 5. RemixIcon Integration (web-frameworks)

### 5.1 Webfont Usage
```tsx
// In layout.tsx
import "remixicon/fonts/remixicon.css";

// In components
<i className="ri-home-line ri-2x"></i>
<i className="ri-search-fill"></i>
```

### 5.2 React Component Usage
```tsx
import { RiHomeLine, RiSearchFill } from "@remixicon/react";

<RiHomeLine size={24} />
<RiSearchFill size={32} color="var(--color-primary)" />
```

### 5.3 Accessibility
- Always provide `aria-label` for icon-only buttons
- Use `currentColor` for flexible theming
- Maintain 24x24 grid alignment for crisp rendering

---

## 6. Form Components (ui-styling + frontend-development)

### 6.1 React Hook Form + Zod
```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

export function LoginForm() {
  const form = useForm({
    resolver: zodResolver(schema),
    defaultValues: { email: "", password: "" },
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(console.log)} className="space-y-6">
        <FormField control={form.control} name="email" render={({ field }) => (
          <FormItem>
            <FormLabel>Email</FormLabel>
            <FormControl><Input type="email" {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )} />
        <Button type="submit" className="w-full">Sign In</Button>
      </form>
    </Form>
  );
}
```

---

## 7. Verification Checklist
- [ ] shadcn/ui components initialized with Tailwind v4
- [ ] Server vs Client Components correctly split
- [ ] Feature-based directory structure implemented
- [ ] MUI v7 styles use `sx` prop with type safety
- [ ] RemixIcon installed (webfont or React components)
- [ ] Forms use React Hook Form + Zod validation
- [ ] All interactive elements have focus states
- [ ] No `any` types in component props

---

## 8. Related References
- [02-tech-stack-setup.md](02-tech-stack-setup.md) → Next.js, Tailwind setup
- [03-design-system.md](03-design-system.md) → Typography, color
- [05-performance-optimization.md](05-performance-optimization.md) → Bundle size, waterfalls
- [06-accessibility-compliance.md](06-accessibility-compliance.md) → WCAG, ARIA
