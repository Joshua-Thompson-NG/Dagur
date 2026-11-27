import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

sqlite_url = os.getenv("DATABASE_URL", "sqlite:///./dagur.db")

engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

class Base(DeclarativeBase):
    pass