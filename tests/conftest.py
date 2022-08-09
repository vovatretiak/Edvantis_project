import json

import pytest

from .db_for_tests import override_get_db
from project.models import Author
from project.models import Book
from project.models import User
from project.utils import get_password_hash


@pytest.fixture(autouse=True)
def create_dummy_users():
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
    yield

    # teardown
    db.query(User).filter(User.username == "john123").delete()
    db.query(User).filter(User.username == "jane123").delete()
    db.commit()


@pytest.fixture(autouse=True)
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


@pytest.fixture(autouse=True)
def create_dummy_books():
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
    db.add(author)
    db.add(author2)
    db.commit()

    with open("E:\\vscode\\edvantis_project\\books.json") as file:
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
    yield

    # teardown
    db.query(Author).filter(Author.id == 1).delete()
    db.query(Author).filter(Author.id == 2).delete()
    db.commit()
