#!/usr/bin/env bash

docker-compose exec -u django rest python3 manage.py $*
