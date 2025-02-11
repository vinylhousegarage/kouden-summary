#!/bin/sh

if [ ! -d "migrations" ]; then
    echo "Initializing database migration..."
    flask db init
    flask db migrate -m "Initial migration"
fi

echo "Applying database migrations..."
flask db upgrade

echo "Starting Gunicorn..."
exec gunicorn -b 0.0.0.0:5000 app:create_app
