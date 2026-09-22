# FinTrust Banking Intelligence

## What this report explains

FinTrust is a synthetic banking portfolio demonstration. Its six pages connect funding, lending, payments, fraud investigations, customer engagement and branch operating costs. Values describe the supplied demo data, not a real bank.

| Page | Decisions supported |
| --- | --- |
| Executive Overview | Compare deposit funding, loan exposure, overdue lending and collection execution. |
| Credit Risk & Collections | Prioritize products and branches with overdue exposure; examine repayment performance by due month. |
| Deposits & Transactions | Track month-end balances and channel activity; compare merchant categories and transaction execution. |
| Fraud & Investigations | Separate high-risk transaction flags from confirmed fraud and financial loss. |
| Customers & Digital | Identify customer segments, cities and risk bands needing retention or engagement attention. |
| Branch Performance | Compare branch funding, credit quality, overhead and cost per home-branch customer. |

## Data and grain

The original import queries still point to `C:\Users\janak\Downloads\FinTrust-Banking-Intelligence-main\FinTrust-Banking-Intelligence-main\data\raw`. No source data was regenerated.

| Table | Rows | Grain |
| --- | ---: | --- |
| customers | 5,000 | Customer |
| branches | 24 | Branch |
| accounts | 6,899 | Account |
| loans | 2,100 | Loan |
| transactions | 120,000 | Transaction |
| monthly_balances | 82,788 | Account-month snapshot |
| loan_payments | 33,740 | Scheduled instalment |
| cards | 2,900 | Card |
| interactions | 4,500 | Customer interaction |
| fraud_cases | 18 | Investigation case |
| Date | 730 | Calendar day, September 2024–August 2026 |

Monthly balance observations run from September 2025 to August 2026. The date dimension extends beyond the available balance observations; selecting an earlier period can correctly produce a blank balance.

## How filters work

Period, region, branch and customer segment slicers are synchronized across pages. Product/category slicers are page-specific. Use the page navigator to move between analyses without losing synchronized context. Standard chart selections cross-filter or highlight related visuals; use the slicers for an explicit selection.

| Filter | Effect and limits |
| --- | --- |
| Period | Uses transaction date, balance snapshot date, and instalment due date. It does not reconstruct historical customer, account or loan status. Investigation results follow the originating transaction date. |
| Region / branch | Filters accounts and loans, then their downstream transactions, balances, cases and payments. Customer/card presentation measures use customer home branch through `TREATAS`, without adding relationships. |
| Customer segment | Filters customers and downstream accounts, loans, cards, transactions and payments. Branch overhead remains the full cost of the selected branches. |
| Account type | Filters accounts, balances, transactions and related fraud cases. It does not filter loans or customer population backwards. |
| Loan type | Filters loans and instalments. |
| Transaction channel | Filters transactions and downstream investigations. |
| Customer risk band | Filters the customer population and its downstream business. |

An unchanged current-state KPI under a date selection is intentional, not evidence that the slicer is broken. Single-direction filtering deliberately prevents facts from filtering their parent dimensions backwards. A branch customer's account may belong to a different branch: customer counts use home branch, while balances and loans use their servicing branch.

The deposit KPI uses the latest available monthly snapshot within the selected period. It is not the sum of balances across multiple months. Current active-account balance is a different metric: **₹487.44M**, compared with **₹522.38M** for the latest monthly snapshot.

## Benchmark definitions

Unfiltered source results match the existing `data/analysis/executive_summary.json`:

| Metric | Value | Definition |
| --- | ---: | --- |
| Customers | 5,000 | Distinct customer IDs |
| Deposit balance | ₹522.38M | Latest month-end balance across accounts |
| Loan outstanding | ₹902.48M | Outstanding loan principal |
| 30+ DPD exposure ratio | 15.17% | Outstanding on loans at least 30 days overdue / total outstanding |
| 90+ DPD exposure ratio | 5.93% | Outstanding on loans at least 90 days overdue / total outstanding |
| Digital transaction share | 62.21% | Completed UPI, Mobile Banking and Internet Banking transactions / completed transactions |
| High-risk transaction rate | 0.02% | High-risk completed transactions / completed transactions |
| Customer churn rate | 5.32% | Churned customers / customers |
| Collection efficiency | 96.09% | Paid instalment amount / scheduled instalment amount |
| Investigation precision | 16.67% | Confirmed fraud cases / all investigation cases |

Investigation precision covers only 18 cases; it is not a population fraud-detection accuracy estimate. The existing Average Portfolio Yield measure is an unweighted average stated loan rate, so the visual calls it “Average loan rate.” CASA follows the preserved definition, including Current, Savings and Salary accounts.

DPD color rules are presentation thresholds: teal below 10%, amber from 10% to below 15%, red from 15%. They are not supplied credit-policy limits. Hover over charts for native data tooltips and use matrices for precise values.

## Model preservation

All original formulas and tables are retained. Technical ID columns are hidden from report view but remain available for relationships and calculations. Eight additional presentation measures support branch-scoped customer/card metrics, a last-available snapshot and a risk color. Existing relationships remain unchanged: 13 single-direction edges with no directed cycle or multiple directed filter paths.

The supplied build notes were reference material. The user's request controlled implementation and validation.

## Validation status

See `validation/source_validation.json` for reproducible source checks. These checks confirm all ten benchmark values, original formula preservation, unchanged relationship definitions, the directed relationship graph and report-canvas bounds. They do not replace Desktop testing.

The first Desktop opening successfully refreshed the original queries and rendered populated visuals. Formatting corrections were subsequently authored. Final Desktop validation, filter interaction checks, PBIX packaging and exports must be completed before declaring this deliverable final.

## Files and reproducibility

- `FinTrust_Banking_Intelligence.pbip`: editable project entry point.
- `FinTrust_Banking_Intelligence.Report`: six native PBIR pages, each with navigation, five slicers, five KPI cards, two charts, a matrix, heading, description and scope notes.
- `FinTrust_Banking_Intelligence.SemanticModel`: original model plus presentation measures and field visibility changes.
- `tools/build_report.py`: reproducible visual authoring script; run only with the project closed.
- `tools/validate_project.py`: read-only source and preservation checks.
- `backups/original_20260921_024611`: original PBIP components and working PBIX backup.

No Git commit or push has been performed. Both supplied directories are extracted folders without `.git` metadata or a verified remote. The user also required validation before committing.
