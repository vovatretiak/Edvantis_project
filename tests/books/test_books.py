import json

import pytest

from ..db_for_tests import override_get_db
from project.models import Author
from project.models import Book


@pytest.fixture(autouse=True, scope="class")
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
    yield

    # teardown
    db.query(Author).filter(Author.id == 1).delete()
    db.query(Author).filter(Author.id == 2).delete()
    db.commit()
