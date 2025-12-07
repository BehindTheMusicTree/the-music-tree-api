#!/usr/bin/env python3
import sys
import os
from mutagen.flac import FLAC
from mutagen.id3 import ID3
from mutagen.wave import WAVE
from mutagen.mp3 import MP3


def remove_id3_tags(filename):
    """Remove ID3 tags while preserving native format metadata"""
    file_ext = os.path.splitext(filename)[1].lower()

    try:
        # Always try to remove ID3 tags first
        try:
            ID3(filename).delete()
            print(f"ID3 tags removed from {filename}")
        except:
            print(f"No ID3 tags found or could not remove from {filename}")

        # Format-specific preservation of native metadata
        if file_ext == '.flac':
            audio = FLAC(filename)
            audio.save()
            print(f"FLAC Vorbis comments preserved in {filename}")
        elif file_ext == '.wav':
            audio = WAVE(filename)
            audio.save()
            print(f"WAV RIFF metadata preserved in {filename}")
        elif file_ext == '.mp3':
            # For MP3, we've already removed ID3 so nothing more to do
            print(f"MP3 processed {filename}")
        else:
            print(f"Unknown file type: {filename}")

    except Exception as e:
        print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: remove_id3.py <audio_file> [audio_file2 ...]")
        sys.exit(1)

    for filename in sys.argv[1:]:
        remove_id3_tags(filename)
