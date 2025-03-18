#!/bin/sh

if [ "$ENV" = "development" ]; then
  echo "Migrating database"
  /app/.venv/bin/alembic upgrade head
  echo "Running with live reload"
  exec /app/.venv/bin/fastapi dev --host 0.0.0.0 --port ${UVICORN_PORT}
elif [ "$ENV" = "production" ]; then
  echo "Migrating database"
  /app/.venv/bin/alembic upgrade head
  echo "Running on production mode"
  exec /app/.venv/bin/fastapi run --host 0.0.0.0 --port ${UVICORN_PORT}
else
  echo "Unknown environment: $ENV. Exiting."
  exit 1
fi
