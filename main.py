from fastapi import FastAPI

from project import models
from project.database import engine
from project.routers import authors
from project.routers import books
from project.routers import reviews
from project.routers import users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(authors.router)
app.include_router(books.router)
app.include_router(reviews.router)
app.include_router(users.router)


@app.get("/")
def root():
    """
    default message
    """
    return {"message": "Hello World"}
