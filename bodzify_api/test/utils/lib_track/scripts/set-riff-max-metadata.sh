#!/bin/bash

# Test file path
FILE="$1"

if [ -z "$FILE" ]; then
    echo "Usage: ./set-riff-max-metadata.sh <filename>"
    exit 1
fi

# Resolve the file path and check if file exists
RESOLVED_FILE=$(readlink -f "$FILE")
if [ ! -f "$RESOLVED_FILE" ]; then
    echo "Error: File not found: $FILE"
    exit 1
fi

# Check if required tools are available
for cmd in wavpack wvunpack; do
    if ! command -v $cmd &> /dev/null; then
        echo "Error: $cmd is required but not installed."
        echo "Please install: wavpack"
        exit 1
    fi
done

# Maximum lengths for RIFF INFO chunks
# These are conservative estimates based on common implementations
MAX_TEXT=256    # Conservative max for text fields
MAX_COMMENT=1024 # Longer text for comments
MAX_URL=512     # URL length

# Create max length strings for different fields
# Using different characters for each field to make them distinguishable
ARTIST=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
TITLE=$(printf 'b%.0s' $(seq 1 $MAX_TEXT))
ALBUM=$(printf 'c%.0s' $(seq 1 $MAX_TEXT))
COMMENT=$(printf 'd%.0s' $(seq 1 $MAX_COMMENT))
GENRE=$(printf 'e%.0s' $(seq 1 $MAX_TEXT))
COPYRIGHT=$(printf 'f%.0s' $(seq 1 $MAX_TEXT))
SOFTWARE=$(printf 'g%.0s' $(seq 1 $MAX_TEXT))
ENGINEER=$(printf 'h%.0s' $(seq 1 $MAX_TEXT))
SOURCE=$(printf 'i%.0s' $(seq 1 $MAX_TEXT))
KEYWORDS=$(printf 'j%.0s' $(seq 1 $MAX_TEXT))
TECHNICIAN=$(printf 'k%.0s' $(seq 1 $MAX_TEXT))
URL=$(printf 'l%.0s' $(seq 1 $MAX_URL))

# Fixed length fields
YEAR="2024"
CREATION_DATE="2024-03-01"
ARCHIVAL_LOCATION="TEST-ARCHIVE-001"
MEDIUM="Digital Audio File"
SUBJECT="Test Subject"

echo "Setting metadata for: $RESOLVED_FILE"

# Create a temporary WavPack file
TEMP_WV=$(mktemp).wv
wavpack -w "IART=$ARTIST" \
    -w "INAM=$TITLE" \
    -w "IPRD=$ALBUM" \
    -w "ICMT=$COMMENT" \
    -w "IGNR=$GENRE" \
    -w "ICOP=$COPYRIGHT" \
    -w "ISFT=$SOFTWARE" \
    -w "IENG=$ENGINEER" \
    -w "ISRC=$SOURCE" \
    -w "IKEY=$KEYWORDS" \
    -w "ITCH=$TECHNICIAN" \
    -w "ICRD=$CREATION_DATE" \
    -w "IYER=$YEAR" \
    -w "IARL=$ARCHIVAL_LOCATION" \
    -w "IMED=$MEDIUM" \
    -w "ISBJ=$SUBJECT" \
    "$RESOLVED_FILE" -o "$TEMP_WV"

if [ $? -ne 0 ]; then
    echo "Error: Failed to write metadata"
    rm -f "$TEMP_WV"
    exit 1
fi

# Convert back to WAV
wvunpack "$TEMP_WV" -o "$RESOLVED_FILE"

if [ $? -ne 0 ]; then
    echo "Error: Failed to convert back to WAV"
    rm -f "$TEMP_WV"
    exit 1
fi

# Clean up temporary file
rm -f "$TEMP_WV"

# Verification section
echo -e "\nVerifying metadata using wvunpack:"
wvunpack -s "$RESOLVED_FILE"

# Additional verification for specific fields
echo -e "\nVerifying specific fields:"
for tag in IART INAM IPRD ICMT IGNR ICOP; do
    echo -n "Checking $tag: "
    wvunpack -s "$RESOLVED_FILE" | grep "$tag" || echo "Not found!"
done

echo -e "\nMetadata setting completed successfully!"