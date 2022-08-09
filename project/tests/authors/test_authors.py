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


def test_get_all_authors():
    """tests get method to show all authors"""
    response = client.get("/authors/")
    assert response.status_code == 200
    authors = response.json()
    assert len(authors) == 3
    assert authors[0]["first_name"] == "Averell"
    assert "id" in authors[0]
    assert "image_file" in authors[0]
    assert authors[1]["middle_name"] is None
    assert authors[1]["id"] == 2
    assert authors[2]["id"] == 3
    assert authors[2]["first_name"] is None
    author = authors[0]
    # with params
    response = client.get("/authors/", params={"offset": 1, "limit": 2})
    assert response.status_code == 200
    authors = response.json()
    assert author not in authors
    assert authors[0]["id"] == 2
    assert len(authors) == 2
