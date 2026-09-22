select account_id, customer_id, branch_id, account_type, open_date, status, current_balance from {{ ref('stg_accounts') }}
