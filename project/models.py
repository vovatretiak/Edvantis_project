
from sqlalchemy import ARRAY, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

AuthorBook = Table("author_book", Base.metadata,
                   Column("book_id", Integer, ForeignKey("books.id")),
                   Column("author_id", Integer, ForeignKey("authors.id")))


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    year = Column(Integer, nullable=False)
    image_file = Column(String)
    pages = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    type = Column(String, nullable=False)
    reviews = Column(ARRAY(String), nullable=True)
    authors_id = Column(ARRAY(Integer))

    def __repr__(self) -> str:
        return f"Book(id={self.id}, title={self.title})"


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    image_file = Column(String)

    books = relationship('Book', secondary=AuthorBook)

    def __repr__(self) -> str:
        return f"Author(id={self.id}, first_name={self.first_name})"
