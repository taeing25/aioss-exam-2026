# 최종 요약 보고서

## 기본 정보
- 이름: 윤태이
- 제출 저장소: https://github.com/taeing25/aioss-exam-2026_2343921
- 제출 일시: 2026-05-22

---

## 문항 1. 협업 워크플로우 구성 (20점)

### 브랜치 전략 (5문장 이내)
GitHub Flow 기반 전략을 적용했다. main 브랜치는 항상 배포 가능한 상태를 유지한다. 모든 기능은 feature 브랜치(`feature/add-health-endpoint`, `feature/exam-workflow`)에서 개발한다. 작업 완료 후 PR을 생성하고 CI 통과를 확인한 뒤 merge한다. merge 후 feature 브랜치는 삭제하거나 다음 작업에 재활용한다.

### PR 링크
- [개발 저장소 PR #1] https://github.com/taeing25/aioss-exam-2026/pull/1
- [제출 저장소 feature/exam-workflow → main] https://github.com/taeing25/aioss-exam-2026_2343921/pulls

### 리뷰 코멘트
PR #1에 리뷰 코멘트 작성 완료.

---

## 문항 2. CI 파이프라인 구축 및 최적화 (30점)

### 워크플로우 구성 요약
- 트리거: `push`, `pull_request` (main, feature/**)
- Matrix: os(ubuntu-latest, windows-latest) × python-version(3.10, 3.11) → 4가지 조합
- 품질 게이트 3개: ruff lint, pytest, build import check
- 최적화: `actions/setup-python cache: 'pip'` → pip install 시간 ~30초 → ~5초로 단축

### CI 실행 링크
| 구분 | 저장소 | 링크 |
|------|--------|------|
| 실패 run (개발 중) | public fork | https://github.com/taeing25/aioss-exam-2026/actions/runs/26268879624 |
| 성공 run (개발 중) | public fork | https://github.com/taeing25/aioss-exam-2026/actions/runs/26269144766 |
| 실패 run (제출 저장소) | private | https://github.com/taeing25/aioss-exam-2026_2343921/actions/runs/26270455814 |
| 성공 run (제출 저장소) | private | https://github.com/taeing25/aioss-exam-2026_2343921/actions/runs/26270508899 |

### 실패 원인 및 수정 내용
- **실패 원인**: `ModuleNotFoundError: No module named 'app'` — pytest 8.x가 working directory를 자동으로 sys.path에 추가하지 않음
- **수정**: `python-exam-minimal/pytest.ini`에 `pythonpath = .` 추가
- **결과**: 4개 matrix 조합 모두 통과

### 최적화 전/후 비교
| 항목 | 최적화 전 | 최적화 후 |
|------|----------|----------|
| pip install 시간 | ~30초 (매번 전체 설치) | ~5초 (캐시 히트 시) |
| 적용 방법 | 없음 | `actions/setup-python cache: 'pip'` |
| 효과 | 의존성 재다운로드 | requirements.txt 해시 기반 캐시 재사용 |

---

## 문항 3. Shift-left 테스트 실습 (20점)

### 테스트 전략 (5문장 이내)
테스트 피라미드 기준으로 단위 테스트 13개, 통합 테스트 5개를 작성했다. 단위 테스트는 `old_recommender`, `next_recommender`, `feature_flags`의 각 함수를 독립적으로 검증한다. 통합 테스트는 FastAPI TestClient로 `/health`와 `/recommendation` 엔드포인트의 실제 HTTP 응답을 검증한다. Feature Flag OFF/ON 시나리오를 통합 테스트에서 모두 커버하여 플래그 분기 로직을 end-to-end로 확인한다. 실패 테스트를 먼저 실행(CI run 실패)하고 코드를 수정하여 통과시키는 Shift-left 흐름을 적용했다.

### 테스트 실행 로그
- 로컬: `18 passed in 0.48s`
- CI 성공 run: https://github.com/taeing25/aioss-exam-2026_2343921/actions/runs/26270508899

### 실패→수정→성공 커밋 흐름
| 단계 | 커밋/run |
|------|---------|
| 실패 | CI run #1 — ModuleNotFoundError |
| 수정 | `pytest.ini` 추가 커밋 |
| 성공 | CI run #3 — 18 passed |

---

## 문항 4. Feature Flag + TBD 적용 (20점)

### 구현 방식
- `app/feature_flags.py`에 환경변수 기반 Feature Flag 구현
- `FEATURE_NEXT_RECOMMENDER`: 플래그 ON/OFF
- `FEATURE_NEXT_RECOMMENDER_ROLLOUT`: 0~100% 점진 배포 비율

### OFF/ON 상태 확인
- **OFF** (기본): `FEATURE_NEXT_RECOMMENDER` 미설정 → `is_next_recommender_enabled() = False` → `baseline-v1` 반환
- **ON** (100% rollout): `FEATURE_NEXT_RECOMMENDER=true`, `ROLLOUT=100` → `is_next_recommender_enabled() = True` → `next-v2` 반환

### 롤백 절차 3단계
1. `FEATURE_NEXT_RECOMMENDER` 환경변수를 `false`로 즉시 변경 → 신규 추천기 비활성화
2. 서버 재시작 없이 환경변수 변경만으로 rollback 완료 (코드 변경 불필요)
3. 문제 원인 분석 후 `ROLLOUT` 값을 0 → 단계적으로 증가시켜 재배포

### 사용한 플래그 유형
**롤아웃 비율 기반 플래그** (0~100% 점진 배포)  
선택 이유: 전체 사용자에게 한 번에 노출하지 않고 SHA-256 해시 버킷(0~99)으로 사용자를 분산하여 신규 추천기의 품질을 안전하게 검증할 수 있기 때문이다. 장애 발생 시 ROLLOUT=0 설정만으로 즉시 차단 가능하다.

---

## 문항 5. 배포 및 운영 메트릭 연결 (10점)

### 배포 결과
- `scripts/deploy_simulation.py` 실행 → `artifacts/deployment_result.json` 생성
- status: "success", environment: "production"

### DORA 지표 수집 방식

| DORA 지표 | 측정값 | 측정 방법 |
|----------|--------|---------|
| Lead Time for Changes | 0.5시간 | feature 브랜치 생성 ~ main merge 시간 |
| Deployment Frequency | 3회/주 | CI Actions run 횟수 기준 |
| Change Failure Rate | 33.3% | 실패 배포(1회) / 전체 배포(3회) |
| MTTR | 15분 | CI 실패 감지 ~ pytest.ini 수정 후 재배포 성공까지 |

### MTTR 단축 액션
CI 실패 시 junit-xml artifact를 자동 업로드하여 실패 테스트 케이스를 즉시 확인 가능하게 구성했다. 이를 통해 원인 분석 → 수정 → 재배포 사이클을 단축한다.

---

## 커밋 이력 요약 (최소 5개)

| 커밋 | 내용 |
|------|------|
| 초기 구현 | app/service.py, feature_flags.py, main.py 구현 |
| CI 구성 | .github/workflows/ci.yml 추가 (matrix 2축, 품질 게이트 3개) |
| 테스트 작성 | unit/test_service.py (13개), integration/test_api.py (5개) |
| CI 수정 | pytest.ini 추가 (pythonpath 설정) |
| 배포/메트릭 | deploy_simulation.py, collect_dora_metrics.py 실행 결과 추가 |
| 문서화 | SUCCESS.md, REPORT.md 작성 |

---

## Actions 실행 링크

| 구분 | URL |
|------|-----|
| 실패 (개발 중 — public fork) | https://github.com/taeing25/aioss-exam-2026/actions/runs/26268879624 |
| 성공 (개발 중 — public fork) | https://github.com/taeing25/aioss-exam-2026/actions/runs/26269144766 |
| 실패 (제출 저장소 — private) | https://github.com/taeing25/aioss-exam-2026_2343921/actions/runs/26270455814 |
| 성공 (제출 저장소 — private) | https://github.com/taeing25/aioss-exam-2026_2343921/actions/runs/26270508899 |
