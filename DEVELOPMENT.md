# CoupleCal Backend - Development Guide

## Project Overview

This is a FastAPI-based backend for the CoupleCal mobile application, implementing a family calendar and task management system with authentication, events, and family groups.

## Architecture

### MVP Pattern (Model-View-Presenter)

- **Models** (`app/models/`): SQLAlchemy database models
- **Views** (`app/api/routes/`): FastAPI route handlers (endpoints)
- **Presenters** (`app/schemas/`): Pydantic schemas for validation and serialization

### Project Structure

```
backendCoupleCal/
├── app/
│   ├── api/
│   │   ├── routes/          # API endpoints (Views)
│   │   │   ├── auth.py      # Authentication endpoints
│   │   │   ├── user.py      # User profile endpoints
│   │   │   ├── family.py    # Family group endpoints
│   │   │   ├── events.py    # Event endpoints
│   │   │   └── tasks.py     # Task endpoints
│   │   ├── dependencies.py  # Dependency injection
│   │   └── exceptions.py    # Custom exceptions
│   ├── core/
│   │   ├── config.py        # Configuration management
│   │   └── security.py      # Security utilities (JWT, hashing)
│   ├── db/
│   │   └── database.py      # Database connection and session
│   ├── models/
│   │   └── models.py        # SQLAlchemy models (Models)
│   ├── schemas/             # Pydantic schemas (Presenters)
│   │   ├── auth.py
│   │   ├── event.py
│   │   ├── family.py
│   │   └── task.py
│   └── utils.py             # Utility functions
├── alembic/                 # Database migrations
├── tests/                   # Test suite
├── main.py                  # FastAPI application entry point
└── requirements.txt         # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- pip and virtualenv

### Initial Setup

1. **Clone and setup**:
```bash
chmod +x setup.sh run.sh migrate.sh
./setup.sh
```

2. **Configure environment**:
```bash
# Edit .env file with your settings
nano .env

# Required settings:
# - DATABASE_URL
# - JWT_SECRET_KEY
```

3. **Create database**:
```bash
createdb couplecal_db
```

4. **Run migrations**:
```bash
./migrate.sh upgrade
```

5. **Start development server**:
```bash
./run.sh
```

The API will be available at `http://localhost:8000`

## Development Workflow

### Adding a New Feature

1. **Create or modify models** (`app/models/models.py`)
2. **Create schemas** (`app/schemas/`)
3. **Create migration**:
   ```bash
   ./migrate.sh create "add_new_feature"
   ```
4. **Apply migration**:
   ```bash
   ./migrate.sh upgrade
   ```
5. **Implement endpoints** (`app/api/routes/`)
6. **Write tests** (`tests/`)
7. **Test manually** using API docs at `/api/docs`

### Database Migrations

```bash
# Create new migration
./migrate.sh create "description_of_changes"

# Apply migrations
./migrate.sh upgrade

# Rollback one version
./migrate.sh downgrade

# Check current version
./migrate.sh current

# View history
./migrate.sh history
```

### Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## API Development

### Authentication Flow

1. User signs up → receives access token + refresh token
2. Access token expires in 60 minutes
3. Use refresh token to get new access token
4. Refresh token expires in 7 days

### Adding a New Endpoint

Example: Add a "Get User Statistics" endpoint

1. **Define schema** (`app/schemas/user_stats.py`):
```python
from pydantic import BaseModel

class UserStatsResponse(BaseModel):
    totalEvents: int
    totalTasks: int
    completedTasks: int
```

2. **Add route** (`app/api/routes/user.py`):
```python
@router.get("/stats", response_model=UserStatsResponse)
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Implementation here
    pass
```

3. **Test**:
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/user/stats
```

### Error Handling

Use custom exceptions from `app/api/exceptions.py`:

```python
from app.api.exceptions import (
    ValidationException,
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
    ConflictException,
)

# Example
if not user:
    raise NotFoundException("User not found")
```

### Database Queries

Always use async/await:

```python
from sqlalchemy import select
from app.models.models import User

# Get single record
result = await db.execute(
    select(User).where(User.id == user_id)
)
user = result.scalar_one_or_none()

# Get multiple records
result = await db.execute(
    select(User).where(User.email.like('%@example.com'))
)
users = result.scalars().all()

# Join tables
result = await db.execute(
    select(User, FamilyGroup)
    .join(family_members)
    .where(family_members.c.user_id == user_id)
)
```

## Security Best Practices

1. **Password Hashing**: Always use `get_password_hash()` from `app/core/security.py`
2. **JWT Tokens**: Use `create_access_token()` and `create_refresh_token()`
3. **Authentication**: Use `get_current_user` dependency for protected routes
4. **Input Validation**: Pydantic schemas validate all input automatically
5. **SQL Injection**: SQLAlchemy ORM prevents SQL injection
6. **CORS**: Configured in `main.py`, update for production

## Environment Variables

Key environment variables:

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# JWT
JWT_SECRET_KEY=your-secret-key  # Use strong random string
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# API
DEBUG=True  # Set to False in production
API_V1_PREFIX=/api
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

## Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### Manual Deployment

1. Set `DEBUG=False` in production
2. Use strong `JWT_SECRET_KEY`
3. Configure production database
4. Set up HTTPS/SSL
5. Use a process manager (systemd, supervisor)
6. Set up monitoring and logging

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Generate strong `JWT_SECRET_KEY`
- [ ] Configure production database
- [ ] Set up SSL/TLS
- [ ] Configure CORS for your frontend domain
- [ ] Set up logging and monitoring
- [ ] Configure rate limiting
- [ ] Set up automated backups
- [ ] Configure email service (SMTP)
- [ ] Set up Redis for caching (optional)

## API Documentation

Once running, access interactive API documentation:

- **Swagger UI**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`
- **OpenAPI JSON**: `http://localhost:8000/api/openapi.json`

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
pg_isready

# Test connection
psql -h localhost -U your_user -d couplecal_db
```

### Migration Issues

```bash
# Reset migrations (WARNING: deletes all data)
./migrate.sh reset

# Check current migration state
./migrate.sh current
```

### Import Errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for functions
- Keep functions focused and small
- Use async/await for database operations

## Contributing

1. Create a feature branch
2. Write tests for new features
3. Ensure all tests pass
4. Update documentation
5. Submit pull request

## Support

For questions or issues:
- Check the API documentation at `/api/docs`
- Review `API_EXAMPLES.md` for cURL examples
- See `BACKEND_README.md` for API specification

## License

Private - All rights reserved

