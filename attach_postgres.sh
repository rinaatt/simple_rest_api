#!/usr/bin/env bash

docker-compose exec -e COLUMNS=$COLUMNS -e LINES=$LINES -e TERM=$TERM postgres bash
