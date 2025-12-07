#!/usr/bin/env python3
import wave
import sys
import os
import tempfile
import shutil


def remove_riff_metadata(input_file):
    """Remove RIFF metadata by copying only audio params and frames to temp file, then replace original"""
    # Create temporary file
    fd, temp_path = tempfile.mkstemp(suffix='.wav')
    os.close(fd)

    try:
        # Extract essential audio data
        with wave.open(input_file, 'rb') as src:
            params = src.getparams()
            frames = src.readframes(src.getnframes())

        # Write to temporary file without metadata
        with wave.open(temp_path, 'wb') as dst:
            dst.setparams(params)
            dst.writeframes(frames)

        # Replace original file with the clean one
        shutil.move(temp_path, input_file)
        print(f"RIFF metadata removed from {input_file}")

    except Exception as e:
        # Clean up temp file in case of error
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: remove_riff.py input.wav")
        sys.exit(1)
    remove_riff_metadata(sys.argv[1])
