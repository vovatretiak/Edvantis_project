from __future__ import annotations

from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import status
from sqlalchemy.orm import Session

from project import crud
from project import database
from project import schemas

router = APIRouter(prefix="/reviews", tags=["Reviews"])


get_db = database.get_db


@router.post("/", response_model=schemas.Review, status_code=status.HTTP_201_CREATED)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(db=db, review=review)


@router.get("/", response_model=List[schemas.Review], status_code=status.HTTP_200_OK)
def get_all_reviews(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=10, lte=15),
):
    return crud.get_reviews(db=db, offset=offset, limit=limit)


@router.get(
    "/{review_id}", response_model=schemas.Review, status_code=status.HTTP_200_OK
)
def get_review_by_id(review_id: int, db: Session = Depends(get_db)):
    return crud.get_review_by_id(db=db, review_id=review_id)


@router.put(
    "/{review_id}", response_model=schemas.Review, status_code=status.HTTP_202_ACCEPTED
)
def update_review(
    review_id: int, updated_review: schemas.ReviewCreate, db: Session = Depends(get_db)
):
    return crud.update_review(db=db, review_id=review_id, updated_review=updated_review)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    return crud.delete_review(db=db, review_id=review_id)
