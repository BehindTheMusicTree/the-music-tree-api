#!/bin/bash

# Test file path
FILE="$1"

if [ -z "$FILE" ]; then
    echo "Usage: ./set-id3v2-max-metadata.sh <filename>"
    exit 1
fi

# Resolve the file path and check if file exists
RESOLVED_FILE=$(readlink -f "$FILE")
if [ ! -f "$RESOLVED_FILE" ]; then
    echo "Error: File not found: $FILE"
    exit 1
fi

# Check if required tools are available
for cmd in mid3v2 mutagen-inspect; do
    if ! command -v $cmd &> /dev/null; then
        echo "Error: $cmd is required but not installed."
        echo "Please install: python-mutagen"
        exit 1
    fi
done

# Check for optional ImageMagick
HAS_IMAGEMAGICK=0
if command -v convert &> /dev/null; then
    HAS_IMAGEMAGICK=1
fi

# Maximum lengths for ID3v2 frames
TEXT_BIG_LENGTH=1000     # Text length to test truncation
MAX_COMMENT=4000 # Maximum comment length
MAX_URL=2000     # Maximum URL length

# Create max length strings for different fields
# Using different characters for each field to make them distinguishable
ARTIST=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
ALBUM_ARTIST=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
TITLE=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
SUBTITLE=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
ALBUM=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
COMPOSER=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
COMMENT=$(printf 'a%.0s' $(seq 1 $MAX_COMMENT))
GENRE=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
COPYRIGHT=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
ENCODED_BY=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
ORIGINAL_ARTIST=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
PUBLISHER=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
CONDUCTOR=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
REMIXER=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
MOOD=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
LYRICS=$(printf 'a%.0s' $(seq 1 $MAX_COMMENT))
URL=$(printf 'a%.0s' $(seq 1 $MAX_URL))
ISRC="USXXX9999999"  # Maximum ISRC format

# Fixed length fields with maximum values
YEAR="9999"                    # Maximum 4-digit year
TRACK="99/99"                  # Maximum track number/total
DISC="99/99"                   # Maximum disc number/total
BPM="999"                      # Maximum reasonable BPM
LANGUAGE="eng"                 # Standard language code
RECORDING_DATE="9999-12-31"    # Maximum date
ORIGINAL_RELEASE="9999-12-31"  # Maximum date
MEDIA_TYPE="DIG"              # Digital Media
RATING="255"                   # Maximum rating (8-bit)

echo "Setting metadata for: $RESOLVED_FILE"

# Write basic metadata tags
mid3v2 \
    --artist="$ARTIST" \
    --album="$ALBUM" \
    --song="$TITLE" \
    --comment="$COMMENT" \
    --genre="$GENRE" \
    --year="$YEAR" \
    --track="$TRACK" \
    "$RESOLVED_FILE"

if [ $? -ne 0 ]; then
    echo "Error: Failed to write basic metadata"
    exit 1
fi

# Write extended metadata tags
mid3v2 \
    --TXXX "MOOD:$MOOD" \
    --TXXX "SUBTITLE:$SUBTITLE" \
    --TXXX "ISRC:$ISRC" \
    --TXXX "CONDUCTOR:$CONDUCTOR" \
    --TXXX "REMIXER:$REMIXER" \
    --TXXX "MEDIA_TYPE:$MEDIA_TYPE" \
    --TPE2 "$ALBUM_ARTIST" \
    --TCOM "$COMPOSER" \
    --TCOP "$COPYRIGHT" \
    --TENC "$ENCODED_BY" \
    --TBPM "$BPM" \
    --TOPE "$ORIGINAL_ARTIST" \
    --TPUB "$PUBLISHER" \
    --TPOS "$DISC" \
    --TLAN "$LANGUAGE" \
    --TIT3 "$SUBTITLE" \
    --WXXX "$URL" \
    --TDRC "$RECORDING_DATE" \
    --TDOR "$ORIGINAL_RELEASE" \
    --USLT "eng:$LYRICS" \
    "$RESOLVED_FILE"

if [ $? -ne 0 ]; then
    echo "Error: Failed to write extended metadata"
    exit 1
fi

# Set ratings (both as POPM and custom TXXX frame)
mid3v2 \
    --POPM "Windows Media Player 9 Series:255" \
    --TXXX "RATING:$RATING" \
    "$RESOLVED_FILE"

if [ $? -ne 0 ]; then
    echo "Error: Failed to write rating metadata"
    exit 1
fi

# Add cover art if ImageMagick is available
if [ $HAS_IMAGEMAGICK -eq 1 ]; then
    echo "ImageMagick detected, adding test cover art..."
    TEMP_IMAGE=$(mktemp).jpg
    convert -size 1200x1200 xc:white -pointsize 20 -gravity center \
        -draw "text 0,0 'Test Cover Art'" "$TEMP_IMAGE"
    
    mid3v2 --APIC "$TEMP_IMAGE" "$RESOLVED_FILE"
    
    if [ $? -ne 0 ]; then
        echo "Warning: Failed to write cover art"
    fi
    
    rm -f "$TEMP_IMAGE"
else
    echo "Note: ImageMagick not found - skipping cover art test"
fi

# Verification section
echo -e "\nVerifying metadata using mid3v2:"
mid3v2 -l "$RESOLVED_FILE"

echo -e "\nVerifying metadata using mutagen-inspect:"
mutagen-inspect "$RESOLVED_FILE"

# Additional verification for specific fields
echo -e "\nVerifying specific fields:"
for tag in MOOD ISRC CONDUCTOR REMIXER MEDIA_TYPE RATING; do
    echo -n "Checking $tag: "
    mid3v2 -l "$RESOLVED_FILE" | grep "$tag" || echo "Not found!"
done

if [ $HAS_IMAGEMAGICK -eq 1 ]; then
    echo -e "\nVerifying cover art presence:"
    mid3v2 -l "$RESOLVED_FILE" | grep "APIC" || echo "Cover art not found!"
fi

echo -e "\nMetadata setting completed successfully!"