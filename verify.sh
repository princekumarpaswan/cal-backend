#!/bin/bash

# CoupleCal Backend - Setup Verification Script

echo "🔍 CoupleCal Backend Setup Verification"
echo "========================================"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check functions
check_pass() {
    echo -e "${GREEN}✓${NC} $1"
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# 1. Check Python version
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    if [ "$(printf '%s\n' "3.10" "$PYTHON_VERSION" | sort -V | head -n1)" = "3.10" ]; then
        check_pass "Python $PYTHON_VERSION (✓ >= 3.10)"
    else
        check_fail "Python $PYTHON_VERSION (requires >= 3.10)"
    fi
else
    check_fail "Python 3 not found"
fi
echo ""

# 2. Check PostgreSQL
echo "Checking PostgreSQL..."
if command -v psql &> /dev/null; then
    PG_VERSION=$(psql --version | awk '{print $3}')
    check_pass "PostgreSQL $PG_VERSION installed"
    
    # Check if server is running
    if pg_isready &> /dev/null; then
        check_pass "PostgreSQL server is running"
    else
        check_warn "PostgreSQL server is not running"
    fi
else
    check_fail "PostgreSQL not found"
fi
echo ""

# 3. Check virtual environment
echo "Checking virtual environment..."
if [ -d "venv" ]; then
    check_pass "Virtual environment exists"
else
    check_warn "Virtual environment not found (run ./setup.sh)"
fi
echo ""

# 4. Check environment file
echo "Checking configuration..."
if [ -f ".env" ]; then
    check_pass ".env file exists"
    
    # Check if important variables are set
    if grep -q "DATABASE_URL=postgresql://" .env; then
        check_pass "DATABASE_URL configured"
    else
        check_warn "DATABASE_URL not configured in .env"
    fi
    
    if grep -q "JWT_SECRET_KEY=" .env && ! grep -q "JWT_SECRET_KEY=your-secret-key" .env; then
        check_pass "JWT_SECRET_KEY configured"
    else
        check_warn "JWT_SECRET_KEY not changed from default"
    fi
else
    check_fail ".env file not found (copy from .env.example)"
fi
echo ""

# 5. Check project structure
echo "Checking project structure..."
REQUIRED_DIRS=("app" "app/api" "app/models" "app/schemas" "alembic" "tests")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        check_pass "$dir/ exists"
    else
        check_fail "$dir/ not found"
    fi
done
echo ""

# 6. Check scripts
echo "Checking scripts..."
SCRIPTS=("setup.sh" "run.sh" "migrate.sh")
for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        if [ -x "$script" ]; then
            check_pass "$script is executable"
        else
            check_warn "$script exists but not executable (run: chmod +x $script)"
        fi
    else
        check_fail "$script not found"
    fi
done
echo ""

# 7. Check dependencies
echo "Checking dependencies..."
if [ -f "requirements.txt" ]; then
    check_pass "requirements.txt exists"
    
    if [ -d "venv" ]; then
        # Activate venv and check if packages are installed
        source venv/bin/activate 2>/dev/null
        if python -c "import fastapi" 2>/dev/null; then
            check_pass "FastAPI installed"
        else
            check_warn "FastAPI not installed (run: pip install -r requirements.txt)"
        fi
        
        if python -c "import sqlalchemy" 2>/dev/null; then
            check_pass "SQLAlchemy installed"
        else
            check_warn "SQLAlchemy not installed"
        fi
        deactivate 2>/dev/null
    fi
else
    check_fail "requirements.txt not found"
fi
echo ""

# 8. Check database
echo "Checking database..."
if [ -f ".env" ]; then
    DB_NAME=$(grep DATABASE_URL .env | cut -d'/' -f4 | cut -d'?' -f1)
    if [ ! -z "$DB_NAME" ]; then
        if psql -lqt 2>/dev/null | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
            check_pass "Database '$DB_NAME' exists"
        else
            check_warn "Database '$DB_NAME' not found (run: createdb $DB_NAME)"
        fi
    fi
fi
echo ""

# 9. Check documentation
echo "Checking documentation..."
DOCS=("QUICKSTART.md" "README_SETUP.md" "DEVELOPMENT.md" "API_EXAMPLES.md" "PROJECT_SUMMARY.md")
for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        check_pass "$doc exists"
    else
        check_warn "$doc not found"
    fi
done
echo ""

# Summary
echo "========================================"
echo "📋 Summary"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. If virtual environment missing:"
echo "   ./setup.sh"
echo ""
echo "2. If .env not configured:"
echo "   cp .env.example .env"
echo "   nano .env  # Edit with your settings"
echo ""
echo "3. If database doesn't exist:"
echo "   createdb couplecal_db"
echo ""
echo "4. Run migrations:"
echo "   ./migrate.sh create \"initial_migration\""
echo "   ./migrate.sh upgrade"
echo ""
echo "5. Start the server:"
echo "   ./run.sh"
echo ""
echo "6. Access API docs:"
echo "   http://localhost:8000/api/docs"
echo ""
echo "📚 For more information, see QUICKSTART.md"
echo ""

