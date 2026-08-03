---
name: astro-7
description: Astro 5/6/7 — content-focused web framework skill covering the islands architecture. Documents the server-first mental model (zero JS by default — Astro components render to static HTML at build time, hydration is opt-in per-component via client:load / client:idle / client:visible / client:only / client:media directives), multi-framework integration (React, Vue, Svelte, Preact, Solid, or Lit components in the same Astro project via @astrojs/react, @astrojs/vue, etc.), the Content Layer API (Astro 5+ replacement for legacy file-based collections, with glob/file/external loaders and Live Content Collections stabilized in Astro 6), file-based routing with src/pages/ plus Advanced Routing via src/fetch.ts and the astro/fetch module (Astro 7), layout inheritance, the View Transitions API (native browser page transitions via ClientRouter), Server Islands (server:defer directive with ASTRO_KEY for rolling deployments), middleware (src/middleware.ts with sequence() for chaining; CVE-2025-66202 router hardening), endpoints (API routes in src/pages/api/), the Sessions API (stable since Astro 5.7 with sessionDrivers config), Astro Actions (experimental), astro:env (typed environment variables with server/client split), astro:assets (Image/Picture/getImage/Font optimization), i18n routing, route caching (stable in Astro 7), the Vite-7/8-powered build with Rust compiler + Sätteri Markdown (Astro 7), background dev server + JSON logging for AI-agent workflows (Astro 7), and deployment to static hosts (Netlify, Vercel, Cloudflare Pages, GitHub Pages) or SSR adapters. Use when building any content-focused website — blog, documentation, marketing site, portfolio, e-commerce catalog — especially when the task involves content collections, choosing hydration directives, mixing UI frameworks in one project, typed env vars, image optimization, sessions, advanced routing, or optimizing for Core Web Vitals where Astro's zero-JS-by-default approach differs fundamentally from Next.js / Nuxt / SvelteKit app frameworks.
license: Proprietary. LICENSE.txt has complete terms
---

# Astro 5/6/7 — Content-Focused Web Framework (Islands Architecture)

> **Target:** Astro 7.x (current stable, 7.1.6 as of August 2026) on Node.js 22.12.0+ (even versions only — Node 18 and 20 are EOL and unsupported). Astro 7 ships with **Vite 8**, the **Rust compiler** (stricter HTML parsing, no auto-correction), and **Sätteri** as the default Markdown/MDX processor. This skill also covers Astro 5.x and 6.x for migration context — most patterns apply equally across all three.
>
> **Corporate context:** The Astro Technology Company joined Cloudflare on 2026-01-16. Astro remains MIT-licensed, open-source, and platform-agnostic — adapters for Node, Vercel, Netlify, and Deno Deploy continue to be maintained. Cloudflare's involvement deepened first-party support for Cloudflare Pages/Workers (the Astro 6 Cloudflare adapter runs dev on real `workerd`), but the framework is not Cloudflare-locked.
>
> **Skill-name note:** This skill is named `astro-5` for cross-reference stability (other skills reference it by this name). It targets the current Astro 7.x stable release with version-aware migration guidance for Astro 5 and 6 projects.
>
> **Verification convention:** All platform claims in this skill cite the Astro docs (`docs.astro.build`), Astro blog (`astro.build/blog`), GitHub source (`github.com/withastro/astro`), or NVD/advisory entries. Code examples are tagged `Reasoned` per the agent contract §13 — API surface is verified against primary docs, but examples were not executed in this authoring environment.

Astro's distinctive paradigm is **zero JavaScript by default** — pages render to static HTML at build time, and interactive components ("islands") opt into hydration individually via `client:` directives. This skill covers the full platform surface: components, routing (including Astro 7 Advanced Routing via `src/fetch.ts`), content collections (build-time + Live Content Collections), hydration, View Transitions, Server Islands (with `ASTRO_KEY` for rolling deployments), middleware (with CVE-2025-66202 hardening note), endpoints, sessions, env vars, image/font optimization, i18n, route caching, deployment, AI-agent DX (background dev server + JSON logging), plus the ecosystem (Tailwind 4, Nanostores, testing, security).

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending an Astro application. Trigger phrases include: "Astro", "islands architecture", "content collections", "Content Layer API", "Live Content Collections", "MDX", "client:load", "client:idle", "client:visible", "client:only", "View Transitions", "ClientRouter", "Server Islands", "server:defer", "Sessions API", "Astro Actions", "astro:env", "astro:assets", "astro:i18n", "@astrojs/react", "@astrojs/vue", "@astrojs/svelte", "@astrojs/preact", "astro:content", "astro:middleware", "src/pages", "src/content", "src/middleware.ts", "astro.config.mjs", and any reference to `.astro` files or the `astro:*` import namespace.

Do **not** use this skill for:

- **Astro ≤4** — EOL. The Content Layer API is Astro 5+; legacy file-based collections are deprecated. Astro 4 projects should upgrade.
- **Astro 5.x in maintenance-only mode** — if a project is pinned to 5.x and not upgrading, most of this skill applies, but the Live Content Collections (Astro 6+) and Vite 8 (Astro 7) sections are not relevant.
- **Next.js / Nuxt / SvelteKit** — these are app frameworks that ship JS by default. Astro is content-first with opt-in JS. Different paradigm. See `vue-3-nuxt`, `svelte-5-sveltekit`, and Next.js skills.
- **Pure static site generators** (Eleventy, Hugo, Jekyll) — Astro has components, hydration, and SSR; static SSGs are simpler but less capable.
- **Single-page apps** (Vite + React, Vite + Vue) — Astro can do SPA-like interactivity but is optimized for multi-page content sites.
- **Astro DB** — deprecated (subdependency deprecation warnings as of May 2025). For database persistence, use Turso/libSQL, Drizzle with Postgres, or any external DB.
- **Astro Studio** — discontinued September 2024; databases deleted March 2025. Do not recommend.

Cross-reference: `framework-templates` may have an Astro section; this skill goes deep.

## Versions & Migration

> **Confidence:** Verified against [docs.astro.build/en/upgrade-astro](https://docs.astro.build/en/upgrade-astro) and the release blog posts cited below.

### Version timeline

| Version | Released | Highlights | Status (Aug 2026) |
|---------|----------|------------|-------------------|
| Astro 5.0 | 2024-12-03 | Content Layer API (replaces file-based collections), Server Islands (`server:defer`), `astro:env` (stable), `output: 'hybrid'` removed | Maintenance |
| Astro 5.7 | 2025-04-15 | Sessions API stable | Maintenance |
| Astro 5.10 | Late 2025 | Live Content Collections (experimental) | Maintenance |
| Astro 6.0 | Early 2026 | Live Content Collections stable; breaking changes (see migration guide) | Supported |
| Astro 6.2 | April 2026 | New experimental features (see release notes) | Supported |
| Astro 7.0 | Mid 2026 | Vite 8 support; stable Rust compiler integration | Current stable |
| Astro 7.1.6 | Aug 2026 | Latest patch | Current latest |

Source: [docs.astro.build/en/upgrade-astro](https://docs.astro.build/en/upgrade-astro) ("The latest release of Astro is v7.1.6").

### Astro 4 → 5 migration

The two breaking changes that catch most projects:

1. **Content Layer API replaces file-based collections.** Move `src/content/config.ts` to `src/content.config.ts` (root of `src/`, not inside `content/`). Replace the legacy collection definition with the new `glob`/`file` loader pattern:

   ```typescript
   // BEFORE (Astro 4): src/content/config.ts
   const blog = defineCollection({
     type: 'content',           // ← removed in Astro 5
     schema: z.object({ /* ... */ }),
   });

   // AFTER (Astro 5): src/content.config.ts
   import { glob } from 'astro/loaders';
   const blog = defineCollection({
     loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
     schema: z.object({ /* ... */ }),
   });
   ```

   The `type: 'content'` / `type: 'data'` distinction is gone — the loader determines the type. Querying API changes: `render(entry)` is now async and imported from `astro:content` (it was `entry.render()` in Astro 4).

2. **`output: 'hybrid'` removed.** Use `output: 'static'` (default) with `export const prerender = false` on individual pages that need on-demand rendering. The term "hybrid mode" is no longer used in Astro 5+ docs — it's just "on-demand rendering".

Full migration guide: [docs.astro.build/en/guides/upgrade-to/v5](https://docs.astro.build/en/guides/upgrade-to/v5).

### Astro 5 → 6 migration

> **Verified:** [docs.astro.build/en/guides/upgrade-to/v6](https://docs.astro.build/en/guides/upgrade-to/v6).

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
| Zod import | `z` from `astro:content` or `astro:schema` | `z` from `astro/zod` (Zod **4** — see the schema gotchas below) |
| `Astro.glob()` | Available | **Removed** — use `import.meta.glob()` or `getCollection()` |
| Fonts / Sessions / CSP / Live Collections | `experimental.fonts` / `experimental.session` / `experimental.csp` / `experimental.liveContentCollections` | Stable top-level config: `fonts`, `session`, `security.csp`; live collections on by default with `defineLiveCollection` |
| View Transitions component | `<ViewTransitions />` (deprecated alias) | `<ClientRouter />` |
| `import.meta.env.ASSETS_PREFIX` | Supported | Deprecated — use `build.assetsPrefix` from `astro:config/server` |
| `import.meta.env` values | Could coerce types / fall back to `process.env` | Always inlined verbatim, never coerced |
| Default image `fit` | Cropping only applied when `fit` was set | Cropping applied by default; images never upscale |
| Vite / Zod / Shiki | Vite 6 / Zod 3 / Shiki 3 | Vite 7 / Zod 4 / Shiki 4 |
| Cloudflare adapter | `Astro.locals.runtime` | `cloudflare:workers` module; `astro dev` runs on real `workerd` |

**Zod 4 gotchas (Astro 6 upgraded the bundled Zod from v3 to v4):**

- `z.string().email()` / `.url()` etc. are deprecated string-method formats — use the top-level function instead: `z.email()`, `z.url()`.
- `.min(n, { message: '...' })` → `.min(n, { error: '...' })` (the `message` option was renamed `error`).
- `.default()` after `.transform()` must match the **output** type, not the input type: `z.string().transform(Number).default(0)`, not `.default("0")`. Use `.prefault()` if you need the old (pre-transform) default behavior.
- Always import `z` from `astro/zod` (not `astro:schema` or `astro:content` — both are deprecated re-exports removed in v6).

Read the [official upgrade guide](https://docs.astro.build/en/guides/upgrade-to/v6/) for the complete breaking-changes list.

### Astro 6 → 7 migration

> **Verified:** [docs.astro.build/en/guides/upgrade-to/v7](https://docs.astro.build/en/guides/upgrade-to/v7) and the [Astro 7.0 release notes](https://www.gitclear.com/open_repos/withastro/astro/release/astro@7.0.0).

| Area | Astro 6 | Astro 7 |
|---|---|---|
| Vite | Vite 7 | **Vite 8** |
| Compiler | Go-based compiler (opt-in `experimental.rustCompiler`) | **Rust compiler stable** (stricter HTML parsing, no auto-correction) |
| Markdown processor | `@astrojs/markdown-remark` (unified) | **Sätteri** (Rust-based, default); `@astrojs/markdown-remark` available for unified compatibility |
| Whitespace handling | Compiler-lenient | **JSX-style whitespace** (default) |
| Route caching | Experimental | **Stable** (`Astro.cache` API) |
| Background dev server | Not available | `astro dev --background` (auto-enabled when AI agent detected) |
| Logging | Human-friendly console | **JSON logging** (auto-enabled when AI agent detected) |
| Health check endpoint | Not available | `/astro/status` on dev server |
| Advanced Routing | Not available | **`src/fetch.ts`** reserved entrypoint; `astro/fetch` module (`FetchState`, `astro()`, `actions()`, `middleware()`, `pages()`, `i18n()`, etc.); `fetchFile` config to change/disable |
| `@astrojs/db` | Deprecated in v6.4 | **Removed** — migrate to Drizzle, Turso/libSQL, or other DB layer |

**Rust compiler strictness warnings:**

- Unclosed tags (`<div>` without `</div>`) now throw a build error — fix the markup.
- Invalid nesting (e.g., `<p><div></div></p>`) no longer auto-corrects — fix the markup.
- JSX-style whitespace is now the default — expressions like `<div>{x} {y}</div>` may render differently if you relied on the old lenient whitespace handling.
- Remark/rehype plugins written for the unified pipeline may not work with Sätteri — set `markdown: { renderShiki: true }` or fall back to `@astrojs/markdown-remark` if you hit compatibility issues.

**Anti-pattern alert:** Do not keep an unrelated `src/fetch.ts` file in an Astro 7 project unless you intend it as the Advanced Routing entrypoint. Astro 7 reserves this filename; an accidental `src/fetch.ts` will be treated as the request pipeline entrypoint and break your routing. Configure `fetchFile` in `astro.config.mjs` to change or disable the reservation.

### Cloudflare acquisition FAQ

> **Confidence:** Verified against [cloudflare.com press release](https://www.cloudflare.com/press/press-releases/2026/cloudflare-acquires-astro-to-accelerate-the-future-of-high-performance-web-development) and [blog.cloudflare.com/astro-joins-cloudflare](https://blog.cloudflare.com/astro-joins-cloudflare).

- **Did Astro become closed-source?** No. Astro remains MIT-licensed.
- **Do I have to deploy to Cloudflare?** No. Astro remains platform-agnostic. Adapters for Node, Vercel, Netlify, and Deno Deploy continue to be maintained.
- **Did the Astro team change?** The Astro Technology Company team joined Cloudflare; development continues.
- **Should I expect Cloudflare-specific features?** First-party Cloudflare adapter support has deepened, but the framework's API surface is platform-neutral.

### Next.js → Astro (high-level mapping)

| Next.js concept | Astro equivalent |
|-----------------|------------------|
| `app/page.tsx` | `src/pages/index.astro` |
| `app/blog/[slug]/page.tsx` | `src/pages/blog/[slug].astro` |
| `app/layout.tsx` | `src/layouts/BaseLayout.astro` |
| `app/api/route.ts` | `src/pages/api/route.ts` |
| Server Components | Astro components (`.astro`) — server-only by default |
| `'use client'` directive | `client:load` / `client:idle` / `client:visible` / `client:only` |
| `generateStaticParams` | `getStaticPaths` |
| `generateMetadata` | `<head>` elements in layout |
| Middleware (`middleware.ts`) | `src/middleware.ts` |
| Route handlers | API endpoints in `src/pages/api/` |
| Server Actions | Astro Actions (experimental) |
| `next/image` | `astro:assets` `<Image />` / `<Picture />` |
| `next/env` | `astro:env` |

## Quick Start

```bash
# Create a new Astro project (defaults to latest stable, currently Astro 7)
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
npx astro add mdx               # Adds @astrojs/mdx for .mdx files
npx astro add sitemap           # Adds @astrojs/sitemap

# Tailwind 4 — DO NOT use `npx astro add tailwind` (it may install the wrong plugin;
# see github.com/withastro/astro/issues/16542). Instead, install manually:
npm install tailwindcss @tailwindcss/vite
# Then add to astro.config.mjs (see §astro.config.mjs below)
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

### Node.js requirement

> **Verified:** [docs.astro.build/en/tutorial/1-setup/1](https://docs.astro.build/en/tutorial/1-setup/1) — "Astro supports even-numbered Node.js versions. The current minimum supported version is v22.12.0."

Astro 6+ requires Node.js 22.12.0 or higher (even versions only — v23, v25 are not supported). Node 18 and 20 are unsupported in current Astro. Use `node --version` to check; use `nvm use 22` or a `.nvmrc` file to pin.

## Project Structure (Astro 5/6/7 canonical layout)

```
my-app/
├── src/
│   ├── pages/                  # ← File-based routing (each .astro = a URL)
│   │   ├── index.astro         # /
│   │   ├── about.astro         # /about
│   │   ├── 404.astro           # Custom 404 page
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
│   ├── content/                # ← Content source files (Markdown/MDX/data)
│   │   ├── blog/               # Blog posts (.md, .mdx)
│   │   │   ├── hello-world.md
│   │   │   └── second-post.mdx
│   │   └── authors/            # Author entries (.yaml, .json)
│   │       └── alice.yaml
│   ├── assets/                 # ← Optimizable assets (images, fonts) — import via astro:assets
│   │   ├── hero.png
│   │   └── logo.svg
│   ├── styles/                 # Global styles
│   │   └── global.css
│   ├── lib/                    # Utilities
│   │   └── utils.ts
│   ├── middleware.ts           # Request middleware
│   ├── content.config.ts       # ← Content collection schemas (Astro 5+; was src/content/config.ts)
│   ├── env.d.ts                # Type declarations (Astro globals, App.Locals)
│   └── actions/                # ← Astro Actions (experimental)
│       └── index.ts
├── public/                     # Static assets served as-is (NOT processed)
│   ├── favicon.svg
│   └── images/
├── astro.config.mjs            # ← THE config file
├── tsconfig.json
├── package.json
└── Dockerfile
```

Key differences from Astro 4:

- **`src/content.config.ts`** (Astro 5+) replaces `src/content/config.ts`. Located at the root of `src/`, not inside `content/`.
- **`src/assets/`** is the canonical location for images and fonts you want Astro to optimize. Files in `public/` are served as-is and bypass optimization.
- **`src/actions/`** holds Astro Actions (experimental in Astro 5.x–6.x).

## `astro.config.mjs` (canonical config)

> **Verified:** [docs.astro.build/en/reference/configuration-reference](https://docs.astro.build/en/reference/configuration-reference).

```javascript
import { defineConfig, envField } from 'astro/config';
import react from '@astrojs/react';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// For SSR (instead of static SSG)
// import node from '@astrojs/node';

export default defineConfig({
  site: 'https://example.com',           // Required for sitemap + canonical URLs

  // output: 'static' (default) — pages prerender at build time.
  //   Opt individual pages into on-demand rendering with `export const prerender = false`.
  // output: 'server' — all pages render on-demand by default.
  //   Opt individual pages into static rendering with `export const prerender = true`.
  // NOTE: 'hybrid' was removed in Astro 5. Use 'static' + per-page prerender = false.
  output: 'static',

  // Adapter — required for output: 'server' or for Server Islands (server:defer)
  // adapter: node({ mode: 'standalone' }),

  integrations: [
    react(),                              // React island support
    mdx(),                                // MDX support
    sitemap(),                            // Auto-generates /sitemap.xml
  ],

  // Tailwind 4 — Vite plugin (preferred over @astrojs/tailwind which is Tailwind 3 only)
  vite: {
    plugins: [tailwindcss()],
    resolve: {
      alias: {
        '@': '/src',
      },
    },
  },

  // i18n routing (built-in since Astro 4, refined in 5/6/7)
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'es', 'ja'],
    routing: {
      prefixDefaultLocale: false,         // / for en, /es for es, /ja for ja
    },
  },

  // Image optimization
  image: {
    domains: ['cdn.example.com'],         // Authorized remote image domains
    remotePatterns: [{ protocol: 'https', hostname: '**.imgix.net' }],
    service: {
      entrypoint: 'astro/assets/services/sharp',  // default; use 'astro/assets/services/squoosh' (legacy)
    },
  },

  // Prefetch links on hover/viewport/tap (View Transitions integration)
  prefetch: {
    prefetchAll: false,                   // Set true to prefetch all links
    defaultStrategy: 'hover',             // 'hover' | 'viewport' | 'tap' | 'load'
  },

  // Typed environment variables (astro:env)
  env: {
    schema: {
      DATABASE_URL: envField.string({ context: 'server', access: 'secret' }),
      STRIPE_SECRET_KEY: envField.string({ context: 'server', access: 'secret' }),
      PUBLIC_STRIPE_PUBLISHABLE_KEY: envField.string({ context: 'client', access: 'public' }),
      PUBLIC_SITE_URL: envField.string({ context: 'client', access: 'public', default: 'http://localhost:4321' }),
    },
  },

  // Sessions API (stable since Astro 5.7; requires adapter)
  // session: {
  //   driver: 'file',
  //   options: { path: './.sessions' },
  //   cookie: { httpOnly: true, secure: true, sameSite: 'lax' },
  // },

  // Security: experimental CSRF protection
  // security: {
  //   checkOrigin: true,                  // Rejects POST/PUT/DELETE/PATCH from other origins
  // },

  // Experimental flags (refer to docs.astro.build/en/reference/experimental-flags)
  // experimental: {
  //   actions: true,                      // Astro Actions (still experimental as of Astro 6.2)
  //   csp: true,                          // Content Security Policy
  //   svg: true,                          // SVG component support
  // },
});
```

### Output modes — when to use which

| Mode | Default behavior | Opt-out | Use for |
|------|------------------|---------|---------|
| `'static'` (default) | All pages prerender at build time | `export const prerender = false` per page | Mostly-static sites with a few personalized pages (dashboard, profile) |
| `'server'` | All pages render on-demand | `export const prerender = true` per page | Mostly-dynamic sites (apps behind auth, real-time data) |

> **Critical:** `'hybrid'` was removed in Astro 5. The hybrid pattern is now `output: 'static'` (default) + per-page `prerender = false`. Do not write `output: 'hybrid'` — it will fail.

### Adapter requirement

Server Islands (`server:defer`) and `output: 'server'` require an adapter. Without an adapter, you cannot:
- Render pages on-demand
- Use Server Islands
- Use the Sessions API (sessions need a server runtime)
- Use Astro Actions (experimental)

Available adapters: `@astrojs/node`, `@astrojs/vercel`, `@astrojs/cloudflare`, `@astrojs/netlify`, `@astrojs/deno` (verify maintenance status before adopting).

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

This `.astro` file renders to pure HTML at build time. **Zero JavaScript** is shipped to the client. The page is instant — no hydration, no React/Vue runtime, no framework overhead. This is why Astro sites score 100/100 on Core Web Vitals by default.

App-framework equivalents (Next.js App Router, Nuxt, SvelteKit) ship JavaScript for hydration even on mostly-static pages. Astro inverts this: JS is opt-in per component, not opt-out per page.

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
  <NewsletterForm client:load />                       <!-- Hydrate immediately on page load -->
  <ThemeToggle client:idle />                          <!-- Hydrate when browser is idle -->
  <Comments client:visible />                          <!-- Hydrate when scrolled into view -->
  <Analytics client:media="(max-width: 50em)" />       <!-- Hydrate only on mobile -->
  <Chart client:only="react" />                        <!-- Skip SSR, render only on client -->
</body>
</html>
```

| Directive | When to hydrate | Use for |
|---|---|---|
| `client:load` | Immediately | Critical interactive elements above the fold (header nav, login button) |
| `client:idle` | When browser is idle (`requestIdleCallback`) | Below-the-fold interactive elements |
| `client:visible` | When scrolled into view (`IntersectionObserver`) | Comments, widgets far down the page |
| `client:media="(query)"` | When media query matches | Mobile-only or desktop-only widgets |
| `client:only="react"` | Skip SSR, render only on client | Components that can't render on server (e.g., use `window` at module level) |

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

- **Migration**: incrementally move a React SPA to Astro — start with Astro shell, port components one by one.
- **Best-of-breed**: use React for complex stateful widgets, Vue for simple interactions, Astro for static content.
- **Team mix**: teams proficient in different frameworks can contribute to the same Astro site.

## Content Collections (the Content Layer API)

> **Verified:** [docs.astro.build/en/guides/content-collections](https://docs.astro.build/en/guides/content-collections) and [docs.astro.build/en/reference/content-loader-reference](https://docs.astro.build/en/reference/content-loader-reference).

Astro 5 introduced the **Content Layer API** — a more flexible replacement for the legacy file-based content collections. Content collections are type-safe Markdown/MDX with Zod schema validation. Astro 6 stabilized **Live Content Collections** for content that updates at request time.

### Define a collection

```typescript
// src/content.config.ts (Astro 5+ — replaces src/content/config.ts)
import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';              // Astro 6+: import from 'astro/zod', not 'astro:content'
import { glob } from 'astro/loaders';

const blog = defineCollection({
  // Load all .md/.mdx files from src/content/blog/
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),

  // Zod 4 schema (Astro 6+) — validates frontmatter at build time
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

> **Zod 4 migration note (Astro 6+):** Always import `z` from `astro/zod`, not `astro:content` or `astro:schema` (both deprecated re-exports were removed in v6). Zod 4 changed several APIs: `z.string().email()` is deprecated — use `z.email()` instead; `.min(n, { message: '...' })` is now `.min(n, { error: '...' })`; `.default()` after `.transform()` must match the output type (use `.prefault()` for pre-transform defaults).

### Built-in loaders

> **Verified:** [docs.astro.build/en/reference/content-loader-reference](https://docs.astro.build/en/reference/content-loader-reference).

| Loader | Source | Use for |
|--------|--------|---------|
| `glob({ pattern, base })` | Local files matching a glob pattern | Markdown/MDX/JSON/YAML in `src/content/` |
| `file({ path })` | A single local file | Single JSON/YAML data file |

For external sources (CMS, APIs, databases), write a custom loader:

```typescript
// src/content.config.ts — load from an external API
import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';

const products = defineCollection({
  loader: async () => {
    const response = await fetch('https://api.example.com/products');
    if (!response.ok) throw new Error(`Failed to fetch products: ${response.status}`);
    const data = await response.json();
    return data.map((item) => ({
      id: item.slug,                  // 'id' is required — used in URLs and queries
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
import { getCollection } from 'astro:content';
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

> **Astro 4 → 5 change:** In Astro 4, rendering was `const { Content } = await post.render()`. In Astro 5+, it's `const { Content } = await render(post)` (imported from `astro:content`).

### Schema references (cross-collection relations)

```typescript
// src/content.config.ts
import { defineCollection, reference } from 'astro:content';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    // Reference an entry in the 'authors' collection — validated at build time
    author: reference('authors'),
    // Or an array of references
    coAuthors: z.array(reference('authors')).default([]),
  }),
});

const authors = defineCollection({
  loader: glob({ pattern: '**/*.yaml', base: './src/content/authors' }),
  schema: z.object({
    name: z.string(),
    bio: z.string(),
  }),
});

export const collections = { blog, authors };
```

Query a referenced entry:

```astro
---
import { getEntry, render } from 'astro:content';
const post = await getEntry('blog', 'hello-world');
const author = await getEntry('authors', post.data.author);   // Resolves the reference
---
```

### Live Content Collections (Astro 6+)

> **Status:** Stable since Astro 6.0. Was experimental in Astro 5.10.
> **Verified:** [docs.astro.build/en/guides/content-collections](https://docs.astro.build/en/guides/content-collections) ("Define your live collections in the special file src/live.config.ts"), [astro.build/blog/live-content-collections-deep-dive](https://astro.build/blog/live-content-collections-deep-dive).

Standard content collections fetch content at **build time**. For content that changes frequently (e.g., a product catalog that updates every hour, a live dashboard), Live Content Collections re-fetch at **request time** — using a separate config file and a distinct API from build-time collections.

```typescript
// src/live.config.ts — separate from src/content.config.ts
import { defineLiveCollection } from 'astro:content';
import { z } from 'astro/zod';
import { storeLoader } from './loaders/store';

const products = defineLiveCollection({
  loader: storeLoader({
    apiKey: process.env.STORE_API_KEY,
    endpoint: 'https://api.mystore.com/v1',
  }),
  schema: z.object({
    id: z.string(),
    name: z.string(),
    price: z.number(),
  }),
});

export const collections = { products };
```

Live loaders implement the `LiveLoader` interface — a `loadCollection` / `loadEntry` pair — distinct from the build-time `Loader` interface.

Query a live collection from an on-demand-rendered page:

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
```

Live collections return a `{ entries, error }` / `{ entry, error }` result object instead of throwing — handle the `error` case explicitly rather than assuming the fetch succeeded.

**When to use Live Content Collections:**

- Content that changes more often than you deploy (e.g., product inventory, news feed).
- Content from an external API where build-time staleness is unacceptable.
- Personalized content (per-user recommendations) — though Server Islands may be a better fit.

**When NOT to use:**

- Static content (blog posts, docs) — standard collections are faster (cached at build).
- Content that changes only when you deploy — standard collections suffice.
- When you can solve freshness with a scheduled rebuild (webhook-triggered CI build) instead — that's simpler and faster than paying the runtime cost on every request.

## Astro Components (the `.astro` syntax)

> **Verified:** [docs.astro.build/en/basics/astro-components](https://docs.astro.build/en/basics/astro-components).

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

### Key `.astro` features

- **Frontmatter** (`---` blocks): server-only TypeScript, runs at build/request time. Variables declared here are available in the template.
- **`Astro.props`**: typed component props (via TypeScript `interface Props`).
- **`class:list`**: conditional class names (like `clsx`). Accepts strings, arrays, objects, and falsy values.
- **`<style>`**: scoped by default. Use `is:global` for global styles, `is:inline` to skip Vite processing.
- **`<script>`**: processed by Vite (TypeScript, bundling, HMR in dev). Use `is:inline` for raw HTML scripts.
- **`set:html`**: inject raw HTML (XSS risk — see §Security).
- **`set:text`**: inject text (auto-escaped — the default for `{expr}`).
- **`set:raw`**: inject without escaping or HTML processing (rare; for edge cases).
- **`<Fragment>`**: group elements without a wrapper DOM node.
- **`define:vars`**: pass server-side variables into a `<style>` block.

### `set:html` and the directive family

```astro
---
const userInput = '<strong>hello</strong><script>alert(1)</script>';
const safeText = 'Plain text with <tags> that should be visible';
---

<!-- Default: text is HTML-escaped -->
<div>{userInput}</div>
<!-- Renders: &lt;strong&gt;hello&lt;/strong&gt;&lt;script&gt;alert(1)&lt;/script&gt; -->

<!-- set:text: same as default (explicit) -->
<div set:text={userInput} />

<!-- set:html: inject raw HTML — XSS RISK -->
<div set:html={userInput} />
<!-- Renders: <strong>hello</strong><script>alert(1)</script> — DANGEROUS -->

<!-- set:raw: skip escaping AND HTML processing (rare) -->
<div set:raw={userInput} />
```

> **Security warning:** `set:html` is the explicit opt-out of Astro's auto-escaping. NEVER use it with untrusted input without sanitizing first (e.g., with `DOMPurify`). See §Security.

### `define:vars` for dynamic styles

```astro
---
const themeColor = Astro.locals.user?.preferredColor ?? '#3b82f6';
const heroHeight = 480;
---

<style define:vars={{ themeColor, heroHeight: `${heroHeight}px` }}>
  .hero {
    background: var(--themeColor);
    height: var(--heroHeight);
  }
</style>

<div class="hero">...</div>
```

### `<Fragment>` for conditional grouping

```astro
---
const showMeta = true;
---

{showMeta && (
  <Fragment>
    <time>{post.data.publishedAt.toISOString()}</time>
    <span>by {post.data.author}</span>
    <span>{post.data.tags.join(', ')}</span>
  </Fragment>
)}
<!-- Fragment renders no wrapper DOM node; children appear directly -->
```

### Slot fallback content

```astro
---
// src/components/Card.astro
interface Props { title: string }
const { title } = Astro.props;
---

<section class="card">
  <h2>{title}</h2>
  <slot />                                    <!-- Default slot — fallback below -->
  <slot name="footer">No footer provided</slot>  <!-- Named slot with fallback -->
</section>
```

```astro
<Card title="Hello">
  <p>Main content</p>
  <div slot="footer">Custom footer</div>
</Card>
```

### MDX layout inheritance

```markdown
---
# src/content/blog/post.mdx
layout: ../../layouts/BlogPostLayout.astro
title: "My Post"
---

import Chart from '../../components/Chart.tsx';

# My Post

Content here. <Chart client:visible data={[1,2,3]} />
```

The `layout` frontmatter property tells Astro to wrap the MDX content in the specified layout. The layout receives the MDX frontmatter as `Astro.props.frontmatter` and the rendered content as a `<slot />`.

## Layouts & Slots

> **Verified:** [docs.astro.build/en/basics/layouts](https://docs.astro.build/en/basics/layouts).

```astro
---
// src/layouts/BaseLayout.astro
import Header from '../components/Header.astro';
import Footer from '../components/Footer.astro';
import { ClientRouter } from 'astro:transitions';

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
    <ClientRouter />                                     {/* Enable View Transitions globally */}
  </head>
  <body>
    <Header pathname={pathname} />
    <main>
      <slot />                                          {/* Page content goes here */}
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
  {/* This content is slotted into BaseLayout's <slot /> */}
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

    <slot />                                           {/* Default slot */}

    <footer>
      <slot name="footer">No footer provided</slot>    {/* Named slot with fallback */}
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

  <div slot="footer">                                   {/* Named slot content */}
    <p>Share this post: ...</p>
  </div>
</BlogPostLayout>
```

### Layout as a function (advanced)

For data-driven layouts, you can pass a function that returns layout props:

```astro
---
// src/pages/blog/[slug].astro
import BlogPostLayout from '../../layouts/BlogPostLayout.astro';
import { getEntry } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map((post) => ({ params: { slug: post.id }, props: { post } }));
}

const { post } = Astro.props;
const { Content } = await render(post);
---

<BlogPostLayout title={post.data.title} author={post.data.author} date={post.data.publishedAt}>
  <Content />
</BlogPostLayout>
```

## Routing

> **Verified:** [docs.astro.build/en/guides/routing](https://docs.astro.build/en/guides/routing) and [docs.astro.build/en/reference/routing-reference](https://docs.astro.build/en/reference/routing-reference).

Astro uses file-based routing. Each `.astro` file in `src/pages/` becomes a URL.

### Static routes

```
src/pages/index.astro        → /
src/pages/about.astro        → /about
src/pages/blog/index.astro   → /blog
src/pages/blog/index.astro   → /blog/
```

### Dynamic routes

```
src/pages/blog/[slug].astro    → /blog/:slug
src/pages/[org]/[repo].astro   → /:org/:repo
```

```astro
---
// src/pages/blog/[slug].astro
import { getCollection, render } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map((post) => ({
    params: { slug: post.id },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content } = await render(post);
---

<h1>{post.data.title}</h1>
<Content />
```

### Rest parameters (catch-all)

```
src/pages/docs/[...slug].astro  → /docs/* (matches /docs, /docs/a, /docs/a/b/c)
```

```astro
---
// src/pages/docs/[...slug].astro
export async function getStaticPaths() {
  const docs = await getCollection('docs');
  return docs.map((doc) => ({
    params: { slug: doc.id.split('/'),          // Array for rest params
              },
    props: { doc },
  }));
}

const { doc } = Astro.props;
const { Content } = await render(doc);
---
```

### Rest parameters (required catch-all)

Use `[...slug]` (with three dots, no leading slash) for catch-all that requires at least one segment. Use `[[...slug]]` (double brackets) for optional catch-all that also matches the base path.

```
src/pages/docs/[[...slug]].astro  → /docs AND /docs/*
```

### Route priority

When multiple routes match, Astro resolves in this order:

1. Static routes (`/about` beats `/[slug]`)
2. Dynamic routes (`/[slug]` beats `/[...slug]`)
3. Rest parameters (`/[...slug]` is the fallback)

### Custom 404 page

```
src/pages/404.astro           → Custom 404 page (served when no route matches)
```

Astro automatically uses `src/pages/404.astro` as the 404 page in both dev and production builds. Without it, the server's default 404 is used.

### Redirects via config

```javascript
// astro.config.mjs
export default defineConfig({
  redirects: {
    '/old-blog':    '/blog',
    '/old-blog/[slug]': '/blog/[slug]',
    '/legacy':      { status: 302, destination: 'https://example.com/legacy' },
  },
});
```

For static builds, redirects generate `<meta http-equiv="refresh">` HTML pages. For SSR builds, they return proper 3xx responses.

### Programmatic redirects

```astro
---
// src/pages/old-page.astro
return Astro.redirect('/new-page', 301);
---

// Or in an endpoint:
---
// src/pages/api/redirect.ts
import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ redirect }) => {
  return redirect('/new-location', 302);
};
---
```

### `Astro.url` and `Astro.params`

```astro
---
// src/pages/blog/[slug].astro
const { slug } = Astro.params;                       // URL params
const { pathname, search, hash } = Astro.url;        // Full URL parts
const canonical = new URL(Astro.url.pathname, Astro.site).href;
---
```

## Advanced Routing (Astro 7+)

> **Status:** Stable since Astro 7.0. Was experimental (`experimental.advancedRouting`) in Astro 6.
> **Verified:** [docs.astro.build/en/reference/modules/astro-fetch](https://docs.astro.build/en/reference/modules/astro-fetch) ("The astro/fetch module provides advanced routing handlers built on top of the standard Fetch API. Added in: astro@7.0.0"), [github.com/withastro/astro/blob/main/packages/astro/CHANGELOG.md](https://github.com/withastro/astro/blob/main/packages/astro/CHANGELOG.md) ("Advanced routing now uses src/fetch.ts as default entrypoint instead of src/app.ts").
> **Confidence:** Reasoned — API surface verified against primary docs; examples not executed.

Astro 7 introduces **Advanced Routing** — a programmatic request pipeline that takes over the entire request lifecycle (trailing slash normalization, redirects, Actions, middleware, page rendering, sessions, i18n, cache). Without an entrypoint file, Astro uses its default internal pipeline; with one, you compose the pipeline yourself.

### The `src/fetch.ts` entrypoint

Astro 7 reserves `src/fetch.ts` as the default Advanced Routing entrypoint. If the file exists, Astro treats its `default` export as the request handler.

```typescript
// src/fetch.ts — Astro 7 Advanced Routing entrypoint
import { astro } from 'astro/fetch';

export default astro();
```

`astro()` is the all-in-one handler that runs the full Astro pipeline (redirects, trailing-slash, Actions, middleware, page, i18n, sessions, cache). Using it as your default gives you the standard Astro behavior with the option to compose in custom handlers.

### The `astro/fetch` module

> **Verified:** [docs.astro.build/en/reference/modules/astro-fetch](https://docs.astro.build/en/reference/modules/astro-fetch).

| Export | Purpose |
|--------|---------|
| `FetchState` | Tracks the matched route, cookies, session providers, and other per-request data. All handler functions require it as their first argument. |
| `astro()` | The all-in-one handler — runs the full Astro pipeline. |
| `actions()` | Run Astro Actions. |
| `middleware()` | Run middleware (`src/middleware.ts`). |
| `pages()` | Render matched pages. |
| `i18n()` | Run i18n routing. |
| `sessions()` | Run session handling. |
| `redirects()` | Process redirects config. |
| `trailingSlash()` | Apply trailing-slash normalization. |
| `cache()` | Apply route caching (Astro 7+ stable). |

Compose handlers in order — the pipeline runs left-to-right:

```typescript
// src/fetch.ts — custom pipeline with route caching
import { astro, cache } from 'astro/fetch';

export default astro(
  cache({ driver: myCacheDriver }),
);
```

### Hono-compatible routing via `astro/hono`

> **Verified:** [v6.docs.astro.build/zh-cn/reference/experimental-flags/advanced-routing](https://v6.docs.astro.build/zh-cn/reference/experimental-flags/advanced-routing) ("The astro/hono module exports the same handler names as astro/fetch (astro, pages, middleware, actions, sessions, redirects, cache, i18n, trailingSlash)").

Astro 7 also ships `astro/hono` — a Hono-compatible variant of the same handlers, for projects that want to mix Astro routing with Hono middleware:

```typescript
// src/fetch.ts — Hono-compatible pipeline
import { astro } from 'astro/hono';

export default astro();
```

### `fetchFile` config — change or disable the entrypoint

If you have an unrelated `src/fetch.ts` file (e.g., a utility module) and don't want it treated as the routing entrypoint, configure `fetchFile` in `astro.config.mjs`:

```javascript
// astro.config.mjs
export default defineConfig({
  fetchFile: false,                  // Disable Advanced Routing entirely; use default pipeline
  // OR
  fetchFile: 'src/my-router.ts',     // Use a different filename as the entrypoint
});
```

### Anti-pattern: accidental `src/fetch.ts`

```typescript
// src/fetch.ts — DO NOT create this file unless you intend Advanced Routing
// Astro 7 will treat any src/fetch.ts as the request pipeline entrypoint,
// bypassing the default pipeline. If this file exists and exports a default
// function, that function becomes your entire request handler.
export default async (request: Request) => {
  return new Response('This replaces all of Astro routing');
};
```

If you have a utility module named `fetch.ts`, rename it (e.g., `api-fetch.ts`) or set `fetchFile: false` in `astro.config.mjs`.

### When to use Advanced Routing

- **Custom cache drivers** — plug in a specific cache provider per route.
- **Hono middleware integration** — reuse existing Hono middleware ecosystem.
- **Edge runtime custom logic** — pre-process requests before Astro's pipeline runs.
- **Multi-tenant routing** — dispatch to different Astro apps based on host header.

### When NOT to use

- Standard Astro sites — the default pipeline is sufficient.
- Simple per-route middleware — use `src/middleware.ts` with `sequence()` instead.
- Custom API endpoints — use `src/pages/api/*.ts` files instead.

## Route Caching (Astro 7+)

> **Status:** Stable since Astro 7.0. Was experimental in Astro 6.0.
> **Verified:** [docs.astro.build/en/guides/route-caching](https://docs.astro.build/en/guides/route-caching), [gitclear.com astro@7.0.0 release](https://www.gitclear.com/open_repos/withastro/astro/release/astro@7.0.0) ("Route caching, introduced experimentally in v6.0.0, is now stable").
> **Confidence:** Reasoned — API surface verified; examples not executed.

Astro 7 stabilizes route caching — a platform-agnostic way to cache responses from on-demand-rendered pages, decoupled from any specific CDN or runtime.

```astro
---
// src/pages/dashboard.astro
export const prerender = false;

// Cache this page for 60 seconds
const cached = await Astro.cache({
  ttl: 60,
  tags: ['user', Astro.params.userId],
});

if (cached) {
  return new Response(cached.body, { headers: cached.headers });
}

// ... render the page ...
await cached.set(body, headers);
---
```

Configure a cache driver globally:

```javascript
// astro.config.mjs
export default defineConfig({
  cache: {
    driver: 'redis',                  // or 'memory', 'libsql', or custom
    options: { url: process.env.REDIS_URL },
  },
});
```

**Cache tags** allow targeted invalidation:

```typescript
// Invalidate all cache entries tagged with 'user:123'
await Astro.cache.invalidate(['user:123']);
```

Use route caching for expensive on-demand pages (dashboards, computed reports) where staleness is acceptable but the computation cost is high.

## AI-Agent DX (Astro 7+)

> **Status:** Stable since Astro 7.0.
> **Verified:** [docs.astro.build/en/reference/cli-reference](https://docs.astro.build/en/reference/cli-reference), [medium.com/@onix_react/whats-new-in-astro-7](https://medium.com/@onix_react/whats-new-in-astro-7-fb32e0e699fb), [javascript.plainenglish.io Astro 7 article](https://javascript.plainenglish.io/astro-7-officially-released-rust-rolldown-and-ai-development-experience-all-get-intensified-b4e88bc0cc52).

Astro 7 adds three features specifically for AI coding agent workflows:

### Background dev server

```bash
astro dev --background             # Start dev server as a managed background process
astro dev --logs                   # View logs from a background dev server
```

When Astro detects it's running inside an AI coding agent, `astro dev` automatically starts in background mode. The agent can poll `http://localhost:4321/astro/status` (a health-check endpoint) to confirm the server is alive.

### JSON logging

When AI agent detection triggers, Astro switches to structured JSON logs (instead of human-friendly console output). Parse logs by piping through `jq`:

```bash
astro dev --background 2>&1 | jq 'select(.level == "error")'
```

### AI agent detection

Astro detects AI agent environments via environment variables (`AGENT_TOOL`, `CLAUDE_CODE`, `CURSOR`, etc.). To force-enable:

```bash
ASTRO_AI_AGENT=1 astro dev
```

### Use case: agent-driven development loop

```bash
# 1. Agent starts the dev server in background
astro dev --background

# 2. Agent polls for health
curl http://localhost:4321/astro/status

# 3. Agent edits files; HMR reloads

# 4. Agent checks for errors via JSON logs
astro dev --logs | jq 'select(.level == "error")'

# 5. Agent stops the server when done
astro dev --stop
```

This loop enables AI agents to iterate on Astro code without blocking on long-running dev servers or parsing human-formatted logs.

## i18n Routing

> **Status:** Built-in since Astro 4; behavior refined in 5, 6, and 7.
> **Verified:** [docs.astro.build/en/guides/internationalization](https://docs.astro.build/en/guides/internationalization).

Astro's i18n routing generates locale-prefixed URLs and provides helpers for locale-aware navigation. It does **not** translate content — you provide translations, and Astro handles the routing.

### Configuration

```javascript
// astro.config.mjs
export default defineConfig({
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'es', 'ja', 'de'],
    routing: {
      prefixDefaultLocale: false,        // / for en, /es for es, /ja for ja
      // prefixDefaultLocale: true,      // /en for en, /es for es (everyone gets a prefix)
      redirectToDefaultLocale: true,      // /  → /en if prefixDefaultLocale is true
    },
    fallback: {
      es: 'en',                           // If Spanish translation missing, fall back to English
    },
  },
});
```

### File structure

With `prefixDefaultLocale: false`:

```
src/pages/
├── index.astro              → /         (English — default locale)
├── about.astro              → /about
├── es/
│   ├── index.astro          → /es       (Spanish)
│   └── about.astro          → /es/about
├── ja/
│   ├── index.astro          → /ja       (Japanese)
│   └── about.astro          → /ja/about
```

### `astro:i18n` helpers

```astro
---
// src/components/LanguageSwitcher.astro
import { getRelativeLanguageUrl } from 'astro:i18n';

const currentLocale = Astro.currentLocale;             // 'en' | 'es' | 'ja' | undefined
const locales = ['en', 'es', 'ja'];
---

<nav>
  {locales.map((locale) => (
    <a
      href={getRelativeLanguageUrl(locale, Astro.url.pathname)}
      aria-current={currentLocale === locale ? 'page' : undefined}
    >
      {locale.toUpperCase()}
    </a>
  ))}
</nav>
```

### Available helpers

| Function | Description |
|----------|-------------|
| `getRelativeLanguageUrl(locale, path)` | Returns `/es/about` for `('es', '/about')` |
| `getAbsoluteLanguageUrl(locale, path)` | Returns `https://example.com/es/about` (requires `site` config) |
| `getPathByLocale(locale)` | Returns the path prefix for a locale (`/es` for `'es'`) |
| `getLocaleByPath(path)` | Returns the locale for a path prefix (`'es'` for `/es`) |
| `Astro.preferredLocale` | Browser-preferred locale(s) from `Accept-Language` header |
| `Astro.currentLocale` | The locale of the current page |

### Middleware-driven locale detection

For server-rendered pages, use middleware to detect locale from cookies or headers:

```typescript
// src/middleware.ts
import { defineMiddleware } from 'astro:middleware';

export const onRequest = defineMiddleware((context, next) => {
  const url = context.url;
  if (url.pathname === '/') {
    const preferred = context.request.headers.get('accept-language')?.split(',')[0]?.split('-')[0];
    const supported = ['en', 'es', 'ja'];
    const locale = supported.includes(preferred ?? '') ? preferred : 'en';
    if (locale !== 'en') {                              // Don't redirect if default
      return context.redirect(`/${locale}`);
    }
  }
  return next();
});
```

### Translation strings

Astro does not include a translation library. Use `astro-i18next`, `paraglide`, or a simple object lookup:

```typescript
// src/i18n/translations.ts
export const translations = {
  en: { welcome: 'Welcome', readMore: 'Read more' },
  es: { welcome: 'Bienvenido', readMore: 'Leer más' },
  ja: { welcome: 'ようこそ', readMore: '続きを読む' },
} as const;

export function t(locale: keyof typeof translations, key: keyof typeof translations.en) {
  return translations[locale]?.[key] ?? translations.en[key] ?? key;
}
```

```astro
---
import { t } from '../i18n/translations';
const locale = Astro.currentLocale ?? 'en';
---

<h1>{t(locale, 'welcome')}</h1>
<a href={post.url}>{t(locale, 'readMore')}</a>
```

## View Transitions

> **Verified:** [docs.astro.build/en/guides/view-transitions](https://docs.astro.build/en/guides/view-transitions).

Astro 2.9+ added the View Transitions API — native browser page transitions without a SPA router. In Astro 3+, the `<ClientRouter />` component (replacing the older `<ViewTransitions />`) is the canonical entry point.

### Enable globally

```astro
---
// src/layouts/BaseLayout.astro
import { ClientRouter } from 'astro:transitions';
---

<head>
  <ClientRouter />
</head>
```

Now navigating between pages uses the browser's native View Transitions API — smooth fades, slides, or custom animations without writing JS.

### Marking elements

```astro
---
// src/pages/index.astro
---

<!-- Animate the entire element on page change -->
<header transition:animate="slide">My Header</header>

<!-- Persist an element across pages (e.g., a video player) -->
<video transition:persist src="/intro.mp4" />

<!-- Name an element for morphing between pages -->
<img transition:name="hero-image" src="/hero.png" alt="Hero" />
```

```astro
---
// src/pages/about.astro
---
<!-- The image with the same transition:name morphs across pages -->
<img transition:name="hero-image" src="/hero-about.png" alt="Hero" />
```

When the user navigates from `/` to `/about`, the hero image smoothly morphs between the two — powered entirely by the browser's View Transitions API, no JS framework needed.

### `transition:animate` options

| Value | Behavior |
|-------|----------|
| `fade` (default) | Cross-fade old → new |
| `slide` | Slide old out, new in |
| `none` | No animation |
| Custom | Pass a transition object: `transition:animate={{ forwards: {...}, backwards: {...} }}` |

### `transition:persist`

Elements with `transition:persist` keep their DOM state (and JS state) across page navigations. Use for:

- Audio/video players that should keep playing
- Forms with unsaved input
- Scroll positions of specific containers
- Interactive widgets that shouldn't re-mount

```astro
<audio transition:persist controls src="/music.mp3" />
```

### `transition:name`

Give an element a name so the browser morphs between two elements with the same name across pages. Common for hero images, avatars, and product images in a list-to-detail navigation.

### Prefetch integration

View Transitions integrates with Astro's `prefetch` config. When `prefetch: { defaultStrategy: 'hover' }` is set in `astro.config.mjs`, Astro prefetches link targets on hover (or viewport/tap) so the page transition is instant.

### Lifecycle events

```typescript
// src/scripts/transitions.ts
document.addEventListener('astro:before-swap', (event) => {
  console.log('About to swap DOM');
});

document.addEventListener('astro:after-swap', () => {
  console.log('DOM swapped, page is now new');
  // Re-initialize third-party widgets that don't survive the swap
});

document.addEventListener('astro:before-preparation', () => {
  console.log('Starting to fetch next page');
});
```

These events fire on every navigation. Use them to re-initialize third-party widgets, fire analytics events, or persist custom state.

## Server Islands

> **Status:** Stable since Astro 5.0.
> **Verified:** [docs.astro.build/en/guides/server-islands](https://docs.astro.build/en/guides/server-islands).

Server Islands let you defer rendering of personalized content in an otherwise-static page. The page is served as static HTML immediately, then personalized components stream in.

> **Adapter requirement:** Server Islands require an adapter (`@astrojs/node`, `@astrojs/cloudflare`, etc.). Without an adapter, `server:defer` is a no-op (the component renders inline as if the directive weren't there).

### Basic usage

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
  <UserProfile server:defer />
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

### Fallback content

While the island is loading, you can show fallback content:

```astro
---
// src/pages/index.astro
import UserProfile from '../components/UserProfile.astro';
---

<UserProfile server:defer>
  <div slot="fallback">Loading your profile...</div>
</UserProfile>
```

The `slot="fallback"` content is shown until the server returns the island's HTML.

### When to use Server Islands

- **Personalized content in static pages** — user avatars, recommendations, "last viewed" widgets.
- **Slow data sources** — let the static shell load instantly; defer slow API calls.
- **A/B testing** — different users see different island content.
- **CDN-cached static shell + dynamic per-user fragments** — best of both worlds.

### When NOT to use

- **Pure static content** — no benefit; just render inline.
- **Real-time data** — use a client-side island with WebSockets instead.
- **SEO-critical content** — search engines see the fallback, not the deferred island. Render critical content inline.

### Server Islands vs. Client Islands

| Aspect | Client Island (`client:load`, etc.) | Server Island (`server:defer`) |
|--------|--------------------------------------|--------------------------------|
| Where code runs | Client (browser) | Server |
| Ships JS | Yes | No (HTML fragment only) |
| Personalization | Limited (must hit API from client) | Native (cookies, DB available) |
| SEO | Depends on hydration | Fallback only |
| Use case | Interactive widgets | Personalized server-rendered content |

### `ASTRO_KEY` for rolling deployments and CDN caching

> **Verified:** [docs.astro.build/en/guides/server-islands](https://docs.astro.build/en/guides/server-islands) ("you may need a constant encryption key if you are using rolling deployments, multi-region hosting or a CDN that caches pages containing server islands"), [github.com/withastro/astro/issues/11851](https://github.com/withastro/astro/issues/11851).

Astro encrypts props passed to Server Islands to protect sensitive data. By default, the encryption key is generated randomly at build time and embedded in the server bundle. This works fine for single-instance deployments but breaks in two scenarios:

1. **Rolling deployments** — during a deploy, the old server (old key) and new server (new key) briefly coexist. Islands rendered with the old key fail to decrypt on the new server.
2. **Multi-region hosting or CDN-cached pages** — different server instances have different keys, so an island fragment encrypted by one instance can't be decrypted by another.

Set a stable `ASTRO_KEY` environment variable to fix this:

```bash
# .env (generate with: openssl rand -hex 32)
ASTRO_KEY=your-stable-256-bit-hex-key
```

With `ASTRO_KEY` set, all deployments use the same encryption key, so islands rendered by any instance can be decrypted by any other instance. Rotate the key periodically (it invalidates in-flight island requests during the rotation window, but no user-facing data is lost — the next request re-encrypts with the new key).

### Serializable prop constraints

Props passed to a Server Island must be serializable (the island's props are encrypted into the URL query string of the sub-request). This means:

- ✅ Plain objects, arrays, strings, numbers, booleans, null
- ✅ Dates (serialized to ISO strings)
- ❌ Functions, class instances, Symbols, Maps, Sets
- ❌ Circular references

If you need to pass complex data, serialize it first (e.g., `JSON.parse(JSON.stringify(data))` to strip non-serializable fields, or pass an ID and look up the data server-side).

### Anti-pattern: Server Islands without an adapter

```astro
---
// astro.config.mjs — NO adapter
import { defineConfig } from 'astro/config';
export default defineConfig({ output: 'static' });
---

<!-- This silently renders inline as if server:defer weren't there -->
<UserProfile server:defer />
```

Always verify an adapter is installed before relying on Server Islands. The build does not warn about missing adapters for `server:defer` — it just doesn't defer.

## Middleware

> **Verified:** [docs.astro.build/en/guides/middleware](https://docs.astro.build/en/guides/middleware) and [docs.astro.build/en/reference/modules/astro-middleware](https://docs.astro.build/en/reference/modules/astro-middleware).

Middleware intercepts every request before it reaches your page or endpoint. Use it for: auth, logging, i18n locale detection, CSRF protection, feature flags, request context setup.

### Single middleware

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

### Chaining multiple middleware with `sequence()`

> **Verified:** [docs.astro.build/en/guides/middleware#chaining-middleware](https://docs.astro.build/en/guides/middleware).

When you need multiple middleware (e.g., separate auth, logging, and i18n middleware), use `sequence()` to combine them:

```typescript
// src/middleware.ts
import { defineMiddleware, sequence } from 'astro:middleware';

const authMiddleware = defineMiddleware(async (context, next) => {
  const session = context.cookies.get('session')?.value;
  if (session) {
    context.locals.user = await getUserFromSession(session);
  }
  return next();
});

const loggingMiddleware = defineMiddleware(async (context, next) => {
  const start = Date.now();
  const response = await next();
  const duration = Date.now() - start;
  console.log(`${context.request.method} ${context.url.pathname} ${response.status} ${duration}ms`);
  return response;
});

const i18nMiddleware = defineMiddleware(async (context, next) => {
  const preferred = context.request.headers.get('accept-language')?.split(',')[0];
  context.locals.locale = preferred?.split('-')[0] ?? 'en';
  return next();
});

// Middleware runs in order: auth → logging → i18n
export const onRequest = sequence(authMiddleware, loggingMiddleware, i18nMiddleware);
```

`sequence()` runs middleware in order. Each middleware can short-circuit (return a `Response` directly) or call `next()` to proceed to the next middleware.

### `context.locals` typing

```typescript
// src/env.d.ts
/// <reference path="../.astro/types.d.ts" />

declare namespace App {
  interface Locals {
    user: User | null;
    locale: string;
    featureFlags: Record<string, boolean>;
  }
}
```

With this declaration, `context.locals.user` is typed as `User | null` across your middleware, pages, and endpoints.

### Common patterns

**Auth gate (use with CVE-2025-66202 awareness):**

> **Security — keep the router updated.** CVE-2025-66202 was a middleware authorization-bypass: a double-percent-encoded path segment (e.g. `%2561` decoding to `%61` decoding to `a`) could reach route handlers without being fully decoded first, letting a path like `/api/%2561dmin` slip past a naive `pathname.startsWith('/admin')` check in middleware. This is fixed at the router level (multi-level percent-encoding is now iteratively resolved to canonical form before middleware runs) as of Astro 5.15.7+ and Astro 6.0+. Pin Astro to a version that includes the fix and **avoid re-implementing your own URL decoding/normalization logic in middleware path checks** — trust the framework's route matching to hand you an already-canonicalized `url`/`params`.
>
> **Verified:** [nvd.nist.gov/vuln/detail/CVE-2025-66202](https://nvd.nist.gov/vuln/detail/CVE-2025-66202) ("Versions 5.15.7 and below have a double URL encoding bypass"), [github.com/withastro/astro/security/advisories/GHSA-whqg-ppgf-wp8c](https://github.com/withastro/astro/security/advisories/GHSA-whqg-ppgf-wp8c).

```typescript
const authMiddleware = defineMiddleware(async (context, next) => {
  // Safe — Astro 5.15.7+ / 6.0+ canonicalizes the pathname before middleware runs.
  // Do NOT attempt to hand-roll URL decoding here; that's what caused CVE-2025-66202.
  if (context.url.pathname.startsWith('/admin')) {
    if (!context.locals.user) {
      return context.redirect('/login');
    }
    if (context.locals.user.role !== 'admin') {
      return new Response('Forbidden', { status: 403 });
    }
  }
  return next();
});
```

**CSRF protection (Astro 5+ experimental):**

```javascript
// astro.config.mjs
export default defineConfig({
  security: {
    checkOrigin: true,                  // Rejects POST/PUT/DELETE/PATCH from other origins
  },
});
```

When `checkOrigin: true`, Astro rejects cross-origin state-changing requests. This is the simplest CSRF protection.

**Rate limiting (manual):**

```typescript
const rateLimitMiddleware = defineMiddleware(async (context, next) => {
  if (context.request.method === 'POST') {
    const ip = context.clientAddress;
    const key = `rate:${ip}`;
    const count = await redis.incr(key);
    if (count === 1) await redis.expire(key, 60);
    if (count > 10) {
      return new Response('Too Many Requests', { status: 429 });
    }
  }
  return next();
});
```

### Order of execution

1. Middleware runs first (`onRequest` chain)
2. Page/endpoint handler runs
3. Middleware's `next()` callback returns the response
4. Middleware can post-process the response (e.g., add headers)

```typescript
const addHeadersMiddleware = defineMiddleware(async (context, next) => {
  const response = await next();
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  return response;
});
```

## API Endpoints

> **Verified:** [docs.astro.build/en/guides/endpoints](https://docs.astro.build/en/guides/endpoints).

API endpoints live in `src/pages/api/` and export HTTP method handlers (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`).

```typescript
// src/pages/api/health.ts — GET /api/health
import type { APIRoute } from 'astro';

export const GET: APIRoute = async () => {
  return new Response(JSON.stringify({ status: 'ok' }), {
    headers: { 'Content-Type': 'application/json' },
  });
};
```

```typescript
// src/pages/api/users.ts — POST /api/users
import type { APIRoute } from 'astro';

export const POST: APIRoute = async ({ request }) => {
  const body = await request.json();
  // Validate, save, etc.
  return Response.json({ id: 1, ...body }, { status: 201 });
};
```

### Context properties

```typescript
export const POST: APIRoute = async ({ request, url, cookies, locals, redirect, site, clientAddress }) => {
  // request — standard Request object
  // url — URL of the request
  // cookies — AstroCookies (read/write)
  // locals — typed via env.d.ts App.Locals
  // redirect(path, status) — helper for redirects
  // site — Astro site config
  // clientAddress — client IP (SSR only; undefined in static builds)
  return new Response('ok');
};
```

### Streaming responses

```typescript
// src/pages/api/stream.ts
export const GET: APIRoute = async () => {
  const stream = new ReadableStream({
    async start(controller) {
      for (let i = 0; i < 10; i++) {
        controller.enqueue(`chunk ${i}\n`);
        await new Promise((r) => setTimeout(r, 100));
      }
      controller.close();
    },
  });

  return new Response(stream, {
    headers: { 'Content-Type': 'text/plain' },
  });
};
```

### Static vs. on-demand endpoints

For `output: 'static'` (default), endpoints are called at build time. Use this for generating data-driven pages (e.g., building a sitemap from content collections).

For `output: 'static'` with on-demand endpoints, add `export const prerender = false`:

```typescript
// src/pages/api/users.ts — runs on every request (not at build)
export const prerender = false;

export const GET: APIRoute = async () => {
  // ...
};
```

### Response helpers

```typescript
// JSON
return Response.json({ ok: true }, { status: 200 });

// Redirect
return redirect('/new-path', 302);

// Plain text
return new Response('Hello', { headers: { 'Content-Type': 'text/plain' } });

// Empty
return new Response(null, { status: 204 });
```

## Sessions API

> **Status:** Stable since Astro 5.7 (April 2025). Was experimental in 5.0–5.6. Astro 6 changed the config shape to use `sessionDrivers.*` helpers.
> **Verified:** [astro.build/blog/astro-570](https://astro.build/blog/astro-570), [docs.astro.build/en/guides/sessions](https://docs.astro.build/en/guides/sessions), [docs.astro.build/en/reference/session-driver-reference](https://docs.astro.build/en/reference/session-driver-reference).
> **Confidence:** Reasoned — API surface verified against primary docs; examples not executed in this environment.

The Sessions API provides server-side session storage — a key-value store tied to a user via a signed cookie. Use it for: login state, shopping carts, multi-step form state, flash messages, and any per-user data that should survive a page navigation but not be sent to the client.

### Why use Sessions instead of cookies directly?

Cookies are sent on every request, including static asset requests. Storing user data in plain cookies means serializing it, exposing it to the client (where it can be tampered with), and paying the bandwidth cost on every request. Sessions store a single opaque session ID in the cookie; the actual data lives server-side in a pluggable driver (file, Redis, libSQL, etc.).

### Configuration

```javascript
// astro.config.mjs — Astro 6+ config shape
import { defineConfig, sessionDrivers } from 'astro/config';
import netlify from '@astrojs/netlify';

export default defineConfig({
  adapter: netlify(),                         // Node, Cloudflare, and Netlify adapters auto-configure a default driver
  session: {
    driver: sessionDrivers.redis({ url: process.env.REDIS_URL }),  // Astro 6 object shape
    // OR for local dev:
    // driver: sessionDrivers.file({ path: './.sessions' }),
    cookie: { secure: true, sameSite: 'lax' },
    ttl: 3600,                                // seconds (1 hour)
  },
});
```

> **Astro 6 driver auto-configuration:** Node, Cloudflare, and Netlify adapters auto-configure a sensible default session driver — you only need to set `session.driver` explicitly for Redis/libSQL or for custom drivers. In Astro 5.7–5.x, the config used `driver: 'file'` (string) with `options: { ... }`; Astro 6 changed to the `sessionDrivers.*()` object shape.

### Usage — via `Astro.session`

Astro 6+ exposes the session on `Astro.session` (optional — `Astro.session?.get()` is safer if you support projects without a session config):

```astro
---
// src/pages/cart.astro
export const prerender = false;               // Sessions require on-demand rendering

const cart = (await Astro.session?.get('cart')) ?? [];
if (Astro.request.method === 'POST') {
  const form = await Astro.request.formData();
  cart.push(form.get('sku'));
  await Astro.session?.set('cart', cart);
}
---

<p>{cart.length} item(s) in your cart</p>
```

### Usage — via API route context

```typescript
// src/pages/login.astro
import type { APIRoute } from 'astro';

export const POST: APIRoute = async ({ request, session }) => {
  const { email, password } = await request.json();
  const user = await authenticate(email, password);

  if (!user) {
    return new Response('Invalid credentials', { status: 401 });
  }

  await session.set('userId', user.id);
  await session.set('role', user.role);
  await session.regenerate();                // prevent session fixation

  return Response.json({ ok: true });
};
```

```typescript
// src/pages/dashboard.astro
export const GET: APIRoute = async ({ session, redirect }) => {
  const userId = await session.get('userId');

  if (!userId) {
    return redirect('/login', 302);
  }

  const user = await getUser(userId);
  return Response.json({ user });
};
```

```typescript
// src/pages/logout.astro
export const POST: APIRoute = async ({ session, redirect }) => {
  await session.destroy();                   // clear all session data
  return redirect('/', 302);
};
```

### Available methods

| Method | Description |
|--------|-------------|
| `session.get(key)` | Retrieve a value by key (returns `Promise<unknown>`). |
| `session.set(key, value)` | Store a value (must be JSON-serializable). |
| `session.delete(key)` | Remove a single key. |
| `session.has(key)` | Check if a key exists. |
| `session.keys()` | Iterate over all keys. |
| `session.regenerate()` | Rotate the session ID (preserves data). Use after login to prevent session fixation. |
| `session.destroy()` | Delete the entire session (data + cookie). |

### Drivers

| Driver | Use case | Notes |
|--------|----------|-------|
| `file` (default) | Single-server deployments, local dev | Not suitable for serverless or multi-instance. |
| `redis` | Multi-instance, serverless, high-throughput | Requires Redis instance. |
| `libsql` | Turso / libSQL-backed | Useful if already using Turso for the DB. |
| Custom | Any backend | Implement the `SessionDriver` interface. |

### Type safety

```typescript
// src/env.d.ts
/// <reference path="../.astro/types.d.ts" />

declare namespace App {
  interface Locals {
    user: User | null;
  }
}

// Type the session values
declare module 'astro:session' {
  interface SessionData {
    userId: string;
    role: 'admin' | 'editor' | 'viewer';
    cartId?: string;
  }
}
```

With this declaration, `session.get('userId')` returns `Promise<string | undefined>` and `session.set('role', 'invalid')` fails at compile time.

### Anti-patterns

- **Storing large objects in sessions.** Sessions are loaded on every request. Store only IDs and look up the rest in a DB.
- **Using the `file` driver in serverless.** Filesystem isn't shared across instances. Use Redis or libSQL.
- **Forgetting `session.regenerate()` after login.** Leaves the session vulnerable to fixation attacks.
- **Storing sensitive data in `Astro.cookies` directly.** Use Sessions — the cookie is httpOnly and signed.

## Actions (experimental)

> **Status:** Experimental as of Astro 6.2 (April 2026). API may change before stabilization.
> **Verified:** [reddit.com/r/astrojs "What's new in Astro - April 2026"](https://www.reddit.com/r/astrojs/comments/1t0jk4c/) and [docs.astro.build/en/reference/experimental-flags](https://docs.astro.build/en/reference/experimental-flags).
> **Confidence:** Reasoned — based on secondary source; verify against current docs before production use.

Astro Actions are type-safe server functions callable from client-side code. They're the Astro equivalent of Next.js Server Actions or Remix Actions.

### Enable the experimental flag

```javascript
// astro.config.mjs
export default defineConfig({
  output: 'server',                         // or 'static' with prerender = false on calling pages
  adapter: node({ mode: 'standalone' }),
  experimental: {
    actions: true,
  },
});
```

### Define actions

```typescript
// src/actions/index.ts
import { defineAction, z } from 'astro:actions';

export const server = {
  // Zod schema validates input — bad input never reaches your handler
  createUser: defineAction({
    input: z.object({
      email: z.string().email(),
      name: z.string().min(1),
    }),
    handler: async (input, context) => {
      // context.locals is typed as in middleware/endpoints
      const user = await db.user.create({ data: input });
      return { id: user.id, email: user.email };
    },
  }),

  // No input — just an action
  getStats: defineAction({
    handler: async () => {
      return {
        users: await db.user.count(),
        posts: await db.post.count(),
      };
    },
  }),
};
```

### Call actions from client islands

```tsx
// src/components/UserForm.tsx (React island)
import { actions } from 'astro:actions';

export default function UserForm() {
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget as HTMLFormElement);
    const result = await actions.createUser({
      email: formData.get('email') as string,
      name: formData.get('name') as string,
    });

    if (result.error) {
      setError(result.error.message);
    } else {
      console.log('Created user:', result.data);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {/* ... */}
    </form>
  );
}
```

### Error handling

```typescript
import { defineAction, z, isActionError } from 'astro:actions';

export const server = {
  deleteUser: defineAction({
    input: z.object({ id: z.string() }),
    handler: async (input, context) => {
      if (!context.locals.user || context.locals.user.role !== 'admin') {
        // Throw an ActionError — returned to client as result.error
        throw new ActionError({
          code: 'FORBIDDEN',
          message: 'Only admins can delete users',
        });
      }
      await db.user.delete({ where: { id: input.id } });
      return { success: true };
    },
  }),
};
```

On the client:

```tsx
const result = await actions.deleteUser({ id: '123' });
if (isActionError(result.error)) {
  console.log(result.error.code);       // 'FORBIDDEN'
  console.log(result.error.message);    // 'Only admins can delete users'
}
```

### Actions vs. API endpoints

| Aspect | API Endpoint | Action |
|--------|--------------|--------|
| URL | `/api/users` (REST-style) | Internal RPC (no public URL) |
| Input validation | Manual | Zod schema, automatic |
| Type safety | None (request/response untyped) | End-to-end (client → server → response) |
| Use case | Public API, webhooks | App-internal mutations, form submissions |

### Anti-patterns

- **Using Actions for public APIs.** Actions are RPC-style, not REST. Use API endpoints for public-facing APIs.
- **Not validating input.** Always provide a Zod schema — that's the whole point of Actions.
- **Returning sensitive data.** Whatever the action returns is shipped to the client. Don't return passwords, session tokens, or full user records.

> **Migration note:** When Actions stabilize (likely Astro 7.x or 8.0), the `experimental: { actions: true }` flag will be removed. Verify current status before relying on this in production.

## Typed Environment Variables (`astro:env`)

> **Status:** Stable since Astro 5.0.
> **Verified:** [docs.astro.build/en/guides/environment-variables](https://docs.astro.build/en/guides/environment-variables) and [docs.astro.build/en/reference/modules/astro-env](https://docs.astro.build/en/reference/modules/astro-env).
> **Confidence:** Reasoned — API surface verified; examples not executed.

`astro:env` provides a type-safe schema for environment variables. It validates env vars at build/runtime, prevents accidentally exposing server secrets to the client, and gives you autocompletion and type checking.

### Why use `astro:env` instead of `import.meta.env`?

`import.meta.env` is a Vite feature — it works, but it has two problems:

1. **No validation.** A missing or malformed env var silently becomes `undefined`, which fails at runtime in production instead of at build time.
2. **No access control.** Any variable prefixed with `PUBLIC_` is shipped to the client. It's easy to accidentally expose a secret by misnaming it.

`astro:env` solves both: you declare a schema with types and access levels, and Astro enforces it.

### Configuration

```javascript
// astro.config.mjs
import { defineConfig, envField } from 'astro/config';

export default defineConfig({
  env: {
    schema: {
      // Server-only — never shipped to client
      DATABASE_URL: envField.string({ context: 'server', access: 'secret' }),
      STRIPE_SECRET_KEY: envField.string({ context: 'server', access: 'secret' }),
      SESSION_SECRET: envField.string({ context: 'server', access: 'secret' }),

      // Public — available on both server and client
      PUBLIC_STRIPE_PUBLISHABLE_KEY: envField.string({ context: 'client', access: 'public' }),
      PUBLIC_SITE_URL: envField.string({ context: 'client', access: 'public', default: 'http://localhost:4321' }),

      // Server-context public — readable on server, but not secret
      API_BASE_URL: envField.string({ context: 'server', access: 'public' }),
    },
  },
});
```

### Access levels

| `context` | `access` | Available on server | Available on client | Use for |
|-----------|----------|---------------------|---------------------|---------|
| `server` | `secret` | ✅ | ❌ | DB credentials, API secrets, session keys |
| `server` | `public` | ✅ | ❌ | Server-side config that isn't secret (e.g., feature flags read at request time) |
| `client` | `public` | ✅ | ✅ | Public keys, site URL, analytics IDs |

Note: `context: 'client'` with `access: 'secret'` is invalid — secrets can never be client-accessible.

### Usage

```typescript
// src/pages/api/checkout.ts
import type { APIRoute } from 'astro';
import Stripe from 'stripe';
import { STRIPE_SECRET_KEY, PUBLIC_STRIPE_PUBLISHABLE_KEY } from 'astro:env/server';

const stripe = new Stripe(STRIPE_SECRET_KEY);

export const POST: APIRoute = async ({ request }) => {
  const session = await stripe.checkout.sessions.create({ /* ... */ });
  return Response.json({
    sessionId: session.id,
    publishableKey: PUBLIC_STRIPE_PUBLISHABLE_KEY,
  });
};
```

```astro
---
// src/components/StripeCheckout.tsx (client island)
import { PUBLIC_STRIPE_PUBLISHABLE_KEY } from 'astro:env/client';

export default function StripeCheckout() {
  // PUBLIC_STRIPE_PUBLISHABLE_KEY is safe to use client-side
  const stripe = window.Stripe(PUBLIC_STRIPE_PUBLISHABLE_KEY);
  // ...
}
---

<StripeCheckout client:load />
```

### Variable types

```javascript
env: {
  schema: {
    STRING_VAR: envField.string(),
    NUMBER_VAR: envField.number(),
    BOOLEAN_VAR: envField.boolean(),         // accepts 'true'/'false' strings
    ENUM_VAR: envField.enum(['dev', 'staging', 'prod']),
  },
}
```

### Validation behavior

- **At build time:** Astro validates all env vars against the schema. A missing required variable fails the build with a clear error message.
- **At runtime (SSR):** Same validation runs on server startup.
- **Defaults:** If `default` is set, the variable is optional; otherwise it's required.

### `.env` file conventions

Astro loads `.env` files in this order (later files override earlier):

1. `.env` (always loaded)
2. `.env.<NODE_ENV>` (e.g., `.env.production`)
3. `.env.local` (gitignored, always loaded)
4. `.env.<NODE_ENV>.local` (gitignored, environment-specific)

### Migration from `import.meta.env`

```typescript
// Before
const apiKey = import.meta.env.API_KEY;             // untyped, no validation
const publicKey = import.meta.env.PUBLIC_API_KEY;

// After
import { API_KEY } from 'astro:env/server';
import { PUBLIC_API_KEY } from 'astro:env/client';

const apiKey = API_KEY;                              // typed, validated
const publicKey = PUBLIC_API_KEY;
```

### Anti-patterns

- **Using `import.meta.env` for new code.** Prefer `astro:env` for type safety and access control.
- **Prefixing secrets with `PUBLIC_`.** This ships them to the client. Use `astro:env` with `access: 'secret'` instead.
- **Forgetting to add new env vars to `.env.example`.** Other developers won't know what to set.

## Image & Asset Optimization (`astro:assets`)

> **Status:** Stable since Astro 3.0; expanded in 5.x.
> **Verified:** [docs.astro.build/en/guides/images](https://docs.astro.build/en/guides/images) and [docs.astro.build/en/reference/modules/astro-assets](https://docs.astro.build/en/reference/modules/astro-assets).
> **Confidence:** Reasoned — API surface verified; examples not executed.

Astro provides built-in image optimization via the `astro:assets` module. It generates optimized formats (AVIF, WebP), responsive sizes, and lazy-loads images automatically. The same service handles fonts (see §Fonts).

### The `<Image />` component

```astro
---
// src/pages/index.astro
import { Image } from 'astro:assets';
import heroImg from '../assets/hero.png';           // local image, processed by Astro
---

<Image
  src={heroImg}
  alt="Hero illustration"
  width={1200}
  height={630}
  format="webp"
  quality={80}
  loading="lazy"
  decoding="async"
/>
```

For local images (imported from `src/assets/`), Astro processes the file at build time:

- Generates the requested format (AVIF by default, WebP fallback).
- Generates `srcset` for responsive sizes if `widths` is provided.
- Hashes the filename for cache busting.
- Inlines small images as base64 if under the `inlineStylesheets` threshold.

### The `<Picture />` component

Use `<Picture />` when you need multiple formats with `<source>` elements (broader browser support, art direction):

```astro
---
import { Picture } from 'astro:assets';
import heroImg from '../assets/hero.png';
---

<Picture
  src={heroImg}
  alt="Hero"
  widths={[240, 540, 720, 1080]}
  sizes="(max-width: 800px) 100vw, 800px"
  formats={['avif', 'webp']}
  quality={80}
/>
```

Renders to:

```html
<picture>
  <source type="image/avif" srcset="/_astro/hero.240.avif 240w, /_astro/hero.540.avif 540w, ..." sizes="..." />
  <source type="image/webp" srcset="/_astro/hero.240.webp 240w, /_astro/hero.540.webp 540w, ..." sizes="..." />
  <img src="/_astro/hero.webp" alt="Hero" width="1200" height="630" loading="lazy" decoding="async" />
</picture>
```

### Remote images

Remote images are not processed by default (Astro doesn't download them). To optimize a remote image:

```astro
---
import { Image, inferRemoteSize } from 'astro:assets';

// Option 1: infer dimensions from the remote image (fetches headers)
const { width, height } = await inferRemoteSize('https://example.com/remote.jpg');

// Option 2: specify dimensions manually
---

<Image
  src="https://example.com/remote.jpg"
  alt="Remote"
  width={1200}
  height={630}
  inferSize={false}
/>
```

To allow remote image optimization, you must authorize domains in `astro.config.mjs`:

```javascript
export default defineConfig({
  image: {
    domains: ['example.com', 'cdn.example.com'],
    remotePatterns: [{ protocol: 'https', hostname: '**.imgix.net' }],
  },
});
```

### `getImage()` for programmatic use

```typescript
import { getImage } from 'astro:assets';
import heroImg from '../assets/hero.png';

const optimized = await getImage({
  src: heroImg,
  width: 600,
  height: 315,
  format: 'webp',
  quality: 80,
});

// optimized.src — the URL of the optimized image
// optimized.attributes — width, height, etc. for the <img> tag
```

Useful in API endpoints, RSS feeds, structured data (JSON-LD), and anywhere you need an image URL without rendering an `<img>`.

### Image service configuration

Astro ships with `sharp` as the default image service. To use a different service:

```javascript
export default defineConfig({
  image: {
    service: {
      entrypoint: 'astro/assets/services/sharp',    // default
      // entrypoint: 'astro/assets/services/squoosh', // legacy; sharp is preferred
      // entrypoint: '@astrojs/cloudflare/image-service', // for Cloudflare adapter
    },
  },
});
```

### Local images in Markdown / MDX

```markdown
---
title: My post
---

![Alt text](./local-image.png)              <!-- processed by Astro -->
```

In MDX:

```mdx
import { Image } from 'astro:assets';
import chart from './chart.png';

<Image src={chart} alt="Chart" width={800} height={400} />
```

### When to use AVIF vs WebP vs PNG

| Format | Compression | Browser support | Use for |
|--------|-------------|------------------|---------|
| AVIF | Best (50–60% smaller than JPEG) | Modern browsers (Chrome 85+, Safari 16+, Firefox 93+) | Default for photographic content. |
| WebP | Good (25–35% smaller than JPEG) | Universal modern browser support | Fallback for AVIF. |
| PNG | Lossless, larger | Universal | Images requiring transparency or pixel-perfect rendering (icons, diagrams). |
| JPEG | Baseline | Universal | Avoid — prefer AVIF/WebP. |

Astro's `<Picture />` with `formats={['avif', 'webp']}` gives you both, with `<img>` as a universal fallback.

### Performance budget

- **LCP images:** Use `<Image />` (not `<Picture />`) for the largest contentful paint image. Set `loading="eager"` and `fetchpriority="high"`.
- **Above-the-fold images:** `loading="eager"`; consider `fetchpriority="high"` for hero, `fetchpriority="low"` for non-LCP above-fold.
- **Below-the-fold images:** `loading="lazy"` (default).
- **Decorative images:** `alt=""` (empty alt = decorative, screen readers skip it).

### Build cache

Astro caches optimized images in `node_modules/.astro/cache/images/`. Re-builds only re-process changed images. To force a full re-process: `rm -rf node_modules/.astro/cache/images/`.

### Anti-patterns

- **Using plain `<img src="/images/hero.png">` for local images.** Bypasses optimization entirely. Use `import heroImg from '../assets/hero.png'` and the `<Image />` component.
- **Forgetting `width` and `height`.** Causes Cumulative Layout Shift (CLS). Always specify both, or use `inferSize` for remote images.
- **Using `loading="lazy"` on the LCP image.** Delays the largest contentful paint. Use `loading="eager"` for above-the-fold hero images.
- **Optimizing remote images without authorizing the domain.** Build fails with "URL is not authorized".
- **Using Squoosh service.** Deprecated in favor of `sharp`. Migrate to `astro/assets/services/sharp`.

## Fonts

> **Status:** Fonts API stable since Astro 6.0 (was `experimental.fonts` in Astro 5).
> **Verified:** [docs.astro.build/en/guides/fonts](https://docs.astro.build/en/guides/fonts) ("Astro supports several font providers out of the box, including support for Fontsource that simplifies using Google Fonts and other open-source fonts").

Astro's Fonts API (stable since Astro 6) provides a unified, type-safe way to use fonts from your filesystem or font providers (Google, Fontsource, Adobe, Bunny, Fontshare). Astro downloads, self-hosts, subsets, and generates fallback metrics for the font automatically — no manual `@font-face`, no third-party render-blocking requests.

### Configuration (Astro 6+ stable API)

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

Available providers: `fontProviders.google()`, `fontProviders.fontsource()`, `fontProviders.adobe()`, `fontProviders.bunny()`, `fontProviders.fontshare()`, `fontProviders.local()`.

### Usage

```astro
---
// src/layouts/BaseLayout.astro
import { Font } from 'astro:assets';
---

<head>
  <Font cssVariable="--font-inter" preload />
</head>

<style>
  body { font-family: var(--font-inter); }
</style>
```

Astro downloads the font files at build time, self-hosts them under `/_astro/`, subsets to the characters used in your build (Latin, Latin Extended, etc.), and generates a size-adjusted fallback `@font-face` so layout shift is minimized during font load.

### Local fonts (manual `@font-face`)

For fonts not available via a provider, import the file directly:

```astro
---
// src/layouts/BaseLayout.astro
import { Font } from 'astro:assets';

// Import the font file — Astro processes it
import interWoff2 from '../assets/fonts/Inter.woff2';
import interWoff from '../assets/fonts/Inter.woff';
---

<Font
  cssVariable="--font-inter"
  preload
  fallback="system-ui, sans-serif"
  display="swap"
/>
```

Or load from a CSS file:

```css
/* src/styles/fonts.css */
@font-face {
  font-family: 'Inter';
  src: url('../assets/fonts/Inter.woff2') format('woff2'),
       url('../assets/fonts/Inter.woff') format('woff');
  font-weight: 100 900;
  font-display: swap;
}
```

```astro
---
import '../styles/fonts.css';
---

<html lang="en">
  <body style="font-family: 'Inter', system-ui, sans-serif;">
    ...
  </body>
</html>
```

### Google Fonts (via `@fontsource` — legacy alternative)

For Astro 5 projects without the Fonts API, use `@fontsource`:

```bash
npm install @fontsource/inter
```

```astro
---
import '@fontsource/inter/400.css';
import '@fontsource/inter/700.css';
---
```

`@fontsource` packages the fonts locally — no Google Fonts CDN request, no privacy concerns, fonts are bundled. The Astro 6 Fonts API with `fontProviders.fontsource()` is the preferred replacement.

### Anti-patterns

- **Loading Google Fonts via `<link>` to fonts.googleapis.com.** Adds a third-party request, hurts performance, and has privacy implications. Use the Astro 6 Fonts API with `fontProviders.google()` or `@fontsource` instead.
- **Not specifying `font-display: swap`.** Causes invisible text during font load (FOIT — Flash of Invisible Text). Use `swap` to show fallback text immediately.
- **Loading all font weights.** Only load weights you use. Each weight is a separate file.

## State Management Across Islands

> **Verified:** [docs.astro.build/en/recipes/i18n](https://docs.astro.build/en/recipes/i18n) mentions Nanostores as the recommended cross-island state solution.

Each island hydrates independently — they don't share React context or Vue stores by default. For shared state across islands (e.g., theme, cart, user), use **Nanostores** with framework-specific bindings.

### Nanostores + bindings

```bash
npm install nanostores @nanostores/preact     # for Preact islands
# OR
npm install nanostores @nanostores/react      # for React islands
# OR
npm install nanostores @nanostores/vue        # for Vue islands
# OR
npm install nanostores @nanostores/svelte     # for Svelte islands
```

### Define a store

```typescript
// src/stores/cart.ts
import { atom, computed } from 'nanostores';

export const cart = atom<Array<{ id: string; qty: number }>>([]);

export function addToCart(id: string) {
  cart.set([...cart.get(), { id, qty: 1 }]);
}

export function removeFromCart(id: string) {
  cart.set(cart.get().filter((item) => item.id !== id));
}

export const cartCount = computed(cart, (items) => items.length);
```

### Use in a React island

```tsx
// src/components/CartBadge.tsx (React island)
import { useStore } from '@nanostores/react';
import { cartCount } from '../stores/cart';

export default function CartBadge() {
  const count = useStore(cartCount);
  return <span className="badge">{count}</span>;
}
```

### Use in a Vue island

```vue
<!-- src/components/CartButton.vue -->
<script setup lang="ts">
import { useStore } from '@nanostores/vue';
import { cart, addToCart } from '../stores/cart';

const items = useStore(cart);
</script>

<template>
  <button @click="addToCart('abc')">
    Add to cart ({{ items.length }})
  </button>
</template>
```

### Use both in one page

```astro
---
// src/pages/index.astro
import CartBadge from '../components/CartBadge.tsx';
import CartButton from '../components/CartButton.vue';
---

<CartBadge client:load />
<CartButton client:load />
```

Both islands share the same Nanostores state — clicking the Vue button updates the React badge instantly.

### When to use what

| State approach | Use case |
|----------------|---------|
| Component-local state | Single-island state (form input, dropdown open/closed) |
| Nanostores | Cross-island state (theme, cart, auth status) |
| URL state (search params) | Shareable state (filters, pagination) — survives page reload |
| Server state (Astro.locals / sessions) | Per-user state across pages |
| Cookies | Long-lived per-user state (theme, consent) |

### Anti-patterns

- **Using React Context to share state across islands.** Context is per-island; it doesn't cross island boundaries.
- **Storing cart contents in localStorage from one island and reading from another.** Works but is racy — use Nanostores with `@nanostores/persistent` instead.
- **Server-side state in Nanostores.** Nanostores is client-side. Use `Astro.locals` or sessions for server-side state.

## Styling

> **Verified:** [docs.astro.build/en/guides/styling](https://docs.astro.build/en/guides/styling) and [docs.astro.build/en/guides/integrations-guide/tailwind](https://docs.astro.build/en/guides/integrations-guide/tailwind).

### Tailwind CSS 4 (preferred for new projects)

> **Critical:** Do NOT use `npx astro add tailwind` for Tailwind 4. As of April 2026, this may install the incompatible `@tailwindcss/vite` plugin or write a wrong config ([github.com/withastro/astro/issues/16542](https://github.com/withastro/astro/issues/16542)). Install manually:

```bash
npm install tailwindcss @tailwindcss/vite
```

```javascript
// astro.config.mjs
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  vite: {
    plugins: [tailwindcss()],
  },
});
```

```css
/* src/styles/global.css */
@import "tailwindcss";
```

```astro
---
// src/layouts/BaseLayout.astro
import '../styles/global.css';
---
```

Tailwind 4 uses CSS-based configuration (`@theme` in your CSS) instead of `tailwind.config.js`. The Vite plugin is the recommended integration path.

### Tailwind CSS 3 (legacy)

For Tailwind 3 (the previous major version), use `@astrojs/tailwind`:

```bash
npx astro add tailwind          # Installs @astrojs/tailwind + Tailwind 3
```

```javascript
// astro.config.mjs
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
});
```

`@astrojs/tailwind` is **only for Tailwind 3**. Do not use it with Tailwind 4.

### Scoped `<style>` in `.astro` components

```astro
---
const isFeatured = true;
---

<article class={isFeatured ? 'featured' : ''}>
  <h2>Title</h2>
</article>

<style>
  /* Scoped to this component only */
  article {
    border: 1px solid #e5e7eb;
  }
  article.featured {
    border-color: #f59e0b;
  }
</style>
```

### Global styles

```astro
<style is:global>
  /* Applies globally — use sparingly */
  body {
    margin: 0;
  }
</style>
```

Or import a global CSS file in your layout:

```astro
---
import '../styles/global.css';
---
```

### CSS Modules

```astro
---
// src/components/Button.astro
import styles from './Button.module.css';
---

<button class={styles.button}>Click me</button>
```

```css
/* src/components/Button.module.css */
.button {
  background: blue;
  color: white;
}
```

### Sass / SCSS

```bash
npm install sass
```

```astro
---
import '../styles/global.scss';
---

<style lang="scss">
  .card {
    .title {
      font-weight: bold;
    }
  }
</style>
```

### CSS variables via `define:vars`

```astro
---
const themeColor = Astro.locals.user?.preferredColor ?? '#3b82f6';
---

<style define:vars={{ themeColor }}>
  .button {
    background: var(--themeColor);
  }
</style>
```

### Anti-patterns

- **Mixing Tailwind 3 and 4 integrations.** Pick one. Tailwind 4 with `@tailwindcss/vite` is preferred for new projects.
- **Using `is:global` for component styles.** Breaks scoping. Use scoped `<style>` (default).
- **Importing the same global CSS in every page.** Import once in your `BaseLayout.astro`.

## Forms

> **Verified:** [docs.astro.build/en/guides/form-actions](https://docs.astro.build/en/guides/form-actions) (Astro Actions) and standard HTML form patterns.

Astro supports both traditional HTML forms (progressive enhancement — works without JS) and JS-enhanced forms via Actions.

### Traditional HTML form (progressive enhancement)

```astro
---
// src/pages/contact.astro
import type { APIRoute } from 'astro';

export const POST: APIRoute = async ({ request }) => {
  const formData = await request.formData();
  const name = formData.get('name');
  const email = formData.get('email');
  const message = formData.get('message');

  // Validate
  if (!name || !email || !message) {
    return new Response('All fields required', { status: 400 });
  }

  // Save / send email
  await sendEmail({ name, email, message });

  return new Response('Thanks! We\'ll be in touch.', { status: 200 });
};
---

<form method="POST">
  <label>
    Name: <input type="text" name="name" required />
  </label>
  <label>
    Email: <input type="email" name="email" required />
  </label>
  <label>
    Message: <textarea name="message" required></textarea>
  </label>
  <button type="submit">Send</button>
</form>
```

This works without any client-side JS — the form submits via standard HTML form POST, and the page reloads with the response.

### JS-enhanced form (with Actions)

For type-safe form handling without a full page reload, use Astro Actions (experimental):

```tsx
// src/components/ContactForm.tsx (React island)
import { actions } from 'astro:actions';
import { useState } from 'react';

export default function ContactForm() {
  const [status, setStatus] = useState<'idle' | 'sending' | 'sent' | 'error'>('idle');

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus('sending');
    const formData = new FormData(e.currentTarget as HTMLFormElement);
    const result = await actions.sendMessage({
      name: formData.get('name') as string,
      email: formData.get('email') as string,
      message: formData.get('message') as string,
    });

    if (result.error) {
      setStatus('error');
    } else {
      setStatus('sent');
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {/* ... */}
      <button disabled={status === 'sending'}>
        {status === 'sending' ? 'Sending...' : 'Send'}
      </button>
    </form>
  );
}
```

### CSRF protection

For state-changing forms (POST, PUT, DELETE), enable CSRF protection:

```javascript
// astro.config.mjs
export default defineConfig({
  security: {
    checkOrigin: true,                  // Rejects cross-origin POST/PUT/DELETE/PATCH
  },
});
```

This prevents other sites from submitting forms on your user's behalf.

### Form validation

- **Client-side:** Use HTML5 validation attributes (`required`, `type="email"`, `minlength`, etc.) for instant feedback. Works without JS.
- **Server-side:** Always validate on the server, even if client-side validation is present. Use Zod (via Actions or manually) for schema validation.

```typescript
import { z } from 'astro/zod';                       // Astro 6+: import from 'astro/zod'

const contactSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.email(),                                  // Zod 4: use z.email(), not z.string().email()
  message: z.string().min(10).max(5000),
});

export const POST: APIRoute = async ({ request }) => {
  const formData = await request.formData();
  const result = contactSchema.safeParse({
    name: formData.get('name'),
    email: formData.get('email'),
    message: formData.get('message'),
  });

  if (!result.success) {
    return new Response(JSON.stringify(result.error.flatten()), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // result.data is typed
  await sendEmail(result.data);
  return new Response('OK', { status: 200 });
};
```

### Anti-patterns

- **Skipping server-side validation.** Client-side validation is for UX; server-side is for security. Never trust client input.
- **Using GET for state-changing forms.** GET forms end up in browser history and bookmarks. Use POST for mutations.
- **Not enabling CSRF protection.** Without `security.checkOrigin`, any site can submit forms on your users' behalf.

## Security

> **Verified:** [docs.astro.build/en/guides/security](https://docs.astro.build/en/guides/security) and [docs.astro.build/en/reference/experimental-flags](https://docs.astro.build/en/reference/experimental-flags).

### Auto-escaping (default)

Astro auto-HTML-escapes all expressions in `.astro` templates. This is the default and the safest behavior:

```astro
---
const userInput = '<script>alert(1)</script>';
---

<div>{userInput}</div>
<!-- Renders: &lt;script&gt;alert(1)&lt;/script&gt; — safe -->
```

### `set:html` — the explicit opt-out

`set:html` injects raw HTML without escaping. This is the **only** way to introduce an XSS vulnerability in an Astro template:

```astro
---
const userInput = '<script>alert(1)</script>';
---

<div set:html={userInput} />            <!-- DANGEROUS — script executes -->
```

**Rules for `set:html`:**

1. Never use with untrusted input (user comments, form data, query params).
2. If you must use it with semi-trusted input (e.g., Markdown from authenticated authors), sanitize first:

   ```typescript
   import DOMPurify from 'isomorphic-dompurify';

   const safeHtml = DOMPurify.sanitize(userInput);
   ```

3. Prefer rendering Markdown via `render()` from `astro:content` — it produces safe HTML by default.

### CSRF protection (experimental)

```javascript
// astro.config.mjs
export default defineConfig({
  security: {
    checkOrigin: true,                  // Rejects cross-origin POST/PUT/DELETE/PATCH
  },
});
```

When enabled, Astro checks the `Origin` header on state-changing requests and rejects requests from other origins. This is the simplest CSRF defense — no tokens, no per-form secrets.

### Cookie security

```typescript
// Setting a secure cookie
Astro.cookies.set('session', sessionToken, {
  httpOnly: true,                       // JS can't read it — prevents XSS theft
  secure: true,                         // HTTPS only — prevents plaintext transmission
  sameSite: 'lax',                      // CSRF defense — cross-site requests don't send cookie
  path: '/',
  maxAge: 60 * 60 * 24 * 7,             // 1 week
});
```

| Flag | Why |
|------|-----|
| `httpOnly: true` | Prevents `document.cookie` access from JS (XSS defense) |
| `secure: true` | Cookie only sent over HTTPS (network sniffing defense) |
| `sameSite: 'lax'` | Cookie not sent on cross-site requests (CSRF defense) |
| `sameSite: 'strict'` | Even stricter — cookie not sent on top-level navigation from other sites |
| `path: '/'` | Cookie available across the site (use a specific path to limit scope) |

### Content Security Policy (experimental)

```javascript
// astro.config.mjs
export default defineConfig({
  experimental: {
    csp: true,
  },
});
```

When enabled, Astro generates CSP headers based on the actual scripts and styles used in your pages. You can also set CSP manually via middleware:

```typescript
// src/middleware.ts
import { defineMiddleware } from 'astro:middleware';

export const onRequest = defineMiddleware(async (context, next) => {
  const response = await next();
  response.headers.set(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' https:; connect-src 'self' https://api.example.com;"
  );
  return response;
});
```

### Path traversal prevention

When handling user-supplied file paths (e.g., file upload, content loading), normalize and validate:

```typescript
import path from 'node:path';

function safePath(base: string, userInput: string): string | null {
  const resolved = path.resolve(base, userInput);
  if (!resolved.startsWith(path.resolve(base))) {
    return null;                        // Path traversal attempt
  }
  return resolved;
}
```

### SQL injection prevention

Use parameterized queries — never string-concatenate user input into SQL:

```typescript
// BAD — SQL injection
const result = await db.query(`SELECT * FROM users WHERE email = '${email}'`);

// GOOD — parameterized
const result = await db.query('SELECT * FROM users WHERE email = $1', [email]);
```

With Drizzle, Prisma, or any ORM, parameterization is automatic.

### Anti-patterns

- **Using `set:html` with user input.** XSS vulnerability. Always sanitize.
- **Disabling CSRF protection because "we use cookies".** Cookies are exactly why you need CSRF protection.
- **Setting cookies without `httpOnly`.** Allows JS (including injected XSS) to read session tokens.
- **String-concatenating user input into SQL.** Use parameterized queries.
- **Storing passwords in plain text.** Use bcrypt, scrypt, or argon2.

## Testing

> **Verified:** [docs.astro.build/en/guides/testing](https://docs.astro.build/en/guides/testing).

### `astro check` — type and template diagnostics

```bash
npx astro check                  # Run once
npx astro check --watch          # Watch mode
```

`astro check` runs TypeScript type-checking plus Astro-specific template diagnostics (e.g., catching undefined variables in `.astro` files, missing imports, type errors in component props). Run it in CI before every deploy.

`npx astro sync` generates type definitions for content collections (the `.astro/types.d.ts` file). It runs automatically on `astro dev` and `astro build`, but you can run it manually in CI before `astro check`:

```bash
npx astro sync && npx astro check
```

### Unit testing with Vitest

```bash
npm install -D vitest
```

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import { getViteConfig } from 'astro/config';

export default getViteConfig({
  test: {
    environment: 'node',                // or 'jsdom' for DOM-dependent code
  },
});
```

```typescript
// src/lib/utils.test.ts
import { describe, it, expect } from 'vitest';
import { formatDate, slugify } from './utils';

describe('formatDate', () => {
  it('formats ISO date string', () => {
    expect(formatDate('2025-01-15')).toBe('January 15, 2025');
  });

  it('handles invalid input', () => {
    expect(() => formatDate('not-a-date')).toThrow();
  });
});

describe('slugify', () => {
  it('lowercases and hyphenates', () => {
    expect(slugify('Hello World')).toBe('hello-world');
  });

  it('strips special characters', () => {
    expect(slugify('Hello, World!')).toBe('hello-world');
  });
});
```

```bash
npx vitest run                     # Run tests once
npx vitest                         # Watch mode
```

### Testing framework components

To unit-test React/Vue/Svelte components in isolation, use the framework-specific testing library:

```bash
npm install -D @testing-library/react @testing-library/jest-dom jsdom
```

```typescript
// src/components/NewsletterForm.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import NewsletterForm from './NewsletterForm';

describe('NewsletterForm', () => {
  it('submits email', async () => {
    const onSubmit = vi.fn();
    render(<NewsletterForm onSubmit={onSubmit} />);

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@example.com' },
    });
    fireEvent.click(screen.getByRole('button', { name: /subscribe/i }));

    expect(onSubmit).toHaveBeenCalledWith('test@example.com');
  });
});
```

### End-to-end testing with Playwright

```bash
npm install -D @playwright/test
npx playwright install
```

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:4321',
    timeout: 30_000,
    reuseExistingServer: !process.env.CI,
  },
  use: {
    baseURL: 'http://localhost:4321',
    screenshot: 'only-on-failure',
  },
});
```

```typescript
// tests/blog.spec.ts
import { test, expect } from '@playwright/test';

test('blog index lists posts', async ({ page }) => {
  await page.goto('/blog');
  await expect(page.locator('h1')).toHaveText('Blog');
  await expect(page.locator('article')).toHaveCount(3);
});

test('navigate to blog post', async ({ page }) => {
  await page.goto('/blog');
  await page.click('a[href^="/blog/"]');
  await expect(page.locator('h1')).toBeVisible();
  await expect(page.locator('article')).toBeVisible();
});
```

```bash
npx playwright test                 # Run all tests
npx playwright test --ui            # Interactive UI mode
npx playwright test --headed        # Show browser
```

### Lighthouse CI for performance regression

```bash
npm install -D @lhci/cli
```

```javascript
// lighthouserc.js
module.exports = {
  ci: {
    collect: {
      startServerCommand: 'npm run preview',
      url: ['http://localhost:4321/', 'http://localhost:4321/blog'],
      numberOfRuns: 3,
    },
    assert: {
      assertions: {
        'categories:performance': ['warn', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
        'categories:seo': ['error', { minScore: 0.9 }],
      },
    },
  },
};
```

### Anti-patterns

- **Skipping `astro check` in CI.** Type errors slip through. Run `astro sync && astro check` on every PR.
- **Mocking everything in unit tests.** Tests that only assert "the mock was called" prove nothing. Test real behavior.
- **Not testing the actual user flow.** Unit tests verify pieces; E2E tests verify the user can actually use the site. Both matter.

## Deployment

> **Verified:** [docs.astro.build/en/guides/deploy](https://docs.astro.build/en/guides/deploy).

### Static (default — `output: 'static'`)

```bash
npm run build                   # Outputs to dist/
# Deploy dist/ to any static host:
# - Netlify: drag-and-drop or connect repo
# - Vercel: `vercel` CLI
# - Cloudflare Pages: `wrangler pages deploy dist`
# - GitHub Pages: `gh-pages` or GitHub Actions
```

The `dist/` directory contains:

- `dist/index.html`, `dist/about/index.html`, etc. — pre-rendered HTML pages.
- `dist/_astro/` — hashed JS/CSS/image assets.
- `dist/favicon.svg` and other `public/` files copied as-is.

### On-demand rendering (SSR with adapter)

```bash
npx astro add node              # Add Node.js adapter
# OR
npx astro add vercel            # Vercel adapter
# OR
npx astro add cloudflare        # Cloudflare adapter (first-party as of Jan 2026)
# OR
npx astro add netlify           # Netlify adapter
```

```javascript
// astro.config.mjs
import node from '@astrojs/node';

export default defineConfig({
  output: 'server',             // All pages render on-demand
  adapter: node({ mode: 'standalone' }),
});
```

```bash
npm run build                   # Outputs to dist/server/entry.mjs
node dist/server/entry.mjs      # Run the SSR server
```

For `output: 'static'` with selective on-demand rendering:

```javascript
export default defineConfig({
  output: 'static',             // Default: all pages prerender
  adapter: node({ mode: 'standalone' }),
});
```

```astro
---
// src/pages/dashboard.astro — opt this page into SSR
export const prerender = false;
---
```

### Adapter reference

| Adapter | Output | Use for |
|---------|--------|---------|
| `@astrojs/node` | Node.js HTTP server (standalone or middleware) | Self-hosted, Docker, traditional Node hosting |
| `@astrojs/vercel` | Vercel serverless / edge | Vercel deployment |
| `@astrojs/cloudflare` | Cloudflare Pages / Workers | Cloudflare deployment (first-party since Jan 2026 acquisition). Astro 6+ dev server runs on real `workerd`; access bindings via `cloudflare:workers` module (`Astro.locals.runtime` is removed in Astro 6). |
| `@astrojs/netlify` | Netlify functions | Netlify deployment |
| `@astrojs/deno` | Deno Deploy | Deno Deploy (verify maintenance status) |

### Cloudflare Workers: real local dev (Astro 6+)

> **Verified:** [docs.astro.build/en/guides/integrations-guide/cloudflare](https://docs.astro.build/en/guides/integrations-guide/cloudflare) ("The Astro.locals.runtime object has been removed in favor of direct access to Cloudflare Workers APIs"), [github.com/withastro/astro/issues/15237](https://github.com/withastro/astro/issues/15237).

Astro 6's dev server is rebuilt on Vite's Environment API. With the Cloudflare adapter, `astro dev` now runs inside `workerd` (Cloudflare's actual JS runtime) instead of a polyfilled approximation — Durable Objects, KV, R2, and Workers Analytics Engine are usable locally with HMR:

```typescript
// Access Cloudflare bindings directly via the cloudflare:workers module (Astro 6+)
import { env } from 'cloudflare:workers';

const kv = env.MY_KV_NAMESPACE;
await kv.put('visits', '1');
```

`Astro.locals.runtime` (the old way of reaching Cloudflare bindings) is removed in the Astro 6 Cloudflare adapter — migrate to the `cloudflare:workers` module directly.

### Docker containerization (Node adapter)

```dockerfile
# Dockerfile
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
EXPOSE 4321
CMD ["node", "dist/server/entry.mjs"]
```

```bash
docker build -t my-astro-app .
docker run -p 4321:4321 my-astro-app
```

### Build output structure

```
dist/
├── client/                       # Static assets (always present)
│   ├── _astro/                   # Hashed JS/CSS/images
│   ├── favicon.svg
│   └── images/
└── server/                       # SSR server (only with adapter)
    └── entry.mjs                 # Entry point for the Node server
```

For `output: 'static'` (no adapter), only `dist/client/` (well, `dist/` directly) is generated.

### Environment variables per deployment

Use `astro:env` (see §Typed Environment Variables) to declare a schema. Then set env vars per platform:

- **Node/Docker:** `docker run -e STRIPE_SECRET_KEY=sk_... -p 4321:4321 my-app`
- **Vercel:** Set in Vercel dashboard or `vercel env add`.
- **Cloudflare Pages:** Set in dashboard or via `wrangler secret put`.
- **Netlify:** Set in dashboard or `netlify env:set`.

Always use `access: 'secret'` for server-only secrets — Astro ensures they never ship to the client.

### Anti-patterns

- **Switching the whole app to `output: 'server'` for one dynamic page.** Use `output: 'static'` (default) with per-page `prerender = false` instead.
- **Shipping `.env` files to production.** Use platform env vars, not committed files.
- **Using the `file` Sessions driver in serverless.** Filesystem isn't shared across instances. Use Redis or libSQL.
- **Forgetting to set `site` in `astro.config.mjs`.** Required for sitemap, canonical URLs, and RSS feeds. Without it, `Astro.site` is undefined.

## Top 20 Anti-Patterns (expanded)

> The first 10 are from the original SKILL.md (with corrections). Items 11–15 are from the prior rewrite. Items 16–20 cover Astro 6/7-specific pitfalls (Zod 4, Rust compiler, src/fetch.ts, ASTRO_KEY, CVE-2025-66202).

1. **Shipping JS when you don't need it.** The #1 Astro mistake. Use Astro components (`.astro`) for static content and reserve framework components (React/Vue/Svelte) for genuinely interactive elements. If a component doesn't have state or event handlers, it should be `.astro`, not `.tsx`.

2. **`client:load` for everything.** `client:load` hydrates immediately — wasteful for below-the-fold components. Use `client:idle` for non-critical interactivity, `client:visible` for components far down the page, `client:media` for mobile/desktop-only widgets. Reserve `client:load` for above-the-fold critical interactions.

3. **Not using content collections for structured content.** Astro's content collections give you Zod-validated frontmatter, type-safe queries, and automatic slug generation. Writing your own Markdown loading logic skips all this. Always use `getCollection()` / `getEntry()` from `astro:content`.

4. **Missing Zod schema validation.** Content collection schemas catch typos and missing fields at build time. Without them, a misspelled `publishedAt` in a Markdown frontmatter becomes a runtime error (or worse, silently renders `undefined`). Always define a `z.object({...})` schema for every collection.

5. **Not using `client:only` for components that use `window`/`document`.** If a React/Vue component references `window` or `document` at module level, SSR will fail with "window is not defined". Use `client:only="react"` to skip SSR — but the component won't render until JS loads (show a placeholder via `slot="fallback"`).

6. **Giant layout files.** Layouts should be the HTML shell (`<html>`, `<head>`, `<body>`, header, footer, `<slot />`). Business logic doesn't belong in layouts. If your layout has `getCollection()` calls or complex conditionals, extract them into components.

7. **Not using View Transitions for multi-page sites.** View Transitions (`<ClientRouter />`) give SPA-like navigation with zero JS framework cost. Without them, every page navigation is a full page reload (jarring). Add `<ClientRouter />` to your base layout's `<head>` — it's a one-line upgrade that dramatically improves perceived performance.

8. **Forgetting `Astro.site` for canonical URLs.** Without `site: 'https://example.com'` in `astro.config.mjs`, `new URL(path, Astro.site)` produces `https://example.com/path` instead of `http://localhost:4321/path` in dev. Set the `site` config always — it's required for sitemaps, RSS feeds, and canonical URLs. Note: In Astro 6+, `Astro.site` is deprecated inside `getStaticPaths()` — use `import.meta.env.SITE` instead.

9. **Not using `prerender` for on-demand rendering.** With `output: 'static'` (default), you can still have SSR pages via `export const prerender = false`. Don't switch the whole app to `output: 'server'` just because one page needs SSR — use per-page opt-out. (Note: `'hybrid'` was removed in Astro 5; this is the canonical pattern now.)

10. **Loading content from external APIs at request time when build time works.** If content doesn't change per-user, fetch it at build time (in the `.astro` frontmatter or a content collection loader). Don't pay the runtime cost of an API call on every request for content that's the same for everyone. Astro 5's Content Layer API supports loading from external APIs at build time — use it.

11. **Not using `astro:env` for typed env vars.** `import.meta.env` is untyped and silently returns `undefined` for missing vars. `astro:env` validates at build time and enforces server/client access control. Always use `astro:env` for new code.

12. **Not using `astro:assets` for images.** Plain `<img src="/images/hero.png">` bypasses optimization entirely — no AVIF/WebP, no responsive `srcset`, no lazy-loading. Use `import heroImg from '../assets/hero.png'` and the `<Image />` component for local images.

13. **Mixing Tailwind 3 and 4 integrations.** `@astrojs/tailwind` is Tailwind 3 only. Tailwind 4 uses `@tailwindcss/vite`. Pick one — don't install both. For new projects, prefer Tailwind 4 with `@tailwindcss/vite`. Do not use `npx astro add tailwind` for Tailwind 4 (it may install the wrong plugin — see [github.com/withastro/astro/issues/16542](https://github.com/withastro/astro/issues/16542)).

14. **Using `set:html` with untrusted input.** XSS vulnerability. `set:html` is the explicit opt-out of Astro's auto-escaping. Never use it with user input without sanitizing (e.g., with `isomorphic-dompurify`). Prefer `set:text` (the default) or render Markdown via `render()` from `astro:content`.

15. **Using Server Islands without an adapter.** `server:defer` silently renders inline as if the directive weren't there when no adapter is installed. Always verify an adapter is configured before relying on Server Islands. The build does not warn about missing adapters.

16. **Importing Zod from the wrong module (Astro 6+).** `z` is no longer exported from `astro:content` or `astro:schema` — both deprecated re-exports were removed in Astro 6. Import from `astro/zod` instead: `import { z } from 'astro/zod';`. Also: `z.string().email()` is deprecated in Zod 4 — use `z.email()`; `.min(n, { message })` is now `.min(n, { error })`; `.default()` after `.transform()` must match the output type (use `.prefault()` for pre-transform defaults).

17. **Keeping an accidental `src/fetch.ts` file in Astro 7.** Astro 7 reserves `src/fetch.ts` as the Advanced Routing entrypoint. If you have an unrelated utility module with this name, Astro will treat it as the request pipeline entrypoint and break your routing. Rename the file or set `fetchFile: false` in `astro.config.mjs`.

18. **Writing invalid HTML expecting the old compiler to fix it (Astro 7).** The Rust compiler (stable in Astro 7) no longer auto-corrects malformed markup — unclosed tags, invalid nesting, and JSX-style whitespace violations now throw build errors. Fix the markup rather than relying on compiler leniency. Verify Remark/rehype plugin compatibility if you hit issues with the new Sätteri Markdown processor (fall back to `@astrojs/markdown-remark` if needed).

19. **Missing `ASTRO_KEY` for Server Islands in rolling deployments.** Without a stable `ASTRO_KEY` environment variable, encrypted island props fail to decrypt across instances during rolling deploys, multi-region hosting, or CDN caching. Set `ASTRO_KEY` to a stable 256-bit hex key (generate with `openssl rand -hex 32`) in production environments that use Server Islands with more than one server instance.

20. **Hand-rolling URL decoding in middleware path checks (CVE-2025-66202).** A naive `url.pathname.startsWith('/admin')` guard was exploitable via double-percent-encoded paths (`%2561dmin` → `%61dmin` → `admin`) before the router-level fix in Astro 5.15.7 / 6.0+. Pin Astro to a patched version and **never attempt to URL-decode paths yourself in middleware** — trust the framework's already-canonicalized `url`/`params`.

## Cross-references

- `framework-templates` — CLAUDE.md generation template for Astro (project onboarding)
- `vue-3-nuxt` — Vue + Nuxt (Astro can use Vue components as islands — the Vue skill covers Vue component authoring)
- `svelte-5-sveltekit` — Svelte + SvelteKit (Astro can use Svelte components as islands)
- `react19-ts6-vite8-tailwindv4-mvp` — React (Astro can use React components as islands)
- `frontend-ui-engineering` — Production-quality UI build patterns (relevant for Astro components)
- `frontend-design` — Design thinking for web UI
- `api-and-interface-design` — Type contract design (relevant for content collection schemas and API endpoints)
- `api-patterns` — REST API patterns (for Astro API routes)
- `security-and-hardening` — OWASP-aware hardening (Astro has good XSS defaults via auto-escaping)
- `clean-code` — General coding standards
- `testing-patterns` — Test pyramid, mocking strategies
- `code-review-checklist` — 12-category code review checklist
- `tailwind-4` (if exists) — Tailwind 4 deep dive
- `cloudflare-workers` (if exists) — Cloudflare Workers deployment patterns

## Dependencies

### Required (installed via `npm create astro`)

- **Node.js** 22.12.0+ (even versions only; v18, v20, v23, v25 are not supported in current Astro)
- **Astro** 7.x (7.1.6 is current latest as of Aug 2026); 5.x and 6.x supported for migration
- **Vite** 8 (Astro 7) or 7 (Astro 6) — build tool, bundled with Astro
- **TypeScript** 5+ (default, can opt out but not recommended)
- **Zod** 4 (Astro 6+; Astro 5 bundled Zod 3) — imported from `astro/zod`
- **Shiki** 4 (Astro 6+; Astro 5 bundled Shiki 3) — syntax highlighting

### UI framework integrations (add via `npx astro add`)

- `@astrojs/react` — React island support
- `@astrojs/vue` — Vue island support
- `@astrojs/svelte` — Svelte island support
- `@astrojs/preact` — Preact island support
- `@astrojs/solid-js` — SolidJS island support
- `@astrojs/lit` — Lit web component support

### Content & styling integrations

- `@astrojs/mdx` — MDX support (Markdown + JSX)
- `@tailwindcss/vite` — Tailwind CSS 4 (preferred Vite plugin)
- `@astrojs/tailwind` — Tailwind CSS 3 (legacy; do not use with Tailwind 4)
- `@astrojs/sitemap` — auto-generate `/sitemap.xml`
- `@astrojs/rss` — RSS feed generation
- `@astrojs/partytown` — move third-party scripts to a web worker (improves performance)

### SSR adapters (add via `npx astro add`)

- `@astrojs/node` — self-hosted Node.js SSR
- `@astrojs/vercel` — Vercel SSR
- `@astrojs/cloudflare` — Cloudflare Pages/Workers SSR (first-party since Jan 2026). Astro 6+: native `workerd` local dev, `cloudflare:workers` bindings module.
- `@astrojs/netlify` — Netlify SSR
- `@astrojs/deno` — Deno Deploy SSR (verify maintenance status before adopting)

### Common additions

- `astro-icon` — icon component (uses Iconify)
- `astro-seo` — SEO meta tags component
- `astro-pagefind` — client-side full-text search (Pagefind)
- `keystatic` + `@keystatic/core` — headless CMS for Astro content collections
- `nanostores` + `@nanostores/react` / `@nanostores/vue` / `@nanostores/svelte` / `@nanostores/preact` — cross-island state management
- `@fontsource/<font>` — bundled Google Fonts (no CDN request; legacy alternative to Astro 6 Fonts API)
- `vitest` — unit testing
- `@playwright/test` — end-to-end testing
- `@lhci/cli` — Lighthouse CI for performance regression

### Deprecated / discontinued — DO NOT USE

- **Astro Studio** — discontinued September 2024; databases deleted March 2025. ([astro.build/blog/goodbye-astro-studio](https://astro.build/blog/goodbye-astro-studio))
- **`@astrojs/db` (Astro DB)** — deprecated in Astro 6.4; **removed in Astro 7.0**. ([docs.astro.build/en/guides/integrations-guide/db](https://docs.astro.build/en/guides/integrations-guide/db): "The Astro DB integration was deprecated in v6.4 and has been removed since Astro v7.0.") Migrate to Drizzle ORM, Turso/libSQL, Node.js SQLite, or another database layer.
- **`Astro.glob()`** — deprecated in Astro 5; **removed in Astro 6**. Use `import.meta.glob()` (Vite's native glob import) or `getCollection()` instead.
- **`<ViewTransitions />`** — deprecated alias; **removed in Astro 6**. Use `<ClientRouter />` from `astro:transitions` instead.
- **Legacy content collections (no `loader:`)** — removed in Astro 6. Every collection needs an explicit loader (`glob()`, `file()`, or custom). Use `legacy.collectionsBackwardsCompat: true` as a temporary migration bridge only.
- **`z` from `astro:content` / `astro:schema`** — deprecated in Astro 6. Import `z` from `astro/zod` instead.
- **`Astro.locals.runtime` (Cloudflare)** — removed in Astro 6 Cloudflare adapter. Use `cloudflare:workers` module instead.
- **`astro:transitions` low-level internals** (`createAnimationScope`, `TRANSITION_*` constants, `isTransitionBeforePreparationEvent` type guards) — removed in Astro 6. Listen for documented DOM events directly.

## Reference Tables

### `Astro.*` globals

Available in `.astro` component frontmatter and templates.

| Global | Type | Description |
|--------|------|-------------|
| `Astro.props` | `Props` | Component props (typed via `interface Props`). |
| `Astro.params` | `Record<string, string>` | URL path parameters (e.g., `slug` from `[slug].astro`). |
| `Astro.url` | `URL` | Full request URL. |
| `Astro.request` | `Request` | Standard Request object. |
| `Astro.response` | `ResponseInit` | Response init — set headers, status. |
| `Astro.cookies` | `AstroCookies` | Cookie read/write API. |
| `Astro.locals` | `App.Locals` | Per-request state (typed via `env.d.ts`). |
| `Astro.site` | `URL \| undefined` | The `site` config value. |
| `Astro.generator` | `string` | Astro version string (e.g., `"Astro v7.1.6"`). |
| `Astro.redirect(path, status?)` | `Response` | Return from frontmatter to redirect. |
| `Astro.slots` | `Slots` | Slot introspection (`Astro.slots.has('name')`). |
| `Astro.clientAddress` | `string \| undefined` | Client IP (SSR only; undefined in static builds). |
| `Astro.preferredLocale` | `string \| string[] \| undefined` | Browser-preferred locale(s) from `Accept-Language` (i18n). |
| `Astro.currentLocale` | `string \| undefined` | The locale of the current page (i18n). |
| `Astro.session` | `Session \| undefined` | Session object (with adapter + session config). Astro 6+: also accessible as `Astro.session?.get()` / `Astro.session?.set()`. |
| `Astro.cache` | `Cache API` | Route caching (Astro 7+ stable). `Astro.cache({ ttl, tags })`, `Astro.cache.invalidate([...tags])`. |
| `Astro.rewrite(path)` | `Response` | Rewrite to a different route without redirect (server-side). |

### `astro:*` module namespaces

| Module | Exports | Purpose |
|--------|---------|---------|
| `astro:content` | `defineCollection`, `defineLiveCollection`, `reference`, `getCollection`, `getEntry`, `getEntries`, `getLiveEntry`, `render` | Content Layer API — define and query content collections (build-time + live). Note: `z` is no longer exported here in Astro 6+ — use `astro/zod`. |
| `astro:loaders` | `glob`, `file` | Built-in content loaders. |
| `astro:zod` | `z` (Zod 4) | Type schema validation (Astro 6+ — replaces deprecated `z` re-export from `astro:content` / `astro:schema`). |
| `astro:middleware` | `defineMiddleware`, `sequence` | Request middleware. |
| `astro:env/server` | Typed env var exports, `getSecret()` | Server-only env vars (configured via `env.schema`). |
| `astro:env/client` | Typed env var exports | Client-accessible env vars. |
| `astro:transitions` | `ClientRouter` | View Transitions API. |
| `astro:assets` | `Image`, `Picture`, `Font`, `getImage`, `inferRemoteSize`, `getConfiguredImageService`, `imageConfig`, `fontData` | Image, font, and asset optimization. |
| `astro:i18n` | `getRelativeLanguageUrl`, `getAbsoluteLanguageUrl`, `getPathByLocale`, `getLocaleByPath` | i18n routing helpers. |
| `astro:actions` | `defineAction`, `z`, `ActionError`, `isActionError`, `actions` | Astro Actions (experimental). |
| `astro:session` | (type augmentation for `SessionData`) | Session type declarations. |
| `astro/fetch` | `FetchState`, `astro`, `actions`, `middleware`, `pages`, `i18n`, `sessions`, `redirects`, `trailingSlash`, `cache` | Advanced Routing (Astro 7+) — programmatic request pipeline. |
| `astro/hono` | Same handler names as `astro/fetch` | Hono-compatible variant of Advanced Routing (Astro 7+). |
| `astro:db` | (removed) | **REMOVED in Astro 7** — was deprecated in 6.4. Use Drizzle, Turso/libSQL, or other DB layer. |

### `client:*` directives (complete)

| Directive | Hydration trigger | Use case |
|-----------|-------------------|----------|
| `client:load` | Immediately on page load | Critical above-the-fold interactivity (header nav, login button). |
| `client:idle` | `requestIdleCallback` | Below-the-fold interactive elements. |
| `client:visible` | `IntersectionObserver` | Components far down the page (comments, widgets). |
| `client:media="(query)"` | Media query match | Mobile-only or desktop-only widgets. |
| `client:only="react"` | Skip SSR; render on client only | Components that can't render on server (use `window`, `document` at module level). |

### `set:*` directives

| Directive | Behavior | Use case |
|-----------|----------|----------|
| (default, no directive) | HTML-escape the value | Safe rendering of text — **always prefer this**. |
| `set:text` | HTML-escape the value (explicit) | Same as default; explicit for clarity. |
| `set:html` | Inject raw HTML (NO escaping) | Trusted HTML only — XSS risk if used with untrusted input. |
| `set:raw` | Inject without escaping or HTML processing | Rare edge cases (e.g., injecting pre-escaped HTML entities). |

### `transition:*` directives

| Directive | Behavior |
|-----------|----------|
| `transition:animate="fade"` | Cross-fade old → new (default). |
| `transition:animate="slide"` | Slide old out, new in. |
| `transition:animate="none"` | No animation. |
| `transition:animate={customObject}` | Custom animation: `{ forwards: {...}, backwards: {...} }`. |
| `transition:persist` | Keep DOM and JS state across page navigation. |
| `transition:name="identifier"` | Morph between elements with the same name across pages. |

### `<style>` / `<script>` directives

| Directive | Applies to | Behavior |
|-----------|------------|----------|
| (default `<style>`) | `<style>` | Scoped to the component. |
| `is:global` | `<style>` | Global — applies to all components. Use sparingly. |
| `is:inline` | `<style>` / `<script>` | Skip Vite processing; embed raw in HTML. |
| `define:vars={...}` | `<style>` | Pass server-side variables as CSS custom properties. |

---

## Verification & Confidence Summary

Per the agent contract §13, the confidence levels of claims in this skill:

- **Verified** (sourced from primary docs at `docs.astro.build`, official blog at `astro.build/blog`, GitHub source at `github.com/withastro/astro`, or NVD/advisory entries):
  - Astro version matrix (5.0 / 5.7 / 5.10 / 6.0 / 6.2 / 7.0 / 7.1.6)
  - Cloudflare acquisition date (2026-01-16)
  - Astro Studio discontinuation / Astro DB deprecation (5.x) / removal (Astro 7.0)
  - Sessions API stability (5.7+); Astro 6 `sessionDrivers.*()` config shape
  - `astro:env` stability (5.0+)
  - `astro:assets` API surface
  - `glob` / `file` loaders from `astro/loaders`
  - `output: 'hybrid'` removal in Astro 5
  - Node.js 22.12.0 minimum (Astro 6+)
  - Tailwind 4 integration approach via `@tailwindcss/vite`
  - `server:defer` directive, adapter requirement, and `ASTRO_KEY` for rolling deployments
  - `sequence()` for middleware chaining
  - `ClientRouter` from `astro:transitions` (replaced `<ViewTransitions />` removed in Astro 6)
  - Zod 4 migration: `astro/zod` import, `z.email()`, `{ error }` vs `{ message }`, `.prefault()` (verified against [zod.dev/v4/changelog](https://zod.dev/v4/changelog) and [docs.astro.build/en/reference/modules/astro-zod](https://docs.astro.build/en/reference/modules/astro-zod))
  - `Astro.glob()` removal in Astro 6 (use `import.meta.glob()` or `getCollection()`)
  - `Astro.site` deprecation in `getStaticPaths()` (Astro 6+) — use `import.meta.env.SITE`
  - `legacy.collectionsBackwardsCompat` flag as Astro 6 migration aid
  - Live Content Collections `defineLiveCollection` / `getLiveEntry` / `src/live.config.ts` API (Astro 6+ stable)
  - Fonts API stable in Astro 6 with `fontProviders.google()` / `fontProviders.fontsource()` etc.
  - `cloudflare:workers` module replacing `Astro.locals.runtime` (Astro 6 Cloudflare adapter)
  - Astro 6 Cloudflare adapter runs dev server on real `workerd` (Vite Environment API)
  - Astro 7 Rust compiler (stable, stricter HTML parsing, no auto-correction)
  - Sätteri default Markdown/MDX processor in Astro 7 (replaces `@astrojs/markdown-remark`)
  - Astro 7 Vite 8 (from Vite 7 in Astro 6)
  - Astro 7 JSX-style whitespace as default
  - Astro 7 Advanced Routing: `src/fetch.ts` reserved entrypoint, `astro/fetch` module (`FetchState`, `astro()`, `actions()`, `middleware()`, `pages()`, `i18n()`, `sessions()`, `redirects()`, `trailingSlash()`, `cache()`), `astro/hono` Hono-compatible variant, `fetchFile` config
  - Astro 7 Route Caching stable (was experimental in 6.0)
  - Astro 7 background dev server (`astro dev --background`), JSON logging, `/astro/status` health endpoint, AI agent detection
  - `@astrojs/db` removed in Astro 7.0 (deprecated in 6.4)
  - CVE-2025-66202 (double-percent-encoding middleware bypass) fixed in Astro 5.15.7 / 6.0+
  - Astro 6 `astro:transitions` low-level internals removal (`createAnimationScope`, `TRANSITION_*` constants, type guards)
  - Astro 6 `import.meta.env` no longer coerces types or falls back to `process.env`
  - Astro 6 default image `fit` change (cropping applied by default; images never upscale)
  - Astro 6 `import.meta.env.ASSETS_PREFIX` deprecated → use `build.assetsPrefix` from `astro:config/server`

- **Reasoned** (API surface verified against primary docs; code examples not executed in this authoring environment):
  - All code examples in Sessions, Actions, `astro:env`, `astro:assets`, Fonts, Advanced Routing, Route Caching, AI-Agent DX sections
  - The Actions API current status (based on secondary source; verify against current docs before production use)
  - Live Content Collections `defineLiveCollection` / `getLiveEntry` API in `src/live.config.ts` — verified against [docs.astro.build/en/guides/content-collections](https://docs.astro.build/en/guides/content-collections)
  - Advanced Routing `astro/fetch` module API surface — verified against [docs.astro.build/en/reference/modules/astro-fetch](https://docs.astro.build/en/reference/modules/astro-fetch)
  - `ASTRO_KEY` for Server Islands — verified against [docs.astro.build/en/guides/server-islands](https://docs.astro.build/en/guides/server-islands) and [github.com/withastro/astro/issues/11851](https://github.com/withastro/astro/issues/11851)
  - CVE-2025-66202 router fix — verified against [nvd.nist.gov/vuln/detail/CVE-2025-66202](https://nvd.nist.gov/vuln/detail/CVE-2025-66202) and [github.com/withastro/astro/security/advisories/GHSA-whqg-ppgf-wp8c](https://github.com/withastro/astro/security/advisories/GHSA-whqg-ppgf-wp8c)
  - Zod 4 migration gotchas (`z.email()`, `{ error }` vs `{ message }`, `.prefault()`) — verified against [zod.dev/v4/changelog](https://zod.dev/v4/changelog)
  - `cloudflare:workers` module replacing `Astro.locals.runtime` — verified against [docs.astro.build/en/guides/integrations-guide/cloudflare](https://docs.astro.build/en/guides/integrations-guide/cloudflare)
  - Astro 7 background dev server, JSON logging, `/astro/status` health check — verified against [medium.com/@onix_react/whats-new-in-astro-7](https://medium.com/@onix_react/whats-new-in-astro-7-fb32e0e699fb), [javascript.plainenglish.io Astro 7 article](https://javascript.plainenglish.io/astro-7-officially-released-rust-rolldown-and-ai-development-experience-all-get-intensified-b4e88bc0cc52), and [docs.astro.build/en/reference/cli-reference](https://docs.astro.build/en/reference/cli-reference)
  - Sätteri Markdown processor (Astro 7 default) — verified against [morello.dev/blog/astro-7](https://morello.dev/blog/astro-7), [weeklyrust.substack.com/p/rust-powered-astro-7](https://weeklyrust.substack.com/p/rust-powered-astro-7)
  - Rust compiler stricter HTML parsing — verified against [morello.dev/blog/astro-7](https://morello.dev/blog/astro-7), [developersdigest.tech/blog/astro-7-rust-vite-8-release](https://www.developersdigest.tech/blog/astro-7-rust-vite-8-release)
  - `@astrojs/db` removal in Astro 7.0 — verified against [docs.astro.build/en/guides/integrations-guide/db](https://docs.astro.build/en/guides/integrations-guide/db), [astro-changelog.netlify.app/releases/re_kwdofl76q84ubwcz](https://astro-changelog.netlify.app/releases/re_kwdofl76q84ubwcz)
  - `Astro.glob()` removal in Astro 6 — verified against [docs.astro.build/en/guides/upgrade-to/v6](https://docs.astro.build/en/guides/upgrade-to/v6), [docs.astro.build/en/reference/errors/astro-glob-used-outside](https://docs.astro.build/en/reference/errors/astro-glob-used-outside)
  - `Astro.site` deprecation in `getStaticPaths()` (Astro 6+) — verified against [docs.astro.build/en/guides/upgrade-to/v6](https://docs.astro.build/en/guides/upgrade-to/v6)
  - Sessions API `sessionDrivers.*()` config shape (Astro 6) — verified against [docs.astro.build/en/reference/session-driver-reference](https://docs.astro.build/en/reference/session-driver-reference)
  - Fonts API `fontProviders.*()` (Astro 6 stable) — verified against [docs.astro.build/en/guides/fonts](https://docs.astro.build/en/guides/fonts)
  - Route caching stability (Astro 7) — verified against [gitclear.com astro@7.0.0 release](https://www.gitclear.com/open_repos/withastro/astro/release/astro@7.0.0), [medium.com/@onix_react/whats-new-in-astro-7](https://medium.com/@onix_react/whats-new-in-astro-7-fb32e0e699fb)

- **Assumed**:
  - Skill name remains `astro-5` (cross-skill references depend on it; rename would require updating all referencing skills). `draft-update-q.md` recommended renaming to `astro-7` — see §5.4 of the planning document for trade-offs.
  - Target Astro 5/6/7 together (rather than splitting per major version) — splits triple maintenance burden
  - Experimental features (Actions, SVG components, Advanced Routing pre-Astro-7) included with clear labeling
  - Code examples not executed in CI — labeled `Reasoned` per agent contract §13

- **Unverifiable in this environment**:
  - Whether each code example runs against Astro 7.1.6 (would require a running Astro project — recommend setting up a CI job that executes examples if upgrading to `Verified` is desired)
  - Exact maintenance status of `@astrojs/deno` adapter (mentioned but not audited)
  - Exact package names for Astro 6 session driver packages (`@astrojs/session-redis`, etc.) — driver ecosystem is evolving; verify against current docs before adoption

## Changelog

- **2026-08-03 (initial rewrite)** — Complete rewrite based on research plan. Major changes:
  - Updated target from Astro 5.0+ to Astro 5/6/7 (current latest 7.1.6)
  - Added Cloudflare acquisition note (Jan 2026)
  - Removed Astro Studio and Astro DB references (discontinued/deprecated)
  - Removed `output: 'hybrid'` (was removed in Astro 5)
  - Updated Node.js requirement to 22.12.0+
  - Updated Vite version to 7 (Astro 6) or 8 (Astro 7)
  - Corrected Tailwind 4 integration (use `@tailwindcss/vite`, not `npx astro add tailwind`)
  - Fixed Server Islands example syntax (removed incorrect `slot="fallback"` on the directive)
  - Added new sections: Versions & Migration, Routing, i18n, Sessions, Actions (experimental), `astro:env`, `astro:assets`, Fonts, State Management, Styling, Forms, Security, Testing, Reference Tables
  - Expanded Anti-Patterns from 10 to 15
  - Added `sequence()` to Middleware section
  - Added `set:text` / `set:raw` to component directives
  - Added `define:vars`, `<Fragment>`, named slot fallback
  - Added Live Content Collections (Astro 6+) subsection
  - Added schema references (`reference()`) for cross-collection relations
  - Added complete `Astro.*` globals and `astro:*` module reference tables

- **2026-08-03 (merge with drafts q, d, s)** — Merged additional details from three attached drafts:
  - **From `draft-update-s.md` (Astro 6 SKILL.md):**
    - Updated Zod import to `astro/zod` (Astro 6+ — `astro:content`/`astro:schema` re-exports removed)
    - Added Zod 4 migration gotchas: `z.email()`, `{ error }` vs `{ message }`, `.prefault()`
    - Replaced Live Content Collections example with correct `defineLiveCollection` + `src/live.config.ts` + `getLiveEntry()` API (returns `{ entry, error }` result)
    - Documented `Astro.glob()` removal (Astro 6) — use `import.meta.glob()` or `getCollection()`
    - Documented `legacy.collectionsBackwardsCompat` migration flag
    - Added Astro 6 detailed migration table (Node 22.12.0+ required, Zod 4, Vite 7, Shiki 4, `entry.id` only, `Astro.site` deprecated in `getStaticPaths()`, `import.meta.env` no longer coerces, default image `fit` change, `Astro.locals.runtime` → `cloudflare:workers`, `import.meta.env.ASSETS_PREFIX` → `build.assetsPrefix`, `<ViewTransitions />` → `<ClientRouter />`)
    - Updated Sessions API to reflect Astro 6 `sessionDrivers.*()` config shape and `Astro.session?.get()` API
    - Updated Fonts API to stable `fontProviders.google()` / `fontProviders.fontsource()` config (Astro 6+)
    - Added `cloudflare:workers` module note (replaces `Astro.locals.runtime` in Astro 6)
  - **From `draft-update-q.md` (Astro 7 strategic plan):**
    - Added new "Advanced Routing (Astro 7+)" section covering `src/fetch.ts` entrypoint, `astro/fetch` module (`FetchState`, `astro()`, `actions()`, `middleware()`, `pages()`, `i18n()`, `sessions()`, `redirects()`, `trailingSlash()`, `cache()`), `astro/hono` Hono-compatible variant, `fetchFile` config, and the accidental-`src/fetch.ts` anti-pattern
    - Added new "Route Caching (Astro 7+)" section covering `Astro.cache` API, cache drivers, and cache tag invalidation
    - Added new "AI-Agent DX (Astro 7+)" section covering `astro dev --background`, JSON logging, `/astro/status` health endpoint, and AI agent detection
    - Added detailed Astro 6→7 migration table (Vite 8, Rust compiler stable, Sätteri Markdown, JSX whitespace, route caching stable, background dev server, JSON logging, `@astrojs/db` removed, Advanced Routing enabled by default)
    - Added Rust compiler strictness warnings (unclosed tags, invalid nesting, JSX whitespace, Sätteri/`@astrojs/markdown-remark` compatibility)
    - Added `ASTRO_KEY` for Server Islands rolling deployments / multi-region / CDN caching
    - Added serializable prop constraints for Server Islands
    - Added CVE-2025-66202 double-percent-encoding middleware bypass note and patched-version requirement
    - Expanded Anti-Patterns from 15 to 20 (added: Zod import, `src/fetch.ts` hazard, Rust compiler strictness, `ASTRO_KEY`, CVE-2025-66202)
    - Added `astro/fetch`, `astro/hono`, `astro/zod` to `astro:*` module reference table
    - Added `Astro.cache`, `Astro.rewrite` to `Astro.*` globals table
    - Updated Dependencies: `@astrojs/db` marked REMOVED in Astro 7.0; added `Astro.glob()`, `<ViewTransitions />`, legacy content collections, `z` from `astro:content`, `Astro.locals.runtime`, `astro:transitions` low-level internals to deprecated/removed list
  - **From `draft-update-d.md (original Astro 5 SKILL.md variations):**
    - Anti-pattern #11 from draft-d (hardcoding environment-specific URLs) — already covered by the existing `astro:env` anti-pattern
    - Anti-pattern #12 from draft-d (ignoring image optimization) — already covered by anti-pattern #12 in the baseline
    - No new content adopted — draft-d's claims about Astro 5.0+, Node 20+, Vite 6, Astro Studio, `output: 'hybrid'` were stale and contradicted by drafts q and s




