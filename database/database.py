import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "mongodb://mongoadmin:supersecret@127.0.0.1:27017/test"
DATABASE_URL = "sqlite:///./tasking.db"

engine = create_engine(
    DATABASE_URL
)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()