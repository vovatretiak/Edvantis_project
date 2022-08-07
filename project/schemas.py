from typing import Union

from pydantic import BaseModel


class Token(BaseModel):
    """
    Token schema describes the token and its type
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    TokenData schema describes the data from token
    """

    username: Union[str, None] = None
