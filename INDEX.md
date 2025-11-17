# 📖 CoupleCal Backend - Documentation Index

Welcome to the CoupleCal Backend documentation! This index will help you find the right documentation for your needs.

## 🚀 Getting Started (Start Here!)

1. **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
   - Quick installation steps
   - Basic testing commands
   - Common operations
   - **Start here if you're new!**

2. **[verify.sh](verify.sh)** - Setup verification script
   - Run `./verify.sh` to check your setup
   - Identifies missing dependencies
   - Provides fix suggestions

## 📚 Complete Guides

### Setup & Installation
- **[README_SETUP.md](README_SETUP.md)** - Detailed setup instructions
  - Prerequisites and requirements
  - Step-by-step installation
  - Project structure overview
  - Available endpoints summary
  - Environment variables reference

### Development
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development workflow guide
  - Architecture overview (MVP pattern)
  - Development workflow
  - Adding new features
  - Database migrations
  - Testing guide
  - Security best practices
  - Deployment checklist

### API Reference
- **[API_EXAMPLES.md](API_EXAMPLES.md)** - cURL examples
  - Complete cURL examples for all endpoints
  - Authentication flow examples
  - User profile examples
  - Family groups examples
  - Events examples
  - Tasks examples

- **[BACKEND_README.md](BACKEND_README.md)** - Complete API specification
  - Detailed endpoint specifications
  - Request/response schemas
  - Validation rules
  - Error codes
  - Database schema recommendations

### Project Overview
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Comprehensive project summary
  - Completed features list
  - Project structure
  - Tech stack details
  - API statistics
  - Production readiness checklist
  - Next steps

## 🛠️ Quick Reference

### Essential Commands

```bash
# Verify setup
./verify.sh

# Initial setup
./setup.sh

# Run server
./run.sh

# Database migrations
./migrate.sh upgrade              # Apply migrations
./migrate.sh create "description" # Create new migration
./migrate.sh downgrade           # Rollback migration

# Testing
pytest                           # Run all tests
pytest -v                        # Verbose output
pytest tests/test_auth.py        # Run specific test

# Docker
docker-compose up -d             # Start all services
docker-compose logs -f api       # View logs
docker-compose down              # Stop services
```

### Key Files Location

```
backendCoupleCal/
├── main.py                    # FastAPI application entry
├── requirements.txt           # Python dependencies
├── .env                       # Configuration (create from .env.example)
├── alembic.ini               # Alembic configuration
│
├── app/
│   ├── api/routes/           # All API endpoints
│   ├── models/models.py      # Database models
│   ├── schemas/              # Pydantic schemas
│   ├── core/config.py        # Settings
│   └── core/security.py      # JWT & hashing
│
└── Documentation Files (this folder)
```

## 📋 Documentation by Use Case

### "I want to..."

#### Set up the project for the first time
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Run `./verify.sh` to check setup
3. Follow any missing steps it identifies

#### Understand the API endpoints
1. Start server: `./run.sh`
2. Visit: `http://localhost:8000/api/docs` (Interactive Swagger UI)
3. Or read: [API_EXAMPLES.md](API_EXAMPLES.md) for cURL examples
4. Full spec: [BACKEND_README.md](BACKEND_README.md)

#### Add a new feature
1. Read [DEVELOPMENT.md](DEVELOPMENT.md) - "Adding a New Feature" section
2. Follow the step-by-step guide
3. Test using Swagger docs

#### Deploy to production
1. Check [DEVELOPMENT.md](DEVELOPMENT.md) - "Deployment" section
2. Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - "Production Readiness"
3. Complete the production checklist

#### Test the API
- **Interactive**: Visit `/api/docs` after starting server
- **Command line**: Use examples from [API_EXAMPLES.md](API_EXAMPLES.md)
- **Automated**: See [DEVELOPMENT.md](DEVELOPMENT.md) - "Running Tests"

#### Understand the architecture
1. [DEVELOPMENT.md](DEVELOPMENT.md) - "Architecture" section
2. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Complete overview
3. [README_SETUP.md](README_SETUP.md) - Project structure

#### Configure for my environment
1. Copy `.env.example` to `.env`
2. Read [README_SETUP.md](README_SETUP.md) - "Environment Variables"
3. Update database and JWT settings

#### Work with database migrations
1. [DEVELOPMENT.md](DEVELOPMENT.md) - "Database Migrations" section
2. Use `./migrate.sh` helper script
3. See Alembic configuration in `alembic.ini`

## 🔍 Quick Links

### API Documentation (when server is running)
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- OpenAPI JSON: http://localhost:8000/api/openapi.json
- Health Check: http://localhost:8000/health

### External Resources
- FastAPI Documentation: https://fastapi.tiangolo.com
- SQLAlchemy Documentation: https://docs.sqlalchemy.org
- Pydantic Documentation: https://docs.pydantic.dev
- Alembic Documentation: https://alembic.sqlalchemy.org

## 📊 Feature Implementation Status

| Feature | Status | Priority | Documentation |
|---------|--------|----------|---------------|
| Authentication | ✅ Complete | P1 | [API_EXAMPLES.md](API_EXAMPLES.md) |
| User Profile | ✅ Complete | P2 | [API_EXAMPLES.md](API_EXAMPLES.md) |
| Family Groups | ✅ Complete | P3 | [API_EXAMPLES.md](API_EXAMPLES.md) |
| Events | ✅ Complete | P4 | [API_EXAMPLES.md](API_EXAMPLES.md) |
| Tasks | ✅ Complete | P5 | [API_EXAMPLES.md](API_EXAMPLES.md) |
| Voice AI | ⏳ Planned | P6 | [BACKEND_README.md](BACKEND_README.md) |
| Image OCR | ⏳ Planned | P7 | [BACKEND_README.md](BACKEND_README.md) |
| Google Calendar | ⏳ Planned | P8 | [BACKEND_README.md](BACKEND_README.md) |

## 🎯 Common Tasks

### First Time Setup
```bash
./verify.sh                          # Check requirements
./setup.sh                           # Setup environment
cp .env.example .env                 # Create config
nano .env                            # Edit configuration
createdb couplecal_db                # Create database
./migrate.sh create "initial"        # Create migration
./migrate.sh upgrade                 # Apply migration
./run.sh                             # Start server
```

### Daily Development
```bash
source venv/bin/activate             # Activate environment
./run.sh                             # Start dev server
# ... make changes ...
./migrate.sh create "my_changes"     # If models changed
./migrate.sh upgrade                 # Apply migration
pytest                               # Run tests
```

### Testing API
```bash
# Start server
./run.sh

# In another terminal
curl http://localhost:8000/health    # Health check

# Use Swagger UI
open http://localhost:8000/api/docs

# Or use cURL examples
# See API_EXAMPLES.md for all examples
```

## 🆘 Troubleshooting

### Something's not working?

1. **Run verification**: `./verify.sh`
2. **Check logs**: Look at terminal output when running `./run.sh`
3. **Common issues**:
   - Database connection: Check `.env` DATABASE_URL
   - Module not found: Run `pip install -r requirements.txt`
   - Migration errors: Check `./migrate.sh current`
4. **Read**: [DEVELOPMENT.md](DEVELOPMENT.md) - "Troubleshooting" section

### Need Help?

1. Check the relevant documentation file above
2. Look at [DEVELOPMENT.md](DEVELOPMENT.md) troubleshooting section
3. Review [API_EXAMPLES.md](API_EXAMPLES.md) for usage examples
4. Check API docs at `/api/docs` when server is running

## 📝 Documentation Maintenance

### For Developers
When adding new features, update:
1. Relevant code files
2. [API_EXAMPLES.md](API_EXAMPLES.md) - Add cURL examples
3. [DEVELOPMENT.md](DEVELOPMENT.md) - If adding new patterns
4. This INDEX.md - If adding new docs

## 🎉 Quick Win Checklist

Perfect for first-time setup:

- [ ] Read [QUICKSTART.md](QUICKSTART.md)
- [ ] Run `./verify.sh`
- [ ] Create `.env` from `.env.example`
- [ ] Update DATABASE_URL and JWT_SECRET_KEY
- [ ] Create database: `createdb couplecal_db`
- [ ] Run `./setup.sh`
- [ ] Run `./migrate.sh upgrade`
- [ ] Start server: `./run.sh`
- [ ] Visit: http://localhost:8000/api/docs
- [ ] Test signup/login from Swagger UI
- [ ] Success! 🎉

---

**Need to get started quickly?** → [QUICKSTART.md](QUICKSTART.md)

**Need complete details?** → [DEVELOPMENT.md](DEVELOPMENT.md)

**Need API examples?** → [API_EXAMPLES.md](API_EXAMPLES.md)

**Need overview?** → [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

Happy coding! 🚀

