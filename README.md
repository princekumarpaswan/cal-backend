# 🎯 CoupleCal Backend API

> A production-ready FastAPI backend for family calendar and task management

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791.svg)](https://www.postgresql.org)
[![License](https://img.shields.io/badge/License-Private-red.svg)]()

## 🌟 Features

- ✅ **Authentication** - JWT-based auth with refresh tokens
- ✅ **User Management** - Profile management and settings
- ✅ **Family Groups** - Create and manage family calendars
- ✅ **Events** - Calendar events with recurrence and reminders
- ✅ **Tasks** - Task management with priorities and assignments
- ✅ **RESTful API** - Clean, well-documented endpoints
- ✅ **Async Database** - Fast PostgreSQL operations
- ✅ **Type Safety** - Full Pydantic validation
- ✅ **Docker Ready** - Easy deployment with Docker Compose

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 14+

### Install in 5 Minutes

```bash
# 1. Setup
./setup.sh

# 2. Configure (edit with your database credentials)
cp .env.example .env
nano .env

# 3. Create database
createdb couplecal_db

# 4. Run migrations
./migrate.sh upgrade

# 5. Start server
./run.sh
```

**API is now running at** `http://localhost:8000`  
**Documentation at** `http://localhost:8000/api/docs`

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[📖 INDEX.md](INDEX.md)** | **Start here!** Complete documentation index |
| [⚡ QUICKSTART.md](QUICKSTART.md) | 5-minute setup guide |
| [🔧 DEVELOPMENT.md](DEVELOPMENT.md) | Development workflow & best practices |
| [📡 API_EXAMPLES.md](API_EXAMPLES.md) | cURL examples for all endpoints |
| [📋 PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Complete project overview |
| [📖 BACKEND_README.md](BACKEND_README.md) | Full API specification |

## 🏗️ Architecture

```
MVP Pattern (Model-View-Presenter)
├── Models (app/models/)      - Database models
├── Views (app/api/routes/)   - API endpoints
└── Presenters (app/schemas/) - Data validation
```

## 📡 API Endpoints

### Core Features (25+ Endpoints)

| Category | Endpoints | Description |
|----------|-----------|-------------|
| **Auth** | 7 endpoints | Signup, login, refresh, logout, etc. |
| **User** | 3 endpoints | Profile management |
| **Family** | 4 endpoints | Group management |
| **Events** | 5 endpoints | Calendar events CRUD |
| **Tasks** | 6 endpoints | Task management |

**Interactive API Docs**: Visit `/api/docs` after starting the server

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL + asyncpg
- **ORM**: SQLAlchemy 2.0 (async)
- **Auth**: JWT + bcrypt
- **Validation**: Pydantic v2
- **Migrations**: Alembic
- **Testing**: pytest + httpx
- **Deployment**: Docker + Docker Compose

## 🔐 Security

- ✅ Bcrypt password hashing
- ✅ JWT access & refresh tokens
- ✅ Token expiration (60min access, 7day refresh)
- ✅ CORS configuration
- ✅ Input validation (Pydantic)
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ Role-based access control

## 🐳 Docker Deployment

```bash
# Start all services (PostgreSQL + API + Redis)
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop
docker-compose down
```

## 🧪 Testing

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# With coverage
pytest --cov=app
```

## 📊 Project Stats

- **Total Models**: 8 database models
- **Total Schemas**: 25+ Pydantic schemas
- **Total Endpoints**: 25+ REST endpoints
- **Lines of Code**: 2,500+
- **Test Framework**: ✅ Ready

## 🗄️ Database Schema

```
users → family_groups (many-to-many)
users → events (creator, attendees)
users → tasks (creator, assignee)
events → tasks (linked tasks)
family_groups → events, tasks
```

## 📝 Environment Variables

```bash
# Required
DATABASE_URL=postgresql://user:pass@localhost:5432/couplecal_db
JWT_SECRET_KEY=your-secret-key

# Optional (with defaults)
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
DEBUG=True
```

See [.env.example](.env.example) for complete configuration

## 🚦 Development Workflow

```bash
# Daily development
source venv/bin/activate     # Activate environment
./run.sh                     # Start dev server

# After model changes
./migrate.sh create "desc"   # Create migration
./migrate.sh upgrade         # Apply migration

# Testing
pytest                       # Run tests
```

## 📦 Project Structure

```
backendCoupleCal/
├── app/
│   ├── api/routes/      # API endpoints
│   ├── models/          # Database models
│   ├── schemas/         # Pydantic schemas
│   ├── core/            # Config & security
│   └── db/              # Database connection
├── alembic/             # Migrations
├── tests/               # Test suite
├── main.py              # FastAPI app
└── Docker files
```

## 🎯 API Examples

### Signup
```bash
curl -X POST "http://localhost:8000/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

### Create Event
```bash
curl -X POST "http://localhost:8000/api/events" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Doctor Appointment",
    "startTime": "2025-01-15T14:00:00Z",
    "endTime": "2025-01-15T15:00:00Z"
  }'
```

See [API_EXAMPLES.md](API_EXAMPLES.md) for all examples

## ✅ Production Checklist

Before deploying:

- [ ] Set `DEBUG=False`
- [ ] Generate strong `JWT_SECRET_KEY`
- [ ] Configure production database
- [ ] Set up HTTPS/SSL
- [ ] Update CORS origins
- [ ] Configure email service
- [ ] Set up monitoring
- [ ] Configure backups

## 🔧 Helper Scripts

| Script | Purpose |
|--------|---------|
| `./setup.sh` | Initial project setup |
| `./run.sh` | Start development server |
| `./migrate.sh` | Database migration helper |
| `./verify.sh` | Verify setup is correct |

## 🤝 Support

- **Documentation**: See [INDEX.md](INDEX.md) for complete guide
- **API Docs**: `http://localhost:8000/api/docs`
- **Issues**: Check troubleshooting in [DEVELOPMENT.md](DEVELOPMENT.md)

## 📈 Roadmap

### Completed ✅
- Authentication & user management
- Family groups
- Calendar events with recurrence
- Task management
- Docker deployment

### Planned 🔜
- Voice command processing (AI)
- Image OCR for schedules
- Google Calendar sync
- Email notifications
- Real-time updates

## 📄 License

Private - All rights reserved

---

## 🎉 Getting Started

1. **New to the project?** → Start with [QUICKSTART.md](QUICKSTART.md)
2. **Need complete docs?** → See [INDEX.md](INDEX.md)
3. **Want to develop?** → Read [DEVELOPMENT.md](DEVELOPMENT.md)
4. **Need API examples?** → Check [API_EXAMPLES.md](API_EXAMPLES.md)

**Built with ❤️ using FastAPI, PostgreSQL, and modern Python**

