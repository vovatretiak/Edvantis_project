from __future__ import annotations

from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import status
from sqlalchemy.orm import Session

from project import crud
from project import database
from project import schemas

router = APIRouter(prefix="/authors", tags=["Authors"])


get_db = database.get_db


@router.post("/", response_model=schemas.Author, status_code=status.HTTP_201_CREATED)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@router.get("/", response_model=List[schemas.Author])
def get_all_authors(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=5, lte=10),
):
    return crud.get_authors(db=db, offset=offset, limit=limit)


@router.get(
    "/{author_id}", response_model=schemas.Author, status_code=status.HTTP_200_OK
)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db=db, author_id=author_id)


@router.put(
    "/{author_id}", response_model=schemas.Author, status_code=status.HTTP_200_OK
)
def update_author(
    author_id: int, updated_author: schemas.AuthorUpdate, db: Session = Depends(get_db)
):
    return crud.update_author(db=db, author_id=author_id, updated_author=updated_author)


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    return crud.delete_author(db=db, author_id=author_id)
