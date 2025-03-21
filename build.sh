#!/bin/bash
if [ -z "$1" ]; then
    echo "Error: No argument supplied. Please provide a directory name."
    exit 1
fi

cd "$1" || { echo "Failed to change directory to $1"; exit 1; }

docker login

docker compose build

docker tag "$1-base" "$1-base:1.0"

docker push "tfds/$1-base:1.0"

cd ..