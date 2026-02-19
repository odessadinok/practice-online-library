import csv
from io import StringIO

from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.auth import authenticate_user, create_access_token, get_user_by_email, hash_password
from app.db import Base, engine
from app.deps import get_current_user, get_db, require_admin


# Для разработки на SQLite можно создавать таблицы автоматически.
# В Postgres используем миграции Alembic.
if engine.url.get_backend_name() == "sqlite":
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="Online Library API")

LOGIN_FORM_OPENAPI = {
    "requestBody": {
        "content": {
            "application/x-www-form-urlencoded": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "grant_type": {"type": "string", "example": "password"},
                        "username": {"type": "string", "example": "user@example.com"},
                        "password": {"type": "string", "example": "SecurePass123"},
                        "scope": {"type": "string", "example": ""},
                        "client_id": {"type": "string", "example": ""},
                        "client_secret": {"type": "string", "example": ""},
                    },
                    "required": ["username", "password"],
                }
            }
        }
    }
}


@app.post("/auth/register", response_model=schemas.UserOut)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = models.User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role="client",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/auth/login", response_model=schemas.Token, openapi_extra=LOGIN_FORM_OPENAPI)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    token = create_access_token(user.email)
    return schemas.Token(access_token=token)


@app.get("/books", response_model=list[schemas.BookOut])
def list_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()


@app.get("/books/{book_id}", response_model=schemas.BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@app.post("/books", response_model=schemas.BookOut, dependencies=[Depends(require_admin)])
def create_book(payload: schemas.BookCreate, db: Session = Depends(get_db)):
    book = crud.create_book(db, payload.title, payload.authors, payload.genres)
    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    db.delete(book)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/users/{user_id}/favorites/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def add_to_favorites(
    user_id: int,
    book_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    crud.add_favorite(db, current_user, book)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/users/{user_id}/favorites/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_favorites(
    user_id: int,
    book_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    crud.remove_favorite(db, current_user, book)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/users/{user_id}/favorites", response_model=list[schemas.BookOut])
def list_favorites(
    user_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    db.refresh(current_user)
    return current_user.favorites


@app.get("/books/export/csv", dependencies=[Depends(require_admin)])
def export_books_csv(db: Session = Depends(get_db)):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "title", "authors", "genres"])
    for book in db.query(models.Book).all():
        authors = ";".join([a.name for a in book.authors])
        genres = ";".join([g.name for g in book.genres])
        writer.writerow([book.id, book.title, authors, genres])
    return Response(content=output.getvalue(), media_type="text/csv")


@app.get("/swagger", include_in_schema=False)
def swagger_redirect():
    return RedirectResponse(url="/docs")
