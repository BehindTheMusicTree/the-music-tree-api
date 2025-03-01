#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <wav_file>"
    exit 1
fi

WAV_FILE="$1"
TMP_FILE="${WAV_FILE}.tmp"

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

# Standard RIFF INFO metadata
TITLE="Test Title"
ARTIST="Test Artist"
ALBUM="Test Album"
GENRE="Rock"
YEAR="2024"
COMMENT="Test Comment"

# Write 32-bit integer in little-endian
write_int32_le() {
    local VALUE=$1
    local B0=$((VALUE & 255))
    local B1=$(((VALUE >> 8) & 255))
    local B2=$(((VALUE >> 16) & 255))
    local B3=$(((VALUE >> 24) & 255))
    printf "\\$(printf '%03o' $B0)"
    printf "\\$(printf '%03o' $B1)"
    printf "\\$(printf '%03o' $B2)"
    printf "\\$(printf '%03o' $B3)"
}

# Write INFO tag
write_info_tag() {
    local ID=$1
    local VALUE=$2
    local LEN=${#VALUE}
    local PADDED_LEN=$((LEN + (LEN % 2)))  # Ensure even length
    
    # Write chunk ID
    printf "%s" "$ID"
    
    # Write chunk size (actual data length, not including padding)
    write_int32_le "$LEN"
    
    # Write data
    printf "%s" "$VALUE"
    
    # Add padding byte if needed
    [ $((LEN % 2)) -eq 1 ] && printf "\0"
}

# Create LIST chunk
LIST_CHUNK=$(mktemp)
trap 'rm -f "$LIST_CHUNK" "$TMP_FILE"' EXIT

# Write LIST chunk content
{
    # Write INFO identifier
    printf "INFO"
    
    # Write standard INFO tags
    write_info_tag "INAM" "$TITLE"    # Name/Title
    write_info_tag "IART" "$ARTIST"   # Artist
    write_info_tag "IPRD" "$ALBUM"    # Product/Album
    write_info_tag "IGNR" "$GENRE"    # Genre
    write_info_tag "ICRD" "$YEAR"     # Creation date
    write_info_tag "ICMT" "$COMMENT"  # Comment
} > "$LIST_CHUNK"

LIST_SIZE=$(stat -f%z "$LIST_CHUNK")

# Create temporary file for audio data
AUDIO_CHUNK=$(mktemp)
trap 'rm -f "$LIST_CHUNK" "$TMP_FILE" "$AUDIO_CHUNK"' EXIT

# Extract audio data (skip RIFF header and any existing metadata)
{
    # Copy WAVE header
    dd if="$WAV_FILE" bs=1 skip=8 count=4 2>/dev/null
    
    # Find and copy fmt chunk
    dd if="$WAV_FILE" bs=1 skip=12 2>/dev/null | (
        while IFS= read -r -d '' -n 4 chunk_id; do
            if [ "$chunk_id" = "fmt " ]; then
                printf "%s" "$chunk_id"
                dd bs=1 count=4 2>/dev/null | (
                    read -r -d '' -n 4 size_bytes
                    printf "%s" "$size_bytes"
                    size=$(printf "%d" "0x${size_bytes}" 2>/dev/null)
                    dd bs=1 count=$((size + (size % 2))) 2>/dev/null
                )
            elif [ "$chunk_id" = "data" ]; then
                printf "%s" "$chunk_id"
                dd 2>/dev/null
                break
            else
                size_bytes=$(dd bs=1 count=4 2>/dev/null)
                size=$(printf "%d" "0x${size_bytes}" 2>/dev/null)
                dd bs=1 count=$((size + (size % 2))) 2>/dev/null >/dev/null
            fi
        done
    )
} > "$AUDIO_CHUNK"

AUDIO_SIZE=$(stat -f%z "$AUDIO_CHUNK")
TOTAL_SIZE=$((AUDIO_SIZE + LIST_SIZE + 8))  # +8 for LIST chunk header

# Create new WAV file
{
    # Write RIFF header
    printf "RIFF"
    write_int32_le "$TOTAL_SIZE"
    
    # Write audio data (includes WAVE header, fmt chunk, and data chunk)
    cat "$AUDIO_CHUNK"
    
    # Write LIST chunk
    printf "LIST"
    write_int32_le "$LIST_SIZE"
    cat "$LIST_CHUNK"
} > "$TMP_FILE"

# Verify output
if [ ! -s "$TMP_FILE" ]; then
    echo "Error: Failed to create output file"
    exit 1
fi

# Replace original file
mv "$TMP_FILE" "$WAV_FILE"
echo "RIFF INFO tags written successfully"