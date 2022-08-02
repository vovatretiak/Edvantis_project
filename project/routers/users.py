from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from project import crud, database, schemas, utils, models
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Users"])

get_db = database.get_db


@router.post(
    "/registration", response_model=schemas.User, status_code=status.HTTP_201_CREATED
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(user=user, db=db)


@router.post(
    "/login", response_model=schemas.Token, status_code=status.HTTP_201_CREATED
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = crud.get_user_by_username(db=db, username=form_data.username)
    hashed_pw = user.password
    if not utils.verify_password(form_data.password, hashed_pw):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )
    access_token = utils.create_access_token(subject=form_data.username)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/", response_model=List[schemas.User], status_code=status.HTTP_200_OK)
def get_users(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=5, lte=10),
):
    return crud.get_users(db=db, offset=offset, limit=limit)


@router.get("/profile", response_model=schemas.User, status_code=status.HTTP_200_OK)
def read_users_me(current_user: models.User = Depends(utils.get_current_user)):
    user = current_user
    return user
