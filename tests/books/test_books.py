import json

import pytest
from fastapi.testclient import TestClient

from ..db_for_tests import override_get_db
from main import app
from project.models import Author
from project.models import Book
from project.models import Review
from project.models import User
from project.utils import get_password_hash


client = TestClient(app)


@pytest.fixture(autouse=True, scope="class")
def create_dummy_books():
    """fixture to execute asserts before and after a test is run"""

    db = next(override_get_db())
    new_user = User(
        username="john123",
        email="john123@mail.com",
        password=get_password_hash("password"),
    )
    new_user2 = User(
        username="jane123",
        email="jane123@mail.com",
        password=get_password_hash("password2"),
    )
    db.add(new_user)
    db.add(new_user2)
    db.commit()

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
    db.add(author)
    db.add(author2)
    db.commit()

    with open("E:\\vscode\\edvantis_project\\books.json", encoding="utf8") as file:
        books = json.load(file)
    for book in books[:11]:
        new_book = Book(
            title=book["title"],
            description=book["description"],
            year=book["year"],
            image_file=book["img"],
            pages=book["pages"],
            genre=book["genre"],
            type=book["type"],
        )
        new_book.authors.append(author)
        if new_book.year < 2000:
            new_book.authors.append(author2)
        db.add(new_book)
        db.commit()

    reviews = [
        Review(user_id=1, text="wow", rating=5, book_id=1),
        Review(user_id=2, text="bad", rating=1, book_id=1),  # rating 3 for book 1
        Review(user_id=1, text="good", rating=3, book_id=2),
        Review(user_id=2, text="wow", rating=5, book_id=2),  # rating 4 for book 2
        Review(user_id=1, text="not good", rating=2, book_id=3),
        Review(user_id=2, text="not good", rating=2, book_id=3),  # rating 2 for book 3
        Review(user_id=1, text="wow", rating=5, book_id=4),
        Review(user_id=2, text="wow", rating=5, book_id=4),  # rating 5 for book 1
    ]
    for review in reviews:
        db.add(review)
        db.commit()
    yield

    # teardown
    db.query(Author).filter(Author.id == 1).delete()
    db.query(Author).filter(Author.id == 2).delete()
    db.query(User).filter(User.username == "john123").delete()
    db.query(User).filter(User.username == "jane123").delete()
    db.commit()


@pytest.mark.usefixtures("create_dummy_books")
class TestBook:
    """tests book methods"""

    def test_create_book(self):
        """tests post method to create new book"""
        response = client.get("/authors/2")
        author = response.json()
        assert author["first_name"] == "Skipp"

        payload = {
            "title": "new book",
            "description": "text about book",
            "year": 2000,
            "pages": 200,
            "genre": "Horror",
            "type": "Paper",
            "author_id": [2],
        }
        response = client.post("/books/", json=payload)
        assert response.status_code == 201, response.text
        book = response.json()
        assert "id" in book
        assert "reviews" in book
        assert book["rating"] == 0
        assert len(book["authors"]) == 1
        assert author in book["authors"]

        response = client.get("/books/", params={"offset": 2})
        assert response.status_code == 200
        books = response.json()
        assert book in books
