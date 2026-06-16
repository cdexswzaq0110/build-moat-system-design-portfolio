from fastapi.testclient import TestClient

from app.main import app


def test_qr_lifecycle_update_analytics_and_delete() -> None:
    client = TestClient(app)

    create_response = client.post("/api/qr/create", json={"url": "https://example.com/start"})
    assert create_response.status_code == 200
    token = create_response.json()["token"]

    update_response = client.patch(
        f"/api/qr/{token}",
        json={"url": "https://example.com/updated"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["url"] == "https://example.com/updated"

    redirect_response = client.get(f"/r/{token}", follow_redirects=False)
    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"] == "https://example.com/updated"

    analytics_response = client.get(f"/api/qr/{token}/analytics")
    assert analytics_response.status_code == 200
    assert analytics_response.json()["total_scans"] == 1

    check_response = client.get(f"/api/qr/{token}/check")
    assert check_response.status_code == 200
    assert check_response.json()["status"] == "active"

    delete_response = client.delete(f"/api/qr/{token}")
    assert delete_response.status_code == 200

    deleted_redirect = client.get(f"/r/{token}", follow_redirects=False)
    assert deleted_redirect.status_code == 410
