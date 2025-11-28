#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <flac_file>"
    exit 1
fi

FLAC_FILE="$1"
TEXT_BIG_LENGTH=1000 # Text length for testing truncation

# Standard Vorbis fields with maximum values
TITLE=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
ARTIST=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
ALBUM=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
ALBUMARTIST=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
TRACKNUMBER="99"  # Max 2-digit track number
TRACKTOTAL="99"   # Max 2-digit total tracks
DISCNUMBER="99"   # Max 2-digit disc number
DISCTOTAL="99"    # Max 2-digit total discs
DATE="9999"       # Max 4-digit year
GENRE=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
COMMENT=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
COPYRIGHT=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
COMPOSER=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
CONDUCTOR=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
ARRANGER=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
LYRICIST=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
AUTHOR=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
ORGANIZATION=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
LOCATION=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
CONTACT=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
ISRC="USXXX9999999"  # Max ISRC format
CATALOGNUMBER=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
DESCRIPTION=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
PERFORMER=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
RATING="255"      # Max rating value (8-bit)
BPM="999"         # Max reasonable BPM value
MOOD=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
VERSION=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
LANGUAGE=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
LABEL=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
ENCODEDBY=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))
ENCODERSETTINGS=$(printf 'a%.0s' $(seq 1 $TEXT_BIG_LENGTH))

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