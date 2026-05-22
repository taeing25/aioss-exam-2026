from dataclasses import dataclass


@dataclass
class RecommendationResult:
    user_id: str
    model: str
    score: float


def old_recommender(user_id: str) -> RecommendationResult:
    """baseline-v1: user_id 길이 기반 단순 score."""
    score = round((len(user_id) % 10) / 10.0, 2)
    return RecommendationResult(user_id=user_id, model="baseline-v1", score=score)


def next_recommender(user_id: str) -> RecommendationResult:
    """next-v2: 해시 기반 score — baseline 대비 분포가 고름."""
    import hashlib
    digest = int(hashlib.sha256(user_id.encode()).hexdigest(), 16)
    score = round((digest % 1000) / 1000.0, 3)
    return RecommendationResult(user_id=user_id, model="next-v2", score=score)
