-- Exposure-weighted delinquency by product
SELECT loan_type,SUM(outstanding_amount) outstanding,
 SUM(CASE WHEN days_past_due>=30 THEN outstanding_amount ELSE 0 END)/NULLIF(SUM(outstanding_amount),0) dpd30_ratio,
 SUM(CASE WHEN days_past_due>=90 THEN outstanding_amount ELSE 0 END)/NULLIF(SUM(outstanding_amount),0) dpd90_ratio
FROM raw.loans GROUP BY loan_type ORDER BY outstanding DESC;

-- Origination vintage deterioration
SELECT EXTRACT(YEAR FROM origination_date) vintage_year,loan_type,COUNT(*) loans,AVG(credit_score) avg_score,AVG(days_past_due) avg_dpd,SUM(outstanding_amount) outstanding
FROM raw.loans GROUP BY EXTRACT(YEAR FROM origination_date),loan_type;

-- Collection efficiency by delinquency state
SELECT l.loan_status,SUM(p.paid_amount)/NULLIF(SUM(p.scheduled_amount),0) collection_efficiency
FROM raw.loan_payments p JOIN raw.loans l ON l.loan_id=p.loan_id GROUP BY l.loan_status;

-- Investigation precision by score band
SELECT CASE WHEN t.risk_score>=.9 THEN '0.90+' WHEN t.risk_score>=.8 THEN '0.80-0.89' ELSE '0.72-0.79' END risk_band,
 COUNT(*) investigated,AVG(CAST(f.confirmed_fraud AS DECIMAL(8,4))) confirmed_rate,SUM(f.loss_amount) confirmed_loss
FROM raw.fraud_cases f JOIN raw.transactions t ON t.transaction_id=f.transaction_id GROUP BY 1;

-- Month-over-month deposit movement
SELECT snapshot_date,SUM(ending_balance) deposits,
 SUM(ending_balance)-LAG(SUM(ending_balance)) OVER(ORDER BY snapshot_date) absolute_change
FROM raw.monthly_balances GROUP BY snapshot_date ORDER BY snapshot_date;
