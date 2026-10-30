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
- **Reasoned** — logical inference/derivation from verified inputs (e.g. waterfall weights,
  implied consensus OCF, structural-vs-cyclical classification). Method disclosed.
- **Assumed** — based on a stated assumption with explicit bounds (e.g. beta estimate when index
  closes are unavailable).
- **Unverifiable** — the environment cannot retrieve the source; listed in the Data-Gap Ledger
  with the exact pull needed.

## Anti-hallucination rules
- No invented API figures, index returns, implied moves, multiples, or filing numbers.
- No "executed verification" claims for price targets or forward guidance — those are reported
  third-party actions, not observable outcomes.
- Forward-looking statements are scenarios, never predictions.
- When tools are offline, shrink scope to verified-in-context data and expand the Data-Gap
  Ledger; never backfill with invented numbers.

## Disclaimer
Analysis only. Not investment advice, not a solicitation. All investments involve
risk. Internal analytical note — not for distribution as sell-side research: no
rating, no price target, no analyst certification or conflict disclosures. Built
from public sources only; if any input is suspected to be material non-public
information (Regulation FD), stop and escalate.
