# Tier-3 Interview Guide

**Why Azure and Databricks?** The dashboard is already a Microsoft Power BI asset, so ADLS and Databricks provide a natural governed lakehouse path. This repository executes the same layout locally because cloud credentials were unavailable.

**Why Spark instead of only Pandas?** The current demo is small, but the transaction transformation uses Spark operations that distribute cleanly when volume grows: deduplication, timestamp derivation, risk bucketing and partition columns. Pandas remains useful for compact validation tasks.

**Why Delta Lake?** Bronze and Silver are genuine Delta tables with transaction logs. That gives an ACID table boundary, schema control, history and a future MERGE path instead of loose Parquet files.

**What do Bronze, Silver and Gold mean here?** Bronze preserves the extract and ingestion metadata. Silver removes duplicate keys, standardizes values and derives analytics fields. Gold is built by dbt into customer/account dimensions and transaction/risk/fraud facts.

**Why dbt after PySpark?** Spark handles lake-scale physical processing; dbt expresses business-facing dimensional SQL, dependencies, tests and documentation. Keeping that boundary avoids repeating the same transformations.

**Why Airflow?** The DAG orders ingestion, layer checks, Spark processing, dbt build/tests, reconciliation and publishing. A failed quality gate stops downstream publication; tasks retry twice and overlapping runs are disabled.

**How does incremental loading work?** A SHA-256 watermark is recorded per source file. An unchanged rerun skips every file, producing zero new Bronze rows. A changed extract becomes a new batch; production would MERGE by business key and event timestamp for late arrivals.

**Why partition by transaction year and month?** Those columns support date-pruned processing without creating thousands of tiny daily partitions. The local demo keeps files compact; Databricks would apply physical partitioning or liquid clustering based on measured volume.

**How do schema and quality controls work?** Delta enforces written schemas; Silver validates primary keys and monetary rules. dbt tests uniqueness, nullability, relationships and accepted values. Reconciliation compares serving KPIs with the validated Power BI baseline.

**How are failures observed?** Each pipeline run writes a JSONL audit record with run ID, timing, status, row counts, skipped inputs, quality result and failure reason.

**How does Power BI consume the result?** Locally, DuckDB is the executed SQL serving layer. In Azure, the same Gold tables would be exposed through Databricks SQL; Power BI would map its existing semantic model and measures to those tables, then run the same reconciliation checks.

**What changes at production scale?** Use ADLS managed identity, Unity Catalog, Databricks Jobs, Delta MERGE, Auto Loader, centralized Airflow, alerts, Key Vault and Power BI Service incremental refresh. The trade-off is more governance and scalability for added platform cost and operational complexity.
