import os
from datetime import timedelta, datetime
from typing import Union, Annotated, Dict

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status

from app.database.fake_db import fake_users_db
from app.models.models import UserInDB, TokenData, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_hashed_password(plain_text_password: str) -> str:
    """
    Get hashed password from plain text hash.

    :param plain_text_password:
    :return:
    """
    return pwd_context.hash(plain_text_password)


def verify_password(plain_text_password: str, hashed_password: str) -> bool:
    """
    Check if passwords are same.

    :param plain_text_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_text_password, hashed_password)


def get_user(db, username: str):
    if username in db.db:
        user_dict = db.db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_user(username: str, password: str) -> None:
    """

    :param username:
    :param password:
    :return:
    """
    fake_users_db.db[username] = {
        "username": username,
        "hashed_password": get_hashed_password(password)
    }


def init_fake_users_db() -> None:
    """
    Initializer for Users database

    :return:
    """
    create_user("admin", os.getenv("ADMIN_PASSWORD") or "password")
    create_user("shivam", "Aspire@123")
    create_user("testuser", "Aspire@123")
