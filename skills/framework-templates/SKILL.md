---
name: framework-templates
description: Deep reference library for framework-specific CLAUDE.md sections. Contains production-ready templates for Next.js, Laravel, Rails, Django, React Native, Flutter, Go, Rust, and more. Use alongside the claude-md skill for complete CLAUDE.md generation.
version: 2.0.0
skills:
  - claude-md
  - clean-code
  - testing-patterns
trigger: "framework-templates"
runtime: agent
subservices:
  get:
    description: Get template for a specific framework
    trigger: "framework-templates:get"
    process:
      - Identify target framework
      - Navigate to framework H2 section in this document
      - Extract CLAUDE.md Sections subsection (complete markdown block)
      - Extract Build Commands table
      - Extract any relevant patterns/patterns
      - Return complete framework-specific CLAUDE.md content
  list:
    description: List all available framework templates
    trigger: "framework-templates:list"
    process:
      - Reference Framework Index in this document
      - Return list of frameworks with detection patterns
      - Include framework category (Web, Mobile, Desktop, Backend)
  detect:
    description: Detect framework from codebase
    trigger: "framework-templates:detect"
    process:
      - Run detection commands for each framework category
      - Match detection patterns against codebase files
      - Return detected framework with confidence level
      - If multiple matches, prefer most specific (e.g., Next.js over generic React)
  validate:
    description: Validate CLAUDE.md for framework-specific completeness
    trigger: "framework-templates:validate"
    process:
      - Identify framework from CLAUDE.md
      - Check required CLAUDE.md sections are present
      - Verify build commands match actual project scripts
      - Check framework-specific patterns are documented
      - Report missing sections with severity rating
---

# Framework Templates

A deep reference library for framework-specific CLAUDE.md sections. This skill provides production-ready templates, patterns, and conventions for generating accurate CLAUDE.md files across 18+ frameworks and platforms.

**Use this skill alongside `claude-md`** - the `claude-md` skill handles the generation process while this skill provides the framework-specific content.

## Purpose

Each framework has unique patterns, conventions, commands, and pitfalls that must be captured in CLAUDE.md for agents to work effectively. This skill provides:

- **Complete CLAUDE.md sections** for each framework
- **Detection patterns** to identify the framework
- **Command references** verified against actual framework tooling
- **Common pitfalls** to document and avoid
- **Version-specific guidance** for major releases

## How to Use

### Step 1: Identify the Framework

Use the **Framework Index** below or run detection commands:

```bash
# Detect from package manager
cat package.json 2>/dev/null | head -5
cat composer.json 2>/dev/null | head -5
cat requirements.txt 2>/dev/null | head -5
cat pyproject.toml 2>/dev/null | head -5
cat go.mod 2>/dev/null | head -5
cat Cargo.toml 2>/dev/null | head -5
cat pubspec.yaml 2>/dev/null | head -5
cat Gemfile 2>/dev/null | head -10

# Detect from file structure
find . -maxdepth 2 \( \
  -name "next.config.*" -o -name "vite.config.*" -o -name "nuxt.config.*" \
  -o -name "artisan" -o -name "config.ru" -o -name "manage.py" \
  -o -name "pubspec.yaml" -o -name "go.mod" -o -name "pom.xml" \
  -o -name "build.gradle" -o -name "mix.exs" \
\) 2>/dev/null
```

### Step 2: Get Framework Template

Navigate to the framework section in this skill and extract:

1. **Detection Section**: Verify framework match
2. **CLAUDE.md Sections**: Copy the complete sections (the ready-to-use markdown)
3. **Build Commands**: Copy the command reference table
4. **Patterns & Pitfalls**: Copy framework-specific guidance

### Step 3: Integrate into CLAUDE.md

```markdown
## Implementation Standards

### [Framework] Specific

{Paste CLAUDE.md Sections content here}

## Development Workflow

### Build Commands

| Command | Purpose |
|---------|---------|
{Paste Build Commands table here}

{Continue with other framework sections}
```

### Step 4: Validate

```bash
# Verify commands exist in package.json
cat package.json | jq '.scripts' 2>/dev/null

# Verify framework detection
cat package.json | grep -E '"(next|nuxt|react|laravel|rails)"' 2>/dev/null
```

## Framework Index

### Web Frameworks

| Framework | Detection | Language | Sections |
|-----------|-----------|----------|----------|
| [Next.js](#nextjs) | `next.config.js` | TypeScript | App Router, Image, Metadata, Server Actions |
| [Nuxt.js](#nuxtjs) | `nuxt.config.ts` | TypeScript | Auto-imports, SSR, Server routes |
| [Vite + React](#vite--react) | `vite.config.js` | TypeScript | Component patterns, state management |
| [SvelteKit](#sveltekit) | `svelte.config.js` | TypeScript | File routing, form actions, stores |
| [Astro](#astro) | `astro.config.mjs` | TypeScript | Islands, content collections |
| [Laravel](#laravel) | `artisan` | PHP | Form Requests, Policies, Jobs, Events |
| [Rails](#rails) | `config.ru` | Ruby | MVC, ActiveRecord, Concerns, Service Objects |
| [Django](#django) | `manage.py` | Python | Models, Views, Forms, Admin |
| [FastAPI](#fastapi) | `pyproject.toml` | Python | Pydantic, Routers, Dependencies |
| [Express/Fastify](#express--fastify) | `package.json` | JavaScript | Middleware, routing patterns |

### Mobile Frameworks

| Framework | Detection | Language | Sections |
|-----------|-----------|----------|----------|
| [React Native](#react-native) | `App.tsx` + `app.json` | TypeScript | Navigation, Platform modules, Native |
| [Flutter](#flutter) | `pubspec.yaml` | Dart | Widgets, State, Clean Architecture |

### Desktop Frameworks

| Framework | Detection | Language | Sections |
|-----------|-----------|----------|----------|
| [Electron](#electron) | `package.json` + `electron` | TypeScript | Main/Renderer, IPC, Native modules |
| [Tauri](#tauri) | `Cargo.toml` + `src-tauri/` | Rust/JS | Rust backend, web frontend |
| [ASP.NET Core](#aspnet-core) | `*.csproj` | C# | Project structure, dependency injection |

### Backend Frameworks

| Framework | Detection | Language | Sections |
|-----------|-----------|----------|----------|
| [Go](#go) | `go.mod` | Go | Project structure, error handling |
| [Rust](#rust) | `Cargo.toml` | Rust | Ownership, error handling, traits |
| [Phoenix](#phoenix) | `mix.exs` | Elixir | Ecto, Channels, LiveView |

---

# Web Frameworks

## Next.js

**Detection:** `next.config.js` or `next.config.ts` in project root

### Detection Commands

```bash
# Verify Next.js in package.json
cat package.json | jq '.dependencies.next' 2>/dev/null
cat package.json | grep '"next":' 2>/dev/null

# Verify config file exists
ls next.config.js next.config.ts 2>/dev/null

# Check for App Router structure
ls app/ 2>/dev/null | head -5
```

### Detection Patterns

```json
// package.json
{
  "dependencies": {
    "next": "^14.0.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0"
  }
}
```

```typescript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
};

module.exports = nextConfig;
```

### CLAUDE.md Sections

```markdown
## Implementation Standards

### Next.js 14+ Specific

- **App Router**: Use `app/` directory for all routes and layouts
- **Server Components**: Default to Server Components; add `'use client'` only when interactivity needed
- **Next.js Image**: Use `<Image>` component for all images (optimization, lazy loading, CLS prevention)
- **next/font**: Use `next/font` for Google Fonts (zero layout shift, self-hosted)
- **Metadata API**: Use `generateMetadata()` and `export const metadata` for SEO
- **Server Actions**: Use Server Actions for form submissions and mutations
- **Route Handlers**: Use `app/api/*/route.ts` only for external API integrations
- **Partial Prerendering (PPR)**: Use `dynamic()` with Suspense for streaming

### TypeScript Strict Mode

- `strict: true` in `tsconfig.json`
- Never use `any` - use `unknown` instead
- Explicit types on all function parameters
- Use `interface` for object shapes, `type` for unions/intersections
- All API routes return typed responses

### React Patterns

- **Client Components**: Only when using `useState`, `useEffect`, event handlers
- **Server Components**: Fetch data, render UI, access backend directly
- **Composition**: Co-locate `Component.tsx` with `Component.test.tsx` and `Component.module.css`
- **Error Handling**: Use `error.tsx` and `loading.tsx` at every route segment
```

### Build Commands

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start development server (http://localhost:3000) |
| `npm run build` | Production build with static optimization |
| `npm run start` | Start production server |
| `npm run lint` | ESLint + Prettier |
| `npm run typecheck` | TypeScript type checking |
| `npm test` | Run Jest tests |
| `npm run test:watch` | Watch mode for tests |
| `npm run test:coverage` | Coverage report |

### Database Patterns

```markdown
### Prisma ORM

- Schema location: `prisma/schema.prisma`
- Always run `npx prisma generate` after schema changes
- Use Prisma Studio for data exploration: `npx prisma studio`
- Migrations: `npx prisma migrate dev --name descriptive_name`
- Seed data: `npx prisma db seed`

### Prisma Commands

| Command | Purpose |
|---------|---------|
| `npx prisma generate` | Generate Prisma client |
| `npx prisma db push` | Push schema changes |
| `npx prisma migrate dev` | Create migration |
| `npx prisma db seed` | Seed database |
| `npx prisma studio` | Open database GUI |
```

### API Patterns

```markdown
### Route Handlers

- Location: `app/api/{resource}/route.ts`
- Method handlers: `GET`, `POST`, `PUT`, `DELETE` exports
- Request validation: Zod schemas
- Response format: Consistent JSON structure

### API Response Format

```typescript
// Success
return Response.json({ data: result, meta?: { page, total } })

// Error
return Response.json(
  { error: { code: 'NOT_FOUND', message: 'Resource not found' } },
  { status: 404 }
)
```
```

### Common Pitfalls

```markdown
### Pitfalls to Avoid

1. **Client Component overuse**: Default to Server Components; add interactivity only where needed
2. **Missing error boundaries**: Create `error.tsx` at every route segment
3. **No loading states**: Create `loading.tsx` for streaming UI
4. **Inline styles**: Use Tailwind or CSS Modules, never style props
5. **Importing Server Components in Client Components**: Creates boundary violations
6. **Missing image optimization**: Use `<Image>` not `<img>` for all images
7. **Unoptimized fonts**: Use `next/font` not `<link>` for Google Fonts
8. **Client-side data fetching**: Use Server Components or Server Actions instead
```

### Version-Specific Notes

```markdown
**Next.js 14.1+**
- CSS Modules in Server Components: Import directly (no barrel file imports)
- Server Actions: Can be nested in layout.tsx for form handling

**Next.js 14.2+**
- Partial Prerendering: Use `dynamic()` with `loading` prop for Suspense boundaries
- tRPC integration: Use `@trpc/server` with App Router adapter
```

---

## Nuxt.js

**Detection:** `nuxt.config.ts` or `nuxt.config.js` in project root

### Detection Commands

```bash
# Verify Nuxt in package.json
cat package.json | grep '"nuxt":' 2>/dev/null

# Verify config file exists
ls nuxt.config.ts nuxt.config.js 2>/dev/null

# Check for Nuxt directory structure
ls app/ pages/ layouts/ 2>/dev/null
```

### Detection Patterns

```json
// package.json
{
  "dependencies": {
    "nuxt": "^3.10.0"
  }
}
```

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt'],
});
```

### CLAUDE.md Sections

```markdown
## Implementation Standards

### Nuxt 3 Specific

- **Auto-imports**: Components, composables, utils auto-imported (no explicit imports needed)
- **File-based Routing**: `pages/` directory generates routes automatically
- **Layouts**: `layouts/` directory for shared layouts
- **Server Routes**: `server/api/` for API endpoints (Nitro server)
- **useFetch**: Use `useFetch` and `useAsyncData` for data fetching (SSR-friendly)
- **Composables**: Place reusable logic in `composables/` (auto-imported)
- **Middleware**: Route middleware in `middleware/` (auto-registered)
- **Plugins**: Run setup code in `plugins/` (client/server aware)

### TypeScript

- Enable `strict: true` in nuxt.config.ts
- Use `defineProps`, `defineEmits` macros
- Type `$fetch` responses explicitly
- Use `ref<T>()` and `reactive<T>()` for typed state

### Pinia State Management

- Use `@pinia/nuxt` module
- Define stores in `stores/` directory
- Use `defineStore` with Setup Store syntax for TypeScript
```

### Build Commands

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start development server (http://localhost:3000) |
| `npm run build` | Production build |
| `npm run generate` | Static site generation (SSG) |
| `npm run preview` | Preview production build |
| `npm run lint` | ESLint |
| `npm run typecheck` | TypeScript checking |
| `npx nuxi prepare` | Generate TypeScript types |
| `npx nuxi info` | Debug Nuxt configuration |

### Common Pitfalls

```markdown
### Pitfalls to Avoid

1. **Manual imports**: Nuxt auto-imports - don't import what you don't need to
2. **Client-only code**: Use `onMounted` or `<ClientOnly>` component
3. **Missing `useFetch` key**: Always provide unique key for caching
4. **SSR hydration mismatch**: Use `ref`/`reactive` consistently (not plain objects)
5. **API route testing**: Mock `$fetch` in unit tests
```

### Version-Specific Notes

```markdown
**Nuxt 3.10+**
- `useFetch` with automatic caching
- `useNuxtData` for pre-populating fetch caches
- Server component support
```

---

## Vite + React

**Detection:** `vite.config.js` or `vite.config.ts` + `package.json` with React

### Detection Commands

```bash
# Verify React and Vite in package.json
cat package.json | jq '.dependencies.react' 2>/dev/null
cat package.json | jq '.devDependencies.vite' 2>/dev/null

# Verify config file exists
ls vite.config.ts vite.config.js 2>/dev/null
```

### Detection Patterns

```json
// package.json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "@vitejs/plugin-react": "^4.2.0"
  }
}
```

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
});
```

### CLAUDE.md Sections

```markdown
## Implementation Standards

### Vite Specific

- **HMR**: Hot Module Replacement enabled by default
- **Environment Variables**: `VITE_*` prefix for client-side vars
- **Import Aliases**: Configure in vite.config.ts (e.g., `@/` → `src/`)
- **Build Optimization**: Code splitting, lazy loading automatic
- **TypeScript**: Use `vite-plugin-checker` for type checking in dev

### React Patterns

- **Functional Components**: Only functional components (no class components)
- **Hooks**: Use hooks for all state and side effects
- **Colocation**: Keep component, test, and styles together
- **Custom Hooks**: Extract reusable logic to `hooks/` directory

### State Management

```typescript
// Local state: useState
const [state, setState] = useState<Type>(initial);

// Derived state: useMemo
const derived = useMemo(() => compute(state), [state]);

// Side effects: useEffect
useEffect(() => {
  // effect
  return () => { /* cleanup */ };
}, [dependencies]);

// Server state: TanStack Query
const { data, isLoading, error } = useQuery({ queryKey: ['key'], queryFn: fn });

// Global state: Zustand (lightweight)
```

### Styling

```typescript
// CSS Modules (preferred for component styles)
import styles from './Component.module.css';

// Tailwind CSS (utility classes)
import clsx from 'clsx';
```

### Build Commands

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start Vite dev server |
| `npm run build` | Production build |
| `npm run preview` | Preview production build |
| `npm run lint` | ESLint + Prettier |
| `npm run typecheck` | TypeScript checking |
| `npm test` | Run tests (Vitest/Jest) |
| `npm run test:coverage` | Coverage report |

### Common Pitfalls

```markdown
### Pitfalls to Avoid

1. **Prop drilling**: Use Context or Zustand instead
2. **Callback hell**: Use React Query for server state
3. **Over-fetching**: Specify exact fields needed
4. **Missing dependencies**: Include all deps in useEffect/useCallback arrays
5. **Memory leaks**: Always return cleanup from useEffect
6. **Unused state**: Don't state what can be computed
```

### Version-Specific Notes

```markdown
**Vite 5.0+**
- Native ESM dev server is now default (no more `@vitejs/plugin-legacy` for modern only)
- `vite-plugin-pwa` for PWA support has breaking changes in v0.5+
- Rollup 4.0 improves build performance by ~20%

**React 19 (when applicable)**
- Actions are now first-class (useFormAction, useFormState)
- Server Components are stable but require framework support
- New `use()` hook for reading promises/context in components
```

---

## SvelteKit

**Detection:** `svelte.config.js` + `src/routes/` directory

### Detection Commands

```bash
# Verify SvelteKit in package.json
cat package.json | grep '"@sveltejs/kit":' 2>/dev/null

# Verify config file exists
ls svelte.config.js 2>/dev/null

# Check for routes directory
ls src/routes/ 2>/dev/null
```

### Detection Patterns

```json
// package.json
{
  "devDependencies": {
    "@sveltejs/kit": "^2.0.0",
    "svelte": "^4.2.0",
    "vite": "^5.0.0"
  }
}
```

```javascript
// svelte.config.js
import adapter from '@sveltejs/adapter-auto';

export default {
  kit: {
    adapter: adapter(),
  },
};
```

### CLAUDE.md Sections

```markdown
## Implementation Standards

### SvelteKit 2.0 Specific

- **File-based Routing**: `src/routes/` generates routes from file structure
- **Server vs Client**: `+page.server.ts` for server logic, `+page.svelte` for UI
- **Form Actions**: Use `actions` in `+page.server.ts` for form submissions
- **Loaders**: Use `load` functions for data fetching
- **Stores**: Use Svelte stores for cross-component state
- **TypeScript**: Enable `strict` mode in svelte.config.js

### SvelteKit Load Function

```typescript
// src/routes/+page.server.ts
export const load = async ({ fetch, locals }) => {
  const user = locals.user; // from hooks
  const posts = await fetch('/api/posts').then(r => r.json());
  return { user, posts };
};
```

### SvelteKit Form Actions

```typescript
// src/routes/+page.server.ts
export const actions = {
  default: async ({ request }) => {
    const data = await request.formData();
    const title = data.get('title');

    await db.post.create({ data: { title } });
    return { success: true };
  },
};
```

### Build Commands

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start development server |
| `npm run build` | Production build |
| `npm run preview` | Preview production build |
| `npm run check` | TypeScript and Svelte check |
| `npx svelte-kit sync` | Sync types |
| `npm run test` | Run tests |

### Common Pitfalls

```markdown
### Pitfalls to Avoid

1. **Missing +page.server.ts**: Data fetching should use load functions, not component script
2. **Client-side mutation**: Use form actions for mutations, not fetch in on:click
3. **Missing form validation**: Validate in actions, not just component
4. **Direct DOM manipulation**: Svelte handles reactivity; don't manually query DOM
```

---

## Astro

**Detection:** `astro.config.mjs` + `src/pages/` directory

### Detection Commands

```bash
# Verify Astro in package.json
cat package.json | grep '"astro":' 2>/dev/null

# Verify config file exists
ls astro.config.mjs 2>/dev/null

# Check for pages directory
ls src/pages/ 2>/dev/null
```

### Detection Patterns

```json
// package.json
{
  "dependencies": {
    "astro": "^4.0.0"
  }
}
```

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
});
```

### CLAUDE.md Sections

```markdown
## Implementation Standards

### Astro 4.0 Specific

- **Islands Architecture**: Interactive components use `client:*` directives
- **Content Collections**: Use `src/content/` for typed content management
- **Zero JS by default**: Only hydrate components marked with `client:*`
- **Server Output**: Configure `output: 'server'` or `output: 'hybrid'` for SSR

### Client Directives

```astro
<!-- Load on page load -->
<MyComponent client:load />

<!-- Load when visible -->
<MyComponent client:visible />

<!-- Load on idle -->
<MyComponent client:idle />

<!-- Load on interaction -->
<MyComponent client:visible />
```

### Content Collections

```typescript
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    pubDate: z.date(),
    description: z.string(),
  }),
});

export const collections = { blog };
```
```

### Build Commands

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start development server |
| `npm run build` | Production build |
| `npm run preview` | Preview production build |
| `npm run check` | TypeScript checking |

### Common Pitfalls

```markdown
### Pitfalls to Avoid

1. **Over-hydration**: Only use `client:*` when component needs interactivity
2. **Missing image optimization**: Use `<Image>` component from `astro:assets`
3. **Mixing SSR modes**: Choose `output: 'static'` or `output: 'server'` consistently
4. **Content collection schema**: Always define schema, don't use `any`
```

### Version-Specific Notes

```markdown
**Astro 4.0+**
- Content Collections now use `defineCollection` with type-safe schemas
- `getStaticPaths` replaced by `getCollection` for dynamic routes
- Server output modes: 'static', 'hybrid', 'server' (previously 'server' was 'output: server')

**Astro 5.0+**
- Content Layer API for connecting to CMS, databases, or other sources
- Built-in image optimization with `<Image>` from `astro:assets`
- Server rendering is now opt-in per-route with `export const prerender = false`
```

---

## Laravel

**Detection:** `artisan` file in project root + `composer.json`

### Detection Commands

```bash
# Verify Laravel
ls artisan 2>/dev/null && echo "Laravel detected"
cat composer.json | grep '"laravel/framework":' 2>/dev/null
php artisan --version 2>/dev/null
```

### Detection Patterns

```json
// composer.json
{
  "require": {
    "laravel/framework": "^11.0"
  }
}
```

### CLAUDE.md Sections

```markdown
## Implementation Standards

### Laravel 11+ Specific

- **Bootstrap Directory**: `bootstrap/app.php` for app configuration
- **Rate Limiting**: Use RateLimiter facade (no middleware files)
- **Health Check**: `/up` route built-in
- **Exception Handler**: `bootstrap/app.php` inline config
- **API Scaffolding**: `php artisan install:api` for API-only setup

### Form Request Validation

```php
// REQUIRED: Use Form Request classes for ALL validation
class StorePostRequest extends FormRequest
{
    public function authorize(): bool { return true; }
    public function rules(): array {
        return [
            'title' => ['required', 'string', 'max:255'],
            'content' => ['required', 'string'],
            'tags' => ['array'],
            'tags.*' => ['exists:tags,id'],
        ];
    }
}
```

### Authorization Policies

```php
// REQUIRED: Use Policy classes for authorization
class PostPolicy
{
    public function create(User $user): bool {
        return $user->role === 'author';
    }
    public function update(User $user, Post $post): bool {
        return $user->id === $post->user_id;
    }
}
```

### Service Layer Pattern

```markdown
### When to Use Services

- Complex business logic spanning multiple models
- External API integrations
- Operations requiring transactions
- Reusable business operations across controllers

### Service Location

- `app/Services/` - Application services
- `app/Integrations/` - External API clients
- `app/Billing/` - Payment processing
```

### Jobs for Long-Running Operations

```markdown
### When to Use Jobs

- Email sending
- File processing (images, videos, documents)
- Third-party API calls
- Large database operations

### Queue Connection

```php
class ProcessPostMediaJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;
    public int $backoff = 60;

    public function __construct(public Post $post) {}

    public function handle(MediaProcessor $processor): void
    {
        $processor->processImages($this->post);
    }
}
```
```

### Events for Decoupled Side Effects

```markdown
### When to Use Events

- Side effects that may grow over time
- Multiple listeners for one action
- Integration with external services

### Event Example

```php
class PostPublished
{
    use Dispatchable, SerializesModels;
    public function __construct(public Post $post) {}
}
```
```

### PHP 8.3+ Standards

```markdown
### Modern PHP Patterns

```php
// Constructor property promotion
public function __construct(
    private PostRepository $posts,
    private TagRepository $tags,
) {}

// Enums for fixed sets
enum PostStatus: string
{
    case Draft = 'draft';
    case Published = 'published';
}

// Named arguments
$post->update([
    'title' => $title,
    'content' => $content,
]);
```
```

### Build Commands

| Command | Purpose |
|---------|---------|
| `php artisan` | List all commands |
| `php artisan serve` | Start development server |
| `php artisan migrate` | Run migrations |
| `php artisan migrate:fresh --seed` | Reset + seed |
| `php artisan db:studio` | Open database GUI |
| `php artisan test` | Run Pest tests |
| `php artisan test --parallel` | Parallel execution |
| `php artisan test --coverage` | Coverage report |
| `php artisan route:list` | List all routes |
| `php artisan route:list --path=api` | API routes only |
| `php artisan schedule:work` | Run scheduler locally |
| `php artisan queue:work` | Process queue |

### Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `APP_ENV` | Environment | `local`, `production` |
| `APP_DEBUG` | Debug mode | `true`, `false` |
| `APP_URL` | Application URL | `https://example.com` |
| `DB_CONNECTION` | Database driver | `pgsql`, `mysql` |
| `DB_HOST` | Database host | `127.0.0.1` |
| `DB_DATABASE` | Database name | `myapp` |
| `CACHE_DRIVER` | Cache driver | `redis`, `file` |
| `QUEUE_CONNECTION` | Queue driver | `redis`, `sync` |
| `SESSION_DRIVER` | Session driver | `redis`, `database` |

### Common Pitfalls

```markdown
### Pitfalls to Avoid

1. **Inline validation**: Always use Form Request classes
2. **Inline authorization**: Always use Policy classes
3. **N+1 queries**: Always eager load relationships with `with()`
4. **Synchronous processing**: Use Jobs for long-running tasks
5. **Direct notifications**: Use Events + Listeners
6. **Raw SQL**: Use Eloquent or Query Builder
```

### Version-Specific Notes

```markdown
**Laravel 11+**
- Bootstrap configuration moved to `bootstrap/app.php`
- Rate limiting configured via RateLimiter facade (not middleware files)
- API scaffolding via `php artisan install:api`
- Health check route `/up` is built-in
- Exception handler configured inline in `bootstrap/app.php`

**Laravel 12+**
- New Laravel Reverb for real-time WebSocket broadcasting
- Laravel Pennant for feature flags
- Per-second rate limiting
- Improved queue monitoring with Horizon 5.0
```

---

## Rails

**Detection:** `config.ru` + `Gemfile` with `rails` gem

### Detection Commands

```bash
# Verify Rails
cat Gemfile | grep "gem 'rails'" 2>/dev/null
ls config.ru 2>/dev/null
```

### Detection Patterns

```ruby
# Gemfile
gem 'rails', '~> 7.1'
```

### CLAUDE.md Sections

```markdown
## Implementation Standards

### Rails 7+ Conventions

- **CoC**: Convention over Configuration
- **DRY**: Don't Repeat Yourself
- **RESTful**: Resources for all models; 7 standard actions per controller

### Directory Structure

```
app/
  controllers/     # ApplicationController + resource controllers
  models/          # ActiveRecord models
  views/           # Templates (ERB, Haml, Slim)
  services/        # Service objects (custom)
  jobs/            # Active Job classes
  mailers/         # Action Mailer classes
config/
  routes.rb        # Route definitions
db/
  migrate/         # Database migrations
spec/              # RSpec tests
  factories/       # FactoryBot factories
```

### MVC Patterns

```ruby
# Models: Business logic + associations + validations
class Post < ApplicationRecord
  belongs_to :author, class_name: 'User', inverse_of: :posts
  has_many :comments, dependent: :destroy
  has_and_belongs_to_many :tags

  validates :title, presence: true, length: { maximum: 255 }

  scope :published, -> { where.not(published_at: nil) }

  def publish!
    update!(published_at: Time.current)
  end
end
```

### Service Objects

```ruby
# For complex business logic
class PublishPostService
  def initialize(post)
    @post = post
  end

  def call
    ActiveRecord::Base.transaction do
      @post.publish!
      send_notifications
    end
  end

  private

  def send_notifications
    @post.subscribers.each do |subscriber|
      PostMailer.with(post: @post, subscriber: subscriber)
                .published.deliver_later
    end
  end
end
```

### Background Jobs (Sidekiq)

```ruby
class ProcessPostMediaJob
  include Sidekiq::Job

  sidekiq_options retry: 3, dead: true

  def perform(post_id)
    post = Post.find(post_id)
    MediaProcessor.call(post)
  end
end
```

### Build Commands

| Command | Purpose |
|---------|---------|
| `rails server` or `rails s` | Start development server |
| `rails console` or `rails c` | Rails console |
| `rails db:migrate` | Run migrations |
| `rails db:migrate:fresh db:seed` | Reset + seed |
| `rails routes` | List routes |
| `rails test` | Run all tests |
| `rspec` | Run RSpec tests |
| `rubocop` | Run linter |
| `rubocop -A` | Auto-fix linting issues |

### Common Pitfalls

```markdown
### Pitfalls to Avoid

1. **Fat controllers**: Extract logic to Service Objects
2. **Fat models**: Extract logic to Concerns or Service Objects
3. **N+1 queries**: Always eager load: `includes(:assoc)`
4. **Callbacks in models**: Prefer explicit service methods
5. **Direct SQL**: Use ActiveRecord, then Arel, then raw SQL
```

---

## Django

**Detection:** `manage.py` + `settings.py`

### Detection Commands

```bash
# Verify Django
ls manage.py 2>/dev/null && echo "Django detected"
grep "django" requirements.txt 2>/dev/null
```

### Detection Patterns

```python
# requirements.txt
Django>=5.0
djangorestframework>=3.14
```

### CLAUDE.md Sections

```markdown
## Implementation Standards

### Django 5.0+ Conventions

- **MTV**: Model-Template-View architecture
- **Explicit over implicit**: Import what you use
- **Fat models, thin views**: Business logic in models/services
- **Migrations always**: Never modify database directly

### Project Structure

```
project/
  manage.py
  project/
    settings.py
    urls.py
  apps/
    posts/
      models.py
      views.py
      urls.py
      services.py
      tests.py
```

### Models

```python
class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
        ]

    def publish(self):
        self.published_at = timezone.now()
        self.save()
```

### Views (Class-Based)

```python
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin

class PostListView(ListView):
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.published().select_related('author')
```

### Services Pattern

```python
# apps/posts/services.py
class PostService:
    @staticmethod
    def create(author, title, content, tags=None):
        post = Post.objects.create(
            author=author,
            title=title,
            content=content,
        )
        if tags:
            post.tags.set(tags)
        return post
```

### Build Commands

| Command | Purpose |
|---------|---------|
| `python manage.py runserver` | Development server |
| `python manage.py shell` | Django shell |
| `python manage.py makemigrations` | Create migrations |
| `python manage.py migrate` | Apply migrations |
| `python manage.py createsuperuser` | Create admin user |
| `python manage.py test` | Run tests |
| `python manage.py test apps.posts` | Run specific app tests |
| `flake8` | Run flake8 linter |
| `black .` | Format code |

### Common Pitfalls

```markdown
### Pitfalls to Avoid

1. **Importing in views.py**: Use services layer for business logic
2. **N+1 queries**: Use `select_related()` and `prefetch_related()`
3. **Direct ORM in templates**: Prepare data in views
4. **Skipping migrations**: Always create migrations for DB changes
```

### Version-Specific Notes

```markdown
**Django 5.0+**
- Generated columns in models: `models.GeneratedField()`
- `default_auto_field` defaults to `BigAutoField` for new projects
- Database default values can be set directly in model field definitions
- Improved async support for ORM operations

**Django 4.2+**
- Asynchronous views and ORM are now stable
- `STORING` computed model fields (alternative to `@property`)
- Sensitive parameters excluded from error logs by default
- Built-in support for PostgreSQL's `search` lookup
```

---

## FastAPI

**Detection:** `pyproject.toml` + `fastapi` dependency

### Detection Commands

```bash
# Verify FastAPI
grep -i fastapi requirements.txt 2>/dev/null
grep fastapi pyproject.toml 2>/dev/null
```

### Detection Patterns

```toml
# pyproject.toml
[project.dependencies]
fastapi = "^0.109.0"
uvicorn = { extras = ["standard"], version = "^0.27.0" }
```

### CLAUDE.md Sections

```markdown
## Implementation Standards

### FastAPI Standards

- **Pydantic**: All request/response models use Pydantic
- **Dependency Injection**: Use FastAPI's `Depends()` for shared logic
- **Async**: Default to async
- **Type hints**: Required for all function parameters
- **Status codes**: Explicit HTTP status codes

### Project Structure

```
app/
  main.py           # FastAPI app entry point
  config.py         # Settings
  dependencies.py   # Shared dependencies
  models/           # SQLAlchemy models
  schemas/          # Pydantic models
  routers/          # API routers
  services/         # Business logic
  crud/             # Database operations
```

### Pydantic Models

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)

class PostCreate(PostBase):
    tags: list[int] = []

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int
    created_at: datetime

class PaginatedResponse(BaseModel):
    items: list[PostResponse]
    total: int
    page: int
```

### Routers

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=PaginatedResponse)
def list_posts(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    posts, total = post_crud.paginate(db, page=page, size=size)
    return PaginatedResponse(items=posts, total=total, page=page)
```

### Build Commands

| Command | Purpose |
|---------|---------|
| `uvicorn app.main:app --reload` | Development server |
| `uvicorn app.main:app --workers 4` | Production |
| `python -m pytest` | Run tests |
| `python -m pytest --cov` | Coverage report |
| `black .` | Format code |
| `ruff check .` | Lint code |
| `mypy app/` | Type checking |

### Common Pitfalls

```markdown
### Pitfalls to Avoid

1. **Sync endpoints for async DB**: Use async SQLAlchemy or run sync in executor
2. **Missing error handling**: Use custom exception handlers
3. **No pagination**: Always paginate list endpoints
4. **Missing validation**: Use Pydantic for all I/O
```

---

## Express / Fastify

**Detection:** `package.json` with `express` or `fastify` dependency

### Detection Commands

```bash
# Verify Express/Fastify
cat package.json | grep -E '"(express|fastify)":' 2>/dev/null
```

### Detection Patterns

```json
// package.json (Express)
{
  "dependencies": {
    "express": "^4.18.0"
  }
}

// package.json (Fastify)
{
  "dependencies": {
    "fastify": "^4.26.0"
  }
}
```

### CLAUDE.md Sections

```markdown
## Implementation Standards

### Express Patterns

- **Middleware**: Chain middleware for request processing
- **Route handlers**: Keep controllers thin, use service layer
- **Error handling**: Use error-handling middleware
- **Validation**: Use `joi`, `zod`, or `express-validator`

### Express Middleware Pattern

```javascript
// middleware/auth.js
const auth = async (req, res, next) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    req.user = await verifyToken(token);
    next();
  } catch (error) {
    res.status(401).json({ error: 'Unauthorized' });
  }
};
```

### Fastify Patterns

```javascript
// fastify route
fastify.get('/posts', {
  schema: {
    response: {
      200: {
        type: 'object',
        properties: {
          posts: { type: 'array' },
          total: { type: 'number' },
        },
      },
    },
  },
  handler: async (request, reply) => {
    const posts = await postService.findAll();
    return { posts, total: posts.length };
  },
});
```

### Build Commands

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm start` | Start production server |
| `npm test` | Run tests |
| `npm run lint` | ESLint |
| `npm run typecheck` | TypeScript checking |

### Common Pitfalls

```markdown
### Pitfalls to Avoid

1. **Callback hell**: Use async/await consistently
2. **No error handling**: Always wrap in try/catch or use error middleware
3. **N+1 in loops**: Batch queries or use eager loading
4. **Missing validation**: Validate all input with Zod/Joi
```

### Version-Specific Notes

```markdown
**Express 5.0+**
- Async route handlers natively supported (no need for express-async-handler)
- Removed `res.redirect('back')` - use `res.redirect(-1)` instead
- Router-level middleware execution order changed

**Fastify 4.26+**
- Native support for `@fastify/multipart` (formerly separate plugin)
- Scoped serialization schemas (per-route response schema)
- `initiate` lifecycle hook for plugin initialization
- Improved TypeScript typings (generated from JSON Schema)
```

---

# Mobile Frameworks

## React Native

**Detection:** `App.tsx` + `app.json` + `package.json` with `react-native`

### Detection Commands

```bash
# Verify React Native
cat package.json | grep '"react-native"' 2>/dev/null
ls App.tsx app.json 2>/dev/null
```

### Detection Patterns

```json
// package.json
{
  "dependencies": {
    "react-native": "0.76.0",
    "react": "18.2.0"
  }
}
```

### CLAUDE.md Sections

```markdown
## Implementation Standards

### React Native 0.76+ Specific

- **New Architecture**: TurboModules enabled by default
- **TypeScript**: Required
- **Hermes**: JS engine enabled by default
- **Fabric**: New renderer enabled by default
- **Auto-linking**: Native modules auto-linked

### Directory Structure

```
src/
  components/       # Reusable UI components
  screens/          # Screen components
  navigation/       # React Navigation config
  hooks/            # Custom hooks
  services/         # API, storage, etc.
  store/            # State management
  types/            # TypeScript types
```

### Navigation Patterns

```typescript
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

export type RootStackParamList = {
  Main: undefined;
  Details: { id: string };
};

const Stack = createNativeStackNavigator<RootStackParamList>();
```

### Platform-Specific Code

```typescript
import { Platform, PlatformIOS } from 'react-native';

const padding = Platform.select({
  ios: 16,
  android: 12,
  default: 16,
});
```

### State Management (Zustand)

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      login: async (email, password) => {
        const response = await api.login(email, password);
        set({ user: response.user, token: response.token });
      },
      logout: () => set({ user: null, token: null }),
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
```

### Build Commands

| Command | Purpose |
|---------|---------|
| `npm start` | Metro bundler |
| `npx react-native run-ios` | Run on iOS simulator |
| `npx react-native run-android` | Run on Android emulator |
| `cd ios && pod install` | Install CocoaPods |
| `npm test` | Run Jest tests |
| `npm run lint` | ESLint |
| `npm run typecheck` | TypeScript |

### Common Pitfalls

```markdown
### Pitfalls to Avoid

1. **Bridge modules**: Use TurboModules (RN 0.76+ default)
2. **No TypeScript**: Always use TypeScript
3. **Hardcoded dimensions**: Use StyleSheet.scale with caution
4. **Memory leaks**: Clean up subscriptions in useEffect cleanup
5. **List rendering**: Use FlatList with proper keyExtractor
```

---

## Flutter

**Detection:** `pubspec.yaml` + `lib/` directory

### Detection Commands

```bash
# Verify Flutter
cat pubspec.yaml | grep "flutter:" 2>/dev/null
ls pubspec.yaml lib/main.dart 2>/dev/null
```

### Detection Patterns

```yaml
# pubspec.yaml
name: my_app
environment:
  sdk: '>=3.4.0 <4.0.0'
dependencies:
  flutter:
    sdk: flutter
```

### CLAUDE.md Sections

```markdown
## Implementation Standards

### Flutter 3.19+ Conventions

- **Dart 3.4+**: Null safety required
- **Clean Architecture**: UI → Domain → Data layers
- **Immutable**: Use `final` and immutable data classes

### Directory Structure

```
lib/
  main.dart
  app/
    app.dart
    router.dart
  core/
    constants/
    errors/
  data/
    datasources/
    models/
    repositories/
  domain/
    entities/
    repositories/
    usecases/
  presentation/
    pages/
    widgets/
    bloc/
```

### Clean Architecture Layers

```dart
// domain/entities/post.dart
class Post {
  final String id;
  final String title;
  final String content;
  final DateTime createdAt;

  const Post({
    required this.id,
    required this.title,
    required this.content,
    required this.createdAt,
  });
}

// domain/repositories/post_repository.dart
abstract class PostRepository {
  Future<List<Post>> getPosts();
  Future<Post> getPost(String id);
}

// data/repositories/post_repository_impl.dart
class PostRepositoryImpl implements PostRepository {
  final PostRemoteDataSource remote;

  @override
  Future<List<Post>> getPosts() async {
    final posts = await remote.getPosts();
    return posts.map(Post.fromJson).toList();
  }
}
```

### State Management (BLoC)

```dart
import 'package:flutter_bloc/flutter_bloc.dart';

// Events
abstract class PostEvent {}
class LoadPosts extends PostEvent {}

// States
abstract class PostState {}
class PostInitial extends PostState {}
class PostLoading extends PostState {}
class PostLoaded extends PostState {
  final List<Post> posts;
  PostLoaded(this.posts);
}
class PostError extends PostState {
  final String message;
  PostError(this.message);
}

// BLoC
class PostBloc extends Bloc<PostEvent, PostState> {
  final PostRepository repository;

  PostBloc({required this.repository}) : super(PostInitial()) {
    on<LoadPosts>((event, emit) async {
      emit(PostLoading());
      try {
        final posts = await repository.getPosts();
        emit(PostLoaded(posts));
      } catch (e) {
        emit(PostError(e.toString()));
      }
    });
  }
}
```

### Build Commands

| Command | Purpose |
|---------|---------|
| `flutter pub get` | Install dependencies |
| `flutter run` | Run on connected device |
| `flutter build apk --debug` | Debug APK |
| `flutter build apk --release` | Release APK |
| `flutter test` | Run widget tests |
| `flutter analyze` | Static analysis |
| `flutter format .` | Format code |

### Common Pitfalls

```markdown
### Pitfalls to Avoid

1. **BuildContext in async**: Pass required data explicitly
2. **Memory leaks**: Dispose controllers in dispose()
3. **Rebuild storms**: Use `const` constructors, proper keys
4. **Deeply nested widgets**: Extract to separate widgets
```

### Version-Specific Notes

```markdown
**Flutter 3.19+**
- Dart 3.4+ with pattern matching (`switch` expressions)
- Inline class modifiers (final, interface, mixin class)
- Triple shift operator `>>>` for logical right shift

**Flutter 4.0 (when available)**
- Impeller rendering engine becomes default (replaces Skia)
- New `Flutter Vite` template for web
- Improved hot reload for large apps

**Flutter 3.16+**
- Material 3 is now the default theme
- Navigation destinations required for BottomNavigationBar
- `useMaterial3` property for opting out if needed
```

---

# Desktop Frameworks

## Electron

**Detection:** `package.json` with `electron` dependency + main process file

### Detection Commands

```bash
# Verify Electron
cat package.json | grep '"electron"' 2>/dev/null
ls main.js main.ts 2>/dev/null
```

### Detection Patterns

```json
// package.json
{
  "devDependencies": {
    "electron": "^28.0.0"
  }
}
```

### CLAUDE.md Sections

```markdown
## Implementation Standards

### Electron 28+ Patterns

- **Main/Renderer separation**: Never access Node.js in renderer
- **Preload scripts**: Bridge between main and renderer
- **Context isolation**: Always enabled
- **IPC for all communication**: Between main and renderer

### Main Process

```typescript
import { app, BrowserWindow, ipcMain } from 'electron';

let mainWindow: BrowserWindow | null = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });
}

app.whenReady().then(createWindow);

ipcMain.handle('read-file', async (event, filePath) => {
  const fs = await import('fs/promises');
  return fs.readFile(filePath, 'utf-8');
});
```

### Preload Script

```typescript
import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electronAPI', {
  readFile: (filePath: string) => ipcRenderer.invoke('read-file', filePath),
});
```

### Build Commands

| Command | Purpose |
|---------|---------|
| `npm start` | Run in development |
| `npm run build` | Build for production |
| `npm run make` | Create distributable |

### Common Pitfalls

```markdown
### Pitfalls to Avoid

1. **nodeIntegration**: Always use contextIsolation
2. **remote module**: Deprecated, use contextBridge
3. **No IPC**: Always communicate via IPC handlers
```

---

## Tauri

**Detection:** `Cargo.toml` with `tauri` dependency + `src-tauri/`

### Detection Commands

```bash
# Verify Tauri
grep "tauri" Cargo.toml 2>/dev/null
ls src-tauri/tauri.conf.json 2>/dev/null
```

### Detection Patterns

```toml
# Cargo.toml
[dependencies]
tauri = { version = "2.0", features = [] }
```

### CLAUDE.md Sections

```markdown
## Implementation Standards

### Tauri 2.0+ Patterns

- **Rust backend**: Core logic in Rust for performance
- **Web frontend**: Any JS framework
- **IPC via commands**: Rust functions callable from JS
- **Security-first**: Scopes for file system, shell access

### Rust Commands

```rust
use tauri::command;

#[command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

#[command]
async fn read_file(path: &str) -> Result<String, String> {
    tokio::fs::read_to_string(path)
        .await
        .map_err(|e| e.to_string())
}
```
```

### Build Commands

| Command | Purpose |
|---------|---------|
| `cargo tauri dev` | Development |
| `cargo tauri build` | Production build |
| `npm run tauri dev` | Via npm (frontend) |

### Common Pitfalls

```markdown
### Pitfalls to Avoid

1. **Blocking Rust calls**: Always use `async` commands; blocking the main thread freezes the UI
2. **Missing Tauri capabilities**: Declare required capabilities in `tauri.conf.json`
3. **No IPC security**: Never expose Rust functions directly; use scoped commands
4. **Frontend/node_modules bundling**: Don't import Node.js modules in Rust side
```

### Version-Specific Notes

```markdown
**Tauri 2.0+**
- Capabilities system replaces plugin Allowlist
- Multi-window support via `WebviewWindow`
- New mobile support (iOS/Android) as first-class platforms
- Scoped fs/path access via capability permissions

**Rust Commands**
- Use `#[command]` attribute for all IPC functions
- Return `Result<T, String>` for error handling
- Async commands use `async_trait` for proper async/await
```

## ASP.NET Core

**Detection:** `*.csproj` file + `Program.cs`

### Detection Commands

```bash
# Verify .NET
ls *.csproj 2>/dev/null
dotnet --version 2>/dev/null
```

### Detection Patterns

```xml
<!-- *.csproj -->
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
  </PropertyGroup>
</Project>
```

### CLAUDE.md Sections

```markdown
## Implementation Standards

### ASP.NET Core 8.0 Patterns

- **Minimal APIs**: Use minimal API endpoints for simple operations
- **Dependency Injection**: Register services in Program.cs
- **Entity Framework Core**: Use for data access
- **Configuration**: Use IConfiguration and options pattern

### Program.cs Pattern

```csharp
var builder = WebApplication.CreateBuilder(args);

// Add services
builder.Services.AddControllers();
builder.Services.AddDbContext<AppDbContext>();
builder.Services.AddScoped<IPostService, PostService>();

var app = builder.Build();

app.MapControllers();
app.Run();
```

### Dependency Injection Pattern

```csharp
// Register service
builder.Services.AddScoped<IPostService, PostService>();

// Use service in controller
[ApiController]
[Route("api/[controller]")]
public class PostsController : ControllerBase
{
    private readonly IPostService _postService;

    public PostsController(IPostService postService)
    {
        _postService = postService;
    }
}
```

### Build Commands

| Command | Purpose |
|---------|---------|
| `dotnet build` | Build project |
| `dotnet run` | Run development |
| `dotnet test` | Run tests |
| `dotnet ef migrations add` | Create migration |
| `dotnet ef database update` | Apply migrations |
| `dotnet format` | Format code |

### Common Pitfalls

```markdown
### Pitfalls to Avoid

1. **Blocking async**: Don't use .Result or .Wait() on async methods
2. **Singleton DbContext**: Use scoped DbContext in web apps
3. **Missing DI**: Don't instantiate services manually
```

### Version-Specific Notes

```markdown
**ASP.NET Core 8.0**
- Minimal APIs are now feature-complete (previously preview)
- Rate limiting middleware is built-in (no third-party needed)
- Output caching for MVC and Minimal APIs
- Native AOT (ahead-of-time) compilation support

**ASP.NET Core 7.0**
- Minimal APIs with endpoint filters
- SignalR with automatic JavaScript client
- OpenAPI improvements with NSwag
```

---

# Backend Frameworks

## Go

**Detection:** `go.mod` + `.go` files

### Detection Commands

```bash
# Verify Go
cat go.mod 2>/dev/null | head -5
go version 2>/dev/null
```

### Detection Patterns

```go
// go.mod
module github.com/user/project

go 1.22

require (
    github.com/gin-gonic/gin v1.9.1
)
```

### CLAUDE.md Sections

```markdown
## Implementation Standards

### Go 1.22+ Conventions

- **Error handling**: Explicit, never ignore errors
- **Context propagation**: Always pass context.Context
- **Project structure**: Standard Go layout or simplified
- **Go modules**: Use `go.mod` for dependencies
- **Generics**: Use where appropriate

### Project Structure

```
cmd/
  server/
    main.go
internal/
  handler/      # HTTP handlers
  service/      # Business logic
  repository/   # Data access
  model/        # Domain models
  middleware/   # HTTP middleware
```

### Error Handling

```go
// Error wrapping
if err != nil {
    return fmt.Errorf("failed to get user: %w", err)
}

// Custom errors
type NotFoundError struct {
    Resource string
    ID       string
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s not found: %s", e.Resource, e.ID)
}
```

### Context Usage

```go
func (s *Service) GetUser(ctx context.Context, id string) (*User, error) {
    user, err := s.repo.FindByID(ctx, id)
    if err != nil {
        return nil, fmt.Errorf("get user: %w", err)
    }
    return user, nil
}
```

### Build Commands

| Command | Purpose |
|---------|---------|
| `go run cmd/server/main.go` | Run development |
| `go build ./...` | Build all packages |
| `go test ./...` | Run all tests |
| `go test -race ./...` | Race detector |
| `go test -cover ./...` | Coverage report |
| `go mod tidy` | Clean up dependencies |
| `go vet ./...` | Static analysis |
| `golangci-lint run` | Run linter |

### Common Pitfalls

```markdown
### Pitfalls to Avoid

1. **Ignoring errors**: Always handle or explicitly ignore with `_`
2. **No context**: Always pass context.Context
3. **Goroutine leaks**: Use errgroup for concurrent operations
4. **Global state**: Avoid package-level variables
```

---

## Rust

**Detection:** `Cargo.toml` + `.rs` files

### Detection Commands

```bash
# Verify Rust
cat Cargo.toml 2>/dev/null | head -10
rustc --version 2>/dev/null
```

### Detection Patterns

```toml
# Cargo.toml
[package]
name = "my-app"
version = "0.1.0"
edition = "2021"

[dependencies]
axum = "0.7"
sqlx = { version = "0.7", features = ["runtime-tokio", "postgres"] }
```

### CLAUDE.md Sections

```markdown
## Implementation Standards

### Rust 1.77+ Conventions

- **Ownership**: Every value has one owner
- **Borrowing**: Mutable OR immutable, never both
- **Lifetimes**: Explicit when needed
- **Error handling**: Result<T, E> for fallible operations
- **No panics**: Use Result for expected failures

### Project Structure

```
src/
  main.rs          # Entry point
  lib.rs           # Library root
  routes/          # HTTP handlers
  services/        # Business logic
  repositories/    # Data access
  models/          # Data structures
```

### Error Handling

```rust
#[derive(Debug)]
pub enum AppError {
    NotFound(String),
    ValidationError(String),
    DatabaseError(sqlx::Error),
    InternalError(String),
}

impl std::fmt::Display for AppError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            AppError::NotFound(id) => write!(f, "Not found: {}", id),
            _ => write!(f, "Internal error"),
        }
    }
}

impl std::error::Error for AppError {}
```

### Build Commands

| Command | Purpose |
|---------|---------|
| `cargo build` | Build project |
| `cargo build --release` | Release build |
| `cargo run` | Run development |
| `cargo test` | Run tests |
| `cargo clippy` | Lint with suggestions |
| `cargo fmt` | Format code |
| `cargo check` | Check without building |
| `cargo audit` | Security audit |

### Common Pitfalls

```markdown
### Pitfalls to Avoid

1. **Mutable borrows**: Don't mutably borrow the same value multiple times
2. **Lifetimes**: Don't fight the borrow checker; let it infer when possible
3. **Panics in library**: Use Result for expected failures
```

### Version-Specific Notes

```markdown
**Rust 1.77+**
- `async fn` in traits now stable (previously required `async-trait` crate)
- `#[deprecated]` attribute improvements
- Improved error messages for borrow checker

**Rust 1.75+**
- `Ryu` built-in (no external dependency for JSON)
- `cargo remove` for removing dependencies
- `async fn` in traits preview

**Rust 1.70+**
- `cargo help` for built-in help
- `SCCACHE` for faster builds
- Default to `proc-macro2` v1.4.4+ for consistency
```

---

## Phoenix (Elixir)

**Detection:** `mix.exs` + `lib/` directory

### Detection Commands

```bash
# Verify Phoenix
cat mix.exs 2>/dev/null | head -10
ls lib/ 2>/dev/null
```

### Detection Patterns

```elixir
# mix.exs
defmodule MyApp.MixProject do
  use Mix.Project

  def project do
    [
      app: :my_app,
      version: "0.1.0",
      elixir: "~> 1.16",
      deps: deps()
    ]
  end
end
```

### CLAUDE.md Sections

```markdown
## Implementation Standards

### Phoenix 1.7+ Conventions

- **Context modules**: Business logic in contexts
- **Components**: Use function components (recommended over views)
- **LiveView**: For real-time features
- **Ecto**: For data access with changesets

### Directory Structure

```
lib/
  my_app/
    application.ex      # Application behaviour
    repo.ex             # Ecto.Repo
  my_app_web/
    components/         # Phoenix components
    controllers/        # HTTP controllers
    live/               # LiveView modules
    router.ex           # Routes
  my_app/*              # Business logic contexts
```

### Context Pattern

```elixir
# lib/my_app/blog.ex
defmodule MyApp.Blog do
  import Ecto.Query
  alias MyApp.Repo
  alias MyApp.Blog.Post

  def list_posts do
    Repo.all(Post)
  end

  def get_post!(id) do
    Repo.get!(Post, id)
  end

  def create_post(attrs) do
    %Post{}
    |> Post.changeset(attrs)
    |> Repo.insert()
  end
end
```

### Ecto Changeset

```elixir
# lib/my_app/blog/post.ex
defmodule MyApp.Blog.Post do
  use Ecto.Schema
  import Ecto.Changeset

  schema "posts" do
    field :title, :string
    field :body, :string
    timestamps()
  end

  def changeset(post, attrs) do
    post
    |> cast(attrs, [:title, :body])
    |> validate_required([:title, :body])
    |> validate_length(:title, max: 255)
  end
end
```

### Build Commands

| Command | Purpose |
|---------|---------|
| `mix phx.server` | Start development server |
| `mix phx.gen.context` | Generate context |
| `mix ecto.create` | Create database |
| `mix ecto.migrate` | Run migrations |
| `mix ecto.reset` | Reset database |
| `mix test` | Run tests |
| `mix format` | Format code |
| `mix credo` | Run Credo linter |

### Common Pitfalls

```markdown
### Pitfalls to Avoid

1. **Logic in controllers**: Always use contexts for business logic
2. **N+1 queries**: Use preload for associations
3. **Missing changesets**: Always validate with changesets
4. **Blocking operations**: Use async tasks for long operations
```

---

# Utility Scripts

## Framework Detection Script

```bash
#!/bin/bash
# detect_framework.sh - Detect framework from project files

echo "Detecting framework..."

# Check for each framework
detect_framework() {
    local fw=$1
    local files=$2

    for file in $files; do
        if [ -f "$file" ]; then
            echo "$fw"
            return 0
        fi
    done
    return 1
}

# Web Frameworks
if [ -f "next.config.js" ] || [ -f "next.config.ts" ]; then
    echo "Next.js"
elif [ -f "nuxt.config.ts" ]; then
    echo "Nuxt.js"
elif [ -f "vite.config.js" ] || [ -f "vite.config.ts" ]; then
    echo "Vite + React"
elif [ -f "svelte.config.js" ]; then
    echo "SvelteKit"
elif [ -f "astro.config.mjs" ]; then
    echo "Astro"
elif [ -f "artisan" ]; then
    echo "Laravel"
elif [ -f "config.ru" ]; then
    echo "Rails"
elif [ -f "manage.py" ]; then
    echo "Django"
elif [ -f "pyproject.toml" ] && grep -q fastapi pyproject.toml 2>/dev/null; then
    echo "FastAPI"
elif [ -f "Gemfile" ] && grep -q sinatra Gemfile 2>/dev/null; then
    echo "Sinatra"

# Mobile
elif [ -f "App.tsx" ] && [ -f "app.json" ]; then
    echo "React Native"
elif [ -f "pubspec.yaml" ]; then
    echo "Flutter"

# Desktop
elif [ -f "package.json" ] && grep -q '"electron"' package.json 2>/dev/null; then
    echo "Electron"
elif [ -f "src-tauri/tauri.conf.json" ]; then
    echo "Tauri"
elif [ -f "*.csproj" ]; then
    echo "ASP.NET Core"

# Backend
elif [ -f "go.mod" ]; then
    echo "Go"
elif [ -f "mix.exs" ]; then
    echo "Phoenix"
elif [ -f "Cargo.toml" ] && ! [ -f "src-tauri/tauri.conf.json" ]; then
    echo "Rust"

else
    echo "Unknown framework"
    exit 1
fi
```

## CLAUDE.md Section Validator

```python
#!/usr/bin/env python3
# validate_claude_md.py

import sys
import re

REQUIRED_SECTIONS = [
    "Core Identity",
    "Foundational Principles",
    "Implementation Standards",
    "Development Workflow",
    "Testing Strategy",
    "Code Quality",
    "Git & Version Control",
    "Error Handling",
]

FRAMEWORK_REQUIREMENTS = {
    "laravel": ["Form Request", "Policy", "Service"],
    "rails": ["Service", "Concerns"],
    "nextjs": ["App Router", "Server Components"],
    "react-native": ["Navigation", "Platform"],
    "django": ["Models", "Views", "Services"],
}

def validate(file_path: str) -> tuple[int, list[str]]:
    with open(file_path) as f:
        content = f.read()

    errors = []

    # Check required sections
    for section in REQUIRED_SECTIONS:
        pattern = rf"##\s+{section}"
        if not re.search(pattern, content, re.IGNORECASE):
            errors.append(f"Missing section: {section}")

    # Check framework-specific sections
    for framework, patterns in FRAMEWORK_REQUIREMENTS.items():
        if framework.lower() in content.lower():
            for pattern in patterns:
                if not re.search(rf".*{pattern}.*", content, re.IGNORECASE | re.DOTALL):
                    errors.append(f"Framework '{framework}' missing: {pattern}")

    # Check for duplicate section names
    h2_sections = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
    seen = {}
    for section in h2_sections:
        if section in seen:
            errors.append(f"Duplicate section name: {section}")
        seen[section] = True

    return len(errors), errors

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "CLAUDE.md"
    errors, messages = validate(path)

    if errors == 0:
        print(f"✅ CLAUDE.md is valid")
    else:
        print(f"❌ CLAUDE.md has {errors} issues:")
        for msg in messages:
            print(f"  - {msg}")

    sys.exit(errors)
```

---

## Troubleshooting

### Framework Not Detected

**Problem**: Unable to determine framework from file analysis.

**Solution**: Run targeted detection commands:

```bash
# For JavaScript/TypeScript projects
cat package.json | jq '.dependencies | keys' 2>/dev/null

# For PHP projects
grep -r "<?php" --include="*.php" . 2>/dev/null | head -1

# For Python projects
cat requirements.txt 2>/dev/null | head -20

# For Ruby projects
cat Gemfile 2>/dev/null | grep -E "gem |rails|sinatra"

# For Go projects
cat go.mod 2>/dev/null | head -10

# For Rust projects
cat Cargo.toml 2>/dev/null | head -20
```

### Generated Sections Are Too Generic

**Problem**: CLAUDE.md sections contain obvious, template-level content.

**Solution**: Run deeper analysis:

```bash
# Find unique patterns in the codebase
grep -r "use Illuminate" --include="*.php" . | head -20
grep -r "from '" --include="*.js" --include="*.ts" . | grep -v node_modules | head -20

# Examine actual project structure
tree -L 3 -d .
find . -name "*.blade.php" -o -name "*.tsx" -o -name "*.vue" | head -30

# Check for custom configuration
find . -maxdepth 2 -name "*.config.*" | head -10
```

### Commands Don't Match Project

**Problem**: Documented commands don't exist in `package.json` or `composer.json`.

**Solution**: Verify commands exist:

```bash
# Verify npm scripts
cat package.json | jq '.scripts' 2>/dev/null

# Verify composer scripts
cat composer.json | jq '.scripts' 2>/dev/null

# Verify Makefile targets
grep "^[a-z-]*:" Makefile 2>/dev/null | head -20

# If commands are missing, either:
# 1. Document the command that should exist (recommendation)
# 2. Add the command to package.json/composer.json
# 3. Document it as a TODO in CLAUDE.md
```

### Missing Framework-Specific Sections

**Problem**: Important framework-specific sections are absent.

**Solution**: Check for framework-specific patterns:

```bash
# Laravel: Check for Form Request classes
find . -name "*Request.php" -path "*/Http/Requests/*" 2>/dev/null

# Laravel: Check for Policy classes
find . -name "*Policy.php" -path "*/Policies/*" 2>/dev/null

# Rails: Check for Service Objects
find . -path "*/app/services/*" -name "*.rb" 2>/dev/null

# Rails: Check for Concerns
find . -path "*/app/concerns/*" -name "*.rb" 2>/dev/null

# Next.js: Check for App Router structure
ls app/api/ app/providers/ app/actions/ 2>/dev/null

# React Native: Check for navigation setup
ls src/navigation/ App.tsx 2>/dev/null

# Flutter: Check for Clean Architecture
ls lib/domain/ lib/data/ lib/presentation/ 2>/dev/null
```

### Version-Specific Issues

**Problem**: CLAUDE.md mentions patterns that don't work with installed version.

**Solution**: Check installed version and adjust guidance:

```bash
# Node.js packages
cat package.json | jq '.dependencies'

# PHP Laravel
php artisan --version

# Python Django
python -c "import django; print(django.VERSION)"

# Ruby Rails
bundle exec rails --version

# Go
go version

# Rust
rustc --version
```

### CLAUDE.md Validation Failures

**Problem**: `validate_claude_md.py` reports errors.

**Common fixes**:

1. **Missing required section**: Add the missing H2 section
2. **Missing framework pattern**: Add the expected pattern for that framework
3. **Duplicate section name**: Rename one of the duplicate H2s

```bash
# Run validation
python3 validate_claude_md.py CLAUDE.md

# Check for duplicate H2s
grep "^## " CLAUDE.md | sort | uniq -d
```

---

## Changelog

### 2.0.0 (2026-04-13)

**Breaking Changes - Structure Rework:**

- ✅ Fixed H2 hierarchy: Each framework H2 now contains ALL its content
- ✅ Removed duplicate "Implementation Standards" H2s - each framework has unique H2
- ✅ Added subservice process steps (get, list, detect, validate)
- ✅ Added 5 missing frameworks: SvelteKit, Astro, Phoenix, ASP.NET Core, Express/Fastify
- ✅ Fixed Framework Index links (now match actual H2 headings)
- ✅ Added Common Pitfalls to all frameworks
- ✅ Added Version-Specific Notes to all frameworks
- ✅ Added Environment Variables section to Laravel
- ✅ Improved detection commands with more comprehensive checks
- ✅ Enhanced validation script with framework-specific checks
- ✅ Expanded detection script with all 18 frameworks

### 1.0.0 (2026-04-12)

- Initial release
- 13 framework templates
- Basic detection patterns
- Build commands tables