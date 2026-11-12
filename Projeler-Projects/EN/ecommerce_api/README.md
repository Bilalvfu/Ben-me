# E-Commerce API

An e-commerce REST API built with FastAPI, SQLAlchemy, and PostgreSQL. It supports user registration and JWT authentication, category and product management, and order creation with stock control.

## Features

- User registration with email and login with the OAuth2 password flow
- JWT access tokens valid for 30 minutes
- Admin-only category and product creation, updates, and deletion
- Public category and product listings
- Authenticated users can create and view their own orders
- Stock validation and stock updates during order creation
- Database schema migrations with Alembic

## Requirements

- Python 3.12 (the Docker image uses Python 3.12)
- Docker and Docker Compose, or a local PostgreSQL 15+ instance

## Quick start with Docker

Create a `.env` file in the project root:

```dotenv
POSTGRES_PASSWORD=a_strong_database_password
SECRET_KEY=a_secret_key_at_least_32_bytes_long
```

You can use OpenSSL to generate a random `SECRET_KEY`:

```bash
openssl rand -hex 32
```

Start the services:

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`. Interactive Swagger documentation is available at `http://localhost:8000/docs`, and an alternative API reference is available at `/redoc`. The API container runs `alembic upgrade head` on startup.

Press `Ctrl+C` to stop the services. To stop services running in the background:

```bash
docker compose down
```

Database data is stored in the Docker volume named `postgres_data`. To remove the data as well, run `docker compose down -v`.

## Local development

Create a database in PostgreSQL and add the following variables to a `.env` file in the project root. Update `DATABASE_URL` with your PostgreSQL username, password, host, and database name:

```dotenv
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/ecommerce_db
SECRET_KEY=a_secret_key_at_least_32_bytes_long
```

Create a virtual environment and install the dependencies:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Apply the database migrations and start the API:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

You can also start the app with `python run.py`. This entry point runs the API at `127.0.0.1:8000` without auto-reload.

## Authentication and admin accounts

Use `POST /auth/register` to create a user. Newly registered accounts are regular users by default. Only users with `is_admin` enabled can create, update, or delete categories and products. The application does not provide a public endpoint for creating an admin. After registering the first admin account through a trusted method, set its `users.is_admin` value to `true` in the database.

To log in, send form data to `POST /auth/login`. Use the email address as the `username` field and the password as the `password` field. Include the returned `access_token` in requests to protected endpoints:

```http
Authorization: Bearer <access_token>
```

Passwords are hashed with bcrypt. `SECRET_KEY` must be at least 32 bytes long. Use a strong, private value in production.

## API endpoints

| Method | Path | Access | Description |
|---|---|---|---|
| `GET` | `/` | Public | API status message |
| `POST` | `/auth/register` | Public | Register a user |
| `POST` | `/auth/login` | Public | Log in with email and password to get a JWT |
| `GET` | `/auth/me` | Authenticated | Get the current user's details |
| `GET` | `/categories/` | Public | List categories (`skip`, `limit`) |
| `POST` | `/categories/` | Admin | Create a category |
| `PUT` | `/categories/{category_id}` | Admin | Update a category |
| `DELETE` | `/categories/{category_id}` | Admin | Delete a category |
| `GET` | `/products/` | Public | List products (`skip`, `limit`) |
| `GET` | `/products/{product_id}` | Public | Get product details |
| `POST` | `/products/` | Admin | Create a product |
| `PUT` | `/products/{product_id}` | Admin | Update a product |
| `DELETE` | `/products/{product_id}` | Admin | Delete a product |
| `POST` | `/orders/` | Authenticated | Create an order and deduct stock |
| `GET` | `/orders/` | Authenticated | List the current user's orders |
| `GET` | `/orders/{order_id}` | Authenticated | Get the current user's order details |

The `limit` parameter for category and product listings can be at most 100. Order items require positive `product_id` and `quantity` values. If stock is insufficient, the request returns `400` and stock remains unchanged.

## Example requests

Register:

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"strong-password"}'
```

Log in using OAuth2 form data:

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=strong-password"
```

Create an order (replace `TOKEN` with the value from the login response):

```bash
curl -X POST http://localhost:8000/orders/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"items":[{"product_id":1,"quantity":2}]}'
```

## Project structure

```text
app/
  core/       Database connection and session management
  crud/       Database operations
  models/     SQLAlchemy models
  routers/    FastAPI endpoints
  schemas/    Request and response schemas
  main.py     FastAPI application
alembic/      Database migrations
tests/        API tests
```

## Tests

Tests run against an in-memory SQLite database. The test configuration sets the environment variables needed to run them. With the virtual environment activated, install the test dependencies and run:

```bash
pip install pytest httpx
pytest
```
```