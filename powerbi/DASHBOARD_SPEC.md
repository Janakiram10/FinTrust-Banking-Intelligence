# Power BI Dashboard Specification

## Global design

- Canvas: 16:9, light neutral background, navy/teal banking palette
- Persistent slicers: date, region, branch, customer segment, product
- KPI cards show value, period change and compact context—not decoration
- Every risk chart uses exposure-weighted metrics where applicable
- Tooltip pages explain metric definitions and caveats

## Pages

1. **Executive Overview** — deposits, loan outstanding, customers, income proxy, DPD30, churn; regional performance and 24-month trends.
2. **Customer 360** — value/risk segmentation, tenure, digital engagement, churn and service experience.
3. **Deposits & Transactions** — CASA mix, channel adoption, transaction value, failure/reversal rates and merchant categories.
4. **Credit Risk** — exposure, portfolio mix, DPD buckets, vintage view, credit-score bands and expected-loss proxy.
5. **Transaction Risk** — high-risk rate, amount/risk scatter, channel/merchant patterns and drill-through transaction table.
6. **Branch Performance** — deposit and loan portfolios, service score, operating-cost proxy and intervention quadrant.

## Required drill-through

- Branch detail
- Customer detail (synthetic IDs only)
- Loan portfolio segment

