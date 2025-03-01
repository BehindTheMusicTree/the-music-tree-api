#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <flac_file>"
    exit 1
fi

FLAC_FILE="$1"
MAX_TEXT=256

# Standard Vorbis fields
TITLE=$(printf 'T%.0s' $(seq 1 $MAX_TEXT))
ARTIST=$(printf 'A%.0s' $(seq 1 $MAX_TEXT))
ALBUM=$(printf 'L%.0s' $(seq 1 $MAX_TEXT))
ALBUMARTIST=$(printf 'AA%.0s' $(seq 1 $MAX_TEXT))
TRACKNUMBER="01"
TRACKTOTAL="99"
DISCNUMBER="1"
DISCTOTAL="9"
DATE="2024"
GENRE="Heavy Metal"
COMMENT=$(printf 'C%.0s' $(seq 1 $MAX_TEXT))
COPYRIGHT="CC0"
COMPOSER=$(printf 'C%.0s' $(seq 1 $MAX_TEXT))
CONDUCTOR=$(printf 'CD%.0s' $(seq 1 $MAX_TEXT))
ARRANGER=$(printf 'AR%.0s' $(seq 1 $MAX_TEXT))
LYRICIST=$(printf 'L%.0s' $(seq 1 $MAX_TEXT))
AUTHOR=$(printf 'AU%.0s' $(seq 1 $MAX_TEXT))
ORGANIZATION=$(printf 'O%.0s' $(seq 1 $MAX_TEXT))
LOCATION=$(printf 'L%.0s' $(seq 1 $MAX_TEXT))
CONTACT=$(printf 'C%.0s' $(seq 1 $MAX_TEXT))
ISRC="USXXX0000001"
CATALOGNUMBER="CAT001"
DESCRIPTION=$(printf 'D%.0s' $(seq 1 $MAX_TEXT))
PERFORMER=$(printf 'P%.0s' $(seq 1 $MAX_TEXT))
RATING="255"
BPM="128"
MOOD="Happy"
VERSION="1.0"
LANGUAGE="eng"
LABEL=$(printf 'L%.0s' $(seq 1 $MAX_TEXT))
ENCODEDBY="Bodzify"
ENCODERSETTINGS="FLAC level 8"

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