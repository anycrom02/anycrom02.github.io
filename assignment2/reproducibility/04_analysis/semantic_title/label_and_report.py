"""Render already-computed results; reviewed labels/findings are versioned JSON inputs."""
from pathlib import Path
import sys,json,csv
P=Path(__file__).resolve().parent;R=P.parents[1];sys.path.insert(0,str(P/'vendor'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font=FontProperties(fname='C:/Windows/Fonts/malgun.ttf')
plt.rcParams.update({'font.family':font.get_name(),'axes.unicode_minus':False,'figure.facecolor':'white','axes.spines.top':False,'axes.spines.right':False})
read=lambda n:json.loads((P/n).read_text(encoding='utf-8'))
def main():
    methods=read('analysis_methods.json');profiles=read('cluster_profiles.json');labels=read('cluster_labels_reviewed.json');findings=read('reviewed_findings.json');run=read('run_manifest.json')
    output=R/'05_output/semantic_title';output.mkdir(exist_ok=True)
    coords=np.load(P/'umap2.npy');cluster=np.load(P/'cluster_labels.npy')
    fig,ax=plt.subplots(figsize=(11,7));palette=plt.get_cmap('tab20')
    for c in [-1]+list(range(methods['cluster_count'])):
        mask=cluster==c;ax.scatter(coords[mask,0],coords[mask,1],s=7 if c>=0 else 4,color=palette(c%20) if c>=0 else '#b9bcc4',alpha=.7,rasterized=True)
    ax.set(xlabel='UMAP 1 (단위 없음)',ylabel='UMAP 2 (단위 없음)',title=f"발명의 명칭 의미지도 · {len(coords):,}건 / {methods['cluster_count']}개 군집 / 미배정 {methods['noise_n']:,}건")
    ax.text(.02,.02,'각 점 = 고유 출원 1건 · 2D 지도는 별도 투영 · 군집은 10D 공간에서 계산',transform=ax.transAxes,fontsize=9)
    fig.tight_layout();fig.savefig(output/'semantic_patent_map.png',dpi=170);plt.close(fig)
    def heatmap(filename,key,out):
        with (P/filename).open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
        names=sorted(set(r[key] for r in rows))
        if key=='ipc':
            totals={n:sum(float(r['fractional_patents']) for r in rows if r[key]==n) for n in names};names=sorted(names,key=lambda n:-totals[n])[:12]
        cols=list(range(min(18,methods['cluster_count'])))+([-2] if methods['cluster_count']>18 else [])+[-1]
        a=np.zeros((len(names),len(cols)));share='field_share_pct' if key=='field' else 'ipc_share_pct'
        for r in rows:
            if r[key] not in names:continue
            c=int(r['cluster']);c=-2 if c>=18 else c;a[names.index(r[key]),cols.index(c)]+=float(r[share])
        fig,ax=plt.subplots(figsize=(15,max(5,len(names)*.45)));im=ax.imshow(a,vmin=0,vmax=50,cmap='Blues',aspect='auto')
        ax.set_xticks(range(len(cols)),['미배정' if c==-1 else '기타 군집' if c==-2 else f'C{c+1:02d}' for c in cols],rotation=45,ha='right');ax.set_yticks(range(len(names)),names)
        for i in range(len(names)):
            for j in range(len(cols)):ax.text(j,i,f'{a[i,j]:.1f}',ha='center',va='center',fontsize=7,color='white' if a[i,j]>30 else '#18234f')
        ax.set_title(('선정분야' if key=='field' else '주요 IPC')+' × 제목 의미군집 · 행 내 구성비(%) / 미배정 포함');fig.colorbar(im,ax=ax,label='구성비 (%)');fig.tight_layout();fig.savefig(output/out,dpi=170);plt.close(fig)
    heatmap('field_cluster_matrix.csv','field','field_cluster_heatmap.png');heatmap('ipc_cluster_matrix.csv','ipc','ipc_cluster_heatmap.png')
    text=['# 특허 발명의 명칭 기반 의미분석','',f"고유 출원 {methods['n']:,}건. title만 사용; 초록 없음. 모델 {methods['model']}, 4,096D.",f"성공 {run['successful_records']:,}건, 실패 {run['failed_records']}건. 파일럿 5건 재사용. 총 {run['total_prompt_tokens_including_pilot']:,} tokens; API usage.cost 합계 ${run['total_api_cost_usd_including_pilot']:.8f} (새 호출 ${run['new_api_cost_usd']:.8f}).",'', '## 방법',json.dumps(methods,ensure_ascii=False,indent=2),'','## 실제 발견']
    for f in findings:text.extend(['### '+f['headline'],f['text']]+[e['title']+' / '+e['application_number']+' / '+e.get('ipc','') for e in f.get('examples',[])])
    text.extend(['','## 군집 검토 기록','이름은 중심 제목·IPC·선정분야 및 경계 제목을 검토한 요약이며 공식 분류가 아니다.'])
    for c in profiles:
        review=labels[str(c['cluster'])];text.extend([f"### {'미배정' if c['cluster']<0 else 'C'+str(c['cluster']+1).zfill(2)} {review['label']} · {c['n']}건",review['reason'],'대표 제목: '+ ' / '.join(r['title'] for r in c['representatives'][:3]),'경계 제목: '+' / '.join(c['boundary_titles'])])
    text.extend(['','## 재현','1. requirements.txt 패키지 설치. embed_all.py 실행은 누락 배치만 실제 API 호출하며 비용 발생. 완성 체크포인트가 있으면 재호출하지 않음.','2. analyze_titles.py 실행(저장된 embeddings.npy와 patent_embedding_records.json 사용).','3. cluster_labels_reviewed.json / reviewed_findings.json은 실제 결과 검토 기록. label_and_report.py는 저장된 분석값으로 PNG·보고서 재생성.','4. submission/tools/build_semantic_section.py를 pre-semantic HTML에 실행하여 정적 웹 결과 생성.','벡터는 embeddings.npy의 행 순서와 patent_embedding_records.json의 행 순서가 일치한다. application_number로 원자료 연결 가능.','', '## 한계','제목만의 언어적 근접성. 전문·초록·청구항을 분석하지 않았다. 의미 군집은 방산 여부, 기업전략, 상용화, 인과적 정책효과의 증거가 아니다. UMAP은 거리·밀도를 왜곡하고 분리를 만들 수 있어 지도상 간격을 기술 거리로 정량 해석하지 않는다. 정규화·차원축소·HDBSCAN parameter에 의존하며 미배정은 무의미한 특허를 뜻하지 않는다. 선정분야 행은 고유 출원당 소속 기록에 1/m, IPC 행은 고유 출원당 고유 서브클래스에 1/k 배분; 기존 EDA의 기업-출원 연결 집계와 분모가 다르다.','', '## 공식 방법자료','[UMAP](https://umap-learn.readthedocs.io/en/latest/clustering.html) · [HDBSCAN](https://hdbscan.readthedocs.io/en/latest/parameter_selection.html) · [OpenRouter](https://openrouter.ai/qwen/qwen3-embedding-8b)'])
    (P/'semantic_report.md').write_text('\n\n'.join(text),encoding='utf-8');print('Rendered report and three figures.')
if __name__=='__main__':main()
