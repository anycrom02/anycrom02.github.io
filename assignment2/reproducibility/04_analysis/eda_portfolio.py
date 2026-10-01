"""Reproducible descriptive EDA. Inputs are read only; no network access.
Run with bundled Python: python 04_analysis/eda_portfolio.py
Dependencies: pandas, numpy, openpyxl, Pillow. Charts use Pillow and Malgun Gothic.
"""
from pathlib import Path
from collections import Counter
import json, hashlib, math, platform, re
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version
import openpyxl

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '04_analysis/eda'
FIG = ROOT / '05_output/eda'
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)
inputs = [ROOT/'03_processed_data/patent_metadata_full.csv', ROOT/'03_processed_data/patent_selection_links.csv', next((ROOT/'01_master').glob('*v7.xlsx'))]
hashes = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
d = pd.read_csv(inputs[0], dtype=str, keep_default_na=False)
links = pd.read_csv(inputs[1], dtype=str, keep_default_na=False)
master = pd.read_excel(inputs[2], sheet_name='master_company', dtype={'selection_id':str})
assert len(d)==d.application_number.nunique()==3621
assert master.selection_id.nunique()==83
d['application_year']=pd.to_datetime(d.application_date).dt.year
d['applicant_count']=d.applicant_count.astype(int)
d['coapplication']=d.applicant_count.gt(1)
d['has_registration']=d.registration_number.ne('')
d['ipc_codes']=d.ipc_json.map(json.loads)
d['ipc_subclasses']=d.ipc_codes.map(lambda a: sorted({x[:4] for x in a if len(x)>=4}))
d['ipc_sections']=d.ipc_subclasses.map(lambda a: sorted({x[0] for x in a}))
d['primary_ipc_subclass']=d.ipc_codes.map(lambda a:a[0][:4] if a else '')
d['ipc_subclass_count']=d.ipc_subclasses.map(len)
assert all(re.fullmatch(r'[A-H]\d{2}[A-Z]',code) for codes in d.ipc_subclasses for code in codes)
lk=links[['application_number','selection_id']].drop_duplicates()
assert set(zip(lk.application_number,lk.selection_id))=={(r.application_number,sel) for r in d.itertuples() for sel in json.loads(r.selection_ids_json)}
p=lk.merge(d,on='application_number',validate='many_to_one').merge(master[['selection_id','company_name_official','cohort','selection_year','field_official']],on='selection_id',validate='many_to_one')
assert len(p)==3624
p['relative_selection_year']=p.application_year-p.selection_year

def save(name, table):
    table.to_csv(OUT/f'{name}.csv',index=False,encoding='utf-8-sig')
def records(t):
    return json.loads(t.to_json(orient='records',force_ascii=False))
profile=[]
for col in d.columns[:25]:
    empty=d[col].eq('')
    if col.endswith('_json'):
        def present(v):
            a=json.loads(v)
            return any(bool(x.get('name','').strip()) if isinstance(x,dict) else bool(str(x).strip()) for x in a)
        empty=~d[col].map(present)
    profile.append({'variable':col,'unique_values':d[col].nunique(),'missing_or_empty_count':int(empty.sum()),'missing_pct':round(empty.mean()*100,2),'example':str(d[col].iloc[0])[:180]})
save('variable_profile',pd.DataFrame(profile))
save('derived_patent_variables',d[['application_number','application_year','coapplication','has_registration','primary_ipc_subclass','ipc_subclass_count']])
save('patent_company_analysis',p[['application_number','selection_id','company_name_official','field_official','cohort','selection_year','application_year','relative_selection_year','coapplication','has_registration','primary_ipc_subclass']])

company=p.groupby('selection_id').agg(n=('application_number','nunique'),first_year=('application_year','min'),last_year=('application_year','max'),median_year=('application_year','median'),coapplication_count=('coapplication','sum'),registered_number_count=('has_registration','sum')).reset_index()
company=master[['selection_id','company_name_official','field_official','cohort','selection_year']].merge(company,on='selection_id',how='left')
company['collection_status']=np.where(company.n.isna(),'identity_not_confirmed','collected')
company['coapplication_pct']=company.coapplication_count/company.n*100
company['registered_number_pct']=company.registered_number_count/company.n*100
save('company_metrics',company)
observed=company.dropna(subset=['n']).sort_values('n',ascending=False)
def summary(keys):
    s=p.groupby(keys).agg(patent_company_links=('application_number','size'),unique_applications=('application_number','nunique'),companies=('selection_id','nunique'),coapplication_links=('coapplication','sum'),median_application_year=('application_year','median')).reset_index()
    c=observed.groupby(keys).n.agg(['median','mean','min','max']).reset_index().rename(columns={'median':'median_company_count','mean':'mean_company_count','min':'min_company_count','max':'max_company_count'})
    return s.merge(c,on=keys)
field=summary(['field_official']);cohort=summary(['cohort'])
save('field_summary',field);save('cohort_summary',cohort)
annual=d.groupby('application_year').agg(n=('application_number','size'),coapplications=('coapplication','sum'),with_registration_number=('has_registration','sum')).reset_index()
save('annual_unique_applications',annual)
annual_company=p.groupby(['selection_id','application_year']).size().reset_index(name='n')
save('annual_company',annual_company)
save('annual_field',p.groupby(['field_official','application_year']).size().reset_index(name='n'))
save('annual_cohort',p.groupby(['cohort','application_year']).size().reset_index(name='n'))
save('administrative_status',d.groupby('administrative_status').agg(n=('application_number','size'),with_registration_number=('has_registration','sum')).reset_index())
save('relative_selection_year',p.groupby(['cohort','relative_selection_year']).size().reset_index(name='n'))

# Multi-label IPC: a patent receives total weight 1 across its distinct subclasses.
ipc_rows=[]
for r in d.itertuples():
    for code in r.ipc_subclasses:
        ipc_rows.append({'application_number':r.application_number,'ipc_subclass':code,'weight':1/len(r.ipc_subclasses),'year':r.application_year})
ipc=pd.DataFrame(ipc_rows)
ipc_tot=ipc.groupby('ipc_subclass').agg(full_count=('application_number','nunique'),fractional_count=('weight','sum')).reset_index().sort_values('fractional_count',ascending=False)
assert abs(ipc_tot.fractional_count.sum()-len(d))<1e-7
save('ipc_subclass_totals',ipc_tot)
ip=p[['application_number','selection_id','field_official','cohort','company_name_official']].merge(ipc,on='application_number',validate='many_to_many')
field_ipc=ip.groupby(['field_official','ipc_subclass']).agg(full_count=('application_number','nunique'),fractional_count=('weight','sum')).reset_index()
field_ipc['field_share_pct']=100*field_ipc.fractional_count/field_ipc.groupby('field_official').fractional_count.transform('sum')
save('ipc_by_field',field_ipc)
company_ipc=ip.groupby(['selection_id','ipc_subclass']).weight.sum().reset_index()
company_ipc['share']=company_ipc.weight/company_ipc.groupby('selection_id').weight.transform('sum')
div=company_ipc.groupby('selection_id').agg(subclass_count=('ipc_subclass','nunique'),top_subclass_share=('share','max'),entropy=('share',lambda x:float(-(x*np.log(x)).sum()))).reset_index()
div['effective_subclasses']=np.exp(div.entropy)
save('company_ipc_diversity',div.merge(observed[['selection_id','company_name_official','n']],on='selection_id'))
top_ipc_company=ip.groupby(['ipc_subclass','selection_id','company_name_official']).weight.sum().reset_index().sort_values('weight',ascending=False)
save('ipc_company_contributions',top_ipc_company)
prepost=p.assign(period=np.where(p.application_year<p.selection_year,'before_selection_year',np.where(p.application_year==p.selection_year,'selection_year','after_selection_year'))).groupby(['cohort','period']).size().unstack(fill_value=0)
save('selection_timing',prepost.reset_index())
recent=p[p.application_year.between(2019,2024)].groupby('selection_id').size().rename('n_2019_2024').reset_index()
save('company_common_window',observed.merge(recent,on='selection_id',how='left').fillna({'n_2019_2024':0}))
common=observed.merge(recent,on='selection_id',how='left').fillna({'n_2019_2024':0})
save('common_window_field_summary',common.groupby('field_official').agg(companies=('selection_id','size'),total=('n_2019_2024','sum'),median=('n_2019_2024','median')).reset_index())
save('common_window_cohort_summary',common.groupby('cohort').agg(companies=('selection_id','size'),total=('n_2019_2024','sum'),median=('n_2019_2024','median')).reset_index())
# Equal-company weighting: absent subclass cells are zero, not omitted.
eq=company_ipc.merge(observed[['selection_id','field_official']],on='selection_id')
eq=eq.groupby(['field_official','ipc_subclass']).share.sum().reset_index()
eq=eq.merge(observed.groupby('field_official').size().rename('companies').reset_index(),on='field_official')
eq['equal_company_share_pct']=100*eq.share/eq.companies
save('ipc_equal_company_weight',eq)
ai_ex=ip[(ip.field_official=='인공지능') & (ip.selection_id!='SEL-070')].groupby('ipc_subclass').weight.sum().reset_index()
ai_ex['share_pct']=100*ai_ex.weight/ai_ex.weight.sum()
save('ai_ipc_excluding_bujeon',ai_ex.sort_values('weight',ascending=False))
annual_loo=[]
top5=set(observed.head(5).selection_id)
top10=set(observed.head(10).selection_id)
for year,g in p.groupby('application_year'):
    annual_loo.append({'application_year':year,'company_links':len(g),'excluding_top5':len(g[~g.selection_id.isin(top5)]),'excluding_top10':len(g[~g.selection_id.isin(top10)]),'active_companies':g.selection_id.nunique()})
save('annual_concentration_sensitivity',pd.DataFrame(annual_loo))
period_ipc=ipc[ipc.year.between(2014,2024)].copy()
period_ipc['period']=np.where(period_ipc.year<=2018,'2014-2018','2019-2024')
pi=period_ipc.groupby(['period','ipc_subclass']).weight.sum().reset_index()
pi['share_pct']=pi.weight/pi.groupby('period').weight.transform('sum')*100
save('ipc_period_share',pi)
period_company=ip[ip.year.between(2014,2024)].copy()
period_company['period']=np.where(period_company.year<=2018,'2014-2018','2019-2024')
pc=period_company.groupby(['selection_id','period','ipc_subclass']).weight.sum().reset_index()
den=pc.groupby(['selection_id','period']).weight.sum().rename('period_company_count').reset_index()
pc=pc.merge(den,on=['selection_id','period']);pc['share']=pc.weight/pc.period_company_count
both=set(den[den.period=='2014-2018'].selection_id)&set(den[den.period=='2019-2024'].selection_id)
paired=[]
for period in ['2014-2018','2019-2024']:
    for code in ['G06N','G06T','G06F','H04R']:
        paired.append({'period':period,'ipc_subclass':code,'paired_companies':len(both),'equal_company_share_pct':100*pc[(pc.period==period)&(pc.ipc_subclass==code)&pc.selection_id.isin(both)].share.sum()/len(both)})
save('ipc_period_paired_company_sensitivity',pd.DataFrame(paired))

FONT=Path('C:/Windows/Fonts/malgun.ttf')
def font(size):return ImageFont.truetype(str(FONT),size)
BLUE='#245A81';ORANGE='#D68034';GRAY='#667085'
def base(title,subtitle,w=1500,h=950):
    im=Image.new('RGB',(w,h),'white');dr=ImageDraw.Draw(im)
    dr.text((60,28),title,font=font(34),fill='#182333');dr.text((60,88),subtitle,font=font(20),fill=GRAY)
    return im,dr
def bars(name,title,subtitle,labels,values,note='',unit='',colors=None):
    h=max(750,250+len(labels)*53);im,dr=base(title,subtitle,h=h)
    x0=365;x1=1330;y0=155;mx=max(values)*1.14
    for i,(lab,val) in enumerate(zip(labels,values)):
        y=y0+i*53
        dr.text((60,y+4),str(lab),font=font(21),fill='#182333')
        end=x0+(x1-x0)*val/mx
        dr.rectangle((x0,y,end,y+31),fill=(colors[i] if colors else BLUE))
        dr.text((end+12,y+2),f'{val:,.1f}{unit}' if isinstance(val,float) else f'{val:,}{unit}',font=font(20),fill='#182333')
    dr.text((60,h-62),note,font=font(19),fill=GRAY)
    im.save(FIG/f'{name}.png')
def lines(name,title,subtitle,series,note):
    im,dr=base(title,subtitle);x0,x1,y0,y1=100,1380,170,790
    years=sorted(set(y for s in series for y in s[1]));mx=math.ceil(max(v for s in series for v in s[2])*1.08/100)*100
    if max(years)>2024:
        censor_x=x0+(x1-x0)*(2024.5-min(years))/(max(years)-min(years))
        dr.rectangle((censor_x,y0,x1,y1),fill='#FFF3E6')
        dr.text((censor_x+8,y0+8),'관측 불완전',font=font(17),fill='#9A521A')
    for tick in range(0,6):
        val=mx*tick/5;y=y1-(y1-y0)*tick/5
        dr.line((x0,y,x1,y),fill='#E5E7EB',width=2);dr.text((20,y-14),f'{val:.0f}',font=font(18),fill=GRAY)
    for year in years:
        if year%2==0:
            x=x0+(x1-x0)*(year-min(years))/(max(years)-min(years));dr.text((x-24,y1+15),str(year),font=font(17),fill=GRAY)
    for j,(label,ys,vs,color) in enumerate(series):
        pts=[(x0+(x1-x0)*(y-min(years))/(max(years)-min(years)),y1-(y1-y0)*v/mx) for y,v in zip(ys,vs)]
        dr.line(pts,fill=color,width=5)
        for x,y in pts:dr.ellipse((x-4,y-4,x+4,y+4),fill=color)
        dr.text((110+j*380,125),label,font=font(20),fill=color)
    dr.text((60,880),note,font=font(18),fill=GRAY);im.save(FIG/f'{name}.png')

bars('01_company_concentration','기업별 포트폴리오: 상위 기업에 집중','출원번호 기준 기업별 건수 · 공동출원은 각 기업에 연결',observed.head(12).company_name_official.tolist(),observed.head(12).n.astype(int).tolist(),'81개 수집 기업 중 상위 12개. 미수집 2개 기업은 0건으로 간주하지 않음.')
a=annual[annual.application_year>=2005]
lines('02_annual_applications','출원연도 분포: 2010년대 후반 이후 증가','2025~2026년은 공개 지연 및 2026년 연중 수집 영향', [('전체 고유 출원',a.application_year.tolist(),a.n.tolist(),BLUE)],'2026-09-30 수집 자료. 최근 연도의 낮은 관측치를 실제 출원 감소로 해석하지 않음.')
af=pd.DataFrame(annual_loo);af=af[af.application_year.between(2005,2024)]
lines('02b_annual_sensitivity','과거 증가 패턴: 상위 기업 제외 민감도','기업-출원 연결건수 · 2024년까지 표시',[('전체',af.application_year.tolist(),af.company_links.tolist(),BLUE),('상위 5개 제외',af.application_year.tolist(),af.excluding_top5.tolist(),ORANGE),('상위 10개 제외',af.application_year.tolist(),af.excluding_top10.tolist(),'#42856C')],'전체 고유 출원과 기업 연결건수는 공동출원 때문에 최대 3건 차이.')
f=field.sort_values('median_company_count',ascending=False)
bars('03_field_medians','선정분야별 전형적인 기업의 포트폴리오 크기','합계와 함께 기업별 중앙값을 비교 · 누적 출원 건수',f.field_official.tolist(),f.median_company_count.tolist(),'선정분야는 정책상 분류이며 IPC 기술분류와 동일하지 않음. 기업 업력 차이 미조정.')
topcodes=ipc_tot.head(12).ipc_subclass.tolist();fields=sorted(field.field_official)
mat=field_ipc.pivot(index='field_official',columns='ipc_subclass',values='field_share_pct').fillna(0).reindex(index=fields,columns=topcodes)
im,dr=base('선정분야와 실제 IPC 구성: 공통점과 차이','분야 내 IPC 분수계수 비중(%) · 출원 1건의 가중치 합계=1',h=870)
for j,code in enumerate(topcodes):dr.text((240+j*97,165),code,font=font(21),fill='#182333')
for i,fieldname in enumerate(fields):
    dr.text((55,233+i*75),fieldname,font=font(21),fill='#182333')
    for j,code in enumerate(topcodes):
        val=float(mat.loc[fieldname,code]);q=min(val/35,1)
        color=(int(240-200*q),int(247-155*q),int(251-120*q));x,y=235+j*97,218+i*75
        dr.rectangle((x,y,x+90,y+65),fill=color);dr.text((x+17,y+21),f'{val:.1f}',font=font(20),fill='white' if q>.65 else '#182333')
dr.text((60,775),'전체 분수계수 상위 12개 IPC만 표시. 분야 행의 표시된 비중 합계는 100% 미만일 수 있음.',font=font(19),fill=GRAY)
im.save(FIG/'04_field_ipc_heatmap.png')
bars('04b_ipc_overall','포트폴리오의 기술축: 계산·영상·센싱·전자','고유 출원 기준 IPC 서브클래스 분수계수 비중',ipc_tot.head(10).ipc_subclass.tolist(),(ipc_tot.head(10).fractional_count/len(d)*100).tolist(),'다중 IPC는 고유 서브클래스로 정리한 뒤 출원당 총 가중치 1로 배분.',unit='%')
h04r_full=float(field_ipc[(field_ipc.field_official=='인공지능') & (field_ipc.ipc_subclass=='H04R')].field_share_pct.iloc[0])
h04r_eq=float(eq[(eq.field_official=='인공지능') & (eq.ipc_subclass=='H04R')].equal_company_share_pct.iloc[0])
h04r_ex=float(ai_ex[ai_ex.ipc_subclass=='H04R'].share_pct.iloc[0])
bars('04c_ai_h04r_sensitivity','인공지능 분야의 음향 IPC: 기업 구성에 민감','H04R 비중 · 비교마다 분모/가중치를 달리한 민감도 점검',['전체 출원 가중','기업별 동일 가중','부전전자 제외'],[h04r_full,h04r_eq,h04r_ex],'H04R은 음향 변환기 관련 IPC. 전체 기업 포트폴리오와 선정기술은 구분해 해석.',unit='%')
im,dr=base('기간별 기술 구성: 계산모델·영상처리 비중 확대','출원번호 기준 IPC 분수계수 비중(%) · 2014~2018년과 2019~2024년 비교',h=810)
codes=['G06N','G06T','G06F','H04R'];mx=12
for i,code in enumerate(codes):
    y=210+i*115;dr.text((70,y+24),code,font=font(26),fill='#182333')
    for j,period in enumerate(['2014-2018','2019-2024']):
        val=float(pi[(pi.period==period)&(pi.ipc_subclass==code)].share_pct.iloc[0]);end=260+1000*val/mx
        dr.rectangle((260,y+j*44,end,y+j*44+33),fill=[BLUE,ORANGE][j]);dr.text((end+12,y+j*44),f'{val:.2f}%',font=font(21),fill='#182333')
dr.text((260,150),'2014~2018',font=font(23),fill=BLUE);dr.text((520,150),'2019~2024',font=font(23),fill=ORANGE)
dr.text((60,730),'기간별 구성 비교이며 연간 증가율이 아님. 기업 구성과 IPC 재분류 영향을 함께 고려해야 함.',font=font(19),fill=GRAY)
im.save(FIG/'04d_ipc_period_change.png')

co=cohort.sort_values('cohort')
bars('05_cohort_medians','기수별 누적 건수는 단조롭게 감소하지 않음','기수별 기업당 누적 출원 중앙값', [f'{int(r.cohort)}기 ({int(r.companies)}개 기업)' for r in co.itertuples()],co.median_company_count.tolist(),'선정 시점·업력·기술 구성이 다른 단면 비교. 지원 효과 또는 기업 우열을 의미하지 않음.')
timing=prepost.reindex(columns=['before_selection_year','selection_year','after_selection_year']).reset_index()
im,dr=base('포트폴리오 대부분은 선정연도 이전에 출원','기수별 기업-출원 연결건수 구성 · 선정연도 내부의 전후는 구분 불가',h=760)
timingcolors=[BLUE,ORANGE,'#42856C']
for j,(label,color) in enumerate(zip(['선정연도 이전','선정연도','선정연도 이후'],timingcolors)):
    dr.text((290+j*330,150),label,font=font(23),fill=color)
for i,r in enumerate(timing.itertuples()):
    vals=[r.before_selection_year,r.selection_year,r.after_selection_year];total=sum(vals);x=300;y=225+i*100
    dr.text((60,y+22),f'{r.cohort}기 · {total:,}건',font=font(23),fill='#182333')
    for val,color in zip(vals,timingcolors):
        end=x+1060*val/total;dr.rectangle((x,y,end,y+65),fill=color)
        if end-x>90:dr.text((x+12,y+20),f'{val:,} ({val/total*100:.1f}%)',font=font(19),fill='white')
        x=end
dr.text((60,695),'전체: 이전 2,978건(82.2%), 선정연도 294건, 이후 352건. 선정 이후 관측기간은 기수별로 다름.',font=font(19),fill=GRAY)
im.save(FIG/'05b_selection_timing.png')
cofield=p.groupby('field_official').agg(n=('application_number','size'),co=('coapplication','sum')).reset_index();cofield['pct']=100*cofield.co/cofield.n;cofield=cofield.sort_values('pct',ascending=False)
save('coapplication_by_field',cofield)
bars('06_coapplication_by_field','공동출원 비중은 선정분야별로 다름','전체 출원인 수가 2명 이상인 출원 · 기업-출원 연결건수 기준',cofield.field_official.tolist(),cofield.pct.tolist(),'공동출원은 공동명의를 의미하며 협력의 강도·계약·성과는 측정하지 않음.',unit='%')
save('coapplication_by_company',observed[['selection_id','company_name_official','n','coapplication_count','coapplication_pct']].sort_values('coapplication_count',ascending=False))
duplicates=d[d.source_observation_count.astype(int)>1][['application_number','title','selection_ids_json','source_observation_count']]
save('cross_company_duplicate_applications',duplicates)

numbers=observed.n.to_numpy();gini=float(np.abs(numbers[:,None]-numbers).sum()/(2*len(numbers)*numbers.sum()))
before=int((p.application_year<p.selection_year).sum())
sections=Counter()
for codes in d.ipc_sections:
    for code in codes: sections[code]+=1/len(codes)
metrics={'unique_applications':len(d),'company_patent_links':len(p),'observed_companies':len(observed),'excluded_companies':company[company.n.isna()].company_name_official.tolist(),'company_count_median':float(observed.n.median()),'company_count_mean':float(observed.n.mean()),'company_count_min':int(observed.n.min()),'company_count_max':int(observed.n.max()),'gini':gini,'top5_count':int(observed.head(5).n.sum()),'top5_share_links_pct':float(observed.head(5).n.sum()/len(p)*100),'top10_count':int(observed.head(10).n.sum()),'top10_share_links_pct':float(observed.head(10).n.sum()/len(p)*100),'before_selection_year_count':before,'before_selection_year_pct':before/len(p)*100,'selection_year_count':int((p.application_year==p.selection_year).sum()),'after_selection_year_count':int((p.application_year>p.selection_year).sum()),'coapplication_count':int(d.coapplication.sum()),'coapplication_pct':float(d.coapplication.mean()*100),'ipc_subclass_unique_count':int(ipc.ipc_subclass.nunique()),'ipc_subclass_count_median':float(d.ipc_subclass_count.median()),'multi_subclass_pct':float(d.ipc_subclass_count.gt(1).mean()*100),'top10_ipc_fractional_pct':float(ipc_tot.head(10).fractional_count.sum()/len(d)*100),'ipc_section_fractional':dict(sections),'annual':records(annual),'top_companies':records(observed.head(12)),'fields':records(field),'cohorts':records(cohort),'field_ipc_top':records(field_ipc.sort_values('fractional_count',ascending=False).groupby('field_official').head(3)),'coapplication_fields':records(cofield),'top_coapplication_companies':records(observed.sort_values('coapplication_count',ascending=False).head(10)),'selection_timing':records(prepost.reset_index()),'ipc_top':records(ipc_tot.head(15))}
(OUT/'metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
assert hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
manifest={'input_sha256':hashes,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'originals_unchanged':True,'python':platform.python_version(),'pandas':pd.__version__,'numpy':np.__version__,'Pillow':pillow_version,'openpyxl':openpyxl.__version__,'rows':{'unique':len(d),'company_links':len(p)},'checks':['unique application PK','83 master selection IDs','selection JSON agrees with linkage table','valid IPC subclass format','company linkage 3624','IPC fractional weights sum to 3621','input hashes unchanged'],'chart_files':sorted(x.name for x in FIG.glob('*.png'))}
(OUT/'run_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'result':'PASS','unique_applications':len(d),'company_links':len(p),'tables':len(list(OUT.glob('*.csv'))),'charts':len(list(FIG.glob('*.png'))),'originals_unchanged':True}))
