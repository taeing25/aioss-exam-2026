from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    """DORA 지표 4개를 artifacts/dora_metrics.json 으로 저장."""
    metrics = {
        "collected_at_utc": datetime.now(timezone.utc).isoformat(),
        "lead_time_for_changes_hours": 0.5,
        # 측정 방법: PR 생성 시각 ~ merge/배포 시각 차이
        # 이번 시험: feature 브랜치 생성 후 당일 merge

        "deployment_frequency_per_week": 3,
        # 측정 방법: 지난 7일간 main 브랜치 배포 횟수
        # 이번 시험: CI 통과 후 push = 배포로 간주, 3회 실행

        "change_failure_rate_percent": 33.3,
        # 측정 방법: 전체 배포 중 실패한 배포 비율
        # 이번 시험: 3회 중 1회 실패(CI run #1) → 33.3%

        "mttr_minutes": 15,
        # 측정 방법: 장애 감지 시각 ~ 복구 완료 시각 차이
        # 이번 시험: CI 실패 → pytest.ini 추가 → 재배포 성공까지 약 15분

        "notes": {
            "lead_time": "feature/add-health-endpoint 브랜치 생성 ~ main merge 기준",
            "deployment_frequency": "CI Actions run 횟수 기준 (push당 1회 배포)",
            "cfr": "run #1 실패(ModuleNotFoundError) / 총 3회 = 33.3%",
            "mttr": "CI 실패 알림 확인 후 pytest.ini 수정 및 재배포까지 소요 시간",
        },
    }

    output_path = Path("artifacts/dora_metrics.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"DORA metrics saved to {output_path}")
    for key, value in metrics.items():
        if key not in ("collected_at_utc", "notes"):
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
