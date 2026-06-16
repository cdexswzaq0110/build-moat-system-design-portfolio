from fastapi.testclient import TestClient

from app.main import app


def test_index_documents_and_chat_flow() -> None:
    client = TestClient(app)

    index_response = client.post("/index")
    assert index_response.status_code == 200
    assert index_response.json()["count"] > 0

    documents_response = client.get("/documents")
    assert documents_response.status_code == 200
    assert documents_response.json()["sections_indexed"] > 0

    chat_response = client.post("/chat", json={"question": "Does this require paid APIs?"})
    assert chat_response.status_code == 200
    data = chat_response.json()
    assert data["answer"]
    assert "learning_focus" in data
    assert data["sources"]
    assert "content" in data["sources"][0]
