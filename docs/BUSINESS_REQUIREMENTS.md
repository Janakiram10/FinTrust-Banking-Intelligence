# Business Requirements

## Scenario

FinTrust Bank is a fictional multi-state retail bank with 24 branches and rapidly growing digital transaction volumes. Leadership lacks a unified view across core banking, lending, cards, CRM and branch systems. Monthly reporting is slow, definitions vary between teams, and risk signals are reviewed separately from profitability.

## Decisions supported

1. Which branches and customer segments create sustainable value?
2. Where is credit quality deteriorating and how much exposure is at risk?
3. Which customers show churn risk and what value is attached to them?
4. Which channels drive adoption, failures and elevated transaction risk?
5. Where do service problems overlap with attrition or financial risk?

## Stakeholders

| Stakeholder | Primary decision |
|---|---|
| CEO / COO | Growth, profitability and operating intervention |
| CFO | Income and balance-sheet proxies |
| Chief Risk Officer | Delinquency, exposure and expected-loss proxy |
| Retail Banking Head | Product, branch and customer performance |
| Digital Head | Adoption, channel reliability and engagement |
| Service Head | Complaints, resolution and satisfaction |

## Non-functional requirements

- Reproducible from code without sensitive data
- Metric definitions separated from dashboard visuals
- Traceable source-to-mart transformations
- Automated tests fail before presentation refresh
- Cloud-ready but runnable locally at no cost

