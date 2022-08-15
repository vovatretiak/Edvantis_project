from fastapi import FastAPI

from project.database import Base
from project.database import engine
from project.routers import authors
from project.routers import books
from project.routers import reviews
from project.routers import users

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Authors",
        "description": """

Things you can do:
* **Get all authors**
* **Create new author**
* **Get author by id**
* **Update author by id**
* **Delete author by id**""",
    },
    {
        "name": "Books",
        "description": """

Things you can do:
* **Get all books (available filters by genre and type)**
* **Create new book**
* **Get books by specific rating**
* **Get books recommendations by genre**
* **Get book by id**
* **Update book by id**
* **Delete book by id**
* **Get books by author id**""",
    },
    {
        "name": "Reviews",
        "description": """
Things you can do:
* **Get all reviews**
* **Create new review if you authorized**
* **Get review by id**
* **Update review by id if you authorized**
* **Delete review by id if you authorized**""",
    },
    {
        "name": "Users",
        "description": """
Things you can do:
* **Create user**
* **Login with your credentials**
* **Get all users**
* **Get your own profile if you authorized**
* **Update your own profile if you authorized**
* **Delete your own profile if you authorized**""",
    },
]

app = FastAPI(
    title="Book Reviews App",
    openapi_tags=tags_metadata,
    version="0.0.1",
    contact={"name": "Volodymyr Tretiak", "email": "vovatretiak97@gmail.com"},
    docs_url="/",
)

app.include_router(authors.router)
app.include_router(books.router)
app.include_router(reviews.router)
app.include_router(users.router)


@app.get("/root/")
def root():
    """
    default message
    """
    return {"message": "Hello Edvantis"}
