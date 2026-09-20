-- 1. Branch risk-adjusted portfolio view
SELECT b.branch_name,
       SUM(l.outstanding_amount) AS loan_outstanding,
       SUM(CASE WHEN l.days_past_due >= 30 THEN l.outstanding_amount ELSE 0 END)
         / NULLIF(SUM(l.outstanding_amount), 0) AS dpd30_ratio,
       SUM(l.expected_loss_proxy) AS expected_loss_proxy
FROM fintrust.fact_loan_snapshot l
JOIN fintrust.dim_branch b ON b.branch_key = l.branch_key
WHERE l.snapshot_date = (SELECT MAX(snapshot_date) FROM fintrust.fact_loan_snapshot)
GROUP BY b.branch_name
ORDER BY expected_loss_proxy DESC;

-- 2. Digital adoption and high-risk rate by channel
SELECT channel,
       COUNT(*) AS transactions,
       SUM(amount) AS value,
       AVG(CAST(is_high_risk AS DECIMAL(8,4))) AS high_risk_rate
FROM fintrust.fact_transaction
WHERE status = 'Completed'
GROUP BY channel
ORDER BY transactions DESC;

-- 3. At-risk customer value
SELECT c.customer_id, c.city, c.annual_income,
       SUM(l.outstanding_amount) AS loan_exposure,
       MAX(l.days_past_due) AS max_dpd
FROM fintrust.dim_customer c
JOIN fintrust.fact_loan_snapshot l ON l.customer_key = c.customer_key
WHERE c.is_current = 1 AND (c.is_churned = 1 OR l.days_past_due >= 30)
GROUP BY c.customer_id, c.city, c.annual_income
ORDER BY loan_exposure DESC;

