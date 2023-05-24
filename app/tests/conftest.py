from typing import Dict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.database.dependencies import get_db_session_context
from app.main import backend

client = TestClient(backend)


@pytest.fixture(scope="module")
def login_headers() -> Dict:
    response = client.post("/token", data={
        "username": "admin",
        "password": "password"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="module")
def login_headers_user() -> Dict:
    response = client.post("/token", data={
        "username": "shivam",
        "password": "Aspire@123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function", autouse=True)
def clean_db() -> None:
    with get_db_session_context() as db:
        db.execute(text("DELETE FROM loan CASCADE;COMMIT;"))
