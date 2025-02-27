
# Vorbis 
## View metadata
metaflac --list test.flac

## Set rating
metaflac --remove-tag=RATING --set-tag="RATING=80" test.flac

# Id3v2 tags
## .mp3
brew install id3v2
id3v2 -l "rating_id3v2=3 star.mp3" | grep POPM

# RIFF
brew install mediainfo
mediainfo "rating_id3v2=3 star.wav"

