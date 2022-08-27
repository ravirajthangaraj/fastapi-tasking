import time

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, status

import settings
from passlib.context import CryptContext
import datetime
from typing import Union
from jose import jwt

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


password_context = CryptContext(schemes=["bcrypt"])


def generate_password(password_string: str) -> str:
    return password_context.hash(password_string)


def check_password(password_string: str, hashed_password: str) -> bool:
    if password_context.verify(password_string, hashed_password):
        return True
    return False


def create_access_token(user: dict, expires_delta: Union[datetime.timedelta, None] = None):
    to_encode = user.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return str(encoded_jwt)


def verify_jwt(token: str) -> bool:
    is_token_valid: bool = False
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        payload = decoded_token if decoded_token["exp"] >= time.time() else None
    except Exception as e:
        print(e)
        payload = None
    if payload:
        is_token_valid = True
    return is_token_valid


class JWTBearerAuthenticate(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearerAuthenticate, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearerAuthenticate, self).__call__(request)
        if not credentials:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code")

        if not credentials.scheme == 'Bearer':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization scheme")

        if not verify_jwt(credentials.credentials):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization required")

        return credentials.credentials
