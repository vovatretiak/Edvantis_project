from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from project.utils import get_password_hash

from . import models, schemas


# crud for books
def get_book_by_id(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} is not found",
        )
    return book


# https://sqlmodel.tiangolo.com/tutorial/fastapi/update/
def update_book(db: Session, book_id: int, updated_book: schemas.BookUpdate):
    book = get_book_by_id(db=db, book_id=book_id)

    for key, value in updated_book.dict(exclude_unset=True).items():
        if key == "author_id":
            book_a = db.query(models.Book).get(book_id)
            book_a.authors.clear()
            db.add(book_a)
            db.commit()
            authors = db.query(models.Author).filter(models.Author.id.in_(value))
            if authors.count() == len(value):
                book.authors.extend(authors)
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Authors is not found"
                )
        setattr(book, key, value)

    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_books_by_author_id(db: Session, author_id: int):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    return author.books


def get_books(db: Session, offset: int, limit: int):
    return db.query(models.Book).offset(offset).limit(limit).all()


# https://blog.miguelgrinberg.com/post/nested-queries-with-sqlalchemy-orm
def get_books_by_rating(db: Session, rating: int, offset: int, limit: int):
    rating_subquery = (
        db.query(models.Review.book_id, func.avg(models.Review.rating).label("average"))
        .group_by(models.Review.book_id)
        .subquery()
    )
    books = (
        db.query(models.Book)
        .join(rating_subquery, models.Book.id == rating_subquery.c.book_id)
        .where(rating_subquery.c.average >= rating)
        .order_by(rating_subquery.c.average.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return books


# https://stackoverflow.com/questions/68394091/fastapi-sqlalchemy-pydantic-%E2%86%92-how-to-process-many-to-many-relations
def create_book(db: Session, book: schemas.BookCreate):
    new_book = models.Book(
        title=book.title,
        description=book.description,
        year=book.year,
        image_file=book.image_file,
        pages=book.pages,
        genre=book.genre,
        type=book.type,
    )
    authors = db.query(models.Author).filter(models.Author.id.in_(book.author_id))
    if authors.count() == len(book.author_id):
        new_book.authors.extend(authors)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Authors is not found"
        )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def delete_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id)
    if not book.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} is not found",
        )
    # remove authors from a book
    book_a = db.query(models.Book).get(book_id)
    book_a.authors.clear()
    db.add(book_a)
    db.commit()
    # remove book
    book.delete()
    db.commit()
    return {"Detail": "Book has been deleted"}


# crud for authors


def create_author(db: Session, author: schemas.AuthorCreate):
    new_author = models.Author(
        first_name=author.first_name,
        last_name=author.last_name,
        middle_name=author.middle_name,
        image_file=author.image_file,
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def get_authors(db: Session, offset: int, limit: int):
    return db.query(models.Author).offset(offset).limit(limit).all()


def get_author_by_id(db: Session, author_id: int):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id {author_id} is not found",
        )
    return author


def update_author(db: Session, author_id: int, updated_author: schemas.AuthorUpdate):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id {author_id} is not found",
        )
    for key, value in updated_author.dict(exclude_unset=True).items():
        setattr(author, key, value)

    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def delete_author(db: Session, author_id: int):
    author = db.query(models.Author).filter(models.Author.id == author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id {author_id} is not found",
        )
    author.delete()
    db.commit()
    return {"Detail": "Author has been deleted"}


# crud for review
def create_review(db: Session, review: schemas.ReviewCreate):
    new_review = models.Review(
        user_id=review.user_id,
        text=review.text,
        rating=review.rating,
        book_id=review.book_id,
    )
    db.add(new_review)
    db.commit()
    book = get_book_by_id(db=db, book_id=review.book_id)
    book.reviews.append(new_review)
    db.add(book)
    db.commit()
    db.refresh(book)
    db.refresh(new_review)

    return new_review


def get_reviews(db: Session, offset: int, limit: int):
    return db.query(models.Review).offset(offset).limit(limit).all()


def get_review_by_id(db: Session, review_id: int):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} is not found",
        )
    return review


def update_review(db: Session, review_id: int, updated_review: schemas.ReviewCreate):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} is not found",
        )
    book = db.query(models.Book).filter(models.Book.id == review.book_id).first()
    if review.book_id != updated_review.book_id:
        book.reviews.remove(review)
        db.add(book)
        db.commit()
        db.refresh(book)
    for key, value in updated_review.dict(exclude_unset=True).items():
        setattr(review, key, value)
    new_book = db.query(models.Book).filter(models.Book.id == review.book_id).first()
    if not new_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {review.book_id} is not found",
        )
    new_book.reviews.append(review)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def delete_review(db: Session, review_id: int):
    review = db.query(models.Review).filter(models.Review.id == review_id)
    if not review.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} is not found",
        )
    book = (
        db.query(models.Book).filter(models.Book.id == review.first().book_id).first()
    )
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {review.first().book_id} is not found",
        )
    book.reviews.remove(review.first())
    db.add(book)
    db.commit()
    db.refresh(book)
    review.delete()
    db.commit()
    return {"Detail": "Review has been deleted"}


# crud for review
def create_user(user: schemas.UserCreate, db: Session):
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"User with username '{user.username}' is already exist",
        )
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"User with email '{user.email}' is already exist",
        )
    hashed_pw = get_password_hash(user.password)
    new_user = models.User(username=user.username, email=user.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_username(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with username '{user.username}' is not exist",
        )
    return user


def get_users(db: Session, offset: int, limit: int):
    users = db.query(models.User).offset(offset).limit(limit).all()
    return users
