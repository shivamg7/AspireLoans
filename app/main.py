import datetime
import logging
from datetime import timedelta
from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    init_fake_users_db
from app.auth.dependencies import get_current_user
from app.database import models
from app.database.crud import CrudMixin
from app.database.db import engine
from app.database.dependencies import get_db
from app.database.models import LoanStatus
from app.handlers import loan_handler
from app.models.models import Token, User
from app.models.schema import Loan, LoanResponse

backend = FastAPI()
models.Base.metadata.create_all(bind=engine)
init_fake_users_db()


@backend.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@backend.post("/loan")
async def create_loan(
    loan_body: Loan, current_user: Annotated[User, Depends(get_current_user)]
):
    loan_handler.create_loan(current_user.username, loan=loan_body)
    return {"message": "loan created"}


@backend.get("/loans", response_model=List[LoanResponse])
async def view_loans(
    current_user: Annotated[User, Depends(get_current_user)]
):
    loans = loan_handler.get_loans(current_user.username)
    if not loans:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="loan does not exist"
        )
    return [{"loan_id": loan.id, "amount": loan.amount, "tenure": loan.tenure} for loan in loans]


@backend.patch("/loan/{loan_id}/approve")
async def approve_loan(loan_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.username != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="only admin authorized"
        )

    db_loan = loan_handler.view_loan(loan_id)
    if not db_loan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="loan does not exist"
        )

    if db_loan.status in [LoanStatus.approved, LoanStatus.paid]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": f"loan is already {db_loan.status.value}"}
        )

    loan_handler.approve_loan(loan_id)

    return {
        "message": "loan approved"
    }


@backend.post("/loan/{loan_id}/payment")
async def make_loan_payment(loan_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    """

    :param loan_id:
    :param current_user:
    :return:
    """
    db_loan = loan_handler.view_loan(loan_id)
    if not db_loan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="loan does not exist"
        )

    if db_loan.status != LoanStatus.approved:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": f"loan is not approved"}
        )