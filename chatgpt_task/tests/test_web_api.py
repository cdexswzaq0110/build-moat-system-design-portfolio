from fastapi.testclient import TestClient

from app.main import app


def test_homepage_loads() -> None:
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert "Task Scheduler" in response.text
    assert "No Node Required" in response.text


def test_summary_endpoint_shape() -> None:
    client = TestClient(app)

    response = client.get("/api/summary")

    assert response.status_code == 200
    data = response.json()
    assert {"total", "pending", "completed", "due", "upcoming"}.issubset(data)
