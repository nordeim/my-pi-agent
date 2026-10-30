# Reportable Segments — US Big Tech

Use the EDGAR 10-Q/10-K segment table as the source of truth. This map distinguishes
**reportable segments** (ASC 280 — what the filing's segment note actually presents)
from **disclosed revenue lines** (product categories the company discloses in the
revenue note or MD&A but that are not reportable segments). Do not present a disclosed
revenue line as a "segment" — the variance table must mirror the filing's own segment
note or the auditor cannot tie it out.

Structures below reflect the FY2025/FY2026 10-Ks. Segment structures change
(divestitures, reorganizations, new GAAP segment rules) — re-verify against the latest
filing before use.

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
- **Apple unit volumes**: Apple ceased reporting unit sales in FY2019 (last disclosed Q4
  FY2018). Never quote or infer iPhone/Mac/iPad unit counts or ASPs from units — use
  reported **product revenue** and disclosed **installed-base** figures. Third-party unit
  estimates (IDC, Canalys) are `Unverifiable` unless a named report is actually sourced,
  and route to the Data-Gap Ledger.
- **Nvidia**: the market-platform table (Data Center, Gaming, …) is what the Street
  quotes, but the ASC 280 reportable segments are Compute & Networking and Graphics —
  label the platform rows accordingly in the variance table so they tie to the filing.
