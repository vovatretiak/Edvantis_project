from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from .database import Base


AuthorBook = Table(
    "author_book",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id")),
    Column("author_id", Integer, ForeignKey("authors.id")),
)

# https://stackoverflow.com/questions/68394091/fastapi-sqlalchemy-pydantic-%E2%86%92-how-to-process-many-to-many-relations


class Book(Base):
    """
    Books table contains main information about books
    """

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    year = Column(Integer, nullable=False)
    image_file = Column(String)
    pages = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    type = Column(String, nullable=False)

    reviews = relationship("Review", back_populates="book", cascade="all, delete")
    authors = relationship("Author", secondary=AuthorBook, back_populates="books")

    def __repr__(self) -> str:
        return f"Book(id={self.id}, title={self.title}, year={self.year}, genre={self.genre}, type={self.type})"

    def __str__(self) -> str:
        return str(self.__dict__)


class Author(Base):
    """
    Authors table contains main information about authors
    """

    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    image_file = Column(String)

    books = relationship(
        "Book", secondary=AuthorBook, back_populates="authors", cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"Author(id={self.id}, first_name={self.first_name})"

    def __str__(self) -> str:
        return str(self.__dict__)


class Review(Base):
    """
    Reviews table contains main information about reviews
    """

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    book_id = Column(Integer, ForeignKey("books.id"))

    book = relationship("Book", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    def __repr__(self) -> str:
        return f"Review(id={self.id}, user_id={self.user_id}, created_at={self.created_at})"

    def __str__(self) -> str:
        return str(self.__dict__)


class User(Base):
    """
    Users table contains main information about users
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    reviews = relationship("Review", back_populates="user", cascade="all, delete")

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, email={self.email})"

    def __str__(self) -> str:
        return str(self.__dict__)
