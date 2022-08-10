import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
from ..db_for_tests import override_get_db
from project.models import Author


@pytest.fixture(autouse=True, scope="class")
def create_dummy_authors():
    """fixture to execute asserts before and after a test is run"""

    db = next(override_get_db())
    author = Author(
        first_name="Averell",
        last_name="Povah",
        middle_name="Astrid",
        image_file="http://dummyimage.com/129x100.png/ff4444/ffffff",
    )
    author2 = Author(
        first_name="Skipp",
        last_name="Bennoe",
        image_file="http://dummyimage.com/118x100.png/cc0000/ffffff",
    )
    author3 = Author(last_name="Dancer", middle_name="Shanda")
    db.add(author)
    db.add(author2)
    db.add(author3)
    db.commit()
    yield

    # teardown
    db.query(Author).filter(Author.id == 1).delete()
    db.query(Author).filter(Author.id == 2).delete()
    db.query(Author).filter(Author.id == 3).delete()
    db.commit()


@pytest.mark.usefixtures("create_dummy_authors")
class TestAuthor:
    """tests author methods"""

    def test_create_author(self):
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
        # assert author in response_data

    def test_get_all_authors(self):
        """tests get method to show all authors"""
        response = client.get("/authors/")
        assert response.status_code == 200
        authors = response.json()
        assert len(authors) == 4
        assert authors[0]["first_name"] == "Averell"
        assert "id" in authors[0]
        assert "image_file" in authors[0]
        assert authors[1]["middle_name"] is None
        assert authors[1]["id"] == 2
        assert authors[2]["id"] == 3
        assert authors[2]["first_name"] is None
        author = authors[0]
        # with params
        response_with_params = client.get("/authors/", params={"offset": 1, "limit": 2})
        assert response_with_params.status_code == 200
        authors = response_with_params.json()
        assert author not in authors
        assert authors[0]["id"] == 2
        assert len(authors) == 2

    def test_get_author_by_id(self):
        """tests get method to show author by its id"""
        author_id = 1
        response = client.get(f"/authors/{author_id}")
        assert response.status_code == 200
        author = response.json()
        assert author["id"] == 1
        assert author["first_name"] == "Averell"
        # author_id is not exist
        author_id = 10
        response = client.get(f"/authors/{author_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == f"Author with id {author_id} is not found"

    def test_update_author(self):
        """tests put method to show author by its id"""
        author_id = 1
        payload = {"first_name": "John", "last_name": "Doe"}
        response = client.put(f"/authors/{author_id}", json=payload)
        assert response.status_code == 202
        updated_author = response.json()
        assert updated_author["id"] == 1
        assert updated_author["first_name"] == "John"
        assert updated_author["last_name"] == "Doe"
        assert updated_author["middle_name"] == "Astrid"
        # author_id is not exist
        author_id = 10
        response = client.put(f"/authors/{author_id}", json=payload)
        assert response.status_code == 404
        assert response.json()["detail"] == f"Author with id {author_id} is not found"

    def test_delete_author(self):
        """tests delete method to delete author by its id"""
        author_id = 1
        response = client.delete(f"/authors/{author_id}")
        assert response.status_code == 204
        # author_id is not exist
        author_id = 10
        response = client.delete(f"/authors/{author_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == f"Author with id {author_id} is not found"
