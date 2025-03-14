#!/bin/bash
set -e

echo "🔍 Checking for migration files..."
if [ ! -d "migrations" ] || [ ! -d "migrations/versions" ]; then
    echo "🔧 No migration files found, initializing..."
    flask db init || true
fi

echo "📌 Checking for model changes..."
flask db migrate -m "Auto migration from entrypoint" || true

echo "📌 Applying database migrations..."
flask db upgrade || { echo "❌ Database migration failed!"; exit 1; }

echo "🚀 Starting flask..."
exec flask run --host=0.0.0.0 --port=5000
