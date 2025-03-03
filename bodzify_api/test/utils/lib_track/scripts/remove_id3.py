
#!/usr/bin/env python3
import sys
from mutagen.flac import FLAC
from mutagen.id3 import ID3

filename = sys.argv[1]
try:
    # Remove ID3 tags
    ID3(filename).delete()
    # Keep Vorbis comments
    audio = FLAC(filename)
    audio.save()
    print(f"ID3 tags removed from {filename}")
except Exception as e:
    print(f"Error: {e}")
