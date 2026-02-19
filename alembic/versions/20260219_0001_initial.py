"""initial

Revision ID: 20260219_0001
Revises: 
Create Date: 2026-02-19
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260219_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
    )
    op.create_index("ix_authors_name", "authors", ["name"], unique=True)

    op.create_table(
        "genres",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
    )
    op.create_index("ix_genres_name", "genres", ["name"], unique=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
    )
    op.create_index("ix_books_title", "books", ["title"], unique=False)

    op.create_table(
        "book_authors",
        sa.Column("book_id", sa.Integer(), sa.ForeignKey("books.id"), primary_key=True),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("authors.id"), primary_key=True),
    )

    op.create_table(
        "book_genres",
        sa.Column("book_id", sa.Integer(), sa.ForeignKey("books.id"), primary_key=True),
        sa.Column("genre_id", sa.Integer(), sa.ForeignKey("genres.id"), primary_key=True),
    )

    op.create_table(
        "user_favorites",
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("book_id", sa.Integer(), sa.ForeignKey("books.id"), primary_key=True),
        sa.UniqueConstraint("user_id", "book_id", name="uq_user_book"),
    )


def downgrade() -> None:
    op.drop_table("user_favorites")
    op.drop_table("book_genres")
    op.drop_table("book_authors")
    op.drop_index("ix_books_title", table_name="books")
    op.drop_table("books")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
    op.drop_index("ix_genres_name", table_name="genres")
    op.drop_table("genres")
    op.drop_index("ix_authors_name", table_name="authors")
    op.drop_table("authors")
