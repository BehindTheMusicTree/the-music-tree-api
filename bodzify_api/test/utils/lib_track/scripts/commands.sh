
# Metadata

## Id3v1
### Read
id3v2 -l1 file.mp3
### Write
id3v2 \
    --comment "COMMENT" \
    --artist "ARTIST" \
    --album "ALBUM" \
    --song "TITLE" \
    --year "YEAR" \
    --track "TRACK" \
    --genre "254" \
    --id3v1-only \
    "test.mp3"

## Id3v2
### Read
mid3v2 -l "files/metadata=max a_id3v2.flac"

### Write
id3v2 --artist "Artist Name" test.flac
id3v2 --album "Album Name" test.flac
id3v2 --song "Song Title" test.flac

### Remove
ffmpeg -i "input.flac" -map_metadata -1 -c:a copy "output.flac"

#### Set rating
mid3v2 --POPM "Windows Media Player 9 Series:128" test.mp3
mid3v2 --POPM "kid3:128" test.mp3
mid3v2 --POPM "Traktor:153" test.mp3

## RIFF
### Read
brew install mediainfo
mediainfo "rating_id3v2=3 star.wav"


## Vorbis 
### Read
metaflac --list test.flac

### Set rating
metaflac --remove-tag=RATING --set-tag="RATING=80" test.flac

