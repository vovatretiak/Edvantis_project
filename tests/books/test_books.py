import json

import pytest
from fastapi.testclient import TestClient

from ..db_for_tests import override_get_db
from main import app
from project.books.schemas import BookGenre
from project.models import Author
from project.models import Book
from project.models import Review
from project.models import User
from project.reviews.crud import create_review
from project.reviews.schemas import ReviewCreate
from project.reviews.schemas import ReviewRating
from project.utils import get_password_hash


client = TestClient(app)

db = next(override_get_db())


@pytest.fixture(autouse=True, scope="class")
def create_dummy_books():
    """fixture to execute asserts before and after a test is run"""

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
    for book in books[:10]:
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

    create_review(
        db,
        user=new_user,
        review=ReviewCreate(text="wow", rating=ReviewRating.FOUR, book_id=1),
    )
    create_review(
        db,
        user=new_user2,
        review=ReviewCreate(text="bad", rating=ReviewRating.ONE, book_id=1),
    )
    create_review(
        db,
        user=new_user,
        review=ReviewCreate(text="good", rating=ReviewRating.THREE, book_id=2),
    )
    create_review(
        db,
        user=new_user2,
        review=ReviewCreate(text="wow", rating=ReviewRating.FIVE, book_id=2),
    )
    create_review(
        db,
        user=new_user,
        review=ReviewCreate(text="not good", rating=ReviewRating.TWO, book_id=3),
    )
    create_review(
        db,
        user=new_user2,
        review=ReviewCreate(text="not good", rating=ReviewRating.TWO, book_id=3),
    )
    create_review(
        db,
        user=new_user,
        review=ReviewCreate(text="wow", rating=ReviewRating.FIVE, book_id=4),
    )
    create_review(
        db,
        user=new_user2,
        review=ReviewCreate(text="wow", rating=ReviewRating.FIVE, book_id=4),
    )

    yield
    # # teardown
    for i in range(1, 9):
        db.query(Review).filter(Review.id == i).delete()
    for i in range(1, 11):
        db.query(Book).filter(Book.id == i).delete()

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
        db.query(Book).filter(Book.id == book["id"]).delete()
        db.commit()

    def test_get_all_books(self):
        """tests get method to show all books"""
        response = client.get("/books/")
        assert response.status_code == 200, response.text
        books = response.json()
        assert len(books) == 10
        assert books[0]["title"] == "Thalasseus maximus"
        assert books[0]["rating"] == 2.5
        assert books[0]["year"] == 2007
        assert books[0]["genre"] == "Thriller"
        assert books[2]["type"] == "Electronic"
        assert books[6]["pages"] == 52
        first_book = books[0]
        # with params
        response = client.get("/books/", params={"offset": 6, "limit": 2})
        assert response.status_code == 200, response.text
        books = response.json()
        assert first_book not in books
        assert len(books) == 2
        assert books[0]["id"] == 7
        assert books[1]["id"] == 8

    def test_books_with_rating(self):
        """tests get method to show books with specific rating"""
        # from 2 and bigger
        rating = 2
        response = client.get(f"/books/rating/{rating}")
        books = response.json()
        assert books[0]["rating"] == 2
        assert books[0]["title"] == "Plegadis falcinellus"
        assert books[1]["rating"] == 2.5
        assert books[1]["title"] == "Thalasseus maximus"
        # from 3 and bigger
        rating = 3
        response = client.get(f"/books/rating/{rating}")
        books = response.json()
        assert books[0]["rating"] == 4
        assert books[0]["title"] == "unavailable"
        assert books[1]["rating"] == 5
        assert books[1]["title"] == "Paroaria gularis"
        # from 4 and bigger
        rating = 4
        response = client.get(f"/books/rating/{rating}")
        books = response.json()
        assert books[0]["rating"] == 4
        assert books[0]["title"] == "unavailable"
        assert books[1]["rating"] == 5
        assert books[1]["title"] == "Paroaria gularis"
        # equal 5
        rating = 5
        response = client.get(f"/books/rating/{rating}")
        books = response.json()
        assert len(books) == 1
        assert books[0]["rating"] == 5
        assert books[0]["title"] == "Paroaria gularis"

    def test_get_book_by_id(self):
        """tests get method to show book by its id"""
        book_id = 1
        response = client.get(f"/books/{book_id}")
        assert response.status_code == 200
        book = response.json()
        assert book["title"] == "Thalasseus maximus"
        # id not exist
        book_id = 12
        response = client.get(f"/books/{book_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == f"Book with id {book_id} is not found"

    def test_get_recommendation(self):
        """tests get method to show book with specific genre
        with rating more than average rating in this genre"""
        # thriller book with rating 0
        book_id = 8
        response = client.get(f"/books/{book_id}")
        assert response.status_code == 200
        book = response.json()
        assert book["genre"] == "Thriller"

        genre = BookGenre.THRILLER
        response = client.get(f"/books/recommendations/{genre}")
        assert response.status_code == 200
        books = response.json()
        assert book not in books
        assert len(books) == 2
        assert books[0]["title"] == "unavailable"
        assert books[0]["rating"] == 4
        assert books[1]["title"] == "Thalasseus maximus"
        assert books[1]["rating"] == 2.5

    def test_get_books_by_author_id(self):
        """tests get method to show books by their author id"""
        author_id = 2
        response = client.get(f"/books/authors/{author_id}")
        assert response.status_code == 200
        books = response.json()
        assert len(books) == 3
        authors_books = ["Dendrocygna viduata", "Paroaria gularis", "unavailable"]
        assert books[0]["title"] in authors_books
        assert books[1]["title"] in authors_books
        assert books[2]["title"] in authors_books
        author_id = 1  # all books
        response = client.get(f"/books/authors/{author_id}")
        assert response.status_code == 200
        books = response.json()
        assert len(books) == 10

    def test_update_book(self):
        """tests put method to update book by its id"""

        book_id = 1
        updated_book = {
            "title": "updated title",
            "year": 1999,
            "genre": BookGenre.FANTASY,
            "author_id": [2],
        }
        response = client.put(f"/books/{book_id}", json=updated_book)
        assert response.status_code == 202
        book = response.json()
        assert book["title"] == updated_book["title"]
        assert book["authors"][0]["id"] == 2
        # books by author1 decreased by 1
        response = client.get("/books/authors/1")
        assert response.status_code == 200
        books = response.json()
        assert len(books) == 9
        # book_id not exist
        book_id = 12
        response = client.put(f"/books/{book_id}", json=updated_book)
        assert response.status_code == 404
        assert response.json()["detail"] == f"Book with id {book_id} is not found"
        # authors not exist
        updated_book["author_id"] = [5]
        book_id = 1
        response = client.put(f"/books/{book_id}", json=updated_book)
        assert response.status_code == 404
        assert response.json()["detail"] == "Authors is not found"
