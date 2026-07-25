---
name: hono
description: "Hono 4 (TypeScript, released 2024) ultra-lightweight web framework for edge runtimes workflow skill. Covers the multi-runtime support (runs UNCHANGED on Cloudflare Workers/Pages, Deno, Bun, Vercel Edge, AWS Lambda, Node.js, Lagon, Netlify Edge — the same code deploys to any runtime via the hono/<adapter> package), the type-safe RPC via hc client (the killer feature — `const client = hc<App>(url)` generates a fully-typed client from the app's routes, end-to-end type safety with zero codegen), routing (the new RegExpRouter for ~3x faster routing than Hono 3, plus the LinearRouter and PatternRouter for different trade-offs), the built-in middleware ecosystem (BasicAuth, BearerAuth, JWT, CORS, Etag, PrettyJSON, Compress, Cache, Logger, Timing, SecureHeaders, CSRF), context-based request/response handling (c.req.json(), c.json(), c.header(), c.set()/c.get() for cross-middleware state), Hono 4's static file serving via @hono/vite-cloudflare-pages or @hono/vite-dev-server, Zod + Valibot integration for validation via @hono/zod-openapi / @hono/standard-validator, the @hono/zod-openapi plugin for OpenAPI 3 spec generation, file-based routing via @hono/hono-fc-router, the WebSocket helper (Hono 4 — works on Deno + Bun + Cloudflare Durable Objects), and deployment to each runtime (wrangler for Cloudflare, deploy.sh for Deno Deploy, bun build for Bun, etc.). Use when building any edge/serverless API, ultra-fast microservice, or runtime-portable web service — especially when the task involves multi-runtime deployment, type-safe RPC client generation, Cloudflare Workers/Durable Objects, Deno Deploy, or Bun server where idiomatic Hono (ultra-light + runtime-agnostic + type-safe RPC) differs from Express/Fastify (Node-only) or from Next.js (heavier, Vercel-coupled)."
license: Proprietary. LICENSE.txt has complete terms
---

# Hono 4 — Ultra-Lightweight Web Framework for Edge Runtimes

> **Target:** Hono 4.x (released 2024) on TypeScript 5+. Hono is a web framework designed for **edge runtimes** — it runs unchanged on Cloudflare Workers/Pages, Deno, Bun, Vercel Edge, AWS Lambda, Netlify Edge, Lagon, and Node.js. Its distinctive features: **zero dependencies** (~14 KB minified+gzipped), a **RegExpRouter** that compiles routes to a single regex for ~3x faster matching, and a **type-safe RPC client** (`hc`) that infers types from your route definitions — end-to-end type safety with zero codegen.

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending a Hono application. Trigger phrases include "Hono", "hono/", "Cloudflare Workers", "Cloudflare Pages", "Deno Deploy", "Bun serve", "Vercel Edge", "AWS Lambda", "Netlify Edge", "Lagon", "hono/cloudflare-workers", "hono/deno", "hono/bun", "hono/vercel", "hono/aws-lambda", "hono/node-server", "hc<", "RpcType", "RegExpRouter", "LinearRouter", "PatternRouter", "@hono/zod-openapi", "@hono/standard-validator", "wrangler", "c.req.json()", "c.json()", "c.set(", "c.get(", "HonoEnv", and any reference to `new Hono()` or the `import { Hono } from 'hono'` import.

Do **not** use this skill for:
- **Hono ≤3** — the router and middleware APIs changed in Hono 4. The RegExpRouter is the default in 4+.
- **Express / Fastify** — Node-only frameworks, different ecosystem, heavier. Hono is runtime-agnostic and 1/10th the size.
- **Next.js / Nuxt / SvelteKit** — these are full-stack app frameworks with SSR, routing, data fetching. Hono is an API framework (though it can serve HTML).
- **NestJS** — enterprise TypeScript backend with IoC + decorators. See `nestjs` skill. Hono is functional, lightweight, no decorators.

Cross-reference: `nestjs` is the enterprise TypeScript alternative (heavier, IoC-based, Node-focused). `go-web` and `rust-web` cover compiled-language backends (different performance characteristics).

## Quick Start

Hono runs on multiple runtimes. Pick your target:

### Cloudflare Workers (the canonical Hono target)

```bash
# Install Wrangler (Cloudflare's CLI)
npm install -g wrangler

# Create a new Hono project for Cloudflare Workers
npm create hono@latest my-app
# Select: cloudflare-workers

cd my-app
npm install

# Dev server (local Cloudflare Workers simulator)
npm run dev          # http://localhost:8787

# Deploy to Cloudflare
npx wrangler deploy
```

### Bun (fastest runtime)

```bash
# Install Bun
curl -fsSL https://bun.sh/install | bash

# Create a new project
bun create hono@latest my-app
# Select: bun

cd my-app
bun install
bun run dev          # http://localhost:3000
```

### Deno

```bash
# Install Deno
curl -fsSL https://deno.land/install.sh | sh

# Create a new project
deno run -A npm:create-hono@latest my-app
# Select: deno

cd my-app
deno task dev        # http://localhost:3000
```

### Node.js (via @hono/node-server)

```bash
npm create hono@latest my-app
# Select: nodejs

cd my-app
npm install
npm run dev          # http://localhost:3000
```

### Key commands (Cloudflare Workers example)

```bash
npm run dev              # Local dev with Wrangler (hot reload)
npm run deploy           # Deploy to Cloudflare Workers (npx wrangler deploy)
npx wrangler tail        # Tail production logs
npx wrangler kv:namespace create MY_KV   # Create a KV namespace
npx wrangler r2 bucket create my-bucket  # Create an R2 bucket
npx wrangler d1 create my-db             # Create a D1 (SQLite) database
```

---

## Project Structure (Hono canonical layout)

Hono projects are minimal — there's no enforced structure. The runtime determines the entry point.

```
my-app/
├── src/
│   ├── index.ts           # Entry point (Hono app instance + routes)
│   ├── routes/            # Route handlers (optional — can be inline)
│   │   ├── users.ts
│   │   ├── posts.ts
│   │   └── auth.ts
│   ├── middleware/         # Custom middleware
│   │   ├── auth.ts
│   │   ├── logging.ts
│   │   └── error-handler.ts
│   ├── lib/                # Utilities, services
│   │   ├── db.ts           # D1 / KV / R2 / Durable Object clients
│   │   ├── jwt.ts
│   │   └── validation.ts
│   └── types.ts           # HonoEnv type (Bindings + Variables)
├── wrangler.toml          # Cloudflare Workers config (or deno.json / package.json for other runtimes)
├── package.json
├── tsconfig.json
└── README.md
```

### The minimal Hono app

```typescript
// src/index.ts
import { Hono } from 'hono';
import { logger } from 'hono/logger';
import { prettyJSON } from 'hono/pretty-json';
import { cors } from 'hono/cors';

// Define the app's environment type (Bindings + Variables)
interface Env {
  Bindings: {
    DB: D1Database;           // Cloudflare D1 binding
    MY_KV: KVNamespace;       // Cloudflare KV binding
    API_TOKEN: string;        // Secret
  };
  Variables: {
    user: { id: string; email: string };   // Set by auth middleware
  };
}

const app = new Hono<Env>();

// Built-in middleware
app.use('*', logger());
app.use('*', prettyJSON());
app.use('*', cors());

// Routes
app.get('/', (c) => c.json({ message: 'Hello, Hono!' }));
app.get('/health', (c) => c.json({ status: 'ok' }));

// Route group (like Express Router)
const api = new Hono<Env>();
api.get('/users', async (c) => {
  const result = await c.env.DB.prepare('SELECT * FROM users').all();
  return c.json(result.results);
});
api.get('/users/:id', async (c) => {
  const id = c.req.param('id');
  const user = await c.env.DB.prepare('SELECT * FROM users WHERE id = ?').bind(id).first();
  if (!user) return c.json({ error: 'Not found' }, 404);
  return c.json(user);
});

app.route('/api', api);

export default app;             // Cloudflare Workers entry point
```

---

## Core Mental Model: Multi-Runtime + Type-Safe RPC + Ultra-Lightweight

Hono's distinctive paradigm is **a single codebase that runs on any JavaScript runtime, with end-to-end type safety via type inference.** Four things differentiate Hono from Express/Fastify/NestJS:

### 1. Multi-runtime (write once, run on any edge runtime)

```typescript
// src/index.ts — THE SAME CODE runs on all runtimes
import { Hono } from 'hono';

const app = new Hono();
app.get('/', (c) => c.json({ hello: 'world' }));

export default app;
```

The runtime-specific entry point is a tiny adapter:

```typescript
// Cloudflare Workers — src/index.ts
export default app;                    // Just export the Hono instance

// Deno — src/index.ts
import { serve } from 'std/http/server.ts';
serve(app.fetch);                      // Pass app.fetch to Deno's serve

// Bun — src/index.ts
export default {
  port: 3000,
  fetch: app.fetch,                    // Pass app.fetch to Bun's fetch handler
};

// Node.js — src/index.ts
import { serve } from '@hono/node-server';
serve(app, { port: 3000 });            // Use @hono/node-server

// Vercel Edge — api/[[...route]].ts
import { handle } from 'hono/vercel';
export const GET = handle(app);        // Use Hono's Vercel handler

// AWS Lambda — src/index.ts
import { handle } from 'hono/aws-lambda';
export const handler = handle(app);    // Use Hono's AWS Lambda handler

// Netlify Edge — netlify/edge-functions/api.ts
import { handle } from 'hono/netlify';
export default handle(app);            // Use Hono's Netlify handler
```

The business logic (routes, middleware, validation) is identical across all runtimes. Only the entry point changes. This is Hono's killer feature for edge deployment — write once, deploy to the cheapest/fastest runtime per region.

### 2. Type-safe RPC via `hc` client (zero codegen)

Hono's `hc` (Hono Client) generates a fully-typed client from your app's route definitions — no code generation step, just type inference:

```typescript
// src/index.ts — server
import { Hono } from 'hono';

const app = new Hono();

app.get('/users/:id', (c) => {
  const id = c.req.param('id');
  return c.json({ id, name: 'Alice', email: 'alice@example.com' });
});

app.post('/users', async (c) => {
  const body = await c.req.json<{ name: string; email: string }>();
  return c.json({ id: '1', ...body }, 201);
});

export type App = typeof app;          // ← Export the app's type
export default app;
```

```typescript
// client.ts — frontend (or another Hono app)
import { hc } from 'hono/client';
import type { App } from './index';

const client = hc<App>('https://api.example.com');

// Fully typed — autocompletion for paths, params, body, and response
const res = await client.users[':id'].$get({ param: { id: '42' } });
const user = await res.json();         // Typed as { id: string; name: string; email: string }

const createRes = await client.users.$post({
  json: { name: 'Bob', email: 'bob@example.com' },
});
const newUser = await createRes.json();
```

**The types flow end-to-end with zero codegen.** Add a route on the server, and the client immediately knows about it (with correct param/body/response types). This is the same DX as tRPC but framework-agnostic and runtime-portable.

### 3. The RegExpRouter (compile routes to a single regex)

```typescript
import { Hono } from 'hono';
import { RegExpRouter } from 'hono/router/reg-exp-router';

const app = new Hono({ router: new RegExpRouter() });

app.get('/users', listUsers);
app.get('/users/:id', getUser);
app.post('/users', createUser);
app.put('/users/:id', updateUser);
app.delete('/users/:id', deleteUser);
app.get('/users/:id/posts', listUserPosts);
app.get('/users/:id/posts/:postId', getUserPost);
```

The RegExpRouter compiles all routes into a single regular expression at startup. Route matching becomes a single regex test — ~3x faster than Hono 3's trie router, and faster than Express's path-to-regexp.

| Router | Trade-off |
|---|---|
| `RegExpRouter` (default in 4+) | Fastest matching, slower initialization. Best for production with many routes. |
| `LinearRouter` | Fast initialization, slower matching. Best for cold-start-sensitive serverless (e.g., AWS Lambda). |
| `PatternRouter` | No overhead, no priority. Best for tiny apps. |

### 4. Context-based request/response (no `req`/`res` objects)

```typescript
app.get('/users/:id', async (c) => {
  // Request — via c.req
  const id = c.req.param('id');              // Path param
  const search = c.req.query('search');      // Query param
  const userAgent = c.req.header('User-Agent');
  const body = await c.req.json();           // Parsed JSON body
  const form = await c.req.parseBody();      // Parsed form data

  // Response — via c (chainable)
  return c
    .header('X-Custom', 'value')
    .status(200)
    .json({ id, name: 'Alice' });

  // Or other response types
  return c.text('Hello');                    // text/plain
  return c.html('<h1>Hello</h1>');           // text/html
  return c.redirect('/other');               // 302 redirect
  return c.body(null, 204);                  // Empty 204
  return c.stream(async (stream) => {        // Streaming response
    await stream.write('chunk1\n');
    await stream.sleep(1000);
    await stream.write('chunk2\n');
  });
});
```

The `Context` (`c`) object is both request and response. There's no separate `req`/`res` — this matches the Web `Request`/`Response` standard (which edge runtimes use) and is simpler than Express's two-object model.

---

## Middleware

Hono ships with a rich set of built-in middleware. All are tree-shakeable — you only bundle what you import.

```typescript
import { Hono } from 'hono';
import { logger } from 'hono/logger';
import { prettyJSON } from 'hono/pretty-json';
import { cors } from 'hono/cors';
import { etag } from 'hono/etag';
import { compress } from 'hono/compress';
import { cache } from 'hono/cache';
import { jwt } from 'hono/jwt';
import { bearerAuth } from 'hono/bearer-auth';
import { basicAuth } from 'hono/basic-auth';
import { secureHeaders } from 'hono/secure-headers';
import { csrf } from 'hono/csrf';
import { timing } from 'hono/timing';

const app = new Hono();

app.use('*', logger());
app.use('*', prettyJSON());
app.use('*', cors({ origin: 'https://example.com', allowMethods: ['GET', 'POST'] }));
app.use('*', etag());
app.use('*', compress());
app.use('*', secureHeaders());
app.use('*', timing());
app.use('/api/*', csrf());

// Auth — apply to specific routes
const api = new Hono();
api.use('/private/*', bearerAuth({ token: 'secret' }));
api.use('/admin/*', basicAuth({ username: 'admin', password: 'secret' }));

// JWT verification
api.use('/protected/*', jwt({ secret: 'your-secret' }));

// Caching (Cloudflare Workers-specific)
app.get('/cached-data', cache({ cacheName: 'my-cache', cacheControl: 'max-age=3600' }), (c) => {
  return c.json({ /* ... */ });
});
```

### Custom middleware

```typescript
import { createMiddleware } from 'hono/factory';

// Type-safe custom middleware
const authMiddleware = createMiddleware<{ Variables: { user: User } }>(async (c, next) => {
  const token = c.req.header('Authorization')?.replace('Bearer ', '');
  if (!token) {
    return c.json({ error: 'Unauthorized' }, 401);
  }

  const user = await verifyToken(token);
  if (!user) {
    return c.json({ error: 'Invalid token' }, 401);
  }

  c.set('user', user);        // Available to downstream handlers
  await next();
});

app.use('/api/*', authMiddleware);
app.get('/api/me', (c) => c.json(c.get('user')));
```

### Cross-middleware state via `c.set()` / `c.get()`

```typescript
// Define the Variables type in HonoEnv
interface Env {
  Variables: {
    user: User;
    requestId: string;
    startTime: number;
  };
}

// Middleware sets
app.use('*', async (c, next) => {
  c.set('requestId', crypto.randomUUID());
  c.set('startTime', Date.now());
  await next();
});

// Handler gets
app.get('/debug', (c) => {
  return c.json({
    requestId: c.get('requestId'),
    elapsed: Date.now() - c.get('startTime'),
  });
});
```

---

## Validation: Zod + Valibot + OpenAPI

### Zod validation via `@hono/standard-validator`

```bash
npm install zod @hono/standard-validator
```

```typescript
import { z } from 'zod';
import { zValidator } from '@hono/standard-validator';

const schema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
  age: z.number().int().min(13).max(120).optional(),
});

app.post('/users', zValidator('json', schema), async (c) => {
  const data = c.req.valid('json');        // Typed as z.infer<typeof schema>
  // ... create user ...
  return c.json({ id: '1', ...data }, 201);
});
```

### OpenAPI 3 spec generation via `@hono/zod-openapi`

```bash
npm install @hono/zod-open-api swagger-ui-dist
```

```typescript
import { createRoute, OpenAPIHono } from '@hono/zod-openapi';
import { z } from '@hono/zod-openapi/components';
import { Scalar } from '@scalar/hono-api-reference';

const app = new OpenAPIHono();

const createUserRoute = createRoute({
  method: 'post',
  path: '/users',
  request: {
    body: {
      content: {
        'application/json': {
          schema: z.object({
            name: z.string().min(2),
            email: z.string().email(),
          }),
        },
      },
    },
  },
  responses: {
    201: {
      content: {
        'application/json': {
          schema: z.object({
            id: z.string(),
            name: z.string(),
            email: z.string(),
          }),
        },
      },
      description: 'User created',
    },
  },
});

app.openapi(createUserRoute, async (c) => {
  const { name, email } = c.req.valid('json');
  return c.json({ id: '1', name, email }, 201);
});

// Serve OpenAPI spec + Scalar docs UI
app.doc('/openapi.json', { openapi: '3.0.0', info: { title: 'My API', version: '1.0.0' } });
app.get('/docs', Scalar({ url: '/openapi.json' }));

export default app;
```

This gives you type-safe validation AND auto-generated OpenAPI docs at `/docs` — comparable to FastAPI's auto-Swagger but for TypeScript.

---

## Cloudflare Workers Bindings (D1, KV, R2, Durable Objects)

Hono shines on Cloudflare Workers because of the bindings system. Bindings are typed access to Cloudflare services:

```typescript
// wrangler.toml
[[d1_databases]]
binding = "DB"
database_name = "my-app-db"
database_id = "..."

[[kv_namespaces]]
binding = "MY_KV"
id = "..."

[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-bucket"

[durable_objects]
bindings = [
  { name = "COUNTER", class_name = "CounterDurableObject" }
]
```

```typescript
// src/index.ts
interface Env {
  Bindings: {
    DB: D1Database;             // Cloudflare D1 (SQLite)
    MY_KV: KVNamespace;         // Cloudflare KV (key-value store)
    MY_BUCKET: R2Bucket;        // Cloudflare R2 (S3-compatible object storage)
    COUNTER: DurableObjectNamespace;  // Durable Objects (stateful, per-entity)
  };
}

const app = new Hono<Env>();

// D1 (SQLite)
app.get('/users', async (c) => {
  const result = await c.env.DB.prepare('SELECT * FROM users LIMIT 100').all();
  return c.json(result.results);
});

app.post('/users', async (c) => {
  const { name, email } = await c.req.json();
  await c.env.DB.prepare('INSERT INTO users (name, email) VALUES (?, ?)').bind(name, email).run();
  return c.json({ name, email }, 201);
});

// KV (key-value cache)
app.get('/cached/:key', async (c) => {
  const key = c.req.param('key');
  const value = await c.env.MY_KV.get(key);
  if (!value) return c.json({ error: 'Not found' }, 404);
  return c.json({ key, value });
});

app.put('/cached/:key', async (c) => {
  const key = c.req.param('key');
  const { value } = await c.req.json();
  await c.env.MY_KV.put(key, JSON.stringify(value), { expirationTtl: 3600 });
  return c.json({ stored: true });
});

// R2 (object storage)
app.post('/upload', async (c) => {
  const body = await c.req.parseBody();
  const file = body['file'] as File;
  await c.env.MY_BUCKET.put(file.name, file.stream(), {
    httpMetadata: { contentType: file.type },
  });
  return c.json({ uploaded: file.name });
});

app.get('/download/:key', async (c) => {
  const key = c.req.param('key');
  const object = await c.env.MY_BUCKET.get(key);
  if (!object) return c.json({ error: 'Not found' }, 404);
  return new Response(object.body, { headers: { 'Content-Type': object.httpMetadata?.contentType || 'application/octet-stream' } });
});
```

### Durable Objects (stateful, per-entity actors)

```typescript
// src/index.ts
import { DurableObject } from 'cloudflare:workers';

export class CounterDurableObject extends DurableObject {
  async increment(): Promise<number> {
    const count = (await this.ctx.storage.get<number>('count')) ?? 0;
    const newCount = count + 1;
    await this.ctx.storage.put('count', newCount);
    return newCount;
  }

  async get(): Promise<number> {
    return (await this.ctx.storage.get<number>('count')) ?? 0;
  }
}

const app = new Hono<Env>();

app.get('/counter/:id', async (c) => {
  const id = c.env.COUNTER.idFromName(c.req.param('id'));
  const stub = c.env.COUNTER.get(id);
  const count = await stub.increment();
  return c.json({ count });
});
```

Durable Objects are Hono's answer to Elixir's GenServers or Phoenix's Presence — per-entity stateful actors with strong consistency. Use cases: real-time collaboration, per-room state, rate limiting per-user, leader election.

---

## WebSocket Helper (Hono 4)

Hono 4 added a WebSocket helper that works across runtimes (Deno, Bun, Cloudflare Durable Objects):

```typescript
import { createBunWebSocket } from 'hono/bun';

const { upgradeWebSocket, websocket } = createBunWebSocket();

const app = new Hono();

app.get(
  '/ws',
  upgradeWebSocket((c) => {
    let intervalId: ReturnType<typeof setInterval>;

    return {
      onOpen(event, ws) {
        intervalId = setInterval(() => {
          ws.send(`Ping: ${new Date().toISOString()}`);
        }, 1000);
      },
      onMessage(event, ws) {
        console.log('Received:', event.data);
        ws.send('Echo: ' + event.data);
      },
      onClose() {
        clearInterval(intervalId);
      },
    };
  })
);

export default { fetch: app.fetch, websocket };
```

For Cloudflare Workers, use Durable Objects for WebSocket state:

```typescript
import { Hono } from 'hono';
import { upgradeWebSocket } from 'hono/cloudflare-workers';

const app = new Hono<{ Bindings: { WEBSOCKET: DurableObjectNamespace } }>();

app.get('/ws', upgradeWebSocket((c) => ({
  onOpen(event, ws) {
    // ... attach to Durable Object for shared state ...
  },
})));
```

---

## Error Handling

```typescript
import { HTTPException } from 'hono/http-exception';

// Throw typed HTTP exceptions
app.get('/users/:id', async (c) => {
  const user = await getUser(c.req.param('id'));
  if (!user) {
    throw new HTTPException(404, { message: 'User not found' });
  }
  return c.json(user);
});

// Global error handler
app.onError((err, c) => {
  if (err instanceof HTTPException) {
    return c.json({ error: err.message }, err.status);
  }
  console.error('Unexpected error:', err);
  return c.json({ error: 'Internal server error' }, 500);
});

// 404 handler
app.notFound((c) => c.json({ error: 'Not found' }, 404));
```

---

## Testing (Vitest)

```typescript
// src/index.test.ts
import { describe, it, expect } from 'vitest';
import app from './index';

describe('User API', () => {
  it('GET /users/:id returns user', async () => {
    const res = await app.request('/users/42');
    expect(res.status).toBe(200);
    const data = await res.json();
    expect(data.id).toBe('42');
  });

  it('POST /users creates user', async () => {
    const res = await app.request('/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'Alice', email: 'alice@example.com' }),
    });
    expect(res.status).toBe(201);
    const data = await res.json();
    expect(data.name).toBe('Alice');
  });

  it('GET /users/:id returns 404 for missing', async () => {
    const res = await app.request('/users/999');
    expect(res.status).toBe(404);
  });
});
```

Hono's `app.request()` method is the testing entry point — it invokes the app's routing and middleware without starting an HTTP server. Fast and clean.

Cross-reference: `testing-patterns` for general test pyramid / mocking strategies.

---

## Deployment

### Cloudflare Workers (canonical)

```bash
npx wrangler deploy
# Outputs: https://my-app.<your-subdomain>.workers.dev
```

```toml
# wrangler.toml
name = "my-app"
main = "src/index.ts"
compatibility_date = "2024-11-01"
compatibility_flags = ["nodejs_compat"]

[observability]
enabled = true

[[d1_databases]]
binding = "DB"
database_name = "my-app-db"
database_id = "..."

[vars]
ENVIRONMENT = "production"
```

### Bun

```bash
bun build src/index.ts --target bun --outfile dist/index.js
bun dist/index.js
```

### Deno Deploy

```bash
deno task deploy
# Or: deployctl deploy --project=my-app src/index.ts
```

### Vercel Edge

```typescript
// api/[[...route]].ts
import { handle } from 'hono/vercel';
import app from '../src/index';
export const GET = handle(app);
export const POST = handle(app);
export const PUT = handle(app);
export const DELETE = handle(app);
```

```bash
vercel --prod
```

### AWS Lambda (via Lambda Function URLs or API Gateway)

```typescript
// src/index.ts
import { handle } from 'hono/aws-lambda';
import { Hono } from 'hono';
const app = new Hono();
app.get('/', (c) => c.json({ hello: 'lambda' }));
export const handler = handle(app);
```

---

## Top 10 Anti-Patterns (the most valuable section)

1. **Using `req`/`res` (Express patterns).** Hono uses a single `Context` object (`c`). `c.req.json()` for the request body, `c.json()` for the response. There's no `req`/`res` pair — that's Express. Mixing them produces TypeScript errors (good) but is a sign you haven't internalized the Hono model.

2. **Not using the `HonoEnv` type for Bindings + Variables.** Without `interface Env { Bindings: {...}; Variables: {...} }` and `new Hono<Env>()`, you lose type safety for `c.env.DB`, `c.get('user')`, etc. Always define the env type — it's the foundation of Hono's type safety.

3. **Using the wrong router for the runtime.** The default `RegExpRouter` is fastest for warm apps but has slower cold starts. For cold-start-sensitive serverless (AWS Lambda), use `LinearRouter` (fast init, slower match). For tiny apps, `PatternRouter` (no overhead).

4. **Not exporting `type App` for the `hc` client.** The type-safe RPC client (`hc<App>(url)`) requires `export type App = typeof app`. If you forget to export it, the client is untyped (`any`). This is Hono's killer feature — don't waste it.

5. **Treating Hono like Node.js.** Hono runs on edge runtimes that lack Node.js APIs (`fs`, `path`, `crypto` with the Node API). Use Web APIs instead (`crypto.subtle` for hashing, `fetch` for HTTP, Web Streams). For Node-only APIs, install `nodejs_compat` flag on Cloudflare or use `@hono/node-server` for full Node compatibility.

6. **Not using `c.env` for runtime bindings.** On Cloudflare Workers, `c.env.DB`, `c.env.MY_KV`, `c.env.MY_BUCKET` are typed bindings to D1/KV/R2. Hardcoding connection strings or credentials (like `new D1Database(url)`) defeats the bindings system and breaks in production (Workers don't allow outbound connections except via `fetch`).

7. **Heavy middleware on every request.** Middleware runs on every matched request. `app.use('*', expensiveMiddleware)` adds latency to every route. Apply middleware only where needed: `app.use('/api/*', authMiddleware)` instead of `app.use('*', authMiddleware)`.

8. **Not using Durable Objects for stateful workloads.** Cloudflare Workers are stateless — `let count = 0; count++;` resets on every request (Workers are ephemeral). For stateful per-entity work (rate limits per user, real-time room state, leader election), use Durable Objects. KV is for cache, not for authoritative state (eventually consistent).

9. **Returning raw objects instead of `c.json()`.** Hono doesn't auto-serialize objects. `return { hello: 'world' }` returns a stringified `"[object Object]"`. Always use `return c.json({...})` or `return c.text(...)` or `return c.html(...)`. The type system catches some of this but not all.

10. **Ignoring the bundle size budget.** Hono's selling point is being ~14 KB. Don't import heavy libraries (`zod` is fine, but `lodash` + `moment` + `aws-sdk` bloats the bundle to MBs). Edge runtimes have size limits (Cloudflare Workers: 10 MB compressed; Vercel Edge: 4 MB). Use `wrangler deploy --dry-run` to check size before deploying.

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for Hono (project onboarding)
- `nestjs` — Enterprise TypeScript backend (heavier, IoC-based, Node-focused — contrast with Hono's functional + edge-native approach)
- `go-web` — Go web patterns (similar stdlib-first philosophy, but Go is compiled and runs as a binary; Hono is interpreted JS on edge runtimes)
- `fastapi-sqlalchemy` — Python async API (similar type-driven validation via Pydantic, but Python is sync by default; Hono is JS/TS)
- `api-and-interface-design` — Type contract design (relevant for Hono's type-safe RPC)
- `api-patterns` — REST API patterns
- `security-and-hardening` — OWASP-aware hardening (Hono's middleware covers CORS, CSRF, JWT, secure headers)
- `clean-code` — General coding standards applicable to TypeScript
- `testing-patterns` — Test pyramid, mocking strategies
- `code-review-checklist` — 12-category code review checklist

---

## Dependencies

Required:
- **TypeScript** 5+ (or JavaScript — Hono is JS, but you lose type safety without TS)
- **Hono** 4.0+ (`npm install hono`)
- A target runtime:
  - **Cloudflare Workers**: `npm install -D wrangler` (Cloudflare CLI)
  - **Deno**: Deno 1.40+
  - **Bun**: Bun 1.0+
  - **Node.js**: `npm install @hono/node-server` + Node.js 20+
  - **Vercel Edge**: Hono's `hono/vercel` adapter (built-in)
  - **AWS Lambda**: Hono's `hono/aws-lambda` adapter (built-in)
  - **Netlify Edge**: Hono's `hono/netlify` adapter (built-in)

### Validation + OpenAPI

- `zod` + `@hono/standard-validator` — Zod validation
- `@hono/zod-openapi` — OpenAPI 3 spec generation from Zod schemas
- `@scalar/hono-api-reference` — Scalar API docs UI (modern alternative to Swagger UI)
- `valibot` + `@hono/standard-validator` — Valibot validation (smaller than Zod)

### Common official middleware (all built-in to Hono)

- `hono/logger` — request logging
- `hono/cors` — CORS handling
- `hono/etag` — ETag generation
- `hono/compress` — response compression (gzip/brotli)
- `hono/cache` — response caching (Cloudflare Workers-specific)
- `hono/jwt` — JWT verification
- `hono/bearer-auth` — Bearer token auth
- `hono/basic-auth` — HTTP Basic auth
- `hono/secure-headers` — security headers (CSP, HSTS, X-Frame-Options, etc.)
- `hono/csrf` — CSRF protection
- `hono/timing` — Server-Timing header
- `hono/pretty-json` — pretty-print JSON in dev
- `hono/streaming` — streaming responses

### Cloudflare-specific (when deploying to Workers)

- `@cloudflare/workers-types` — TypeScript types for Workers bindings
- `wrangler` — Cloudflare CLI (dev, deploy, logs)
- `cloudflare:workers` (built-in to Workers runtime) — DurableObject base class, WebSocket support

### Storage (Cloudflare bindings)

- D1 (SQLite) — `c.env.DB` (D1Database)
- KV (key-value) — `c.env.MY_KV` (KVNamespace)
- R2 (S3-compatible) — `c.env.MY_BUCKET` (R2Bucket)
- Durable Objects — `c.env.MY_DO` (DurableObjectNamespace)
- Queues — `c.env.MY_QUEUE` (Queue)

### Common additions

- `@hono/vite-dev-server` — Vite plugin for local dev with HMR
- `@hono/vite-cloudflare-pages` — Vite plugin for Cloudflare Pages
- `@hono/zod-openapi` — OpenAPI generation from Zod schemas
- `@hono/swagger-ui` — Swagger UI middleware
- `hono/swagger-ui` — alternative Swagger UI
- `hono/firebase-auth` — Firebase Auth verification middleware
- `hono/supabase` — Supabase integration helpers
- `drizzle-orm` — TypeScript ORM (works with D1, Postgres, MySQL, SQLite)
- `kysely` — TypeScript SQL query builder (works with D1)
