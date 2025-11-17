#!/bin/bash

# Database Migration Helper Script

case "$1" in
    create)
        echo "📝 Creating new migration: $2"
        alembic revision --autogenerate -m "$2"
        ;;
    upgrade)
        echo "⬆️  Upgrading database to latest version..."
        alembic upgrade head
        ;;
    downgrade)
        echo "⬇️  Downgrading database by 1 version..."
        alembic downgrade -1
        ;;
    current)
        echo "📊 Current database version:"
        alembic current
        ;;
    history)
        echo "📜 Migration history:"
        alembic history
        ;;
    reset)
        echo "🔄 Resetting database (WARNING: This will delete all data!)"
        read -p "Are you sure? (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            alembic downgrade base
            alembic upgrade head
            echo "✅ Database reset complete"
        else
            echo "❌ Reset cancelled"
        fi
        ;;
    *)
        echo "Usage: $0 {create|upgrade|downgrade|current|history|reset} [migration_name]"
        echo ""
        echo "Commands:"
        echo "  create <name>  - Create a new migration"
        echo "  upgrade        - Upgrade to latest version"
        echo "  downgrade      - Downgrade by one version"
        echo "  current        - Show current version"
        echo "  history        - Show migration history"
        echo "  reset          - Reset database (WARNING: deletes all data)"
        exit 1
        ;;
esac

