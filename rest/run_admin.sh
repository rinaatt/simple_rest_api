#!/usr/bin/env bash

# python3 manage.py migrate

# python3 manage.py collectstatic --settings='rest_admin.settings' --noinput

python3 manage.py runserver --settings 'rest_admin.settings' --nostatic "rest-admin:8000"
