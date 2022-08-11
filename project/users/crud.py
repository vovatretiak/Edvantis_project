from typing import List

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from project import models
from project.users import schemas
from project.utils import get_password_hash


def create_user(user: schemas.UserCreate, db: Session) -> models.User:
    """creates instance of Review model and adds it to database

    Args:
        user (schemas.UserCreate): New User instance
        db (Session): Manages persistence operations for ORM-mapped objects

    Raises:
        HTTPException: Handle if value exist

    Returns:
        models.User: returns instance of User model
    """
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"User with username '{user.username}' is already exist",
        )
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"User with email '{user.email}' is already exist",
        )
    hashed_pw = get_password_hash(user.password)
    new_user = models.User(username=user.username, email=user.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_username(db: Session, username: str) -> models.User:
    """gets instance of User model from database by its username

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        username (str): Unique value in User model

    Raises:
        HTTPException: Handle if value not exist

    Returns:
        models.User: returns instance of User model
    """
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with username '{user.username}' is not exist",
        )
    return user


def get_users(db: Session, offset: int, limit: int) -> List[models.User]:
    """gets list of instances of User model from database

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        offset (int): Query parameter, the number of items to skip before returning
        limit (int): Query parameter, the number of items returned from a query

    Returns:
        List[models.User]: returns list of instances of User model
    """
    users = db.query(models.User).offset(offset).limit(limit).all()
    return users


def update_user(
    db: Session, current_user: models.User, updated_user: schemas.UserUpdate
) -> models.User:
    """updates current user

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        current_user (models.User): current user model
        updated_user (schemas.UserUpdate): updated user schema

    Raises:
        HTTPException: Hande invalid value

    Returns:
        models.User
    """
    c_user = (
        db.query(models.User)
        .filter(models.User.username == current_user.username)
        .first()
    )
    if updated_user.username:
        user = (
            db.query(models.User)
            .filter(models.User.username == updated_user.username)
            .first()
        )
        if user:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"User with username '{updated_user.username}' is already exist",
            )
        c_user.username = updated_user.username
    if updated_user.email:
        user = (
            db.query(models.User)
            .filter(models.User.email == updated_user.email)
            .first()
        )
        if user:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"User with email '{updated_user.email}' is already exist",
            )
        c_user.email = updated_user.email
    if updated_user.password and updated_user.confirm_password:
        hashed_pw = get_password_hash(updated_user.password)
        c_user.password = hashed_pw
    db.add(c_user)
    db.commit()
    db.refresh(c_user)
    return c_user


def delete_user(db: Session, current_user: models.User) -> None:
    """deletes current user

    Args:
        db (Session): Manages persistence operations for ORM-mapped objects
        current_user (models.User): current user model
    """
    user = db.query(models.User).filter(models.User.username == current_user.username)
    user.delete()
    db.commit()
