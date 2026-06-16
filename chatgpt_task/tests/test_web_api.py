from fastapi.testclient import TestClient

from app.main import app


def test_homepage_loads() -> None:
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert "Task Scheduler" in response.text
    assert "Focus on what needs your attention now." in response.text


def test_summary_endpoint_shape() -> None:
    client = TestClient(app)

    response = client.get("/api/summary")

    assert response.status_code == 200
    data = response.json()
    assert {"total", "pending", "completed", "due", "upcoming"}.issubset(data)


def test_update_and_delete_task() -> None:
    client = TestClient(app)
    create_response = client.post(
        "/api/tasks",
        json={
            "content": "draft launch plan",
            "due_at": "2026-05-31T09:00:00Z",
            "priority": "high",
            "note": "portfolio demo",
        },
    )
    job_id = create_response.json()["job"]["id"]
    assert create_response.json()["job"]["priority"] == "high"
    assert create_response.json()["job"]["note"] == "portfolio demo"

    update_response = client.patch(
        f"/api/tasks/{job_id}",
        json={
            "content": "revise launch plan",
            "due_at": "2026-06-01T10:00:00Z",
            "priority": "low",
            "note": "updated context",
        },
    )

    assert update_response.status_code == 200
    assert update_response.json()["job"]["content"] == "revise launch plan"
    assert update_response.json()["job"]["priority"] == "low"
    assert update_response.json()["job"]["note"] == "updated context"

    delete_response = client.delete(f"/api/tasks/{job_id}")

    assert delete_response.status_code == 200
    assert delete_response.json() == {"status": "deleted", "id": job_id}


def test_cancel_task_endpoint() -> None:
    client = TestClient(app)
    create_response = client.post(
        "/api/tasks",
        json={
            "content": "cancel this task",
            "due_at": "2026-05-31T09:00:00Z",
            "priority": "medium",
            "note": "",
        },
    )
    job_id = create_response.json()["job"]["id"]

    cancel_response = client.post(f"/api/tasks/{job_id}/cancel")

    assert cancel_response.status_code == 200
    assert cancel_response.json()["job"]["status"] == "cancelled"


def test_process_due_endpoint_executes_due_task() -> None:
    client = TestClient(app)
    create_response = client.post(
        "/api/tasks",
        json={
            "content": "process this due task",
            "due_at": "2026-05-31T09:00:00Z",
            "priority": "high",
            "note": "",
        },
    )
    job_id = create_response.json()["job"]["id"]

    process_response = client.post("/api/tasks/process-due")

    assert process_response.status_code == 200
    executed_ids = {job["id"] for job in process_response.json()["executed"]}
    assert job_id in executed_ids
