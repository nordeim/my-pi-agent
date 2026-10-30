# Methodology — Full Phase-by-Phase Playbook

Institutional-grade RCA on US big-tech stock price events. Read the section matching your
current phase; sections 12–14 (freshness, pitfalls, compliance) apply throughout.

**Worked example used throughout:** Alphabet (GOOG) Q3 2026 earnings, reported Oct 28 2026,
which produced a −12.29% session on Oct 29 — the worst day since its 2004 IPO, erasing
≈$482B of market value. All figures below are real, verified facts from that analysis.

## Table of contents

1. [Phase 0 — Scope & event definition](#1-phase-0--scope--event-definition)
2. [Phase 1 — Fact-base construction](#2-phase-1--fact-base-construction)
3. [Phase 2 — Quantify the market reaction](#3-phase-2--quantify-the-market-reaction)
4. [Phase 3 — Construct the hypothesis tree](#4-phase-3--construct-the-hypothesis-tree)
5. [Phase 4 — Test & classify hypotheses](#5-phase-4--test--classify-hypotheses)
6. [Phase 5 — Quantify surviving mechanisms](#6-phase-5--quantify-surviving-mechanisms)
7. [Phase 6 — Separate noise from signal](#7-phase-6--separate-noise-from-signal)
8. [Phase 7 — Amplifiers & the overlooked case](#8-phase-7--amplifiers--the-overlooked-case)
9. [Phase 8 — Synthesis & forward frame](#9-phase-8--synthesis--forward-frame)
10. [Phase 9 — Report production workflow](#10-phase-9--report-production-workflow)
11. [Phase 10 — Audit protocol & data freshness](#11-phase-10--audit-protocol--data-freshness)
12. [The fact base in practice](#12-the-fact-base-in-practice)
13. [Full pitfall catalog](#13-full-pitfall-catalog)
14. [Compliance, tone & two-sidedness](#14-compliance-tone--two-sidedness)

---

## 1. Phase 0 — Scope & event definition

Write a one-page **event charter** before touching data. It contains:

- **Trigger**: the event and its exact timestamp ("Q3 FY2026 earnings release + conference call, Oct 28 2026, 16:05 ET release / 17:30 ET call").
- **Subject**: ticker + share class + why that class (GOOG is the more liquid C-share line; GOOGL carries votes — quote both when they diverge materially). Note any split/dividend basis.
- **Reaction definition**: primary reaction = first **full-session close after the event** (T+1 close). After-hours and T+0 intraday are secondary color, always labeled as such. Rationale: after-hours prints are thin and headline writers anchor on them; the close is what clears real size.
- **Observation window**: pre-event baseline (typically −90 trading days for trend, prior close for the move), event day, post-event through the data cutoff.
- **Benchmarks**: S&P 500, Nasdaq-100, and a named peer basket. For mega-cap tech use MSFT, META, AMZN, AAPL, NVDA at minimum; add sector-adjacent names (e.g. TSM, Samsung for semis/hardware exposure) when relevant.
- **Deliverable spec**: audience (institutional PM/IC), format (default 12–16 page HTML deck, 1280×720, Midnight IC system), language, whether speaker notes are wanted, citation style (inline source chips + closing ledger).
- **Data cutoff**: "All prices as of close YYYY-MM-DD; analysis reflects information available through YYYY-MM-DD HH:MM, TZ." This goes on the cover and governs refresh duty (§11).

**Gate:** the charter exists, the ticker class and reaction definition are pinned, and the user's explicit requirements (length, sections, must-include facts) are copied into it verbatim.

---

## 2. Phase 1 — Fact-base construction

The fact base is the report's spine. Every number that appears in the deck must exist here,
with a source. Build it with web search/fetch against the tiers below.

### 2.1 Source tiers — what each source is allowed to support

| Tier | Sources | Allowed to support |
|---|---|---|
| **T1 — Primary** | SEC EDGAR filings (10-Q, 10-K, 8-K); company IR press release / shareholder letter; the earnings-call transcript **as hosted by the company's own IR site** (or audio); official company blogs & product pages | All fundamental figures: revenue, segments, margins, EPS, capex, FCF, guidance language, one-off items, AI/usage metrics |
| **T2 — Named press & verified transcripts** | Reuters, Bloomberg, CNBC, FT, WSJ, AP, Fortune, Barron's; FactSet/LSEG consensus **as reported** by these outlets or by TradingView/MarketBeat; full third-party transcripts (Motley Fool / Seeking Alpha / roic.ai) — treat as T2 **until cross-checked against the IR audio/transcript**, then upgrade the cross-checked figures | Consensus estimates and surprise framing; market-reaction color; analyst actions (rating/PT changes with shop + analyst name); macro prints; transcript quotes once cross-checked |
| **T3 — Data aggregators** | Yahoo Finance, Stooq, Macrotrends, TIKR, CNN Markets, Google Finance | Price history, closes, market cap, 52-week ranges, YTD/1y performance, after-hours prints. **Never** fundamental claims |

Rules:

- Decision-critical numbers (the 5–15 figures the RCA turns on) require **≥2 independent sources**; ideally one T1 + one T2.
- If sources conflict, record **both** values in the fact base with a `conflict` flag and resolve explicitly on the slide ("Reuters says X, transcript says Y — we use the transcript"). Silent picking is forbidden.
- An aggregator may confirm but not originate a fundamental number.
- Store the URL and retrieval timestamp for every source, and verify URLs resolve before delivery.

### 2.2 Price-data hygiene

- **Share class**: GOOG vs GOOGL, BRK.A/B, LEN/LEN.B — quote the class the press quotes for headline comparisons, and say which you used for your own computations.
- **Splits/adjustments**: for trend work use split-adjusted series; for event-day headlines use the raw quoted close. Never mix bases in one table.
- **Market-cap delta**: compute as shares outstanding × Δprice (shares outstanding from the latest 10-Q cover page, T1). If you instead scale the prior market cap by the % move, label the approximation. Example: GOOG shares ≈ 12.1B × (−$39.57) ≈ −$479B ≈ the ≈$482B figure the press reported — agreement between the two methods is itself a cross-check.
- **Ath/drawdown**: verify the all-time-high date and price with a T3 source (e.g. Macrotrends) before using "−X% from ATH".

### 2.3 Consensus & estimates

- Consensus revenue/EPS/segment estimates: take from T2 (Reuters/CNBC/Bloomberg story on the print, or FactSet/Visible Alpha as reported). Record the outlet, not "the Street said".
- For segment-level consensus (e.g. Search $64.9B vs actual $63.4B), cite the specific story or data page; if only the total is available, present segment "short of estimates" qualitatively rather than inventing a number.
- Price targets: shop, analyst name, old PT, new PT, date, source. Consensus PT before/after with analyst count (e.g. FactSet consensus $426.20 → $404.63 across 61 analysts, Oct 29 2026).

### 2.4 Transcript protocol

The call transcript is where the real signal lives. While reading it:

1. Capture exact quotes (speaker + role) for: guidance language, capex outlook, one-off item explanations, the CEO's strongest defense, the CFO's strongest warning. Example: CFO stating on the call that FCF included a $5.2B European Commission fine payment — this single sentence converts a "cash-flow collapse" into a "one-off-adjusted in-line quarter" and must be captured verbatim.
2. Log forward-looking phrases with their hedge words intact ("we expect capex to increase significantly in 2027" — that is guidance, treat as T1 fact about guidance, not a forecast of fact).
3. Note analyst questions that presage the Street's next estimate cycle (they reveal what models are being rebuilt around).

### 2.5 Macro & positioning

- Macro on the day: 10Y yield, latest CPI/PCE prints, Fed stance — each needs a T2/T3 source with date. Example: "10Y ~4.99%, PCE 3.6% (from 3.4%), Fed on hold with hawkish signals, Oct 29 2026."
- Positioning/crowding: pre-event run-up %, index weight, ownership stats — only with a named source (TIKR, 13F filings, ETF factsheets). If you cannot source it, write the qualitative version ("a crowded, record-weight mega-cap") and mark the causal use `Reasoned`.
- Same-week peer prints: log peer event → peer stock reaction as standalone facts (e.g. "META Oct 21: revenue beat $64.6B, FCF −$2.12B, capex floor raised to $135–145B, stock −7%" — T2-sourced). These become amplifier evidence in Phase 7.

**Gate:** every fact the RCA will turn on is in `fact_base.json` with tier, URL, retrieval time; decision-critical numbers are double-sourced; zero numbers from memory.

---

## 3. Phase 2 — Quantify the market reaction

Compute (in code, not by hand) and record as facts:

- **Headline move**: T+1 close vs pre-event close, % and $. Example: GOOG −12.29% to $282.32 (Oct 29 2026) from $321.89.
- **Cross-class check**: quote the other share class with its own sourced print — for the Alphabet example, GOOGL (Class A) closed Oct 28 at $324.89 and printed ≈−12.8% intraday on Oct 29 (Yahoo Finance); its class-A close was not independently pinned, so only the sourced prints are used. Divergence between classes is itself data on which holders flinched — record the class, print time and source for both, and never mix classes in one computation.
- **After-hours**: the AH print ("~−10% to ~$290 per AP") labeled as after-hours, secondary.
- **Market-cap delta**: shares × Δprice (§2.2), cross-checked to press "≈$482B erased".
- **Historical ranking**: "worst day since 2004 IPO", "second-largest one-day market-cap loss ever for a US-listed stock (behind Nvidia, Jan 2025)" — only from T2 sources that state the ranking. If none, drop the ranking.
- **Distance from highs**: ATH close $402.12 (May 13 2026) → −29.8% below; pre-print close was already −20% off the high. The pre-event drawdown context matters: it tells you how much hope was still priced in.
- **Same-day cross-section**: S&P 500 and Nasdaq-100 moves, each peer's move with reason (e.g. "MSFT beat and spiked same evening — rotation within AI, not blanket risk-off", "AMZN −4.3% next day after its own miss"). This cross-section is the single best discriminator between narrative repricing and market-wide de-risking: **target down + peers up = idiosyncratic verdict against the name.**
- **Volume/IV/flows**: include only with a source; otherwise omit entirely.

**Presentation artifact:** a price-ladder or drawdown chart (ATH → pre-print close → post-print close → after-hours), pure CSS where possible (§10).

**Gate:** move quantified in ≥4 independent ways; every ranking claim carries a source; cross-section table complete.

---

## 4. Phase 3 — Construct the hypothesis tree

Enumerate 5–8 competing hypotheses **before** writing any narrative. Use the eight lenses:

| Lens | Question | Alphabet worked example |
|---|---|---|
| (a) Revenue miss | Did top-line miss consensus, and how much? | Revenue $127.57B vs $128.2B (−0.5%) |
| (b) Margin/EPS miss | Did profitability miss on its own basis? | GAAP EPS $2.12 vs $3.02 |
| (c) Segment deterioration | Which franchise broke? | Search $63.4B vs $64.9B (−2.3%) |
| (d) Guidance shock | Explicit cut, or hidden in call language? | Q4 lapping Search acceleration + FX + Cloud margin pressure |
| (e) Capital-allocation regime | Did the investment equation break? | Q3 capex $51.4B; FY26 held $195–205B; 2027 "significant increase"; FCF −$9.1B vs −$3.5B est. |
| (f) Structural narrative | Is a secular threat now evidenced? | AI (Claude/ChatGPT) visibly denting Search monetization |
| (g) Positioning + macro | Was the entry too crowded for any miss? | +46% y/y into print, ATH in May, 10Y ~4.99%, PCE 3.6%, Meta capex scare 7 days prior |
| (h) One-off noise | Is the headline miss mostly non-operating? | −$8.2B unrealized SpaceX markdown inside OI&E; $5.2B EU fine inside FCF |

For each hypothesis write a **card**:

```
H2 — Capex/FCF regime break
Statement     : The market repriced the AI investment equation; capex has no visible
                ceiling and FCF turned structurally negative.
Mechanism     : negative FCF + open-ended capex guide → DCF terminal-year fear →
                multiple compression on the whole complex.
Predictions   : P1 FCF misses consensus badly (≤ −$5B).
                P2 capex guide ≥ prior FY guide, with 2027 escalation language.
                P3 CFO/CED tone on the call defensive on spend.
                P4 peer with same profile (META) traded the same way last week.
Evidence FOR  : (see fact_base H2-*)   Evidence AGAINST: (see fact_base H2-*)
Verdict       : PRIMARY — mechanical        Confidence: High
```

Rules:

- Predictions must be **falsifiable and checkable** against the fact base. A hypothesis that cannot lose is not a hypothesis.
- Cover all lenses even if some feel unlikely — the excluded lens is often where the honest "market got it wrong" finding lives (that is how Cloud demand failure gets excluded when Cloud grew +103%).
- Expect **coexistence**: big moves usually have one narrative driver + one mechanical driver + amplifiers. The tree exists to allocate weight between them, not to crown a single winner.

**Gate:** 5–8 hypothesis cards, all eight lenses touched, every card has ≥3 falsifiable predictions.

---

## 5. Phase 4 — Test & classify hypotheses

For each hypothesis, assemble evidence FOR and AGAINST from the fact base. Standards:

- ≥2 items per side where the fact base allows; each item carries its source tier.
- Distinguish evidence classes: **what the numbers did** (verified P&L/cash-flow facts) vs **what the market said** (call language, analyst notes, press framing). Both are legitimate, but a verdict must rest primarily on the first.
- Test predictions explicitly: "P1 confirmed (FCF −$9.1B ≤ −$5B). P2 confirmed (2027 escalation language). P3 not tested — no direct quote found."

Verdict taxonomy (mutually exclusive):

| Verdict | Meaning |
|---|---|
| `PRIMARY — narrative` | The belief change that carried the repricing (the story the market now tells) |
| `PRIMARY — mechanical` | The arithmetic driver (cash-flow, multiple, index-flow math) |
| `CONTRIBUTOR` | Real, additively negative/positive, but not sufficient alone |
| `AMPLIFIER` | Explains depth/velocity, not direction or trigger (positioning, macro tape) |
| `NOISE` | One-off, non-cash, or non-recurring; excluded from the organic read |
| `EXCLUDED` | Falsified by the evidence — say so with the falsifying fact |

Rules:

- At least one hypothesis must end `EXCLUDED` with the falsifying fact named. This is the discipline that separates RCA from confirmation-seeking. (Worked example: H6 "Cloud demand failure" excluded — Cloud revenue $30.7B, +103% y/y; operating margin 36.2% vs 23.7%; backlog $561B with ~55% converting within 24 months.)
- A verdict with no `AGAINST` evidence is suspect; go find the strongest bull counter-argument and test again (Phase 7 exists partly for this).
- Confidence per verdict: `High` (verified facts, mechanism tight), `Medium` (direction clear, magnitude uncertain), `Low` (inference on inference — avoid publishing these).

**Gate:** every hypothesis has a verdict with ≥2 cited evidence items; ≥1 excluded; narrative vs mechanical drivers separated.

---

## 6. Phase 5 — Quantify surviving mechanisms

For each surviving hypothesis, attach the 2–4 numbers that carry it, plus one mechanism chart or table where useful.

Templates by driver type:

- **Capex/FCF regime**: Q3 capex ($51.4B, ~40% of quarterly revenue); FY guide vs prior ($195–205B, unchanged); next-year signal ("significant increase" in 2027); FCF actual vs consensus (−$9.1B vs −$3.5B); TTM context (TTM FCF $19.7B vs TTM operating cash flow $179.6B — the gap **is** the capex bill).
- **Narrative/structural**: segment growth trend (Search +12% y/y — decelerating, not declining); usage-vs-monetization gap metrics (1B AI users, queries at 5-year high, AI Mode queries 3× longer); sell-side de-rating math (BofA valuing Search at ~10x earnings vs 18.7x for the S&P 500).
- **Guidance**: what changed in Street models (Q4 lapping, FX headwind, Cloud margin drag) → the estimate-cut cycle that follows.
- **Optics/one-off**: GAAP vs adjusted EPS bridge (Phase 6).

**Valuation decomposition** — attribute the move between estimates and multiple:

```
P₀ = E₀ × M₀   →   P₁ = E₁ × M₁
ΔP ≈ ΔE × M₀ + E₁ × ΔM
```

State plainly which term did the work. Example pattern: if consensus EPS barely moved in the
days after the print while the stock fell 12%, the move was almost entirely multiple
compression — expectations were cut by price first, estimates second ("consensus PT fell
~5.1% while the stock fell ~12.3% — the market now trades ahead of published Street marks").

**Street response ledger**: every named action (Citizens JMP downgrade Oct 29; Wedbush PT $445→$387; FactSet consensus $426.20→$404.63) with source and date; the stock-vs-PT gap is itself a finding.

**Gate:** each surviving mechanism has its carrying numbers; the estimate-cut vs multiple-compression attribution is stated; Street ledger complete.

---

## 7. Phase 6 — Separate noise from signal

The most common RCA failure is explaining the wrong miss. Procedure:

1. Build the GAAP↔adjusted bridge for every headline line. Inventory one-offs:
   unrealized gains/losses on equity stakes (mark-to-market of holdings like SpaceX), regulatory fines (accrued **and** cash-paid), restructuring charges, legal reserves, discrete tax items, FX.
2. Recompute organic figures, arithmetic on the slide:
   - Example A (EPS): GAAP EPS $2.12 vs $3.02 consensus — but OI&E was −$8.2B, primarily an **unrealized, non-cash** SpaceX markdown; operating income actually rose +30% y/y to $40.6B (31.8% margin). Adjusted EPS $2.67 — still short, so the miss is real but far smaller than −30%.
   - Example B (FCF): headline FCF −$9.1B vs −$3.5B expected; per the CFO on the call it included the **$5.2B EU fine payment** → ex-fine ≈ −$3.9B, roughly in line with the Street. The "clean" miss is narrower than the headline.
3. Determine the **consensus basis**: state which number the market actually trades on (usually the adjusted/consensus basis) and re-express the miss on that basis. "−12% on a −0.5% revenue miss" is the sentence that launches the whole RCA.
4. Label recomputed figures `Reasoned (derived)` with the formula. Never let an ex-item figure masquerade as a reported one.
5. Keep the noise verdict honest in both directions: one-offs explain the *headline gap*, but if the adjusted number still missed, say so — noise-stripping must not become spin.

**Gate:** bridge table shown on a slide; headline miss restated on comparable basis; ex-item arithmetic visible.

---

## 8. Phase 7 — Amplifiers & the overlooked case

### 8.1 Amplifier layer

Amplifiers explain **depth, never trigger**. Checklist:

- **Entry positioning**: run-up into the event (+46% y/y; +65% in the prior year; ATH in May), index weight/passive flow exposure, valuation percentile if sourced.
- **Macro tape on the day**: 10Y (~4.99%), inflation prints (PCE 3.6% re-acceleration), Fed path (hawkish hold), risk proxies (Bitcoin −4%, crude on geopolitical tension).
- **Sector tape / priming events**: same-week peer prints that pre-loaded the anxiety (META's negative FCF and −7% seven days earlier), same-night peers (MSFT beat and **spiked** — flows rotated within AI rather than leaving it; that asymmetry is evidence of name-specific repricing), next-day follow-ons (AMZN −4.3% on its own miss).
- Attribution discipline: write amplifier claims with direction confidence and magnitude humility — "High on direction, Medium on magnitude" is an acceptable on-slide confidence statement.

### 8.2 The overlooked case (counter-evidence page)

Dedicate one page to the 2–4 strongest **verified** datapoints the move ignored. Alphabet
example: Cloud $30.7B +103% y/y with operating income $11.1B (36.2% margin) and $561B
backlog; TPU external sales; operating income +30%; AI usage metrics. Frame it as "what the
market may be underweighting" — never as a prediction or a rebuke. This page is what makes
an IC trust the rest of the analysis.

**Gate:** amplifier list complete with sources; counter-case page drafted from verified facts only.

---

## 9. Phase 8 — Synthesis & forward frame

- **One-sentence root cause**, template: *"The market repriced [mechanism] when [evidence 1] arrived in the same print as [evidence 2]."* Worked example: *"the market repriced the AI investment equation — evidence that AI is denting the highest-margin revenue pool arrived in the same print as confirmation that defending it keeps getting more expensive."* If you cannot write this sentence, return to Phase 4.
- **Ranked driver table**: ordinal ranks only. Publish a percentage attribution **only if** it is computable from sourced data; otherwise write "attribution is qualitative". Fake precision is worse than admitted ambiguity.
- **Scenario table** (bull/base/bear): each scenario = narrative + 2–3 quantifiable conditions + the signposts that would confirm/refute it. Explicitly label scenarios as analytic frames, **not price targets**. Example watch conditions: "Q4 Search growth ≥ +12% y/y", "2027 capex guided ≥$230B", "sequential Search deceleration below +8%".
- **Falsifiers for your own RCA**: state what evidence would flip each verdict — an RCA without falsifiers is an opinion.
- **Dated watchlist**: 5–8 items with dates/quarters, each mapped to the hypothesis it tests (next print, capex guide, monetization disclosures, regulatory calendar, FCF path ex-one-offs).

**Gate:** one-sentence cause written; ordinal ranking only; scenarios + falsifiers + watchlist present; zero price targets.

---

## 10. Phase 9 — Report production workflow

1. **Brief first**: write `assets/slides_brief.template.json`-style `slides_brief.json` with per-page title, layout archetype, and a task brief that already contains the exact figures, quotes and sources. Building pages while improvising content is how numbers drift from the fact base.
2. **Page architecture** (15-page default; compress to 12–16 as needed):
   01 Cover (title, 4-stat strip, cutoff + disclaimer) · 02 Verdict (3 tagged cards + "what the panic missed" band) · 03 Event timeline · 04 Results scorecard table · 05 Price action + drawdown ladder · 06 Section divider: The Hypothesis Tree · 07 H-page (primary narrative) · 08 H-page (primary mechanical) · 09 Contributor pages (H3+H4 combined) · 10 Amplifier page · 11 Evidence matrix (all hypotheses, verdicts, confidence) · 12 Overlooked case · 13 Street reaction & valuation damage · 14 Scenarios & falsifiers · 15 Sources & confidence ledger.
3. **Design system**: Midnight IC tokens, components and the 1280×720 overflow budget are specified in `references/report-design.md`. Follow the budget — it is derived from real overflow failures.
4. **Every page**: kicker, headline, source line (named sources), confidence chips, no emoji, no lorem.
5. **Charts**: prefer pure CSS bars/ladders (`.bar-track/.bar-fill`) for deterministic rendering; if using a chart library it must render fully offline from local data.
6. **Viewer**: one extra HTML file linking all pages with keyboard navigation (←/→), so the reviewer can flip through the deck as one artifact.
7. Build pages → run Phase 10 audits → fix the brief/generator, not the rendered page.

**Gate:** brief complete before first page; all pages match brief; audits clean.

---

## 11. Phase 10 — Audit protocol & data freshness

### 11.1 Numeric audit

```
python3 scripts/fact_base_audit.py --slides <slides_dir> --fact-base <fact_base.json>
python3 scripts/fact_base_audit.py --slides <slides_dir> --checks <checks.json>   # simple needle format
python3 scripts/fact_base_audit.py --slides <slides_dir>                          # placeholder scan only
python3 scripts/fact_base_audit.py --selftest
```

- The fact-base mode verifies every fact's numeric tokens appear in the assigned pages (anchored, sign/symbol-tolerant matching — a digit substring of a longer slide number never satisfies a fact), arithmetically checks derived-fact formulas, enforces the Assumed-on-method-page rule (`meta.method_page` or `--method-page`), and reverse-checks numbers found in slides against the fact base to surface **unverified candidates**.
- The checks-file format is `{"slide_01.html": ["-12.29%", "$482B", ...]}` — one needle list per page, same as used successfully in the Alphabet engagement (212 checks).
- Placeholder scan always runs, on visible text only: `lorem`, `todo`, `placeholder`, `xxx`, `【`, `tbd`, `nan`, `undefined`, `insert …`.
- Investigate every failure. The Alphabet engagement's two documented false positives are the model: needles `$205` and `$500` failed only because the slides print those figures inside ranges (`$195–205B`, `$300–500`) — the numbers were present and correct. Prefer fact-base mode (anchored token matching) over needle mode for exactly this reason, and when a needle fails, check for range/abbreviated formatting before touching the slide.

### 11.2 Render audit

```
node scripts/overflow_audit.mjs --dir <slides_dir>            # 1280x720 overflow/clipping
node scripts/overflow_audit.mjs --dir <slides_dir> --shots /tmp/shots   # + screenshots
node scripts/overflow_audit.mjs --selftest
```

- Flags visible elements extending past the slide canvas by >2px, **measured relative to the `.slide` element itself** (default body margins cannot fake a pass or a failure). Only the explicit non-content markers are skipped: `data-bleed="intentional"`, `data-decor`, `aria-hidden="true"` — no class-name guessing.
- Fix failures in the brief/generator (reduce content, shrink type a step, restructure), never by nudging the rendered HTML ad hoc. Re-run until clean.

### 11.3 Data freshness

- Stamp the cutoff on the cover; before delivery, if the market has since traded, refresh price facts and re-run audits, or explicitly restate the cutoff.
- Weekend/holiday: verify the last close date you are quoting is the last **trading** day.
- Keep the fact base append-only during an engagement: corrections are new entries referencing the old, never silent overwrites.

---

## 12. The fact base in practice

Schema, field definitions and worked examples live in `references/fact-base-schema.md`.
Working rules that experience says matter most:

- One fact = one row = one source trail. Compound facts get split ("FCF −$9.1B" and "of which $5.2B EU fine" are two facts).
- Include the source **sentence** in `notes` for anything you will quote or paraphrase on a slide.
- Tag each fact with the hypothesis IDs it can evidence (`supports: ["H2"]`) — this makes Phase 4 assembly mechanical and the evidence matrix auditable.
- Derived facts cite their parent facts and formula (`derived_from: ["F-042","F-047"], formula: "-9.1 + 5.2 = -3.9"`).

---

## 13. Full pitfall catalog

| # | Pitfall | Rule that prevents it |
|---|---|---|
| 1 | Explaining the wrong miss (GAAP vs adjusted basis confusion) | §7 bridge before any causal claim; state the consensus basis |
| 2 | Attributing one-off noise (impairments, fines) to narrative | §7 one-off inventory; ex-item arithmetic on the slide |
| 3 | Consensus numbers from memory | §2.3 every estimate carries outlet + date |
| 4 | Treating the after-hours print as the reaction | §1 reaction = T+1 close; AH labeled secondary |
| 5 | Share-class / split-basis errors | §2.2 ticker-class check at Phase 0 |
| 6 | Macro attribution while peers moved idiosyncratically | §3 same-day peer cross-section before any macro claim |
| 7 | Fake-precision attribution percentages | §9 ordinal ranks unless computable |
| 8 | Skipping call Q&A | §2.4 transcript protocol is mandatory, not optional |
| 9 | "Worst since / record / biggest ever" from memory | §3 rankings only from named sources |
| 10 | Single-story narrative, no competing hypotheses | §4 ≥5 hypotheses, ≥1 excluded |
| 11 | Content overflow / clipped slides discovered at review | §10.3 overflow budget; §11.2 render audit |
| 12 | Numbers drifting from sources during page building | §10.1 brief-first + numeric audit gate |
| 13 | Decorative bleed elements flagged as overflow | mark them non-content: `data-bleed="intentional"`, `data-decor`, or `aria-hidden="true"` |
| 14 | Publishing scenarios that read as price targets | §9 explicit "analytic frames, not price targets" |
| 15 | Stale data shipped after market moved | §11.3 cutoff stamp + refresh duty |

---

## 14. Compliance, tone & two-sidedness

- Every report carries: "Informational only — not investment advice, not a solicitation. No price targets published." (If the user insists on targets, they become `Assumed` scenario inputs, clearly labeled, never recommendations.)
- **MNPI / Regulation FD**: build only from public sources (filings, IR materials, press). If an input is suspected to be material non-public information, stop and escalate. Never incorporate it into a fact base.
- **Internal-use framing**: the deliverable is an internal analytical pre-read, not sell-side research — no rating, no price target, no Reg AC analyst certification, no FINRA 2241 disclosure package. Do not distribute it as if it carried those.
- Two-sided by construction: the counter-case page and the `AGAINST` evidence columns are mandatory. A report that only justifies the move's direction is advocacy, not research.
- Tone: institutional, concrete, zero hyperbole. Let magnitudes carry the drama ("−12.29% to $282.32" beats "sky fell").
- Name humans with roles and shops ("Pivotal Research CEO Jeffrey Wlodarczak"), quote exactly, attribute always.
- Never invent, round toward the thesis, or drop a conflicting source. If the evidence is genuinely ambiguous, the report says so — ambiguity stated is credibility earned.
