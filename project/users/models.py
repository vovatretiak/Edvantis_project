from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from project.database import Base


class User(Base):
    """
    Users table contains main information about users
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    rank = Column(String, nullable=False, default="9 kyu")

    reviews = relationship("Review", back_populates="user", cascade="all, delete")

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, email={self.email})"

    def __str__(self) -> str:
        return str(self.__dict__)
