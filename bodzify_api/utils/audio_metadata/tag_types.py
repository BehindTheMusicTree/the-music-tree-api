"""Tag type constants for audio metadata handling."""


class TagTypes:
    """Constants for audio metadata tag types."""
    ID3V2 = 'id3v2'
    ID3V1 = 'id3v1'
    VORBIS = 'vorbis'
    RIFF = 'riff'

    # Define tag type priorities for different file formats
    # First tag type in each list has highest priority
    PRIORITIES = {
        '.flac': [VORBIS, ID3V2],      # Prefer Vorbis comments over ID3v2 tags for FLAC
        '.mp3': [ID3V2, ID3V1],        # Prefer ID3v2 over ID3v1 for MP3
        '.wav': [RIFF]                  # WAV files only use RIFF metadata
    }