from typing import List
from fastapi import FastAPI

from schemas import Book, BookGenres, BookType

app = FastAPI()

db: List[Book] = [
    Book(
        id=1,
        title='First book',
        description='description for book',
        year=2000,
        ISBN='978-966-2355-57-4',
        pages=200,
        author=['Jonh Doe', 'Jane doe'],
        genre=BookGenres.horror,
        type=BookType.paper,
        reviews=[]
    ),
    Book(
        id=2,
        title='Second book',
        description='description for new book',
        year=1998,
        ISBN='978-961-2312-57-3',
        pages=400,
        author=['Bob Cat'],
        genre=BookGenres.comic_book,
        type=BookType.paper,
        reviews=['this is cool']
    )
]


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/books/")
def get_all_books():
    return db


@app.post("/books/")
def create_book(book: Book):
    db.append(book)
    return book
