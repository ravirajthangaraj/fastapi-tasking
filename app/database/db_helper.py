
from sqlalchemy.orm import Session
from app.schemas.user import UserDetail


from app.models import user


def get_user_by_username(db: Session, username: str) -> UserDetail:
    return db.query(user.User).filter(user.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> UserDetail:
    return db.query(user.User).filter(user.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 50):
    return db.query(user.User).offset(skip).limit(limit).all()
