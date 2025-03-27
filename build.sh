#!/bin/bash
if [ -z "$1" ]; then
    echo "Error: No target supplied. Please provide a directory name."
    return 1
fi

if [ -z "$2" ]; then
    echo "Error: No minor revision supplied. Please provide an int."
    return 1
fi

cd "$1" || { echo "Failed to change directory to $1"; exit 1; }

echo "copying book_runner.py from ../datastack/Papermill/book_runner.py"
cp ../../datastack/Papermill/book_runner.py .

docker login

docker compose build

echo 'pushing...'
docker tag "$1-base" "tfds/$1-base:1.0"
docker push "tfds/$1-base:1.0"

docker tag "$1-base" "tfds/$1-base:1.0.$2"
docker push "tfds/$1-base:1.0.$2"

cd ..