#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: ./encode.sh <secret_message> <key>"
    exit 1
fi

SECRET=$1
KEY=$2

python3 generator.py grammar.cfg "$SECRET" "$KEY" > encoded_text.txt
echo "Secret message encoded successfully and saved to encoded_text.txt"
