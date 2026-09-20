# Azure Deployment Reference

1. Provision an Azure Data Lake Storage Gen2 account with `bronze`, `silver` and `gold` containers.
2. Upload generated source extracts to the Bronze landing path using managed identity.
3. Configure Azure Databricks access through an access connector; do not embed account keys.
4. Parameterize the ABFSS placeholders in `pyspark/` through environment-specific configuration.
5. Schedule Bronze-to-Silver validation and Silver-to-Gold aggregates as Databricks jobs.
6. Expose curated Gold tables through Synapse serverless SQL or load them into a dedicated SQL pool when scale justifies cost.
7. Connect Power BI to the curated layer, configure incremental refresh and enforce row-level security if required.
8. Send pipeline failures and data-quality results to monitoring before refreshing the semantic model.

The repository contains a deployable reference design, not proof of a live Azure deployment.

