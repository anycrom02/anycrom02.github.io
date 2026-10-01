# 과제 제출용 특허 데이터 스토리

`index.html`을 더블클릭해 열면 됩니다. 실행 시 인터넷·CDN·외부 JS·웹서버가 필요하지 않습니다. 공식 출처 링크를 여는 경우만 인터넷이 필요합니다. 모든 내부 링크는 상대경로입니다.

## 파일 안내

- index.html: 최종 한 페이지 스토리
- assets/styles.css, assets/app.js: 반응형 스타일 및 선택적 분야 필터
- data/: 기존 분석값의 표시용 JSON, 주요 결과 CSV, 원본 보존 해시
- reproducibility/: 기존 EDA·분해 코드, 입력 데이터 사본, 결과·보고서 사본
- tools/: HTML 표시 파일 생성 코드와 템플릿
- qa/: 화면 캡처와 검수 기록

## 분석 재현

`reproducibility` 폴더에서 다음 명령을 실행합니다. Python과 pandas·numpy·openpyxl·Pillow가 필요합니다. 분석 코드 사본은 원본을 그대로 보존했으며 차트 생성에는 Windows의 맑은 고딕을 사용합니다. 코드는 이번 입력 건수에 대한 검증 조건을 포함합니다.

```
python 04_analysis/eda_portfolio.py
python 04_analysis/decompose_ipc_change.py
```

분석 재현 실행은 사본의 분석결과를 재생성합니다. 웹페이지 자체는 실행 없이 열 수 있습니다. 기존 master와 분석 입력은 다운로드 사본이며 새 자료가 아닙니다. 원자료의 전체 페이지 HTML·JSON은 용량과 제출 범위를 고려해 포함하지 않았으므로 웹 수집 자체의 재실행 패키지는 아닙니다. 수집·식별 로그는 함께 제공합니다.

`tools/build_page.py`는 원래 프로젝트 폴더 아래에 이 제출 폴더가 있을 때 기존 결과를 읽어 표시 파일을 재생성하는 도구입니다. 새 분석을 수행하지 않습니다.

## GitHub Pages

이 폴더의 **내용 전체**를 저장소 루트 또는 Pages에 지정한 폴더에 올립니다. index.html 위치를 Pages 공개 루트로 지정하면 됩니다. 빌드 도구·npm 설치·환경변수는 필요 없습니다. 루트 경로를 전제로 하는 링크가 없어 프로젝트 저장소의 하위 URL에서도 작동합니다.

본 패키지는 배포 준비 상태이며 실제 업로드·공개 배포는 수행하지 않았습니다.

## Title embedding 추가 (2026-10-01)
초록이 없어 title만 사용했습니다. 3,621건·4,096D, PCA50→UMAP10→HDBSCAN, 39개 군집·643건 미배정입니다. 별도 UMAP2는 지도 표시용입니다. data/semantic에 설정, 결과, 검토 기록과 보고서가 있습니다. assets/semantic-data.js는 벡터를 제외한 정적 지도 데이터입니다.
전체 벡터와 재사용 체크포인트는 로컬 04_analysis/semantic_title에 보존하며 웹 배포에는 포함하지 않습니다. 기존 원자료와 EDA·분해결과를 수정하지 않았습니다. 새 분석 코드 재현 시 requirements.txt를 설치하고 README 및 semantic_report.md를 참고하세요.
별도 배포 폴더: 05_output/github_pages. 이 폴더 내용 전체를 GitHub Pages 루트에 올리면 index.html(과제1) ↔ assignment2/index.html 왕복 링크가 연결됩니다. 자동 공개 배포는 하지 않았습니다.
API key는 openrouterkey.txt에서 런타임에 읽으며 .gitignore 및 export-ignore로 제외합니다. 브라우저에서는 API를 호출하지 않습니다.
