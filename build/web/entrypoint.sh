#!/usr/bin/env bash

init() {
    flask init-db
}

if [ "$1" == "run" ]; then
    [ -f instance/${DATABASE_URL} ] || init
    exec flask run -h 0.0.0.0
elif [ "$1" == "debug" ]; then
    [ -f instance/${DATABASE_URL} ] || init
    exec flask run -h 0.0.0.0
elif [ "$1" == "init" ]; then
    init
else
    exec "$@"
fi
