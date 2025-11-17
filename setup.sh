#!/bin/bash

# CoupleCal Backend Setup Script

echo "🚀 Setting up CoupleCal Backend..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your database credentials and secret keys!"
fi

# Initialize Alembic (if not already initialized)
if [ ! -d "alembic/versions" ]; then
    echo "🗄️  Initializing database migrations..."
    alembic revision --autogenerate -m "Initial migration"
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your PostgreSQL credentials"
echo "2. Create PostgreSQL database: createdb couplecal_db"
echo "3. Run migrations: alembic upgrade head"
echo "4. Start the server: uvicorn main:app --reload"

