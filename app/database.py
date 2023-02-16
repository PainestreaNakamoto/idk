from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

SQL_URL = "sqlite:///./sqlite.db"
engine = create_engine(SQL_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False , autoflush=False,bind=engine)
Base = declarative_base()

def get_db():
    try:
        db = SessionLocal()
        yield db

    finally:
        db.close()
