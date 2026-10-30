---
name: big-tech-earnings-postmortem
version: 1.3.0
description: >
  Conduct fact-based, evidence-disciplined root-cause analysis of a US-listed big-tech stock's price move around earnings, and produce a single-file HTML research note passing bundled lite delivery gates (placeholder, disclosure, render audits). The lightweight, fastest-ship member of the big-tech research family: layered driver attribution with durability and evidence axes, no multi-page deck, lite bundled audits instead of the flagship's machine-checked fact base — use analyzing-us-bigtech-stocks for a full audited IC deck and bigtech-equity-research for a quantified single-note with segment deep-dive and options math. Trigger when the user asks why a big-tech stock (Alphabet, Microsoft, Amazon, Meta, Apple, Nvidia, Tesla) moved sharply after earnings, or requests a post-earnings deep dive / market research report with root-cause attribution — phrases like "post-earnings analysis", "why did X drop after earnings", "earnings post-mortem", "stock price drop root cause", or "big tech earnings deep dive".
license: Apache-2.0
compatibility: Requires web search and page-fetch tools for primary-source verification; render gate needs Node.js with Playwright.
---

# Big-Tech Earnings Post-Mortem & Trend Analysis

Produce a research artifact that a portfolio manager could defend in an
investment committee: every number traceable, every causal claim layered and
falsifiable, every judgment labeled with its confidence basis.

## Canonical methodology

The full statement of this framework — the two-axis driver classification
(durability × evidentiary basis), the ranking heuristic, the risk/catalyst
matrix, and the failure-mode catalog — lives canonically in the sibling skill
at `analyzing-us-bigtech-stocks/references/postmortem-framework.md`. This file
is the standalone operative summary for deployments without that folder
installed. On any divergence between the two, the canonical copy wins: fix it
there and mirror the change here in the same commit (the repository's
consistency tests, `tests/test_repo_consistency.py`, guard this wiring).

## Skill folder structure

```
big-tech-earnings-postmortem/
├── SKILL.md                       # This file: triggers, workflow, gates
├── assets/checks.json             # Disclosure needles the lite audit enforces
└── scripts/
    ├── note_audit.py              # Placeholder + disclosure-needle gate
    └── note_overflow_audit.mjs     # Render/overflow gate (Node + Playwright)
```

The two scripts are the skill's own delivery gates — trimmed ports of the
flagship's `fact_base_audit.py` placeholder/needle checks and
`overflow_audit.mjs`, adapted for a single-file scrolling note. They require
no fact base and no sibling skill: compliance is bundled, not
"if the flagship happens to be installed".

## When this skill applies

Use for **any US-listed large-cap technology company** after an earnings release,
guidance update, or a sharp unexplained price move. Examples: GOOGL, MSFT, AMZN,
META, AAPL, NVDA, TSLA, ORCL. The company does not need to be a "hyperscaler" —
the workflow generalizes; only the metric emphasis shifts (see §5).

Do **not** use for: intraday technical analysis, macro-only commentary,
pre-earnings previews with no price event to explain, or private companies.

## Core principle: separate the number from the narrative

A stock move is **the market's revision of expectations**, not a verdict on the
company. Your job is to answer three questions in order:

1. **What exactly did the market react to?** (mechanical trigger)
2. **Which of those items are structural vs. temporary?** (durability filter)
3. **What would falsify the current narrative?** (catalyst/risk matrix)

Never skip from "stock fell X%" to "investors are worried about AI." That is
narrative without attribution.

**Arithmetic discipline — compute, don't recall.** Never do arithmetic
in-context (mentally, in the running text). Every delta, percentage, ratio,
and market-cap figure is executed in code — a scratch script, the sibling
skill's `quant_helpers.py`, or any executed tool — and the code's output is
what goes in the note. In-context arithmetic is where transcription and
magnitude errors enter, and it is the one failure mode no audit gate can
catch downstream (a wrong number that was never computed cannot be
re-derived by a checker).

## Workflow

### Step 1 — Pin the event mechanics

Before reading any analysis, establish the observable facts:

- **Exact date and session** of the move: the primary reaction is the **first
  full-session close after the event (T+1 close)**; after-hours and T+0 intraday
  are secondary color. Report both if they differ materially.
- **Share class and basis**: pin the ticker class (GOOG vs GOOGL, BRK.A/B) and
  split-adjusted basis in writing before pulling prices — never mix classes in
  one computation.
- **Point move and percentage move** on the pinned class; market-cap change in
  dollars (shares outstanding × Δprice).
- **Idiosyncratic vs market-wide split**: compute the market-adjusted excess
  return = stock return − same-day benchmark return (QQQ/XLK or the peer basket).
  If a beta estimate is available, subtract `beta × benchmark return` instead and
  say which convention you used and why. The residual, not the headline move, is
  what the root-cause analysis must explain.
- **Historical rank** of the move ("worst since IPO", "largest one-day cap loss
  ever") — verify against at least two independent sources.
- **Pre-event positioning**: 52-week high/low, YTD performance, and whether the
  stock was already in a drawdown or at an all-time high. A −13% move from a
  peak means something different from −13% after a 40% run.
- **Sector/session context**: did peers move the same day? Was there a macro
  catalyst (Fed, CPI, another company's print)?

**Source tiers** (what each source class may support — mirrors the family
convention in `analyzing-us-bigtech-stocks`):

| Tier | Sources | May support |
|---|---|---|
| **T1 — Primary** | SEC EDGAR (8-K/10-Q/10-K), company IR press release, company-hosted transcript/audio | All fundamentals: revenue, segments, margins, EPS, capex, FCF, guidance, one-offs |
| **T2 — Named press** | Reuters, Bloomberg, CNBC, FT, WSJ, AP; third-party transcripts (Motley Fool, Seeking Alpha) cross-checked against IR | Consensus, surprise framing, analyst actions, macro prints |
| **T3 — Aggregators** | Yahoo Finance, Stooq, Macrotrends, TIKR | Prices, closes, market cap, ranges. **Never** fundamentals or consensus |

"Two independent sources" means two **different tiers or origination chains** — two
aggregators scraping the same wire story do not corroborate anything.

**Output of this step:** a verified event box with source citations. Do not
proceed until the move is numerically pinned.

### Step 2 — Build the financial scorecard against consensus

Pull the reported figures and the consensus estimate for each. Cover **at
minimum**:

| Category | Metrics |
|---|---|
| Top line | Total revenue; segment revenue (search/ads, cloud, devices, etc.) |
| Profitability | GAAP EPS; non-GAAP EPS; operating income; operating margin |
| Cash generation | Operating cash flow; capex; **free cash flow**; capex/OCF ratio |
| Guidance | Current-quarter and full-year revenue/EPS guidance; capex guidance |
| Balance sheet | Cash & securities; total debt; net debt; share count change |

Rules:

- **Always compute FCF = OCF − Capex.** Report the capex/OCF ratio explicitly.
  A ratio above 100% means the company is funding growth with external capital or
  cash reserves — this is a high-signal fact for big-tech names. For
  capital-allocation debates, also show stock-based compensation and, where the
  Street debate warrants it, unlevered FCF (state the basis: SBC add-back,
  working-capital moves) — FCF that ignores SBC overstates cash generation.
- **Split GAAP vs. non-GAAP**. Identify every material below-the-line item
  (mark-to-market losses, legal fines, restructuring, tax one-offs) and state
  whether it is **cash or non-cash**, **recurring or one-time**, **dilutive or
  not**. Do not label the whole gap "accounting noise" without this split.
- **Share count matters.** A GAAP EPS miss caused by dilution is not the same as
  one caused by an operating miss. Check diluted share count QoQ and YoY.
- Cross-check each figure across **at least two independent outlets** and, where
  possible, the company's own press release or SEC filing.

**Output of this step:** a scorecard table with beat/miss/in-line for each metric.

### Step 3 — Layered root-cause attribution (the core of the skill)

Do **not** present causes as a flat list. Rank them by explanatory power for the
observed move and classify each along two axes:

**Axis A — Durability:**
- **Mechanical/temporary** — position unwind, one-off accounting mark, index
  rebalancing, sympathy selling. Reversible.
- **Structural** — change in unit economics, competitive position, monetization
  rate, or capital-intensity regime. Not reversible by a good next quarter.

**Axis B — Evidentiary basis:**
- **Disclosed** — management said it, or the filing shows it.
- **Inferred** — logical deduction from disclosed data.
- **Assumed** — market narrative or analyst speculation.

For each driver, answer:
1. What is the claim?
2. What is the **single strongest piece of evidence** (quote, filing line,
   calculated ratio)?
3. Is it structural or mechanical?
4. How much of the move does it plausibly explain? (Rank, don't quantify
   falsely — say "primary", "contributing", "secondary".)

**Ranking heuristic for big-tech post-earnings moves**, in rough order of
explanatory power:

1. **Cash-flow surprise** (FCF vs. consensus; capex/OCF ratio change). Most
   mechanical and least debatable trigger.
2. **Core-franchise deceleration** (the highest-margin segment slowing). Most
   structurally important; often the real driver beneath a cash-flow headline.
3. **Earnings-quality deterioration** (GAAP vs. operating divergence, dilution,
   below-the-line volatility). Amplifies the miss but is often partly temporary.
4. **Guidance revision** (capex up without FCF recovery; revenue guide cut).
   Resets the forward model.
5. **Positioning/valuation reset** (stock was priced for perfection). Mechanical
   multiplier on the other four.

Adjust order based on what the data actually shows — the heuristic is a prior,
not a straitjacket.

**Elimination is a finding, not a failure.** Identify at least one superficially
plausible driver that the data contradicts, and reject it explicitly with the
falsifying fact (e.g. "Cloud demand failure — rejected: Cloud grew +103% with
record backlog"). A ranked table of surviving drivers without a tested rejection
of an attractive wrong one is confirmation-seeking, not analysis.

**Output of this step:** a ranked driver table with durability and evidence tags,
plus at least one explicitly rejected driver with its falsifying fact.

### Step 4 — Peer and industry context

A single company's FCF deficit looks like failure in isolation; in a sector-wide
capex cycle it looks like a regime. Establish:

- **Peer capex/FCF comparison**: same metric, same quarter, for 2–4 closest
  peers. Is the company an outlier or in line?
- **Industry-wide guidance trend**: are peers also guiding capex up? Cutting?
- **Sector reaction**: did peers sell off on the same day, and by how much?
  This separates idiosyncratic from systematic repricing.
- **Supply-chain / credit signals** where relevant (bond yields, lease
  commitments, supplier commentary).

**Output:** a peer table and a one-paragraph "is this company-specific or
sector-wide?" verdict.

### Step 5 — Sell-side positioning

Collect, for each major analyst action published within ~48 hours:

- Firm, analyst name (if named), rating change (or maintained), price target
  before and after.
- The **stated rationale**, summarized faithfully — do not infer a rationale
  the analyst did not give.

Look for the **pattern**: target cuts with maintained Buy ratings signal a
time-horizon debate ("right story, wrong quarter"), not an existential
downgrade. Downgrades with target cuts signal a thesis change. Report which
pattern dominates.

**Output:** analyst table + one-paragraph read on what the sell-side is
actually debating.

### Step 6 — Risk / catalyst matrix (the "what would change the narrative" test)

This is what separates institutional research from commentary. Build a table
with:

| Variable | Bear case if unresolved | Bull case if resolved | Observable trigger & timeline | Weight |
|---|---|---|---|---|

Rules:
- Each row must have an **observable, dated trigger** — a metric release, a
  guidance update, a product milestone, a regulatory docket. "Sentiment
  improves" is not a trigger.
- Weight by **impact on the structural debate**, not by how interesting it is.
- Include at least one **near-term** (next 1–2 quarters) and one **medium-term**
  (4–8 quarters) catalyst.

### Step 7 — Synthesis and confidence labeling

Write the final verdict as a **falsifiable thesis**, not a prediction. State:

- What the move was **actually pricing** (your central claim).
- What would **prove the claim wrong** (falsification condition).
- The **time horizon** over which the debate resolves.
- The **valuation boundary**: the note explains the repricing; it does **not**
  opine on whether the name is now cheap or expensive. Say so in one line
  ("no DCF / SOTP / scenario-weighted fair value is produced; the valuation
  model gap is logged as an open item") so an IC reader never mistakes a
  post-mortem for a complete investment memo.

Tag every non-trivial claim:

- `Verified` — executed/checked and observed directly (number cross-checked,
  ratio recomputed, quote confirmed).
- `Reasoned` — logical inference from verified data, not directly observed.
- `Assumed` — based on a stated assumption; say what the assumption is.
- `Unverifiable` — environment does not allow verification; say what would be
  needed.

**Never write "the stock will..." or "this proves..." without a confidence tag.**
Never present a forward-looking synthesis as a verified fact.

### Step 8 — Build the verification ledger

Produce a final table listing the **10–15 most load-bearing claims**, each with:

- The claim.
- Source(s).
- Confidence tag.
- **How it was verified** (cross-checked across N outlets; ratio recomputed;
  direct quote from transcript; filing line).

This ledger is non-negotiable for institutional-quality output. It is the
difference between a report that *looks* rigorous and one that *is*.

### Step 9 — Assemble the HTML deliverable

Use the following slide sequence. Keep the visual language restrained and
data-dense — this is an investment-committee artifact, not a marketing page.

1. **Event box + executive summary** — the move pinned, the thesis in 3–4
   sentences, the four KPI tiles (move, cap loss, EPS surprise, FCF).
2. **Financial scorecard** — the Step 2 table, with beat/miss flags.
3. **Layered root-cause decomposition** — the Step 3 ranked drivers, each with
   its evidence block and durability tag.
4. **Peer/industry context** — the Step 4 table and verdict.
5. **Sell-side reaction** — the Step 5 table and pattern read.
6. **Risk/catalyst matrix** — the Step 6 table.
7. **Verification ledger + method note** — the Step 8 table, plus a short
   paragraph on what was and was not independently verifiable.

Design constraints:
- Dark or neutral institutional palette; one accent color.
- Monospace for all numbers.
- Severity/confidence tags color-coded consistently.
- Tables over prose wherever the content is comparative.
- No placeholder values, no "TODO", no fabricated citations.
- A **verification-status line** in the note header stating which gates the
  finished note passed — "Verification status: lite audit gates passed —
  disclosure needles + render audit", or "Draft — human verification required"
  with the reason when a gate could not run. Keep the wording free of the
  audit scan tokens (`todo`, `tbd`, `xxx`, `nan`, `undefined`, `placeholder`,
  `lorem`, `insert data/numbers`, `foo bar`, `【`) so the gate does not flag
  the status line itself.
- Mobile: collapse multi-column KPI rows to 2×2; stack two-column grids.

## Metric emphasis by company type

| Company type | Prioritize | De-emphasize |
|---|---|---|
| Hyperscaler / AI infra (GOOGL, MSFT, AMZN, META, ORCL) | Capex/OCF, FCF, cloud backlog, AI monetization rate, lease commitments | Traditional P/E alone |
| Consumer hardware (AAPL) | Product revenue by line, gross margin, services attach, China exposure | Capex intensity |
| Semiconductor (NVDA) | Data-center revenue, backlog/bookings, gross margin, inventory days | FCF (usually strong) |
| EV / auto-tech (TSLA) | Deliveries, auto gross margin ex-credits, energy storage, regulatory credits | Traditional ad/cloud metrics |

## Quality gates (check before delivering)

- [ ] Event move is numerically pinned and cross-checked across ≥2 sources.
- [ ] FCF is computed, not copied; capex/OCF ratio is shown.
- [ ] Every below-the-line item is split into cash/non-cash and recurring/one-time.
- [ ] Causes are ranked, not listed; each is tagged structural vs. mechanical.
- [ ] The single strongest piece of evidence for the top driver is quoted or
      shown, not paraphrased vaguely.
- [ ] Peer comparison is present and answers "company-specific or sector-wide?"
- [ ] Analyst actions are attributed to named firms with before/after targets.
- [ ] Risk/catalyst rows each have an observable, dated trigger.
- [ ] Every non-trivial claim carries a confidence tag.
- [ ] All deltas, ratios, and market-cap figures were computed in code, never
      in-context (arithmetic discipline).
- [ ] A verification ledger exists with 10+ load-bearing claims.
- [ ] No fabricated numbers, citations, IDs, or analyst targets.
- [ ] Forward-looking statements are explicitly labeled `Reasoned` or `Assumed`.
- [ ] At least one plausible-but-wrong driver explicitly rejected with its falsifying fact.
- [ ] Valuation boundary stated: the note explains the repricing and does not
      opine on mispricing; the model gap is named as an open item.
- [ ] `Unverifiable` gaps are listed in a Data-Gap Ledger with the exact pull needed.
- [ ] `python3 scripts/note_audit.py --note <note.html> --checks assets/checks.json`
      exits 0 (placeholder + disclosure gates).
- [ ] `node scripts/note_overflow_audit.mjs --note <note.html>` exits 0 (render
      gate), or the verification-status line says "Draft — human verification
      required" with the reason.
- [ ] The verification-status line is present and matches the actual gate results.
- [ ] Disclaimer present on the deliverable: informational only, not investment
      advice; no price targets published.

## Degraded mode (tools offline or rate-limited)

Web search and page-fetch tools are a hard dependency of this skill. When they
are unavailable or fail mid-task:

1. Proceed only on figures already retrieved and verified in this session.
2. Tag every remaining gap `Unverifiable` (or `Assumed` with stated bounds) and
   list it in a **Data-Gap Ledger**: the exact source and pull needed to close it.
3. Never backfill a missing figure from memory or model prior knowledge — shrink
   the scope instead and say so.

## Verification and delivery gates

These gates are **mandatory and bundled** — they ship with this skill, so
compliance does not depend on the flagship being installed:

1. **Placeholder + disclosure gate** (always):
   `python3 scripts/note_audit.py --note <note.html> --checks assets/checks.json`
   Fails the delivery on placeholder tokens in visible text, on a missing
   compliance disclaimer or verification-status line, and — when the note
   quantifies a driver allocation or mentions a beta — on a missing
   "Reasoned allocation — not a measured decomposition" label or beta
   estimation-window disclosure. `--selftest` proves the script works.
2. **Render gate** (always):
   `node scripts/note_overflow_audit.mjs --note <note.html>`
   Flags horizontal overflow, elements spilling past the viewport width, and
   overflow:hidden boxes clipping their content (headless Chromium; install
   with `npm install playwright && npx playwright install chromium` if
   missing — the script prints the exact commands on failure).
3. If an environment genuinely cannot run the render gate, do not ship
   silently: set the verification-status line to "Draft — human verification
   required (render gate not run: <reason>)" and say so in the reply.
4. For a **full fact-base numeric audit** (every figure machine-checked
   against a sourced fact base, formula arithmetic, cross-check enforcement),
   build the sibling flagship's `fact_base.json` and run its
   `fact_base_audit.py` — that is the family's upgrade path to a fully
   audited IC deliverable, and the verification-status line should then say
   "full fact-base + render audits passed".

The Step 8 verification ledger is still the human-layer control: the gates
above check placeholders, disclosures, and rendering; the ledger is what makes
every load-bearing claim traceable. Both layers are required.

- Every deliverable carries the disclaimer: "Informational only — not investment
  advice, not a solicitation. No price targets published."
- These outputs are internal analytical notes, not sell-side research: no rating,
  no price target, no analyst certification or conflict disclosures — do not
  distribute them as if they carried those. Build only from public sources; if
  any input is suspected to be MNPI (Regulation FD), stop and escalate.

## Common failure modes (avoid these)

- **Flat attribution**: listing three causes without ranking or durability
  classification. The reader cannot act on it.
- **"Accounting noise" hand-wave**: dismissing a GAAP miss without checking
  whether dilution or a cash fine is inside it.
- **Narrative-first**: starting from "AI fears" and selecting numbers to fit,
  instead of letting the FCF/capex data drive the ranking.
- **Peer omission**: analyzing FCF in isolation and calling it company failure
  when the whole sector is in a capex cycle.
- **False precision**: inventing a percentage of the move attributable to each
  driver. Use ordinal ranks, not fake decompositions.
- **Sell-side ventriloquism**: attributing a rationale to an analyst that they
  did not state.
- **Confidence inflation**: writing "this confirms" when the evidence is
  `Reasoned` or `Assumed`.
