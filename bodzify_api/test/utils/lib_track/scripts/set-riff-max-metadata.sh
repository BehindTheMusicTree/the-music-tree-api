#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <wav_file>"
    exit 1
fi

WAV_FILE="$1"

# Validate input file
if [ ! -f "$WAV_FILE" ]; then
    echo "Error: File not found: $WAV_FILE"
    exit 1
fi

# Check if it's a valid WAV file
if ! head -c 4 "$WAV_FILE" | grep -q "RIFF"; then
    echo "Error: Not a valid RIFF/WAV file"
    exit 1
fi

# Standard RIFF INFO metadata values
TITLE="Test Title"
ARTIST="Test Artist"
ALBUM="Test Album"
GENRE="Rock"
YEAR="2024"
COMMENT="Test Comment"

# Use bwfmetaedit to set all metadata fields
bwfmetaedit \
    --INAM="$TITLE" \
    --IART="$ARTIST" \
    --IPRD="$ALBUM" \
    --IGNR="$GENRE" \
    --ICRD="$YEAR" \
    --ICMT="$COMMENT" \
    "$WAV_FILE"

if [ $? -eq 0 ]; then
    echo "RIFF INFO tags written successfully"
else
    echo "Error: Failed to write RIFF INFO tags"
    exit 1
fi