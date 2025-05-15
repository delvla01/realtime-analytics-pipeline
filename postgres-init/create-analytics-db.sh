#!/bin/bash
set -e

# Create analytics database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
  CREATE DATABASE analytics;
  GRANT ALL PRIVILEGES ON DATABASE analytics TO $POSTGRES_USER;
EOSQL

# Create clickstream_events table in analytics database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "analytics" <<-EOSQL
  CREATE TABLE IF NOT EXISTS clickstream_events (
    user_id BIGINT,
    event_type VARCHAR(255),
    timestamp DOUBLE PRECISION,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
EOSQL
