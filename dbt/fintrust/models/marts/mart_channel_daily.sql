select
  cast(transaction_ts as date) as transaction_date,
  channel,
  count(*) as transaction_count,
  sum(amount) as transaction_value,
  avg(cast(is_high_risk as decimal(8,4))) as high_risk_rate
from {{ ref('stg_transactions') }}
where status = 'Completed'
group by cast(transaction_ts as date), channel

