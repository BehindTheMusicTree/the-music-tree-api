
# Metadata
## Vorbis 
### Read
metaflac --list test.flac

### Set rating
metaflac --remove-tag=RATING --set-tag="RATING=80" test.flac

## Id3v2
mutagen-inspect "rating_id3v2=1 star.wav"

## RIFF
brew install mediainfo
mediainfo "rating_id3v2=3 star.wav"

