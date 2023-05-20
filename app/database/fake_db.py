import os

from app.utils.utils import get_hashed_password

fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": get_hashed_password(os.getenv("ADMIN_PASSWORD"))
    }
}