---
name: big-tech-earnings-postmortem
description: >
  Conduct fact-based, evidence-disciplined root-cause analysis of a US-listed
  big-tech stock's price move around earnings, and produce an institutional-grade
  HTML research deliverable. Use when the user asks why a big-tech stock (Alphabet,
  Microsoft, Amazon, Meta, Apple, Nvidia, Tesla, etc.) moved sharply after
  earnings, or requests a post-earnings deep dive / market research report with
  root-cause attribution and trend assessment. Trigger on phrases like
  "post-earnings analysis", "why did X drop after earnings", "earnings post-mortem",
  "stock price drop root cause", or "big tech earnings deep dive".
license: Apache 2.0
compatibility: Requires web search and page-fetch tools for primary-source verification.
---

# Big-Tech Earnings Post-Mortem & Trend Analysis

Produce a research artifact that a portfolio manager could defend in an
investment committee: every number traceable, every causal claim layered and
falsifiable, every judgment labeled with its confidence basis.

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

## Workflow

### Step 1 — Pin the event mechanics

Before reading any analysis, establish the observable facts:

- **Exact date and session** of the move (regular vs. after-hours; report both
  if they differ materially).
- **Point move and percentage move**; market-cap change in dollars.
- **Historical rank** of the move ("worst since IPO", "largest one-day cap loss
  ever") — verify against at least two independent sources.
- **Pre-event positioning**: 52-week high/low, YTD performance, and whether the
  stock was already in a drawdown or at an all-time high. A −13% move from a
  peak means something different from −13% after a 40% run.
- **Sector/session context**: did peers move the same day? Was there a macro
  catalyst (Fed, CPI, another company's print)? Isolate company-specific
  abnormal return from sector beta.

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
  cash reserves — this is a high-signal fact for big-tech names.
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

**Output of this step:** a ranked driver table with durability and evidence tags.

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
- [ ] A verification ledger exists with 10+ load-bearing claims.
- [ ] No fabricated numbers, citations, IDs, or analyst targets.
- [ ] Forward-looking statements are explicitly labeled `Reasoned` or `Assumed`.

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
