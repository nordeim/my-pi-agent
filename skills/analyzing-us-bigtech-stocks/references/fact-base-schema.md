# Fact-Base Schema — Fields, Rules & Worked Examples

The fact base (`fact_base.json`) is the single source of truth for every number in the
report. The numeric audit script consumes it directly. If a number is not in the fact base,
it does not go in the report.

## Table of contents

1. [Top-level structure](#1-top-level-structure)
2. [Field definitions](#2-field-definitions)
3. [Confidence assignment rules](#3-confidence-assignment-rules)
4. [Derived facts](#4-derived-facts)
5. [Conflicts](#5-conflicts)
6. [Worked examples](#6-worked-examples)
7. [How the audit script consumes it](#7-how-the-audit-script-consumes-it)

---

## 1. Top-level structure

```json
{
  "meta": {
    "subject": "Alphabet Inc. (NASDAQ: GOOG / GOOGL)",
    "event": "Q3 FY2026 earnings release + conference call",
    "event_timestamp": "2026-10-28T16:05:00-04:00",
    "reaction_definition": "T+1 full-session close (2026-10-29)",
    "data_cutoff": "2026-10-30T13:00:00+08:00",
    "prepared": "2026-10-30",
    "method_page": "slide_15.html",
    "benchmarks": ["S&P 500", "Nasdaq-100", "MSFT", "META", "AMZN", "AAPL", "NVDA"]
  },
  "hypotheses": [
    { "id": "H1", "statement": "AI is visibly denting Search monetization",
      "lens": "(f) structural narrative", "verdict": "PRIMARY — narrative",
      "confidence": "High" }
  ],
  "facts": [ { ... }, { ... } ]
}
```

`meta.method_page` names the slide that carries the assumptions/method list — the page
the audit checks for `Assumed` facts (the final Sources & Confidence Ledger page by
convention; CLI override: `fact_base_audit.py --method-page <file>`).

The `hypotheses` array mirrors the Phase 3 tree; facts link to hypotheses via `supports`,
which makes the Phase 4 evidence assembly mechanical.

## 2. Field definitions

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes | Stable ID, `F-001`, `F-002`, … never reuse or renumber mid-engagement |
| `category` | enum | yes | `market_reaction` \| `fundamentals` \| `guidance` \| `capital_allocation` \| `one_off` \| `positioning` \| `macro` \| `peer` \| `sell_side` \| `narrative_metric` |
| `metric` | string | yes | Human-readable name ("Search & other revenue, Q3 2026") |
| `value` | number \| string | yes | The number as reported (keep exact decimals: `127.57`, not `127.6`) |
| `unit` | string | yes | `$B`, `%`, `count`, `ratio`, `date`, `text` |
| `as_of` | string | yes | Period the value pertains to ("Q3 2026", "2026-10-29 close") |
| `source_tier` | enum | yes | `T1` \| `T2` \| `T3` |
| `source_name` | string | yes | "Motley Fool — Alphabet Q3 2026 earnings call transcript" |
| `source_url` | string | yes | Resolvable URL; archived link if paywalled at retrieval |
| `retrieved_at` | string | yes | ISO timestamp of retrieval |
| `confidence` | enum | yes | `Verified` \| `Reasoned` \| `Assumed` \| `Unverifiable` |
| `cross_checked_with` | array | decision-critical | Other fact IDs or source names confirming the value |
| `supports` | array | yes | Hypothesis IDs this fact can evidence, e.g. `["H2"]`; `["deck"]` for general context |
| `slide_pages` | array | recommended | Page filenames where the number must appear — used by the audit |
| `derived_from` | array | derived only | Parent fact IDs |
| `formula` | string | derived only | The arithmetic shown on the slide, e.g. `"-9.1 + 5.2 = -3.9"` |
| `quote` | string | quotes/paraphrases | Exact source sentence captured at retrieval |
| `notes` | string | optional | Basis notes, hedged language, caveats |
| `conflict` | object | conflicts only | `{"with": "F-034", "resolution": "used transcript (T1) over press figure"}` |

## 3. Confidence assignment rules

| Label | Assign when | Audit consequence |
|---|---|---|
| `Verified` | Observed directly in ≥1 named source; decision-critical items cross-checked in ≥2 | Must have `source_url` + `retrieved_at`; spot-checked by audit |
| `Reasoned` | Computed or inferred from `Verified` parents | Must have `derived_from` + `formula` (or a stated inference chain); arithmetic-checked by audit |
| `Assumed` | Needed but unavailable; explicit modeling choice | Must appear on the method/assumptions page (`meta.method_page`) — enforced by audit; keep count at/near zero |
| `Unverifiable` | Source not retrievable with the tools at hand | Logged with the exact pull needed; never in headline statistics; listed with the final confidence legend |

Escalation discipline: never downgrade silently (`Verified` → `Reasoned` after a failed
cross-check means **record the conflict**, §5). Never upgrade (`Reasoned` ≠ `Verified` no
matter how obvious the inference).

## 4. Derived facts

Every computed figure gets its own row so the audit can chase the arithmetic:

```json
{ "id": "F-048", "category": "capital_allocation", "metric": "FCF ex-EU fine, Q3 2026",
  "value": -3.9, "unit": "$B", "as_of": "Q3 2026",
  "confidence": "Reasoned", "derived_from": ["F-042", "F-047"],
  "formula": "-9.1 + 5.2 = -3.9 (fine is a cash outflow inside FCF; removing it)",
  "supports": ["H2"], "slide_pages": ["slide_08.html"] }
```

Rules: percentages of sourced numbers are derived facts; market-cap deltas are derived facts
(shares outstanding × Δprice, with both parents); rankings are **never** derived — they are
either `Verified` from a named source or omitted.

## 5. Conflicts

When two sources disagree, keep both:

```json
{ "id": "F-051", "metric": "after-hours move, Oct 28", "value": "-10% to ~$290",
  "confidence": "Verified", "source_name": "AP (Oct 28)",
  "conflict": { "with": "F-052 (Morningstar: ~-9.5%)",
                "resolution": "quoted AP figure on slide; range stated in notes" } }
```

Silent resolution is the failure mode; a recorded resolution is a finding.

## 6. Worked examples

Real entries from the Alphabet Q3 2026 engagement (values verified across the cited sources
at retrieval time on 2026-10-28/30):

```json
{ "id": "F-001", "category": "market_reaction", "metric": "GOOG close, 2026-10-29",
  "value": 282.32, "unit": "$", "as_of": "2026-10-29 close",
  "source_tier": "T3", "source_name": "Yahoo Finance / CNN Markets",
  "source_url": "https://finance.yahoo.com/quote/GOOG",
  "retrieved_at": "2026-10-30T13:00:00+08:00", "confidence": "Verified",
  "cross_checked_with": ["CNN Markets", "F-002 (% move derived from pair)"],
  "supports": ["deck"], "slide_pages": ["slide_01.html", "slide_05.html"] }

{ "id": "F-014", "category": "fundamentals", "metric": "Google Search & other revenue vs consensus, Q3 2026",
  "value": "63.4 vs 64.9", "unit": "$B", "as_of": "Q3 2026",
  "source_tier": "T2", "source_name": "Yahoo Finance — Brian Sozzi (2026-10-29)",
  "source_url": "https://finance.yahoo.com/news/...", "retrieved_at": "2026-10-29T22:10:00+08:00",
  "confidence": "Verified", "cross_checked_with": ["Motley Fool transcript"],
  "supports": ["H1", "H6-exclusion"], "slide_pages": ["slide_02.html", "slide_04.html", "slide_07.html", "slide_11.html"] }

{ "id": "F-031", "category": "one_off", "metric": "OI&E — unrealized markdown, SpaceX stake",
  "value": -8.2, "unit": "$B", "as_of": "Q3 2026",
  "source_tier": "T1", "source_name": "Alphabet Q3 2026 earnings call transcript (Motley Fool)",
  "source_url": "https://www.fool.com/earnings/call-transcripts/...",
  "retrieved_at": "2026-10-29T20:00:00+08:00", "confidence": "Verified",
  "quote": "OI&E reflects an $8.2 billion unrealized loss, primarily on our investment in SpaceX (non-cash).",
  "supports": ["H3"], "slide_pages": ["slide_02.html", "slide_04.html", "slide_09.html"] }
```

## 7. How the audit script consumes it

`scripts/fact_base_audit.py` in fact-base mode:

1. For each fact, extracts numeric tokens from `value` (e.g. `282.32`, `-12.29`, `63.4`,
   `64.9`) and, if `slide_pages` is set, requires each page to contain all tokens; if
   `slide_pages` is absent, tokens must appear **somewhere** in the deck. Matching is
   **anchored**: a token matches only a complete number on the slide (sign/symbol
   tolerant), never a digit substring of a longer number — a fact of `82.3` cannot
   satisfy itself against a slide's `$282.32`.
2. Reverse mode: pulls every `$…B/%…/$…` pattern out of the visible slide text and
   reports tokens not covered by any fact as **unverified candidates** — a to-do list
   for the fact base, not automatically an error (words like "Fiscal 2026" can produce
   benign hits).
3. Always runs the placeholder scan (on visible text only — script/style blocks are
   not reader-visible) and checks that `Assumed` facts are listed on the method/
   assumptions page designated by `meta.method_page` (or `--method-page`). Assumed
   facts with no designated method page fail closed.
4. Evaluates every derived fact's `formula` of the form `LHS = RHS` (numbers and
   `+ - * / ( )` only, percent-aware): both sides must compute and agree. Formulas
   containing words are skipped, not failed.

Exit code 0 = clean; 1 = failures (fix before delivery); false positives are documented in
the delivery note, never ignored silently. `--selftest` proves all of the above works.
