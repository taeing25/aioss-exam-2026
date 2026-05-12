import hashlib
import os


def _to_bool(value: str | None, default: bool = False) -> bool:
    # TODO: 문자열 환경변수를 bool로 변환하세요.
    # 예: "1", "true", "yes", "on" -> True
    raise NotImplementedError("TODO: _to_bool")


def _rollout_bucket(user_id: str) -> int:
    # TODO: 사용자 ID를 0~99 버킷으로 매핑하세요.
    # 힌트 제거 버전: 해시 방식은 자유롭게 선택 가능
    raise NotImplementedError("TODO: _rollout_bucket")


def is_next_recommender_enabled(user_id: str) -> bool:
    # TODO: FEATURE_NEXT_RECOMMENDER, FEATURE_NEXT_RECOMMENDER_ROLLOUT 기반으로
    #       다음 추천기 활성화 여부를 반환하세요.
    # 요구사항:
    # - 기본값은 OFF
    # - rollout 값은 0~100으로 보정
    raise NotImplementedError("TODO: is_next_recommender_enabled")
