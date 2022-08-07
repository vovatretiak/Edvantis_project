from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import status
from sqlalchemy.orm import Session

from project import database
from project.authors import crud
from project.authors import schemas

router = APIRouter(prefix="/authors", tags=["Authors"])


get_db = database.get_db


@router.post("/", response_model=schemas.Author, status_code=status.HTTP_201_CREATED)
def create_author(
    author: schemas.AuthorCreate, db: Session = Depends(get_db)
) -> schemas.Author:
    """post method to create new author

    Args:
        author (schemas.AuthorCreate): describes author model
        db (Session, optional): Defaults to Depends(get_db).

    Returns:
        schemas.Author
    """
    return crud.create_author(db=db, author=author)


@router.get("/", response_model=List[schemas.Author])
def get_all_authors(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=5, lte=10),
) -> List[schemas.Author]:
    """get method to show all authors

    Args:
        db (Session, optional): Defaults to Depends(get_db).
        offset (int, optional): Defaults to 0.
        limit (int, optional): Defaults to Query(default=5, lte=10).

    Returns:
        List[schemas.Author]
    """
    return crud.get_authors(db=db, offset=offset, limit=limit)


@router.get(
    "/{author_id}", response_model=schemas.Author, status_code=status.HTTP_200_OK
)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db=db, author_id=author_id)


@router.put(
    "/{author_id}", response_model=schemas.Author, status_code=status.HTTP_202_ACCEPTED
)
def update_author(
    author_id: int, updated_author: schemas.AuthorUpdate, db: Session = Depends(get_db)
) -> schemas.Author:
    """get method to show author by its id
    Args:
        author_id (int)
        updated_author (schemas.AuthorUpdate): author schema with updated values
        db (Session, optional): Defaults to Depends(get_db).

    Returns:
        schemas.Author
    """
    return crud.update_author(db=db, author_id=author_id, updated_author=updated_author)


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)) -> None:
    """delete method to delete author by its id

    Args:
        author_id (int)
        db (Session, optional): Defaults to Depends(get_db).
    """
    return crud.delete_author(db=db, author_id=author_id)
