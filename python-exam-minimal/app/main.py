from fastapi import FastAPI, Query

from app.feature_flags import is_next_recommender_enabled
from app.service import next_recommender, old_recommender

app = FastAPI(title="AI OSS Exam API (Minimal)", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/recommendation")
def recommendation(user_id: str = Query(..., min_length=3)) -> dict[str, str | float]:
    # TODO: Feature Flag에 따라 old/new recommender를 선택하고
    #       표준 응답(JSON)을 반환하세요.
    raise NotImplementedError("TODO: /recommendation")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
