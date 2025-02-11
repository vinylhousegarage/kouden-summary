#!/bin/sh

if [ ! -d "migrations" ]; then
    echo "Initializing database migration..."
    flask db init
    flask db migrate -m "Initial migration"
fi

echo "Applying database migrations..."
flask db upgrade

echo "Starting Flask development server..."
exec flask run --host=0.0.0.0 --port=5000
