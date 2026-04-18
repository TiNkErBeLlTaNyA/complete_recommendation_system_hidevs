from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_recommend():
    response = client.get("/recommend/1")

    assert response.status_code == 200

    data = response.json()

    assert "user_id" in data
    assert "results" in data
    assert isinstance(data["results"], list)

    if len(data["results"]) > 0:
        item = data["results"][0]
        assert "item" in item
        assert "score" in item
        assert "reason" in item


def test_invalid_user():
    response = client.get("/recommend/9999")

    # your API allows cold-start users → returns 200
    assert response.status_code == 200

    data = response.json()
    assert "note" in data
    assert data["note"] == "cold start user"