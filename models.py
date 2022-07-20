from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class BookGenres(str, Enum):
    action_and_adventure = "Action and adventure"
    biography = "Biography"
    classic = "Classic"
    comic_book = 'Comic book'
    drama = 'Drama'
    horror = 'Horror'
    poetry = "Poetry"
    romance = "Romance"
    science = "Science"
    thriller = 'Thriller'


class BookType(str, Enum):
    paper = 'Paper'
    electronic = "Electronic"


class Book(BaseModel):
    title: str
    description: str
    year: int
    ISBN: str
    pages: int
    category: str
    author: List[str]
    genre: BookGenres
    type: BookType
    reviews: Optional[List[str]] = None
