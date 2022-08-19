from pydantic import BaseModel


class UserDetail(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str


class AuthUser(BaseModel):
    username: str
    password: str