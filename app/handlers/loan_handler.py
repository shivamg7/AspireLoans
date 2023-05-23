import datetime
import logging
from datetime import timedelta
from typing import List

from fastapi import HTTPException
from starlette import status

from app.database import models
from app.database.crud import CrudMixin
from app.database.dependencies import get_db_session_context
from app.database.models import LoanStatus
from app.models.schema import Loan


logger = logging.getLogger()


def create_loan(username: str, loan: Loan) -> None:
    """
    Create a loan record in DB.

    Create payment records as well setting status to default pending.
    :param username: current user
    :param loan: loan object
    :return:
    """
    with get_db_session_context() as db:
        try:
            user = CrudMixin.get_user(db=db, username=username)
            loan_db = models.Loan(user=user, amount=loan.amount, tenure=loan.tenure)
            db.add(loan_db)
            # Flush the session to make the loan id available
            db.flush()
            db.refresh(loan_db)
            payment_list = get_payment_list(loan=loan)
            for payment in payment_list:
                payment.loan = loan_db
                db.add(payment)
            db.commit()
        except Exception as e:
            logger.error(e)
            db.rollback()
            raise HTTPException(status_code=500, detail="something went wrong")


def approve_loan(loan_id: int) -> None:
    """
    Approve a loan record in DB.

    :param loan_id:
    :return:
    """
    with get_db_session_context() as db:
        try:
            loan = CrudMixin.get_loan(db=db, loan_id=loan_id)
            if not loan:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="loan not found")
            loan.status = LoanStatus.approved
            db.add(loan)
            db.commit()
        except Exception as e:
            logger.error(e)
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="something went wrong")


def make_payment(loan_id: int, schedule: str) -> None:
    """

    :param loan_id:
    :param schedule:
    :return:
    """
    with get_db_session_context() as db:
        try:
            loan_payment = CrudMixin.get_loan_payment(db, loan_id, schedule)
            loan_payment.status = models.PaymentStatus.paid
            db.add(loan_payment)
            db.flush()
            pending_payments = CrudMixin.get_pending_payments(db, loan_id)
            if not pending_payments:
                loan = CrudMixin.get_loan(db, loan_id)
                loan.status = LoanStatus.paid
                db.add(loan)

            db.commit()
        except Exception as e:
            logger.error(e)
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="something went wrong")


def view_loan(loan_id: int) -> models.Loan:
    """

    :param loan_id:
    :return:
    """
    with get_db_session_context() as db:
        loan = CrudMixin.get_loan(db, loan_id)
        # Making reference to related objects so that they are loaded
        if loan:
            _, _ = loan.user, loan.loan_payments
        return loan


def get_loans(username: str) -> List[models.Loan]:
    """
    Get all loans for the user

    :param username: username
    :return: List[Loan]
    """
    with get_db_session_context() as db:
        loans = CrudMixin.get_loans(db, username)
        _ = [loan.loan_payments for loan in loans]
        return loans


def get_payment_list(loan: Loan) -> List[models.LoanPayment]:
    """
    Utility method to get the payments models for creating a loan.

    :param loan: Loan
    :return: List[models.LoanPayment]
    """
    per_payment = round(loan.amount/loan.tenure, 2)
    today = datetime.date.today()
    payments = []
    for i in range(0, loan.tenure):
        payments.append(
            models.LoanPayment(
                amount=per_payment,
                payment_schedule=today + timedelta(days=7*(i+1))
            )
        )
    return payments
