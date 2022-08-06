from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import status
from sqlalchemy.orm import Session

from project import crud
from project import database
from project import models
from project import schemas
from project import utils

router = APIRouter(prefix="/reviews", tags=["Reviews"])


get_db = database.get_db


@router.post("/", response_model=schemas.Review, status_code=status.HTTP_201_CREATED)
def create_review(
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(utils.get_current_user),
) -> schemas.Review:
    """post method to create new review

    Args:
        review (schemas.ReviewCreate)
        db (Session, optional): Defaults to Depends(get_db).

    Returns:
        schemas.Review
    """
    return crud.create_review(db=db, review=review, user=current_user)


@router.get("/", response_model=List[schemas.Review], status_code=status.HTTP_200_OK)
def get_all_reviews(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=10, lte=15),
) -> List[schemas.Review]:
    """get method to show all reviews

    Args:
        db (Session, optional): Defaults to Depends(get_db).
        offset (int, optional): Defaults to 0.
        limit (int, optional): Defaults to Query(default=10, lte=15).

    Returns:
        List[schemas.Review]
    """
    return crud.get_reviews(db=db, offset=offset, limit=limit)


@router.get(
    "/{review_id}", response_model=schemas.Review, status_code=status.HTTP_200_OK
)
def get_review_by_id(review_id: int, db: Session = Depends(get_db)) -> schemas.Review:
    """get method to show review by its id

    Args:
        review_id (int)
        db (Session, optional): Defaults to Depends(get_db).

    Returns:
        schemas.Review
    """
    return crud.get_review_by_id(db=db, review_id=review_id)


@router.put(
    "/{review_id}", response_model=schemas.Review, status_code=status.HTTP_202_ACCEPTED
)
def update_review(
    review_id: int, updated_review: schemas.ReviewCreate, db: Session = Depends(get_db)
) -> schemas.Review:
    """put method to update review by its id

    Args:
        review_id (int)
        updated_review (schemas.ReviewCreate): review schema with updated values
        db (Session, optional): Defaults to Depends(get_db).

    Returns:
        schemas.Review
    """
    return crud.update_review(db=db, review_id=review_id, updated_review=updated_review)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db)) -> None:
    """delete method to delete review by its id

    Args:
        review_id (int)
        db (Session, optional): Defaults to Depends(get_db).
    """
    return crud.delete_review(db=db, review_id=review_id)
