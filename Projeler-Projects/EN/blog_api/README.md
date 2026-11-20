# Blog API

A REST API built with FastAPI for creating blog posts and comments. It uses SQLAlchemy and SQLite for data storage, and Alembic for database schema migrations.

## Features

- Create, list, and retrieve users
- Create, list, and retrieve posts
- Add comments to posts and list comments
- Create and list tags
- Model relational data with one-to-many `User`–`Post` and `User`–`Comment` relationships, and a many-to-many `Post`–`Tag` relationship through the `post_tags` association table
- API and database health checks
- Interactive API documentation with Swagger UI and ReDoc

## Tech Stack

- Python
- FastAPI and Pydantic
- SQLAlchemy
- Alembic
- SQLite
- Uvicorn

## Requirements

Python 3.10 or later and `pip` are required.

## Installation

Create and activate a virtual environment in the project directory.

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Windows (Git Bash)

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies and create the database tables by applying the migrations:

```bash
python -m pip install -r requirements.txt
python -m alembic upgrade head
```

## Run the Application

```bash
python -m uvicorn app.main:app --reload
```

By default, the server runs at `http://127.0.0.1:8000`.

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Basic health check: `http://127.0.0.1:8000/`
- Database health check: `http://127.0.0.1:8000/health/db`

## API Endpoints

| Resource | Method | Path | Description |
|---|---|---|---|
| Health | `GET` | `/` | Confirms that the API is running. |
| Health | `GET` | `/health/db` | Checks the database connection. |
| Users | `POST` | `/users/` | Creates a user. |
| Users | `GET` | `/users/` | Lists users. |
| Users | `GET` | `/users/{user_id}` | Retrieves a user. |
| Posts | `POST` | `/posts/` | Creates a post. |
| Posts | `GET` | `/posts/` | Lists posts. |
| Posts | `GET` | `/posts/{post_id}` | Retrieves a post. |
| Comments | `POST` | `/comments/` | Adds a comment to a post. |
| Comments | `GET` | `/comments/` | Lists comments. |
| Tags | `POST` | `/tags/` | Creates a tag. |
| Tags | `GET` | `/tags/` | Lists tags. |

See `/docs` for request body fields and response schemas. To create a user, provide `username`, `email`, and `password`; a post requires `title`, `content`, `slug`, and `author_id`; a comment requires `content`, `post_id`, and `author_id`; and a tag requires `name`. The referenced user or post must already exist when creating a post or comment.

## Database and Migrations

The application uses SQLite and connects to the `blog.db` file in the project root. Apply schema migrations with:

```bash
python -m alembic upgrade head
```

To roll back the most recent migration:

```bash
python -m alembic downgrade -1
```

### Development Note

This project is intended for academic review and local development. Password hashing, authentication and authorization, and production security hardening are planned as future steps.

## Project Structure

```text
app/
├── db/          # Database connection and base configuration
├── models/      # SQLAlchemy models
├── routers/     # API endpoints
├── schemas/     # Pydantic request and response schemas
└── main.py      # FastAPI application
alembic/         # Database migrations
alembic.ini      # Alembic configuration
requirements.txt # Python dependencies
```
adsadadad
