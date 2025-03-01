
# Metadata
## Vorbis 
### Read
metaflac --list test.flac

### Set rating
metaflac --remove-tag=RATING --set-tag="RATING=80" test.flac

## Id3v2
### Read
mutagen-inspect "rating_id3v2=1 star.wav"

### Write
id3v2 --artist "Artist Name" test.flac
id3v2 --album "Album Name" test.flac
id3v2 --song "Song Title" test.flac

## RIFF
brew install mediainfo
mediainfo "rating_id3v2=3 star.wav"

