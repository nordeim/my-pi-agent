## Recommended outcome

The existing `astro-5` skill should be rewritten as a current-stable Astro skill, preferably named `astro-7` or `astro-current`, while preserving the proprietary license. The old Astro 5 material should survive only as a migration/legacy appendix.

Rationale: the public Astro homepage currently says “Astro 7.1 Available now!” [[74]]. Astro 7.0 is described as bringing “faster builds with Vite 8, a new Rust compiler, Advanced Routing, background dev server support, and structured logging” [[73]]. The current docs also state that “The current minimum supported version is v22.12.0” for Node.js [[99]]. A skill that still targets Astro 5, Node 20, Vite 6, Astro Studio, and `@astrojs/db` is now materially outdated for most production use cases.

---

## 1. Strategic positioning for the improved skill

### Primary target

Rewrite the skill for:

- Current stable Astro 7.x.
- Node.js 22.12.0+ [[99]].
- Vite 8 and the Rust-based Astro compiler [[73]].
- Content Layer API, including build-time and live collections [[261]] [[111]].
- Server Islands, Actions, Sessions, route caching, and advanced routing [[66]] [[125]] [[138]] [[118]] [[78]].

### Secondary target

Include a compact version-aware section for:

- Astro 6 projects that need upgrade guidance.
- Astro 5 projects still in the wild.
- Migration from removed APIs and deprecated patterns.

The skill should not treat Astro 5 as the default target unless the user explicitly says they are maintaining an Astro 5 codebase.

---

## 2. Evidence-based audit of the current SKILL.md

The current file is conceptually strong but contains several high-impact outdated claims.

### 2.1 Version and runtime target

Current skill says:

- Target: Astro 5.0+.
- Node.js 20+.
- Vite 6.

Current evidence:

- Astro 7.1 is available now [[74]].
- Astro 7.0 introduces Vite 8, a Rust compiler, Advanced Routing, background dev server support, and structured logging [[73]].
- Current docs say the minimum supported Node version is v22.12.0 [[99]].

Planned change:

- Replace the target block with Astro 7.x.
- Add a version-support matrix.
- Add explicit upgrade guidance from Astro 5 and Astro 6.

---

### 2.2 Astro Studio and Astro DB

Current skill presents Astro Studio + Astro DB as Astro’s managed backend.

Current evidence:

- Astro Studio was wound down and existing databases were scheduled for deletion after March 1, 2025 [[23]].
- The Astro v7 upgrade guide states that `@astrojs/db` has been removed and is no longer maintained [[54]].

Planned change:

- Remove Astro Studio as a recommended backend.
- Remove `@astrojs/db` from the main skill body.
- Add a migration note pointing to alternatives such as Drizzle, Turso/libSQL, Node.js SQLite, or another database layer.
- Keep a short historical note only in a legacy/migration appendix.

---

### 2.3 Content collections

Current skill covers the Content Layer API, but not deeply enough for current Astro.

Current evidence:

- Build-time collections are defined in `src/content.config.ts` [[261]].
- Live collections use a different API from build-time collections [[111]].
- A legacy content config file should be moved to `src/content.config.ts` [[268]].
- Astro v6 removed automatic legacy content collections support [[51]].
- Zod should be imported from `astro/zod` [[276]].
- Astro v6 upgraded to Zod 4 and deprecated `astro:schema` and `z` from `astro:content` [[284]].

Planned change:

Expand the content collections section into a full content-system section covering:

- Build-time collections.
- Live collections.
- `glob()` and `file()` loaders.
- Custom loaders.
- Zod 4 schema patterns.
- Collection references.
- Entry IDs versus legacy slugs.
- Route generation from collections.
- Caching behavior for live collections.
- Draft handling.
- CMS integration patterns.

---

### 2.4 Rendering modes and `output: "hybrid"`

Current skill mentions hybrid mode as if `output: "hybrid"` is still a normal option.

Current evidence:

- The Astro v5 upgrade guide says projects must remove `output: "hybrid"` because it no longer exists [[230]].

Planned change:

- Remove `output: "hybrid"` as a recommended config.
- Explain the current model:
  - `output: "static"` as the default.
  - Per-page `export const prerender = false` for on-demand pages.
  - `output: "server"` for fully on-demand SSR.
- Add adapter guidance for Node, Vercel, Netlify, Cloudflare, and Deno.

---

### 2.5 Server Islands

Current skill includes Server Islands but misses operational details.

Current evidence:

- Server Islands use `server:defer`.
- Fallback content uses `slot="fallback"`.
- Props must be serializable.
- Rolling deployments, multi-region hosting, or CDN caching may require a reusable encryption key via `ASTRO_KEY` [[66]].

Planned change:

Expand Server Islands into a production-ready section covering:

- When to use Server Islands.
- Fallback design.
- Serializable prop constraints.
- Caching behavior.
- `GET` versus `POST` island requests.
- `ASTRO_KEY` for rolling deployments.
- Interaction with adapters and SSR.
- Accessibility and loading-state patterns.

---

### 2.6 View Transitions and client routing

Current skill correctly mentions `<ClientRouter />`, but the ecosystem has moved.

Current evidence:

- Astro’s view transitions docs describe `<ClientRouter />` and native cross-document transitions [[30]].
- The old `<ViewTransitions />` component was removed in Astro v6 [[51]].
- There is growing emphasis on native browser view transitions and reducing dependence on client-side routing [[31]].

Planned change:

Update the View Transitions section to cover:

- `<ClientRouter />` usage.
- Native MPA view transitions.
- When to avoid client-side routing entirely.
- `transition:name`, `transition:persist`, and `transition:animate`.
- Script lifecycle events such as `astro:page-load`.
- Accessibility, including reduced motion.
- Migration from removed `<ViewTransitions />`.

---

### 2.7 Routing, middleware, endpoints, and advanced routing

Current skill covers file-based routing, middleware, and API endpoints, but not Astro 7 advanced routing.

Current evidence:

- Astro’s routing guide covers file-based routing and advanced routing added in Astro 7 [[59]].
- Astro v7 reserves `src/fetch.ts` for advanced routing and allows changing or disabling it with `fetchFile` [[78]].
- The `astro/fetch` module provides `FetchState`, `astro()`, `actions()`, `middleware()`, `pages()`, `i18n()`, and other handlers [[88]].
- Middleware allows request/response interception and `locals` injection [[191]].

Planned change:

Add a routing-and-server section covering:

- Static file-based routing.
- Dynamic routes and `getStaticPaths()`.
- Rest routes.
- Redirects and rewrites.
- Route priority.
- Middleware.
- API endpoints.
- Actions.
- Sessions.
- Advanced routing with `src/fetch.ts`.
- Hono-compatible routing patterns.
- Reserved file names and migration hazards.

---

### 2.8 Actions, Sessions, environment variables, i18n, images, and security

Current skill lacks several now-core Astro capabilities.

Current evidence:

- Astro Actions allow type-safe backend functions [[125]].
- Actions are exported from `src/actions/index.ts` [[149]].
- Sessions are used to share server-side data across requests [[138]].
- `astro:env` provides type-safe environment variable schemas [[169]].
- Astro has built-in i18n routing [[177]].
- Astro has built-in image optimization via `<Image />` and related APIs [[184]].
- Astro added built-in CSP support in Astro 6 via a security configuration option [[202]].

Planned change:

Add new sections or subsections for:

- Actions.
- Sessions.
- Typed environment variables.
- i18n routing.
- Image optimization.
- Security hardening, including CSP, input validation, secret handling, and unsafe HTML injection.

---

### 2.9 Styling and Tailwind

Current skill mentions `@astrojs/tailwind`, but Tailwind 4 changes the recommended setup.

Current evidence:

- Tailwind CSS now offers a Vite plugin, which is the preferred way to use Tailwind 4 in Astro [[133]].
- Astro 5.2 introduced an updated `astro add tailwind` path for Tailwind 4 [[136]].
- Astro `<style>` CSS rules are automatically scoped by default [[291]].

Planned change:

Rewrite the styling section to cover:

- Scoped styles.
- Global styles.
- `class:list`.
- CSS variables.
- Tailwind 4 using the Vite plugin.
- Migration from `@astrojs/tailwind` and Tailwind 3.
- Sass, Less, Stylus, PostCSS, and LightningCSS where relevant.

---

### 2.10 Performance, caching, and build behavior

Current skill emphasizes zero JS by default, which remains valid, but misses current performance features.

Current evidence:

- Astro 7 focuses heavily on build speed, with Vite 8, Rust compiler, Rust Markdown processing, and queued rendering [[73]].
- Route caching requires a cache provider and supports runtime caching semantics [[118]].
- Route caching is now stable after being introduced experimentally [[122]].

Planned change:

Add a performance-and-caching section covering:

- Zero-JS-by-default mental model.
- Island hydration budgeting.
- Route caching.
- CDN cache providers.
- Cache tags and invalidation.
- Live collection cache hints.
- Build performance implications of Rust compiler and Sätteri Markdown.
- Core Web Vitals guidance.

---

### 2.11 Compiler and Markdown behavior changes

Current skill does not mention Astro 7’s stricter compiler or new Markdown pipeline.

Current evidence:

- The Astro v7 upgrade guide warns that the Rust compiler is stricter about invalid HTML syntax and no longer auto-corrects markup [[78]].
- The default whitespace handling changed to JSX-style rules in Astro 7 [[78]].
- The default Markdown processor changed to Sätteri, with `@astrojs/markdown-remark` available for unified compatibility [[78]].

Planned change:

Add migration-critical notes and anti-patterns for:

- Unclosed tags.
- Invalid nesting.
- JSX whitespace changes.
- Remark/rehype plugin compatibility.
- Sätteri versus unified Markdown pipeline.
- Debugging template output changes after upgrade.

---

### 2.12 Testing and DX

Current skill mentions `astro check`, but not a full testing story.

Current evidence:

- Astro supports many testing tools, including Jest, Mocha, Jasmine, Cypress, and Playwright [[206]].
- `astro check` checks files included in the TypeScript project [[223]].
- Astro 7 adds background dev server support and structured JSON logging [[73]].

Planned change:

Add a testing-and-DX section covering:

- `astro check`.
- TypeScript diagnostics.
- Unit testing Astro components.
- Integration testing.
- End-to-end testing with Playwright or Cypress.
- Background dev server usage.
- JSON logs for agent-driven development and production observability.

---

## 3. Research plan

The research phase should be organized by workstream. Each workstream should produce source notes, verified code snippets, and a list of skill sections to update.

### Workstream A: Version and support matrix

Questions:

1. What is the current stable Astro version?
2. What Node versions are supported?
3. What Vite version is used?
4. What upgrade paths exist from Astro 5 and Astro 6?
5. Which features are stable, experimental, deprecated, or removed?

Primary sources:

- Astro homepage and release announcements [[74]] [[73]].
- Astro upgrade guides [[78]] [[51]].
- Node version documentation [[99]].
- GitHub releases and changelogs [[54]].

Verification:

- Run `npm view astro version` in a clean environment.
- Create a fresh Astro project.
- Confirm Node version requirement.
- Confirm `astro --version`.
- Record package versions for official integrations.

Deliverable:

A version matrix in the skill:

- Astro 7.x: current recommended target.
- Astro 6.x: supported migration source.
- Astro 5.x: legacy, migration-only.
- Astro 4.x and below: out of scope except migration.

---

### Workstream B: Core component model and islands

Questions:

1. What are the current hydration directives?
2. What has changed in framework integration packages?
3. What are current best practices for zero-JS Astro components?
4. What are the current multi-framework integration patterns?
5. What deprecations affect React, Vue, Svelte, Preact, Solid, or Lit integrations?

Primary sources:

- Islands architecture docs [[254]].
- Framework component docs [[250]].
- Directive reference [[245]].
- Client directive documentation [[259]].
- Astro v7 upgrade guide for integration/container-renderer deprecations [[78]].

Verification:

- Create a test project with React, Vue, and Svelte components.
- Verify each `client:` directive.
- Verify `client:only` behavior.
- Verify framework component SSR behavior.
- Verify that non-interactive components remain JS-free.

Deliverable:

Updated islands section with current directive table, anti-patterns, and framework-specific notes.

---

### Workstream C: Content Layer, collections, and CMS patterns

Questions:

1. How do build-time collections work now?
2. How do live collections differ?
3. What loaders are built in?
4. How should schemas be written with Zod 4?
5. How should references, drafts, IDs, and route generation be handled?
6. How should external CMS data be loaded?
7. How do caching and revalidation interact with live collections?

Primary sources:

- Content collections guide [[261]].
- Live collections documentation [[111]].
- Legacy content config error reference [[268]].
- Astro v6 upgrade guide for removal of legacy collections [[51]].
- Zod import guidance [[276]].
- Zod 4 migration notes [[284]].
- Content loader reference [[263]].

Verification:

- Build a collection using Markdown.
- Build a collection using JSON/YAML.
- Build a collection using a custom loader.
- Create a live collection if adapter support is available.
- Validate schema failure behavior.
- Generate dynamic routes from collection entries.
- Confirm type generation with `astro sync` or dev/build.

Deliverable:

A complete content-system section with examples for:

- Blog posts.
- Authors.
- Products.
- External API content.
- CMS-driven content.
- Draft filtering.
- References.
- Route generation.

---

### Workstream D: Rendering, deployment, caching, and adapters

Questions:

1. What are the current rendering modes?
2. How should per-page SSR be configured?
3. What adapters are current and stable?
4. How does route caching work?
5. How do CDN cache providers work?
6. What deployment pitfalls exist for Server Islands and route caching?

Primary sources:

- Routing guide [[59]].
- Route caching guide [[118]].
- Route caching stabilization notes [[122]].
- Astro 7 release notes [[73]].
- Astro v5 upgrade guide for removal of `output: "hybrid"` [[230]].
- Server Islands docs [[66]].

Verification:

- Build a static site.
- Build an SSR site with a Node adapter.
- Use `prerender = false` on selected pages.
- Test Server Islands with fallback content.
- Test route caching with a memory cache provider.
- Verify cache invalidation patterns where possible.

Deliverable:

A rendering-and-deployment section covering static, SSR, hybrid behavior without `output: "hybrid"`, adapters, Server Islands, and route caching.

---

### Workstream E: Server APIs: middleware, endpoints, Actions, Sessions, advanced routing

Questions:

1. How should middleware be used in current Astro?
2. How should API endpoints be structured?
3. How do Actions compare to endpoints?
4. How should Sessions be used?
5. How does advanced routing change request handling?
6. When should `src/fetch.ts` be used or avoided?

Primary sources:

- Middleware guide [[191]].
- Actions guide [[125]].
- Actions API reference [[149]].
- Sessions guide [[138]].
- Advanced routing guide [[59]].
- Astro v7 upgrade guide for `src/fetch.ts` reservation [[78]].
- `astro/fetch` API reference [[88]].

Verification:

- Create middleware that sets `locals`.
- Create an API endpoint.
- Create an Action with input validation.
- Create a Session-backed example.
- Create an advanced routing entrypoint.
- Verify request order for middleware, Actions, and pages.

Deliverable:

A server-side API section that clearly distinguishes:

- Middleware.
- Endpoints.
- Actions.
- Sessions.
- Advanced routing.
- Authentication and authorization patterns.

---

### Workstream F: Styling, UI, images, i18n, environment, and security

Questions:

1. What are current styling best practices?
2. How should Tailwind 4 be configured?
3. How should images be optimized?
4. How should i18n routing be configured?
5. How should environment variables be typed?
6. What security features should be included in the skill?

Primary sources:

- Styling guide [[291]].
- Tailwind integration guidance [[133]].
- Tailwind 4 upgrade path [[136]].
- Images guide [[184]].
- i18n routing guide [[177]].
- Environment variables guide [[169]].
- CSP support notes [[202]].

Verification:

- Add scoped styles.
- Add global styles.
- Add Tailwind 4 via the Vite plugin.
- Use `<Image />` with local images.
- Configure a basic i18n route.
- Define typed environment variables.
- Review security configuration options.

Deliverable:

A UI-and-platform section covering styling, images, i18n, env, and security.

---

### Workstream G: Testing, DX, observability, and AI-agent workflows

Questions:

1. What should an Astro project’s test pyramid look like?
2. How should `astro check` be used?
3. What testing tools are recommended?
4. How should background dev server and JSON logging be used?
5. What patterns are useful for AI-assisted development?

Primary sources:

- Testing guide [[206]].
- TypeScript/`astro check` guide [[223]].
- Astro 7 background dev server and JSON logging announcement [[73]].

Verification:

- Add a minimal Vitest setup.
- Add a Playwright smoke test.
- Run `astro check`.
- Run `astro dev --background` where available.
- Confirm JSON logging output where available.

Deliverable:

A testing-and-DX section with commands, patterns, and CI recommendations.

---

## 4. Proposed new SKILL.md structure

The rewritten skill should be broader than the old file but still focused on content-first Astro development.

Suggested frontmatter:

```markdown
---
name: astro-7
description: Astro 7.x content-first web framework skill — islands architecture, zero JS by default, Content Layer build-time/live collections, Server Islands, Actions, Sessions, route caching, advanced routing, Vite 8, Rust compiler, Tailwind 4, and deployment to static or SSR hosts. Use for current Astro projects and migration from Astro 5/6.
license: Proprietary. LICENSE.txt has complete terms
---
```

Suggested top-level structure:

1. **Astro 7 — Content-First Web Framework**
2. **When to Use This Skill**
3. **Version Support Matrix**
4. **Quick Start**
5. **Project Structure**
6. **Core Mental Model**
   - Zero JS by default.
   - Islands architecture.
   - Multi-framework components.
   - Server-first rendering.
7. **Content Layer and Collections**
   - Build-time collections.
   - Live collections.
   - Loaders.
   - Zod 4 schemas.
   - References.
   - Route generation.
   - Drafts and filtering.
   - CMS integration patterns.
8. **Astro Components**
   - Frontmatter.
   - Props.
   - Slots.
   - Scoped styles.
   - Scripts.
   - Safe HTML and XSS awareness.
9. **Layouts and Page Composition**
10. **Islands and Hydration Directives**
   - `client:load`
   - `client:idle`
   - `client:visible`
   - `client:media`
   - `client:only`
   - Framework-specific notes.
11. **Server Islands**
   - `server:defer`
   - Fallbacks.
   - Serializable props.
   - Caching.
   - `ASTRO_KEY`.
   - Deployment concerns.
12. **Routing**
   - Static routes.
   - Dynamic routes.
   - Rest routes.
   - Redirects.
   - Rewrites.
   - Route priority.
   - Pagination.
   - i18n routing.
13. **Middleware, Endpoints, Actions, Sessions**
   - `src/middleware.ts`
   - API routes.
   - `src/actions/index.ts`
   - Session storage.
   - Authentication patterns.
   - Authorization patterns.
14. **Advanced Routing**
   - `src/fetch.ts`
   - `fetchFile`
   - `astro/fetch`
   - Hono compatibility.
   - When not to use it.
15. **Rendering Modes and Deployment**
   - Static output.
   - On-demand rendering.
   - Per-page `prerender = false`.
   - SSR adapters.
   - Route caching.
   - CDN cache providers.
   - Netlify, Vercel, Cloudflare, Node, GitHub Pages.
16. **View Transitions and Client Navigation**
   - `<ClientRouter />`
   - Native transitions.
   - Persistent elements.
   - Lifecycle events.
   - Accessibility.
17. **Styling and UI**
   - Scoped CSS.
   - Global CSS.
   - Tailwind 4.
   - CSS variables.
   - Design-system integration.
18. **Images, Assets, and Performance**
19. **Environment Variables and Configuration**
20. **Security Hardening**
   - Input validation.
   - Actions security.
   - Cookies and Sessions.
   - CSP.
   - Secrets.
   - Path traversal and unsafe HTML.
21. **Testing and Verification**
22. **Top Anti-Patterns**
23. **Migration Guide**
   - Astro 5 to Astro 6.
   - Astro 6 to Astro 7.
   - Removed APIs.
   - Deprecated APIs.
   - Database migration from `@astrojs/db`.
24. **Cross-References**
25. **Dependencies and Ecosystem**

---

## 5. High-priority content corrections

These should be treated as blocking updates.

### 5.1 Replace the version target

Old:

```markdown
Target: Astro 5.0+ (released November 2024) on Node.js 20+.
```

New direction:

```markdown
Target: Astro 7.x on Node.js 22.12.0+.
```

Supporting evidence:

- Astro 7.1 is available now [[74]].
- Node minimum is v22.12.0 [[99]].
- Astro 7 uses Vite 8 and the Rust compiler [[73]].

---

### 5.2 Remove or demote Astro Studio and Astro DB

Old section:

```markdown
Astro Studio + Astro DB (Astro's managed backend)
```

New direction:

```markdown
Astro Studio is discontinued, and @astrojs/db has been removed from Astro 7. Use Drizzle, Turso/libSQL, Node.js SQLite, or another database layer.
```

Supporting evidence:

- Astro Studio was wound down [[23]].
- `@astrojs/db` was removed in Astro v7 [[54]].

---

### 5.3 Update content collection configuration location

Old example:

```ts
// src/content.config.ts (Astro 5 — replaces src/content/config.ts)
```

That comment is directionally correct, but the skill should be explicit and include migration guidance.

New guidance:

- Use `src/content.config.ts` for build-time collections [[261]].
- Do not use `src/content/config.ts` except when diagnosing legacy projects [[268]].
- Explain that Astro v6 removed legacy collections [[51]].

---

### 5.4 Update Zod imports

Old example:

```ts
import { defineCollection, z } from 'astro:content';
```

New direction:

```ts
import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
```

Supporting evidence:

- Zod should be imported from `astro/zod` [[276]].
- `astro:schema` and `z` from `astro:content` were deprecated in Astro v6 [[284]].

---

### 5.5 Remove `output: "hybrid"`

Old example:

```js
output: 'hybrid'
```

New direction:

```js
output: 'static'
```

With per-page opt-out:

```astro
export const prerender = false;
```

Supporting evidence:

- `output: "hybrid"` no longer exists and must be removed [[230]].

---

### 5.6 Add `src/fetch.ts` reserved-file warning

New anti-pattern:

- Do not keep an unrelated `src/fetch.ts` file in an Astro 7 project unless it is intended as the advanced routing entrypoint.

Supporting evidence:

- Astro v7 reserves `src/fetch.ts` for advanced routing and provides `fetchFile` to change or disable it [[78]].

---

### 5.7 Add Rust compiler migration warning

New migration note:

- Astro 7’s Rust compiler is stricter about invalid HTML.
- Unclosed tags and invalid nesting may now fail or render differently.
- JSX-style whitespace handling is now the default.

Supporting evidence:

- The Astro v7 upgrade guide documents these breaking changes [[78]].

---

### 5.8 Update Tailwind guidance

Old direction:

```bash
npx astro add tailwind
```

That command may still exist, but the skill should explain the current Tailwind 4 preference.

New direction:

- Use the Tailwind 4 Vite plugin as the preferred path [[133]].
- Use the updated `astro add tailwind` flow where applicable [[136]].
- Explain migration from `@astrojs/tailwind` and Tailwind 3.

---

## 6. Proposed expanded anti-patterns section

The existing top 10 anti-patterns are useful but should be refreshed.

Recommended current anti-patterns:

1. **Shipping JavaScript for static content.**
   - Preserve the existing zero-JS guidance.
   - Reinforce with current islands docs [[254]].

2. **Using `client:load` for every interactive component.**
   - Keep.
   - Update directive list with official directives [[259]].

3. **Using legacy content collections or legacy config files.**
   - Add.
   - Cite `src/content.config.ts` requirement [[261]].
   - Cite legacy config error guidance [[268]].

4. **Importing Zod from the wrong module.**
   - Add.
   - Use `astro/zod` [[276]].

5. **Using `output: "hybrid"` in modern Astro.**
   - Add.
   - It was removed [[230]].

6. **Assuming Astro Studio or `@astrojs/db` is still a managed backend option.**
   - Add.
   - Studio was wound down [[23]].
   - `@astrojs/db` was removed in v7 [[54]].

7. **Keeping an accidental `src/fetch.ts` file in Astro 7.**
   - Add.
   - `src/fetch.ts` is reserved for advanced routing [[78]].

8. **Writing invalid HTML expecting the old compiler to fix it.**
   - Add.
   - The Rust compiler is stricter and no longer auto-corrects markup [[78]].

9. **Using Server Islands without considering serializable props, fallbacks, or deployment keys.**
   - Add.
   - Server Islands have prop serialization limits and may require `ASTRO_KEY` [[66]].

10. **Using Actions or endpoints without input validation and authorization.**
   - Add.
   - Actions provide validation but still need secure authorization patterns [[125]].

11. **Using View Transitions without handling script re-execution and accessibility.**
   - Add.
   - Client routing changes script lifecycle and needs accessible route announcement and reduced-motion support [[30]].

12. **Skipping route caching for expensive on-demand pages.**
   - Add.
   - Route caching provides a platform-agnostic caching API [[118]].

---

## 7. Proposed migration appendix

The improved skill should include a compact migration appendix because many users will arrive from Astro 5 or Astro 6.

### Astro 5 to Astro 6

Cover:

- Removal of legacy content collections [[51]].
- Move to `src/content.config.ts` [[268]].
- Zod 4 changes [[284]].
- Removal of old `<ViewTransitions />` component [[51]].
- Deprecation of `z` from `astro:content` [[284]].

### Astro 6 to Astro 7

Cover:

- Vite 8 upgrade [[73]].
- Rust compiler strictness [[78]].
- Sätteri Markdown default [[78]].
- JSX whitespace default [[78]].
- Advanced routing enabled by default and `src/fetch.ts` reservation [[78]].
- Removal of `@astrojs/db` [[54]].
- Route caching stabilization [[122]].
- Background dev server and JSON logging [[73]].

### Astro Studio / Astro DB migration

Cover:

- Studio sunset [[23]].
- `@astrojs/db` removal [[54]].
- Recommended replacements:
  - Drizzle ORM.
  - Turso/libSQL.
  - Node.js SQLite.
  - Platform-native database services.

---

## 8. Verification plan for the rewritten skill

The rewritten skill should not be accepted unless the examples are verified.

### 8.1 Environment verification

Commands:

```bash
node -v
npm view astro version
npm create astro@latest astro-skill-verification
cd astro-skill-verification
npm install
npx astro version
npm run dev
npm run build
npm run preview
npx astro check
```

Expected checks:

- Node version is 22.12.0 or higher [[99]].
- Installed Astro version is current 7.x [[74]].
- Dev server starts.
- Production build succeeds.
- `astro check` runs.

---

### 8.2 Content collection verification

Create examples for:

- Markdown collection.
- JSON collection.
- YAML collection.
- Custom loader.
- Live collection if adapter-supported.

Verify:

- `src/content.config.ts` is recognized [[261]].
- Zod schema validation fails clearly on invalid data.
- `getCollection()` returns typed entries.
- `getEntry()` works.
- Dynamic routes generate correctly.
- Draft filtering works.
- References resolve.

---

### 8.3 Islands verification

Create components in:

- Astro.
- React.
- Vue.
- Svelte.

Verify:

- No `client:` directive means no hydration JS.
- `client:load` hydrates immediately.
- `client:idle` hydrates when idle.
- `client:visible` hydrates when visible.
- `client:only` skips SSR.
- Multi-framework components coexist.

Supporting guidance:

- Official directives include `client:load`, `client:idle`, `client:visible`, `client:media`, and `client:only` [[259]].

---

### 8.4 Server Islands verification

Create a Server Island example with:

- `server:defer`
- Fallback slot.
- Cookie-based personalization.
- Serializable props.

Verify:

- Initial HTML contains fallback.
- Island endpoint resolves.
- Props are serialized safely.
- Missing or invalid props do not crash the page.
- `ASTRO_KEY` guidance is documented for rolling deployments [[66]].

---

### 8.5 Actions, Sessions, and middleware verification

Create:

- Middleware setting `locals`.
- API endpoint.
- Action with schema validation.
- Session-backed cart or user state.

Verify:

- Middleware runs in expected order [[191]].
- Actions validate input [[125]].
- Actions are exported from the expected actions entrypoint [[149]].
- Sessions persist across requests where supported [[138]].
- Unauthorized access is rejected.

---

### 8.6 Advanced routing verification

Create:

- Default Astro routing project.
- Optional `src/fetch.ts` example.
- Custom `fetchFile` example.
- Hono-compatible example if useful.

Verify:

- Default behavior unchanged without `src/fetch.ts`.
- `src/fetch.ts` is treated as advanced routing entrypoint [[78]].
- `astro/fetch` handlers compose correctly [[88]].
- Existing unrelated `src/fetch.ts` files are renamed or disabled.

---

### 8.7 Styling verification

Create examples for:

- Scoped styles [[291]].
- Global styles.
- Tailwind 4 via Vite plugin [[133]].
- Tailwind migration from Tailwind 3 [[136]].

Verify:

- Scoped styles do not leak.
- Global styles apply as expected.
- Tailwind utilities are generated.
- Build output contains expected CSS chunks.

---

### 8.8 Testing verification

Add minimal tests:

- Type check with `astro check` [[223]].
- Unit or integration test using a supported tool [[206]].
- E2E smoke test with Playwright or Cypress [[206]].

Verify:

- Tests run in CI-like mode.
- Failures are actionable.
- No test depends on brittle implementation details.

---

## 9. Definition of Ready for the rewrite

The rewrite should begin only after the following are confirmed:

1. The target skill name is chosen: `astro-7`, `astro-current`, or retained `astro-5` with a legacy warning.
2. The target Astro version is fixed to current stable 7.x [[74]].
3. The target Node version is fixed to 22.12.0+ [[99]].
4. The license remains proprietary and unchanged.
5. The intended audience is confirmed: general Astro developers, AI coding agents, or both.
6. The skill should remain a single file unless the skill system supports split files.
7. Migration content is confirmed to be in-scope rather than a separate skill.

If no explicit choice is made, use this default:

- Rename to `astro-7`.
- Keep one file.
- Include migration guidance.
- Do not recommend deprecated Astro Studio or `@astrojs/db`.

---

## 10. Definition of Done

The improved skill is complete when:

1. The frontmatter targets Astro 7.x.
2. Node, Vite, and Astro version claims match current official sources [[74]] [[73]] [[99]].
3. All deprecated or removed APIs are either absent from main guidance or explicitly confined to migration sections.
4. Content collections use `src/content.config.ts`, Content Layer patterns, and `astro/zod` where appropriate [[261]] [[276]].
5. Live collections are covered separately from build-time collections [[111]].
6. Server Islands include fallback, serialization, caching, and `ASTRO_KEY` guidance [[66]].
7. Advanced routing includes `src/fetch.ts` reservation and `astro/fetch` composition guidance [[78]] [[88]].
8. Actions, Sessions, middleware, and endpoints are covered with secure patterns [[125]] [[138]] [[191]].
9. Tailwind guidance reflects Tailwind 4 and the Vite plugin path [[133]].
10. View Transitions guidance reflects `<ClientRouter />`, lifecycle events, and accessibility [[30]].
11. Anti-patterns include current Astro 7 pitfalls such as Rust compiler strictness and reserved `src/fetch.ts` [[78]].
12. Migration guidance covers Astro 5 → 6 → 7 and Astro DB/Studio sunset [[51]] [[78]] [[54]] [[23]].
13. Every nontrivial code example has been run in a clean Astro 7 project or explicitly marked as unverified.
14. No placeholder values, dead code, or unverified package claims remain.
15. The skill remains concise enough for agent use while being production-practical.

---

## 11. Suggested implementation sequence

### Phase 1: Research and source pack

Tasks:

- Collect current official docs.
- Collect upgrade guides.
- Collect changelog entries.
- Create a source ledger.
- Identify all removed and deprecated APIs.

Exit criterion:

- Every major topic has at least one current primary source.

### Phase 2: Scratch project verification

Tasks:

- Create a clean Astro 7 project.
- Verify Node version.
- Verify build/dev/check commands.
- Create small examples for each major feature.

Exit criterion:

- All examples compile, build, and behave as documented.

### Phase 3: Draft rewritten SKILL.md

Tasks:

- Rewrite frontmatter.
- Rewrite quick start.
- Rewrite mental model.
- Rewrite content collections.
- Add server-side API sections.
- Add advanced routing.
- Add caching/performance.
- Add security.
- Add testing.
- Add migration appendix.

Exit criterion:

- Full draft exists with no known deprecated main-path guidance.

### Phase 4: Example validation

Tasks:

- Copy every code block into the scratch project where feasible.
- Run `astro check`.
- Run `astro build`.
- Run runtime checks for SSR/Actions/Server Islands where applicable.
- Mark examples as verified or reason-verified.

Exit criterion:

- Verification ledger exists.

### Phase 5: Anti-slop and security review

Tasks:

- Remove filler.
- Remove unsupported claims.
- Remove placeholder values.
- Check secret handling.
- Check XSS and unsafe HTML guidance.
- Check input validation guidance.
- Check dependency recommendations.

Exit criterion:

- The skill is safe, concise, and evidence-backed.

### Phase 6: Final delivery

Tasks:

- Produce final SKILL.md.
- Include verification ledger.
- Include known limitations.
- Include future review date or version policy.

Exit criterion:

- The skill satisfies the Definition of Done.

---

## 12. Pre-mortem: likely failure modes and mitigations

### Failure mode 1: The skill still contains Astro 5-era examples

Mitigation:

- Perform a deprecated-API sweep.
- Search for `output: 'hybrid'`, `src/content/config.ts`, `ViewTransitions`, `@astrojs/db`, `astro:schema`, and `z` from `astro:content`.

### Failure mode 2: The skill becomes too broad and loses usefulness

Mitigation:

- Keep the main skill focused on content-first Astro.
- Move deep adapter, CMS, or database guidance into focused subsections or cross-references.

### Failure mode 3: Examples are docs-accurate but not agent-practical

Mitigation:

- Prefer small, complete, runnable examples.
- Include acceptance criteria for each major pattern.
- Include anti-patterns and debugging notes.

### Failure mode 4: Version drift makes the skill stale quickly

Mitigation:

- Add a version policy section.
- State the verified Astro version.
- Include a “last verified” field if the skill system supports it.
- Prefer stable APIs over experimental ones unless explicitly labeled.

### Failure mode 5: Security guidance is generic and not Astro-specific

Mitigation:

- Cover Actions input validation.
- Cover middleware authorization.
- Cover unsafe HTML injection.
- Cover secrets and environment variables.
- Cover CSP where documented [[202]].

---

## 13. Confidence and verification status

The current-state summary above is based on official Astro documentation, upgrade guides, release notes, and blog sources retrieved during planning.

Confidence:

- Current major version and feature direction: high confidence from official Astro sources [[74]] [[73]].
- Node minimum: high confidence from official docs [[99]].
- Removal of Astro Studio and `@astrojs/db`: high confidence from official announcement and upgrade guide [[23]] [[54]].
- Content Layer and live collections direction: high confidence from official docs [[261]] [[111]].
- Advanced routing and Astro 7 breaking changes: high confidence from official upgrade guide and API reference [[78]] [[88]].
- Exact code examples: not yet locally executed in this planning step; they must be verified in a scratch Astro 7 project before final delivery.

Next practical step: create a clean Astro 7 verification project, run the examples listed in Section 8, and then produce the fully rewritten SKILL.md.
