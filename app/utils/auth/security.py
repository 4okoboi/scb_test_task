from datetime import datetime, timedelta

from typing import Optional

from jose import jwt

from config import SECRET_AUTH_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update(
        {"exp": expire}
    )
    encoded_jwt = jwt.encode(
        to_encode, SECRET_AUTH_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt