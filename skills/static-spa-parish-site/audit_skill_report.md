# Meticulous Review Plan — The SKILL Revision Family (5 documents, 3 SKILL generations)

**Request:** Meticulously plan to review and analyze the attached versions/revisions of the SKILL file; critically compare them.
**Mode:** C (Audit/Review) — planning stage. Read-only discipline: no SKILL file is edited until a report is delivered and a fix pass is separately approved.
**Method:** Meticulous Approach — ANALYZE → PLAN → VALIDATE → IMPLEMENT → VERIFY → DELIVER (house convention per `UNIFIED-V3-PLAN.md` / `REVIEW-PLAN-SKILL-vs-unified-v3.md`).

---

## 1. Executive Summary & Go/No-Go

**One sentence:** The attached set is not two documents but a *lineage of competing single-source-of-truth claims* — `rothershrine-v2_SKILL.md` (hop-1 fossil, v1.3.0), `unified-v3_SKILL.md` (Lineage Master v3.0.0, 2026-08-31), and `SKILL.md` (unified v3.0.0 + `package_version: 1.4.4`, 2026-09-01, claiming supersession via its §0 Volatile Facts Register + Appendix G ledger) — plus the two planning documents that record what each was *supposed* to deliver; the review must therefore audit (a) each document against itself, (b) each against the others, (c) each against its own plan, and (d) — the sharpest test — whether `SKILL.md`, the document whose entire thesis is "every restatement is a future fossil," carries any uncatalogued fossils of its own.

**Go/No-Go: GO.** A close read has already surfaced **34 candidate findings** (Appendix A), of which **2 are High-severity internal contradictions inside `SKILL.md`'s own §0 register** (S-1: "hours 6 keys" vs the 7 keys in its verbatim `site.ts`; S-2: "mass 11 keys" vs the 9 keys in the same verbatim block) — meaning the audit-of-the-auditor axis is not optional decoration; it is where the verdict will be decided.

**Recommendation preview (to be confirmed or overturned by evidence):** Promote `SKILL.md` as canonical **conditionally** — contingent on fixing its §0 register errors (a single source of truth with wrong numbers *in the register* violates its own ADR-7 contract more severely than any fossil it catalogs) — and freeze `unified-v3_SKILL.md` as the lineage-superset profile, `rothershrine-v2_SKILL.md` as the origin snapshot.

**Environment caveat (Section 13 honesty):** This environment has no repo and no shell. All repo-state claims (`src/index.css` byte counts, test greens, `wc -l`) are **Unverifiable** here; document-internal claims below are **Verified at text level** (I read the attached content) or **Reasoned**. The `rg`/`wc`/`diff` gate in §3.2 is written to be executed in IMPLEMENT — by me if execution becomes available, otherwise handed to you as exact commands.

---

## 2. Phase 1 — ANALYZE: What Each Document Is & The Central Conflict

### 2.1 Inventory

| # | File | Role | Identity / version | Date | Claimed state |
|---|---|---|---|---|---|
| 1 | `SKILL.md` | **Candidate canonical** — "stop the lineage docs from fossilizing again" | `static-spa-parish-site` v3.0.0 (doc axis) + `package_version: 1.4.4` (repo axis) | 2026-09-01 | §0 register + Appendix G (26 findings) + fossil-sweep protocol; 25+2 tokens |
| 2 | `unified-v3_SKILL.md` | **Incumbent** — Lineage Master governing all 4 hops | `singapore-parish-lineage` v3.0.0 | 2026-08-31 | `~`-shorthand machine-asserted counts; 26+2 token superset; parameterized Appendix B |
| 3 | `rothershrine-v2_SKILL.md` | **Ancestor / frozen origin snapshot** (redirect stub) | `st-joseph-bt` v1.3.0 | 2026-08-29 | 24+2 tokens; 16/92 + 35 E2E era; `#mandarin` anchor era |
| 4 | `UNIFIED-V3-PLAN.md` | **Intent baseline** for #2 (decisions A–F, Q1–Q5) | — | 2026-08-31 | Promised ~1400–1500 lines, 3-hook §6, full tree, parameterized smoke |
| 5 | `REVIEW-PLAN-SKILL-vs-unified-v3.md` | **Pending plan** comparing #1 vs #2 (9-axis) | — | 2026-09-01 | Recommends single-canonical, bless 25+2, 27-utility convention, report-only |

**Not attached but referenced as ground-truth baseline:** `risen-christ_SKILL.md`, `st-mary-of-angels_SKILL.md`. See Q1 (§4).

### 2.2 Genealogy & the three competing truth-claims

```
rothershrine-v2 (hop 1, 2026-08-29)          UNIFIED-V3-PLAN (intent)
        │  (st-mary hop — file not attached)          │
        ▼                                               ▼
unified-v3_SKILL.md (2026-08-31)  ◄── built per plan; claims to govern all hops
        │
        ▼  (one day later; claims unified-v3's approach is the weaker countermeasure)
SKILL.md (2026-09-01) + REVIEW-PLAN (same day, written to judge SKILL.md vs unified-v3 — never executed)
```

The central conflict: **both #1 and #2 declare themselves the single source of truth** (`SKILL.md` "How to use": *"the single-source-of-truth for any future agent…"*; `unified-v3` file-name note: *"governs all hops… all future architectural updates go here"*). Two live cannons pointing at the same parish. The review's job is to pick one on evidence and freeze the other with an explicit role.

### 2.3 The three audit layers (why this plan extends the existing REVIEW-PLAN)

| Layer | Question | Existing coverage | This plan adds |
|---|---|---|---|
| L1 — Cross-document | Which file is canonical; what regressed vs survived across generations | REVIEW-PLAN V1–V9 (two files) | Ancestor axis (#3), trajectory matrix, plan-fidelity axis |
| L2 — Self-consistency | Does each file contradict itself? | Partial (SKILL App G catalogs #2/#3 fossils) | Full fossil inventory for all 3, **including SKILL.md itself** (axis V11) |
| L3 — Plan-vs-deliverable | Did each file deliver what its plan promised? | None | Axis V10: `UNIFIED-V3-PLAN` → `unified-v3`; `REVIEW-PLAN` recommendations → `SKILL.md`; plus errors *inside* the plans (P-1, P-2) |

### 2.4 Headline pre-read observations (seeds for Appendix A; confidence labeled)

1. **`SKILL.md`'s §0 register contains at least two wrong counts** — `hours 6 keys` and `mass 11 keys` — while its own §20.3 "verbatim" `site.ts` shows **7 hours keys** and **9 mass keys**. Verified at text level. Root-cause hypothesis for `6`: the hop-3 diff computed St Mary `7 − columbarium = 6`, forgetting `mediaCentre` was a *replacement* (+1), not a removal. `mass 11` has no document-internal derivation — repo check needed to adjudicate which side is right.
2. **`SKILL.md`'s sum-verified counts actually verify**: the 35-term unit-test breakdown sums to exactly 202 (I re-summed it), and the 8 E2E specs sum to 51. Verified (arithmetic).
3. **`unified-v3` still carries ~15 of the 26 fossils SKILL.md's Appendix G claims to have fixed** — including `§6 "Two hooks"` while its own test list has `hooks/useScrollSpy (6)`, `§10 "32 files / 184 tests"`, the missing `z-[60]` row, the duplicated `// src/components/SafeImage.tsx` comment, and Appendix F's round-7-era `1.3.0 / 32-179+48`. All Verified at text level.
4. **`REVIEW-PLAN` itself contains a factual error**: its Appendix A #10 claims unified-v3's §18 has the `z-[60]` row ("Parity — both fixed") — unified-v3's §18 has no such row. It also calls §0 a "16 rows" register; the actual table has 19 rows. Verified at text level.
5. **`rothershrine-v2` is correctly frozen** (redirect-stub note present) but carries the triple-version conflict (1.3.0 frontmatter / 1.1.0 §2 / 1.0.0 Appendix D) and three generations of test counts in one §11 — both already cataloged by G (#1, #16, #17).

---

## 3. Phase 2 — PLAN: 11-Axis Comparative Review & Methods

### 3.1 Axis matrix

Axes V1–V9 extend REVIEW-PLAN's nine axes to the full three-generation set; V10–V11 are new.

| Axis | Tests | Method | Pass criterion | Severity |
|---|---|---|---|---|
| **V1 — Identity & versioning** | name/version axes across all 3; triple-version fossil in #3; doc/repo axis split in #1 | `rg "^name:|^version:|^package_version:|^display_name:"` all files; `head -30` each | #3's 1.3.0/1.1.0/1.0.0 conflict confirmed & cataloged; #1's split resolves it (App G #1); #2's single axis explained | Critical |
| **V2 — Structural completeness** | Heading counts, TOC integrity, §0 presence, skeleton preservation (§§1–20 + appendices) | `rg -n "^## |^# " \| wc -l` per file; `diff` heading lists pairwise | #1: §0 + A–G + QR, nothing from #2's contract lost; #2: §§1–20 + A–F; #3: §§1–20 + A–D; no silent section deletion | Critical |
| **V3 — Token & style contracts** | 24+2 → 26+2 → 25+2 trajectory; utility/keyframe register completeness vs claimed counts | `sed -n '/@theme/,/^ }/p'` each file \| `rg -c "color-shrine-"`; count §4.3 table rows; `rg "drawer-item-in|page-in|card-tint|img-zoom|bg-gold-bloom"` | #1: 25 colors/27 utilities/8 keyframes all enumerated & counts agree with §0; #2: 26+2 superset internally consistent **and** §4.3 table reconciled vs its "28 utilities / 8 keyframes" claim (currently fails: 6 keyframes listed); #3: 24+2 era-correct | High |
| **V4 — Volatile-facts discipline** (central) | §0 single-source vs restatement; every restated count agrees with §0; every count summed | Build the **count-trajectory matrix** (§3.3); `rg -n "202 tests|35 files|51 E2E|397\.52|77 files|11 keys|6 keys"` all files; arithmetic re-sum of every breakdown | #1: all restatements agree with §0 (S-1/S-2 currently fail); #2: `~`-shorthand + prose restatements quantified; #3: three count generations mapped, not fixed | Critical |
| **V5 — Parish fidelity & leak classification** | Predecessor facts (Oklahoma/Tepeyac, 620 Upper BT, Bukit Batok, `#mandarin`, T08CC4043C/4053H, 4 OFM) outside lineage appendices | `rg -n "Oklahoma|Tepeyac|620 Upper|Bukit Batok|#mandarin|T08CC4053H|T08CC4043C|4 OFM"` each file, **classified by section** | Zero leaks outside §1-lineage/Appendices D/E/F/G in #1; #2's Parish-X template rows scored as intentional parameterization, not leaks; #3 era-correct throughout | High |
| **V6 — Config & contract completeness** | vite test block, `server.watch.ignored`, `playwright.built`, tsconfig 5-entry include, CSP, `src.orig` policy, ssh-key advisory | `rg -n "playwright\.built|server\.watch\.ignored|img-src|repo-hygiene|src\.orig"` + read §3.2 tables | All 3 agree on immutable config; **#2's CSP self-contradiction adjudicated** (§3.2 "no wikimedia/pexels allowlist" vs §5.5/§9#13 "legacy allowlist retained"); #2's 4-entry include fossil (§10/§13) flagged | High |
| **V7 — Audit-ledger depth & accuracy** | Each of G's 26 findings: (a) exists in the named source? (b) resolved in SKILL.md body? | Re-verify every G row against the attached texts; `rg "Appendix G|Fossil-Sweep|ADR-7|ADR-8|L13|L14|L15"` | All 26 findings reproducible in the attached sources where the source is attached (#1/#2/#3); every claimed resolution present in #1's body; findings G missed are logged as new (U-14, S-1…S-3 candidates) | High |
| **V8 — Migration appendices & `as of` discipline** | D/E/F labeling; historical snapshots dated; F corrected vs round-7-era | Read appendices pairwise; `rg "as of"` #1 vs #2 | #1: every historical number carries `as of <date>`; #2: F's `1.3.0` / `32-179+48` / St-Mary-`24+2` fossils confirmed (App F St Mary tokens should be 26+2 at round 7) | Medium |
| **V9 — Lineage invariants** | Immutable contracts preserved across all 3 generations | `rg -n "17 Route|5 alias|HashRouter|singlefile|twMerge\(clsx|resolveAnchor|preventDefault"` all files | Identical: HashRouter, singlefile, 17/5/7 route contract, `cn()`, SkipLink hash discipline, Button discriminated union, double-hash `resolveAnchor`; any regression = FAIL | Critical |
| **V10 — Plan-vs-deliverable fidelity** (new) | Did #2 deliver `UNIFIED-V3-PLAN` decisions A–F & §3.2 promises? Did #1 embody REVIEW-PLAN's A1–A4? Do the plans contain errors? | Read plan promise tables against delivered text | Key failures already visible: plan promised 3-hook §6 → delivered "Two hooks" (D-1); full tree → 3 files missing (D-2); App E fossil replacement → still `16/92+35` (D-3). REVIEW-PLAN errors P-1/P-2 logged | High |
| **V11 — Auditor self-consistency** (new) | Apply G.4 fossil-sweep protocol *to SKILL.md itself* | Run §3.2 block G; re-sum every §0 number; reconcile §0 ↔ §20.3 verbatim blocks | §0 has zero internally-contradicted rows. Currently fails S-1 (hours 6≠7) and S-2 (mass 11≠9) | Critical |

### 3.2 Reproducible command gate (executed in IMPLEMENT; outputs pasted verbatim into the report)

```bash
# — Block V1: identity & versions
rg -n "^name:|^display_name:|^version:|^package_version:|^last_updated:" SKILL.md unified-v3_SKILL.md rothershrine-v2_SKILL.md
rg -n "package.json. version is" SKILL.md unified-v3_SKILL.md rothershrine-v2_SKILL.md
wc -l SKILL.md unified-v3_SKILL.md rothershrine-v2_SKILL.md REVIEW-PLAN-SKILL-vs-unified-v3.md UNIFIED-V3-PLAN.md

# — Block V2: structure
rg -n "^## |^# " SKILL.md unified-v3_SKILL.md rothershrine-v2_SKILL.md | wc -l
diff <(rg -n "^## " SKILL.md | sed 's/^[0-9]*://') <(rg -n "^## " unified-v3_SKILL.md | sed 's/^[0-9]*://') | head -60

# — Block V3: tokens & utilities
for f in SKILL.md unified-v3_SKILL.md rothershrine-v2_SKILL.md; do
  echo "== $f"; sed -n '/@theme {/,/^ }/p' "$f" | rg -c -- "--color-shrine-"; done   # expect 25 / 26 / 24
rg -n "gold-700|terracotta-600" SKILL.md unified-v3_SKILL.md | head -20
rg -n "drawer-item-in|page-in|card-tint|img-zoom|bg-gold-bloom" unified-v3_SKILL.md  # expect: absent from §4.3 table
rg -c "^\| [0-9]+ \|" SKILL.md   # §4.3 numbered rows → expect 27

# — Block V4: volatile facts
rg -n "hours 6 keys|mass 11 keys" SKILL.md unified-v3_SKILL.md
rg -n "32 files / 184|25 files/142|25 files / 141|16 files / 92|11 files / 67|9/53" SKILL.md unified-v3_SKILL.md rothershrine-v2_SKILL.md
rg -n "see §0|§0\)" SKILL.md | wc -l

# — Block V5: leaks (classify each hit by section)
rg -n "Oklahoma|Tepeyac|620 Upper Bukit Timah|Bukit Batok|#mandarin|T08CC4053H|T08CC4043C|4 OFM|Portiuncula" SKILL.md | head -30

# — Block V6: config
rg -n "img-src|wikimedia|pexels" unified-v3_SKILL.md | head -20   # expose the CSP self-contradiction
rg -n 'include .*playwright\.built' unified-v3_SKILL.md SKILL.md

# — Block V7/V11: ledger & self-audit
rg -n "Two hooks|Three hooks" SKILL.md unified-v3_SKILL.md rothershrine-v2_SKILL.md
rg -n "z-\[60\]" SKILL.md unified-v3_SKILL.md rothershrine-v2_SKILL.md
rg -n "SafeImage.tsx// src" unified-v3_SKILL.md                    # duplicated comment fossil
rg -n "fetchPriority" unified-v3_SKILL.md SKILL.md
```

### 3.3 Count-trajectory matrix (review artifact, filled in IMPLEMENT)

One row per volatile fact, one column per document-generation — the visualization of the "restated 5–8×" root cause:

| Fact | rothershrine-v2 (hop 1) | unified-v3 (master) | SKILL.md (v3) | Verdict |
|---|---|---|---|---|
| package version | 1.3.0 / 1.1.0 / 1.0.0 (×3!) | 3.0.0 (+ Risen ref 1.4.4) | doc 3.0.0 + repo 1.4.4 | … |
| Unit tests | 16/92 ↔ 11/67 ↔ 9/53 | ~35/202 (+ §10 fossil 32/184; App C 25/142) | 35/202 (§0; sum-verified) | … |
| E2E | 35 ↔ 27 ↔ 22 | 51 | 51 ×2 passes | … |
| src files | 45 ↔ 52 | 77 (41+35+1) | 77 (§0) | … |
| Tokens | 24+2 | 26+2 superset | 25+2 byte-truth claim | CONCERN-by-design |
| hours keys | 5 (bookshop era) | "6" (enumerates 7) | "6" (verbatim shows 7) | **S-1/U fossil** |
| mass keys | 7 | (7 fossil in §5.2) | "11" (verbatim shows 9) | **S-2 — adjudicate vs repo** |
| Hooks | "Two" (tree: 1 file) | "Two" (harness proves 3) | Three ✓ | … |

### 3.4 Manual spot-checks (checkbox list for IMPLEMENT)

- [ ] §0 in SKILL.md: every row's number matches its "Where else referenced" occurrences (grep each value)
- [ ] §0 vs §20.3: `hours`/`mass` key counts reconciled against the verbatim object (S-1/S-2)
- [ ] §4.3 registers: 27 utility rows + 8 named keyframes in SKILL.md; count unified-v3's actual rows vs its "28/8" claim
- [ ] §18 z-index: `z-[60]` rail row present in SKILL.md only (contra REVIEW-PLAN App A #10)
- [ ] Appendix B: SKILL.md's 19-step script is Risen-filled with zero St Mary values; unified-v3's Parish-X rows scored as intentional template
- [ ] G ledger: each of findings #1–26 re-verified against attached sources; unattached sources (`st-mary`, `risen-christ`) marked Unverifiable
- [ ] G.4 protocol executed against SKILL.md itself (the auditor audited)
- [ ] Alias/anchor contracts byte-identical: 7 aliases / 5 groups / 9 anchors; `#language-communities` (SKILL/unified) vs `#mandarin` (rothershrine — era-correct)
- [ ] Freeze discipline: rothershrine stub note intact; no instruction in any file to edit stubs independently

### 3.5 Success criteria

| Criterion | Gate |
|---|---|
| All 11 axes scored PASS / CONCERN-with-rationale / FAIL with `rg` citations | No Critical/High FAIL left unaddressed or mislabeled |
| Count-trajectory matrix complete (every volatile fact, all 3 generations) | No cell "unknown" without a stated reason |
| Every Appendix A candidate finding confirmed, refuted, or reclassified | Zero orphan hypotheses |
| Canonical verdict states PROMOTE / FREEZE roles with explicit blockers | No ambiguous recommendation |
| Repo-dependent claims labeled Unverifiable with the exact command that would verify them | No "works/green" claims without evidence |

---

## 4. Phase 3 — VALIDATE: Confirmation Gate

Reply with one of:

| Option | Triggers |
|---|---|
| **`approve plan as-is`** | I run the 11-axis review immediately → `REVIEW-REPORT-SKILL-REVISIONS.md` → VERIFY self-check → handoff. No edits to any SKILL file. |
| **`approve with scope tweak`** | Specify A1–A5 below; I revise and re-issue. |
| **`expand to fix pass`** | Report first, then a second plan for surgical fixes (only for confirmed FAILs — starting with S-1/S-2 in SKILL.md's §0). Two-phase approval preserved. |

**Open questions:**

| # | Question | My recommendation |
|---|---|---|
| Q1 | Attach `risen-christ_SKILL.md` + `st-mary-of-angels_SKILL.md`? REVIEW-PLAN uses risen-christ as byte-level ground truth; without them, V9's baseline degrades to "SKILL.md's claims about its sources" (Reasoned, not Verified). | Attach if available; otherwise proceed with the 3 attached generations and label baseline checks accordingly. |
| Q2 | Canonical decision timing: pre-commit to SKILL.md, or evidence-first? | Evidence-first — but note S-1/S-2: if confirmed, SKILL.md wins the architecture argument while needing a same-commit §0 fix before promotion. |
| Q3 | Token verdict: bless 25+2 (byte-truth) vs 26+2 (lineage superset)? | 25+2 canonical + 26+2 documented as the future-port option (SKILL.md's own lineage-note mechanism) — pending `grep shrine- src/index.css` on the repo. |
| Q4 | Are the two planning documents audit targets or just context? | Targets — P-1/P-2 prove they carry factual errors that would mis-execute the review (REVIEW-PLAN App A #10 already contradicts unified-v3's actual §18). |
| Q5 | Fix policy if FAILs are found? | Report-only in this pass (matches REVIEW-PLAN A4 and Mode C scope discipline). |

---

## 5. Phase 4 — IMPLEMENT: How the Review Will Run (after approval)

1. Execute command gate §3.2 — capture stdout verbatim (or hand you the exact commands if no runner is available; nothing is asserted green without output).
2. Read all five files front-to-back (offset reads; no truncation — the G ledger and Appendix F live at the tail).
3. Score V1–V11; fill the count-trajectory matrix (§3.3).
4. Confirm/refute all 34 Appendix A candidate findings; classify V5 leaks by section.
5. Diff the immutable contracts (V9): §4 `@theme`, §5.4 routing, §9 anti-patterns, §15 patterns across the 3 generations.
6. Adjudicate the two intentional divergences (25+2 vs 26+2; 27 vs 28 utilities) as CONCERN-with-rationale, not FAIL.
7. Draft the report. **No edits to any SKILL file, plan file, or appendix.**

---

## 6. Phase 5 — VERIFY: Iron Law

- [ ] Every axis has a verdict + evidence citation + severity + which file is ahead.
- [ ] Every Appendix A finding resolved: Confirmed / Refuted / Reclassified.
- [ ] Command outputs pasted verbatim (or exact commands handed off with the reason).
- [ ] No edit made to any of the 5 files.
- [ ] Report states canonical/freeze roles with explicit blockers.
- [ ] Repo-dependent claims labeled Unverifiable; arithmetic claims labeled Verified.

---

## 7. Phase 6 — DELIVER: Report & Recommendation

| Deliverable | Path | Content |
|---|---|---|
| Comparative report | `REVIEW-REPORT-SKILL-REVISIONS.md` | 11-axis scoring; count-trajectory matrix; confirmed fossil inventory (per file, severity-ordered); head-to-head deltas; canonical verdict + blockers |
| Evidence appendix | inside the report | Verbatim `rg`/`wc`/`diff` outputs |
| Fix plan (only if `expand to fix pass`) | separate approval | Surgical: §0 corrections (S-1/S-2), unified-v3 fossil list, REVIEW-PLAN App A #10 correction |

Suggested commits (docs-only):
```
docs(plan): add REVIEW-PLAN-SKILL-REVISIONS.md — 11-axis family audit plan
docs(review): 11-axis audit of SKILL revisions — <verdict: promote X / freeze Y>
```

---

## 8. Appendix A — Candidate Findings Inventory (pre-read; to confirm/refute in IMPLEMENT)

Severity per Section 12 taxonomy. Confidence: **V** = Verified at text level (read in attachment), **P** = pending command execution.

### A.1 Against `unified-v3_SKILL.md` (mostly pre-cataloged by SKILL.md App G — the review verifies both fossil and claimed resolution)

| # | Location | Finding | Sev | G# | Conf |
|---|---|---|---|---|---|
| U-1 | §6 | "Status: **Two hooks**" while §2/§11 list `hooks/useScrollSpy (6 tests)` and Quick Ref lists 3 hooks | High | 25 | V |
| U-2 | §5.2 tree | Missing `hooks/useScrollSpy.ts`, `utils/monogram.ts`, `utils/deepLinks.ts` despite test list naming them | High | 25 | V |
| U-3 | §10 | "should be **32 files / 184 tests**" vs 35/202 everywhere else | High | 4 | V |
| U-4 | §18 | No `z-[60]` ScrollProgress row, though §5.2/§5.5 specify it; conflict rule ignores the rail | Med | 24 | V |
| U-5 | §20.3 | Duplicated `// src/components/SafeImage.tsx` comment; `SafeImageProps` lacks `fetchPriority` that §5.5 documents | Med | 18/19 | V |
| U-6 | App C | "harness is green (**25 files/142 + 48 E2E**)" vs 35/202+51 | Med | 14 | V |
| U-7 | App F | Round-7-era snapshot: package **1.3.0**, **32/179+48** tests, and St Mary tokens "**24+2**" (St Mary round-7 was 26+2) | Med | 15 (+new) | V |
| U-8 | §13 | "`src.orig/` … inert guards" vs §2/Quick Ref (pruned round-12 + `repo-hygiene` guard) | High | 5 | V |
| U-9 | §14 | `skills/` "live only in git history at `c774ed9`" vs §2 (re-added in full, `0be0fe8`) | Med | 5 | V |
| U-10 | §4.3 | Keyframes prose lists **6** vs "8" claim; utility table lacks `drawer-item-in`/`page-in`/`card-tint`/`img-zoom`/`bg-gold-bloom` vs its own 27+8 claim | High | 22/23 | V |
| U-11 | §5.2 comments | "images export (11 keys, **3 CDN**)", "hours(**5**)", "mass(**7**)" vs §7 (all-local, 7 hours keys, 9+ mass keys) | Med | 20 | V |
| U-12 | §12 L9/L10 | CDN-era "CSP extended to upload.wikimedia.org"; "Rewritten to Bukit Batok St Mary … 35 green (2026-08-28)" | Low | 10/21 | V |
| U-13 | §3.2 vs §5.5/§9#13 | CSP self-contradiction: "no wikimedia/pexels allowlist" vs "legacy allowlist retained" | Med | 9-part | V |
| U-14 | §10/§13 | tsconfig include lists **4 entries** vs §3.2's 5 (missing `playwright.built.config.ts`) | Low | new | V |
| U-15 | App D.4 | "Do not delete it" vs Quick Ref "removed from tree + index" | Med | 13 | V |

### A.2 Against `rothershrine-v2_SKILL.md` (era fossils; file is a frozen stub — catalog, don't fix)

| # | Location | Finding | Sev | G# | Conf |
|---|---|---|---|---|---|
| R-1 | fm/§2/App D | Triple version: **1.3.0** (fm) / **1.1.0** (§2) / **1.0.0** (App D) | High | 1 | V |
| R-2 | §5.2 | Heading "**45 files** (33+11+1)" vs counts line "**52** (35+16+1)" | Med | 16 | V |
| R-3 | §11 | Three count generations in one section: 11/67+27 → 9/53+22 → 16/92+35; E2E likewise 27↔35↔22 | Med | 17 | V |
| R-4 | §6/§5.2 | "Two hooks" but tree lists only `useScrolled.ts`; `useScrollProgress` proven by test list, absent from tree | Low | 25-analog | V |
| R-5 | §3.2/QR/§4.3 | Utilities "**24**" vs "**22** + 6 keyframes" vs ~17 table rows | Low | 22/23-part | V |
| R-6 | File-name note | Redirect-stub freeze instruction present | PASS | — | V |

### A.3 Against `SKILL.md` — **auditing the auditor** (the decisive set)

| # | Location | Finding | Sev | G# | Conf |
|---|---|---|---|---|---|
| **S-1** | §0 + §1 vs §20.3 | Register says "hours **6 keys**"; §1 enumerates 7 names; §20.3 verbatim `site.ts` defines **7** (`gates, mainChurch, chapel, reception, parishOffice, mediaCentre, adorationRoom`). Hypothesis: hop-3 diff computed 7 − columbarium = 6, forgetting `mediaCentre` was a replacement | **High** | new | V |
| **S-2** | §0 + §7.1 vs §20.3 | Register says "mass **11 keys**"; verbatim `mass` object defines **9** (`weekdayMorning, weekdayEvening, saturday, sunday, confession, adoration, secondCollection, note, monthly`). No document-internal derivation for 11 — repo `site.ts` must adjudicate | **High** | new | V |
| S-3 | §2 heading | "current reality (2026-08-31, **round-6** verified)" vs §0 "as of … **round-12**" | Low | new | V |
| S-4 | §0 sum claims | Unit breakdown sums to exactly 202 (35 terms); E2E 11+8+4+4+7+6+8+3 = 51; §4.1 = 25 colors; §4.3 = 27 rows; §19 = 25 rows | PASS | — | V (arithmetic) |
| S-5 | App G resolutions | All 26 claimed resolutions must be located in SKILL.md body (method step, not a finding) | — | — | P |

### A.4 Against the two plans (audit targets per Q4)

| # | Location | Finding | Sev | Conf |
|---|---|---|---|---|
| P-1 | REVIEW-PLAN App A #10 | Claims unified-v3 §18 "Same row present (post-audit) — Parity"; unified-v3 §18 has **no** `z-[60]` row | Med | V |
| P-2 | REVIEW-PLAN §2.2 | "§0 … (16 rows)"; actual §0 table has **19 rows** (its own parenthetical lists 18) | Low | V |
| P-3 | REVIEW-PLAN §2.1 | Line counts 1590/1438 | — | P (`wc -l`) |
| D-1 | UNIFIED-V3-PLAN §3.2 → unified §6 | Plan promised "3 hooks fences … `useScrollSpy` tie-break"; delivered "**Two hooks**" | High | V |
| D-2 | Plan §3.2 → unified §5.2 | Plan promised complete tree; delivered missing 3 files (U-2) | High | V |
| D-3 | Plan §2.4 C-2 → unified App E | Plan: "replace fossil" `16/92+35`; delivered still carries it (labeled "at time of audit" — adjudicate whether the label suffices) | Med | V |
| D-4 | Plan §3.1 → unified length | Promised 1400–1500 lines | Low | P (`wc -l`) |
| D-5 | Plan decision C → unified practice | `~` machine-asserted shorthand adopted in frontmatter, but exact counts restated throughout §§2/3/11 — weaker discipline than the decision implied | Med | V |

---

## 9. Appendix B — Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Register errors (S-1/S-2) get buried** as "Low count pedantry" because SKILL.md is otherwise superior | High | High — the canonical doc's core contract (§0 infallibility) silently broken | V11 is a Critical axis; verdict makes §0 fix a promotion *blocker*, not a footnote |
| Token count false-FAIL (25 vs 26 flagged as drift) | High | High — blocks a correct promotion | CONCERN-with-rationale classification; `src/index.css` byte count as tie-breaker when repo available |
| Missing baseline files degrade V9 to Reasoned-only | Medium | Medium | Q1: request `risen-christ_SKILL.md` / `st-mary-of-angels_SKILL.md`; else label explicitly |
| No shell/repo in this environment → count claims unverifiable | Certain | Medium | Exact commands in §3.2 handed off; every such claim labeled Unverifiable, never asserted |
| REVIEW-PLAN's errors propagate into execution (P-1) | Medium | Medium | This plan supersedes its deltas; App A #10 explicitly corrected before V3 runs |
| Scope creep into editing during audit | Medium | Medium | Iron law: read-only; fixes gated behind a second approval (`expand to fix pass`) |
| Reviewer fatigue at 3×1500-line corpus | Medium | Low | Count-trajectory matrix + Appendix A inventory focus reading; tails read via offset passes |

