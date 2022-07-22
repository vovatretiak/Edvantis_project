from typing import List, Optional, Union

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    description: str
    year: int
    image_file: Optional[str] = None
    pages: int
    author: List[str]
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
    author: Union[List[str], None] = None
    genre: Union[str, None] = None
    type: Union[str, None] = None


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True
