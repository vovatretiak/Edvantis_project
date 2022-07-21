from enum import Enum
from typing import List, Optional

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


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True
