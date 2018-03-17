#!/usr/bin/env bash

docker-compose exec -u django -e COLUMNS=$COLUMNS -e LINES=$LINES -e TERM=$TERM rest bash
