"""Generate a deterministic, relational synthetic retail-banking dataset."""
from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw"
SEED = 20260920

SCALES = {
    "test": (80, 700),
    "demo": (5_000, 120_000),
    "portfolio": (50_000, 1_500_000),
}

FIRST = np.array(["Aarav", "Aditi", "Arjun", "Divya", "Ishaan", "Kavya", "Meera", "Nikhil", "Priya", "Rahul", "Sai", "Sneha"])
LAST = np.array(["Reddy", "Sharma", "Patel", "Rao", "Iyer", "Khan", "Das", "Nair", "Gupta", "Singh"])
CITIES = np.array(["Hyderabad", "Bengaluru", "Chennai", "Mumbai", "Pune", "Delhi", "Kolkata", "Visakhapatnam"])
STATES = {"Hyderabad":"Telangana", "Bengaluru":"Karnataka", "Chennai":"Tamil Nadu", "Mumbai":"Maharashtra", "Pune":"Maharashtra", "Delhi":"Delhi", "Kolkata":"West Bengal", "Visakhapatnam":"Andhra Pradesh"}


def ids(prefix: str, n: int, width: int = 8) -> list[str]:
    return [f"{prefix}{i:0{width}d}" for i in range(1, n + 1)]


def build(scale: str) -> dict[str, pd.DataFrame]:
    n_customers, n_transactions = SCALES[scale]
    rng = np.random.default_rng(SEED)
    snapshot = pd.Timestamp("2026-08-31")

    branch_cities = np.resize(CITIES, 24)
    branches = pd.DataFrame({
        "branch_id": ids("BR", 24, 3),
        "branch_name": [f"{city} {i+1}" for i, city in enumerate(branch_cities)],
        "city": branch_cities,
        "state": [STATES[x] for x in branch_cities],
        "region": np.where(np.isin(branch_cities, ["Delhi", "Kolkata"]), "North/East", "South/West"),
        "opened_date": pd.to_datetime(rng.integers(pd.Timestamp("1998-01-01").value//10**9, pd.Timestamp("2022-01-01").value//10**9, 24), unit="s").date,
        "monthly_operating_cost": rng.integers(700_000, 2_200_000, 24),
    })

    age = np.clip(rng.normal(39, 12, n_customers).round(), 18, 78).astype(int)
    income = np.clip(rng.lognormal(np.log(720_000), .58, n_customers), 180_000, 7_500_000).round(0)
    city = rng.choice(CITIES, n_customers)
    join_days = rng.integers(60, 3650, n_customers)
    digital_score = np.clip(rng.beta(2.5, 1.7, n_customers), 0, 1)
    churn_prob = np.clip(.035 + .11*(digital_score < .25) + .07*(income < 350_000) + rng.normal(0,.025,n_customers), .01, .45)
    customers = pd.DataFrame({
        "customer_id": ids("CU", n_customers),
        "full_name": rng.choice(FIRST, n_customers) + " " + rng.choice(LAST, n_customers),
        "age": age,
        "gender": rng.choice(["Female", "Male", "Non-binary"], n_customers, p=[.48,.51,.01]),
        "city": city,
        "state": [STATES[x] for x in city],
        "occupation_segment": rng.choice(["Salaried", "Self-employed", "Professional", "Student", "Retired"], n_customers, p=[.48,.22,.13,.08,.09]),
        "annual_income": income,
        "risk_band": pd.cut(income, bins=[0,400_000,900_000,1_800_000,np.inf], labels=["High","Medium","Low","Very Low"]).astype(str),
        "join_date": (snapshot - pd.to_timedelta(join_days, unit="D")).date,
        "home_branch_id": rng.choice(branches.branch_id, n_customers),
        "digital_engagement_score": digital_score.round(4),
        "is_churned": rng.binomial(1, churn_prob),
    })

    n_accounts = int(n_customers * 1.38)
    account_customer = rng.choice(customers.customer_id, n_accounts, replace=True)
    account_type = rng.choice(["Savings", "Current", "Salary", "Fixed Deposit"], n_accounts, p=[.5,.13,.25,.12])
    balance = np.where(account_type == "Fixed Deposit", rng.lognormal(12.2, .8, n_accounts), rng.lognormal(10.2, 1.1, n_accounts))
    accounts = pd.DataFrame({
        "account_id": ids("AC", n_accounts),
        "customer_id": account_customer,
        "branch_id": rng.choice(branches.branch_id, n_accounts),
        "account_type": account_type,
        "open_date": (snapshot - pd.to_timedelta(rng.integers(20, 3000, n_accounts), unit="D")).date,
        "status": rng.choice(["Active", "Dormant", "Closed"], n_accounts, p=[.91,.06,.03]),
        "current_balance": balance.round(2),
        "interest_rate": np.select([account_type=="Savings",account_type=="Fixed Deposit",account_type=="Salary"],[2.7,7.1,2.5],default=0.0),
    })

    tx_accounts = rng.choice(accounts.account_id, n_transactions)
    channels = rng.choice(["UPI", "Mobile Banking", "Internet Banking", "ATM", "Branch", "POS"], n_transactions, p=[.38,.14,.1,.1,.06,.22])
    tx_type = rng.choice(["Debit", "Credit"], n_transactions, p=[.64,.36])
    amount = np.clip(rng.lognormal(8.0, 1.25, n_transactions), 10, 750_000)
    risk_score = np.clip(rng.beta(.8, 7, n_transactions) + (amount>150_000)*.3 + (channels=="ATM")*.03, 0, 1)
    event_days = rng.integers(0, 730, n_transactions)
    transactions = pd.DataFrame({
        "transaction_id": ids("TX", n_transactions, 10),
        "account_id": tx_accounts,
        "transaction_ts": snapshot - pd.to_timedelta(event_days, unit="D") + pd.to_timedelta(rng.integers(0,86400,n_transactions), unit="s"),
        "transaction_type": tx_type,
        "channel": channels,
        "merchant_category": rng.choice(["Grocery","Fuel","Travel","Healthcare","Education","Utilities","E-commerce","Transfer"], n_transactions),
        "amount": amount.round(2),
        "status": rng.choice(["Completed","Failed","Reversed"], n_transactions, p=[.965,.025,.01]),
        "risk_score": risk_score.round(4),
        "is_high_risk": (risk_score >= .72).astype(int),
    })

    n_loans = int(n_customers * .42)
    principal = np.clip(rng.lognormal(13, 1.0, n_loans), 50_000, 12_000_000)
    dpd = rng.choice([0,15,30,60,90,120], n_loans, p=[.77,.08,.06,.04,.03,.02])
    loans = pd.DataFrame({
        "loan_id": ids("LN", n_loans),
        "customer_id": rng.choice(customers.customer_id, n_loans, replace=False),
        "branch_id": rng.choice(branches.branch_id, n_loans),
        "loan_type": rng.choice(["Home","Personal","Vehicle","Education","Business"], n_loans, p=[.28,.26,.2,.1,.16]),
        "origination_date": (snapshot - pd.to_timedelta(rng.integers(45,2200,n_loans), unit="D")).date,
        "principal_amount": principal.round(2),
        "outstanding_amount": (principal*rng.uniform(.12,.96,n_loans)).round(2),
        "interest_rate": rng.uniform(7.5,19.5,n_loans).round(2),
        "term_months": rng.choice([12,24,36,60,120,180,240], n_loans),
        "days_past_due": dpd,
        "credit_score": np.clip(rng.normal(725,65,n_loans),450,850).round().astype(int),
        "loan_status": np.select([dpd>=90,dpd>=30],["Non-performing","Delinquent"],default="Current"),
    })

    cards = pd.DataFrame({
        "card_id": ids("CD", int(n_customers*.58)),
        "customer_id": rng.choice(customers.customer_id, int(n_customers*.58), replace=False),
        "card_type": rng.choice(["Classic","Gold","Platinum","Business"], int(n_customers*.58), p=[.4,.3,.22,.08]),
        "credit_limit": rng.choice([50_000,100_000,200_000,350_000,500_000], int(n_customers*.58)),
        "current_outstanding": np.clip(rng.lognormal(9.2,1.1,int(n_customers*.58)),0,450_000).round(2),
        "status": rng.choice(["Active","Blocked","Closed"], int(n_customers*.58), p=[.94,.03,.03]),
    })

    interactions = pd.DataFrame({
        "interaction_id": ids("IN", int(n_customers*.9)),
        "customer_id": rng.choice(customers.customer_id, int(n_customers*.9)),
        "interaction_date": (snapshot - pd.to_timedelta(rng.integers(0,730,int(n_customers*.9)), unit="D")).date,
        "channel": rng.choice(["Call Centre","Branch","Chat","Email","App"], int(n_customers*.9)),
        "reason": rng.choice(["Service request","Complaint","Loan enquiry","Card issue","KYC","Digital help"], int(n_customers*.9)),
        "resolution_hours": np.clip(rng.gamma(2.2,8,int(n_customers*.9)),.1,120).round(2),
        "satisfaction_score": rng.choice([1,2,3,4,5], int(n_customers*.9), p=[.04,.08,.18,.38,.32]),
    })
    return {"branches":branches,"customers":customers,"accounts":accounts,"transactions":transactions,"loans":loans,"cards":cards,"interactions":interactions}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", choices=SCALES, default="demo")
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    tables = build(args.scale)
    for name, frame in tables.items():
        frame.to_csv(args.output / f"{name}.csv", index=False)
        print(f"{name:14s} {len(frame):>10,} rows")


if __name__ == "__main__":
    main()

