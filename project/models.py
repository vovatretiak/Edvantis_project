
from sqlalchemy import ARRAY, Column, Integer, String

from .database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    year = Column(Integer, nullable=False)
    image_file = Column(String)
    pages = Column(Integer, nullable=False)
    author = Column(ARRAY(String), nullable=False)
    genre = Column(String, nullable=False)
    type = Column(String, nullable=False)
    reviews = Column(ARRAY(String), nullable=True)

    def __repr__(self) -> str:
        return f"Book(id={self.id}, title={self.title})"
