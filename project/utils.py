import os
from datetime import datetime, timedelta
from typing import Any, Union

from dotenv import find_dotenv, load_dotenv
from jose import jwt
from passlib.context import CryptContext

load_dotenv(find_dotenv())

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]  # secrets.token_hex(30)


def create_access_token(subject: Union[str, Any], expires_delta: int = None):
    if expires_delta:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt
