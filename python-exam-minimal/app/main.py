from fastapi import FastAPI, Query

from app.feature_flags import is_next_recommender_enabled
from app.service import next_recommender, old_recommender

app = FastAPI(title="AI OSS Exam API (Minimal)", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/recommendation")
def recommendation(user_id: str = Query(..., min_length=3)) -> dict[str, str | float]:
    """Feature Flag에 따라 old/new recommender 선택 후 JSON 반환."""
    if is_next_recommender_enabled(user_id):
        result = next_recommender(user_id)
    else:
        result = old_recommender(user_id)
    return {"user_id": result.user_id, "model": result.model, "score": result.score}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
