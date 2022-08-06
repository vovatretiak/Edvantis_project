from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from project import crud
from project import database
from project import models
from project import schemas
from project import utils

router = APIRouter(prefix="/users", tags=["Users"])


get_db = database.get_db


@router.post(
    "/registration", response_model=schemas.User, status_code=status.HTTP_201_CREATED
)
def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.User:
    """post method to create new user

    Args:
        user (schemas.UserCreate): describes user model
        db (Session, optional): Manages persistence operations for ORM-mapped objects.
        Defaults to Depends(get_db).

    Returns:
        schemas.User
    """
    return crud.create_user(user=user, db=db)


@router.post(
    "/login", response_model=schemas.Token, status_code=status.HTTP_201_CREATED
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> schemas.Token:
    """post method to create token for user

    Args:
        form_data (OAuth2PasswordRequestForm, optional):  Defaults to Depends().
        db (Session, optional): Manages persistence operations for ORM-mapped objects.
        Defaults to Depends(get_db).

    Raises:
        HTTPException: Handle wrong password

    Returns:
        schemas.Token
    """
    user = crud.get_user_by_username(db=db, username=form_data.username)
    hashed_pw = user.password
    if not utils.verify_password(form_data.password, hashed_pw):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )
    access_token = utils.create_access_token(subject=form_data.username)
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.get("/", response_model=List[schemas.User], status_code=status.HTTP_200_OK)
def get_users(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=5, lte=10),
) -> List[schemas.User]:
    """get method to show all users

    Args:
        db (Session, optional)  Defaults to Depends(get_db).
        offset (int, optional)  Defaults to 0.
        limit (int, optional)  Defaults to Query(default=5, lte=10).

    Returns:
        List[schemas.User]
    """
    return crud.get_users(db=db, offset=offset, limit=limit)


@router.get("/profile", response_model=schemas.User, status_code=status.HTTP_200_OK)
def read_me(
    current_user: models.User = Depends(utils.get_current_user),
) -> schemas.User:
    """get method to show current user

    Args:
        current_user (models.User, optional): Defaults to Depends(utils.get_current_user).

    Returns:
        schemas.User
    """
    user = current_user
    return user


@router.put(
    "/profile", response_model=schemas.User, status_code=status.HTTP_202_ACCEPTED
)
def update_me(
    updated_user: schemas.UserUpdate,
    current_user: models.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
) -> schemas.User:
    """put method to update current user

    Args:
        db (Session, optional)  Defaults to Depends(get_db).
        updated_user (schemas.UserUpdate)
        current_user (models.User, optional): Defaults to Depends(utils.get_current_user).

    Returns:
        schemas.User
    """
    return crud.update_user(db=db, current_user=current_user, updated_user=updated_user)


@router.delete("/profile", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(
    current_user: models.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """delete method to delete current user

    Args:
        current_user (models.User, optional): Defaults to Depends(utils.get_current_user).
    """
    return crud.delete_user(db=db, current_user=current_user)
