#!/usr/bin/env bash
set -u

. env.sh

if [ -z "$PWD" ]; then
    echo "Check env.sh values are set"
    exit 1
fi

DIR=$(cd "$(dirname "$0")" && pwd)

echo "Cleaning database"
mysql -p"$PWD" -u "$USER" "$DB" < sla.sql

