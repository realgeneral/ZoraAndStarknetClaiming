#!/bin/bash

pip install --no-cache-dir --upgrade -r requirements.txt

while true; do
    python3 -m app.main
    exit_code=$?
    if [ $exit_code -eq 0 ]; then
        exit
    else
        sleep 2
    fi
done