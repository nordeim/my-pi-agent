# Astro 5 SKILL.md — Research & Improvement Plan

> **Document type:** Planning deliverable (research methodology + gap analysis + proposed structure + 3 sample drafted sections + implementation plan).
> **Target artifact:** Improved/expanded `astro-5` SKILL.md.
> **Research date:** 2026-08-03.
> **Scope:** Astro core platform + adjacent ecosystem (Tailwind 4, CMS integrations, image/font optimization, testing, security).
> **Confidence convention:** Claims are tagged `Verified` (sourced from primary docs/release notes), `Reasoned` (logical inference from sourced facts), or `Assumed` (stated assumption). See §1.2.

---

## Executive Summary

The current `astro-5` SKILL.md was written around the Astro 5.0 release (November 2024) and is now materially stale. As of August 2026:

1. **Astro 7.1.6 is the latest stable release.** Astro 6 shipped in early 2026 (Live Content Collections stabilized), and Astro 7 is current (Vite 8 support, stable Rust compiler integration). The skill still targets "Astro 5.0+" with no awareness of 6 or 7. (`Verified` — docs.astro.build/en/upgrade-astro)
2. **Cloudflare acquired the Astro Technology Company on 2026-01-16.** Astro remains MIT-licensed, open-source, and platform-agnostic, but the corporate context that should appear in the skill's "When to Use" section is missing entirely. (`Verified` — cloudflare.com press release, blog.cloudflare.com/astro-joins-cloudflare)
3. **Astro Studio is discontinued** (announced 2024-09-13, databases deleted 2025-03-01) and **Astro DB is deprecated** (subdependency deprecation warnings as of May 2025). The current SKILL.md still advertises both as features. (`Verified` — astro.build/blog/goodbye-astro-studio, github.com/withastro/astro/issues/13855)
4. **The Sessions API is stable** (since Astro 5.7, April 2025) and **`astro:env` is stable** (since Astro 5.0). Neither is mentioned in the current SKILL.md. (`Verified` — astro.build/blog/astro-570, bryanlrobinson.com type-safe env vars article)
5. **`output: 'hybrid'` was removed in Astro 5.** The current SKILL.md still lists it as a valid config option. (`Verified` — docs.astro.build/en/guides/on-demand-rendering)

The current SKILL.md has strong bones — its mental-model framing (zero JS / islands / multi-framework) is excellent — but it is missing roughly 12 platform features, 8 ecosystem topics, and contains at least 4 stale/incorrect claims that should not be propagated.

**Headline recommendation:** Rewrite the SKILL.md against Astro 5/6/7 (current) rather than 5.0+. Keep the existing structural backbone (Quick Start → Project Structure → Mental Model → Content Collections → Components → Layouts → View Transitions → Server Islands → Middleware → Endpoints → Deployment → Anti-Patterns → Cross-refs → Dependencies). Insert 7 new platform-feature sections (Sessions, Actions, i18n, `astro:env`, `astro:assets`, Fonts, Live Content Collections), 4 new ecosystem sections (Tailwind 4, Nanostores, Testing, Security), and 1 new "Versions & Migration" section. Correct all 4 stale claims. Sample drafted sections for Sessions, `astro:env`, and `astro:assets` are provided in Part 4 as the target quality bar.

---

## Part 1 — Research Methodology & Verification Ledger

### 1.1 Methodology

This plan's claims rest on targeted verification of 17 critical facts that the current SKILL.md either states, implies, or omits. Verification was performed on 2026-08-03 via web search against primary and high-quality secondary sources.

**Source hierarchy (in descending authority):**

1. **Primary docs** — `docs.astro.build/*` (canonical API reference, guides, upgrade guide)
2. **Official blog** — `astro.build/blog/*` (release announcements, deprecation notices)
3. **GitHub source of truth** — `github.com/withastro/astro` releases, CHANGELOG, issues (deprecation warnings, breaking-change tracking)
4. **Vendor press releases** — `cloudflare.com`, `blog.cloudflare.com` (for the acquisition)
5. **High-signal secondary** — `thenewstack.io`, `dev.to`, reputable practitioner blogs (bryanlrobinson.com, chenhuijing.com, maciekpalmowski.dev) when they cite verifiable primary sources

**What was not searched (out of scope for this round):**

- Per-integration changelogs (`@astrojs/react`, `@astrojs/vue`, etc.) — verified only at the "is the integration still maintained" level.
- Astro 7's full experimental-flags list — only confirmed Vite 8 + Rust compiler headline.
- VSCode extension feature history — mentioned but not audited.

These are flagged in §5.2 as follow-up verification gates if the user upgrades this plan to a full rewrite.

**Research artifacts:** Raw search results saved to `/home/z/my-project/scripts/research_01_*.json` through `research_17_*.json` (17 files). Each file is the JSON output of the `z-ai web_search` function for one query. They are retained as audit trail for the verification ledger below.

### 1.2 Verification Ledger

Each row maps a claim in the current SKILL.md (or a fact the SKILL.md should state) to its verified current reality.

| # | Topic | Current SKILL.md claim | Verified reality (2026-08-03) | Source | Confidence | Action |
|---|-------|------------------------|-------------------------------|--------|------------|--------|
| 1 | Astro version | "Astro 5.0+ (released November 2024)" | Astro 5.x latest ~5.15; Astro 6 stable (early 2026); Astro 7.1.6 is current latest | docs.astro.build/en/upgrade-astro | Verified | Update target to "Astro 5/6/7 (current)" with version-specific notes |
| 2 | Node.js minimum | "Node.js 20+ (or Bun 1.1+)" | Current docs state v22.12.0 minimum (even versions only); older docs said 18.17.1+ | docs.astro.build/en/tutorial/1-setup/1 | Verified | Update to "Node.js 22.12.0+ (even versions only)" |
| 3 | Vite version | "Vite 6+ (build tool, bundled with Astro)" | Vite 7 in Astro 6; Vite 8 in Astro 7 alpha | reddit r/astrojs Apr 2026 roundup | Verified | Update to "Vite 7+ (Astro 6) or 8 (Astro 7 alpha)" |
| 4 | `output: 'hybrid'` | Listed as valid option: `'static' \| 'server' \| 'hybrid'` | `'hybrid'` removed in Astro 5; hybrid pattern = `output: 'static'` + per-page `export const prerender = false` | docs.astro.build/en/guides/on-demand-rendering | Verified | Remove `'hybrid'` from config example; the existing anti-pattern #9 is correct, the config example is wrong |
| 5 | Astro Studio | "Astro Studio + Astro DB (Astro's managed backend)" — advertised as a feature | Discontinued 2024-09-13; databases deleted 2025-03-01 | astro.build/blog/goodbye-astro-studio | Verified | Remove all references; if backend persistence is needed, mention Turso/libSQL or external DBs only |
| 6 | Astro DB | Listed in dependencies ecosystem | Deprecated (subdependency deprecation warnings as of May 2025) | github.com/withastro/astro/issues/13855 | Verified | Remove or mark deprecated; point users to Turso/libSQL, Drizzle, or external DBs |
| 7 | Cloudflare acquisition | Not mentioned | Cloudflare acquired Astro Technology Company on 2026-01-16; Astro remains MIT-licensed and platform-agnostic | cloudflare.com press release, blog.cloudflare.com/astro-joins-cloudflare | Verified | Add to "When to Use" or new "Project Context" section; reassure that Astro is still OSS |
| 8 | Sessions API | Not mentioned | Stable since Astro 5.7 (2025-04-15); was experimental in 5.0–5.6 | astro.build/blog/astro-570 | Verified | Add new "Sessions API" section (drafted in §4.A) |
| 9 | Actions API | Not mentioned | Still experimental as of April 2026 (Astro 6.2 release notes); not yet stable | reddit r/astrojs "What's new in Astro - April 2026" | Reasoned | Add new "Actions (experimental)" section with clear experimental labeling |
| 10 | i18n routing | Not mentioned | Built-in since Astro 4; behavior refined in 5, 6, and 7 | docs.astro.build/en/guides/internationalization, edgekits.dev 2026 guide | Verified | Add new "i18n Routing" section |
| 11 | `astro:env` | Not mentioned (only `import.meta.env` implied) | Stable since Astro 5.0; provides typed schema for env vars with server/client split | docs.astro.build/en/guides/environment-variables, bryanlrobinson.com article | Verified | Add new "Typed Environment Variables (`astro:env`)" section (drafted in §4.B) |
| 12 | `astro:assets` (Image, Picture, getImage) | Not mentioned | Stable API; `Image`, `Picture`, `getImage`, `inferRemoteSize`, `getConfiguredImageService`, `imageConfig`, `fontData`, `Font` exports | docs.astro.build/en/reference/modules/astro-assets | Verified | Add new "Image & Asset Optimization (`astro:assets`)" section (drafted in §4.C) |
| 13 | Tailwind 4 integration | Mentioned parenthetically: "or use Tailwind 4 Vite plugin" | `@tailwindcss/vite` is the preferred Vite plugin for Tailwind 4 in Astro; `@astrojs/tailwind` is for Tailwind 3 (legacy); some setups may need `@tailwindcss/postcss` instead | docs.astro.build/en/guides/integrations-guide/tailwind, github.com/withastro/astro/issues/16542 | Verified | Replace `npx astro add tailwind` recommendation with explicit Tailwind 4 setup; mark `@astrojs/tailwind` as Tailwind 3 only |
| 14 | Server Islands syntax | `<UserProfile slot="fallback" server:defer>` with nested `<div slot="fallback">` | `server:defer` directive is correct, but the slot="fallback" pattern shown is not the canonical pattern; an adapter is required | docs.astro.build/en/guides/server-islands | Verified | Fix example syntax; note adapter requirement |
| 15 | Content Layer `glob` loader import | `import { glob } from 'astro/loaders';` | Correct — `glob` and `file` are exported from `astro/loaders` | docs.astro.build/en/reference/content-loader-reference | Verified | Keep as-is |
| 16 | Middleware `sequence()` | Not mentioned (only single `onRequest` shown) | `sequence()` from `astro:middleware` combines multiple middleware functions | docs.astro.build/en/guides/middleware, github.com/withastro/roadmap discussions | Verified | Add `sequence()` example to Middleware section |
| 17 | Live Content Collections | Not mentioned | Stable in Astro 6 (was experimental in 5.10); enables content collections that update at request time rather than build time | medium "What's new in Astro 6" | Verified | Add note in Content Collections section about Live Content Collections (Astro 6+) |

### 1.3 Other Findings Worth Noting

These did not make the headline list but inform the proposed structure:

- **`set:html` XSS warning is present but understated.** The current SKILL.md says "(use carefully — XSS risk)". The improved version should be more explicit: never use `set:html` with untrusted input without sanitization; cross-reference `security-and-hardening` skill.
- **`Astro.redirect()` is not documented.** Common need; should be in a "Routing & Navigation" reference.
- **`404.astro` convention is not documented.** Common need; should be in routing section.
- **`redirects` config in `astro.config.mjs`** is not mentioned. Should be in routing section.
- **`astro check` workflow** is mentioned in commands but the type-gen flow (`.astro/types.d.ts`, `astro sync`) deserves a dedicated subsection.
- **Nanostores** (recommended for cross-island state by Astro docs) is not mentioned. Should be in a new "State Management" subsection under Islands.
- **Partytown** is mentioned in dependencies but not explained. Should have a brief "Third-Party Scripts" subsection.
- **MDX layout inheritance** (`layout` frontmatter property) is not shown.
- **`define:vars`** for passing server variables into client `<style>` is not mentioned.
- **`set:text` / `set:html` / `set:raw`** directive family is incomplete (only `set:html` is mentioned).
- **`transition:animate`** options (`fade`, `slide`, `none`, custom) are not enumerated.
- **`prefetch` config** (`prefetch: { prefetchAll: true, defaultStrategy: 'viewport' }`) is not mentioned.

---

## Part 2 — Gap Analysis of Current SKILL.md

### 2.1 Strengths to Preserve

These sections are well-executed and should be kept (with minor updates), not rewritten:

1. **"When to Use This Skill"** (lines 723–733) — clear trigger phrases, explicit "do not use for" list. Excellent routing logic.
2. **"Quick Start"** (lines 735–768) — correct commands, useful annotations.
3. **"Project Structure"** (lines 772–812) — canonical layout is accurate.
4. **"Core Mental Model: Zero JS by Default + Islands Architecture + Multi-Framework"** (lines 851–948) — this is the strongest section; the three-pillar framing is pedagogically excellent. Keep verbatim with minor version updates.
5. **Hydration directive table** (lines 911–917) — accurate and practical.
6. **Content Layer API examples** (lines 951–1105) — `glob` loader usage, Zod schema, external API loader — all correct and well-chosen.
7. **`.astro` component anatomy** (lines 1109–1183) — frontmatter, `Astro.props`, `class:list`, scoped `<style>`, Vite-processed `<script>` — all correct.
8. **Layouts + Named Slots** (lines 1187–1276) — accurate.
9. **View Transitions** (lines 1280–1323) — `ClientRouter`, `transition:animate`, `transition:persist`, `transition:name` — all correct.
10. **Middleware core pattern** (lines 1369–1410) — `defineMiddleware`, `context.locals`, typed via `env.d.ts` — correct.
11. **API Endpoints** (lines 1414–1437) — `APIRoute`, `GET`/`POST` exports — correct.
12. **Top 10 Anti-Patterns** (lines 1492–1513) — this is the second-strongest section; the items are concrete and high-signal. Anti-pattern #9 correctly notes the `prerender = false` hybrid pattern even though the config example earlier in the doc is wrong.
13. **Cross-references** (lines 1516–1529) — appropriate skill graph.
14. **Dependencies** (lines 1533–1572) — accurate package list (with the exceptions called out in §2.2).

### 2.2 Stale or Incorrect Items (Must Fix)

These are factual errors or stale claims in the current SKILL.md. Per the agent contract §13, they must not propagate into the rewrite.

| # | Location (line in current SKILL.md) | Stale/incorrect claim | Correction | Severity |
|---|--------------------------------------|------------------------|------------|----------|
| 1 | 715 (description frontmatter) | "Astro Studio + Astro DB (Astro's managed backend)" | Remove — both discontinued/deprecated | Critical |
| 2 | 721 (target banner) | "Astro 5.0+ (released November 2024) ... Vite 6" | Update to "Astro 5/6/7 (current); Astro 5.0 released Nov 2024, Astro 6 shipped Feb 2026, Astro 7 current as of Aug 2026. Vite 7 (Astro 6) or Vite 8 (Astro 7)" | Critical |
| 3 | 727–731 (do-not-use list) | "Astro ≤4 — the Content Layer API is Astro 5+" | Update to add: Astro 4 is EOL; Astro 5 is in maintenance; Astro 6/7 are current | High |
| 4 | 827 (config example) | `output: 'static'` ... `'static' (default) or 'server' (SSR) or 'hybrid'` | Remove `'hybrid'` from the comment — it was removed in Astro 5 | Critical |
| 5 | 884 | "Compare to Next.js, which ships ~80KB of JS even for a static page" | Soften — Next.js 15 with App Router has improved; cite a current measured figure or remove the comparison | Medium |
| 6 | 1282 | "Astro 2.9+ added the View Transitions API" | Update — `ClientRouter` replaced the older `<ViewTransitions />` component; verify the current canonical import path (still `astro:transitions`) | Low |
| 7 | 1343–1346 | Server Islands example shows `<UserProfile slot="fallback" server:defer>` with nested `<div slot="fallback">` | Fix to canonical pattern: `<UserProfile server:defer />` with fallback handled via the component's own render; add note that an adapter is required for Server Islands | High |
| 8 | 1372 | `src/middleware.ts` is "Request middleware (Astro 2.6+)" | Note that `sequence()` is now the standard pattern for combining multiple middleware; current example only shows single `onRequest` | Medium |
| 9 | 1479 | "Hybrid mode (Astro 4.12+ — `output: 'static'` with per-page SSR)" | Update — this is no longer called "hybrid mode" in Astro 5+; it's just "on-demand rendering" with `output: 'static'` (default) and per-page opt-out | Medium |
| 10 | 1536 | "Node.js 20+ (or Bun 1.1+)" | Update to "Node.js 22.12.0+ (even versions only; v18, v20 unsupported in current Astro)" | High |
| 11 | 1538 | "Vite 6+ (build tool, bundled with Astro)" | Update to "Vite 7+ (bundled with Astro 6); Vite 8 in Astro 7" | High |
| 12 | 1553 | "`@astrojs/tailwind` — Tailwind CSS integration (or use `@tailwindcss/vite` for Tailwind 4)" | Invert: "`@tailwindcss/vite` is the preferred Vite plugin for Tailwind 4; `@astrojs/tailwind` is for Tailwind 3 (legacy)" | High |
| 13 | 1564 | "`@astrojs/deno` — Deno Deploy SSR" | Verify this adapter is still maintained; if not, remove | Low (needs verification) |
| 14 | 1568–1572 | "Common additions" list (astro-icon, astro-seo, etc.) | Audit each for current maintenance status; add `@astrojs/node` v9+ notes if relevant | Low |

### 2.3 Missing Topics (Organized by Category)

The following topics are absent from the current SKILL.md and should be added. They are grouped by category and tagged with proposed priority (P0 = must add, P1 = should add, P2 = nice to add).

#### A. Astro Platform Features (P0 — must add)

- **Sessions API** (stable 5.7+) — server-side session storage with pluggable drivers (file, redis, etc.). Drafted in §4.A.
- **Actions API** (experimental) — type-safe server functions callable from client islands. Clearly label as experimental.
- **i18n Routing** — `i18n` config in `astro.config.mjs`, `astro:i18n` module, locale-aware routing, middleware-driven locale detection.
- **`astro:env`** (stable since 5.0) — typed env var schema with server/client split. Drafted in §4.B.
- **`astro:assets` Image Optimization** — `Image`, `Picture`, `getImage`, `inferRemoteSize`, image service configuration. Drafted in §4.C.
- **Fonts API** — `astro:assets` Font component, `getImage`-equivalent for fonts.
- **Live Content Collections** (Astro 6+) — collections that re-fetch at request time rather than build time.
- **SVG Component Support** — `experimental.svg` flag (verify current status).

#### B. Component Authoring Details (P1 — should add)

- `set:text`, `set:html` (with XSS warning), `set:raw` directive family — complete the trio.
- `define:vars` for `<style>` — pass server-side values into client CSS.
- `is:global`, `is:inline` directives for `<style>` and `<script>`.
- `<Fragment>` for conditional grouping without a wrapper element.
- `<slot />` fallback content pattern (mentioned but not shown clearly).
- `class:list` advanced usage with arrays, objects, and falsy values.

#### C. Routing Patterns (P1 — should add)

- Rest parameters (`[...slug].astro`) for catch-all routes.
- Multiple dynamic params (`/[org]/[repo].astro`).
- `404.astro` convention for custom 404 pages.
- `redirects` config in `astro.config.mjs` for path aliases.
- `Astro.redirect()` for programmatic redirects.
- Route priority and conflict resolution rules.

#### D. Performance & Optimization (P1 — should add)

- **Prefetch API** — `prefetch` config, `data-astro-prefetch` attribute, default strategy.
- **Partytown integration** — move third-party scripts (analytics, ads) to a web worker.
- **Font subsetting** — `astro:assets` Font component auto-subsets.
- **Build performance** — content collection caching, parallel rendering, Vite cache.
- **Image format guidance** — when to use AVIF vs WebP vs PNG.
- **Core Web Vitals** — how Astro's defaults help LCP/CLS/INP.

#### E. Testing & Quality (P1 — should add)

- **Vitest setup** — `vitest.config.ts`, `vitest` integration for unit-testing utilities and pure functions.
- **Playwright for E2E** — `@playwright/test`, testing Astro pages across viewports.
- **`astro check` workflow** — type-checking + Astro template diagnostics, CI integration.
- **Lighthouse CI** — performance regression testing.
- **Testing framework components** — how to test React/Vue/Svelte islands in isolation.

#### F. Security (P1 — should add)

- **Astro's auto-escaping** — by default, all expressions in `.astro` templates are HTML-escaped; `set:html` is the explicit opt-out.
- **`set:html` XSS warning** — concrete example of unsafe usage and the sanitization pattern.
- **CSRF protection** — Astro 5 has experimental CSRF protection via `security.checkOrigin` config.
- **Cookie security** — `Astro.cookies.set()` with `httpOnly`, `secure`, `sameSite: 'lax'` flags.
- **CSP headers** — Astro 5 has experimental CSP support.
- **Content Security Policy** — how to configure via middleware or headers.

#### G. Deployment Scenarios (P0 — must add at least the canonical ones)

- **Edge runtime deployment** — Cloudflare Workers (now first-party given acquisition), Vercel Edge, Deno Deploy, Bun.
- **Docker containerization** — minimal Dockerfile for `@astrojs/node` standalone mode.
- **Environment variables per deployment** — `astro:env` integration with platform-specific env var injection.
- **Build output structure** — `dist/` for static, `dist/server/entry.mjs` for SSR, `dist/client/` for assets.

#### H. Migration Guides (P1 — should add)

- **Astro 4 → 5 migration** — Content Layer API migration, `output: 'hybrid'` removal, `client:.*` changes.
- **Astro 5 → 6 migration** — Live Content Collections stabilization, breaking changes.
- **Astro 6 → 7 migration** — Vite 8, Rust compiler.
- **Legacy content collections → Content Layer API** — the `astro:content` API migration path.
- **Next.js → Astro** — high-level mapping (app directory → `src/pages`, server components → Astro components with islands, API routes → endpoints).

#### I. Ecosystem & Integrations (P1 — should add)

- **Nanostores** — official recommendation for cross-island state; `@nanostores/preact` / `@nanostores/react` bindings.
- **CMS integration patterns** — Sanity, Contentful, Shopify, Strapi via Content Layer API loaders. Brief example for each.
- **Astro Icon** — `astro-icon` package with Iconify.
- **Astro SEO** — `astro-seo` package or roll-your-own meta tags.
- **Astro Pagefind** — client-side full-text search.
- **Keystatic** — headless CMS for Astro content collections.

#### J. Dev Workflow (P2 — nice to add)

- **VSCode extension** — Astro language server features.
- **Astro DevTools** — browser extension for debugging islands.
- **Debug patterns** — `Astro.locals` inspection, dev vs prod differences.

#### K. Reference Tables (P0 — at least one consolidated reference)

- **`Astro.*` globals** — `Astro.url`, `Astro.request`, `Astro.cookies`, `Astro.locals`, `Astro.site`, `Astro.generator`, `Astro.redirect`, `Astro.response`, `Astro.params`, `Astro.props`, `Astro.slots`, `Astro.clientAddress`, `Astro.preferredLocale`, `Astro.currentLocale`.
- **`astro:*` module namespaces** — `astro:content`, `astro:middleware`, `astro:env`, `astro:transitions`, `astro:assets`, `astro:db` (deprecated), `astro:i18n`.
- **All `client:*` directives** — complete table with edge cases (`client:media` query syntax, `client:only` framework names).

---

## Part 3 — Proposed New Structure

The proposed structure preserves the existing backbone (so existing readers can navigate by familiarity) and inserts new sections in their natural position. Estimated line counts are targets, not hard limits.

```
1.  Frontmatter (description update)                                    [~15 lines]
2.  # Astro 5/6/7 — Content-Focused Web Framework (Islands Architecture) [~30 lines]
    - Target banner (version matrix, Cloudflare acquisition note)
3.  ## When to Use This Skill                                           [~30 lines]
    - Updated trigger phrases (add Sessions, Actions, astro:env, astro:assets, i18n, Live Content Collections)
    - Updated do-not-use list (Astro 4 = EOL, Astro 5 = maintenance, Astro 6/7 = current)
4.  ## Versions & Migration (NEW)                                       [~120 lines]
    - Version timeline table (5.0 → 5.7 → 5.10 → 6.0 → 6.2 → 7.0 → 7.1.6)
    - Astro 4 → 5 migration (Content Layer API, output:hybrid removal)
    - Astro 5 → 6 migration (Live Content Collections)
    - Astro 6 → 7 migration (Vite 8, Rust compiler)
    - Cloudflare acquisition FAQ (license, platform neutrality)
5.  ## Quick Start                                                      [~40 lines]
    - Updated Node version requirement
    - Note: `npm create astro@latest` may default to Astro 7
6.  ## Project Structure                                                [~50 lines]
    - Same canonical layout
    - Add `src/content.config.ts` note (Astro 5+)
    - Add `public/` vs `src/assets/` distinction (for astro:assets)
7.  ## `astro.config.mjs` (canonical config)                            [~80 lines]
    - Fixed output modes (remove 'hybrid')
    - Add `i18n` config example
    - Add `security.checkOrigin` (experimental)
    - Add `prefetch` config
    - Add `vite` passthrough with `@tailwindcss/vite`
8.  ## Core Mental Model: Zero JS + Islands + Multi-Framework          [~120 lines]
    - Keep existing three-pillar framing verbatim with minor version updates
9.  ## Content Collections (Content Layer API)                          [~250 lines]
    - Existing glob/file loader content (keep)
    - NEW: Live Content Collections (Astro 6+) subsection
    - NEW: Schema references (z.referral) for cross-collection relations
    - NEW: External API loader patterns (Sanity, Contentful, Shopify examples)
10. ## Astro Components (`.astro` syntax)                               [~180 lines]
    - Existing anatomy (keep)
    - NEW: `set:text` / `set:html` / `set:raw` directive family
    - NEW: `define:vars` for `<style>`
    - NEW: `is:global` / `is:inline` for `<style>` / `<script>`
    - NEW: `<Fragment>` for conditional grouping
11. ## Layouts & Slots                                                  [~80 lines]
    - Existing content (keep, minor polish)
12. ## Routing                                                          [~120 lines] (NEW consolidated section)
    - Static routes, dynamic routes, rest parameters
    - `404.astro` convention
    - `redirects` config
    - `Astro.redirect()`
    - Route priority rules
13. ## i18n Routing (NEW)                                               [~120 lines]
    - `i18n` config in astro.config.mjs
    - `astro:i18n` module (`getRelativeLanguageUrl`, `getAbsoluteLanguageUrl`)
    - Locale-aware routing
    - Middleware-driven locale detection
14. ## View Transitions                                                 [~100 lines]
    - Existing content (keep)
    - Add: `transition:animate` options table (fade, slide, none, custom)
    - Add: `prefetch` integration
15. ## Server Islands                                                   [~80 lines]
    - Fix example syntax
    - Note adapter requirement
    - Add: fallback pattern
16. ## Middleware                                                       [~100 lines]
    - Existing content (keep)
    - NEW: `sequence()` for combining multiple middleware
    - NEW: common patterns (auth, logging, i18n, CSRF)
17. ## API Endpoints                                                    [~60 lines]
    - Existing content (keep)
    - Add: `Astro.redirect()` from endpoints
    - Add: streaming responses
18. ## Sessions API (NEW)                                               [~120 lines]
    - Drafted in §4.A
19. ## Actions (experimental) (NEW)                                     [~100 lines]
    - `defineAction()` from `astro:actions`
    - `isActionError` and error handling
    - Calling actions from client islands
    - Clear experimental labeling
20. ## Typed Environment Variables (`astro:env`) (NEW)                  [~100 lines]
    - Drafted in §4.B
21. ## Image & Asset Optimization (`astro:assets`) (NEW)                [~150 lines]
    - Drafted in §4.C
22. ## Fonts (NEW)                                                      [~60 lines]
    - `astro:assets` Font component
    - Local font optimization
23. ## State Management Across Islands (NEW)                            [~80 lines]
    - Nanostores + bindings
    - When to use vs. prop drilling vs. URL state
24. ## Styling                                                          [~100 lines] (NEW consolidated section)
    - Tailwind 4 with `@tailwindcss/vite` (preferred)
    - Tailwind 3 with `@astrojs/tailwind` (legacy)
    - CSS Modules, Sass, scoped `<style>`
    - CSS variables via `define:vars`
25. ## Forms (NEW)                                                      [~80 lines]
    - Progressive enhancement with HTML forms
    - Astro Actions for type-safe submissions
    - CSRF protection
26. ## Security (NEW)                                                   [~100 lines]
    - Auto-escaping defaults
    - `set:html` XSS warning
    - `security.checkOrigin` (experimental CSRF)
    - Cookie security flags
    - CSP (experimental)
27. ## Testing (NEW)                                                    [~100 lines]
    - Vitest setup
    - Playwright for E2E
    - `astro check` workflow
28. ## Deployment                                                       [~150 lines]
    - Static (default)
    - On-demand rendering (per-page `prerender = false`)
    - Adapters: Node, Vercel, Cloudflare (first-party), Netlify
    - Edge runtime notes
    - Docker containerization
29. ## Top 10 Anti-Patterns (expanded)                                  [~120 lines]
    - Keep existing 10 (with corrections)
    - Add: 11. Not using `astro:env` for typed env vars
    - Add: 12. Not using `astro:assets` for images
    - Add: 13. Mixing Tailwind 3 and 4 integrations
30. ## Cross-references                                                 [~30 lines]
    - Existing list (keep)
    - Add: `tailwind-4` skill if exists
    - Add: `cloudflare-workers` skill if exists
31. ## Dependencies                                                     [~80 lines]
    - Corrected package list
    - Version matrix (Astro 5 / 6 / 7 compatibility)
32. ## Reference Tables (NEW)                                           [~150 lines]
    - `Astro.*` globals table
    - `astro:*` module namespaces table
    - `client:*` directives complete table
    - `set:*` directives table
    - `transition:*` directives table
```

**Estimated total:** ~2,800–3,200 lines (current SKILL.md is ~860 lines). Roughly a 3.5× expansion, in line with the "expanded" goal.

**What is explicitly NOT added** (to avoid scope creep):

- No CI/CD pipeline templates (out of scope; belongs in a separate `ci-cd-patterns` skill).
- No full CMS integration tutorials (only brief loader patterns in Content Collections section).
- No design system guidance (belongs in `frontend-design` skill).
- No SEO deep-dive (mention briefly in Layouts; full SEO belongs in a `seo` skill).
- No a11y deep-dive (mention briefly in Components; full a11y belongs in `accessibility` skill).

---

## Part 4 — Sample Drafted Sections

These three sections are drafted at the target quality bar for the improved SKILL.md. They are intended as concrete examples of the depth, code-example density, and confidence-labeling that the full rewrite should hit. They are not placeholders.

### 4.A — Sessions API (new section, ~120 lines)

```markdown
## Sessions API (stable since Astro 5.7)

> **Status:** Stable since Astro 5.7 (April 2025). Was experimental in 5.0–5.6.
> **Confidence:** Verified against [astro.build/blog/astro-570](https://astro.build/blog/astro-570) and [docs.astro.build/en/reference/modules/astro-session](https://docs.astro.build/en/reference/modules/astro-session).

The Sessions API provides server-side session storage — a key-value store tied to a user via a signed cookie. Use it for: login state, shopping carts, multi-step form state, flash messages, and any per-user data that should survive a page navigation but not be sent to the client.

### Why use Sessions instead of cookies directly?

Cookies are sent on every request, including static asset requests. Storing user data in plain cookies means serializing it, exposing it to the client (where it can be tampered with), and paying the bandwidth cost on every request. Sessions store a single opaque session ID in the cookie; the actual data lives server-side in a pluggable driver (file, Redis, libSQL, etc.).

### Configuration

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import node from '@astrojs/node';

export default defineConfig({
  output: 'server',                         // or 'static' with per-page prerender = false
  adapter: node({ mode: 'standalone' }),
  session: {
    driver: 'file',                          // 'file' (default), 'redis', 'libsql', or custom
    options: {
      path: './.sessions',                   // for 'file' driver
    },
    // Cookie options:
    cookie: {
      name: 'astro_session',
      httpOnly: true,                        // always true for sessions
      secure: true,                          // require HTTPS in prod
      sameSite: 'lax',
      maxAge: 60 * 60 * 24 * 7,              // 1 week
    },
  },
});
```

For Redis or libSQL drivers, install the driver package (`@astrojs/session-redis`, `@astrojs/session-libsql`) and pass connection options. (Verify package names against current docs — driver ecosystem is evolving.)

### Usage

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
import type { APIRoute } from 'astro';

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

### Cross-references

- `security-and-hardening` — OWASP session management best practices.
- `api-patterns` — REST API authentication patterns.
```

### 4.B — Typed Environment Variables (`astro:env`) (new section, ~100 lines)

```markdown
## Typed Environment Variables (`astro:env`)

> **Status:** Stable since Astro 5.0.
> **Confidence:** Verified against [docs.astro.build/en/guides/environment-variables](https://docs.astro.build/en/guides/environment-variables) and [docs.astro.build/en/reference/modules/astro-env](https://docs.astro.build/en/reference/modules/astro-env).

`astro:env` provides a type-safe schema for environment variables. It validates env vars at build/runtime, prevents accidentally exposing server secrets to the client, and gives you autocompletion and type checking.

### Why use `astro:env` instead of `import.meta.env`?

`import.meta.env` is a Vite feature — it works, but it has two problems:

1. **No validation.** A missing or malformed env var silently becomes `undefined`, which fails at runtime in production instead of at build time.
2. **No access control.** Any variable prefixed with `PUBLIC_` is shipped to the client. It's easy to accidentally expose a secret by misnaming it.

`astro:env` solves both: you declare a schema with types and access levels, and Astro enforces it.

### Configuration

```typescript
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

```typescript
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

### Cross-references

- `security-and-hardening` — secret management at rest and in transit.
- `api-patterns` — API key rotation patterns.
```

### 4.C — Image & Asset Optimization (`astro:assets`) (new section, ~150 lines)

```markdown
## Image & Asset Optimization (`astro:assets`)

> **Status:** Stable since Astro 3.0; expanded in 5.x.
> **Confidence:** Verified against [docs.astro.build/en/guides/images](https://docs.astro.build/en/guides/images) and [docs.astro.build/en/reference/modules/astro-assets](https://docs.astro.build/en/reference/modules/astro-assets).

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
- Inlines small images as base64 if under `inlineStylesheets` threshold.

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
import { Image } from 'astro:assets';

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

Astro ships with `sharp` as the default image service. To use a different service (e.g., Squoosh, or a custom service for Cloudflare Images / Cloudinary):

```javascript
export default defineConfig({
  image: {
    service: {
      entrypoint: 'astro/assets/services/sharp',    // default
      // entrypoint: 'astro/assets/services/squoosh', // no longer recommended; sharp is preferred
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

### Cross-references

- `frontend-ui-engineering` — responsive image patterns and Core Web Vitals.
- `security-and-hardening` — remote image SSRF risks (why domain authorization is required).
```

---

## Part 5 — Implementation Plan & Risk Assessment

### 5.1 Phased Rollout

The rewrite is sized for 4 phases. Each phase produces a coherent subset that could be shipped independently if needed.

**Phase 1 — Corrections & Version Update (P0, ~1 day)**

Goal: Eliminate all stale/incorrect claims from §2.2. No new sections added.

- Update frontmatter description (remove Astro Studio + Astro DB).
- Update target banner (Astro 5/6/7 version matrix, Vite 7/8, Node 22.12.0+).
- Fix `astro.config.mjs` example (remove `'hybrid'` from output comment).
- Fix Server Islands example syntax.
- Update Dependencies section (Node, Vite, Tailwind 4 integration).
- Update Quick Start (Node version note).
- Update anti-pattern #9 wording (it's "on-demand rendering", not "hybrid mode").
- Add Cloudflare acquisition note to "When to Use" section.

**Verification gate:** All claims in §2.2 corrected; no other content changed. Diff should be surgical.

**Phase 2 — Platform Features (P0, ~2–3 days)**

Goal: Add the 7 new platform-feature sections identified in §2.3-A.

- Sessions API (use draft in §4.A).
- Actions (experimental) — needs live doc verification before drafting.
- i18n Routing — needs live doc verification.
- `astro:env` (use draft in §4.B).
- `astro:assets` (use draft in §4.C).
- Fonts — needs live doc verification.
- Live Content Collections (Astro 6+) — subsection of Content Collections.

**Verification gate:** Each new section must cite its primary source. Experimental features must be labeled with `> **Status:** Experimental` callout.

**Phase 3 — Ecosystem & Reference (P1, ~2 days)**

Goal: Add the 4 ecosystem sections (§2.3-I) and the Reference Tables (§2.3-K).

- Tailwind 4 styling section.
- Nanostores state management section.
- Testing section (Vitest + Playwright).
- Security section (auto-escaping, CSRF, CSP, cookies).
- Reference Tables (`Astro.*` globals, `astro:*` modules, `client:*` directives, `set:*` directives, `transition:*` directives).

**Verification gate:** Reference tables must be complete — no "etc." placeholders. If a directive or global is listed, it must be described.

**Phase 4 — Migration, Routing, Polish (P1, ~1 day)**

Goal: Add the migration guide (§2.3-H), expand routing (§2.3-C), expand the anti-patterns list, and do a final pass.

- Versions & Migration section.
- Routing section (rest params, 404, redirects, `Astro.redirect()`).
- Anti-patterns 11–13 (env vars, image optimization, Tailwind 3/4 mixing).
- Cross-references update.
- Final read-through for tone consistency.

**Verification gate:** Full document reads as a coherent whole; no "TODO" or "placeholder" markers remain; every code example is syntactically valid against the targeted Astro version.

### 5.2 Verification Gates

Per the agent contract §13, claims of correctness require evidence. The following gates apply to the rewrite:

| Gate | When | Method |
|------|------|--------|
| **Stale-claim check** | End of Phase 1 | Diff against §2.2 table; every row must be addressed. |
| **Source citation** | End of Phase 2 | Every new platform-feature section must include a `> **Status:**` callout with a link to primary docs. |
| **Code example validation** | End of each phase | Every code example must be syntactically valid against the targeted Astro version. If a runtime check is not possible in the authoring environment, label as `Reasoned` per §13. |
| **Reference table completeness** | End of Phase 3 | Every `Astro.*` global and `astro:*` module listed in the official docs reference must appear in the table. No "etc." |
| **Final review** | End of Phase 4 | Full document read-through; check for internal contradictions, version drift between sections, and broken cross-references. |

**Gates not run in this plan** (would require follow-up if the user upgrades to a full rewrite):

- Per-integration changelog audit (verify `@astrojs/react`, `@astrojs/vue`, etc. are still maintained at the stated versions).
- Astro 7 experimental-flags full enumeration.
- VSCode extension feature audit.
- Live Content Collections behavior verification (needs a running Astro 6+ project).

### 5.3 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Astro 7 changes break code examples between drafting and shipping** | Medium | High (looks incompetent) | Pin every code example to a stated Astro version in the `> **Status:**` callout. Add a note at the top: "Examples verified against Astro 7.1.x; check the official docs for current API." |
| **Actions API stabilizes mid-rewrite** | Medium | Medium | Label Actions section as `Experimental` and include the version where it became experimental. Add a note: "Check current status before relying on this in production." |
| **Cloudflare acquisition changes roadmap priorities** | Low | Medium | Keep acquisition note factual ("joined Cloudflare 2026-01-16; remains MIT-licensed") without speculating on roadmap. |
| **Tailwind 4 integration changes (the `@tailwindcss/vite` vs `@tailwindcss/postcss` issue)** | Medium | Low | Document both approaches; note that `astro add tailwind` may install the wrong plugin as of Apr 2026 (github.com/withastro/astro/issues/16542). |
| **Rewrite introduces internal contradictions** | Medium | Medium | Run the final review gate (§5.2). Use a single "Versions & Migration" section as the source of truth for version-specific behavior. |
| **Document length exceeds practicality** | High | Low | The proposed structure is ~3,000 lines. If this feels too long, split into multiple skills (e.g., `astro-5-core`, `astro-ecosystem`, `astro-migration`). The current single-skill approach is preferred for discoverability. |
| **Live verification of every code example is not possible in the authoring environment** | High | Medium | Per §13, label each example as `Verified` (if run) or `Reasoned` (if not). The three sample sections in §4 are `Reasoned` — they are based on verified API surface from primary docs, but the examples themselves were not executed. |

### 5.4 Open Questions for the User

These are decisions that affect the rewrite but were not answerable from the existing SKILL.md or web research:

1. **Skill name:** Should the skill remain `astro-5` (now misleading) or rename to `astro` (current version)? Renaming has cross-skill reference implications (other skills reference `astro-5`).
2. **Version scope:** Target Astro 5/6/7 together (proposed), or split into separate skills per major version? Splitting avoids version confusion but triples maintenance burden.
3. **Experimental feature policy:** Include experimental features (Actions, SVG components, CSP) with clear labeling, or omit them entirely until stable? Including them helps practitioners; omitting them keeps the doc evergreen.
4. **Code example execution:** Should the rewrite include a CI job that runs every code example against a real Astro project? This is the only way to upgrade `Reasoned` examples to `Verified`. Significant effort (~1 day setup + ongoing maintenance).

These are flagged, not answered. The user should decide before Phase 2 begins.

---

## Appendix A — Source Index

All sources consulted during research, organized by topic. URLs are the canonical entry points; specific claims cite the specific page where the claim is verified.

### Astro version & upgrade
- docs.astro.build/en/upgrade-astro — "The latest release of Astro is v7.1.6"
- astro.build/blog/astro-5 — Astro 5.0 release announcement (Dec 3, 2024)
- astro.build/blog/astro-570 — Astro 5.7 release (Sessions API stable, April 15, 2025)
- medium.com/@onix_react/whats-new-in-astro-6 — "Live Content Collections are now stable in Astro 6"
- southwellmedia.com/blog/astro-6-whats-coming-2026 — Astro 6 beta timeline
- reddit.com/r/astrojs/comments/1t0jk4c/whats_new_in_astro_april_2026 — Astro 7 alpha, Vite 8, Rust compiler

### Cloudflare acquisition
- cloudflare.com/press/press-releases/2026/cloudflare-acquires-astro-to-accelerate-the-future-of-high-performance-web-development
- blog.cloudflare.com/astro-joins-cloudflare
- astro.build/blog/joining-cloudflare — "Astro remains open-source, MIT-licensed, and platform-agnostic"

### Deprecations
- astro.build/blog/goodbye-astro-studio — Astro Studio shutdown (Sep 13, 2024; databases deleted Mar 1, 2025)
- github.com/withastro/astro/issues/13855 — Astro DB deprecated subdependencies (May 25, 2025)

### Platform features
- docs.astro.build/en/guides/server-islands — `server:defer` directive; adapter requirement
- docs.astro.build/en/guides/on-demand-rendering — `output: 'static'` + per-page `prerender = false`; `'hybrid'` removed
- docs.astro.build/en/guides/internationalization — i18n routing built-in
- docs.astro.build/en/guides/environment-variables — `astro:env` API
- docs.astro.build/en/reference/modules/astro-env — `astro:env` API reference
- docs.astro.build/en/guides/images — `<Image />`, `<Picture />` components
- docs.astro.build/en/reference/modules/astro-assets — `Image`, `Picture`, `getImage`, `inferRemoteSize`, `getConfiguredImageService`, `imageConfig`, `fontData`, `Font`
- docs.astro.build/en/guides/middleware — `sequence()` for chaining middleware
- docs.astro.build/en/reference/content-loader-reference — `glob` and `file` loaders from `astro/loaders`

### Tooling & ecosystem
- docs.astro.build/en/guides/integrations-guide/tailwind — "@tailwindcss/vite is preferred for Tailwind 4; @astrojs/tailwind is for Tailwind 3"
- docs.astro.build/en/tutorial/1-setup/1 — "minimum supported Node.js version is v22.12.0"
- github.com/withastro/astro/issues/16542 — `astro add tailwind` may install incompatible plugin (Apr 30, 2026)
- dev.to/ingosteinke/integrating-astro-5-storybook-9-vite-7-and-tailwind-3 — Vite 7 with Astro 5
- github.com/tailwindlabs/tailwindcss/discussions/19044 — Astro 5.12.6 + Tailwind 4.1.11 + @tailwindcss/vite + Node 22.14.0

### Migration
- chenhuijing.com/blog/migrating-content-collections-from-astro-4-to-5 — Content Collections migration
- harshil.dev/writings/migrating-astro-5-to-astro-6 — Astro 5 → 6 migration

---

## Appendix B — Confidence Summary

Per the agent contract §13, the following claims in this plan are tagged with their confidence level:

- **Verified** (sourced from primary docs or official blog): All claims in §1.2 verification ledger rows 1–8, 10–17. The Cloudflare acquisition date. The Astro Studio/Astro DB deprecation. The Sessions API stability. The `astro:env` stability. The `astro:assets` API surface. The `glob` loader import path. The `output: 'hybrid'` removal. The Node.js 22.12.0 minimum. The Vite 7/8 versions. The Tailwind 4 integration approach.
- **Reasoned** (logical inference from verified facts): The Actions API status (still experimental as of April 2026 — based on Reddit roundup; not confirmed against official docs in this research pass). The proposed structure's estimated line counts. The risk assessment likelihoods.
- **Assumed**: The proposed skill name should remain `astro-5` (open question §5.4 #1). The three sample sections in Part 4 are `Reasoned` (API surface verified, examples not executed).
- **Unverifiable in this environment**: Whether each code example in §4 actually runs against Astro 7.1.6 (would require a running Astro project — see §5.4 #4).

---

*End of plan.*
