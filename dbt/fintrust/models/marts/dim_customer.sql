select customer_id, full_name, age, gender, city, state, occupation_segment, annual_income,
       risk_band, join_date, home_branch_id, digital_engagement_score, is_churned
from {{ ref('stg_customers') }}
