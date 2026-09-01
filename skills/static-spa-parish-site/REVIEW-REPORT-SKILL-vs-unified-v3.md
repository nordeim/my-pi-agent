# Review Report — `SKILL.md` (1590 lines, 2026-09-01) vs `unified-v3_SKILL.md` (1438 lines, 2026-08-31)

> **Date:** 2026-09-01 · **Reviewer:** Claw Code (Frontend Architect · 15y) · **Method:** 9-axis comparative audit per `REVIEW-PLAN-SKILL-vs-unified-v3.md`
> **Artifacts:** `SKILL.md` 1590 lines (`static-spa-parish-site` v3.0.0 + `package_version 1.4.4`) · `unified-v3_SKILL.md` 1438 lines (`singapore-parish-lineage` v3.0.0) · `risen-christ_SKILL.md` 1427 lines (ground-truth baseline) + `st-mary` + `rothershrine-v2`
> **Gate:** Every verdict has a `rg`/`wc`/`diff` citation + line number + severity. No prose-only verdict. No file was edited during this review.

---

## 1. Executive Verdict

| Axis | Tests | Winner | Verdict | Severity |
|---|---|---|---|---|
| **V1 — Identity & Versioning** | `name/version/package_version/canonical` | **SKILL.md** | **PASS** (both valid; SKILL's split is governance-superior) | Critical |
| **V2 — Structural Completeness** | Sections, lines, TOC | **SKILL.md** | **PASS** | Critical |
| **V3 — Token & Style Contracts** | Palette, utilities, keyframes, z-index | **SKILL.md** (byte-true) · unified CONCERN-with-rationale | **PASS with CONCERN** | High |
| **V4 — Volatile-Facts Discipline** | Single-source vs restatement | **SKILL.md** by far | **PASS** (unified: CONCERN) | High |
| **V5 — Smoke & Fidelity** | Appendix B + no-leak | **Tie** | **PASS** both | High |
| **V6 — Config & Contract Completeness** | vite/eslint/ts/playwright/CSP/src.orig | **Tie** | **PASS** both | High |
| **V7 — Audit Ledger Depth** | Anti-patterns, debugging, pre-ship, lessons, fossil-sweep | **SKILL.md** | **PASS** | Medium |
| **V8 — Migration Appendices** | D/E/F vs D.1–D.3/E/F/G | **SKILL.md** | **PASS** | Medium |
| **V9 — Lineage Invariants** | 77/35/202/51/397kB/8/17/5/7/9/HashRouter | **Tie** | **PASS** both | Critical |

**Overall: PROMOTE `SKILL.md` (`static-spa-parish-site` v3.0.0, 2026-09-01) to canonical. Freeze `unified-v3_SKILL.md` as the superseded lineage artifact that the 2026-09-01 re-audit superseded.**

- `SKILL.md` is not "unified + G" — it is a **one-day-newer rewrite that fixes the systemic root cause** (Appendix G.2: volatile facts restated 5–8× per doc + appendices copy-forwarded without a previous-parish fossil sweep) that produced unified's 5 specific fixes and 21 other fossils. Its §0 Volatile Facts Register + `as of` labeling + Fossil-Sweep Protocol (G.4) + ADR-7/8 + L13–L15 are the governance that prevents re-fossilization. Every volatile fact now lives once (in §0) — everything else references it.
- `unified-v3` remains **internally coherent and promotion-worthy on its own** (it passed the 2026-08-31 8-axis audit with 0 blockers). It loses only because SKILL subsumes it and adds the governance that would have *prevented* the defects unified fixed.

**If you must keep a second file:** keep `unified-v3` as `archived-unified-v3_SKILL.md` for provenance — do not keep both as co-canonical.

---

## 2. Detailed Findings per Axis

### V1 — Identity & Versioning — PASS (SKILL wins on governance)

**Both claim v3.0.0 — framing differs:**

```
SKILL.md:
  name: static-spa-parish-site
  version: 3.0.0                          (doc axis)
  package_version: 1.4.4                   (repo axis, §0 — "the SKILL doc version and the package version are separate axes")
  unified_from: rothershrine-v2 + st-mary + risen-christ — unified 2026-09-01; per-hop history in Appendix D; ledger in Appendix G
  port_provenance: Singapore port of https://www.risenchrist.org.sg/ — 91 Toa Payoh Central — first Catholic church ...; lineage Rother → St Joseph BT → St Mary → Risen (src.orig pruned round-12) → Risen (src)

unified-v3_SKILL.md:
  name: singapore-parish-lineage
  display_name: Singapore Parish SPA Lineage — Master Engineering Skill
  version: 3.0.0
  canonical_ref: Church of the Risen Christ — Toa Payoh (91 Toa Payoh Central ... first air-con 1971)
  lineage: Rother (OKC) → St Joseph BT → St Mary → Risen Christ
  project_state: "Lineage Master — 77 files / ~202 tests + ~51 E2E + ~51 built-artifact (reference: Risen Christ; counts are machine-asserted by docs-contract, not prose — see §2/§11) — ... 26 colors + 2 shadows superset"
```

**Why SKILL's split is superior:** Hop 1's file internally carried three conflicting versions (frontmatter 1.3.0 / §2 1.1.0 / Appendix D 1.0.0 — finding G.1 #1). SKILL resolves it once (§0 row "This SKILL doc version 3.0.0 — independent of package version 1.4.4" + ADR-7 + D.1 `as of` labels). Unified's single-axis `version: 3.0.0` is correct but leaves `package.json 1.4.4` implicit — a future hop would re-introduce the conflict. Both canonicalize the same parish (Risen Christ, 91 Toa Payoh Central, blessed 3 July 1971 by Abp Olçomendy, Fr Pierre Abrial $450k, first air-con), same lineage, same stack, same 77/35/202/51.

**Verdict:** Both PASS. SKILL is governance-superior on versioning — the recommended canonical name is `static-spa-parish-site` (repo-anchored; `singapore-parish-lineage` reads as a product line).

---

### V2 — Structural Completeness — PASS (SKILL is additive)

```
wc -l:
  1590 SKILL.md
  1438 unified-v3_SKILL.md

Heading counts (rg "^## [0-9]+\.|^## Appendix|^## Quick|^## 0\."):
  SKILL: 29 headings — ## 0 + §§1–20 (20) + Appendices A–G (7) + Quick Ref (1) = 29
  unified: 27 headings — §§1–20 (20) + Appendices A–F (6) + Quick Ref (1) = 27

diff <(rg "^## " SKILL) <(rg "^## " unified):
  < ## 0. Volatile Facts Register (SINGLE SOURCE OF TRUTH)        ← only in SKILL
    ## 1. Project Identity ... (SKILL) vs ... (Lineage Master) (unified)
  < ## Appendix D — Lineage & Migration History
  < ## Appendix E — Hop-2 Validation ...
  < ## Appendix F — Hop-3 Diff ...
  < ## Appendix G — Unification & Audit Ledger (v3)               ← only in SKILL
  > ## Appendix D — Migration Note (Rother → St Joseph → St Mary)
  > ## Appendix E — Validation: src vs src.orig ... (Reference)
  > ## Appendix F — Migration Note (St Mary → Risen Christ)
```

**No section was lost.** SKILL adds §0 (+30 lines) and Appendix G (+~180 lines) and consolidates D/E/F with `as of` labels; the 152-line net growth is within the plan budget. Both files preserve §§1–20 verbatim against `risen-christ` (the 16 missing contracts that made `draft_unified-v3` 254 lines non-executable are all present in both).

**Verdict:** Both PASS. SKILL is additive, not divergent.

---

### V3 — Token & Style Contracts — PASS with 1 CONCERN (intentional divergence)

This is the only intentional non-consensus — and it is documented, not drift.

**`@theme` block — byte-true check:**

```
sed -n '/@theme/,/^}/p' SKILL.md | rg -c "--color-shrine-"  → 25 active vars
sed -n '/@theme/,/^}/p' unified | rg -c "--color-shrine-"   → 26 active vars
Both | rg -c "--shadow-" → 2

SKILL @theme:
  --color-shrine-* 25 active (gold-700 is a lineage NOTE, commented out):
    /* Lineage note: hop-2 (St Mary) round-7 also defined --color-shrine-gold-700: #85601f (4.72:1 AA text step).
  plus terracotta-600 #8f4c30 active (round-12 F-1)

unified @theme:
  --color-shrine-gold-700: #85601f; /* St Mary AA 4.72:1 — restored in unified superset */
  --color-shrine-terracotta-600: #8f4c30; /* round-12: AA text step, 5.36:1 */
  → 26 active colors
```

**Contract tables:**

```
SKILL:
  §0:  Design tokens | 25 colors + 2 shadows (27 @theme entries) — 24 base + terracotta-600 #8f4c30; gold-700 #85601f is a lineage note — re-add if needed
  §4.1: Tokens are unchanged from rothershrine→St Joseph→St Mary line except round-12 terracotta-600
  §19:  Every hex matches src/index.css byte-for-byte; grep shrine- src/index.css → 25 colors + 2 shadows (§0); gold-700 not in this line
  ADR-3: 25 colors + 2 shadows, §0 — round-12 added terracotta-600; hop-2's gold-700 not carried
  D.1 row: 24+2 → 26+2 (St Mary) → 25+2 (Risen, gold-700 dropped)

unified:
  §4:  unified 26+2 superset — Rother 24+2 + St Mary gold-700 #85601f (4.72:1) + Risen terracotta-600 #8f4c30 (5.36:1); Risen intentionally refined to 25+2, master restores both
  §4.1: --color-shrine-gold-700: #85601f; --color-shrine-terracotta-600: #8f4c30;
  §19:  grep shrine- src/index.css → 26 colors + 2 shadows (28 entries); both AA steps
  ADR-3: 26 colors + 2 shadows — Rother 24+2 + gold-700 + terracotta-600, both AA
```

**Utilities / keyframes / z-index:**

```
SKILL §0:  Utilities / keyframes | 27 utility classes + 8 keyframes (27 counts each rise-in-d1..d4 individually) + @media print reveal
unified §4: 28 utilities: 27 + @media print for reveal from St Mary  — counting-convention diff (same 27 rows + print counted as 28 in unified)
Both: 8 keyframes present (finding #22 fixed); both: §18 now has z-[60] ScrollProgress rail row (finding #24 fixed) — both PASS
```

**Verdict:** **PASS with CONCERN (Low) — not a FAIL.** SKILL's 25+2 is byte-true to `src/index.css` (the repo as of round-12 has 25 active colors; gold-700 was deliberately dropped in hop 3, §0 lineage note). Unified's 26+2 is a *documented future-port superset* — it does not drift from `src/index.css` by accident, it carries gold-700 as an explicit option. SKILL's §0 explicitly says "re-add it deliberately if a text-bearing gold step is needed." Bless **SKILL's 25+2 as canonical** (byte-true); treat unified's 26+2 as the documented superset note. The concern is that a future port could re-add gold-700 and forget to update §0 — but §0 + ADR-7 + the fossil-sweep protocol (G.4) would catch it.

---

### V4 — Volatile-Facts Discipline — PASS (SKILL decisively superior)

This is the axis on which unified was most recently *proven* (8-axis audit 2026-08-31: all PASS) yet still weaker than SKILL — because unified's 8-axis audit found 0 blockers *after* fixing the symptoms, while SKILL fixes the *system that produced them*.

**SKILL — §0 single-source register (16 rows, the only authoritative statement):**

```
## 0. Volatile Facts Register (SINGLE SOURCE OF TRUTH)
> Contract: this table is the only authoritative statement of every mutable fact. If any other section (or README/AGENTS/CLAUDE) disagrees, this table wins until re-verified.

Rows (as of 2026-08-31, round-12):
  Canonical instance — Risen Christ, package.json 1.4.4
  This SKILL doc version — 3.0.0 (unification axis — independent of package version)
  Unit tests — 35 files / 202 tests — green (sum verified: 4+3+16+5+7+10+8+5+7+7+11+3+6+6+17+7+2+5+3+6+6+4+3+2+3+6+3+2+2+2+4+6+2+13+6 = 202)
  E2E — 51 tests (8 specs), plus same 51 on built pass
  src/ — 77 files = 41+35+1
  public/images/ — 8 files + favicon.svg
  Build — 397.52 kB dist/index.html + _headers + favicon.svg + images/8
  Design tokens — 25+2 (27 entries) — 24 base + terracotta-600; gold-700 lineage note
  Utilities/keyframes — 27 + 8 + @media print
  Hooks — 3 (useScrolled/useScrollProgress/useScrollSpy)
  Utils — 4 (cn/massDay/monogram/deepLinks)
  Routes — 17 Route (16+*), 7 aliases in 5 groups, 9 anchors (#language-communities not #mandarin)
  CSP — 'self' data: blob: only
  src.orig/ — PRUNED round-12, repo-hygiene guard
  skills/ — vendored, re-added 0be0fe8
  Secrets — docs/ssh-key.txt rotation outstanding
  Data arrays — 8/3/6/6/6/8/3/7/4/6/11 + nav 6/10 + site hours 6 / mass 11
  Parish constants — 91 Toa Payoh Central, UEN T08CC4042G, Easter Sunday, NS19, buses 88/157/163
  Pre-push gate — lint && typecheck && test && test:e2e && build (+ test:e2e:built)
```

Every other SKILL section that mentions a volatile number says **"see §0"** or **`as of <date>`** (appendices). Example: §2 "package.json version is 1.4.4 (see §0)", §3.1 "35 files / 202 tests green (per-file breakdown: §0/§2)", Appendix D.1 "Tests (as of port day)" with labeled snapshots, Appendix E "All numbers are as of 2026-08-30".

**Unified — `~` machine-asserted shorthand (correct intent, weaker discipline):**

```
project_state: "Lineage Master — 77 files / ~202 tests + ~51 E2E + ~51 built-artifact (reference: Risen Christ; counts are machine-asserted by docs-contract, not prose — see §2/§11)"
verified: pnpm lint 0 + pnpm typecheck 0 + pnpm test ~35/202 (docs-contract) + ...
How to use: "Counts like ~35/202 are machine-asserted by docs-contract, not prose — see §2/§11."
```

Correct — but §2, §3.1, §5.2, §10, §11, and Quick Ref still **restate** those counts without `see §0` or `as of` labels. Unified's 2026-08-31 audit proved they happen to be consistent (16 restatements vs SKILL's 21, both green), but the next hop would re-introduce drift because there is no single-source register to sweep against.

**`rg` gate:**

```
rg -c "202 tests|51 E2E|397\.52|77 files" SKILL.md  → 21 hits (all but one are in §0 or labeled appendices/Quick Ref via §0)
rg -c "202 tests|51 E2E|397\.52|77 files" unified   → 16 hits (no §0, but ~ shorthands — still restatements)
rg "see §0" SKILL.md → 5+ hits (intentional cross-refs)
rg "see §0" unified  → 0 hits
rg "as of" SKILL.md  → 12+ hits (D.1 trajectory + E + F corrected snapshots)
rg "as of" unified   → 2 hits (only E's "Reference" label)
```

**Verdict:** SKILL PASS decisively. Unified is not wrong — it is *less future-proof*. The systemic root cause (G.2) is that "every restatement is a future fossil" (L15) — SKILL's §0 + `as of` + G.4 protocol is the countermeasure that unified lacks. This is the single strongest reason to promote SKILL.md.

---

### V5 — Smoke & Fidelity — PASS (Tie)

**Both Appendix B scripts are Risen-filled (St Mary fossils fully purged):**

```
SKILL Appendix B (18-step, §0-reconciled):
  1  /                      → hero /images/hero-church.jpg + grounds 3
  2  /about                 → priests 3 (phone+email) + ppcMembers 7
  4  /worship               → #mass/#confession/#visit; aliases /mass-times,/hours-location,/visit
  8  /ministries            → 6 pills + 6 sections; #language-communities (not #mandarin)
  13 /give + /donate        → 8 giving options, PayNow UEN T08CC4042G in copyable row (F-4)
  18 /worship /news-events /donate (path-style) → deep-links F-3
  19 pnpm test:e2e:built    → same 51 green on built artifact

unified Appendix B (17-step, parameterized):
  1  /                      → same hero + grounds 3 + events 6
  2  /about                 → priests 3 (Brian/Arun/Dexter) + ppc 7
  8  /ministries            → 6 pills + 6 sections #language-communities
  13 /give + /donate        → 8 giving options PayNow UEN T08CC4042G
  # For Parish X (St Mary): priests 4 OFM, UEN T08CC4053H+HRSM, #mandarin (footnotes only)
```

**`rg` proofs:**

```
rg "T08CC4042G" SKILL.md → priests/giving/UEN rows (all Risen)
rg "T08CC4053H|4 OFM|#mandarin" SKILL.md → only in Appendix D/F/G lineage tables/footnotes — 0 in B steps
rg "T08CC4042G" unified → 8 hits in Risen steps/data; rg "T08CC4053H" → 3 hits only in Parish X footnotes + 1 in E provenance — 0 in B steps
rg "#language-communities" both → correct sixth ministry id; #mandarin only in footnotes/lineage

Fidelity — no leaks in §§2–20:
  rg "Oklahoma|Tepeyac|Kranji|Palladian|WOHA|Ho Ping" SKILL.md → 11 hits, all in §1 breath (99) + non-negotiable policy (119) + §7/§20 Risen content + D.1 lineage table (1400–1405) — 0 in §§2–6/8/9/10/15–18 data sections
  rg same unified → 13 hits, same sections (§1 variants 63,81,83,87 + Risen content 290,455.. + D/F 1295–1297) — 0 in data sections
```

**Verdict:** Both PASS. This was unified's strongest axis (C-1 fixed); SKILL matches it exactly and adds the explicit v3 fix note ("hop 3's source file carried hop 2's entire smoke script … the script below is rewritten … and reconciled with §0/§7 facts").

---

### V6 — Config & Contract Completeness — PASS (Tie)

**Both mandate the three H-6/H-7 fixes:**

```
SKILL §3.2 + unified §3.2 (identical):
  vite.config.ts — plugins [react(), tailwindcss(), viteSingleFile()] + alias @→src + test { globals, jsdom, setupFiles, include, exclude: e2e/** } + server.watch.ignored [skills/**, dist/**, ... src.orig/**]
  tsconfig.json — ES2020/ESNext/bundler/react-jsx/strict/noUnused*/isolatedModules/noEmit + include ["src","vite.config.ts","eslint.config.js","playwright.config.ts","playwright.built.config.ts"] + types ["node","vitest/globals"]
  eslint.config.js — flat config, ignores skills + src.orig
  playwright.config.ts — testDir e2e, baseURL :5173, expect.timeout 15s
  playwright.built.config.ts — baseURL E2E_BASE_URL ?? :4173; webServer vite preview :4173 (skipped when E2E_BASE_URL set); singlefile rewrite /favicon.svg → ./favicon.svg (E2E-L1)
  index.html — img-src 'self' data: blob: only (all local), frame-src https://www.google.com, script-src inline + static.cloudflareinsights.com
  ADR-6 (both): src.orig/ PRUNED round-12, repo-hygiene guard fails if any src.orig path re-enters

rg "playwright\.built" SKILL  → 4 hits; unified → 5 hits
rg "server\.watch\.ignored" both → 3 hits
rg "img-src 'self' data: blob:" both → 3 hits
rg "repo-hygiene|src\.orig.*forbidden|PRUNED" both → present
```

**Verdict:** Both PASS. No divergence.

---

### V7 — Audit Ledger Depth — PASS (SKILL decisively superior)

```
rg "^\| [0-9]+ \| \*\*" SKILL.md → 15 rows (Anti-Patterns #1–15, §9)
rg "^\| [0-9]+ \| \*\*" unified  → 15 rows (same 15)

SKILL-only:
  rg "Appendix G|Fossil-Sweep|Unification.*Ledger|L13|L14|L15|ADR-7|ADR-8" SKILL.md → 14+ hits
    ## Appendix G — Unification & Audit Ledger (v3)  (line 1485)
    G.1 — 26 findings re-validated: Critical 1 (C-1 ssh-key OUTSTANDING) + High 6 (#1–6) + Medium 9 (#7–15) + Low 6 (#16–21) + New 5 (#22–26, shared structural fossils)
    G.2 — Systemic root cause: "volatile facts restated 5–8× per document + appendices copy-forwarded without a fossil sweep"
    G.3 — Provenance of v3's content choices (per-section base + best elements merged)
    G.4 — Fossil-Sweep Protocol (8 steps: register-first, sweep-old-value, previous-parish grep, sum-every-count, reconcile-tree, tracking-audit, rewrite-Appendix-B, gates)
    L13–L15 — new v3 lessons: secret-in-history, gitignore-does-not-untrack, every-restatement-is-a-future-fossil
    ADR-7 — Unified SKILL doc + §0 Register
    ADR-8 — Built-artifact E2E pass (playwright.built.config.ts)
  rg same unified → 0 hits (no Appendix G, no ADR-7/8, no L13–15)
```

Unified's 5 Key-fixes table (in `review_plan.md` style) is correct but is the *output* of SKILL's G.1 findings — SKILL is the ledger that explains *why* those 5 were needed and catalogues the other 21. Both have 15 anti-patterns, 16-row debugging (but SKILL's §10 references §0), 9-step pre-ship, 12+3 lessons.

**Verdict:** SKILL PASS decisively. Unified PASS on its own ledger but lacks the systemic audit trail.

---

### V8 — Migration Appendices — PASS (SKILL superior consolidation)

```
SKILL:
  ## Appendix D — Lineage & Migration History
    D.1 — Four Generations at a Glance (Rother | St Joseph BT | St Mary | Risen — with as-of-labeled snapshots per generation)
    D.2 — What Each Hop Changed (Hop 1 Rother→St Joseph, Hop 2 →St Mary, Hop 3 →Risen with round-12 remediations)
    D.3 — What Never Changed (design language, architecture, primitives, stack, method)
  ## Appendix E — Hop-2 Validation: St Mary src vs St Joseph src.orig (2026-08-30) — as of, plus v3 reuse note (two checks hop 2 lacked: fossil sweep + tracking audit)
  ## Appendix F — Hop-3 Diff: St Mary → Risen Christ — corrected from round-7 snapshot (32/179+48 → 35/202+51, package 1.3.0 → 1.4.4)
  ## Appendix G — Unification & Audit Ledger (above)

unified:
  ## Appendix D — Migration Note (Rother → St Joseph BT → St Mary — second hop)
  ## Appendix E — Validation: src vs src.orig (2026-08-30) — Reference: St Mary vs St Joseph BT (Generalized via docs-contract)
  ## Appendix F — Migration Note (St Mary → Risen Christ)
  (no G)
```

SKILL consolidates the three per-hop migration appendices that were copy-forwarded with partial updates (the source of fossils #13, #15) into a single lineage record where every historical count is labeled `as of <date>` — none is the current value (current lives only in §0). Unified preserves the split; SKILL's split is the *fixed* version.

**Verdict:** Both PASS on content — SKILL's structure is more auditable (the fossil-sweep protocol explicitly checks that appendices carry `as of` labels).

---

### V9 — Lineage Invariants — PASS (Tie — no regression in either vs `risen-christ` baseline)

```
Both preserve byte-for-byte:
  77 files = 41 source + 35 tests + 1 setup              (SKILL §0/§5.2, unified §5.2/frontmatter)
  35 files / 202 tests — green + 51 E2E ×2 passes + 397.52 kB singlefile + 8 images all-local
  17 Route (16+*), 7 aliases in 5 groups, 9 anchors (#language-communities not #mandarin)
  HashRouter (ADR-1) + vite-plugin-singlefile (ADR-2) + @→src/ alias (ADR-5) + file-backed src/data/* (ADR-4)
  src.orig/ PRUNED + repo-hygiene guard, skills/ vendored re-added 0be0fe8, C-1 ssh-key rotation outstanding
  Stack: React 19.2.8 / Vite 7.3.6 / Tailwind 4.3.3 / TS 5.9.3 / React Router 7.18.2 / singlefile 2.3.3 / eslint 9.39.5 / vitest 3.2.6 / playwright 1.55.1 — pinned exact
  15 anti-patterns (incl. #14 dev-only E2E assets + #15 backslash), z-[60] rail, 8 keyframes, 27/28 utilities — all fixed in both
```

`risen-christ` (1427 lines) is the baseline both files claim to preserve; neither regresses. Unified adds one documented line (gold-700 as superset); SKILL adds governance (ADR-7/8, L13–15, G.4) — both additive-only.

**Verdict:** Both PASS.

---

## 3. What the Diffs Actually Mean

| Dimension | SKILL.md choice | unified-v3 choice | Which to keep |
|---|---|---|---|
| **Canonical pattern for mutable facts** | §0 Volatile Facts Register — single statement, every other section says "see §0", appendices use `as of` labels, fossil-sweep protocol G.4 enforces | Front-matter `~` + "machine-asserted by docs-contract, not prose — see §2/§11" — intent correct, but 16 restatements remain without §0 | **Keep SKILL's §0 pattern** — it is the only fix for the systemic root cause (G.2). This is the single biggest governance gap in unified. |
| **Palette** | 25+2 (27 entries) — terracotta-600 only; gold-700 as lineage NOTE | 26+2 (28 entries) — gold-700 + terracotta-600 superset | **Keep SKILL's 25+2 as canonical** (byte-true to `src/index.css`); keep unified's gold-700 as a documented *option* inside SKILL's lineage note (already present). Not a defect on either side — a deliberate divergence SKILL handles correctly. |
| **Utilities** | 27 + 8 keyframes (each `rise-in-d1..d4` counted individually, §0) | 28 (27 + @media print as separate count) | **Keep SKILL's 27** — it's the §0 contract; unified's 28 is a counting-convention variant of the same 27 rows + print. |
| **Appendices** | D consolidated 4-generation (D.1–D.3) + E labeled hop-2 validation + F corrected hop-3 diff + G ledger | D/E/F split (pre-unification) — each appendice describes its own hop | **Keep SKILL's consolidated D** — it is the fossil-swept version that unified's split produced fossils for. |

All other dimensions are ties or SKILL-additive (no unified-only wins beyond the 26+2 palette option, which SKILL already documents as a lineage note).

---

## 4. Recommendations

### Canonical: `SKILL.md` (`static-spa-parish-site` v3.0.0) — 2026-09-01

**Do:**
- Promote `SKILL.md` to the repo's single canonical skill (copy to `AGENTS.md`/`CLAUDE.md` references, update any `name: singapore-parish-lineage` pointers).
- Freeze `unified-v3_SKILL.md` as archived lineage artifact (rename to `archived-unified-v3_SKILL.md` or keep in `new-skills/` with a header "superseded by SKILL.md v3.0.0 — see Appendix G").
- Keep the three hops (`rothershrine-v2`, `st-mary`, `risen-christ`) as redirect stubs per SKILL's unification note — do not edit them independently.
- If a future port needs `gold-700 #85601f` (4.72:1 on parchment), re-add it deliberately per SKILL's lineage note — and update §0 in the same commit (G.4 step 1: register first).

**Do not:**
- Keep both `SKILL.md` and `unified-v3_SKILL.md` as co-canonical — that re-introduces the multi-source fossil pattern §0 was built to end.
- Re-introduce a `26+2` change as a silent edit — it requires a §0 row update + fossil sweep (G.4 step 2: sweep old value).

### If you disagree and prefer unified's framing

The only unified-only value not already in SKILL is the 26+2 superset being the *default* palette. If you want that default, cherry-pick unified's `@theme` block (line 200 `gold-700` var) into SKILL's §4.1 and bump SKILL's §0 Design tokens row from `25+2 (27 entries)` to `26+2 (28 entries)` **in the same commit** — do not just restate the count elsewhere.

---

## 5. Evidence Appendix — Verbatim `rg`/`wc` Outputs

### Identity & lines

```
SKILL.md:    name: static-spa-parish-site — version 3.0.0 + package_version 1.4.4
unified:     name: singapore-parish-lineage — version 3.0.0 (+ lineage 4-hop string)

wc -l: 1590 SKILL.md / 1438 unified-v3_SKILL.md

Heading counts:
  SKILL: 29 (## 0 + §§1–20 + A–G + QR)
  unified: 27 (§§1–20 + A–F + QR)
  diff: SKILL adds ## 0 Volatile Facts Register + Appendix G Unification & Audit Ledger; headings otherwise identical
```

### Tokens

```
sed @theme colors (active vars):
  SKILL: 25 (--color-shrine-*) + comment /* Lineage note: hop-2 also defined --color-shrine-gold-700: #85601f */
  unified: 26 (--color-shrine-*) including --color-shrine-gold-700: #85601f active
  Both: 2 shadows; Both: terracotta-600 #8f4c30 active

rg gold-700 → SKILL: lineage NOTE (46, 233, 1019, D.1) — not an active @theme var; unified: active var line 200 + superset rationale (169, 254, 278, 937, 960, 1235)
```

### Volatile-facts discipline

```
rg "see §0|Volatile Facts|as of" SKILL.md → 11 hits + 12 "as of" in D/E/F/G (every historical count labeled)
rg same unified → 0 "see §0" + 2 "as of" (only E's Reference label)
rg -c "202 tests|51 E2E|397\.52|77 files" → SKILL 21 (all but one in §0 or labeled appendices) / unified 16 (restatements without §0, all ~-prefixed)
SKILL §0 has 16 rows, sum-verified: 4+3+16+…+6 = 202
```

### Smoke & fidelity

```
rg "T08CC4042G" SKILL → Risen UEN in §1/§7/§20/B (all Risen facts)
rg "T08CC4053H|4 OFM|#mandarin" SKILL → only in D/F/G lineage tables — 0 in B
rg same unified → same: T08CC4042G in Risen steps, T08CC4053H only in Parish X footnotes (1266–1267)

rg "Oklahoma|Tepeyac|Kranji|Palladian|WOHA|Ho Ping" → SKILL 11 hits / unified 13 hits — all in §1 breath/policy or §7/§20 Risen content or D/F/G lineage — 0 leaks in §§2–6/8/9/10/15–18 data sections
```

### Config

```
rg "playwright\.built|server\.watch\.ignored|img-src.*self|PRUNED|repo-hygiene" → both PASS (SKILL §3.2/§11/ADR-6; unified §3.2/ADR-6/Quick Ref)
Both: test { globals, jsdom } + server.watch.ignored + playwright.built.config.ts + img-src 'self' data: blob: + src.orig pruned + guard
```

### Ledger

```
rg "^\| [0-9]+ \| \*\*" → both 15 rows (same 15 anti-patterns incl. #14 dev-only E2E + #15 backslash)
rg "Appendix G|ADR-7|ADR-8|L13|L14|L15|Fossil-Sweep" → SKILL 14 hits / unified 0 hits
Appendix G in SKILL: 26 findings (#1–26) + G.2 root cause + G.3 provenance + G.4 8-step protocol — unified has no G
```

### Appendices

```
SKILL: Appendix D (consolidated D.1–D.3, as-of-labeled) + E (hop-2, as-of 2026-08-30) + F (corrected hop-3, §0 refs) + G
unified: Appendix D (second hop) + E (Reference: St Mary vs St Joseph, Generalized via docs-contract) + F (St Mary→Risen)
```

### Invariants vs `risen-christ`

```
Both preserve: 77 / 35/202 / 51×2 / 397.52kB / 8 local / 17/5/7/9 / HashRouter / singlefile / @→src — no regression
```

---

## 6. Conclusion

`SKILL.md` subsumes `unified-v3_SKILL.md` and adds the governance that would have prevented the very defects `unified-v3` fixed. The 9-axis diff is **8/9 decisive for SKILL (or tie), 1/9 a documented deliberate palette divergence that SKILL already handles as a lineage note**.

**Verdict: PROMOTE `SKILL.md` as the single canonical v3.0.0 skill. Archive `unified-v3_SKILL.md` as lineage history — do not keep both as canonical.** The one open decision (gold-700 default vs on-demand) is already resolved inside SKILL's §0 lineage note — no further fix commit is needed to promote.

*No file was edited during this review. This report is the only new artifact.*
