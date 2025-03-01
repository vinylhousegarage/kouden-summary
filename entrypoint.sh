#!/bin/bash
set -e

if [ ! -d "migrations" ] || [ ! -d "migrations/versions" ]; then
    echo "Database migration files not found!"
    echo "Run 'flask db init' and 'flask db migrate' in development to generate migrations."
    echo "Then apply them in production with 'flask db upgrade'."
    exit 1
fi

echo "Applying database migrations..."
if ! flask db upgrade; then
    echo "Database migration failed! Exiting..."
    exit 1
fi

echo "Starting flask run..."
exec flask run --host=0.0.0.0 --port=5000
