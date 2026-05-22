import hashlib
import os


def _to_bool(value: str | None, default: bool = False) -> bool:
    """환경변수 문자열을 bool로 변환. '1','true','yes','on' -> True."""
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _rollout_bucket(user_id: str) -> int:
    """user_id를 0~99 버킷으로 매핑 (SHA-256 해시 기반)."""
    digest = int(hashlib.sha256(user_id.encode()).hexdigest(), 16)
    return digest % 100


def is_next_recommender_enabled(user_id: str) -> bool:
    """FEATURE_NEXT_RECOMMENDER 환경변수 + rollout 비율로 활성화 여부 반환.
    기본값 OFF.
    """
    enabled = _to_bool(os.environ.get("FEATURE_NEXT_RECOMMENDER"), default=False)
    if not enabled:
        return False

    rollout_str = os.environ.get("FEATURE_NEXT_RECOMMENDER_ROLLOUT", "100")
    try:
        rollout = max(0, min(100, int(rollout_str)))
    except ValueError:
        rollout = 0

    return _rollout_bucket(user_id) < rollout
