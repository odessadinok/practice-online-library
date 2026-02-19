import typer
from sqlalchemy.orm import Session

from app.auth import get_user_by_email
from app.db import SessionLocal


def main(email: str, role: str):
    if role not in {"admin", "client"}:
        raise typer.BadParameter("role must be admin or client")
    db: Session = SessionLocal()
    try:
        user = get_user_by_email(db, email)
        if not user:
            raise typer.BadParameter("user not found")
        user.role = role
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    typer.run(main)
