# Canonical Peer Baskets — US Big Tech

> **What this is.** The default peer sets for the family's peer comparisons (skill 2
> Step 4, skill 3 Phase 5, the flagship's Phase 2 cross-section), plus the selection
> criteria that make a peer legitimate. Comparative reports 6/7 (finding M-4/synthesized
> #9, "peer basket subjectivity"): "2–4 closest peers" with no criteria invites
> cherry-picking — comparing a mega-cap's capex to a mid-cap software name flatters or
> damns it by construction. The basket is stated in the deliverable, and any
> substitution is justified in one line.

## Selection criteria (the rule)

A peer is legitimate for a metric comparison when **all** of these hold:

1. **Same primary revenue driver** — the peer monetizes the same economic engine for the
   metric being compared (ad monetization, hyperscale cloud, data-center silicon,
   ecosystem/services, deliveries). "Big tech" alone is not a basis.
2. **Market-cap proximity** — within roughly one order of magnitude of the covered
   name. A $3T name and a $30B name do not face the same index-flow, liquidity, or
   investment-capacity regime.
3. **Same comparison axis** — the peer actually reports the metric on a comparable
   basis (capex/OCF, segment growth, gross margin ex-items). Where definitions differ,
   state the normalization.
4. **2–4 peers, basket stated** — fewer than 2 is not a comparison; more than 4 dilutes
   the read. The note names the basket and the criteria; every substitution from the
   defaults below carries a one-line reason.

## Default baskets

| Covered name | Default basket | Basis |
|---|---|---|
| **GOOGL** | META, MSFT, AMZN | Ads monetization + hyperscale cloud + the AI-infra capex cohort |
| **MSFT** | GOOGL, AMZN, ORCL | Hyperscale cloud + AI-infrastructure capex race |
| **AMZN** | MSFT, GOOGL, META | Cloud (AWS vs Azure vs GCP) + ads + the capex cycle |
| **META** | GOOGL, AMZN, MSFT | Digital-ads duopoly economics + AI-infra capex cohort |
| **AAPL** | MSFT, GOOGL | Large-cap platform/ecosystem economics and services attach; China-exposure reads are sourced separately, not peer-averaged |
| **NVDA** | AMD, AVGO | Accelerated-computing / data-center silicon cohort (outside the family's seven-name coverage universe, but the standard large-cap comp set) |
| **TSLA** | *(no default)* | No clean mega-cap comp on the auto-margin axis — see below |

**TSLA note.** Tesla has no large-cap peer that shares its primary revenue driver
(deliveries + auto gross margin ex-credits + energy storage). Build the basket per
comparison axis and justify each member in the note: auto gross margin ex-credits vs
the listed automakers that disclose it; energy-storage growth vs the storage names;
or the AI/robotics narrative vs the tech complex — never mix axes in one table.

**Sector tape (the Phase 2 cross-section)** is a different artifact from the metric
basket: it uses the family-wide mega-cap list (MSFT, META, AMZN, AAPL, NVDA at minimum)
to separate idiosyncratic repricing from systematic de-risking on the day. A name can
be in the cross-section without being in the metric basket and vice versa.

## Usage rules

- The defaults are priors, not straitjackets: an engagement may substitute when the
  metric demands it (e.g. comparing cloud growth may add ORCL for GOOGL/MSFT/AMZN) —
  state the basket and the reason.
- Same metric, same quarter, same basis for every basket member; a peer table mixing
  GAAP and non-GAAP margins is worse than no table.
- "Outlier or in line?" is the deliverable's question — a sector-wide capex cycle
  reframes a single name's FCF deficit as a regime, not a failure (skill 2 Step 4).
- Baskets are reference doctrine, not analysis: they change here first and mirror into
  the family skills in the same commit, per the canonical-copy discipline
  (`tests/test_repo_consistency.py` guards the wiring).

## Constituent hygiene (round 4, reports 8/9 M-8)

A static basket cached in this file is a survivorship-bias vector: M&A, spin-offs,
delistings, and bankruptcies silently remove or transform constituents, and a basket
that lost its distressed member flatters the peer average — making the covered name
look worse than it is. Before computing any peer cross-section or metric comparison:

1. **Corporate-action check per named constituent**: a T2 news check on each basket
   member (M&A, spin-off, delisting, bankruptcy, material restructuring) dated within
   the comparison window. These are **bespoke analyst baskets, not index
   constituents** — an index-membership API is the wrong control; the named-member
   news check is the right one.
2. **Cache-age gate**: if the basket's underlying facts (the quarter's metrics, the
   constituent list as verified) are >90 days old or undated, re-verify before use.
3. **Record the check**: state "Basket verified against corporate actions as of
   <date>" in the deliverable, and log any substitution the check forced.

The hygiene check is procedural (an agent-run news sweep), not a machine gate — the
Definition-of-Done checklists in the family skills pin it per engagement.
