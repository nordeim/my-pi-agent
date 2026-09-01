# Meticulous Plan — Unified `unified-v3_SKILL.md` (Lineage Master v3.0.0)

> **Request:** Review & validate `draft_unified-v3_SKILL.md` (254 lines), then create a comprehensive, production-grade `unified-v3_SKILL.md` that merges the 3 source skills and combines every best element — with zero tail-end decay.
> **Author:** Claw Code · **Date:** 2026-08-31 · **Method:** Meticulous Approach (ANALYZE → PLAN → VALIDATE → IMPLEMENT → VERIFY → DELIVER)

---

## Table of Contents
1. [Executive Summary & Go/No-Go](#1-executive-summary--gono-go)
2. [Phase 1 — ANALYZE: Draft Validation & Source Triangulation](#2-phase-1--analyze-draft-validation--source-triangulation)
3. [Phase 2 — PLAN: Unified-v3 Architecture & Merge Strategy](#3-phase-2--plan-unified-v3-architecture--merge-strategy)
4. [Phase 3 — VALIDATE: Explicit Confirmation Checkpoint](#4-phase-3--validate-explicit-confirmation-checkpoint)
5. [Phase 4 — IMPLEMENT: Build Unified-v3 (Surgical, No Drift)](#5-phase-4--implement-build-unified-v3-surgical-no-drift)
6. [Phase 5 — VERIFY: Pre-Ship Gate for Unified-v3](#6-phase-5--verify-pre-ship-gate-for-unified-v3)
7. [Phase 6 — DELIVER: Handoff & Freeze Protocol](#7-phase-6--deliver-handoff--freeze-protocol)
8. [Appendix A — Detailed Review of `draft_unified-v3_SKILL.md`](#8-appendix-a--detailed-review-of-draft_unified-v3_skillmd)
9. [Appendix B — Best-Elements Merge Matrix (What to Take From Each Source)](#9-appendix-b--best-elements-merge-matrix-what-to-take-from-each-source)
10. [Appendix C — Risk Register & Mitigations](#10-appendix-c--risk-register--mitigations)

---

## 1. Executive Summary & Go/No-Go

**One sentence:** `draft_unified-v3_SKILL.md` correctly diagnoses the lineage's tail-end decay but is **~5× too short to replace the sources** — it is a sound strategy memo, not a production-grade skill. The production `unified-v3_SKILL.md` must be a **~1400–1500 line Lineage Master** built on the `risen-christ` skeleton (the most mature), elevated from parish-specific `Church of the Risen Christ` to lineage-wide `Singapore Parish SPA Lineage v3.0.0` with Risen as the canonical reference implementation, merging the best evidence from all three sources and fixing every verified defect.

**Go/No-Go:** **GO** — with the plan below. Risk is Low if we stay on the proven §§1–20 + Appendices A–F skeleton and use copy-pasteable verbatim blocks (no invention). Risk becomes Medium if we instead expand the draft's 254-line outline without the missing §§5–20 contracts.

**Best recommendation (6 decisions):**

| Decision | Draft proposes | My recommendation (with rationale) |
|---|---|---|
| **A. Baseline skeleton** | New 11-section outline (1. Lineage … 11. Patterns + Appendices A–D) | **Keep `risen-christ` §§1–20 + Appendices A–F skeleton verbatim** — it is the only structure that passed 35/202 + 51 E2E + round-12 audit. Draft loses §§8–20 contracts (a11y motion kill, anti-patterns 15, debugging 16, lessons 12, pitfalls, best practices, TypeScript verbatim, breakpoints, z-index, color ref). | 
| **B. Framing** | `singapore-parish-lineage v3.0.0` with Risen as canonical ref impl | **Adopt exactly** — rename `name: singapore-parish-lineage`, `display_name: Singapore Parish SPA Lineage — Master`, `version: 3.0.0`, `canonical_ref: risen-christ (Toa Payoh)`. Keep `port_provenance` as lineage string `Rother → St Joseph → St Mary → Risen`. |
| **C. Metrics** | Remove hardcoded counts, reference `docs-contract` | **Adopt, but with current reference counts as documented examples** — e.g., `verified: pnpm lint 0 + typecheck 0 + test ~35/202 + test:e2e ~51 (Risen Christ reference — actual counts are machine-asserted by docs-contract, not prose)`. Prevents drift while keeping the doc self-contained. |
| **D. Design tokens** | Unified 26+2 superset (restore `gold-700` + keep `terracotta-600`) | **Adopt superset** — 26 colors + 2 shadows (both AA text steps). But **document the Risen refinement rationale**: Risen intentionally dropped `gold-700` because only `terracotta-600` was needed for its Devotion chip; the master keeps both for future ports that may need either. | 
| **E. CSP** | Strict `img-src 'self' data: blob:` only, forbid legacy CDN | **Adopt strict** — matches Risen round-6 removal. Document legacy `wikimedia/pexels` as **forbidden**, with `SafeImage` still guarding any future external image (why the guard stays even with tight CSP). |
| **F. Appendices** | Replace Live-Site Validation + Migration Notes with Porting Runbook + Lineage Ledger | **Merge, not replace** — Keep **Appendix B Live-Site Smoke (parameterized for any parish)** + **Appendix B-port Porting Runbook** + **Appendix D Lineage Ledger (3 hops) + Appendix E Validation + Appendix F St Mary→Risen diff**. The smoke script is the only manual verification the E2E cannot cover (mobile Safari offset, font FOIT, weave paint). |

**Deliverable:** One file `unified-v3_SKILL.md` (1400–1500 lines, §§1–20 + Appendices A–F + Quick Ref, front-matter with `name/version/lineage`), plus updated `CRITICAL-COMPARISON.md` with unified-vs-sources diff.

---

## 2. Phase 1 — ANALYZE: Draft Validation & Source Triangulation

### 2.1 What the draft gets right (strengths to preserve) — 5/5

| Strength | Evidence | Keep in unified-v3 |
|---|---|---|
| Correct defect taxonomy (C-1 … H-8) | C-1 Risen Appendix B = verbatim St Mary smoke (4 OFM, T08CC4053H, `#mandarin`) — verified by `rg` in CRITICAL-COMPARISON §6 | Promote to unified Appendix E validation table |
| Machine-asserted metrics | `docs-contract` + `repo-hygiene` tests as source of truth, not prose counts | Adopt per decision C |
| Strict CSP + forbidden legacy CDN | Risen tight `img-src 'self' data: blob:` vs St Mary permissive contradiction — correctly resolves to strict | Adopt per decision E |
| `playwright.built.config.ts` mandated | Correctly elevates round-9 E2E-L1 (favicon `/` → `./`) to mandatory | Already in Risen; elevate to unified mandate |
| Lineage Master framing | Correctly picks Risen as canonical ref (repo-hygiene, docs-contract, deepLinks, useScrollSpy) | Adopt per decision B |
| Unified palette 26+2 | Correctly keeps both AA steps for coverage | Adopt per decision D |

### 2.2 What the draft loses (critical gaps — must be restored) — scored

| Gap vs source § | Detail missing in draft (254 lines) | Impact if not restored | Source to restore from |
|---|---|---|---|
| §5.2 Directory Inventory (77 files) | No file tree, no `public/images` 8, no `e2e/ 8 specs`, no `hooks/` 3, no `utils/` 3 | Agent cannot "know where to put code" — violates skill goal | Risen §5.2 + St Mary §5.2 (best) |
| §5.4 Routing Contract (17 routes, 5 alias groups table, hash anchor discipline, double-hash `resolveAnchor`) | Draft §5.1 has summary but no alias table, no `scroll-mt-28`, no `Layout` double-hash code | Breaks alias contract L1 — inbound parish links 404 | Risen §5.4 (most complete) |
| §5.5 Component Conventions table (Button/Container/SectionHeading/PageHero/SafeImage/Header with modal drawer trap, Reveal, Accordion `grid-rows+inert`) | Draft §5.2 mentions SafeImage but no API table, no 44px, no focus trap | A11y regression on mobile drawer | Risen §5.5 |
| §6 Hooks Deep Dive (3 hooks with code fence) | Draft §6 lists 3 hooks but no contract code, no SSR-safe guard, no tie-break | Cannot copy-paste | Risen §6 (`useScrolled` fence + `useScrollProgress`/`useScrollSpy` notes) |
| §7 Content Management (10 arrays with counts/shapes, 8 interfaces, `images 11 local`, add-content recipes) | Draft §7 has 3 bullets, no counts, no 8 interfaces, no recipes, no `images` fallback | Agent inlines copy, breaks `imageAlt` required | Risen §7.1–7.4 + Appendix F diff tables |
| §8 A11y (contrast 4 rows + focus ring + landmarks + motion kill `0.01ms` + halo) | Draft §8 has 4 bullets but no table, no `focus-visible` offset, no `skip-link` hash discipline, no `prefers-reduced-motion` fence | WCAG AAA cannot be claimed | Risen §8 |
| §9 Anti-Patterns (15 entries with severity/symptom/root cause/fix/lesson) | Draft §9 has 9 rows, missing #10 imageAlt, #11 `<a href="#id">`, #12 aria-expanded, #13 SafeImage fallback, #14 built-artifact, #15 backslash — the most audit-driven rows | Agents re-introduce the top 6 bugs that audits found | Risen §9 (15) |
| §10 Debugging Guide (16 rows + live-site verification) | Draft has no debugging guide — claims "machine-asserted" but manual smoke is still needed for mobile Safari/font/weave | Un-debuggable | Risen §10 |
| §§11–14 Pre-Ship Checklist (9-step + category table + Lessons 12 / Pitfalls / Best Practices) | Draft §10 has 6-step checklist but no category table, no Lessons L1–L12, no Pitfalls, no Best Practices | Pre-ship gate incomplete | Risen §§11–14 |
| §§15–20 Coding Patterns (Button variant, Layout hash-scroll, cn, PageHero, Ministries jump nav) + Anti-Patterns + Responsive/Z-Index/Color/TypeScript verbatim | Draft §11 has 2 patterns but no Ministries jump nav, no §16–20 at all | Not copy-pasteable | Risen §§15–20 |
| Appendices B/C/D/E/F | Draft has 4 new appendices but loses Appendix C Meticulous Approach, E Validation 10/10, F St Mary→Risen diff — the lineage provenance | Loss of audit trail | Risen Appendices A–F |

**Score:** Draft **covers 4 of 20 sections adequately** — to be production-grade it must absorb the 16 missing sections from the sources.

### 2.3 Source triangulation — what each source contributes best

See Appendix B (merge matrix) — summary:

| Source | Best-in-class element to lift verbatim into unified-v3 |
|---|---|
| **Risen Christ (primary baseline)** | §§1–20 skeleton, 77-file inventory, 3 hooks, 15 anti-patterns, 16-row debugging, Appendix F diff, `deepLinks.resolveHashRedirect` + `useScrollSpy`, `docs-contract`/`repo-hygiene` tests, tight CSP, 25→26 token superset (with rationale) |
| **St Mary** | WOHA 2004 narrative as lineage ledger example, `gold-700 #85601f` AA token, 7-hour keys with columbarium as `hours` shape variant, Tamil `19.45` + Sinhala/Malayalam as Language Communities diversity example, `head` 14 + `security-headers` 6 test split, print-media `@media print` for reveal |
| **St Joseph BT** | Palladian 1853 + M.E.P. + cemetery as origin narrative, first `GroundsPlace`/`Ministry` split and 6-pill jump nav invention, canonical flip `/about` table, `prose` on why `src.orig/` is not in repo (inert guards) as origin policy variant |

### 2.4 Defects to fix while unifying (from draft §1 + CRITICAL-COMPARISON §6)

| Defect | In sources | Unified fix |
|---|---|---|
| C-1 Risen Appendix B = St Mary smoke (4 OFM, T08CC4053H, `#mandarin`) | Risen §B | Parameterize smoke script: `{{parish}} priests {{N}} {{roles}}, UEN {{uen}}, anchors {{#list}}` — example filled for Risen, with note "replace for Parish X" |
| C-2 Appendix E identical `16/92+35 E2E+380kB` (St Joseph metrics in St Mary/Risen) | St Mary + Risen §E | Re-run validation: `52 files, 10 pages, 8 interfaces, 92 tests preserved; St Mary/Risen add 7 improvements — no regression`. Replace fossil with CRITICAL-COMPARISON §6-verified counts |
| C-3 Test schizophrenia (St Mary `31/172` vs `24/134` vs `25/141`, sum 140≠172) | St Mary §2/§11/C | Use decision C: prose says `~31/172 (asserted by docs-contract)`, itemized list in §5.2 is informative, not authoritative; fix sum to 172 |
| H-1/H-2 narrative leaks (§20.1 comments Kranji/1 May) | St Mary | Comments become `// 1957–2026 Franciscan/WOHA — see Lineage Ledger for Kranji/1 May hill variants` |
| H-4 token drift claim | Risen §4 | Change `unchanged from St Mary` → `evolved from St Mary: 24+2 → 26+2 (adds gold-700 + terracotta-600 AA), Risen refines to 25+2, unified master keeps 26+2 superset` |
| H-6/H-7 config contradictions | Risen + St Joseph | Mandate `test` block + `server.watch.ignored` + `playwright.built` per decision F |
| H-8 src.orig governance | All §2 Environment | Unified: `src.orig/ is forbidden in index (repo-hygiene); lineage history lives in Appendices D/F + git history — not on disk` |

---

## 3. Phase 2 — PLAN: Unified-v3 Architecture & Merge Strategy

### 3.1 File spec

| Field | Value | Verified against |
|---|---|---|
| `path` | `new-skills/unified-v3_SKILL.md` | — |
| `name` | `singapore-parish-lineage` | Draft §3 + Risen lineage |
| `display_name` | `Singapore Parish SPA Lineage — Master Engineering Skill` | Draft |
| `version` | `3.0.0` | Draft (major bump — merges 1.2.0 + 1.3.0 + 1.4.4 → lineage major) |
| `last_updated` | `2026-08-31` | Same day as sources |
| `canonical_ref` | `Church of the Risen Christ — Toa Payoh (91 Toa Payoh Central, UEN T08CC4042G, Easter Sunday)` — with `site.ts as const` example inline | Risen §1/§20.3 |
| `port_provenance` | `Blessed Stanley Rother Shrine (OKC) → St Joseph BT (620 Upper Bukit Timah, 1845–2017) → St Mary of the Angels (5 Bukit Batok, 1957–2026) → Risen Christ (91 Toa Payoh, 1969–2026)` | All three §1 + Appendix D |
| `stack` | React 19.2.8 … Playwright 1.55.1 (identical pins) — copy Risen §2 | `package.json` |
| `rendering/deploy/data_layer` | HashRouter static SPA, singlefile → dist/index.html + dist/images/, file-backed typed arrays | ADRs |
| `length target` | **1400–1500 lines** (risen-christ is 1427 — master will be similar + 50–80 lines for Lineage Ledger + Porting Runbook) | `wc -l` |

### 3.2 Section map (mirrors risen-christ §§1–20, elevated to lineage master)

| Sec | Title (from risen) | Elevation for unified-v3 (what changes) | Source baseline | Best elements merged |
|---|---|---|---|---|
| 0 | Front-matter + How to use + Sources of truth + File name note + Migration note | New front-matter per §3.1; Sources of truth unchanged; File name note: `Canonical Lineage Master v3.0.0 — governs all hops; parish skills are now profile overlays, not forks; Risen is the reference implementation` | Risen §0 | Draft B + Risen |
| 1 | Project Identity & Design Philosophy | **Lineage identity** (4 parishes in one breath, each one sentence) + **Canonical ref identity** (Risen fullconstants table as example) + **Porting philosophy** (5 non-negotiables with `{{Parish X}}` template); Design thesis "Reverent, not austere" kept verbatim | Risen §1 | Risen (Toa Payoh) + St Mary WOHA + St Joseph hill — each as one breath, not merged prose |
| 2 | Tech Stack & Environment | Copy Risen §2 table verbatim (11 layers, locked versions) + unified `verified` line per decision C + Environment with forbidden `src.orig/` + leaked key advisory (rotate `docs/ssh-key.txt`) | Risen §2 | Risen (most complete) + St Mary `docs-contract` note |
| 3 | Bootstrapping & Configuration | Copy Risen §3.1 zero-to-running + §3.2 critical config (vite/tsconfig/eslint/playwright/built/e2e/.github/src/index.css/index.html/.gitignore) with **mandated** `test` + `server.watch.ignored` + `playwright.built` per decision F | Risen §3 | Risen (mandated) — draft §3 correct |
| 4 | Design System (Code-First) | **Unified tokens 26+2** (draft §4 superset) with Risen refinement note + 28 utilities table (merge Risen 27 + St Mary `@media print` = 28) + 8 keyframes + motion kill + Accordion contract | Risen §4 | Risen palette + St Mary `gold-700` + `print` |
| 5 | Component Architecture & Patterns | **77-file inventory** (Risen) as reference + 5.4 routing contract 17/5/7 + alias table + hash anchor discipline + `resolveAnchor` double-hash + 5.5 conventions table (Button/Container/SectionHeading/PageHero/SafeImage/Header modal drawer/BackToTop/ScrollProgress/Timeline/ui) — with lineage note: `ministries last id is {{parish}}: mandarin (St Joseph/St Mary) → language-communities (Risen)` | Risen §5 | Risen (77) + St Joseph 6-pill invention note |
| 6 | Custom Hooks Deep Dive | **3 hooks** fences: `useScrolled` code + `useScrollProgress` rAF guard + `useScrollSpy` tie-break (Risen) — origin note: `1→2→3 hops` | Risen §6 | Risen |
| 7 | Content Management | 10 arrays + 8 interfaces + `images 11 local` + `site.ts as const` verbatim (Risen) + add-content recipes + lineage variants footnote (columbarium, `sunday[4]` vs `[5]` vs `[6]`, UEN HRSM, Bahasa/Tamil/Tagalog monthly vs Tamil 19.45) | Risen §7 + Appendix F | Risen (primary) + St Mary variants |
| 8 | Accessibility (WCAG AAA) | Copy Risen §8 table + focus/landmarks/images/motion fences verbatim | Risen §8 | Risen |
| 9 | Anti-Patterns | **15 entries** verbatim from Risen §9 (the audit-driven superset including #14 built-artifact + #15 backslash) | Risen §9 | Risen |
| 10 | Debugging Guide | **16 rows + live-site verification** verbatim from Risen §10 — parameterized as `{{parish}} routes /about /history /worship#mass ...` with Risen example filled | Risen §10 | Risen |
| 11 | Pre-Ship Checklist | **9-step Risen checklist** (with `test:e2e:built` + `ls dist` + a11y) + category table — per decision C with machine-asserted note | Risen §11 | Risen |
| 12 | Lessons Learnt (12) | Copy Risen §12 L1–L12 table (alias contract … canonical flip) | Risen §12 | Risen |
| 13 | Pitfalls to Avoid | Copy Risen §13 (Architecture/TS/Styling/Data/Build) | Risen §13 | Risen |
| 14 | Best Practices | Copy Risen §14 (naming/imports/types/React/styling/data/git/docs) | Risen §14 | Risen |
| 15 | Coding Patterns | Copy Risen §15.1–15.5 (Button variant, Layout hash-scroll with `resolveAnchor`, cn, PageHero overlay, Ministries jump nav with `aria-label`) | Risen §15 | Risen |
| 16 | Coding Anti-Patterns | Copy Risen §16 table (12 rows) | Risen §16 | Risen |
| 17 | Responsive Breakpoint Ref | Copy Risen §17 (default / sm / lg) | Risen §17 | Risen |
| 18 | Z-Index Layer Map | Copy Risen §18 (100 / 50 / 40 / auto) + sticky clearance rule | Risen §18 | Risen |
| 19 | Color Reference (Complete) | **26 colors + 2 shadows table** — every hex from draft §4.1 superset, with AA footnotes `gold-700 4.72:1 + terracotta-600 5.36:1` | Draft §4.1 + Risen §19 | Draft superset + Risen table format |
| 20 | TypeScript Interface Reference | Copy Risen §20.1–20.5 verbatim (TimelineEntry … devotions + images `as const` + NavLink/NavItem + `site as const` with `monthly` + SafeImageProps + Button/Container/SectionHeading/PageHero/Reveal/Accordion + useScrolled + cn) — add lineage variant notes as comments, not forks | Risen §20 | Risen |
| A | ADRs (6) | Copy Risen Appendix A ADR-1…ADR-6 (HashRouter/singlefile/@theme/file-backed/alias/src.orig pruned) | Risen A | Risen |
| B | Live-Site Validation | **Parameterized smoke script** (draft runbook style but keep Risen's 17-step detail): `{{parish}}: / /about /history (8 entries) /worship#mass …` with Risen example filled + what CI cannot catch | Risen B | Draft runbook idea + Risen detail |
| C | Meticulous Approach (6-phase) | Copy Risen Appendix C (Analyze→Deliver with harness green note `~35/202+51` per decision C) | Risen C | Risen |
| D | Migration Note (Rother→St Joseph→St Mary) | Copy Risen Appendix D (second-hop history) verbatim — the proven provenance record | Risen D | Risen |
| E | Validation: src vs src.orig | **Rewritten** per §2.4 C-2 fix: actual `52 files, 10 pages, 8 interfaces` + 7 improvements, not fossil `16/92` | Draft + CRITICAL-COMPARISON | Draft diagnosis + Risen structure |
| F | Migration Note (St Mary→Risen Christ) | Copy Risen Appendix F diff tables verbatim (package.json, site.address/hours/mass/transport/feast/uen, priests/ppc, lifeTimeline, grounds, faqs/events/giving, tests, CSP, tokens/routing/motion) | Risen F | Risen |
| QR | Quick Reference Card | Copy Risen Quick Ref — updated to `singapore-parish-lineage v3.0.0` name, 26+2 tokens, `playwright.built`, `useScrollSpy`, `deepLinks`, audit ledger links | Risen QR | Risen |

**Length reconciliation:** Draft 254 → Unified 1400–1500 is not bloat — it is restoring the 16 missing contracts that make the skill executable. The 4-hop lineage adds only ~80 lines (D/E/F provenance + 1.3 token + runbook).

### 3.3 Merge discipline & invariant checks

| Invariant | How unified-v3 preserves it |
|---|---|
| **No parish re-introduction outside ledger** | §1 lists 4 parishes each in one breath with `site.ts` single-source reminder; every other section uses `{{Parish X}}` or Risen example with explicit "replace for Parish X" |
| **Singlefile dictates imports** | §9 #3 + §11 build check `dist/index.html` is one file + §3.2 `playwright.built` rewrite warning |
| **Hash is the route** | §5.4 + §9 #11 + §15.5 Ministries jump nav `Link` vs `<a>` + §10 debugging double-hash |
| **SafeImage fallback** | §5.5 + §9 #13 + §3.2 CSP tight `img-src 'self'` + fallback `hero-church.jpg` |
| **Alias contract 17/5/7** | §5.4 table + §12 L1 + §9 #2 |
| **No arbitrary hex** | §4 + §19 + §9 #4 + §14 Best Practices `extend @theme` |
| **`@` alias desync** | §9 #5 + §3.2 alias MUST stay in sync + restart dev server |
| **`include` is type boundary** | §9 #7 + §3.2 `playwright.built` in include |

---

## 4. Phase 3 — VALIDATE: Explicit Confirmation Checkpoint

Before writing any file, confirm:

| # | Question | Options | My preference |
|---|---|---|---|
| Q1 | **Scope of unified-v3** — should it be a **replacement master** (`new-skills/unified-v3_SKILL.md` becomes the new canonical, 3 sources frozen as §6 planned) or an **additional overlay** (unified-v3 sits alongside the 3, which stay writable)? | Replacement master (my plan) vs Overlay | **Replacement master** — single source of truth per Meticulous Approach; 3 sources already diverged, unified without replacement adds a 4th fork |
| Q2 | **Lineage vs parish framing** — should unified-v3's §1 constants table show **Risen example (Toa Payoh)** with footnote variants, or a **neutral template** with `{{street}}` placeholders? | Risen example (my plan, §3.2) vs Neutral template | **Risen example** — an example you can grep against `src/data/site.ts` is more verifiable than a template; add "for Parish X, replace …" as done in draft runbook |
| Q3 | **Token superset** — keep **26+2 (both AA)** as draft proposes, or **25+2 (keep Risen refinement, drop gold-700)**? | 26+2 superset (my plan) vs 25+2 refined | **26+2 superset** — cost is one token, benefit is future ports can pick either AA step without adding a new token; note the Risen refinement rationale so reviewers know `gold-700` is optional |
| Q4 | **Validation metric in prose** — should Appendix B smoke list **Risen example values** (4 OFM → actually 3 priests for Risen) or stay parameterized? | Parameterized + Risen example filled (my plan) vs Fully parameterized only | **Parameterized + Risen example** — copy-pasteable for the current reference, instructive for the next port |
| Q5 | **Delivery of appendices** — should unified-v3 include **Appendices D+E+F full verbatim** (adds ~200 lines) or **condensed ledger** (draft's 1-table ledger)? | Full verbatim (my plan) vs Condensed | **Full verbatim** — appendices are the provenance record; condensing re-introduces tail-end decay by design |

**Validation gate:** Reply with `Q1–Q5` choices (e.g., `1 master / 2 example / 3 superset / 4 parameterized / 5 full`) or `approve plan as-is`. I will not write `unified-v3_SKILL.md` until you confirm.

---

## 5. Phase 4 — IMPLEMENT: Build Unified-v3 (Surgical, No Drift)

*Trigger: after VALIDATE approval.*

**One commit, one file:**

```bash
write new-skills/unified-v3_SKILL.md  # 1400–1500 lines, §§1–20 + Appendices A–F + Quick Ref + front-matter v3.0.0
```

**Build order inside the file (top→bottom):**
1. Front-matter (name/display_name/version/last_updated/canonical_ref/lineage/stack/rendering/deploy)
2. How to use + Sources of truth + File name note + Migration note (elevated to Lineage Master)
3. TOC (22 entries)
4. §§1–20 per §3.2 map (copy risen baseline, merge St Mary/St Joseph best as noted)
5. Appendices A–F per §3.2
6. Quick Reference Card (updated to v3.0.0 + 26+2 + 3 hooks + deepLinks)
7. Append §R reproduction note (`rg` counts, `wc -l`)

**Anti-generic enforcement:** No `Inter`/`Roboto`, no purple gradients — whitespace is structure (same as risen).

**No new tokens, no new routes, no new utils** beyond the merged superset — singlefile, HashRouter, 17-route contract are immutable.

---

## 6. Phase 5 — VERIFY: Pre-Ship Gate for Unified-v3

*Same 9-step gate as risen §11, with machine-asserted variant:*

```bash
# 1. Docs hygiene
rg -n "shrine-" new-skills/unified-v3_SKILL.md | wc -l   # expect 91+ (26+2 tokens)
rg -n "gold-700|terracotta-600" unified-v3_SKILL.md      # expect both (superset)
rg -n "17 Route|7 alias|9 hash" unified-v3_SKILL.md      # expect 5 hits (alias contract)
rg -n "Tail-end|tail-end|fossil" unified-v3_SKILL.md     # expect 0 (no decay)
rg -n "Tepeyac|Oklahoma" unified-v3_SKILL.md             # expect only in Appendix D (ledger)
rg -n "Kranji|Palladian|WOHA|Ho Ping" unified-v3_SKILL.md # expect only in §1 + Appendix D/F (one breath each)

# 2. Section completeness
rg -n "^## [0-9]+\. |^## Appendix|^## Quick" unified-v3_SKILL.md | wc -l  # expect 27 (§§1–20 + A–F + QR)
rg -n "useScrolled|useScrollProgress|useScrollSpy" unified-v3_SKILL.md     # expect 3 hooks
rg -n "Anti-Pattern.*Severity|Debugging Guide|Pre-Ship Checklist|Lessons Learnt" unified-v3_SKILL.md

# 3. Type contract
rg -n "interface TimelineEntry|interface GroundsPlace|interface Ministry|site as const" unified-v3_SKILL.md
wc -l new-skills/unified-v3_SKILL.md  # expect 1400–1500

# 4. No overwrite of parish facts outside ledger
rg -n "T08CC4042G" unified-v3_SKILL.md  # expect Risen example in §1/§7/§20 + ledger, not duplicated per section
```

*Success:* All `rg` expectations pass + `wc -l` in target + no `any`/`as any` in §20.

---

## 7. Phase 6 — DELIVER: Handoff & Freeze Protocol

| Deliverable | Path | Note |
|---|---|---|
| `unified-v3_SKILL.md` | `new-skills/unified-v3_SKILL.md` | **Canonical from 2026-08-31** — single source of truth per File name note |
| Updated `CRITICAL-COMPARISON.md` | `new-skills/CRITICAL-COMPARISON.md` | Add §12 `Unified-v3 vs sources` diff (5 lines, not rewrite) |
| Freeze the 3 sources | `new-skills/risen-christ_SKILL.md` + `st-mary…` + `rothershrine-v2…` | Add `> Frozen since unified-v3 v3.0.0 — do not edit independently` header if not already (risen stays writable until unified is promoted, then it too freezes) |
| `VERIFICATION.md` | `new-skills/VERIFICATION.md` | Append unified-v3 gate run |
| `docs/lineage.md` (optional) | `new-skills/docs/lineage.md` | Extract Appendix D ledger as standalone onboarding doc |

**Recommended commit chain:**
```
docs(plan): add UNIFIED-V3-PLAN.md — lineage master v3.0.0 merge strategy
docs(skill): add unified-v3_SKILL.md — master lineage skill (risen baseline + 26+2 superset + 15 anti-patterns + parameterized smoke)
```

**No `src/` change** — this is docs-only lineage convergence. The leaked `docs/ssh-key.txt` rotation advisory stays in §2 Environment as in risen.

---

## 8. Appendix A — Detailed Review of `draft_unified-v3_SKILL.md`

*254 lines — strategy memo, not a skill.*

**Strengths (keep):**
1. **Defect taxonomy is exact** — C-1 verbatim smoke (4 OFM, T08CC4053H, `#mandarin`) is reproducible via `rg "4 OFM" risen-christ_SKILL.md` inside Appendix B; C-2 identical validation `16/92+35+380kB` is reproducible via `rg "380.19" st-mary… risen…`; C-3 schizophrenia `31/172 vs 24/134 vs 25/141` is reproducible via `rg "31/172|24/134|25/141"`; H-4 token drift `unchanged` vs `gold-700` missing is reproducible via `rg "gold-700"`; H-8 src.orig governance drift is reproducible via `rg "src.orig" *.md`.
2. **5 unification decisions are correct** (Lineage Master framing, machine-asserted metrics, porting runbook, mandated test/watch, unified palette) — each maps to a verified defect.

**Weaknesses (must be fixed in unified-v3):**

| Area | Draft text | Problem | Fix in unified-v3 |
|---|---|---|---|
| §4.1 Tokens | Shows partial CSS ending at `--color-shrine-maroon-700: #55191a;  --color-shrine-maroon-800: #431315;` | Truncated — no `maroon-900/950`, `gold-100…700`, `pine`, `terracotta-600`, shadows. Agent cannot grep-verify `grep shrine- src/index.css → 26+2` | Use full `@theme` block from risen §4.1, add `gold-700 #85601f` from St Mary |
| §4.2 Utilities | `28 utilities including hero-ken-burns, gold-rule … bg-gold-bloom` as one line | No table, no CSS, no motion kill fence — not verifiable | Restore risen §4.3 table (27 utilities → 28 with `print`) + `prefers-reduced-motion` fence |
| §5.1 Routing | `17 Route entries … 5 Alias Groups … Canonical Flip /about` as 4 lines | No alias table (canonical→aliases/origin), no `scroll-mt-28`, no `Layout resolveAnchor` code, no `useScrolled(16)` nuance | Restore risen §5.4 full contract |
| §5.2 SafeImage | `Default fallback is /images/hero-church.jpg` as one line | No `alt` required, no `fetchPriority?`, no `cn()` merge, no `public/images/` 8 count | Restore risen §5.5 table |
| §6 Hooks | 3 lines per hook, no code fence | Not copy-pasteable — breaks "How to use" contract | Restore risen §6 `useScrolled` fence + rAF + tie-break notes |
| §7 Content | `8 exported interfaces … site.ts single source` as 3 bullets | No GroundsPlace/Ministry required `imageAlt`/`imageFallback`, no `ppcMembers 7`, no `lifeTimeline 1969–2026`, no `images 11 local`, no add-content recipes | Restore risen §7.1–7.4 |
| §8 A11y | 4 bullets, no contrast table, no `focus-visible` offset | Cannot claim AAA without ratio table | Restore risen §8 |
| §9 Anti-Patterns | 9 rows, missing #10–15 (the audit-driven core) | Re-introduces the top 6 bugs audits found | Use risen 15 |
| Missing §§10–20 | No debugging, no pre-ship gate, no lessons, no pitfalls, no best practices, no patterns, no anti-patterns, no breakpoints/z-index/color/type refs | Skill is not executable — agents cannot ship | Restore risen §§10–20 |
| Appendices | Runbook + Ledger only, no ADRs 6, no smoke detail, no Validation 10/10, no Meticulous Approach, no Full diff F | Loses audit trail | Restore risen A–F per §3.2 |

**Verdict on draft:** **Sound diagnosis, incomplete prescription.** It is the right *plan* for unified-v3, but the unified document inside its §3 code fence must be discarded and rebuilt per §3.2 map above — not expanded inline.

---

## 9. Appendix B — Best-Elements Merge Matrix (What to Take From Each Source)

| Element | Risen (Toa Payoh) — take as baseline | St Mary (Bukit Batok) — cherry-pick | St Joseph BT — cherry-pick | Draft — take decision only |
|---|---|---|---|---|
| Front-matter | `version 1.4.4, verified 35/202+51, 77 files, 397.52kB` → becomes `3.0.0, ~35/202+~51 (asserted by docs-contract)` | `gold-700` mention for superset note | `st-joseph-bt` name vs `rothershrine-v2` filename lineage note | v3.0.0 lineage master framing |
| §1 Identity | Ho Ping 1969 → first air-con 1971 $450k → Grateful Faithful Sent, Easter Sunday, 91 Toa Payoh, UEN T08CC4042G | WOHA 2004 8.5k seats + Design of Year 2006 + Portiuncula 2 Aug as ledger example | Kranji 1846 M.E.P. + Palladian 6 Doric + cemetery as ledger example | Parish Fidelity over Pixel Theft (keep) |
| §2 Stack | Full 11-layer table + `playwright.built` + `repo-hygiene` + leaked key advisory | `gold-700` AA note | `src.orig` not in repo as origin policy | Environment `pnpm --frozen-lockfile` |
| §3 Bootstrapping | Full `vite/tsconfig/eslint/playwright/built/index.html/.gitignore` + 5 gates | — | — | Mandated test/watch |
| §4 Design | 25+2 tokens + 27 utilities + 8 keyframes | `gold-700 #85601f` + `@media print` | 24+2 as origin palette | 26+2 superset decision |
| §5 Architecture | 77-file tree + 17-route + alias + double-hash + 5.5 conventions (modal drawer trap) | — | 6-pill jump nav invention note | Routing rule `<Link>` |
| §6 Hooks | 3 hooks with code fence + rAF + tie-break | — | — | List of 3 |
| §7 Content | 10 arrays + 8 interfaces + `images 11 local` + recipes + `site.ts as const` with `monthly` | columbarium 7 keys + `sunday[6]` + Tamil 19.45 as variant | — | 8 interfaces note |
| §8 A11y | Contrast 13:1 + focus ring + inert + 44px + ring | — | — | WCAG AAA intent |
| §9 Anti-patterns | 15 entries (superset) | — | — | 9 rows → expand to 15 |
| §10 Debugging | 16 rows + live-site 17-step smoke | — | — | Runbook idea |
| §11 Pre-ship | 9-step + category table + `test:e2e:built` | — | — | 6-step → expand to 9 |
| §12–20 | Lessons/L1–12 + Pitfalls + Best Practices + Patterns (5) + Anti-Patterns + Breakpoints + Z-Index + Color 26+2 + TS verbatim | — | — | Missing → restore |
| Appendices | A ADRs 6 + B Live-Site + C Meticulous + D Second-hop + E Validation + F St Mary→Risen diff + QR | E Validation 10/10 structure | D Rother→St Joseph origin | B Runbook + C Ledger → merge as B + Runbook + D/E/F full |

---

## 10. Appendix C — Risk Register & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Tail-end decay re-introduced** by condensing appendices | High if draft expanded naively | Critical — fossilized smoke + validation re-introduced | Use §3.2 map: keep appendices A–F full verbatim, parameterized smoke with Risen example — not condensed ledger |
| **Token drift** by incomplete `@theme` | High (draft already truncated) | High — `grep shrine- src/index.css → 26+2` fails | Copy full `@theme` from risen + add `gold-700`; verify via `rg` in Phase 5 |
| **Parish re-introduction** outside ledger | Medium (WOHA/hill narratives leak) | Critical — fidelity breach | §1 one-breath per parish + `site.ts` single-source reminder; `rg Tepeyac|Oklahoma` only in Appendix D |
| **Metric drift** by hardcoding `31/172` vs `35/202` | High (sources already drift) | Medium — docs lie vs `docs-contract` | Decision C: prose says `~35/202 (asserted by docs-contract)`; §5.2 itemized list is informative, not authoritative |
| **Scope creep** (new tokens/routes/utils) | Low | Medium — adds unverified design debt | Freeze: no new tokens/routes/utils beyond 26+2 superset + 28 utilities; any addition requires ADR |
| **File too long to review** (~1500 lines) | Medium | Low — reviewer fatigue | Keep `risen-christ` as diff base — reviewers can `diff -u risen-christ_SKILL.md unified-v3_SKILL.md` to see ~80-line delta, not 1500 new |

---

## 11. Next Step (VALIDATE)

**Reply with one of:**

- `approve plan as-is` — I will write `new-skills/unified-v3_SKILL.md` (~1450 lines, §§1–20 + Appendices A–F + Quick Ref, v3.0.0, Risen baseline + 26+2 superset, 15 anti-patterns, parameterized smoke) in one `write` call, then verify via `rg` and start the frozen-sources commit.
- `Q1: … / Q2: …` per §4 table — I will revise the plan and re-issue before writing.

No file will be written until you validate.
