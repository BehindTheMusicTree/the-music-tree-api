#!/bin/bash

# Test file path
FILE="$1"

if [ -z "$FILE" ]; then
    echo "Usage: ./set-id3v2-max-metadata.sh <filename>"
    exit 1
fi

# Maximum lengths for ID3v2 frames
MAX_TEXT=250  # Conservative max for text frames
MAX_COMMENT=4000

# Create long strings
ARTIST=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
TITLE=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
ALBUM=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
COMMENT=$(printf 'a%.0s' $(seq 1 $MAX_COMMENT))
GENRE=$(printf 'a%.0s' $(seq 1 $MAX_COMMENT))
YEAR="2024"
TRACK="1/1"

# Write all metadata using mid3v2
mid3v2 \
    --artist="$ARTIST" \
    --album="$ALBUM" \
    --song="$TITLE" \
    --comment="$COMMENT" \
    --genre="$GENRE" \
    --year="$YEAR" \
    --track="$TRACK" \
    --POPM="Windows Media Player 9 Series:255" \
    "$FILE"

# Verify
mid3v2 -l "$FILE"