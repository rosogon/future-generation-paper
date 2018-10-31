#!/usr/bin/env bash
. env.sh

if [ -z "$PWD" ]; then
    echo "Check env.sh values are set"
    exit 1
fi
killall client.py
killall server.sh
./restoreDatabase.sh

set -x
./server.py "$@" &> server.out &
PID=$!
echo "Server running with PID $PID"
./load-samples-core.sh
./client.sh
kill $PID
