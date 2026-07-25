---
name: vue-3-nuxt
description: "Vue 3.5+ (Composition API) + Nuxt 4 full-stack TypeScript workflow skill. Covers the reactivity system (ref vs reactive, computed, watch vs watchEffect, automatic dependency tracking — fundamentally different from React hooks' manual dependency arrays), Single File Components (.vue with <script setup>), Nuxt 4 project structure (app/ directory, server/api/, nuxt.config.ts), file-based routing with definePageMeta, layout system, data fetching (useFetch, useAsyncData, $fetch), server routes via Nitro engine, Pinia for state management (the modern Vuex successor), nuxt-auth (Auth.js wrapper) or sidebase auth, Nitro deployment presets (Vercel / Cloudflare / Netlify / Node / static), layers for monorepo code sharing. Use when building any web app on Vue 3 or Nuxt 4 — especially when the task involves migrating Vue 2 Options API code to Composition API, choosing between ref and reactive, wiring Pinia stores, or setting up Nuxt server routes with the Nitro engine."
license: Proprietary. LICENSE.txt has complete terms
---

# Vue 3 + Nuxt 4 — Full-Stack TypeScript Workflow Skill

> **Target:** Vue 3.5+ (Composition API is the default; Options API still supported but not recommended for new code) + Nuxt 4.x (released 2025; the `app/` directory is the new default, replacing Nuxt 3's root-level directories). Vite is the build tool. TypeScript is the default. Pinia is the official state manager (Vuex is in maintenance mode).

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending a Vue 3 or Nuxt 4 application. Trigger phrases include "Vue 3", "Nuxt 4", "Composition API", "script setup", "ref", "reactive", "computed", "watchEffect", "Pinia", "defineProps", "defineEmits", "useFetch", "useAsyncData", "Nitro", "server/api", "nuxt.config.ts", "definePageMeta", "useRuntimeConfig", and any reference to a `.vue` Single File Component or a Nuxt `app/` directory layout.

Do **not** use this skill for:
- **Vue 2** — Composition API does not exist; the mental model is Options API + Vuex. Migrate to Vue 3 first.
- **Nuxt 3 with root-level directories** (no `app/` dir) — Nuxt 4 reorganized the structure; some patterns here assume the `app/` directory.
- **React / Svelte / Solid** — different frameworks, different reactivity models. See `svelte-5-sveltekit` for Svelte, `react19-ts6-vite8-tailwindv4-mvp` for React.
- **Vue 3 without Nuxt** (e.g., Vue + Vite SPA) — only the Composition API and SFC sections apply; routing/data-fetching sections assume Nuxt.

Cross-reference: `framework-templates` has a Vue section; this skill goes deep.

## Quick Start

```bash
# Create a new Nuxt 4 project (the canonical scaffolder)
npx nuxi@latest init my-app
# Prompts: package manager (pnpm / npm / yarn / bun), initialize git, install dependencies

cd my-app
pnpm install                  # or npm install / yarn install
pnpm dev                      # Dev server at http://localhost:3000
```

### Vue 3 only (without Nuxt) — for SPAs or embedded widgets

```bash
npm create vue@latest         # Official Vue 3 scaffolder (Vite-based)
# Prompts: TypeScript, JSX, Router, Pinia, Vitest, E2E testing, ESLint, Prettier
cd my-app
npm install
npm run dev                   # http://localhost:5173
```

### Key scripts (Nuxt 4 `package.json`)

```bash
pnpm dev                      # Nuxt dev server with HMR
pnpm build                    # Production build (.output/ directory)
pnpm preview                  # Preview the production build locally
pnpm postinstall              # Runs nuxt prepare (auto-runs on install)
pnpm test                     # Vitest (if configured)
pnpm typecheck                # vue-tsc type checking
```

---

## Project Structure (Nuxt 4 canonical layout)

Nuxt 4 introduced the `app/` directory as the new default for application code. This is the single biggest structural change from Nuxt 3.

```
my-app/
├── app/                        # ← NEW in Nuxt 4: application code lives here
│   ├── components/             # Auto-imported Vue components
│   ├── composables/            # Auto-imported composable functions
│   ├── layouts/                # Layout components (default.vue, custom.vue)
│   ├── middleware/             # Route middleware (auth.ts, guest.ts)
│   ├── pages/                  # File-based routing (index.vue, about.vue, posts/[slug].vue)
│   ├── plugins/                # Vue plugins (run on app startup)
│   ├── utils/                  # Auto-imported utility functions
│   ├── app.vue                 # Root component (<NuxtLayout><NuxtPage /></NuxtLayout>)
│   └── error.vue               # Custom error page (404, 500, etc.)
├── public/                     # Static assets served as-is (favicon, robots.txt)
├── server/                     # ← Server-only code (Nitro engine)
│   ├── api/                    # API routes (auto-mapped to /api/*)
│   │   ├── posts.get.ts        # GET /api/posts
│   │   ├── posts.post.ts       # POST /api/posts
│   │   └── [id].get.ts         # GET /api/posts/:id
│   ├── middleware/             # Server middleware (runs on every request)
│   ├── routes/                 # File-based server routes (non-/api)
│   └── plugins/                # Server plugins (run on Nitro startup)
├── shared/                     # ← NEW in Nuxt 4: code shared between app/ and server/
│   ├── types/                  # Shared TypeScript types
│   └── utils/                  # Shared utilities (auto-imported in both contexts)
├── assets/                     # Processed assets (CSS, images via Vite)
├── content/                    # @nuxt/content module (Markdown-based content)
├── layers/                     # Nuxt layers (extendable project modules)
├── nuxt.config.ts              # Nuxt configuration
├── app.config.ts               # Runtime public config (exposed to client)
├── tsconfig.json
└── package.json
```

### The `app/` directory revolution (Nuxt 4)

In Nuxt 3, `pages/`, `components/`, `composables/`, etc. lived at the project root. In Nuxt 4, they live under `app/`. This separation makes the project structure cleaner: `app/` is client+SSR code, `server/` is server-only, `shared/` is both. The Nuxt 3 → 4 migration tool moves these directories automatically.

### Auto-imports (the Nuxt magic)

Nuxt auto-imports:
- Components from `app/components/` (e.g., `app/components/PostCard.vue` → `<PostCard />` in any page)
- Composables from `app/composables/` (e.g., `app/composables/usePosts.ts` → `usePosts()` available everywhere)
- Utils from `app/utils/` and `shared/utils/`
- Vue 3 APIs (`ref`, `computed`, `watch`, `reactive`, `defineComponent`, etc.) — no `import { ref } from 'vue'` needed

This is the #1 thing that surprises newcomers. You can write a component that uses `ref()` without importing it. Auto-imports are configurable in `nuxt.config.ts` if you want to disable them for explicitness.

---

## Core Mental Model: Reactivity (the Vue 3 revolution)

Vue 3's reactivity system is **fundamentally different from React hooks**. The single biggest mental shift: **Vue tracks dependencies automatically; React requires explicit dependency arrays.**

### `ref` vs `reactive` — the two ways to create reactive state

#### `ref` — wraps any value (primitives OR objects)

```vue
<script setup lang="ts">
import { ref } from 'vue'  // (auto-imported in Nuxt — import shown for clarity)

const count = ref(0)              // ref<number>
const user = ref({ name: 'Alice', age: 30 })  // ref<{ name: string; age: number }>

function increment() {
  count.value++                   // ← .value is required for refs in <script>
  user.value.age++
}
</script>

<template>
  <!-- In <template>, .value is auto-unwrapped -->
  <button @click="increment">
    {{ count }} — {{ user.name }} is {{ user.age }}
  </button>
</template>
```

**Rule:** Use `ref` for primitives. Use `ref` for objects too if you want to replace the whole object (`user.value = newUser`). The `.value` access in `<script>` is the only friction.

#### `reactive` — wraps an object deeply (no `.value`)

```vue
<script setup lang="ts">
import { reactive } from 'vue'

const state = reactive({
  count: 0,
  user: { name: 'Alice', age: 30 }
})

function increment() {
  state.count++                   // ← no .value needed
  state.user.age++
}
</script>

<template>
  <button @click="increment">
    {{ state.count }} — {{ state.user.name }}
  </button>
</template>
```

**Rule:** Use `reactive` for grouped state objects. **Cannot** be used for primitives (`reactive(0)` does nothing). **Cannot** be reassigned (`state = newState` loses reactivity — you must mutate fields: `Object.assign(state, newState)`).

#### The decision rule

| Situation | Use |
|---|---|
| Primitive value (number, string, boolean) | `ref` |
| Object you might replace wholesale | `ref` |
| Grouped state object (like a form) | `reactive` |
| Coming from React `useState` | `ref` (closest analog) |

**Opinionated default:** prefer `ref` for new code. The `.value` friction is minor and `ref` works for all types. `reactive` is fine for form-state objects.

### `computed` — derived state (like React useMemo, but automatic)

```vue
<script setup lang="ts">
import { ref, computed } from 'vue'

const count = ref(0)
const doubled = computed(() => count.value * 2)         // Read-only
const parity = computed(() => (count.value % 2 === 0 ? 'even' : 'odd'))

// Writable computed (rare — for v-model on computed values)
const displayName = computed({
  get: () => user.value.name,
  set: (val) => { user.value.name = val.toUpperCase() }
})
</script>

<template>
  <button @click="count++">{{ count }}</button>
  <p>Doubled: {{ doubled }} ({{ parity }})</p>
</template>
```

**Key difference from React `useMemo`:** Vue's `computed` caches the result and only recomputes when its dependencies change. There is no dependency array — Vue's reactivity proxy tracks which refs were accessed during the computation. You cannot forget a dependency (the #1 React hooks bug).

### `watch` vs `watchEffect` — side effects

```vue
<script setup lang="ts">
import { ref, watch, watchEffect } from 'vue'

const count = ref(0)
const user = ref({ name: 'Alice' })

// watch: explicit source — runs only when `count` changes
watch(count, (newVal, oldVal) => {
  console.log(`Count: ${oldVal} → ${newVal}`)
})

// watch multiple sources
watch([count, () => user.value.name], ([newCount, newName]) => {
  console.log(`Count: ${newCount}, Name: ${newName}`)
})

// watch with deep option for objects
watch(user, (newUser) => {
  console.log('User changed:', newUser)
}, { deep: true })                // ← required to watch nested changes

// watchEffect: automatic dependency tracking — runs immediately, re-runs when any accessed ref changes
watchEffect(() => {
  console.log(`Count is ${count.value}, name is ${user.value.name}`)
  // Vue tracks that this effect reads count.value and user.value.name
})
</script>
```

| Watcher | When to use |
|---|---|
| `watch` | You want to react to a specific source, access old value, or defer the run |
| `watchEffect` | You want automatic dependency tracking (no source list), runs immediately |
| `watch(callback, { flush: 'post' })` | You need to run after DOM update (default is 'pre') |

### Single File Components (`.vue`)

```vue
<!-- PostCard.vue -->
<script setup lang="ts">
// Props (defineProps is a compile-time macro — no import needed)
interface Props {
  post: { id: string; title: string; body: string; author: { name: string } }
  featured?: boolean
}
const props = withDefaults(defineProps<Props>(), {
  featured: false
})

// Emits (defineEmits is also a compile-time macro)
const emit = defineEmits<{
  'click': [postId: string]
  'bookmark': [post: Props['post']]
}>()

// Two-way binding opt-in (defineModel is the Vue 3.4+ way)
const title = defineModel<string>('title')

// Local state
import { ref, computed } from 'vue'
const isExpanded = ref(false)
const excerpt = computed(() => props.post.body.slice(0, 100) + '...')
</script>

<template>
  <article :class="{ 'post-card': true, 'post-card--featured': featured }">
    <h3 @click="emit('click', post.id)">{{ post.title }}</h3>
    <p v-if="isExpanded">{{ post.body }}</p>
    <p v-else>{{ excerpt }}</p>
    <button @click="isExpanded = !isExpanded">
      {{ isExpanded ? 'Show less' : 'Show more' }}
    </button>
    <button @click="emit('bookmark', post)">Bookmark</button>
    <footer>By {{ post.author.name }}</footer>
  </article>
</template>

<style scoped>
/* Scoped styles — only apply to this component's elements */
.post-card {
  border: 1px solid #e5e7eb;
  padding: 1rem;
  border-radius: 0.5rem;
}
.post-card--featured {
  border-color: #f59e0b;
  background: #fffbeb;
}
</style>
```

The `<script setup>` syntax is the modern default. It's syntactic sugar that:
- Auto-exposes all top-level bindings to `<template>` (no `return` statement)
- Makes `defineProps`, `defineEmits`, `defineModel`, `defineExpose` available as compile-time macros
- Is more concise than the Options API

---

## Routing & Pages (Nuxt 4)

Nuxt routing is **file-system based** under `app/pages/`. The directory structure IS the URL structure.

### Route types

| URL | Page file |
|---|---|
| `/` | `app/pages/index.vue` |
| `/about` | `app/pages/about.vue` |
| `/posts/:slug` | `app/pages/posts/[slug].vue` |
| `/posts/[id]` (catch-all) | `app/pages/posts/[...id].vue` |
| `/users/[id]` (matcher) | `app/pages/users/[id].int.vue` (integers only) |

### `definePageMeta` — per-route config

```vue
<!-- app/pages/posts/[slug].vue -->
<script setup lang="ts">
// definePageMeta is a compile-time macro — runs before the component is created
definePageMeta({
  layout: 'blog',                   // Use layouts/blog.vue instead of default
  middleware: ['auth'],             // Run app/middleware/auth.ts before rendering
  title: 'Post Detail',             // Custom meta — accessible via route.meta
  key: (route) => route.params.slug // Cache key for keep-alive
})

// useRoute gives access to the current route
const route = useRoute()
const slug = computed(() => route.params.slug as string)
</script>
```

### Layouts

```vue
<!-- app/layouts/default.vue -->
<template>
  <div class="app-shell">
    <AppHeader />
    <main>
      <slot />                       <!-- ← Page content goes here -->
    </main>
    <AppFooter />
  </div>
</template>
```

```vue
<!-- app/layouts/blog.vue -->
<template>
  <div class="blog-shell">
    <BlogSidebar />
    <main>
      <slot />
    </main>
  </div>
</template>
```

Switch layout per-page via `definePageMeta({ layout: 'blog' })`.

### Route middleware

```typescript
// app/middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const { loggedIn } = useUserSession()

  if (!loggedIn.value) {
    return navigateTo('/login?redirect=' + encodeURIComponent(to.fullPath))
  }
})
```

Middleware runs on the server during SSR and on the client during navigation. Return `navigateTo()` to redirect, or nothing to continue.

---

## Data Fetching

Nuxt 4 provides 3 composable functions for data fetching. Choosing the right one matters.

### `useFetch` — for one-off fetches tied to component lifecycle

```vue
<script setup lang="ts">
// Auto-deduplicates, auto-keyed by URL, refetches on URL change, SSR-friendly
const { data: posts, pending, error, refresh } = await useFetch('/api/posts')

// With options
const { data: userPosts } = await useFetch('/api/posts', {
  query: { authorId: '123', status: 'published' },
  method: 'GET',
  headers: { 'Accept': 'application/json' },
  transform: (posts: Post[]) => posts.slice(0, 10),
  default: () => [],                  // Initial value while loading
  watch: [someRef],                  // Refetch when someRef changes
  server: true,                      // Run on server (SSR) — default true
  lazy: false,                       // If true, don't block navigation — default false
})
</script>
```

### `useAsyncData` — for non-fetch async work (or custom fetchers)

```vue
<script setup lang="ts">
// Use when you need to call a function that's NOT $fetch (e.g., direct DB call in server route)
const { data } = await useAsyncData('posts', () => $fetch('/api/posts'))

// With a custom handler (e.g., calling a composable that wraps a server function)
const { data: stats } = await useAsyncData(
  'post-stats',
  () => $fetch('/api/posts/stats'),
  { transform: (s) => ({ total: s.count, avg: s.average }) }
)
</script>
```

### `$fetch` — for one-off fetches NOT tied to component lifecycle

```typescript
// In an event handler, server route, or non-setup context
async function submitForm() {
  const result = await $fetch('/api/posts', {
    method: 'POST',
    body: { title: 'New Post', body: 'Hello' }
  })
}
```

**Do NOT** use `$fetch` in component setup — use `useFetch` instead. `$fetch` doesn't deduplicate, doesn't handle SSR, and won't serialize state from server to client.

### Decision matrix

| Situation | Use |
|---|---|
| Fetch data when component mounts, refresh on param change | `useFetch` |
| Async work that's not a fetch (DB call, complex transform) | `useAsyncData` |
| Fetch triggered by user action (button click, form submit) | `$fetch` |
| Fetch inside a Pinia store action | `$fetch` |

---

## Server Routes (Nitro engine)

Nuxt 4's server engine is **Nitro** — a standalone server runtime that powers Nuxt's SSR and API routes. Server routes live in `server/` and are NOT auto-imported (unlike `app/` code).

### API routes

```typescript
// server/api/posts.get.ts  →  GET /api/posts
import { db } from '~~/server/utils/db'  // Server-only util (~~ alias points to project root)

export default defineEventHandler(async (event) => {
  const query = getQuery(event)
  const status = query.status as string | undefined

  const posts = await db.post.findMany({
    where: status ? { status } : undefined,
    orderBy: { createdAt: 'desc' }
  })

  return posts   // Auto-serialized to JSON
})

// server/api/posts.post.ts  →  POST /api/posts
export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  // Validate body (use zod for production)
  const post = await db.post.create({ data: body })
  setResponseStatus(event, 201)
  return post
})

// server/api/posts/[id].get.ts  →  GET /api/posts/:id
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')!
  const post = await db.post.findUnique({ where: { id } })

  if (!post) {
    throw createError({ statusCode: 404, statusMessage: 'Post not found' })
  }

  return post
})
```

### Server middleware

```typescript
// server/middleware/auth.ts  →  runs before every server route
import { getToken } from '~~/server/utils/auth'

export default defineEventHandler(async (event) => {
  // Skip auth for public routes
  if (event.path.startsWith('/api/public')) return

  const token = getToken(event)
  if (!token) {
    throw createError({ statusCode: 401, statusMessage: 'Unauthorized' })
  }

  // Attach to event.context for downstream handlers
  event.context.user = await getUserFromToken(token)
})
```

### Server-only utils

Place server-only code in `server/utils/`. These files can be imported via the `~~/server/utils/` alias and are guaranteed to never end up in the client bundle.

```typescript
// server/utils/db.ts
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()
export const db = prisma   // Singleton — Nitro keeps this alive across requests
```

---

## State Management: Pinia (the modern Vuex)

Pinia is the official state manager for Vue 3. Vuex is in maintenance mode — do not use it for new projects.

```bash
npx nuxi module add pinia       # Adds @pinia/nuxt to nuxt.config.ts and installs
```

### Define a store (Setup Store syntax — recommended)

```typescript
// app/stores/cart.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  // State
  const items = ref<Array<{ id: string; name: string; price: number; qty: number }>>([])

  // Getters (computed)
  const total = computed(() => items.value.reduce((sum, i) => sum + i.price * i.qty, 0))
  const count = computed(() => items.value.reduce((sum, i) => sum + i.qty, 0))
  const isEmpty = computed(() => items.value.length === 0)

  // Actions
  function add(item: { id: string; name: string; price: number }) {
    const existing = items.value.find((i) => i.id === item.id)
    if (existing) existing.qty++
    else items.value.push({ ...item, qty: 1 })
  }

  function remove(id: string) {
    items.value = items.value.filter((i) => i.id !== id)
  }

  function clear() {
    items.value = []
  }

  // Async action
  async function checkout() {
    const result = await $fetch('/api/checkout', {
      method: 'POST',
      body: { items: items.value }
    })
    clear()
    return result
  }

  return { items, total, count, isEmpty, add, remove, clear, checkout }
})
```

### Use the store in a component

```vue
<script setup lang="ts">
import { useCartStore } from '~/stores/cart'
import { storeToRefs } from 'pinia'

const cart = useCartStore()

// Destructure with reactivity preserved (storeToRefs is required — plain destructuring loses reactivity)
const { total, count, isEmpty } = storeToRefs(cart)

// Actions can be destructured directly (they're plain functions)
const { add, remove, checkout } = cart
</script>

<template>
  <div v-if="!isEmpty">
    <p>{{ count }} items — ${{ total.toFixed(2) }}</p>
    <button @click="checkout">Checkout</button>
  </div>
  <p v-else>Your cart is empty</p>
</template>
```

**Iron rule:** Always use `storeToRefs()` to destructure state and getters from a Pinia store. Plain destructuring (`const { total } = cart`) loses reactivity — `total` becomes a snapshot, not a live value.

---

## Environment Variables & Runtime Config

Nuxt exposes env vars via `useRuntimeConfig()` — a typed config object available on both server and client.

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  runtimeConfig: {
    // Server-only (private) — NEVER exposed to client
    databaseUrl: '',                // Set via NUXT_DATABASE_URL env var
    stripeSecretKey: '',            // Set via NUXT_STRIPE_SECRET_KEY

    // Public (client-safe) — exposed to client
    public: {
      appName: 'My App',            // Set via NUXT_PUBLIC_APP_NAME
      stripePublishableKey: '',     // Set via NUXT_PUBLIC_STRIPE_PUBLISHABLE_KEY
    }
  }
})
```

```typescript
// In a server route (server/api/*)
export default defineEventHandler((event) => {
  const config = useRuntimeConfig(event)
  // config.databaseUrl        ← server-only, safe
  // config.stripeSecretKey    ← server-only, safe
  // config.public.appName     ← also accessible here
})

// In a component (app/**/*.vue)
<script setup lang="ts">
const config = useRuntimeConfig()
// config.public.appName           ← accessible
// config.public.stripePublishableKey  ← accessible
// config.databaseUrl              ← UNDEFINED on client (good — secret stays secret)
</script>
```

**Iron rule:** Anything under `runtimeConfig` (not `runtimeConfig.public`) is server-only. Nuxt will NOT bundle it into the client, but you must not log it or return it from a server route either.

---

## Authentication

### Option A: `nuxt-auth` (Auth.js wrapper, session-based)

```bash
npx nuxi module add auth
```

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@sidebase/nuxt-auth'],
  auth: {
    provider: {
      type: 'authjs',
      // Configure Auth.js providers here
    }
  }
})
```

```typescript
// server/auth/[...].ts  →  Auth.js handler
import NextAuth from 'next-auth'
import GitHub from 'next-auth/providers/github'

const handler = NextAuth({
  providers: [
    GitHub({ clientId: '...', clientSecret: '...' })
  ],
  session: { strategy: 'jwt' }
})

export { handler as GET, handler as POST }
```

### Option B: Custom session-based auth (lighter, no Auth.js dependency)

```typescript
// server/utils/auth.ts
import { createHash, randomBytes } from 'node:crypto'

export async function createSession(userId: string) {
  const token = randomBytes(32).toString('hex')
  await db.session.create({
    data: {
      token: createHash('sha256').update(token).digest('hex'),
      userId,
      expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)  // 7 days
    }
  })
  return token
}

export async function getUserFromToken(token: string | undefined) {
  if (!token) return null
  const hashed = createHash('sha256').update(token).digest('hex')
  const session = await db.session.findUnique({
    where: { token: hashed },
    include: { user: true }
  })
  if (!session || session.expiresAt < new Date()) return null
  return session.user
}
```

```typescript
// server/middleware/auth.ts
export default defineEventHandler(async (event) => {
  const token = getCookie(event, 'session')
  const user = await getUserFromToken(token)
  event.context.user = user   // Available in all downstream handlers
})
```

```vue
<!-- app/composables/useUser.ts -->
export function useUser() {
  const user = useState<User | null>('user', () => null)

  async function fetchUser() {
    user.value = await $fetch('/api/me')
  }

  async function login(email: string, password: string) {
    const { token } = await $fetch('/api/login', { method: 'POST', body: { email, password } })
    await fetchUser()
  }

  async function logout() {
    await $fetch('/api/logout', { method: 'POST' })
    user.value = null
    navigateTo('/login')
  }

  return { user, fetchUser, login, logout }
}
```

---

## Deployment (Nitro presets)

Nuxt builds to a Nitro server that can deploy to many targets. Configure in `nuxt.config.ts`:

```typescript
export default defineNuxtConfig({
  nitro: {
    preset: 'node-server'   // or 'vercel', 'cloudflare', 'netlify', 'static', 'vercel-edge'
  }
})
```

| Preset | Use |
|---|---|
| `node-server` (default) | Self-hosted Node server (Docker, VPS). Output: `.output/server/index.mjs` |
| `vercel` | Vercel with edge functions |
| `cloudflare` | Cloudflare Pages/Workers |
| `netlify` | Netlify with functions |
| `static` (or `cloudflare-pages-static`) | Pre-render entire site. Only works if every route can be prerendered. |
| `vercel-edge` | Vercel Edge Runtime |
| `bun` | Bun's native runtime |
| `deno` | Deno Deploy |

```bash
pnpm build                     # Output: .output/ directory
pnpm preview                   # Preview the build locally

# Node server in production
node .output/server/index.mjs

# Static prerender (if preset is 'static')
pnpm build                     # Generates .output/public/ with static HTML files
```

For SSR with a database, use `node-server` (self-host) or `vercel`/`cloudflare` (managed). For static sites, use `static` and mark every route as prerenderable.

---

## Testing (Vitest + Vue Test Utils + Playwright)

```bash
npx nuxi module add vitest       # Adds @nuxt/test-utils + vitest
pnpm add -D @vue/test-utils @testing-library/vue
pnpm add -D @playwright/test
```

### Component tests with Vitest + Vue Test Utils

```typescript
// tests/Counter.test.ts
import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import Counter from '~/components/Counter.vue'

describe('Counter', () => {
  it('increments on click', async () => {
    const wrapper = mount(Counter)
    expect(wrapper.text()).toContain('0')
    await wrapper.find('button').trigger('click')
    expect(wrapper.text()).toContain('1')
  })
})
```

### E2E tests with Playwright

```typescript
// tests/e2e/posts.spec.ts
import { test, expect } from '@playwright/test'

test('user can publish a post', async ({ page }) => {
  await page.goto('/posts/new')
  await page.fill('input[name="title"]', 'My Test Post')
  await page.fill('textarea[name="body"]', 'Hello world')
  await page.click('button[type="submit"]')
  await expect(page).toHaveURL(/\/posts\/.+/)
  await expect(page.locator('h1')).toContainText('My Test Post')
})
```

Cross-reference: `testing-patterns` for general test pyramid / mocking. Cross-reference: `playwright-cli` for advanced Playwright debugging.

---

## Top 10 Anti-Patterns (the most valuable section)

1. **Destructuring `reactive()` loses reactivity.** `const { count } = reactive({ count: 0 })` makes `count` a plain number — mutating it does NOT trigger updates. Use `toRefs()` to convert reactive fields to refs first: `const { count } = toRefs(state)`.

2. **Mutating props directly.** In Vue, props are read-only. Mutating `props.foo = 'bar'` throws a warning in dev and breaks in prod. Use `defineModel()` for two-way binding, or emit an event to ask the parent to update.

3. **Missing `key` in `v-for`.** Vue uses `key` to track list items across re-renders. Without a stable `key` (use a unique ID, not the array index), Vue may reuse the wrong DOM node and you'll see stale state. Always: `<div v-for="item in items" :key="item.id">`.

4. **Using `v-if` and `v-for` on the same element.** This is always wrong — `v-for` has higher priority so `v-if` runs once per iteration, not once for the whole list. Wrap in a `<template v-for>` or compute the filtered list upstream.

5. **Using `$fetch` in component setup.** `$fetch` doesn't deduplicate, doesn't handle SSR, and won't serialize state from server to client. Use `useFetch` (for fetches tied to component lifecycle) or `useAsyncData` (for non-fetch async work) in setup. Reserve `$fetch` for event handlers and Pinia actions.

6. **Importing server-only code into client code.** Code in `server/` must never be imported into `app/` — Nuxt will throw an error. Use `shared/` for code that needs to run in both contexts. If you need server-only logic in a component, fetch it via an API route.

7. **Forgetting `storeToRefs()` when destructuring Pinia stores.** `const { total } = useCartStore()` makes `total` a snapshot — it won't update. Always use `const { total } = storeToRefs(useCartStore())` for state and getters.

8. **Putting secrets in `runtimeConfig.public`.** Anything under `runtimeConfig.public` is bundled into the client and visible to anyone who opens dev tools. Use `runtimeConfig.databaseUrl` (server-only) for secrets, `runtimeConfig.public.appName` for public values.

9. **Using Vuex for new projects.** Vuex is in maintenance mode. Pinia is the official Vue 3 state manager — better TypeScript support, simpler API, smaller bundle. Existing Vuex 4 code works on Vue 3, but new stores should use Pinia.

10. **Forgetting that `watch` on `reactive()` requires `{ deep: true }`.** By default, `watch(state, cb)` only fires when the top-level reference changes (which can't happen for `reactive()`). Use `watch(state, cb, { deep: true })` to watch nested mutations, or watch a getter: `watch(() => state.count, cb)`.

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for Vue/Nuxt (project onboarding)
- `svelte-5-sveltekit` — Svelte 5 + SvelteKit 2 (similar file-based routing, different reactivity model — useful for comparison)
- `api-and-interface-design` — Type contract design (relevant for `server/api/*` routes)
- `api-patterns` — REST API patterns (for Nuxt server routes)
- `security-and-hardening` — OWASP-aware hardening
- `clean-code` — General coding standards
- `testing-patterns` — Test pyramid, mocking strategies
- `playwright-cli` — Playwright CLI for advanced E2E debugging
- `frontend-ui-engineering` — Production-quality UI build patterns
- `code-review-checklist` — 12-category code review checklist

---

## Dependencies

Required (installed by `npx nuxi init`):
- **Node.js** 20+ (or Bun 1.1+)
- **Vue** 3.5+
- **Nuxt** 4.x
- **Vite** 5+ (build tool, bundled with Nuxt)
- **Nitro** 2+ (server engine, bundled with Nuxt)
- **TypeScript** 5+ (default, can opt out but not recommended)

Common additions (install on demand):
- **Pinia** + **@pinia/nuxt** — state management (`npx nuxi module add pinia`)
- **@nuxt/content** — Markdown-based content (docs, blogs)
- **@nuxt/image** — Optimized images (next-gen formats, responsive)
- **@nuxt/ui** — Official UI component library (Tailwind-based)
- **@sidebase/nuxt-auth** — Auth.js wrapper for Nuxt
- **Drizzle ORM** (`pnpm add drizzle-orm`) — TypeScript-first ORM, pairs naturally with Nuxt server routes
- **zod** (`pnpm add zod`) — Schema validation for server routes
- **@vue/test-utils** + **@testing-library/vue** — component testing
- **@playwright/test** — E2E testing
- **vue-tsc** — TypeScript checking for Vue SFCs
- **Tailwind CSS** (`pnpm add -D @nuxtjs/tailwindcss` + `npx nuxi module add tailwindcss`) — utility-first CSS
