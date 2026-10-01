# 국내 특허·실용신안 수집 및 품질 점검

검사시각: 2026-10-01T00:32:16.617053 (로컬 KST). 출원번호 단위의 목록 건수이며 등록특허만의 건수가 아니다.

## 수집 범위 및 방법

- applicant_identity_full.csv에서 collection_eligible가 Y인 82개 코드, 81개 선정기록만 사용. AP=[출원인코드] 검색, 국내 특허·실용신안 전체 권리구분 및 전체 행정상태. 최대 90개씩 페이지 수집. 사업자 동일성 미검증 코드는 추가하지 않았다.
- 공개된 KIPRIS 검색 목록의 서지정보를 수집했다. 미공개·비밀출원은 공개 검색으로 확인할 수 없으며, 코드에 연결되지 않은 과거 법인·승계사의 출원을 포함한다고 가정하지 않는다.
- 디브레인 SEL-033, 인텔릭스 SEL-057은 기존 조건부 식별로 미수집. 0건으로 처리하지 않았다. 기존 identity review queue의 검토 항목도 계속 유효하다.
- 공동출원인 이름·코드를 배열로 전부 보존. 출원인은 최초/현재 표시정보이며 최종권리자와 구분한다. 최종권리자 코드로 수집범위를 확장하지 않았다.

## 저장 구조

- 02_raw_data/kipris_patent_full: 코드별 manifest, 페이지 JSON, 원문 article HTML, 검색식, 페이지·수집시각·출처. incomplete_view_attempt에는 초기 축약 화면 수집 시도를 보존하며 최종 데이터 생성에는 사용하지 않는다.
- 02_raw_data/patent_list_full_raw.csv: 코드별 관측행 3,624행. source_record_id로 페이지 JSON까지 추적한다.
- 03_processed_data/patent_metadata_full.csv: 출원번호별 대표행 3,621행. 발견횟수·선정기록·코드·원자료 ID로 중복을 식별. 동일 서지값을 확인하고 최신 수집시각 행을 대표값으로 사용.
- patent_selection_links.csv: 관측별 기업/코드 연결 3,624행. patent_applicants_full.csv: 공동출원인을 포함한 출원인 이름·코드 관계. JSON 필드는 UTF-8 JSON 배열이고 번호는 문자열로 읽어야 한다.
- patent_collection_company_counts.csv: 전체 83개 선정기록별 건수 및 미수집 사유. patent_collection_code_counts.csv: 82개 코드별 기대/실제 건수. 기업별 건수는 기업 내부 출원번호 중복을 제거하고, 기업 간 공동출원은 각각 집계하므로 합계가 전체 고유출원 수와 다를 수 있다.
- patent_collection_review_queue.csv: 신규 동일명 미승인 코드, 대상 코드 누락, 서지 충돌 전용. 현재 헤더만 있으며 검토항목 0건. 일반 공동출원인 코드는 자동 수집 대상으로 추가하지 않았다.

## 품질 점검

- 특허 3,564건, 실용신안 57건, 총 3,621건. 출원일 1996-03-15 ~ 2026-09-10.
- 3개 출원은 서로 다른 선정기록에서 발견(추가 관측 3행). 공동출원 316건. 코드 내부 출원번호 중복 없음.
- 82개 코드의 화면 총건수 = 저장행수 = 코드 내부 고유 출원번호 수. 모든 CSV를 재독해 PK·FK·JSON 배열·출원인 코드 포함 여부 및 전체 83개 선정기록을 검사했다.
- 주요 결측: {"right_type":0,"title":0,"administrative_status":0,"application_date":0,"publication_number":1263,"publication_date":1263,"registration_number":930,"registration_date":930,"applicants_json":0,"inventors_json":0,"agents_json":20,"current_right_holders_json":930,"ipc_json":0,"cpc_json":0}. 결측은 화면의 빈값을 그대로 보존했다. 공개/등록번호의 부재 원인을 개별 사건 조회 없이 확정하지 않았다. 행정상태별 결측은 patent_collection_missing_by_status.csv 참고.
- 최종 실패 코드 0건, 대상 코드가 출원인 목록에 없는 건 0건, 신규 동일명 미승인 코드 0건, 서지 충돌 0건.

## 오류 및 복구

- 최초 페이지당 행 수 반영 지연, 일시적 버튼 클릭 오류, 서지 보기 갱신 지연 발생. 오류 기록은 collection_events.jsonl에 남겼으며 재시도로 복구했다.
- 실행 시간 초과로 연결이 재설정된 배치가 있었으나 완료 manifest를 재사용하고 미완료 코드만 이어서 처리했다.
- 재독 검사에서 30개 코드의 축약 화면 필드 누락을 발견했다. 초기 시도를 별도 보존한 후 전체 서지 필드가 나타날 때까지 확인·재클릭하도록 보완하고 30개 코드를 재수집했다. 재수집 전 임시 분석용 파일은 최종 데이터로 다시 생성했다.

## 입력 보존 및 제한

- 입력 SHA256: {"01_master/방산혁신기업100_master_company_v7.xlsx":"f8c4c2647093077fb002460711ebf8cabd9cf3b53f355e9cc1a983593ca6fcdc","03_processed_data/applicant_identity_pilot.csv":"06f9aeddf9d937173a0cf3f0ca2f3a3e7071fb025d37942b5010f90b89ef865c","03_processed_data/applicant_identity_full.csv":"27058ffa7b9995e7bc52299cc10858ce2083cf5569e7a73962a7905389a6b678"}
- 전체 특허목록 수집 및 품질 검사만 수행. 본격적인 EDA·시계열 추세·기술분야 분석은 수행하지 않았다.

## 기업별 건수

|선정기록|기업|고유 출원 수|처리|
|---|---|---:|---|
|SEL-001|ANH스트럭쳐|54|complete|
|SEL-002|단암시스템즈|46|complete|
|SEL-003|제노코|6|complete|
|SEL-004|솔빛시스템|22|complete|
|SEL-005|에스아이에이|68|complete|
|SEL-006|아이브스|28|complete|
|SEL-007|웨이비스|32|complete|
|SEL-008|RFHIC|57|complete|
|SEL-009|에스오에스랩|138|complete|
|SEL-010|코모텍|16|complete|
|SEL-011|대한광통신|65|complete|
|SEL-012|영풍전자|18|complete|
|SEL-013|빅텍|33|complete|
|SEL-014|네스앤텍|35|complete|
|SEL-015|아이블포토닉스|71|complete|
|SEL-016|스탠다드시험연구소|69|complete|
|SEL-017|우리별|15|complete|
|SEL-018|성신디펜스솔루션|11|complete|
|SEL-019|하나에이엠티|14|complete|
|SEL-020|루미르|11|complete|
|SEL-021|코난테크놀로지|92|complete|
|SEL-022|다비오|29|complete|
|SEL-023|인피닉|155|complete|
|SEL-024|웨이브피아|31|complete|
|SEL-025|쿠오핀|21|complete|
|SEL-026|마이크로인피니티|47|complete|
|SEL-027|컨트로맥스|17|complete|
|SEL-028|링크플로우|33|complete|
|SEL-029|두타기술|14|complete|
|SEL-030|니어스랩|65|complete|
|SEL-031|파블로항공|38|complete|
|SEL-032|센서피아|20|complete|
|SEL-033|디브레인||excluded_identity_conditional|
|SEL-034|아이디케이|25|complete|
|SEL-035|심네트|11|complete|
|SEL-036|솔탑|38|complete|
|SEL-037|두시텍|29|complete|
|SEL-038|아이스펙|8|complete|
|SEL-039|코모텍|15|complete|
|SEL-040|펀진|60|complete|
|SEL-041|젠젠에이아이|20|complete|
|SEL-042|모라이|53|complete|
|SEL-043|코클|13|complete|
|SEL-044|마키나락스|91|complete|
|SEL-045|퓨리오사에이아이|15|complete|
|SEL-046|옵토웰|63|complete|
|SEL-047|웨이브로드|182|complete|
|SEL-048|에이유|19|complete|
|SEL-049|포멀웍스|13|complete|
|SEL-050|유비파이|7|complete|
|SEL-051|소나테크|35|complete|
|SEL-052|유뱃|36|complete|
|SEL-053|아이티사이언스|10|complete|
|SEL-054|패리티|37|complete|
|SEL-055|위플로|27|complete|
|SEL-056|삼정오토메이션|9|complete|
|SEL-057|인텔릭스||excluded_identity_conditional|
|SEL-058|덕산넵코어스|38|complete|
|SEL-059|버넥트|83|complete|
|SEL-060|이오시스템|100|complete|
|SEL-061|휴라|13|complete|
|SEL-062|삼영기계|11|complete|
|SEL-063|스텝랩|13|complete|
|SEL-064|극동통신|35|complete|
|SEL-065|나라스페이스 테크놀로지|16|complete|
|SEL-066|스페이스맵|1|complete|
|SEL-067|텔레픽스|30|complete|
|SEL-068|인텔리빅스|67|complete|
|SEL-069|데이터메이커|21|complete|
|SEL-070|부전전자|233|complete|
|SEL-071|마크애니|256|complete|
|SEL-072|써로마인드|15|complete|
|SEL-073|아이쓰리시스템|34|complete|
|SEL-074|딥엑스|114|complete|
|SEL-075|라이온로보틱스|1|complete|
|SEL-076|삼현|65|complete|
|SEL-077|케이알엠|22|complete|
|SEL-078|센서뷰|110|complete|
|SEL-079|유큐브|9|complete|
|SEL-080|비이아이랩|28|complete|
|SEL-081|모아컴코리아|15|complete|
|SEL-082|이루온|92|complete|
|SEL-083|유저스|15|complete|
