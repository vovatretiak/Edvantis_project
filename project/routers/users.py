from typing import List

from fastapi import APIRouter, Depends, status
from project import crud, database, schemas
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Users"])

get_db = database.get_db


@router.post(
    "/registration", response_model=schemas.User, status_code=status.HTTP_201_CREATED
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(user=user, db=db)
