from contextlib import contextmanager

from sqlalchemy.orm import Session

from app.database.db import SessionLocal


@contextmanager
def get_db_session_context() -> Session:
    """
    Generator object for DB connection

    :return: Session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
