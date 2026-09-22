# Desktop validation record

## Observed passes

- Opened the supplied working PBIX: six empty report pages and eleven loaded model tables were visible.
- Backed up that PBIX and all original PBIP components before editing.
- Opened the authored PBIP in Power BI Desktop.
- Ran Home > Refresh. The refresh dialog completed, the incomplete-data warning disappeared, and visuals populated.
- Executive matrix showed ₹522.38M deposits, ₹902.48M loans and 15.17% overdue exposure. Cards showed 5,000 customers and 96.09% collection efficiency.
- Corrected double display-unit scaling and rejected untyped numeric formatting properties after visual inspection.
- Corrected duplicate `isHidden` metadata detected on reopening.
- Reopened the corrected project successfully with populated visuals and preserved imported model cache.
- Independently recomputed all ten source benchmarks; all match the original Python summary.
- Verified all original formulas, all 13 relationships and the unambiguous directed graph; the report contains six 16:9 pages and 108 native elements within canvas bounds.

## Final validation completed

- Saved `FinTrust_Banking_Intelligence_FINAL.pbix` with the embedded model.
- Reopened that exact PBIX and refreshed all source queries successfully.
- Inspected all six pages in Desktop; titles, KPIs, slicers, charts, matrices, navigation, page notes and risk colors render.
- Tested the Region slicer with North/East. It synchronized across all six pages and changed customer, deposit, lending, collections, transaction, fraud, card and branch metrics consistently.
- Re-ran source reconciliation and model-preservation checks after final save.
- Verified PBIX ZIP package integrity.

## Remaining artifact limitation

The final PBIX is validated. PDF/PNG export was interrupted by repeated foreground-focus loss between Power BI Desktop and Codex. This affects only the additional static exports, not the report, model, refresh, KPI reconciliation, or filter behavior.
