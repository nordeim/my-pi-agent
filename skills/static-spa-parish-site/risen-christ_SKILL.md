---
name: risen-christ
display_name: Church of the Risen Christ — Toa Payoh
version: 1.4.4
last_updated: 2026-08-31
project_state: "static SPA — 35 files / 202 tests + 51 E2E green — port of www.risenchrist.org.sg, hop Rother→St Joseph→St Mary (src.orig, pruned round-12)→Risen Christ (src)"
verified: pnpm lint 0 + pnpm typecheck 0 + pnpm test 35/202 + pnpm test:e2e 51 + pnpm build 397.52kB → dist/index.html + dist/_headers + dist/images/8
stack: react 19.2.8 / vite 7.3.6 / tailwind 4.3.3 (@tailwindcss/vite 4.1.17) / typescript 5.9.3 / react-router 7.18.2 / singlefile 2.3.3 / eslint 9.39.5 flat / vitest 3.2.6 jsdom / testing-library 16.2.0 / playwright 1.55.1 chromium (51 E2E green)
rendering: static SPA (HashRouter, no SSR)
data_layer: file-backed typed arrays in src/data/* + const site object
deploy: vite-plugin-singlefile → dist/index.html + dist/images/ → GH Pages / S3 (publicDir copy — not inlined)
port_provenance: Singapore port of https://www.risenchrist.org.sg/ — Church of the Risen Christ, 91 Toa Payoh Central, Singapore 319193 — first Catholic church in the new town, blessed 3 July 1971 (first air-con, Fr Pierre Abrial); lineage Rother Shrine → St Joseph BT → St Mary of the Angels (src.orig) → Risen Christ (src) — see Appendices D+F
---

# `risen-christ` — Engineering Skill

> **How to use this document:** This is the single-source-of-truth for any future agent extending, debugging, onboarding, or replicating the Church of the Risen Christ (Toa Payoh) port. Read §§ 1–4 for identity and constraints, §5 for where to put code, §§ 9–11 before shipping, and §§ 15–20 as copy-pasteable contracts. Every version, hex, and path is verified against `package.json` / `src/index.css` / `tsconfig.json` / `src/data/*` — if it drifts, fix this file first.

**Sources of truth:** `README.md` (visitor overview) → `AGENTS.md` (60-sec cheat sheet) → `CLAUDE.md` (deep workflow, 6-phase) → this file (complete distillate). If they conflict, trust executable config. Note: `src.orig/` is the archived St Mary of the Angels port (Rother → St Joseph → St Mary → Risen Christ lineage); its ignore entries in eslint/vite config are active guards — not inert.

**File name note:** Canonical skill for **Church of the Risen Christ, Toa Payoh** as of 2026-08-31 (this file). Lineage files `st-mary-of-angels_SKILL.md` (previous port) and `rothershrine-v2_SKILL.md` are retained as redirect stubs — do not edit them independently; all future updates go here.

**Migration note:** This file is the Risen Christ distillate (from the St Mary of the Angels distillate; third hop of the lineage). The sectional skeleton (§§ 1–20 + Appendices + Quick Ref) is preserved verbatim; all parish narrative is verified against `src/App.tsx` / `src/data/content.ts` / `src/data/nav.ts` / `src/data/site.ts` / `public/images/`. Lineage: Rother Shrine → St Joseph BT → St Mary of the Angels (archived as `src.orig/`) → Risen Christ (src). See Appendix D (second-hop history) and Appendix F (St Mary → Risen Christ diff).

---

## Table of Contents

1. [Project Identity & Design Philosophy](#1-project-identity--design-philosophy)
2. [Tech Stack & Environment](#2-tech-stack--environment)
3. [Bootstrapping & Configuration](#3-bootstrapping--configuration)
4. [The Design System (Code-First)](#4-the-design-system-code-first)
5. [Component Architecture & Patterns](#5-component-architecture--patterns)
6. [Custom Hooks Deep Dive](#6-custom-hooks-deep-dive)
7. [Content Management & Data Ingestion](#7-content-management--data-ingestion)
8. [Accessibility (WCAG AAA) Implementation](#8-accessibility-wcag-aaa-implementation)
9. [Anti-Patterns & Common Bugs](#9-anti-patterns--common-bugs)
10. [Debugging Guide](#10-debugging-guide)
11. [Pre-Ship Checklist](#11-pre-ship-checklist)
12. [Lessons Learnt & How to Avoid Them](#12-lessons-learnt--how-to-avoid-them)
13. [Pitfalls to Avoid](#13-pitfalls-to-avoid)
14. [Best Practices](#14-best-practices)
15. [Coding Patterns](#15-coding-patterns)
16. [Coding Anti-Patterns](#16-coding-anti-patterns)
17. [Responsive Breakpoint Reference](#17-responsive-breakpoint-reference)
18. [Z-Index Layer Map](#18-z-index-layer-map)
19. [Color Reference (Complete)](#19-color-reference-complete)
20. [The Complete TypeScript Interface Reference](#20-the-complete-typescript-interface-reference)
- [Appendix A — ADRs](#appendix-a--adrs-architecture-decision-records)
- [Appendix B — Live-Site Validation](#appendix-b--live-site-validation)
- [Appendix C — The Meticulous Approach (6-Phase Workflow)](#appendix-c--the-meticulous-approach-6-phase-workflow)
- [Appendix D — Migration Note (Rother → St Joseph BT → St Mary)](#appendix-d--migration-note-rother--st-joseph-bt--st-mary)
- [Appendix E — Validation: src vs src.orig (2026-08-30)](#appendix-e--validation-src-vs-srcorig-2026-08-30)
- [Appendix F — Migration Note (St Mary → Risen Christ)](#appendix-f--migration-note-st-mary--risen-christ)
- [Quick Reference Card](#quick-reference-card)

---

## 1. Project Identity & Design Philosophy

**One sentence:** A reverent, editorial parish site for Church of the Risen Christ — Toa Payoh — the first Catholic church in the new town, blessed 3 July 1971 by Archbishop Michel Olçomendy and Singapore's first fully air-conditioned church (Fr Pierre Abrial, $450k), at 91 Toa Payoh Central gathering the household in English, Mandarin, Tamil, Bahasa Indonesia, and Tagalog — named for the Resurrection: He is risen (feast Easter Sunday).

**The parish in one breath:** 1969 Catholics of Toa Payoh gather at Ho Ping Centre, Block 82 Lorong 4, and the government invites tenders for a 40,000-square-foot plot at Toa Payoh Central / Lorong 4 → 3 July 1971 the church is consecrated by Archbishop Michel Olçomendy — the new town's first Catholic church and Singapore's first fully air-conditioned church (Fr Pierre Abrial, $450k) → 1970s many tongues — English, Mandarin, Tamil — and the Velankanni devotion takes root → 2003 four-storey wing: classrooms, youth room, auditorium → 2010s Filipino, Indonesian, and Myanmar households join; Simbang Gabi; monthly Bahasa/Tamil/Tagalog Masses → 2021 Golden Jubilee → 2023 Fr Brian D'Souza parish priest → 2026 Grateful, Faithful, and Sent (54th Velankanni, CEP, F.R.E.E. Acts).

**Parish constants (canonical in `src/data/site.ts`):**

| Fact | Value | Source |
|---|---|---|
| Name | Church of the Risen Christ — `shortName` Risen Christ Toa Payoh — `chineseName` 耶稣复活堂 | `site.name / shortName / chineseName` |
| Address | 91 Toa Payoh Central, Singapore 319193 | `site.address.full` (with `query` getter for maps) |
| Tagline / Vision | "Grateful, Faithful, and Sent." / "He is risen." | `site.tagline / site.vision` |
| Patronal feast | The Risen Christ — **Easter Sunday** | `site.feast` |
| Gates | Open for Mass, Adoration, and parish programmes | `site.hours.gates` |
| Hours | 6 keys: `gates` (open for Mass/Adoration/programmes), `mainChurch`, `chapel` Adoration Room Mon 12–22 / Tue–Sat 7–22 / Sun 7–18, `reception` Mon–Fri 9–16 / Sat 9–12 / Sun 8–13, `parishOffice` Mon–Fri 9–16 / Sat 9–12 / Sun 8–13, `mediaCentre` Tue & Fri 12–16 / Sat 12–19 / Sun 8–13, `adorationRoom` (same as chapel) | `site.hours` |
| Transport | MRT Toa Payoh NS19 — 6 minutes' walk from Exit A; buses 88, 157, 163 — 2 minutes from stop B52261 | `site.transport` |
| Contacts | Parish priest +65 6255 7509, office +65 6253 2166, media centre +65 6356 5958, emails `crc.secretariat@catholic.org.sg` · `crc.admin@` / `crc.pastoral@` / `crc.youth@` / `dpo.crc@catholic.org.sg` | `site.contact` |
| Giving identity | UEN **T08CC4042G**, cheque payable **Church of the Risen Christ** | `site.uen / site.chequePayee` |

**Design thesis — "Reverent, not austere":** Warm parchment/maroon/gold on cream, generous whitespace, Fraunces display + Source Sans 3 body. Every page is a welcome from Toa Payoh Central — the 1971 first air-con nave, the Adoration Room, the parish hall & media centre — not a brochure. No purple gradients, no `Inter` defaults, no generic card-grid templates.

**Non-negotiable rules:**

1. **Parish fidelity over pixel theft** — rephrase narrative, preserve Singapore facts exactly (1969–2026 Toa Payoh details: Ho Ping Centre, 1971 Olçomendy blessing, first air-con $450k, Velankanni, Simbang Gabi, 91 Toa Payoh Central, Mass 6.30a/6p + Sat 5.30p + Sun 5 Masses, UEN T08CC4042G). Never reintroduce St Mary of the Angels / Bukit Batok narratives outside the historical appendices — this is Church of the Risen Christ.
2. **Single-file deployability** — must remain a standalone `index.html` (+ `dist/images/`) shippable to GH Pages/S3 without a server. No SSR, no API until explicitly requested.
3. **Static-first data** — parish copy lives in `src/data/content.ts` + `src/data/nav.ts` + canonical facts in `src/data/site.ts`; no CMS/API to invent.
4. **Accessibility is doctrinal** — keyboard-navigable header, 4.5:1 contrast on `shrine-ink/cream`, meaningful `alt`, `prefers-reduced-motion` respect, SkipLink hash discipline under HashRouter.

**Anti-generic mandate:** Reject `Inter`/`Roboto` safety, purple-on-white clichés, predictable 3-col hero grids. Whitespace is structure. See `avant-garde-design-v4` when adding sections.

---

## 2. Tech Stack & Environment

| Layer | Technology | Locked Version | Critical Note |
|---|---|---|---|
| UI Runtime | `react` / `react-dom` | `19.2.8` | Hooks-only, no class components; `StrictMode` in `src/main.tsx` |
| Routing | `react-router-dom` | `7.18.2` | `HashRouter` intentionally for static hosts; see ADR-1 |
| Build | `vite` / `@vitejs/plugin-react` | `7.3.6` / `5.2.0` | Node ≥20 required; HMR default; alias `@→src/` |
| Styling | `tailwindcss` / `@tailwindcss/vite` | `4.3.3` / `4.1.17` | **CSS-first `@theme` inline** — no `tailwind.config.*`; tokens in `src/index.css` |
| Language | `typescript` / `@types/react` / `@types/react-dom` / `@types/node` | `5.9.3` / `19.2.18` / `19.2.5` / `22.20.1` | `strict` + `noUnusedLocals/Params` — breaches fail `tsc` |
| Icons | `lucide-react` | `1.34.0` | Header/footer + Home quick-facts + Give icons |
| Utils | `clsx` / `tailwind-merge` | `2.1.1` / `3.6.0` | `cn()` = `twMerge(clsx(...))` — only merge path |
| Bundling | `vite-plugin-singlefile` | `2.3.3` | Inlines JS+CSS into `dist/index.html`; `public/images/` → `dist/images/` (not inlined) |
| Fonts | Google Fonts (CDN, `index.html`) | — | `Fraunces` 400/500/600/700 + `Source Sans 3` 400/500/600/700; no runtime loader |

> All versions pinned exact (no `^`) in `package.json` (`pnpm@11.0.0`, `engines: node>=20`). Re-pin on upgrade; `pnpm --frozen-lockfile` in CI verifies lockfile. `package.json` version is **1.4.4** for the Risen Christ port (St Mary line was 1.2.0 — see Appendix F).

**Environment:** No `.env`, no DB, no auth, no docker. `pnpm` is the supported manager (`--frozen-lockfile` in CI). `npm ci` fails on these exact pins (typescript-eslint 8.28.0 peer range predates TS 5.9) — use `npm ci --legacy-peer-deps` if npm is unavoidable. `skills/` is vendored reference content — pruned in round 3 (2026-08-30) and re-added in full (catalog + per-skill `SKILL.md` files, commit `0be0fe8`, 2026-08-31); tooling (eslint ignores, tsconfig excludes, vite watch ignores) still excludes it — do not import or lint it. No `package-lock.json` in the repo (untracked, round 3). `docs/ssh-key.txt` was accidentally tracked in `0be0fe8` and untracked again in round 6 (`git rm --cached`; round-6 audit C1) — **the leaked key must be rotated by the repo owner**; history still contains it. `src.orig/` was **archived St Mary of the Angels** (Rother→St Joseph→St Mary lineage) — discovered still tracked (64 files) by the round-12 comparative-audit remediation (F-9: `.gitignore` listed it since round 3 but ignore rules do not untrack) and pruned 2026-08-31 (`git rm -r --cached` + tree removal; `repo-hygiene` guard now fails if any `src.orig` path re-enters the index; lineage history lives in Appendices D/F + git history).

**Test harness — current reality (2026-08-31, round-6 verified):**

| Suite | Status | Detail |
|---|---|---|
| `vitest` unit (`pnpm test`) | **35 files / 202 tests — green** | `ci-workflow` 4 + `repo-hygiene` 3 + `docs-contract` 16 + `utils/cn` 5 + `data/nav` 7 + `data/content` 10 + `data/site` 8 + `utils/massDay` 5 + `utils/monogram` 7 + `utils/deepLinks` 7 + `ui/Button` 11 + `SkipLink` 3 + `ui/Accordion` 6 + `SafeImage` 6 + `Header` 17 + `BackToTop` 7 + `ui/Reveal` 2 + `components/wcag-contrast` 5 + `pages/Ministries` 3 + `pages/cta-bands` 6 + `pages/worship-mass` 6 + `pages/about-visuals` 4 + `pages/event-chips` 3 + `pages/give-featured` 2 + `pages/give-uen` 3 + `pages/card-affordances` 6 + `components/Timeline` 3 + `pages/NotFound` 2 + `pages/History` 2 + `Layout` 2 + `hooks/useScrollProgress` 4 + `hooks/useScrollSpy` 6 + `ScrollProgress` 2 + `head` 13 + `security-headers` 6 via `src/test/setup.ts` (jest-dom + IntersectionObserver mock + scrollTo/scrollIntoView stubs + matchMedia stub). Data values: priests 3 (each phone+email), ppc 7, lifeTimeline 1969–2026, grounds 3, ministries 6, faqs 6, events 6, giving 8, serveRoles 4, devotions 6, images 11 all-local. `vite.config.ts test { globals, jsdom, setupFiles, include, exclude }` keeps `e2e/**` out. |
| `playwright` E2E (`pnpm test:e2e`) | **51 tests — green** | 8 specs `smoke 11 + navigation 8 + ministries 4 + give-faq 4 + enhancements 7 + enhancements-round5 6 + enhancements-round7 8 + deep-links 3` (chromium) — Toa Payoh (Risen Christ) routes `/worship`/`/ministries`/`/serve`/`/give` + `#mass`/`#liturgical` etc. + `SafeImage` fallback via `route.abort` + mobile drawer same-route close regression + rise-in hero entrance + event chips + back-to-top + aria-current nav states + Round-2 audit (CTA-band cream, head completeness, page-in, progress rail/ring, drawer aria-current) + Round-4 (mobile drawer modal: dialog + `aria-modal` + trapped focus + Escape focus restore; scroll-rail deterministic mid-depth landing) + Round-5 (Worship today-Mass card via `utils/massDay` + Sunday gold-dot list, gold category chips + display-serif dates, Give closing band h2 cream, sticky History story `lg:sticky`, gradient timeline rail, `.img-zoom` grounds/ministries drift, `.bg-gold-bloom` dark bands, Button aria-hidden icon nudge, About ghost numerals + monogram discs, NotFound ghost emblem + rise-in) + Round-7 "Honest Light" (print-media reveal override + IO try/catch fallback + early-entry `rootMargin`, Worship sticky mercy column, News bulletin + FAQ office closure bands, Give featured PayNow card, Ministries scrollspy via `hooks/useScrollSpy`, About PPC hover tint + `link-underline` priest contacts, desktop nav `after:` gold hairline (scale-x 0→100), `card-tint` info-card honesty system, PageHero atmosphere 35→45) + Round-12 audit (path-style deep links `/worship`/`/news-events`/`/donate` land on their pages, not Home). |
| `lint` / `typecheck` / `build` | Green on fresh clones | `eslint 9.39.5` flat `--max-warnings 0`, `tsc --noEmit` strict, `viteSingleFile` → `dist/index.html` (397.52 kB, JS+CSS inlined) + `dist/_headers` + `dist/favicon.svg` + `dist/images/` 8 files |

---

## 3. Bootstrapping & Configuration

### 3.1 From Zero to Running

```bash
git clone <repo-url> risen-christ-church && cd risen-christ-church
pnpm install --frozen-lockfile  # deterministic — versions pinned exact (pnpm 11.0.0)
# npm users: `npm ci --legacy-peer-deps` (typescript-eslint 8.28.0 peer predates TS 5.9)
pnpm dev                # → http://localhost:5173 (Vite HMR)
pnpm lint               # → eslint 9.39.5 flat — must be clean (--max-warnings 0)
pnpm typecheck          # → tsc --noEmit — must be silent
pnpm test               # → vitest 3.2.6 jsdom — 35 files / 202 tests green (ci-workflow 4 + repo-hygiene 3 + docs-contract 16 + cn 5 + nav 7 + content 10 + site 8 + massDay 5 + monogram 7 + deepLinks 7 + Button 11 + SkipLink 3 + Accordion 6 + SafeImage 6 + Header 17 + BackToTop 7 + Reveal 2 + wcag-contrast 5 + Ministries 3 + cta-bands 6 + worship-mass 6 + about-visuals 4 + event-chips 3 + give-featured 2 + give-uen 3 + card-affordances 6 + Timeline 3 + NotFound 2 + History 2 + Layout 2 + useScrollProgress 4 + useScrollSpy 6 + ScrollProgress 2 + head 13 + security-headers 6)
pnpm test:e2e           # → playwright 1.55.1 chromium — 51 tests (smoke 11 + navigation 8 + ministries 4 + give-faq 4 + enhancements 7 + enhancements-round5 6 + enhancements-round7 8 + deep-links 3) green
pnpm test:e2e:built     # → playwright vs built artifact (playwright.built.config.ts — vite preview :4173; E2E_BASE_URL → live host, webServer skipped) — same 51 tests green
pnpm build              # → dist/index.html + dist/images/ (viteSingleFile 2.3.3 inlines JS+CSS; publicDir copied)
pnpm preview            # → http://localhost:4173 (preview dist)
```

**Pre-push gate — all five must be green:**

```bash
pnpm lint && pnpm typecheck && pnpm test && pnpm test:e2e && pnpm build
```

### 3.2 Critical Config Files

| File | Purpose | Gotcha |
|---|---|---|
| `vite.config.ts` | `plugins: [react(), tailwindcss(), viteSingleFile()]` + `resolve.alias["@"]` + `test { globals, jsdom, setupFiles: src/test/setup.ts, include: src/**/*.{test,spec}.{ts,tsx}, exclude: e2e/** }` + `server.watch.ignored [skills/**, dist/**, playwright-report/**, test-results/**, coverage/**, src.orig/**]` | `test` keeps `e2e/**` out of unit runs; `server.watch.ignored` prevents `ENOSPC` from vendored `skills/` tree (large `.venv`). `@` must stay in sync (`vite.config.ts` ↔ `tsconfig.json` `paths`). |
| `tsconfig.json` | `ES2020`/`ESNext`/`bundler`/`react-jsx`/`strict`/`noUnused*`/`isolatedModules`/`noEmit` + `include ["src","vite.config.ts","eslint.config.js","playwright.config.ts","playwright.built.config.ts"]` + `types ["node","vitest/globals"]` + `paths {"@/*":["src/*"]}` + `baseUrl:"."` | `include` covers `src` + all config files (so `eslint.config.js` + `playwright.config.ts` + `playwright.built.config.ts` are type-checked). `types [vitest/globals]` required for `describe/it/expect` globals. Adding a file outside `src/` requires expanding `include`. |
| `eslint.config.js` | flat config (`eslint 9.39.5` + `@eslint/js 9.39.5` + `typescript-eslint 8.28.0` + `react-hooks 5.2.0` + `react-refresh 0.4.19` + `globals 16.1.0`) — ignores `dist/node_modules/coverage/playwright-report/test-results` **and `skills` and `src.orig`** | Flat. `pnpm lint:fix` → `eslint . --fix`. Ignoring `skills` + `src.orig` is what keeps the gate green. Never re-add `src.orig/` to lint/tsc. |
| `playwright.config.ts` | `playwright 1.55.1` (`@playwright/test 1.55.1` chromium, `webServer` → `pnpm exec vite --port 5173 --host 127.0.0.1 --strictPort`) | `testDir: e2e`, `baseURL: http://localhost:5173`, `reuseExistingServer: !CI`, `expect.timeout: 15s`, `trace/video on failure`. **Green** — 51 tests: `smoke 11 + navigation 8 + ministries 4 + give-faq 4 + enhancements 7 + enhancements-round5 6 + enhancements-round7 8 + deep-links 3`. |
| `playwright.built.config.ts` | Extends the base config — `baseURL = E2E_BASE_URL ?? http://127.0.0.1:4173`; `webServer: pnpm exec vite preview --port 4173` (skipped when `E2E_BASE_URL` is set) | Built-artifact pass (`pnpm test:e2e:built`): runs the same 51 tests against `dist/` via `vite preview`, or against the live host via `E2E_BASE_URL`. Exists because the singlefile pipeline rewrites root-relative asset refs (`/favicon.svg` → `./favicon.svg`) — dev-only assertions pass on `pnpm dev` and fail on the built artifact (round-9 E2E-L1). |
| `e2e/` | 51 tests — `smoke.spec.ts` (11), `navigation.spec.ts` (8), `ministries.spec.ts` (4), `give-faq.spec.ts` (4), `enhancements.spec.ts` (7), `enhancements-round5.spec.ts` (6), `enhancements-round7.spec.ts` (8), `deep-links.spec.ts` (3) + `helpers.ts` | **green** — Worship/Ministries anchors + aliases + `SafeImage` fallback + drawer same-route close regression + rise-in entrance + event chips + back-to-top + aria-current nav + Round-2 audit (CTA-band cream h2, head completeness, page-in keyed wrapper, scroll-progress rail/ring, drawer aria-current) + Round-4 (modal drawer dialog/aria-modal/trapped focus + Escape restore; scroll-rail mid-depth landing) + Round-5 (today Mass card matches run date, Give band h2 cream, sticky story at 1440px, img-zoom matrix on hover, gradient rail, 404 emblem) + Round-7 (print reveal, sticky mercy column, cream/gold band colors, scrollspy pill, nav hairline scale, home event links, FAQ loop-back) |
| `.github/workflows/ci.yml` | CI: lint → typecheck → test → test:e2e (chromium) → build + artifacts | `pnpm 11`, `node 24`. All five green — `dist/` + `playwright-report/` artifacts. |
| `src/index.css` | `@import "tailwindcss"` + `@theme` (25 colors + 2 shadows) + `@layer base/utilities` (27 utilities incl. `hero-ken-burns`, `gold-rule`/`gold-rule-left`, `reveal`/`reveal-visible`, `rise-in`+`rise-in-d1..d4`, `menu-in`, `drawer-in`, `drawer-item-in`, `page-in`, `dot-pulse`, `card-lift`, `card-tint`, `link-underline`, `skip-link`, `mask-fade-b`, `img-zoom`, `bg-gold-bloom` + 8 keyframes `gold-rule-draw`/`hero-ken-burns`/`rise-in`/`menu-in`/`drawer-in`/`drawer-item-in`/`page-in`/`halo-pulse` + themed scrollbar in `@layer base`) | Only token source; no `tailwind.config.*` exists. |
| `index.html` | `lang en`, `viewport`, `meta description`, scoped `Content-Security-Policy` meta + `referrer` meta, `/favicon.svg` link + `theme-color #200a0a`, full OG (`og:url`/`og:site_name`/`og:locale`/`og:image`+`og:image:alt`) + `twitter:card summary_large_image` + Church JSON-LD (drift-checked by `src/head.test.ts`), preconnect `fonts.googleapis.com`, `Fraunces`+`Source Sans 3`, `#root` + `src/main.tsx` | CSP allows inline script/style (singlefile), Google Fonts, `img-src 'self' data: blob:` (all images local — no wikimedia/pexels allowlist), `frame-src https://www.google.com` (maps embed). Social share + search-engine identity for Church of the Risen Christ (www.risenchrist.org.sg, Easter Sunday). |
| `.gitignore` | Ignores `node_modules/`, `.next/`, `dist/`, `skills/`, `src.orig/`, `docs/ssh-key.txt`, `package-lock.json` + `nohup.out`, `.venv`, `bak.git/` | `skills/` is committed vendored reference (catalog re-added in `0be0fe8`) — the ignore entry is inert for tracked files, tooling ignores apply instead. Package-lock.json untracked since round 3. `docs/ssh-key.txt` was tracked in `0be0fe8` and untracked in round 6 (C1) — ignore entry now effective for it; rotate the key. `src.orig/` was still tracked despite this entry (round-12 F-9 found 64 files; pruned 2026-08-31 — the ignore entry is effective now). |

**Env vars:** None. `VITE_*` prefix convention applies if added; guard with `src/env.d.ts` (`import.meta.env`). Document new vars in `README.md` + `CLAUDE.md` + this §.

---

## 4. The Design System (Code-First)

**Single source:** `src/index.css` `@theme` block. No `tailwind.config.*`. Tokens are **unchanged from the rothershrine → St Joseph BT → St Mary line** — only the imagery and copy they frame is now Toa Payoh: the 1971 first air-con nave, the Adoration Room, the parish hall & media centre — still warm parchment/maroon/gold on cream.

### 4.1 Tokens (`@theme`)

```css
@theme {
  --font-display: "Fraunces", "Iowan Old Style", serif;
  --font-sans: "Source Sans 3", system-ui, sans-serif;
  --font-body: var(--font-sans); /* alias */

  --color-shrine-cream: #faf6ec;
  --color-shrine-parchment: #f2e9d6;
  --color-shrine-parchment-dark: #e7d9b8;
  --color-shrine-stone: #dccfae;
  --color-shrine-ink: #2a2115;
  --color-shrine-charcoal: #423a2c;

  --color-shrine-maroon-50: #fbf0ee;
  --color-shrine-maroon-100: #f3d9d4;
  --color-shrine-maroon-500: #7c2a25;
  --color-shrine-maroon-600: #691f1e;
  --color-shrine-maroon-700: #55191a;
  --color-shrine-maroon-800: #431315;
  --color-shrine-maroon-900: #33100f;
  --color-shrine-maroon-950: #200a0a;

  --color-shrine-gold-100: #f8ecd2;
  --color-shrine-gold-300: #e2bf72;
  --color-shrine-gold-400: #d1a955;
  --color-shrine-gold-500: #c3963f;
  --color-shrine-gold-600: #a67a2e;

  --color-shrine-pine-500: #335840;
  --color-shrine-pine-600: #26402f;
  --color-shrine-pine-700: #1c3123;

  --color-shrine-terracotta-400: #c17a53;
  --color-shrine-terracotta-500: #ab5f3c;
  --color-shrine-terracotta-600: #8f4c30; /* round-12 (audit F-1): AA text step, 5.36:1 on parchment */

  --shadow-shrine: 0 20px 60px -20px rgba(51, 16, 15, 0.45);
  --shadow-shrine-lg: 0 40px 90px -30px rgba(51, 16, 15, 0.55);
}
```

### 4.2 Typography

| Role | Font | Weights | Tracking | Class / Usage |
|---|---|---|---|---|
| Display / Quote | `Fraunces` | 400/500/600/700/800 + italic 500/600 | `tracking-tight` / `[0.25–0.35em]` on eyebrow | `font-display`, `h1–h4` (`@layer base`), hero title |
| Body | `Source Sans 3` | 400/500/600/700 | `tracking-wide` / `[0.3em]` on eyebrow | `font-sans` (alias `font-body`) on `body`, all `p`/`li` |
| Eyebrow (light) | — | 600 | `[0.25–0.35em]` | `text-shrine-gold-300 text-xs uppercase` |
| Eyebrow (dark) | — | 600 | `[0.25em]` | `text-shrine-maroon-500` |

### 4.3 Custom Utilities (`@layer utilities`)

| Name | CSS | Purpose |
|---|---|---|
| `.text-balance` | `text-wrap: balance` | Hero + heading line-wrap |
| `.bg-adobe-texture` | double radial gradient (white 0.06 + black 0.08) | Subtle adobe wash on dark bands |
| `.bg-grain` | `data:image/svg+xml` turbulence (`opacity 0.035`) | Grain overlay for hero/dark bands |
| `.divider-weave` | `repeating-linear-gradient(45deg, gold-500 0 6px, maroon-600 6 12px, pine-600 12 18px)` | `Footer` 6px weave strip + pilgrim bands |
| `.divider-weave-thin` | `repeating-linear-gradient(90deg, gold 0 10px, maroon 10 20, pine 20 30)` height 3px | Thin weave (hero bottom, footer top) |
| `.gold-rule` | `linear-gradient(90deg, transparent, gold-500 18%, gold-300 50%, gold-500 82%, transparent)` height 1px + `gold-rule-draw` 0.9s | Centered gold rule (section dividers) |
| `.gold-rule-left` | `linear-gradient(90deg, gold-500, transparent)` height 1px + `gold-rule-draw` 0.9s | Left-aligned gold rule (eyebrow / `SectionHeading` line) |
| `.hero-ken-burns` | `scale(1)→1.05` 20s ease-out `hero-ken-burns` | Hero image slow zoom |
| `.mask-fade-b` | `linear-gradient(to bottom, black 70%, transparent)` | Mask for image fades |
| `.reveal` / `.reveal-visible` | `translateY(24px)→0`, `opacity 0→1`, `0.7s cubic-bezier(0.22,1,0.36,1)` + `prefers-reduced-motion` kill | Scroll-reveal via `Reveal.tsx` + `IntersectionObserver` |
| `.rise-in` (+ `.rise-in-d1..d4`) | `rise-in` keyframe: `translateY(20px)→0`, `opacity 0→1`, `0.7s ease-out`, fill `both`; delay steps 90/180/280/380ms | Staged entrance for Home hero + PageHero content (eyebrow→title→copy→CTA) |
| `.menu-in` | `menu-in` keyframe: `translateY(-4px)→0`, `opacity 0→1`, `0.18s ease-out` | Desktop dropdown `<ul>` entrance (runs on conditional mount) |
| `.drawer-in` | `drawer-in` keyframe: `translateY(-12px)→0`, `opacity 0→1`, `0.24s ease-out` | Mobile drawer entrance (runs on conditional mount) |
| `.dot-pulse` | `::after` gold ring `halo-pulse` 2.6s infinite (scale 0.6→1.7 + fade); reduced-motion → `opacity:0` | Timeline dot halo |
| `.card-lift` | hover `translateY(-4px)` + `shadow-shrine` + gold border tint, 300ms ease-out | Uniform card hover (grounds/devotions/pillars/roles/giving/events) |
| `.link-underline` | `::after` gold gradient underline, `scaleX(0)→1` 300ms on hover/focus | Footer nav, top-bar Give link, WhatsApp links |
| `.skip-link` | `fixed z-[100] -translate-y-24 → focus:translate-y-0` | Skip-to-content link (`SkipLink.tsx` + `Layout.tsx`) |

Plus keyframes `gold-rule-draw` (scaleX 0→1), `hero-ken-burns`, `rise-in`, `menu-in`, `drawer-in`, `halo-pulse` — all killed/instant under `prefers-reduced-motion` (global 0.01ms override in `@layer base` + `.dot-pulse::after` opacity 0).

**Accordion collapse contract:** panels animate via `grid-template-rows 0fr↔1fr` (`grid grid-rows-[0fr|1fr]` + inner `overflow-hidden`) — never `hidden`. Closed panels carry `aria-hidden="true"` + `inert`; `aria-expanded` on the button stays the single source of truth (see `docs/ui-ux-remediation-plan-2026-08-28.md`).

### 4.4 Shadows & Radii

- Shadows: `shadow-shrine` (default) + `shadow-shrine-lg` (elevated cards/dropdowns). Radii are `rounded-sm` (buttons/cards) and `rounded-full` (emblem icon). Don't introduce `shadow-lg`/`rounded-xl` without a rationale.

**Verification:** `grep --color shrine- src/index.css` → 25 colors + 2 shadows (27 theme entries); copy-paste `@theme` into this doc to prevent drift.

---

## 5. Component Architecture & Patterns

### 5.1 Layer Map (SPA — no 5-layer BE model needed)

```
index.html (#root) → src/main.tsx (StrictMode+createRoot + #root guard)
  → src/App.tsx (HashRouter + Routes + Layout outlet)
    → Layout (Header / Outlet / Footer) + scroll/hash restore
      → Pages (10) → ui/* primitives → utils/cn
      → data/* (nav + content + site) — single-source, typed
```

No global store, no API layer, no `server/` — add only with an ADR.

### 5.2 Directory Inventory (77 files in `src/` — 41 source + 35 tests + 1 setup)

```
src/ (77 files — 41 source + 35 tests + 1 setup)
  App.tsx                 # HashRouter + 17 Route entries (16 content paths + * NotFound; 5 alias groups, 7 alias paths)
  main.tsx                # StrictMode + createRoot + explicit #root guard + resolveHashRedirect pre-mount rewrite (round-12 F-3: path-style deep links land on their page)
  index.css               # @theme (25 colors + 2 shadows) + @layer base/utilities (27 utilities + 8 keyframes + themed scrollbar)
  components/
    Layout.tsx            # Outlet + hash-aware scroll restoration (double-hash aware, 80ms, timeout cleanup) + ScrollProgress (decoupled rail z-[60]) + SkipLink + BackToTop + keyed page-in container
    Header.tsx            # z-50 fixed maroon-950 bar (solid = scrolled||!isHome||mobileOpen; translucent+blur when solid, transparent at top of Home), useScrolled(16) (default 12), hover/focus-open dropdown (no click-toggle — keyboard via onFocusCapture), mobile modal drawer (round-4 L-5: role=dialog + aria-modal + initial focus + Tab/Shift+Tab focus trap + focus restore to hamburger + outside-tap close; Escape handler, parentActive, 44px hamburger, menu-in/drawer-in)
    Footer.tsx            # 4-col + divider-weave-thin + 4 SocialIcons (Facebook/Instagram/YouTube/Telegram) + site.ts address/flows
    PageHero.tsx          # maroon-950 hero (compact?, bg-grain, dual gradients, divider-weave-thin; image alt="" only)
    SafeImage.tsx         # local fallback (fallback=/images/hero-church.jpg, lazy, fetchPriority?, onError→dataset.fallback guard) — all current images local; CDN keys naveCdn/courtyardCdn now local fallbacks; legacy CSP allowlist retained
    Emblem.tsx            # inline SVG emblem (crook + wheat, currentColor)
    SkipLink.tsx          # skip-to-#main-content link; preventDefault + imperative focus — never rewrites the hash (HashRouter)
    SocialIcons.tsx       # hand-drawn Facebook/Instagram/YouTube/Telegram glyphs (4)
    BackToTop.tsx         # threshold 480 + SVG progress ring (stroke-dashoffset via useScrollProgress) + reduced-motion, hash-safe
    ScrollProgress.tsx    # fixed gold rail (h-[3px], scaleX progress, aria-hidden, z-[60]) — decoupled from Header, rendered by Layout
    Timeline.tsx          # gradient rail ([data-testid=timeline-rail], fades at both ends) + display-serif gold years + Reveal per entry + dot-pulse halos — fed 1969–2026 Toa Payoh milestones (Ho Ping Centre → first air-con → Grateful/Faithful/Sent)
    ui/
      Button.tsx          # discriminated union (to/href/button) + icon, 4 variants
      Container.tsx       # max-w-7xl mx-auto px-5 sm:px-8
      SectionHeading.tsx  # eyebrow? / title / description + align/light + line (gold-rule-left)
      Accordion.tsx       # FAQ accordion (aria-expanded, grid-rows animation, Plus rotate-45)
      Reveal.tsx          # IntersectionObserver fade+slide (threshold 0.15, fallback visible, prefers-reduced-motion)
  hooks/
    useScrolled.ts        # scrollY > threshold boolean (threshold=12 default; Header passes 16)
    useScrollProgress.ts  # 0..1 scroll progress, rAF-throttled, unscrollable guard
  pages/                  # Home, About, History, Worship, Ministries, NewsEvents, Serve, Give, FAQ, NotFound (10 pages, all named exports)
  data/
    nav.ts                # primaryNav (6 + description on children) / footerNav (10)
    content.ts            # 8 interfaces + 10 exports (~476 lines) + images export (11 keys, 3 CDN)
    site.ts               # site as const — name/shortName/chineseName/tagline/vision + address + hours(5) + mass(7) + contact + transport + feast + uen/chequePayee/facebook/archdiocese/mapsUrl/mapsEmbedSrc — single source
  utils/
    cn.ts                 # twMerge(clsx) + cn helper
    massDay.ts            # massDayKey(date): 'weekdays'|'saturday'|'sunday' — single source for the Worship today-highlight
  test/
    setup.ts              # vitest jsdom setup (jest-dom + IntersectionObserver mock + scrollTo/scrollIntoView stubs)
  **/*.test.{ts,tsx}      # 35 files / 202 tests: ci-workflow (4), repo-hygiene (3), docs-contract (16), utils/cn (5), data/nav (7), data/content (10), data/site (8), utils/massDay (5), utils/monogram (7), utils/deepLinks (7), ui/Button (11), SkipLink (3), ui/Accordion (6), SafeImage (6), Header (17), BackToTop (7), ui/Reveal (2), components/wcag-contrast (5), pages/Ministries (3), pages/cta-bands (6), pages/worship-mass (6), pages/about-visuals (4), pages/event-chips (3), pages/give-featured (2), pages/give-uen (3), pages/card-affordances (6), components/Timeline (3), pages/NotFound (2), pages/History (2), Layout (2), hooks/useScrollProgress (4), hooks/useScrollSpy (6), ScrollProgress (2), head (13), security-headers (6)
```

**Counts:** `find src -type f | wc -l` → 77 (41 source + 35 tests + 1 setup); `public/images/` → 8 files (`hero-church.jpg`, `chapel-interior.jpg`, `sanctuary.jpg`, `rosary-garden.jpg`, `stained-glass.jpg`, `parish-hall.jpg`, `cemetery.jpg`, `feast.jpg`) → `dist/images/` on build (not inlined) + `public/favicon.svg`. Tests cover ScrollProgress/useScrollProgress/BackToTop/cta-bands/head etc.

### 5.3 Client vs Server

**All components are client components.** No RSC, no `use server`. SPA mental model: React 19 hooks (`useState`/`useEffect`/`useLocation`) only; no `createServerFn`.

### 5.4 Routing Contract (`src/App.tsx`)

**17 `Route` entries = 16 content paths + `*` NotFound, covering 10 page components, with 7 alias paths in 5 groups and hash anchors on two pages.**

```tsx
// src/App.tsx — 17 entries (16 paths + *)
// HashRouter is intentional: static GH Pages/S3 with no SPA fallback.
import { HashRouter, Route, Routes } from "react-router-dom";
import { Layout } from "@/components/Layout";
import { Home } from "@/pages/Home";
import { About } from "@/pages/About";
import { History } from "@/pages/History";
import { Worship } from "@/pages/Worship";
import { Ministries } from "@/pages/Ministries";
import { NewsEvents } from "@/pages/NewsEvents";
import { Serve } from "@/pages/Serve";
import { Give } from "@/pages/Give";
import { FAQ } from "@/pages/FAQ";
import { NotFound } from "@/pages/NotFound";

export default function App() {
  return (
    <HashRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Home />} />                          {/* / */}
          <Route path="/about" element={<About />} />                 {/* canonical — orig was /about-blessed-stanley-rother */}
          <Route path="/history" element={<History />} />
          <Route path="/worship" element={<Worship />} />             {/* canonical for 3 aliases */}
          <Route path="/mass-times" element={<Worship />} />          {/* aliasOf /worship */}
          <Route path="/hours-location" element={<Worship />} />      {/* aliasOf /worship (was Pilgrimage in orig) */}
          <Route path="/visit" element={<Worship />} />               {/* aliasOf /worship (was Pilgrimage in orig) */}
          <Route path="/ministries" element={<Ministries />} />       {/* canonical for 1 alias — replaces /what-to-see */}
          <Route path="/ministry" element={<Ministries />} />         {/* aliasOf /ministries */}
          <Route path="/news-events" element={<NewsEvents />} />      {/* canonical for 1 alias */}
          <Route path="/news-and-events" element={<NewsEvents />} />  {/* aliasOf /news-events */}
          <Route path="/serve" element={<Serve />} />                 {/* canonical for 1 alias — replaces /volunteer alone */}
          <Route path="/volunteer" element={<Serve />} />             {/* aliasOf /serve */}
          <Route path="/give" element={<Give />} />                   {/* canonical for 1 alias */}
          <Route path="/donate" element={<Give />} />                 {/* aliasOf /give (was /shrinegift in orig) */}
          <Route path="/faq" element={<FAQ />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </HashRouter>
  );
}
```

**Alias groups (5):**

| Canonical | Aliases | Origin |
|---|---|---|
| `/worship` | `/mass-times`, `/hours-location`, `/visit` | `/mass-times` is new; `/hours-location`+`/visit` moved from `Pilgrimage` (orig) |
| `/ministries` | `/ministry` | Replaces `/what-to-see` + `/grounds-art-architecture` (orig) |
| `/news-events` | `/news-and-events` | Unchanged |
| `/serve` | `/volunteer` | `/serve` is new canonical; orig had `/volunteer` alone |
| `/give` | `/donate` | Replaces `/shrinegift` (orig) |

**Canonical flip:** `/about` is now canonical (orig: `/about-blessed-stanley-rother` canonical, `/about` was the alias).

**Hash anchors:**

| Route | IDs | Nav wiring | Notes |
|---|---|---|---|
| `/worship` | `#mass`, `#confession`, `#visit` | `primaryNav → /worship#mass` / `#confession` / `#visit` + `footerNav → /worship#mass` | 3 sections: Mass schedule (three `MassCard`s — Clock/MoonStar/Sun icons; the card matching `massDayKey(new Date())` carries `data-today="true"` + gold top rule + "Today" chip; Sunday slots are a gold-dot hover list), Confession & Adoration, Find Us (map). Each `section id="…"` has `scroll-mt-28`. |
| `/ministries` | `#liturgical`, `#faith-formation`, `#pastoral-care`, `#family-life`, `#youth`, `#language-communities` | `primaryNav → 3` of them; `footerNav → 3`; **Ministries jump nav** `ministries.map → <Link to="/ministries#<id>">` (6 pills, `aria-label="Jump to ministry"`, alternating `bg-shrine-cream`/`bg-shrine-parchment`) | Must use `<Link to="/ministries#id">`, never `<a href="#id">` — plain href would replace the HashRouter hash and route to NotFound. |
| `/serve` | *(none)* | No section ids — `serveRoles`/`devotions` rendered without anchors | |
| *(orig)* | ~~`#pilgrim-center`/`#shrine-church`/`#tepeyac-hill`~~ | Gone — predecessor `WhatToSee` anchors removed | See Appendix D |

**Rule:** When adding a route, add its alias if external parish/school links or printed material expects it. Keep `Layout.tsx` hash logic intact — it resolves the anchor from `useLocation().hash` or the double-hash `window.location.hash`, then `getElementById` + `scrollIntoView({smooth})` (80ms) with fallback `window.scrollTo(0,0)`.

### 5.5 Component Conventions

| Primitive | File | API | Rule |
|---|---|---|---|
| `Button` | `src/components/ui/Button.tsx` | discriminated `to` (Link) / `href` (a) / native `button` + `variant`, `icon?`, `className?` | `to`→`<Link>`, `href`→`<a>`, else `<button>`; `variantClasses` + `cn()` + focus ring |
| `Container` | `src/components/ui/Container.tsx` | `children, className?` | All sections wrap in `<Container>` |
| `SectionHeading` | `src/components/ui/SectionHeading.tsx` | `eyebrow?, title, description?, align?, light?` | Eyebrow renders `gold-rule-left` line + gold/maroon; light = gold/cream on dark |
| `PageHero` | `src/components/PageHero.tsx` | `eyebrow, title, description?, image, children?, compact?` | `compact` shrinks padding; `bg-grain` + dual gradients; `alt=""` |
| `SafeImage` | `src/components/SafeImage.tsx` | `src, fallback?, alt, className?, loading?, fetchPriority?` (`fallback` default `/images/hero-church.jpg`, `loading` default `lazy`, `fetchPriority` optional `"high"` on heroes) | Wraps `<img>` with `onError→dataset.fallback` guard to swap `src` once; always via `cn()`. All current `images.*` are local (naveCdn/courtyardCdn point to local); legacy allowlist `upload.wikimedia.org`/`images.pexels.com` retained for any future external image; don't use bare `<img>` for CDN sources. |
| `Header` | `src/components/Header.tsx` | `useScrolled(16)` (default 12) + `mobileOpen`, `openDesktopMenu` + Escape handler | Fixed maroon-950 bar (`maroon-950/92` + blur when solid; `solid = scrolled||!isHome||mobileOpen`); `aria-haspopup`/`aria-expanded` on dropdown trigger + `aria-current` states (plain "page", parent "true"), close on `pathname`+`hash` change + onClickCapture in drawer/dropdown; **mobile drawer is a modal dialog (round-4 L-5): `role="dialog"` + `aria-modal="true"` + `aria-label="Site menu"`, panel focused on open, `Tab`/`Shift+Tab` trapped (`handleDrawerKeyDown`), focus restored to the hamburger on every close path, outside `pointerdown` closes**; hamburger 44px (h-11 w-11); threshold 16 delays transparent→solid on Home (intentional) |
| `Reveal` | `src/components/ui/Reveal.tsx` | `children, delay?, as?: "div"│"li", className?` | `IntersectionObserver` 0.15 threshold; falls back visible if unsupported; respects `prefers-reduced-motion` |
| `Accordion` | `src/components/ui/Accordion.tsx` | `items: {question,answer}[]` | Single-open, `grid-rows` animation, `Plus rotate-45` — used by `FAQ.tsx` for `faqs[6]` |
| `BackToTop` | `src/components/BackToTop.tsx` | threshold 480 + SVG ring + reduced-motion | Appears when scrollY>480, hides below (aria-hidden+tabIndex -1), progress ring via `useScrollProgress` (`data-testid="back-to-top"` + `data-progress`); hash-safe (window.scrollTo only) |
| `ScrollProgress` | `src/components/ScrollProgress.tsx` | `useScrollProgress` 0..1 | Fixed `h-[3px]` rail (`data-testid="scroll-progress"`, `aria-hidden`, `scaleX(progress)`) at z-[60], rendered by Layout — decoupled from Header |
| `Emblem` / `SkipLink` / `Timeline` | `src/components/*` | see files | `Emblem` is inline SVG; `SkipLink` targets `#main-content` via preventDefault + imperative focus (never rewrites the hash); `Timeline` is a drawn gradient rail (`[data-testid="timeline-rail"]`, fades at both ends — no `border-l`) with display-serif gold years + Reveal per entry + dot-pulse halos — now shows 1969–2026 Toa Payoh milestones |
| `cn` | `src/utils/cn.ts` | `cn(...ClassValue[])` | Only merge path — `twMerge(clsx(...))` |

---

## 6. Custom Hooks Deep Dive

**Status: Two hooks — `useScrolled` + `useScrollProgress` (decoupled, shared by Header/ScrollProgress/BackToTop).**

Extracted from `Header.tsx` into `src/hooks/useScrolled.ts` so `Header` stays declarative. Before the elevation there were zero hooks; this is the first `src/hooks/` file.

**Contract:**

```ts
// src/hooks/useScrolled.ts (and useScrollProgress.ts)
// useScrollProgress: rAF-throttled 0..1 (Layout/BackToTop share it)

import { useEffect, useState } from "react";
export function useScrolled(threshold = 12) {
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > threshold);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, [threshold]);
  return scrolled;
}
```

- `Header.tsx` calls `useScrolled(16)` — the 16 vs default-12 mismatch is intentional (delays transparent→solid on Home). Don't "fix" it.
- `useScrollProgress` returns 0..1 scroll progress, rAF-throttled, with an unscrollable guard (returns 0 when document height ≤ viewport). Used by `ScrollProgress` (gold rail) and `BackToTop` (ring). Never touches the hash.
- SSR-safe by construction (`window` only inside `useEffect`).

**When you add one:**

- Location: `src/hooks/useThing.ts` (`camelCase`, `use` prefix).
- Must be SSR-safe even in an SPA (guard `window` access): `useEffect` for scroll/listeners, `useState` initial `false`.
- Cleanup: return a remover in `useEffect` (e.g., `removeEventListener`, `clearTimeout`).

---

## 7. Content Management & Data Ingestion

**No CMS, no RSS, no API.** Pure file-backed content — the simplest thing that works. `src/data/content.ts` is the data layer; `src/data/site.ts` is the canonical fact single-source; `src/data/nav.ts` is the navigation single-source. Pages render from data — don't inline copy.

### 7.1 Data Files — Complete Inventory

| File | Exports | Count / Shape | Consumer |
|---|---|---|---|
| `src/data/content.ts` | `lifeTimeline: TimelineEntry[]` | **8** — `1969–2026` Toa Payoh (Ho Ping Centre 1969 → 1971 first air-con $450k → many tongues + Velankanni 1970s → four-storey 2003 → Simbang Gabi 2010s → Golden Jubilee 2021 → Fr Brian 2023 → Grateful/Faithful/Sent 2026) (see §7.2) | `History.tsx`, `About.tsx`, `Timeline.tsx` |
|  | `grounds: GroundsPlace[]` | **3** — `main-church`, `chapel`, `parish-hall` (Main Church / Adoration Room / Parish Hall & Media Centre; + `image`/`imageFallback`/`imageAlt` — all local; `image` and fallbacks point to `/images/*`) | `Home.tsx` (grounds preview) |
|  | `ministries: Ministry[]` | **6** — `liturgical`, `faith-formation`, `pastoral-care`, `family-life`, `youth`, `language-communities` (Mandarin Sun 8.15, Tamil 2nd Sun 19.00, Tagalog 4th Sun 15.00, Bahasa 1st Fri 20.00) (each + `image`/`imageFallback`/`imageAlt` — all local) | `Ministries.tsx` (jump nav + 6 alternating sections) |
|  | `faqs: FaqItem[]` | **6** — Mass times, confession (approach a priest / parish office), how to get there (MRT Toa Payoh NS19 + buses), parking (HDB blks 66/70/73), baptism/marriage/Mass intention, Adoration Room | `FAQ.tsx` (`Accordion`) |
|  | `upcomingEvents: EventItem[]` | **6** — `title`+`date`+`summary`+`category` + optional `href` (categories `Parish`\|`Devotion`\|`Formation`\|`Archdiocese`) — 54th Velankanni 10–12 Sep, CEP 16 Aug–11 Oct (cep-sg.org), F.R.E.E. Acts 30 Jun–10 Nov (free.risenchrist.org.sg), Sunday Reflections, RCIA, Intercessory Prayer | `NewsEvents.tsx`, `Home.tsx` |
|  | `givingOptions: GivingOption[]` | **8** — PayNow UEN T08CC4042G, weekend collections, cheque payable Church of the Risen Christ, cash at office, Mass offerings, General Church Offering, SSVP, Church Maintenance (icons `flame`/`church`/`sprout`/`hand-heart`/`book`/`heart`/`landmark`/`globe`) | `Give.tsx` |
|  | `priests: Priest[]` | **3** — Fr Brian D'Souza (Parish Priest), Fr Arun Bellarmin, Fr Dexter Chua (Assistant) — each with `email` + `phone` | `About.tsx` |
|  | `ppcMembers: PpcMember[]` | **7** — 3 priests + Secretariat Peter Quek / Parish Administrator Audrey Rozario / Youth Coordinator Calvin Swee / Pastoral Coordinator Cheryl-Anne Goh | `About.tsx` |
|  | `serveRoles` (untyped const) | **4** — Liturgical ministers, Catechists & facilitators, Pastoral care, Hospitality & media (each `title`+`summary`) | `Serve.tsx` |
|  | `devotions` (untyped const) | **6** — Adoration daily, Intercessory 2nd & 4th Thu 20.00, Velankanni Sep, Simbang Gabi Dec, Bahasa 1st Fri 20.00, Tamil & Tagalog 2nd/4th Sun | `Serve.tsx`, `Worship.tsx` |
|  | `images` (`as const`) | **11 keys — all local** — `hero`/`heroFallback` `/images/hero-church.jpg`, `chapel`/`sanctuary`/`garden`/`glass`/`hall`/`cemetery`/`feast` (all `/images/*`), `naveCdn`→`/images/sanctuary.jpg`, `courtyardCdn`→`/images/rosary-garden.jpg` (local aliases) | `Home.tsx`, `PageHero`, `SafeImage` fallbacks |
| `src/data/nav.ts` | `primaryNav: NavItem[]` | **6** — Home, About(3 children), Worship(3 children with hash), Ministries(3 children with hash), News & Events, Serve. Children carry `description`. | `Header.tsx` |
|  | `footerNav: NavLink[]` | **10** — The Parish, Mass Times, History, FAQ, Liturgical, Faith Formation, Pastoral Care, News & Events, Serve, Give | `Footer.tsx` |
| `src/data/site.ts` | `site: { as const }` | **1 canonical object** — `name`/`shortName`/`chineseName` 耶稣复活堂/`tagline`/`vision` + `address` 91 Toa Payoh Central / 319193 (`full`/`query` getters) + `hours` (6: `gates`/`mainChurch`/`chapel` Adoration Room Mon 12–22/Tue–Sat 7–22/Sun 7–18/`reception` Mon–Fri 9–16 Sat 9–12 Sun 8–13/`parishOffice` same/`mediaCentre` Tue & Fri 12–16 Sat 12–19 Sun 8–13 +65 6356 5958/`adorationRoom` same as chapel) + `mass` (`weekdayMorning` Mon–Fri 6.30a/`weekdayEvening` 6p/`saturday` 6.30a+5.30p anticipated/`sunday[5]` 7/8.15 Mandarin/9.45/11.30/5.30/`confession` approach a priest/`adoration` Adoration Room daily/`secondCollection` bulletin + `note` public holidays + `monthly` Bahasa 1st Fri 20.00 · Tamil 2nd Sun 19.00 · Tagalog 4th Sun 15.00) + `contact` (parishPriestPhone 6255 7509/officePhone 6253 2166/mediaPhone 6356 5958/email crc.secretariat/admin crc.admin/connect crc.pastoral/youth crc.youth/dpo dpo.crc) + `transport` (MRT Toa Payoh NS19 Exit A + buses 88/157/163 B52261) + `feast` The Risen Christ — Easter Sunday + `uen` T08CC4042G/`chequePayee` Church of the Risen Christ/`facebook`/`instagram`/`youtube`/`archdiocese`/`freeMinistry`/`ssvp`/`bulletin`/`cep`/`mapsUrl`/`mapsEmbedSrc` + `origin`/`url`/`ogImage` | `Footer.tsx`, `Worship.tsx`, `About.tsx` — single source; don't duplicate |

**Interfaces:** 8 exported (`TimelineEntry`, `GroundsPlace`, `Ministry`, `FaqItem`, `EventItem`, `GivingOption`, `Priest`, `PpcMember`) — see §20 for verbatim definitions.

### 7.2 Life Timeline — 8 Entries (1969–2026 — Toa Payoh)

| Year | Title | Parish moment |
|---|---|---|
| 1969 | Mass in a new town | Catholics gather at Ho Ping Centre, Block 82 Lorong 4, and at an HDB function hall; first Mass 6 April; tenders invited for the Toa Payoh Central / Lorong 4 plot |
| 1971 | A church rises | Blessed by Archbishop Michel Olçomendy on 3 July — first Catholic church in Toa Payoh and Singapore's first fully air-conditioned church (Fr Pierre Abrial, $450k) |
| 1970s | Many tongues | English, Mandarin, and Tamil Masses; the Velankanni devotion takes root with the parish community |
| 2003 | Room to grow | Four-storey wing adds classrooms, a youth room, and an auditorium for a growing new-town household |
| 2010s | A wider household | Filipino, Indonesian, and Myanmar communities join; Simbang Gabi; monthly Bahasa/Tamil/Tagalog Masses |
| 2021 | Golden Jubilee | Fifty years of the parish at the heart of Toa Payoh |
| 2023 | A new shepherd | Fr Brian D'Souza arrives as Parish Priest |
| 2026 | Grateful, Faithful, and Sent | The parish's triennial theme — 54th Velankanni feast, CEP, F.R.E.E. Acts |

*1969–2026 Toa Payoh arc — from Ho Ping Centre to the first air-con nave and a household of many tongues.*




### 7.3 Other Arrays at a Glance

**`grounds[3]`** — `main-church` (Main Church: the 1971 first air-con nave at Toa Payoh Central — English from dawn to evening, Mandarin at 8.15 a.m.), `chapel` (Adoration Room: quiet house of prayer beside the nave, no appointment needed), `parish-hall` (Parish Hall & Media Centre: 2003-wing classrooms, youth room, auditorium, and the Apostolate of Media — bulletin and Sunday reflections). Each has `image` + `imageFallback` + `imageAlt` (all local; `naveCdn`/`courtyardCdn` are local aliases).

**`ministries[6]`** — `liturgical` (altar servers, lectors, choirs, hospitality), `faith-formation` ( catechesis of the Good Shepherd, Sunday catechism, RCIA, adult formation), `pastoral-care` (SSVP visits, sick & homebound, bereavement), `family-life` (baptism preparation, marriage prep, family events), `youth` (youth gatherings, outreach, formation), `language-communities` (Mandarin Sun 8.15, Tamil 2nd Sun 19.00, Tagalog 4th Sun 15.00, Bahasa Indonesia 1st Fri 20.00). Each drives one alternating `bg-shrine-cream`/`bg-shrine-parchment` section in `Ministries.tsx`.

**`faqs[6]`** — Mass times (weekday 6.30a/6p, Sat 6.30a+5.30p, Sun 5 Masses incl. Mandarin 8.15), confession (approach a priest after Mass or the parish office), how to get there (91 Toa Payoh Central, MRT Toa Payoh NS19 Exit A, buses 88/157/163), parking (HDB blks 66/70/73 nearby), baptism/marriage/Mass intention (parish office 6253 2166), Adoration Room hours.

**`upcomingEvents[6]`** — `title`+`date`+`summary`+`category` + optional `href` (2 of 6 carry href: `cep-sg.org`, `free.risenchrist.org.sg`). Categories `Parish`/`Devotion`/`Formation`/`Archdiocese`. Examples: 54th Feast of Our Lady of Velankanni 10–12 Sep 2026 (Devotion), Couple Empowerment Programme 16 Aug–11 Oct (Parish), Acts: The Spread of the Kingdom 30 Jun–10 Nov (Formation), Sunday Reflections, RCIA, Intercessory Prayer.

**`givingOptions[8]`** — PayNow UEN T08CC4042G, weekend collections, Mass offerings, SSVP (poor & needy), cheque payable Church of the Risen Christ, cash at the parish office, General Church Offering, Church Maintenance Fund. No HRSM, no Tap & Give — the Risen Christ set replaces the St Mary line.

### 7.4 How to Add Content

**Add a timeline entry:**

1. Append to `lifeTimeline` in `src/data/content.ts` with `{ year, title, description }`.
2. Re-run `pnpm typecheck` (type gate).
3. No page change — `History.tsx` maps the array via `Timeline.tsx`.

**Add a ministry:**

1. Append to `ministries` with `{ id, title, summary, details[], image, imageFallback, imageAlt }` — `id` becomes the hash anchor (`/ministries#<id>`).
2. Verify `Ministries.tsx` jump nav (`ministries.map → <Link to="/ministries#id">`) picks it up automatically.
3. Run `pnpm typecheck && pnpm build`.

**Add a nav item:**

1. Append to `primaryNav` or `footerNav` in `src/data/nav.ts` (include `description` for dropdown children).
2. If routed, add `<Route path="…">` in `src/App.tsx` — include an alias if a legacy/external path expects it.
3. Verify `Header` hover dropdown + mobile drawer render the child.

**Why no `import.meta.glob`:** Vite glob is for file-system content collections (e.g., Astro). This is a typed-array SPA — direct export + import is simpler and fully type-checked. For a future CMS, isolate behind `src/lib/cms/` and keep `content.ts` as fallback.

---

## 8. Accessibility (WCAG AAA) Implementation

**Target:** WCAG AAA intent — this section documents the contract, not a certification claim. Verify with `axe-core` / Lighthouse a11y before claiming pass.

### 8.1 Contrast (body text)

| Foreground | Background | Ratio | Level |
|---|---|---|---|
| `shrine-ink #2a2115` | `shrine-cream #faf6ec` | ~13:1 | AAA |
| `shrine-charcoal #423a2c` | `shrine-cream` | ~10:1 | AAA |
| `shrine-cream #faf6ec` | `shrine-maroon-900 #33100f` | ~13:1 | AAA |
| `shrine-gold-300 #e2bf72` | `shrine-maroon-900` | ~7:1 | AAA |

Verify new pairings with a contrast checker before merging.

### 8.2 Focus & Navigation

- **Focus ring:** `focus-visible:outline` via Tailwind defaults; `src/index.css` `@layer base` sets `outline: 2px solid --color-shrine-gold-500` + `offset 3px` for `:focus-visible`. Preserve on `Button` and `Header` toggle. Do not remove outlines.
- **Header toggle:** `aria-label` toggles `Open menu`/`Close menu`, `aria-expanded` reflects `mobileOpen`. Keep both.
- **Dropdowns:** Hover-open (`onMouseEnter`/`onMouseLeave` on `primaryNav` children). If converting to click-open, add `aria-haspopup="true"` + focus-trap + `Escape` close.
- **Skip-to-content:** Implemented — `SkipLink.tsx` renders `<a href="#main-content">` first in `Layout`. Under HashRouter the component **must not** let the browser follow the href (the hash is the route): `onClick` `preventDefault`s and imperatively focuses `#main-content` (`<main id="main-content">` in `Layout`). Covered by `src/components/SkipLink.test.tsx` (3 tests) + `e2e/navigation.spec.ts` (SkipLink hash-preserving).
- **Landmarks:** `header`/`main`/`footer` present via `Layout`; every page's `PageHero` is `section` with heading hierarchy `h1 → h2`. Each ministry section in `Ministries.tsx` has `aria-labelledby` pointing to its `h2`.

### 8.3 Images & Media

- Decorative hero overlays (`PageHero` image): `alt=""` + `aria-hidden="true"`; `PageHero` also renders `bg-grain` + dual gradients over the image for contrast.
- Content images (`grounds` cards, `ministries` sections, Home): `imageAlt` is required — `GroundsPlace.imageAlt` and `Ministry.imageAlt` enforce it (see §20). `SafeImage` passes it through.
- Icon-only links: each `lucide-react` icon has `aria-hidden="true"` and the anchor has `aria-label`.
- Ministries jump nav pills: `aria-label="Jump to ministry"` on each `<Link>`.

### 8.4 Motion

- `html { scroll-behavior: smooth }` in `src/index.css`. Honor `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after { animation-duration: 0.01ms !important; }
}
```

- `src/index.css` already kills `.reveal` (opacity/transform) and `.hero-ken-burns` under `prefers-reduced-motion: reduce`, and `Reveal.tsx` falls back visible if `IntersectionObserver` is unsupported.

---

## 9. Anti-Patterns & Common Bugs

Each entry: symptom → root cause → fix → lesson. Severity: `Critical` (breaks deploy/route) / `High` (breaks type/build) / `Medium` (visual/contrast) / `Low` (nit).

| # | Anti-Pattern (Severity) | Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|---|---|
| 1 | **HashRouter → BrowserRouter** (Critical) | Deep-link 404 on GH Pages/S3 refresh | Static host has no fallback rewrites | Stay on `HashRouter`; if `BrowserRouter` is required, add `404.html` redirect shim | Static deploy = hash routing |
| 2 | **Breaking alias routes** (Critical) | Parish/school inbound links 404; `/#/visit` or `/#/donate` blank | Removed `path="mass-times"` / `"hours-location"` / `"visit"` / `"ministry"` / `"donate"` / `"volunteer"` / `"news-and-events"` alias | Keep alias routes in `App.tsx` or add explicit redirect; there are **7 aliases in 5 groups** | Alias routes are part of the contract (§5.4) |
| 3 | **Assumed code-splitting** (Critical) | `viteSingleFile` warnings / missing chunks | Dynamic `import()` expects chunks, but `singlefile` inlines all | Avoid `import()` splits unless removing `singlefile`; verify `dist/index.html` is one file | Build plugin dictates import style |
| 4 | **Arbitrary hex color** (High) | Token drift, contrast regression | Used `bg-[#691f1e]` instead of `bg-shrine-maroon-600` | Use `shrine-*` token from `@theme` | Only `@theme` is the palette |
| 5 | **`@` alias desync** (High) | `Cannot find module '@/...'` | Changed `vite.config.ts` alias without `tsconfig.json` `paths` (or vice versa) | Update both files; restart dev server | Alias is a two-file contract |
| 6 | **Bypassing `cn()`** (High) | Duplicated/conflicting Tailwind classes not deduped | Used `` `px-3 ${cond? "px-6":""}` `` | Always `cn("px-3", cond && "px-6")` | `twMerge` is the only path |
| 7 | **Stale `include`** (High) | File not type-checked | Added file outside `src/` but didn't expand `tsconfig.json` `include` | Add path to `include` (currently `["src","vite.config.ts","eslint.config.js","playwright.config.ts","playwright.built.config.ts"]`) | `include` is the type boundary |
| 8 | **`noUnusedLocals` breach** (Medium) | `tsc --noEmit` fails on unused import/var | Left placeholder imports/params after refactor | Remove or prefix deliberately unused param with `_` (`_idx`) | Strict flags are the gate |
| 9 | **Runtime font loader** (Medium) | FOIT + duplicate load | Imported fonts in JS instead of `index.html` | Fonts belong in `index.html` + `@theme`; no JS loader | One font source of truth |
| 10 | **Missing `imageAlt`** (Medium) | Empty alt on content image | Added `GroundsPlace`/`Ministry` without `imageAlt` | `imageAlt` is required — fill it | Content interface enforces a11y (§20) |
| 11 | **Plain `<a href="#id">` in HashRouter** (High) | Clicking a ministry pill routes to `NotFound` or loses the page | Used `<a href="#liturgical">` instead of `<Link to="/ministries#liturgical">` — plain href replaces the HashRouter hash | Always `<Link to="/ministries#id">` and `<Link to="/worship#id">` for hash anchors (see §5.4) | Hash is the route |
| 12 | **Lost `aria-expanded`** (Low) | Screen reader can't tell drawer state | Refactored `Header` toggle without `aria-expanded` | Keep `aria-expanded={mobileOpen}` + `aria-label` toggle | A11y props are functional |
| 13 | **Wrong `SafeImage` fallback** (Medium) | Broken hero on Wikimedia/Pexels failure shows shrine fallback | Used old `fallback="/images/hero-shrine.jpg"` (Rother path) instead of `"/images/hero-church.jpg"` | Default fallback is `/images/hero-church.jpg` — verify `src/components/SafeImage.tsx` default | All 11 `images.*` are now local (`naveCdn`/`courtyardCdn` point to local fallbacks); legacy CSP `upload.wikimedia.org`/`images.pexels.com` is retained but unused — keep `SafeImage` for any future external image (CDN → local discipline §5.5) |
| 14 | **Dev-only E2E asset assertions** (Medium) | Spec green on `pnpm dev`, red against `dist/`/live | Spec asserted the exact dev-form asset path (`/favicon.svg`) that `viteSingleFile` rewrites to `./favicon.svg` in the built HTML | Env-agnostic regex (`/^(?:\.\/|\/)favicon\.svg$/`) + resolution check; run `pnpm test:e2e:built` before shipping (round-9 E2E-L1) | Dev artifacts ≠ built artifacts |
| 15 | **agent-browser eval backslash mangling** (Low) | eval returns empty; stderr (when visible) shows "SyntaxError: Unterminated group" | Backslash-escaped regex literal inside an `agent-browser eval` string — the CLI strips backslashes from the command before JS evaluation, and `2>/dev/null` hides the error | Backslash-free contract checks: string comparisons (`h === './x'`) or `new RegExp` built from a string source; keep stderr visible while debugging (round-11 E2E-J1, ledger: `docs/e2e-live-pass-round11-2026-08-31.md`) | CLI arg parsing ≠ JS string literals |

---

## 10. Debugging Guide

| Symptom | Cause | Fix |
|---|---|---|
| `pnpm dev` → `EADDRINUSE :5173` | Port in use | `pnpm dev -- --port 5174` or `lsof -i:5173` then kill |
| `Cannot find module '@/utils/cn'` | Alias desync (see §9 #5) | Align `vite.config.ts` ↔ `tsconfig.json` `paths @/*` (`baseUrl:"."`) — change both; restart Vite |
| `npx tsc --noEmit` → `TS6133 'x' is declared but never used` | `noUnusedLocals`/`Params` (`strict` + `noUnusedLocals:true` `noUnusedParameters:true`) | Remove import or use it; for intentionally unused param, prefix `_` (e.g., `_idx`) |
| `pnpm test` → "no test files found" | `src/test/setup.ts` missing or `vite.config.ts test.include` misconfigured | Verify `src/test/setup.ts` exists and `vite.config.ts test` includes `src/**/*.{test,spec}.{ts,tsx}` with `exclude: ["e2e/**"]` — should be 32 files / 184 tests |
| `pnpm test:e2e` → failures on `#mass`/`#liturgical` etc. | Missing `id` or `Layout` double-hash logic stale | Verify `Worship.tsx` has `id="mass"`/`"confession"`/`"visit"` and `Ministries.tsx` has 6 ministry `id`s; `Layout` `resolveAnchor` must handle `/#/worship#mass` form |
| Hash anchor lands at top (`/#/worship#mass` or `/#/ministries#liturgical`) | Target `id` missing or `Layout` effect stale | Verify `id="mass"` in `Worship.tsx` and `id="liturgical"` in `Ministries.tsx`; check `Layout` `useEffect` deps `[pathname, hash]`; jump nav must be `<Link to="/ministries#id">` (not plain `<a href="#id">`, see §9 #11) |
| Double-hash `#/ministries#liturgical` doesn't scroll | `Layout` `resolveAnchor` not matching `pathname` | Verify `resolveAnchor` splits `window.location.hash` on `#`, filters, strips leading `/`, and compares against `pathname.replace(/^\//,"")` — the `cleaned === pathname…` guard prevents false anchors |
| `pnpm build` → `dist/index.html` missing or not inlined | `viteSingleFile` misordered or removed | Verify `plugins: [react(), tailwindcss(), viteSingleFile()]` order; check `dist/index.html` exists and `Inlining: index-*.js` in log; `dist/images/` alongside is expected (publicDir copy) |
| Styles missing locally but build works | `@import "tailwindcss"` order wrong | `@import` must be first line of `src/index.css` |
| Fonts not loading | `index.html` preconnect or href typo | Verify `fonts.googleapis.com` preconnect + `Fraunces`/`Source Sans 3` href intact; no JS font loader |
| GH Pages deep-link 404 on refresh | Switched to `BrowserRouter` | Revert to `HashRouter` or add `404.html` SPA redirect |
| Image 404 (`/images/hero-church.jpg`) or Wikimedia/Pexels CDN fails | Wrong public path / missing `dist/images/` on deploy / CDN blocked / old shrine fallback | Hero/fallback belong in `public/images/` and referenced as `/images/…` (absolute from root; Vite copies to `dist/images/` — upload alongside `index.html`); CDN URLs (`images.hero` Wikimedia + `naveCdn`/`courtyardCdn` Pexels in `content.ts`) must use `SafeImage` (`fallback` default `/images/hero-church.jpg` + `dataset.fallback` guard + `loading="lazy"` default) — don't use bare `<img>` for CDN sources. Upload count: **8 files** in `public/images/` |
| `tests` not found or `e2e` leaking into vitest | `test.include`/`exclude` misconfigured | Verify `vite.config.ts test: { globals:true, environment:"jsdom", setupFiles:["src/test/setup.ts"], include:["src/**/*.{test,spec}.{ts,tsx}"], exclude:["e2e/**","node_modules/**","playwright-report/**","test-results/**"] }` — `e2e/**` must be excluded |
| `vite.config.ts` `server.watch` `ENOSPC` on `pnpm dev` | Vendored `skills/` tree (large `.venv`) watched without ignore | Verify `server.watch.ignored: ["**/skills/**","**/dist/**","**/playwright-report/**","**/test-results/**","**/coverage/**","**/src.orig/**"]` is present in `vite.config.ts` |
| `tsconfig.json` errors on `eslint.config.js` or `playwright.config.ts` | Added those files to `include` without installing their types | `include` is `["src","vite.config.ts","eslint.config.js","playwright.config.ts"]` with `types ["node","vitest/globals"]` — required for `describe/it/expect` globals. |

**Live-site verification (post-deploy — Toa Payoh / Risen Christ routes):**

```bash
pnpm build && pnpm preview  # :4173
# Click through every primaryNav item + all hash anchors:
# /  /about  /history  /worship  /ministries  /news-events  /serve  /give  /faq
# /mass-times (→ Worship)  /hours-location (→ Worship)  /visit (→ Worship)
# /ministry (→ Ministries)  /news-and-events (→ NewsEvents)  /volunteer (→ Serve)  /donate (→ Give)
# /worship#mass  /worship#confession  /worship#visit
# /ministries#liturgical  #faith-formation  #pastoral-care  #family-life  #youth  #language-communities
# Direct: /#/worship#mass  and  /#/ministries#liturgical  → should land on-section
# Refresh on /#/ministries#youth → stays on-section (HashRouter)
# /does-not-exist → NotFound
```

---

## 11. Pre-Ship Checklist

Run in order — every step must be green before pushing `main` (`main` is the deploy branch).

```bash
pnpm lint                      # 1 — eslint 9.39.5 flat --max-warnings 0
pnpm typecheck                 # 2 — tsc --noEmit (strict + noUnusedLocals/Params + noFallthroughCasesInSwitch)
pnpm test                      # 3 — vitest 3.2.6 jsdom — 35 files / 202 tests green (ci-workflow 4 + repo-hygiene 3 + docs-contract 16 + cn 5 + nav 7 + content 10 + site 8 + massDay 5 + monogram 7 + deepLinks 7 + Button 11 + SkipLink 3 + Accordion 6 + SafeImage 6 + Header 17 + BackToTop 7 + Reveal 2 + wcag-contrast 5 + Ministries 3 + cta-bands 6 + worship-mass 6 + about-visuals 4 + event-chips 3 + give-featured 2 + give-uen 3 + card-affordances 6 + Timeline 3 + NotFound 2 + History 2 + Layout 2 + useScrollProgress 4 + useScrollSpy 6 + ScrollProgress 2 + head 13 + security-headers 6)
pnpm test:e2e                  # 4 — playwright 1.55.1 chromium — 51 tests green (smoke 11 + navigation 8 + ministries 4 + give-faq 4 + enhancements 7 + enhancements-round5 6 + enhancements-round7 8 + deep-links 3)
pnpm test:e2e:built            # 4b — playwright vs built artifact (vite preview :4173; E2E_BASE_URL → live host) — same 51 tests green
pnpm build                     # 5 — singlefile 2.3.3 build → dist/index.html (JS+CSS inlined) + dist/images/ (8 files, copied not inlined)
pnpm preview &                 # 6 — smoke: spot-check 10 routes + 7 alias paths + 9 hash anchors (3 on /worship + 6 on /ministries)
ls -lh dist/                   # 7 — confirm dist/index.html + dist/images/ (8 files) — publicDir copy expected, not inlined
# 8 — axe/Lighthouse a11y spot-check on Header + Home hero + FAQ + Worship#visit map
git push origin main           # 9 — deploy (GH Pages / S3 upload of dist/index.html + dist/images/)
```

| Category | Check | How |
|---|---|---|
| Lint | `pnpm lint` clean | `eslint 9.39.5` flat `eslint . --max-warnings 0` (`typescript-eslint 8.28.0` + `react-hooks 5.2.0`) — ignores `skills` + `src.orig` |
| Types | `pnpm typecheck` (`npx tsc --noEmit`) clean | `strict` + `noUnusedLocals`/`noUnusedParameters`/`noFallthroughCasesInSwitch`/`isolatedModules`/`noEmit` pass; `tsconfig.json` `include` covers `src` + `vite.config.ts` + `eslint.config.js` + `playwright.config.ts` + `playwright.built.config.ts` with `types [node, vitest/globals]` |
| Tests | `pnpm test` — 35 files / 202 tests green | `vitest 3.2.6 jsdom` via `src/test/setup.ts` (jest-dom + IntersectionObserver mock + scrollTo/scrollIntoView stubs + matchMedia stub) + `vite.config.ts test.include [src/**/*.{test,spec}.{ts,tsx}]` — `e2e/**` excluded |
| E2E | `pnpm test:e2e` — 51 tests green (8 specs) | `smoke 11 + navigation 8 + ministries 4 + give-faq 4 + enhancements 7 + enhancements-round5 6 + enhancements-round7 8 + deep-links 3` — Toa Payoh aliases + hash anchors + SafeImage fallback + mobile drawer same-route close regression + modal drawer focus trap (round-4) + rise-in hero entrance + event chips + back-to-top progress ring + aria-current nav + ScrollProgress rail + path-style deep-link redirects (round-12). `playwright.config.ts` `expect.timeout: 15s` + `webServer → pnpm exec vite :5173` — built-artifact pass: `playwright.built.config.ts` (`vite preview :4173`; `E2E_BASE_URL` → live host) |
| Build | `pnpm build` greens | `viteSingleFile 2.3.3` inlines JS + CSS; `dist/images/` 8 files copied (not inlined) — verify one-file `dist/index.html` |
| Routes | All 10 pages + 7 alias paths + 9 hash anchors navigate (HashRouter) | Manual or `agent-browser` smoke (`Layout` double-hash aware `#/ministries#id` → split + 80ms `scrollIntoView`) |
| A11y | Contrast ≥4.5:1 on body, `alt` on content images (`SafeImage` fallback), `aria-expanded` on toggle, `SkipLink` hash discipline, `aria-label="Jump to ministry"` | Spot-check per §8 table + `axe-core` on Header/Home hero/FAQ/Worship map |
| Visual | Hero gradients + `shadow-shrine`/`shadow-shrine-lg` + `divider-weave`/`divider-weave-thin` + `gold-rule`/`gold-rule-left` + `hero-ken-burns` render | Preview comparison — hero is the local `hero-church.jpg` (dusk nave) |
| Images | `SafeImage` fallback verified (all images local) + `public/images/` → `dist/images/` (8 files) + `dist/favicon.svg` on deploy | Block images or off-line smoke; check `dist/images/` has 8 files (`hero-church`, `chapel-interior`, `sanctuary`, `rosary-garden`, `stained-glass`, `parish-hall`, `cemetery`, `feast`) |
| CSP | No console CSP violations | Verify `index.html` CSP: `img-src 'self' data: blob:` (all images local), `frame-src https://www.google.com` for maps embed; no `unsafe-eval` |
| Git | No `dist/`/`node_modules/` committed; no secret material tracked (`src/repo-hygiene.test.ts` guards `docs/ssh-key.txt` + the pruned `src.orig/`) | `.gitignore` respected (`skills/` stays tracked as vendored reference but ignored by tooling; `src.orig/` pruned round-12 — guard fails if it re-enters) |

**Pre-push gate — all five must be green (verified 2026-08-31, round-9 E2E-L1 remediation):**

```bash
pnpm lint && pnpm typecheck && pnpm test && pnpm test:e2e && pnpm build
# → lint 0 + typecheck 0 + test 35/202 + test:e2e 51 + build 397.52kB dist/index.html + dist/_headers + dist/favicon.svg + dist/images/8
```

---

## 12. Lessons Learnt & How to Avoid Them

| # | Lesson | What Happened | Fix / Guard |
|---|---|---|---|
| L1 | **Alias routes are a contract, not tech debt** | Both lines considered removing alias paths as "duplicates" (orig: `shrinegift`/`grounds-art-architecture`; now: `mass-times`/`hours-location`/`ministry`/`donate`). Inbound parish/school/programme links + printed QR codes 404'd. | Documented §5.4; **7 aliases in 5 groups** preserved in `App.tsx`. Rule: renaming a canonical path requires keeping the old alias or adding a redirect. |
| L2 | **No README → this SKILL** | Early project shipped with only `docs/prompts.md`; onboarding required reading 10 files. | Added `README.md` + `AGENTS.md` + `CLAUDE.md`; this file distills all three. Update all four when adding a route/token/image. |
| L3 | **`@theme` drift is silent** | Arbitrary `bg-[#...]` would compile but evade review. | Enforce `shrine-*` tokens only; grep CI: `rg -n "bg-\[#"` or forbid `amber-`/`slate-` via test. |
| L4 | **Singlefile dictates imports** | `import()` assumed chunks until `singlefile` warning appeared. | Document §9 #3; verify `dist/index.html` is one file post-build. |
| L5 | **Strict flags catch real debt** | `noUnusedLocals` surfaced 3 dead imports post-scaffold; port surfaced similar. | Keep `strict` flags on; gate is `tsc --noEmit`. |
| L6 | **HashRouter vs BrowserRouter is a deploy decision** | Considered `BrowserRouter` for cleaner URLs; would have broken GH Pages/S3 deep-links. | ADR-1 (Appendix A) locks `HashRouter` with `404.html` escape hatch. |
| L7 | **Content shape = UI shape** | Orig `WhatToSeeSection.imageAlt` was optional in a draft; a11y regression followed. Port `GroundsPlace`/`Ministry` keep `imageAlt` + `imageFallback` required for the same reason. | Required in §20 interfaces; future entries must include both. |
| L8 | **Hash is the route — `<Link>` not `<a>`** | Ministries jump nav drafted with `<a href="#liturgical">` — would have replaced the HashRouter hash and routed to NotFound. | Fixed to `<Link to="/ministries#id">` in `Ministries.tsx` + Worship children; documented §5.4 / §9 #11. |
| L9 | **`SafeImage` default drift** | Wikimedia hero (`images.hero`) introduced a new CDN host; old default `/images/hero-shrine.jpg` would have 404'd on fallback. | Updated `SafeImage.tsx` default to `/images/hero-church.jpg`; added `images.heroFallback` + `imageFallback` on every `grounds`/`ministries` entry; CSP extended to `upload.wikimedia.org`. |
| L10 | **Stale `e2e/` was a trap — now resolved** | Port initially kept the 20-test Rother E2E verbatim (`#pilgrim-center` etc.); CI would have failed. | Rewritten to Bukit Batok St Mary: `smoke 11 + navigation 8 + ministries 4 + give-faq 4 + enhancements 8` = 35 green (2026-08-28 enhancements, incl. drawer same-route close regression + ScrollProgress + BackToTop ring + aria-current). Alias is `what-to-see` → `ministries`, `pilgrimage` → `worship` — now covered under St Mary routes. |
| L11 | **`vite.config.ts` `test` block is required** | Restoring `src/test/setup.ts` without the `test` block leaves vitest misconfigured. | `vite.config.ts` now has `test { globals:true, jsdom, setupFiles:["src/test/setup.ts"], include:["src/**/*.{test,spec}.{ts,tsx}"], exclude:["e2e/**"] }` + `types ["vitest/globals"]` — keep both in sync (see §3.2). |
| L12 | **Canonical flip: `/about` not `/about-blessed-stanley-rother`** | Port flipped the About canonical (orig: `/about-blessed-stanley-rother` canonical, `/about` alias). Any hard-coded deep link to the old canonical would 404 if the alias were dropped. | Kept only `/about` (no alias needed — the old canonical is intentionally retired for the parish). Document the flip in §5.4 + Appendix D; if old shrine links must survive, add `/about-blessed-stanley-rother` as an alias back to `/about`. |

---

## 13. Pitfalls to Avoid

**Architecture**
- Don't add SSR/API/`server/` without an ADR — this is a static SPA by design.
- Don't scatter route tables outside `src/App.tsx` — it is the only route table (17 entries, 5 alias groups).
- Don't put data arrays outside `src/data/*` — they are the data layer (`content.ts` + `nav.ts` + `site.ts`).
- Don't reintroduce St Mary of the Angels / Bukit Batok parish narratives outside the historical appendices — this is Church of the Risen Christ (91 Toa Payoh Central, 1969–2026 Toa Payoh line, Easter Sunday, UEN T08CC4042G). Hours, Mass, and address are the single source in `site.ts`; don't duplicate them across pages.

**TypeScript**
- Don't use `any` — use `unknown` + narrowing; `as any` is a last resort with `// ponytail: ceiling…` comment.
- Don't use `type` for object shapes — prefer `interface` (`type` is for unions).
- Don't relax `strict` flags to silence errors — fix the code. `noUnusedLocals`/`noUnusedParameters`/`noFallthroughCasesInSwitch`/`isolatedModules`/`noEmit` are the gate.
- Don't assume `tsconfig.json` scope — it includes `["src","vite.config.ts","eslint.config.js","playwright.config.ts"]` with `types ["node","vitest/globals"]`. Don't re-add `src.orig/` to `include`.

**Styling**
- Don't introduce `amber-400`/`slate-*`/`zinc-*` — forbidden; use `shrine-*`.
- Don't use arbitrary `bg-[#...]` — extend `@theme`.
- Don't add `tailwind.config.*` — v4 is CSS-first (`src/index.css` `@theme` is the only token source).
- Don't bypass `cn()` — `tailwind-merge` dedup matters; never concatenate Tailwind strings with template literals.

**Data / A11y**
- Don't omit `imageAlt` or `imageFallback` on `grounds`/`ministries`.
- Don't remove `alt=""` on decorative hero overlays (`PageHero`); don't drop `aria-expanded`/`aria-label` on the mobile toggle or `aria-label="Jump to ministry"` on the Ministries pills.
- Don't let `SkipLink` rewrite the hash — its `preventDefault` + imperative `focus()` is load-bearing for HashRouter.

**Build / Deploy**
- Don't commit `dist/`/`node_modules/`. `skills/` is already committed vendored reference content — don't import from it or lint it (eslint ignores it). `src.orig/` is not part of this repository (its ignore entries are inert guards).
- Don't upload `dist/index.html` without `dist/images/` — the 8 image files are copied via `publicDir`, not inlined; both must ship together to GH Pages/S3.
- Don't ship a "green CI" claim without running the full gate (`pnpm lint && pnpm typecheck && pnpm test && pnpm test:e2e && pnpm build`) — all five must be green (35 files / 202 + 51 E2E). Asset-path e2e assertions must be env-agnostic — run `pnpm test:e2e:built` so dev-only forms (e.g. `/favicon.svg` vs the singlefile-rewritten `./favicon.svg`) cannot ship (round-9 E2E-L1).

---

## 14. Best Practices

- **File naming:** `PascalCase.tsx` for components/pages (`PageHero.tsx`), `camelCase.ts` for data/utils (`content.ts`, `cn.ts`), `useThing.ts` for hooks (`useScrolled.ts`).
- **Imports:** Always `@/` for cross-directory; relative `./` only within the same folder.
- **Types:** `interface` for shapes, `type` for unions; `import type` for type-only imports; rely on inference, add explicit returns only at public boundaries. Never `any`.
- **React:** Hooks-only, composition over inheritance, early returns, handle `loading`/`error`/`empty`/`success` where data is async; disable buttons during async ops.
- **Styling:** Extend `@theme` before adding a utility; keep bespoke CSS to `@layer base/utilities` in `src/index.css`; mobile-first `sm:`/`lg:`; one shadow (`shadow-shrine`), two radii (`sm`/`full`). Use `shrine-cream/parchment(+dark)/stone/ink/charcoal/maroon-*/gold-*/pine-*/terracotta-*` + utilities `text-balance` / `bg-adobe-texture` / `bg-grain` / `divider-weave`/`divider-weave-thin` / `gold-rule`/`gold-rule-left` / `hero-ken-burns` / `rise-in`(+`-d1..d4`) / `menu-in` / `drawer-in` / `dot-pulse` / `card-lift` / `link-underline` / `reveal`+`reveal-visible` / `skip-link` / `mask-fade-b`. Motion: transform/opacity only, everything gated by the global `prefers-reduced-motion` block.
- **Data:** Keep `site.ts` as the single source for name/address/hours/mass/contact/transport/feast/uen/chequePayee/facebook/archdiocese/mapsUrl/mapsEmbedSrc. Pages consume it — don't duplicate. `content.ts` arrays + `nav.ts` nav are the only other data sources.
- **Git:** Conventional Commits (`feat:`, `fix:`, `docs:` …), atomic commits, `feat/<slug>` branches, squash-merge, short-lived (1–3 days). Don't edit `package.json` by hand for deps — use `pnpm install <pkg>`.
- **Docs:** Update `README.md` + `AGENTS.md` + `CLAUDE.md` + this file when adding a route/token/image/nav child. Keep the pruned `skills/` tree out of scope (vendored; catalog + SKILL.md contents live only in git history at `c774ed9`).

---

## 15. Coding Patterns

### 15.1 Button Variant Record (copy-pasteable)

Location: `src/components/ui/Button.tsx`

```tsx
// src/components/ui/Button.tsx — actual implementation (discriminated union)
import { Link } from "react-router-dom";
import { cn } from "@/utils/cn";

type Variant = "primary" | "secondary" | "ghost" | "outline-light";
const variantClasses: Record<Variant, string> = {
  primary: "bg-shrine-gold-500 text-shrine-maroon-900 hover:bg-shrine-gold-300 shadow-shrine",
  secondary: "bg-shrine-maroon-600 text-shrine-cream hover:bg-shrine-maroon-500",
  ghost: "bg-transparent text-shrine-maroon-600 hover:bg-shrine-maroon-50",
  "outline-light": "border border-shrine-cream/70 text-shrine-cream hover:bg-shrine-cream/10",
};
// baseClasses adds rounded-sm sizing + focus-visible ring + disabled styles.
export function Button(props: ButtonProps) {
  const classes = cn(baseClasses, variantClasses[props.variant ?? "primary"], props.className);
  if ("to" in props && props.to) return <Link to={props.to} className={classes} {...rest} />;
  if ("href" in props && props.href) return <a href={props.href} className={classes} {...rest} />;
  return <button type="button" className={classes} {...rest} />;
}
```

### 15.2 Layout Hash-Scroll Restoration (double-hash aware)

Location: `src/components/Layout.tsx` — preserves both `/#/worship#mass` and `/#/ministries#liturgical` forms.

```tsx
// src/components/Layout.tsx — actual Toa Payoh (Risen Christ) implementation
import { useEffect } from "react";
import { Outlet, useLocation } from "react-router-dom";
import { Footer } from "@/components/Footer";
import { Header } from "@/components/Header";
import { SkipLink } from "@/components/SkipLink";

function resolveAnchor(pathname: string, hash: string) {
  if (hash && hash.length > 1) return hash.slice(1);
  // Double-hash form: #/ministries#liturgical or #/worship#mass → take the last segment
  const raw = window.location.hash;
  const parts = raw.split("#").filter(Boolean);
  if (parts.length < 2) return "";
  const last = parts[parts.length - 1] ?? "";
  const cleaned = last.replace(/^\//, "");
  if (!cleaned || cleaned === pathname.replace(/^\//, "")) return "";
  return cleaned;
}

export function Layout() {
  const { pathname, hash } = useLocation();
  useEffect(() => {
    const id = resolveAnchor(pathname, hash);
    if (id) {
      const el = document.getElementById(id);
      if (el) {
        window.setTimeout(() => el.scrollIntoView({ behavior: "smooth", block: "start" }), 80);
        return;
      }
    }
    window.scrollTo({ top: 0, behavior: "instant" as ScrollBehavior });
  }, [pathname, hash]);
  return (
    <>
      <SkipLink />
      <Header />
      <main id="main-content" tabIndex={-1}>
        <Outlet />
      </main>
      <Footer />
    </>
  );
}
```

Current anchor targets: `#mass`/`#confession`/`#visit` on `/worship` and `#liturgical`/`#faith-formation`/`#pastoral-care`/`#family-life`/`#youth`/`#language-communities` on `/ministries` (see §5.4). Any new hash anchor must be added as a `section id="…" className="scroll-mt-28 …"` and wired via `primaryNav`/`footerNav` + the Ministries jump nav where appropriate.

### 15.3 `cn()` Merge

Location: `src/utils/cn.ts`

```ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)); }
```

### 15.4 PageHero Overlay (decorative image)

Location: `src/components/PageHero.tsx`

```tsx
export function PageHero({ eyebrow, title, description, image, children, compact }: PageHeroProps) {
  return (
    <section className="relative overflow-hidden bg-shrine-maroon-900 py-20 sm:py-28">
      <img src={image} alt="" className="absolute inset-0 h-full w-full object-cover opacity-25" aria-hidden="true" />
      <div className="absolute inset-0 bg-gradient-to-t from-shrine-maroon-900 via-shrine-maroon-900/85 to-shrine-maroon-900/60" />
      <div className="absolute inset-0 bg-grain opacity-40" aria-hidden="true" />
      <Container className="relative">
        <p className="text-xs font-semibold uppercase tracking-[0.3em] text-shrine-gold-300">{eyebrow}</p>
        <h1 className="mt-4 max-w-3xl text-balance font-display text-4xl font-semibold text-shrine-cream sm:text-5xl">{title}</h1>
        {description ? <p className="mt-5 max-w-2xl text-base leading-relaxed text-shrine-cream/80">{description}</p> : null}
        {children}
      </Container>
      <div className="divider-weave-thin absolute inset-x-0 bottom-0" aria-hidden="true" />
    </section>
  );
}
```

### 15.5 Ministries Jump Nav (HashRouter-safe)

Location: `src/pages/Ministries.tsx`

```tsx
import { Link } from "react-router-dom";
import { images, ministries } from "@/data/content";

// Pills — must use <Link to="/ministries#id">, never <a href="#id">
<nav aria-label="Ministries">
  {ministries.map((ministry) => (
    <Link
      key={ministry.id}
      to={`/ministries#${ministry.id}`}
      aria-label="Jump to ministry"
      className="rounded-full border border-shrine-stone bg-white px-4 py-2 text-sm font-medium text-shrine-charcoal hover:bg-shrine-parchment"
    >
      {ministry.title}
    </Link>
  ))}
</nav>

// Sections — alternating bands, each a hash target
{ministries.map((ministry, index) => (
  <section
    key={ministry.id}
    id={ministry.id}
    className={cn("scroll-mt-28 py-16 sm:py-20", index % 2 === 0 ? "bg-shrine-cream" : "bg-shrine-parchment")}
    aria-labelledby={`${ministry.id}-heading`}
  >
    <Container>
      <h2 id={`${ministry.id}-heading`} className="font-display text-2xl font-semibold text-shrine-maroon-700">{ministry.title}</h2>
      {/* … */}
    </Container>
  </section>
))}
```

---

## 16. Coding Anti-Patterns

| Don't | Do Instead | Why |
|---|---|---|
| `className="bg-[#691f1e]"` | `className="bg-shrine-maroon-600"` | Token drift — `@theme` is the palette |
| `` className={`px-3 ${open?"px-6":""}`} `` | `className={cn("px-3", open && "px-6")}` | `twMerge` dedup |
| `import hero from "../../public/images/hero.jpg"` | `<img src="/images/hero-church.jpg" … />` or `images.heroFallback` | `public/` is served at root (`/images/…`); Vite copies to `dist/images/` |
| `<a href="/about">` for internal nav | `<Link to="/about">` or `<Button to="/about">` | HashRouter + active state; plain `<a>` triggers full reload |
| `<a href="#liturgical">` inside Ministries | `<Link to="/ministries#liturgical">` | Hash is the route — plain `href` replaces it and routes to NotFound (§9 #11) |
| `type TimelineEntry = { year: string }` for a shape | `interface TimelineEntry { year: string }` | `interface` for shapes (`type` for unions) |
| `const x: any = json` | `const x: unknown = json; if (isTimeline(x)) …` | No `any` — narrow `unknown` |
| `import { tailwindConfig } from "…"` | Extend `@theme` in `src/index.css` | No config file in Tailwind v4 |
| `BrowserRouter` without `404.html` | `HashRouter` (or add GH Pages SPA shim) | Static-host deep-link 404 |
| `fallback="/images/hero-shrine.jpg"` | `fallback="/images/hero-church.jpg"` (or `images.heroFallback`) | Rother fallback path is gone |
| Duplicating `site.address`/`site.mass` strings in a page | `import { site } from "@/data/site"` | `site.ts` is the single source (§7.1) |
| Adding `GroundsPlace`/`Ministry` without `imageAlt`/`imageFallback` | Always include both | A11y + CDN fallback contract |

---

## 17. Responsive Breakpoint Reference

Tailwind defaults only (no custom config). Project usage:

| Breakpoint | Min-Width | Usage in this SPA |
|---|---|---|
| *(default)* | `0` | Single-col, stacked hero, mobile drawer (`Header` hamburger) |
| `sm` | `640px` | 2-col quick-facts `grid-cols-2`, `px-8`, `text-5xl` heroes, `py-24 sm:py-28` sections |
| `lg` | `1024px` | `lg:flex` header nav (desktop dropdown), `lg:grid-cols-2` welcome split, `lg:grid-cols-3` grounds cards |

**Rule:** Mobile-first — default is mobile; `sm:` then `lg:` only. Test: `pnpm dev` + Chrome DevTools `375×812` (iPhone) → `1280×800`. Header breakpoint is `lg` (drawer below `lg`, flex nav at `lg`).

---

## 18. Z-Index Layer Map

| Layer | `z-*` | Element | File | Purpose |
|---|---|---|---|---|
| Top | `z-[100]` | Skip-to-content link | `src/components/SkipLink.tsx` (`.skip-link` utility) | Always reachable above everything when focused |
| High | `z-50` | `<header>` + its desktop dropdown | `src/components/Header.tsx` | Fixed nav above content + hero; dropdown inherits header stacking |
| Mid | `z-40` | Ministries jump nav (sticky under header, if sticky) | `src/pages/Ministries.tsx` | Sticky section nav below the fixed header — verify against `Header` height |
| Base | `z-auto` | `main`, `footer`, `PageHero` gradients, `Timeline` rail | `src/components/Layout.tsx`, `Footer.tsx`, `PageHero.tsx`, `Timeline.tsx` | Normal flow |
| Portal | — | None yet | — | Add Radix/Portal table when modals exist |

**Conflict rule:** `Header` owns `z-50`; jump nav stays below it at `z-40`; only the skip link may exceed them (`z-[100]`). Don't add competing layers without updating this table. If making the Ministries pill bar `sticky top-[…]`, verify `scroll-mt-28` on target sections still clears the header.

---

## 19. Color Reference (Complete)

Every hex matches `src/index.css` `@theme` byte-for-byte. **Fail the build if it drifts.** Round-12 extended the terracotta scale with one text-bearing step (`terracotta-600 #8f4c30` — WCAG AA for the Devotion chip; contract `src/components/wcag-contrast.test.tsx` computes ratios from this token layer); verification command `grep shrine- src/index.css` → 25 colors + 2 shadows.

| Token | Hex | RGB | Tailwind Class | Usage (Risen Christ / Toa Payoh context) |
|---|---|---|---|---|
| `shrine-cream` | `#faf6ec` | `250,246,236` | `bg-shrine-cream` | Page bg, card on dark, alternating ministry band |
| `shrine-parchment` | `#f2e9d6` | `242,233,214` | `bg-shrine-parchment` | Section bands, alternating ministry band |
| `shrine-parchment-dark` | `#e7d9b8` | `231,217,184` | `bg-shrine-parchment-dark` | Dark parchment variant |
| `shrine-stone` | `#dccfae` | `220,207,174` | `border-shrine-stone` | Borders/dividers, ministry pill border |
| `shrine-ink` | `#2a2115` | `42,33,21` | `text-shrine-ink` | Primary text |
| `shrine-charcoal` | `#423a2c` | `66,58,44` | `text-shrine-charcoal` | Secondary text / 70% |
| `shrine-maroon-50` | `#fbf0ee` | `251,240,238` | `bg-shrine-maroon-50` | Ghost hover bg |
| `shrine-maroon-100` | `#f3d9d4` | `243,217,212` | — | Light tint |
| `shrine-maroon-500` | `#7c2a25` | `124,42,37` | `text-shrine-maroon-500` | Eyebrow on light, links |
| `shrine-maroon-600` | `#691f1e` | `105,31,30` | `bg-shrine-maroon-600` | Secondary btn, timeline badge, weave band |
| `shrine-maroon-700` | `#55191a` | `85,25,26` | `text-shrine-maroon-700` | Display heading (`h1–h4`) |
| `shrine-maroon-800` | `#431315` | `67,19,21` | — | Mid-dark maroon |
| `shrine-maroon-900` | `#33100f` | `51,16,15` | `bg-shrine-maroon-900` | Hero + footer bg |
| `shrine-maroon-950` | `#200a0a` | `32,10,10` | `bg-shrine-maroon-950` | Deepest maroon (header top strip) |
| `shrine-gold-100` | `#f8ecd2` | `248,236,210` | — | Light gold |
| `shrine-gold-300` | `#e2bf72` | `226,191,114` | `text-shrine-gold-300` | Eyebrow on dark, icon tint |
| `shrine-gold-400` | `#d1a955` | `209,169,85` | — | Gold mid |
| `shrine-gold-500` | `#c3963f` | `195,150,63` | `bg-shrine-gold-500` | Primary CTA, gold rule |
| `shrine-gold-600` | `#a67a2e` | `166,122,46` | — | Gold hover |
| `shrine-pine-500` | `#335840` | `51,88,64` | `text-shrine-pine-500` | Pine accent |
| `shrine-pine-600` | `#26402f` | `38,64,47` | `bg-shrine-pine-600` | Weave third band |
| `shrine-pine-700` | `#1c3123` | `28,49,35` | `bg-shrine-pine-700` | Deep pine |
| `shrine-terracotta-400` | `#c17a53` | `193,122,83` | — | Terracotta mid |
| `shrine-terracotta-500` | `#ab5f3c` | `171,95,60` | `bg-shrine-terracotta-500` | Devotion chip border (decorative) |
| `shrine-terracotta-600` | `#8f4c30` | `143,76,48` | `text-shrine-terracotta-600` | Devotion chip text — AA 5.36:1 on parchment (round-12, audit F-1) |
| `shadow-shrine` | `rgba(51,16,15,0.45)` | — | `shadow-shrine` | `0 20px 60px -20px` |
| `shadow-shrine-lg` | `rgba(51,16,15,0.55)` | — | `shadow-shrine-lg` | `0 40px 90px -30px` |

**Forbidden:** `amber-*`, `slate-*`, `zinc-*`, `gray-*` generics (except Tailwind neutrals in tooling). Only exception: tooling grays in `node_modules`.

---

## 20. The Complete TypeScript Interface Reference

All interfaces below compile as-is against `tsconfig.json` (`strict` + `bundler` + `react-jsx`). Locations: `src/data/*`, `src/components/ui/*`, `src/utils/cn.ts`. **Verbatim against `src/data/content.ts`, `src/data/nav.ts`, `src/data/site.ts`, `src/components/SafeImage.tsx`, `src/components/ui/*`.**

### 20.1 Content Interfaces (`src/data/content.ts`)

```ts
export interface TimelineEntry {
  year: string;
  title: string;
  description: string;
}
// lifeTimeline: TimelineEntry[] — 8 entries (1969, 1971, 1970s, 2003, 2010s, 2021, 2023, 2026)
// Toa Payoh arc: Ho Ping Centre → 1971 consecration (first air-con, $450k) → many tongues + Velankanni → 2003 four-storey wing → Simbang Gabi households → Golden Jubilee → Fr Brian → Grateful/Faithful/Sent

export interface GroundsPlace {
  id: string;              // "main-church" | "chapel" | "parish-hall"
  title: string;
  summary: string;
  details: string[];       // 4 bullets each
  image: string;           // CDN (naveCdn/courtyardCdn) or local /images/*
  imageFallback: string;   // local /images/* — required (SafeImage fallback)
  imageAlt: string;        // required — a11y
}
// grounds: GroundsPlace[] — 3 (Main Church / Adoration Room / Parish Hall & Media Centre)

export interface Ministry {
  id: string;              // "liturgical" | "faith-formation" | "pastoral-care" | "family-life" | "youth" | "language-communities"
  title: string;
  summary: string;
  details: string[];       // 4 bullets each
  image: string;
  imageFallback: string;   // required
  imageAlt: string;        // required
}
// ministries: Ministry[] — 6 (new — no orig counterpart)

export interface FaqItem {
  question: string;
  answer: string;
}
// faqs: FaqItem[] — 6 (Mass/confession/how to get there/parking/baptism-marriage-Mass intention/Adoration Room)

export interface EventItem {
  title: string;
  date: string;            // "22–23 August" | "First Wednesday of each month" | "Sundays from 23 August, 12.45–3.30 p.m." …
  summary: string;
  category: "Parish" | "Devotion" | "Formation" | "Archdiocese";
  href?: string;           // optional — e.g. CEP → https://www.cep-sg.org, F.R.E.E. → https://free.risenchrist.org.sg/
}
// upcomingEvents: EventItem[] — 6 (Velankanni 10–12 Sep, CEP, F.R.E.E. Acts, Sunday Reflections, RCIA, Intercessory Prayer)

export interface GivingOption {
  name: string;            // PayNow UEN T08CC4042G | Weekend collections | Mass offerings | SSVP | Cheque | Cash at office | General Church Offering | Church Maintenance
  description: string;
  icon: "flame" | "church" | "sprout" | "heart" | "book" | "hand-heart" | "landmark" | "globe";
}
// givingOptions: GivingOption[] — 8 (PayNow/collections/Mass offerings/SSVP/cheque/cash/General Offering/Maintenance)

export interface Priest {
  name: string;
  role: string;            // "Parish Priest" | "Assistant Parish Priest"
  email?: string;          // e.g. brian.dsouza@catholic.org.sg — diocesan clergy carry email + phone
}
// priests: Priest[] — 3 (Brian D'Souza, Arun Bellarmin, Dexter Chua — each email + phone)

export interface PpcMember {
  role: string;            // "Parish Priest" | "Assistant Parish Priest" | "Secretariat" | "Parish Administrator" | "Youth Coordinator" | "Pastoral Coordinator"
  name: string;
}
// ppcMembers: PpcMember[] — 7 (3 priests + Secretariat/Admin/Youth/Pastoral lay roles)

// Untyped const exports (no exported interface — shape inferred):

export const serveRoles: {
  title: string;           // "Liturgical ministers" | "Catechists & facilitators" | "Pastoral care" | "Hospitality & media"
  description: string;
}[] // 4

export const devotions: {
  title: string;           // "Adoration" | "Intercessory Prayer" | "Velankanni Devotion" | "Simbang Gabi" | "Bahasa Prayer Group" | "Tamil & Tagalog Devotions"
  when: string;            // "First Wednesday, 7.30 p.m. rosary · 8.00 p.m. Mass" | …
  where: string;           // "Adoration Room — daily" | "Main Church — 2nd & 4th Thu 8.00 p.m." | "September — parish feast of Our Lady of Velankanni" | "December — nine-day novena" | "1st Friday, 8.00 p.m." | "2nd/4th Sunday after Mass" | …
}[] // 6

export const images: {
  hero: string;            // "/images/hero-church.jpg" (local — was Wikimedia in src.orig)
  heroFallback: string;    // "/images/hero-church.jpg"
  chapel: string;          // "/images/chapel-interior.jpg"
  sanctuary: string;       // "/images/sanctuary.jpg"
  garden: string;          // "/images/rosary-garden.jpg"
  glass: string;           // "/images/stained-glass.jpg"
  hall: string;            // "/images/parish-hall.jpg"
  cemetery: string;        // "/images/cemetery.jpg"
  feast: string;           // "/images/feast.jpg"
  naveCdn: string;         // local alias → "/images/sanctuary.jpg"
  courtyardCdn: string;    // local alias → "/images/rosary-garden.jpg"
} // as const — 11 keys, all local (naveCdn/courtyardCdn are local aliases)
```

### 20.2 Navigation Interfaces (`src/data/nav.ts`)

```ts
export interface NavLink {
  label: string;
  to: string;              // "/about" | "/worship#mass" | "/ministries#liturgical" | "/news-events" …
}
export interface NavItem {
  label: string;
  to: string;
  description?: string;
  children?: (NavLink & { description?: string })[]; // hover dropdown + mobile drill-down source
}
// primaryNav: NavItem[] — 6 (Home, About [3 children], Worship [3 children: #mass/#confession/#visit], Ministries [3 children: liturgical/faith-formation/pastoral-care], News & Events, Serve)
// footerNav: NavLink[] — 10 (The Parish, Mass Times→/worship#mass, History, FAQ, Liturgical→/ministries#liturgical, Faith Formation, Pastoral Care, News & Events, Serve, Give)
```

### 20.3 Site Constants (`src/data/site.ts`) — verbatim (drift-checked by `src/head.test.ts` + `src/data/site.test.ts`)

```ts
// src/data/site.ts — single source for parish facts (as const) — verbatim from src/data/site.ts
export const site = {
  name: "Church of the Risen Christ",
  shortName: "Risen Christ Toa Payoh",
  chineseName: "耶稣复活堂",
  tagline: "Grateful, Faithful, and Sent.",
  vision: "He is risen.",
  address: {
    street: "91 Toa Payoh Central",
    city: "Singapore",
    zip: "319193",
    get full() { return `${this.street}, ${this.city} ${this.zip}`; },
    get query() { return encodeURIComponent(this.full); },
  },
  hours: {
    gates: "Open for Mass, Adoration, and parish programmes",
    mainChurch: "Open for Mass and private prayer",
    chapel: "Adoration Room — Mon 12.00 noon–10.00 p.m.; Tue–Sat 7.00 a.m.–10.00 p.m.; Sun 7.00 a.m.–6.00 p.m.; Public holidays 8.00 a.m.–6.00 p.m.",
    reception: "Parish Office: Mon–Fri 9.00 a.m.–4.00 p.m.; Sat 9.00 a.m.–12.00 noon; Sun 8.00 a.m.–1.00 p.m.",
    parishOffice: "Mon–Fri 9.00 a.m.–4.00 p.m.; Sat 9.00 a.m.–12.00 noon; Sun 8.00 a.m.–1.00 p.m.",
    mediaCentre: "Tue & Fri 12.00 noon–4.00 p.m.; Sat 12.00 noon–7.00 p.m.; Sun 8.00 a.m.–1.00 p.m. Tel +65 6356 5958",
    adorationRoom: "Mon 12.00 noon–10.00 p.m.; Tue–Sat 7.00 a.m.–10.00 p.m.; Sun 7.00 a.m.–6.00 p.m.; Public holidays 8.00 a.m.–6.00 p.m.",
  },
  mass: {
    weekdayMorning: "Mon–Fri, 6.30 a.m.",
    weekdayEvening: "Mon–Fri, 6.00 p.m.",
    saturday: "6.30 a.m. · 5.30 p.m. (anticipated Sunday Mass)",
    sunday: ["7.00 a.m. English", "8.15 a.m. Mandarin", "9.45 a.m. English", "11.30 a.m. English", "5.30 p.m. English"] as const,
    confession: "Please approach a priest after Mass, or contact the parish office to arrange a time of Reconciliation.",
    adoration: "Adoration Room — Monday 12.00 noon–10.00 p.m.; Tuesday to Saturday 7.00 a.m.–10.00 p.m.; Sunday 7.00 a.m.–6.00 p.m.; Public holidays 8.00 a.m.–6.00 p.m.",
    secondCollection: "Announced in the weekly bulletin",
    note: "All Masses are held in the Main Church unless otherwise indicated. Public holidays (Mon–Fri): 7.30 a.m. only. Saturday public holidays: 7.30 a.m. and 5.30 p.m.",
    monthly: "Bahasa Indonesia: 1st Friday, 8.00 p.m. · Tamil: 2nd Sunday, 7.00 p.m. · Tagalog: 4th Sunday, 3.00 p.m.",
  },
  contact: {
    parishPriestPhone: "+65 6255 7509",
    officePhone: "+65 6253 2166",
    mediaPhone: "+65 6356 5958",
    email: "crc.secretariat@catholic.org.sg",
    adminEmail: "crc.admin@catholic.org.sg",
    connectEmail: "crc.pastoral@catholic.org.sg",
    youthEmail: "crc.youth@catholic.org.sg",
    dpoEmail: "dpo.crc@catholic.org.sg",
  },
  transport: {
    mrt: "Toa Payoh (NS19) — 6 minutes' walk from Exit A",
    buses: "88, 157, 163 — 2 minutes from bus stop B52261",
  },
  feast: {
    name: "The Risen Christ",
    date: "Easter Sunday",
  },
  uen: "T08CC4042G",
  chequePayee: "Church of the Risen Christ",
  facebook: "https://www.facebook.com/risenchrist.sg",
  instagram: "https://www.instagram.com/churchoftherisenchrist",
  youtube: "https://www.youtube.com/churchoftherisenchrist",
  archdiocese: "https://www.catholic.sg/",
  mapsUrl: "https://www.google.com/maps/search/?api=1&query=91+Toa+Payoh+Central+Singapore+319193",
  mapsEmbedSrc: "https://www.google.com/maps?q=91+Toa+Payoh+Central,+Singapore+319193&output=embed",
  origin: "https://www.risenchrist.org.sg",
  freeMinistry: "https://free.risenchrist.org.sg/",
  ssvp: "https://ssvp.risenchrist.org.sg/",
  bulletin: "https://online.fliphtml5.com/krnap/qfut/",
  cep: "https://www.cep-sg.org",
  get url() { return `${this.origin}/`; },
  get ogImage() { return `${this.origin}/images/hero-church.jpg`; },
} as const; // Footer + Worship + About consume it; never duplicate parish facts in pages — origin/url/ogImage drift-checked by head.test.ts

// src/components/SafeImage.tsx// src/components/SafeImage.tsx
export interface SafeImageProps {
  src: string;
  fallback?: string;           // default "/images/hero-church.jpg" (local hero image)
  alt: string;                 // required — a11y
  className?: string;
  loading?: "lazy" | "eager";  // default "lazy"
}

// images export (see 20.1) — 11 entries; 3 CDN fall back to /images/* via SafeImage
```

### 20.4 UI Primitive Props

```ts
// src/components/ui/Button.tsx
type Variant = "primary" | "secondary" | "ghost" | "outline-light";
type ButtonProps =
  | ({ to: string } & React.AnchorHTMLAttributes<HTMLAnchorElement> & { variant?: Variant; icon?: React.ReactNode; className?: string })
  | ({ href: string } & React.AnchorHTMLAttributes<HTMLAnchorElement> & { variant?: Variant; icon?: React.ReactNode; className?: string })
  | (React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: Variant; icon?: React.ReactNode; className?: string });
// discriminated: `to` → <Link>, `href` → <a>, else <button>; all carry `className?` via rest + cn()

// src/components/ui/Container.tsx
interface ContainerProps { children: React.ReactNode; className?: string; }

// src/components/ui/SectionHeading.tsx
interface SectionHeadingProps {
  eyebrow?: string;
  title: string;
  description?: string;
  align?: "left" | "center";
  light?: boolean;         // light = gold/cream on dark
  className?: string;
}

// src/components/PageHero.tsx
interface PageHeroProps {
  eyebrow: string;
  title: string;
  description?: string;
  image: string;           // hero image src (Wikimedia CDN, fallback /images/hero-church.jpg via SafeImage where used)
  children?: React.ReactNode;
  compact?: boolean;       // tighter vertical padding
}

// src/components/ui/Reveal.tsx
interface RevealProps { children: React.ReactNode; delay?: number; as?: "div" | "li"; className?: string; }

// src/components/ui/Accordion.tsx
interface AccordionProps { items: { question: string; answer: string }[]; } // faqs[6]

// src/hooks/useScrolled.ts
export function useScrolled(threshold?: number): boolean; // default 12; Header uses 16
```

### 20.5 Utility

```ts
// src/utils/cn.ts
import type { ClassValue } from "clsx";
export function cn(...inputs: ClassValue[]): string; // twMerge(clsx(...))
```

---

## Appendix A — ADRs (Architecture Decision Records)

| # | Decision | Rationale | Consequence |
|---|---|---|---|
| ADR-1 | `HashRouter` over `BrowserRouter` | Zero-config deploy to GH Pages/S3 — no server rewrites; deep-links (`/#/worship#mass`, `/#/ministries#liturgical`) survive refresh | URLs contain `/#/` — acceptable for a parish SPA; `404.html` shim required if migrating to `BrowserRouter` |
| ADR-2 | `vite-plugin-singlefile` | Primary `dist/index.html` (+ `dist/images/` public copy — 8 files) — trivial upload, no asset path breakage | Singlefile inlines JS+CSS only; `publicDir` is copied; no code-splitting; keep `index.html` ≤400 kB |
| ADR-3 | Tailwind v4 CSS-first `@theme` | Tokens co-located with CSS, no `tailwind.config.*` drift; `index.css` is the palette (24 colors + 2 shadows unchanged from rothershrine) | Extend `@theme` only, never arbitrary hex |
| ADR-4 | File-backed `src/data/*` (no CMS) | Typed arrays are enough for ~40 items (8+3+6+6+6+8+3+16+4+6) plus `site` + `nav`; CMS adds auth/ISR without benefit | Keep `content.ts`/`site.ts`/`nav.ts` as fallback if CMS is introduced behind `src/lib/cms/` |
| ADR-5 | Alias `@→src/` sync contract | Short imports (`@/utils/cn`) without relative `../../../` | Two-file change (`vite.config.ts` + `tsconfig.json` `paths` + `include`) — must stay synced |
| ADR-6 | `src.orig/` reference policy | The St Joseph BT intermediate is **retained locally, ignored via `.gitignore` (not committed)**; `eslint`/`vite watch` ignore entries are active guards; lineage Rother → St Joseph BT (`src.orig/`) → St Mary of the Angels (`src`) | `eslint` ignores `src.orig/`; `vite watch` ignores it; never import from it; do not re-add to `tsconfig.json` `include` |

---

## Appendix B — Live-Site Validation

**Smoke script (manual or `agent-browser` — Bukit Batok / St Mary routes):**

```
# after pnpm build && pnpm preview (:4173)
1. /                      → hero (local `/images/hero-church.jpg` + `SafeImage` fallback) + quick-facts + grounds 3 + events visible
2. /about                 → parish identity (Pray·Form·Go) + priests 4 OFM + ppcMembers 6
3. /history               → timeline 8 entries (1957–2026 Franciscan/WOHA) via Timeline left rail + dot-pulse
4. /worship               → #mass (weekday/weekend Mass), #confession (confession + adoration + devotions), #visit (map + hours + transport); test /mass-times, /hours-location, /visit aliases all land on Worship
5. /worship#mass (direct) → lands on Mass schedule
6. /worship#confession    → lands on Confession & Adoration
7. /worship#visit         → lands on Find Us (map embed + Bukit Batok NS2 / Beauty World DT5 + buses Ave 2/3/4/6)
8. /ministries            → 6 pills + 6 alternating sections; click each #liturgical/#faith-formation/#pastoral-care/#family-life/#youth/#mandarin scrolls to section
9. /ministries#liturgical (direct) → lands on Liturgical
10. /ministry             → same as /ministries (alias)
11. /news-events + /news-and-events → 6 events (Parish/Devotion/Formation/Archdiocese)
12. /serve + /volunteer   → serveRoles 4 (title+summary) + devotions 6 (title+when+where)
13. /give + /donate       → 8 giving options (PayNow UEN T08CC4053H / Poor & Needy HRSM, Tap & Give, Church Maintenance Fund, cheque payable Church of St Mary of the Angels, cash at Reception, General Church Offering, Mass offerings)
14. /faq                  → 6 Q&As via Accordion
15. /does-not-exist       → NotFound
16. refresh on /#/worship#visit → stays on-section (HashRouter)
17. refresh on /#/ministries#youth → stays on-section
```

What CI cannot catch: hash-scroll offset on mobile Safari, `divider-weave` paint, font FOIT, `shadow-shrine` clip on `overflow-hidden` parent, Wikimedia/Pexels CDN fallback timing.

---

## Appendix C — The Meticulous Approach (6-Phase Workflow)

This project follows **ANALYZE → PLAN → VALIDATE → IMPLEMENT → VERIFY → DELIVER** for every non-trivial task.

1. **ANALYZE** — Mine explicit, implicit, and ambiguous requirements; explore 2–3 approaches with trade-offs.
2. **PLAN** — Sequenced phases with checklists + success criteria; present for approval.
3. **VALIDATE** — Obtain explicit go-ahead before coding.
4. **IMPLEMENT** — Library-first, modular, TDD Red→Green→Refactor (one cycle per commit) — harness is **green (25 files/142 + 48 E2E)**; gate on `lint && typecheck && test && test:e2e && build` + manual smoke.
5. **VERIFY** — `pnpm lint` + `pnpm typecheck` + `pnpm test` + `pnpm test:e2e` + `pnpm build` + a11y/perf review + edge cases.
6. **DELIVER** — Usage instructions + runbook + follow-up recommendations.

---

## Appendix D — Migration Note (Rother → St Joseph BT → St Mary of the Angels — second hop)

### D.1 Provenance

| Item | Detail |
|---|---|
| Origin | Blessed Stanley Rother Shrine (Oklahoma City) clone — `rothershrine-v2_SKILL.md` v1.3.0, 2026-08-27, 49 tests (29 unit + 20 E2E) green |
| Intermediate | St Joseph's Church (Bukit Timah), Singapore — https://stjoseph-bt.org.sg/ — 620 Upper Bukit Timah Road, S678116 — second-oldest parish, Palladian 1853, cemetery, 1845–2017 hill line; now archived as `src.orig/` (Rother→St Joseph) |
| Port | Church of St Mary of the Angels, Bukit Batok — https://www.stmary.sg/ — 5 Bukit Batok East Ave 2, S659918 — Franciscan parish since 1970 (Portiuncula, OFM Custody of St Anthony), WOHA 2004, Garden of Peace, 1957–2026 timeline |
| Port version | **1.2.0** (`package.json` `version`) — St Mary line (intermediate St Joseph was 1.0.0 → reset from 1.3.0 Rother); stack and tooling versions unchanged (see §2) |
| Date | 2026-08-30 (second hop St Joseph → St Mary) |
| Singlefile deploy | Unchanged — `dist/index.html` (+ `dist/images/` now **8** files vs orig 4) → GH Pages/S3 |
| Test state | **25 files / 141 tests + 42 E2E green** (St Mary green, same harness as St Joseph 1.3.0; orig 29 unit + 20 E2E preserved in `src.orig/` as Rother snapshot) |
| Preservation | `src.orig/` is a frozen snapshot of the **St Joseph BT** port (which itself preserves the Rother original) — Rother → St Joseph (src.orig) → St Mary (src). `src.orig/` is retained locally, untracked since round 3 (2026-08-30 — `git rm -r --cached` + `.gitignore`), eslint + vite-watch ignored, never imported, never re-added to `include`. |

### D.2 What Changed (AUDIT diff summary)

**Routes — 17 entries (16 paths + `*`) vs orig 16 (15 + `*`):**

| Aspect | Current (St Mary of the Angels) | Intermediate (St Joseph BT, in `src.orig/`) / Orig (Rother) | Note |
|---|---|---|---|
| Total | 17 `Route` entries | 16 | +1 alias path |
| Page components | 10 (Home, About, History, Worship, Ministries, NewsEvents, Serve, Give, FAQ, NotFound) — same as St Joseph | 10 (Home, AboutRother, History, WhatToSee, Pilgrimage, NewsEvents, Volunteer, Give, FAQ, NotFound) in Rother; St Joseph already had the 4 renames | Renames `AboutRother→About`, `WhatToSee→Ministries`, `Pilgrimage→Worship`, `Volunteer→Serve` were done in the first hop (Rother→St Joseph) and preserved |
| Alias groups | 5 groups, 7 alias paths | 5 groups, 6 alias paths | See §5.4 |
| `/about` | **Canonical** | Alias of `/about-blessed-stanley-rother` (canonical) | **Flipped** |
| `/hours-location` | Alias of **`/worship`** | Alias of `/pilgrimage` | **Reassigned** |
| `/visit` | Alias of **`/worship`** (with `/mass-times`) | Alias of `/pilgrimage` (with `/visit-planning`) | `/visit` moved; `/mass-times` new, `/visit-planning` removed |
| `/what-to-see` / `/grounds-art-architecture` | **Gone** — replaced by `/ministries` / `/ministry` | Canonical `/what-to-see` + alias `/grounds-art-architecture` | 6 ministries + jump nav replace 3 shrine-site cards |
| `/volunteer` | **Alias** of `/serve` | Sole route (no alias) | `/serve` is new canonical |
| `/give` aliases | `/donate` | `/shrinegift` | Replaced |
| Hash anchors | `#mass`/`#confession`/`#visit` (Worship) + 6 ministry ids | `#pilgrim-center`/`#shrine-church`/`#tepeyac-hill` (WhatToSee) + `#visit` (Pilgrimage) | **Completely replaced** |

**Data — `src/data/content.ts`:**

| Array / Export | Current | Orig | Diff |
|---|---|---|---|
| Interfaces | 8 (`TimelineEntry`, `GroundsPlace`, `Ministry`, `FaqItem`, `EventItem`, `GivingOption`, `Priest`, `PpcMember`) | 5 (`TimelineEntry`, `WhatToSeeSection`, `FaqItem`, `EventItem`, `GivingOption`) | `WhatToSeeSection` removed; `GroundsPlace`/`Ministry`/`Priest`/`PpcMember` added |
| `lifeTimeline` | 8 — **1957–2026** Franciscan Bukit Batok (WOHA) | 8 — 1845–2017 Singapore hill mission (intermediate) / 1935–2023 Oklahoma/Guatemala martyr (orig) | Same length, different century/parish — second hop shifts 1845–2017 → 1957–2026 |
| `grounds` | 3 — `main-church`/`chapel`/`rosary-garden` (+ `imageFallback`) | `whatToSee` 3 — `pilgrim-center`/`shrine-church`/`tepeyac-hill` | Renamed + split; `GroundsPlace` extends `WhatToSeeSection` with `+imageFallback` |
| `ministries` | 6 — `liturgical`/`faith-formation`/`pastoral-care`/`family-life`/`youth`/`mandarin` | *(none)* | New |
| `faqs` | 6 — Mass/confession/MRT+ gates/feast 1 May/baptism-marriage/cemetery | 6 — shrine hours/cost/Mass duration/accessibility/burial | Same count, entirely rewritten |
| `upcomingEvents` | 6 — `title`+`date`+`summary`+`category` + `href?` (Parish/Devotion/Formation/Archdiocese) | 4 — `date`+`title`+`location`+`description`+`category` (Feast/Pilgrimage/Formation/Community) | +2 events, shape lost `location`, gained `href` |
| `givingOptions` | 8 — PayNow UEN, collections, cash boxes, cheque, SSVP, GIFT, Boys' Town, Mass offerings | 8 — General Fund, Pipe Organ, Tepeyac Hill, Apla's Circle, Education, Hospitality, Shrine Church, Guatemala Mission | Same count, all names/icons/meanings replaced |
| `priests` | 3 | *(none)* | New |
| `ppcMembers` | 16 | *(none)* | New |
| `serveRoles` | 4 (untyped const) | *(none)* | New |
| `devotions` | 6 — St Anthony Tue 18.30, Adoration daily 7–21.30, Reconciliation wknd, Lauds, Deaf Community Sun 16.00, Portiuncula 2 Aug | 6 — Mass in Honour of St Joseph, First Friday, Holy Hour for Vocations, Children's Mass, Divine Mercy, Adoration | Retained shape, devotion names updated for Franciscan parish |
| `images` | **11 keys** — `hero` (Wikimedia 2025) + `heroFallback` `/images/hero-church.jpg` + `chapel`/`sanctuary`/`garden`/`glass`/`hall`/`cemetery`/`feast` + `naveCdn`/`courtyardCdn` (Pexels). CDN 3 on 2 hosts | 10 keys — `hero` (Pexels) + `heroFallback` `/images/hero-shrine.jpg` + `wheat`/`wheatFallback`/`atitlan`/`atitlanSunset`/`atitlanAerial`/`chapel`/`garden`/`hillChapel`. CDN 7 on 1 host | `hero` host changed to Wikimedia; wheat/atitlan set removed; local count 8 vs 3 |
| `site.ts` | 17+ top keys; `address` 5 Bukit Batok East Ave 2 659918, `hours` 7 (gates/mainChurch/chapel/reception/parishOffice/columbarium/adorationRoom), `mass` 7 (weekdayMorning 7+12.15/weekdayEvening 18.30/saturday 16/18+19.45 Tamil/sunday[6] 7.15 Man+9/11/13/17/19 Eng/confession wknd 7 slots/adoration daily 7–21.30/secondCollection CMOF + note), `contact` 5 phones + 2 emails, `transport` Bukit Batok NS2/Beauty World DT5 + Ave 2/3/4/6 buses, `feast` 2 Aug Portiuncula, `uen` T08CC4053H + HRSM/`chequePayee`/`facebook`/`instagram`/`youtube`/`telegram`/`whatsapp`/`franciscans`/`mapsUrl`/`mapsEmbedSrc` + origin/url/ogImage | St Joseph intermediate: 620 Upper BT, hours 5 (gates/mainChurch/chapel/bookshop/adorationRoom), mass 7 (sunday[4], confession 15 min, adoration Tue, secondCollection 4th Sun), contact 3 phones, transport Cashew + 67 etc., feast 1 May, uen T08CC4043C, cheque St Joseph's Church (Bukit Timah) | Entirely replaced again (parish facts single-source) |

**Config drift:**

| File | Current | Orig |
|---|---|---|
| `vite.config.ts` | No `test` block, no `server.watch.ignored` | Had `test { globals, jsdom, setupFiles, include, exclude }` + `server.watch.ignored` for `skills/` |
| `tsconfig.json` | `include ["src","vite.config.ts"]`, `types ["node"]` | `include ["src","vite.config.ts","eslint.config.js","playwright.config.ts"]`, `types ["node","vitest/globals"]` |
| `eslint.config.js` | Ignores `skills` + `src.orig` | Ignores `skills` only |
| `public/images/` | **8 files** (hero-church, chapel-interior, sanctuary, rosary-garden, stained-glass, parish-hall, cemetery, feast) | 4 files (hero-shrine etc.) |
| `index.html` | CSP `img-src` adds `upload.wikimedia.org`; OG/meta for St Joseph BT | CSP `img-src https:` only; OG for Rother Shrine |
| `_redirects`/`404.html` | Not needed (`HashRouter`) | Not needed |

### D.3 What Stayed

- **Design tokens** — `src/index.css` `@theme` (24 colors + 2 shadows) + `@layer` utilities (22 + 6 keyframes) + typography (Fraunces + Source Sans 3) — byte-for-byte identical.
- **Component primitives** — `Button`/`Container`/`SectionHeading`/`Accordion`/`Reveal`/`SafeImage`/`Emblem`/`SkipLink`/`Timeline`/`SocialIcons`/`Header`/`Footer`/`PageHero`/`Layout` — same files, same APIs, only `SafeImage` default fallback updated (`hero-church.jpg`).
- **Hook** — `useScrolled.ts` identical; Header still `useScrolled(16)`.
- **Stack & versions** — React 19.2.8, Vite 7.3.6, Tailwind 4.3.3, TypeScript 5.9.3, React Router 7.18.2, singlefile 2.3.3, eslint 9.39.5, vitest 3.2.6, playwright 1.55.1 — all pinned exact.
- **HashRouter + singlefile + alias-contract patterns** — same ADRs, only the route names changed.

### D.4 How to Use `src.orig/`

- **Read-only reference** for auditing the port — diff `src/App.tsx` vs `src.orig/App.tsx`, `src/data/*` vs `src.orig/data/*`, etc.
- **Do not import** from it — the app must not depend on `src.orig/`.
- **Do not lint/type-check** it — it is excluded from `eslint.config.js` `ignores` and `tsconfig.json` `include`.
- **Do not delete** it — it is the provenance record for the Rother Shrine line and the template for rewriting `e2e/` + unit tests (6 files/29 tests reference).

---

## Appendix E — Validation: src vs src.orig (2026-08-30)

Full report: [`docs/validation-src-vs-src.orig-2026-08-30.md`](docs/validation-src-vs-src.orig-2026-08-30.md) — `lint 0 + typecheck 0 + 16/92 + 35 E2E + 380.19 kB` green at time of audit.

**Scope:** Did `src/` (5 Bukit Batok East Ave 2 / T08CC4053H / 1957–2026, 52 files) adopt every good contract from `src.orig/` (620 Upper Bukit Timah / T08CC4043C / 1845–2017, 52 files) and improve where the port demanded? Parish facts *must* differ; design *must not* regress. `src.orig/` is archived, ignored via `.gitignore` (not committed).

**Verdict — 10/10 adopted, 7 improved, 0 regression:**

| Dimension | Adopted? | Improved? | Evidence |
|---|---|---|---|
| 1. Structure & interfaces | ✅ 52 files, 10 pages, 8 interfaces, 92 tests preserved | — | `find src\|wc -l` 52/52, `grep export interface` 8/8 |
| 2. Design system (`@theme` 24+2, 24 utilities, 8 keyframes) | ✅ Tokens byte-identical, 8 keyframes | ✅ `.skip-link` extracted, `link-underline 300ms→0.35s`, motion kill expanded 1→7 | `diff index.css`, `grep @keyframes` 8/8 |
| 3. Components (Layout/Header/SafeImage/Button/BackToTop/SkipLink/Accordion/ScrollProgress/cn) | ✅ All contracts (HashRouter-safe, hash discipline, 44px, grid-rows+inert) | ✅ Header `solid = scrolled\|\|!isHome\|\|mobileOpen`, `ScrollProgress` decoupled to `Layout`, `SafeImage` typed `delete dataset.fallback`, `Button` types cleaned | `diff -u src.orig/components/*` + 11+6+6… tests |
| 4. Routing & nav (17 entries, 5 alias groups/7 aliases, 9 anchors) | ✅ Routes identical, shape `NavItem` identical | ✅ CDN `naveCdn/courtyardCdn` Pexels→local, alias groups preserved | `grep -c Route` 17/17 |
| 5. Data single-source (`content.ts`/`site.ts`/`nav.ts`) | ✅ 8 interfaces preserved | ✅ `Priest.phone→email`, `hours 5→7`, `mass sunday 4→6`, `contact 3→5`, `uen 4043C→4053H`, `images 11 local` | `diff site.ts` |
| 6. Quality gates | ✅ `lint 0 + typecheck 0 + 16/92 + 35 + singlefile` | ✅ `dist/images/ 4→8`, `server.watch.ignored` adds `src.orig/**` | `pnpm lint && typecheck && test && build` |
| 7. A11y/perf | ✅ SkipLink hash, focus ring, landmarks, alt, Accordion inert | ✅ Motion kill 1→7, fewer external fetches (legacy CSP retained unused) | `rg prefers-reduced-motion` |

**7 improvements ledger (what `src/` does better):** image locality (all local), header solidity (`||mobileOpen`), motion kill expanded, type safety, `ScrollProgress` decoupling, `.skip-link` extraction, parish fidelity (5 Bukit Batok, 6 Masses, UEN 4053H). No token drift, no route dropped, no test lost.

Recorded in `README.md` (Current audits + File Hierarchy `docs/`) and `AGENTS.md` (Where to look next) and `CLAUDE.md` (Continuous Improvement + Validation Checklist row 15). Re-run `lint && typecheck && test && test:e2e && build` before claiming regression.

---

## Appendix F — Migration Note (St Mary → Risen Christ)

> `src.orig/` is now **St Mary of the Angels, Bukit Batok** (5 Bukit Batok East Ave 2, Portiuncula, OFM, WOHA 2004/2006) — the previous port. `src/` is **Church of the Risen Christ, Toa Payoh** (91 Toa Payoh Central 319193, blessed 1971 first air-con, Ho Ping Centre). Design tokens + routing + motion system are unchanged; only parish narrative and `site.ts`/`content.ts`/`nav.ts` changed.

| Area | St Mary (`src.orig`) | Risen Christ (`src`) |
|---|---|---|
| `package.json` | `st-mary-of-angels` 1.2.0 | `risen-christ-church` 1.3.0 |
| `site.name` | Church of St Mary of the Angels / St Mary's Bukit Batok / 天神之后圣母堂 | Church of the Risen Christ / Risen Christ Toa Payoh / 耶稣复活堂 |
| `site.tagline/vision` | Towards a Prayerful & Missionary Parish. / According to Thy Word. | Grateful, Faithful, and Sent. / He is risen. |
| `site.address` | 5 Bukit Batok East Ave 2 659918 | 91 Toa Payoh Central 319193 |
| `site.hours` | 7 keys (columbarium) | 6 keys (mediaCentre Tue&Fri 12–16…, no columbarium) |
| `site.mass` | 7/12.15/18.30, Sat 16/18+Tamil 19.45, Sun 6, confession wknd 7 slots | 6.30a/6p, Sat 6.30a+5.30p, Sun 5, confession approach priest, monthly Bahasa/Tamil/Tagalog |
| `site.transport` | NS2/DT5 + buses Ave 2/3/4/6 | NS19 Exit A + buses 88/157/163 B52261 |
| `site.feast` | Our Lady of the Angels · Portiuncula 2 Aug | The Risen Christ — Easter Sunday |
| `site.uen` | T08CC4053H + HRSM, telegram/whatsapp | T08CC4042G (no HRSM), freeMinistry/ssvp/bulletin/cep |
| `priests` | 4 OFM (Esmond/Julian/Justin/Robin) | 3 (Brian D'Souza, Arun Bellarmin, Dexter Chua — each phone+email) |
| `ppcMembers` | 6 (friars ex-officio + Custody) | 7 (Secretariat Peter Quek / Admin Audrey Rozario / Youth Calvin Swee / Pastoral Cheryl-Anne Goh) |
| `lifeTimeline` | 1957–2026 Franciscan/WOHA | 1969–2026 Toa Payoh (Ho Ping→first air-con→2003 wing→Simbang Gabi→Jubilee) |
| `grounds` | main-church/chapel/rosary-garden (Garden of Peace) | main-church/Adoration Room/parish-hall & Media Centre |
| `faqs/events/giving` | Portiuncula/columbarium/WOHA… | Velankanni/CEP/F.R.E.E./Adoration Room… |
| Tests | 25 files / 141 + 42 E2E green | 32 files / 179 + 48 E2E green (Risen Christ fixtures ported 2026-08-31; round-7 design round + tiered audit + remediation same day) |
| `index.html` CSP | img-src wikimedia/pexels legacy + google | img-src 'self' data: blob: only + google |
| Tokens/routing/motion | shrine-* 24+2, 17 routes, Sacred Motion | **unchanged** — same tokens/routes/motion |

Skill filename: `st-mary-of-angels_SKILL.md` is now a redirect stub → `risen-christ_SKILL.md` (canonical). `rothershrine-v2_SKILL.md` remains the lineage stub.

## Quick Reference Card

| Need | Path |
|---|---|
| Visitor overview | `README.md` |
| 60-sec agent cheat sheet | `AGENTS.md` |
| Deep workflow + parish fidelity | `CLAUDE.md` |
| Intent lineage | `docs/prompts.md` (if present) |
| Tokens (25 colors + 2 shadows) + utilities (27 + 8 keyframes) | `src/index.css` (`--font-sans` alias `--font-body`; utilities incl. `gold-rule`/`gold-rule-left`/`hero-ken-burns`/`rise-in`+`rise-in-d1..d4`/`menu-in`/`drawer-in`/`dot-pulse`/`card-lift`/`link-underline`/`reveal`+`reveal-visible`/`skip-link`/`divider-weave`+`divider-weave-thin`/`bg-grain`+`bg-adobe-texture`+`bg-gold-bloom`/`mask-fade-b`/`img-zoom`/`page-in`/`drawer-item-in`) |
| Route table + aliases + anchors | `src/App.tsx` — 17 Route entries (16 content paths + `*`), 7 alias paths in 5 groups (see §5.4), 9 hash anchors (3 on `/worship`, 6 on `/ministries`) |
| Nav single-source | `src/data/nav.ts` (`primaryNav` 6 + `footerNav` 10, with `description` on children) |
| Content arrays (10) + images + site | `src/data/content.ts` (`priests` 3 (phone+email), `ppcMembers` 7 (3 priests + Secretariat/Admin/Youth/Pastoral), `lifeTimeline` 8 [1969–2026 Toa Payoh], `grounds` 3 (main-church/Adoration Room/parish-hall), `ministries` 6 (Language Communities last), `faqs` 6, `upcomingEvents` 6 (Velankanni/CEP/F.R.E.E., 2 with href), `givingOptions` 8 (PayNow T08CC4042G etc.), `serveRoles` 4 (summary), `devotions` 6 + `images` 11 all-local) + `src/data/site.ts` (`site as const`: hours 6 + mass (sunday[5] + monthly + note) + transport NS19/88-157-163 + feast Easter Sunday + uen T08CC4042G + cheque + 3 socials + freeMinistry/ssvp/bulletin/cep + maps + origin) |
| Primitives | `src/components/ui/*` (Button/Container/SectionHeading/Accordion/Reveal) + SafeImage/Emblem/SkipLink/Timeline/SocialIcons/PageHero/Layout/Header/Footer |
| Hooks | `src/hooks/` — `useScrolled.ts` (threshold 12 default; Header uses 16) + `useScrollProgress.ts` (rAF; BackToTop ring + ScrollProgress rail) + `useScrollSpy.ts` (round-7 Ministries jump-nav; document-order tie-break per round-7 audit L-2) |
| Merge helper + mass-day mapping + deep links | `src/utils/cn.ts` (`twMerge(clsx)`) + `src/utils/massDay.ts` (`massDayKey(date)` — drives the Worship today-highlight) + `src/utils/deepLinks.ts` (`knownRoutePaths` + `resolveHashRedirect` — round-12 F-3: path-style deep links rewrite to hash routes pre-mount; drift-guarded against `App.tsx`) |
| Images | `public/images/*.jpg` (8 files → `dist/images/`) + `public/favicon.svg` — all local (`naveCdn`→`sanctuary.jpg`, `courtyardCdn`→`rosary-garden.jpg` are local aliases) + `images` export (11 keys all `/images/*`, `SafeImage` with `hero-church.jpg` fallback) |
| Vite alias + singlefile | `vite.config.ts` (`@→src`, `viteSingleFile()` + `test {globals,jsdom,setupFiles,include,exclude}` + `server.watch.ignored` [skills,dist,playwright-report,test-results,coverage,src.orig]) |
| TS strict + include | `tsconfig.json` (`strict` + `noUnused*` + `noFallthroughCasesInSwitch`/`isolatedModules`/`noEmit` + `include: ["src","vite.config.ts","eslint.config.js","playwright.config.ts","playwright.built.config.ts"]` + `types: ["node","vitest/globals"]` + `paths @/*` + `baseUrl:"."`) |
| Pre-ship gate | `pnpm lint && pnpm typecheck && pnpm test && pnpm test:e2e && pnpm build` → 35/202 + 51 E2E green → `dist/index.html` + `dist/_headers` + `dist/favicon.svg` + `dist/images/` (8 files) → `pnpm preview` → manual smoke (see §11) |
| Frozen reference | (pruned round-12, audit F-9) `src.orig/` was the archived St Mary of the Angels port (Rother→St Joseph→St Mary lineage) for diff reference — discovered still tracked (64 files) and removed from tree + index 2026-08-31; `.gitignore` entry + `repo-hygiene` guard prevent re-entry; lineage history: Appendix D/F + git history |
| CSP allowlist | `index.html` — `img-src 'self' data: blob:` (all images local), `frame-src` `https://www.google.com` (maps embed), `script-src` + `static.cloudflareinsights.com` — `SafeImage` fallback `/images/hero-church.jpg` |
| Audit ledger + remediation | `docs/code-review-audit-round6-2026-08-31.md` + `docs/remediation-plan-round6-2026-08-31.md` (round 6) · `docs/code-review-audit-round7-2026-08-31.md` + `docs/remediation-plan-round7-2026-08-31.md` (round-7 audit of the "Honest Light" commits — zero new C/H/M; scrollspy tie-break + E2E sleep remediation) · `docs/design-enhancement-round7-2026-08-31.md` (round-7 design) · `docs/remediation-plan-round9-2026-08-31.md` (round-9 built-artifact E2E contract — E2E-L1 favicon form + `playwright.built.config.ts`) · `docs/e2e-live-pass-round11-2026-08-31.md` (round-11 live pass vs `66d2398` — byte-verified deploy + tri-env 48/48 + journey 43/43; E2E-J1 `agent-browser eval` backslash lesson → pitfall #15) · `docs/UI-UX-Design-Audit_StMaryOfAngels_vs_RisenChrist.md` + `docs/remediation-plan-round12-2026-08-31.md` + `docs/remediation-round12-2026-08-31.md` (round-12 comparative UI/UX audit remediation — F-1 Devotion chip to AA terracotta-600 5.36:1, F-2 mass-card footnote /85 + date lock, F-3 path-style deep-link rewrite, F-4 Give UEN out of the heading into a copyable PayNow row, F-9 src.orig prune; TDD red→green, 35/202 + 51 E2E) |
