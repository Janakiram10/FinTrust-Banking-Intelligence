# Power BI Portfolio Export

The validated report is `FinTrust_Banking_Intelligence_FINAL.pbix`. The desktop automation surface was unavailable during the portfolio phase, so the following is the single required manual action.

1. Open the final PBIX in Power BI Desktop at 100% zoom.
2. Clear any temporary report filters and confirm each page renders.
3. Use full-screen or collapse the Filters, Data and Visualizations panes.
4. Capture each complete 16:9 canvas at the same pixel dimensions and save:
   - `01_executive_overview.png`
   - `02_credit_risk_collections.png`
   - `03_deposits_transactions.png`
   - `04_fraud_investigations.png`
   - `05_customers_digital.png`
   - `06_branch_performance.png`
5. Save the PNGs in this directory.
6. In Power BI Desktop select **File > Export > Export to PDF** and save all six pages as `FinTrust_Banking_Intelligence_Dashboard.pdf` in this directory.
7. Open the PDF once and confirm it contains six readable pages with no error dialogs.

After these files exist, replace the export-status paragraph in the root README with the Executive Overview image and the six-page gallery.
