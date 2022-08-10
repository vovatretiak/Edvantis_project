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
