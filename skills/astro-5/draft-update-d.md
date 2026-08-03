---
name: astro-5
description: Astro 5, content-focused web framework workflow skill — the islands architecture. Covers the server-first mental model (zero JS by default — Astro components render to static HTML at build time, hydration is opt-in per-component via client:load / client:idle / client:visible / client:only directives), the multi-framework integration (use React, Vue, Svelte, Preact, Solid, or Lit components in the same Astro project — @astrojs/react, @astrojs/vue, etc.), content collections (the type-safe Markdown/MDX authoring system with Zod schemas — Content Layer API in Astro 5 replaces the legacy file-based collections), Astro Studio + Astro DB (Astro's managed backend), file-based routing with src/pages/, layout inheritance with Astro layouts, the View Transitions API (native browser page transitions without React Router), Server Islands (Astro 5 — deferred rendering for personalized content in otherwise-static pages), middleware (src/middleware.ts), endpoints (API routes in src/pages/api/), the Vite-powered build, and deployment to static hosts (Netlify, Vercel, Cloudflare Pages, GitHub Pages) or SSR adapters. Use when building any content-focused website — blog, documentation, marketing site, portfolio, e-commerce catalog — especially when the task involves content collections, choosing hydration directives, mixing UI frameworks in one project, or optimizing for Core Web Vitals where Astro's zero-JS-by-default approach differs fundamentally from Next.js / Nuxt / SvelteKit app frameworks.
license: Proprietary. LICENSE.txt has complete terms
---

# Astro 5 — Content-Focused Web Framework (Islands Architecture)

> **Target:** Astro 5.0+ (released November 2024) on Node.js 20+. Astro 5 introduced the **Content Layer API** (replacing the legacy file-based content collections), **Server Islands** (deferred rendering for personalized content in static pages), and the **Vite 6** build tool. Astro's distinctive paradigm: **zero JavaScript by default** — pages render to static HTML at build time, and interactive components ("islands") opt into hydration individually via `client:` directives.

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending an Astro 5 application. Trigger phrases include "Astro", "islands architecture", "content collections", "Content Layer API", "MDX", "client:load", "client:idle", "client:visible", "client:only", "View Transitions", "Server Islands", "Astro DB", "Astro Studio", "@astrojs/react", "@astrojs/vue", "@astrojs/svelte", "@astrojs/preact", "astro:content", "src/pages", "src/content", "src/middleware.ts", "astro.config.mjs", and any reference to `.astro` files or the `astro:*` import namespace.

Do **not** use this skill for:
- **Astro ≤4** — the Content Layer API is Astro 5+. Legacy content collections still work but are deprecated.
- **Next.js / Nuxt / SvelteKit** — these are app frameworks that ship JS by default. Astro is content-first with opt-in JS. Different paradigm. See `vue-3-nuxt`, `svelte-5-sveltekit`, and Next.js skills.
- **Pure static site generators** (Eleventy, Hugo, Jekyll) — Astro has components, hydration, and SSR; static SSGs are simpler but less capable.
- **Single-page apps** (Vite + React, Vite + Vue) — Astro can do SPA-like interactivity but is optimized for multi-page content sites.

Cross-reference: `framework-templates` may have an Astro section; this skill goes deep.

## Quick Start

```bash
# Create a new Astro project
npm create astro@latest my-app
# Prompts: template (Empty / Blog / Docs / Portfolio), TypeScript (yes/recommended), 
#          install deps, init git, VS Code setup

cd my-app
npm install
npm run dev                     # Dev server at http://localhost:4321

# Add a UI framework integration (you can mix multiple in one project)
npx astro add react             # Adds @astrojs/react + React
npx astro add vue               # Adds @astrojs/vue + Vue
npx astro add svelte            # Adds @astrojs/svelte + Svelte
npx astro add tailwind          # Adds @astrojs/tailwind (or use Tailwind 4 Vite plugin)
npx astro add mdx               # Adds @astrojs/mdx for .mdx files
npx astro add sitemap           # Adds @astrojs/sitemap
```

### Key commands

```bash
npm run dev                     # Dev server with HMR
npm run build                   # Production build to dist/
npm run preview                 # Preview the production build
npm run astro check             # TypeScript + Astro template diagnostics
npm run astro check --watch     # Watch mode

npx astro add <integration>     # Add an integration (auto-configures astro.config.mjs)
npx astro sync                  # Generate content collection types (auto-runs on dev/build)
npx astro telemetry disable     # Opt out of telemetry
```

---

## Project Structure (Astro 5 canonical layout)

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
│   ├── components/             # Reusable components (Astro + framework)
│   │   ├── Header.astro
│   │   ├── Footer.astro
│   │   ├── NewsletterForm.tsx  # React island
│   │   └── ThemeToggle.vue     # Vue island
│   ├── content/                # ← Content collections (Markdown/MDX)
│   │   ├── config.ts           # Collection schemas (Zod validation)
│   │   ├── blog/               # Blog posts (.md, .mdx)
│   │   │   ├── hello-world.md
│   │   │   └── second-post.mdx
│   │   └── authors/            # Author entries (.yaml, .json)
│   │       └── alice.yaml
│   ├── styles/                 # Global styles
│   │   └── global.css
│   ├── lib/                    # Utilities
│   │   └── utils.ts
│   └── middleware.ts           # Request middleware (Astro 2.6+)
├── public/                     # Static assets served as-is
│   ├── favicon.svg
│   └── images/
├── astro.config.mjs            # ← THE config file
├── tsconfig.json
├── package.json
└── Dockerfile
```

### `astro.config.mjs` (the canonical config)

```javascript
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

// For SSR (instead of static SSG)
// import node from '@astrojs/node';

export default defineConfig({
  site: 'https://example.com',           // Required for sitemap + canonical URLs
  output: 'static',                       // 'static' (default) or 'server' (SSR) or 'hybrid'

  integrations: [
    react(),                              // React island support
    mdx(),                                // MDX support
    sitemap(),                            // Auto-generates /sitemap.xml
  ],

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

  // Image optimization (astro:assets)
  image: {
    service: {
      entrypoint: 'astro/assets/services/sharp', // or 'squoosh' for smaller bundles
    },
    domains: ['images.example.com'],
    remotePatterns: [{ protocol: 'https' }],
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
        <a href={`/blog/${post.slug}`}>{post.data.title}</a>
        <time>{post.data.publishedAt.toLocaleDateString()}</time>
      </li>
    ))}
  </ul>
</BaseLayout>
```

This `.astro` file renders to pure HTML at build time. **Zero JavaScript** is shipped to the client. The page is instant — no hydration, no React/Vue runtime, no framework overhead. This is why Astro sites score 100/100 on Core Web Vitals by default.

Compare to Next.js, which ships ~80KB of JS even for a static page (React runtime + Next.js runtime + page component).

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

## Content Collections (the Content Layer API)

Astro 5 introduced the **Content Layer API** — a more flexible replacement for the legacy file-based content collections. Content collections are type-safe Markdown/MDX with Zod schema validation.

### Define a collection

```typescript
// src/content.config.ts (Astro 5 — replaces src/content/config.ts)
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  // Load all .md/.mdx files from src/content/blog/
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),

  // Zod schema — validates frontmatter at build time
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

### Author content

```markdown
---
# src/content/blog/hello-world.md
title: "Hello World"
description: "My first Astro blog post"
publishedAt: 2025-01-15
author: "alice"
tags: ["astro", "tutorial"]
draft: false
---

# Hello World

This is my first post. The frontmatter above is validated against the Zod schema
at build time — if I misspell `publishedAt` or use a string instead of a date,
the build fails with a clear error.

MDX is also supported — import React components directly:

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
import { getEntry, render } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map((post) => ({
    params: { slug: post.id },                       // URL parameter
    props: { post },                                 // Pass to the page
  }));
}

const { post } = Astro.props;
const { Content } = await render(post);              // Render Markdown to Astro component
---

<h1>{post.data.title}</h1>
<time>{post.data.publishedAt.toLocaleDateString()}</time>

<Content />                                          <!-- The Markdown body -->
```

### Loading from external sources (Astro 5 Content Layer API)

Astro 5's Content Layer API can load content from anywhere — not just local files:

```typescript
// src/content.config.ts — load from an external API
import { defineCollection, z } from 'astro:content';

const products = defineCollection({
  loader: async () => {
    const response = await fetch('https://api.example.com/products');
    const data = await response.json();
    return data.map((item) => ({
      id: item.slug,
      ...item,
    }));
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

### Advanced: References and Relations between Collections

You can define references to other collections to build relationships:

```typescript
// src/content.config.ts
const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    author: z.string().ref(('authors')), // reference to an author entry's ID
    // OR
    authorRef: z.object({
      id: z.string().ref('authors'),
    }),
  }),
});

const authors = defineCollection({
  loader: glob({ pattern: '**/*.yaml', base: './src/content/authors' }),
  schema: z.object({ name: z.string(), bio: z.string() }),
});
```

Then in a page, you can `getEntry` to resolve the referenced author:

```astro
---
import { getEntry } from 'astro:content';
const post = await getEntry('blog', 'hello-world');
const author = await getEntry('authors', post.data.author);
---
<p>Written by {author.data.name}</p>
```

### Rendering Markdown with custom components

You can pass custom components to the `render` function to override HTML elements:

```astro
---
import { render } from 'astro:content';
import MyLink from '../components/MyLink.astro';
const { Content } = await render(post, {
  components: {
    a: MyLink,   // override <a> tags
    h1: 'h2',    // render h1 as h2
  }
});
---
<Content />
```

---

## Server Islands (Astro 5 — deferred rendering)

Server Islands let you defer rendering of personalized content in an otherwise-static page. The page is served as static HTML immediately, then personalized components stream in.

```astro
---
// src/pages/index.astro — static page with one personalized island
import BaseLayout from '../layouts/BaseLayout.astro';
import UserProfile from '../components/UserProfile.astro';
---

<BaseLayout title="Home">
  <h1>Welcome!</h1>
  <p>This page is static — instant load, zero JS.</p>

  <!-- Server Island — renders later, can be personalized -->
  <UserProfile slot="fallback" server:defer>
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

The page renders instantly as static HTML. The `UserProfile` island is fetched separately (as an HTML fragment) and swapped in when ready. This gives you the performance of static pages with the personalization of SSR — without shipping JS for the personalization logic.

**Use cases for Server Islands:**
- User‑specific greetings or profile widgets
- Real‑time data like notifications or cart count
- A/B testing variants that depend on user cookies
- Ads or dynamic content that must be personalized

**Under the hood:** Astro uses streaming HTML. The main page is served immediately; the island placeholder triggers a sub‑request to the server which renders the island and streams it back, replacing the placeholder. This works without client‑side JS.

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

  .post-card h3 {
    font-size: 1.25rem;
    margin: 0 0 0.5rem;
  }

  .post-card .meta {
    font-size: 0.875rem;
    color: #6b7280;
    margin-top: 0.5rem;
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
- **`set:html`**: inject raw HTML (use carefully — XSS risk; prefer `set:text` for safe text)
- **`<slot />`**: content placeholders with fallback, named slots (`<slot name="footer" />`)

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
    <link rel="canonical" href={new URL(Astro.url.pathname, Astro.site).href} />
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

```astro
---
// src/pages/index.astro
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout title="Home" description="Welcome to my site">
  <h1>Hello, World!</h1>
  <!-- This content is slotted into BaseLayout's <slot /> -->
</BaseLayout>
```

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

## View Transitions (native browser page transitions)

Astro 2.9+ added the View Transitions API — native browser page transitions without a SPA router:

```astro
---
// src/layouts/BaseLayout.astro
import { ClientRouter } from 'astro:transitions';
---

<head>
  <ClientRouter />                                   <!-- Enable View Transitions globally -->
</head>
<body>
  <header>...</header>
  <main><slot /></main>
</body>
```

Now navigating between pages uses the browser's native View Transitions API — smooth fades, slides, or custom animations without writing JS.

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
// src/pages/about.astro
<!-- The image with the same transition:name morphs across pages -->
<img transition:name="hero-image" src="/hero-about.png" alt="Hero" />
```

When the user navigates from `/` to `/about`, the hero image smoothly morphs between the two — powered entirely by the browser's View Transitions API, no JS framework needed.

---

## Middleware

```typescript
// src/middleware.ts
import { defineMiddleware } from 'astro:middleware';

export const onRequest = defineMiddleware(async (context, next) => {
  const { request, url, cookies, locals } = context;

  // Log every request
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
/// <reference path="../.astro/types.d.ts" />

declare namespace App {
  interface Locals {
    user: User | null;
  }
}
```

### Advanced Middleware Patterns

**Redirect based on user agent:**
```typescript
if (request.headers.get('user-agent')?.includes('bot')) {
  return new Response(null, { status: 301, headers: { Location: '/seo-version' } });
}
```

**Rewrite (serve a different page without redirect):**
```typescript
// Rewrite to a different route
return context.rewrite('/other-page');
```

**Error handling middleware:**
```typescript
try {
  return next();
} catch (error) {
  // log error and return a custom error page
  return new Response('Something went wrong', { status: 500 });
}
```

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
  // Validate, save, etc.
  return new Response(JSON.stringify({ id: 1, ...body }), {
    status: 201,
    headers: { 'Content-Type': 'application/json' },
  });
};
```

For SSR mode, API endpoints run on every request. For static mode, they're called at build time (useful for generating data-driven pages).

---

## Image Optimization (`astro:assets`)

Astro has built‑in image optimization similar to Next.js `next/image`.

```astro
---
import { Image } from 'astro:assets';
import heroImage from '../assets/hero.png';
---

<!-- Responsive image with automatic format selection and lazy loading -->
<Image src={heroImage} alt="Hero" width={800} height={400} format="avif" />
```

You can also generate optimized images programmatically:

```typescript
import { getImage } from 'astro:assets';
import myImage from '../assets/photo.jpg';

const optimized = await getImage({
  src: myImage,
  width: 300,
  height: 200,
  format: 'webp',
});
// optimized.src is the URL to the optimized image
```

Configuration in `astro.config.mjs`:

```javascript
image: {
  service: {
    entrypoint: 'astro/assets/services/sharp', // or 'squoosh'
  },
  domains: ['images.unsplash.com'],
  remotePatterns: [{ protocol: 'https', hostname: '**.cdn.com' }],
}
```

---

## Environment Variables

Use `import.meta.env` to access environment variables. Astro automatically loads `.env` files.

```typescript
// In .env
PUBLIC_API_URL=https://api.example.com
SECRET_KEY=abc123
```

```astro
---
// In .astro frontmatter
const apiUrl = import.meta.env.PUBLIC_API_URL;  // accessible in client too
const secret = import.meta.env.SECRET_KEY;      // only on server
---

<script>
  // Client-side script can only access PUBLIC_* variables
  console.log(import.meta.env.PUBLIC_API_URL);
</script>
```

**Important:** Variables starting with `PUBLIC_` are exposed to the client. Never put secrets in public variables.

---

## State Management (with Nanostores)

Astro works well with [Nanostores](https://github.com/nanostores/nanostores) for client-side state that can be shared across islands.

```bash
npm install nanostores
```

```typescript
// src/lib/cartStore.ts
import { atom } from 'nanostores';

export const cartItems = atom([]);
export const addItem = (item) => {
  cartItems.set([...cartItems.get(), item]);
};
```

```astro
---
// In your island component (React example)
import { useStore } from '@nanostores/react';
import { cartItems } from '../lib/cartStore';

function Cart() {
  const items = useStore(cartItems);
  return <div>Cart has {items.length} items</div>;
}
```

This state is scoped to the client and does not require server-side rendering.

---

## Testing

Astro provides `@astrojs/test` (still experimental) but you can also use Vitest with the `astro` environment.

### Setup Vitest:

```bash
npm install -D vitest @vitest/ui @vitejs/plugin-vue @vitejs/plugin-react
```

```javascript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import astro from '@astrojs/vite-plugin-astro';

export default defineConfig({
  plugins: [astro()],
  test: {
    environment: 'jsdom',
    globals: true,
  },
});
```

### Testing content collection queries:

```typescript
import { getCollection } from 'astro:content';
import { describe, expect, test } from 'vitest';

describe('blog collection', () => {
  test('has at least one post', async () => {
    const posts = await getCollection('blog');
    expect(posts.length).toBeGreaterThan(0);
  });
});
```

### Testing components with `@astrojs/test` (experimental):

```typescript
import { render } from '@astrojs/test';
import MyComponent from './MyComponent.astro';

test('renders correctly', async () => {
  const result = await render(MyComponent, { props: { name: 'World' } });
  expect(result.html).toContain('Hello World');
});
```

---

## Performance Optimization

- **Prefetching**: Use `astro:prefetch` to prefetch pages when the user hovers a link.

```astro
---
import { prefetch } from 'astro:prefetch';
---
<a href="/blog" onmouseenter={() => prefetch('/blog')}>Blog</a>
```

- **Lazy loading images**: Use `<img loading="lazy" />` or the `Image` component from `astro:assets` which adds lazy loading automatically.
- **Code splitting**: Astro automatically splits code by route and by island. Each island's JS is loaded only when needed.
- **Caching**: For SSR, use `cache-control` headers in middleware or endpoints.
- **Build analysis**: Run `npm run build -- --verbose` to see bundle sizes.

---

## Deployment

### Static (default — `output: 'static'`)

```bash
npm run build                   # Outputs to dist/
# Deploy dist/ to any static host:
# - Netlify: drag-and-drop or connect repo
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
export default defineConfig({
  output: 'server',             // SSR mode
  adapter: node({ mode: 'standalone' }),
});
```

```bash
npm run build                   # Outputs to dist/server/entry.mjs
node dist/server/entry.mjs      # Run the SSR server
```

### Hybrid mode (Astro 4.12+ — `output: 'static'` with per-page SSR)

```astro
---
// src/pages/dashboard.astro — opt this page into SSR
export const prerender = false;
---
```

With `output: 'static'` (default) and `export const prerender = false` on specific pages, you get the best of both worlds: most pages are static (pre-rendered at build), but personalized pages (dashboard, profile) render on the server per request.

### Environment variables in production

For static builds, environment variables are inlined at build time. For SSR, they are read at runtime. Use `.env.production` for production overrides.

---

## Security Considerations

- **XSS prevention**: Astro automatically escapes HTML content. However, using `set:html` or injecting raw HTML can introduce XSS. Prefer `set:text` for user‑provided text.
- **Content injection**: In MDX, ensure that any user‑provided components are safe. Sanitize HTML if using `set:html`.
- **Authentication**: Use cookies with `httpOnly` and `secure` flags. Use `Astro.cookies` to set them.
- **CSRF**: For API endpoints, validate origin headers or use CSRF tokens.
- **Secrets**: Never hardcode secrets in code. Use environment variables.
- **Headers**: Set security headers (CSP, HSTS, etc.) using middleware or via `astro.config.mjs` with the `security` option.

---

## Advanced Routing

### Dynamic routes with `getStaticPaths`

```astro
---
// src/pages/blog/[slug].astro
export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map((post) => ({
    params: { slug: post.id },
    props: { post },
  }));
}
const { post } = Astro.props;
---
<h1>{post.data.title}</h1>
```

### Pagination

```astro
---
// src/pages/blog/page/[page].astro
export async function getStaticPaths() {
  const posts = await getCollection('blog');
  const perPage = 10;
  const pages = Math.ceil(posts.length / perPage);
  return Array.from({ length: pages }, (_, i) => ({
    params: { page: String(i + 1) },
    props: { posts: posts.slice(i * perPage, (i + 1) * perPage) },
  }));
}
const { posts } = Astro.props;
---
<BlogList posts={posts} />
```

### Catch‑all routes

```astro
// src/pages/[...slug].astro — matches any path not matched by other routes
export function getStaticPaths() { return [] } // if static
```

### Route priority

Astro matches routes in the order they are defined in the file system. More specific routes (like `[slug].astro`) take precedence over catch‑all (`[...slug].astro`).

---

## Top 12 Anti‑Patterns (expanded)

1. **Shipping JS when you don't need it.** The #1 Astro mistake. Use Astro components (`.astro`) for static content and reserve framework components (React/Vue/Svelte) for genuinely interactive elements. If a component doesn't have state or event handlers, it should be `.astro`, not `.tsx`.

2. **`client:load` for everything.** `client:load` hydrates immediately — wasteful for below‑the‑fold components. Use `client:idle` for non‑critical interactivity, `client:visible` for components far down the page, `client:media` for mobile/desktop‑only widgets. Reserve `client:load` for above‑the‑fold critical interactions.

3. **Not using content collections for structured content.** Astro's content collections give you Zod‑validated frontmatter, type‑safe queries, and automatic slug generation. Writing your own Markdown loading logic skips all this. Always use `getCollection()` / `getEntry()` from `astro:content`.

4. **Missing Zod schema validation.** Content collection schemas catch typos and missing fields at build time. Without them, a misspelled `publishedAt` in a Markdown frontmatter becomes a runtime error (or worse, silently renders `undefined`). Always define a `z.object({...})` schema for every collection.

5. **Not using `client:only` for components that use `window`/`document`.** If a React/Vue component references `window` or `document` at module level, SSR will fail with "window is not defined". Use `client:only="react"` to skip SSR — but the component won't render until JS loads (show a placeholder via `slot="fallback"`).

6. **Giant layout files.** Layouts should be the HTML shell (`<html>`, `<head>`, `<body>`, header, footer, `<slot />`). Business logic doesn't belong in layouts. If your layout has `getCollection()` calls or complex conditionals, extract them into components.

7. **Not using View Transitions for multi‑page sites.** View Transitions (`<ClientRouter />`) give SPA‑like navigation with zero JS framework cost. Without them, every page navigation is a full page reload (jarring). Add `<ClientRouter />` to your base layout's `<head>` — it's a one‑line upgrade that dramatically improves perceived performance.

8. **Forgetting `Astro.site` for canonical URLs.** Without `site: 'https://example.com'` in `astro.config.mjs`, `new URL(path, Astro.site)` produces `https://example.com/path` instead of `http://localhost:4321/path` in dev. Set the `site` config always — it's required for sitemaps, RSS feeds, and canonical URLs.

9. **Not using `prerender` for hybrid mode.** With `output: 'static'` (default), you can still have SSR pages via `export const prerender = false`. Don't switch the whole app to `output: 'server'` just because one page needs SSR — use hybrid mode and prerender everything except the personalized pages.

10. **Loading content from external APIs at request time when build time works.** If content doesn't change per‑user, fetch it at build time (in the `.astro` frontmatter or a content collection loader). Don't pay the runtime cost of an API call on every request for content that's the same for everyone. Astro 5's Content Layer API supports loading from external APIs at build time — use it.

11. **Hardcoding environment‑specific URLs.** Use environment variables for API endpoints, base URLs, etc. Avoid hardcoding `localhost` or production domains in code.

12. **Ignoring image optimization.** Unoptimized images can wreck performance. Use `astro:assets` Image component or at least include `width` and `height` attributes to prevent layout shift. Always serve modern formats (AVIF, WebP) when possible.

---

## Troubleshooting Common Errors

| Error | Likely cause | Solution |
|-------|--------------|----------|
| `window is not defined` | A framework component (React/Vue) uses browser APIs at top‑level. | Use `client:only` or move the API usage inside `useEffect`/`onMounted`. |
| `Cannot find module 'astro/loaders'` | Using Astro 4 or older. | Upgrade to Astro 5 (`npm install astro@latest`). |
| `[vite] Cannot find module ...` | Vite cache or missing dependency. | Delete `node_modules/.vite` and restart dev. |
| `Content collection "blog" not found` | Missing `src/content.config.ts` or collection name mismatch. | Ensure `src/content.config.ts` exports the collection with the correct name. |
| `Astro.site` is `http://localhost:4321` in production | `site` config missing. | Set `site` in `astro.config.mjs`. |
| `Image` component fails for remote images | Domain not allowed in `image.domains`. | Add the domain to `image.domains` or `remotePatterns`. |
| `Server Island not rendering` | Missing `server:defer` directive. | Add `server:defer` to the component invocation and provide a fallback slot. |

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for Astro (project onboarding)
- `vue-3-nuxt` — Vue + Nuxt (Astro can use Vue components as islands — the Vue skill covers Vue component authoring)
- `svelte-5-sveltekit` — Svelte + SvelteKit (Astro can use Svelte components as islands)
- `react19-ts6-vite8-tailwindv4-mvp` — React (Astro can use React components as islands)
- `frontend-ui-engineering` — Production‑quality UI build patterns (relevant for Astro components)
- `frontend-design` — Design thinking for web UI
- `api-and-interface-design` — Type contract design (relevant for content collection schemas and API endpoints)
- `api-patterns` — REST API patterns (for Astro API routes)
- `security-and-hardening` — OWASP‑aware hardening (Astro has good XSS defaults via auto‑escaping)
- `clean-code` — General coding standards
- `testing-patterns` — Test pyramid, mocking strategies
- `code-review-checklist` — 12‑category code review checklist

---

## Dependencies

Required (installed via `npm create astro`):
- **Node.js** 20+ (or Bun 1.1+)
- **Astro** 5.0+
- **Vite** 6+ (build tool, bundled with Astro)
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
- `@astrojs/tailwind` — Tailwind CSS integration (or use `@tailwindcss/vite` for Tailwind 4)
- `@astrojs/sitemap` — auto‑generate `/sitemap.xml`
- `@astrojs/rss` — RSS feed generation
- `@astrojs/partytown` — move third‑party scripts to a web worker (improves performance)

### SSR adapters (add via `npx astro add`)

- `@astrojs/node` — self‑hosted Node.js SSR
- `@astrojs/vercel` — Vercel SSR
- `@astrojs/cloudflare` — Cloudflare Pages/Workers SSR
- `@astrojs/netlify` — Netlify SSR
- `@astrojs/deno` — Deno Deploy SSR

### Common additions

- `astro-icon` — icon component (uses Iconify)
- `astro-seo` — SEO meta tags component
- `@astrolib/analytics` — analytics integration
- `astro-pagefind` — client‑side full‑text search (Pagefind)
- `keystatic` + `@keystatic/core` — headless CMS for Astro content collections
- `nanostores` — lightweight client‑side state
