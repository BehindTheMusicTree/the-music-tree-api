#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <flac_file>"
    exit 1
fi

FLAC_FILE="$1"
MAX_TEXT=256  # Maximum length for text fields

# Standard Vorbis fields with maximum values
TITLE=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
ARTIST=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
ALBUM=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
ALBUMARTIST=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
TRACKNUMBER="99"  # Max 2-digit track number
TRACKTOTAL="99"   # Max 2-digit total tracks
DISCNUMBER="99"   # Max 2-digit disc number
DISCTOTAL="99"    # Max 2-digit total discs
DATE="9999"       # Max 4-digit year
GENRE=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
COMMENT=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
COPYRIGHT=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
COMPOSER=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
CONDUCTOR=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
ARRANGER=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
LYRICIST=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
AUTHOR=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
ORGANIZATION=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
LOCATION=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
CONTACT=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
ISRC="USXXX9999999"  # Max ISRC format
CATALOGNUMBER=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
DESCRIPTION=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
PERFORMER=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
RATING="255"      # Max rating value (8-bit)
BPM="999"         # Max reasonable BPM value
MOOD=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
VERSION=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
LANGUAGE=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
LABEL=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
ENCODEDBY=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))
ENCODERSETTINGS=$(printf 'a%.0s' $(seq 1 $MAX_TEXT))

# Remove existing tags
metaflac --remove-all-tags "$FLAC_FILE"

# Write all tags
metaflac \
    --set-tag="TITLE=$TITLE" \
    --set-tag="ARTIST=$ARTIST" \
    --set-tag="ALBUM=$ALBUM" \
    --set-tag="ALBUMARTIST=$ALBUMARTIST" \
    --set-tag="TRACKNUMBER=$TRACKNUMBER" \
    --set-tag="TRACKTOTAL=$TRACKTOTAL" \
    --set-tag="DISCNUMBER=$DISCNUMBER" \
    --set-tag="DISCTOTAL=$DISCTOTAL" \
    --set-tag="DATE=$DATE" \
    --set-tag="GENRE=$GENRE" \
    --set-tag="COMMENT=$COMMENT" \
    --set-tag="COPYRIGHT=$COPYRIGHT" \
    --set-tag="COMPOSER=$COMPOSER" \
    --set-tag="CONDUCTOR=$CONDUCTOR" \
    --set-tag="ARRANGER=$ARRANGER" \
    --set-tag="LYRICIST=$LYRICIST" \
    --set-tag="AUTHOR=$AUTHOR" \
    --set-tag="ORGANIZATION=$ORGANIZATION" \
    --set-tag="LOCATION=$LOCATION" \
    --set-tag="CONTACT=$CONTACT" \
    --set-tag="ISRC=$ISRC" \
    --set-tag="CATALOGNUMBER=$CATALOGNUMBER" \
    --set-tag="DESCRIPTION=$DESCRIPTION" \
    --set-tag="PERFORMER=$PERFORMER" \
    --set-tag="RATING=$RATING" \
    --set-tag="BPM=$BPM" \
    --set-tag="MOOD=$MOOD" \
    --set-tag="VERSION=$VERSION" \
    --set-tag="LANGUAGE=$LANGUAGE" \
    --set-tag="LABEL=$LABEL" \
    --set-tag="ENCODED-BY=$ENCODEDBY" \
    --set-tag="ENCODER_SETTINGS=$ENCODERSETTINGS" \
    "$FLAC_FILE"

# Verify tags
metaflac --list --block-type=VORBIS_COMMENT "$FLAC_FILE"
echo "All Vorbis comments written successfully"