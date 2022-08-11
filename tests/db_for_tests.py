from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from project.database import Base
from project.database import DB_HOST
from project.database import DB_PASS
from project.database import DB_PORT
from project.database import DB_USER
from project.database import get_db


DB_NAME = "edvantis_project_test"

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    """database generator"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
