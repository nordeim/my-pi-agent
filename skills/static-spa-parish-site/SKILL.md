---
name: static-spa-parish-site
description: Complete engineering reference for static SPA parish/church/nonprofit/community brochure sites — React 19 + Vite 7 + Tailwind CSS v4 CSS-first @theme + TypeScript + HashRouter + vite-plugin-singlefile (single dist/index.html for GH Pages/S3, no SSR/CMS). Covers design system, component architecture, file-backed typed content, routing alias/anchor contracts, WCAG AAA, and pre-ship gates. Use when building, extending, debugging, onboarding, cloning, replicating, re-porting this parish-site family or scaffolding any static content-driven marketing/brochure/landing site template.
version: 3.0.0
---

# Parish Site Engineering Skill — Unified v3 (Church of the Risen Christ, Toa Payoh — canonical instance)

package_version: 1.4.4 (repo `package.json` — the SKILL doc version and the package version are separate axes; see §0)
project_state: "static SPA — 77 src files (41 source + 35 tests + 1 setup) / 202 unit tests + 51 E2E green — canonical instance is the Risen Christ port of www.risenchrist.org.sg; lineage Rother → St Joseph BT → St Mary of the Angels → Risen Christ"
verified: pnpm lint 0 + pnpm typecheck 0 + pnpm test 35/202 + pnpm test:e2e 51 + pnpm test:e2e:built 51 + pnpm build 397.52kB → dist/index.html + dist/_headers + dist/favicon.svg + dist/images/8
stack: react 19.2.8 / vite 7.3.6 / tailwind 4.3.3 (@tailwindcss/vite 4.1.17) / typescript 5.9.3 / react-router 7.18.2 / singlefile 2.3.3 / eslint 9.39.5 flat / vitest 3.2.6 jsdom / testing-library 16.2.0 / playwright 1.55.1 chromium (51 E2E green ×2 passes)
rendering: static SPA (HashRouter, no SSR)
data_layer: file-backed typed arrays in src/data/* + const site object
deploy: vite-plugin-singlefile → dist/index.html + dist/images/ → GH Pages / S3 (publicDir copy — not inlined)
unified_from: "rothershrine-v2_SKILL.md (st-joseph-bt hop 1) + st-mary-of-angels_SKILL.md (hop 2) + risen-christ_SKILL.md (hop 3) — unified 2026-09-01; per-hop history preserved in Appendix D; unification ledger in Appendix G"
port_provenance: Singapore port of https://www.risenchrist.org.sg/ — Church of the Risen Christ, 91 Toa Payoh Central, Singapore 319193 — first Catholic church in the new town, blessed 3 July 1971 (first air-con, Fr Pierre Abrial); lineage Rother Shrine → St Joseph BT → St Mary of the Angels (src.orig, pruned round-12) → Risen Christ (src) — see Appendices D+F

> **How to use this document:** This is the single-source-of-truth for any future agent extending, debugging, onboarding, replicating, or **re-porting** the parish-site family. Read §0 first (the volatile-facts register — the only place mutable numbers live), then §§ 1–4 for identity and constraints, §5 for where to put code, §§ 9–11 before shipping, and §§ 15–20 as copy-pasteable contracts. Every version, hex, and path is verified against `package.json` / `src/index.css` / `tsconfig.json` / `src/data/*` — if it drifts, fix this file first.

**Sources of truth:** `README.md` (visitor overview) → `AGENTS.md` (60-sec cheat sheet) → `CLAUDE.md` (deep workflow, 6-phase) → this file (complete distillate). If they conflict, trust executable config.

**Unification note (v3, 2026-09-01):** This file merges and supersedes the three lineage SKILL files — `rothershrine-v2_SKILL.md` (hop 1: St Joseph BT), `st-mary-of-angels_SKILL.md` (hop 2: St Mary of the Angels), and `risen-christ_SKILL.md` (hop 3: Risen Christ, the canonical instance). The sectional skeleton (§§ 1–20 + Appendices + Quick Ref) is preserved; the **best elements of each hop were combined** (hop-3 body as base — it is the most internally coherent — plus hop-2's src-vs-src.orig validation method, hop-1's migration diff discipline, and each hop's unique lessons). Every cross-file conflict found in the 2026-09-01 re-audit was resolved exactly once, and every resolution is recorded in **Appendix G (Unification & Audit Ledger)**. The lineage files are retained as redirect stubs — do not edit them independently; all future updates go here.

**What v3 fixes structurally (the systemic root cause):** the three source files restated every volatile fact (test counts, file counts, color counts, version numbers, CSP allowlists, src.orig policy) **5–8 times each**, and each hop's appendices were copy-forwarded **without a previous-parish fossil sweep** — so the older a fact, the more stale copies of it survived (evidence per file in Appendix G). v3 therefore introduces:

1. **§0 — Volatile Facts Register.** The *only* section allowed to state a mutable number. Every other section **references** §0 ("see §0") instead of restating. Historical snapshots are permitted *only* in the lineage appendices, and only with an explicit **`as of <date>`** label.
2. **A completed contracts layer.** §4.3 now lists all 27 utility classes and all 8 keyframes; §18 gains the `z-[60]` scroll-rail row; §6 covers all three hooks; §5.2's tree includes every hook/util the test harness proves exists; §20's `SafeImageProps` includes `fetchPriority`.
3. **A fossil-sweep protocol** (Appendix G.4) that any future port must run before its doc ships — the checklist that would have caught every defect catalogued in Appendix G.

---

## 0. Volatile Facts Register (SINGLE SOURCE OF TRUTH)

> **Contract:** this table is the only authoritative statement of every mutable fact in this document. If any other section (or `README`/`AGENTS`/`CLAUDE`) disagrees, **this table wins until the repo is re-verified, then all copies are fixed to match it in the same commit**. When a fact changes, change it here first, then grep the doc for stale copies (`rg -n "<old value>"`) — see Appendix G.4.

| Fact | Value (as of 2026-08-31, round-12) | Where else it is referenced (must agree) |
|---|---|---|
| Canonical instance | Church of the Risen Christ, Toa Payoh — `risen-christ-church` repo, `package.json` version **1.4.4** | §1, §2, Appendix F |
| This SKILL doc version | **3.0.0** (unification axis — independent of package version) | frontmatter, Appendix G |
| Unit tests | **35 files / 202 tests — green** (sum verified: 4+3+16+5+7+10+8+5+7+7+11+3+6+6+17+7+2+5+3+6+6+4+3+2+3+6+3+2+2+2+4+6+2+13+6 = 202) | §2, §3.1, §5.2, §10, §11, App C |
| E2E tests | **51 tests — green, 8 specs** (`smoke 11 + navigation 8 + ministries 4 + give-faq 4 + enhancements 7 + enhancements-round5 6 + enhancements-round7 8 + deep-links 3` = 51) — plus the same 51 green on the built-artifact pass (`pnpm test:e2e:built`) | §2, §3.1, §3.2, §11, App C |
| `src/` inventory | **77 files = 41 source + 35 tests + 1 setup** (`find src -type f \| wc -l` → 77) | §5.2 |
| `public/images/` | **8 files** (`hero-church`, `chapel-interior`, `sanctuary`, `rosary-garden`, `stained-glass`, `parish-hall`, `cemetery`, `feast`) + `public/favicon.svg`; all images local | §5.2, §11, App B |
| Build artifact | `dist/index.html` **397.52 kB** (JS+CSS inlined) + `dist/_headers` + `dist/favicon.svg` + `dist/images/` (8 files, publicDir copy) | §2, §11, Quick Ref |
| Design tokens | **25 colors + 2 shadows (27 `@theme` entries)** — 24 base colors + `terracotta-600 #8f4c30` (round-12 AA step). *Lineage note:* hop 2 (St Mary) round-7 also added `gold-700 #85601f` (4.72:1) — the Risen Christ line does not carry it; re-add it deliberately if a text-bearing gold step is needed | §4.1, §4.4, §19, ADR-3 |
| Utilities / keyframes | **27 utility classes + 8 keyframes** (27 counts each `rise-in-d1..d4` delay class individually) + themed scrollbar + `@media print` reveal override | §4.3, §5.2, Quick Ref |
| Hooks | **3** — `useScrolled`, `useScrollProgress`, `useScrollSpy` (round-7) | §6, §5.2, Quick Ref |
| Utils | **4** — `cn`, `massDay`, `monogram`, `deepLinks` | §5.2, §20, Quick Ref |
| Routes | **17 `Route` entries** (16 content paths + `*`), **7 alias paths in 5 groups**, **9 hash anchors** (3 on `/worship`, 6 on `/ministries` — sixth ministry id is `#language-communities`, **not** the legacy `mandarin` anchor) | §5.4, App B |
| CSP `img-src` | **`'self' data: blob:` only** (round-6 tightened; wikimedia/pexels legacy hosts removed — all images local). `frame-src https://www.google.com` (maps embed). `script-src` allows inline (singlefile) + `static.cloudflareinsights.com` | §3.2, §11, Quick Ref |
| `src.orig/` policy | **PRUNED** round-12 (2026-08-31): was the archived St Mary port, discovered still tracked (64 files — F-9: `.gitignore` does not untrack), removed from tree + index; `repo-hygiene` guard now fails if any `src.orig` path re-enters. Lineage history lives in Appendices D/F + git history only | §2, §3.2, §11, §13, ADR-6 |
| `skills/` policy | Vendored reference content — pruned round 3 (2026-08-30, full tree at `c774ed9`), **re-added in full in `0be0fe8` (2026-08-31)**; tooling (eslint/tsconfig/vite watch) still excludes it — never import or lint it | §2, §3.2, §13, §14 |
| Secrets | `docs/ssh-key.txt`: **key must be rotated by the repo owner** — tracked in `0be0fe8`, untracked round 6 (C1), **still present in git history**. `package-lock.json` untracked since round 3 (H-1) | §2 (top notice), §3.2, §11, App G |
| Data arrays | `lifeTimeline` 8 (1969–2026) · `grounds` 3 · `ministries` 6 · `faqs` 6 · `upcomingEvents` 6 (2 with `href`) · `givingOptions` 8 · `priests` 3 (phone+email) · `ppcMembers` 7 · `serveRoles` 4 · `devotions` 6 · `images` 11 (all local) · `nav` primary 6 / footer 10 · `site` hours 7 keys / mass 9 keys (incl. `sunday`, `note`, `monthly`) | §7, §20, Quick Ref |
| Parish constants | 91 Toa Payoh Central, Singapore 319193 · UEN **T08CC4042G** · feast: Easter Sunday · MRT Toa Payoh NS19 Exit A · buses 88/157/163 (B52261) · office +65 6253 2166 · parish priest +65 6255 7509 · media centre +65 6356 5958 | §1, §7, §20 |
| Pre-push gate | `pnpm lint && pnpm typecheck && pnpm test && pnpm test:e2e && pnpm build` (+ `pnpm test:e2e:built` before shipping) — **all green 2026-08-31** | §3.1, §11, App C |

---

## Table of Contents

0. [Volatile Facts Register (Single Source of Truth)](#0-volatile-facts-register-single-source-of-truth)
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
- [Appendix D — Lineage & Migration History (Rother → St Joseph BT → St Mary → Risen Christ)](#appendix-d--lineage--migration-history)
- [Appendix E — Hop-2 Validation: St Mary src vs St Joseph src.orig (2026-08-30)](#appendix-e--hop-2-validation-st-mary-src-vs-st-joseph-srcorig-2026-08-30)
- [Appendix F — Hop-3 Diff: St Mary → Risen Christ](#appendix-f--hop-3-diff-st-mary--risen-christ)
- [Appendix G — Unification & Audit Ledger (v3)](#appendix-g--unification--audit-ledger-v3)
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
| Hours | 7 keys: `gates`, `mainChurch`, `chapel` (Adoration Room Mon 12–22 / Tue–Sat 7–22 / Sun 7–18), `reception`, `parishOffice`, `mediaCentre` (Tue & Fri 12–16 / Sat 12–19 / Sun 8–13), `adorationRoom` (same as chapel) | `site.hours` |
| Transport | MRT Toa Payoh NS19 — 6 minutes' walk from Exit A; buses 88, 157, 163 — 2 minutes from stop B52261 | `site.transport` |
| Contacts | Parish priest +65 6255 7509, office +65 6253 2166, media centre +65 6356 5958, emails `crc.secretariat@catholic.org.sg` · `crc.admin@` / `crc.pastoral@` / `crc.youth@` / `dpo.crc@catholic.org.sg` | `site.contact` |
| Giving identity | UEN **T08CC4042G**, cheque payable **Church of the Risen Christ** | `site.uen / site.chequePayee` |

**Design thesis — "Reverent, not austere":** Warm parchment/maroon/gold on cream, generous whitespace, Fraunces display + Source Sans 3 body. Every page is a welcome from Toa Payoh Central — the 1971 first air-con nave, the Adoration Room, the parish hall & media centre — not a brochure. No purple gradients, no `Inter` defaults, no generic card-grid templates.

**Non-negotiable rules:**

1. **Parish fidelity over pixel theft** — rephrase narrative, preserve Singapore facts exactly (1969–2026 Toa Payoh details: Ho Ping Centre, 1971 Olçomendy blessing, first air-con $450k, Velankanni, Simbang Gabi, 91 Toa Payoh Central, Mass 6.30a/6p + Sat 5.30p + Sun 5 Masses, UEN T08CC4042G). Never reintroduce St Mary of the Angels / Bukit Batok / St Joseph BT / Rother Shrine narratives outside the historical appendices — this is Church of the Risen Christ.
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

> All versions pinned exact (no `^`) in `package.json` (`pnpm@11.0.0`, `engines: node>=20`). Re-pin on upgrade; `pnpm --frozen-lockfile` in CI verifies lockfile. `package.json` version is **1.4.4** (see §0 — the SKILL doc version 3.0.0 is a separate axis).

**Environment:** No `.env`, no DB, no auth, no docker. `pnpm` is the supported manager (`--frozen-lockfile` in CI). `npm ci` fails on these exact pins (typescript-eslint 8.28.0 peer range predates TS 5.9) — use `npm ci --legacy-peer-deps` if npm is unavoidable. `skills/` is vendored reference content — pruned in round 3 (2026-08-30) and re-added in full (catalog + per-skill `SKILL.md` files, commit `0be0fe8`, 2026-08-31); tooling (eslint ignores, tsconfig excludes, vite watch ignores) still excludes it — do not import or lint it. No `package-lock.json` in the repo (untracked, round 3). `docs/ssh-key.txt` was accidentally tracked in `0be0fe8` and untracked again in round 6 (`git rm --cached`; round-6 audit C1) — **the leaked key must be rotated by the repo owner**; history still contains it. `src.orig/` was the **archived St Mary of the Angels** port (Rother→St Joseph→St Mary lineage) — discovered still tracked (64 files) by the round-12 comparative-audit remediation (F-9: `.gitignore` listed it since round 3 but ignore rules do not untrack) and pruned 2026-08-31 (`git rm -r --cached` + tree removal; `repo-hygiene` guard now fails if any `src.orig` path re-enters the index; lineage history lives in Appendices D/F + git history).

**Test harness — current reality (2026-08-31, round-6 verified; counts authoritative in §0):**

| Suite | Status | Detail |
|---|---|---|
| `vitest` unit (`pnpm test`) | **35 files / 202 tests — green** | `ci-workflow` 4 + `repo-hygiene` 3 + `docs-contract` 16 + `utils/cn` 5 + `data/nav` 7 + `data/content` 10 + `data/site` 8 + `utils/massDay` 5 + `utils/monogram` 7 + `utils/deepLinks` 7 + `ui/Button` 11 + `SkipLink` 3 + `ui/Accordion` 6 + `SafeImage` 6 + `Header` 17 + `BackToTop` 7 + `ui/Reveal` 2 + `components/wcag-contrast` 5 + `pages/Ministries` 3 + `pages/cta-bands` 6 + `pages/worship-mass` 6 + `pages/about-visuals` 4 + `pages/event-chips` 3 + `pages/give-featured` 2 + `pages/give-uen` 3 + `pages/card-affordances` 6 + `components/Timeline` 3 + `pages/NotFound` 2 + `pages/History` 2 + `Layout` 2 + `hooks/useScrollProgress` 4 + `hooks/useScrollSpy` 6 + `ScrollProgress` 2 + `head` 13 + `security-headers` 6 via `src/test/setup.ts` (jest-dom + IntersectionObserver mock + scrollTo/scrollIntoView stubs + matchMedia stub). Data values per §0. `vite.config.ts test { globals, jsdom, setupFiles, include, exclude }` keeps `e2e/**` out. |
| `playwright` E2E (`pnpm test:e2e`) | **51 tests — green** | 8 specs `smoke 11 + navigation 8 + ministries 4 + give-faq 4 + enhancements 7 + enhancements-round5 6 + enhancements-round7 8 + deep-links 3` (chromium) — Toa Payoh (Risen Christ) routes `/worship`/`/ministries`/`/serve`/`/give` + `#mass`/`#liturgical` etc. + `SafeImage` fallback via `route.abort` + mobile drawer same-route close regression + rise-in hero entrance + event chips + back-to-top + aria-current nav states + Round-2 audit (CTA-band cream, head completeness, page-in, progress rail/ring, drawer aria-current) + Round-4 (mobile drawer modal: dialog + `aria-modal` + trapped focus + Escape focus restore; scroll-rail deterministic mid-depth landing) + Round-5 (Worship today-Mass card via `utils/massDay` + Sunday gold-dot list, gold category chips + display-serif dates, Give closing band h2 cream, sticky History story `lg:sticky`, gradient timeline rail, `.img-zoom` grounds/ministries drift, `.bg-gold-bloom` dark bands, Button aria-hidden icon nudge, About ghost numerals + monogram discs, NotFound ghost emblem + rise-in) + Round-7 "Honest Light" (print-media reveal override + IO try/catch fallback + early-entry `rootMargin`, Worship sticky mercy column, News bulletin + FAQ office closure bands, Give featured PayNow card, Ministries scrollspy via `hooks/useScrollSpy`, About PPC hover tint + `link-underline` priest contacts, desktop nav `after:` gold hairline (scale-x 0→100), `card-tint` info-card honesty system, PageHero atmosphere 35→45) + Round-12 audit (path-style deep links `/worship`/`/news-events`/`/donate` land on their pages, not Home). |
| `playwright` built-artifact E2E (`pnpm test:e2e:built`) | **51 tests — green** | Same 51 specs against `dist/` via `vite preview :4173` (or the live host via `E2E_BASE_URL`) — `playwright.built.config.ts`; exists because singlefile rewrites root-relative asset refs (round-9 E2E-L1, §9 #14) |
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
pnpm test               # → vitest 3.2.6 jsdom — 35 files / 202 tests green (per-file breakdown: §0/§2)
pnpm test:e2e           # → playwright 1.55.1 chromium — 51 tests green (8 specs, §0)
pnpm test:e2e:built     # → playwright vs built artifact (playwright.built.config.ts — vite preview :4173; E2E_BASE_URL → live host, webServer skipped) — same 51 tests green
pnpm build              # → dist/index.html + dist/images/ (viteSingleFile 2.3.3 inlines JS+CSS; publicDir copied)
pnpm preview            # → http://localhost:4173 (preview dist)
```

**Pre-push gate — all five must be green (six with the built pass):**

```bash
pnpm lint && pnpm typecheck && pnpm test && pnpm test:e2e && pnpm build
pnpm test:e2e:built    # before shipping — dev-only asset-path assertions cannot pass here (§9 #14)
```

### 3.2 Critical Config Files

| File | Purpose | Gotcha |
|---|---|---|
| `vite.config.ts` | `plugins: [react(), tailwindcss(), viteSingleFile()]` + `resolve.alias["@"]` + `test { globals, jsdom, setupFiles: src/test/setup.ts, include: src/**/*.{test,spec}.{ts,tsx}, exclude: e2e/** }` + `server.watch.ignored [skills/**, dist/**, playwright-report/**, test-results/**, coverage/**, src.orig/**]` | `test` keeps `e2e/**` out of unit runs; `server.watch.ignored` prevents `ENOSPC` from vendored `skills/` tree (large `.venv`). `@` must stay in sync (`vite.config.ts` ↔ `tsconfig.json` `paths`). |
| `tsconfig.json` | `ES2020`/`ESNext`/`bundler`/`react-jsx`/`strict`/`noUnused*`/`isolatedModules`/`noEmit` + `include ["src","vite.config.ts","eslint.config.js","playwright.config.ts","playwright.built.config.ts"]` + `types ["node","vitest/globals"]` + `paths {"@/*":["src/*"]}` + `baseUrl:"."` | `include` covers `src` + all config files (so `eslint.config.js` + `playwright.config.ts` + `playwright.built.config.ts` are type-checked). `types [vitest/globals]` required for `describe/it/expect` globals. Adding a file outside `src/` requires expanding `include`. |
| `eslint.config.js` | flat config (`eslint 9.39.5` + `@eslint/js 9.39.5` + `typescript-eslint 8.28.0` + `react-hooks 5.2.0` + `react-refresh 0.4.19` + `globals 16.1.0`) — ignores `dist/node_modules/coverage/playwright-report/test-results` **and `skills` and `src.orig`** | Flat. `pnpm lint:fix` → `eslint . --fix`. Ignoring `skills` + `src.orig` is what keeps the gate green. Never re-add `src.orig/` to lint/tsc. |
| `playwright.config.ts` | `playwright 1.55.1` (`@playwright/test 1.55.1` chromium, `webServer` → `pnpm exec vite --port 5173 --host 127.0.0.1 --strictPort`) | `testDir: e2e`, `baseURL: http://localhost:5173`, `reuseExistingServer: !CI`, `expect.timeout: 15s`, `trace/video on failure`. **Green** — 51 tests per §0. |
| `playwright.built.config.ts` | Extends the base config — `baseURL = E2E_BASE_URL ?? http://127.0.0.1:4173`; `webServer: pnpm exec vite preview --port 4173` (skipped when `E2E_BASE_URL` is set) | Built-artifact pass (`pnpm test:e2e:built`): runs the same 51 tests against `dist/` via `vite preview`, or against the live host via `E2E_BASE_URL`. Exists because the singlefile pipeline rewrites root-relative asset refs (`/favicon.svg` → `./favicon.svg`) — dev-only assertions pass on `pnpm dev` and fail on the built artifact (round-9 E2E-L1). |
| `e2e/` | 51 tests — `smoke.spec.ts` (11), `navigation.spec.ts` (8), `ministries.spec.ts` (4), `give-faq.spec.ts` (4), `enhancements.spec.ts` (7), `enhancements-round5.spec.ts` (6), `enhancements-round7.spec.ts` (8), `deep-links.spec.ts` (3) + `helpers.ts` | **green** — full round coverage per §2 E2E row: anchors + aliases + `SafeImage` fallback + drawer same-route close regression + modal drawer focus trap (round-4) + rise-in entrance + event chips + back-to-top ring + aria-current nav + ScrollProgress rail + path-style deep-link redirects (round-12) + round-7 print reveal / sticky mercy column / cream-gold bands / scrollspy pill / nav hairline scale / home event links / FAQ loop-back |
| `.github/workflows/ci.yml` | CI: lint → typecheck → test → test:e2e (chromium) → build + artifacts | `pnpm 11`, `node 24`. All five green — `dist/` + `playwright-report/` artifacts. Drift-guarded by `src/ci-workflow.test.ts` (4 tests). |
| `src/index.css` | `@import "tailwindcss"` + `@theme` (25 colors + 2 shadows, §0) + `@layer base/utilities` (27 utilities + 8 keyframes, §4.3) + themed scrollbar in `@layer base` + `@media print` reveal override | Only token source; no `tailwind.config.*` exists. |
| `index.html` | `lang en`, `viewport`, `meta description`, scoped `Content-Security-Policy` meta + `referrer` meta, `/favicon.svg` link + `theme-color #200a0a`, full OG (`og:url`/`og:site_name`/`og:locale`/`og:image`+`og:image:alt`) + `twitter:card summary_large_image` + Church JSON-LD (drift-checked by `src/head.test.ts`), preconnect `fonts.googleapis.com`, `Fraunces`+`Source Sans 3`, `#root` + `src/main.tsx` | CSP allows inline script/style (singlefile) + Google Fonts; `img-src 'self' data: blob:` (all images local — no wikimedia/pexels allowlist, §0), `frame-src https://www.google.com` (maps embed), `script-src` + `static.cloudflareinsights.com`. Social share + search-engine identity for Church of the Risen Christ (www.risenchrist.org.sg, Easter Sunday). |
| `.gitignore` | Ignores `node_modules/`, `.next/`, `dist/`, `skills/`, `src.orig/`, `docs/ssh-key.txt`, `package-lock.json` + `nohup.out`, `.venv`, `bak.git/` | `skills/` is committed vendored reference (catalog re-added in `0be0fe8`) — the ignore entry is inert for tracked files, tooling ignores apply instead. `package-lock.json` untracked since round 3. `docs/ssh-key.txt` was tracked in `0be0fe8` and untracked in round 6 (C1) — ignore entry now effective for it; **rotate the key** (§0). `src.orig/` was still tracked despite this entry (round-12 F-9 found 64 files; pruned 2026-08-31 — the ignore entry is effective now, `repo-hygiene` guard enforces). |

**Env vars:** None. `VITE_*` prefix convention applies if added; guard with `src/env.d.ts` (`import.meta.env`). Document new vars in `README.md` + `CLAUDE.md` + this §.

---
## 4. The Design System (Code-First)

**Single source:** `src/index.css` `@theme` block. No `tailwind.config.*`. Tokens are **unchanged from the rothershrine → St Joseph BT → St Mary line** except the round-12 `terracotta-600` addition (§0) — the imagery and copy they frame is now Toa Payoh: the 1971 first air-con nave, the Adoration Room, the parish hall & media centre — still warm parchment/maroon/gold on cream.

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
  /* Lineage note: hop-2 (St Mary) round-7 also defined --color-shrine-gold-700: #85601f (4.72:1 AA text step).
     The Risen Christ line does not carry it — re-add deliberately (with a §19 row) if a text-bearing gold step is needed. */

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

### 4.3 Custom Utilities (`@layer utilities`) — complete register

> **v3 fix:** the three source files' §4.3 tables listed only the hop-1 subset (~18 rows) while §3.2 claimed 27 utilities, and their keyframe prose listed 6 while claiming 8. This table now enumerates **all 27 utility classes** (counting each `rise-in-d1..d4` delay class individually, which is how the 27 is derived) and **all 8 keyframes**. If you add a utility, add its row here *and* update the count in §0 — never leave the two out of sync.

| # | Name | CSS | Purpose |
|---|---|---|---|
| 1 | `.text-balance` | `text-wrap: balance` | Hero + heading line-wrap |
| 2 | `.bg-adobe-texture` | double radial gradient (white 0.06 + black 0.08) | Subtle adobe wash on dark bands |
| 3 | `.bg-grain` | `data:image/svg+xml` turbulence (`opacity 0.035`) | Grain overlay for hero/dark bands |
| 4 | `.bg-gold-bloom` | radial gold bloom gradient (round-5) | Warm gold wash on dark CTA bands |
| 5 | `.divider-weave` | `repeating-linear-gradient(45deg, gold-500 0 6px, maroon-600 6 12px, pine-600 12 18px)` | `Footer` 6px weave strip + pilgrim bands |
| 6 | `.divider-weave-thin` | `repeating-linear-gradient(90deg, gold 0 10px, maroon 10 20, pine 20 30)` height 3px | Thin weave (hero bottom, footer top) |
| 7 | `.gold-rule` | `linear-gradient(90deg, transparent, gold-500 18%, gold-300 50%, gold-500 82%, transparent)` height 1px + `gold-rule-draw` 0.9s | Centered gold rule (section dividers) |
| 8 | `.gold-rule-left` | `linear-gradient(90deg, gold-500, transparent)` height 1px + `gold-rule-draw` 0.9s | Left-aligned gold rule (eyebrow / `SectionHeading` line) |
| 9 | `.hero-ken-burns` | `scale(1)→1.05` 20s ease-out `hero-ken-burns` | Hero image slow zoom |
| 10 | `.mask-fade-b` | `linear-gradient(to bottom, black 70%, transparent)` | Mask for image fades |
| 11 | `.reveal` | `translateY(24px)→0`, `opacity 0→1`, `0.7s cubic-bezier(0.22,1,0.36,1)` + `prefers-reduced-motion` kill | Scroll-reveal via `Reveal.tsx` + `IntersectionObserver` (print override round-7) |
| 12 | `.reveal-visible` | paired state class of `.reveal` | Applied by `Reveal.tsx` on intersect |
| 13 | `.rise-in` | `rise-in` keyframe: `translateY(20px)→0`, `opacity 0→1`, `0.7s ease-out`, fill `both` | Staged entrance for Home hero + PageHero content (eyebrow→title→copy→CTA) |
| 14 | `.rise-in-d1` | delay 90ms | Stage 2 (title) |
| 15 | `.rise-in-d2` | delay 180ms | Stage 3 (copy) |
| 16 | `.rise-in-d3` | delay 280ms | Stage 4 (CTA) |
| 17 | `.rise-in-d4` | delay 380ms | Stage 5 (extras) |
| 18 | `.menu-in` | `menu-in` keyframe: `translateY(-4px)→0`, `opacity 0→1`, `0.18s ease-out` | Desktop dropdown `<ul>` entrance (runs on conditional mount) |
| 19 | `.drawer-in` | `drawer-in` keyframe: `translateY(-12px)→0`, `opacity 0→1`, `0.24s ease-out` | Mobile drawer panel entrance (runs on conditional mount) |
| 20 | `.drawer-item-in` | staggered item entrance inside the mobile drawer | Drawer link cascade |
| 21 | `.page-in` | keyed route-transition entrance (round-2) | Page wrapper fade/slide on route change |
| 22 | `.dot-pulse` | `::after` gold ring `halo-pulse` 2.6s infinite (scale 0.6→1.7 + fade); reduced-motion → `opacity:0` | Timeline dot halo |
| 23 | `.card-lift` | hover `translateY(-4px)` + `shadow-shrine` + gold border tint, 300ms ease-out | Uniform card hover (grounds/devotions/pillars/roles/giving/events) |
| 24 | `.card-tint` | info-card honesty tint (round-7) | Distinguishes informational cards from interactive ones |
| 25 | `.link-underline` | `::after` gold gradient underline, `scaleX(0)→1` 300ms on hover/focus (+ `aria-current` state) | Footer nav, top-bar Give link, priest contacts, WhatsApp links |
| 26 | `.skip-link` | `fixed z-[100] -translate-y-24 → focus:translate-y-0` | Skip-to-content link (`SkipLink.tsx` + `Layout.tsx`) |
| 27 | `.img-zoom` | grounds/ministries image drift-on-hover (round-5) | Image interior pan while card lifts |

**Keyframes (8 — complete):** `gold-rule-draw` (scaleX 0→1) · `hero-ken-burns` · `rise-in` · `menu-in` · `drawer-in` · `drawer-item-in` · `page-in` · `halo-pulse` — all killed/instant under `prefers-reduced-motion` (global 0.01ms override in `@layer base` + `.dot-pulse::after` opacity 0; motion kill expanded 1→7 rules at hop 2). Plus a themed scrollbar in `@layer base` and an `@media print` reveal override (round-7) — neither counts as a utility.

**Accordion collapse contract:** panels animate via `grid-template-rows 0fr↔1fr` (`grid grid-rows-[0fr|1fr]` + inner `overflow-hidden`) — never `hidden`. Closed panels carry `aria-hidden="true"` + `inert`; `aria-expanded` on the button stays the single source of truth (see `docs/ui-ux-remediation-plan-2026-08-28.md`).

### 4.4 Shadows & Radii

- Shadows: `shadow-shrine` (default) + `shadow-shrine-lg` (elevated cards/dropdowns). Radii are `rounded-sm` (buttons/cards) and `rounded-full` (emblem icon). Don't introduce `shadow-lg`/`rounded-xl` without a rationale.

**Verification:** `grep --color shrine- src/index.css` → 25 colors + 2 shadows (27 theme entries, §0); copy-paste `@theme` into this doc to prevent drift. `src/components/wcag-contrast.test.tsx` computes ratios from this token layer (round-12).

---

## 5. Component Architecture & Patterns

### 5.1 Layer Map (SPA — no 5-layer BE model needed)

```
index.html (#root) → src/main.tsx (StrictMode+createRoot + #root guard + resolveHashRedirect pre-mount rewrite)
  → src/App.tsx (HashRouter + Routes + Layout outlet)
    → Layout (Header / Outlet / Footer) + scroll/hash restore + ScrollProgress + BackToTop + keyed page-in
      → Pages (10) → ui/* primitives → utils/cn
      → data/* (nav + content + site) — single-source, typed
```

No global store, no API layer, no `server/` — add only with an ADR.

### 5.2 Directory Inventory (77 files in `src/` — 41 source + 35 tests + 1 setup; authoritative counts in §0)

> **v3 fix:** the source files' trees omitted `hooks/useScrollSpy.ts`, `utils/monogram.ts`, and `utils/deepLinks.ts` even though their own test harnesses and Quick Refs proved they exist. The tree below includes them.

```
src/ (77 files — 41 source + 35 tests + 1 setup)
  App.tsx                 # HashRouter + 17 Route entries (16 content paths + * NotFound; 5 alias groups, 7 alias paths)
  main.tsx                # StrictMode + createRoot + explicit #root guard + resolveHashRedirect pre-mount rewrite (round-12 F-3: path-style deep links land on their page)
  index.css               # @theme (25 colors + 2 shadows) + @layer base/utilities (27 utilities + 8 keyframes + themed scrollbar)
  env.d.ts                # import.meta.env guard (VITE_* convention)
  components/
    Layout.tsx            # Outlet + hash-aware scroll restoration (double-hash aware, 80ms, timeout cleanup) + ScrollProgress (decoupled rail z-[60]) + SkipLink + BackToTop + keyed page-in container
    Header.tsx            # z-50 fixed maroon-950 bar (solid = scrolled||!isHome||mobileOpen; translucent+blur when solid, transparent at top of Home), useScrolled(16) (default 12), hover/focus-open dropdown (no click-toggle — keyboard via onFocusCapture), mobile modal drawer (round-4 L-5: role=dialog + aria-modal + initial focus + Tab/Shift+Tab focus trap + focus restore to hamburger + outside-tap close; Escape handler, parentActive, 44px hamburger, menu-in/drawer-in)
    Footer.tsx            # 4-col + divider-weave-thin + 4 SocialIcons (Facebook/Instagram/YouTube/Telegram) + site.ts address/flows
    PageHero.tsx          # maroon-950 hero (compact?, bg-grain, dual gradients, divider-weave-thin; image alt="" only)
    SafeImage.tsx         # local fallback (fallback=/images/hero-church.jpg, lazy, fetchPriority?, onError→dataset.fallback guard) — all current images local; CDN keys naveCdn/courtyardCdn now local fallbacks
    Emblem.tsx            # inline SVG emblem (crook + wheat, currentColor)
    SkipLink.tsx          # skip-to-#main-content link; preventDefault + imperative focus — never rewrites the hash (HashRouter)
    SocialIcons.tsx       # hand-drawn Facebook/Instagram/YouTube/Telegram glyphs (4)
    BackToTop.tsx         # threshold 480 + SVG progress ring (stroke-dashoffset via useScrollProgress) + reduced-motion, hash-safe
    ScrollProgress.tsx    # fixed gold rail (h-[3px], scaleX progress, aria-hidden, z-[60]) — decoupled from Header, rendered by Layout
    Timeline.tsx          # gradient rail ([data-testid=timeline-rail], fades at both ends) + display-serif gold years + Reveal per entry + dot-pulse halos — fed 1969–2026 Toa Payoh milestones
    ui/
      Button.tsx          # discriminated union (to/href/button) + icon, 4 variants
      Container.tsx       # max-w-7xl mx-auto px-5 sm:px-8
      SectionHeading.tsx  # eyebrow? / title / description + align/light + line (gold-rule-left)
      Accordion.tsx       # FAQ accordion (aria-expanded, grid-rows animation, Plus rotate-45)
      Reveal.tsx          # IntersectionObserver fade+slide (threshold 0.15, fallback visible, prefers-reduced-motion, round-7 IO try/catch + rootMargin)
  hooks/
    useScrolled.ts        # scrollY > threshold boolean (threshold=12 default; Header passes 16)
    useScrollProgress.ts  # 0..1 scroll progress, rAF-throttled, unscrollable guard
    useScrollSpy.ts       # round-7 Ministries jump-nav scrollspy — document-order tie-break per round-7 audit L-2
  pages/                  # Home, About, History, Worship, Ministries, NewsEvents, Serve, Give, FAQ, NotFound (10 pages, all named exports)
  data/
    nav.ts                # primaryNav (6 + description on children) / footerNav (10)
    content.ts            # 8 interfaces + 10 exports + images export (11 keys, all local — §0/§7.1)
    site.ts               # site as const — name/shortName/chineseName/tagline/vision + address + hours(7) + mass(9 keys) + contact + transport + feast + uen/chequePayee/socials/ministry links + origin/url/ogImage — single source
  utils/
    cn.ts                 # twMerge(clsx) + cn helper
    massDay.ts            # massDayKey(date): 'weekdays'|'saturday'|'sunday' — single source for the Worship today-highlight
    monogram.ts           # About monogram disc glyphs (round-5) — 7 tests
    deepLinks.ts          # knownRoutePaths + resolveHashRedirect (round-12 F-3) — path-style deep links rewrite to hash routes pre-mount; drift-guarded against App.tsx — 7 tests
  test/
    setup.ts              # vitest jsdom setup (jest-dom + IntersectionObserver mock + scrollTo/scrollIntoView stubs + matchMedia stub)
  **/*.test.{ts,tsx}      # 35 files / 202 tests — per-file breakdown in §0/§2
```

**Counts (§0):** `find src -type f | wc -l` → 77 (41 source + 35 tests + 1 setup); `public/images/` → 8 files → `dist/images/` on build (not inlined) + `public/favicon.svg`. Tests cover ScrollProgress/useScrollProgress/useScrollSpy/BackToTop/cta-bands/head/repo-hygiene/docs-contract/ci-workflow etc.

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

**Path-style deep links (round-12 F-3):** `main.tsx` calls `resolveHashRedirect` (from `utils/deepLinks.ts`) *before* mounting — `risenchrist.org.sg/worship` (no `#`) rewrites to `#/worship` so the user lands on the page, not Home. `knownRoutePaths` is drift-guarded against `App.tsx` (`utils/deepLinks` 7 tests). Covered by `e2e/deep-links.spec.ts` (3 tests).

**Hash anchors:**

| Route | IDs | Nav wiring | Notes |
|---|---|---|---|
| `/worship` | `#mass`, `#confession`, `#visit` | `primaryNav → /worship#mass` / `#confession` / `#visit` + `footerNav → /worship#mass` | 3 sections: Mass schedule (three `MassCard`s — Clock/MoonStar/Sun icons; the card matching `massDayKey(new Date())` carries `data-today="true"` + gold top rule + "Today" chip; Sunday slots are a gold-dot hover list), Confession & Adoration, Find Us (map). Each `section id="…"` has `scroll-mt-28`. |
| `/ministries` | `#liturgical`, `#faith-formation`, `#pastoral-care`, `#family-life`, `#youth`, `#language-communities` | `primaryNav → 3` of them; `footerNav → 3`; **Ministries jump nav** `ministries.map → <Link to="/ministries#<id>">` (6 pills, `aria-label="Jump to ministry"`, alternating `bg-shrine-cream`/`bg-shrine-parchment`, scrollspy-highlighted via `useScrollSpy`) | Must use `<Link to="/ministries#id">`, never `<a href="#id">` — plain href would replace the HashRouter hash and route to NotFound. Sixth id is `language-communities` (§0). |
| `/serve` | *(none)* | No section ids — `serveRoles`/`devotions` rendered without anchors | |
| *(orig)* | ~~`#pilgrim-center`/`#shrine-church`/`#tepeyac-hill`~~ | Gone — predecessor `WhatToSee` anchors removed | See Appendix D |

**Rule:** When adding a route, add its alias if external parish/school links or printed material expects it. Keep `Layout.tsx` hash logic intact — it resolves the anchor from `useLocation().hash` or the double-hash `window.location.hash`, then `getElementById` + `scrollIntoView({smooth})` (80ms) with fallback `window.scrollTo(0,0)`.

### 5.5 Component Conventions

| Primitive | File | API | Rule |
|---|---|---|---|
| `Button` | `src/components/ui/Button.tsx` | discriminated `to` (Link) / `href` (a) / native `button` + `variant`, `icon?`, `className?` | `to`→`<Link>`, `href`→`<a>`, else `<button>`; `variantClasses` + `cn()` + focus ring; icons get `aria-hidden` nudge (round-5) |
| `Container` | `src/components/ui/Container.tsx` | `children, className?` | All sections wrap in `<Container>` |
| `SectionHeading` | `src/components/ui/SectionHeading.tsx` | `eyebrow?, title, description?, align?, light?` | Eyebrow renders `gold-rule-left` line + gold/maroon; light = gold/cream on dark |
| `PageHero` | `src/components/PageHero.tsx` | `eyebrow, title, description?, image, children?, compact?` | `compact` shrinks padding; `bg-grain` + dual gradients; `alt=""`; atmosphere opacity 45 (round-7) |
| `SafeImage` | `src/components/SafeImage.tsx` | `src, fallback?, alt, className?, loading?, fetchPriority?` (`fallback` default `/images/hero-church.jpg`, `loading` default `lazy`, `fetchPriority` optional `"high"` on heroes) | Wraps `<img>` with `onError→dataset.fallback` guard to swap `src` once; always via `cn()`. All current `images.*` are local (naveCdn/courtyardCdn point to local); the guard stays valid for any future external image; don't use bare `<img>` for external sources. |
| `Header` | `src/components/Header.tsx` | `useScrolled(16)` (default 12) + `mobileOpen`, `openDesktopMenu` + Escape handler | Fixed maroon-950 bar (`maroon-950/92` + blur when solid; `solid = scrolled\|\|!isHome\|\|mobileOpen`); `aria-haspopup`/`aria-expanded` on dropdown trigger + `aria-current` states (plain "page", parent "true"), close on `pathname`+`hash` change + onClickCapture in drawer/dropdown; **mobile drawer is a modal dialog (round-4 L-5): `role="dialog"` + `aria-modal="true"` + `aria-label="Site menu"`, panel focused on open, `Tab`/`Shift+Tab` trapped (`handleDrawerKeyDown`), focus restored to the hamburger on every close path, outside `pointerdown` closes**; hamburger 44px (h-11 w-11); threshold 16 delays transparent→solid on Home (intentional) |
| `Reveal` | `src/components/ui/Reveal.tsx` | `children, delay?, as?: "div"│"li", className?` | `IntersectionObserver` 0.15 threshold + round-7 `rootMargin` early-entry; IO constructed in try/catch with visible fallback; respects `prefers-reduced-motion` |
| `Accordion` | `src/components/ui/Accordion.tsx` | `items: {question,answer}[]` | Single-open, `grid-rows` animation, `Plus rotate-45` — used by `FAQ.tsx` for `faqs[6]` |
| `BackToTop` | `src/components/BackToTop.tsx` | threshold 480 + SVG ring + reduced-motion | Appears when scrollY>480, hides below (aria-hidden+tabIndex -1), progress ring via `useScrollProgress` (`data-testid="back-to-top"` + `data-progress`); hash-safe (window.scrollTo only) |
| `ScrollProgress` | `src/components/ScrollProgress.tsx` | `useScrollProgress` 0..1 | Fixed `h-[3px]` rail (`data-testid="scroll-progress"`, `aria-hidden`, `scaleX(progress)`) at z-[60], rendered by Layout — decoupled from Header |
| `Emblem` / `SkipLink` / `Timeline` | `src/components/*` | see files | `Emblem` is inline SVG; `SkipLink` targets `#main-content` via preventDefault + imperative focus (never rewrites the hash); `Timeline` is a drawn gradient rail (`[data-testid="timeline-rail"]`, fades at both ends — no `border-l`) with display-serif gold years + Reveal per entry + dot-pulse halos — now shows 1969–2026 Toa Payoh milestones |
| `cn` | `src/utils/cn.ts` | `cn(...ClassValue[])` | Only merge path — `twMerge(clsx(...))` |

---

## 6. Custom Hooks Deep Dive

**Status: Three hooks — `useScrolled` + `useScrollProgress` + `useScrollSpy` (round-7).**

> **v3 fix:** the source files said "Two hooks" and omitted `useScrollSpy` from the tree, while their own test harness (`hooks/useScrollSpy` 6 tests), Quick Ref, and round-7 E2E descriptions proved it exists.

**Contracts:**

```ts
// src/hooks/useScrolled.ts
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

// src/hooks/useScrollProgress.ts — rAF-throttled 0..1, unscrollable guard
export function useScrollProgress(): number; // returns 0 when document height ≤ viewport

// src/hooks/useScrollSpy.ts — round-7 Ministries jump-nav highlight
export function useScrollSpy(ids: string[], options?: { offset?: number }): string | undefined;
// Tracks which section id is in view for the 6 ministry pills.
// Tie-break: when two sections compete, the one FIRST IN DOCUMENT ORDER wins
// (round-7 audit L-2 — never the tallest/nearest, which caused pill flicker).
```

- `Header.tsx` calls `useScrolled(16)` — the 16 vs default-12 mismatch is intentional (delays transparent→solid on Home). Don't "fix" it.
- `useScrollProgress` is shared by `ScrollProgress` (gold rail, z-[60]) and `BackToTop` (progress ring) — one listener, two consumers. Never touches the hash.
- `useScrollSpy` is consumed by the Ministries jump nav; 6 tests in `hooks/useScrollSpy.test.ts`.
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
|  | `grounds: GroundsPlace[]` | **3** — `main-church`, `chapel`, `parish-hall` (Main Church / Adoration Room / Parish Hall & Media Centre; + `image`/`imageFallback`/`imageAlt` — all local) | `Home.tsx` (grounds preview) |
|  | `ministries: Ministry[]` | **6** — `liturgical`, `faith-formation`, `pastoral-care`, `family-life`, `youth`, `language-communities` (Mandarin Sun 8.15, Tamil 2nd Sun 19.00, Tagalog 4th Sun 15.00, Bahasa 1st Fri 20.00) (each + `image`/`imageFallback`/`imageAlt` — all local) | `Ministries.tsx` (jump nav + 6 alternating sections) |
|  | `faqs: FaqItem[]` | **6** — Mass times, confession (approach a priest / parish office), how to get there (MRT Toa Payoh NS19 + buses), parking (HDB blks 66/70/73), baptism/marriage/Mass intention, Adoration Room | `FAQ.tsx` (`Accordion`) |
|  | `upcomingEvents: EventItem[]` | **6** — `title`+`date`+`summary`+`category` + optional `href` (categories `Parish`\|`Devotion`\|`Formation`\|`Archdiocese`) — 54th Velankanni 10–12 Sep, CEP 16 Aug–11 Oct (cep-sg.org), F.R.E.E. Acts 30 Jun–10 Nov (free.risenchrist.org.sg), Sunday Reflections, RCIA, Intercessory Prayer | `NewsEvents.tsx`, `Home.tsx` |
|  | `givingOptions: GivingOption[]` | **8** — PayNow UEN T08CC4042G, weekend collections, Mass offerings, SSVP, cheque payable Church of the Risen Christ, cash at office, General Church Offering, Church Maintenance (icons `flame`/`church`/`sprout`/`hand-heart`/`book`/`heart`/`landmark`/`globe`) | `Give.tsx` |
|  | `priests: Priest[]` | **3** — Fr Brian D'Souza (Parish Priest), Fr Arun Bellarmin, Fr Dexter Chua (Assistant) — each with `email` + `phone` | `About.tsx` |
|  | `ppcMembers: PpcMember[]` | **7** — 3 priests + Secretariat Peter Quek / Parish Administrator Audrey Rozario / Youth Coordinator Calvin Swee / Pastoral Coordinator Cheryl-Anne Goh | `About.tsx` |
|  | `serveRoles` (untyped const) | **4** — Liturgical ministers, Catechists & facilitators, Pastoral care, Hospitality & media (each `title`+`summary`) | `Serve.tsx` |
|  | `devotions` (untyped const) | **6** — Adoration daily, Intercessory 2nd & 4th Thu 20.00, Velankanni Sep, Simbang Gabi Dec, Bahasa 1st Fri 20.00, Tamil & Tagalog 2nd/4th Sun | `Serve.tsx`, `Worship.tsx` |
|  | `images` (`as const`) | **11 keys — all local** — `hero`/`heroFallback` `/images/hero-church.jpg`, `chapel`/`sanctuary`/`garden`/`glass`/`hall`/`cemetery`/`feast` (all `/images/*`), `naveCdn`→`/images/sanctuary.jpg`, `courtyardCdn`→`/images/rosary-garden.jpg` (local aliases) | `Home.tsx`, `PageHero`, `SafeImage` fallbacks |
| `src/data/nav.ts` | `primaryNav: NavItem[]` | **6** — Home, About(3 children), Worship(3 children with hash), Ministries(3 children with hash), News & Events, Serve. Children carry `description`. | `Header.tsx` |
|  | `footerNav: NavLink[]` | **10** — The Parish, Mass Times, History, FAQ, Liturgical, Faith Formation, Pastoral Care, News & Events, Serve, Give | `Footer.tsx` |
| `src/data/site.ts` | `site: { as const }` | **1 canonical object** — `name`/`shortName`/`chineseName` 耶稣复活堂/`tagline`/`vision` + `address` 91 Toa Payoh Central / 319193 (`full`/`query` getters) + `hours` (7: §1) + `mass` (9 keys: `weekdayMorning`/`weekdayEvening`/`saturday`/`sunday`/`confession`/`adoration`/`secondCollection`/`note`/`monthly`) + `contact` (3 phones + 5 emails) + `transport` (MRT NS19 + buses) + `feast` Easter Sunday + `uen` T08CC4042G/`chequePayee`/`facebook`/`instagram`/`youtube`/`archdiocese`/`freeMinistry`/`ssvp`/`bulletin`/`cep`/`mapsUrl`/`mapsEmbedSrc` + `origin`/`url`/`ogImage` | `Footer.tsx`, `Worship.tsx`, `About.tsx` — single source; don't duplicate |

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

**`ministries[6]`** — `liturgical` (altar servers, lectors, choirs, hospitality), `faith-formation` (catechesis of the Good Shepherd, Sunday catechism, RCIA, adult formation), `pastoral-care` (SSVP visits, sick & homebound, bereavement), `family-life` (baptism preparation, marriage prep, family events), `youth` (youth gatherings, outreach, formation), `language-communities` (Mandarin Sun 8.15, Tamil 2nd Sun 19.00, Tagalog 4th Sun 15.00, Bahasa Indonesia 1st Fri 20.00). Each drives one alternating `bg-shrine-cream`/`bg-shrine-parchment` section in `Ministries.tsx`.

**`faqs[6]`** — Mass times (weekday 6.30a/6p, Sat 6.30a+5.30p, Sun 5 Masses incl. Mandarin 8.15), confession (approach a priest after Mass or the parish office), how to get there (91 Toa Payoh Central, MRT Toa Payoh NS19 Exit A, buses 88/157/163), parking (HDB blks 66/70/73 nearby), baptism/marriage/Mass intention (parish office 6253 2166), Adoration Room hours.

**`upcomingEvents[6]`** — `title`+`date`+`summary`+`category` + optional `href` (2 of 6 carry href: `cep-sg.org`, `free.risenchrist.org.sg`). Categories `Parish`/`Devotion`/`Formation`/`Archdiocese`. Examples: 54th Feast of Our Lady of Velankanni 10–12 Sep 2026 (Devotion), Couple Empowerment Programme 16 Aug–11 Oct (Parish), F.R.E.E. Acts: The Spread of the Kingdom 30 Jun–10 Nov (Formation), Sunday Reflections, RCIA, Intercessory Prayer.

**`givingOptions[8]`** — PayNow UEN T08CC4042G, weekend collections, Mass offerings, SSVP (poor & needy), cheque payable Church of the Risen Christ, cash at the parish office, General Church Offering, Church Maintenance Fund. No HRSM, no Tap & Give — the Risen Christ set replaces the St Mary line (Appendix F). Round-12 F-4: the UEN lives in a copyable PayNow row, out of the heading.

### 7.4 How to Add Content

**Add a timeline entry:**

1. Append to `lifeTimeline` in `src/data/content.ts` with `{ year, title, description }`.
2. Re-run `pnpm typecheck` (type gate).
3. No page change — `History.tsx` maps the array via `Timeline.tsx`.

**Add a ministry:**

1. Append to `ministries` with `{ id, title, summary, details[], image, imageFallback, imageAlt }` — `id` becomes the hash anchor (`/ministries#<id>`).
2. Verify `Ministries.tsx` jump nav (`ministries.map → <Link to="/ministries#id">`) picks it up automatically; add the id to the `useScrollSpy` watch list.
3. Run `pnpm typecheck && pnpm build`.

**Add a nav item:**

1. Append to `primaryNav` or `footerNav` in `src/data/nav.ts` (include `description` for dropdown children).
2. If routed, add `<Route path="…">` in `src/App.tsx` — include an alias if a legacy/external path expects it, and add the path to `utils/deepLinks.ts` `knownRoutePaths`.
3. Verify `Header` hover dropdown + mobile drawer render the child.

**Why no `import.meta.glob`:** Vite glob is for file-system content collections (e.g., Astro). This is a typed-array SPA — direct export + import is simpler and fully type-checked. For a future CMS, isolate behind `src/lib/cms/` and keep `content.ts` as fallback.

---

## 8. Accessibility (WCAG AAA) Implementation

**Target:** WCAG AAA intent — this section documents the contract, not a certification claim. Verify with `axe-core` / Lighthouse a11y before claiming pass. `src/components/wcag-contrast.test.tsx` (round-12) computes the ratios from the `@theme` token layer so drift fails a test, not a review.

### 8.1 Contrast (body text)

| Foreground | Background | Ratio | Level |
|---|---|---|---|
| `shrine-ink #2a2115` | `shrine-cream #faf6ec` | ~13:1 | AAA |
| `shrine-charcoal #423a2c` | `shrine-cream` | ~10:1 | AAA |
| `shrine-cream #faf6ec` | `shrine-maroon-900 #33100f` | ~13:1 | AAA |
| `shrine-gold-300 #e2bf72` | `shrine-maroon-900` | ~7:1 | AAA |
| `shrine-terracotta-600 #8f4c30` | `shrine-parchment #f2e9d6` | 5.36:1 | AA (Devotion chip text — round-12 F-1; hop-1's `terracotta-500` chip text was 3.4:1, decorative only) |

Verify new pairings with a contrast checker before merging — or add them to `wcag-contrast.test.tsx`.

### 8.2 Focus & Navigation

- **Focus ring:** `focus-visible:outline` via Tailwind defaults; `src/index.css` `@layer base` sets `outline: 2px solid --color-shrine-gold-500` + `offset 3px` for `:focus-visible`. Preserve on `Button` and `Header` toggle. Do not remove outlines.
- **Header toggle:** `aria-label` toggles `Open menu`/`Close menu`, `aria-expanded` reflects `mobileOpen`. Keep both.
- **Dropdowns:** Hover/focus-open (`onMouseEnter`/`onMouseLeave` + `onFocusCapture` on `primaryNav` children — keyboard reachable without a click-toggle). If converting to click-open, add `aria-haspopup="true"` + focus-trap + `Escape` close.
- **Mobile drawer is a modal (round-4 L-5):** `role="dialog"` + `aria-modal="true"` + `aria-label="Site menu"`; panel receives initial focus; `Tab`/`Shift+Tab` trapped; focus restored to the hamburger on every close path (including Escape and outside-tap); 44px hamburger target.
- **Skip-to-content:** Implemented — `SkipLink.tsx` renders `<a href="#main-content">` first in `Layout`. Under HashRouter the component **must not** let the browser follow the href (the hash is the route): `onClick` `preventDefault`s and imperatively focuses `#main-content` (`<main id="main-content">` in `Layout`). Covered by `src/components/SkipLink.test.tsx` (3 tests) + `e2e/navigation.spec.ts` (SkipLink hash-preserving).
- **Landmarks:** `header`/`main`/`footer` present via `Layout`; every page's `PageHero` is `section` with heading hierarchy `h1 → h2`. Each ministry section in `Ministries.tsx` has `aria-labelledby` pointing to its `h2`.

### 8.3 Images & Media

- Decorative hero overlays (`PageHero` image): `alt=""` + `aria-hidden="true"`; `PageHero` also renders `bg-grain` + dual gradients over the image for contrast.
- Content images (`grounds` cards, `ministries` sections, Home): `imageAlt` is required — `GroundsPlace.imageAlt` and `Ministry.imageAlt` enforce it (see §20). `SafeImage` passes it through.
- Icon-only links: each `lucide-react` icon has `aria-hidden="true"` and the anchor has `aria-label`.
- Ministries jump nav pills: `aria-label="Jump to ministry"` on each `<Link>`; active pill state mirrored by scrollspy.

### 8.4 Motion

- `html { scroll-behavior: smooth }` in `src/index.css`. Honor `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after { animation-duration: 0.01ms !important; }
}
```

- `src/index.css` kills all 8 keyframes and `.reveal` (opacity/transform) under `prefers-reduced-motion: reduce` (motion kill expanded 1→7 rules at hop 2); `Reveal.tsx` constructs its `IntersectionObserver` in try/catch and falls back visible if unsupported (round-7).
- `@media print` overrides `.reveal` to visible (round-7 "Honest Light") — printed pages must not depend on scroll-triggered opacity.

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
| 7 | **Stale `include`** (High) | File not type-checked | Added file outside `src/` but didn't expand `tsconfig.json` `include` | Add path to `include` (currently 5 entries, §3.2) | `include` is the type boundary |
| 8 | **`noUnusedLocals` breach** (Medium) | `tsc --noEmit` fails on unused import/var | Left placeholder imports/params after refactor | Remove or prefix deliberately unused param with `_` (`_idx`) | Strict flags are the gate |
| 9 | **Runtime font loader** (Medium) | FOIT + duplicate load | Imported fonts in JS instead of `index.html` | Fonts belong in `index.html` + `@theme`; no JS loader | One font source of truth |
| 10 | **Missing `imageAlt`** (Medium) | Empty alt on content image | Added `GroundsPlace`/`Ministry` without `imageAlt` | `imageAlt` is required — fill it | Content interface enforces a11y (§20) |
| 11 | **Plain `<a href="#id">` in HashRouter** (High) | Clicking a ministry pill routes to `NotFound` or loses the page | Used `<a href="#liturgical">` instead of `<Link to="/ministries#liturgical">` — plain href replaces the HashRouter hash | Always `<Link to="/ministries#id">` and `<Link to="/worship#id">` for hash anchors (see §5.4) | Hash is the route |
| 12 | **Lost `aria-expanded`** (Low) | Screen reader can't tell drawer state | Refactored `Header` toggle without `aria-expanded` | Keep `aria-expanded={mobileOpen}` + `aria-label` toggle | A11y props are functional |
| 13 | **Wrong `SafeImage` fallback** (Medium) | Broken hero on image failure shows shrine fallback | Used old `fallback="/images/hero-shrine.jpg"` (Rother path) instead of `"/images/hero-church.jpg"` | Default fallback is `/images/hero-church.jpg` — verify `src/components/SafeImage.tsx` default | All 11 `images.*` are local (`naveCdn`/`courtyardCdn` point to local fallbacks); the `onError` guard stays for any future external image (CDN → local discipline §5.5) |
| 14 | **Dev-only E2E asset assertions** (Medium) | Spec green on `pnpm dev`, red against `dist/`/live | Spec asserted the exact dev-form asset path (`/favicon.svg`) that `viteSingleFile` rewrites to `./favicon.svg` in the built HTML | Env-agnostic regex (`/^(?:\.\/|\/)favicon\.svg$/`) + resolution check; run `pnpm test:e2e:built` before shipping (round-9 E2E-L1) | Dev artifacts ≠ built artifacts |
| 15 | **agent-browser eval backslash mangling** (Low) | eval returns empty; stderr (when visible) shows "SyntaxError: Unterminated group" | Backslash-escaped regex literal inside an `agent-browser eval` string — the CLI strips backslashes from the command before JS evaluation, and `2>/dev/null` hides the error | Backslash-free contract checks: string comparisons (`h === './x'`) or `new RegExp` built from a string source; keep stderr visible while debugging (round-11 E2E-J1, ledger: `docs/e2e-live-pass-round11-2026-08-31.md`) | CLI arg parsing ≠ JS string literals |

---

## 10. Debugging Guide

| Symptom | Cause | Fix |
|---|---|---|
| `pnpm dev` → `EADDRINUSE :5173` | Port in use | `pnpm dev -- --port 5174` or `lsof -i:5173` then kill |
| `Cannot find module '@/utils/cn'` | Alias desync (see §9 #5) | Align `vite.config.ts` ↔ `tsconfig.json` `paths @/*` (`baseUrl:"."`) — change both; restart Vite |
| `npx tsc --noEmit` → `TS6133 'x' is declared but never used` | `noUnusedLocals`/`Params` (`strict` + `noUnusedLocals:true` `noUnusedParameters:true`) | Remove import or use it; for intentionally unused param, prefix `_` (e.g., `_idx`) |
| `pnpm test` → "no test files found" | `src/test/setup.ts` missing or `vite.config.ts test.include` misconfigured | Verify `src/test/setup.ts` exists and `vite.config.ts test` includes `src/**/*.{test,spec}.{ts,tsx}` with `exclude: ["e2e/**"]` — should be **35 files / 202 tests** (§0) |
| `pnpm test:e2e` → failures on `#mass`/`#liturgical` etc. | Missing `id` or `Layout` double-hash logic stale | Verify `Worship.tsx` has `id="mass"`/`"confession"`/`"visit"` and `Ministries.tsx` has 6 ministry `id`s (sixth = `language-communities`); `Layout` `resolveAnchor` must handle `/#/worship#mass` form |
| Hash anchor lands at top (`/#/worship#mass` or `/#/ministries#liturgical`) | Target `id` missing or `Layout` effect stale | Verify `id="mass"` in `Worship.tsx` and `id="liturgical"` in `Ministries.tsx`; check `Layout` `useEffect` deps `[pathname, hash]`; jump nav must be `<Link to="/ministries#id">` (not plain `<a href="#id">`, see §9 #11) |
| Double-hash `#/ministries#liturgical` doesn't scroll | `Layout` `resolveAnchor` not matching `pathname` | Verify `resolveAnchor` splits `window.location.hash` on `#`, filters, strips leading `/`, and compares against `pathname.replace(/^\//,"")` — the `cleaned === pathname…` guard prevents false anchors |
| Path-style URL (`/worship` without `#`) lands on Home | `resolveHashRedirect` not wired or path missing from `knownRoutePaths` | `main.tsx` must call `resolveHashRedirect` pre-mount; `utils/deepLinks.ts` `knownRoutePaths` must list every content path (drift-guarded against `App.tsx`, 7 tests) — round-12 F-3 |
| `pnpm build` → `dist/index.html` missing or not inlined | `viteSingleFile` misordered or removed | Verify `plugins: [react(), tailwindcss(), viteSingleFile()]` order; check `dist/index.html` exists and `Inlining: index-*.js` in log; `dist/images/` alongside is expected (publicDir copy) |
| E2E green in dev, red on built artifact / live | Dev-only asset-path assertion (§9 #14) | Env-agnostic regex + run `pnpm test:e2e:built` (round-9 E2E-L1) |
| Styles missing locally but build works | `@import "tailwindcss"` order wrong | `@import` must be first line of `src/index.css` |
| Fonts not loading | `index.html` preconnect or href typo | Verify `fonts.googleapis.com` preconnect + `Fraunces`/`Source Sans 3` href intact; no JS font loader |
| GH Pages deep-link 404 on refresh | Switched to `BrowserRouter` | Revert to `HashRouter` or add `404.html` SPA redirect |
| Image 404 (`/images/hero-church.jpg`) | Wrong public path / missing `dist/images/` on deploy | Hero/fallback belong in `public/images/` and referenced as `/images/…` (absolute from root; Vite copies to `dist/images/` — upload alongside `index.html`); all `images.*` are local (§0). Upload count: **8 files** in `public/images/` |
| `tests` not found or `e2e` leaking into vitest | `test.include`/`exclude` misconfigured | Verify `vite.config.ts test: { globals:true, environment:"jsdom", setupFiles:["src/test/setup.ts"], include:["src/**/*.{test,spec}.{ts,tsx}"], exclude:["e2e/**","node_modules/**","playwright-report/**","test-results/**"] }` — `e2e/**` must be excluded |
| `vite.config.ts` `server.watch` `ENOSPC` on `pnpm dev` | Vendored `skills/` tree (large `.venv`) watched without ignore | Verify `server.watch.ignored: ["**/skills/**","**/dist/**","**/playwright-report/**","**/test-results/**","**/coverage/**","**/src.orig/**"]` is present in `vite.config.ts` |
| `tsconfig.json` errors on `eslint.config.js` / `playwright.config.ts` / `playwright.built.config.ts` | Added those files to `include` without installing their types | `include` is the 5-entry list in §3.2 with `types ["node","vitest/globals"]` — required for `describe/it/expect` globals |
| `repo-hygiene` test fails | `src.orig/` or `docs/ssh-key.txt` path re-entered the git index | `git rm -r --cached <path>`; the guard is the enforcement of §0's prune policy — do not weaken the test |

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
# Path-style: /worship  /news-events  /donate (no #) → land on their pages, not Home (round-12 F-3)
```

---

## 11. Pre-Ship Checklist

Run in order — every step must be green before pushing `main` (`main` is the deploy branch).

```bash
pnpm lint                      # 1 — eslint 9.39.5 flat --max-warnings 0
pnpm typecheck                 # 2 — tsc --noEmit (strict + noUnusedLocals/Params + noFallthroughCasesInSwitch)
pnpm test                      # 3 — vitest 3.2.6 jsdom — 35 files / 202 tests green (per-file breakdown: §0/§2)
pnpm test:e2e                  # 4 — playwright 1.55.1 chromium — 51 tests green (8 specs, §0)
pnpm test:e2e:built            # 4b — playwright vs built artifact (vite preview :4173; E2E_BASE_URL → live host) — same 51 tests green
pnpm build                     # 5 — singlefile 2.3.3 build → dist/index.html (JS+CSS inlined) + dist/images/ (8 files, copied not inlined)
pnpm preview &                 # 6 — smoke: spot-check 10 routes + 7 alias paths + 9 hash anchors (3 on /worship + 6 on /ministries)
ls -lh dist/                   # 7 — confirm dist/index.html + dist/_headers + dist/favicon.svg + dist/images/ (8 files) — publicDir copy expected, not inlined
# 8 — axe/Lighthouse a11y spot-check on Header + Home hero + FAQ + Worship#visit map
git push origin main           # 9 — deploy (GH Pages / S3 upload of dist/index.html + dist/images/)
```

| Category | Check | How |
|---|---|---|
| Lint | `pnpm lint` clean | `eslint 9.39.5` flat `eslint . --max-warnings 0` (`typescript-eslint 8.28.0` + `react-hooks 5.2.0`) — ignores `skills` + `src.orig` |
| Types | `pnpm typecheck` (`npx tsc --noEmit`) clean | `strict` + `noUnusedLocals`/`noUnusedParameters`/`noFallthroughCasesInSwitch`/`isolatedModules`/`noEmit` pass; `tsconfig.json` `include` covers the 5 entries in §3.2 with `types [node, vitest/globals]` |
| Tests | `pnpm test` — 35 files / 202 tests green | `vitest 3.2.6 jsdom` via `src/test/setup.ts` (jest-dom + IntersectionObserver mock + scrollTo/scrollIntoView stubs + matchMedia stub) + `vite.config.ts test.include [src/**/*.{test,spec}.{ts,tsx}]` — `e2e/**` excluded |
| E2E | `pnpm test:e2e` — 51 tests green (8 specs) | Full spec list + round coverage in §2/§0. `playwright.config.ts` `expect.timeout: 15s` + `webServer → pnpm exec vite :5173` — built-artifact pass: `playwright.built.config.ts` (`vite preview :4173`; `E2E_BASE_URL` → live host) |
| Build | `pnpm build` greens | `viteSingleFile 2.3.3` inlines JS + CSS; `dist/images/` 8 files copied (not inlined) — verify one-file `dist/index.html` (397.52 kB, §0) |
| Routes | All 10 pages + 7 alias paths + 9 hash anchors navigate (HashRouter) + path-style deep links land on their pages | Manual or `agent-browser` smoke (`Layout` double-hash aware `#/ministries#id` → split + 80ms `scrollIntoView`; `main.tsx` pre-mount `resolveHashRedirect`) |
| A11y | Contrast ≥4.5:1 on body (incl. terracotta-600 chip 5.36:1), `alt` on content images (`SafeImage` fallback), `aria-expanded` on toggle, drawer modal focus trap + Escape restore, `SkipLink` hash discipline, `aria-label="Jump to ministry"` | Spot-check per §8 table + `axe-core` on Header/Home hero/FAQ/Worship map + `wcag-contrast` unit suite |
| Visual | Hero gradients + `shadow-shrine`/`shadow-shrine-lg` + `divider-weave`/`divider-weave-thin` + `gold-rule`/`gold-rule-left` + `hero-ken-burns` render | Preview comparison — hero is the local `hero-church.jpg` (dusk nave) |
| Images | `SafeImage` fallback verified (all images local) + `public/images/` → `dist/images/` (8 files) + `dist/favicon.svg` on deploy | Block images or off-line smoke; check `dist/images/` has the 8 files listed in §0 |
| CSP | No console CSP violations | Verify `index.html` CSP: `img-src 'self' data: blob:` (all images local), `frame-src https://www.google.com` for maps embed, `script-src` inline + `static.cloudflareinsights.com`; no `unsafe-eval` |
| Git | No `dist/`/`node_modules/` committed; no secret material tracked (`src/repo-hygiene.test.ts` guards `docs/ssh-key.txt` + the pruned `src.orig/`) | `.gitignore` respected (`skills/` stays tracked as vendored reference but ignored by tooling; `src.orig/` pruned round-12 — guard fails if it re-enters). **Outstanding: rotate the leaked ssh key (§0)** |
| Docs | This file + `README` + `AGENTS` + `CLAUDE` agree on every §0 fact | `src/docs-contract.test.ts` (16 tests) enforces the drift guard at CI level |

**Pre-push gate — all five must be green (verified 2026-08-31, round-9 E2E-L1 remediation; counts in §0):**

```bash
pnpm lint && pnpm typecheck && pnpm test && pnpm test:e2e && pnpm build
# → lint 0 + typecheck 0 + test 35/202 + test:e2e 51 + build 397.52kB dist/index.html + dist/_headers + dist/favicon.svg + dist/images/8
```

---

## 12. Lessons Learnt & How to Avoid Them

> L1–L12 are the per-hop engineering lessons (carried through all three source files). **L13–L15 are new in v3** — the doc-fidelity lessons from the 2026-09-01 unification audit (full ledger: Appendix G).

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
| L9 | **`SafeImage` default drift** | Wikimedia hero (`images.hero`) introduced a new CDN host at hop 1; old default `/images/hero-shrine.jpg` would have 404'd on fallback. Later hops went all-local. | `SafeImage.tsx` default is `/images/hero-church.jpg`; `images.heroFallback` + `imageFallback` on every `grounds`/`ministries` entry; the `onError` guard is kept for future external images. |
| L10 | **Stale `e2e/` was a trap — resolved per hop** | Hop 1 initially kept the 20-test Rother E2E verbatim (`#pilgrim-center` etc.); CI would have failed. Each hop rewrote the suite to its own parish. | E2E rewritten per hop (current: 51 tests / 8 specs, §0). Alias mapping `what-to-see` → `ministries`, `pilgrimage` → `worship` covered under current routes. |
| L11 | **`vite.config.ts` `test` block is required** | Restoring `src/test/setup.ts` without the `test` block leaves vitest misconfigured. | `vite.config.ts` has `test { globals:true, jsdom, setupFiles:["src/test/setup.ts"], include:["src/**/*.{test,spec}.{ts,tsx}"], exclude:["e2e/**"] }` + `types ["vitest/globals"]` — keep both in sync (see §3.2). |
| L12 | **Canonical flip: `/about` not `/about-blessed-stanley-rother`** | Hop 1 flipped the About canonical (orig: `/about-blessed-stanley-rother` canonical, `/about` alias). Any hard-coded deep link to the old canonical would 404 if the alias were dropped. | Kept only `/about` (no alias needed — the old canonical is intentionally retired for the parish). Document the flip in §5.4 + Appendix D; if old shrine links must survive, add `/about-blessed-stanley-rother` back as an alias to `/about`. |
| L13 | **A secret in git history is a live secret** (new, v3) | `docs/ssh-key.txt` was committed (`0be0fe8`), untracked next round — but `git rm --cached` does not scrub history, so the key remains recoverable from every clone. | Round-6 C1 disclosure carried in §0/§2; `repo-hygiene` test guards the working tree. **Rotation is the only real fix**; consider `git filter-repo` + force-push + credential revocation. |
| L14 | **`.gitignore` does not untrack** (new, v3) | `src.orig/` was listed in `.gitignore` since round 3 yet remained tracked (64 files) until round-12 F-9 found it — ignore rules only prevent *new* additions. | `git rm -r --cached <path>` to actually untrack; `repo-hygiene` test now fails if a guarded path re-enters the index. Rule: adding a path to `.gitignore` for something already committed requires an explicit untrack commit in the same change. |
| L15 | **Every restatement is a future fossil** (new, v3 — the systemic root cause) | The three source docs restated each volatile fact 5–8×; each hop healed the body but copy-forwarded the appendices without a previous-parish sweep, leaving contradictory counts (three test-count generations inside one doc; three version numbers inside hop 1's doc; a St Mary smoke script inside hop 3's Appendix B). | v3 introduces §0 (single statement of every volatile fact, all other sections reference it), explicit **`as of <date>`** labels for historical snapshots in appendices, `docs-contract` tests (16) at CI level, and the fossil-sweep protocol (Appendix G.4) that every future port must run before its doc ships. |

---

## 13. Pitfalls to Avoid

**Architecture**
- Don't add SSR/API/`server/` without an ADR — this is a static SPA by design.
- Don't scatter route tables outside `src/App.tsx` — it is the only route table (17 entries, 5 alias groups); the only *companion* is `utils/deepLinks.ts` `knownRoutePaths`, which is drift-guarded against it.
- Don't put data arrays outside `src/data/*` — they are the data layer (`content.ts` + `nav.ts` + `site.ts`).
- Don't reintroduce St Mary of the Angels / Bukit Batok / St Joseph BT / Rother Shrine parish narratives outside the historical appendices — this is Church of the Risen Christ (91 Toa Payoh Central, 1969–2026 Toa Payoh line, Easter Sunday, UEN T08CC4042G). Hours, Mass, and address are the single source in `site.ts`; don't duplicate them across pages.

**TypeScript**
- Don't use `any` — use `unknown` + narrowing; `as any` is a last resort with `// ponytail: ceiling…` comment.
- Don't use `type` for object shapes — prefer `interface` (`type` is for unions).
- Don't relax `strict` flags to silence errors — fix the code. `noUnusedLocals`/`noUnusedParameters`/`noFallthroughCasesInSwitch`/`isolatedModules`/`noEmit` are the gate.
- Don't assume `tsconfig.json` scope — it includes the 5 entries in §3.2 with `types ["node","vitest/globals"]`. Don't re-add `src.orig/` to `include`.

**Styling**
- Don't introduce `amber-400`/`slate-*`/`zinc-*` — forbidden; use `shrine-*`.
- Don't use arbitrary `bg-[#...]` — extend `@theme`.
- Don't add `tailwind.config.*` — v4 is CSS-first (`src/index.css` `@theme` is the only token source).
- Don't bypass `cn()` — `tailwind-merge` dedup matters; never concatenate Tailwind strings with template literals.

**Data / A11y**
- Don't omit `imageAlt` or `imageFallback` on `grounds`/`ministries`.
- Don't remove `alt=""` on decorative hero overlays (`PageHero`); don't drop `aria-expanded`/`aria-label` on the mobile toggle, the modal-dialog drawer contract (round-4), or `aria-label="Jump to ministry"` on the Ministries pills.
- Don't let `SkipLink` rewrite the hash — its `preventDefault` + imperative `focus()` is load-bearing for HashRouter.

**Build / Deploy**
- Don't commit `dist/`/`node_modules/`. `skills/` is committed vendored reference content (re-added in `0be0fe8`) — don't import from it or lint it (eslint ignores it). `src.orig/` is **pruned and guarded** — never re-add it; lineage history lives in Appendices D/F + git history.
- Don't upload `dist/index.html` without `dist/images/` — the 8 image files are copied via `publicDir`, not inlined; both must ship together to GH Pages/S3.
- Don't ship a "green CI" claim without running the full gate (`pnpm lint && pnpm typecheck && pnpm test && pnpm test:e2e && pnpm build`) — all five must be green (counts in §0). Asset-path e2e assertions must be env-agnostic — run `pnpm test:e2e:built` so dev-only forms (e.g. `/favicon.svg` vs the singlefile-rewritten `./favicon.svg`) cannot ship (round-9 E2E-L1).
- Don't state a mutable number anywhere except §0 — every other statement of it is a future fossil (L15).

---

## 14. Best Practices

- **File naming:** `PascalCase.tsx` for components/pages (`PageHero.tsx`), `camelCase.ts` for data/utils (`content.ts`, `cn.ts`), `useThing.ts` for hooks (`useScrolled.ts`).
- **Imports:** Always `@/` for cross-directory; relative `./` only within the same folder.
- **Types:** `interface` for shapes, `type` for unions; `import type` for type-only imports; rely on inference, add explicit returns only at public boundaries. Never `any`.
- **React:** Hooks-only, composition over inheritance, early returns, handle `loading`/`error`/`empty`/`success` where data is async; disable buttons during async ops.
- **Styling:** Extend `@theme` before adding a utility; keep bespoke CSS to `@layer base/utilities` in `src/index.css`; mobile-first `sm:`/`lg:`; one shadow (`shadow-shrine`), two radii (`sm`/`full`). Use the `shrine-*` scales + the 27 utilities in §4.3. Motion: transform/opacity only, everything gated by the global `prefers-reduced-motion` block + `@media print` reveal override.
- **Data:** Keep `site.ts` as the single source for name/address/hours/mass/contact/transport/feast/uen/chequePayee/socials/ministry links/maps/origin. Pages consume it — don't duplicate. `content.ts` arrays + `nav.ts` nav are the only other data sources.
- **Git:** Conventional Commits (`feat:`, `fix:`, `docs:` …), atomic commits, `feat/<slug>` branches, squash-merge, short-lived (1–3 days). Don't edit `package.json` by hand for deps — use `pnpm install <pkg>`. Adding a path to `.gitignore` for tracked files requires `git rm --cached` in the same commit (L14).
- **Docs:** Update `README.md` + `AGENTS.md` + `CLAUDE.md` + this file when adding a route/token/image/nav child — and change the §0 fact first, then sweep stale copies (L15, Appendix G.4). Keep `skills/` out of scope (vendored, re-added in `0be0fe8`). `docs-contract` (16 tests) + `ci-workflow` (4) + `repo-hygiene` (3) enforce the doc/CI/git contracts at test level.

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
// src/components/Layout.tsx — core hash-scroll contract (Toa Payoh / Risen Christ)
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

> **v3 note:** the snippet above is the *load-bearing hash contract* shown for copy-paste clarity — the same principle the three source files printed. The production `Layout.tsx` additionally renders `<ScrollProgress />` and `<BackToTop />`, wraps the Outlet in a keyed page-in container, and **cleans up its 80ms `setTimeout` on effect re-run** (hop-1 remediation "Layout timeout cleanup" — keep the cleanup when editing; a stale timer can scroll the user away from a newly-mounted page). `main.tsx` also runs `resolveHashRedirect` pre-mount (round-12 F-3, §5.4).

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

> The image is a **local** `/images/*` path (§0); atmosphere opacity moves 35→45 in round-7. Keep `alt=""` + `aria-hidden` — the hero image is decorative.

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

> Round-7: the active pill is highlighted by `useScrollSpy(ids)` — document-order tie-break (§6). Keep the pill bar at `z-40` if made sticky (§18).

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
| Adding `GroundsPlace`/`Ministry` without `imageAlt`/`imageFallback` | Always include both | A11y + fallback contract |
| Asserting `/favicon.svg` exactly in E2E | Env-agnostic regex `/^(?:\.\/|\/)favicon\.svg$/` + `test:e2e:built` | Singlefile rewrites root-relative refs (§9 #14) |
| Restating a test/token/file count in prose | Reference §0 | Every restatement is a future fossil (L15) |

---

## 17. Responsive Breakpoint Reference

Tailwind defaults only (no custom config). Project usage:

| Breakpoint | Min-Width | Usage in this SPA |
|---|---|---|
| *(default)* | `0` | Single-col, stacked hero, mobile drawer (`Header` hamburger) |
| `sm` | `640px` | 2-col quick-facts `grid-cols-2`, `px-8`, `text-5xl` heroes, `py-24 sm:py-28` sections |
| `lg` | `1024px` | `lg:flex` header nav (desktop dropdown), `lg:grid-cols-2` welcome split, `lg:grid-cols-3` grounds cards, `lg:sticky` History story (round-5) |

**Rule:** Mobile-first — default is mobile; `sm:` then `lg:` only. Test: `pnpm dev` + Chrome DevTools `375×812` (iPhone) → `1280×800`. Header breakpoint is `lg` (drawer below `lg`, flex nav at `lg`).

---

## 18. Z-Index Layer Map

> **v3 fix:** all three source files omitted the `z-[60]` scroll-progress rail row even though their own §5.2/§5.5 specify it. The table below includes it.

| Layer | `z-*` | Element | File | Purpose |
|---|---|---|---|---|
| Top | `z-[100]` | Skip-to-content link | `src/components/SkipLink.tsx` (`.skip-link` utility) | Always reachable above everything when focused |
| Rail | `z-[60]` | Scroll-progress gold rail (`h-[3px]`, `aria-hidden`) | `src/components/ScrollProgress.tsx` (rendered by `Layout`) | Reading-progress indicator above content + header chrome, below skip link |
| High | `z-50` | `<header>` + its desktop dropdown + open mobile drawer overlay | `src/components/Header.tsx` | Fixed nav above content + hero; dropdown/drawer inherit header stacking; modal drawer (round-4) traps focus within this layer while open |
| Mid | `z-40` | Ministries jump nav (sticky under header, if sticky) | `src/pages/Ministries.tsx` | Sticky section nav below the fixed header — verify against `Header` height |
| Base | `z-auto` | `main`, `footer`, `PageHero` gradients, `Timeline` rail | `src/components/Layout.tsx`, `Footer.tsx`, `PageHero.tsx`, `Timeline.tsx` | Normal flow |
| Portal | — | None yet | — | Add Radix/Portal table when modals exist |

**Conflict rule:** the skip link owns `z-[100]`; the progress rail owns `z-[60]`; `Header` owns `z-50`; jump nav stays below it at `z-40`; nothing else may exceed `z-40` without a row here. Don't add competing layers without updating this table. If making the Ministries pill bar `sticky top-[…]`, verify `scroll-mt-28` on target sections still clears the header (and the rail).

---
## 19. Color Reference (Complete)

Every hex matches `src/index.css` `@theme` byte-for-byte. **Fail the build if it drifts.** Round-12 extended the terracotta scale with one text-bearing step (`terracotta-600 #8f4c30` — WCAG AA for the Devotion chip; contract `src/components/wcag-contrast.test.tsx` computes ratios from this token layer); verification command `grep shrine- src/index.css` → **25 colors + 2 shadows** (§0). *Lineage note:* hop 2 (St Mary) also carried `gold-700 #85601f` (4.72:1) — not in this line; re-add with a row here if needed.

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

All interfaces below compile as-is against `tsconfig.json` (`strict` + `bundler` + `react-jsx`). Locations: `src/data/*`, `src/components/ui/*`, `src/utils/*`. **Verbatim against `src/data/content.ts`, `src/data/nav.ts`, `src/data/site.ts`, `src/components/SafeImage.tsx`, `src/components/ui/*`.**

> **v3 fixes carried into this section:** `SafeImageProps` gains `fetchPriority?` (it was documented in §5.5 but missing from the interface listing in all three source files); stale hop-1 comments ("3 CDN", "Wikimedia", "Bukit Timah") are corrected to the all-local reality; hooks/utils signatures for `useScrollSpy`/`massDay`/`deepLinks`/`monogram` are added (they existed in code but were absent from §20).

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
  image: string;           // local /images/* (legacy CDN keys are local aliases)
  imageFallback: string;   // local /images/* — required (SafeImage fallback)
  imageAlt: string;        // required — a11y
}
// grounds: GroundsPlace[] — 3 (Main Church / Adoration Room / Parish Hall & Media Centre)

export interface Ministry {
  id: string;              // "liturgical" | "faith-formation" | "pastoral-care" | "family-life" | "youth" | "language-communities"
  title: string;
  summary: string;
  details: string[];       // 4 bullets each
  image: string;           // local /images/*
  imageFallback: string;   // required
  imageAlt: string;        // required
}
// ministries: Ministry[] — 6 (sixth is Language Communities — hash anchor #language-communities, §5.4)

export interface FaqItem {
  question: string;
  answer: string;
}
// faqs: FaqItem[] — 6 (Mass/confession/how to get there/parking/baptism-marriage-Mass intention/Adoration Room)

export interface EventItem {
  title: string;
  date: string;            // "10–12 September" | "16 August – 11 October" | …
  summary: string;
  category: "Parish" | "Devotion" | "Formation" | "Archdiocese";
  href?: string;           // optional — 2 of 6 carry it: CEP → https://www.cep-sg.org, F.R.E.E. → https://free.risenchrist.org.sg/
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
  email?: string;          // e.g. brian.dsouza@catholic.org.sg
  phone?: string;          // diocesan clergy carry email + phone
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
  summary: string;
}[] // 4

export const devotions: {
  title: string;           // "Adoration" | "Intercessory Prayer" | "Velankanni Devotion" | "Simbang Gabi" | "Bahasa Prayer Group" | "Tamil & Tagalog Devotions"
  when: string;            // "daily" | "2nd & 4th Thu 8.00 p.m." | "September" | …
  where: string;           // "Adoration Room — daily" | "Main Church" | "September — parish feast of Our Lady of Velankanni" | …
}[] // 6

export const images: {
  hero: string;            // "/images/hero-church.jpg" (local — was Wikimedia in hop 1)
  heroFallback: string;    // "/images/hero-church.jpg"
  chapel: string;          // "/images/chapel-interior.jpg"
  sanctuary: string;       // "/images/sanctuary.jpg"
  garden: string;          // "/images/rosary-garden.jpg"
  glass: string;           // "/images/stained-glass.jpg"
  hall: string;            // "/images/parish-hall.jpg"
  cemetery: string;        // "/images/cemetery.jpg"
  feast: string;           // "/images/feast.jpg"
  naveCdn: string;         // local alias → "/images/sanctuary.jpg" (was Pexels in hop 1)
  courtyardCdn: string;    // local alias → "/images/rosary-garden.jpg" (was Pexels in hop 1)
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

// src/components/SafeImage.tsx
export interface SafeImageProps {
  src: string;
  fallback?: string;               // default "/images/hero-church.jpg" (local hero image)
  alt: string;                     // required — a11y
  className?: string;
  loading?: "lazy" | "eager";      // default "lazy"
  fetchPriority?: "auto" | "high" | "low" | "eager";  // optional — "high" on above-the-fold heroes (fetchPriority heroes landed hop-1 2026-08-28)
}

// images export (see 20.1) — 11 entries, all local; the SafeImage onError guard covers any future external src
```

### 20.4 UI Primitive Props

```ts
// src/components/ui/Button.tsx
type Variant = "primary" | "secondary" | "ghost" | "outline-light";
type ButtonProps =
  | ({ to: string } & React.AnchorHTMLAttributes<HTMLAnchorElement> & { variant?: Variant; icon?: React.ReactNode; className?: string })
  | ({ href: string } & React.AnchorHTMLAttributes<HTMLAnchorElement> & { variant?: Variant; icon?: React.ReactNode; className?: string })
  | (React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: Variant; icon?: React.ReactNode; className?: string });
// discriminated: `to` → <Link>, `href` → <a>, else <button>; all carry `className?` via rest + cn(); icon gets aria-hidden nudge (round-5)

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
  image: string;           // local /images/* hero src (fallback /images/hero-church.jpg via SafeImage where used)
  children?: React.ReactNode;
  compact?: boolean;       // tighter vertical padding
}

// src/components/ui/Reveal.tsx
interface RevealProps { children: React.ReactNode; delay?: number; as?: "div" | "li"; className?: string; }

// src/components/ui/Accordion.tsx
interface AccordionProps { items: { question: string; answer: string }[]; } // faqs[6]
```

### 20.5 Hooks & Utils

```ts
// src/hooks/useScrolled.ts
export function useScrolled(threshold?: number): boolean; // default 12; Header uses 16

// src/hooks/useScrollProgress.ts
export function useScrollProgress(): number; // 0..1, rAF-throttled, 0 when unscrollable — ScrollProgress rail + BackToTop ring

// src/hooks/useScrollSpy.ts (round-7)
export function useScrollSpy(ids: readonly string[], options?: { offset?: number }): string | undefined;
// Active section id for the Ministries jump nav; document-order tie-break (round-7 audit L-2)

// src/utils/cn.ts
import type { ClassValue } from "clsx";
export function cn(...inputs: ClassValue[]): string; // twMerge(clsx(...))

// src/utils/massDay.ts
export type MassDayKey = "weekdays" | "saturday" | "sunday";
export function massDayKey(date: Date): MassDayKey; // drives the Worship today-highlight card

// src/utils/monogram.ts (round-5)
export function monogramGlyph(name: string): string; // About monogram discs — 7 tests

// src/utils/deepLinks.ts (round-12 F-3)
export const knownRoutePaths: readonly string[];    // every content path — drift-guarded against App.tsx (7 tests)
export function resolveHashRedirect(): void;        // pre-mount: path-style URL → #/path rewrite
```

---

## Appendix A — ADRs (Architecture Decision Records)

| # | Decision | Rationale | Consequence |
|---|---|---|---|
| ADR-1 | `HashRouter` over `BrowserRouter` | Zero-config deploy to GH Pages/S3 — no server rewrites; deep-links (`/#/worship#mass`, `/#/ministries#liturgical`) survive refresh | URLs contain `/#/` — acceptable for a parish SPA; `404.html` shim required if migrating to `BrowserRouter`. Path-style inbound links (no `#`) are normalized pre-mount by `resolveHashRedirect` (round-12 F-3) |
| ADR-2 | `vite-plugin-singlefile` | Primary `dist/index.html` (+ `dist/images/` public copy — 8 files) — trivial upload, no asset path breakage | Singlefile inlines JS+CSS only; `publicDir` is copied; no code-splitting; keep `index.html` ≤400 kB; rewrites root-relative asset refs → env-agnostic E2E assertions + built-artifact pass required (§9 #14, ADR-8) |
| ADR-3 | Tailwind v4 CSS-first `@theme` | Tokens co-located with CSS, no `tailwind.config.*` drift; `index.css` is the palette (25 colors + 2 shadows, §0 — round-12 added the terracotta-600 AA text step; hop-2's gold-700 not carried) | Extend `@theme` only, never arbitrary hex; `wcag-contrast.test.tsx` computes ratios from the token layer |
| ADR-4 | File-backed `src/data/*` (no CMS) | Typed arrays are enough for ~40 items (8+3+6+6+6+8+3+7+4+6) plus `site` + `nav`; CMS adds auth/ISR without benefit | Keep `content.ts`/`site.ts`/`nav.ts` as fallback if CMS is introduced behind `src/lib/cms/` |
| ADR-5 | Alias `@→src/` sync contract | Short imports (`@/utils/cn`) without relative `../../../` | Two-file change (`vite.config.ts` + `tsconfig.json` `paths` + `include`) — must stay synced |
| ADR-6 | `src.orig/` lineage-archive policy | The previous-hop snapshot was retained locally as a diff reference; it was **pruned 2026-08-31 (round-12 F-9)** after being discovered still tracked (64 files) — `.gitignore` does not untrack | Working tree: gone, `repo-hygiene` test fails if any `src.orig` path re-enters the index; lineage history lives only in Appendices D/F + git history. Never re-add it to lint/tsc/include |
| ADR-7 | Unified SKILL doc + §0 Volatile Facts Register (v3) | The three lineage docs restated every volatile fact 5–8×; each hop's appendices copy-forwarded without a fossil sweep — contradictory counts and previous-parish narratives survived three hops (Appendix G) | One authoritative register (§0); every other section references it; historical snapshots only in appendices with `as of <date>` labels; `docs-contract` tests enforce; fossil-sweep protocol (App G.4) is part of every future port's definition-of-done |
| ADR-8 | Built-artifact E2E pass (`playwright.built.config.ts`) | Dev server and built artifact differ: singlefile rewrites `/favicon.svg` → `./favicon.svg`, so dev-only assertions ship red against `dist/` (round-9 E2E-L1) | Same 51 specs run against `vite preview :4173` or the live host (`E2E_BASE_URL`); asset assertions written env-agnostic; `pnpm test:e2e:built` in the pre-ship gate (§11 step 4b) |

---

## Appendix B — Live-Site Validation

> **v3 fix:** hop 3's source file carried hop 2's entire smoke script (St Mary facts: 4 OFM priests, ppc 6, `#mandarin`, UEN T08CC4053H, Bukit Batok NS2/DT5). The script below is rewritten for the canonical instance (Risen Christ, Toa Payoh) and reconciled with §0/§7 facts.

**Smoke script (manual or `agent-browser` — Toa Payoh / Risen Christ routes):**

```
# after pnpm build && pnpm preview (:4173)
1.  /                      → hero (local /images/hero-church.jpg + SafeImage fallback) + quick-facts + grounds 3 + events visible
2.  /about                 → parish identity (Grateful, Faithful, and Sent) + priests 3 (phone+email) + ppcMembers 7 + monogram discs
3.  /history               → timeline 8 entries (1969–2026 Toa Payoh) via Timeline gradient rail + dot-pulse + sticky story at 1440px
4.  /worship               → #mass (weekday/weekend Mass + today-highlight card), #confession, #visit (map + hours + transport); test /mass-times, /hours-location, /visit aliases all land on Worship
5.  /worship#mass (direct) → lands on Mass schedule
6.  /worship#confession    → lands on Confession & Adoration
7.  /worship#visit         → lands on Find Us (map embed + MRT Toa Payoh NS19 Exit A + buses 88/157/163)
8.  /ministries            → 6 pills (scrollspy-highlighted) + 6 alternating sections; click each #liturgical/#faith-formation/#pastoral-care/#family-life/#youth/#language-communities scrolls to section
9.  /ministries#liturgical (direct) → lands on Liturgical
10. /ministry              → same as /ministries (alias)
11. /news-events + /news-and-events → 6 events (Parish/Devotion/Formation/Archdiocese; CEP + F.R.E.E. carry href) + bulletin band
12. /serve + /volunteer    → serveRoles 4 (title+summary) + devotions 6 (title+when+where)
13. /give + /donate        → 8 giving options (PayNow UEN T08CC4042G in a copyable row — round-12 F-4, weekend collections, Mass offerings, SSVP, cheque, cash, General Offering, Maintenance) + featured PayNow card (round-7)
14. /faq                   → 6 Q&As via Accordion + office closure band (round-7)
15. /does-not-exist        → NotFound (ghost emblem + rise-in)
16. refresh on /#/worship#visit → stays on-section (HashRouter)
17. refresh on /#/ministries#youth → stays on-section
18. /worship /news-events /donate (no #, path-style) → land on their pages, not Home (round-12 F-3 deep-links)
19. pnpm test:e2e:built    → same 51 E2E green against the built artifact (or live host via E2E_BASE_URL) — round-9/11 live pass byte-verified deploy vs 66d2398
```

What CI cannot catch: hash-scroll offset on mobile Safari, `divider-weave` paint, font FOIT, `shadow-shrine` clip on `overflow-hidden` parent, reduced-motion variants. (Image-CDN fallback timing is no longer CI-relevant — all images are local, §0; keep `SafeImage` guard for future externals.)

---

## Appendix C — The Meticulous Approach (6-Phase Workflow)

This project follows **ANALYZE → PLAN → VALIDATE → IMPLEMENT → VERIFY → DELIVER** for every non-trivial task.

1. **ANALYZE** — Mine explicit, implicit, and ambiguous requirements; explore 2–3 approaches with trade-offs.
2. **PLAN** — Sequenced phases with checklists + success criteria; present for approval.
3. **VALIDATE** — Obtain explicit go-ahead before coding.
4. **IMPLEMENT** — Library-first, modular, TDD Red→Green→Refactor (one cycle per commit) — harness is green per §0 (35 files / 202 + 51 E2E, both passes); gate on `lint && typecheck && test && test:e2e && build` (+ `test:e2e:built`) + manual smoke.
5. **VERIFY** — `pnpm lint` + `pnpm typecheck` + `pnpm test` + `pnpm test:e2e` + `pnpm test:e2e:built` + `pnpm build` + a11y/perf review + edge cases.
6. **DELIVER** — Usage instructions + runbook + follow-up recommendations + **doc sync: §0 first, then sweep** (L15, Appendix G.4).

---
## Appendix D — Lineage & Migration History

> **v3 structure:** the three source docs each carried a migration appendix describing *their own* hop (hop 1: Rother→St Joseph; hop 2: Rother→St Joseph→St Mary; hop 3: St Mary→Risen Christ), copy-forwarded with partial updates that left previous-parish fossils. This consolidated appendix merges all three into a single lineage record. **Every historical count below is a snapshot labeled `as of <date>` — none of them is the current value (current values live only in §0).**

### D.1 The Four Generations at a Glance

| | Gen 0 — Rother Shrine (origin) | Gen 1 — St Joseph BT (hop 1) | Gen 2 — St Mary of the Angels (hop 2) | Gen 3 — Risen Christ (hop 3, canonical) |
|---|---|---|---|---|
| Parish | Blessed Stanley Rother Shrine, Oklahoma City | St Joseph's Church (Bukit Timah), Singapore — https://stjoseph-bt.org.sg/ — 620 Upper Bukit Timah Road, S678116 — second-oldest Catholic parish (est. 1846) | Church of St Mary of the Angels, Bukit Batok — https://www.stmary.sg/ — 5 Bukit Batok East Ave 2, S659918 — Franciscan parish since 1970 (Portiuncula, OFM Custody of St Anthony), WOHA 2004 | Church of the Risen Christ, Toa Payoh — https://www.risenchrist.org.sg/ — 91 Toa Payoh Central, S319193 — first Catholic church in the new town, blessed 3 July 1971 |
| SKILL doc | `rothershrine-v2_SKILL.md` v1.3.0 (2026-08-27) — *later reused as hop-1 file, whose frontmatter kept `name: st-joseph-bt`* | same file, internally claiming 1.3.0 (fm) / 1.1.0 (§2) / 1.0.0 (App D) — the version conflict that v3's §0/`package_version` split resolves | `st-mary-of-angels_SKILL.md` v1.2.0 (2026-08-31) | `risen-christ_SKILL.md` v1.4.4 (2026-08-31) → **unified-v3 3.0.0** (2026-09-01, this file) |
| `package.json` | 1.3.0 | 1.0.0 (reset to mark the Singapore line; §2 of the hop-1 doc says 1.1.0 — unresolved conflict, see App G) | 1.2.0 | 1.4.4 |
| Tests (as of port day) | 29 unit + 20 E2E = 49 | as of 2026-08-27: 0 unit + 20 E2E stale; as of 2026-08-28: 16 files/92 + 35 E2E | as of 2026-08-30 (round 3): 24 files/134 + 42 E2E; as of 2026-08-31: 31 files/172 + 45 E2E | as of 2026-08-31 round-7: 32 files/179 + 48 E2E; as of 2026-08-31 round-12 (current): **35 files / 202 + 51 E2E** (§0) |
| Timeline | 1935–2023 Oklahoma/Guatemala martyr (8) | 1845–2017 Singapore hill mission (8) | 1957–2026 Franciscan Bukit Batok (8) | 1969–2026 Toa Payoh (8) |
| UEN / giving | Shrine funds (General Fund, Pipe Organ, Tepeyac Hill, Apla's Circle…) | T08CC4043C (PayNow, SSVP–Friends in Need, GIFT, Boys' Town…) | T08CC4053H + Poor & Needy T08CC4053HRSM (Tap & Give, Maintenance…) | T08CC4042G (PayNow, SSVP, Maintenance…) |
| Sixth ministry id | — (WhatToSee instead) | `mandarin` | `mandarin` (Language Communities content) | **`language-communities`** (id renamed; `#mandarin` no longer an anchor) |
| CSP `img-src` | `https:` | + `upload.wikimedia.org` (+ Pexels via hop) | `'self' data: blob:` (round-6 tightened; legacy allowlist retained unused) | `'self' data: blob:` (all local) |
| Design tokens | 24 colors + 2 shadows | 24 + 2 (unchanged) | 26 + 2 (round-7: +gold-700, +terracotta-600) | **25 + 2** (terracotta-600 only; gold-700 dropped) |

### D.2 What Each Hop Changed

**Hop 1 — Rother → St Joseph BT (2026-08-27/28):** 4 page renames (`AboutRother→About`, `WhatToSee→Ministries`, `Pilgrimage→Worship`, `Volunteer→Serve`); canonical flip `/about` ↔ `/about-blessed-stanley-rother`; route table 16→17 entries; data layer +5 interfaces (`GroundsPlace`, `Ministry`, `Priest`, `PpcMember` replacing `WhatToSeeSection`); `images` 10→11 keys (hero → Wikimedia, +8 local); `public/images/` 4→8; CSP +`upload.wikimedia.org`; E2E rewritten from 20 Rother tests to Bukit Timah routes; `src.orig/` (Rother snapshot) never committed — ignore entries inert from day one.

**Hop 2 — St Joseph BT → St Mary of the Angels (2026-08-30):** parish facts replaced wholesale (address/hours 5→7 keys/mass sunday 4→6/contact 3→5/UEN/4 socials/origin-url-ogImage getters); `Priest.phone→email` (4 OFM friars, ppc 6); all images localized (naveCdn/courtyardCdn → local aliases) and CSP tightened to `'self' data: blob:` in round 6 while retaining the legacy allowlist entry unused; `skills/` pruned in round 3 (tree at `c774ed9`) and `src.orig/` + `docs/ssh-key.txt` + `package-lock.json` untracked; `src.orig/` became the St Joseph archive (retained locally, untracked). UI rounds 4–7 added the modal drawer, today-Mass card, scrollspy, `card-tint`, `img-zoom`, `bg-gold-bloom`, gold-700 + terracotta-600, `dist/_headers`, `security-headers` tests, `deepLinks` F-3 path→hash redirects (deep-links spec born here as audit F-3).

**Hop 3 — St Mary → Risen Christ (2026-08-31):** parish facts replaced again (hours 7→7 keys — mediaCentre replaces columbarium, count unchanged; mass sunday 6→5 + `monthly` Bahasa/Tamil/Tagalog + public-holiday `note`; contact 3 phones + 5 emails incl. DPO; ppc 6→7; priests 4 OFM→3 diocesan with phone+email); sixth ministry id `mandarin`→`language-communities`; grounds `rosary-garden`→`parish-hall`; round-12 remediations (F-1 terracotta-600 AA Devotion chip, F-2 mass-card footnote /85 + date lock, F-3 path-style deep-link rewrite promoted into `main.tsx` + `utils/deepLinks.ts` with drift guard, F-4 Give UEN copyable row, F-9 src.orig prune + repo-hygiene guard); `skills/` re-added in full (`0be0fe8`); gold-700 dropped (25 colors); round-9 added `playwright.built.config.ts` + `test:e2e:built`; round-11 live pass (deploy byte-verified vs `66d2398`, E2E-J1 `agent-browser eval` lesson → pitfall #15). Detailed diff: Appendix F.

### D.3 What Never Changed (the family inheritance)

- **Design language** — warm parchment/maroon/gold on cream; Fraunces + Source Sans 3; `@theme` CSS-first (ADR-3); 24 base colors + 2 shadows byte-identical across all four generations (only the two AA text steps varied late).
- **Architecture** — static SPA, `HashRouter` (ADR-1), `vite-plugin-singlefile` (ADR-2), `@→src/` alias (ADR-5), file-backed `src/data/*` (ADR-4), 17-entry route table with 5 alias groups, double-hash-aware Layout scroll restoration, `SkipLink` hash discipline.
- **Component primitives** — `Button`/`Container`/`SectionHeading`/`Accordion`/`Reveal`/`SafeImage`/`Emblem`/`SkipLink`/`Timeline`/`SocialIcons`/`Header`/`Footer`/`PageHero`/`Layout` + `BackToTop`/`ScrollProgress` (from hop 1's "Sacred Polish" round onward).
- **Stack** — React 19.2.8, Vite 7.3.6, Tailwind 4.3.3, TypeScript 5.9.3, React Router 7.18.2, singlefile 2.3.3, eslint 9.39.5, vitest 3.2.6, playwright 1.55.1 — pinned exact throughout.
- **Method** — the 6-phase workflow (Appendix C), the pre-push five-gate, and (from v3) the §0 register + fossil-sweep protocol (ADR-7).

---

## Appendix E — Hop-2 Validation: St Mary src vs St Joseph src.orig (2026-08-30)

> Preserved from the hop-2 doc (it is the lineage's only *method* template for validating a hop). All numbers are **as of 2026-08-30**. Full report: `docs/validation-src-vs-src.orig-2026-08-30.md` — `lint 0 + typecheck 0 + 16/92 + 35 E2E + 380.19 kB` green at time of audit.

**Scope:** Did `src/` (5 Bukit Batok East Ave 2 / T08CC4053H / 1957–2026, 52 files) adopt every good contract from `src.orig/` (620 Upper Bukit Timah / T08CC4043C / 1845–2017, 52 files) and improve where the port demanded? Parish facts *must* differ; design *must not* regress.

**Verdict — 10/10 adopted, 7 improved, 0 regression:**

| Dimension | Adopted? | Improved? | Evidence |
|---|---|---|---|
| 1. Structure & interfaces | ✅ 52 files, 10 pages, 8 interfaces, 92 tests preserved | — | `find src\|wc -l` 52/52, `grep export interface` 8/8 |
| 2. Design system (`@theme` 24+2, 24 utilities, 8 keyframes) | ✅ Tokens byte-identical, 8 keyframes | ✅ `.skip-link` extracted, `link-underline 300ms→0.35s`, motion kill expanded 1→7 | `diff index.css`, `grep @keyframes` 8/8 |
| 3. Components (Layout/Header/SafeImage/Button/BackToTop/SkipLink/Accordion/ScrollProgress/cn) | ✅ All contracts (HashRouter-safe, hash discipline, 44px, grid-rows+inert) | ✅ Header `solid = scrolled\|\|!isHome\|\|mobileOpen`, `ScrollProgress` decoupled to `Layout`, `SafeImage` typed `delete dataset.fallback`, `Button` types cleaned | `diff -u src.orig/components/*` + per-file tests |
| 4. Routing & nav (17 entries, 5 alias groups/7 aliases, 9 anchors) | ✅ Routes identical, shape `NavItem` identical | ✅ CDN `naveCdn/courtyardCdn` Pexels→local, alias groups preserved | `grep -c Route` 17/17 |
| 5. Data single-source (`content.ts`/`site.ts`/`nav.ts`) | ✅ 8 interfaces preserved | ✅ `Priest.phone→email`, `hours 5→7`, `mass sunday 4→6`, `contact 3→5`, `uen 4043C→4053H`, `images 11 local` | `diff site.ts` |
| 6. Quality gates | ✅ `lint 0 + typecheck 0 + 16/92 + 35 + singlefile` | ✅ `dist/images/ 4→8`, `server.watch.ignored` adds `src.orig/**` | `pnpm lint && typecheck && test && build` |
| 7. A11y/perf | ✅ SkipLink hash, focus ring, landmarks, alt, Accordion inert | ✅ Motion kill 1→7, fewer external fetches (legacy CSP retained unused) | `rg prefers-reduced-motion` |

**7 improvements ledger:** image locality (all local), header solidity (`||mobileOpen`), motion kill expanded, type safety, `ScrollProgress` decoupling, `.skip-link` extraction, parish fidelity. No token drift, no route dropped, no test lost.

> **v3 reuse note:** run this same validation shape at every future hop — and add the two checks hop 2 lacked: (1) **fossil sweep of the doc** (App G.4 — hop 2's own doc shipped 141-vs-172 breakdown sums and a round-3 gate block while claiming current numbers), (2) **tracking audit of ignored paths** (`git ls-files` vs `.gitignore` — hop 3 found `src.orig/` still tracked 64 files, F-9).

Recorded in `README.md` (Current audits + File Hierarchy `docs/`) and `AGENTS.md` (Where to look next) and `CLAUDE.md` (Continuous Improvement + Validation Checklist row 15). Re-run `lint && typecheck && test && test:e2e && build` before claiming regression.

---

## Appendix F — Hop-3 Diff: St Mary → Risen Christ

> Corrected from the hop-3 doc's Appendix F (whose "current" column was a round-7-era snapshot: 32/179+48, package 1.3.0 — superseded values now labeled or replaced by §0 references).

| Area | St Mary (`src.orig`, pruned round-12) | Risen Christ (`src`, canonical) |
|---|---|---|
| `package.json` | `st-mary-of-angels` 1.2.0 | `risen-christ-church` **1.4.4** (§0) |
| `site.name` | Church of St Mary of the Angels / St Mary's Bukit Batok / 天神之后圣母堂 | Church of the Risen Christ / Risen Christ Toa Payoh / 耶稣复活堂 |
| `site.tagline/vision` | Towards a Prayerful & Missionary Parish. / According to Thy Word. | Grateful, Faithful, and Sent. / He is risen. |
| `site.address` | 5 Bukit Batok East Ave 2 659918 | 91 Toa Payoh Central 319193 |
| `site.hours` | 7 keys (columbarium) | 7 keys (mediaCentre Tue&Fri 12–16…, replaces columbarium) |
| `site.mass` | 7/12.15/18.30, Sat 16/18+Tamil 19.45, Sun 6, confession wknd 7 slots | 6.30a/6p, Sat 6.30a+5.30p, Sun 5, confession approach priest, monthly Bahasa/Tamil/Tagalog |
| `site.transport` | NS2/DT5 + buses Ave 2/3/4/6 | NS19 Exit A + buses 88/157/163 B52261 |
| `site.feast` | Our Lady of the Angels · Portiuncula 2 Aug | The Risen Christ — Easter Sunday |
| `site.uen` | T08CC4053H + HRSM, telegram/whatsapp/franciscans | T08CC4042G (no HRSM), freeMinistry/ssvp/bulletin/cep |
| `priests` | 4 OFM (Esmond/Julian/Justin/Robin, email) | 3 (Brian D'Souza, Arun Bellarmin, Dexter Chua — each phone+email) |
| `ppcMembers` | 6 (friars ex-officio + Custody) | 7 (Secretariat Peter Quek / Admin Audrey Rozario / Youth Calvin Swee / Pastoral Cheryl-Anne Goh) |
| `lifeTimeline` | 1957–2026 Franciscan/WOHA | 1969–2026 Toa Payoh (Ho Ping→first air-con→2003 wing→Simbang Gabi→Jubilee) |
| `grounds` | main-church/chapel/rosary-garden (Garden of Peace) | main-church/Adoration Room/parish-hall & Media Centre |
| `faqs/events/giving` | Portiuncula/columbarium/WOHA… | Velankanni/CEP/F.R.E.E./Adoration Room… |
| Sixth ministry id | `mandarin` | **`language-communities`** (anchor `#language-communities`) |
| Tests | as of 2026-08-30 round 3: 24 files/141 + 42 E2E | **35 files / 202 + 51 E2E** (§0; both dev + built passes) |
| `index.html` CSP | img-src wikimedia/pexels legacy + google | img-src `'self' data: blob:` only + google + cloudflareinsights script |
| Tokens | 26 colors + 2 (gold-700 + terracotta-600) | **25 + 2** (terracotta-600 only, §0) |
| `skills/`, `src.orig/`, secrets | skills pruned (`c774ed9`); src.orig archived St Joseph, untracked; ssh-key untracked round 6 | skills re-added in full (`0be0fe8`); **src.orig pruned + repo-hygiene guard** (F-9); ssh key **rotation still outstanding** (§0) |
| Tokens/routing/motion | shrine-* scales, 17 routes, Sacred Motion | **unchanged** — same tokens/routes/motion |

Skill filenames: `st-mary-of-angels_SKILL.md` and `rothershrine-v2_SKILL.md` are lineage redirect stubs → canonical skill (this file, superseding `risen-christ_SKILL.md` as of v3, 2026-09-01). Do not edit the stubs independently.

---

## Appendix G — Unification & Audit Ledger (v3)

> This appendix records the 2026-09-01 re-audit of the three source files (all findings re-verified at text level against the full documents; repo-state claims remain **Unverifiable** — no repo access, document-internal consistency only) and how each was resolved in this unified doc. It exists so a future reader can trace *why* v3 reads the way it does, and so future ports inherit the checklist instead of the fossils.

### G.1 Findings carried from the comparative audit — all re-validated

**Critical (1) — repo-level, OUTSTANDING:**
- **C-1 SSH key rotation.** `docs/ssh-key.txt` tracked in `0be0fe8`, untracked round 6; history still contains it. Disclosed in hop 3's §2/§3.2/§11. **Resolution:** promoted to the top-of-file notice + §0 row + L13; flagged as the only action requiring the repo owner. *Not fixable by documentation.*

**High (6) — all confirmed, all resolved in v3:**
1. Hop 1 carried three conflicting versions (frontmatter 1.3.0 / §2 1.1.0 / Appendix D 1.0.0). → Resolved: frontmatter `version: 3.0.0` (doc axis) + `package_version: 1.4.4` (repo axis) + §0 row + ADR-7; lineage versions consolidated in D.1 with `as of` labels.
2. Hop 2 §3.1 + §11 step-3 test breakdown summed to 141 while claiming 172 (6 files/28 tests missing; site 7≠8, Header 16≠17, head 13≠14 — the §2 table was the correct one). → Resolved: v3 carries the full per-file breakdown once (§0/§2, sum-verified 202) and other sections reference it.
3. Hop 2 §19 claimed 26 colors but its own table listed 24 (gold-700/terracotta-600 missing from the table while present in §4.1). → Resolved: §19 lists all 25 canonical colors + 2 shadows; gold-700 documented as a lineage note (§4.1/§19/D.1).
4. Hop 3 §10 said "32 files / 184 tests" against 35/202 everywhere else. → Resolved: §10 references §0.
5. Hop 3 §13 said "`src.orig/` is not part of this repository (inert guards)" and §14 said "pruned skills tree at `c774ed9`" — contradicting its own §2 (pruned round-12 + guard; skills re-added in `0be0fe8`). → Resolved: §13/§14 rewritten against §0's policy rows.
6. Hop 3 ADR-6 still described hop-2 semantics ("src.orig is the St Joseph BT intermediate, retained locally"). → Resolved: ADR-6 rewritten (pruned + guard), lineage in D.

**Medium (9) — all confirmed, all resolved:**
7. Hop 2 §5.2 "64 files (38+25+1)" vs its own counts line "61 (36+24+1)" vs §2's 31 test files. → Resolved: single inventory (77 = 41+35+1, §5.2/§0).
8. Hop 2 §11 gate block "24/134 + 42 E2E (round-3)" vs frontmatter 31/172+45. → Resolved: one gate block, §0-dated (§11).
9. Hop 2 §11 CSP row still required wikimedia+pexels while §3.2 documented the round-6 tightening to `'self data: blob:'`. → Resolved: §11 CSP row matches §0/§3.2.
10. Hop 2 §12 L10 "35 green (2026-08-28)" narrative fossil. → Resolved: L10 rewritten as a per-hop lesson with §0 reference.
11. Hop 3 Appendix B was entirely hop 2's smoke script (4 OFM priests, ppc 6, `#mandarin`, T08CC4053H, NS2/DT5). → Resolved: Appendix B rewritten for Risen Christ (18-step script + built pass).
12. Hop 3 ADR-3 "24 colors unchanged from rothershrine" vs its own 25. → Resolved: ADR-3 updated (25 + terracotta-600 note).
13. Hop 3 D.4 "Do not delete it" vs §2 "pruned 2026-08-31". → Resolved: D.4 folded into ADR-6/D (prune policy).
14. Hop 3 Appendix C "25 files/142 + 48 E2E" vs 35/202+51. → Resolved: Appendix C references §0.
15. Hop 3 Appendix F "current" column was round-7-era (32/179+48, package 1.3.0). → Resolved: F corrected with §0 references + labeled snapshots.

**Low (6) — all confirmed, all resolved:**
16. Hop 1 §5.2 "45 files (33+11+1)" vs counts line "52 (35+16+1)". → Resolved by design: §0/§5.2 single inventory.
17. Hop 1 §11 carried three generations of counts (11/67+27 → 9/53+22 → 16/92+35) in one section. → Resolved by design: §0.
18. Hop 2 §20 fossils: SafeImageProps comment "Bukit Timah", tail "3 CDN", PageHero "Wikimedia CDN", missing `fetchPriority`. → Resolved: §20 cleaned + `fetchPriority?` added (20.3/20.4 v3 notes).
19. Hop 3 §20.3 duplicated comment typo ("// src/components/SafeImage.tsx// src/components/SafeImage.tsx"). → Resolved.
20. Hop 3 §5.2 data comments "11 keys, 3 CDN" + "hours(5)" vs §7's all-local + hours 6. → Resolved: §5.2 tree comments match §7/§0.
21. Hop 3 L10 kept hop 2's "Bukit Batok St Mary" e2e narrative. → Resolved (L10).

**New findings surfaced by the v3 re-read (shared structural fossils — all fixed):**
22. §4.3 "Plus keyframes" prose listed 6 keyframes while §3.2 claimed 8 (`drawer-item-in`, `page-in` omitted) — in **all three** files. → Resolved: §4.3 enumerates 8.
23. §4.3 utilities tables listed ~18 classes vs the claimed 27 (counting each `rise-in-d1..d4` individually). → Resolved: §4.3 is a 27-row register.
24. §18 z-index maps omitted the `z-[60]` ScrollProgress rail in **all three** files. → Resolved: §18 rail row.
25. Hop 3 §5.2 tree + §6 said "Two hooks" while its own harness (useScrollSpy 6 tests), Quick Ref, and round-7 E2E proved `useScrollSpy.ts` exists; utils tree likewise omitted `monogram.ts`/`deepLinks.ts` (7+7 tests). → Resolved: §6 three hooks + §5.2 complete tree + §20.5 signatures.
26. Hop 2 Appendix E ("16/92+35 E2E, 2026-08-30") vs hop 2 §11 ("24/134+42, round-3, 2026-08-30") — two different snapshots for the same date, neither matching the frontmatter. → Resolved: E is labeled "as of 2026-08-30 (port-day audit)" and D.1 carries the full count trajectory.

### G.2 The systemic root cause (and the v3 countermeasure)

Every finding above is an instance of one failure mode: **volatile facts restated 5–8× per document + appendices copy-forwarded at each hop without a previous-parish fossil sweep.** Body sections healed hop over hop (hop 3's body was the cleanest) while appendices accreted (hop 3's Appendix B was 100% hop-2 content). The countermeasure is ADR-7: **§0 is the single statement of every volatile fact; everything else references it; historical numbers only exist in appendices with `as of <date>` labels; `docs-contract` tests (16) enforce at CI level.**

### G.3 Provenance of v3's content choices

| v3 section | Base | Best elements merged in |
|---|---|---|
| §0 Volatile Facts Register | **new (v3)** | countermeasure for the audit's root cause |
| §§1–3, 5–11, 13–18 | hop 3 (risen-christ) | hop 1/2 lineage facts folded into §2 environment narrative; hop-3-only `playwright.built.config.ts` + `test:e2e:built` |
| §4 | hop 3 tokens | hop 2's gold-700 as a labeled lineage note; 27-utility register completed from all hops' cumulative rounds (2/4/5/7/12) |
| §6 | hop 2/3 | `useScrollSpy` contract + round-7 tie-break rule |
| §8 | hop 3 | hop-2 round-4 modal drawer contract; hop-3 round-12 `wcag-contrast` row + terracotta-600 AA pair |
| §9 | hop 3 (15 entries) | hop-3-only #14 (dev-only E2E assets) + #15 (agent-browser eval) |
| §12 | L1–L12 (all hops) | **new L13–L15** (secret-in-history, gitignore-does-not-untrack, every-restatement-is-a-fossil) |
| §19–20 | hop 3 | `fetchPriority` + cleaned comments + §20.5 hooks/utils signatures (v3) |
| App A | hop 3's six ADRs | all corrected; **ADR-7 + ADR-8 new** |
| App B | hop 3 §10 route list | rewritten from hop 2's fossil to Risen Christ facts |
| App C | hop 3 | hop-1/2's "(+ once rewritten)" fossil removed; counts via §0 |
| App D | all three docs' migration appendices | consolidated 4-generation lineage with labeled snapshots |
| App E | hop 2 (unique) | v3 reuse note: two checks hop 2 lacked |
| App F | hop 3 (unique) | corrected to §0-referenced values |
| App G | **new (v3)** | this ledger |
| Quick Ref | hop 3 (most complete — incl. audit-ledger row) | hooks/utils rows completed (3 hooks, 4 utils) |

### G.4 Fossil-Sweep Protocol (run before any future port's doc ships)

1. **Register first.** Update §0 (one row per changed fact) *before* touching prose anywhere else.
2. **Sweep the old value.** `rg -n "<old value>"` across the doc, README, AGENTS, CLAUDE — every hit is either updated to a §0 reference or explicitly labeled `as of <date>` in an appendix.
3. **Previous-parish grep.** For every parish-specific token of the *previous* instance (address, UEN, phone numbers, feast date, priest names, ministry ids, MRT station, bus list, parish-specific anchor ids like `#mandarin`), run `rg -n` and verify each remaining hit lives in a labeled lineage appendix: `rg -n "620 Upper|T08CC4053H|T08CC4043C|Bukit Batok|Bukit Timah|Portiuncula|NS2|DT5|Cashew|#mandarin|St Mary|St Joseph"`.
4. **Sum every count you state.** Test counts, file counts, color/utility/keyframe counts, route/alias/anchor counts — recompute; never copy a sum forward.
5. **Reconcile code samples with the tree.** Every file the test harness references must appear in §5.2's tree; every §4.3 row must match the §0 utility count; every §18 layer must match the z-indexes named in §5.5.
6. **Tracking audit.** `git ls-files` vs `.gitignore` for `src.orig/`, secrets, lockfiles — ignore ≠ untracked (L14).
7. **Appendix B is parish-critical.** The smoke script names priests/ppc/UEN/anchors — rewrite it wholesale; it is the single most-fossilized section in the lineage (finding #11).
8. **Gate.** `docs-contract` tests green + a fresh reviewer reads §0 against the frontmatter and Quick Ref in one pass and finds zero unexplained numbers.

---

## Quick Reference Card

| Need | Path |
|---|---|
| Visitor overview | `README.md` |
| 60-sec agent cheat sheet | `AGENTS.md` |
| Deep workflow + parish fidelity | `CLAUDE.md` |
| Intent lineage | `docs/prompts.md` (if present) |
| **Volatile facts (versions, counts, policies) — 35/202 + 51 E2E** | **§0 of this file — the single source; everything else defers to it** |
| Tokens (25 colors + 2 shadows, §0) + utilities (27 + 8 keyframes, §4.3) | `src/index.css` (`--font-sans` alias `--font-body`; utilities incl. `gold-rule`/`gold-rule-left`/`hero-ken-burns`/`rise-in`+`rise-in-d1..d4`/`menu-in`/`drawer-in`/`drawer-item-in`/`page-in`/`dot-pulse`/`card-lift`/`card-tint`/`link-underline`/`reveal`+`reveal-visible`/`skip-link`/`divider-weave`+`divider-weave-thin`/`bg-grain`+`bg-adobe-texture`+`bg-gold-bloom`/`mask-fade-b`/`img-zoom`) |
| Route table + aliases + anchors | `src/App.tsx` — 17 Route entries (16 content paths + `*`), 7 alias paths in 5 groups (§5.4), 9 hash anchors (3 on `/worship`, 6 on `/ministries` — sixth is `#language-communities`) + path-style deep-link rewrite (`utils/deepLinks.ts` → `main.tsx` pre-mount) |
| Nav single-source | `src/data/nav.ts` (`primaryNav` 6 + `footerNav` 10, with `description` on children) |
| Content arrays (10) + images + site | `src/data/content.ts` (per §0/§7.1: `priests` 3 (phone+email), `ppcMembers` 7, `lifeTimeline` 8 [1969–2026 Toa Payoh], `grounds` 3 (main-church/Adoration Room/parish-hall), `ministries` 6 (Language Communities last), `faqs` 6, `upcomingEvents` 6 (Velankanni/CEP/F.R.E.E., 2 with href), `givingOptions` 8 (PayNow T08CC4042G etc.), `serveRoles` 4, `devotions` 6 + `images` 11 all-local) + `src/data/site.ts` (`site as const`: hours 7 + mass 9 keys (sunday + monthly + note) + transport NS19/88-157-163 + feast Easter Sunday + uen T08CC4042G + cheque + 3 socials + freeMinistry/ssvp/bulletin/cep + maps + origin/url/ogImage) |
| Primitives | `src/components/ui/*` (Button/Container/SectionHeading/Accordion/Reveal) + SafeImage/Emblem/SkipLink/Timeline/SocialIcons/PageHero/Layout/Header/Footer/BackToTop/ScrollProgress |
| Hooks (3) | `src/hooks/useScrolled.ts` (threshold 12 default; Header uses 16) + `useScrollProgress.ts` (rAF; BackToTop ring + ScrollProgress rail) + `useScrollSpy.ts` (round-7 Ministries jump-nav; document-order tie-break) |
| Utils (4) | `src/utils/cn.ts` (`twMerge(clsx)`) + `massDay.ts` (`massDayKey` — Worship today-highlight) + `monogram.ts` (About discs) + `deepLinks.ts` (`knownRoutePaths` + `resolveHashRedirect` — round-12 F-3; drift-guarded against `App.tsx`) |
| Images | `public/images/*.jpg` (8 files → `dist/images/`) + `public/favicon.svg` — all local (`naveCdn`→`sanctuary.jpg`, `courtyardCdn`→`rosary-garden.jpg` are local aliases) + `images` export (11 keys all `/images/*`, `SafeImage` with `hero-church.jpg` fallback) |
| Vite alias + singlefile | `vite.config.ts` (`@→src`, `viteSingleFile()` + `test {globals,jsdom,setupFiles,include,exclude}` + `server.watch.ignored` [skills,dist,playwright-report,test-results,coverage,src.orig]) |
| TS strict + include | `tsconfig.json` (`strict` + `noUnused*` + `noFallthroughCasesInSwitch`/`isolatedModules`/`noEmit` + `include: ["src","vite.config.ts","eslint.config.js","playwright.config.ts","playwright.built.config.ts"]` + `types: ["node","vitest/globals"]` + `paths @/*` + `baseUrl:"."`) |
| E2E (dev + built) | `playwright.config.ts` (vite :5173) + `playwright.built.config.ts` (vite preview :4173; `E2E_BASE_URL` → live host) — same 51 specs (§0) |
| Pre-ship gate | `pnpm lint && pnpm typecheck && pnpm test && pnpm test:e2e && pnpm build` (+ `pnpm test:e2e:built`) → counts per §0 → `dist/index.html` + `dist/_headers` + `dist/favicon.svg` + `dist/images/` (8 files) → `pnpm preview` → manual smoke (Appendix B) |
| Frozen reference | (pruned round-12, F-9) `src.orig/` was the archived St Mary port — removed from tree + index 2026-08-31; `.gitignore` entry + `repo-hygiene` guard prevent re-entry; lineage history: Appendices D/F + git history |
| CSP allowlist | `index.html` — `img-src 'self' data: blob:` (all images local), `frame-src https://www.google.com` (maps embed), `script-src` inline (singlefile) + `static.cloudflareinsights.com` — `SafeImage` fallback `/images/hero-church.jpg` |
| **Outstanding security action** | **Rotate the ssh key leaked in git history (`docs/ssh-key.txt`, commit `0be0fe8`) — repo owner action; working-tree guard is `src/repo-hygiene.test.ts`** |
| Audit ledger + remediation | `docs/code-review-audit-round6-2026-08-31.md` + `docs/remediation-plan-round6-2026-08-31.md` (round 6) · `docs/code-review-audit-round7-2026-08-31.md` + `docs/remediation-plan-round7-2026-08-31.md` (round-7 audit of the "Honest Light" commits — zero new C/H/M; scrollspy tie-break + E2E sleep remediation) · `docs/design-enhancement-round7-2026-08-31.md` (round-7 design) · `docs/remediation-plan-round9-2026-08-31.md` (round-9 built-artifact E2E contract — E2E-L1 favicon form + `playwright.built.config.ts`) · `docs/e2e-live-pass-round11-2026-08-31.md` (round-11 live pass vs `66d2398` — byte-verified deploy + tri-env + journey; E2E-J1 `agent-browser eval` backslash lesson → pitfall #15) · `docs/UI-UX-Design-Audit_StMaryOfAngels_vs_RisenChrist.md` + `docs/remediation-plan-round12-2026-08-31.md` + `docs/remediation-round12-2026-08-31.md` (round-12 comparative UI/UX audit remediation — F-1 Devotion chip AA terracotta-600 5.36:1, F-2 mass-card footnote /85 + date lock, F-3 path-style deep-link rewrite, F-4 Give UEN copyable row, F-9 src.orig prune; TDD red→green) · **unification audit 2026-09-01: Appendix G** |

## reference `package.json`
```json
{
  "name": "risen-christ-church",
  "private": true,
  "version": "1.4.4",
  "type": "module",
  "packageManager": "pnpm@11.0.0",
  "engines": {
    "node": ">=20"
  },
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "typecheck": "tsc --noEmit",
    "lint": "eslint . --max-warnings 0",
    "lint:fix": "eslint . --fix",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "test:e2e": "playwright test",
    "test:e2e:built": "playwright test --config=playwright.built.config.ts",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:report": "playwright show-report"
  },
  "dependencies": {
    "clsx": "2.1.1",
    "lucide-react": "1.34.0",
    "react": "19.2.8",
    "react-dom": "19.2.8",
    "react-router-dom": "7.18.2",
    "tailwind-merge": "3.6.0"
  },
  "devDependencies": {
    "@eslint/js": "9.39.5",
    "@playwright/test": "1.55.1",
    "@tailwindcss/vite": "4.1.17",
    "@testing-library/jest-dom": "6.6.3",
    "@testing-library/react": "16.2.0",
    "@testing-library/user-event": "14.5.2",
    "@types/node": "22.20.1",
    "@types/react": "19.2.18",
    "@types/react-dom": "19.2.5",
    "@vitejs/plugin-react": "5.2.0",
    "@vitest/coverage-v8": "3.2.6",
    "eslint": "9.39.5",
    "eslint-plugin-react-hooks": "5.2.0",
    "eslint-plugin-react-refresh": "0.4.19",
    "globals": "16.1.0",
    "jsdom": "26.1.0",
    "tailwindcss": "4.3.3",
    "typescript": "5.9.3",
    "typescript-eslint": "8.28.0",
    "vite": "7.3.6",
    "vite-plugin-singlefile": "2.3.3",
    "vitest": "3.2.6"
  },
  "allowScripts": {
    "esbuild@0.27.7": true,
    "esbuild@0.25.12": true
  }
}
```

## reference `AGENTS.md`
```markdown
# AGENTS — risen-christ-church

> Port of https://www.risenchrist.org.sg/ — Church of the Risen Christ, Toa Payoh (91 Toa Payoh Central, Singapore 319193). First Catholic church in the new town, blessed 3 July 1971 by Archbishop Michel Olçomendy — Singapore's first fully air-conditioned church (Fr Pierre Abrial, $450k). Grateful, Faithful, and Sent. Static SPA — no backend, no DB, no SSR. For deep conventions, workflow, and design system detail, read `CLAUDE.md`.

## Stack

`React 19.2.8` + `Vite 7.3.6` + `Tailwind CSS 4.3.3` (`@tailwindcss/vite 4.1.17`, CSS-first `@theme` inline in `src/index.css`) + `TypeScript 5.9.3` strict + `React Router 7.18.2` `HashRouter` + `vite-plugin-singlefile 2.3.3` (primary `dist/index.html` + `dist/images/` for GH Pages / S3) + `eslint 9.39.5` flat + `vitest 3.2.6` (`jsdom 26.1.0`) + `@testing-library/react 16.2.0` + `playwright 1.55.1` (chromium) · alias `@` → `src/` (sync `vite.config.ts` `path.resolve(__dirname,"src")` ↔ `tsconfig.json` `paths: {"@/*":["src/*"]}` + `baseUrl:"."`) · `pnpm 11.0.0` (`packageManager` + `engines node>=20`, `pnpm-lock.yaml` committed, `--frozen-lockfile` in CI), `npm` works · all deps pinned exact — no `^` in `package.json` (re-pin on upgrade, update docs)

## Commands

All commands verified in `package.json` `scripts`. Don't document a script until it exists there.

| Command | Purpose |
|---|---|
| `pnpm install` | Install deps (Node 20+ for Vite 7, pnpm 11) — pnpm is the supported path; `npm ci` needs `--legacy-peer-deps` (typescript-eslint 8.28.0 peer range predates TS 5.9) |
| `pnpm dev` | Vite HMR dev server (default `http://localhost:5173`) |
| `pnpm build` | Production single-file build → `dist/index.html` |
| `pnpm preview` | Preview `dist` locally |
| `pnpm typecheck` | Type gate `tsc --noEmit` — **run before every push** |
| `pnpm lint` | ESLint flat (`eslint . --max-warnings 0`) |
| `pnpm lint:fix` | ESLint auto-fix (`eslint . --fix`) |
| `pnpm test` | Vitest `jsdom` `run` — **35 files / 202 tests** (`ci-workflow` 4 + `repo-hygiene` 3 + `docs-contract` 16 + `cn` 5 + `nav` 7 + `content` 10 + `site` 8 + `massDay` 5 + `monogram` 7 + `deepLinks` 7 + `Button` 11 + `SkipLink` 3 + `Accordion` 6 + `SafeImage` 6 + `Header` 17 + `BackToTop` 7 + `Reveal` 2 + `wcag-contrast` 5 + `Ministries` 3 + `cta-bands` 6 + `worship-mass` 6 + `about-visuals` 4 + `event-chips` 3 + `give-featured` 2 + `give-uen` 3 + `card-affordances` 6 + `Timeline` 3 + `NotFound` 2 + `History` 2 + `Layout` 2 + `useScrollProgress` 4 + `useScrollSpy` 6 + `ScrollProgress` 2 + `head` 13 + `security-headers` 6) via `src/test/setup.ts` |
| `pnpm test:watch` | Vitest watch mode |
| `pnpm test:coverage` | Vitest with coverage (`vitest run --coverage`) |
| `pnpm test:e2e` | Playwright `chromium` (8 specs — **51 tests**: smoke 11 + navigation 8 + ministries 4 + give-faq 4 + enhancements 7 + enhancements-round5 6 + enhancements-round7 8 + deep-links 3) — Risen Christ copy (91 Toa Payoh Central, He is risen, Velankanni, Toa Payoh NS19) |
| `pnpm test:e2e:ui` | Playwright UI mode |
| `pnpm test:e2e:report` | Open last Playwright HTML report |
| `pnpm lint && pnpm typecheck && pnpm test && pnpm test:e2e && pnpm build` | Pre-push gate (all five must be green) |

## Structure

```
src/ (35 files / 202 tests — 41 source + 35 tests + 1 setup + 51 E2E)
  App.tsx              # HashRouter + 17 Route entries (16 content paths + * NotFound; see Routing below)
  main.tsx             # StrictMode + createRoot + resolveHashRedirect pre-mount rewrite (round-12 F-3)
  index.css            # @theme tokens (25 colors + 2 shadows) + @layer base/utilities (26 utilities: text-balance, bg-adobe-texture, bg-gold-bloom, bg-grain, divider-weave, divider-weave-thin, gold-rule, gold-rule-left, hero-ken-burns, img-zoom, mask-fade-b, reveal, reveal-visible, rise-in + rise-in-d1..d4, menu-in, drawer-in, drawer-item-in, page-in, dot-pulse, card-lift, link-underline, skip-link + 8 keyframes gold-rule-draw/hero-ken-burns/rise-in/menu-in/drawer-in/drawer-item-in/page-in/halo-pulse + themed scrollbar (maroon thumb on parchment track, webkit + scrollbar-color))
  components/          # Layout (+SkipLink +BackToTop +ScrollProgress), Header (useScrolled(16) + aria-current nav states + menu-in/drawer-in entrances + modal drawer: dialog/aria-modal/focus-trap/focus-restore + Escape handler), Footer (3 socials + SSVP/Free/CEP/bulletin links), PageHero (rise-in staged content), Emblem, Timeline (dot-pulse halos), SocialIcons (3: Facebook/Instagram/YouTube), SafeImage (local fallback), BackToTop (threshold 480, progress ring, reduced-motion-aware), ui/{Button (active press),Container,SectionHeading,Accordion (animated grid-rows collapse),Reveal}
  hooks/               # useScrolled.ts (threshold 12 default; Header passes 16) + useScrollProgress.ts (0..1, rAF-throttled) + useScrollSpy.ts (round-7 ministries scrollspy, viewport-middle-band IO)
  pages/               # Home, About, History, Worship, Ministries, NewsEvents, Serve, Give, FAQ, NotFound (10 pages, all named exports: Home, About, History, Worship, Ministries, NewsEvents, Serve, Give, FAQ, NotFound)
  data/                # nav.ts (primaryNav + footerNav with description on children), content.ts (TimelineEntry/GroundsPlace/Ministry/FaqItem/EventItem/GivingOption/Priest/PpcMember + priests[3] (Brian D'Souza, Arun Bellarmin, Dexter Chua — each email+phone)/ppcMembers[7]/lifeTimeline[8 1969–2026]/grounds[3]/ministries[6]/faqs[6]/upcomingEvents[6]/givingOptions[8]/serveRoles[4]/devotions[6] + images {hero/heroFallback/chapel/sanctuary/garden/glass/hall/cemetery/feast/naveCdn/courtyardCdn — all local}), site.ts (site as const: name/shortName/耶稣复活堂/tagline/vision + address {street/city/zip/full+query getters} + hours {gates/mainChurch/chapel/reception/parishOffice/mediaCentre/adorationRoom} + mass {weekdayMorning/weekdayEvening/saturday/sunday[5]/confession/adoration/secondCollection + note + monthly (Bahasa/Tamil/Tagalog)} + contact {parishPriestPhone/officePhone/mediaPhone/email/adminEmail/connectEmail/youthEmail/dpoEmail} + transport {mrt Toa Payoh NS19 / buses 88,157,163 B52261} + feast {The Risen Christ, Easter Sunday} + uen T08CC4042G/chequePayee/facebook/instagram/youtube/archdiocese/mapsUrl/mapsEmbedSrc + freeMinistry/ssvp/bulletin/cep + origin/url/ogImage)
  utils/               # cn.ts — twMerge(clsx), always merge via cn() + massDay.ts — massDayKey(date): 'weekdays'|'saturday'|'sunday', single source for the Worship today-highlight + monogram.ts — monogram(name): "Fr Brian D'Souza" → "BD", honorific stripping
  components/EventMeta.tsx # shared categoryTone + EventMeta chip (Home + NewsEvents, R5-M1 remediation)
vite.config.ts         # alias @→src + test { globals, jsdom, setupFiles: src/test/setup.ts, include: src/**/*.{test,spec}.{ts,tsx}, exclude: e2e/** } + server.watch.ignored [skills/**, dist/**, playwright-report/**, test-results/**, coverage/**, src.orig/**] + viteSingleFile()
tsconfig.json          # strict + noUnusedLocals/noUnusedParameters/noFallthroughCasesInSwitch/isolatedModules/noEmit + include [src, vite.config.ts, eslint.config.js, playwright.config.ts] + types [node, vitest/globals] + paths @/*
eslint.config.js       # flat config (typescript-eslint 8 + react-hooks 5 + react-refresh); ignores [dist, node_modules, coverage, playwright-report, test-results, skills, src.orig]
playwright.config.ts   # Playwright 1.55.1 (chromium, webServer → pnpm exec vite :5173, expect timeout 15s; CSP is a meta tag in index.html, not a config header)
e2e/                   # 8 specs — 51 tests: smoke.spec.ts (11) + navigation.spec.ts (8) + ministries.spec.ts (4) + give-faq.spec.ts (4) + enhancements.spec.ts (7) + enhancements-round5.spec.ts (6) + enhancements-round7.spec.ts (8) + deep-links.spec.ts (3) + helpers.ts — Risen Christ (91 Toa Payoh Central, He is risen)
.github/workflows/ci.yml # CI: lint → typecheck → test → test:e2e → build + artifacts (Node 24, pnpm 11)
public/                 # 8 images (hero-church.jpg, chapel-interior.jpg, sanctuary.jpg, rosary-garden.jpg, stained-glass.jpg, parish-hall.jpg, cemetery.jpg, feast.jpg → dist/images/) + `_headers` (Cloudflare Pages security headers → dist/_headers — honored only on Cloudflare Pages deploys; the current proxied host serves none — round-6 audit H1) + `favicon.svg` (→ dist/favicon.svg); all local images — CDN keys hero/naveCdn/courtyardCdn now point to local fallbacks
index.html             # Google Fonts Fraunces + Source Sans 3; CSP `img-src 'self' data: blob:` only (no legacy wikimedia/pexels), `object-src 'none'`, `base-uri 'self'`, frames from google.com (maps embed); OG tags + Church JSON-LD for Church of the Risen Christ (www.risenchrist.org.sg)
src.orig/              # (pruned round-12, 2026-08-31) — was the archived St Mary of the Angels port (5 Bukit Batok East Ave 2, Portiuncula, OFM Custody 1970 / WOHA 2004); had remained git-tracked despite `.gitignore` since round 3 — 64 files found tracked by the round-12 audit and removed (`git rm -r --cached` + tree removal); `src/repo-hygiene.test.ts` guard now fails if it re-enters; lineage: Rother Shrine → St Joseph BT → St Mary of the Angels (src.orig) → Risen Christ (src)
```

## Quirks — would break if guessed wrong

- **HashRouter is intentional** — static hosts (GH Pages / S3) have no SPA fallback. Don't switch to `BrowserRouter` without adding a `404.html` redirect. Deep links are `/#/worship`, `/#/ministries#liturgical`, etc.
- **`viteSingleFile()` inlines JS+CSS** — `public/images/` is still copied to `dist/images/` (Vite `publicDir` is not inlined; upload both). No assumed code-splitting. Dynamic `import()` that expects chunks will be inlined or break.
- **Alias `@` must stay in sync** — `vite.config.ts` (`path.resolve(__dirname,"src")`) ↔ `tsconfig.json` (`paths: {"@/*":["src/*"]}`, `baseUrl:"."`) — change both.
- **Tailwind v4 has no `tailwind.config.js`** — tokens live only in `src/index.css` `@theme`. Don't add arbitrary `bg-[#...]`; extend `@theme` with a named `shrine-*` token.
- **TS strict will fail on unused code** — `noUnusedLocals:true` + `noUnusedParameters:true` + `noFallthroughCasesInSwitch:true` + `isolatedModules:true` + `noEmit:true`. Clean unused vars/params before commit.
- **Test/lint harness** — `eslint 9.39.5` flat + `vitest 3.2.6` (jsdom) + `@testing-library/react 16.2.0` + `playwright 1.55.1` (chromium) — gate is `lint && typecheck && test && test:e2e && build` (`35 files / 202` via `src/test/setup.ts` + `51 E2E` via `e2e/`: smoke 11 + navigation 8 + ministries 4 + give-faq 4 + enhancements 7 + enhancements-round5 6 + enhancements-round7 8 + deep-links 3). CI mirrors this. `eslint` ignores `skills/` + `src.orig/`; `vite.config.ts` `test` + `server.watch.ignored` + `tsconfig.json` `types [vitest/globals]` are required.
- **`skills` is vendored, git-tracked reference content** — pruned in round 3 (2026-08-30), re-added in full at `0be0fe8` (2026-08-31): `skills/skills-catalog.md` + per-skill `SKILL.md` files are tracked again. Tooling ignores it regardless: `eslint.config.js` `ignores` + `tsconfig` excludes + `vite.config.ts` watch-ignores. Don't lint, type-check, or import from it.
- **Google Fonts loaded in `index.html`** — `Fraunces` (display) + `Source Sans 3` (body). CSP in that file whitelists `fonts.googleapis.com`/`fonts.gstatic.com` + `google.com` for the maps iframe. No `upload.wikimedia.org`/`images.pexels.com` allowlist (removed for Risen Christ — all `images.*` are local). Don't add runtime font loaders in components.
- **`Layout.tsx` handles hash scroll** — double-hash aware (`#/ministries#liturgical` → split on `#` + strip `/`) + `setTimeout 80ms` + fallback `window.scrollTo`. Current anchor targets are `#mass`/`#confession`/`#visit` on `/worship` and `#liturgical`/`#faith-formation`/`#pastoral-care`/`#family-life`/`#youth`/`#language-communities` on `/ministries`. Preserve when extending layout. Layout also wraps outlet in a keyed `page-in` container (`data-testid="page-container"` + `data-route`) so route changes replay entrance while hash-only updates keep the node.
- **`vite.config.ts` `server.watch.ignored`** — ignores `**/skills/**`, `**/dist/**`, `**/playwright-report/**`, `**/test-results/**`, `**/coverage/**`, `**/src.orig/**` to avoid `ENOSPC` file-watcher limit from the vendored `skills/` tree (contains large `.venv`) and archived `src.orig/`.
- **`SafeImage` fallback** — `src/components/SafeImage.tsx` wraps `<img>` with `fallback` default `/images/hero-church.jpg`, `loading="lazy"` default, optional `fetchPriority` (set `"high"` on above-the-fold heroes — Home hero + PageHero), and `onError` → `dataset.fallback` guard to swap `src` once. All current `images.*` are local; CDN keys `naveCdn`/`courtyardCdn` point to local fallbacks. Use `SafeImage` for any future external image; don't use bare `<img>` for CDN sources.
- **SkipLink never rewrites the hash** — `src/components/SkipLink.tsx` `preventDefault`s and imperatively focuses `#main-content` (`<main>` in `Layout`). A native jump would rewrite the hash and route to NotFound under HashRouter.
- **Header close-on-activation** — the mobile drawer closes on any in-drawer link activation (`onClickCapture` on the drawer `<nav>`), not only on pathname change: a tap on a link to the **current** route never changes `pathname`, so the `useEffect([pathname,hash])` close cannot fire (H-1 in `docs/code-review-audit-2026-08-28.md` — fixed 2026-08-28). Desktop dropdown `<ul>` also closes on child-link click. Drawer top-level links carry `aria-current="page"` when any child is active; hamburger is `h-11 w-11` (44px). Header also handles `Escape` to close menus/drawer.
- **Header modal drawer (round 4, audit L-5)** — the mobile drawer is a modal dialog (`role="dialog"` + `aria-modal="true"` + `aria-label="Site menu"` + `tabIndex={-1}`): the panel receives initial focus on open, `Tab`/`Shift+Tab` cycle inside it (trap in `handleDrawerKeyDown`), every close path (toggle, `Escape`, in-drawer link, route change, outside `pointerdown`) restores focus to the hamburger toggle (`drawerWasOpenRef` guard keeps mount from stealing focus), and a `pointerdown` outside the drawer closes it. Don't downgrade it back to a disclosure or remove the trap.
- **`useScrolled` threshold** — `src/hooks/useScrolled.ts` defaults to `12`; `Header.tsx` calls `useScrolled(16)` to delay the transparent→solid switch on Home. Don't "fix" the mismatch — it's intentional.
- **`ScrollProgress` is decoupled from Header** — `src/components/ScrollProgress.tsx` is a fixed `h-[3px]` rail (`data-testid="scroll-progress"`, `aria-hidden`, `scaleX(progress)`) rendered by `Layout` at `z-[60]`; it is not inside `Header`. `Header` solid calculation now includes `mobileOpen`.
- **`Ministries` jump nav** — uses `<Link to="/ministries#id">` (not plain `<a href="#id">`) to preserve HashRouter route; plain `#id` would replace the hash and route to NotFound. Renders `ministries.map` → 6 pill links (`#liturgical`, `#faith-formation`, `#pastoral-care`, `#family-life`, `#youth`, `#language-communities`) with `aria-label="Jump to ministry"` + `aria-current="true"` on the pill matching `useLocation().hash` + alternating `bg-shrine-cream`/`bg-shrine-parchment` sections.
- **"Sacred Motion" package** (docs/ui-ux-remediation-plan-2026-08-28.md — all transform/opacity only, gated by the global `prefers-reduced-motion` block in `index.css`):
  - **Staged entrances** — `.rise-in` + `.rise-in-d1..d4` delay steps animate Home hero and PageHero content on mount (keyframe `rise-in`, fill `both` → settles at opacity 1; instant under reduced motion).
  - **Menu entrances** — `.menu-in` on the desktop dropdown `<ul>`, `.drawer-in` on the mobile drawer (both conditionally rendered, so the keyframe runs on mount).
  - **Accordion collapse** — panels use the `grid-template-rows 0fr→1fr` technique (`grid grid-rows-[0fr|1fr]` + inner `overflow-hidden`), NOT `hidden`. Closed panels carry `aria-hidden="true"` + `inert` so screen readers/keyboard skip them; `aria-expanded` on the button is the single source of truth.
  - **Card hover system** — `.card-lift` (lift + `shadow-shrine` + gold border tint) is the one true card hover; grounds/devotion/pillar/role/giving/event cards all use it. Don't re-add ad-hoc `hover:-translate-y-*` chains.
  - **Link affordances** — `.link-underline` draws a gold underline via a `::after` scaleX transform (footer nav, top-bar Give link). Buttons add `active:translate-y-0 active:scale-[0.98]` press feedback.
  - **Timeline halo** — `.dot-pulse::after` is an expanding gold ring (keyframe `halo-pulse`, infinite); reduced-motion sets it to `opacity: 0`.
- **`BackToTop` contract** — `src/components/BackToTop.tsx` (mounted in `Layout` before `<Footer/>`): appears when `window.scrollY > 480`, hides below (`aria-hidden` + `tabIndex -1` + `pointer-events-none` when hidden), click → `window.scrollTo({ top: 0, behavior: matchMedia('(prefers-reduced-motion: reduce)') ? 'auto' : 'smooth' })`. It never touches the hash (HashRouter-safe). It carries a progress ring (`data-testid="back-to-top-progress"` + inner `circle[data-progress]`) whose `stroke-dashoffset` fills with `useScrollProgress`. When it hides while focused, it blurs itself first (focus must not rest inside an `aria-hidden` subtree — round-3 audit L-4).
- **Worship "today" Mass highlight** — `src/utils/massDay.ts` `massDayKey(date)` maps `getDay()` 0→sunday / 6→saturday / rest→weekdays; `Worship.tsx` renders the matching card via a local `MassCard` with `data-testid="mass-card"` + `data-card-day` + `data-today="true"` + gold top rule + "Today" chip (exactly one per calendar day — never hardcode a day or duplicate the mapping). Sunday slots are a gold-dot list with `hover:bg-shrine-maroon-50/60`.
- **Round-5 "Light of the Portiuncula" package** (`docs/design-enhancement-round5-2026-08-30.md` — St Mary enhancement, retained in motion system) — event cards render the category inside a bordered gold chip (`rounded-full` + `categoryTone` color) with the date in `font-display` beside it (shared `src/components/EventMeta.tsx` — `categoryTone` + `EventMeta`); the History story column is `lg:sticky lg:top-28 lg:self-start` (`data-testid="history-story"`) beside the timeline; the Timeline rail is `[data-testid="timeline-rail"]` (`bg-gradient-to-b ... via-shrine-gold-400/70`) — don't restore `border-l`; `.img-zoom` drifts only inside `.group` cards; `.bg-gold-bloom` decorates the Home + Give dark bands; Button icons render inside an `aria-hidden` span with `group-hover:translate-x-0.5` nudge; NotFound carries the ghost `Emblem` + `rise-in` staging; About pillars use ghost `font-display text-5xl` numerals and friar cards carry `aria-hidden` monogram discs (`src/utils/monogram.ts` `monogram()` handles Fr/Friar, covered by `monogram.test.ts` in `src.orig`).
- **`aria-current` nav contract** — Header plain links get `aria-current="page"` when `pathname === item.to`; dropdown parent buttons get `aria-current="true"` + gold tint when any `child.to.split("#")[0] === pathname`; dropdown child links get `aria-current="page"` on exact `pathname + hash === child.to`; Ministries pills get `aria-current="true"` on hash match. Mobile drawer parents get `aria-current="page"` when a child route is active (e.g. `/history` → About parent current). Header hamburger is `h-11 w-11` (44px touch target) — don't shrink it.

## Conventions

- **Routing:** `App.tsx` is the only route table — 17 `Route` entries (16 content paths + `*` NotFound) covering 10 pages, with 7 alias paths in 5 groups (`/worship` canonical for `/mass-times`+`/hours-location`+`/visit`; `/ministries` canonical for `/ministry`; `/news-events` canonical for `/news-and-events`; `/serve` canonical for `/volunteer`; `/give` canonical for `/donate`) and hash anchors on two pages: `/worship` → `#mass`/`#confession`/`#visit` (Mass schedule, Confession & Adoration, Find Us) and `/ministries` → `#liturgical`/`#faith-formation`/`#pastoral-care`/`#family-life`/`#youth`/`#language-communities` (6 ministry sections). Nav is driven by `src/data/nav.ts` (`primaryNav` with `description` on children + `footerNav: NavLink[]`) — update there, `Header`/`Footer` render from it. `Header` dropdowns and `Ministries` jump nav must use `<Link to="/path#id">`, never `<a href="#id">`.
- **Data:** `src/data/content.ts` is the data layer — 8 exported interfaces (`TimelineEntry`, `GroundsPlace`, `Ministry`, `FaqItem`, `EventItem`, `GivingOption`, `Priest`, `PpcMember`) and 10 exports: `priests[3]` (Fr Brian D'Souza, Fr Arun Bellarmin, Fr Dexter Chua — each `email`+`phone`) + `ppcMembers[7]` (Parish Priest + 2 Assistants + Secretariat Peter Quek / Admin Audrey Rozario / Youth Calvin Swee / Pastoral Cheryl-Anne Goh) + `lifeTimeline[8]` spanning **1969–2026** Toa Payoh (1969 Ho Ping Centre + tender → 1971 Olçomendy $450k first air-con → 1970s many tongues Velankanni → 2003 four-storey → 2010s Filipino/Indonesian/Myanmar Simbang Gabi → 2021 Golden Jubilee → 2023 Fr Brian → 2026 Grateful/Faithful/Sent) + `grounds[3]` (`main-church`/`chapel`/`parish-hall`, each with `image`+`imageFallback`+`imageAlt` — all local) + `ministries[6]` (`liturgical`/`faith-formation`/`pastoral-care`/`family-life`/`youth`/`language-communities`→ Bahasa 1st Fri 20.00, Tamil 2nd Sun 19.00, Tagalog 4th Sun 15.00, Mandarin 8.15) + `faqs[6]` (Mass/confession/how to get there/parking/baptism-marriage/columbarium-funeral) + `upcomingEvents[6]` (`title`+`date`+`summary`+`category` Parish|Devotion|Formation|Archdiocese + optional `href` — Velankanni 10–12 Sep, CEP, F.R.E.E. Acts…) + `givingOptions[8]` (PayNow UEN T08CC4042G, collections, cheque payable Church of the Risen Christ, cash at office, etc. — no HRSM) + `serveRoles[4]`/`devotions[6]` untyped consts + `images` (11 keys: `hero`/`heroFallback`/`chapel`/`sanctuary`/`garden`/`glass`/`hall`/`cemetery`/`feast` local, `naveCdn`/`courtyardCdn` local aliases). `src/data/site.ts` (`site as const`) is the canonical single source for `name` Church of the Risen Christ / `shortName` Risen Christ Toa Payoh / `chineseName` 耶稣复活堂 / `tagline` Grateful, Faithful, and Sent. / `vision` He is risen. + `address` 91 Toa Payoh Central Singapore 319193 (`full`/`query` getters) + `hours` (7 keys: `gates`, `mainChurch`, `chapel` Adoration Room Mon 12–22…, `reception`, `parishOffice`, `mediaCentre`, `adorationRoom`) + `mass` (9 keys: `weekdayMorning`, `weekdayEvening`, `saturday`, `sunday[5]`, `confession`, `adoration`, `secondCollection`, `note`, `monthly`) + `contact` (office 6253 2166, media 6356 5958, `crc.secretariat@catholic.org.sg` / `crc.admin` / `crc.pastoral` / `crc.youth` / `dpo.crc`) + `transport` (Toa Payoh NS19 Exit A, buses 88/157/163 B52261) + `feast` The Risen Christ — Easter Sunday + `uen` T08CC4042G/`chequePayee`/`facebook`/`instagram`/`youtube`/`freeMinistry`/`ssvp`/`bulletin`/`cep`/`mapsUrl`/`mapsEmbedSrc` — Footer + Worship + About consume it, don't duplicate. Pages render from data — don't inline copy.
- **Components:** `Button` (discriminated `to`/`href`/native `button` + `icon`; variants `primary|secondary|ghost|outline-light`; `active` press feedback), `Container` (`max-w-7xl px-5 sm:px-8`), `SectionHeading` (`eyebrow/title/description` + `align/light` + line), `PageHero` (`compact?`, `bg-grain` + dual gradients + `rise-in` staged content), `Reveal` (`delay`/`as`), `Accordion` (single-open, animated grid-rows collapse, `inert` closed panels), `Timeline` (left rail + `dot-pulse` halos — fed 1969–2026 Toa Payoh milestones), `SafeImage` (`src` + `fallback` + `alt` + `loading` + optional `fetchPriority`; always via `cn()`), `BackToTop` (threshold 480 + SVG ring + reduced-motion-aware, hash-safe), `ScrollProgress` (decoupled rail). Extend via `cn()`, not ad-hoc class strings.
- **Styling:** Use `shrine-cream/parchment(+dark)/stone/ink/charcoal/maroon-*/gold-*/pine-*/terracotta-*` + `shadow-shrine`/`shadow-shrine-lg` + utilities `text-balance` / `bg-adobe-texture` / `bg-grain` / `divider-weave`/`divider-weave-thin` / `gold-rule`/`gold-rule-left` / `hero-ken-burns` / `rise-in`(+`-d1..d4`) / `menu-in` / `drawer-in` / `dot-pulse` / `card-lift` / `link-underline` / `reveal`+`reveal-visible` / `skip-link` / `mask-fade-b` + `page-in`. Motion rule: transform/opacity only, `prefers-reduced-motion` gates everything (global block in `index.css`). Mobile-first (`sm:`/`lg:`). Tokens are unchanged — only the imagery/content they frame is now Toa Payoh (1971 first air-con nave, Adoration Room, parish hall & media centre).

## Don't

- Switch `HashRouter` → `BrowserRouter`, break alias routes, or prop-drill nav arrays. The 7 aliases exist for bookmarks/printed material — keep each `aliasOf` → canonical pair in `App.tsx`.
- Add one-off hex colors or bypass `cn()` (`tailwind-merge` dedup matters).
- Rebuild `Dialog`/`Dropdown` from scratch if `shadcn/ui` (Radix) is adopted — use its primitives.
- Add SSR, API routes, or a CMS without an explicit architecture decision — this is a static SPA (`CLAUDE.md` isolates future CMS behind `lib/cms`).
- Reintroduce St Mary of the Angels / Bukit Batok content (5 Bukit Batok East Ave 2, Portiuncula, OFM Custody of St Anthony, WOHA 2004 house of light, Garden of Peace, tian shen zhi hou, Towards a Prayerful & Missionary Parish, UEN T08CC4053H/HRSM, columbarium, telegram, whatsapp) or reassign `src/data/site.ts` parish facts. Hours, Mass, and address are the single source — don't duplicate them across pages.
- Assume gates are green — run `pnpm lint && pnpm typecheck && pnpm test && pnpm test:e2e && pnpm build` before shipping; all five must pass (32/184 + 48 E2E + 395.66kB). Asset-path e2e assertions must be env-agnostic — `pnpm test:e2e:built` proves the built artifact (round-9 E2E-L1).

## Where to look next

- `CLAUDE.md` — full six-phase workflow, detailed conventions, anti-patterns, env contract, and validation checklist.
- `docs/code-review-audit-round3-2026-08-30.md` — **round-3 tiered review + security audit** (historical — audited St Mary of the Angels before the Risen Christ port; C1/H3/M4/L6/I4 with evidence + verification ledger).
- `docs/remediation-plan-round3-2026-08-30.md` — the TDD remediation plan executed for round 3 (St Mary — historical).
- `docs/design-enhancement-round5-2026-08-30.md` — **round-5 design enhancement plan + validation** (historical — "Light of the Portiuncula" for St Mary; motion system retained for Risen Christ; screenshots in `docs/audit-shots-round5/`).
- `docs/remediation-round4-2026-08-30.md` — **round-4 closure of the deferred L-5**: mobile drawer is now a modal dialog (dialog/aria-modal/focus-trap/focus-restore/outside-tap close) + scroll-rail E2E race root-caused and made deterministic.
- `docs/code-review-audit-round6-2026-08-31.md` — **round-6 tiered review + security audit** (live-site E2E + browser journeys verified byte-identical to `dist/`; findings C1/H1/M1–M3/L1–L4 with verification ledger; C1: `docs/ssh-key.txt` untracked — **rotate the leaked key**).
- `docs/remediation-plan-round6-2026-08-31.md` — the TDD remediation plan executed for round 6 (guard tests `src/ci-workflow.test.ts` + `src/repo-hygiene.test.ts` + `src/docs-contract.test.ts`).
- `docs/design-enhancement-round7-2026-08-31.md` — **round-7 design enhancement plan + validation (current)** — "Honest Light": reveal resilience (print override + IO guard + early-entry rootMargin), Worship sticky mercy column, News/FAQ closure bands, Give featured PayNow card, Ministries scrollspy (`src/hooks/useScrollSpy.ts`), About PPC/link affordances, desktop nav gold hairline, `card-tint` info-card honesty system, PageHero atmosphere; screenshots in `docs/audit-shots-round7/`.
- `risen-christ_SKILL.md` — canonical engineering distillate (full §§ 1–20 + Appendices, verified against `src/`); `st-mary-of-angels_SKILL.md` is now a redirect stub (points here) and `rothershrine-v2_SKILL.md` remains the lineage stub.
- `docs/validation-src-vs-src.orig-2026-08-30.md` — **historical validation: `src` (St Mary) adopted 10/10 good contracts from `src.orig` (St Joseph) and improved 7** — retained for lineage; **2026-08-31 32/184 + 48 + 395.66kB green (re-verified post round-9 E2E-L1 remediation)** — Risen Christ port verified (lint 0 + typecheck 0 + 32/184 + 48 E2E + build).
- `docs/code-review-audit-round7-2026-08-31.md` — **round-7 tiered audit of commits `2f65c11..30a9b98` (current)** — six-phase audit of the "Honest Light" round (static gates, per-file Six-Axis review, architecture/security/motion checks, 48 E2E + live-DOM verification, live == dist md5); findings L-1/L-2 + I-1..I-3, **zero new C/H/M**; carried ops items H1′ (host security headers) + C1′ (key rotation) re-flagged.
- `docs/remediation-plan-round7-2026-08-31.md` — the TDD remediation executed for the round-7 audit: `useScrollSpy` document-order tie-break + truthful JSDoc (L-2/I-2), E2E hard-sleep removal (L-1), docs re-pin 32/179 (M-2/M-3 drift found during re-pin).
- `docs/remediation-plan-round9-2026-08-31.md` — **round-9 built-artifact E2E contract (current)** — the fresh live E2E pass vs `8e4f811` (47/48) exposed E2E-L1: the favicon spec asserted the dev form `/favicon.svg` while the singlefile build ships `./favicon.svg`. Remediated TDD-style: env-agnostic assertion + resolution check, new tracked `playwright.built.config.ts` (`pnpm test:e2e:built` — `vite preview :4173` or `E2E_BASE_URL` → live), docs-contract +2 pins, re-pin 32/181, v1.4.2. Suite green on dev + dist + live (48/48 each).
- `docs/prompts.md` — intent lineage.
- `docs/e2e-live-pass-round11-2026-08-31.md` — **round-11 live E2E pass** — fresh pass vs `66d2398`: deployment byte-verified (live md5 6ee34e4a… ≡ dist 395,663 B), five gates green, tri-env E2E 48/48 (dev + dist + live), agent-browser journey 43/43, zero console/page errors; finding E2E-J1 (`agent-browser eval` strips backslashes from regex literals → hidden SyntaxError → false FAIL; site correct) fixed backslash-free in the local journey script; lesson pinned as SKILL pitfall #15 + docs-contract guard; v1.4.3.
- `docs/UI-UX-Design-Audit_StMaryOfAngels_vs_RisenChrist.md` + `docs/remediation-plan-round12-2026-08-31.md` + `docs/remediation-round12-2026-08-31.md` — **round-12 comparative-audit remediation (current)** — the comparative UI/UX audit of the two parish sites, Risen Christ findings closed TDD-style: F-1 Devotion chip retone to `terracotta-600` (`#8f4c30`, 5.36:1 AA on parchment), F-2 Worship mass-card footnote `/70`→`/85` (4.16→6.19:1) + date-tone lock, F-3 `src/utils/deepLinks.ts` path-style deep-link rewrite (reproduced soft-404 first), F-4 Give section retitled "Ways to give" + copyable UEN row in the PayNow card, F-9 tracked `src.orig/` pruned (64 files — `.gitignore` never untracks); counts re-pinned 32/184+48 → 35/202+51, v1.4.4.
- `docs/ui-ux-remediation-plan-2026-08-28.md` — UI/UX audit findings + "Sacred Motion" enhancement plan (TDD mapping, validation table).
- `src/index.css` — authoritative token list.
- `src.orig/` — pruned round-12 (2026-08-31): the archived St Mary port had remained git-tracked despite `.gitignore` (ignore rules do not untrack — same lesson as round-6 C1); `git rm -r --cached` + tree removal; `src/repo-hygiene.test.ts` guard now fails if it re-enters. Lineage history: `docs/` + git history. Legacy parish facts must not be reintroduced.
```
