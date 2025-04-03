from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from models import Base
from contextlib import contextmanager


DATABASE_URL = "sqlite:///./event.db" 
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()