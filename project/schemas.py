from datetime import datetime
from enum import Enum
from enum import IntEnum
from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import root_validator
from pydantic import validator
from strenum import StrEnum


class Token(BaseModel):
    """
    Token schema describes the token and its type
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    TokenData schema describes the data from token
    """

    username: Union[str, None] = None


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
    book_id: int


class ReviewCreate(ReviewBase):
    """
    ReviewCreate schema to create review with user_id, text, rating and book_id
    validation may be added in the future
    """


class ReviewUpdate(ReviewBase):
    """
    ReviewUpdate schema to update review with user_id, text, rating and book_id
    """

    text: Union[None, str] = None
    rating: Union[None, int] = None
    book_id: Union[None, int] = None


class Review(ReviewBase):
    """
    Review schema to show review with its id, user_id, text, rating and time when its created
    """

    id: int
    user_id: int
    created_at: datetime

    class Config:
        """config class for review"""

        orm_mode = True


class UserBase(BaseModel):
    """
    UserBase schema describes basic user by username, text, email and password
    """

    username: str
    email: str
    password: str

    @validator("username")
    @classmethod
    def username_alphanumeric(cls, username):
        """checks if username is alphanumeric"""
        assert username.isalnum(), "must be alphanumeric"
        return username


class UserCreate(UserBase):
    """
    UserCreate schema to create user with username, text, email, password and confirm_password
    """

    confirm_password: str

    @root_validator
    @classmethod
    def passwords_match(cls, values):
        """checks if the password and the confirm_password match"""
        pw1, pw2 = values.get("password"), values.get("confirm_password")
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        return values


class User(UserBase):
    """
    User schema to show user with its id, username, text, email, password and list of reviews
    """

    id: int
    reviews: List[Review] = []

    class Config:
        """config class for user"""

        orm_mode = True


class AuthorBase(BaseModel):
    """
    AuthorBase schema describes basic author by first_name, last_name, middle_name and image_file
    """

    first_name: Union[str, None]
    last_name: Union[str, None]
    middle_name: Union[str, None]
    image_file: Union[str, None] = None


class AuthorCreate(AuthorBase):
    """
    AuthorCreate schema to create author with first_name, last_name, middle_name and image_file
    """


class AuthorUpdate(BaseModel):
    """
    AuthorUpdate schema to update author with first_name, last_name, middle_name and image_file
    """

    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    middle_name: Union[str, None] = None
    image_file: Union[str, None] = None


class Author(AuthorBase):
    """
    Author schema to show author with its id, first_name, last_name, middle_name and image_file
    """

    id: int

    class Config:
        """config class for user"""

        orm_mode = True


class BookType(StrEnum):
    """
    Enum class for books type
    """

    PAPER = "Paper"
    ELECTRONIC = "Electronic"


class BookGenre(StrEnum):
    """
    Enum class for books genre
    """

    MYSTERY = "Mystery"
    THRILLER = "Thriller"
    HORROR = "Horror"
    HISTORICAL = "Historical"
    ROMANCE = "Romance"
    FANTASY = "Fantasy"
    SCI_FI = "Science Fiction"


class BookBase(BaseModel):
    """
    BookBase schema describes basic book by title, description, year, image_file,
    pages, genre and type
    """

    title: str
    description: Union[str, None] = None
    year: int
    image_file: Union[str, None] = None
    pages: int
    genre: BookGenre
    type: BookType

    @validator("year")
    @classmethod
    def year_validation(cls, value):
        """checks if year is valid"""
        if value > 2022:
            raise ValueError("The year cannot be greater than the current one")
        if value < 1450:
            raise ValueError("The year cannot be lower than 1450")
        return value

    @validator("pages")
    @classmethod
    def pages_validation(cls, value):
        """check if number of pages is valid"""
        if value < 15:
            raise ValueError("There cannot be less than 15 pages")
        return value


class BookCreate(BookBase):
    """
    BookCreate schema to create book with title, description, year, image_file,
    pages, genre, type and list of authors id
    """

    author_id: List[int] = []


class BookUpdate(BookBase):
    """
    BookCreate schema to update book with title, description, year, image_file,
    pages, genre, type and list of authors id
    """

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
    """
    Book schema to show book with its id, title, description, year, image_file,
    pages, genre, type, list of authors and list of reviews
    """

    id: int
    rating: float
    authors: List[Author] = []
    reviews: List[Review] = []

    class Config:
        """config class for book"""

        orm_mode = True
