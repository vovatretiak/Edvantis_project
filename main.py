from typing import List

from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session

from project import crud, models, schemas
from project.database import SessionLocal, engine
from project.routers import books

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(books.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
