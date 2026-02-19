from pydantic import BaseModel, EmailStr, Field


class AuthorOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": 1,
                    "name": "Harper Lee",
                }
            ]
        }


class GenreOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": 1,
                    "name": "Classic",
                }
            ]
        }


class BookOut(BaseModel):
    id: int
    title: str
    authors: list[AuthorOut]
    genres: list[GenreOut]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": 1,
                    "title": "To Kill a Mockingbird",
                    "authors": [{"id": 1, "name": "Harper Lee"}],
                    "genres": [{"id": 1, "name": "Classic"}],
                }
            ]
        }


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    authors: list[str] = Field(min_length=1)
    genres: list[str] = Field(min_length=1)

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "title": "To Kill a Mockingbird",
                    "authors": ["Harper Lee"],
                    "genres": ["Classic", "Fiction"],
                }
            ]
        }


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": 1,
                    "email": "user@example.com",
                    "role": "client",
                }
            ]
        }


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "email": "user@example.com",
                    "password": "SecurePass123",
                }
            ]
        }


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                }
            ]
        }
