# Reportable Segments — US Big Tech

> **Map version:** `segment_map_version: 2026-10` · `last_verified_against_filing:
> FY2025/FY2026 10-Ks` (verified 2026-10-30 against the filed 10-K segment notes).

Use the EDGAR 10-Q/10-K segment table as the source of truth. This map distinguishes
**reportable segments** (ASC 280 — what the filing's segment note actually presents)
from **disclosed revenue lines** (product categories the company discloses in the
revenue note or MD&A but that are not reportable segments). Do not present a disclosed
revenue line as a "segment" — the variance table must mirror the filing's own segment
note or the auditor cannot tie it out.

**Staleness rule (hard):** before building any variance table, compare this map's
`last_verified_against_filing` above with the filing you are actually using. If your
filing is newer (a more recent 10-K/10-Q, or a filing whose segment note restructures
the map below), re-verify the segment structure against that filing's own segment note
first and update this map (bump `segment_map_version`, set the new
`last_verified_against_filing`) — a variance table tied to a stale map will not tie
out to the current filing, and nothing downstream will catch it. Segment structures
change (divestitures, reorganizations, new GAAP segment rules) — treat the map as a
cached verification, never as the filing itself.

| Company | Reportable segments (ASC 280) | Disclosed revenue lines (not segments) | Primary price movers |
|---|---|---|---|
| **Alphabet (GOOGL)** | Google Services; Google Cloud; Other Bets | Within Services: Search & other, YouTube ads, Google Network, Subscriptions/Platforms/Devices | Search growth; Cloud growth + margin; capex/FCF |
| **Microsoft (MSFT)** | Productivity & Business Processes; Intelligent Cloud; More Personal Computing | Azure and other cloud services (disclosed within Intelligent Cloud) | Azure growth; capex; AI run-rate |
| **Amazon (AMZN)** | North America; International; AWS | Advertising services; subscription services (disclosed revenue lines, not segments) | AWS growth + margin; ad growth; capex; retail margin |
| **Apple (AAPL)** | Geographic: Americas; Europe; Greater China; Japan; Rest of Asia Pacific | Product categories: iPhone, Mac, iPad, Wearables/Home/Accessories, Services | iPhone revenue + installed-base growth; Services growth + margin; China (Greater China segment) |
| **Meta (META)** | Family of Apps; Reality Labs | Within FoA: advertising, other revenue | Ad revenue; DAP; Reality Labs losses; capex |
| **Nvidia (NVDA)** | Compute & Networking; Graphics | Market platforms within Compute & Networking: Data Center, Networking, Automotive, Professional Visualization; Gaming and OEM & Other within Graphics | Data Center revenue growth; guidance; gross margin; export limits |
| **Tesla (TSLA)** | Automotive; Energy Generation and Storage; Services and Other | — | Deliveries; auto margin ex-credits; energy growth |

## Usage notes

- Identify the **cash-cow** segment (funds investment) and the **growth** segment (the story).
- For trend mode, pull 4–8 quarters of each segment to spot inflections.
- "Subscriptions/Devices" and "Other Bets"-style residual lines often require the 10-Q to split;
  if only the aggregate is available, report the residual and tag it `Unverifiable`.
- The variance table cites the filing it ties to (form type + fiscal period) so a reader
  can check it against the map version above.
- **Apple unit volumes**: Apple ceased reporting unit sales in FY2019 (last disclosed Q4
  FY2018). Never quote or infer iPhone/Mac/iPad unit counts or ASPs from units — use
  reported **product revenue** and disclosed **installed-base** figures. Third-party unit
  estimates (IDC, Canalys) are `Unverifiable` unless a named report is actually sourced,
  and route to the Data-Gap Ledger.
- **Nvidia**: the market-platform table (Data Center, Gaming, …) is what the Street
  quotes, but the ASC 280 reportable segments are Compute & Networking and Graphics —
  label the platform rows accordingly in the variance table so they tie to the filing.
