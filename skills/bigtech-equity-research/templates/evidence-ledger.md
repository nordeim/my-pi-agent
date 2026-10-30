# Evidence & Verification Ledger (Section 14)

Two tables in the deliverable appendix.

## Table 1 — Evidence ledger
| Claim | Source(s) | Confidence | Verification method |
|---|---|---|---|
| e.g. Revenue $127.58B | Earnings release; transcript; CNBC | Verified | Cross-checked ≥3 outlets, consistent to decimal |
| e.g. Benchmark −1.5% | Index closes unavailable | Assumed | Bounded −1.0 to −2.0; see Data-Gap Ledger |

## Table 2 — Data-Gap Ledger (everything Assumed/Unverifiable)
| Gap | Phase | Exact source / action to close |
|---|---|---|
| QQQ/XLK + comp closes | 2 (market-adjusted return) | Pull daily OHLC from exchange/vendor feed for event window |
| Pre-print ATM straddle | 2 (positioning) | Options chain for nearest expiry; implied vs realized |
| EDGAR segment split | 1 & 3 | EDGAR CIK → 8-K/10-Q → segment tables |
| Forward P/E vs band | 11 (Valuation Impact) | Valuation feed + forward consensus EPS |
| Intrinsic valuation (DCF/SOTP) | 11 (Valuation boundary) | The named open item: forward estimates + discount-rate framework + scenario weights |

## Method note (always include)
State the source hierarchy used, that no "executed verification" is claimed for price targets or
forward guidance, and that root-cause weights are `Reasoned (judged)` — analytical judgment, not
reported fact — while deterministic figures (deltas, bridges, options math) are `Reasoned
(derived)` with their formulas shown. The sum-to-move identity is an arithmetic consistency
check, not evidence of causation.
Also state the valuation boundary: no intrinsic valuation (DCF/SOTP/scenario-weighted fair
value) is produced — the forward-multiple band is context only, and the model gap is the
open item a valuation pass would close (forward estimates, discount-rate framework,
scenario weights). Close with the verification-status line matching the note's cover,
and the provenance seal line when the deliverable was sealed.
