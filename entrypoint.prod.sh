#!/bin/bash
set -e

if [ ! -d "migrations" ] || [ ! -d "migrations/versions" ]; then
    echo "❌ Error: Migration files are missing!"
    echo "💡 Make sure to generate migrations in development and commit them."
    exit 1
fi

echo "📌 Applying database migrations..."
flask db upgrade || { echo "❌ Database migration failed!"; exit 1; }

echo "Starting Gunicorn..."
exec gunicorn -w 1 --threads 2 --timeout 90 -b 0.0.0.0:5000 "app:create_app()"
