from typing import List

from sqlalchemy.orm import Session

from app.database import models
from app.database.models import User, Loan


class CrudMixin:

    @staticmethod
    def get_user(db: Session, username: str) -> User:
        return db.query(models.User).filter(models.User.username == username).first()

    @staticmethod
    def create_user(db: Session, username: str, hashed_password: str) -> None:
        db_user = models.User(username=username, hashed_password=hashed_password)
        db.add(db_user)

    @staticmethod
    def create_loan(db: Session, username: str, amount: float, tenure: int) -> None:
        user = CrudMixin.get_user(db, username)
        db_loan = models.Loan(user=user, amount=amount, tenure=tenure)
        db.add(db_loan)

    @staticmethod
    def get_loan(db: Session, loan_id: int) -> models.Loan:
        loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
        return loan

    @staticmethod
    def get_loans(db: Session, username: str) -> List[Loan]:
        user = CrudMixin.get_user(db, username)
        db_loans = db.query(models.Loan).filter(models.Loan.user == user).all()
        return db_loans