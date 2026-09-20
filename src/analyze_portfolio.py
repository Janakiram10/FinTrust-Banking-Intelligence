"""Generate reproducible executive KPIs from validated source data."""
import json
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/"data"/"raw"; OUT=ROOT/"data"/"analysis"
def pct(x): return round(float(x)*100,2)
def main():
    d={p.stem:pd.read_csv(p) for p in RAW.glob("*.csv")}
    c,t,l,p,f=d["customers"],d["transactions"],d["loans"],d["loan_payments"],d["fraud_cases"]
    completed=t[t.status.eq("Completed")]
    latest=d["monthly_balances"].query("snapshot_date == snapshot_date.max()")
    m={"customers":int(c.customer_id.nunique()),"deposit_balance":round(float(latest.ending_balance.sum()),2),
       "loan_outstanding":round(float(l.outstanding_amount.sum()),2),
       "dpd30_exposure_ratio_pct":pct(l.loc[l.days_past_due.ge(30),"outstanding_amount"].sum()/l.outstanding_amount.sum()),
       "dpd90_exposure_ratio_pct":pct(l.loc[l.days_past_due.ge(90),"outstanding_amount"].sum()/l.outstanding_amount.sum()),
       "digital_transaction_share_pct":pct(completed.channel.isin(["UPI","Mobile Banking","Internet Banking"]).mean()),
       "high_risk_transaction_rate_pct":pct(completed.is_high_risk.mean()),"churn_rate_pct":pct(c.is_churned.mean()),
       "collection_efficiency_pct":pct(p.paid_amount.sum()/p.scheduled_amount.sum()),
       "investigation_precision_pct":pct(f.confirmed_fraud.mean())}
    OUT.mkdir(parents=True,exist_ok=True); (OUT/"executive_summary.json").write_text(json.dumps(m,indent=2))
    lines=["# Executed Portfolio Findings","","Generated from the reproducible synthetic demo dataset.",""]+[f"- **{k.replace('_',' ').title()}:** {v:,}" for k,v in m.items()]
    lines += ["","## Guardrails","","- Delinquency is exposure-weighted.","- High-risk events are signals, not confirmed fraud.","- Findings demonstrate methodology, not a real bank's performance."]
    (OUT/"FINDINGS.md").write_text("\n".join(lines)+"\n"); print(json.dumps(m,indent=2))
if __name__=="__main__": main()
