---
name: big-tech-earnings-postmortem
version: 1.6.0
description: >
  Conduct fact-based, evidence-disciplined root-cause analysis of a US-listed big-tech stock's price move around earnings, and produce a single-file HTML note passing bundled lite delivery gates (number registry with consensus + temporal-order + snapshot-linkage checks, placeholder, scoped disclosure, render, accessibility audits) with provenance sealing and source snapshots. The lightweight, fastest-ship member of the big-tech research family: layered driver attribution (durability × evidence axes), a machine-checked lite number registry instead of the flagship's full fact base — use analyzing-us-bigtech-stocks for a full audited IC deck and bigtech-equity-research for a quantified single-note with segment deep-dive and options math. Trigger when the user asks why a big-tech stock moved sharply after earnings, or requests a post-earnings deep dive — phrases like "post-earnings analysis", "why did X drop after earnings", "earnings post-mortem", "stock price drop root cause", or "big tech earnings deep dive".
license: Apache-2.0
compatibility: Requires web search and page-fetch tools for primary-source verification; Python >= 3.9 for the audit/quant scripts; render and accessibility gates need Node.js >= 18 with Playwright >= 1.40.
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
├── assets/checks.json             # Scoped disclosure needles the lite audit enforces
├── assets/fact_base_lite.template.json   # Number-registry skeleton (Step 8)
└── scripts/
    ├── fact_base_lite_audit.py    # Number-registry gate (round 3; consensus +
    │                              #   temporal-order checks round 4; snapshot
    │                              #   linkage + --strict-temporal + --json round 5)
    ├── quant_helpers.py           # Bundled arithmetic + beta/market-cap math
    │                              #   (byte-identical family copy, round 4)
    ├── source_snapshot.py         # Source-truth snapshots: record/verify the
    │                              #   fetched source content (round 5)
    ├── note_audit.py              # Placeholder + scoped disclosure-needle gate
    │                              #   (--json for CI, round 5)
    ├── note_overflow_audit.mjs     # Render/overflow gate (Node + Playwright)
    ├── a11y_audit.mjs             # Accessibility gate (lang/heading/alt/WCAG-AA contrast)
    └── provenance_seal.py         # SHA-256 sealing + tamper-evident verification
```

The scripts are the skill's own delivery gates — trimmed ports of the
flagship's `fact_base_audit.py` checks and `overflow_audit.mjs`, adapted for a
single-file scrolling note. Round 3 added the number-registry gate
(`fact_base_lite_audit.py`): the note's every money/percentage figure is
machine-checked against a lite fact base, so even the fastest-ship member has a
checked number trail (the reports-6/7 "lite-variant verification gap"). Round 4
(reports 8/9) bundled `quant_helpers.py` itself (M-5: the skill no longer
borrows the sibling's helper — standalone means standalone) and extended the
registry gate with the lite CONSENSUS check (provider + vintage + mean/median
statistic, M-1) and the TEMPORAL check (pre-filing embargo with the
`data_type` discriminator, M-6). Round 5 (reports 10/11) adds the SNAPSHOT
linkage check (`--snapshots` / `--strict-snapshots` — the registry is tied to
hashed snapshots of the fetched sources, closing the internal-consistency-vs-
source-truth gap), `--strict-temporal` (date-only retrieval stamps fail on
intraday-sensitive engagements), `--json` machine-readable output for CI, and
`source_snapshot.py` itself. They require no sibling skill: compliance is
bundled, not "if the flagship happens to be installed".

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
and market-cap figure is executed in code — the skill's own bundled
`scripts/quant_helpers.py` (byte-identical family copy, round 4), a scratch
script, or any executed tool — and the code's output is what goes in the note.
In-context arithmetic is where transcription and magnitude errors enter, and it
is the one failure mode no audit gate can catch downstream (a wrong number
that was never computed cannot be re-derived by a checker).

## Workflow

### Step 1 — Pin the event mechanics

Before reading any analysis, establish the observable facts:

- **Exact date and session** of the move, set by the **event-window rule
  (round 4, reports 8/9 H-3)**: an after-close event (the classic earnings
  drop) → primary reaction = the **first full-session close after the event
  (T+1 close)**; a pre-market or intraday event (guidance shock, regulatory
  ruling, product launch) → primary reaction = the **T+0 close** — T+1 for an
  intraday event contaminates the event return and the benchmark excess
  return with an extra session. Report after-hours and intraday prints as
  secondary color, labeled as such.
- **Share class and basis**: pin the ticker class (GOOG vs GOOGL, BRK.A/B) and
  split-adjusted basis in writing before pulling prices — never mix classes in
  one computation.
- **Point move and percentage move** on the pinned class; market-cap change in
  dollars. **Multi-class names (round 4, reports 8/9 H-4)**: compute each
  share class separately and sum — `scripts/quant_helpers.py::market_cap_delta`
  — never one class's shares with another class's price; disclose the method.
- **Idiosyncratic vs market-wide split**: compute the market-adjusted excess
  return = stock return − same-day benchmark return (QQQ/XLK or the peer basket).
  If a beta estimate is available, subtract `beta × benchmark return` instead and
  say which convention you used and why — with the beta estimated over the family's
  canonical default window (2-year monthly returns vs QQQ) unless the company's
  risk profile structurally changed, in which case justify the alternative window.
  **Beta regime diagnostics (round 4, reports 8/9 M-7)**: run
  `quant_helpers.beta_diagnostics` (R² + correlation-breakdown flag) and
  `volatility_regime_flag` (trailing-vol z-score) on the estimation window —
  if R² < 0.30 or |z| > 2, the canonical window is fitting a broken regime
  (2022 rate shock, 2023 AI re-rating): justify the window explicitly or
  re-estimate over a shorter (e.g. 6-month daily) window and disclose it.
  The residual, not the headline move, is what the root-cause analysis must explain.
- **Historical rank** of the move ("worst since IPO", "largest one-day cap loss
  ever") — verify against at least two independent sources.
- **Pre-event positioning**: 52-week high/low, YTD performance, and whether the
  stock was already in a drawdown or at an all-time high. A −13% move from a
  peak means something different from −13% after a 40% run.
- **Sector/session context**: did peers move the same day? Was there a macro
  catalyst (Fed, CPI, another company's print)? **Peer-basket hygiene (round 4,
  reports 8/9 M-8)**: before reading the sector cross-section, run a
  corporate-action check on each named peer (M&A, spin-off, delisting — a T2
  news check per name) and re-verify when the basket facts are >90 days old or
  undated; a basket that silently lost a distressed constituent flatters the
  sector average.

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

- **Always compute FCF = OCF − Capex, in code** (the bundled
  `quant_helpers.py::fcf`, a scratch script, or any executed tool). Report the
  capex/OCF ratio explicitly. A ratio above 100% means the company is funding
  growth with external capital or cash reserves — this is a high-signal fact for
  big-tech names.
- **Pair every FCF figure with FCF ex-SBC = OCF − Capex − SBC** (SBC from the
  quarter's cash-flow statement, T1) as a mandatory reconciliation row of the
  scorecard — not an optional add-on. SBC is structurally material for every
  US mega-cap tech name; FCF that ignores it overstates the cash generation
  available for buybacks and dividends. State which basis (reported FCF or
  ex-SBC) each beat/miss is computed on, and show stock-based compensation and,
  where the Street debate warrants it, unlevered FCF (state the basis: SBC
  add-back, working-capital moves).
- **Consensus figures carry provider + vintage + recorded statistic, T1/T2
  sourcing.** The consensus is the denominator of every beat/miss delta: record
  the named provider (FactSet / Visible Alpha / LSEG / Bloomberg as reported by
  a named outlet), the as-of date of the estimate set (**within 1–3 trading
  days of the event** — round 4 tightened this from ~10 days, reports 8/9 M-1;
  the registry gate checks the fields), the **statistic printed** (`mean` /
  `median` / `undisclosed` — record it even when the outlet does not say: a
  $0.02-vs-$0.05 miss flips on which statistic the wire printed; when it is
  genuinely `undisclosed`, the audit prints a NOTE and the licensed-feed pull
  needed to close the gap goes in the Data-Gap Ledger — round 5, reports 10/11
  §5.7), and the contributor count when disclosed. Never source a consensus
  from a lone T3 aggregator; a single T2 chain must be cross-verified against a
  second distinct origination chain.
- **Reg G / Item 10(e) discipline (round 4, reports 8/9 M-2)**: every non-GAAP
  metric presented is reconciled to its most directly comparable GAAP measure —
  show the bridge or cite the issuer's own reconciliation table — and state
  which basis (GAAP vs non-GAAP) each beat/miss is computed on.
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
plus at least one explicitly rejected driver with its falsifying fact. If a
quantified allocation accompanies the ranking, it is a `Reasoned (judged)` signed
allocation whose sum-to-move identity is an arithmetic consistency check —
labeled adjacent to the chart, never presented as a measured decomposition.

### Step 4 — Peer and industry context

A single company's FCF deficit looks like failure in isolation; in a sector-wide
capex cycle it looks like a regime. Establish:

- **Peer capex/FCF comparison**: same metric, same quarter, for 2–4 closest
  peers. Is the company an outlier or in line? Use the family's canonical
  basket for the name (same primary revenue driver, market-cap proximity within
  roughly an order of magnitude — the sibling skill's `reference/peers.md`
  convention) or a documented alternative, and state the basket and the
  selection criteria in the note: a mega-cap's capex against a mid-cap's is a
  construction artifact, not a finding.
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
  post-mortem for a complete investment memo. Until a valuation module exists
  the note is firewalled as an IC **pre-read attribution note** — an input to
  the IC memo, not the memo (round 4, reports 8/9 C-2).
- **Expected Fundamental Value matrix (round 4, reports 8/9 H-6 — optional,
  recommended for IC-facing notes)**: weight the *fundamental* outcomes of the
  risk/catalyst matrix with subjective probabilities (e.g. FY+1 FCF path in
  bull/base/bear at 25/50/25) and compute the EV-adjusted fundamental range in
  code — `Reasoned (judged)` probabilities, method disclosed, a
  fundamental-expectation construct, **never a price target or fair-value
  claim**. Unweighted narratives cannot feed sizing; the EV matrix is the
  minimum quantitative asymmetry profile the family ships.

Tag every non-trivial claim:

- `Verified` — executed/checked and observed directly (number cross-checked,
  ratio recomputed, quote confirmed).
- `Reasoned (derived)` — deterministic derivation from verified inputs (a delta,
  a bridge, a ratio): formula shown, reproducible.
- `Reasoned (judged)` — analytical judgment (driver weights, structural-vs-
  mechanical calls): signed, method disclosed, explicitly non-causal.
- `Assumed` — based on a stated assumption; say what the assumption is.
- `Unverifiable` — environment does not allow verification; say what would be
  needed.

**Never write "the stock will..." or "this proves..." without a confidence tag.**
Never present a forward-looking synthesis as a verified fact.

### Step 8 — Build the number registry and the verification ledger

Two layers, both machine- or human-checkable:

**The lite number registry** (`fact_base_lite.json`, skeleton in
`assets/fact_base_lite.template.json`) — before assembling the HTML note,
register every money/percentage figure the note will print, each with id,
metric, value, source name, URL, retrieval date, and confidence label. This is
the lightweight counterpart of the flagship's fact base (reports 6/7 finding
H-4/H-5: the lite note used to ship with confidence tags and a
verification-status line while nothing machine-checked its numbers — a
credibility-spillover risk against the family's flagship). Round 4 (reports
8/9) adds two registry disciplines: consensus-side entries carry
`consensus_provider` + `consensus_vintage` + `consensus_statistic`
(mean/median/undisclosed — M-1), and when `meta.t1_filing_timestamp` is pinned,
every entry declares `data_type` `pre_event_input` | `post_event_fact` with
post-event entries retrieved at/after the verified filing time (M-6 — the
temporal embargo: never launder pre-filing chatter into a confirmed fact; a
data-integrity control, not a Reg FD control). The
`scripts/fact_base_lite_audit.py` gate fails the build on unregistered note
figures, registry numbers absent from the note, missing source fields,
consensus/temporal violations, or placeholder tokens.

**Source snapshots (round 5, reports 10/11 §3.4/§6.9) — pin what was actually
fetched.** The registry gate certifies that the note matches the registry —
internal consistency — not that the registry matches the cited source: a wrong
figure with a valid-looking URL passes every check. For decision-critical T1
pulls (the scorecard numbers the verdict leans on), save the fetched source
content as a file and record it: `python3 scripts/source_snapshot.py --record
--url <url> --content <file> --out source_snapshots.json`; reference the
printed SHA-256 in the entry's `source_snapshot` field. The registry gate's
SNAPSHOT check (`--snapshots source_snapshots.json`) then fails the build if
the registry and the snapshot archive drift apart; `--strict-snapshots`
requires every `Verified` entry to carry one; `source_snapshot.py --verify`
re-hashes the saved files (tamper evidence); seal the snapshots with the note
via `provenance_seal.py --inputs`. Before delivery, re-open each
snapshot and re-check the number against the raw text — the snapshot makes the
re-verification pass possible; the pass itself is the analyst's checklist.

**The verification ledger** — a final table listing the **10–15 most
load-bearing claims**, each with:

- The claim.
- Source(s).
- Confidence tag.
- **How it was verified** (cross-checked across N outlets; ratio recomputed;
  direct quote from transcript; filing line).

Both layers are non-negotiable for institutional-quality output. The registry
is the machine layer; the ledger is the human layer. Together they are the
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
  number registry + disclosure needles + render audit", or "Draft — human
  verification required" with the reason when a gate could not run. Keep the
  wording free of the audit scan tokens (`todo`, `tbd`, `xxx`, `nan`,
  `undefined`, `placeholder`, `lorem`, `insert data/numbers`, `foo bar`, `【`)
  so the gate does not flag the status line itself. When the deliverable is
  sealed, the provenance seal line printed by `scripts/provenance_seal.py`
  sits next to it.
- **Methodology-status line (round 5, reports 10/11 §3.6)** — required needle
  in `assets/checks.json`: "Methodology status: empirically unvalidated — face
  validity only (validation harness pending)". The driver-attribution
  methodology has no backtested track record yet; a green gate run is internal
  consistency, not evidence of calibration, and the reader must not have to
  guess that.
- **Scope legends (round 4, reports 8/9 C-1/M-3)**: the note header carries
  "Internal analytical pre-read — not a research report" and the
  "Public-source-only" limitation line (no channel checks, expert calls,
  surveys, or management access). Both are required needles in
  `assets/checks.json` — the note fails the disclosure gate without them.
- **Position disclosure is unconditional once declared (round 5, reports 10/11
  §3.5)**: IC-facing notes carry the fund-position disclosure — "Fund position:
  long / short / none / undetermined, as of <date>" — plus any mandate
  constraint or author conflict that could bear on independence (CFA Institute
  Standard I(B); buy-side fiduciary duty), and the lite audit's conditional
  needle fails an IC memo without it. **And once any position in the covered
  name exists — any `meta.mandate_context` in the registry — the disclosure is
  required whatever the audience**: the registry gate fails a declared-but-
  incomplete `mandate_context`, because a position does not stop being a
  conflict when the reader is not a committee.
- Mobile: collapse multi-column KPI rows to 2×2; stack two-column grids.

## Metric emphasis by company type

| Company type | Prioritize | De-emphasize |
|---|---|---|
| Hyperscaler / AI infra (GOOGL, MSFT, AMZN, META, ORCL) | Capex/OCF, FCF, cloud backlog, AI monetization rate, lease commitments | Traditional P/E alone |
| Consumer hardware (AAPL) | Product revenue by line, gross margin, services attach, China exposure | Capex intensity |
| Semiconductor (NVDA) | Data-center revenue, backlog/bookings, gross margin, inventory days | FCF (usually strong) |
| EV / auto-tech (TSLA) | Deliveries, auto gross margin ex-credits, energy storage, regulatory credits | Traditional ad/cloud metrics |

## Quality gates (check before delivering)

- [ ] Event move is numerically pinned and cross-checked across ≥2 sources;
      the event-window rule is stated (after-close → T+1 close; pre-market/
      intraday → T+0 close).
- [ ] FCF is computed, not copied; capex/OCF ratio is shown; non-GAAP metrics
      carry their GAAP reconciliation (Reg G / Item 10(e) discipline).
- [ ] Market-cap delta computed per-class and summed for multi-class names
      (method disclosed).
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
- [ ] The lite number registry exists and every money/percentage figure printed
      in the note is registered in it (or whitelisted as benign furniture with
      a justification); consensus-side entries carry provider + vintage +
      statistic; entries are `data_type`-classified and temporally clean when
      `meta.t1_filing_timestamp` is pinned.
- [ ] Decision-critical T1 pulls carry `source_snapshot` hashes; the
      `--snapshots` linkage is clean (or the no-snapshots NOTE is consciously
      accepted); `source_snapshot.py --verify` exits 0 when snapshots exist
      (round 5).
- [ ] `python3 scripts/fact_base_lite_audit.py --note <note.html> --fact-base
      <fact_base_lite.json>` exits 0 (number-registry + consensus + temporal +
      mandate + snapshot gates); `--strict-temporal` used for intraday-
      sensitive engagements; `--json` available for CI.
- [ ] Peer-basket corporate-action check run (each named constituent verified
      alive/unmerged at the comparison date).
- [ ] No fabricated numbers, citations, IDs, or analyst targets.
- [ ] Forward-looking statements are explicitly labeled `Reasoned` or `Assumed`.
- [ ] At least one plausible-but-wrong driver explicitly rejected with its falsifying fact.
- [ ] Valuation boundary stated: the note explains the repricing and does not
      opine on mispricing; the model gap is named as an open item.
- [ ] `Unverifiable` gaps are listed in a Data-Gap Ledger with the exact pull needed.
- [ ] `python3 scripts/note_audit.py --note <note.html> --checks assets/checks.json`
      exits 0 (placeholder + scoped disclosure gates).
- [ ] `node scripts/note_overflow_audit.mjs --note <note.html>` exits 0 (render
      gate), or the verification-status line says "Draft — human verification
      required" with the reason.
- [ ] `node scripts/a11y_audit.mjs --note <note.html>` exits 0 (lang / heading
      order / image alt / WCAG-AA contrast), or the status line records why it
      could not run.
- [ ] The verification-status line is present and matches the actual gate results;
      when sealed, the provenance seal line is embedded and `provenance.json`
      ships with the note.
- [ ] IC-facing notes carry the fund-position disclosure; any declared
      `meta.mandate_context` is complete (fund_position + position_as_of)
      whatever the audience (round 5).
- [ ] "Not a research report" and "Public-source-only" legends present.
- [ ] The **methodology-status line** is present: "Methodology status:
      empirically unvalidated — face validity only (validation harness
      pending)" (round 5 — required needle).
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

1. **Number-registry gate** (always, round 3 + round 4 + round 5 extensions):
   `python3 scripts/fact_base_lite_audit.py --note <note.html> --fact-base <fact_base_lite.json>`
   Fails the build on note figures with no registry entry, registry numbers
   absent from the note, missing source fields, and placeholder tokens. This
   closes the reports-6/7 "lite-variant verification gap": the note's numbers
   are machine-checked even in lightweight mode. Round 4 adds the lite
   CONSENSUS check (consensus-side entries need provider + vintage + statistic,
   reports 8/9 M-1) and the TEMPORAL check (when `meta.t1_filing_timestamp` is
   set: every entry classified `data_type`, post-event entries retrieved
   at/after the filing time — pre-filing contamination fails the build,
   reports 8/9 M-6). Round 5 (reports 10/11) adds the MANDATE check (a
   declared `meta.mandate_context` must be complete whatever the audience,
   §3.5), the SNAPSHOT linkage check (`--snapshots source_snapshots.json`:
   declared `source_snapshot` hashes must exist in the manifest;
   `--strict-snapshots` requires them on every `Verified` entry — §3.4),
   `--strict-temporal` (date-only retrieval on the filing date fails — for
   intraday-sensitive engagements), and `--json` (machine-readable stdout for
   CI). `--selftest` proves the script works.
2. **Placeholder + scoped disclosure gate** (always):
   `python3 scripts/note_audit.py --note <note.html> --checks assets/checks.json`
   Fails the delivery on placeholder tokens in visible text, on a missing
   compliance disclaimer, verification-status line, or methodology-status line
   (round 5 required needle), and — when the note quantifies a driver
   allocation or mentions a beta — on a missing "allocation — not a measured
   decomposition" label or beta estimation-window disclosure. Round 3 scoped
   the needles: the qualifying label must sit adjacent to the content it
   qualifies (a footer label does not satisfy a waterfall disclosure), and
   notes discussing the options-implied move must carry the
   volatility-risk-premium caveat near it. `--selftest` proves the script
   works; `--json` gives CI a machine-readable summary (round 5).
   **What these gates do NOT check (round 5, reports 10/11 §2.4/§3.4)**: a
   clean run certifies internal consistency (note ↔ registry) and disclosure
   presence — not source truth (snapshots mitigate), not the economic
   correctness of assumptions, and not the methodology's empirical calibration
   (face validity only; hence the methodology-status needle).
3. **Render gate** (always):
   `node scripts/note_overflow_audit.mjs --note <note.html>`
   Flags horizontal overflow, elements spilling past the viewport width, and
   overflow:hidden boxes clipping their content (headless Chromium; install
   with `npm install playwright && npx playwright install chromium` if
   missing — the script prints the exact commands on failure).
4. **Accessibility gate** (always, round 3):
   `node scripts/a11y_audit.mjs --note <note.html>`
   Checks `<html lang>`, heading order, image alt text, and WCAG-AA text
   contrast — the note's design constraints claim WCAG-AA, so the claim is
   enforced rather than asserted (reports 6/7 M-5/M-6). Same Playwright
   prerequisite as the render gate.
5. **Provenance sealing** (after the gates pass):
   `python3 scripts/provenance_seal.py --inputs <note.html> <fact_base_lite.json> --out provenance.json`
   Writes the SHA-256 manifest, prints the seal line to embed next to the
   verification-status line, and ships as a sidecar; `--verify` re-checks the
   delivered artifact against the seal later (tamper evidence — reports 6/7
   C-2's in-scope core; WORM archival and firm-key signing remain out of scope
   by the standing round-2 rejection). When source snapshots are on record,
   add the manifest and saved content files to `--inputs` so the seal covers
   the evidence trail end to end, and run `source_snapshot.py --verify` first
   (round 5, reports 10/11 §6.9).
6. If an environment genuinely cannot run a gate, do not ship silently: set
   the verification-status line to "Draft — human verification required
   (<gate> not run: <reason>)" and say so in the reply.
7. For a **full fact-base numeric audit** (every figure machine-checked
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
- **Internal-use-only scope control (round 4, reports 8/9 C-1)**: these outputs
  are internal analytical notes, **not research reports** — the note carries
  that legend — and they are for internal use only: no client or external
  distribution, and any wider distribution requires compliance sign-off first.
  No rating, no price target, no analyst certification — do not distribute them
  as if they carried those. Until a valuation module exists, firewalled as IC
  pre-read attribution notes. Build only from public sources; if any input is
  suspected to be MNPI (Regulation FD), stop and escalate.
- **Public-source-only limitation (round 4, reports 8/9 M-3)**: every note
  states "Public-source-only" — no channel checks, expert calls, surveys, or
  management access inform it. A stated limitation, not an aspiration.
- **Data licensing & redistribution (round 4, reports 8/9 M-4)**: vendor figures
  (Yahoo Finance, Stooq, consensus providers) are cited with attribution for
  internal analytical use only; do not reproduce vendor tables at scale and do
  not redistribute the note externally — redistribution rights belong to the
  licensed feeds.
- **Buy-side conflict disclosure (round 3, reports 6/7 C-1; round 5 hardening,
  reports 10/11 §3.5):** an IC-facing note additionally discloses the fund's
  position in the covered name — "Fund position: long/short/none/undetermined,
  as of <date>" — plus mandate constraints and author conflicts that could
  bear on independence (CFA Institute Standard I(B); Advisers Act fiduciary
  duty). Conflict visibility is what lets the committee discount the analysis
  for an existing position. **Once any position exists, the disclosure is
  unconditional**: declare `meta.mandate_context` with both `fund_position` and
  `position_as_of` in the registry whatever the intended audience — the
  registry gate fails a declared-but-incomplete block. The sell-side Reg AC
  package stays inapplicable by the family's standing scoping position.

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
