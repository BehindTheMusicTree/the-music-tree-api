#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <audio_file>"
    exit 1
fi

AUDIO_FILE="$1"

# ID3v1 field max lengths
TITLE_MAX=30
ARTIST_MAX=30
ALBUM_MAX=30
YEAR_MAX=4
COMMENT_MAX=28  # 28 for ID3v1.1 to allow track number
TRACK_MAX=1     # Single byte for ID3v1.1
GENRE_MAX=1     # Single byte index

# Create maximum length content
TITLE=$(printf 'a%.0s' $(seq 1 $TITLE_MAX))
ARTIST=$(printf 'a%.0s' $(seq 1 $ARTIST_MAX))
ALBUM=$(printf 'a%.0s' $(seq 1 $ALBUM_MAX))
YEAR="2024"
COMMENT=$(printf 'a%.0s' $(seq 1 $COMMENT_MAX))
TRACK="1"
GENRE="0"  # Blues = 0

# Install id3v2 if needed
command -v id3v2 >/dev/null 2>&1 || {
    echo "id3v2 tool not found. Installing..."
    brew install id3v2
}

# Write ID3v1 tags
id3v2 \
    --comment "$COMMENT" \
    --artist "$ARTIST" \
    --album "$ALBUM" \
    --song "$TITLE" \
    --year "$YEAR" \
    --track "$TRACK" \
    --genre "$GENRE" \
    --id3v1-only \
    "$AUDIO_FILE"

# Verify tags
id3v2 -l "$AUDIO_FILE"
echo "ID3v1 tags written successfully"