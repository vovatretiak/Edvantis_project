from typing import List

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from project import models
from project.books import schemas
from project.models import Author
from project.models import Review


def get_book_by_id(db: Session, book_id: int) -> models.Book:
    """gets instance of Book model from database by its id

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        book_id (int): Primary key of Book model

    Raises:
        HTTPException: Handles no value

    Returns:
        models.Book: returns instance of Book model
    """
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} is not found",
        )
    return book


# https://sqlmodel.tiangolo.com/tutorial/fastapi/update/
def update_book(
    db: Session, book_id: int, updated_book: schemas.BookUpdate
) -> models.Book:
    """updates instance of Book model from database by its id

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        book_id (int): Primary key of Book model
        updated_book (schemas.BookUpdate): Book schema with updated values

    Raises:
        HTTPException: Handles no value

    Returns:
        models.Book: returns updated instance of Book model
    """
    book = get_book_by_id(db=db, book_id=book_id)

    for key, value in updated_book.dict(exclude_unset=True).items():
        if key == "author_id":
            book_authors = db.query(models.Book).get(book_id)
            book_authors.authors.clear()
            db.add(book_authors)
            db.commit()
            authors = db.query(Author).filter(Author.id.in_(value))
            if authors.count() == len(value):
                book.authors.extend(authors)
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Authors is not found"
                )
        setattr(book, key, value)

    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_books_by_author_id(db: Session, author_id: int) -> List[models.Book]:
    """gets list of instances of Book model from database by specific author

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        author_id (int): Primary key of Author model

    Returns:
        List[models.Book]: returns list of instances of Book model
    """
    author = db.query(Author).filter(Author.id == author_id).first()
    return author.books


def get_books(db: Session, offset: int, limit: int) -> List[models.Book]:
    """gets list of instances of Book model from database

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        offset (int): Query parameter, the number of items to skip before returning
        limit (int): Query parameter, the number of items returned from a query

    Returns:
        List[models.Book]: returns list of instances of Book model
    """
    return db.query(models.Book).offset(offset).limit(limit).all()


def get_books_by_rating(
    db: Session, rating: int, offset: int, limit: int
) -> List[models.Book]:
    """gets list of instances of Book model from database with specific rating

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        rating (int): Path parameter, value limit of needed rating
        offset (int): Query parameter, the number of items to skip before returning
        limit (int): Query parameter, the number of items returned from a query

    Returns:
        List[models.Book]: returns list of instances of Book model with specific rating
    """
    books = (
        db.query(models.Book)
        .where(models.Book.rating >= rating)
        .order_by(models.Book.rating.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return books


def get_recommendations(
    db: Session, genre: str, offset: int, limit: int
) -> List[models.Book]:
    """gets list of instances of Book model from database with specific genre

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        genre (str): Path parameter, preferred genre
        offset (int): Query parameter, the number of items to skip before returning
        limit (int): Query parameter, the number of items returned from a query

    Returns:
        List[models.Book]: returns list of instances of Book model with pregerred genre
    """
    avg_rating = (
        db.query(func.avg(models.Book.rating))
        .filter(models.Book.genre == genre)
        .group_by(models.Book.genre)
        .scalar_subquery()
    )
    books = (
        db.query(models.Book)
        .filter(models.Book.genre == genre)
        .where(models.Book.rating >= avg_rating)
        .order_by(models.Book.rating.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return books


# https://stackoverflow.com/questions/68394091/fastapi-sqlalchemy-pydantic-%E2%86%92-how-to-process-many-to-many-relations
def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    """creates instance of Book model and adds it to database

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        book (schemas.BookCreate): New Book instance

    Raises:
        HTTPException: Handles no value

    Returns:
        models.Book: returns new instance of Book model
    """
    new_book = models.Book(
        title=book.title,
        description=book.description,
        year=book.year,
        image_file=book.image_file,
        pages=book.pages,
        genre=book.genre,
        type=book.type,
    )
    authors = db.query(Author).filter(Author.id.in_(book.author_id))
    if authors.count() == len(book.author_id):
        new_book.authors.extend(authors)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Authors is not found"
        )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def delete_book(db: Session, book_id: int) -> None:
    """deletes instance of Book model from database

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        book_id (int): Primary key of Book model

    Raises:
        HTTPException: Handles no value
    """
    book = db.query(models.Book).filter(models.Book.id == book_id)
    if not book.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} is not found",
        )
    # remove authors from a book
    book_authors = db.query(models.Book).get(book_id)
    book_authors.authors.clear()
    db.add(book_authors)
    db.commit()
    # delete reviews
    book_reviews = (
        db.query(models.Book)
        .join(models.Book.reviews)
        .filter(models.Book.id == book_id)
        .first()
    )
    if book_reviews:
        for review in book_reviews.reviews:
            r = db.query(Review).filter(Review.id == review.id)
            r.delete()
            db.commit()
    # remove book
    book.delete()
    db.commit()
