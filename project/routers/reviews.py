from typing import List

from fastapi import APIRouter, Depends, status
from project import crud, database, schemas
from sqlalchemy.orm import Session

router = APIRouter(prefix="/reviews", tags=["Reviews"])

get_db = database.get_db


@router.post("/", response_model=schemas.Review, status_code=status.HTTP_201_CREATED)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(db=db, review=review)


@router.get("/", response_model=List[schemas.Review], status_code=status.HTTP_200_OK)
def get_all_reviews(db: Session = Depends(get_db)):
    return crud.get_reviews(db=db)


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
