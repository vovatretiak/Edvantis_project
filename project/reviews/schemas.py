from datetime import datetime
from enum import IntEnum
from typing import Union

from pydantic import BaseModel
from pydantic import validator


class ReviewRating(IntEnum):
    """
    Enum class for review rating
    """

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class ReviewBase(BaseModel):
    """
    ReviewBase schema describes basic review by user_id, text, rating and book_id
    """

    text: Union[str, None]
    rating: ReviewRating


class ReviewCreate(ReviewBase):
    """
    ReviewCreate schema to create review with user_id, text, rating and book_id
    validation may be added in the future
    """

    book_id: int

    @validator("book_id")
    def book_id_validation(cls, value: int):
        """check if booj id is valid"""
        if value < 1:
            raise ValueError("Id cannot be less then 1")
        return value


class ReviewUpdate(ReviewBase):
    """
    ReviewUpdate schema to update review with user_id, text, rating and book_id
    """

    text: Union[None, str] = None
    rating: Union[None, int] = None


class Review(ReviewBase):
    """
    Review schema to show review with its id, user_id, text, rating and time when its created
    """

    id: int
    user_id: int
    book_id: int
    created_at: datetime

    class Config:
        """config class for review"""

        orm_mode = True
