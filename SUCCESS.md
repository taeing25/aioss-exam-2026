# AI OSS 실습기반 시험 성공 기준

시험 문항별 성공 기준을 체크박스 형태로 정리한 문서입니다.

## 문항 1. 협업 워크플로우 구성
- [x] PR 링크 1개를 제출했다.
  - https://github.com/taeing25/aioss-exam-2026/pull/1
- [x] 브랜치 전략 설명을 5문장 이내로 정리했다.
  - GitHub Flow 기반 전략 적용. main 브랜치는 항상 배포 가능한 상태를 유지한다. 모든 기능은 feature 브랜치(`feature/add-health-endpoint`)에서 개발한다. 작업 완료 후 PR을 생성하고 CI 통과를 확인한 뒤 merge한다. merge 후 feature 브랜치는 삭제하거나 다음 작업에 재활용한다.
- [x] 리뷰 코멘트 1개 이상을 남겼다.

## 문항 2. CI 파이프라인 구축 및 최적화
- [x] 워크플로우 실행 링크 2개 이상을 남겼다.
  - [개발 중 실패] https://github.com/taeing25/aioss-exam-2026/actions/runs/26268879624
  - [개발 중 성공] https://github.com/taeing25/aioss-exam-2026/actions/runs/26269144766
  - [제출 저장소 실패] https://github.com/taeing25/aioss-exam-2026_2343921/actions/runs/26270455814
  - [제출 저장소 성공] https://github.com/taeing25/aioss-exam-2026_2343921/actions/runs/26270508899
- [x] 실패 후 수정 성공 이력 1세트를 증빙했다.
  - 실패 원인: `ModuleNotFoundError: No module named 'app'` (pytest가 python-exam-minimal/을 sys.path에 추가 안 함)
  - 수정: `pytest.ini`에 `pythonpath = .` 추가 → 재실행 성공
- [x] 최적화 전/후 실행 시간 비교표를 작성했다.

| 항목 | 최적화 전 | 최적화 후 |
|---|---|---|
| pip install 시간 | ~30초 (매번 전체 설치) | ~5초 (캐시 히트 시) |
| 적용 방법 | 없음 | `actions/setup-python cache: 'pip'` |
| 효과 | 의존성 재다운로드 | requirements.txt 해시 기반 캐시 재사용 |

## 문항 3. Shift-left 테스트 실습
- [x] 테스트 실행 로그를 남겼다.
  - CI 성공 run: https://github.com/taeing25/aioss-exam-2026/actions/runs/26269144766
  - 로컬: 18 passed in 0.48s
- [x] 실패 → 수정 → 성공 흐름이 보이는 커밋 2개 이상을 남겼다.
  - 실패: `55180a7` (pytest ModuleNotFoundError)
  - 수정: `262343e` (pytest.ini 추가)
  - 성공: CI run #3 통과
- [x] 테스트 전략 설명을 5문장 이내로 정리했다.
  - 테스트 피라미드 기준으로 단위 테스트 13개, 통합 테스트 5개를 작성했다. 단위 테스트는 old_recommender, next_recommender, feature_flags의 각 함수를 독립적으로 검증한다. 통합 테스트는 FastAPI TestClient로 /health와 /recommendation 엔드포인트의 실제 HTTP 응답을 검증한다. Feature Flag OFF/ON 시나리오를 통합 테스트에서 모두 커버하여 플래그 분기 로직을 end-to-end로 확인한다. 실패 테스트를 먼저 실행(CI run #1)하고 코드를 수정하여 통과시키는 Shift-left 흐름을 적용했다.

## 문항 4. Feature Flag + TBD 적용
- [x] OFF 상태 캡처 1개와 ON 상태 캡처 1개를 남겼다.
  - OFF: `FEATURE_NEXT_RECOMMENDER` 미설정 → `FLAG OFF: False` → baseline-v1 반환
  - ON: `FEATURE_NEXT_RECOMMENDER=true`, `ROLLOUT=100` → `FLAG ON: True` → next-v2 반환
- [x] 롤백 절차 3단계를 정리했다.
  1. `FEATURE_NEXT_RECOMMENDER` 환경변수를 `false`로 즉시 변경 → 신규 추천기 비활성화
  2. 서버 재시작 없이 환경변수 변경만으로 rollback 완료 (코드 변경 불필요)
  3. 문제 원인 분석 후 `ROLLOUT` 값을 0 → 단계적으로 증가시켜 재배포
- [x] 사용한 플래그 유형 1개와 선택 이유를 설명했다.
  - **롤아웃 비율 기반 플래그** (0~100% 점진 배포) 선택. 이유: 전체 사용자에게 한 번에 노출하지 않고 해시 버킷(0~99)으로 사용자를 분산하여 신규 추천기의 품질을 안전하게 검증할 수 있기 때문이다. 장애 발생 시 ROLLOUT=0 설정만으로 즉시 차단 가능하다.

## 문항 5. 배포 및 운영 메트릭 연결
- [x] 배포 결과 링크 또는 배포 성공 로그를 남겼다.
  - `python-exam-minimal/artifacts/deployment_result.json` 생성 완료
  - status: "success", environment: "production"
- [x] 지표 수집 방식 요약표를 작성했다.

| DORA 지표 | 측정값 | 측정 방법 |
|---|---|---|
| Lead Time for Changes | 0.5시간 | feature 브랜치 생성 ~ main merge 시간 |
| Deployment Frequency | 3회/주 | CI Actions run 횟수 기준 |
| Change Failure Rate | 33.3% | 실패 배포(1회) / 전체 배포(3회) |
| MTTR | 15분 | CI 실패 감지 ~ pytest.ini 수정 후 재배포 성공까지 |

## 최종 제출 체크
- [x] 최종 저장소 링크(Private)에 chunsejin을 협력자로 추가했다.
- [x] 문항 1~5 관련 요구사항 답변을 포함했다.
- [x] Actions 실행 링크 2개 이상을 포함했다.
- [x] 배포 결과를 포함했다.
- [x] 최종 요약 보고서를 포함했다.
