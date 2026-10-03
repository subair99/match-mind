"""Run: uv run --package matchmind-companion uvicorn matchmind_companion.app:app --reload --port 8002"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="MatchMind companion")
INDEX = Path(__file__).parent / "static" / "index.html"


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return INDEX.read_text()
