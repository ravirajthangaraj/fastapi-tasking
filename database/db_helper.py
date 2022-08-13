from sqlalchemy.orm import Session


from models import user


def get_user_by_username(db: Session, username: str):
    return db.query(user.User).filter(user.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(user.User).filter(user.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 50):
    return db.query(user.User).offset(skip).limit(limit).all()
