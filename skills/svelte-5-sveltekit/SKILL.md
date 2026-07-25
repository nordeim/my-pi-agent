---
name: svelte-5-sveltekit
description: "Svelte 5 + SvelteKit 2 full-stack TypeScript workflow skill. Covers the runes reactivity model ($state, $derived, $effect, $props, $bindable) which is fundamentally different from React hooks, file-based routing with +page.svelte / +layout.svelte / +page.server.ts / +page.ts, form actions as the idiomatic mutation pattern (progressive enhancement), load functions (server vs universal), hooks.server.ts for request-level interception, $env modules for typed environment variables (static vs dynamic, private vs public), adapters for deployment targets (auto / node / static / cloudflare / vercel). Use when building any web app on Svelte 5 or SvelteKit 2 — especially when the task involves migrating Svelte 4 store-based code to runes, choosing between server load and universal load, or wiring form actions with validation."
license: Proprietary. LICENSE.txt has complete terms
---

# Svelte 5 + SvelteKit 2 — Full-Stack TypeScript Workflow Skill

> **Target:** Svelte 5.x (runes reactivity model, released October 2024) + SvelteKit 2.x (released December 2023). The `sv` CLI is the canonical project scaffolder (replaces the old `npm create svelte` flow). Vite is the build tool. TypeScript is the default.

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending a Svelte 5 or SvelteKit 2 application. Trigger phrases include "Svelte 5", "SvelteKit", "runes", "$state", "$derived", "$effect", "$props", "form actions", "load function", "+page.server.ts", "hooks.server.ts", "$env/static/private", and any reference to a `src/routes/` directory layout with `+page.svelte` / `+layout.svelte` files.

Do **not** use this skill for:
- **Svelte 4 or earlier** — runes do not exist; the mental model is completely different (stores, reactive `$:` labels, `export let` for props). If the project is on Svelte 4, suggest upgrading to 5 first.
- **SvelteKit 1** — file conventions changed in SvelteKit 2 (`goto()` now requires `await`, `invalidate()` semantics changed).
- **Plain Svelte without SvelteKit** (e.g., embedded widgets) — only the runes sections apply; routing/load/actions sections do not.
- **Vue / React / Solid** — different frameworks, different mental models. Vue 3 Composition API looks superficially similar to runes but the reactivity boundary is different.

## Quick Start

```bash
# Create a new SvelteKit project (the `sv` CLI is the canonical scaffolder as of 2024)
npx sv create my-app
# Prompts: template (minimal / demo / library), TypeScript (yes), ESLint, Prettier, Vitest, Playwright

cd my-app
npm install
npm run dev                      # Dev server at http://localhost:5173 (Vite default)
```

### Key scripts (in `package.json`)

```bash
npm run dev                      # Vite dev server with HMR
npm run build                    # Production build via adapter (default: adapter-auto)
npm run preview                  # Preview the production build locally
npm run check                    # svelte-check: type-check + accessibility audit
npm run check:watch              # Watch mode for svelte-check
npm run test                     # Vitest (unit tests)
npm run test:e2e                 # Playwright (e2e tests)
```

---

## Project Structure (SvelteKit canonical layout)

```
my-app/
├── src/
│   ├── routes/                  # ← File-based routing lives here
│   │   ├── +layout.svelte       # Root layout (wraps every page)
│   │   ├── +layout.ts           # Root universal load (runs on server + client)
│   │   ├── +layout.server.ts    # Root server load (server-only, can read DB)
│   │   ├── +page.svelte         # Home page (/)
│   │   ├── +page.server.ts      # Home page server load + form actions
│   │   ├── +page.ts             # Home page universal load (optional)
│   │   ├── about/
│   │   │   └── +page.svelte     # /about page
│   │   ├── posts/
│   │   │   ├── +page.svelte     # /posts (list)
│   │   │   ├── +page.server.ts  # /posts server load + actions
│   │   │   └── [slug]/
│   │   │       └── +page.svelte # /posts/:slug (dynamic param)
│   │   └── api/
│   │       └── health/
│   │           └── +server.ts   # /api/health (GET, POST, etc. handlers)
│   ├── lib/
│   │   ├── components/          # Reusable Svelte components
│   │   ├── server/              # Server-only code (DB clients, auth utilities)
│   │   ├── stores/              # Cross-component state (runes-based, in .svelte.ts files)
│   │   ├── utils/               # Utility functions
│   │   └── index.ts             # Barrel exports (import from $lib)
│   ├── app.html                 # HTML shell template
│   ├── app.css                  # Global styles (import in root +layout.svelte)
│   ├── app.d.ts                 # App-wide type declarations (Locals, PageData, etc.)
│   └── hooks.server.ts          # Request-level interception (auth, logging, etc.)
├── static/                      # Static assets served as-is (favicon, robots.txt, images)
├── tests/                       # Test files
├── package.json
├── svelte.config.js             # SvelteKit config (adapter, preprocessors)
├── vite.config.ts               # Vite config
├── tsconfig.json
└── .env                         # Environment variables (prefix with VITE_ for public)
```

### The `+` file convention (memorize this)

SvelteKit uses filename prefixes to identify route building blocks. The `+` prefix is mandatory and the suffix matters:

| File | Runs where | Purpose |
|---|---|---|
| `+page.svelte` | Client | Page UI component (always client-rendered after hydration) |
| `+page.ts` | Universal (server on first load, then client) | Load data + return PageData; can use browser APIs on client nav |
| `+page.server.ts` | Server only | Load data from DB/secrets; export `actions` for mutations |
| `+layout.svelte` | Client | Layout component wrapping all child routes |
| `+layout.ts` | Universal | Layout load |
| `+layout.server.ts` | Server | Layout server load (auth check, user session) |
| `+server.ts` | Server | API endpoint (GET, POST, PUT, DELETE handlers) |
| `+error.svelte` | Client | Error page for this route subtree |

A route can have ALL of these files (a full-stack route) or just `+page.svelte` (a static page). The minimum viable route is a directory containing `+page.svelte`.

---

## Core Mental Model: Runes (the Svelte 5 revolution)

Svelte 5 introduced **runes** — special `$`-prefixed functions that the Svelte compiler transforms into reactive primitives. Runes replace Svelte 4's `export let` props, `$:` reactive labels, and the `writable()`/`readable()` store pattern for component-local state.

### The 5 runes you must know

#### `$state` — reactive variable

```svelte
<script lang="ts">
  let count = $state(0);
  let user = $state({ name: 'Alice', age: 30 });

  function increment() {
    count++;                       // Mutation triggers reactivity
    user.age++;
  }
</script>

<button onclick={increment}>
  {count} — {user.name} is {user.age}
</button>
```

`$state` deep-wraps objects and arrays — mutating any nested property triggers updates. No need for `writable()` or spread patterns.

#### `$derived` — computed value

```svelte
<script lang="ts">
  let count = $state(0);
  let doubled = $derived(count * 2);
  let parity = $derived(count % 2 === 0 ? 'even' : 'odd');
</script>

<button onclick={() => count++}>Count: {count}</button>
<p>Doubled: {doubled} ({parity})</p>
```

`$derived` recomputes only when its dependencies change. It is read-only — never assign to a `$derived` value.

#### `$effect` — side effects

```svelte
<script lang="ts">
  let count = $state(0);

  $effect(() => {
    // Runs after the DOM updates, when `count` changes
    document.title = `Count: ${count}`;
    return () => {
      // Cleanup function runs before the next effect or on unmount
    };
  });
</script>
```

Use `$effect` for: DOM measurements, third-party library sync, subscriptions. **Do NOT** use `$effect` to derive state — use `$derived` instead. **Do NOT** use `$effect` to update other state if you can avoid it — that's a sign you should restructure as `$derived`.

#### `$props` — component inputs (replaces `export let`)

```svelte
<script lang="ts">
  // Svelte 5 idiom — $props() returns all props
  let { title, count = 0, onIncrement } = $props();
  
  // With TypeScript:
  interface Props {
    title: string;
    count?: number;
    onIncrement?: () => void;
  }
  let { title, count = 0, onIncrement }: Props = $props();
  
  // Rest props (spread any unknown attrs onto a child element)
  let { title, ...rest } = $props();
</script>
```

#### `$bindable` — opt-in two-way binding

```svelte
<!-- Child.svelte -->
<script lang="ts">
  interface Props { value?: string }
  let { value = $bindable() }: Props = $props();
</script>
<input bind:value />

<!-- Parent.svelte -->
<script lang="ts">
  import Child from './Child.svelte';
  let name = $state('Alice');
</script>
<Child bind:value={name} />
<p>Hello, {name}</p>
```

Two-way binding is **opt-in** in Svelte 5 — the child must declare the prop as `$bindable()`. This is a deliberate departure from Svelte 4 where `bind:value` worked on any `export let` prop.

### Cross-component state: `.svelte.ts` modules with `$state`

For state shared across components (the old use case for `writable()` stores), create a `.svelte.ts` file that exports a `$state`-based object:

```typescript
// src/lib/stores/cart.svelte.ts
interface CartItem { id: string; name: string; price: number; qty: number; }

class CartStore {
  items = $state<CartItem[]>([]);

  get total() { return this.items.reduce((sum, i) => sum + i.price * i.qty, 0); }
  get count() { return this.items.reduce((sum, i) => sum + i.qty, 0); }

  add(item: Omit<CartItem, 'qty'>) {
    const existing = this.items.find(i => i.id === item.id);
    if (existing) existing.qty++;
    else this.items.push({ ...item, qty: 1 });
  }

  remove(id: string) {
    this.items = this.items.filter(i => i.id !== id);
  }
}

export const cart = new CartStore();
```

```svelte
<!-- Any component -->
<script lang="ts">
  import { cart } from '$lib/stores/cart.svelte';
</script>

<button onclick={() => cart.add({ id: '1', name: 'Widget', price: 9.99 })}>
  Add to cart
</button>
<p>{cart.count} items — ${cart.total.toFixed(2)}</p>
```

The `.svelte.ts` extension is what makes runes work in a non-component module. Plain `.ts` files cannot use runes.

### The old `$store` syntax still works (backwards compat)

Svelte 4 stores (`writable`, `readable`, `$store` auto-subscription) are NOT removed in Svelte 5. Existing code keeps working. But for new code, prefer the `.svelte.ts` class pattern above — it's more ergonomic and type-safe.

---

## Routing & Load Functions

SvelteKit routing is **file-system based**. The directory structure under `src/routes/` IS the URL structure.

### Route types

| URL | Route file |
|---|---|
| `/` | `src/routes/+page.svelte` |
| `/about` | `src/routes/about/+page.svelte` |
| `/posts/:slug` | `src/routes/posts/[slug]/+page.svelte` |
| `/posts/[id]` (catch-all) | `src/routes/posts/[...id]/+page.svelte` |
| `/users/[id]` (matcher) | `src/routes/users/[id=integer]/+page.svelte` |
| `/api/health` | `src/routes/api/health/+server.ts` |

### Load functions: server vs universal

The single most important decision in SvelteKit is whether your load function runs on the **server** (`+page.server.ts`) or as a **universal** function (`+page.ts`).

```typescript
// src/routes/posts/+page.server.ts  — SERVER load
import type { PageServerLoad } from './$types';
import { db } from '$lib/server/db';

export const load: PageServerLoad = async ({ locals }) => {
  // ✅ Can import $env/static/private
  // ✅ Can query the database directly
  // ✅ Can read cookies, locals.user (set by hooks.server.ts)
  // ❌ Cannot use browser APIs (window, document, localStorage)
  const posts = await db.post.findMany({ where: { published: true } });
  return { posts };   // Serialized to JSON, sent to client
};
```

```typescript
// src/routes/posts/+page.ts  — UNIVERSAL load (runs on server first load, then client on nav)
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ data, fetch }) => {
  // `data` is whatever the server load returned (if both exist)
  // `fetch` is SvelteKit's enhanced fetch (handles relative URLs, credentials)
  // ✅ Can call your own API endpoints
  // ✅ Can use browser APIs on client-side navigation
  // ❌ Cannot import $env/static/private (would leak to client bundle)
  // ❌ Cannot import $lib/server/*
  const stats = await fetch('/api/posts/stats').then(r => r.json());
  return { ...data, stats };
};
```

**Rule of thumb:** if the data is sensitive or requires DB/secrets, use `+page.server.ts`. If it's a client-side enhancement (calling your own API, browser-only logic), use `+page.ts`. A route can have BOTH — the universal load receives the server load's output as `data`.

### `+page.svelte` receives the load result

```svelte
<script lang="ts">
  import type { PageData } from './$types';
  let { data }: { data: PageData } = $props();
  // data.posts is fully typed from the load function's return type
</script>

<h1>Posts</h1>
<ul>
  {#each data.posts as post (post.id)}
    <li><a href="/posts/{post.slug}">{post.title}</a></li>
  {/each}
</ul>
```

The `$types` import is auto-generated by SvelteKit — it gives you end-to-end type safety from load function → component props.

---

## Form Actions (the idiomatic mutation pattern)

SvelteKit does **not** use a separate API layer for mutations within your app. The idiomatic pattern is **form actions** — progressive-enhancement-friendly handlers that work without JavaScript.

### Define actions in `+page.server.ts`

```typescript
// src/routes/posts/new/+page.server.ts
import type { Actions, PageServerLoad } from './$types';
import { fail, redirect } from '@sveltejs/kit';
import { db } from '$lib/server/db';

export const load: PageServerLoad = async ({ locals }) => {
  if (!locals.user) throw redirect(302, '/login');
  return { categories: await db.category.findMany() };
};

export const actions: Actions = {
  create: async ({ request, locals }) => {
    if (!locals.user) return fail(401, { message: 'Unauthorized' });

    const formData = await request.formData();
    const title = formData.get('title') as string;
    const body = formData.get('body') as string;
    const categoryId = formData.get('categoryId') as string;

    // Validation
    if (!title || title.length < 3) {
      return fail(400, { title, body, categoryId, errors: { title: 'Title must be at least 3 characters' } });
    }

    const post = await db.post.create({
      data: { title, body, categoryId, authorId: locals.user.id, status: 'draft' }
    });

    throw redirect(303, `/posts/${post.slug}`);
  },

  // Multiple actions per route are fine
  draft: async ({ request }) => {
    const formData = await request.formData();
    // ... save as draft
    return { success: true };
  }
};
```

### Use actions in `+page.svelte` via `use:enhance`

```svelte
<script lang="ts">
  import type { PageData, ActionData } from './$types';
  import { enhance } from '$app/forms';

  let { data, form }: { data: PageData; form: ActionData } = $props();
  // `form` holds the return value of the most recent action call (e.g., fail() data)
  let loading = $state(false);
</script>

<form
  method="POST"
  action="?/create"
  use:enhance={() => {
    loading = true;
    return async ({ update }) => {
      await update();
      loading = false;
    };
  }}
>
  <input name="title" value={form?.title ?? ''} />
  {#if form?.errors?.title}<span class="error">{form.errors.title}</span>{/if}

  <textarea name="body">{form?.body ?? ''}</textarea>

  <select name="categoryId">
    {#each data.categories as cat}
      <option value={cat.id} selected={form?.categoryId === cat.id}>{cat.name}</option>
    {/each}
  </select>

  <button disabled={loading}>{loading ? 'Saving...' : 'Publish'}</button>
</form>
```

`use:enhance` progressively enhances the form: without JS, it submits as a normal POST and reloads the page; with JS, it submits via `fetch` and updates the page without reload. **The server-side action is the source of truth either way.**

For programmatic action calls (not triggered by a form submit), use `enhance`'s lower-level API or call the action via the `applyAction` function from `$app/forms`.

---

## Environment Variables: the `$env` modules

SvelteKit exposes environment variables via four typed modules. **The module you choose determines whether the variable is bundled into the client.**

| Module | When to use | Bundled in client? |
|---|---|---|
| `$env/static/private` | Server-only secrets (DB passwords, API keys) — inlined at build time | ❌ Never |
| `$env/static/public` | Public constants (app name, public Stripe key) — must start with `PUBLIC_` prefix | ✅ Yes |
| `$env/dynamic/private` | Server-only runtime env (Docker, serverless) — read at runtime | ❌ Never |
| `$env/dynamic/public` | Public runtime env (`PUBLIC_` prefix) — read at runtime on client | ✅ Yes |

```typescript
// src/lib/server/stripe.ts  — server-only file (the /server/ path segment is enforced)
import { STRIPE_SECRET_KEY } from '$env/static/private';
import Stripe from 'stripe';

export const stripe = new Stripe(STRIPE_SECRET_KEY);
```

```svelte
<!-- Any .svelte file — public env is safe to import -->
<script lang="ts">
  import { PUBLIC_APP_NAME } from '$env/static/public';
</script>
<h1>{PUBLIC_APP_NAME}</h1>
```

**Iron rule:** Never import from `$env/static/private` in a file under `src/routes/+page.svelte`, `src/routes/+page.ts`, or `src/lib/` (outside of `src/lib/server/`). The SvelteKit compiler will throw an error, but if it slips through, you leak secrets to the client bundle.

The `src/lib/server/` directory is **enforced server-only** by SvelteKit — any file in this tree (or its subdirectories) can be imported only by `+page.server.ts`, `+layout.server.ts`, `+server.ts`, or other `src/lib/server/*` files.

---

## `hooks.server.ts` — request-level interception

The `hooks.server.ts` file runs on every request. The canonical uses are: auth session loading, request logging, security headers, and CORS.

```typescript
// src/hooks.server.ts
import type { Handle } from '@sveltejs/kit';
import { dev } from '$app/environment';
import { db } from '$lib/server/db';

export const handle: Handle = async ({ event, resolve }) => {
  const sessionCookie = event.cookies.get('session');

  if (sessionCookie) {
    const session = await db.session.findUnique({
      where: { id: sessionCookie },
      include: { user: true }
    });

    if (session && session.expiresAt > new Date()) {
      event.locals.user = session.user;   // Available in every load + action
    } else {
      event.cookies.delete('session', { path: '/' });
    }
  }

  // Security headers
  const response = await resolve(event, {
    preload: ({ type }) => type === 'js' || type === 'css' || type === 'font'
  });
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  return response;
};
```

The `event.locals` object is the canonical place to stash per-request data that load functions and actions need to read (e.g., `locals.user`, `locals.tenantId`). Type it in `src/app.d.ts`:

```typescript
// src/app.d.ts
declare global {
  namespace App {
    interface Locals {
      user: { id: string; email: string; role: 'admin' | 'user' } | null;
    }
    interface PageData {
      // Add fields every PageData has, if any
    }
    // interface Error {}
    // interface PageState {}
  }
}
export {};
```

---

## Adapters & Deployment

SvelteKit uses **adapters** to convert the built output into a deployable shape. Configure in `svelte.config.js`:

```javascript
import adapter from '@sveltejs/adapter-auto';   // Default — auto-detects target
// import adapter from '@sveltejs/adapter-node';
// import adapter from '@sveltejs/adapter-static';
// import adapter from '@sveltejs/adapter-cloudflare';
// import adapter from '@sveltejs/adapter-vercel';

export default {
  kit: {
    adapter: adapter(),
    // adapter-static only: configure prerendering
    // prerender: { entries: ['*'] }
  }
};
```

| Adapter | Use |
|---|---|
| `adapter-auto` | Default. Auto-detects the deployment target (Vercel, Netlify, Cloudflare). Works for most hosted platforms. |
| `adapter-node` | Self-hosted Node server (Docker, VPS). Produces a `build/` directory with a `node index.js` entry point. |
| `adapter-static` | Pre-render the entire site to static HTML. Only works if every route can be prerendered (no dynamic server-side data per request). Use for blogs, marketing sites, docs. |
| `adapter-cloudflare` | Cloudflare Pages/Workers with edge runtime. |
| `adapter-vercel` | Vercel with edge functions. |
| `adapter-bun` | Bun's native runtime. |

For SSR with a database, use `adapter-node` (self-host) or `adapter-vercel`/`adapter-cloudflare` (managed). For static sites, use `adapter-static` and mark every route as prerenderable.

---

## Testing (Vitest + Playwright)

```bash
npm run test                     # Vitest (unit + component)
npm run test:e2e                 # Playwright (end-to-end)
```

### Component tests with Vitest

```typescript
// tests/Counter.test.ts
import { render, screen, fireEvent } from '@testing-library/svelte';
import Counter from '$lib/components/Counter.svelte';

it('increments on click', async () => {
  render(Counter);
  expect(screen.getByText('0')).toBeInTheDocument();
  await fireEvent.click(screen.getByRole('button'));
  expect(screen.getByText('1')).toBeInTheDocument();
});
```

### E2E tests with Playwright

```typescript
// tests/posts.spec.ts
import { test, expect } from '@playwright/test';

test('user can publish a post', async ({ page }) => {
  await page.goto('/posts/new');
  await page.fill('input[name="title"]', 'My Test Post');
  await page.fill('textarea[name="body"]', 'Hello world');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL(/\/posts\/.+/);
  await expect(page.locator('h1')).toContainText('My Test Post');
});
```

Cross-reference: `testing-patterns` skill for general test pyramid / mocking strategies. Cross-reference: `playwright-cli` skill for advanced Playwright debugging.

---

## Top 10 Anti-Patterns (the most valuable section)

1. **Using Svelte 4 stores for component-local state.** `$state` is simpler, more ergonomic, and more type-safe than `writable()`. Use stores only for cross-component state, and prefer the `.svelte.ts` class pattern over `writable()`.

2. **Using `$effect` to derive state.** `$effect` is for side effects (DOM, subscriptions, third-party sync). If you're computing a value, use `$derived`. If you're computing and storing it in `$state`, you almost certainly want `$derived` instead.

3. **Mixing server-only imports into universal loads.** Importing `$env/static/private` or `$lib/server/*` in a `+page.ts` (universal) or `+page.svelte` file will fail the build — but importing it in `+page.server.ts` is correct. The boundary is enforced, so listen to the compiler.

4. **Calling `fetch()` to your own API from a server load.** In `+page.server.ts`, query the database directly. Calling your own `/api/*` endpoint via `fetch` adds a round-trip for no benefit. Reserve `fetch` for universal loads (`+page.ts`) calling endpoints, or for cross-service calls.

5. **Forgetting to await `goto()`.** SvelteKit 2 made `goto()` return a Promise. Code that does `goto('/foo'); doSomethingNext();` will race. Always `await goto('/foo');`.

6. **Using `bind:value` on a prop that isn't `$bindable()`.** Two-way binding is opt-in in Svelte 5. The child must declare `let { value = $bindable() } = $props();` or `bind:value` silently fails.

7. **Putting secrets in `PUBLIC_*` env vars.** `PUBLIC_` prefix means the value is bundled into the client. Any var prefixed with `PUBLIC_` is visible to anyone who opens the browser dev tools. Use `$env/static/private` for secrets.

8. **Returning complex class instances from load functions.** Load return values are serialized to JSON (using devalue). Custom class instances become plain objects. Use plain objects, `Date` (devalue handles it), or `bigint` (also handled). Avoid `Map`, `Set`, `Symbol` — they don't serialize.

9. **Not handling `form` prop after action failures.** When `fail()` returns data, the `form` prop in `+page.svelte` holds it. If you don't read `form` and re-populate the form fields, the user loses their input on validation failure. Always `value={form?.title ?? ''}`.

10. **Choosing `adapter-auto` for a self-hosted Docker deployment.** `adapter-auto` only auto-detects hosted platforms (Vercel, Netlify, Cloudflare). For Docker/VPS, use `adapter-node` explicitly — otherwise the build produces a non-runnable output.

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for SvelteKit (project onboarding)
- `api-and-interface-design` — Type contract design (relevant for `+server.ts` API endpoints)
- `api-patterns` — REST API patterns (for SvelteKit `+server.ts` files)
- `security-and-hardening` — OWASP-aware hardening (SvelteKit has CSRF protection for form actions built in; this skill covers what SvelteKit doesn't)
- `clean-code` — General coding standards
- `testing-patterns` — Test pyramid, mocking strategies (SvelteKit-specific syntax above; general principles there)
- `playwright-cli` — Playwright CLI for advanced E2E debugging
- `frontend-ui-engineering` — Production-quality UI build patterns (relevant for `+page.svelte` components)
- `code-review-checklist` — 12-category code review checklist

---

## Dependencies

Required (installed by `npx sv create`):
- **Node.js** 20+ (or Bun 1.1+)
- **Svelte** 5.x
- **SvelteKit** 2.x
- **Vite** 5+ (build tool)
- **TypeScript** 5+ (default, can opt out but not recommended)

Common additions (install on demand):
- **Tailwind CSS** (`npm install -D tailwindcss @tailwindcss/vite`) — SvelteKit 2 + Tailwind 4 uses the Vite plugin
- **Drizzle ORM** (`npm install drizzle-orm`) — TypeScript-first ORM, pairs naturally with SvelteKit
- **Lucia** (`npm install lucia`) — session-based auth library (replaces Auth.js for SvelteKit)
- **@sveltejs/adapter-node** / **adapter-static** / **adapter-cloudflare** / **adapter-vercel** — swap as needed
- **Vitest** (`npm install -D vitest`) — unit/component testing (default in `sv create`)
- **Playwright** (`npm install -D @playwright/test`) — E2E testing (default in `sv create`)
- **svelte-check** (`npm install -D svelte-check`) — type-check + a11y audit (default in `sv create`)
- **@testing-library/svelte** (`npm install -D @testing-library/svelte`) — component testing utilities
- **zod** (`npm install zod`) — schema validation for form actions and API endpoints
