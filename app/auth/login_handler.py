from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session

from app.utils.auth.security import create_access_token
from app.auth import schemas
from config import ACCESS_TOKEN_EXPIRE_MINUTES

from app.auth.auth import authenticate_user, check_token_expire

login_router = APIRouter()

@login_router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session)
) -> schemas.Token:
    user = await authenticate_user(email=form_data.username, password=form_data.password, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@login_router.post("/check_token", response_model=bool)
async def check_login_token(
    data: schemas.CheckToken,
    session: AsyncSession = Depends(get_async_session)
) -> bool:
    return await check_token_expire(data.access_token)
