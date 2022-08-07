import os
from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Union

from dotenv import find_dotenv
from dotenv import load_dotenv
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import database
from . import models
from . import schemas


load_dotenv(find_dotenv())

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """verify password

    Args:
        plain_password (str): password to check
        hashed_password (str): hashed password from db

    Returns:
        bool: returns true or false
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """gets hashed password

    Args:
        password (str): user password

    Returns:
        str: hashed password
    """
    return pwd_context.hash(password)


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]  # secrets.token_hex(30)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    """creates access token

    Args:
        subject (Union[str, Any]): data from the authorization form
        expires_delta (int, optional): time delta. Defaults to None.

    Returns:
        str: JWT
    """
    if expires_delta:
        expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def get_current_user(
    db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)
) -> models.User:
    """gets current user from database if credentials is valid

    Args:
        db (Session, optional): Defaults to Depends(database.get_db).
        token (str, optional): Defaults to Depends(oauth2_scheme).

    Raises:
        credentials_exception: Handle wrong credentials

    Returns:
        models.User: returns current user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        return credentials_exception
    user = (
        db.query(models.User)
        .filter(models.User.username == token_data.username)
        .first()
    )
    if user is None:
        raise credentials_exception
    return user


def get_user_rank(reviews_number: int):
    """_summary_

    Args:
        reviews_number (int)

    Returns:
       user rank
    """
    if reviews_number < 5:
        return schemas.UserRank.KYU_9
    elif reviews_number < 10:
        return schemas.UserRank.KYU_8
    elif reviews_number < 20:
        return schemas.UserRank.KYU_7
    elif reviews_number < 30:
        return schemas.UserRank.KYU_6
    elif reviews_number < 40:
        return schemas.UserRank.KYU_5
    elif reviews_number < 50:
        return schemas.UserRank.KYU_4
    elif reviews_number < 60:
        return schemas.UserRank.KYU_3
    elif reviews_number < 70:
        return schemas.UserRank.KYU_2
    elif reviews_number < 90:
        return schemas.UserRank.KYU_1
    elif reviews_number > 100:
        return schemas.UserRank.DAN_1
