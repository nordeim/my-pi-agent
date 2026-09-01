Unified unified-v3_SKILL.md v3.0.0 — Lineage Master complete, verified, and ready. 
 
### Built per UNIFIED-V3-PLAN.md (approved as-is) 
 
Baseline: risen-christ 1427-line §§1–20 + Appendices A–F skeleton (most mature: 35/202 + 51+51, useScrollSpy + deepLinks, docs-contract + repo-hygiene) 
Merged: St Mary gold-700 #85601f + @media print + columbarium variant · St Joseph BT Palladian hill origin + 6-pill invention · Draft's v3.0.0 framing + machine-asserted + strict CSP 
Result: unified-v3_SKILL.md 1438 lines / 27 sections (§§1–20 + A–F + Quick Ref) — 26 colors + 2 shadows superset, 28 utilities, 15 anti-patterns, parameterized smoke 
 
### Key fixes (draft diagnosis → unified) 
 
┌─────────────────────────────────────────────────────────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ 
│ Defect                                                          │ Unified fix                                                                                                                                 │ 
├─────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ 
│ C-1 Risen Appendix B = St Mary smoke (4 OFM, T08CC4053H,        │ Appendix B now parameterized — Risen example filled: 3 priests (Brian/Arun/Dexter), UEN T08CC4042G,                                         │ 
│ #mandarin)                                                      │                                                                                                                                             │ 
├─────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ 
│ H-4 unchanged from St Mary token drift                          │ §4 unified 26+2 superset — gold-700 (St Mary 4.72:1) + terracotta-600 (Risen 5.36:1), with Risen refinement rationale                       │ 
├─────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ 
│ H-6/H-7 vite test / CSP contradictions                          │ §3.2 + ADR-6 mandated: test { globals, jsdom } + server.watch.ignored + playwright.built.config.ts; img-src 'self' data: blob: only, legacy │ 
│                                                                 │ forbidden                                                                                                                                   │ 
├─────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ 
│ C-3 31/172 vs 24/134 schizophrenia                              │ Front-matter ~35/202~51 (machine-asserted by docs-contract) — prose no longer hardcodes drift-prone counts                                  │ 
├─────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ 
│ Tail-end decay (fossil validation 16/92)                        │ Appendix E relabeled Reference: St Mary vs St Joseph (Generalized via docs-contract) + §1 lineage breath keeps all 4 hops in one place      │ 
└─────────────────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ 
 
### Verification (all green) 
 
``` 
  front-matter:    singapore-parish-lineage v3.0.0, canonical Risen Toa Payoh, 4-hop lineage ✓ 
  tokens:          gold-700 + terracotta-600 → 26+2 / 28-theme superset ✓ 
  sections:        27 (§§1-20 + A-F + QR) ✓ 
  Appendix B:      Parameterized — Risen example (smoke) ✓ 
  fidelity:        Oklahoma/Tepeyac only in §1 breath + D/F provenance, 0 in data sections ✓ 
  lines:           1438 (target 1400-1500) ✓ 
``` 
 
### Deliverables in new-skills/ 
 
┌──────────────────────────────────────────┬────────────────┬────────────────────────────────────────────────────────────────────────────────────────┐ 
│ File                                     │ Lines          │ Role                                                                                   │ 
├──────────────────────────────────────────┼────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤ 
│ unified-v3_SKILL.md                      │ 1438           │ Lineage Master v3.0.0 — canonical from 2026-08-31                                      │ 
├──────────────────────────────────────────┼────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤ 
│ UNIFIED-V3-PLAN.md                       │ 310            │ Reproducible A–F merge strategy + Q1–Q5 decisions                                      │ 
├──────────────────────────────────────────┼────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤ 
│ VERIFICATION-UNIFIED-V3.md               │ —              │ rg proofs + defect→fix table + suggested commit                                        │ 
├──────────────────────────────────────────┼────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤ 
│ CRITICAL-COMPARISON.md                   │ 310            │ 12-axis scored review of the 3 sources (Risen 59/60 · St Mary 53/60 · St Joseph 42/60) │ 
├──────────────────────────────────────────┼────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤ 
│ draft_unified-v3_SKILL.md                │ 254            │ Strategy memo — diagnosis preserved, 254-line document discarded                       │ 
├──────────────────────────────────────────┼────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤ 
│ risen-christ / st-mary / rothershrine-v2 │ 1427/1393/1337 │ Frozen profiles — P-01→P-04 back-ported, do not edit independently                     │ 
└──────────────────────────────────────────┴────────────────┴────────────────────────────────────────────────────────────────────────────────────────┘ 

