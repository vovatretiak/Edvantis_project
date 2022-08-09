from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_author():
    """tests post method to create new author"""
    data = {"first_name": "New", "last_name": "Author"}
    response = client.post("/authors/", json=data)
    assert response.status_code == 201
    author = response.json()
    assert "id" in author
    assert author["first_name"] == data["first_name"]
    assert author["last_name"] == data["last_name"]

    response = client.get("/authors/")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 4
    assert author in response_data
