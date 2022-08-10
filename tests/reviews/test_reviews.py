import pytest
from fastapi.testclient import TestClient

from main import app
from project.reviews.schemas import ReviewRating
from project.utils import create_access_token
from tests.books.test_books import create_dummy_books

client = TestClient(app)


@pytest.mark.usefixtures("create_dummy_books")
class TestReview:
    """tests book methods"""

    def test_get_reviews(self):
        "test get method to show all reviews"
        response = client.get("/reviews/")
        assert response.status_code == 200
        reviews = response.json()
        assert len(reviews) == 8
        assert reviews[0]["user_id"] == 1
        assert reviews[0]["rating"] == 4
        assert reviews[-1]["user_id"] == 2
        assert reviews[-1]["rating"] == 5
        # with params
        response = client.get("/reviews/", params={"offset": 4, "limit": 3})
        assert response.status_code == 200
        reviews = response.json()
        assert len(reviews) == 3
        assert reviews[0]["user_id"] == 1
        assert reviews[0]["rating"] == 2
        assert reviews[0]["text"] == "not good"
        assert reviews[2]["id"] == 7

    def test_create_review(self):
        """tests post method to create new review"""
        user_access_token = create_access_token("john123")
        payload = {"text": "new review", "rating": ReviewRating.FIVE, "book_id": 5}
        response = client.post(
            "/reviews/",
            headers={"Authorization": f"Bearer {user_access_token}"},
            json=payload,
        )
        assert response.status_code == 201
        review = response.json()
        assert "created_at" in review
        assert review["user_id"] == 1
        assert review["text"] == payload["text"]
        assert review["book_id"] == payload["book_id"]

        response = client.get("/reviews/")
        assert response.status_code == 200
        reviews = response.json()
        assert len(reviews) == 9
        # bad token
        user_access_token = create_access_token("john1234")
        response = client.post(
            "/reviews/",
            headers={"Authorization": f"Bearer {user_access_token}"},
            json=payload,
        )
        assert response.status_code == 401

    def test_review_get_by_id(self):
        """tests get method to show review by its id"""
        user_access_token = create_access_token("john123")
        review_id = 9
        response = client.get(
            f"/reviews/{review_id}",
            headers={"Authorization": f"Bearer {user_access_token}"},
        )
        assert response.status_code == 200
        review = response.json()
        assert review["text"] == "new review"
        assert review["rating"] == 5
        # id not exits
        review_id = 100
        response = client.get(
            f"/reviews/{review_id}",
            headers={"Authorization": f"Bearer {user_access_token}"},
        )
        assert response.status_code == 404
