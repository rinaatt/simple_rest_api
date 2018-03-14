#!/bin/bash
set -e

source /var/opt/parse_url_func.sh
parse_url $DATABASE_URL

psql -U postgres -c "CREATE USER $DB_USER WITH CREATEDB PASSWORD '$DB_PASS'"
psql -U postgres -c "CREATE DATABASE $DB_NAME WITH OWNER = $DB_USER TEMPLATE=template0 ENCODING = UTF8"
