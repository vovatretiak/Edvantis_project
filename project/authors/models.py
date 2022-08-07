from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from project.database import Base


AuthorBook = Table(
    "author_book",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id")),
    Column("author_id", Integer, ForeignKey("authors.id")),
)

# https://stackoverflow.com/questions/68394091/fastapi-sqlalchemy-pydantic-%E2%86%92-how-to-process-many-to-many-relations


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
