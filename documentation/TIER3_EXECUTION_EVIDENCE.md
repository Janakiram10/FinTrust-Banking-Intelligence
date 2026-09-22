# Tier-3 Execution Evidence

Run date: 2026-09-22. The validated six-page Power BI report remains unchanged.

| Technology | Status | Implementation and validation | Evidence |
|---|---|---|---|
| Azure-style data lake | IMPLEMENTED LOCALLY | `landing`, `bronze`, `silver`, `gold/serving`, `checkpoints`, and `logs` conventions; immutable landing copies and file checksums | `lakehouse/pipeline.py`, `validation/tier3_quality.json` |
| Azure ADLS Gen2 | BLOCKED BY CREDENTIALS | Local paths map directly to ADLS containers; no Azure subscription or storage credentials were available | `documentation/AZURE_DEPLOYMENT.md` |
| Databricks | DESIGNED ONLY | Processing code is Databricks-portable, but no authenticated workspace/cluster was available | `lakehouse/pipeline.py` |
| PySpark / Apache Spark | IMPLEMENTED LOCALLY | Spark 4.0.1 performed native CSV reads, deduplication, type/date derivation, risk bucketing and partition columns across 257,969 rows | `monitoring/pipeline_runs.jsonl`, `validation/tier3_quality.json` |
| Delta Lake | IMPLEMENTED LOCALLY | Ten Bronze and ten Silver Delta tables were written with transaction logs; Bronze includes source, batch and ingestion metadata | `lakehouse/pipeline.py`, `validation/tier3_quality.json` |
| Medallion architecture | IMPLEMENTED LOCALLY | Bronze preserves source shape; Silver cleans, deduplicates and enriches; dbt builds dimensional Gold tables | `documentation/LINEAGE.md` |
| dbt | IMPLEMENTED + VALIDATED | dbt-duckdb built 11 models; 12 unique, not-null, relationship, accepted-value and business tests passed | `validation/dbt_build_summary.json`, `dbt/fintrust/target/manifest.json` generated locally |
| Airflow | DESIGNED ONLY | Eight-task quality-gated DAG with retries and single-active-run behavior; source and dependency chain validated, but no Airflow scheduler executed because Docker is unavailable and native Windows is unsupported | `airflow/dags/fintrust_daily_pipeline.py` |
| Serving layer | IMPLEMENTED + VALIDATED | DuckDB warehouse exposes dimensions, facts and daily channel mart for Power BI-compatible SQL access | `tools/tier3_validate.py` |
| Incremental processing | IMPLEMENTED + VALIDATED | SHA-256 checkpoint prevents reingestion; second run wrote zero rows and skipped ten unchanged files | `validation/incremental_rerun.json` |
| Data quality | IMPLEMENTED + VALIDATED | Layer row counts, key uniqueness, null keys, nonnegative amounts, relationships and KPI reconciliation execute as failure gates | `validation/tier3_quality.json` |
| Monitoring | IMPLEMENTED LOCALLY | JSONL log records run ID, timestamps, status, rows, skipped files, quality result, duration and failures | `monitoring/pipeline_runs.jsonl` |

The cloud-specific claims are intentionally limited. No paid Azure, Databricks, Synapse or Power BI capacity was created.
