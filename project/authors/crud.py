from typing import List

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from project.authors import models
from project.authors import schemas


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    """creates instance of Author model and adds it to database

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        author (schemas.AuthorCreate): New Author instance

    Returns:
        models.Author: returns new instance of Author model
    """
    new_author = models.Author(
        first_name=author.first_name,
        last_name=author.last_name,
        middle_name=author.middle_name,
        image_file=author.image_file,
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def get_authors(db: Session, offset: int, limit: int) -> List[models.Author]:
    """gets list of instances of Author model from database

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        offset (int): Query parameter, the number of items to skip before returning
        limit (int): Query parameter, the number of items returned from a query

    Returns:
        List[models.Author]: returns list of instances of Author model
    """
    return db.query(models.Author).offset(offset).limit(limit).all()


def get_author_by_id(db: Session, author_id: int) -> models.Author:
    """gets instance of Author model from database by its id

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        author_id (int): Primary key of Author model

    Raises:
        HTTPException: Handles no value

    Returns:
        models.Author: returns instance of Author model
    """
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id {author_id} is not found",
        )
    return author


def update_author(
    db: Session, author_id: int, updated_author: schemas.AuthorUpdate
) -> models.Author:
    """updates instance of Author model from database by its id

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        author_id (int): Primary key of Author model
        updated_author (schemas.AuthorUpdate): Author schema with updated values

    Raises:
        HTTPException: Handles no value

    Returns:
        models.Author: returns updated instance of Author model
    """
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id {author_id} is not found",
        )
    for key, value in updated_author.dict(exclude_unset=True).items():
        setattr(author, key, value)

    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def delete_author(db: Session, author_id: int) -> None:
    """deletes instance of Author model from database

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        author_id (int): Primary key of Author model

    Raises:
        HTTPException: Handles no value
    """
    author = db.query(models.Author).filter(models.Author.id == author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id {author_id} is not found",
        )
    author.delete()
    db.commit()
