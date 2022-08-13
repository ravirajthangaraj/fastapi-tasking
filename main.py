
from fastapi import Depends, FastAPI
import uvicorn
from database import db_helper
from models.user import Base, User
from database.database import session_local, engine
from sqlalchemy.orm import Session
from schemas.user import UserCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def root():
    return {'message': 'Welcome to FastAPI Tasking'}


@app.get('/users')
def get_all_users(db: Session = Depends(get_db)):
    result = db_helper.get_users(db)
    return result


@app.get('/users/{email}')
def get_user(email: str, db: Session = Depends(get_db)):
    result = db_helper.get_user_by_email(db, email)
    return result


@app.post('/users')
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    fake_hashed_password = user.password + "notreallyhashed"
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


"""for development and debugging"""
# if __name__ == '__main__':
#     uvicorn.run(app, host="127.0.0.1", port="8000")
