---
name: solidstart
description: "SolidStart 1 (SolidJS 1.9+, released 2024) full-stack TypeScript framework workflow skill — signals-based reactivity without a virtual DOM. Covers the fine-grained reactivity mental model (createSignal returns a getter+setter — calling the getter tracks the dependency, calling the setter triggers ONLY the effects that read it; no component re-renders, no virtual DOM diffing, no fiber tree — the opposite of React's model), the SolidJS primitives (createSignal, createMemo, createEffect, createResource for async, createStore for nested objects, on for explicit dependencies, batch for grouping updates), JSX compilation (Solid compiles JSX to direct DOM operations — no React.createElement, no reconciliation), SolidStart 1 conventions (file-based routing in src/routes/, server functions 'use server' for RPC, server-only modules in src/server/, load functions for data fetching, useNavigate/useParams for navigation), the meta package (Title, Meta, Link for document head), Vinxi build tool (Vite-based, handles SSR + client + server bundles), deployment adapters (Vercel, Cloudflare, Netlify, Node, static), the islands-with-streaming story (Solid streams HTML and hydrates only interactive parts), and the comparison with React (same JSX syntax, completely different execution model). Use when building any full-stack TypeScript web app where React's re-render model is a performance bottleneck — especially when the task involves createSignal/createEffect patterns, server functions ('use server'), file-based routing, or migrating from React where idiomatic Solid (fine-grained signals, no virtual DOM, compile-time JSX optimization) differs fundamentally from React (component re-renders, virtual DOM diffing, hooks rules)."
license: Proprietary. LICENSE.txt has complete terms
---

# SolidStart 1 (SolidJS) — Signals-Based Full-Stack TypeScript

> **Target:** SolidStart 1.0+ (released 2024) on SolidJS 1.9+ with TypeScript 5+. SolidStart is the full-stack meta-framework for SolidJS — file-based routing, server functions, SSR, and deployment adapters. SolidJS's distinctive paradigm: **fine-grained reactivity via signals, no virtual DOM, no component re-renders.** JSX compiles to direct DOM operations at build time. Same JSX syntax as React, completely different execution model.

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending a SolidStart or SolidJS application. Trigger phrases include "Solid", "SolidJS", "SolidStart", "createSignal", "createMemo", "createEffect", "createResource", "createStore", "signals", "fine-grained reactivity", "no virtual DOM", "'use server'", "server function", "useNavigate", "useParams", "Vinxi", "@solidjs/router", "@solidjs/meta", "solid-js/web", and any reference to a `src/routes/` directory with `route.tsx` / `page.tsx` files or the `createSignal` API.

Do **not** use this skill for:
- **React / Next.js** — different reactivity model (React re-renders components; Solid re-runs only the effects that depend on a signal). See Next.js skills.
- **Vue 3 / Nuxt** — Vue also has reactivity but via Proxies (different mechanism). See `vue-3-nuxt` skill.
- **Svelte 5 / SvelteKit** — Svelte 5 runes are conceptually similar to Solid signals but with different syntax and compile-time vs runtime trade-offs. See `svelte-5-sveltekit` skill.
- **Plain SolidJS (without SolidStart)** — only the reactivity + component sections apply; the routing/server-functions sections assume SolidStart.

Cross-reference: `svelte-5-sveltekit` is the closest comparable framework (both are signals-based, both have file-based routing, both ship less JS than React). The mental models are similar but the syntax and compilation differ.

## Quick Start

```bash
# Create a new SolidStart project
npx degit solidjs/templates/start my-app
# OR the interactive scaffolder:
npm create solid@latest

cd my-app
npm install
npm run dev             # Dev server at http://localhost:3000

# Build for production
npm run build           # Outputs to .output/ (Vinxi build)
npm run start           # Run the production build
```

### Key commands

```bash
npm run dev             # Dev server with HMR
npm run build           # Production build (Vinxi → .output/)
npm run start           # Run the production server
npm run preview         # Preview the production build locally

# The SolidStart VS Code extension is recommended for JSX IntelliSense
```

### SolidStart project structure

```
my-app/
├── src/
│   ├── routes/              # ← File-based routing (Vinxi)
│   │   ├── index.tsx        # / (home page)
│   │   ├── about.tsx        # /about
│   │   ├── users/
│   │   │   ├── index.tsx    # /users (list)
│   │   │   └── [id].tsx     # /users/:id (dynamic)
│   │   └── api/
│   │       └── users.ts     # /api/users (API route)
│   ├── components/          # Reusable Solid components
│   │   ├── Counter.tsx
│   │   └── UserCard.tsx
│   ├── lib/                 # Shared utilities
│   │   └── api.ts
│   ├── server/              # Server-only modules
│   │   ├── db.ts            # Database client (NEVER imported by client code)
│   │   └── auth.ts          # Auth utilities
│   ├── entry-client.tsx     # Client entry (hydration)
│   ├── entry-server.tsx     # Server entry (SSR)
│   ├── app.tsx              # Root component (Router + Providers)
│   └── global.d.ts          # Type declarations
├── public/                  # Static assets
├── app.config.ts            # ← SolidStart config (adapters, plugins)
├── tsconfig.json
├── package.json
└── Dockerfile
```

```typescript
// app.config.ts — SolidStart config
import { defineConfig } from '@solidjs/start/config';
import node from '@solidjs/start/node';      // Node adapter
// import vercel from '@solidjs/start/vercel';
// import cloudflare from '@solidjs/start/cloudflare';
// import netlify from '@solidjs/start/netlify';

export default defineConfig({
  server: {
    preset: 'node-server',       // or 'vercel', 'cloudflare', 'netlify', 'static'
    // adapter: node(),           // Alternative to preset
  },
  ssr: true,                     // Enable SSR (default)
});
```

---

## Core Mental Model: Fine-Grained Signals + No Virtual DOM + Compile-Time JSX

Solid's distinctive paradigm is **signals drive fine-grained updates — no component re-renders, no virtual DOM diffing.** Four things differentiate Solid from React:

### 1. Signals track dependencies automatically (no hooks rules, no re-renders)

```tsx
import { createSignal, createEffect } from 'solid-js';

function Counter() {
  const [count, setCount] = createSignal(0);    // Returns getter + setter
  const [name, setName] = createSignal('Alice');

  // createEffect re-runs ONLY when count() changes — NOT when name() changes
  createEffect(() => {
    console.log('Count is:', count());          // Calling count() tracks it
  });

  // This effect depends on name() — re-runs only when name() changes
  createEffect(() => {
    console.log('Name is:', name());
  });

  return (
    <div>
      <p>{count()} — {name()}</p>               {/* Calling getters in JSX */}
      <button onClick={() => setCount(c => c + 1)}>+1</button>
      <button onClick={() => setName('Bob')}>Rename</button>
    </div>
  );
}
```

**Critical difference from React:**
- In React, `setCount(c => c + 1)` triggers a **component re-render** — the entire `Counter` function runs again, including all JSX.
- In Solid, `setCount(c => c + 1)` triggers **only the specific DOM updates** that depend on `count()`. The `Counter` function runs **once** (at component creation). The `createEffect` for count re-runs; the one for name doesn't. The `<p>{count()}</p>` text node updates; nothing else does.

This is **fine-grained reactivity** — updates are scoped to the exact dependency, not the component. Solid's benchmarks show ~3-5x faster updates than React for fine-grained state changes.

### 2. The getter pattern (calling the signal reads its value)

```tsx
// Solid — signals are getter functions
const [count, setCount] = createSignal(0);

// READ — call the getter
console.log(count());         // 0
const doubled = count() * 2;  // Evaluates immediately (not reactive)

// In JSX — call the getter
return <p>{count()}</p>;      // Updates reactively

// In createEffect/createMemo — calling the getter tracks the dependency
createEffect(() => {
  console.log(count());       // This effect re-runs when count() changes
});
```

```tsx
// React — state is a value
const [count, setCount] = useState(0);

// READ — it's a value
console.log(count);           // 0
const doubled = count * 2;    // Evaluates immediately

// In JSX — use the value directly
return <p>{count}</p>;        // Updates on re-render

// In useEffect — but you must list count in the deps array
useEffect(() => {
  console.log(count);         // Only re-runs if [count] is the deps array
}, [count]);
```

The `()` (calling the getter) is the #1 thing that trips up React developers new to Solid. You write `count()` everywhere, not `count`. This is because Solid signals are functions — calling them both reads the value AND registers the dependency (if called inside a tracking scope like `createEffect`).

### 3. No hooks rules (call signals anywhere, any time, any order)

React hooks have strict rules:
- Only call hooks at the top level (no loops, conditions, nested functions)
- Only call hooks from React functions (components or custom hooks)

Solid has **no such rules**. Signals are just values — create them anywhere:

```tsx
// Solid — completely legal (would break React's hooks rules)
function Counter() {
  if (Math.random() > 0.5) {
    const [lucky, setLucky] = createSignal(true);  // Conditional signal — fine!
  }

  const [count, setCount] = createSignal(0);

  // Signal inside a callback — fine!
  const handleClick = () => {
    const [clicks, setClicks] = createSignal(0);   // Signal in event handler
    setClicks(c => c + 1);
  };

  // Signal in a loop — fine!
  for (let i = 0; i < 3; i++) {
    const [value, setValue] = createSignal(i);
  }

  return <button onClick={() => setCount(c => c + 1)}>{count()}</button>;
}
```

This is because Solid signals don't rely on call-order tracking (React's hooks do). Each `createSignal` creates an independent reactive primitive. You can create them conditionally, in loops, in event handlers — anywhere.

### 4. JSX compiles to direct DOM operations (no virtual DOM)

```tsx
// This JSX:
function Counter() {
  const [count, setCount] = createSignal(0);
  return <button onClick={() => setCount(c => c + 1)}>{count()}</button>;
}

// Compiles (at build time) to something like:
function Counter() {
  const [count, setCount] = createSignal(0);
  const _el$ = document.createElement('button');
  _el$.addEventListener('click', () => setCount(c => c + 1));
  // This is the magic — insertExpression sets up a reactive effect
  // that updates _el$.textContent when count() changes
  insert(_el$, count);
  return _el$;
}
```

Solid compiles JSX to **direct DOM operations** (`document.createElement`, `addEventListener`, `insert`). There's no `React.createElement` call tree, no virtual DOM, no reconciliation. When `count()` changes, Solid directly updates `_el$.textContent` — no diffing.

**Implication:** Solid components run their function body **exactly once** (at creation). The JSX is set up with reactive effects that update DOM properties directly. This is why Solid is faster than React for updates — there's no re-render, no diff, no commit phase.

---

## Solid Primitives

### `createSignal` — reactive value

```tsx
const [count, setCount] = createSignal(0);
const [user, setUser] = createSignal({ name: 'Alice', age: 30 });

// Read
console.log(count());                    // 0
console.log(user().name);                // Alice

// Write
setCount(5);                             // Set to 5
setCount(c => c + 1);                    // Update via function
setUser(u => ({ ...u, age: u.age + 1 }));  // Immutable update (recommended for objects)
```

### `createMemo` — derived value (like useMemo, but automatic)

```tsx
const [count, setCount] = createSignal(2);
const doubled = createMemo(() => count() * 2);   // Recomputes only when count() changes
const quadrupled = createMemo(() => doubled() * 2);  // Chained memos

console.log(doubled());                  // 4
console.log(quadrupled());               // 8

setCount(5);
console.log(doubled());                  // 10 (recomputed)
console.log(quadrupled());               // 20 (recomputed)
```

`createMemo` caches the result and only recomputes when its dependencies change. Unlike React's `useMemo`, there's no dependency array — Solid tracks automatically.

### `createEffect` — side effect (like useEffect, but scoped)

```tsx
const [count, setCount] = createSignal(0);

// Runs immediately, then re-runs whenever count() changes
createEffect(() => {
  console.log('Count:', count());
  document.title = `Count: ${count()}`;
});

// With cleanup (use onCleanup inside the effect)
createEffect(() => {
  const interval = setInterval(() => setCount(c => c + 1), 1000);
  onCleanup(() => clearInterval(interval));   // Runs before re-run or on dispose
});

// With explicit dependencies (use on())
createEffect(on(count, (newCount, prevCount) => {
  console.log(`Count: ${prevCount} → ${newCount}`);
}));
```

### `createResource` — async data (like useQuery + Suspense)

```tsx
import { createResource, Suspense } from 'solid-js';

// Fetcher function — async, returns Promise
async function fetchUser(id: string): Promise<User> {
  const res = await fetch(`/api/users/${id}`);
  return res.json();
}

function UserProfile({ id }: { id: string }) {
  const [user] = createResource(() => id, fetchUser);
  // user() returns: undefined (loading) | User (loaded) | Error (thrown)

  return (
    <Suspense fallback={<p>Loading...</p>}>
      <div>
        {user() && (
          <>
            <h1>{user()!.name}</h1>
            <p>{user()!.email}</p>
          </>
        )}
      </div>
    </Suspense>
  );
}

// With a refetch + mutate (for mutations)
const [user, { refetch, mutate }] = createResource(() => id, fetchUser);

// Refetch on demand
<button onClick={() => refetch()}>Refresh</button>

// Optimistic update
mutate({ ...user()!, name: 'New Name' });
```

### `createStore` — nested reactive objects

```tsx
import { createStore, produce } from 'solid-js/store';

const [state, setState] = createStore({
  users: [
    { id: 1, name: 'Alice', posts: [{ id: 1, title: 'Hello' }] },
    { id: 2, name: 'Bob', posts: [] },
  ],
  selectedId: 1,
});

// Read (reactive — only the accessed property is tracked)
console.log(state.users[0].name);         // Alice
console.log(state.users[state.selectedId - 1].posts[0].title);  // Hello

// Write — fine-grained (only the changed path triggers updates)
setState('users', 0, 'name', 'Alice Smith');         // Update nested field
setState('users', 0, 'posts', 1, { id: 2, title: 'World' });  // Add post
setState('selectedId', 2);                            // Update root field

// Immutable update via produce (like Immer)
setState(produce(s => {
  s.users[0].name = 'Alice Smith';
  s.users.push({ id: 3, name: 'Carol', posts: [] });
}));
```

`createStore` makes **nested properties reactive** — accessing `state.users[0].name` tracks only that specific property. Updating `state.users[0].name` triggers only effects that read that exact path. This is fine-grained reactivity applied to objects.

### `batch` — group updates into one notification

```tsx
import { batch } from 'solid-js';

const [count, setCount] = createSignal(0);
const [name, setName] = createSignal('Alice');

// Without batch — two separate update cycles
setCount(1);
setName('Bob');

// With batch — one update cycle (effects run once)
batch(() => {
  setCount(1);
  setName('Bob');
});
```

### `on` — explicit dependencies (opt out of automatic tracking)

```tsx
import { createEffect, on } from 'solid-js';

const [a, setA] = createSignal(1);
const [b, setB] = createSignal(2);

// Without on — tracks a() AND b()
createEffect(() => {
  console.log(`a=${a()}, b=${b()}`);
});

// With on — tracks ONLY a() (even though b() is read)
createEffect(on(a, () => {
  console.log(`a=${a()}, b=${b()}`);     // b() is read but not tracked
}));

// With defer — don't run immediately, only on change
createEffect(on(a, () => { /* ... */ }, { defer: true }));
```

---

## SolidStart: File-Based Routing + Server Functions

### File-based routing (`@solidjs/router`)

```tsx
// src/routes/index.tsx — /
import { Title } from '@solidjs/meta';

export default function Home() {
  return (
    <>
      <Title>Home</Title>
      <h1>Welcome</h1>
    </>
  );
}

// src/routes/users/[id].tsx — /users/:id
import { useParams } from '@solidjs/router';

export default function UserPage() {
  const params = useParams();             // { id: "42" }
  return <h1>User {params.id}</h1>;
}

// src/routes/users/index.tsx — /users
import { A } from '@solidjs/router';      // A = anchor with active class

export default function UsersList() {
  return (
    <ul>
      <li><A href="/users/1">User 1</A></li>
      <li><A href="/users/2">User 2</A></li>
    </ul>
  );
}
```

### Load functions (data fetching)

```tsx
// src/routes/users/[id].tsx
import { useParams } from '@solidjs/router';

// routeData — runs on server during SSR, then on client during navigation
export function routeData({ params }: RouteDefinitionArgs) {
  // This function runs on the server — can use DB, secrets, etc.
  return getUser(params.id);
}

export default function UserPage() {
  const user = routeData();               // Returns a resource
  return (
    <Suspense fallback={<p>Loading...</p>}>
      <h1>{user()?.name}</h1>
    </Suspense>
  );
}
```

### Server functions (`'use server'`)

```tsx
// src/server/db.ts — server-only module
'use server';
import { db } from './db';

export async function getUser(id: string) {
  return db.user.findUnique({ where: { id } });
}

export async function createUser(input: { name: string; email: string }) {
  return db.user.create({ data: input });
}
```

```tsx
// src/components/CreateUser.tsx — client component
import { createSignal } from 'solid-js';
import { createUser } from '~/server/db';   // Imported as an RPC

export default function CreateUser() {
  const [name, setName] = createSignal('');
  const [email, setEmail] = createSignal('');

  const handleSubmit = async (e: Event) => {
    e.preventDefault();
    // createUser is an RPC — SolidStart generates a fetch call to the server
    const user = await createUser({ name: name(), email: email() });
    console.log('Created:', user);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input value={name()} onInput={e => setName(e.currentTarget.value)} />
      <input value={email()} onInput={e => setEmail(e.currentTarget.value)} />
      <button type="submit">Create</button>
    </form>
  );
}
```

The `'use server'` directive marks functions as server-only. SolidStart's compiler generates an RPC endpoint for each — calling `createUser()` from the client makes an HTTP request to the server. The server function has access to DB, secrets, file system — everything. The client never sees the implementation.

### Server-only modules

```tsx
// src/server/db.ts — the 'use server' directive OR the src/server/ path
// Both ensure this code never ships to the client bundle
import { PrismaClient } from '@prisma/client';

export const db = new PrismaClient();     // Server-only — never imported by client
```

Modules in `src/server/` are automatically server-only. The compiler throws an error if client code imports them.

---

## Document head management (`@solidjs/meta`)

```tsx
// src/routes/index.tsx
import { Title, Meta, Link } from '@solidjs/meta';

export default function Home() {
  return (
    <>
      <Title>My App — Home</Title>
      <Meta name="description" content="Welcome to my app" />
      <Meta property="og:title" content="My App" />
      <Link rel="canonical" href="https://example.com/" />
      <h1>Home</h1>
    </>
  );
}
```

The `Title`, `Meta`, and `Link` components update the document head during SSR and on the client. They're reactive — if the title depends on a signal, it updates when the signal changes.

---

## State Management: Signals + Stores (no Redux needed)

Solid's fine-grained reactivity makes most state management libraries unnecessary. The pattern:

```tsx
// src/lib/store.ts — global store (module-level signals)
import { createSignal } from 'solid-js';

// Module-level — shared across all components that import it
const [count, setCount] = createSignal(0);
export { count, setCount };

// Or as a context (for scoped state)
import { createContext, useContext } from 'solid-js';

const CounterContext = createContext<{ count: () => number; increment: () => void }>();

export function CounterProvider(props: { children: any }) {
  const [count, setCount] = createSignal(0);
  const value = { count, increment: () => setCount(c => c + 1) };
  return (
    <CounterContext.Provider value={value}>
      {props.children}
    </CounterContext.Provider>
  );
}

export function useCounter() {
  const ctx = useContext(CounterContext);
  if (!ctx) throw new Error('useCounter must be used within CounterProvider');
  return ctx;
}
```

```tsx
// src/components/Counter.tsx
import { useCounter } from '~/lib/store';

export default function Counter() {
  const { count, increment } = useCounter();
  return <button onClick={increment}>{count()}</button>;
}
```

For server state (API data), use `createResource` (built-in) — it handles loading/error states, refetching, and Suspense integration. No TanStack Query needed for most cases (though it's available if you want its cache/features).

---

## Deployment

SolidStart uses **Vinxi** (Vite-based) for builds. The `app.config.ts` determines the deployment target:

```typescript
// Node.js
export default defineConfig({ server: { preset: 'node-server' } });

// Vercel
export default defineConfig({ server: { preset: 'vercel' } });

// Cloudflare Pages
export default defineConfig({ server: { preset: 'cloudflare' } });

// Netlify
export default defineConfig({ server: { preset: 'netlify' } });

// Static (SSG — pre-render all routes)
export default defineConfig({ server: { preset: 'static' } });
```

```bash
npm run build       # Outputs to .output/
# Node: node .output/server/index.mjs
# Vercel/Cloudflare/Netlify: deploy via their CLI
```

---

## Testing (Vitest + @solidjs/testing-library)

```tsx
// src/components/Counter.test.tsx
import { render, fireEvent } from '@solidjs/testing-library';
import Counter from './Counter';

test('increments on click', async () => {
  const { getByText } = render(() => <Counter />);
  const button = getByText('0');
  fireEvent.click(button);
  expect(button.textContent).toBe('1');     // Updates immediately — no async wait
});
```

Solid's synchronous updates make testing simpler than React — no `await waitFor(() => ...)` needed. The DOM updates immediately when the signal changes.

Cross-reference: `testing-patterns` for general test pyramid / mocking strategies.

---

## Top 10 Anti-Patterns (the most valuable section)

1. **Forgetting `()` on signal reads.** `count` is a function; `count()` is the value. Writing `{count}` in JSX renders `[Function]`. Writing `console.log(count)` logs the function. Always call the getter: `{count()}`, `console.log(count())`. This is the #1 Solid mistake for React developers.

2. **Destructuring signals loses reactivity.** `const { data } = createResource(...)` makes `data` a snapshot — accessing `data` later doesn't track the dependency. Always access via the getter: `const [data] = createResource(...); data()`. Destructuring `props` has the same issue — use `props.foo` not `const { foo } = props`.

3. **Treating components like React components (expecting re-renders).** Solid components run their function body **once**. The JSX is set up with reactive effects. If you put `console.log('render')` in a component, it logs once — not on every state change. Don't write code that depends on the component function re-running.

4. **Using `useState`/`useEffect` patterns from React.** Solid has `createSignal`/`createEffect` — different API, different semantics. `useEffect` with a deps array → `createEffect` (no deps array — automatic tracking). `useMemo` with deps → `createMemo` (no deps array). `useCallback` → just define the function (no re-renders to worry about).

5. **Mutating store objects directly.** `state.users[0].name = 'New'` doesn't trigger updates — use `setState('users', 0, 'name', 'New')` or `setState(produce(s => { s.users[0].name = 'New'; }))`. Direct mutation breaks reactivity tracking.

6. **Not using `onCleanup` for side effects.** Solid effects don't have a cleanup return like React's `useEffect`. Use `onCleanup(() => clearInterval(interval))` inside the effect. Without it, intervals/listeners leak across effect re-runs.

7. **Creating signals inside JSX (re-creates on every render — but Solid doesn't re-render).** Actually this is fine in Solid (no re-renders), but it's a code smell. Create signals at the top of the component function, not inside JSX expressions.

8. **Importing server modules into client code.** `'use server'` modules and `src/server/*` files are server-only. Importing them into client components will fail the build (good) — but if you accidentally share a file that mixes server and client code, secrets can leak. Keep server code in `src/server/`.

9. **Not using `Suspense` for async resources.** `createResource` returns `undefined` while loading. Accessing `user()?.name` without `Suspense` means the component renders nothing during loading. Wrap async components in `<Suspense fallback={<Loading />}>` for proper loading UX.

10. **Reaching for state management libraries (Redux, Zustand, Jotai).** Solid's fine-grained reactivity makes most external state managers unnecessary. Module-level signals + context cover 95% of cases. TanStack Query is still useful for server cache, but client state should use signals + stores.

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for SolidStart (project onboarding)
- `svelte-5-sveltekit` — Svelte 5 + SvelteKit (closest comparable — both signals-based, both file-routing, both ship less JS than React)
- `vue-3-nuxt` — Vue 3 + Nuxt (similar reactivity concept but via Proxies, different syntax)
- `react19-ts6-vite8-tailwindv4-mvp` — React 19 (contrast: re-render model vs signals)
- `astro-5` — Astro (can use Solid components as islands)
- `frontend-ui-engineering` — Production-quality UI build patterns
- `api-and-interface-design` — Type contract design (relevant for server function types)
- `api-patterns` — REST API patterns (for SolidStart API routes)
- `security-and-hardening` — OWASP-aware hardening
- `clean-code` — General coding standards applicable to TypeScript
- `testing-patterns` — Test pyramid, mocking strategies
- `code-review-checklist` — 12-category code review checklist

---

## Dependencies

Required:
- **Node.js** 20+ (or Bun 1.1+)
- **SolidJS** 1.9+
- **SolidStart** 1.0+
- **Vinxi** (build tool, bundled with SolidStart)
- **Vite** 5+ (underlying build tool)
- **TypeScript** 5+ (default, can opt out but not recommended)

### Common additions (install via `npm install`)

- `@solidjs/router` — file-based routing (bundled with SolidStart)
- `@solidjs/meta` — document head management (Title, Meta, Link)
- `@solidjs/start` — SolidStart core (the meta-framework)
- `@solidjs/testing-library` — component testing utilities
- `solid-js` — the core SolidJS library (signals, stores, context)
- `@prisma/client` + `prisma` — TypeScript ORM (pairs naturally with SolidStart server functions)
- `drizzle-orm` — alternative TypeScript ORM
- `vinxi` — the build tool (usually via SolidStart)
- `tailwindcss` + `@tailwindcss/vite` — Tailwind CSS 4 via Vite plugin
- `vitur` — Vue Test Utils equivalent for Solid (alternative to @solidjs/testing-library)
- `@tanstack/solid-query` — TanStack Query for Solid (server cache, if you need it beyond createResource)
- `@kobalte/core` — accessible unstyled component library (Headless UI for Solid)
- `solid-styled-components` — CSS-in-JS for Solid
- `@solid-primitives/storage` — persistent storage (localStorage/sessionStorage)
- `@solid-primitives/i18n` — internationalization
- `@solid-primitives/scheduled` — debounce/throttle
- `@solid-primitives/media` — media query helpers
- `@solid-primitives/intersection` — IntersectionObserver wrapper (for infinite scroll, lazy load)
