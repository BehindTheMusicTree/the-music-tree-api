#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <wav_file>"
    exit 1
fi

# Resolve the file path and check if file exists
WAV_FILE=$(readlink -f "$1")
if [ ! -f "$WAV_FILE" ]; then
    echo "Error: File not found: $1"
    exit 1
fi

# Check if bwfmetaedit is available
if ! command -v bwfmetaedit &> /dev/null; then
    echo "Error: bwfmetaedit is required but not installed."
    exit 1
fi

# Check if it's a valid WAV file
if ! head -c 4 "$WAV_FILE" | grep -q "RIFF"; then
    echo "Error: Not a valid RIFF/WAV file"
    exit 1
fi

# Generate a string of 'a' characters for maximum length testing
STRING_BIG_LENGTH=$(printf 'a%.0s' {1..1000}) # 1000 to test truncation

echo "Setting metadata for: $WAV_FILE"

# Use bwfmetaedit to set all available RIFF INFO metadata fields
# Note: Removed trailing backslashes which could cause issues
bwfmetaedit \
    --INAM="$STRING_BIG_LENGTH" \
    --IART="$STRING_BIG_LENGTH" \
    --IPRD="$STRING_BIG_LENGTH" \
    --IGNR="$STRING_BIG_LENGTH" \
    --ICRD="9999" \
    --ICMT="$STRING_BIG_LENGTH" \
    --ISFT="$STRING_BIG_LENGTH" \
    --ICOP="$STRING_BIG_LENGTH" \
    --IENG="$STRING_BIG_LENGTH" \
    --ITCH="$STRING_BIG_LENGTH" \
    --ISRC="USXXX9999999" \
    --ISBJ="$STRING_BIG_LENGTH" \
    --IKEY="$STRING_BIG_LENGTH" \
    --IMED="$STRING_BIG_LENGTH" \
    --ICMS="$STRING_BIG_LENGTH" \
    --ITRK="99" \
    --IARL="$STRING_BIG_LENGTH" \
    --ILOC="$STRING_BIG_LENGTH" \
    "$WAV_FILE"

RESULT=$?
if [ $RESULT -eq 0 ]; then
    echo "All RIFF INFO tags written successfully with maximum length values"
    echo "Metadata setting completed successfully!"
else
    echo "Error: Failed to write RIFF INFO tags (exit code: $RESULT)"
    exit 1
fi