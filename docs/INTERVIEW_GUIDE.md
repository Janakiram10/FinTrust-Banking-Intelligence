# Interview Guide

## 60-second explanation

FinTrust is a synthetic retail-banking analytics platform that integrates customer, account, transaction, lending, card and service data. I designed the data at operational grain, added deterministic generation and quality gates, transformed it into dimensional marts with SQL/dbt and provided PySpark/Delta and Airflow reference implementations for a modern Azure architecture. The reporting layer focuses on profitability, credit deterioration, digital adoption, churn and transaction-risk signals. I explicitly label expected loss and fraud outputs as analytical proxies rather than regulatory or confirmed-fraud measures.

## Strong technical talking points

- Explain why DPD ratios are weighted by outstanding exposure.
- Explain why `transaction_id` uniqueness is checked before aggregation.
- Separate suspicious-activity signals from confirmed fraud.
- Describe Bronze/Silver/Gold responsibilities and replayability.
- Explain why presentation measures should not duplicate transformation logic.
- Be honest that cloud scripts are deployment-ready references unless you actually deploy them.

## Resume bullets

- Built an end-to-end retail-banking analytics platform integrating seven synthetic operational domains across Python, SQL, dbt, PySpark/Delta, Airflow and Power BI design artifacts.
- Designed governed KPIs for deposit mix, delinquency, exposure, churn, digital adoption and transaction-risk signals, with automated integrity and business-rule validation.
- Modeled Bronze/Silver/Gold and dimensional warehouse layers and documented an Azure Data Lake, Databricks and Synapse deployment path without exposing credentials or customer data.

