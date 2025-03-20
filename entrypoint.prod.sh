#!/bin/bash
set -e

echo "⏳ Waiting for MariaDB to be ready..."
until mariadb-admin ping -h "${DB_HOST}" -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}" --silent --wait=30; do
    echo "Waiting for MariaDB..."
    sleep 5
done
echo "✅ MariaDB is ready!"

if [ ! -d "migrations" ] || [ ! -d "migrations/versions" ]; then
    echo "❌ Error: Migration files are missing!"
    echo "💡 Make sure to generate migrations in development and commit them."
    exit 1
fi

echo "🔹 Checking if 'sessions' table needs modification..."
CURRENT_TYPE=$(mariadb -h "${DB_HOST}" -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}" "${MYSQL_DATABASE}" -e "SHOW COLUMNS FROM sessions WHERE Field='data';" | grep 'MEDIUMBLOB')

if [ -z "$CURRENT_TYPE" ]; then
    echo "🔹 Altering 'sessions' table to use MEDIUMBLOB..."
    mariadb -h "${DB_HOST}" -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}" "${MYSQL_DATABASE}" -e "ALTER TABLE sessions MODIFY data MEDIUMBLOB;"
    echo "✅ MEDIUMBLOB applied!"
else
    echo "✅ 'sessions' table is already using MEDIUMBLOB."
fi

echo "📌 Running database migrations..."
if ! flask db upgrade; then
    echo "❌ Database migration failed!"
    echo "🛠️  Check the logs above for details."
    exit 1
fi

echo "🚀 Starting Gunicorn..."
exec gunicorn -w 1 --threads 2 --timeout 90 -b 0.0.0.0:5000 "app:create_app()"
