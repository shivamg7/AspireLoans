from typing import Union, Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.database.fake_db import fake_users_db
from app.models.models import UserInDB
from app.utils.utils import create_user, get_hashed_password

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def decode_token(token: str) -> str:


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/loan/")
def read_loans(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@app.post("/loan/")
def create_loan(token: Annotated[str, Depends(oauth2_scheme)]):
    return {}


@app.post("/loan/{load_id}/approve")
def approve_load(item_id: int, token: Annotated[str, Depends(oauth2_scheme)]):
    return {}


@app.post("/loan/{loan_id}/payment")
def create_load_payment(load_id: int, token: Annotated[str, Depends(oauth2_scheme)]):
    return {}


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@app.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Login endpoint for app

    :param form_data:
    :return:
    """
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        create_user(username=form_data.username, password=form_data.password)
        return {"access_token": form_data.username, "token_type": "Bearer"}

    user = UserInDB(**user_dict)
    hashed_password = get_hashed_password(form_data.password)

    if hashed_password != user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect password")

    return {"access_token": user.username, "token_type": "Bearer"}

