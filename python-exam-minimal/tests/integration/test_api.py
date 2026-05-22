"""통합(API) 테스트: FastAPI TestClient 기반"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# ── /health ──────────────────────────────────────────────────────
def test_health_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ── /recommendation ──────────────────────────────────────────────
def test_recommendation_flag_off(monkeypatch: pytest.MonkeyPatch) -> None:
    """Feature Flag OFF -> baseline-v1 모델 반환"""
    monkeypatch.delenv("FEATURE_NEXT_RECOMMENDER", raising=False)
    response = client.get("/recommendation", params={"user_id": "alice"})
    assert response.status_code == 200
    data = response.json()
    assert data["model"] == "baseline-v1"
    assert "score" in data


def test_recommendation_flag_on(monkeypatch: pytest.MonkeyPatch) -> None:
    """Feature Flag ON (100% rollout) -> next-v2 모델 반환"""
    monkeypatch.setenv("FEATURE_NEXT_RECOMMENDER", "true")
    monkeypatch.setenv("FEATURE_NEXT_RECOMMENDER_ROLLOUT", "100")
    response = client.get("/recommendation", params={"user_id": "alice"})
    assert response.status_code == 200
    data = response.json()
    assert data["model"] == "next-v2"
    assert 0.0 <= data["score"] <= 1.0


def test_recommendation_user_id_too_short() -> None:
    """user_id가 3자 미만이면 422 반환"""
    response = client.get("/recommendation", params={"user_id": "ab"})
    assert response.status_code == 422


def test_recommendation_response_shape(monkeypatch: pytest.MonkeyPatch) -> None:
    """응답 JSON에 user_id, model, score 필드가 있어야 한다."""
    monkeypatch.delenv("FEATURE_NEXT_RECOMMENDER", raising=False)
    response = client.get("/recommendation", params={"user_id": "testuser"})
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == {"user_id", "model", "score"}
    assert data["user_id"] == "testuser"
