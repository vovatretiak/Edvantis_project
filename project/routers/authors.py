
from typing import List

from fastapi import APIRouter, Depends, status
from project import crud, database, schemas
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/authors",
    tags=["Authors"])

get_db = database.get_db


@router.post("/", response_model=schemas.Author, status_code=status.HTTP_201_CREATED)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@router.get("/", response_model=List[schemas.Author])
def get_all_authors(db: Session = Depends(get_db)):
    return crud.get_authors(db=db)
