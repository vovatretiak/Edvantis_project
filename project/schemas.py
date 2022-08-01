from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, root_validator, validator


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class ReviewRating(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class ReviewBase(BaseModel):
    user_id: int
    text: Optional[str]
    rating: ReviewRating
    book_id: int


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(ReviewBase):
    user_id: Union[int, None] = None
    text: Union[str, None] = None
    rating: Union[ReviewRating, None] = None
    book_id: Union[int, None] = None


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
    reviews: List[Review] = []

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    image_file: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    middle_name: Union[str, None] = None
    image_file: Union[str, None] = None


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
    HORROR = "Horrror"
    HISTORICAL = "Historical"
    ROMANCE = "Romance"
    FANTASY = "Fantasy"
    SCI_FI = "Science Fiction"


class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    year: int
    image_file: Optional[str] = None
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
    author_id: List[int] = []


class BookUpdate(BookBase):
    title: Union[str, None] = None
    description: Union[str, None] = None
    year: Union[int, None] = None
    image_file: Union[str, None] = None
    pages: Union[int, None] = None
    author_id: Union[List[int], None] = None
    review_id: Union[List[int], None] = None
    genre: Union[BookGenre, None] = None
    type: Union[BookType, None] = None


class Book(BookBase):
    id: int
    authors: List[Author] = []
    reviews: List[Review] = []

    class Config:
        orm_mode = True
