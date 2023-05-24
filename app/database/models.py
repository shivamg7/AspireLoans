import enum

from sqlalchemy import (Column, DateTime, Enum, Float, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship

from app.database.db import Base


class LoanStatus(enum.Enum):
    """Status for Loan"""
    approved = "approved"
    pending = "pending"
    paid = "paid"


class PaymentStatus(enum.Enum):
    """Status for individual loan payments"""
    pending = "pending"
    paid = "paid"


class User(Base):
    """
    Model for user
    """

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)

    loans = relationship("Loan", back_populates="user")

    __tablename__ = "user"


class Loan(Base):
    """
    Model for Loan
    """

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    amount = Column(Float)
    tenure = Column(Integer)
    status = Column(Enum(LoanStatus), default=LoanStatus.pending)

    user = relationship("User", back_populates="loans")

    loan_payments = relationship("LoanPayment", back_populates="loan")

    __tablename__ = "loan"


class LoanPayment(Base):
    """
    Model for Loan payment schedule
    """

    id = Column(Integer, primary_key=True)
    loan_id = Column(
        Integer, ForeignKey("loan.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    amount = Column(Float)
    payment_schedule = Column(DateTime)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)

    loan = relationship("Loan", back_populates="loan_payments")

    __tablename__ = "loan_payment"
