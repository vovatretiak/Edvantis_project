from typing import List

from fastapi import APIRouter, Depends, status
from project import crud, database, schemas
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"])

get_db = database.get_db


@router.post("/", response_model=schemas.Review, status_code=status.HTTP_201_CREATED)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(db=db, review=review)


@router.get("/", response_model=List[schemas.Review], status_code=status.HTTP_200_OK)
def get_all_review(db: Session = Depends(get_db)):
    return crud.get_reviews(db=db)
