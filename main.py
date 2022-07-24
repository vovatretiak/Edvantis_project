from fastapi import FastAPI

from project import models
from project.database import engine
from project.routers import authors, books, reviews

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(authors.router)
app.include_router(books.router)
app.include_router(reviews.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
