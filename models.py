
from sqlalchemy import Column, Integer, String, ARRAY
from database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    descrition = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    isbn = Column(String, nullable=False)
    image_file = Column(String)
    pages = Column(Integer, nullable=False)
    author = Column(ARRAY(String), nullable=False)
    genre = Column(String, nullable=False)
    type = Column(String, nullable=False)
    reviews = Column(ARRAY(String), nullable=True)
