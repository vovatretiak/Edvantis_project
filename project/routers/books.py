from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi import Query
from fastapi import status
from sqlalchemy.orm import Session

from project import database
from project.books import crud
from project.books import schemas

router = APIRouter(prefix="/books", tags=["Books"])


get_db = database.get_db


@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(
    book: schemas.BookCreate, db: Session = Depends(get_db)
) -> schemas.Book:
    """post method to create new book

    Args:
        book (schemas.BookCreate): describes book model
        db (Session, optional): Manages persistence operations for ORM-mapped objects.
        Defaults to Depends(get_db).

    Returns:
        schemas.Book
    """
    return crud.create_book(db=db, book=book)


@router.get("/", response_model=List[schemas.Book], status_code=status.HTTP_200_OK)
def get_all_books(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=10, lte=15),
) -> List[schemas.Book]:
    """get method to show all books

    Args:
        db (Session, optional): Defaults to Depends(get_db).
        offset (int, optional):  Defaults to 0.
        limit (int, optional):  Defaults to Query(default=10, lte=15).

    Returns:
        List[schemas.Book]
    """
    return crud.get_books(db=db, offset=offset, limit=limit)


@router.get(
    "/rating/{rating}",
    response_model=List[schemas.Book],
    status_code=status.HTTP_200_OK,
)
def get_books_with_rating(
    rating: int = Path(title="The rating of the book", ge=1, le=5),
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=3, lte=5),
) -> List[schemas.Book]:
    """get method to show books with specific rating

    Args:
        rating (int, optional): Defaults to Path(title="The rating of the book", ge=1, le=5).
        db (Session, optional): Defaults to Depends(get_db).
        offset (int, optional): Defaults to 0.
        limit (int, optional): Defaults to Query(default=3, lte=5).

    Returns:
        List[schemas.Book]
    """
    return crud.get_books_by_rating(db=db, rating=rating, offset=offset, limit=limit)


@router.get(
    "/recommendations/{genre}",
    response_model=List[schemas.Book],
    status_code=status.HTTP_200_OK,
)
def get_recommendations(
    genre: schemas.BookGenre,
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=3, lte=5),
) -> List[schemas.Book]:
    """gets list of instances of Book model from database with specific genre

    Args:
        genre (schemas.BookGenre): _description_
        db (Session, optional): Defaults to Depends(get_db).
        offset (int, optional): Defaults to 0.
        limit (int, optional): Defaults to Query(default=3, lte=5).

    Returns:
        List[schemas.Book]
    """
    return crud.get_recommendations(db=db, genre=genre, offset=offset, limit=limit)


@router.get("/{book_id}", response_model=schemas.Book, status_code=status.HTTP_200_OK)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)) -> schemas.Book:
    """get method to show book by its id

    Args:
        book_id (int)
        db (Session, optional): Defaults to Depends(get_db).

    Returns:
        schemas.Book
    """
    return crud.get_book_by_id(db=db, book_id=book_id)


@router.get(
    "/authors/{author_id}",
    response_model=List[schemas.Book],
    status_code=status.HTTP_200_OK,
)
def get_books_by_author_id(
    author_id: int, db: Session = Depends(get_db)
) -> List[schemas.Book]:
    """get method to show books by their author id

    Args:
        author_id (int)
        db (Session, optional): Defaults to Depends(get_db).

    Returns:
        List[schemas.Book]
    """
    return crud.get_books_by_author_id(db=db, author_id=author_id)


@router.put(
    "/{book_id}", response_model=schemas.Book, status_code=status.HTTP_202_ACCEPTED
)
def update_book(
    book_id: int, updated_book: schemas.BookUpdate, db: Session = Depends(get_db)
) -> schemas.Book:
    """put method to update book by its id

    Args:
        book_id (int)
        updated_book (schemas.BookUpdate): book schema with updated values
        db (Session, optional): Defaults to Depends(get_db).

    Returns:
        schemas.Book
    """
    return crud.update_book(db=db, book_id=book_id, updated_book=updated_book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)) -> None:
    """delete method to delete book by its id

    Args:
        book_id (int)
        db (Session, optional): Defaults to Depends(get_db).
    """
    return crud.delete_book(db=db, book_id=book_id)
