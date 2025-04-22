#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Usage: $0 <grammar_file> <text_file> [possible_keys]"
    exit 1
fi

GRAMMAR_FILE="$1"
TEXT_FILE="$2"
KEYS="${3:-unknown}"

python3 detector.py "$GRAMMAR_FILE" "$TEXT_FILE" "$KEYS"
