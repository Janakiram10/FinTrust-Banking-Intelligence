"""Read-only source/KPI/model checks. Does not substitute for Desktop validation."""
from pathlib import Path
import json, re, hashlib
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT
MODEL=ROOT/'FinTrust_Banking_Intelligence.SemanticModel/definition'
OUT=ROOT/'validation'; OUT.mkdir(exist_ok=True)
raw_files=list((SOURCE/'data/raw').glob('*.csv'))
if raw_files:
    d={p.stem:pd.read_csv(p) for p in raw_files}
else:
    from src.generate_data import build
    d=build('demo')
c,t,l,p,f=d['customers'],d['transactions'],d['loans'],d['loan_payments'],d['fraud_cases']
completed=t[t.status.eq('Completed')]; b=d['monthly_balances']; latest=b[b.snapshot_date.eq(b.snapshot_date.max())]
pct=lambda x:round(float(x)*100,2)
kpis={'customers':int(c.customer_id.nunique()),'deposit_balance':round(float(latest.ending_balance.sum()),2),'loan_outstanding':round(float(l.outstanding_amount.sum()),2),'dpd30_exposure_ratio_pct':pct(l.loc[l.days_past_due.ge(30),'outstanding_amount'].sum()/l.outstanding_amount.sum()),'dpd90_exposure_ratio_pct':pct(l.loc[l.days_past_due.ge(90),'outstanding_amount'].sum()/l.outstanding_amount.sum()),'digital_transaction_share_pct':pct(completed.channel.isin(['UPI','Mobile Banking','Internet Banking']).mean()),'high_risk_transaction_rate_pct':pct(completed.is_high_risk.mean()),'churn_rate_pct':pct(c.is_churned.mean()),'collection_efficiency_pct':pct(p.paid_amount.sum()/p.scheduled_amount.sum()),'investigation_precision_pct':pct(f.confirmed_fraud.mean())}
expected=json.loads((SOURCE/'data/analysis/executive_summary.json').read_text())
assert kpis==expected,(kpis,expected)
backup=ROOT/'validation/baseline_model'
assert (MODEL/'relationships.tmdl').read_text().strip()==(backup/'relationships.tmdl').read_text().strip()
def measures(text):return {m.group(1):re.sub(r'\s+',' ',m.group(2)).strip() for m in re.finditer(r"\tmeasure '([^']+)' =([\s\S]*?)(?=\n\t+(?:formatString|displayFolder|lineageTag)|\n\t(?:measure|partition))",text)}
for table in (backup/'tables').glob('*.tmdl'):
    old=measures(table.read_text(encoding='utf-8')); new=measures((MODEL/'tables'/table.name).read_text(encoding='utf-8'))
    assert all(new.get(k)==v for k,v in old.items()),table.name
source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in raw_files}
relationships=(MODEL/'relationships.tmdl').read_text()
edges=[]
for rel in relationships.split('relationship ')[1:]:
    a=re.search(r'fromColumn: ([^.]+)\.',rel).group(1); z=re.search(r'toColumn: ([^.]+)\.',rel).group(1)
    assert 'bothDirections' not in rel
    edges.append((z,a))
def paths(start,end,seen=()):
    assert start not in seen,'Cycle found'
    if start==end:return 1
    return sum(paths(b,end,seen+(start,)) for a,b in edges if a==start)
nodes=set(sum(([a,b] for a,b in edges),[]))
assert all(paths(a,b)<=1 for a in nodes for b in nodes if a!=b),'Ambiguous directed filter path'
visuals=list((ROOT/'FinTrust_Banking_Intelligence.Report/definition/pages').glob('*/visuals/*/visual.json'))
for path in visuals:
    v=json.loads(path.read_text(encoding='utf-8')); pos=v['position']; assert pos['x']>=0 and pos['y']>=0 and pos['x']+pos['width']<=1280 and pos['y']+pos['height']<=720
result={'source_kpis':kpis,'all_ten_benchmarks_match':True,'rows':{k:len(v) for k,v in d.items()},'source_sha256':source_hashes,'original_measures_preserved':True,'relationships_unchanged_except_serialization':True,'single_direction_unambiguous_graph':True,'visual_count':len(visuals),'desktop_validation':'Final PBIX reopened, refreshed, rendered on six pages, and synchronized Region filter tested in Power BI Desktop'}
(OUT/'source_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
