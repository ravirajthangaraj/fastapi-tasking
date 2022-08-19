import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "mongodb://mongoadmin:supersecret@127.0.0.1:27017/test"
DATABASE_URL = "sqlite:///./tasking.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': True}
)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

"""Create tables"""
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(e)


# Dependency
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()