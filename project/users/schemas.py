from typing import List
from typing import Union

from pydantic import BaseModel
from pydantic import root_validator
from pydantic import validator
from strenum import StrEnum

from project.reviews.schemas import Review


class UserRank(StrEnum):
    """
    Enum class for user rank
    """

    KYU_9 = "9 kyu"
    KYU_8 = "8 kyu"
    KYU_7 = "7 kyu"
    KYU_6 = "6 kyu"
    KYU_5 = "5 kyu"
    KYU_4 = "4 kyu"
    KYU_3 = "3 kyu"
    KYU_2 = "2 kyu"
    KYU_1 = "1 kyu"
    DAN_1 = "1 dan"


class UserBase(BaseModel):
    """
    UserBase schema describes basic user by username, text, email and password
    """

    username: str
    email: str
    password: str

    @validator("username")
    def username_alphanumeric(cls, username):
        """checks if username is alphanumeric"""
        assert username.isalnum(), "must be alphanumeric"
        return username


class UserCreate(UserBase):
    """
    UserCreate schema to create user with username, text, email, password and confirm_password
    """

    confirm_password: str

    @root_validator
    def passwords_match(cls, values):
        """checks if the password and the confirm_password match"""
        pw1, pw2 = values.get("password"), values.get("confirm_password")
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        return values


class UserUpdate(UserBase):
    """
    UserUpdate schema to update user with username, text, email, password and confirm_password
    """

    username: Union[str, None] = None
    email: Union[str, None] = None
    password: Union[str, None] = None
    confirm_password: Union[str, None] = None

    @root_validator
    def passwords_match(cls, values):
        """checks if the password and the confirm_password match"""
        pw1, pw2 = values.get("password", None), values.get("confirm_password", None)
        if pw1 is not None and pw2 is not None and pw1 == pw2:
            return values
        raise ValueError("passwords do not match")


class User(UserBase):
    """
    User schema to show user with its id, username, text, email, password and list of reviews
    """

    id: int
    rank: UserRank
    reviews: List[Review] = []

    class Config:
        """config class for user"""

        orm_mode = True
