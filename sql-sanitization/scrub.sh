#!/bin/bash
set -e

DATE=$(date +%F)

# We stream directly: pg_dump -> stdout -> gsutil -> GCS

echo "Starting streaming masked dump..."

export PGPASSWORD="$POSTGRES_PASSWORD"

# This command creates a PostgreSQL backup and uploads it to Google Cloud Storage.

pg_dump \
  --host="/cloudsql/$CLOUD_SQL_CONNECTION_NAME" \
  --username="$POSTGRES_USER" \
  --dbname="$POSTGRES_DB" \
  --no-security-labels \
  --exclude-extension="anon" \
  --no-owner \
  --format=plain | gsutil cp - "gs://$GCS_BUCKET/sanitized-$DATE.sql"


echo "Stream complete."
