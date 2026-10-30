# Sourcing Standards & Confidence Taxonomy

## Source hierarchy (best → acceptable)
1. SEC EDGAR filings (8-K, 10-Q, press release) — segment splits, balance sheet.
2. Official IR transcript / earnings-call audio.
3. Exchange-sourced or vendor price feeds (programmatic).
4. Named consensus source (FactSet, Visible Alpha, Bloomberg, Refinitiv/LSEG).
5. Wire services (Reuters, Bloomberg) and major outlets (CNBC) — for sell-side reactions,
   management quotes, and cross-checks.
6. Aggregators (TipRanks, Investing.com, Motley Fool) — acceptable for analyst PT changes and
   transcript cross-checks; verify the underlying number elsewhere.

**Never** present a figure reconstructed from memory. If the only source is a model's prior
knowledge, tag it `Assumed` and flag it.

## Confidence taxonomy (tag every figure)
- **Verified** — observed in ≥2 independent primary/near-primary sources, consistent to the
  reported precision.
- **Reasoned** — inference or computation from verified inputs. Round 3 splits it into two
  **mandatory sub-kinds** so an IC reader can tell reproducible math from opinion at the
  record level (reports 6/7 H-2):
  - **`Reasoned (derived)`** — deterministic derivation (FCF = OCF − Capex, delta arithmetic,
    GAAP bridges, options math). Must carry a formula and its parent inputs; reproducible and
    audit-checked. The parenthesized form or an explicit `epistemic_kind: derived` field both
    satisfy the flagship's schema gate.
  - **`Reasoned (judged)`** — analytical allocation or classification (driver-decomposition
    weights, structural-vs-cyclical calls). Signed, method disclosed, sum-checked when part
    of a decomposition — and explicitly non-causal: an arithmetic consistency check is not
    evidence of causation.
- **Assumed** — based on a stated assumption with explicit bounds (e.g. beta estimate when index
  closes are unavailable).
- **Unverifiable** — the environment cannot retrieve the source; listed in the Data-Gap Ledger
  with the exact pull needed.

## Consensus sourcing (round 3, reports 6/7 H-1; tightened round 4, reports 8/9 M-1)
Consensus figures are the denominator of every beat/miss delta and get tier discipline, not
convenience: named **provider** (FactSet / Visible Alpha / LSEG / Bloomberg as reported),
**vintage** (as-of date of the estimate set, within **1–3 trading days** of the event —
the CONSENSUS gate default is 5 calendar days ≈ 3 trading days), **statistic**
(`consensus_statistic`: mean / median / undisclosed — recorded even when the outlet does
not say which it prints; a $0.02-vs-$0.05 miss flips on it), **contributor
count** when disclosed, and a **T1/T2 source** — never a lone aggregator print; a single T2
chain must be cross-verified against a second distinct origination chain. State mean vs
median on the note when the outlet discloses which it prints. See
`reference/methodology.md` Phase 1.

## Anti-hallucination rules
- No invented API figures, index returns, implied moves, multiples, or filing numbers.
- No "executed verification" claims for price targets or forward guidance — those are reported
  third-party actions, not observable outcomes.
- Forward-looking statements are scenarios, never predictions.
- When tools are offline, shrink scope to verified-in-context data and expand the Data-Gap
  Ledger; never backfill with invented numbers.

## Disclaimer
Analysis only. Not investment advice, not a solicitation. All investments involve
risk. Internal analytical note — **not a research report** (round 4, reports 8/9 C-1):
internal use only, no client or external distribution, wider distribution requires
compliance sign-off. No rating, no price target, no analyst certification or conflict
disclosures. **Public-source-only** (round 4, reports 8/9 M-3): no channel checks,
expert calls, surveys, or management access inform the analysis — a stated limitation.
**Data licensing** (round 4, reports 8/9 M-4): vendor figures are cited with
attribution for internal analytical use; do not reproduce vendor tables at scale or
redistribute the deliverable externally. Built from public sources only; if any input is
suspected to be material non-public information (Regulation FD), stop and escalate.

**Position & mandate disclosure (round 3, reports 6/7 C-1, buy-side regime).**
When the deliverable is for an investment-committee audience, the note discloses the
**fund's position** in the covered name — "Fund position: long / short / none /
undetermined, as of <date>" — plus any mandate constraint or author conflict that
could bear on independence (CFA Institute Standard I(B); Advisers Act fiduciary
duty). This is the buy-side counterpart of sell-side conflict disclosure and is
what lets the committee discount the analysis for an existing position. The lite
audit's conditional needle fails an IC-facing note without it. (Reg AC / FINRA
2241 certification remains inapplicable: these notes are not distributed
sell-side research — the family's standing scoping position, per the round-2
rejection.)
