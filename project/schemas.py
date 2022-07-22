from typing import List, Optional, Union

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    description: str
    year: int
    image_file: Optional[str] = None
    pages: int
    # author_id: List[int]
    genre: str
    type: str
    reviews: Optional[List[str]] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    title: Union[str, None] = None
    description: Union[str, None] = None
    year: Union[int, None] = None
    image_file: Union[str, None] = None
    pages: Union[int, None] = None
    # author_id: Union[List[int], None] = None
    genre: Union[str, None] = None
    type: Union[str, None] = None


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    image_file: Optional[str] = None
    books_id: List[int]


class BookCreate(BookBase):
    pass
