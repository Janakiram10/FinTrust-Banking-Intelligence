# FinTrust Power BI Build Notes

## Current implementation and validation

The six pages now contain 108 native PBIR elements: page navigation, synchronized common slicers, page-specific category slicers, KPI cards, charts, matrices, headings and scope notes. The report uses a 1280 × 720 canvas and the FinTrust navy/white/teal theme.

Read `REPORT_GUIDE.md` for metric definitions, filter propagation, data grains and limitations. `tools/validate_project.py` verifies all ten source benchmarks and preservation of the original DAX and relationships. These checks pass.

Desktop successfully opened the project, refreshed the source queries, and displayed populated visuals. Subsequent formatting fixes and a duplicate hidden-property repair were applied; the corrected project opened with populated visuals. **Final page-by-page rendering at 100%, filter tests, FINAL.pbix save/reopen, and PDF/PNG exports are not complete.** Desktop automation repeatedly failed with minimized-window/user-input errors, including after session recovery. Do not treat the current project as finally validated.

The original PBIP components and working PBIX are backed up in `backups/original_20260921_024611`. No source dataset was regenerated. No original relationship or DAX formula was changed. Git commit/push remains pending: the supplied extracted directories have no Git metadata, and final validation is a prerequisite.

The recommendations below are the original reference notes, not a claim that the final verification has been completed.

## What is already automated

- Governed 11-table semantic model with 13 single-direction relationships.
- One shared Date dimension; Power BI auto-date tables are disabled.
- Forty reusable DAX measures grouped into business display folders.
- Six report pages named for the intended banking decision workflow.
- Chronological month sorting and Indian-rupee/percentage formatting.

## Recommended page visuals

### 01 Executive Overview

- KPI cards: Active Deposit Balance, Loan Outstanding, 30 Plus DPD Ratio, Collection Efficiency, Customer Churn Rate, Confirmed Fraud Loss.
- Combo chart: Date[Year Month], Latest Deposit Balance, Loan Outstanding.
- Matrix: branches[region], Active Deposit Balance, Loan Outstanding, 30 Plus DPD Ratio, Total Customers.

### 02 Credit Risk & Collections

- KPI cards: Loan Outstanding, 30 Plus DPD Exposure, 90 Plus DPD Exposure, Average Portfolio Yield, Collection Efficiency.
- Bar chart: loans[loan_type] by Loan Outstanding, colored by 30 Plus DPD Ratio.
- Line chart: Date[Year Month] by Late Payment Rate.
- Matrix: branches[branch_name], Loan Outstanding, 30 Plus DPD Ratio, 90 Plus DPD Ratio.

### 03 Deposits & Transactions

- KPI cards: Active Deposit Balance, CASA Ratio, Completed Transaction Value, Digital Transaction Share, Transaction Failure Rate.
- Line chart: Date[Year Month] by Latest Deposit Balance.
- Column chart: transactions[channel] by Completed Transaction Value.
- Bar chart: transactions[merchant_category] by Completed Transaction Value.

### 04 Fraud & Investigations

- KPI cards: High Risk Transaction Rate, Investigated Cases, Confirmed Fraud Cases, Investigation Precision, Confirmed Fraud Loss.
- Scatter plot: transactions[amount] by transactions[risk_score], legend transactions[is_high_risk].
- Matrix: transactions[merchant_category], Completed Transaction Value, High Risk Transaction Rate, Confirmed Fraud Loss.

### 05 Customers & Digital

- KPI cards: Total Customers, Customer Churn Rate, Average Digital Engagement, Active Cards, Card Utilization.
- Bar chart: customers[occupation_segment] by Total Customers and Customer Churn Rate.
- Column chart: customers[risk_band] by Average Digital Engagement.
- Matrix: customers[city], Total Customers, Active Deposit Balance, Customer Churn Rate.

### 06 Branch Performance

- KPI cards: Monthly Operating Cost, Cost per Customer, Active Deposit Balance, Loan Outstanding.
- Map: branches[city] sized by Active Deposit Balance.
- Matrix: branches[branch_name], Total Customers, Active Deposit Balance, Loan Outstanding, 30 Plus DPD Ratio, Cost per Customer.

## Final verification

Open `FinTrust_Banking_Intelligence.pbip` in Power BI Desktop. If prompted, refresh using the existing `data/raw` folder, confirm the model opens without errors, then save. Power BI Desktop is required to render the visuals and export final dashboard screenshots.
