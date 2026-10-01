# 특허 발명의 명칭 기반 의미분석



고유 출원 3,621건. title만 사용; 초록 없음. 모델 qwen/qwen3-embedding-8b, 4,096D.

성공 3,621건, 실패 0건. 파일럿 5건 재사용. 총 132,998 tokens; API usage.cost 합계 $0.00132998 (새 호출 $0.00132808).



## 방법

{
  "model": "qwen/qwen3-embedding-8b",
  "input": "title only; abstracts not available",
  "n": 3621,
  "dimension": 4096,
  "normalization": "L2 unit vectors",
  "pca": {
    "components": 50,
    "svd_solver": "randomized",
    "random_state": 42,
    "whiten": false,
    "explained_variance_ratio": 0.48566144704818726
  },
  "cluster_projection": {
    "method": "UMAP",
    "components": 10,
    "n_neighbors": 30,
    "min_dist": 0.0,
    "metric": "cosine",
    "random_state": 42,
    "n_jobs": 1
  },
  "clustering": {
    "method": "HDBSCAN",
    "min_cluster_size": 25,
    "min_samples": 10,
    "metric": "euclidean",
    "cluster_selection_method": "eom"
  },
  "map_projection": {
    "method": "UMAP",
    "components": 2,
    "n_neighbors": 30,
    "min_dist": 0.15,
    "metric": "cosine",
    "random_state": 42,
    "n_jobs": 1
  },
  "cluster_count": 39,
  "clustered_n": 2978,
  "noise_n": 643,
  "noise_pct": 17.757525545429438,
  "sensitivity": [
    {
      "variant": "min_cluster_size=20",
      "clusters": 44,
      "noise": 612,
      "ari_all_including_noise": 0.9378566099591396,
      "common_assigned_n": 2963,
      "ari_common_assigned": 0.9907778924181171
    },
    {
      "variant": "min_cluster_size=40",
      "clusters": 27,
      "noise": 530,
      "ari_all_including_noise": 0.7181604785154596,
      "common_assigned_n": 2918,
      "ari_common_assigned": 0.8618641926313284
    },
    {
      "variant": "UMAP seed=7",
      "clusters": 41,
      "noise": 557,
      "ari_all_including_noise": 0.6998336055742036,
      "common_assigned_n": 2875,
      "ari_common_assigned": 0.9537304858984231
    }
  ],
  "versions": {
    "numpy": "2.5.3",
    "scipy": "1.18.1",
    "scikit-learn": "1.9.1",
    "umap-learn": "0.5.12",
    "hdbscan": "0.8.44",
    "matplotlib": "3.11.2"
  },
  "reason": "PCA speeds neighbor search; 10D manifold projection precedes density clustering without specifying cluster count; independent 2D projection is display only. min_cluster_size25 excludes tiny groups and min_samples10 reduces weak assignments. UMAP distorts density and global distance; all outputs exploratory and parameter-dependent.",
  "matrix_counting": "Each unique application receives total1 across selection memberships and total1 across unique IPC subclasses; separate matrices both sum3621. Noise retained in denominators."
}



## 실제 발견

### 인공지능 선정기업의 포트폴리오에도 스피커 기술이 있다.

스피커·이어폰 군집 C03은 155건이며 153건(98.7%)이 부전전자에 연결된다. 인공지능 분야 고유 출원 가중치의 12.29%가 이 군집에 귀속된다. 선정분야는 기업의 전체 과거 포트폴리오와 구분해야 한다.

마이크로 스피커 구조(Micro speaker structure) / 1020180030334 / H04R

### G06N 안에서도 NPU와 학습 데이터가 나뉜다.

G06N 분수계수의 30.91%는 C05 신경망 프로세서·NPU, 22.28%는 C08 학습 데이터·모델 관리, 10.86%는 C15 어노테이션·데이터 작업에 귀속된다. 같은 코드 안의 세부 주제를 제목이 드러내지만 정답 분류를 뜻하지 않는다.

신경망 프로세싱 유닛(NEURAL NETWORK PROCESSING UNIT) / 1020237015212 / G06F · G06N

학습 데이터 관리 방법(METHOD FOR MANAGING TRAINING DATA) / 1020210112012 / G06F · G06N

어노테이션 작업 제어 방법 및 이를 실행하기 위하여 기록매체에 기록된 컴퓨터 프로그램(Method for controlling annotation work, and computer program recorded on record-medium for executing method therefor) / 1020210035692 / G06F · G06N

### G11B와 H04N의 워터마크 제목이 같은 군집에 묶인다.

출원번호 1020010021531와 1020010023984는 IPC 서브클래스가 겹치지 않지만 C14 워터마킹 군집에 속한다. 원래 4,096D 제목 embedding의 cosine 유사도는 0.958이다. 제목 수준의 연결 사례이며 구현·권리범위가 같다는 뜻은 아니다.

디지털 워터마크의 삽입 및 검출방법과 이를 이용한워터마크 삽입/검출 장치(METHOD OF INSERTING/DETECTING DIGITAL WATERMARKS ANDAPPARATUS FOR USING THEREOF) / 1020010021531 / G11B

디지털 워터마크의 삽입/추출방법과 이를 이용한 워터마크삽입/추출 장치(METHOD OF INSERTING/EXTRACTING DIGITAL WATERMARKS ANDAPPARATUS FOR USING THEREOF) / 1020010023984 / H04N

### 일부 군집은 특정 기업과 제목 작성양식의 영향을 받는다.

C15 어노테이션·데이터 작업 83건 중 80건은 인피닉에 연결되고 57건은 2021년 출원이다. ‘기록매체에 기록된 컴퓨터 프로그램’ 같은 반복 서술도 포함되어, 군집을 산업 전체의 독립적 기술영역으로 일반화하지 않는다.

### 39개는 고정된 기술분류가 아니다.

643건(17.8%)은 미배정이다. 최소 군집 크기20/40을 적용하면 군집 수는 44/27개, UMAP seed7에서는 41개다. 기준 결과와의 전체 ARI는 각각 0.938/0.718/0.700으로 설정 의존성을 함께 보고한다.



## 군집 검토 기록

이름은 중심 제목·IPC·선정분야 및 경계 제목을 검토한 요약이며 공식 분류가 아니다.

### C01 영상·객체 검출 · 206건

대표 제목에는 객체 검출 방법 및 그 장치 / 객체 검출 방법 / 객체 검출 방법가 나타난다. 주요 IPC G06T, H04N, G06V 및 주요 선정분야 인공지능, 로봇를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 객체 검출 방법 및 그 장치(Method for detecting object and apparatus thereof) / 객체 검출 방법(METHOD FOR DETECTING OBJECT) / 객체 검출 방법(METHOD FOR DETECTING OBJECT)

경계 제목: 360°의 화각을 확보할 수 있는 카메라 시스템(CAMERA SYSTEM CAPABLE OF OBTAINING 360 DEGREESPICTURE ANGLE) / 자장을 이용하는 캡슐형 내시경 제어장치(Apparatus for controlling capsule endoscope usingmagnetic field) / PTZ 카메라의 협업을 이용한 영상 감시 시스템, 방법, 및 상기 방법을 실행시키기 위한 컴퓨터 판독 가능한 프로그램을 기록한 기록 매체(System and method for surveilling video using collaboration of PTZ cameras, and a recording medium recording a computer readable program for executing the method)

### C02 무인비행체·드론 제어 · 177건

대표 제목에는 무인 비행체의 이동 방법 및 그 무인 비행체 / 드론 조작을 위한 제어 장치 / 무인 비행체 편대 비행 지원 장치가 나타난다. 주요 IPC B64U, B64C, B64D 및 주요 선정분야 드론, 우주를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 무인 비행체의 이동 방법 및 그 무인 비행체(MOVING METHOD IN UNMANNED AERIAL VEHICLE AND THE UNMANNED AERIAL VEHICLE) / 드론 조작을 위한 제어 장치(Control device for operating drones) / 무인 비행체 편대 비행 지원 장치(APPARATUS FOR ASSISTING FORMATION FLIGHT OF UNMANNED AERIAL VEHICLE)

경계 제목: 스마트 항공전자 슈트(Smart Avionics Suite) / 에일러론이 미장착되는 쌍발형 고정익 비행체(Fixed wing flight vehicle unequipped aileron) / 구명환 투하 시스템(RESCUE EQUIPMENT DROP SYSTEM)

### C03 마이크로 스피커·이어폰 · 155건

대표 제목에는 마이크로 스피커 구조 / 마이크로스피커의 프레임 구조 / 마이크로스피커의 물 배출 구조가 나타난다. 주요 IPC H04R, G10K, H05K 및 주요 선정분야 인공지능, 로봇를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 마이크로 스피커 구조(Micro speaker structure) / 마이크로스피커의 프레임 구조(Frame structure of microspeaker) / 마이크로스피커의 물 배출 구조(Water drainage structure for microspeaker)

경계 제목: 스마트폰용 유에스비 타입 이어폰 젠더(USB type earphone gender for smartphone) / 케이블 스토퍼부재가 구비된 이어폰(Ear-phone) / 헤드셋의 IR 윈도우 팩키지(IR Window Package in headset)

### C04 혼합 기술군 · 통신·서비스 · 151건

대표 제목에는 개인화된 무선 인터넷 서비스 제공 시스템 / 멀티미디어 서비스 시스템 및 방법 / 다중 모빌리티 관리 시스템의 제어 방법가 나타난다. 주요 IPC H04W, G06Q, H04L 및 주요 선정분야 드론, 인공지능를 함께 확인했다. 중심과 경계 제목의 범위가 넓어 혼합으로 남겼다.

대표 제목: 개인화된 무선 인터넷 서비스 제공 시스템(SYSTEM FOR PROVIDING PERSONALIZED MOBILE INTERNET SERVICE) / 멀티미디어 서비스 시스템 및 방법(System And Method For Serving Multimedia) / 다중 모빌리티 관리 시스템의 제어 방법(METHOD FOR CONTROLLING A MULTI-MOBILITY MANAGEMENT SYSTEM)

경계 제목: 비인가 무선망 및 씨디엠에이 이동통신망 연동 서비스가 가능한 듀얼모드 단말기(Dual Mode Terminal Capable Of Unlicensed Radio Network And CDMA Mobile Communication Network Converged Service) / 사용자가 수행하는 결제 프로세스를 포함하지 않는 무인 결제 시스템(An unmanned payment system that does not include a payment process performed by a user) / 주파수 오프셋 추적기를 이용한 패킷 지연 변이 극복 방법 및 주파수 오프셋 추적기(METHOD TO OVERCOME PACKET DELAY VARIATION USING FREQUENCY OFFSET TRACER AND FREQUENCY OFFSET TRACER)

### C05 신경망 프로세서·NPU · 140건

대표 제목에는 신경망 프로세싱 유닛 / 신경망 프로세싱 유닛 / 신경 프로세싱 유닛 및 이의 동작 방법가 나타난다. 주요 IPC G06N, G06F, G06V 및 주요 선정분야 반도체, 인공지능를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 신경망 프로세싱 유닛(NEURAL NETWORK PROCESSING UNIT) / 신경망 프로세싱 유닛(NEURAL NETWORK PROCESSING UNIT) / 신경 프로세싱 유닛 및 이의 동작 방법(NEURAL PROCESSING UNIT AND OPERATION METHOD THEREOF)

경계 제목: 관통 비아홀 연결을 포함하고 적어도 하나의 나노와이어를 이용하는 신경 소자(Neural device having via hole connection and using at least one nano-wire) / 복수의 위상을 갖는 클럭 신호들에 따라 다수의 NPU들을 구동시키는 SoC(SOC FOR OPERATING PLURAL NPUS ACCORDING TO PLURAL CLOCK SIGNALS HAVING MULTI-PHASES) / 구동중인 컴포넌트를 테스트할 수 있는 NPU(NPU CAPABLE OF TESTING COMPONENT THEREIN DURING RUNTIME)

### C06 라이다·점군 인식 · 122건

대표 제목에는 라이다 장치 / 라이다 장치 / 라이다 장치가 나타난다. 주요 IPC G01S, G02B, H01S 및 주요 선정분야 로봇, 인공지능를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 라이다 장치(LIDAR DEVICE) / 라이다 장치(LIDAR DEVICE) / 라이다 장치(LIDAR DEVICE)

경계 제목: 레이더 및 라이다를 기반으로 하는 자율주행 학습 데이터의 처리 방법 및 실행하기 위하여 기록매체에 기록된 컴퓨터 프로그램(Method for processing data of machine learning for automatic driving based on radar and lidar, and computer program recorded on record-medium for executing method therefor) / 라이다 점군에서 특정된 객체 정보를 이용한 2D 이미지 객체 예측 방법 및 이를 실행하기 위하여 기록매체에 기록된 컴퓨터 프로그램(Method for predicting object of 2D image using object information of point group of a lidar, and computer program recorded on record-medium for executing method therefor) / 라이다 점군으로부터 카메라 이미지의 바운딩 박스를 조정하는 방법 및 이를 실행하기 위하여 기록매체에 기록된 컴퓨터 프로그램(adjusting method of bounding box of camera image from point group of lidar, and computer program recorded on record-medium for executing method thereof)

### C07 디지털 문서·콘텐츠 보안 · 117건

대표 제목에는 디지털 문서의 보안을 위한 방법 및 이를 이용한 장치 / 문서 보안 방법 및 장치 / 디지털 정보 보안 방법 및 그 시스템가 나타난다. 주요 IPC G06F, H04L, G06Q 및 주요 선정분야 인공지능, 드론를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 디지털 문서의 보안을 위한 방법 및 이를 이용한 장치(METHOD AND APPARATUS FOR PROTECTING DIGITAL DOCUMENTS) / 문서 보안 방법 및 장치(Method and Apparatus for Document Secure) / 디지털 정보 보안 방법 및 그 시스템(METHOD OF PROTECTING DIGITAL INFORMATION AND SYSTEMTHEREOF)

경계 제목: 위변조의 확인이 가능한 프레임 바코드가 삽입된 문서를 제작하는 방법 및 장치, 그리고 상기 문서를 인증하는 방법 및 장치(METHOD AND APPARATUS FOR PRODUCING A FRAME-BARCODE INSERTED DOCUMENT WHICH IS CAPABLE OF PREVENTING A FORGERY OR AN ALTERATION OF ITSELF, AND METHOD AND APPARATUS FOR AUTHENTICATING THE DOCUMENT) / 디지털 파일 암호화 방법, 디지털 파일 복호화 방법,디지털 파일 처리 장치 및 암호화 포맷 변환 장치(Digital File Encryption Method, Digital File Decryption Method, Digital File Processing Apparatus and Encryption Format Converting Apparatus) / 메타버스 (Metaverse) 공간에서 DID 에 기초하여 차등적으로 서비스를 제공하는 방법(METHOD FOR PROVIDING SERVICE DIFFERENTIALLY BASED ON DECENTRALIZED IDENTIFIER)

### C08 학습 데이터·모델 관리 · 112건

대표 제목에는 학습 데이터 관리 방법 / 학습 데이터 관리 방법 / 인공지능 학습을 위한 데이터 관리 시스템 및 방법가 나타난다. 주요 IPC G06N, G06F, G06V 및 주요 선정분야 인공지능, 반도체를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 학습 데이터 관리 방법(METHOD FOR MANAGING TRAINING DATA) / 학습 데이터 관리 방법(METHOD FOR MANAGING TRAINING DATA) / 인공지능 학습을 위한 데이터 관리 시스템 및 방법(DATA MANAGEMENT SYSTEM AND METHOD FOR MACHINE LEARNING)

경계 제목: Ontology 및 Agentic AI 기반 AI 프레임워크 제어 시스템(ONTOLOGY AND AGENTIC AI BASED AI FRAMEWORK CONTROL SYSTEM) / 인식 업무를 위한 LLM(Large Language Model)을 사용하여 비정형 쿼리로부터 검색 가능한 쿼리 추정(Seachable Query estimation from unformatted query using Large Language Model for recognition task) / 운량 예측 정보를 고려하여 태양광 발전량을 예측하는 방법(METHOD FOR PREDICTING SOLAR POWER GENERATION CONSIDERING CLOUD COVER PREDICTION INFORMATION)

### C09 안테나·밀리미터파 · 106건

대표 제목에는 밀리미터 웨이브용 안테나 장치 / 안테나 장치 / 밀리미터파 안테나가 나타난다. 주요 IPC H01Q, H01P, G01S 및 주요 선정분야 드론, 우주를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 밀리미터 웨이브용 안테나 장치(Antenna Device for Millimeter Wave) / 안테나 장치(ANTENNA DEVICE WITH HIGH ISOLATION) / 밀리미터파 안테나(ANTENNA FOR MILLIMETER WAVE)

경계 제목: 하니콤 에어스트립라인의 지지구조(Support Structure of Honeycomb Air Stripline) / 전개형 미러 어셈블리(Deployable mirror assembly) / 광대역 모노펄스 피드(Broadband Monopulse Feed)

### C10 모터·구동장치 · 103건

대표 제목에는 모터 구동 장치 / 고정자 구조체 및 액셜 모터 / 모터의 하우징 압입 구조체가 나타난다. 주요 IPC H02K, F16H, H02P 및 주요 선정분야 로봇, 드론를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 모터 구동 장치(Device for driving a motor) / 고정자 구조체 및 액셜 모터(Stator Structure And Axial Motor) / 모터의 하우징 압입 구조체(Housing press fitting structure of motor)

경계 제목: 모세관형 일렉트로 스프레이(Capillary Electrospray) / 틸팅기능과 주차브레이크 장치가 구비된 전동스쿠터(electrical scooter) / 모터용 컨넥터(Motor connector)

### C11 광학·조준·열상 장치 · 100건

대표 제목에는 열상 장치용 대물렌즈계 / 목표물의 조준 방법 및 장치 / 광학장치가 나타난다. 주요 IPC G02B, F41G, G01J 및 주요 선정분야 기타, 드론를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 열상 장치용 대물렌즈계(Objective lens system for thermal image device) / 목표물의 조준 방법 및 장치(Method and apparatus for aiming target) / 광학장치(Apparatus of optics instrument)

경계 제목: 핸드폰을 이용한 어군확인 초음파 낚시찌(A FLOAT FOR FISH GROUP CONFIRMATION) / 탈부착이 용이한 수중익선의 전방감시소나용 포드(Foward Looking Sonar POD of Hydrofoil) / 항공기 투하용 소노부이(SONOBUOY FOR AIRDROP)

### C12 광섬유·광통신 · 95건

대표 제목에는 광섬유의 제조방법 / 광섬유 및 그 제조방법 / 광섬유 모재의 제조 방법 및 광섬유 모재가 나타난다. 주요 IPC G02B, C03B, H04B 및 주요 선정분야 드론, 반도체를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 광섬유의 제조방법(METHOD FOR MANUFACTURING OPTICAL FIBER) / 광섬유 및 그 제조방법(Optical fiber and method for making the same) / 광섬유 모재의 제조 방법 및 광섬유 모재(The Method of Optical Fiber and Optical Fiber thereof)

경계 제목: 고분자 바인더로 개질된 폴리(메타)아크릴레이트를함유하는 광고분자 조성물(Photopolymer Composition Comprising ModifiedPolymetacrylate Derivatives as Polymer Binder) / 광 파워미터(Optical powermeter) / 통신복합조가선(COMMUNICATION COMPOSITE SUSPENSION WIRE)

### C13 질화물 반도체·결정 성장 · 92건

대표 제목에는 3차원 질화물 구조 도입을 통한 고품질 GaN HEMT 전력반도체 에피택시 웨이퍼 및 그 제조 방법 / 그룹3족 질화물 반도체 템플릿의 제조 방법 / 질화물 반도체 제조방법가 나타난다. 주요 IPC H10D, H10P, H10H 및 주요 선정분야 반도체, 기타를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 3차원 질화물 구조 도입을 통한 고품질 GaN HEMT 전력반도체 에피택시 웨이퍼 및 그 제조 방법(High-quality GaN HEMT power semiconductor epitaxial wafer manufacturing method by introducing a 3D nitride structure) / 그룹3족 질화물 반도체 템플릿의 제조 방법(METHOD FOR MANUFACTURING GROUP 3 NITRIDE SEMICONDUCTOR TEMPLATE) / 질화물 반도체 제조방법(Method for fabricating a nitride compound semiconductor)

경계 제목: 단결정 성장용 시드(SEED FOR GROWING SINGLE CRYSTAL) / 파우더가 도포된 Ⅲ―Ⅴ족 화합물 반도체 발광소자(Powder-coated Ⅲ-Ⅴ compound semiconductor light emitting device) / 핫 셀프스플릿 공정을 통한 SiC 전력반도체 소자 제조 방법(Method for manufacturing SiC power device through hot self-split process)

### C14 디지털 워터마킹 · 87건

대표 제목에는 워터마크 삽입 방법 및 장치, 및 시스템 / 디지털 워터마킹 방법 및 장치 / 디지털 워터마크의 삽입 및 검출을 위한 방법 및 장치가 나타난다. 주요 IPC H04N, G06T, G11B 및 주요 선정분야 인공지능, 로봇를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 워터마크 삽입 방법 및 장치, 및 시스템(WATERMARK EMBEDDING METHOD AND APPARATUS, AND SYSTEM) / 디지털 워터마킹 방법 및 장치(DIGITAL WATERMARKING METHOD AND APPARATUS) / 디지털 워터마크의 삽입 및 검출을 위한 방법 및 장치(METHOD AND APPARATUS FOR DIGITAL WATERMARK EMBEDDING AND EXTRACTING)

경계 제목: 오프라인상의 문서 또는 물품의 정보를 포함하는 스티커를제작하는 방법 및 장치, 그리고 상기 방법에 의해 제작된스티커(METHOD AND APPARATUS OF MANUFACTURING A STICKERCONTAINING AN INFORMATION OF AN OFFLINE DOCUMENT ANDGOODS, AND A STICKER MANUFACTURED BY SAID METHOD) / 휴대용 WMA 복호화 장치(Portable WMA decoder) / 추적 정보를 삽입하여 컨텐츠를 전송하는 방법 및 장치, 그리고 추적 정보를 삽입하여 컨텐츠를 수신하는 방법 및 장치(METHOD AND APPARATUS FOR TRANSMITTING CONTENT BY INSERTING TRACKING INFORMATION, AND METHOD AND APPARATUS FOR RECEIVING CONTENT BY INSERTING TRACKING INFORMATION)

### C15 어노테이션·데이터 작업 · 83건

대표 제목에는 어노테이션 작업 제어 방법 및 이를 실행하기 위하여 기록매체에 기록된 컴퓨터 프로그램 / 지점 지정을 통한 어노테이션 방법 및 이를 실행하기 위하여 기록매체에 기록된 컴퓨터 프로그램 / 어노테이션 작업 및 질의 제어 방법 및 이를 실행하기 위하여 기록매체에 기록된 컴퓨터 프로그램가 나타난다. 주요 IPC G06N, G06T, G06F 및 주요 선정분야 인공지능, 센서를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 어노테이션 작업 제어 방법 및 이를 실행하기 위하여 기록매체에 기록된 컴퓨터 프로그램(Method for controlling annotation work, and computer program recorded on record-medium for executing method therefor) / 지점 지정을 통한 어노테이션 방법 및 이를 실행하기 위하여 기록매체에 기록된 컴퓨터 프로그램(Annotation method through point designation and a computer program recorded on a recording medium to execute it) / 어노테이션 작업 및 질의 제어 방법 및 이를 실행하기 위하여 기록매체에 기록된 컴퓨터 프로그램(Method for controlling annotation work and question, and computer program recorded on record-medium for executing method therefor)

경계 제목: 자율주행 데이터 수집을 위한 센서 간의 위상차 제어 방법 및 실행하기 위하여 기록매체에 기록된 컴퓨터 프로그램(Method for correcting difference of multiple sensors, and computer program recorded on record-medium for executing method therefor) / 웹에서 SSH를 이용한 노심해석코드를 실행하는 방법 및 시스템과 그 방법을 기록한 컴퓨터판독가능한 기록매체(System and Method for Performing Core Analysis Code and Computer-readable Recording Medium Storing the Method) / 인공지능과 전자현미경 및 EDS 분석기를 이용하여 대면적에 분포된 미세 입자를 자동 분석하는 방법(Method for automatically analyzing micro particles distributed over a large area using artificial intelligence, electron microscope and EDS analyzer)

### C16 위성항법·위성 운용 · 82건

대표 제목에는 위성항법 신호의 추적을 위한 장치 / 위성항법 신호의 획득을 위한 장치 / 위성 항법 시스템의 재밍 처리 장치 및 재밍 처리 방법가 나타난다. 주요 IPC G01S, G06F, B64G 및 주요 선정분야 우주, 기타를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 위성항법 신호의 추적을 위한 장치(Apparatus for Tracking a Satellite Navigation Signal) / 위성항법 신호의 획득을 위한 장치(Apparatus for Acquisition of a Satellite Navigation Signal) / 위성 항법 시스템의 재밍 처리 장치 및 재밍 처리 방법(ANTI-JAMMING APPARATUS FOR GLOBAL NAVIGATION SATELLITE SYSTEM AND ANTI-JAMMING METHOD FOR GLOBAL NAVIGATION SATELLITE SYSTEM)

경계 제목: 비용에 따른 임무 효율을 고려하는 위성체의 궤도상 서비스에 대한 임무 설계안 도출 방법 및 시스템(METHOD AND SYSTEM FOR DERIVING A MISSION DESIGN PLAN FOR SATELLITE ON-ORBIT SERVICE THAT CONSIDERS MISSION EFFICIENCY ACCORDING TO COST) / 위성의 궤도결정을 위한 GNSS/IMU 통합 칼만필터 알고리즘 방법, 이를 구현하기 위한 프로그램이 저장된 기록매체.(THE ALGORITHM OF KALMAN FILTER INTEGRATING GNSS AND INS FOR ORBIT DETERMINATION OF A SATELLITE AND RECORDING MEDIUM STORING PROGRAM FOR EXECUTING THE SAME) / 인공위성 용 지구 재진입 장치 및 이를 포함하는 인공위성(Earth Re-entry Apparatus for Satellites and Satellites having the Same)

### C17 혼합 기술군 · 음향·센싱 · 71건

대표 제목에는 음향 기반 현장 모니터링 방법 및 시스템 / 맥파 검출용 음향출력장치 / 길이가 조절되는 탄성파 수집 봉가 나타난다. 주요 IPC G01N, G01S, G01L 및 주요 선정분야 드론, 기타를 함께 확인했다. 중심과 경계 제목의 범위가 넓어 혼합으로 남겼다.

대표 제목: 음향 기반 현장 모니터링 방법 및 시스템(METHOD AND SYSTEM FOR ACOUSTICS-BASED ON-SITE MONITORING) / 맥파 검출용 음향출력장치(AN AUDIO RECEIVER FOR MEASURING PULSE WAVE) / 길이가 조절되는 탄성파 수집 봉(A measurement device of elastic wave that is adjustable length)

경계 제목: 전력망이나 전력 설비의 상시 안전 감시 시스템(Off-site safety surveilance system in electric power network or utilities) / 멀티빔 사이드스캔소나의 트랜스듀서(multiple electron beam side scan sonar) / 다중 빔을 이용한 고해상도 측면 주사 소나 시스템의 진행방향 해상도 향상을 위한 트랜스듀서의 셀 배치 구조.(Using a high-resolution multi-beam sonar system the direction of the side injectin for improving the resolution cell of the rtansducer arrangement)

### C18 반도체 발광소자 · 64건

대표 제목에는 반도체 발광소자를 제조하는 방법 / 반도체 발광소자를 제조하는 방법 / 반도체 발광소자를 제조하는 방법가 나타난다. 주요 IPC H10H, H01S, H10P 및 주요 선정분야 반도체, 로봇를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 반도체 발광소자를 제조하는 방법(METHOD OF MANUFACTURING A LIGHT EMITTING DEVICE) / 반도체 발광소자를 제조하는 방법(METHOD OF MANUFACTURING A LIGHT EMITTING DEVICE) / 반도체 발광소자를 제조하는 방법(METHOD OF MANUFACTURING A LIGHT EMITTING DEVICE)

경계 제목: 빅셀 구동용 레이저 드라이버(LASER DRIVER FOR DRIVING VCSEL) / 수직공진 표면발광레이저(Vertical-cavity surface-emitting laser) / 핫 셀프스플릿 공정을 통한 박막형 칩 구조의 고출력 자외선 발광소자 및 그 제조방법(High-output ultra-violet(UV) LED with thin-film chip structure through hot self-split process and method for manufacturing the same)

### C19 전기화학 소자·전지 · 64건

대표 제목에는 전기화학 소자 및 이의 제조방법 / 전기화학 소자 및 이의 제조방법 / 전기화학 소자 및 이의 제조방법가 나타난다. 주요 IPC H01M, H01G, H01B 및 주요 선정분야 드론, 우주를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 전기화학 소자 및 이의 제조방법(Electrochemical device and manufacturing method thereof) / 전기화학 소자 및 이의 제조방법(Electrochemical device and manufacturing method thereof) / 전기화학 소자 및 이의 제조방법(Electrochemical device and its manufacturing method)

경계 제목: 중공형 금속 미분체를 포함하는 고분자 기재 금속 필라멘트 및 이의 제조방법(Metal Filament wherein Hollow Metal Particles Dispersed in Polymer Matrix And Method Thereof) / 자전연소 합성법을 이용한 붕소 입자 제조 방법(Preparation Method of Boron particles by using Self-propagating High-temperature Synthesis(SHS)) / 고체산화물 연료 전지(Solid oxide fuel cell)

### C20 원전·소화·안전설비 · 61건

대표 제목에는 원자력발전소 가스소화설비 설계농도 측정 및 유지 장치 / 원전의 가스계 소화약제 방출시험 방법 / 원자력 발전소 방화지역의 상대적 종합안전위험관리 시스템 및 그 방법가 나타난다. 주요 IPC G21C, G21D, A62C 및 주요 선정분야 기타, 센서를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 원자력발전소 가스소화설비 설계농도 측정 및 유지 장치(Monitoring and Actuating device for Gas Extinguishing System in Nuclear Power Plant) / 원전의 가스계 소화약제 방출시험 방법(Method for Emission Test of Gaseous Extinguishing Agent in Nuclear Power Plant) / 원자력 발전소 방화지역의 상대적 종합안전위험관리 시스템 및 그 방법(System for monitoring relative safety hazards of nuclear plant fire protection areas and method thereof)

경계 제목: 소화약제 연장 방출 시스템(Extinguishing Agent Extended Emission System) / 원전 설비 해체용 작업장(Workplace for Dismantling Nuclear Power Plant) / 소화약제 회수 및 플러싱 기능을 갖는 화재 진압 시스템(Fire Suppression System with Fire Extinguishing Agent Return and Flushing Function)

### C21 반도체 공정·제조 · 60건

대표 제목에는 반도체 소자의 제조방법 / 반도체 소자의 제조방법 / 반도체 소자의 제조 방법가 나타난다. 주요 IPC H10D, H10W, H10P 및 주요 선정분야 반도체, 드론를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 반도체 소자의 제조방법(METHOD OF MANUFACTURING A SEMICONDUCTOR DEVICE) / 반도체 소자의 제조방법(METHOD OF MANUFACTURING A SEMICONDUCTOR DEVICE) / 반도체 소자의 제조 방법(METHOD OF MANUFACTURING A SEMICONDUCTOR DEVICE)

경계 제목: 칩 좌표 정보가 표시된 웨이퍼(Wafer with chip coordinates) / 단일 챔버 내에서 기판의 양면에 박막 형성이 가능한 롤투롤 스퍼터링 장치(Roll-to-roll sputtering device capable of forming thin films on both sides of the substrate within a single chamber) / 단일 챔버 내에서 기판의 양면에 박막 형성이 가능한 롤투롤 스퍼터링 장치(Roll-to-roll sputtering device capable of forming thin films on both sides of the substrate within a single chamber)

### C22 증강현실·객체 추적 · 60건

대표 제목에는 AR 객체 트래킹 방법 및 시스템 / 공간 인식 및 사물 인식이 동시에 적용된 증강현실 시스템 / 증강현실을 위한 객체 트래킹 방법 및 시스템가 나타난다. 주요 IPC G06T, G06F, G06Q 및 주요 선정분야 기타, 로봇를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: AR 객체 트래킹 방법 및 시스템(METHOD AND SYSTEM FOR AUGMENTED-REALITY OBJECT TRACKING) / 공간 인식 및 사물 인식이 동시에 적용된 증강현실 시스템(Augmented Reality System with Space and Object Recognition) / 증강현실을 위한 객체 트래킹 방법 및 시스템(METHOD AND SYSTEM FOR TRACKING OBJECT FOR AUGMENTED REALITY)

경계 제목: 웹 환경에서 구현되는 수중탐사장비의 3차원 시뮬레이션 시스템(3D simulation system of underwater information searching machine managing on web) / 실물 객체에 대한 정밀한 추적을 위해 카메라 모듈의 내부 및 외부 파라미터를 계산하는 자동화된 캘리브레이션 시스템, 캘리브레이션 방법 및 캘리브레이션 방법을 기초로 이미지 내에서 실물 객체를 추적하고 실물 객체에 가상 모델을 증강하는 방법(An automated calibration system for calculating intrinsic parameter and extrinsic parameter of a camera module for precise tracking a real object, a calibration method, and a method for tracking a real object in an image based on the calibration method and augmenting a virtual model on the real object) / 타겟 객체의 디지털 모델로부터 에지의 특성을 검출하고 샘플 포인트를 설정하여 타겟 객체를 학습하는 방법 및 이를 이용하여 타켓 객체를 구현한 실물 객체에 가상 모델을 증강하는 방법(A method for learning a target object by detecting an edge from a digital model of the target object and setting sample points, and a method for augmenting a virtual model on a real object implementing the target object using the same)

### C23 커넥터·연결 회로 · 56건

대표 제목에는 케이블 커넥터 및 이를 포함하는 케이블 조립체 / RF 커넥터 및 이를 이용하는 디바이스 연결 방법 / 리셉터클 커넥터와 플러그 커넥터를 포함하는 커넥터 조립체가 나타난다. 주요 IPC H01R, G01R, H01P 및 주요 선정분야 드론, 우주를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 케이블 커넥터 및 이를 포함하는 케이블 조립체(Cable connector and cable assembly having the same) / RF 커넥터 및 이를 이용하는 디바이스 연결 방법(RF CONNECTOR AND METHOD FOR CONNECTING DEVICES USING SAME) / 리셉터클 커넥터와 플러그 커넥터를 포함하는 커넥터 조립체(Connector assembly including receptacle connector and plug connector)

경계 제목: 랫-레이스 회로(Rat-Race Circuit) / IP 카메라 선로용 HEMP 필터 장치(HEMP Filter for IP Camera Line) / 차량 무선기기용 전원 안정화 필터(Power stabilization filter for wireless devices in vehicles)

### C24 3D 점군·모델 생성 · 53건

대표 제목에는 3D 점군 데이터 일괄 처리 방법 / 3차원 바운딩 박스 데이터 생성 방법 및 시스템 / 3차원 모델 생성 장치 및 방법가 나타난다. 주요 IPC G06T, G01S, G06N 및 주요 선정분야 인공지능, 기타를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 3D 점군 데이터 일괄 처리 방법(Batch processing method of 3D points group, and computer program recorded on record-medium for executing method thereof) / 3차원 바운딩 박스 데이터 생성 방법 및 시스템(METHOD AND SYSTEM FOR GENERATING 3-DIMENTIONAL BOUNDING BOX DATA) / 3차원 모델 생성 장치 및 방법(Apparatus and method for generating three-dimensional model)

경계 제목: 전자해도 좌표 체계 및 텍스쳐 매핑에 의한 객체 표현이 가능한 3차원 전자해도 시스템(system for generating 3 dimensional electronic nautical chart capable of expressing object using electronic nautical chart coordinates and texture mapping) / 전자해도 면 객체의 삼각화 표현이 가능한 3차원 전자해도 시스템(system for generating 3 dimensional electronic nautical chart capable of expressing triangulated area object) / 2D 경로 추론을 통한 동일 객체 추적 방법 및 이를 실행하기 위하여 기록매체에 기록된 컴퓨터 프로그램(Method for tracking object through 2D path inference, and computer program recorded on record-medium for executing method therefor)

### C25 혼합 기술군 · RF·패키지 · 48건

대표 제목에는 복수개의 유전체 블럭을 포함하는 세라믹 도파관 필터 / 비방사 유전체 도파관을 이용한 금속 포스트 필터 조립체 / RF 트랜지스터 패키지 및 이의 제조방법가 나타난다. 주요 IPC H01P, H10W, G06K 및 주요 선정분야 반도체, 드론를 함께 확인했다. 중심과 경계 제목의 범위가 넓어 혼합으로 남겼다.

대표 제목: 복수개의 유전체 블럭을 포함하는 세라믹 도파관 필터(Ceramin Waveguide Filter Including Muliple Dielectric Blocks) / 비방사 유전체 도파관을 이용한 금속 포스트 필터 조립체(METAL POST FILTER ASSEMBLY USING NON-RADIATIVEDIELECTRIC WAVEGUIDE) / RF 트랜지스터 패키지 및 이의 제조방법(RF TRANSISTOR PACKAGE AND FABRICATING METHOD OF THE SAME)

경계 제목: CMOS 오실레이터를 포함하는 크리스털-프리 블루투스 IC, 및 상기 블루투스 IC를 포함하는 블루투스 패키지(CRYSTAL-FREE BLUETOOTH INTEGRATED CHIP INCLUDING CMOS OSCILLATOR, AND BLUETOOTH PACKAGE INCLUDING THE SAME) / 패키지 레벨에서 온도 모니터링이 가능한 알에프 소자 패키지(RF Device Package capable of monitoring Temperature at Package Level) / 엔알디가이드와 구형도파관의 직접접속방법과 이를 위한엔알디가이드(Method for coupling an NRD waveguide with arectangular waveguide directly and NRD waveguidethereof)

### C26 전기음향 변환·진동 · 46건

대표 제목에는 전기-음향변환장치의 진동체 제조방법 / 전기-음향변환장치 / 전기음향변환장치가 나타난다. 주요 IPC H04R, H02K, B06B 및 주요 선정분야 인공지능, 기타를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 전기-음향변환장치의 진동체 제조방법(METHOD FOR FABRICATING BIVRATOR OF ELECTRO-ACOUSTICTRANSDUCER) / 전기-음향변환장치(ELECTRIC-ACOUSTIC TRNSDUCER) / 전기음향변환장치(ELECTRO-ACOUSTIC TRANSDUCER)

경계 제목: 장방형 수직 선형 엑츄에이터(vertical linear type rectangular actuator) / 수평형 리니어 진동기(Linear type vibration motor vibrated horizontally) / 컨틸레버형 진동발생기(CANTILEVER TYPE VIBRATOR)

### C27 극저온·수소 저장 · 46건

대표 제목에는 액화수소 공급 시스템 / 냉각장치를 이용한 초저온 증류시스템 / 극저온 수소저장용기의 열 유입 차단 장치가 나타난다. 주요 IPC F25J, F17C, B01D 및 주요 선정분야 드론, 기타를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 액화수소 공급 시스템(LIQUIFIED HYDROGEN SUPPLY SYSTEM) / 냉각장치를 이용한 초저온 증류시스템(Cryogenic Distillation System Using Cooling Device) / 극저온 수소저장용기의 열 유입 차단 장치(Apparatus for Heat Blocking in Cryogenic Hydrogen Storage Tank)

경계 제목: 탄소 포집을 위한 블루카본 리포트 생성 방법 및 시스템(METHOD AND SYSTEM FOR GENERATE BLUE CARBON REPORT FOR CARBON CAPTURE) / 랙 콘덴싱 타입 냉각 시스템(Rack Condensing Type Cooling System) / 삼중 극저온 유체이송관(TRIPLE CRYOGENIC FLUID DELIVERY LINERS)

### C28 압전체·초음파 · 43건

대표 제목에는 유전상수 저하가 적은 단결정 압전체 / 압전특성 측정방법 / 압전특성 측정장치가 나타난다. 주요 IPC H10N, G01N, H01L 및 주요 선정분야 기타, 반도체를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 유전상수 저하가 적은 단결정 압전체(PIEZOELECTRIC BODY OF SINGLE CRYSTAL WITH LOW REDUCTION OF DIELECTRIC CONSTANT) / 압전특성 측정방법(Method for measuring piezoelectricity) / 압전특성 측정장치(Apparatus for measuring piezoelectricity)

경계 제목: 고주파형 초음파 센서(High Frequency Type Ultrasonic Sensor) / Y cut LiNbO3을 이용한 전단용 트랜스듀서(A transducer for shear mode using Y cut LiNbO3) / 분광학적 타원해석법을 이용하여 강유전체 단결정의물리적 물성을 측정하기 위한 장치 및 방법(APPARATUS AND METHOD FOR DETERMINING PHYSICALPROPERTIES OF FERROELECTRIC SINGLE CRYSTAL USINGSPECTROSCOPIC ELLIPSOMETRY)

### C29 자율주행 시뮬레이션 · 43건

대표 제목에는 자율 주행 알고리즘의 성능 평가 방법 및 이를 지원하는 전자 장치 / 주행 시뮬레이션 데이터를 생성하는 방법 및 시스템 / 무인 이동체의 주행 시뮬레이션 환경 생성 방법 및 시스템가 나타난다. 주요 IPC G06F, B60W, G06T 및 주요 선정분야 인공지능, 로봇를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 자율 주행 알고리즘의 성능 평가 방법 및 이를 지원하는 전자 장치(METHOD FOR EVALUATING PERFORMANCE OF AUTONOMOUS DRIVING ALGORITHM AND ELECTRONIC DEVICE SUPPORTING THE SAME) / 주행 시뮬레이션 데이터를 생성하는 방법 및 시스템(METHOD AND SYSTEM FOR GENERATING DRIVING SIMULATION DATA) / 무인 이동체의 주행 시뮬레이션 환경 생성 방법 및 시스템(METHOD AND SYSTEM FOR GENERATING DRIVING SIMULATION EVIRONMENT FOR UNMANNED VEHICLE)

경계 제목: 자동차의 주변 상황이 위험상황인지를 판단하고 주행가이드를 생성하여 경보하여 주는 방법 및 이를 이용한 장치(METHOD FOR ALERTING WHEN SURROUNDING SITUATION OF CAR IS DANGEROUS SITUATION BY DRIVING GUIDE, AND DEVICE USING THE SAME) / 차량 좌회전 감응신호 제어방법 및 장치(A sensitive left turn signal control method and the device in use with) / 다이내믹 시뮬레이션용 2축 모션 베이스(TWO AXIS MOTION BASE FOR DYNAMIC SIMULATION)

### C30 혼합 기술군 · 기기 제어 · 41건

대표 제목에는 사용자 적응형 모바일 디바이스 제어 방법 및 시스템 / 동적 장치 제어 방법 및 그 장치 / 조절 장치 및 방법가 나타난다. 주요 IPC G06F, G06N, G05B 및 주요 선정분야 로봇, 인공지능를 함께 확인했다. 중심과 경계 제목의 범위가 넓어 혼합으로 남겼다.

대표 제목: 사용자 적응형 모바일 디바이스 제어 방법 및 시스템(USER ADAPTIVE METHOD AND SYSTEM FOR CONTROLLING MOBILE DEVICE) / 동적 장치 제어 방법 및 그 장치(METHOD FOR CONTROLLING A DYNAMIC APPARATUS ANDAPPARARTUS THEREOF) / 조절 장치 및 방법(Apparatus and Method for Controlling Display Devices)

경계 제목: 개량 커패시턴스 터치스크린(Capacitance touch screen) / 1차원 터치포인트 포지셔닝 커패시턴스 터치스크린(1-Dimensional touchpoint positioning capacitance touch screen) / 프로젝터를 구비한 모바일 기기 및 모바일 기기에 구비된 프로젝터가 투사하는 영상을 제어하는 방법(Mobile device including a projector and method for controlling images projected by a projector included in a mobile device)

### C31 거리·위치 측정 · 38건

대표 제목에는 거리 측정 장치 / 거리 측정 장치 / 거리 측정 장치가 나타난다. 주요 IPC G01S, G01C, G02B 및 주요 선정분야 기타, 로봇를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 거리 측정 장치(Distance measuring apparatus) / 거리 측정 장치(DISTANCE MEASURING DEVICE) / 거리 측정 장치(DISTANCE MEASURING DEVICE)

경계 제목: 레일 이동장치의 위치 보정 시스템(Correction System for the Positioning of the railmachine) / 차선 이동장치의 위치 보정 시스템(Correction System for the Positioning of the trackmachine) / 가속도 감지수단을 이용한 피치각/롤각 측정장치 및 그 방법(Pitch/Roll angle sensing mean using accelerometer andmethod thereof)

### C32 마이크로디스플레이·LED · 37건

대표 제목에는 마이크로디스플레이 패널 및 그 제조 방법 / 마이크로디스플레이 패널 및 그 제조 방법 / 마이크로디스플레이 패널 및 그 제조 방법가 나타난다. 주요 IPC H10H, H10W, H10D 및 주요 선정분야 반도체, 드론를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 마이크로디스플레이 패널 및 그 제조 방법(MICRODISPLAY PANEL AND MANUFACTURING METHOD THEREOF) / 마이크로디스플레이 패널 및 그 제조 방법(MICRODISPLAY PANEL AND MANUFACTURING METHOD THEREOF) / 마이크로디스플레이 패널 및 그 제조 방법(MICRODISPLAY PANEL AND MANUFACTURING METHOD THEREOF)

경계 제목: 마이크로 엘이디 디스플레이용 무선 알지비 엘이디(WIRELESS RGB LED FOR MICRO LED DISPLAY) / 단결정 LLO 희생분리층을 포함하는 템플릿 기판 및 이를 이용한 고수율의 마이크로LED 칩 광원 제조 방법(Template substrate with single-crystal LLO sacrificial separation layer and method for manufacturing high-yield micro-LED chip light source using the same) / 투명 벤딩 필름이 결합된 디스플레이 장치(DISPLAY APPARATUS OF FLEXIBLE BENDING FILM)

### C33 지도·위치정보 생성 · 36건

대표 제목에는 유저 기반의 지도 제작 장치 / 수색 영역 정보 생성 장치 및 방법 / 수색 영역 정보 생성 장치 및 방법가 나타난다. 주요 IPC H04W, G01C, G06T 및 주요 선정분야 인공지능, 드론를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 유저 기반의 지도 제작 장치(USER BASED MAP MANUFACTURING APPARATUS) / 수색 영역 정보 생성 장치 및 방법(APPARATUS AND METHOD FOR GENERATING SEARCH AREA INFORMATION) / 수색 영역 정보 생성 장치 및 방법(APPARATUS AND METHOD FOR GENERATING SEARCH AREA INFORMATION)

경계 제목: LTE 신호기반 요구조자 위치측위 서버, 방법 및 컴퓨터 판독가능 기록매체(SERVER FOR POSITIONING VICTIM BASED ON LTE SIGNAL, METHOD THEREFOF AND COMPUTER READABLE RECORDING MEDIUM) / 선박 정보 제공 장치(SHIP INFORMATION PROVIDING DEVICE) / 위치기반의 대리운전 고객 접수/처리 장치(The device which receives/handles the designated-driver service user based on the location)

### C34 비디오 메타데이터·전송 · 35건

대표 제목에는 비디오 메타데이터 증대를 위한 장치 또는 방법 / 영상 데이터 전송을 위한 데이터 변환 방법 및 그를 위한 장치 / 동영상 메타데이터 태깅 시스템 및 그 방법가 나타난다. 주요 IPC H04N, G06F, G06T 및 주요 선정분야 인공지능, 반도체를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 비디오 메타데이터 증대를 위한 장치 또는 방법(Apparatus or Method for Enhancing Video Metadata) / 영상 데이터 전송을 위한 데이터 변환 방법 및 그를 위한 장치(Method and Apparatus for Converting Data for Video Data Transmission) / 동영상 메타데이터 태깅 시스템 및 그 방법(Video metadata tagging system and method thereof)

경계 제목: 비디오 콘텐츠에 대한 위변조를 방지하기 위한 부가데이터를 검출하여 디스플레이하는 장치, 방법 및 시스템, 상기 디스플레이 장치와 연동하는 재생장치, 상기 장치의 재생방법(DISPLAY APPARATUS, METHOD AND SYSTEM DISPLAYING CONTENT BY DETECTING ADDITIONAL DATA FOR PREVENTING COUNTERFEIT AND FALSIFICATION FOR VIDEO CONTENT, RENDERING APPARATUS INTERLOCKING WITH SAID DISPLAY APPARATUS, AND RENDERING METHOD OF SAID RENDERING APPARATUS) / 디스플레이 미러링을 위한 멀티미디어 콘텐츠의 실시간 무선 송수신 시스템 및 방법(Real-time wireless transmission and reception system and method for multimedia contents's display mirroring) / 동영상 콘텐츠 식별을 위한 정보 추출 방법 및 장치, 상기 방법을 이용한 동영상 콘텐츠 식별 방법 및 장치, 및 동영상 콘텐츠 식별 시스템(METHOD AND APPARATUS FOR EXTRACTING INFORMATION FOR IDENTIFYING VIDEO CONTENT, VIDEO CONTENT INDENTIFICATION METHOD AND APPARATUS USING SAID METHOD, AND VIDEO CONTENT INDENTIFICATION SYSTEM)

### C35 혼합 기술군 · 움직임·생체신호 · 34건

대표 제목에는 움직임을 인식하는 장치 및 방법 / 이벤트 감지 방법 및 이를 실행하는 장치 / 움직임 감지를 통한 사용자 명령 입력 방법 및 디바이스가 나타난다. 주요 IPC A61B, G06F, G08B 및 주요 선정분야 로봇, 인공지능를 함께 확인했다. 중심과 경계 제목의 범위가 넓어 혼합으로 남겼다.

대표 제목: 움직임을 인식하는 장치 및 방법(Apparatus and method for recognizing movement) / 이벤트 감지 방법 및 이를 실행하는 장치(METHOD OF SENING EVENT AND APPARATUS PERFORMING THE SAME) / 움직임 감지를 통한 사용자 명령 입력 방법 및 디바이스(Method and Device for inputing user's commands based on motion sensing)

경계 제목: 포인터 이동 값 계산 장치, 포인터 이동 값 보정 방법 및자세 각도 변화량 보정 방법, 이를 사용하는 3차원 포인팅디바이스(Apparatus for calculating pointer movement value and method for correcting pointer movement value and variation of angle, 3D pointing device using the same) / 손목형 디지털 혈압계(Digital hemadynamometer of wristwatch type) / 생체신호 측정장치와 생체신호 영상화장치 그리고 뇌영상 기반 뇌질환 진단 시스템(BIO SIGNAL MEASURING DEVICE AND BIO SIGNAL IMAGING DEVICE AND BRAIN IMAGING BASED BRAIN DISEASE DIAGNOSTIC SYSTEM)

### C36 음원·음성 인식 · 32건

대표 제목에는 이상 음원 탐지 장치 및 방법 / 인공지능 기반의 이상음원 인식 장치, 그 방법 및 이를 이용한 관제시스템 / 인공지능 기반의 이상음원 인식 장치, 그 방법 및 이를 이용한 관제시스템가 나타난다. 주요 IPC G10L, G06F, G06N 및 주요 선정분야 인공지능, 기타를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 이상 음원 탐지 장치 및 방법(APPARATUS AND METHOD FOR DETECTING UNUSUAL SOUND) / 인공지능 기반의 이상음원 인식 장치, 그 방법 및 이를 이용한 관제시스템(ABNORMALY SOUND RECOGNIZING METHOD AND APPARATUS BASED ON ARTIFICIAL INTELLIGENCE AND MONITORING SYSTEM USING THE SAME) / 인공지능 기반의 이상음원 인식 장치, 그 방법 및 이를 이용한 관제시스템(ABNORMALY SOUND RECOGNIZING METHOD AND APPARATUS BASED ON ARTIFICIAL INTELLIGENCE AND MONITORING SYSTEM USING THE SAME)

경계 제목: 인공지능 기반 음성 대화 환경을 제공하는 방법, 스마트 전자 장치 및 시스템(A method, a smart electronic device, and a system for providing an artificial intelligence-based voice conversation environment) / 딥 러닝 기반으로 음향 및 진동을 이용하여 기계의 고장을 진단하는 방법 및 이를 이용한 진단 장치(METHOD FOR DIAGNOSING MACHINE FAILURE USING SOUND AND VIBRTION BASED ON DEEP LEARNING AND DIAGNOSTIC DEVICE USING THEM) / 인공지능을 이용한 음성 기반 세일즈 정보 추출 및 리드 추천방법과 이를 수행하는 데이터 분석장치(Voice-based sales information extraction and lead recommendation method using artificial intelligence, and data analysis apparatus therefor)

### C37 고주파 전력·증폭 회로 · 29건

대표 제목에는 고주파 전력 증폭기 / 고주파 전력 증폭기 / 위상이 조절되는 알에프 파워 제너레이터가 나타난다. 주요 IPC H03F, H02M, H03K 및 주요 선정분야 반도체, 드론를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 고주파 전력 증폭기(High frequency power amplifier) / 고주파 전력 증폭기(HIGH FREQUENCY POWER AMPLIFIER) / 위상이 조절되는 알에프 파워 제너레이터(Phase adjusted RF power generator)

경계 제목: 엑스 밴드 및 쿠 밴드에서 동작하는 저잡음 증폭기(Low noise amplifier for working over X band and Ku band) / 파워 증폭기(Power amplifier) / 고속차단기능을 가지는 단락보호회로(High speed short protection circuits)

### C38 복합재·성형 · 27건

대표 제목에는 열가소성 복합재를 이용한 항공기 좌석부품 제조 방법 / 열가소성 복합재 튜브 밴딩장치 / 열가소성 복합재가 적용된 튜브 제작을 위한 와인딩 성형 장치 및 그 방법가 나타난다. 주요 IPC B29C, G06F, B21D 및 주요 선정분야 우주, 로봇를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 열가소성 복합재를 이용한 항공기 좌석부품 제조 방법(MANUFACTURING METHOD FOR SEAT PART OF AIRCRAFT USING THERMOPLASTIC COMPOSITE) / 열가소성 복합재 튜브 밴딩장치(Device for bending a thermoplastic composite tube) / 열가소성 복합재가 적용된 튜브 제작을 위한 와인딩 성형 장치 및 그 방법(WINDING APPARATUS FOR THERMOPLASTIC COMPOSITE TUBES AND THE METHOD OF THEREOF)

경계 제목: 피스톤링의 표면 열처리 방법 및 그 피스톤링(Heating processing method for surface of piston ringand A Piston ring) / 복합재 이너프레임 다중 접합형 배럴을 포함하는 외피 일체형 발사체 추진제 탱크 및 이의 제조방법(Skirt integral composite propellant tank containing Barrel fastened or bonded with multiple composite inner frames and manufacturing method thereof) / 크기 조절이 가능한 부품 제작용 금형(Mold for making parts with adjustable size)

### C39 로봇 작업 경로 · 26건

대표 제목에는 작업 수행 로봇의 작업 경로의 길이를 계산하는 방법 / 작업 수행 로봇의 작업 경로의 길이를 계산하는 방법 / 작업 수행 로봇의 작업 경로의 길이를 계산하는 방법가 나타난다. 주요 IPC B25J, G05B, G05D 및 주요 선정분야 인공지능, 로봇를 함께 확인했다. 중심 제목의 주제를 요약한 label이며 전체 제목의 균질성을 보장하지 않는다.

대표 제목: 작업 수행 로봇의 작업 경로의 길이를 계산하는 방법(METHOD FOR CALCULAING THE LENGTH OF WORK PATH OF A TASK-PERFORMING ROBOT) / 작업 수행 로봇의 작업 경로의 길이를 계산하는 방법(METHOD FOR CALCULAING THE LENGTH OF WORK PATH OF A TASK-PERFORMING ROBOT) / 작업 수행 로봇의 작업 경로의 길이를 계산하는 방법(METHOD FOR CALCULAING THE LENGTH OF WORK PATH OF A TASK-PERFORMING ROBOT)

경계 제목: 공사장 작업자 안전 관제 시스템(SYSTEM FOR MONITORING SAFETY OF WORKERS AT CONSTRUCTION SITE) / 복수개의 이동형 로봇을 실시간 제어하여 단일 임무를 협동 수행하게 하는 로봇 제어 장치 및 시스템, 그리고 로봇 제어 방법(ROBOT CONTROL DEVICE AND SYSTEM FOR REAL-TIME CONTROL OF MULTIPLE MOBILE ROBOTS TO COLLABOLATIVELY PERFORM A SINGLE TASK, AND METHOD FOR CONTROLLING ROBOT) / 스마트 크레인 시스템의 권상 및 권하 동작 방법(A METHOD FOR HOISTING OF SMART CRANE SYSTEM)

### 미배정 미배정 · 643건

대표 제목에는 SAR 영상 분석 장치 및 그 방법 / 이미지 생성 방법 및 시스템 / 위성 영상 처리 방법 및 시스템가 나타난다. 주요 IPC G06F, G06T, G06N 및 주요 선정분야 인공지능, 드론를 함께 확인했다. 중심과 경계 제목의 범위가 넓어 혼합으로 남겼다.

대표 제목: SAR 영상 분석 장치 및 그 방법(APPARATUS FOR ANALYZING SAR IMAGE AND METHOD THEREOF) / 이미지 생성 방법 및 시스템(METHOD AND SYSTEM FOR GENERATING IMAGES) / 위성 영상 처리 방법 및 시스템(METHOD AND SYSTEM FOR SATELLITE IMAGE PROCESSING)

경계 제목: 외주면이 이종 강재로 된 구상화 흑연 주철 및 주철 크랭크사프트(The speroidization graphitization cast iron, in which the outer circumference is to the different kind steel material the cast iron crank axle) / 고 전자 이동도 트랜지스터(High Electron Mobility Transistor) / 인렛 파이프(Inlet Pipe)가 구비된 붕소 농도 측정기(BORON METER WITH INLET PIPE)



## 재현

1. requirements.txt 패키지 설치. embed_all.py 실행은 누락 배치만 실제 API 호출하며 비용 발생. 완성 체크포인트가 있으면 재호출하지 않음.

2. analyze_titles.py 실행(저장된 embeddings.npy와 patent_embedding_records.json 사용).

3. cluster_labels_reviewed.json / reviewed_findings.json은 실제 결과 검토 기록. label_and_report.py는 저장된 분석값으로 PNG·보고서 재생성.

4. submission/tools/build_semantic_section.py를 pre-semantic HTML에 실행하여 정적 웹 결과 생성.

벡터는 embeddings.npy의 행 순서와 patent_embedding_records.json의 행 순서가 일치한다. application_number로 원자료 연결 가능.



## 한계

제목만의 언어적 근접성. 전문·초록·청구항을 분석하지 않았다. 의미 군집은 방산 여부, 기업전략, 상용화, 인과적 정책효과의 증거가 아니다. UMAP은 거리·밀도를 왜곡하고 분리를 만들 수 있어 지도상 간격을 기술 거리로 정량 해석하지 않는다. 정규화·차원축소·HDBSCAN parameter에 의존하며 미배정은 무의미한 특허를 뜻하지 않는다. 선정분야 행은 고유 출원당 소속 기록에 1/m, IPC 행은 고유 출원당 고유 서브클래스에 1/k 배분; 기존 EDA의 기업-출원 연결 집계와 분모가 다르다.



## 공식 방법자료

[UMAP](https://umap-learn.readthedocs.io/en/latest/clustering.html) · [HDBSCAN](https://hdbscan.readthedocs.io/en/latest/parameter_selection.html) · [OpenRouter](https://openrouter.ai/qwen/qwen3-embedding-8b)