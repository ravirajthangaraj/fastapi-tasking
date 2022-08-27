import datetime
from typing import List

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse
from app.database.mongo import db
from app.schemas.user import AuthenticateUser, UserCreate, UserAuthenticated
from app.utils import password
from app.schemas.user import user_entity, users_entity, UserDetail
from app.utils.password import create_access_token, JWTBearerAuthenticate

router = APIRouter(prefix='/users')


@router.get('/', response_model=List[UserDetail], dependencies=[Depends(JWTBearerAuthenticate())])
def get_all_users(response: Response):
    users_list = list()
    try:
        result = db.get('users', {})
        return users_entity(result)
    except Exception as e:
        print(f'{e}')
    return users_list


@router.post('/signup/', response_model=UserDetail)
def create_user(user: UserCreate, response: Response):
    # check if user already exists with email
    if db.retrieve('users', {'email': user.email}):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': 'Email already exists'}

    # check if user already exists with username
    if db.retrieve('users', {'username': user.username}):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': 'Username already exists'}

    hashed_password = password.generate_password(user.password)
    db_user = {
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "hashed_password": hashed_password,
        "is_active": True,
        "user_type": 'admin',
        "last_login": datetime.datetime.utcnow()
    }
    user_created = db.create('users', db_user)
    if user_created:
        return user_entity(db.retrieve('users', {'email': user.email}))
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {'message': 'Bad Request'}


@router.post('/authenticate/', response_model=UserAuthenticated, responses={400: {'model': dict}})
def authenticate_user(auth: AuthenticateUser, response: Response):
    user = db.retrieve('users', {'username': auth.username})
    if not user:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Username/Password invalid"})

    if not password.check_password(auth.password, user.get('hashed_password')):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Username/Password invalid"})

    user = user_entity(user)
    jwt_token = create_access_token(user)
    response.body = {'access_token': str(jwt_token)}
    # response.body.update({'access_token': str(jwt_token)})
    return response.body


@router.get('/{email}/', response_model=UserDetail, responses={404: {'model': dict}}, dependencies=[Depends(JWTBearerAuthenticate())])
def get_user(email: str, response: Response):
    result = db.retrieve('users', {'email': email})
    if result:
        return user_entity(result)
    response.status_code = status.HTTP_404_NOT_FOUND
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not found"})
