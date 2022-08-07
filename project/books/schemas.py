from typing import List
from typing import Union

from pydantic import BaseModel
from pydantic import validator
from strenum import StrEnum

from project.authors.schemas import Author
from project.reviews.schemas import Review


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
