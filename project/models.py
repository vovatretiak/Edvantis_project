
from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base


AuthorBook = Table("author_book", Base.metadata,
                   Column("book_id", Integer, ForeignKey("books.id")),
                   Column("author_id", Integer, ForeignKey("authors.id")))

# https://stackoverflow.com/questions/68394091/fastapi-sqlalchemy-pydantic-%E2%86%92-how-to-process-many-to-many-relations


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

    authors = relationship(
        'Author', secondary=AuthorBook,
        back_populates='books'
    )

    def __repr__(self) -> str:
        return f"Book(id={self.id}, title={self.title})"


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    image_file = Column(String)

    books = relationship(
        'Book', secondary=AuthorBook,
        back_populates='authors',
        cascade='all, delete',
    )

    def __repr__(self) -> str:
        return f"Author(id={self.id}, first_name={self.first_name})"
