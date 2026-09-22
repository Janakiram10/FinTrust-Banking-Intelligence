select loan_id, customer_id, branch_id, loan_type, origination_date, principal_amount,
       outstanding_amount, interest_rate, term_months, days_past_due, credit_score, loan_status
from {{ ref('stg_loans') }}
