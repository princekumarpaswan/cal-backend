# 🚀 CoupleCal Backend - Quick Start Guide

## What You've Got

A complete FastAPI backend with:
- ✅ User authentication (JWT)
- ✅ User profiles
- ✅ Family groups
- ✅ Calendar events with recurrence
- ✅ Task management
- ✅ PostgreSQL database
- ✅ Async operations
- ✅ API documentation
- ✅ Docker support
- ✅ Testing setup

## 5-Minute Setup

### Step 1: Install Dependencies

```bash
# Make scripts executable
chmod +x setup.sh run.sh migrate.sh

# Run setup
./setup.sh
```

### Step 2: Configure Database

```bash
# Edit .env file
nano .env

# Update this line:
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/couplecal_db

# Generate a secret key for JWT:
# Run: python3 -c "import secrets; print(secrets.token_urlsafe(32))"
JWT_SECRET_KEY=your-generated-secret-key-here
```

### Step 3: Create Database

```bash
# Create PostgreSQL database
createdb couplecal_db

# Or connect to PostgreSQL and run:
# CREATE DATABASE couplecal_db;
```

### Step 4: Run Migrations

```bash
# Create initial migration
./migrate.sh create "initial_migration"

# Apply migrations
./migrate.sh upgrade
```

### Step 5: Start Server

```bash
./run.sh
```

🎉 **Done!** Your API is running at `http://localhost:8000`

## Test It Out

### 1. Check Health

```bash
curl http://localhost:8000/health
```

### 2. View API Docs

Open in browser: `http://localhost:8000/api/docs`

### 3. Create a User

```bash
curl -X POST "http://localhost:8000/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

### 4. Login

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

Save the `accessToken` from the response!

## Alternative: Docker Setup

If you prefer Docker:

```bash
# Start everything (database + API)
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop
docker-compose down
```

## Project Structure

```
backendCoupleCal/
├── app/                    # Application code
│   ├── api/               # API routes and logic
│   ├── core/              # Config and security
│   ├── db/                # Database setup
│   ├── models/            # Database models
│   └── schemas/           # Pydantic schemas
├── alembic/               # Database migrations
├── tests/                 # Test suite
├── main.py                # FastAPI app
├── requirements.txt       # Dependencies
├── .env                   # Configuration (create from .env.example)
├── setup.sh              # Setup script
├── run.sh                # Run server script
└── migrate.sh            # Migration helper
```

## Common Commands

```bash
# Start server
./run.sh

# Create migration
./migrate.sh create "description"

# Apply migrations
./migrate.sh upgrade

# Rollback migration
./migrate.sh downgrade

# Run tests
pytest

# View migration history
./migrate.sh history
```

## API Endpoints

### Authentication (`/api/auth`)
- `POST /signup` - Register user
- `POST /login` - Login
- `POST /refresh` - Refresh token
- `POST /logout` - Logout

### User (`/api/user`)
- `GET /profile` - Get profile
- `PUT /profile` - Update profile
- `POST /change-password` - Change password

### Family Groups (`/api/family`)
- `POST /groups` - Create group
- `GET /groups` - List groups
- `GET /groups/{id}` - Get group
- `POST /groups/{id}/invite` - Invite member

### Events (`/api/events`)
- `POST /` - Create event
- `GET /` - List events
- `GET /{id}` - Get event
- `PUT /{id}` - Update event
- `DELETE /{id}` - Delete event

### Tasks (`/api/tasks`)
- `POST /` - Create task
- `GET /` - List tasks
- `GET /{id}` - Get task
- `PUT /{id}` - Update task
- `PATCH /{id}/status` - Update status
- `DELETE /{id}` - Delete task

## Documentation Files

- `README_SETUP.md` - Detailed setup instructions
- `DEVELOPMENT.md` - Development guide
- `API_EXAMPLES.md` - cURL examples for all endpoints
- `BACKEND_README.md` - Complete API specification

## Environment Variables

Key settings in `.env`:

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/couplecal_db

# Security
JWT_SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# API
DEBUG=True
API_V1_PREFIX=/api
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:19006"]
```

## Troubleshooting

### "Module not found" error
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Database connection error
```bash
# Check PostgreSQL is running
pg_isready

# Verify credentials in .env match your PostgreSQL setup
```

### Migration errors
```bash
# Check current state
./migrate.sh current

# If needed, reset (WARNING: deletes data)
./migrate.sh reset
```

## Next Steps

1. ✅ **Test the API** - Use the Swagger docs at `/api/docs`
2. ✅ **Connect your frontend** - Update CORS origins in `.env`
3. ✅ **Add features** - See `DEVELOPMENT.md` for guide
4. ✅ **Deploy** - See deployment section in `README_SETUP.md`

## Production Checklist

Before deploying to production:

- [ ] Set `DEBUG=False`
- [ ] Generate strong `JWT_SECRET_KEY`
- [ ] Use production database
- [ ] Configure HTTPS/SSL
- [ ] Update CORS origins
- [ ] Set up monitoring
- [ ] Configure email service
- [ ] Set up backups

## Need Help?

- **API Documentation**: `http://localhost:8000/api/docs`
- **Examples**: See `API_EXAMPLES.md`
- **Development**: See `DEVELOPMENT.md`
- **API Spec**: See `BACKEND_README.md`

---

**Built with FastAPI + PostgreSQL + SQLAlchemy**

Happy coding! 🎉

