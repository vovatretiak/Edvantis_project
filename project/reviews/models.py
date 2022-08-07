from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from project.database import Base


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
