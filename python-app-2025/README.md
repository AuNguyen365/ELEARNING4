# Python App 2025

A modern FastAPI application with clean architecture.

## Project Structure

```
python-app-2025/
├─ src/
│  └─ app/
│     ├─ main.py                 # FastAPI entrypoint
│     ├─ api/                    # Routes and API endpoints
│     ├─ core/                   # Core configurations
│     ├─ schemas/                # Pydantic models
│     ├─ services/               # Business logic
│     ├─ db/                     # Database models and session
│     ├─ middleware/             # Custom middleware
│     ├─ utils/                  # Utility functions
│     └─ assets/                 # Static assets
└─ tests/
   ├─ unit/                      # Unit tests
   └─ e2e/                       # End-to-end tests
```

## Setup

1. Install dependencies:

```bash
poetry install
```

2. Copy .env.example to .env and configure your environment variables:

```bash
cp .env.example .env
```

3. Run the application:

```bash
poetry run uvicorn src.app.main:app --reload
```

## Testing

Run tests with:

```bash
poetry run pytest
```

## API Documentation

Once running, visit:

- http://localhost:8000/docs for Swagger UI
- http://localhost:8000/redoc for ReDoc
