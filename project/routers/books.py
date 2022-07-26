from typing import List

from fastapi import APIRouter, Depends, status
from project import crud, database, schemas
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/books",
    tags=["Books"])

get_db = database.get_db


@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@router.get("/", response_model=List[schemas.Book], status_code=status.HTTP_200_OK)
def get_all_books(db: Session = Depends(get_db)):
    return crud.get_books(db=db)


@router.get("/{book_id}", response_model=schemas.Book, status_code=status.HTTP_200_OK)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    return crud.get_book_by_id(db=db, book_id=book_id)


@router.get("/author/{author_id}", response_model=List[schemas.Book], status_code=status.HTTP_200_OK)
def get_books_by_author_id(author_id: int, db: Session = Depends(get_db)):
    return crud.get_books_by_author_id(db=db, author_id=author_id)


@router.put("/{book_id}", response_model=schemas.Book,
            status_code=status.HTTP_202_ACCEPTED)
def update_book(book_id: int, updated_book: schemas.BookUpdate, db: Session = Depends(get_db)):
    return crud.update_book(db=db, book_id=book_id, updated_book=updated_book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return crud.delete_book(db=db, book_id=book_id)