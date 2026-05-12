# Python Exam Minimal (Student Distribution)

이 폴더는 학생 배포용 최소 버전입니다.
정답 힌트가 제거되어 있으며, 모든 핵심 로직은 TODO로 남겨져 있습니다.

## 목표
- 실습기반 시험 문항(협업, CI, 테스트, Feature Flag, 배포/메트릭)을 직접 구현

## 빠른 시작
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
pytest -q
python -m app.main
```

## 구현해야 할 TODO
1. `app/service.py`
- 기존 추천기와 신규 추천기 로직 구현

2. `app/feature_flags.py`
- bool 파싱, 사용자 버킷 계산, 롤아웃 조건 구현

3. `app/main.py`
- `/health`, `/recommendation` 엔드포인트 완성

4. `tests/unit/test_service.py`
- 단위 테스트 최소 3개 작성

5. `tests/integration/test_api.py`
- 통합/API 테스트 최소 1개 이상 작성

6. `.github/workflows/ci.yml`
- push + pull_request 트리거 CI, 품질 게이트 3개 이상, matrix 2축 이상

7. `scripts/deploy_simulation.py`
- 배포 시뮬레이션 결과 JSON 생성

8. `scripts/collect_dora_metrics.py`
- DORA 지표 2개 이상 JSON 생성

## 제출 체크
- TODO가 모두 구현되었는지 확인
- 테스트 통과 로그 첨부
- CI 실행 링크 첨부
- 배포/메트릭 결과 파일 첨부
