from typing import List

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from project.books.models import Book
from project.reviews import models
from project.reviews import schemas
from project.users.models import User
from project.utils import get_user_rank


def create_review(
    db: Session, review: schemas.ReviewCreate, user: User
) -> models.Review:
    """creates instance of Review model and adds it to database

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        review (schemas.ReviewCreate): New Review instance
    Raises:
        HTTPException: Handles no value

    Returns:
        returns instance of Review model
    """
    book = db.query(Book).filter(Book.id == review.book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {review.book_id} is not found",
        )
    new_review = models.Review(
        user_id=user.id,
        text=review.text,
        rating=review.rating,
        book_id=review.book_id,
    )
    db.add(new_review)
    db.commit()
    book.reviews.append(new_review)
    rating = (
        db.query(func.avg(models.Review.rating))
        .filter(models.Review.book_id == review.book_id)
        .group_by(models.Review.book_id)
        .first()
    )
    book.rating = float(rating[0])
    db.add(book)
    user = db.query(User).filter(User.id == user.id).first()
    rank = get_user_rank(len(user.reviews))
    user.rank = rank
    db.add(user)
    db.commit()
    db.refresh(book)
    db.refresh(user)
    db.refresh(new_review)

    return new_review


def get_reviews(db: Session, offset: int, limit: int) -> List[models.Review]:
    """gets list of instances of Review model from database

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        offset (int): Query parameter, the number of items to skip before returning
        limit (int): Query parameter, the number of items returned from a query

    Returns:
        List[models.Review]: returns list of instances of Review model
    """
    return db.query(models.Review).offset(offset).limit(limit).all()


def get_review_by_id(db: Session, review_id: int) -> models.Review:
    """gets instance of Review model from database by its id

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        review_id (int): Primary key of Review model

    Raises:
        HTTPException: Handle no value

    Returns:
        returns instance of Review model
    """
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} is not found",
        )
    return review


def update_review(
    db: Session, review_id: int, updated_review: schemas.ReviewUpdate, user: User
) -> models.Review:
    """updates instance of Review model from database by its id

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        review_id (int): Primary key of Review model
        updated_review (schemas.ReviewCreate): Review schema with updated values

    Raises:
        HTTPException: Handle no value or if access is granted

    Returns:
        returns updated instance of Review model
    """
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} is not found",
        )
    if review.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    for key, value in updated_review.dict(exclude_unset=True).items():
        setattr(review, key, value)
    db.add(review)
    db.commit()
    db.refresh(review)
    book = db.query(Book).filter(Book.id == review.book_id).first()
    rating = (
        db.query(func.avg(models.Review.rating))
        .filter(models.Review.book_id == review.book_id)
        .group_by(models.Review.book_id)
        .first()
    )
    book.rating = float(rating[0])
    db.add(book)
    db.commit()
    db.refresh(book)
    return review


def delete_review(db: Session, review_id: int, user: User) -> None:
    """deletes instance of Review model from database by its id

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        review_id (int): Primary key of Review model

    Raises:
        HTTPException: Handle no value
    """
    review = db.query(models.Review).filter(models.Review.id == review_id)
    if not review.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} is not found",
        )
    if review.first().user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    book = db.query(Book).filter(Book.id == review.first().book_id).first()
    book.reviews.remove(review.first())
    review.delete()
    db.commit()
    if len(book.reviews) >= 1:
        rating = (
            db.query(func.avg(models.Review.rating))
            .filter(models.Review.book_id == review.first().book_id)
            .group_by(models.Review.book_id)
            .first()
        )
        book.rating = float(rating[0])
        db.add(book)
        db.commit()
        db.refresh(book)
    if len(book.reviews) == 0:
        book.rating = 0
        db.add(book)
        db.commit()
        db.refresh(book)
