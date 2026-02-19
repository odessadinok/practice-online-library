from sqlalchemy import Column, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


book_authors = Table(
    "book_authors",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
)

book_genres = Table(
    "book_genres",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
)

user_favorites = Table(
    "user_favorites",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    UniqueConstraint("user_id", "book_id", name="uq_user_book"),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(32), default="client")

    favorites: Mapped[list["Book"]] = relationship(
        "Book", secondary=user_favorites, back_populates="favorited_by"
    )


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    books: Mapped[list["Book"]] = relationship(
        "Book", secondary=book_authors, back_populates="authors"
    )


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    books: Mapped[list["Book"]] = relationship(
        "Book", secondary=book_genres, back_populates="genres"
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), index=True)

    authors: Mapped[list[Author]] = relationship(
        "Author", secondary=book_authors, back_populates="books"
    )
    genres: Mapped[list[Genre]] = relationship(
        "Genre", secondary=book_genres, back_populates="books"
    )
    favorited_by: Mapped[list[User]] = relationship(
        "User", secondary=user_favorites, back_populates="favorites"
    )
