# Post-Mortem Framework — Canonical Driver-Attribution Doctrine

**What this is.** The canonical statement of the big-tech post-mortem methodology:
the layered driver-attribution framework with its two classification axes
(durability × evidentiary basis), the ranking heuristic for post-earnings moves,
the risk/catalyst matrix, the metric-emphasis tables, and the failure-mode
catalog. The sibling skill `big-tech-earnings-postmortem` executes this framework
in lightweight standalone form (single-file note, no bundled tooling). This file
is where the doctrine lives and where changes land first: **if any restatement in
a family skill disagrees with this file, this file wins** — mirror the change into
the restating skill rather than forking a third variant. (Cross-skill doctrine
divergence was the root cause of audit findings M-2 and M-6; the repository's
consistency tests in `tests/test_repo_consistency.py` guard this wiring.)

**When this skill uses it:**

1. **Lightweight mode** — the deliverable is a single-file post-earnings note
   rather than the full 12–16 page deck. Run Phases 0–8 of the main pipeline at
   compressed depth, producing the seven-section note defined in §11, and still
   pass both Phase 10 audit gates on the file. This is the mode
   `big-tech-earnings-postmortem` ships as a standalone skill.
2. **Deep mode (full deck)** — use §2's two-axis classification as an additional
   lens inside Phase 4 (test & classify), §3's heuristic to order hypothesis
   testing in Phases 3–5, and §7's matrix as the layout for the Phase 8
   forward-frame page.

## 1. The three questions, in order

A stock move is **the market's revision of expectations**, not a verdict on the
company. The post-mortem answers exactly three questions, in this order:

1. **What exactly did the market react to?** (mechanical trigger)
2. **Which of those items are structural vs. temporary?** (durability filter)
3. **What would falsify the current narrative?** (catalyst/risk matrix)

Never skip from "stock fell X%" to "investors are worried about AI." That is
narrative without attribution. Pin the event mechanics first (Phase 0 charter,
Phase 2 reaction decomposition): T+1 close as the primary reaction, share class
and split basis pinned in writing, market-cap delta computed as
shares outstanding × Δprice, and the idiosyncratic-vs-market split (market-
adjusted or beta-adjusted excess return, convention stated) before any causal
claim.

## 2. Two-axis driver classification

Classify every surviving driver along two axes. This is the lens Phase 4 applies
on top of its verdict vocabulary.

**Axis A — Durability:**

| Class | Meaning | Reversible by a good next quarter? |
|---|---|---|
| **Mechanical / temporary** | Position unwind, one-off accounting mark, index rebalancing, sympathy selling | Yes |
| **Structural** | Change in unit economics, competitive position, monetization rate, or capital-intensity regime | No |

**Axis B — Evidentiary basis** (maps one-to-one onto the family confidence
labels — never run a second taxonomy):

| Class | Meaning | Confidence label |
|---|---|---|
| **Disclosed** | Management said it, or the filing shows it | `Verified` |
| **Inferred** | Logical deduction from disclosed data | `Reasoned` |
| **Assumed** | Market narrative or analyst speculation | `Assumed` |

**Mapping to Phase 4 verdicts** (the two vocabularies are one system, not two):

| This framework | Phase 4 verdict | Use when |
|---|---|---|
| Structural driver, disclosed evidence | `PRIMARY — narrative` | The market repriced a structural fact |
| Mechanical driver, disclosed evidence | `PRIMARY — mechanical` | A mechanical trigger (FCF print, guide math) carried the move |
| Supporting structural/mechanical driver | `CONTRIBUTOR` | Real, but not the trigger |
| Mechanical/temporary, depth-not-trigger | `AMPLIFIER` | Explains the size, never the cause (crowding, macro tape) |
| One-off noise masquerading as a miss | `NOISE` | Phase 6 reconciliation removes it from the headline |
| Tested and rejected by evidence | `EXCLUDED` | §4's mandatory elimination |

For each driver, answer: (1) what is the claim; (2) what is the **single
strongest piece of evidence** (quote, filing line, calculated ratio); (3)
structural or mechanical; (4) how much of the move does it plausibly explain —
rank it ("primary", "contributing", "secondary"), never a fabricated percentage.

## 3. Ranking heuristic for big-tech post-earnings moves

A prior for ordering hypothesis testing (Phases 3–5), in rough order of
explanatory power:

1. **Cash-flow surprise** (FCF vs. consensus; capex/OCF ratio change) — the most
   mechanical, least debatable trigger.
2. **Core-franchise deceleration** (the highest-margin segment slowing) — the
   most structurally important; often the real driver beneath a cash-flow
   headline.
3. **Earnings-quality deterioration** (GAAP vs. operating divergence, dilution,
   below-the-line volatility) — amplifies the miss but is often partly temporary.
4. **Guidance revision** (capex up without FCF recovery; revenue guide cut) —
   resets the forward model.
5. **Positioning/valuation reset** (stock was priced for perfection) — a
   mechanical multiplier on the other four.

Adjust the order based on what the data shows — the heuristic is a prior, not a
straitjacket.

## 4. Elimination is a finding, not a failure

Identify at least one superficially plausible driver that the data contradicts,
and reject it explicitly with the falsifying fact (e.g. "Cloud demand failure —
rejected: Cloud grew +103% with record backlog"). A ranked table of surviving
drivers without a tested rejection of an attractive wrong one is
confirmation-seeking, not analysis. This is Phase 4's mandatory-exclusion rule;
the rejection row is a required element of every post-mortem deliverable.

## 5. Peer & industry context protocol

A single company's FCF deficit looks like failure in isolation; in a
sector-wide capex cycle it looks like a regime. Establish:

- **Peer capex/FCF comparison** — same metric, same quarter, 2–4 closest peers:
  outlier or in line?
- **Industry-wide guidance trend** — are peers also guiding capex up? Cutting?
- **Sector reaction** — did peers sell off the same day, and by how much? This
  is the Phase 2 same-day cross-section; it separates idiosyncratic repricing
  from systematic de-risking.
- **Supply-chain / credit signals** where relevant (bond yields, lease
  commitments, supplier commentary).

Output: a peer table plus a one-paragraph "company-specific or sector-wide?"
verdict.

## 6. Sell-side positioning pattern read

For each major analyst action within ~48 hours, collect firm, analyst name,
rating change, target before → after, and the **stated rationale summarized
faithfully** — never infer a rationale the analyst did not give. Read the
pattern: target cuts with maintained Buy ratings signal a time-horizon debate
("right story, wrong quarter"), not an existential downgrade; downgrades with
target cuts signal a thesis change. Report which pattern dominates, and compare
the consensus PT delta with the stock's move — the gap is itself a finding.

## 7. Risk / catalyst matrix

The "what would change the narrative" table — the forward frame (Phase 8) in
post-mortem layout:

| Variable | Bear case if unresolved | Bull case if resolved | Observable trigger & timeline | Weight |
|---|---|---|---|---|

Rules: every row carries an **observable, dated trigger** (metric release,
guidance update, product milestone, regulatory docket — "sentiment improves" is
not a trigger); weight by impact on the structural debate, not by novelty; and
include at least one near-term (1–2 quarters) and one medium-term (4–8 quarters)
catalyst.

## 8. Metric emphasis by company type

| Company type | Prioritize | De-emphasize |
|---|---|---|
| Hyperscaler / AI infra (GOOGL, MSFT, AMZN, META, ORCL) | Capex/OCF, FCF, cloud backlog, AI monetization rate, lease commitments | Traditional P/E alone |
| Consumer hardware (AAPL) | Product revenue by line, gross margin, services attach, China exposure | Capex intensity |
| Semiconductor (NVDA) | Data-center revenue, backlog/bookings, gross margin, inventory days | FCF (usually strong) |
| EV / auto-tech (TSLA) | Deliveries, auto gross margin ex-credits, energy storage, regulatory credits | Traditional ad/cloud metrics |

Always compute FCF = OCF − Capex and show the capex/OCF ratio; a ratio above
100% means the company is funding growth with external capital or reserves.

## 9. Failure-mode catalog

- **Flat attribution** — listing three causes without ranking or durability
  classification. The reader cannot act on it.
- **"Accounting noise" hand-wave** — dismissing a GAAP miss without checking
  whether dilution or a cash fine is inside it (Phase 6 reconciliation exists
  for this).
- **Narrative-first** — starting from "AI fears" and selecting numbers to fit,
  instead of letting the FCF/capex data drive the ranking.
- **Peer omission** — analyzing FCF in isolation and calling it company failure
  when the whole sector is in a capex cycle (§5).
- **False precision** — inventing a percentage of the move attributable to each
  driver. Ordinal ranks by default; a quantified allocation only as a labeled
  `Reasoned` signed allocation whose sum-to-move identity is an arithmetic
  consistency check, never a measured decomposition.
- **Sell-side ventriloquism** — attributing a rationale to an analyst that they
  did not state (§6).
- **Confidence inflation** — writing "this confirms" when the evidence is
  `Reasoned` or `Assumed`.

## 10. Degraded mode (tools offline or rate-limited)

Web search and page-fetch tools are a hard dependency. When they fail:

1. Proceed only on figures already retrieved and verified in this session.
2. Tag every remaining gap `Unverifiable` (or `Assumed` with stated bounds) and
   list it in the **Data-Gap Ledger**: the exact source and pull needed to close
   it.
3. Never backfill a missing figure from memory or model prior knowledge —
   shrink the scope instead and say so.

## 11. Running lightweight mode inside this skill

The framework compresses onto the main pipeline as follows — the standalone
skill's nine steps are this pipeline at reduced depth, not a different method:

| Post-mortem step | Pipeline phase |
|---|---|
| 1 Pin the event mechanics | 0 Scope + 2 Reaction decomposition |
| 2 Financial scorecard vs consensus | 1 Fact base + 6 GAAP↔adjusted bridge |
| 3 Layered root-cause attribution | 3 Hypothesis tree + 4 Test & classify (§2 axes) + 5 Quantify |
| 4 Peer and industry context | 2 Cross-section + 7 Amplifiers |
| 5 Sell-side positioning | 5 Track the Street's response |
| 6 Risk/catalyst matrix | 8 Forward frame (§7 layout) |
| 7 Synthesis & confidence labeling | 8 Synthesis |
| 8 Verification ledger | 1 Fact base + closing ledger page |
| 9 Assemble the HTML deliverable | 9 Report production (single file) |

**Deliverable:** one self-contained HTML note with the seven-section sequence —
event box + executive summary (with KPI tiles: move, cap loss, EPS surprise,
FCF) → financial scorecard → layered root-cause decomposition → peer/industry
context → sell-side reaction → risk/catalyst matrix → verification ledger +
method note. Visual language: restrained, data-dense, institutional palette
with one accent, monospace numbers, tables over prose, no placeholder values.

**Audit gates do not relax for the lightweight deliverable.** Build the fact
base (`assets/fact_base.template.json`) for every figure in the note, name the
file `slide_01.html` in its own directory, and run both Phase 10 gates:

```bash
python3 scripts/fact_base_audit.py --slides <note_dir> --fact-base <fact_base.json>
node scripts/overflow_audit.mjs --dir <note_dir>
```

The note carries the same confidence legend, method note, and disclaimer as the
full deck: "Informational only — not investment advice, not a solicitation. No
price targets published."

## 12. Provenance and change discipline

Folded in from `big-tech-earnings-postmortem` (v1.1) as audit remediation for
the deferred P1/P2 roadmap items; the lightweight skill retains its operative
summary and defers to this file on divergence. Any doctrine change lands here
first, then mirrors into the family skills in the same commit — the
`tests/test_repo_consistency.py` suite fails the build on a restatement that
diverges from this canonical copy.
