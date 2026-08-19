# FastAPI JWT Auth

A reusable JWT authentication template for FastAPI applications. Clone it, configure your database, and run `docker compose up` — tables are created automatically and sample users are seeded.

## Features

- User login with email & password
- Access token & refresh token pair
- Token refresh endpoint
- Logout with refresh token revocation
- Role-based authorization (`admin`, `user`)
- Protected endpoints via Bearer token
- Database-backed session/token management (PostgreSQL)
- Password hashing with Argon2
- Structured logging

## Tech Stack

- Python 3.12+
- FastAPI 0.141
- SQLAlchemy 2.0 + Alembic
- PostgreSQL (psycopg 3)
- PyJWT (HS256)
- pwdlib (Argon2)
- Docker & Docker Compose

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/your-org/fastapi-jwt-auth.git
cd fastapi-jwt-auth
```

### 2. Configure environment

Copy the example env file and update the values:

```bash
cp .env.example .env
```

```env
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/application_db

JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
```

> `DATABASE_URL` points to the PostgreSQL instance on the host machine. Make sure PostgreSQL is running before starting the container.

### 3. Run with Docker

```bash
docker compose up --build
```

On first startup the entrypoint will:

1. Wait for the database to be ready
2. Run Alembic migrations (creates `users` and `refresh_tokens` tables)
3. inserd two sample users
4. Start the FastAPI server on port 8000

### 4. Open the API docs

```
http://localhost:8000/docs
```

## Sample Users (seeded automatically)

| Name       | Email                    | Password  | Role  |
|------------|--------------------------|-----------|-------|
| Test User  | testuser@example.com     | Test@123  | user  |
| Demo User  | demouser@example.com     | demo@123  | admin |

## API Endpoints

| Method | Endpoint              | Auth Required | Role        | Description                       |
|--------|-----------------------|---------------|-------------|-----------------------------------|
| POST   | `/auth/login`         | No            | —           | Login, returns access+refresh tokens |
| POST   | `/auth/refresh`       | No            | —           | Exchange refresh token for new access token |
| POST   | `/auth/logout`        | No            | —           | Revoke a refresh token            |
| GET    | `/auth/profile`       | Yes           | Any         | Get current user info             |
| GET    | `/auth/admin/dashboard` | Yes         | admin       | Admin-only endpoint               |
| GET    | `/auth/user/dashboard`  | Yes         | user        | User-only endpoint                |
| GET    | `/health_check`       | No            | —           | Health check                      |

## Usage Example

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email_address":"testuser@example.com","password":"Test@123"}'
```

### Access a protected endpoint

```bash
curl http://localhost:8000/auth/profile \
  -H "Authorization: Bearer <access_token>"
```

### Refresh the access token

```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"<refresh_token>"}'
```

### Logout (revoke refresh token)

```bash
curl -X POST http://localhost:8000/auth/logout \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"<refresh_token>"}'
```

### Use role-based endpoints

```bash
# Admin only
curl http://localhost:8000/auth/admin/dashboard \
  -H "Authorization: Bearer <admin_access_token>"

# User only
curl http://localhost:8000/auth/user/dashboard \
  -H "Authorization: Bearer <user_access_token>"
```

## Project Structure

```
.
├── alembic/                    # Database migrations
│   ├── env.py
│   └── versions/
├── src/
│   ├── config.py               # Env vars, logging setup
│   ├── database.py             # SQLAlchemy engine & session
│   ├── insert_user.py          # Seed script
│   ├── main.py                 # FastAPI app entry point
│   ├── jwt_auth/
│   │   ├── api.py              # Auth route handlers
│   │   ├── models.py           # SQLAlchemy models
│   │   └── schema.py           # Pydantic schemas
│   ├── services/jwt_auth/
│   │   ├── dependancy.py       # get_current_user, require_role
│   │   └── service.py          # Auth business logic
│   └── utils/
│       ├── jwt_handler.py      # JWT encode/decode
│       └── password_helper.py  # Argon2 hashing
├── docker-compose.yaml
├── dockerfile
├── docker-entrypoint.sh
├── .env.example
├── pyproject.toml
└── README.md
```

## Logging

Logs are written to stdout with the format:

```
2026-08-19 10:00:00 | INFO     | src.jwt_auth.api | User logged in: testuser@example.com
```

Set the `LOG_LEVEL` env var to control verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`).

## Development (without Docker)

```bash
pip install poetry
poetry install
cp .env.example .env   # update DATABASE_URL to point to your local Postgres
alembic upgrade head
python -m src.insert_user
uvicorn src.main:app --reload
```

## License

MIT
