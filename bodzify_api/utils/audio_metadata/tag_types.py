"""Tag type constants for audio metadata handling."""
from enum import Enum
from typing import Dict, List


class TagTypes(str, Enum):
    """Constants for audio metadata tag types."""
    ID3V2 = 'id3v2'
    ID3V1 = 'id3v1'
    VORBIS = 'vorbis'
    RIFF = 'riff'

    @classmethod
    def get_priorities(cls) -> Dict[str, List['TagTypes']]:
        """Get tag type priorities for different file formats.
        First tag type in each list has highest priority.
        
        Returns:
            Dictionary mapping file extensions to ordered list of tag types
        """
        return {
            '.flac': [cls.VORBIS, cls.ID3V2],  # Prefer Vorbis comments over ID3v2 tags for FLAC
            '.mp3': [cls.ID3V2, cls.ID3V1],    # Prefer ID3v2 over ID3v1 for MP3
            '.wav': [cls.RIFF]                  # WAV files only use RIFF metadata
        }