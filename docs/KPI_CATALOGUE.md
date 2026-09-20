# KPI Catalogue

| KPI | Definition | Grain / filter | Caveat |
|---|---|---|---|
| Deposit balance | Sum of current balance for active deposit accounts | Snapshot, account | Synthetic point-in-time proxy |
| CASA ratio | Current + savings + salary balances / eligible deposit balances | Snapshot | Product mapping must be governed |
| Loan outstanding | Sum of current outstanding loan principal | Loan snapshot | Excludes undrawn limits |
| 30+ DPD ratio | Outstanding on loans with DPD >= 30 / total outstanding | Loan snapshot | Exposure-weighted, not account-count rate |
| 90+ DPD ratio | Outstanding on loans with DPD >= 90 / total outstanding | Loan snapshot | Portfolio-risk indicator |
| Expected loss proxy | Outstanding × PD proxy × LGD proxy | Loan snapshot | Educational proxy, not IFRS 9/ECL |
| Digital transaction share | Completed UPI/mobile/internet transactions / completed transactions | Period | Count-based; value share is separate |
| High-risk transaction rate | High-risk completed transactions / completed transactions | Period/channel | Rule-derived signal, not confirmed fraud |
| Churn rate | Churned customers / eligible customers | Customer snapshot | Synthetic label |
| At-risk customer value | Deposits plus exposure attached to churn/risk flags | Customer snapshot | Do not interpret as recoverable revenue |
| Branch cost-to-income proxy | Monthly operating cost / estimated branch income | Month/branch | Proxy, not audited financial reporting |

