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
    --INAM="$MAX_STRING" \     # Title
    --IART="$MAX_STRING" \     # Artist
    --IPRD="$MAX_STRING" \     # Album
    --IGNR="$MAX_STRING" \     # Genre
    --ICRD="9999" \           # Creation date (max year)
    --ICMT="$MAX_STRING" \     # Comments
    --ISFT="$MAX_STRING" \     # Software
    --ICOP="$MAX_STRING" \     # Copyright
    --IENG="$MAX_STRING" \     # Engineer
    --ITCH="$MAX_STRING" \     # Technician
    --ISRC="USXXX9999999" \   # ISRC (max format)
    --ISBJ="$MAX_STRING" \     # Subject
    --IKEY="$MAX_STRING" \     # Keywords
    --IMED="$MAX_STRING" \     # Medium
    --ICMS="$MAX_STRING" \     # Commissioned by
    --ITRK="99" \             # Track number (max 2-digit)
    --IARL="$MAX_STRING" \     # Archival Location
    --ILOC="$MAX_STRING" \     # Location
    "$WAV_FILE"

if [ $? -eq 0 ]; then
    echo "All RIFF INFO tags written successfully with maximum length values"
else
    echo "Error: Failed to write RIFF INFO tags"
    exit 1
fi