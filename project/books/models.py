from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from project.authors.models import AuthorBook
from project.database import Base


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
    rating = Column(Float(decimal_return_scale=2), default=0)
    pages = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    type = Column(String, nullable=False)

    reviews = relationship("Review", back_populates="book", cascade="all, delete")
    authors = relationship("Author", secondary=AuthorBook, back_populates="books")

    def __repr__(self) -> str:
        return f"Book(id={self.id}, title={self.title}, \
             year={self.year}, genre={self.genre}, type={self.type})"

    def __str__(self) -> str:
        return str(self.__dict__)
