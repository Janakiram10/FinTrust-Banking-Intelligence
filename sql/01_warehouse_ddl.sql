-- Synapse/PostgreSQL-friendly dimensional model (adapt data types per engine).
CREATE SCHEMA IF NOT EXISTS fintrust;

CREATE TABLE fintrust.dim_customer (
  customer_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id VARCHAR(20) NOT NULL UNIQUE,
  age INT, gender VARCHAR(20), city VARCHAR(80), state VARCHAR(80),
  occupation_segment VARCHAR(40), annual_income DECIMAL(18,2),
  risk_band VARCHAR(20), join_date DATE, digital_engagement_score DECIMAL(6,4),
  is_churned SMALLINT, effective_from DATE, effective_to DATE, is_current SMALLINT
);

CREATE TABLE fintrust.dim_branch (
  branch_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  branch_id VARCHAR(20) NOT NULL UNIQUE,
  branch_name VARCHAR(100), city VARCHAR(80), state VARCHAR(80), region VARCHAR(40),
  monthly_operating_cost DECIMAL(18,2)
);

CREATE TABLE fintrust.fact_transaction (
  transaction_id VARCHAR(24) PRIMARY KEY,
  account_id VARCHAR(20) NOT NULL,
  customer_key BIGINT NOT NULL,
  branch_key BIGINT NOT NULL,
  transaction_ts TIMESTAMP NOT NULL,
  transaction_type VARCHAR(10), channel VARCHAR(40), merchant_category VARCHAR(40),
  amount DECIMAL(18,2), status VARCHAR(20), risk_score DECIMAL(6,4), is_high_risk SMALLINT
);

CREATE TABLE fintrust.fact_loan_snapshot (
  snapshot_date DATE NOT NULL,
  loan_id VARCHAR(20) NOT NULL,
  customer_key BIGINT NOT NULL,
  branch_key BIGINT NOT NULL,
  principal_amount DECIMAL(18,2), outstanding_amount DECIMAL(18,2),
  interest_rate DECIMAL(8,4), days_past_due INT, credit_score INT,
  loan_status VARCHAR(30), expected_loss_proxy DECIMAL(18,2),
  PRIMARY KEY(snapshot_date, loan_id)
);

