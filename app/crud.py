from sqlalchemy.orm import Session

from app import models


def get_or_create_author(db: Session, name: str) -> models.Author:
    author = db.query(models.Author).filter(models.Author.name == name).first()
    if author:
        return author
    author = models.Author(name=name)
    db.add(author)
    return author


def get_or_create_genre(db: Session, name: str) -> models.Genre:
    genre = db.query(models.Genre).filter(models.Genre.name == name).first()
    if genre:
        return genre
    genre = models.Genre(name=name)
    db.add(genre)
    return genre


def create_book(db: Session, title: str, authors: list[str], genres: list[str]) -> models.Book:
    book = models.Book(title=title)
    book.authors = [get_or_create_author(db, name) for name in authors]
    book.genres = [get_or_create_genre(db, name) for name in genres]
    db.add(book)
    return book


def add_favorite(db: Session, user: models.User, book: models.Book) -> None:
    if book not in user.favorites:
        user.favorites.append(book)


def remove_favorite(db: Session, user: models.User, book: models.Book) -> None:
    if book in user.favorites:
        user.favorites.remove(book)
