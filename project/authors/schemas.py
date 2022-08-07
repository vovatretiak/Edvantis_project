from typing import Union

from pydantic import BaseModel


class AuthorBase(BaseModel):
    """
    AuthorBase schema describes basic author by first_name, last_name, middle_name and image_file
    """

    first_name: Union[str, None]
    last_name: Union[str, None]
    middle_name: Union[str, None]
    image_file: Union[str, None] = None


class AuthorCreate(AuthorBase):
    """
    AuthorCreate schema to create author with first_name, last_name, middle_name and image_file
    """


class AuthorUpdate(BaseModel):
    """
    AuthorUpdate schema to update author with first_name, last_name, middle_name and image_file
    """

    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    middle_name: Union[str, None] = None
    image_file: Union[str, None] = None


class Author(AuthorBase):
    """
    Author schema to show author with its id, first_name, last_name, middle_name and image_file
    """

    id: int

    class Config:
        """config class for user"""

        orm_mode = True
