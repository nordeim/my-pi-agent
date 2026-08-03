---
name: astro-6
description: Astro web framework workflow skill — the islands architecture, updated for Astro 6 (stable since March 2026, built on Astro 5's Content Layer API foundation). Covers the server-first mental model (zero JS by default — Astro components render to static HTML at build time, hydration is opt-in per-component via client:load / client:idle / client:visible / client:only / client:media directives), the multi-framework integration (React, Vue, Svelte, Preact, Solid, or Lit components in the same project), the Content Layer API for content collections (loader-based, Zod-4-validated Markdown/MDX/JSON/remote-API authoring — the legacy file-based collections were removed in Astro 6), Live Content Collections (stable in v6 — runtime data fetching with the same getCollection-style API), the Sessions API, the Fonts API, and built-in Content Security Policy (all stable in v6), Astro DB running on self-hosted libSQL/Turso (Astro Studio was sunset in 2025), file-based routing, layout inheritance, the View Transitions API via <ClientRouter />, Server Islands, middleware (src/middleware.ts, including the CVE-2025-66202 double-encoding hardening baked into the router), API endpoints (src/pages/api/), astro:env for type-safe environment variables, the Vite-7-powered build with the new Environment-API dev server (including native Cloudflare Workers/workerd local development), and deployment to static hosts or SSR adapters. Use when building any content-focused site — blog, documentation, marketing site, portfolio, e-commerce catalog — especially when the task involves content collections, choosing hydration directives, mixing UI frameworks in one project, migrating an existing Astro 5 project to Astro 6, or optimizing for Core Web Vitals where Astro's zero-JS-by-default approach differs fundamentally from Next.js / Nuxt / SvelteKit app frameworks.
license: Proprietary. LICENSE.txt has complete terms
---

# Astro 6 — Content-Focused Web Framework (Islands Architecture)

> **Target:** Astro **6.0+** (stable since March 2026) on **Node.js 22.12.0+** (Node 18 and 20 are End-of-Life and unsupported — Astro 6 requires Node 22.12.0 or higher). Astro 6 runs on **Vite 7** with a redesigned dev server built on Vite's Environment API, and **Zod 4** for content schema validation. It carries forward everything introduced in Astro 5 (the **Content Layer API**, **Server Islands**) and stabilizes what were previously experimental features: the **Sessions API**, the **Fonts API**, **Content Security Policy (CSP)**, and **Live Content Collections**. Astro's distinctive paradigm is unchanged: **zero JavaScript by default** — pages render to static HTML at build time, and interactive components ("islands") opt into hydration individually via `client:` directives.
>
> Still on Astro 5? Everything in this guide except the [Migration section](#migrating-from-astro-5-to-astro-6) applies equally — Astro 6 is an incremental evolution, not a rewrite. The legacy file-based content collections (no loader, `src/content/config.ts` without `loader:`) were removed in v6; if you haven't migrated yet, see [Migrating from Astro 5 to Astro 6](#migrating-from-astro-5-to-astro-6) first.

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending an Astro application (v5 or v6). Trigger phrases include "Astro", "islands architecture", "content collections", "Content Layer API", "live content collections", "MDX", "client:load", "client:idle", "client:visible", "client:only", "View Transitions", "ClientRouter", "Server Islands", "Astro DB", "Astro Sessions", "Astro Fonts API", "Content Security Policy" + Astro, "Astro Studio", "@astrojs/react", "@astrojs/vue", "@astrojs/svelte", "@astrojs/preact", "astro:content", "astro:env", "src/pages", "src/content", "src/middleware.ts", "astro.config.mjs", and any reference to `.astro` files or the `astro:*` import namespace.

Do **not** use this skill for:
- **Astro ≤4** — the Content Layer API is Astro 5+, and legacy file-based collections are removed entirely in Astro 6. This skill's syntax targets 5/6; Astro 4 projects need the older `src/content/config.ts` file-based collection API.
- **Next.js / Nuxt / SvelteKit** — these are app frameworks that ship JS by default. Astro is content-first with opt-in JS. Different paradigm. See `vue-3-nuxt`, `svelte-5-sveltekit`, and Next.js skills.
- **Pure static site generators** (Eleventy, Hugo, Jekyll) — Astro has components, hydration, and SSR; static SSGs are simpler but less capable.
- **Single-page apps** (Vite + React, Vite + Vue) — Astro can do SPA-like interactivity but is optimized for multi-page content sites.

Cross-reference: `framework-templates` may have an Astro section; this skill goes deep.

## Quick Start

```bash
# Create a new Astro project
npm create astro@latest my-app
# Prompts: template (Empty / Blog / Docs / Portfolio), TypeScript (yes/recommended),
#          install deps, init git, editor setup

cd my-app
npm install
npm run dev                     # Dev server at http://localhost:4321

# Add a UI framework integration (you can mix multiple in one project)
npx astro add react             # Adds @astrojs/react + React
npx astro add vue               # Adds @astrojs/vue + Vue
npx astro add svelte            # Adds @astrojs/svelte + Svelte
npx astro add tailwind          # Adds the Tailwind Vite plugin (Tailwind 4+)
npx astro add mdx               # Adds @astrojs/mdx for .mdx files
npx astro add sitemap           # Adds @astrojs/sitemap

# Upgrading an existing project (Astro + all official integrations together)
npx @astrojs/upgrade
```

### Key commands

```bash
npm run dev                     # Dev server with HMR (Astro 6: runs on Vite's Environment API)
npm run build                   # Production build to dist/
npm run preview                 # Preview the production build
npm run astro check             # TypeScript + Astro template diagnostics
npm run astro check --watch     # Watch mode

npx astro add <integration>     # Add an integration (auto-configures astro.config.mjs)
npx astro sync                  # Generate content collection types (auto-runs on dev/build)
npx astro info                  # Print environment + config diagnostics (useful for bug reports)
npx astro telemetry disable     # Opt out of telemetry
```

---

## Project Structure (canonical layout)

```
my-app/
├── src/
│   ├── pages/                  # ← File-based routing (each .astro = a URL)
│   │   ├── index.astro         # /
│   │   ├── about.astro         # /about
│   │   ├── blog/
│   │   │   ├── index.astro     # /blog
│   │   │   └── [slug].astro    # /blog/:slug (dynamic route)
│   │   └── api/
│   │       └── health.ts       # /api/health (API endpoint)
│   ├── layouts/                # Page layouts (reusable wrappers)
│   │   ├── BaseLayout.astro
│   │   └── BlogLayout.astro
│   ├── components/              # Reusable components (Astro + framework)
│   │   ├── Header.astro
│   │   ├── Footer.astro
│   │   ├── NewsletterForm.tsx  # React island
│   │   └── ThemeToggle.vue     # Vue island
│   ├── content.config.ts       # ← Content collection schemas (Astro 5+: replaces src/content/config.ts)
│   ├── content/                 # Local content sources (Markdown/MDX/data)
│   │   ├── blog/                # Blog posts (.md, .mdx)
│   │   │   ├── hello-world.md
│   │   │   └── second-post.mdx
│   │   └── authors/              # Author entries (.yaml, .json)
│   │       └── alice.yaml
│   ├── live.config.ts          # Live (runtime) content collections — stable in Astro 6
│   ├── styles/                  # Global styles
│   │   └── global.css
│   ├── lib/                     # Utilities
│   │   └── utils.ts
│   ├── middleware.ts            # Request middleware
│   └── env.d.ts                 # Ambient types (App.Locals, etc.)
├── public/                      # Static assets served as-is
│   ├── favicon.svg
│   └── images/
├── astro.config.mjs             # ← THE config file
├── tsconfig.json
├── package.json
└── Dockerfile
```

> **Astro 6 note:** `Astro.glob()` was removed. Use `import.meta.glob()` (Vite's native glob import, which is synchronous — no `await`) for arbitrary file imports, or `getCollection()` for content. Legacy content collections (schema without a `loader:`) are also gone — every collection needs an explicit loader (see below). A temporary `legacy.collectionsBackwardsCompat` config flag exists as a migration aid but is not a long-term fix.

### `astro.config.mjs` (the canonical config)

```javascript
import { defineConfig, fontProviders } from 'astro/config';
import react from '@astrojs/react';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

// For SSR (instead of static SSG)
// import node from '@astrojs/node';

export default defineConfig({
  site: 'https://example.com',           // Required for sitemap + canonical URLs
  output: 'static',                       // 'static' (default) or 'server' (SSR)

  integrations: [
    react(),                              // React island support
    mdx(),                                // MDX support
    sitemap(),                            // Auto-generates /sitemap.xml
  ],

  // Stable in Astro 6 — previously experimental.fonts
  fonts: [
    {
      provider: fontProviders.google(),
      name: 'Inter',
      cssVariable: '--font-inter',
    },
  ],

  // Stable in Astro 6 — previously experimental.csp
  security: {
    csp: true,                             // Auto-hashes inline scripts/styles, emits CSP headers/meta
  },

  // For SSR mode:
  // adapter: node({ mode: 'standalone' }),

  // Vite config passthrough
  vite: {
    resolve: {
      alias: {
        '@': '/src',
      },
    },
  },
});
```

---

## Core Mental Model: Zero JS by Default + Islands Architecture + Multi-Framework

Astro's distinctive paradigm is **server-first rendering with opt-in client-side interactivity.** Three things differentiate Astro from Next.js / Nuxt / SvelteKit:

### 1. Zero JavaScript by default (ship HTML, not JS)

```astro
---
// src/pages/index.astro
// This "frontmatter" runs on the server (build time for static, request time for SSR)
// NO JavaScript is shipped to the client by default
import { getCollection } from 'astro:content';
import BaseLayout from '../layouts/BaseLayout.astro';

const posts = await getCollection('blog');
const sortedPosts = posts.sort((a, b) => b.data.publishedAt.valueOf() - a.data.publishedAt.valueOf());
---

<BaseLayout title="Home">
  <h1>Latest Posts</h1>
  <ul>
    {sortedPosts.map((post) => (
      <li>
        <a href={`/blog/${post.id}`}>{post.data.title}</a>
        <time>{post.data.publishedAt.toLocaleDateString()}</time>
      </li>
    ))}
  </ul>
</BaseLayout>
```

This `.astro` file renders to pure HTML at build time. **Zero JavaScript** is shipped to the client. The page is instant — no hydration, no React/Vue runtime, no framework overhead. This is why Astro sites score well on Core Web Vitals by default.

Compare to Next.js, which ships tens of kilobytes of JS even for a static page (React runtime + framework runtime + page component).

> Note the entry is referenced by `post.id`, not `post.slug`. Astro 5's Content Layer API renamed the stable per-entry identifier to `id` (path-derived by default, or loader-defined); the legacy `slug` property only exists under the `legacy.collectionsBackwardsCompat` flag and is gone entirely in a default Astro 6 setup.

### 2. Islands architecture (opt-in hydration per component)

When you DO need interactivity, you create an "island" — an isolated interactive component hydrated independently of the rest of the page.

```astro
---
// src/pages/index.astro
import NewsletterForm from '../components/NewsletterForm.tsx';  // React component
import ThemeToggle from '../components/ThemeToggle.vue';          // Vue component
---

<html>
<body>
  <h1>My Blog</h1>

  <!-- Hydration directives: -->
  <NewsletterForm client:load />            <!-- Hydrate immediately on page load -->
  <ThemeToggle client:idle />               <!-- Hydrate when browser is idle -->
  <NewsletterForm client:visible />         <!-- Hydrate when scrolled into view -->
  <NewsletterForm client:only="react" />    <!-- Skip SSR, render only on client -->
  <NewsletterForm client:media="(max-width: 50em)" />  <!-- Hydrate only on mobile -->
</body>
</html>
```

| Directive | When to hydrate | Use for |
|---|---|---|
| `client:load` | Immediately | Critical interactive elements above the fold (header nav, login button) |
| `client:idle` | When browser is idle (requestIdleCallback) | Below-the-fold interactive elements |
| `client:visible` | When scrolled into view (IntersectionObserver) | Comments, widgets far down the page |
| `client:media="(query)"` | When media query matches | Mobile-only or desktop-only widgets |
| `client:only="react"` | Skip SSR, render only on client | Components that can't render on server (e.g., use `window`) |

The key insight: each island hydrates **independently**. A heavy React chart at the bottom of the page doesn't block the header navigation from becoming interactive. This is fundamentally different from React/Vue SPA apps where the entire app hydrates as one unit.

### 3. Multi-framework (use React + Vue + Svelte in one project)

Astro is renderer-agnostic. You can install multiple framework integrations and use components from each in the same page:

```bash
npx astro add react vue svelte preact
```

```astro
---
// src/pages/index.astro — mixing React, Vue, and Svelte in one page
import ReactChart from '../components/ReactChart.tsx';      // React
import VueCounter from '../components/VueCounter.vue';       // Vue
import SvelteSearch from '../components/SvelteSearch.svelte'; // Svelte
import AstroHeader from '../components/AstroHeader.astro';   // Astro (zero JS)
---

<AstroHeader />                          <!-- Static HTML, no JS -->
<ReactChart client:visible />            <!-- React island, lazy-hydrated -->
<VueCounter client:load />               <!-- Vue island, immediately hydrated -->
<SvelteSearch client:idle />             <!-- Svelte island, idle-hydrated -->
```

This is invaluable for:
- **Migration**: incrementally move a React SPA to Astro — start with Astro shell, port components one by one
- **Best-of-breed**: use React for complex stateful widgets, Vue for simple interactions, Astro for static content
- **Team mix**: teams proficient in different frameworks can contribute to the same Astro site

---

## Content Collections — the Content Layer API (mandatory since Astro 6)

Astro 5 introduced the **Content Layer API**; Astro 6 makes it the *only* way to define collections (the old schema-only, loader-less collections were removed). Content collections are type-safe Markdown/MDX/JSON/YAML/remote-API data with Zod schema validation.

### Define a collection

```typescript
// src/content.config.ts
import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';          // Astro 6: import z from 'astro/zod', not 'astro:content'
import { glob } from 'astro/loaders';

const blog = defineCollection({
  // Load all .md/.mdx files from src/content/blog/
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),

  // Zod 4 schema — validates frontmatter at build time
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishedAt: z.coerce.date(),
    updatedAt: z.coerce.date().optional(),
    author: z.string(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
    image: z.string().optional(),
  }),
});

const authors = defineCollection({
  // Can also load from JSON, YAML, or external APIs
  loader: glob({ pattern: '**/*.yaml', base: './src/content/authors' }),
  schema: z.object({
    name: z.string(),
    bio: z.string(),
    avatar: z.string(),
    social: z.object({
      twitter: z.string().optional(),
      github: z.string().optional(),
    }).optional(),
  }),
});

export const collections = { blog, authors };
```

> **Zod 4 gotchas (Astro 6 upgraded the bundled Zod from v3 to v4):**
> - `z.string().email()` / `.url()` etc. are deprecated string-method formats — use the top-level function instead: `z.email()`, `z.url()`.
> - `.min(n, { message: '...' })` → `.min(n, { error: '...' })` (the `message` option was renamed `error`).
> - `.default()` after `.transform()` must match the **output** type, not the input type: `z.string().transform(Number).default(0)`, not `.default("0")`. Use `.prefault()` if you need the old (pre-transform) default behavior.
> - Always import `z` from `astro/zod` (not `astro:schema` or `astro:content` — both are deprecated re-exports removed in v6).

### Author content

```markdown
---
# src/content/blog/hello-world.md
title: "Hello World"
description: "My first Astro blog post"
publishedAt: 2026-01-15
author: "alice"
tags: ["astro", "tutorial"]
draft: false
---

# Hello World

This is my first post. The frontmatter above is validated against the Zod schema
at build time — if I misspell `publishedAt` or use a string instead of a date,
the build fails with a clear error.

MDX is also supported — import framework components directly:

import Chart from '../../components/Chart.tsx';

<Chart client:visible data={[1, 2, 3]} />
```

### Query content

```astro
---
// src/pages/blog/index.astro
import { getCollection, render } from 'astro:content';
import BaseLayout from '../../layouts/BaseLayout.astro';

// Get all blog entries (type-safe — entries are typed by the Zod schema)
const posts = await getCollection('blog', ({ data }) => {
  return import.meta.env.PROD ? !data.draft : true;   // Filter drafts in prod
});

// Sort by date
posts.sort((a, b) => b.data.publishedAt.valueOf() - a.data.publishedAt.valueOf());
---

<BaseLayout title="Blog">
  <ul>
    {posts.map((post) => (
      <li>
        <a href={`/blog/${post.id}`}>{post.data.title}</a>
        <time>{post.data.publishedAt.toLocaleDateString()}</time>
        <ul>
          {post.data.tags.map((tag) => <li>{tag}</li>)}
        </ul>
      </li>
    ))}
  </ul>
</BaseLayout>
```

```astro
---
// src/pages/blog/[slug].astro — dynamic route
import { getCollection, getEntry, render } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map((post) => ({
    params: { slug: post.id },                       // URL parameter — must be a string
    props: { post },                                 // Pass to the page
  }));
}

const { post } = Astro.props;
const { Content } = await render(post);              // Standalone render(), not entry.render()
---

<h1>{post.data.title}</h1>
<time>{post.data.publishedAt.toLocaleDateString()}</time>

<Content />                                          <!-- The Markdown body -->
```

> `getEntryBySlug()` and `getDataEntryById()` are deprecated in favor of a single `getEntry('collectionName', id)`. `entry.render()` is gone — import and call the standalone `render(entry)` function from `astro:content` instead.

### Loading from external sources (build-time)

The Content Layer API can load content from anywhere — not just local files:

```typescript
// src/content.config.ts — load from an external API at build time
import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';

const products = defineCollection({
  loader: async () => {
    const response = await fetch('https://api.example.com/products');
    if (!response.ok) throw new Error(`Failed to load products: ${response.status}`);
    const data = await response.json();
    return data.map((item: { slug: string }) => ({ id: item.slug, ...item }));
  },
  schema: z.object({
    id: z.string(),
    name: z.string(),
    price: z.number(),
    description: z.string(),
  }),
});

export const collections = { products };
```

This makes Astro a powerful headless-CMS-friendly framework — fetch from Sanity, Contentful, Shopify, or any API at build time, with full type safety.

### Live Content Collections (stable in Astro 6 — runtime data)

Build-time collections bake data into the site at `build`. When content genuinely changes per request (stock prices, inventory, a live dashboard), use **Live Content Collections** — the same `getCollection`-style API, but resolved at request time against an on-demand-rendered page.

```typescript
// src/live.config.ts
import { defineLiveCollection } from 'astro:content';
import { storeLoader } from './loaders/store';

const products = defineLiveCollection({
  loader: storeLoader({
    apiKey: process.env.STORE_API_KEY,
    endpoint: 'https://api.mystore.com/v1',
  }),
});

export const collections = { products };
```

```astro
---
// src/pages/products/[slug].astro
export const prerender = false;                       // Required — live collections need on-demand rendering
import { getLiveEntry } from 'astro:content';

const { entry: product, error } = await getLiveEntry('products', Astro.params.slug);

if (error) {
  console.error('Failed to load product:', error.message);
  return Astro.rewrite('/404');
}
---

<h1>{product.data.name}</h1>
<p>{Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(product.data.price)}</p>
```

Live collections return a `{ entries, error }` / `{ entry, error }` result object instead of throwing — handle the `error` case explicitly rather than assuming the fetch succeeded. Live loaders need `defineLiveCollection` + a `LiveLoader` (a `loadCollection` / `loadEntry` pair), distinct from the build-time `Loader` interface used by `defineCollection`.

---

## Astro Components (the `.astro` syntax)

```astro
---
// src/components/PostCard.astro
// Frontmatter (server-side only — runs at build or request time)
import type { CollectionEntry } from 'astro:content';

interface Props {
  post: CollectionEntry<'blog'>;
  featured?: boolean;
}

const { post, featured = false } = Astro.props;
const url = `/blog/${post.id}`;
---

<article class:list={['post-card', { featured }]}>
  {post.data.image && <img src={post.data.image} alt={post.data.title} loading="lazy" />}
  <div class="content">
    <h3><a href={url}>{post.data.title}</a></h3>
    <p>{post.data.description}</p>
    <div class="meta">
      <time>{post.data.publishedAt.toLocaleDateString()}</time>
      <span>by {post.data.author}</span>
    </div>
  </div>
</article>

<style>
  /* Scoped by default — only applies to this component */
  .post-card {
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    padding: 1rem;
    margin-bottom: 1rem;
  }

  .post-card.featured {
    border-color: #f59e0b;
    background: #fffbeb;
  }
</style>

<script>
  // Client-side JS (processed by Vite — TypeScript + bundling supported)
  // This runs ONLY if the component is rendered on a page
  document.querySelectorAll('.post-card').forEach((card) => {
    card.addEventListener('click', (e) => {
      if (e.target instanceof HTMLAnchorElement) return;
      const link = card.querySelector('a');
      link?.click();
    });
  });
</script>
```

Key `.astro` features:
- **Frontmatter** (`---` blocks): server-only TypeScript, runs at build/request time
- **`Astro.props`**: typed component props (via TypeScript `interface Props`)
- **`class:list`**: conditional class names (like `clsx`)
- **`<style>`**: scoped by default (use `is:global` for global styles)
- **`<script>`**: processed by Vite (TypeScript, bundling, HMR in dev)
- **`set:html`**: inject raw HTML (sanitize first — this bypasses Astro's automatic escaping and is an XSS vector for untrusted input)

> **Compiler note:** Astro 6 ships an opt-in Rust-based compiler (`@astrojs/compiler-rs`, `experimental: { rustCompiler: true }`) that is faster and has stricter diagnostics than the original Go-based compiler, and is on a path to becoming the default. It does **not** auto-correct invalid HTML nesting the way the Go compiler silently did — malformed markup that used to "just work" may now throw a build error or render differently. Fix the markup rather than relying on compiler leniency.

---

## Layouts

```astro
---
// src/layouts/BaseLayout.astro
import Header from '../components/Header.astro';
import Footer from '../components/Footer.astro';

interface Props {
  title: string;
  description?: string;
}

const { title, description = 'Default description' } = Astro.props;
const { pathname } = Astro.url;
---

<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <meta name="description" content={description} />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link rel="canonical" href={new URL(pathname, import.meta.env.SITE).href} />
  </head>
  <body>
    <Header pathname={pathname} />
    <main>
      <slot />                                       <!-- Page content goes here -->
    </main>
    <Footer />
  </body>
</html>
```

> `Astro.site` is deprecated for use inside `getStaticPaths()` in Astro 6 (it only ever exposed `site`/`generator` there, which was confusing). Use `import.meta.env.SITE` instead — it works consistently in both frontmatter and `getStaticPaths()`.

### Named slots

```astro
---
// src/layouts/BlogPostLayout.astro
import BaseLayout from './BaseLayout.astro';

interface Props { title: string; author: string; date: Date }
const { title, author, date } = Astro.props;
---

<BaseLayout title={title}>
  <article>
    <header>
      <h1>{title}</h1>
      <p>by {author} on {date.toLocaleDateString()}</p>
    </header>

    <slot />                                         <!-- Default slot -->

    <footer>
      <slot name="footer">No footer provided</slot>  <!-- Named slot with fallback -->
    </footer>
  </article>
</BaseLayout>
```

```astro
---
// src/pages/blog/[slug].astro
import BlogPostLayout from '../../layouts/BlogPostLayout.astro';
---

<BlogPostLayout title="Hello" author="Alice" date={new Date()}>
  <p>Main content goes here.</p>

  <div slot="footer">                                <!-- Named slot content -->
    <p>Share this post: ...</p>
  </div>
</BlogPostLayout>
```

---

## View Transitions (`<ClientRouter />`)

Astro's View Transitions component gives native browser page transitions without a SPA router. It was renamed from `<ViewTransitions />` to **`<ClientRouter />`** to better describe what it does (it's not the View Transitions API itself, but Astro's client-side router built on top of it) — use `<ClientRouter />` in new code.

```astro
---
// src/layouts/BaseLayout.astro
import { ClientRouter } from 'astro:transitions';
---

<head>
  <ClientRouter />                                   <!-- Enable client-side page transitions globally -->
</head>
<body>
  <header>...</header>
  <main><slot /></main>
</body>
```

```astro
---
// src/pages/index.astro
---

<!-- Mark elements for transition behavior -->
<header transition:animate="slide">My Header</header>

<!-- Persist an element across pages (e.g., a video player) -->
<video transition:persist src="/intro.mp4" />

<!-- Name an element for morphing between pages -->
<img transition:name="hero-image" src="/hero.png" alt="Hero" />
```

```astro
---
// src/pages/about.astro — the image with the same transition:name morphs across pages
<img transition:name="hero-image" src="/hero-about.png" alt="Hero" />
```

> Astro 6 removes a handful of previously-exposed low-level internals from `astro:transitions` / `astro:transitions/client` (`createAnimationScope()`, the `TRANSITION_*` string constants, `isTransitionBeforePreparationEvent()` and similar type guards). If you were relying on these, listen for the documented DOM events directly (e.g. `document.addEventListener('astro:before-preparation', ...)`) instead of the removed helper exports.

---

## Server Islands

Server Islands defer rendering of personalized content in an otherwise-static page. The page is served as static HTML immediately, then personalized components stream in.

```astro
---
// src/pages/index.astro — static page with one personalized island
import BaseLayout from '../layouts/BaseLayout.astro';
import UserProfile from '../components/UserProfile.astro';
---

<BaseLayout title="Home">
  <h1>Welcome!</h1>
  <p>This page is static — instant load, zero JS for the static parts.</p>

  <!-- Server Island — renders later, can be personalized -->
  <UserProfile server:defer>
    <div slot="fallback">Loading your profile...</div>
  </UserProfile>
</BaseLayout>
```

```astro
---
// src/components/UserProfile.astro — the deferred component
// This runs on the server when the island is requested
import { getUserFromCookie } from '../lib/auth';

const user = await getUserFromCookie(Astro.cookies);
---

{user ? (
  <div class="profile">Hello, {user.name}!</div>
) : (
  <div class="profile"><a href="/login">Sign in</a></div>
)}
```

The page renders instantly as static HTML. The `UserProfile` island is fetched separately (as an HTML fragment) and swapped in when ready. This gives you the performance of static pages with the personalization of SSR — without shipping JS for the personalization logic. Astro 6 also exempts server island internal routes from `getStaticPaths()` validation, fixing false-positive build errors when using server islands on fully static (`output: 'static'`) sites.

---

## New Stable APIs in Astro 6: Sessions, Fonts, CSP

### Sessions API (stable since Astro 5.7)

Server-side session storage tied to a visitor, without exposing data in cookies. Requires on-demand rendering (`export const prerender = false;`, or `output: 'server'`).

```javascript
// astro.config.mjs
import { defineConfig, sessionDrivers } from 'astro/config';
import netlify from '@astrojs/netlify';

export default defineConfig({
  adapter: netlify(),
  session: {
    driver: sessionDrivers.redis({ url: process.env.REDIS_URL }),  // Astro 6 object shape
    cookie: { secure: true },
    ttl: 3600,
  },
});
```

```astro
---
// src/pages/cart.astro
export const prerender = false;

const cart = (await Astro.session?.get('cart')) ?? [];
if (Astro.request.method === 'POST') {
  const form = await Astro.request.formData();
  cart.push(form.get('sku'));
  await Astro.session?.set('cart', cart);
}
---

<p>{cart.length} item(s) in your cart</p>
```

Node, Cloudflare, and Netlify adapters auto-configure a sensible default session driver; other targets need an explicit driver. `session.regenerate()` and `session.destroy()` handle ID rotation and logout.

### Fonts API (stable since Astro 6 — top-level `fonts` config)

```javascript
// astro.config.mjs
import { defineConfig, fontProviders } from 'astro/config';

export default defineConfig({
  fonts: [
    { provider: fontProviders.google(), name: 'Inter', cssVariable: '--font-inter' },
    { provider: fontProviders.fontsource(), name: 'JetBrains Mono', cssVariable: '--font-mono' },
  ],
});
```

```astro
---
import { Font } from 'astro:assets';
---
<head>
  <Font cssVariable="--font-inter" preload />
</head>
<style>
  body { font-family: var(--font-inter); }
</style>
```

Astro downloads, self-hosts, subsets, and generates fallback metrics for the font automatically — no manual `@font-face`, no third-party render-blocking requests.

### Content Security Policy (stable since Astro 6 — `security.csp`)

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';

export default defineConfig({
  security: {
    csp: true,   // Auto-hashes every script/style and emits CSP headers or a <meta> tag
  },
});
```

For more control:

```javascript
export default defineConfig({
  security: {
    csp: {
      algorithm: 'SHA-512',          // 'SHA-256' (default), 'SHA-384', or 'SHA-512'
      directives: [
        "default-src 'self'",
        "img-src 'self' https://images.cdn.example.com",
      ],
      styleDirective: { hashes: ['sha384-styleHash'] },
      scriptDirective: { hashes: ['sha384-scriptHash'] },
    },
  },
});
```

CSP works across static and on-demand rendering, is compatible with all official adapters, and — as of Astro 6 — automatically hashes the classes/attributes generated by responsive `<Image />` styling too.

---

## Middleware

```typescript
// src/middleware.ts
import { defineMiddleware } from 'astro:middleware';

export const onRequest = defineMiddleware(async (context, next) => {
  const { request, url, cookies } = context;

  // Log every request (avoid logging cookies, auth headers, or full request bodies)
  console.log(`${request.method} ${url.pathname}`);

  // Auth check (skip for public routes)
  if (!url.pathname.startsWith('/admin')) {
    return next();
  }

  const session = cookies.get('session')?.value;
  if (!session) {
    return new Response(null, {
      status: 302,
      headers: { Location: '/login' },
    });
  }

  // Attach to locals (typed via env.d.ts)
  context.locals.user = await getUserFromSession(session);

  return next();
});
```

```typescript
// src/env.d.ts — type locals
declare namespace App {
  interface Locals {
    user: User | null;
  }
}
```

> **Security — keep the router updated.** CVE-2025-66202 was a middleware authorization-bypass: a double-percent-encoded path segment (e.g. `%2561` decoding to `%61` decoding to `a`) could reach route handlers without being fully decoded first, letting a path like `/api/%61dmin` slip past a naive `pathname.startsWith('/admin')` check in middleware. This is fixed at the router level (multi-level percent-encoding is now iteratively resolved to canonical form before middleware runs) as of the patched Astro releases — pin Astro to a version that includes the fix and avoid re-implementing your own decoding logic in middleware path checks, since that's exactly the class of bug that caused this.

---

## API Endpoints

```typescript
// src/pages/api/health.ts — GET /api/health
import type { APIRoute } from 'astro';

export const GET: APIRoute = async () => {
  return new Response(JSON.stringify({ status: 'ok' }), {
    headers: { 'Content-Type': 'application/json' },
  });
};

// src/pages/api/users.ts — POST /api/users
export const POST: APIRoute = async ({ request }) => {
  const body = await request.json();
  // Validate with a schema (e.g. z.object(...).parse(body)) before trusting any field
  return new Response(JSON.stringify({ id: 1, ...body }), {
    status: 201,
    headers: { 'Content-Type': 'application/json' },
  });
};
```

For SSR mode, API endpoints run on every request. For static mode, they're called at build time (useful for generating data-driven pages). Endpoints whose URL ends in a file extension (e.g. `sitemap.xml.ts`) can no longer be reached with a trailing slash in Astro 6, regardless of `build.trailingSlash` — link to `/sitemap.xml`, not `/sitemap.xml/`.

---

## `astro:env` — type-safe environment variables

Astro's `env` config validates environment variables against a schema and exposes them through typed modules, instead of the untyped `import.meta.env` string bag.

```javascript
// astro.config.mjs
import { defineConfig, envField } from 'astro/config';

export default defineConfig({
  env: {
    schema: {
      PUBLIC_SITE_NAME: envField.string({ context: 'client', access: 'public' }),
      DATABASE_URL: envField.string({ context: 'server', access: 'secret' }),
      MAX_ITEMS: envField.number({ context: 'server', access: 'public', default: 50 }),
    },
  },
});
```

```typescript
// Client-side (browser-safe — only "public" context: "client" vars)
import { PUBLIC_SITE_NAME } from 'astro:env/client';

// Server-side (never bundled to the client)
import { DATABASE_URL, MAX_ITEMS, getSecret } from 'astro:env/server';

// getSecret() reads variables not declared in the schema (works across Node, Cloudflare, Deno)
const backupUrl = getSecret('BACKUP_DATABASE_URL');
```

This catches an entire class of bug at build time: a secret imported into a client component now throws instead of silently leaking into the browser bundle. Prefer `astro:env` over raw `import.meta.env` for anything security- or type-sensitive; note that Astro 6 always inlines `import.meta.env` values verbatim (no more automatic `"true"` → `true` coercion or silent fallback to `process.env` for non-public keys) — read `process.env` explicitly server-side if you need that.

---

## Astro DB (post-Studio: bring your own libSQL)

**Astro Studio, the hosted database/deploy service, was sunset in 2025.** `@astrojs/db` still works, but there is no first-party hosted backend anymore — you point it at any libSQL-compatible database yourself (Turso is the most common choice; Cloudflare D1, plain SQLite files, or a self-hosted libSQL server also work).

```typescript
// db/config.ts
import { defineDb, defineTable, column } from 'astro:db';

const Comment = defineTable({
  columns: {
    id: column.number({ primaryKey: true }),
    postSlug: column.text(),
    author: column.text(),
    body: column.text(),
    createdAt: column.date({ default: new Date() }),
  },
});

export default defineDb({ tables: { Comment } });
```

```bash
# Local development uses a local SQLite file automatically — no setup needed
npm run dev

# Production: provision a Turso (or other libSQL) database, then:
astro db push --remote
```

```bash
# .env (production)
ASTRO_DB_REMOTE_URL=libsql://your-db-name.turso.io
ASTRO_DB_APP_TOKEN=your-turso-auth-token
```

If you're following an older tutorial that uses `astro login` / `astro link` / the Astro Studio dashboard, those commands no longer work — replace that workflow with a Turso (or other libSQL provider) database and the `ASTRO_DB_REMOTE_URL` / `ASTRO_DB_APP_TOKEN` environment variables above. For anything beyond a comments widget or small dataset, evaluate whether a dedicated Postgres/MySQL service plus an ORM (Drizzle, Prisma) better fits the durability and query needs — Astro DB is a convenience layer, not a required piece of the stack.

---

## Deployment

### Static (default — `output: 'static'`)

```bash
npm run build                   # Outputs to dist/
# Deploy dist/ to any static host:
# - Netlify: connect repo or drag-and-drop
# - Vercel: `vercel` CLI
# - Cloudflare Pages: `wrangler pages deploy dist`
# - GitHub Pages: `gh-pages` or GitHub Actions
```

### SSR (with adapter)

```bash
npx astro add node              # Add Node.js adapter
# OR
npx astro add vercel            # Vercel adapter
# OR
npx astro add cloudflare        # Cloudflare adapter
# OR
npx astro add netlify           # Netlify adapter
```

```javascript
// astro.config.mjs
import node from '@astrojs/node';

export default defineConfig({
  output: 'server',             // SSR mode
  adapter: node({ mode: 'standalone' }),
});
```

```bash
npm run build                   # Outputs to dist/server/entry.mjs
node dist/server/entry.mjs      # Run the SSR server
```

### Hybrid mode (`output: 'static'` with per-page SSR)

```astro
---
// src/pages/dashboard.astro — opt this page into on-demand rendering
export const prerender = false;
---
```

With `output: 'static'` (default) and `export const prerender = false` on specific pages, you get the best of both worlds: most pages are static (pre-rendered at build), but personalized pages (dashboard, profile, live-collection pages) render on the server per request. This requires an adapter even though most pages stay static.

### Cloudflare Workers: real local dev, not a simulation

Astro 6's dev server is rebuilt on Vite's Environment API. With the Cloudflare adapter, `astro dev` now runs inside `workerd` (Cloudflare's actual JS runtime) instead of a polyfilled approximation — Durable Objects, KV, R2, and Workers Analytics Engine are usable locally with HMR:

```javascript
// Access bindings directly via the cloudflare:workers module
import { env } from 'cloudflare:workers';

const kv = env.MY_KV_NAMESPACE;
await kv.put('visits', '1');
```

`Astro.locals.runtime` (the old way of reaching Cloudflare bindings) is removed in the Astro 6 Cloudflare adapter — migrate to the `cloudflare:workers` module directly.

---

## Migrating from Astro 5 to Astro 6

Run the automated upgrader first, then work through what it can't fix automatically:

```bash
npx @astrojs/upgrade
```

| Area | Astro 5 | Astro 6 |
|---|---|---|
| Node.js | 18.20.8+ / 20.3.0+ | **22.12.0+ required** — Node 18 & 20 are unsupported |
| Content collections | Content Layer API *or* legacy file-based | **Content Layer API only** — legacy collections removed (temporary `legacy.collectionsBackwardsCompat` escape hatch) |
| Entry identifier | `entry.slug` (legacy) / `entry.id` (Content Layer) | `entry.id` only — `.slug` is gone outside the compat flag |
| Rendering markdown body | `entry.render()` | Standalone `render(entry)` imported from `astro:content` |
| Zod import | `z` from `astro:content` or `astro:schema` | `z` from `astro/zod` (Zod **4** — see the schema gotchas above) |
| `Astro.glob()` | Available | **Removed** — use `import.meta.glob()` or `getCollection()` |
| Fonts / Sessions / CSP / Live Collections | `experimental.fonts` / `experimental.session` / `experimental.csp` / `experimental.liveContentCollections` | Stable top-level config: `fonts`, `session`, `security.csp`; live collections on by default with `defineLiveCollection` |
| View Transitions component | `<ViewTransitions />` (deprecated alias) | `<ClientRouter />` |
| `import.meta.env.ASSETS_PREFIX` | Supported | Deprecated — use `build.assetsPrefix` from `astro:config/server` |
| `import.meta.env` values | Could coerce types / fall back to `process.env` | Always inlined verbatim, never coerced |
| Default image `fit` | Cropping only applied when `fit` was set | Cropping applied by default; images never upscale |
| Vite / Zod / Shiki | Vite 6 / Zod 3 / Shiki 3 | Vite 7 / Zod 4 / Shiki 4 |
| Cloudflare adapter | `Astro.locals.runtime` | `cloudflare:workers` module; `astro dev` runs on real `workerd` |

Read the [official upgrade guide](https://docs.astro.build/en/guides/upgrade-to/v6/) for the complete breaking-changes list (adapter API changes, `SSRManifest` shape, Vite Environment API impacts on custom integrations) — it is long, but the vast majority of entries only matter if you maintain a custom integration or adapter. A typical content site mainly needs: bump Node, switch to loader-based collections if not already done, fix `entry.slug` → `entry.id`, update Zod schemas for v4, and re-check any code that reached into `experimental.*` config keys.

---

## Top Anti-Patterns (the most valuable section)

1. **Shipping JS when you don't need it.** The #1 Astro mistake. Use Astro components (`.astro`) for static content and reserve framework components (React/Vue/Svelte) for genuinely interactive elements. If a component doesn't have state or event handlers, it should be `.astro`, not `.tsx`.

2. **`client:load` for everything.** `client:load` hydrates immediately — wasteful for below-the-fold components. Use `client:idle` for non-critical interactivity, `client:visible` for components far down the page, `client:media` for mobile/desktop-only widgets. Reserve `client:load` for above-the-fold critical interactions.

3. **Still using loader-less content collections.** Astro 6 removed the legacy schema-only collection API entirely. If a project still has `src/content/config.ts` with a `type: 'content'`/`type: 'data'` collection and no `loader:`, either migrate it to `glob()` (or another loader) now, or set `legacy.collectionsBackwardsCompat: true` as a short-lived bridge — don't leave that flag on indefinitely, it's explicitly a temporary migration helper, not a supported long-term mode.

4. **Reaching for Live Content Collections when a build-time collection would do.** Live collections add a network round trip, error-handling burden, and force `prerender = false` on every page that uses them. If content changes at most a few times a day, a build-time `defineCollection` loader plus a scheduled rebuild (webhook-triggered CI build) is simpler and faster than paying the runtime cost on every request.

5. **Not using `client:only` for components that use `window`/`document`.** If a React/Vue component references `window` or `document` at module level, SSR will fail with "window is not defined". Use `client:only="react"` to skip SSR — but the component won't render until JS loads (show a placeholder via `slot="fallback"`).

6. **Giant layout files.** Layouts should be the HTML shell (`<html>`, `<head>`, `<body>`, header, footer, `<slot />`). Business logic doesn't belong in layouts. If your layout has `getCollection()` calls or complex conditionals, extract them into components.

7. **Not using View Transitions for multi-page sites.** `<ClientRouter />` gives SPA-like navigation with zero JS framework cost. Without it, every page navigation is a full page reload (jarring). Add `<ClientRouter />` to your base layout's `<head>` — it's a one-line upgrade that dramatically improves perceived performance. (If a tutorial shows `<ViewTransitions />`, mentally substitute `<ClientRouter />` — the old name is a deprecated alias.)

8. **Forgetting `site` for canonical URLs.** Without `site: 'https://example.com'` in `astro.config.mjs`, canonical URLs, sitemaps, and RSS feeds resolve against `localhost` in dev and can silently produce wrong absolute URLs in edge cases. Set the `site` config always, and read it via `import.meta.env.SITE` (not `Astro.site`) inside `getStaticPaths()`.

9. **Rolling your own path-prefix auth check in middleware.** A naive `url.pathname.startsWith('/admin')` guard is exactly the pattern that was exploitable via double-percent-encoded paths before the router-level fix for CVE-2025-66202. Keep Astro patched, and don't attempt to hand-roll URL decoding/normalization in middleware — trust the framework's route matching to hand you an already-canonicalized `url`/`params`.

10. **Skipping `astro:env` for secrets.** Reading `import.meta.env.DATABASE_URL` (or worse, a hardcoded string) inside a component that might get imported client-side risks bundling a secret into the browser payload with no warning. Define server secrets in the `env.schema` with `context: 'server', access: 'secret'` — Astro throws at build time if a secret leaks into a client-context import.

11. **Assuming Astro Studio is still the Astro DB backend.** Older tutorials reference `astro login` / `astro link` and a Studio dashboard; Astro Studio was sunset in 2025. Point `astro db push --remote` at a Turso (or other libSQL) database via `ASTRO_DB_REMOTE_URL` / `ASTRO_DB_APP_TOKEN` instead, or use a different database entirely for anything beyond small, low-durability datasets.

12. **Loading content from external APIs at request time when build time works.** If content doesn't change per-user, fetch it at build time (in the `.astro` frontmatter or a content collection loader). Don't pay the runtime cost of an API call on every request for content that's the same for everyone — that's what Live Content Collections are for when you *do* need per-request freshness, and a build-time loader otherwise.

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for Astro (project onboarding)
- `vue-3-nuxt` — Vue + Nuxt (Astro can use Vue components as islands — the Vue skill covers Vue component authoring)
- `svelte-5-sveltekit` — Svelte + SvelteKit (Astro can use Svelte components as islands)
- `react19-ts6-vite8-tailwindv4-mvp` — React (Astro can use React components as islands)
- `frontend-ui-engineering` — Production-quality UI build patterns (relevant for Astro components)
- `frontend-design` — Design thinking for web UI
- `api-and-interface-design` — Type contract design (relevant for content collection schemas and API endpoints)
- `api-patterns` — REST API patterns (for Astro API routes)
- `security-and-hardening` — OWASP-aware hardening (Astro has good XSS defaults via auto-escaping; see the CSP and middleware sections above)
- `clean-code` — General coding standards
- `testing-patterns` — Test pyramid, mocking strategies (note: Astro 6 requires Vitest's `node` environment, not `jsdom`/`happy-dom`, for tests that render `.astro` components via the Container API)
- `code-review-checklist` — 12-category code review checklist

---

## Dependencies

Required (installed via `npm create astro`):
- **Node.js** 22.12.0+ (Node 18 and 20 are End-of-Life and unsupported by Astro 6)
- **Astro** 6.0+ (5.x still works with this guide minus the Migration section)
- **Vite** 7+ (build tool, bundled with Astro 6; Astro 5 bundled Vite 6)
- **TypeScript** 5+ (default, can opt out but not recommended)

### UI framework integrations (add via `npx astro add`)

- `@astrojs/react` — React island support
- `@astrojs/vue` — Vue island support
- `@astrojs/svelte` — Svelte island support
- `@astrojs/preact` — Preact island support
- `@astrojs/solid-js` — SolidJS island support
- `@astrojs/lit` — Lit web component support

### Content & styling integrations

- `@astrojs/mdx` — MDX support (Markdown + JSX)
- Tailwind CSS 4 — via the official Vite plugin (`@tailwindcss/vite`), the current recommended path; `@astrojs/tailwind` targeted Tailwind 3 and is in maintenance mode
- `@astrojs/sitemap` — auto-generate `/sitemap.xml`
- `@astrojs/rss` — RSS feed generation
- `@astrojs/partytown` — move third-party scripts to a web worker (improves performance)

### SSR adapters (add via `npx astro add`)

- `@astrojs/node` — self-hosted Node.js SSR
- `@astrojs/vercel` — Vercel SSR
- `@astrojs/cloudflare` — Cloudflare Pages/Workers SSR (Astro 6: native `workerd` local dev, `cloudflare:workers` bindings)
- `@astrojs/netlify` — Netlify SSR
- `@astrojs/deno` — Deno Deploy SSR

### Common additions

- `astro-icon` — icon component (uses Iconify)
- `astro-seo` — SEO meta tags component
- `astro-pagefind` — client-side full-text search (Pagefind)
- `@astrojs/db` — Astro DB; point `ASTRO_DB_REMOTE_URL` / `ASTRO_DB_APP_TOKEN` at Turso or another libSQL provider (Astro Studio is sunset)
- `keystatic` + `@keystatic/core` — headless CMS for Astro content collections
