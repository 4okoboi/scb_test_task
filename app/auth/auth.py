from app.auth.DAL import UserDAL
from app.auth.models import User as UserModel
from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from app.utils.auth.hashing import Hasher

from fastapi import Depends, HTTPException
from starlette import status

from typing import Union
from config import ALGORITHM, SECRET_AUTH_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


async def _get_user_by_email_for_auth(
    email: str,
    session: AsyncSession
) -> Union[UserModel, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_email(email=email)
        return user


async def authenticate_user(
    email: str,
    password: str,
    session: AsyncSession
) -> Union[UserModel, None]:
    user = await _get_user_by_email_for_auth(email=email, session=session)
    if user is None:
        return
    if not Hasher.verify_password(password, user.hashed_password):
        return
    return user


async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session)
) -> UserModel:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials."
    )
    try:
        payload = jwt.decode(
            token,
            SECRET_AUTH_KEY,
            algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    user = await _get_user_by_email_for_auth(email=email, session=session)
    if user is None:
        raise credential_exception
    return user

async def check_token_expire(
    token: str
) -> bool:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token was expired"
    )
    try:
        payload = jwt.decode(
            token,
            SECRET_AUTH_KEY,
            algorithms=[ALGORITHM]
        )
    except ExpiredSignatureError:
        raise credential_exception
    return True