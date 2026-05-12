from dataclasses import dataclass


@dataclass
class RecommendationResult:
    user_id: str
    model: str
    score: float


def old_recommender(user_id: str) -> RecommendationResult:
    # TODO: baseline 추천 로직을 구현하세요.
    # 조건:
    # - model 필드는 "baseline-v1"
    # - score는 0.0~1.0 범위 float
    raise NotImplementedError("TODO: old_recommender")


def next_recommender(user_id: str) -> RecommendationResult:
    # TODO: 신규 추천 로직을 구현하세요.
    # 조건:
    # - model 필드는 "next-v2"
    # - old_recommender 대비 개선된 score 전략을 정의
    raise NotImplementedError("TODO: next_recommender")
