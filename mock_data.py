import json
from random import choice
from random import randint

from sqlalchemy.orm import Session

from project import crud
from project import database
from project import models
from project import schemas
from project.utils import get_password_hash

db = Session(bind=database.engine)

# with open("authors.json", "r") as f:
#     authors = json.load(f)

# for a in authors:
#     f_name = a.get("first_name")
#     l_name = a.get("last_name")
#     m_name = a.get("middle_name")
#     img = a.get("img")

#     new_a = models.Author(
#         first_name=f_name, last_name=l_name, middle_name=m_name, image_file=img
#     )
#     db.add(new_a)
#     db.commit()
#     db.refresh(new_a)
#     print(new_a)

# with open("books.json", "r") as f:
#     books = json.load(f)

# for b in books:
#     title = b.get("title")
#     description = b.get("description")
#     year = b.get("year")
#     img = b.get("img")
#     pages = b.get("pages")
#     genre = b.get("genre")
#     type = b.get("type")
#     authors = [randint(1, 50)]
#     if books.index(b) % 5 == 0:
#         second_author = randint(1, 50)
#         if second_author not in authors:
#             authors.append(second_author)
#     new_book = models.Book(
#         title=title,
#         description=description,
#         year=year,
#         image_file=img,
#         pages=pages,
#         genre=genre,
#         type=type,
#     )
#     authors_db = db.query(models.Author).filter(models.Author.id.in_(authors))
#     if authors_db.count() == len(authors):
#         new_book.authors.extend(authors_db)
#     db.add(new_book)
#     db.commit()
#     db.refresh(new_book)
#     print(new_book)


# with open("users.json", "r") as f:
#     users = json.load(f)

# for u in users:
#     username = u.get("username")
#     email = u.get("email")
#     password = u.get("password")
#     hashed_pw = get_password_hash(password)
#     new_user = models.User(username=username, email=email, password=hashed_pw)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     print(new_user.id, new_user.username)

with open("reviews.json", "r") as f:
    reviews = json.load(f)

for r in reviews:
    user_id = r.get("user_id")
    text = r.get("text")
    rating = r.get("rating")
    book_id = r.get("book_id")

    schema_review = schemas.ReviewCreate(
        user_id=user_id, text=text, rating=rating, book_id=book_id
    )
    user = db.query(models.User).filter(models.User.id == user_id).first()
    crud.create_review(db=db, review=schema_review, user=user)
