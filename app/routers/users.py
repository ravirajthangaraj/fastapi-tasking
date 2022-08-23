import datetime

from fastapi import APIRouter, Depends, Response, status
from app.database.mongo import db
from app.schemas.user import AuthUser, UserCreate
from app.utils import password
from app.utils.response import convert_time_zone, modify_object_id


router = APIRouter(prefix='/users')


@router.get('/')
def get_all_users(response: Response):
    users_list = list()
    try:
        result = db.get('users', {}, exclude_fields={'hashed_password': 0})
        for res in result:
            users_list.append(res)
    except Exception as e:
        print(f'{e}')
    return users_list


@router.post('/')
def create_user(user: UserCreate, response: Response):
    # TODO: hash password
    fake_hashed_password = password.generate_password(user.password)
    db_user = {
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "hashed_password": fake_hashed_password,
        "is_active": True,
        "user_type": 'admin',
        "last_login": datetime.datetime.utcnow()
    }
    user_created = db.create('users', db_user)
    if user_created:
        return db.retrieve('users', {'email': user.email})
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {'message': 'Bad Request'}


@router.get('/{email}')
def get_user(email: str, response: Response):
    result = db.retrieve('users', {'email': email}, exclude_fields={'hashed_password': 0})
    if result:
        return result
    response.status_code = status.HTTP_404_NOT_FOUND
    return {'message': 'Not found'}
