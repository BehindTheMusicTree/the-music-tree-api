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

# Generate a string of 'a' characters for maximum length testing
MAX_STRING=$(printf 'a%.0s' {1..256})

# Use bwfmetaedit to set all available RIFF INFO metadata fields
bwfmetaedit \
    --INAM="$MAX_STRING" \
    --IART="$MAX_STRING" \
    --IPRD="$MAX_STRING" \
    --IGNR="$MAX_STRING" \
    --ICRD="$MAX_STRING" \
    --ICMT="$MAX_STRING" \
    --ISFT="$MAX_STRING" \
    --ICOP="$MAX_STRING" \
    --IENG="$MAX_STRING" \
    --ITCH="$MAX_STRING" \
    --ISRC="$MAX_STRING" \
    --ISBJ="$MAX_STRING" \
    --IKEY="$MAX_STRING" \
    --IMED="$MAX_STRING" \
    --ICMS="$MAX_STRING" \
    --ITRK="$MAX_STRING" \
    --IARL="$MAX_STRING" \
    --ILOC="$MAX_STRING" \
    "$WAV_FILE"

if [ $? -eq 0 ]; then
    echo "All RIFF INFO tags written successfully with maximum length values"
else
    echo "Error: Failed to write RIFF INFO tags"
    exit 1
fi