from typing import List
from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine

import crud
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/books/", response_model=List[schemas.Book])
def get_all_books(db: Session = Depends(get_db)):
    return crud.get_books(db=db)


@app.post("/books/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
