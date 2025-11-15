# OutfitLens Backend Project

## Project Overview
This is the backend service for **OutfitLens**, a virtual try-on application that uses AI to generate images of users wearing clothing items. Built with FastAPI and SQLite (local), the project follows **100% domain-driven design (DDD) principles** with a focus on scalable architecture, clean separation of concerns, and maintainable code structure.

**Application Purpose**: Users upload two images (their photo + clothing item photo), and the system uses Google's Gemini 2.5 Flash Image model to generate a composite image showing the user wearing that clothing.

**Current Status**: Initial development phase - clean architecture foundation ready for implementation.

## Tech Stack
- **Framework**: FastAPI (Python 3.11+)
- **Database**: SQLite (local) with SQLAlchemy ORM
- **Migrations**: Alembic for database schema migrations
- **AI Integration**: Google Gemini 2.5 Flash Image API
- **Authentication**: JWT tokens with bcrypt password hashing
- **Package Management**: UV (for virtual environment and dependencies)
- **Configuration Management**: pyproject.toml
- **Environment Management**: .env files for different environments
- **File Storage**: Local filesystem (future migration to AWS S3)

## Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application entry point
│   │
│   ├── domain/                  # Domain Layer (DDD - Business Logic)
│   │   ├── __init__.py
│   │   ├── shared/              # Shared domain models and value objects
│   │   │   ├── __init__.py
│   │   │   ├── base.py          # Base entity, aggregate root, value objects
│   │   │   ├── enums.py         # Shared enumerations
│   │   │   └── events.py        # Domain events
│   │   │
│   │   ├── user/                # User Domain
│   │   │   ├── __init__.py
│   │   │   ├── entities.py      # User, UserProfile entities
│   │   │   ├── value_objects.py # Email, Password value objects
│   │   │   ├── repositories.py  # UserRepository interface
│   │   │   └── services.py      # User domain services
│   │   │
│   │   ├── image/               # Image Domain
│   │   │   ├── __init__.py
│   │   │   ├── entities.py      # Image, ImageMetadata entities
│   │   │   ├── value_objects.py # ImageFormat, ImageDimensions, ImageType
│   │   │   ├── repositories.py  # ImageRepository interface
│   │   │   └── services.py      # Image domain services
│   │   │
│   │   └── generation/          # Generation Domain
│   │       ├── __init__.py
│   │       ├── entities.py      # Generation, GenerationRequest entities
│   │       ├── value_objects.py # GenerationStatus, ProcessingTime
│   │       ├── repositories.py  # GenerationRepository interface
│   │       └── services.py      # Generation domain services
│   │
│   ├── infrastructure/          # Infrastructure Layer (Technical Implementations)
│   │   ├── __init__.py
│   │   ├── database/            # Database implementations
│   │   │   ├── __init__.py
│   │   │   ├── connection.py    # SQLAlchemy database connection
│   │   │   ├── models.py        # SQLAlchemy ORM models
│   │   │   └── repositories/    # Repository implementations
│   │   │       ├── __init__.py
│   │   │       ├── user_repository.py
│   │   │       ├── image_repository.py
│   │   │       └── generation_repository.py
│   │   │
│   │   ├── storage/             # File storage implementations
│   │   │   ├── __init__.py
│   │   │   ├── local_storage.py # Local filesystem storage
│   │   │   └── storage_interface.py  # Storage interface for future S3
│   │   │
│   │   └── external/            # External service integrations
│   │       ├── __init__.py
│   │       └── gemini_service.py  # Gemini AI API integration
│   │
│   ├── application/             # Application Layer (Use Cases)
│   │   ├── __init__.py
│   │   ├── services/            # Application services (orchestration)
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py      # Authentication use cases
│   │   │   ├── user_service.py      # User management use cases
│   │   │   ├── image_service.py     # Image upload/management use cases
│   │   │   └── generation_service.py  # Generation workflow use cases
│   │   │
│   │   └── dtos/                # Data Transfer Objects
│   │       ├── __init__.py
│   │       ├── user_dtos.py
│   │       ├── image_dtos.py
│   │       └── generation_dtos.py
│   │
│   ├── api/                     # Presentation Layer (API/Routes)
│   │   ├── __init__.py
│   │   ├── dependencies.py      # FastAPI dependencies
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   │   ├── __init__.py
│   │   │   ├── auth_schemas.py
│   │   │   ├── user_schemas.py
│   │   │   ├── image_schemas.py
│   │   │   └── generation_schemas.py
│   │   │
│   │   └── routers/             # API route handlers
│   │       ├── __init__.py
│   │       ├── auth.py          # /api/v1/auth/*
│   │       ├── users.py         # /api/v1/users/*
│   │       ├── images.py        # /api/v1/images/*
│   │       └── generations.py   # /api/v1/generations/*
│   │
│   ├── core/                    # Core configurations
│   │   ├── __init__.py
│   │   ├── config.py            # Application configuration
│   │   ├── security.py          # JWT, password hashing
│   │   └── exceptions.py        # Custom exception classes
│   │
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       ├── logger.py            # Logging utilities
│       └── validators.py        # Validation helpers
│
├── alembic/                     # Alembic migration files
│   ├── versions/                # Migration version files
│   │   └── [timestamp]_[description].py
│   ├── env.py                   # Alembic environment configuration
│   └── script.py.mako           # Migration template
│
├── storage/                     # Local file storage (gitignored)
│   ├── user_photos/             # User uploaded photos
│   ├── clothing_photos/         # Clothing item photos
│   └── generated_results/       # AI-generated images
│
├── tests/                       # Test scripts and test cases
│   ├── __init__.py
│   ├── unit/                    # Unit tests
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   ├── integration/             # Integration tests
│   └── e2e/                     # End-to-end tests
│
├── alembic.ini                  # Alembic configuration
├── .env.example                 # Environment template (safe to commit)
├── .env.dev                     # Development environment variables
├── .env.prod                    # Production environment variables
├── pyproject.toml               # Project configuration and dependencies
├── requirements.txt             # Generated from pyproject.toml
├── run_dev.py                   # Development server runner
├── run_prod.py                  # Production server runner
└── README.md
```

## Domain-Driven Design Architecture

### Core Domains

#### 1. User Domain
**Purpose**: Manage user accounts, authentication, and profiles

**Entities**:
- `User` (Aggregate Root): User account with authentication
- `UserProfile`: User profile information and preferences

**Value Objects**:
- `Email`: Validated email address
- `Password`: Password with strength validation

**Responsibilities**:
- User registration and email verification
- Authentication and password management
- Profile management
- Account lifecycle (activation, deactivation, deletion)

**Repository**: `UserRepository`

#### 2. Image Domain
**Purpose**: Handle image uploads, storage, and metadata

**Entities**:
- `Image` (Aggregate Root): Image entity with metadata
- `ImageMetadata`: Image technical details (size, dimensions, format)

**Value Objects**:
- `ImageFormat`: Supported image formats (JPG, PNG, WEBP)
- `ImageDimensions`: Width and height
- `ImageType`: user_photo, clothing_photo, generated_result
- `ImageSize`: File size in bytes

**Responsibilities**:
- Image upload and validation
- Image storage (local filesystem, future S3)
- Image retrieval and serving
- Metadata management
- Image lifecycle (deletion, cleanup)

**Repository**: `ImageRepository`

#### 3. Generation Domain
**Purpose**: Manage AI generation requests and results

**Entities**:
- `Generation` (Aggregate Root): Generation request and result
- `GenerationRequest`: Initial request details
- `GenerationResult`: Generated image result

**Value Objects**:
- `GenerationStatus`: pending, processing, completed, failed
- `ProcessingTime`: Time taken for generation in milliseconds

**Responsibilities**:
- Creating generation requests
- Managing generation lifecycle
- Tracking generation status
- Handling errors and retries
- Generation history management

**Repository**: `GenerationRepository`

#### 4. AI Service (Infrastructure)
**Purpose**: Integration with Google Gemini 2.5 Flash Image API

**Responsibilities**:
- API communication with Gemini
- Request formatting (user photo + clothing photo)
- Response parsing and validation
- Error handling and retries (max 3 attempts)
- Rate limiting management

**Interface**: `AIServiceInterface` (domain), `GeminiService` (implementation)

### Domain Relationships

```
User (1) ────────> (N) Image
         uploads

User (1) ────────> (N) Generation
         creates

Generation (1) ──> (1) Image (user photo)
               uses

Generation (1) ──> (1) Image (clothing photo)
               uses

Generation (1) ──> (1) Image (result)
           generates
```

### Layer Responsibilities

**Domain Layer**:
- Contains business logic and rules
- Independent of frameworks and infrastructure
- Defines repository interfaces (not implementations)
- No dependencies on outer layers

**Application Layer**:
- Orchestrates use cases
- Coordinates between domains
- Uses domain services and repositories
- Transaction management

**Infrastructure Layer**:
- Implements repository interfaces
- Database access (SQLAlchemy models)
- External service integrations (Gemini API)
- File storage implementations

**Presentation Layer (API)**:
- HTTP request/response handling
- Input validation (Pydantic schemas)
- Authentication/authorization
- API documentation

## Development Guidelines

### Architecture Principles
- **100% Domain-Driven Design**: All business logic in domain layer
- **Dependency Rule**: Dependencies point inward (API → Application → Domain ← Infrastructure)
- **Single Responsibility**: Each class/module has one reason to change
- **Interface Segregation**: Small, focused interfaces for repositories and services
- **Dependency Injection**: Use FastAPI's dependency injection for loose coupling
- **No Cross-Domain Dependencies**: Domains communicate through application services

### Environment Setup
- Use UV for virtual environment management
- Maintain separate virtual environment for backend
- Install packages using UV: `uv add package-name`
- Environment variables accessed from `.env` files
- Never commit `.env.dev` or `.env.prod` to version control

### Database Management

#### SQLAlchemy Models
- **Location**: `app/infrastructure/database/models.py`
- **Convention**: One model per domain entity
- **Relationships**: Use foreign keys for relationships
- **Naming**: Table names are lowercase plural (e.g., `users`, `images`, `generations`)

#### Alembic Migrations
- **All schema changes through migrations** - never modify database directly
- **Migration files location**: `alembic/versions/`
- **Naming convention**: Auto-generated timestamp + descriptive name

#### Migration Commands
```bash
# Create a new migration
alembic revision --autogenerate -m "description of changes"

# Run all pending migrations (upgrade to head)
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# View current migration version
alembic current

# Rollback to specific version
alembic downgrade <revision_id>
```

#### Migration Best Practices
- Always review auto-generated migrations before running
- Test migrations in development before production
- Write both `upgrade()` and `downgrade()` functions
- Keep migrations atomic and focused
- Add indexes for foreign keys and frequently queried fields
- Document complex migrations with comments

### Database Schema

#### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Images Table
```sql
CREATE TABLE images (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    image_type VARCHAR(50) NOT NULL,  -- 'user_photo', 'clothing_photo', 'generated_result'
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(50),
    width INTEGER,
    height INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_images (user_id, created_at)
);
```

#### Generations Table
```sql
CREATE TABLE generations (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user_photo_id UUID NOT NULL REFERENCES images(id),
    clothing_photo_id UUID NOT NULL REFERENCES images(id),
    result_image_id UUID REFERENCES images(id),
    status VARCHAR(20) NOT NULL,  -- 'pending', 'processing', 'completed', 'failed'
    error_message TEXT,
    processing_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    INDEX idx_user_generations (user_id, created_at),
    INDEX idx_status (status)
);
```

### Environment Configuration

#### Environment Files
- **`.env.example`**: Template with all required variables (safe to commit)
- **`.env.dev`**: Development environment configuration (gitignored)
- **`.env.prod`**: Production environment configuration (gitignored)

#### Required Environment Variables
```bash
# Application
APP_NAME=OutfitLens
APP_ENV=development  # or production
DEBUG=true
API_V1_PREFIX=/api/v1

# Database
DATABASE_URL=sqlite:///./outfitlens.db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# File Storage
STORAGE_PATH=./storage
MAX_UPLOAD_SIZE_MB=10
ALLOWED_IMAGE_FORMATS=jpg,jpeg,png,webp

# Google Gemini AI
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash-image
GEMINI_TIMEOUT_SECONDS=30
GEMINI_MAX_RETRIES=3

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

#### Running the Application
```bash
# Development mode (uses .env.dev)
python run_dev.py
# or
uvicorn app.main:app --reload --env-file .env.dev

# Production mode (uses .env.prod)
python run_prod.py
# or
uvicorn app.main:app --host 0.0.0.0 --port 8000 --env-file .env.prod
```

### Code Organization Standards

#### Domain Layer Rules
- No dependencies on infrastructure or application layers
- No framework-specific code (FastAPI, SQLAlchemy, etc.)
- Pure Python classes with business logic
- Define interfaces, not implementations
- Use value objects for data validation

#### Application Layer Rules
- Orchestrate use cases using domain services
- Handle transactions
- Coordinate between multiple domains
- No business logic (delegate to domain services)
- Return DTOs, not domain entities

#### Infrastructure Layer Rules
- Implement repository interfaces from domain layer
- Handle all external dependencies (DB, APIs, file system)
- Convert between domain entities and persistence models
- No business logic

#### API Layer Rules
- Handle HTTP requests/responses only
- Validate input with Pydantic schemas
- Use dependency injection for services
- No business logic (delegate to application services)
- Return consistent response formats

### File Storage Structure
```
storage/
├── user_photos/
│   └── {user_id}/
│       └── {image_id}.{ext}
├── clothing_photos/
│   └── {user_id}/
│       └── {image_id}.{ext}
└── generated_results/
    └── {user_id}/
        └── {generation_id}.{ext}
```

**Storage Guidelines**:
- Organize by user ID for easy cleanup
- Use UUIDs for image filenames to prevent conflicts
- Validate file types and sizes before saving
- Implement cleanup for failed generations
- Future: Abstract storage interface for S3 migration

### Error Handling & Debugging Process

#### Error Handling Strategy
1. **Domain Exceptions**: Create custom exceptions in domain layer
2. **Application Exceptions**: Handle and translate domain exceptions
3. **API Error Responses**: Convert exceptions to HTTP responses
4. **Logging**: Log all errors with context for debugging

#### Custom Exception Hierarchy
```python
# Domain exceptions
class DomainException(Exception): pass
class UserAlreadyExistsError(DomainException): pass
class InvalidImageFormatError(DomainException): pass
class GenerationFailedError(DomainException): pass

# Application exceptions
class ApplicationException(Exception): pass
class AuthenticationError(ApplicationException): pass
class AuthorizationError(ApplicationException): pass

# Infrastructure exceptions
class InfrastructureException(Exception): pass
class DatabaseError(InfrastructureException): pass
class StorageError(InfrastructureException): pass
class ExternalServiceError(InfrastructureException): pass
```

#### Debugging Process
1. **Root Cause Analysis (RCA)**: Identify the underlying issue
2. **Fix Implementation**: Apply the solution
3. **Test Script Creation**: Create test script in `tests/` to verify fix
4. **Iterative Testing**: Test → Fix → Test cycle until resolution
5. **Cleanup**: Delete temporary test scripts after successful resolution

### API Standards

#### Response Format
```python
# Success Response
{
    "success": true,
    "data": { ... },
    "message": "Operation successful"
}

# Error Response
{
    "success": false,
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable error message",
        "details": { ... }
    }
}
```

#### API Versioning
- Use prefix: `/api/v1/`
- Version in URL path
- Maintain backward compatibility within version

#### Authentication
- JWT tokens in `Authorization: Bearer <token>` header
- Access token: 1 hour expiry
- Refresh token: 7 days expiry
- Protected routes use `Depends(get_current_user)`

### Testing Strategy

#### Unit Tests (`tests/unit/`)
- Test domain entities and value objects
- Test domain services
- Test application services (with mocked repositories)
- Test utility functions
- No database or external dependencies

#### Integration Tests (`tests/integration/`)
- Test repository implementations with test database
- Test API endpoints with test client
- Test file storage operations
- Test external service integrations (with mocking)

#### End-to-End Tests (`tests/e2e/`)
- Complete user workflows
- Authentication flows
- Image upload and generation flows
- Error scenarios

#### Testing Commands
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/domain/test_user.py

# Run with coverage
pytest --cov=app --cov-report=html

# Run only unit tests
pytest tests/unit/

# Run with verbose output
pytest -v
```

### Dependencies Management

#### Adding Dependencies
```bash
# Add production dependency
uv add fastapi

# Add development dependency
uv add --dev pytest

# Add with version constraint
uv add "sqlalchemy>=2.0.0,<3.0.0"
```

#### Core Dependencies
- `fastapi` - Web framework
- `uvicorn[standard]` - ASGI server
- `sqlalchemy` - ORM
- `alembic` - Database migrations
- `pydantic` - Data validation
- `python-jose[cryptography]` - JWT handling
- `passlib[bcrypt]` - Password hashing
- `python-multipart` - File upload support
- `google-generativeai` - Gemini API client
- `pillow` - Image processing
- `python-dotenv` - Environment variable management

#### Development Dependencies
- `pytest` - Testing framework
- `pytest-cov` - Test coverage
- `pytest-asyncio` - Async test support
- `httpx` - Test client for FastAPI
- `black` - Code formatting
- `ruff` - Linting
- `mypy` - Type checking

#### Generating requirements.txt
```bash
# UV automatically manages requirements
uv pip compile pyproject.toml -o requirements.txt
```

## Development Workflow

### Initial Setup
1. Clone repository
2. Set up virtual environment: `uv venv`
3. Activate virtual environment: `source .venv/bin/activate`
4. Install dependencies: `uv pip install -r requirements.txt`
5. Copy `.env.example` to `.env.dev` and configure
6. Run initial migration: `alembic upgrade head`
7. Start development server: `python run_dev.py`

### Feature Development
1. Create feature branch from `main`
2. Define domain models and interfaces
3. Implement infrastructure (repositories, external services)
4. Implement application services (use cases)
5. Create API routes and schemas
6. Write tests (unit → integration → e2e)
7. Update documentation
8. Create pull request

### Database Changes
1. Modify SQLAlchemy models in `app/infrastructure/database/models.py`
2. Generate migration: `alembic revision --autogenerate -m "description"`
3. Review generated migration file
4. Test migration: `alembic upgrade head`
5. Test rollback: `alembic downgrade -1`
6. Commit migration file with code changes

### Testing Before Commit
```bash
# Run linter
ruff check .

# Format code
black .

# Type check
mypy app/

# Run tests
pytest

# Check coverage
pytest --cov=app --cov-report=term-missing
```

## Quality Standards

### Code Quality
- Follow PEP 8 style guide
- Use type hints for all functions
- Maximum line length: 100 characters
- Docstrings for all public classes and functions
- No commented-out code in commits

### Architecture Quality
- Respect layer boundaries (no circular dependencies)
- Keep domain layer pure (no framework dependencies)
- Use dependency injection
- Follow SOLID principles
- Keep functions small and focused

### Security Standards
- Never commit secrets or API keys
- Use environment variables for configuration
- Validate all user inputs
- Sanitize file uploads
- Use parameterized queries (SQLAlchemy handles this)
- Implement rate limiting on API endpoints
- Use HTTPS in production
- Hash passwords with bcrypt (min 12 rounds)
- Validate JWT tokens on protected routes

### Performance Standards
- API response time: < 200ms (excluding AI generation)
- Database query time: < 50ms
- Image upload: < 5 seconds for 10MB file
- AI generation: < 10 seconds (target)
- Implement database indexes for foreign keys
- Use pagination for list endpoints (default: 20 items)
- Optimize image sizes before storage

### Documentation Standards
- Keep this file updated with architectural changes
- Document all API endpoints (OpenAPI auto-generated)
- Add comments for complex business logic
- Update PRD for feature changes
- Maintain changelog for releases

## Current Project State

### Implementation Status
- [ ] Project structure created
- [ ] Database setup (SQLite + SQLAlchemy)
- [ ] Alembic migrations configured
- [ ] Domain models defined
- [ ] Infrastructure layer implemented
- [ ] Application services implemented
- [ ] API routes implemented
- [ ] Authentication system
- [ ] Image upload functionality
- [ ] Gemini AI integration
- [ ] Generation workflow
- [ ] Generation history
- [ ] Testing suite
- [ ] Documentation complete

### Next Steps
1. Set up project structure and dependencies
2. Configure database and Alembic
3. Implement User domain and authentication
4. Implement Image domain and storage
5. Implement Generation domain
6. Integrate Gemini AI API
7. Build API endpoints
8. Write comprehensive tests
9. Security hardening
10. Performance optimization

## Reference Documentation
- [PRD (Product Requirements Document)](docs/prd.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Google Gemini API Documentation](https://ai.google.dev/)
- [Domain-Driven Design Principles](https://martinfowler.com/bliki/DomainDrivenDesign.html)

## Notes
- Frontend code is separate (`frontend/` directory)
- Focus exclusively on backend development
- Maintain clean separation between backend and frontend
- Follow RESTful API design principles
- Use SQLite for local development (easy setup, no external dependencies)
- Design with future cloud migration in mind (PostgreSQL, S3)
- Ensure all file paths use forward slashes for cross-platform compatibility
