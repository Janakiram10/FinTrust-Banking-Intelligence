# Data Dictionary

The generator creates seven source tables. All IDs and names are synthetic.

## customers

`customer_id` primary key; demographics; geography; occupation and income; risk band; relationship date; home branch; digital engagement score; churn label.

## accounts

`account_id` primary key; customer and branch foreign keys; product type; open date; status; current balance and interest rate.

## transactions

`transaction_id` primary key; account foreign key; timestamp; debit/credit; channel; merchant category; amount; posting status; risk score and high-risk flag.

## loans

`loan_id` primary key; customer and branch foreign keys; loan product; origination; principal and outstanding balance; rate; term; DPD; credit score and loan status.

## cards

`card_id` primary key; customer foreign key; card tier; limit; outstanding and status.

## interactions

`interaction_id` primary key; customer foreign key; date; channel; reason; resolution time and satisfaction score.

## branches

`branch_id` primary key; name; geography; region; opening date and monthly operating cost.

