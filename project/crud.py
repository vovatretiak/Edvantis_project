from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas


# crud for books
def get_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                'detail': f'Book with id {book_id} is not found'
            }
        )
    return book


def get_books(db: Session):
    return db.query(models.Book).all()


def create_book(db: Session, book: schemas.BookCreate):
    new_book = models.Book(
        title=book.title, description=book.description, year=book.year,
        image_file=book.image_file, pages=book.pages, author=book.author,
        genre=book.genre, type=book.type, reviews=book.reviews
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book
