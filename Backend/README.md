# OutfitLens Backend

AI-powered virtual try-on application backend built with FastAPI and SQLAlchemy.

## Overview

OutfitLens allows users to upload their photo and clothing item photos to generate AI-powered virtual try-on images using Google's Gemini 2.0 Flash model.

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (local) with SQLAlchemy ORM
- **Migrations**: Alembic
- **AI Integration**: Google Gemini 2.0 Flash
- **Authentication**: JWT tokens with bcrypt
- **Package Management**: UV

## Project Structure

```
backend/
├── app/
│   ├── domain/          # Domain layer (business logic)
│   ├── infrastructure/  # Infrastructure layer (DB, storage, external services)
│   ├── application/     # Application layer (use cases)
│   ├── api/             # API layer (routes, schemas)
│   ├── core/            # Core configuration
│   └── utils/           # Utilities
├── tests/               # Test suites
├── alembic/             # Database migrations
├── storage/             # Local file storage
└── docs/                # Documentation
```

## Setup

### Prerequisites

- Python 3.11 or higher
- UV package manager

### Installation

1. Clone the repository
2. Create virtual environment:
   ```bash
   uv venv
   ```

3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

4. Configure environment:
   ```bash
   cp .env.example .env.dev
   # Edit .env.dev with your configuration
   ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start development server:
   ```bash
   python run_dev.py
   ```

## Development

### Running the Server

**Development mode:**
```bash
python run_dev.py
```

**Production mode:**
```bash
python run_prod.py
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Run migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/domain/test_user.py
```

### Code Quality

```bash
# Format code
black .

# Lint code
ruff check .

# Type check
mypy app/
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## Environment Variables

See `.env.example` for all required environment variables.

Key variables:
- `GEMINI_API_KEY`: Google Gemini API key
- `SECRET_KEY`: JWT secret key (generate with `openssl rand -hex 32`)
- `DATABASE_URL`: Database connection string

## Architecture

This project follows **Domain-Driven Design (DDD)** principles with clean architecture:

- **Domain Layer**: Pure business logic, no dependencies
- **Application Layer**: Use cases and orchestration
- **Infrastructure Layer**: Database, file storage, external APIs
- **API Layer**: HTTP endpoints and request/response handling

## Documentation

- [PRD (Product Requirements Document)](docs/prd.md)
- [Architecture Guide](claude.md)
- [Implementation Steps](docs/v1_implementation_steps.md)

## License

Copyright © 2025 OutfitLens Team
