<!-- TOC -->
* [Online Library API (FastAPI)](#online-library-api-fastapi)
  * [Вимоги](#вимоги)
  * [Встановлення з нуля (з .venv)](#встановлення-з-нуля-з-venv)
  * [Запуск (SQLite)](#запуск-sqlite)
  * [Запуск з PostgreSQL (Docker)](#запуск-з-postgresql-docker)
  * [Міграції (Alembic)](#міграції-alembic)
  * [Swagger / OpenAPI](#swagger--openapi)
  * [Функціонал](#функціонал)
    * [Авторизація](#авторизація)
    * [Книжки](#книжки)
    * [Вибране](#вибране)
    * [Експорт](#експорт)
    * [Ролі](#ролі)
  * [Основні ендпоінти (за сутностями)](#основні-ендпоінти-за-сутностями)
    * [Auth](#auth)
    * [Books](#books)
    * [Users / Favorites](#users--favorites)
<!-- TOC -->

# Online Library API (FastAPI)

API для онлайн-бібліотеки: реєстрація, логін, каталог книжок, вибране, експорт CSV, ролі.

## Вимоги
- Python 3.12
- Windows PowerShell

## Встановлення з нуля (з .venv)
1. Створити віртуальне оточення (Python 3.12):
```powershell
py -3.12 -m venv .venv
```

2. Активувати оточення:
```powershell
.\.venv\Scripts\Activate.ps1
```

3. Оновити `pip`:
```powershell
python -m pip install --upgrade pip
```

4. Встановити залежності:
```powershell
pip install -r requirements.txt
```


## Запуск (SQLite)
```powershell
uvicorn app.main:app --reload
```

Після запуску застосунок доступний за адресою:
- `http://127.0.0.1:8000`

## Запуск з PostgreSQL (Docker)
1. Підняти Postgres:
```powershell
docker compose up -d
```

2. Задати `DATABASE_URL` (через змінну середовища або `.env`):
```powershell
$env:DATABASE_URL="postgresql+psycopg://app:app@localhost:5432/library"
```
Або створити `.env` у корені проєкту на основі `.env.example`.

3. Застосувати міграції:
```powershell
alembic upgrade head
```

4. Запустити застосунок:
```powershell
uvicorn app.main:app --reload
```

## Міграції (Alembic)
- Ініціалізація вже виконана, перша міграція є в `alembic/versions/`.
- Для створення нової міграції:
```powershell
alembic revision --autogenerate -m "опис"
```
- Застосувати міграції:
```powershell
alembic upgrade head
```

## Swagger / OpenAPI
- Swagger UI: `http://127.0.0.1:8000/docs`
- Swagger-ендпоінт (редирект): `http://127.0.0.1:8000/swagger`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## Функціонал
### Авторизація
- Реєстрація користувача за email/паролем.
- Логін за email/паролем з видачею JWT.

### Книжки
- Список усіх книжок (без логіну).
- Отримання книжки за id (без логіну).
- Додавання книжки (лише адмін).
- Видалення книжки (лише адмін).

### Вибране
- Додавання книжки у вибране користувачу (лише свій акаунт).
- Видалення книжки з вибраного користувачу (лише свій акаунт).
- Список вибраних книжок користувача (лише свій акаунт).

### Експорт
- Вивантаження списку книжок у CSV (лише адмін).

### Ролі
- Доступні ролі: `admin`, `client`.
- Зміна ролі через консольну команду.

Команда:
```powershell
python -m app.cli user@example.com admin
```

## Основні ендпоінти (за сутностями)
### Auth
- `POST /auth/register`
- `POST /auth/login`

### Books
- `GET /books`
- `GET /books/{book_id}`
- `POST /books` (admin)
- `DELETE /books/{book_id}` (admin)
- `GET /books/export/csv` (admin)

### Users / Favorites
- `GET /users/{user_id}/favorites`
- `POST /users/{user_id}/favorites/{book_id}`
- `DELETE /users/{user_id}/favorites/{book_id}`
