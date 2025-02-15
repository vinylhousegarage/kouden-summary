#!/bin/bash

if [ ! -d "migrations/versions" ]; then
    echo "Database migration files not found!"
    echo "Please generate migrations in development and apply them in production."
    exit 1
fi

echo "Applying database migrations..."
if ! flask db upgrade; then
    echo "Database migration failed! Exiting..."
    exit 1
fi

echo "Starting Gunicorn..."
exec gunicorn -b 0.0.0.0:5000 --workers 2 app:create_app
