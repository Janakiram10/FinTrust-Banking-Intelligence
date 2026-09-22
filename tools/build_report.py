"""Author native PBIR visuals against the preserved FinTrust semantic model."""
from pathlib import Path
import json, re, hashlib

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'FinTrust_Banking_Intelligence.Report'
MODEL = ROOT / 'FinTrust_Banking_Intelligence.SemanticModel' / 'definition'
NAVY, TEAL, BG, INK, MUTED, RED = '#102A43', '#008C95', '#F2F6FA', '#17324D', '#62788C', '#C54646'
def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding='utf-8')
def lit(v):
    return {'expr': {'Literal': {'Value': ("'"+v.replace("'", "''")+"'") if isinstance(v,str) else str(v).lower() if isinstance(v,bool) else str(v)+'D'}}}
def color(v): return {'solid': {'color': lit(v)}}
def obj(**kw): return [{'properties':kw}]

# Add report-specific measures; never rewrite existing validated formulas.
additions = {
 'monthly_balances': [('Selected Deposit Balance', '''VAR LastSnapshot = MAX(monthly_balances[snapshot_date])
RETURN CALCULATE([Deposit Balance Snapshot], KEEPFILTERS(monthly_balances[snapshot_date] = LastSnapshot))''', '₹#,0,,.00"M"')],
 'customers': [
 ('Branch Customers', '''IF(ISCROSSFILTERED(branches), CALCULATE([Total Customers], KEEPFILTERS(TREATAS(VALUES(branches[branch_id]), customers[home_branch_id]))), [Total Customers])''', '#,0'),
 ('Branch Churn Rate', '''IF(ISCROSSFILTERED(branches), CALCULATE([Customer Churn Rate], KEEPFILTERS(TREATAS(VALUES(branches[branch_id]), customers[home_branch_id]))), [Customer Churn Rate])''','0.00%'),
 ('Branch Digital Engagement', '''IF(ISCROSSFILTERED(branches), CALCULATE([Average Digital Engagement], KEEPFILTERS(TREATAS(VALUES(branches[branch_id]), customers[home_branch_id]))), [Average Digital Engagement])''','0.0')],
 'cards': [('Branch Active Cards', '''IF(ISCROSSFILTERED(branches), CALCULATE([Active Cards], KEEPFILTERS(TREATAS(VALUES(branches[branch_id]), customers[home_branch_id]))), [Active Cards])''','#,0'),
 ('Branch Card Utilization', '''IF(ISCROSSFILTERED(branches), CALCULATE([Card Utilization], KEEPFILTERS(TREATAS(VALUES(branches[branch_id]), customers[home_branch_id]))), [Card Utilization])''','0.00%')],
 'branches': [('Branch Cost per Customer', 'DIVIDE([Monthly Operating Cost], [Branch Customers])','₹#,0')],
 'loans': [('DPD Risk Color', 'IF([30 Plus DPD Ratio] >= 0.15, "#C54646", IF([30 Plus DPD Ratio] >= 0.10, "#BC7A19", "#008C95"))','')]
}
for table, measures in additions.items():
    p = MODEL/'tables'/f'{table}.tmdl'
    text = p.read_text(encoding='utf-8')
    for name, expression, fmt in measures:
        if f"measure '{name}'" in text: continue
        definition = f"\n\tmeasure '{name}' =\n" + '\n'.join('\t\t\t'+s for s in expression.splitlines())+'\n'
        if fmt: definition += f'\t\tformatString: {fmt}\n'
        definition += '\t\tdisplayFolder: Report Presentation\n'
        text = text.replace(f'\tpartition {table} =', definition+f'\tpartition {table} =')
    p.write_text(text,encoding='utf-8')
for p in (MODEL/'tables').glob('*.tmdl'):
    text=p.read_text(encoding='utf-8')
    def hide_id(m):
        block=m.group(0)
        if re.match(r'\tcolumn [^\n]*_id\n',block):
            block=block.replace('\t\tisHidden\n','')
            block=block.replace('\n','\n\t\tisHidden\n',1)
        return block
    text=re.sub(r'\tcolumn [\s\S]*?(?=\n\t(?:column|measure|partition|annotation) |\Z)',hide_id,text)
    p.write_text(text,encoding='utf-8')

measures={}
for p in (MODEL/'tables').glob('*.tmdl'):
    for m in re.findall(r"\tmeasure '([^']+)'",p.read_text(encoding='utf-8')): measures[m]=p.stem
def field(t,n,measure=False): return {('Measure' if measure else 'Column'):{'Expression':{'SourceRef':{'Entity':t}},'Property':n}}
def proj(t,n,measure=False,label=None):
    d={'field':field(t,n,measure),'queryRef':f'{t}.{n}','nativeQueryRef':n}
    if label: d['displayName']=label
    if measure:
        if any(s in n for s in ['Ratio','Rate','Share','Efficiency','Precision','Utilization','Yield']): d['format']='0.00%'
        elif any(s in n for s in ['Balance','Outstanding','Exposure','Value','Loss','Cost','Amount']): d['format']='₹#,0,,.00"M"' if 'per Customer' not in n else '₹#,0'
    return d
def mp(n,label=None): return proj(measures[n],n,True,label)
def cp(t,n): return proj(t,n)

def visual(page,name,kind,x,y,w,h,title='',roles=None,objects=None,bg='#FFFFFF'):
    v={'$schema':'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json','name':name,'position':{'x':x,'y':y,'width':w,'height':h,'z':len(list(page.glob('visuals/*'))),'tabOrder':len(list(page.glob('visuals/*')))},'visual':{'visualType':kind,'drillFilterOtherVisuals':True,'visualContainerObjects':{'title':obj(show=lit(bool(title)),text=lit(title),fontColor=color(INK),fontSize=lit(12),bold=lit(True),fontFamily=lit('Segoe UI')),'background':obj(show=lit(True),color=color(bg),transparency=lit(0)),'border':obj(show=lit(False)),'visualHeader':obj(show=lit(False))}}}
    if roles: v['visual']['query']={'queryState':{k:{'projections':ps} for k,ps in roles.items()}}
    if objects: v['visual']['objects']=objects
    save(page/'visuals'/name/'visual.json',v)
    return v
def text(page,name,text,x,y,w,h,size=12,fg=INK,bg=BG):
    return visual(page,name,'textbox',x,y,w,h,objects={'general':obj(paragraphs=[{'textRuns':[{'value':text,'textStyle':{'fontSize':f'{size}pt','fontFamily':'Segoe UI','color':fg}}]}])},bg=bg)
def card(page,index,name,label):
    label=label.replace('Latest deposit snapshot','Deposit snapshot').replace('Completed transaction value','Completed value').replace('Current active CASA mix','Active CASA mix').replace('Average stated rate','Average loan rate').replace('Cost per home customer','Cost / home customer')
    v=visual(page,f'kpi{index}','card',24+index*248,182,236,90,label,{'Values':[mp(name)]},{'labels':obj(color=color(TEAL if index!=2 else INK),fontSize=lit(25),labelDisplayUnits=lit(1)),'categoryLabels':obj(show=lit(False))})
    if name=='30 Plus DPD Ratio':
        v['visual']['objects']['labels'][0]['properties']['color']={'solid':{'color':{'expr':field('loans','DPD Risk Color',True)}}}
        save(page/'visuals'/f'kpi{index}'/'visual.json',v)
def chart(page,name,kind,category,ms,x,y,w,h,title):
    roles={'Category':[cp(*category)],'Y':[mp(m) for m in ms]}
    for pr in roles['Y']:
        if 'format' in pr and 'M' in pr['format']:pr['format']='₹#,0.00'
    visual(page,name,kind,x,y,w,h,title,roles,{'categoryAxis':obj(show=lit(True),fontSize=lit(10),showAxisTitle=lit(False)),'valueAxis':obj(show=lit(True),fontSize=lit(10),showAxisTitle=lit(False)),'legend':obj(show=lit(len(ms)>1)),'dataPoint':obj(defaultColor=color(TEAL))})
def matrix(page,category,ms,title):
    v=visual(page,'detailmatrix','pivotTable',24,488,1232,190,title,{'Rows':[cp(*category)],'Values':[mp(m) for m in ms]}, {'grid':obj(rowPadding=lit(5),gridVertical=lit(False)),'columnHeaders':obj(fontColor=color('#FFFFFF'),backColor=color(NAVY),fontSize=lit(11)),'values':obj(fontSize=lit(11)),'rowHeaders':obj(fontSize=lit(11))})
    if '30 Plus DPD Ratio' in ms:
        v['visual']['objects']['values'].append({'selector':{'metadata':'loans.30 Plus DPD Ratio'},'properties':{'fontColor':{'solid':{'color':{'expr':field('loans','DPD Risk Color',True)}}}}})
        save(page/'visuals/detailmatrix/visual.json',v)

configs=[
 ('9c29942aa1b78802630c','Executive Overview','Balance sheet strength, portfolio risk and collection discipline',
 [('Branch Customers','Customers'),('Selected Deposit Balance','Latest deposit snapshot'),('Loan Outstanding','Loan outstanding'),('30 Plus DPD Ratio','30+ DPD exposure'),('Collection Efficiency','Collection efficiency')],
 [('deposittrend','lineChart',('Date','Year Month'),['Selected Deposit Balance'],'Track month-end funding strength'),('regionrisk','clusteredBarChart',('branches','region'),['Loan Outstanding'],'Where lending exposure is concentrated')],
 ('branches','region'),['Selected Deposit Balance','Loan Outstanding','30 Plus DPD Ratio','Branch Customers'], 'Compare regional funding and credit exposure',('accounts','account_type'),
 'Date filters snapshots and collections; loan exposure and customers are current-state. Customer counts use home branch.'),
 ('creditrisk001','Credit Risk & Collections','Prioritize overdue exposure and monitor repayment execution',
 [('Loan Outstanding','Loan outstanding'),('30 Plus DPD Exposure','30+ DPD exposure'),('90 Plus DPD Ratio','90+ DPD exposure'),('Average Portfolio Yield','Average stated rate'),('Collection Efficiency','Collection efficiency')],
 [('loanmix','clusteredBarChart',('loans','loan_type'),['Loan Outstanding'],'Focus collections by lending product'),('paymenttrend','lineChart',('Date','Year Month'),['Collection Efficiency','Late Payment Rate'],'Track collection efficiency and late payments')],
 ('branches','branch_name'),['Loan Outstanding','30 Plus DPD Ratio','90 Plus DPD Ratio','Collection Efficiency'], 'Prioritize branches with overdue exposure',('loans','loan_type'),
 'Date uses instalment due date for collections. Loan exposure is a current snapshot; DPD ratios are exposure-weighted.'),
 ('deposits001','Deposits & Transactions','Monitor funding stability, channel adoption and transaction execution',
 [('Selected Deposit Balance','Latest deposit snapshot'),('CASA Ratio','Current active CASA mix'),('Completed Transaction Value','Completed transaction value'),('Digital Transaction Share','Digital transaction share'),('Transaction Failure Rate','Transaction failure rate')],
 [('deposittrend','lineChart',('Date','Year Month'),['Selected Deposit Balance'],'Track month-end deposit balances'),('channels','clusteredBarChart',('transactions','channel'),['Completed Transaction Value'],'Identify channels carrying transaction value')],
 ('transactions','merchant_category'),['Completed Transaction Value','Completed Transactions','Digital Transaction Share','High Risk Transaction Rate'], 'Inspect transaction quality by merchant category',('accounts','account_type'),
 'Date filters transaction date and balance snapshot date. CASA uses current active accounts; digital share uses completed transactions.'),
 ('fraud001','Fraud & Investigations','Separate risk signals from confirmed outcomes and financial loss',
 [('High Risk Transaction Rate','High-risk transaction rate'),('Investigated Cases','Investigated cases'),('Confirmed Fraud Cases','Confirmed fraud cases'),('Investigation Precision','Investigation precision'),('Confirmed Fraud Loss','Confirmed fraud loss')],
 [('riskchannels','clusteredBarChart',('transactions','channel'),['High Risk Transaction Rate'],'Locate channels with elevated risk signals'),('cases','clusteredColumnChart',('fraud_cases','case_status'),['Investigated Cases'],'Review investigation workload by status')],
 ('transactions','merchant_category'),['Completed Transactions','High Risk Transaction Rate','Investigated Cases','Confirmed Fraud Loss'], 'Compare risk signals with confirmed losses',('transactions','channel'),
 'High-risk flags are signals, not proven fraud. Date filters the originating transaction, not the investigation opening date.'),
 ('customers001','Customers & Digital','Identify retention needs and opportunities for digital engagement',
 [('Branch Customers','Customers'),('Branch Churn Rate','Customer churn rate'),('Branch Digital Engagement','Digital engagement score'),('Branch Active Cards','Active cards'),('Branch Card Utilization','Card utilization')],
 [('segments','clusteredBarChart',('customers','occupation_segment'),['Branch Customers'],'Identify the customer segments that matter'),('engagement','clusteredColumnChart',('customers','risk_band'),['Branch Digital Engagement'],'Compare engagement across customer risk bands')],
 ('customers','city'),['Branch Customers','Branch Churn Rate','Branch Digital Engagement','Active Deposit Balance'], 'Target retention and engagement by customer city',('customers','risk_band'),
 'Customer and card KPIs are current-state; date does not time-travel them. Region and branch scope customers by home branch.'),
 ('branches001','Branch Performance','Compare branch scale, operating cost and credit quality',
 [('Monthly Operating Cost','Monthly operating cost'),('Branch Cost per Customer','Cost per home customer'),('Selected Deposit Balance','Latest deposit snapshot'),('Loan Outstanding','Loan outstanding'),('30 Plus DPD Ratio','30+ DPD exposure')],
 [('regionalfunding','clusteredBarChart',('branches','region'),['Selected Deposit Balance'],'Compare regional funding capacity'),('regionalrisk','clusteredBarChart',('branches','region'),['30 Plus DPD Ratio'],'Locate regional delinquency pressure')],
 ('branches','branch_name'),['Branch Customers','Selected Deposit Balance','Loan Outstanding','30 Plus DPD Ratio','Branch Cost per Customer'], 'Balance branch scale, credit quality and cost',('accounts','account_type'),
 'Costs are monthly branch overhead, not allocated by product or segment. Customer denominator uses home branch; date filters deposits.')
]
for idx,(pid,title,desc,kpis,charts,cat,ms,mt,product,note) in enumerate(configs):
    page=REPORT/'definition/pages'/pid
    p=json.loads((page/'page.json').read_text(encoding='utf-8'))
    p.update(width=1280,height=720,displayOption='FitToPage',displayName=title)
    p['objects']={'background':obj(color=color(BG),transparency=lit(0))}
    save(page/'page.json',p)
    text(page,'brand',f'FINTRUST  /  {title.upper()}',0,0,1280,43,22,'#FFFFFF',NAVY)
    text(page,'description',desc,24,45,1232,26,11,MUTED)
    visual(page,'navigation','pageNavigator',24,74,1232,30,objects={'text':obj(fontSize=lit(10),fontColor=color(NAVY))},bg=BG)
    slicers=[('Date','Year Month','Period'),('branches','region','Region'),('branches','branch_name','Branch'),('customers','occupation_segment','Customer segment'),(*product,'Product / category')]
    for i,(t,n,label) in enumerate(slicers):
        v=visual(page,f'filter{i}','slicer',24+i*248,110,236,64,label,{'Values':[cp(t,n)]},{'data':obj(mode=lit('Dropdown')),'header':obj(show=lit(False)),'items':obj(textSize=lit(10)),'selection':obj(singleSelect=lit(False),selectAllCheckboxEnabled=lit(True))})
        if i<4:
            v['visual']['syncGroup']={'groupName':f'FinTrust_{t}_{n}','fieldChanges':True,'filterChanges':True}
            save(page/'visuals'/f'filter{i}'/'visual.json',v)
    for i,(m,label) in enumerate(kpis):card(page,i,m,label)
    for i,(name,kind,category,values,ct) in enumerate(charts):chart(page,name,kind,category,values,24+i*624,280,608,196,ct)
    matrix(page,cat,ms,mt)
    text(page,'scope_note',note,24,684,1190,30,9,MUTED)
    text(page,'page_number',f'{idx+1:02d} / 06',1212,684,60,30,9,MUTED)

theme={'name':'FinTrust Premium','dataColors':[TEAL,NAVY,'#4D9FCE','#BC7A19',RED,'#8EA6B8'],'background':'#FFFFFF','foreground':INK,'tableAccent':TEAL,'good':TEAL,'neutral':'#BC7A19','bad':RED,'textClasses':{'label':{'fontFace':'Segoe UI','fontSize':10},'title':{'fontFace':'Segoe UI Semibold','fontSize':12},'callout':{'fontFace':'Segoe UI Semibold','fontSize':27}}}
save(REPORT/'StaticResources/RegisteredResources/FinTrustPremium.json',theme)
report_path=REPORT/'definition/report.json'
r=json.loads(report_path.read_text(encoding='utf-8'))
r['themeCollection']['customTheme']={'name':'FinTrustPremium','reportVersionAtImport':{'visual':'2.4.0','report':'3.3.0','page':'2.1.0'},'type':'RegisteredResources'}
r['resourcePackages']=[rp for rp in r['resourcePackages'] if rp['name']!='RegisteredResources']+[{'name':'RegisteredResources','type':'RegisteredResources','items':[{'name':'FinTrustPremium','path':'FinTrustPremium.json','type':'CustomTheme'}]}]
save(report_path,r)
pages_path=REPORT/'definition/pages/pages.json'
ps=json.loads(pages_path.read_text(encoding='utf-8')); ps['activePageName']=configs[0][0]; save(pages_path,ps)
print('Authored',len(list((REPORT/'definition/pages').glob('*/visuals/*/visual.json'))),'native visuals across six pages. Desktop validation remains required.')
