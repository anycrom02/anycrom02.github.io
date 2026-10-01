"""Minimal midpoint decomposition of G06N/G06T shares; preserve all EDA files.
Run: bundled Python 04_analysis/decompose_ipc_change.py
"""
from pathlib import Path
import json, hashlib, platform
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'04_analysis/ipc_change_decomposition';OUT.mkdir(exist_ok=True)
FIG=ROOT/'05_output/ipc_change_decomposition';FIG.mkdir(exist_ok=True)
preserved=[ROOT/'03_processed_data/patent_metadata_full.csv',ROOT/'04_analysis/eda_portfolio.py',ROOT/'04_analysis/eda_report.md']+list((ROOT/'04_analysis/eda').glob('*'))+list((ROOT/'05_output/eda').glob('*'))
def hashes():return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in preserved if p.is_file()}
before_hashes=hashes()
d=pd.read_csv(ROOT/'03_processed_data/patent_metadata_full.csv',dtype=str,keep_default_na=False)
lk=pd.read_csv(ROOT/'04_analysis/eda/patent_company_analysis.csv',dtype=str,keep_default_na=False)
lk=lk[['application_number','selection_id','company_name_official']].drop_duplicates()
assert not lk.duplicated(['application_number','selection_id']).any()
d['year']=pd.to_datetime(d.application_date).dt.year
d=d[d.year.between(2014,2024)].copy()
d['period']=np.where(d.year<=2018,'2014-2018','2019-2024')
d['subclasses']=d.ipc_json.map(lambda x:sorted({v[:4] for v in json.loads(x)}))
for code in ['G06N','G06T']:
    d[code]=d.subclasses.map(lambda a:float(code in a)/len(a))
p=lk.merge(d[['application_number','period','G06N','G06T']],on='application_number',validate='many_to_one')
# Preserve unique-patent totals exactly: a patent linked to m selected firms gives 1/m to each.
p['attribution']=1/p.groupby('application_number').selection_id.transform('size')
for code in ['G06N','G06T']:p[code+'_mass']=p[code]*p.attribution
g=p.groupby(['selection_id','company_name_official','period']).agg(patent_mass=('attribution','sum'),G06N_mass=('G06N_mass','sum'),G06T_mass=('G06T_mass','sum')).reset_index()
periods=['2014-2018','2019-2024']
sets=[set(g[g.period==t].selection_id) for t in periods]
C=sets[0]&sets[1];E=sets[1]-sets[0];X=sets[0]-sets[1]
g['group']=g.selection_id.map(lambda sid:'common' if sid in C else ('later_only' if sid in E else 'earlier_only'))
for code in ['G06N','G06T']:g[code+'_share']=g[code+'_mass']/g.patent_mass
def save(name,t):t.to_csv(OUT/f'{name}.csv',index=False,encoding='utf-8-sig')
save('company_period_shares',g)
coverage=[]
for t in periods:
    for group in ['common','earlier_only','later_only']:
        z=g[(g.period==t)&(g.group==group)]
        coverage.append({'period':t,'group':group,'companies':z.selection_id.nunique(),'patent_mass':z.patent_mass.sum(),'share_of_all_patents':z.patent_mass.sum()/len(d[d.period==t]),'G06N_mass':z.G06N_mass.sum(),'G06T_mass':z.G06T_mass.sum()})
save('coverage_groups',pd.DataFrame(coverage))
totals=[len(d[d.period==t]) for t in periods]
cg=[g[(g.period==t)&g.selection_id.isin(C)].set_index('selection_id').reindex(sorted(C)) for t in periods]
alpha=[z.patent_mass.sum()/n for z,n in zip(cg,totals)]
avg_alpha=sum(alpha)/2
w=[z.patent_mass/z.patent_mass.sum() for z in cg]
results=[];contributions=[];details=[];sensitivity=[];ordering=[]
for code in ['G06N','G06T']:
    s=[z[code+'_share'] for z in cg]
    common_share=[float((wt*st).sum()) for wt,st in zip(w,s)]
    within=avg_alpha*(w[0]+w[1])/2*(s[1]-s[0])
    weight=avg_alpha*(s[0]+s[1])/2*(w[1]-w[0])
    common_mean=sum(common_share)/2
    zE=g[(g.period==periods[1])&g.selection_id.isin(E)]
    zX=g[(g.period==periods[0])&g.selection_id.isin(X)]
    entering=(zE[code+'_mass'].sum()-zE.patent_mass.sum()*common_mean)/totals[1]
    exiting=-(zX[code+'_mass'].sum()-zX.patent_mass.sum()*common_mean)/totals[0]
    shares=[d[d.period==t][code].mean() for t in periods]
    delta=shares[1]-shares[0]
    values={'within_common_firms':float(within.sum()),'reweighting_common_firms':float(weight.sum()),'later_only_composition':float(entering),'earlier_only_composition':float(exiting)}
    assert abs(sum(values.values())-delta)<1e-12
    old=pd.read_csv(ROOT/'04_analysis/eda/ipc_period_share.csv')
    for t,share in zip(periods,shares):assert abs(float(old[(old.period==t)&(old.ipc_subclass==code)].share_pct.iloc[0])/100-share)<1e-12
    row={'ipc_subclass':code,'share_early_pct':shares[0]*100,'share_late_pct':shares[1]*100,'change_pp':delta*100,'common_share_early_pct':common_share[0]*100,'common_share_late_pct':common_share[1]*100,'within_pp':values['within_common_firms']*100,'reweighting_pp':values['reweighting_common_firms']*100,'later_only_pp':entering*100,'earlier_only_pp':exiting*100,'within_share_of_change_pct':values['within_common_firms']/delta*100,'reweighting_share_of_change_pct':values['reweighting_common_firms']/delta*100,'composition_share_of_change_pct':(entering+exiting)/delta*100,'identity_residual_pp':(delta-sum(values.values()))*100}
    results.append(row)
    for term,val in values.items():details.append({'ipc_subclass':code,'component':term,'contribution_pp':val*100,'share_of_change_pct':val/delta*100})
    # The midpoint allocates the interaction equally. Check both sequential endpoints.
    for order in ['shares_then_weights','weights_then_shares']:
        if order=='shares_then_weights':
            wi=avg_alpha*float((w[0]*(s[1]-s[0])).sum())
            rw=avg_alpha*float((s[1]*(w[1]-w[0])).sum())
        else:
            wi=avg_alpha*float((w[1]*(s[1]-s[0])).sum())
            rw=avg_alpha*float((s[0]*(w[1]-w[0])).sum())
        assert abs(wi+rw+entering+exiting-delta)<1e-12
        ordering.append({'ipc_subclass':code,'order':order,'within_pp':wi*100,'reweighting_pp':rw*100,'composition_pp':(entering+exiting)*100})
    for sid in sorted(C):
        contributions.append({'ipc_subclass':code,'selection_id':sid,'company_name_official':cg[0].loc[sid,'company_name_official'],'early_patent_mass':cg[0].loc[sid,'patent_mass'],'late_patent_mass':cg[1].loc[sid,'patent_mass'],'early_within_company_share_pct':s[0].loc[sid]*100,'late_within_company_share_pct':s[1].loc[sid]*100,'within_contribution_pp':within.loc[sid]*100,'reweighting_contribution_pp':weight.loc[sid]*100})
    for sid in sorted(E):
        z=zE[zE.selection_id==sid].iloc[0]
        contributions.append({'ipc_subclass':code,'selection_id':sid,'company_name_official':z.company_name_official,'early_patent_mass':0,'late_patent_mass':z.patent_mass,'early_within_company_share_pct':np.nan,'late_within_company_share_pct':z[code+'_share']*100,'within_contribution_pp':0,'reweighting_contribution_pp':0,'composition_contribution_pp':(z[code+'_mass']-z.patent_mass*common_mean)/totals[1]*100})
    for sid in sorted(X):
        z=zX[zX.selection_id==sid].iloc[0]
        contributions.append({'ipc_subclass':code,'selection_id':sid,'company_name_official':z.company_name_official,'early_patent_mass':z.patent_mass,'late_patent_mass':0,'early_within_company_share_pct':z[code+'_share']*100,'late_within_company_share_pct':np.nan,'within_contribution_pp':0,'reweighting_contribution_pp':0,'composition_contribution_pp':-(z[code+'_mass']-z.patent_mass*common_mean)/totals[0]*100})
    sensitivity.append({'ipc_subclass':code,'common_firms':len(C),'equal_company_share_early_pct':s[0].mean()*100,'equal_company_share_late_pct':s[1].mean()*100,'firms_increased':int((s[1]>s[0]+1e-12).sum()),'firms_decreased':int((s[1]<s[0]-1e-12).sum()),'firms_unchanged':int((abs(s[1]-s[0])<=1e-12).sum()),'counterfactual_old_common_weights_new_shares_pct':float((w[0]*s[1]).sum()*100),'counterfactual_new_common_weights_old_shares_pct':float((w[1]*s[0]).sum()*100)})
save('decomposition_summary',pd.DataFrame(results));save('decomposition_components',pd.DataFrame(details));save('company_contributions',pd.DataFrame(contributions));save('common_company_sensitivity',pd.DataFrame(sensitivity))
save('ordering_sensitivity',pd.DataFrame(ordering))
f=lambda size:ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',size)
im=Image.new('RGB',(1450,830),'white');dr=ImageDraw.Draw(im)
dr.text((55,30),'G06N·G06T 증가의 분해: 기업 내부 변화와 구성 효과',font=f(32),fill='#182333')
dr.text((55,90),'2014~2018 → 2019~2024 · 고유 출원 IPC 분수계수 비중의 변화(%p)',font=f(21),fill='#667085')
labels=['동일 기업 내부 비중 변화','공통 기업 출원량 가중 변화','한 기간만 관측된 기업 구성'];colors=['#245A81','#D68034','#42856C']
for k,row in enumerate(results):
    top=175+k*275
    dr.text((55,top),f"{row['ipc_subclass']}  전체 +{row['change_pp']:.2f}%p",font=f(27),fill='#182333')
    vals=[row['within_pp'],row['reweighting_pp'],row['later_only_pp']+row['earlier_only_pp']]
    for j,(lab,val,color) in enumerate(zip(labels,vals,colors)):
        y=top+55+j*55;x=510;end=x+690*val/10
        dr.text((55,y),lab,font=f(22),fill='#182333');dr.rectangle((min(x,end),y,max(x,end),y+31),fill=color)
        dr.text((max(x,end)+12,y),f'{val:+.2f}%p ({val/row["change_pp"]*100:.1f}%)',font=f(21),fill='#182333')
dr.text((55,755),'기업 구성은 관측 여부의 변화이며 기업 설립·퇴출을 뜻하지 않음. 분해는 기술통계이며 인과효과가 아님.',font=f(19),fill='#667085')
im.save(FIG/'ipc_change_components.png')
assert before_hashes==hashes()
manifest={'python':platform.python_version(),'period_unique_counts':dict(zip(periods,totals)),'common_firms':len(C),'earlier_only_firms':len(X),'later_only_firms':len(E),'common_patent_fraction':dict(zip(periods,alpha)),'preserved_sha256':before_hashes,'existing_artifacts_unchanged':True,'checks':['period shares reproduce EDA','exact midpoint decomposition residual < 1e-12','unique patent weight split over selected companies','all existing EDA and original hashes unchanged'],'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(OUT/'run_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'summary':results,'coverage':coverage,'sensitivity':sensitivity},ensure_ascii=False,indent=2))
