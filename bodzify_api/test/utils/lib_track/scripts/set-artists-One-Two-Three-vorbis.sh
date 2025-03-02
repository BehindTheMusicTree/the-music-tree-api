#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <flac_file>"
    exit 1
fi

# Resolve the file path and check if file exists
FLAC_FILE=$(readlink -f "$1")
if [ ! -f "$FLAC_FILE" ]; then
    echo "Error: File not found: $1"
    exit 1
fi

# Check if metaflac is available
if ! command -v metaflac &> /dev/null; then
    echo "Error: metaflac is required but not installed."
    exit 1
fi

echo "Setting artists metadata for: $FLAC_FILE"

# First remove any existing ARTIST tags to avoid duplicates
metaflac --remove-tag=ARTIST "$FLAC_FILE"

# Set three specific artists using separate ARTIST tags
metaflac \
    --set-tag="ARTIST=One" \
    --set-tag="ARTIST=Two" \
    --set-tag="ARTIST=Three" \
    "$FLAC_FILE"

RESULT=$?
if [ $RESULT -eq 0 ]; then
    echo "Artists metadata set successfully!"
    # Verify the changes
    echo "Current artists metadata:"
    metaflac --list --tag=ARTIST "$FLAC_FILE"
else
    echo "Error: Failed to write artists metadata (exit code: $RESULT)"
    exit 1
fi