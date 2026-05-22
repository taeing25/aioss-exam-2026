"""단위 테스트: service.py / feature_flags.py"""
import pytest

from app.feature_flags import _rollout_bucket, _to_bool, is_next_recommender_enabled
from app.service import RecommendationResult, next_recommender, old_recommender


# ── old_recommender ───────────────────────────────────────────────
def test_old_recommender_model() -> None:
    result = old_recommender("alice")
    assert result.model == "baseline-v1"


def test_old_recommender_returns_dataclass() -> None:
    result = old_recommender("bob123")
    assert isinstance(result, RecommendationResult)
    assert result.user_id == "bob123"


def test_old_recommender_score_in_range() -> None:
    result = old_recommender("testuser")
    assert 0.0 <= result.score <= 1.0


# ── next_recommender ─────────────────────────────────────────────
def test_next_recommender_model() -> None:
    result = next_recommender("charlie")
    assert result.model == "next-v2"


def test_next_recommender_score_in_range() -> None:
    result = next_recommender("dave99")
    assert 0.0 <= result.score <= 1.0


def test_next_recommender_deterministic() -> None:
    """같은 user_id는 항상 같은 score를 반환해야 한다."""
    assert next_recommender("eve").score == next_recommender("eve").score


# ── feature_flags ────────────────────────────────────────────────
def test_to_bool_true_values() -> None:
    for v in ("1", "true", "True", "yes", "on"):
        assert _to_bool(v) is True


def test_to_bool_false_values() -> None:
    for v in ("0", "false", "no", "off", ""):
        assert _to_bool(v) is False


def test_to_bool_none_default() -> None:
    assert _to_bool(None, default=False) is False
    assert _to_bool(None, default=True) is True


def test_rollout_bucket_range() -> None:
    for uid in ("alpha", "beta", "gamma", "delta", "epsilon"):
        assert 0 <= _rollout_bucket(uid) <= 99


def test_feature_flag_off_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FEATURE_NEXT_RECOMMENDER", raising=False)
    assert is_next_recommender_enabled("anyuser") is False


def test_feature_flag_on_full_rollout(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FEATURE_NEXT_RECOMMENDER", "true")
    monkeypatch.setenv("FEATURE_NEXT_RECOMMENDER_ROLLOUT", "100")
    assert is_next_recommender_enabled("anyuser") is True


def test_feature_flag_zero_rollout(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FEATURE_NEXT_RECOMMENDER", "true")
    monkeypatch.setenv("FEATURE_NEXT_RECOMMENDER_ROLLOUT", "0")
    assert is_next_recommender_enabled("anyuser") is False
