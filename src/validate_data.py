"""Fail-fast validation and a machine-readable quality report."""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
QUALITY = ROOT / "data" / "quality"

PKS = {"branches":"branch_id","customers":"customer_id","accounts":"account_id","monthly_balances":"balance_snapshot_id","transactions":"transaction_id","loans":"loan_id","loan_payments":"payment_id","cards":"card_id","interactions":"interaction_id","fraud_cases":"case_id"}

def validate(raw: Path = RAW) -> dict:
    frames = {name: pd.read_csv(raw / f"{name}.csv") for name in PKS}
    checks = []
    def check(name: str, passed: bool, detail: str = ""):
        checks.append({"check":name,"passed":bool(passed),"detail":detail})
    for name, pk in PKS.items():
        check(f"{name}.primary_key_unique", frames[name][pk].is_unique)
        check(f"{name}.primary_key_not_null", frames[name][pk].notna().all())
    check("accounts.customer_fk", frames["accounts"].customer_id.isin(frames["customers"].customer_id).all())
    check("transactions.account_fk", frames["transactions"].account_id.isin(frames["accounts"].account_id).all())
    check("monthly_balances.account_fk", frames["monthly_balances"].account_id.isin(frames["accounts"].account_id).all())
    check("loans.customer_fk", frames["loans"].customer_id.isin(frames["customers"].customer_id).all())
    check("loan_payments.loan_fk", frames["loan_payments"].loan_id.isin(frames["loans"].loan_id).all())
    check("fraud_cases.transaction_fk", frames["fraud_cases"].transaction_id.isin(frames["transactions"].transaction_id).all())
    check("cards.customer_fk", frames["cards"].customer_id.isin(frames["customers"].customer_id).all())
    check("interactions.customer_fk", frames["interactions"].customer_id.isin(frames["customers"].customer_id).all())
    check("accounts.balance_nonnegative", frames["accounts"].current_balance.ge(0).all())
    check("transactions.amount_positive", frames["transactions"].amount.gt(0).all())
    check("transactions.risk_score_range", frames["transactions"].risk_score.between(0,1).all())
    check("loans.outstanding_lte_principal", frames["loans"].outstanding_amount.le(frames["loans"].principal_amount).all())
    check("monthly_balances.nonnegative", frames["monthly_balances"].ending_balance.ge(0).all())
    check("loan_payments.nonnegative", frames["loan_payments"][["scheduled_amount","paid_amount"]].ge(0).all().all())
    check("fraud.loss_only_if_confirmed", frames["fraud_cases"].loc[frames["fraud_cases"].confirmed_fraud.eq(0),"loss_amount"].eq(0).all())
    check("customers.digital_score_range", frames["customers"].digital_engagement_score.between(0,1).all())
    report = {"status":"PASS" if all(c["passed"] for c in checks) else "FAIL", "checks":checks, "row_counts":{k:len(v) for k,v in frames.items()}}
    return report

def main():
    report = validate()
    QUALITY.mkdir(parents=True, exist_ok=True)
    (QUALITY / "quality_report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    if report["status"] != "PASS":
        raise SystemExit(1)

if __name__ == "__main__":
    main()
