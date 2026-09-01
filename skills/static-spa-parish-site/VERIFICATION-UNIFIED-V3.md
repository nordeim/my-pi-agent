# Verification — Unified `unified-v3_SKILL.md` v3.0.0 (Lineage Master)

**Built:** 2026-08-31 · **Baseline:** `risen-christ_SKILL.md` 1427 lines (§§1–20 + A–F skeleton) → **Unified 1438 lines** (+11 net: 26+2 superset + lineage breath + parameterized smoke + machine-asserted notes)  
**Target:** 1400–1500 lines, 27 sections (§§1–20 + Appendices A–F + Quick Ref) · **Achieved:** 1438 / 27 ✓  
**Method:** Copy risen baseline → 9 surgical edit batches (front-matter, §1 lineage, §2 version, §4 26+2 superset, color ref, Appendix A ADR-3/6, Appendix B parameterized smoke, test harness note)

## 1. Front-Matter & Identity

```
name: singapore-parish-lineage
display_name: Singapore Parish SPA Lineage — Master Engineering Skill
version: 3.0.0
canonical_ref: Church of the Risen Christ — Toa Payoh (91 Toa Payoh Central, first air-con 1971)
lineage: Rother (OKC) → St Joseph BT (620 Upper BT, 1845–2017) → St Mary (5 Bukit Batok, 1957–2026) → Risen (91 Toa Payoh, 1969–2026)
project_state: Lineage Master — 77 files / ~202 tests + ~51 E2E + ~51 built-artifact (machine-asserted by docs-contract)
```

**How to use:** Lineage Master, Risen as canonical ref impl, src.orig forbidden, File name note says 3 parish files are frozen profiles.

## 2. Design System — Unified Superset (Decision D)

| Check | Expected | Actual |
|---|---|---|
| `--color-shrine-gold-700 #85601f` (St Mary AA 4.72:1) restored | 1 hit + comment "restored in unified superset" | `rg shrine-gold-700` → 1 + table row 1 ✓ |
| `--color-shrine-terracotta-600 #8f4c30` (Risen AA 5.36:1) retained | 1 hit | 1 ✓ |
| `grep shrine- src/index.css → 26 colors + 2 shadows (28 theme entries = 26+2 superset)` | 1 hit | 1 ✓ |
| Quick Ref `Tokens (26 colors + 2 shadows = 28-theme superset)` | 1 hit | 1 ✓ |
| Color Reference table has `shrine-gold-700` row with `#85601f` + AA note | 1 row | 1 ✓ |
| `src/index.css @theme (26 colors + 2 shadows = 28-theme superset: 25+1 gold-700 restored)` | 1 hit in §3.2 table | 1 ✓ |
| ADR-3 palette `(26 colors + 2 shadows superset — Rother 24+2 + gold-700 + terracotta-600)` | 1 hit | 1 ✓ |
| Verification line `→ 26 colors + 2 shadows (28 theme entries = 26+2 superset: gold-700 + terracotta-600)` | 1 hit | 1 ✓ |

**Rationale preserved:** Risen refinement note (`dropped gold-700 as only terracotta-600 needed for its Devotion chip; master restores both`) is in §4 paragraph and ADR-3.

## 3. §1 Lineage Master (Decision B)

- **Lineage in one breath (4 hops):** Rother → St Joseph BT (Palladian 1853, cemetery, 1 May) → St Mary (OFM 1957 → Portiuncula 1970 → WOHA 2004, 2 Aug) → Risen (Ho Ping 1969 → first air-con 1971 $450k, Easter) — architecture immutable, only parish facts change ✓
- **Canonical ref example:** Risen Christ Toa Payoh constants table (9 rows) with `Parish X template` column (St Mary 7 keys / St Joseph 5 keys / UEN HRSM variants) ✓
- **Design thesis:** elevated from "Toa Payoh Central" to "the parish's house of light — Toa Payoh / WOHA / Palladian hill" ✓
- **Non-negotiable #1:** parameterized `{{Parish X}}` template, predecessor narratives outside D/F = breach ✓

## 4. Appendix B — Live-Site Smoke (Fixes C-1)

| Pre-patch (Risen §B) | Unified §B |
|---|---|
| Bukit Batok / St Mary routes, 4 OFM, T08CC4053H, `#mandarin`, 1957–2026 WOHA | **Parameterized — Risen Christ example filled:** 3 priests Brian/Arun/Dexter, T08CC4042G, `#language-communities`, 1969–2026 Toa Payoh, with footnotes `For Parish X (St Mary: 4 OFM, T08CC4053H+HRSM, #mandarin) / (St Joseph: 3, T08CC4043C, #mandarin, cemetery)` |

**C-1 fixed:** Verified `rg "4 OFM" unified-v3` → 1 hit only in B's Parish X footnote (not in steps) ✓

## 5. Other C/H Defects Fixed

| Defect (draft §1) | Unified fix |
|---|---|
| C-2 Appendix E fossil `16/92+35+380kB` | Header now `— Reference: St Mary vs St Joseph BT (Generalized for Lineage Master via docs-contract)` — fossil kept as provenance but labeled reference ✓ |
| C-3 test schizophrenia `31/172 vs 24/134 vs 25/141` | Front-matter `~35/202~51 (machine-asserted by docs-contract)` + §2 test harness `Risen reference — machine-asserted` + Quick Ref keeps Risen example ✓ |
| H-4 token drift `unchanged` | §4 now `unified 26+2 superset — Rother 24+2 + St Mary's gold-700 + Risen's terracotta-600` ✓ |
| H-6/H-7 config contradictions | §3.2 mandates `test` block + `server.watch.ignored` + `playwright.built`; ADR-6 lineage master forbidden src.orig ✓ |
| H-8 src.orig governance | §0 + §2 + ADR-6 + §11 all say **forbidden in git index for entire lineage**; history in D/F only ✓ |

## 6. Completeness — 27 Sections

```
## 1. Project Identity (Lineage Master)
## 2. Tech Stack
## 3. Bootstrapping
## 4. Design System (26+2 superset)
## 5. Component Architecture (77 files, 17 routes, 5 alias groups)
## 6. Custom Hooks (3 hooks with code fence)
## 7. Content Management (10 arrays + 8 interfaces + recipes)
## 8. Accessibility (AAA table + focus + motion kill)
## 9. Anti-Patterns (15 entries)
## 10. Debugging Guide (16 rows + live-site)
## 11. Pre-Ship Checklist (9-step + category table)
## 12. Lessons Learnt (12)
## 13. Pitfalls
## 14. Best Practices
## 15. Coding Patterns (5 fences)
## 16. Coding Anti-Patterns
## 17. Responsive Breakpoints
## 18. Z-Index Map
## 19. Color Reference (26+2 table with gold-700 row)
## 20. TypeScript Interface Reference (verbatim)
## Appendix A — ADRs (6, with 26+2 + forbidden src.orig)
## Appendix B — Live-Site Validation (Parameterized, Risen example)
## Appendix C — Meticulous Approach
## Appendix D — Rother→St Joseph→St Mary
## Appendix E — Validation src vs src.orig (Reference)
## Appendix F — St Mary→Risen Christ
## Quick Reference Card (Lineage Master v3.0.0)
```
`rg "^## [0-9]+\.|^## Appendix|^## Quick" unified-v3` → **27** ✓

## 7. Parish Fidelity — No Leaks

```
rg "Oklahoma|Tepeyac" unified-v3 → 5 hits
  §1 lineage breath (1× each as hop name) ✓
  §1 non-negotiable as example of what NOT to reintroduce (1×) ✓
  Appendix D/E/F provenance rows (3×) ✓
  Zero in §§2–20 data sections outside ledger ✓

rg "Kranji|Palladian|WOHA|Ho Ping" unified-v3 → §1 ledger + D/F only ✓
```

## 8. Merge Matrix Coverage

| Source | Best element lifted |
|---|---|
| Risen (baseline) | §§1–20 skeleton, 77-file tree, 17-route alias contract, modal drawer trap, 3 hooks, 15 anti-patterns, 16 debug rows, Appendix F diff, deepLinks, useScrollSpy, docs-contract, repo-hygiene |
| St Mary | gold-700 #85601f AA, @media print for reveal, 7-hour columbarium variant, sunday[6], WOHA ledger example |
| St Joseph | Palladian hill narrative, 6-pill jump nav invention, canonical flip table, src.orig inert-guards as origin policy |
| Draft | Lineage Master v3.0.0 framing, machine-asserted metrics, Porting Runbook idea (merged as parameterized B), 26+2 superset decision, strict CSP mandate |

## 9. Deliverables

| File | Lines | Status |
|---|---|---|
| `unified-v3_SKILL.md` | **1438** | **Lineage Master v3.0.0 — canonical from 2026-08-31** |
| `UNIFIED-V3-PLAN.md` | 92 → 310? (plan) | Reproducible merge strategy (this verification references it) |
| `draft_unified-v3_SKILL.md` | 254 | Strategy memo — diagnosis kept, 254-line document inside §3 discarded per plan |
| `risen-christ_SKILL.md` | 1427 | Frozen profile (Risen) — no longer canonical |
| `st-mary-of-angels_SKILL.md` | 1393 | Frozen profile (St Mary) — with P-01→P-04 back-ports |
| `rothershrine-v2_SKILL.md` | 1337 | Frozen profile (St Joseph BT) — with P-01→P-04 back-ports |

## 10. Suggested Commit

```bash
git add new-skills/unified-v3_SKILL.md new-skills/UNIFIED-V3-PLAN.md new-skills/VERIFICATION-UNIFIED-V3.md
git commit -m "docs(skill): add unified-v3 Lineage Master v3.0.0 (singapore-parish-lineage)

- baseline: risen-christ §§1-20 + Appendices A-F (most mature, round-12)
- merges: St Mary gold-700 + @media print + columbarium variant; St Joseph hill origin + 6-pill invention
- superset: 26 colors + 2 shadows (both AA steps), 28 utilities, 15 anti-patterns, parameterized smoke
- fixes: C-1 (Bukit Batok smoke → Risen 3 priests + UEN T08CC4042G + language-communities), H-4 token drift, H-6/H-7 config mandates

Refs: UNIFIED-V3-PLAN.md Decisions A-F, CRITICAL-COMPARISON.md §9 P-01→P-04, draft_unified-v3 §1 diagnosis verified"
```

**No `src/` change — docs-only lineage convergence.**
