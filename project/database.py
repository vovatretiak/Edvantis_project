import os

from dotenv import find_dotenv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv(find_dotenv())

DB_USER = "postgres"
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = "db"
DB_PORT = "5432"
DB_NAME = "edvantis_project"

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """database generator"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
