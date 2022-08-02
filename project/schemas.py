from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import root_validator
from pydantic import validator


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class ReviewRating(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class ReviewBase(BaseModel):
    user_id: int
    text: str | None
    rating: ReviewRating
    book_id: int


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(ReviewBase):
    user_id: int | None = None
    text: str | None = None
    rating: ReviewRating | None = None
    book_id: int | None = None


class Review(ReviewBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str
    password: str

    @validator("username")
    @classmethod
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v


class UserCreate(UserBase):
    confirm_password: str

    @root_validator
    @classmethod
    def passwords_match(cls, values):
        pw1, pw2 = values.get("password"), values.get("confirm_password")
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        return values


class User(UserBase):
    id: int
    reviews: list[Review] = []

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    first_name: str | None
    last_name: str | None
    middle_name: str | None
    image_file: str | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    image_file: str | None = None


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookType(Enum):
    PAPER = "Paper"
    ELECTRONIC = "Electronic"


class BookGenre(Enum):
    MYSTERY = "Mystery"
    THRILLER = "Thriller"
    HORROR = "Horror"
    HISTORICAL = "Historical"
    ROMANCE = "Romance"
    FANTASY = "Fantasy"
    SCI_FI = "Science Fiction"


class BookBase(BaseModel):
    title: str
    description: str | None = None
    year: int
    image_file: str | None = None
    pages: int
    genre: BookGenre
    type: BookType

    @validator("year")
    @classmethod
    def year_validation(cls, v):
        if v > 2022:
            raise ValueError("The year cannot be greater than the current one")
        elif v < 1450:
            raise ValueError("The year cannot be lower than 1450")
        return v

    @validator("pages")
    @classmethod
    def pages_validation(cls, v):
        if v < 15:
            raise ValueError("There cannot be less than 15 pages")
        return v


class BookCreate(BookBase):
    author_id: list[int] = []


class BookUpdate(BookBase):
    title: str | None = None
    description: str | None = None
    year: int | None = None
    image_file: str | None = None
    pages: int | None = None
    author_id: list[int] | None = None
    review_id: list[int] | None = None
    genre: BookGenre | None = None
    type: BookType | None = None


class Book(BookBase):
    id: int
    authors: list[Author] = []
    reviews: list[Review] = []

    class Config:
        orm_mode = True
