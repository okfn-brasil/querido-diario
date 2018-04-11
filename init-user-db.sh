#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER anonymous;
    GRANT ALL PRIVILEGES ON DATABASE gazette TO anonymous;
EOSQL
