from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel


class ReviewBase(BaseModel):
    username: str
    text: str
    rating: int
    book_id: int


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(ReviewBase):
    username: Union[str, None] = None
    text: Union[str, None] = None
    rating: Union[int, None] = None
    book_id: Union[int, None] = None


class Review(ReviewBase):
    id: int
    created_at: datetime

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


class BookBase(BaseModel):
    title: str
    description: str
    year: int
    image_file: Optional[str] = None
    pages: int
    genre: str
    type: str


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
    genre: Union[str, None] = None
    type: Union[str, None] = None


class Book(BookBase):
    id: int
    authors: List[Author] = []
    reviews: List[Review] = []

    class Config:
        orm_mode = True
