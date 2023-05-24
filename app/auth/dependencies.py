from typing import Annotated

from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from starlette import status

from app.auth.auth import ALGORITHM, SECRET_KEY, get_user, oauth2_scheme
from app.models.models import TokenData


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Authentication dependency to authentication and fetch the current logged in user

    :param token:
    :return:
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
