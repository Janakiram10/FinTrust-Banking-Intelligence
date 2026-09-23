# FinTrust Project Execution State

Last updated: 2026-09-23

## Completed

- Preserved the original PBIP, semantic model, validated DAX, 11 loaded tables, 13 relationships, and source CSVs.
- Created a timestamped recovery backup before report editing.
- Built six 16:9 Power BI pages with a consistent navy, white, teal, amber, and red banking theme.
- Added 108 native PBIR elements: page navigation, synchronized slicers, page-specific slicers, KPI cards, charts, matrices, page descriptions, and scope notes.
- Hid technical ID fields from report view without removing them from the model.
- Added presentation-only measures for last-available deposit snapshot, home-branch customer/card metrics, branch cost, and DPD risk coloring.
- Recomputed and matched all ten benchmark KPIs against the existing Python analysis output.
- Verified the original measures are preserved and the relationship graph remains single-direction, acyclic, and unambiguous.
- Opened and refreshed the authored PBIP in Power BI Desktop.
- Saved `FinTrust_Banking_Intelligence_FINAL.pbix` with the embedded model.
- Reopened the exact final PBIX, refreshed it successfully, and verified all six pages render.
- Tested the Region slicer on North/East and verified synchronized filter propagation across all six pages.
- Verified the final PBIX ZIP package has no corrupt archive member.
- Located and cloned the existing GitHub repository `Janakiram10/FinTrust-Banking-Intelligence`.
- Committed and pushed the validated Power BI deliverables and documentation to the `main` branch.

## Validated KPI baseline

- Customers: 5,000
- Latest deposit snapshot: ₹522.38M
- Loan outstanding: ₹902.48M
- 30+ DPD exposure: 15.17%
- 90+ DPD exposure: 5.93%
- Digital transaction share: 62.21%
- High-risk transaction rate: 0.02%
- Customer churn rate: 5.32%
- Collection efficiency: 96.09%
- Investigation precision: 16.67%

## Current task

- Phase 1 recruiter-facing portfolio assets are complete and ready for publication. The project repository README is ready to publish through Git; three account-bound actions remain because no authenticated editable Power BI, GitHub-profile or LinkedIn surface is available.

## Phase 1 completed

- Repositioned the repository README for a 60-second recruiter review with verified technologies, business scope, KPIs, insights, recommendations, validation and limitations.
- Created a truthful GitHub profile README draft centered on Data Analyst positioning and the FinTrust and MediCore projects.
- Created LinkedIn headline, About, experience, skill-priority, project and Featured-section content using official employment titles.
- Rewrote the FinTrust LinkedIn launch post with validated counts and accurate local lakehouse wording.
- Created and visually validated a one-page Data Analyst resume in editable DOCX and PDF formats with working GitHub project links.
- Added one exact manual Power BI export procedure for the six PNG files and consolidated PDF.

## Phase 1 blockers

- Power BI Desktop is not exposed to the current automation surface, so genuine dashboard PNG/PDF exports could not be captured automatically.
- LinkedIn is blocked in the available in-app browser and the LinkedIn connector is read-only for profile editing, so profile changes and the post are prepared but unpublished.
- The available public GitHub browser is signed out and the GitHub connector does not expose repository metadata or profile-repository creation, so profile README and About/topics changes are prepared but not published.

## Phase 1 deliverables

- Editable resume: `portfolio/resume/Palla_Janakiram_Data_Analyst_Resume.docx`
- Recruiter-ready resume: `portfolio/resume/Palla_Janakiram_Data_Analyst_Resume.pdf`
- GitHub profile copy: `portfolio/GITHUB_PROFILE_README.md`
- LinkedIn profile copy: `portfolio/LINKEDIN_PROFILE_FINAL.md`
- LinkedIn launch post: `docs/LINKEDIN_POST.md`
- Power BI export procedure: `assets/dashboard/EXPORT_INSTRUCTIONS.md`

## Phase 1 publication status

- Recruiter-facing asset commit: `7116d812b287fba6e6e16c2a79d021b641714c75`
- GitHub project repository: pushed to `origin/main` and verified on the public repository.
- GitHub profile README: complete locally; manual profile-repository publication required.
- LinkedIn profile and launch post: complete locally; manual authenticated paste required.
- Dashboard PNG/PDF assets: manual Power BI Desktop export required; exact instructions are recorded above.

## Final recruiter-positioning correction

- Standardized authoritative employment titles as `Analyst | Blue Dome Technologies` and `Senior Associate | Tech Mahindra` across the resume and LinkedIn preparation file.
- Standardized education as B.Tech Mechanical Engineering, WISTM / Andhra University, completed 2023, GPA 7.19/10; omitted unverified certifications.
- Regenerated the one-page resume and aligned LinkedIn, GitHub-profile and FinTrust README openings with Data Analyst-first positioning.

## Tier-3 completed locally

- Loaded 257,969 rows into ten genuine Bronze Delta tables with source, batch and ingestion metadata.
- Executed PySpark 4.0.1 transformations across all ten tables and wrote genuine Silver Delta outputs.
- Implemented checksum-based incremental ingestion; the duplicate rerun wrote zero rows and skipped ten unchanged files.
- Built eleven dbt models in a DuckDB SQL serving layer and passed all twelve dbt tests.
- Implemented and source-validated an eight-task Airflow DAG with retries, quality gates and reconciliation.
- Reconciled customer, loan, delinquency, digital, fraud-risk and churn metrics with the Power BI baseline.
- Added JSONL pipeline monitoring, lineage, Azure deployment path, execution evidence and interview guidance.

## Tier-3 cloud status

- Azure ADLS Gen2: BLOCKED BY CREDENTIALS.
- Azure Databricks and Databricks SQL: BLOCKED BY CREDENTIALS.
- Local ADLS-style storage, Delta Lake, PySpark, dbt, DuckDB serving and pipeline validation: IMPLEMENTED + VALIDATED.
- Airflow DAG: IMPLEMENTED LOCALLY and source/dependency validated; an Airflow scheduler was not started because native Windows is unsupported and Docker is unavailable.

## Known issue

- Windows application focus repeatedly shifted from Power BI to Codex during automated screenshot/PDF export. The final PBIX itself is validated; PDF/PNG export remains the only Power BI artifact not yet created.

## Files modified or created

- `FinTrust_Banking_Intelligence.Report/`
- `FinTrust_Banking_Intelligence.SemanticModel/`
- `FinTrust_Banking_Intelligence_FINAL.pbix`
- `REPORT_GUIDE.md`
- `POWER_BI_BUILD_NOTES.md`
- `validation/source_validation.json`
- `validation/DESKTOP_VALIDATION.md`
- `tools/build_report.py`
- `tools/validate_project.py`

## Tests completed

- Full source KPI reconciliation.
- Original-measure preservation check.
- Relationship definition and directed-graph checks.
- Six-page canvas-bound checks for all 108 report elements.
- Power BI Desktop open, refresh, render, final PBIX save, final PBIX reopen, and second refresh.
- Cross-page synchronized region filter test.
- PBIX package integrity check.

## Final validation status

The final PBIX remains working and validated. The Tier-3 local pipeline passes its layer checks, dbt build/tests, idempotent rerun test and KPI reconciliation. PDF/PNG dashboard exports remain pending because the Windows UI automation target repeatedly lost foreground focus.
