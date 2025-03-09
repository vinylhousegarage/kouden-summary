#!/bin/bash
set -e

if [ ! -d "migrations" ] || [ ! -d "migrations/versions" ]; then
    echo "🔧 No migration files found, initializing..."
    flask db init || true
    flask db migrate -m "Initial migration" || true
fi

echo "📌 Applying database migrations..."
flask db upgrade || { echo "❌ Database migration failed!"; exit 1; }

echo "🚀 Starting flask..."
exec flask run --host=0.0.0.0 --port=5000
