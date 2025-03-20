#!/bin/bash
set -e

echo "⏳ Waiting for MariaDB to be ready..."
until mariadb-admin ping -h db -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}" --silent; do
    echo "Waiting for MariaDB..."
    sleep 5
done
echo "✅ MariaDB is ready!"

if [ ! -d "migrations" ] || [ ! -d "migrations/versions" ]; then
    echo "❌ Error: Migration files are missing!"
    echo "💡 Make sure to generate migrations in development and commit them."
    exit 1
fi

echo "🔹 Altering 'sessions' table to use MEDIUMBLOB..."
mariadb -h db -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}" "${MYSQL_DATABASE}" -e "ALTER TABLE sessions MODIFY data MEDIUMBLOB;"

echo "📌 Applying database migrations..."
flask db upgrade || { echo "❌ Database migration failed!"; exit 1; }

echo "🚀 Starting flask..."
exec flask run --host=0.0.0.0 --port=5000
