from contextlib import contextmanager

from sqlalchemy.orm import Session

from app.database.db import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session_context() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
