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
    return encoded_jwt
