from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from project import crud, database, schemas, utils
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
