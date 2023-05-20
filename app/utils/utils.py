import hashlib
import uuid

from app.database.fake_db import fake_users_db


def get_hashed_password(plain_text_password: str) -> str:
    """
    Get hashed password from plain text hash.

    :param plain_text_password:
    :return:
    """
    hashed_password = hashlib.sha512(plain_text_password.encode()).hexdigest()
    return hashed_password


def check_password(plain_text_password: str, hashed_password: str) -> bool:
    """
    Check if passwords are same.

    :param plain_text_password:
    :param hashed_password:
    :return:
    """
    plain_password_hashed = get_hashed_password(plain_text_password=plain_text_password)
    return hashed_password == plain_password_hashed


def create_user(username: str, password: str) -> None:
    """

    :param username:
    :param password:
    :return:
    """
    fake_users_db[username] = {
        "username": username,
        "hashed_password": get_hashed_password(password)
    }
