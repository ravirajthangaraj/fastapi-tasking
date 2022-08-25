from pydantic import BaseModel


def user_entity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "fuid": item["fuid"],
        "username": item["username"],
        "email": item["email"],
        "first_name": item["first_name"],
        "last_name": item["last_name"],
        "last_login": str(item["last_login"]),
    }


def users_entity(users) -> list:
    return [user_entity(item) for item in users]


class UserDetail(BaseModel):
    id: str
    fuid: str
    username: str
    email: str
    first_name: str
    last_name: str
    last_login: str


class UserCreate(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str


class AuthenticateUser(BaseModel):
    username: str
    password: str
