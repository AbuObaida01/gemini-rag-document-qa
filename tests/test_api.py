from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_empty_query():
    response = client.post(
        "/api/query",
        json={
            "question": ""
        },
    )

    assert response.status_code == 422


def test_whitespace_query():
    response = client.post(
        "/api/query",
        json={
            "question": "   "
        },
    )

    assert response.status_code in (400, 422)


def test_list_documents():
    response = client.get(
        "/api/documents"
    )

    assert response.status_code == 200

    data = response.json()

    assert "documents" in data
    assert isinstance(
        data["documents"],
        list,
    )