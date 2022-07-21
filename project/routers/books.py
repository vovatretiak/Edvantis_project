
from typing import List

from fastapi import APIRouter, Depends, status
from project import crud, database, models, schemas
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/books",
    tags=["Books"])

get_db = database.get_db


@router.get("/", response_model=List[schemas.Book])
def get_all_books(db: Session = Depends(get_db)):
    return crud.get_books(db=db)


@router.get("/{id}", response_model=schemas.Book)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    return crud.get_book(db=db, book_id=book_id)


@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@router.put("/", response_model=schemas.Book, status_code=status.HTTP_202_ACCEPTED)
def update_book():
    pass
