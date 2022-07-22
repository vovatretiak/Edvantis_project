from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import values
from sqlalchemy.orm import Session

from . import models, schemas


# crud for books
def get_book_by_id(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                'detail': f'Book with id {book_id} is not found'
            }
        )
    return book


# https://sqlmodel.tiangolo.com/tutorial/fastapi/update/
def update_book(db: Session, book_id: int, updated_book: schemas.BookUpdate):
    book = get_book_by_id(db=db, book_id=book_id)
    for key, value in updated_book.dict(exclude_unset=True).items():
        setattr(book, key, value)
    print(book)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_books(db: Session):
    return db.query(models.Book).all()


def create_book(db: Session, book: schemas.BookCreate):
    new_book = models.Book(
        title=book.title, description=book.description, year=book.year,
        image_file=book.image_file, pages=book.pages,
        genre=book.genre, type=book.type, reviews=book.reviews
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book
