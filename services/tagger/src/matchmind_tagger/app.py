"""Run: uv run --package matchmind-tagger uvicorn matchmind_tagger.app:app --reload --port 8001"""
from fastapi import FastAPI

app = FastAPI(title="MatchMind tagger")


@app.get("/health")
def health() -> dict:
    return {"ok": True}
