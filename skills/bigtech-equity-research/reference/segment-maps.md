# Reportable Segments — US Big Tech

Use the EDGAR 10-Q segment table as the source of truth. This map tells you what each company
reports and which lines typically move the stock.

| Company | Reportable segments | Primary price movers |
|---|---|---|
| **Alphabet (GOOGL)** | Google Services: Search & other · YouTube ads · Google Network · Subscriptions/Platforms/Devices; Google Cloud; Other Bets | Search growth; Cloud growth + margin; capex/FCF |
| **Microsoft (MSFT)** | Productivity & Business Processes (Office/LinkedIn/Dynamics); Intelligent Cloud (Azure/server); More Personal Computing (Windows/gaming/search ads) | Azure growth; capex; AI run-rate |
| **Amazon (AMZN)** | North America; International; AWS; Advertising | AWS growth + margin; ad growth; capex; retail margin |
| **Apple (AAPL)** | iPhone; Mac; iPad; Wearables/Home/Accessories; Services | iPhone units/ASP; Services growth + margin; China |
| **Meta (META)** | Family of Apps (advertising + other); Reality Labs | Ad revenue; DAP; Reality Labs losses; capex |
| **Nvidia (NVDA)** | Data Center; Gaming; Professional Visualization; Automotive; OEM | Data Center growth; guidance; gross margin; export limits |
| **Tesla (TSLA)** | Automotive; Energy Generation & Storage; Services & Other | Deliveries; auto margin; energy growth |

## Usage notes
- Identify the **cash-cow** segment (funds investment) and the **growth** segment (the story).
- For trend mode, pull 4–8 quarters of each segment to spot inflections.
- "Subscriptions/Devices" and "Other Bets"-style residual lines often require the 10-Q to split;
  if only the aggregate is available, report the residual and tag it `Unverifiable`.
