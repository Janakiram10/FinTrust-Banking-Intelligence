select
  cast(transaction_id as varchar(24)) as transaction_id,
  cast(account_id as varchar(20)) as account_id,
  cast(transaction_ts as timestamp) as transaction_ts,
  transaction_type, channel, merchant_category,
  cast(amount as decimal(18,2)) as amount,
  status,
  cast(risk_score as decimal(6,4)) as risk_score,
  cast(is_high_risk as smallint) as is_high_risk
from {{ source('raw', 'transactions') }}
where amount > 0

