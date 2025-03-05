#!/bin/bash
set -e

export SECRET_KEY=$(aws ssm get-parameter --name "/param-store/SECRET_KEY" --with-decryption --query "Parameter.Value" --output text)
export AWS_REGION=$(aws ssm get-parameter --name "/param-store/AWS_REGION" --query "Parameter.Value" --output text)
export AWS_COGNITO_USER_POOL_ID=$(aws ssm get-parameter --name "/param-store/AWS_COGNITO_USER_POOL_ID" --query "Parameter.Value" --output text)
export AWS_COGNITO_USER_POOL_CLIENT_ID=$(aws ssm get-parameter --name "/param-store/AWS_COGNITO_USER_POOL_CLIENT_ID" --query "Parameter.Value" --output text)
export COGNITO_DOMAIN=$(aws ssm get-parameter --name "/param-store/COGNITO_DOMAIN" --with-decryption --query "Parameter.Value" --output text)
export COGNITO_CLIENT_ID=$(aws ssm get-parameter --name "/param-store/COGNITO_CLIENT_ID" --query "Parameter.Value" --output text)
export COGNITO_AUTHORITY=$(aws ssm get-parameter --name "/mparam-store/COGNITO_AUTHORITY" --query "Parameter.Value" --output text)
export COGNITO_METADATA_URL=$(aws ssm get-parameter --name "/param-store/COGNITO_METADATA_URL" --query "Parameter.Value" --output text)
export COGNITO_SCOPE=$(aws ssm get-parameter --name "/param-store/COGNITO_SCOPE" --with-decryption --query "Parameter.Value" --output text)
export COGNITO_REDIRECT_URI=$(aws ssm get-parameter --name "/param-store/COGNITO_REDIRECT_URI" --query "Parameter.Value" --output text)

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

echo "Starting Gunicorn..."
exec gunicorn -w 2 -b 0.0.0.0:5000 "app:create_app()"
