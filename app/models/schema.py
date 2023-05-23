import datetime
from typing import Any, List

from pydantic import BaseModel, validator
from pydantic.datetime_parse import get_numeric, parse_date


def validate_date(v: Any) -> datetime.date:
    return parse_date(v)


class StrictDate(datetime.date):
    @classmethod
    def __get_validators__(cls):
        yield validate_date


class Loan(BaseModel):
    """Pydantic model for Loan request body"""

    amount: float
    tenure: int

    @validator("amount")
    def validate_amount(cls, amount):
        if amount <= 0:
            raise ValueError("amount must be greater than zero")
        return amount

    @validator("tenure")
    def validate_tenure(cls, tenure):
        if tenure <= 0:
            raise ValueError("tenure must be greater than zero")

        if tenure > 36:
            raise ValueError("tenure must be less than 36 months")
        return tenure


class LoanPaymentResponse(BaseModel):
    """"""

    amount: float
    schedule: str
    status: str


class LoanResponse(BaseModel):
    """Pydantic model for Loan response body"""

    amount: float
    tenure: int
    loan_id: int
    status: str
    payments: List[LoanPaymentResponse]


class LoanPaymentRequest(BaseModel):
    """"""

    amount: float
    schedule: StrictDate
