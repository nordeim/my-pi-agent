---
name: fastify
description: "Fastify 5 (Node.js 20+, released 2024) high-performance web framework workflow skill — the canonical Express replacement. Covers the schema-first design (JSON Schema for request validation + response serialization — Fastify compiles schemas via fast-json-stringify for 2-3x faster serialization than JSON.stringify), the plugin encapsulation model (fastify.register() creates isolated scopes with their own decorators/hooks/encapsulated plugins — contrast with Express where middleware is global), the hook system (onRequest, preParsing, preValidation, preHandler, preSerialization, onSend, onResponse, onError, onTimeout — a more granular pipeline than Express), decorators (fastify.decorate('utility', fn) adds to the Fastify instance, request, or reply), TypeScript support via @fastify/type-provider-typebox (TypeBox for schema = types, no duplication) or @fastify/type-provider-json-schema-to-ts, the official plugin ecosystem (@fastify/cors, @fastify/helmet, @fastify/rate-limit, @fastify/jwt, @fastify/cookie, @fastify/multipart, @fastify/static, @fastify/swagger, @fastify/under-pressure, @fastify/express for Express middleware compat), the @fastify/cli for config-driven routing, child loggers via pino (Fastify ships pino by default — 3x faster than Winston/Bunyan), and deployment via standard Node.js (PM2, Docker, systemd). Use when building any Node.js HTTP API, microservice, or high-throughput backend — especially when the task involves schema validation, plugin encapsulation, migrating from Express, performance optimization, or comparing Fastify vs Express vs Hono vs NestJS where idiomatic Fastify (schema-first + encapsulated plugins + pino logging) differs from Express (loose middleware + no built-in schema) or NestJS (IoC + decorators + heavier)."
license: Proprietary. LICENSE.txt has complete terms
---

# Fastify 5 — High-Performance Node.js Web Framework

> **Target:** Fastify 5.0+ (released 2024) on Node.js 20+ with TypeScript 5+. Fastify is the canonical Express replacement for high-performance Node.js APIs. Its distinctive features: **schema-first design** (JSON Schema for validation + serialization — compiled via `fast-json-stringify` for 2-3x faster JSON output), **plugin encapsulation** (each `fastify.register()` creates an isolated scope — unlike Express's global middleware), and **pino logging** built-in (3x faster than Winston/Bunyan).

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending a Fastify application. Trigger phrases include "Fastify", "fastify.register", "fastify.get", "fastify.post", "JSON Schema", "schema-first", "fast-json-stringify", "preHandler", "preValidation", "onRequest", "onSend", "fastify.decorate", "@fastify/cors", "@fastify/jwt", "@fastify/cookie", "@fastify/rate-limit", "@fastify/multipart", "@fastify/swagger", "@fastify/static", "@fastify/helmet", "@fastify/type-provider-typebox", "TypeBox", "pino", "encapsulated plugin", and any reference to `fastify({ logger: true })` or the `fastify` instance pattern.

Do **not** use this skill for:
- **Express** — different middleware model (global vs encapsulated), no built-in schema validation, slower. Migrate to Fastify if performance matters.
- **Koa** — similar to Express but with async middleware. Different ecosystem.
- **NestJS** — NestJS can use Fastify as its underlying adapter, but NestJS is IoC + decorators on top. See `nestjs` skill for the NestJS layer.
- **Hono** — Hono is edge-runtime-focused (Cloudflare Workers, Deno, Bun). Fastify is Node.js-focused. See `hono` skill for edge.
- **Fastify ≤4** — some plugin APIs and the type provider system changed in 5.0.

Cross-reference: `nestjs` can use Fastify as an adapter (`@nestjs/platform-fastify`). `hono` covers the edge-runtime equivalent. `go-web` and `rust-web` cover compiled-language alternatives.

## Quick Start

```bash
# Create a new Fastify project
npm init fastify
# OR manually:
mkdir my-app && cd my-app
npm init -y
npm install fastify

# Create the server
cat > app.js << 'EOF'
const fastify = require('fastify')({ logger: true })

fastify.get('/', async (request, reply) => {
  return { hello: 'world' }
})

const start = async () => {
  try {
    await fastify.listen({ port: 3000, host: '0.0.0.0' })
    console.log('Server listening on http://localhost:3000')
  } catch (err) {
    fastify.log.error(err)
    process.exit(1)
  }
}
start()
EOF

node app.js               # http://localhost:3000
```

### TypeScript setup (recommended)

```bash
npm install fastify
npm install -D typescript @types/node tsx
npx tsc --init

# For schema = types (no duplication):
npm install @fastify/type-provider-typebox @sinclair/typebox
```

```typescript
// src/app.ts
import Fastify from 'fastify';
import { TypeBoxTypeProvider } from '@fastify/type-provider-typebox';
import { Type } from '@sinclair/typebox';

const fastify = Fastify({
  logger: true,
}).withTypeProvider<TypeBoxTypeProvider>();

// Schema defines BOTH validation AND TypeScript types
const createUserSchema = {
  body: Type.Object({
    name: Type.String({ minLength: 2, maxLength: 100 }),
    email: Type.String({ format: 'email' }),
    age: Type.Optional(Type.Integer({ minimum: 13, maximum: 120 })),
  }),
  response: {
    201: Type.Object({
      id: Type.String(),
      name: Type.String(),
      email: Type.String(),
    }),
  },
};

fastify.post('/users', { schema: createUserSchema }, async (request, reply) => {
  // request.body is FULLY TYPED from the schema — no duplication
  const { name, email, age } = request.body;
  const user = await createUser({ name, email, age });
  reply.code(201).send(user);
});

const start = async () => {
  try {
    await fastify.listen({ port: 3000, host: '0.0.0.0' });
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};
start();
```

### Key commands

```bash
npx tsx src/app.ts            # Run dev server (TypeScript)
node dist/app.js              # Run compiled JS
npm run build                 # tsc → dist/
npm run dev                   # tsx watch (HMR-like reload)

# @fastify/cli (optional — for config-driven routing)
npm install -g fastify-cli
fastify start app.js          # Start with the CLI
fastify start -d              # Debug mode
```

---

## Project Structure (Fastify canonical layout)

Fastify projects are minimal — there's no enforced structure, but the **plugin-based** layout is the canonical pattern:

```
my-app/
├── src/
│   ├── app.ts                 # Fastify instance creation + plugin registration
│   ├── server.ts              # listen() — the entry point
│   ├── plugins/               # Custom Fastify plugins (decorate, hooks)
│   │   ├── prisma.ts          # Database client plugin
│   │   ├── auth.ts            # Auth decorator + preHandler
│   │   ├── error-handler.ts   # Error formatting
│   │   └── sensible.ts        # @fastify/sensible (error helpers)
│   ├── routes/                # Route plugins (each is encapsulated)
│   │   ├── users.ts           # /users routes
│   │   ├── posts.ts           # /posts routes
│   │   └── auth.ts            # /auth routes
│   ├── schemas/               # JSON Schema / TypeBox definitions
│   │   ├── user.ts
│   │   └── post.ts
│   ├── services/              # Business logic (called from routes)
│   │   ├── user-service.ts
│   │   └── post-service.ts
│   ├── lib/                   # Utilities
│   │   ├── config.ts          # Env config (envschema)
│   │   └── logger.ts          # Pino logger config
│   └── types.ts               # TypeScript declarations
├── test/                      # Tests (tap, vitest, or jest)
│   ├── users.test.ts
│   └── helper.ts              # Test app builder
├── package.json
├── tsconfig.json
└── Dockerfile
```

### The app + server separation

```typescript
// src/app.ts — create the Fastify instance (testable — no listen())
import Fastify from 'fastify';
import { TypeBoxTypeProvider } from '@fastify/type-provider-typebox';
import cors from '@fastify/cors';
import helmet from '@fastify/helmet';
import jwt from '@fastify/jwt';
import rateLimit from '@fastify/rate-limit';
import { prismaPlugin } from './plugins/prisma';
import { authPlugin } from './plugins/auth';
import { usersRoutes } from './routes/users';
import { postsRoutes } from './routes/posts';

export function buildApp() {
  const app = Fastify({
    logger: {
      level: process.env.LOG_LEVEL || 'info',
      transport: process.env.NODE_ENV === 'development'
        ? { target: 'pino-pretty' }
        : undefined,
    },
  }).withTypeProvider<TypeBoxTypeProvider>();

  // Register official plugins
  app.register(cors, { origin: true });
  app.register(helmet);
  app.register(rateLimit, { max: 100, timeWindow: '1 minute' });
  app.register(jwt, { secret: process.env.JWT_SECRET! });

  // Register custom plugins
  app.register(prismaPlugin);
  app.register(authPlugin);

  // Register routes (each is encapsulated)
  app.register(usersRoutes, { prefix: '/api/users' });
  app.register(postsRoutes, { prefix: '/api/posts' });

  return app;
}
```

```typescript
// src/server.ts — the entry point (calls listen)
import { buildApp } from './app';

const app = buildApp();

const start = async () => {
  try {
    await app.listen({ port: Number(process.env.PORT) || 3000, host: '0.0.0.0' });
  } catch (err) {
    app.log.error(err);
    process.exit(1);
  }
};

start();
```

Separating `buildApp()` from `listen()` is the canonical Fastify pattern — it makes the app testable (you can call `app.inject()` without binding a port).

---

## Core Mental Model: Schema-First + Encapsulated Plugins + Hook Pipeline

Fastify's distinctive paradigm is **schemas drive validation AND serialization AND types, with encapsulated plugin scopes.** Four things differentiate Fastify from Express:

### 1. Schema-first design (validation + serialization + types in one)

```typescript
import { Type } from '@sinclair/typebox';

const userSchema = {
  // Request validation — Fastify validates BEFORE the handler runs
  body: Type.Object({
    name: Type.String({ minLength: 2, maxLength: 100 }),
    email: Type.String({ format: 'email' }),
    age: Type.Optional(Type.Integer({ minimum: 13 })),
  }),
  querystring: Type.Object({
    include: Type.Optional(Type.String()),
  }),
  params: Type.Object({
    id: Type.String(),
  }),
  headers: Type.Object({
    'x-api-key': Type.String(),
  }),

  // Response serialization — Fastify compiles this to a fast-json-stringify function
  // 2-3x faster than JSON.stringify because it skips runtime type checks
  response: {
    200: Type.Object({
      id: Type.String(),
      name: Type.String(),
      email: Type.String(),
      age: Type.Optional(Type.Integer()),
    }),
    400: Type.Object({
      error: Type.String(),
    }),
  },
};

fastify.put('/users/:id', { schema: userSchema }, async (request, reply) => {
  // request.body, request.querystring, request.params, request.headers
  // are ALL typed from the schema — no manual types needed
  const { id } = request.params;
  const { name, email, age } = request.body;

  const user = await updateUser(id, { name, email, age });

  // reply.send() uses the response schema for SERIALIZATION (not just validation)
  // Fastify compiles the schema to a specialized function — much faster than JSON.stringify
  return reply.code(200).send(user);
});
```

**The schema does three things at once:**
1. **Validates** the request (returns 400 with details if invalid)
2. **Serializes** the response (compiles to `fast-json-stringify` for 2-3x speed)
3. **Types** the handler (TypeBox generates TypeScript types from the schema)

This is the opposite of Express, where you'd use a separate validation library (`joi`, `zod`), serialize with `JSON.stringify` (no optimization), and types are manual.

### 2. Encapsulated plugins (not global middleware)

```typescript
// Fastify plugins are ENCAPSULATED — they don't leak to the parent
fastify.register(async (instance, opts) => {
  // This plugin has its own decorators, hooks, and routes
  // They DON'T affect the parent fastify instance
  instance.decorate('db', createDbConnection());

  instance.addHook('onRequest', async (request, reply) => {
    // This hook only runs for routes registered in THIS plugin
    request.log.info('Plugin-scoped request');
  });

  instance.get('/users', async () => {
    return instance.db.getUsers();   // instance.db is available here
  });
}, { prefix: '/api/v1' });

// fastify.db is UNDEFINED here — the decorator is scoped
// The onRequest hook doesn't run for routes outside the plugin
fastify.get('/health', async () => ({ status: 'ok' }));
```

**Contrast with Express:**

```javascript
// Express — middleware is GLOBAL
app.use((req, res, next) => {
  // This runs for ALL routes — no encapsulation
  next();
});

app.use('/api/v1', router);  // The router is mounted, but middleware still global
```

Fastify's encapsulation is enforced — a plugin's decorators, hooks, and child plugins stay inside the plugin's scope. This makes large apps manageable (no accidental global state).

**Opt out with `fastify-plugin`** when you WANT to leak to the parent:

```typescript
import fp from 'fastify-plugin';

// fp() wraps the plugin so decorators/hooks leak to the parent
export default fp(async (fastify, opts) => {
  fastify.decorate('db', createDbConnection());   // Available in the parent
});
```

Use `fp()` for utility plugins (database, auth) that should be globally available. Use plain `register()` for route plugins that should be isolated.

### 3. The hook pipeline (more granular than Express middleware)

```
Request
  ↓
onRequest          — auth checks, rate limit (before parsing)
  ↓
preParsing         — modify the raw request stream (rare)
  ↓
preValidation      — modify headers/body before validation
  ↓
preValidation → validation (via schema, if defined)
  ↓
preHandler         — business logic before the handler (auth, fetch user)
  ↓
handler            — the route function
  ↓
preSerialization   — modify the response before serialization
  ↓
onSend             — modify the response payload (logging, headers)
  ↓
Response sent
  ↓
onResponse         — after response is sent (metrics, logging)
  ↓
(onError           — if any hook/handler throws)
(onTimeout         — if the request times out)
```

```typescript
// Auth check in preHandler (most common)
fastify.addHook('preHandler', async (request, reply) => {
  const token = request.headers.authorization;
  if (!token) {
    throw fastify.httpErrors.unauthorized('Missing token');  // @fastify/sensible
  }
  try {
    request.user = fastify.jwt.verify(token);   // Decorate request with user
  } catch {
    throw fastify.httpErrors.unauthorized('Invalid token');
  }
});

// Logging after response
fastify.addHook('onResponse', async (request, reply) => {
  request.log.info({ statusCode: reply.statusCode, url: request.url }, 'Request completed');
});

// Error handling
fastify.addHook('onError', async (request, reply, error) => {
  request.log.error({ err: error }, 'Request failed');
});
```

### 4. Decorators (extend request/reply/Fastify instance)

```typescript
// Decorate the Fastify instance (available in all handlers)
fastify.decorate('db', new PrismaClient());
fastify.decorate('verifyToken', (token: string) => jwt.verify(token));

// Decorate the request (via a plugin or hook)
fastify.decorateRequest('user', null);   // Declare the type
fastify.addHook('preHandler', async (request) => {
  request.user = getUserFromToken(request);   // Now request.user is typed
});

// Decorate the reply
fastify.decorateReply('success', function (this: FastifyReply, data: unknown) {
  this.send({ success: true, data });
});

// Usage
fastify.get('/me', async (request, reply) => {
  return reply.success(request.user);   // Typed
});
```

Decorators are how you add functionality to the Fastify instance, request, or reply. They're the Fastify equivalent of Express's `req.foo = bar` — but typed and scoped.

---

## Official Plugin Ecosystem

Fastify has a curated set of official plugins (prefixed with `@fastify/`):

### Common plugins

```bash
npm install @fastify/cors @fastify/helmet @fastify/rate-limit @fastify/jwt @fastify/cookie @fastify/multipart @fastify/static @fastify/swagger @fastify/swagger-ui @fastify/sensible @fastify/under-pressure @fastify/env @fastify/express
```

```typescript
import cors from '@fastify/cors';
import helmet from '@fastify/helmet';
import rateLimit from '@fastify/rate-limit';
import jwt from '@fastify/jwt';
import cookie from '@fastify/cookie';
import multipart from '@fastify/multipart';
import fastifyStatic from '@fastify/static';
import swagger from '@fastify/swagger';
import swaggerUi from '@fastify/swagger-ui';
import sensible from '@fastify/sensible';
import underPressure from '@fastify/under-pressure';
import env from '@fastify/env';

// CORS
app.register(cors, {
  origin: ['https://example.com', 'https://admin.example.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  credentials: true,
});

// Security headers (Helmet)
app.register(helmet, {
  contentSecurityPolicy: {
    directives: { defaultSrc: ["'self'"] },
  },
});

// Rate limiting
app.register(rateLimit, {
  max: 100,
  timeWindow: '1 minute',
  // Per-IP by default; customize with keyGenerator
  keyGenerator: (req) => req.ip,
});

// JWT
app.register(jwt, {
  secret: process.env.JWT_SECRET!,
  sign: { expiresIn: '1h' },
});

// Cookies (required for @fastify/jwt to read cookies, and for sessions)
app.register(cookie, {
  secret: process.env.COOKIE_SECRET!,
  hook: 'onRequest',
});

// Multipart (file uploads)
app.register(multipart, {
  limits: { fileSize: 10 * 1024 * 1024 },   // 10 MB
});

// Static file serving
app.register(fastifyStatic, {
  root: path.join(__dirname, 'public'),
  prefix: '/public/',
});

// Swagger docs (auto-generated from schemas)
app.register(swagger, {
  openapi: { info: { title: 'My API', version: '1.0.0' } },
});
app.register(swaggerUi, { routePrefix: '/docs' });

// @fastify/sensible — error helpers (httpErrors), assertion, etc.
app.register(sensible);
// Now: throw fastify.httpErrors.notFound('User not found')
//      throw fastify.httpErrors.badRequest('Invalid email')

// Under pressure — reject requests when the event loop is overloaded
app.register(underPressure, {
  maxEventLoopDelay: 1000,
  maxHeapUsedBytes: 100000000,
  maxRssBytes: 100000000,
  message: 'Server under pressure',
  retryAfter: 50,
});

// Env schema validation (fail fast on bad config)
const envSchema = {
  type: 'object',
  required: ['DATABASE_URL', 'JWT_SECRET'],
  properties: {
    DATABASE_URL: { type: 'string' },
    JWT_SECRET: { type: 'string', minLength: 32 },
    PORT: { type: 'integer', default: 3000 },
    NODE_ENV: { type: 'string', default: 'development' },
  },
};
app.register(env, { schema: envSchema, dotenv: true });
// app.config.DATABASE_URL, app.config.PORT, etc.
```

### Express middleware compatibility (`@fastify/express`)

```typescript
import express from '@fastify/express';
import passport from 'passport';   // Express middleware

app.register(express);
// Now you can use Express middleware
app.use(passport.initialize());
app.use(passport.session());
```

Use this for migration — run Express middleware inside Fastify while you gradually port to native Fastify plugins.

---

## TypeBox: Schema = Types (no duplication)

TypeBox is the canonical schema library for Fastify + TypeScript. Define a schema once → get validation AND TypeScript types.

```typescript
import { Type, Static } from '@sinclair/typebox';

// Define the schema
const UserSchema = Type.Object({
  id: Type.String(),
  name: Type.String({ minLength: 2, maxLength: 100 }),
  email: Type.String({ format: 'email' }),
  age: Type.Optional(Type.Integer({ minimum: 13 })),
  role: Type.Union([Type.Literal('admin'), Type.Literal('user')], { default: 'user' }),
  tags: Type.Array(Type.String()),
  metadata: Type.Record(Type.String(), Type.Unknown()),
});

// Static<typeof Schema> generates the TypeScript type
type User = Static<typeof UserSchema>;
// { id: string; name: string; email: string; age?: number; role: 'admin' | 'user'; tags: string[]; metadata: Record<string, unknown> }

// Use in a route
fastify.post('/users', {
  schema: {
    body: UserSchema,
    response: { 201: UserSchema },
  },
}, async (request, reply) => {
  const user = request.body;   // Typed as User — no manual interface
  // ...
});
```

### Alternative: JSON Schema to TypeScript (`@fastify/type-provider-json-schema-to-ts`)

If you have existing JSON Schemas (not TypeBox), use this type provider to infer types:

```typescript
import { JsonSchemaToTsProvider } from '@fastify/type-provider-json-schema-to-ts';

const app = Fastify().withTypeProvider<JsonSchemaToTsProvider>();

const userSchema = {
  type: 'object',
  properties: {
    name: { type: 'string' },
    email: { type: 'string', format: 'email' },
  },
  required: ['name', 'email'],
} as const;   // The 'as const' is critical for type inference

app.post('/users', { schema: { body: userSchema } }, async (request) => {
  const { name, email } = request.body;   // Typed from the JSON Schema
  // ...
});
```

---

## Testing (Fastify's `inject()` + tap/vitest/jest)

Fastify's killer testing feature: `app.inject()` — invoke the app's routing without binding a port or making HTTP requests.

```typescript
// test/users.test.ts
import { buildApp } from '../src/app';
import { test, beforeEach, afterEach } from 'tap';

let app: ReturnType<typeof buildApp>;

beforeEach(async () => {
  app = buildApp();
  await app.ready();
});

afterEach(async () => {
  await app.close();
});

test('POST /users creates a user', async (t) => {
  const response = await app.inject({
    method: 'POST',
    url: '/api/users',
    payload: { name: 'Alice', email: 'alice@example.com', age: 30 },
    headers: { 'content-type': 'application/json' },
  });

  t.equal(response.statusCode, 201);
  const body = JSON.parse(response.payload);
  t.equal(body.name, 'Alice');
  t.equal(body.email, 'alice@example.com');
});

test('POST /users with invalid email returns 400', async (t) => {
  const response = await app.inject({
    method: 'POST',
    url: '/api/users',
    payload: { name: 'Alice', email: 'not-an-email' },
    headers: { 'content-type': 'application/json' },
  });

  t.equal(response.statusCode, 400);
  const body = JSON.parse(response.payload);
  t.match(body.message, /email/);
});

test('GET /users/:id with auth', async (t) => {
  const token = app.jwt.sign({ id: 1, email: 'alice@example.com' });

  const response = await app.inject({
    method: 'GET',
    url: '/api/users/42',
    headers: { authorization: `Bearer ${token}` },
  });

  t.equal(response.statusCode, 200);
});
```

`app.inject()` is **synchronous and fast** — no HTTP overhead, no port binding, no network. Tests run in milliseconds.

Cross-reference: `testing-patterns` for general test pyramid / mocking strategies.

---

## Logging (Pino — built-in)

Fastify ships with **pino** — the fastest Node.js logger (3x faster than Winston, 10x faster than Bunyan).

```typescript
const fastify = Fastify({
  logger: {
    level: 'info',
    // Pretty print in dev, JSON in prod
    transport: process.env.NODE_ENV === 'development'
      ? { target: 'pino-pretty', options: { colorize: true } }
      : undefined,
    // Redact sensitive fields
    redact: ['req.headers.authorization', 'req.headers.cookie', 'req.body.password'],
  },
});

// Every request gets a child logger with request ID
fastify.get('/users/:id', async (request, reply) => {
  request.log.info({ userId: request.params.id }, 'Fetching user');
  // Logs: { level: 'info', requestId: 1, userId: '42', msg: 'Fetching user' }
  return user;
});
```

### Structured logging best practices

```typescript
// ✅ Good — structured data
request.log.info({ userId: request.params.id, action: 'fetch' }, 'User fetch');

// ❌ Bad — string interpolation (loses structure)
request.log.info(`Fetching user ${request.params.id}`);
```

Pino logs are JSON by default — pipe to `pino-pretty` in dev for readability, ship JSON to your log aggregator (Datadog, Splunk, ELK) in prod.

---

## Deployment

Fastify runs on standard Node.js — no special runtime needed.

```bash
# Build
npm run build                 # tsc → dist/

# Run
node dist/server.js

# With PM2 (process manager — cluster mode)
npm install -g pm2
pm2 start dist/server.js --name my-api -i max    # -i max = one per CPU core
pm2 logs
pm2 restart my-api
pm2 save
pm2 startup                   # Auto-start on boot
```

### Docker multi-stage build

```dockerfile
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-slim
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY --from=builder /app/dist ./dist
EXPOSE 3000
USER node
CMD ["node", "dist/server.js"]
```

### Performance tuning for production

```typescript
const fastify = Fastify({
  logger: { level: 'info' },   // No pino-pretty in prod
  bodyLimit: 1 * 1024 * 1024,  // 1 MB (default is 1 MB — increase if needed)
  connectionTimeout: 0,        // 0 = no timeout (use reverse proxy for timeouts)
  keepAliveTimeout: 72000,     // 72s (must be > load balancer's idle timeout)
  maxRequestsPerSocket: 0,     // 0 = unlimited
  requestTimeout: 30000,       // 30s
});

// Use cluster mode via PM2 or Node's cluster module
// Fastify itself is single-process — scale horizontally
```

---

## Top 10 Anti-Patterns (the most valuable section)

1. **Not using schemas.** Fastify without schemas is just a faster Express. The schema does THREE jobs (validation + serialization + types) — skipping it wastes the framework's main advantage. Always define `body`, `querystring`, `params`, and `response` schemas.

2. **Using `JSON.stringify` for responses instead of relying on the response schema.** When you define a `response` schema, Fastify compiles it to a `fast-json-stringify` function — 2-3x faster than `JSON.stringify`. Without the response schema, Fastify falls back to `JSON.stringify`. Always define `response` schemas for hot paths.

3. **Treating plugins like Express middleware (expecting global scope).** Fastify plugins are **encapsulated** — decorators and hooks don't leak to the parent unless you wrap with `fastify-plugin` (`fp()`). If you register an auth plugin and then routes can't access `fastify.db`, you forgot `fp()`.

4. **Using `req`/`res` (Express naming).** Fastify uses `request`/`reply`. `request.body` (not `req.body`), `reply.send()` (not `res.send()`), `reply.code(201)` (not `res.status(201)`). Mixing Express naming produces TypeScript errors (good) but signals you haven't internalized the Fastify model.

5. **Registering plugins after routes.** In Fastify, the order of `register()` calls matters — plugins registered AFTER routes won't have their hooks apply to those routes. Register all plugins (cors, helmet, jwt, etc.) BEFORE registering routes.

6. **Not using `app.inject()` for testing.** Writing tests that make real HTTP requests to `localhost:3000` is slow and requires port binding. `app.inject()` invokes the routing pipeline synchronously without HTTP — 100x faster. Always use `inject()` for Fastify tests.

7. **Mutating `request`/`reply` directly.** Use decorators (`fastify.decorateRequest('user', null)`) to add properties to request/reply. Direct mutation (`request.foo = 'bar'`) works in JS but loses type safety and can break with future Fastify versions.

8. **Not using pino for logging.** Fastify ships pino by default. Using `console.log` bypasses pino's structure, request ID correlation, and redaction. Use `request.log.info()` or `fastify.log.info()` — never `console.log()`.

9. **Synchronous work in handlers.** Fastify is fast because it's async — blocking the event loop with sync work (crypto, large JSON.parse, CPU-heavy loops) kills throughput. Use `setImmediate` or worker threads for CPU-bound work.

10. **Not separating `buildApp()` from `listen()`.** Putting `fastify.listen()` in the same file as `buildApp()` makes the app untestable (the port binds on import). Separate them: `buildApp()` returns the instance, `server.ts` calls `listen()`. Tests import `buildApp()` and use `inject()`.

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for Fastify (project onboarding)
- `nestjs` — NestJS can use Fastify as its adapter (`@nestjs/platform-fastify`) — 2x faster than the Express adapter
- `hono` — Edge-runtime equivalent (Cloudflare Workers, Deno, Bun) — Hono is to edge what Fastify is to Node
- `go-web` — Go web patterns (similar stdlib-first philosophy for Go; Fastify is the Node equivalent)
- `fastapi-sqlalchemy` — Python async API (similar schema-driven validation via Pydantic)
- `api-and-interface-design` — Type contract design (Fastify schemas ARE the type contract)
- `api-patterns` — REST API patterns
- `security-and-hardening` — OWASP-aware hardening (@fastify/helmet, @fastify/cors, @fastify/rate-limit cover most concerns)
- `clean-code` — General coding standards applicable to TypeScript
- `testing-patterns` — Test pyramid, mocking strategies (Fastify's `inject()` is the key testing tool)
- `code-review-checklist` — 12-category code review checklist

---

## Dependencies

Required:
- **Node.js** 20+ (or Bun 1.1+ — but Fastify is optimized for Node)
- **Fastify** 5.0+
- **TypeScript** 5+ (optional but recommended — Fastify has first-class TS support)

### Type providers (pick one for TypeScript)

- `@fastify/type-provider-typebox` + `@sinclair/typebox` — schema = types (recommended — TypeBox is the canonical Fastify schema library)
- `@fastify/type-provider-json-schema-to-ts` — infer types from existing JSON Schemas

### Official plugins (install via `npm install`)

- `@fastify/cors` — CORS handling
- `@fastify/helmet` — security headers (CSP, HSTS, X-Frame-Options)
- `@fastify/rate-limit` — rate limiting (per-IP or custom key)
- `@fastify/jwt` — JWT auth (sign + verify)
- `@fastify/cookie` — cookie parsing + signing
- `@fastify/multipart` — file uploads (multipart/form-data)
- `@fastify/static` — static file serving
- `@fastify/swagger` + `@fastify/swagger-ui` — OpenAPI 3 spec generation + Swagger UI
- `@fastify/sensible` — error helpers (`httpErrors.notFound()`), assertion, etc.
- `@fastify/under-pressure` — reject requests when overloaded (event loop lag, memory)
- `@fastify/env` — env var schema validation (fail fast on bad config)
- `@fastify/express` — Express middleware compatibility (for migration)
- `@fastify/session` — server-side sessions (with `@fastify/cookie`)
- `@fastify/passport` — Passport.js integration
- `@fastify/websocket` — WebSocket support
- `@fastify/type-provider-typebox` — TypeBox type provider

### Common additions

- `pino` + `pino-pretty` — logging (Fastify ships pino, but you may want pino-pretty for dev)
- `@prisma/client` + `prisma` — TypeScript ORM
- `drizzle-orm` — alternative TypeScript ORM
- `fastify-plugin` — for writing plugins that leak to the parent scope
- `@fastify/awilix` — DI container via awilix (if you need IoC without NestJS)
- `tap` or `vitest` or `jest` — testing framework (tap is Fastify's default in templates)
- `@fastify/otel` — OpenTelemetry instrumentation
