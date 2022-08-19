from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.database import db_helper
from app.models.user import User
from app.schemas.user import AuthUser, UserCreate
from app.utils import password

from app.database.database import get_db

router = APIRouter(prefix='/users')


@router.get('/')
def get_all_users(response: Response, db: Session = Depends(get_db)):
    result = db_helper.get_users(db)
    return result


@router.post('/')
def create_user(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    # TODO: hash password
    fake_hashed_password = password.generate_password(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=fake_hashed_password,
        user_type='admin'
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    

@router.get('/{email}')
def get_user(email: str, response: Response, db: Session = Depends(get_db)):
    result = db_helper.get_user_by_email(db, email)
    if result:
        return result
    response.status_code = status.HTTP_404_NOT_FOUND
    return {'message': 'Not found'}


@router.post('/authenticate')
def authenticate_user(auth: AuthUser, response: Response, db: Session = Depends(get_db)):
    user = db_helper.get_user_by_username(db, auth.username)
    if not user:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': f'No account found with username - {auth.username}'}
    if password.check_password(auth.password, user.hashed_password):
        response.status_code = status.HTTP_200_OK
        return {'access_token': 'newbearertoken'}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {'message': 'Not authorized'}