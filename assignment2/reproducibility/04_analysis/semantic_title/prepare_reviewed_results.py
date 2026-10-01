"""Persist actual profile review. This labels results without changing assignments."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent
def main():
    profiles=json.loads((P/'cluster_profiles.json').read_text(encoding='utf-8'));comp=json.loads((P/'comparison_examples.json').read_text(encoding='utf-8'))
    names=['영상·객체 검출','무인비행체·드론 제어','마이크로 스피커·이어폰','혼합 기술군 · 통신·서비스','신경망 프로세서·NPU','라이다·점군 인식','디지털 문서·콘텐츠 보안','학습 데이터·모델 관리','안테나·밀리미터파','모터·구동장치','광학·조준·열상 장치','광섬유·광통신','질화물 반도체·결정 성장','디지털 워터마킹','어노테이션·데이터 작업','위성항법·위성 운용','혼합 기술군 · 음향·센싱','반도체 발광소자','전기화학 소자·전지','원전·소화·안전설비','반도체 공정·제조','증강현실·객체 추적','커넥터·연결 회로','3D 점군·모델 생성','혼합 기술군 · RF·패키지','전기음향 변환·진동','극저온·수소 저장','압전체·초음파','자율주행 시뮬레이션','혼합 기술군 · 기기 제어','거리·위치 측정','마이크로디스플레이·LED','지도·위치정보 생성','비디오 메타데이터·전송','혼합 기술군 · 움직임·생체신호','음원·음성 인식','고주파 전력·증폭 회로','복합재·성형','로봇 작업 경로']
    labels={}
    for c in profiles:
        name=names[c['cluster']] if c['cluster']>=0 else '미배정'
        labels[str(c['cluster'])]={'label':name,'reason':('대표 제목에는 '+ ' / '.join(r['title'].split('(')[0] for r in c['representatives'][:3])+ '가 나타난다. 주요 IPC '+', '.join(list(c['top_ipc'])[:3])+' 및 주요 선정분야 '+', '.join(list(c['top_fields'])[:2])+'를 함께 확인했다. '+('중심과 경계 제목의 범위가 넓어 혼합으로 남겼다.' if '혼합' in name or c['cluster']<0 else '중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.')),'reviewed_application_numbers':[r['application_number'] for r in c['representatives']],'boundary_titles_reviewed':c['boundary_titles']}
    (P/'cluster_labels_reviewed.json').write_text(json.dumps(labels,ensure_ascii=False,indent=2),encoding='utf-8')
    def example(r,group):return {'group':group,'title':r['title'],'application_number':r['application_number'],'ipc':' · '.join(r.get('ipc',r.get('ipc_subclasses',[])))}
    g=next(c for c in comp['same_ipc'] if c['ipc']=='G06N');pair=next(c for c in comp['different_ipc_near_pairs'] if c['cluster']==13)
    findings=[
      {'question':'선정분야와 의미군집','headline':'인공지능 선정기업의 포트폴리오에도 스피커 기술이 있다.','text':'스피커·이어폰 군집 C03은 155건이며 153건(98.7%)이 부전전자에 연결된다. 인공지능 분야 고유 출원 가중치의 12.29%가 이 군집에 귀속된다. 선정분야는 기업의 전체 과거 포트폴리오와 구분해야 한다.','examples':[example(profiles[2]['representatives'][0],'C03 · 스피커·이어폰')]},
      {'question':'같은 IPC, 다른 제목 주제','headline':'G06N 안에서도 NPU와 학습 데이터가 나뉜다.','text':f"G06N 분수계수의 30.91%는 C05 신경망 프로세서·NPU, 22.28%는 C08 학습 데이터·모델 관리, 10.86%는 C15 어노테이션·데이터 작업에 귀속된다. 같은 코드 안의 세부 주제를 제목이 드러내지만 정답 분류를 뜻하지 않는다.",'examples':[example(x['examples'][0],f"C{x['cluster']+1:02d} · "+names[x['cluster']]) for x in g['groups']]},
      {'question':'다른 IPC, 가까운 제목','headline':'G11B와 H04N의 워터마크 제목이 같은 군집에 묶인다.','text':f"출원번호 {pair['a']['application_number']}와 {pair['b']['application_number']}는 IPC 서브클래스가 겹치지 않지만 C14 워터마킹 군집에 속한다. 원래 4,096D 제목 embedding의 cosine 유사도는 {pair['cosine_similarity']:.3f}이다. 제목 수준의 연결 사례이며 구현·권리범위가 같다는 뜻은 아니다.",'examples':[example(pair['a'],'G11B'),example(pair['b'],'H04N')]},
      {'question':'관측 밀도의 해석','headline':'일부 군집은 특정 기업과 제목 작성양식의 영향을 받는다.','text':'C15 어노테이션·데이터 작업 83건 중 80건은 인피닉에 연결되고 57건은 2021년 출원이다. ‘기록매체에 기록된 컴퓨터 프로그램’ 같은 반복 서술도 포함되어, 군집을 산업 전체의 독립적 기술영역으로 일반화하지 않는다.','examples':[]},
      {'question':'안정성과 미배정','headline':'39개는 고정된 기술분류가 아니다.','text':'643건(17.8%)은 미배정이다. 최소 군집 크기20/40을 적용하면 군집 수는 44/27개, UMAP seed7에서는 41개다. 기준 결과와의 전체 ARI는 각각 0.938/0.718/0.700으로 설정 의존성을 함께 보고한다.','examples':[]}
    ]
    (P/'reviewed_findings.json').write_text(json.dumps(findings,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Reviewed labels and five findings saved.')
if __name__=='__main__':main()
