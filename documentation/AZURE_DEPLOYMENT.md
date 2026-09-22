# Azure Deployment Path

The repository executes locally without cloud charges. Azure deployment requires authenticated resources and is therefore **BLOCKED BY CREDENTIALS**.

1. Create one ADLS Gen2 account and containers matching `landing`, `bronze`, `silver`, `gold`, `checkpoints`, and `logs`.
2. Upload immutable extracts to `landing` and replace local paths with `abfss://` configuration values.
3. Import `lakehouse/pipeline.py` into an Azure Databricks job and use a managed identity or service principal through a secret scope.
4. Persist Gold tables in Unity Catalog and expose them through one Databricks SQL warehouse.
5. Point Power BI to that SQL endpoint, map the existing tables, and re-run KPI reconciliation before publishing.
6. Configure `RangeStart` and `RangeEnd` parameters for transaction-date incremental refresh in Power BI Service.

No credentials belong in Git. Production would use Key Vault, private endpoints, RBAC, diagnostic logs and environment-specific job parameters.
