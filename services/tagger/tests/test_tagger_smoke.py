from fastapi.testclient import TestClient

from matchmind_tagger.app import app


def test_health():
    assert TestClient(app).get("/health").json() == {"ok": True}
