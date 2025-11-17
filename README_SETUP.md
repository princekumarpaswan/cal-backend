# CoupleCal Backend

A FastAPI backend for the CoupleCal mobile application with PostgreSQL database.

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy (async)
- **Authentication**: JWT with bcrypt
- **Migrations**: Alembic
- **Architecture**: MVP (Model-View-Presenter) pattern

## Features

- ✅ User authentication (signup, login, refresh tokens)
- ✅ User profile management
- ✅ Family group management
- ✅ Calendar events with recurrence
- ✅ Task management
- ✅ Role-based access control
- ✅ Async database operations
- ✅ API documentation (Swagger/OpenAPI)

## Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL 14+

### Installation

1. Clone the repository
2. Run setup script:

```bash
chmod +x setup.sh
./setup.sh
```

3. Update `.env` with your database credentials:

```bash
DATABASE_URL=postgresql://username:password@localhost:5432/couplecal_db
JWT_SECRET_KEY=your-secret-key-here
```

4. Create PostgreSQL database:

```bash
createdb couplecal_db
```

5. Run migrations:

```bash
alembic upgrade head
```

6. Start the server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:

- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## Project Structure

```
backendCoupleCal/
├── alembic/              # Database migrations
├── app/
│   ├── api/              # API layer
│   │   ├── routes/       # API endpoints
│   │   ├── dependencies.py
│   │   └── exceptions.py
│   ├── core/             # Core configuration
│   │   ├── config.py
│   │   └── security.py
│   ├── db/               # Database configuration
│   │   └── database.py
│   ├── models/           # SQLAlchemy models
│   │   └── models.py
│   └── schemas/          # Pydantic schemas
│       ├── auth.py
│       ├── event.py
│       ├── family.py
│       └── task.py
├── main.py               # FastAPI application
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
└── alembic.ini          # Alembic configuration

```

## Available Endpoints

### Authentication (`/api/auth`)

- `POST /signup` - Register new user
- `POST /login` - User login
- `POST /refresh` - Refresh access token
- `POST /logout` - User logout
- `POST /forgot-password` - Request password reset
- `POST /reset-password` - Reset password
- `POST /verify-email` - Verify email address

### User Profile (`/api/user`)

- `GET /profile` - Get user profile
- `PUT /profile` - Update user profile
- `POST /change-password` - Change password

### Family Groups (`/api/family`)

- `POST /groups` - Create family group
- `GET /groups` - Get user's family groups
- `GET /groups/{id}` - Get specific group
- `POST /groups/{id}/invite` - Invite member

### Events (`/api/events`)

- `POST /` - Create event
- `GET /` - Get events (with filters)
- `GET /{id}` - Get specific event
- `PUT /{id}` - Update event
- `DELETE /{id}` - Delete event

### Tasks (`/api/tasks`)

- `POST /` - Create task
- `GET /` - Get tasks (with filters)
- `GET /{id}` - Get specific task
- `PUT /{id}` - Update task
- `PATCH /{id}/status` - Update task status
- `DELETE /{id}` - Delete task

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:

- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET_KEY` - Secret key for JWT tokens
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Access token expiration (default: 60)
- `REFRESH_TOKEN_EXPIRE_DAYS` - Refresh token expiration (default: 7)

## Development

### Create a new migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback migration

```bash
alembic downgrade -1
```

## Security Features

- Bcrypt password hashing
- JWT access and refresh tokens
- CORS middleware
- Input validation with Pydantic
- SQL injection protection via SQLAlchemy
- Role-based access control

## License

Private - All rights reserved
