"""
ID3 Metadata Format Support Documentation.

ID3 is a metadata container format primarily used with MP3 audio files. It exists in two main variants:
ID3v1 (legacy) and ID3v2 (modern), each with different capabilities and format support.

1. ID3v1 (Legacy Format):
   Structure:
   - Fixed 128-byte block at end of file
   - Latin-1 encoding only
   - Fixed field lengths (30 chars)
   - Simple metadata fields only
   
   Limitations:
   - No Unicode support
   - No album artist support
   - No BPM support
   - No ratings support
   - No language support
   - No custom genres
   - No multiple genres/artists
   - Read-only (modification not safe)

2. ID3v2 (Modern Format):
   Common Features Across All v2 Versions:
   - Variable size tags at file start
   - Extensive metadata fields
   - Read/write support
   - All standard fields supported

   Version-Specific Features:
   * v2.2 (Original):
     - Three-character frame IDs (TT2, TP1, etc.)
     - ISO-8859-1 or UCS-2 text encoding
     - Simpler header structure
     - Less common but fully functional

   * v2.3 (Improved):
     - Four-character frame IDs
     - TYER+TDAT frames for dates
     - UTF-16/UTF-16BE text encoding
     - Basic unsynchronization
     - Most widely used version
     - Improved structure

   * v2.4 (Latest):
     - TDRC frame for full timestamps
     - UTF-8 text encoding
     - Extended header features
     - Unsynchronization per frame
     - Preferred for new tags
     - Most advanced features

3. Format Support:
   MP3:
   - Primary format for ID3
   - Full native support for ID3v1
   - Full native support for all ID3v2 versions
   - Recommended format for ID3 tags

   WAV:
   - Native format: RIFF
   - Can contain ID3v2 but non-standard
   - ID3 support is technically possible but not recommended
   - Should use RIFF INFO chunks instead

   FLAC:
   - Native format: Vorbis comments
   - Can contain ID3v2 but non-standard
   - ID3 support is technically possible but not recommended
   - Should use Vorbis comments instead

Note: Only MP3 format fully supports both ID3v1 and ID3v2 as its native metadata format.
Other formats may technically be able to contain ID3 tags but should use their native
metadata formats for better compatibility and reliability.
"""

from bodzify_api.utils.audio_metadata.manager.MetadataManager import MetadataManager


class Id3Manager(MetadataManager):
    """Base class for ID3 metadata managers.
    
    This class serves as a base for both ID3v1 and ID3v2 managers,
    providing common functionality and documentation for ID3 metadata handling.
    See module docstring for detailed ID3 format support information.
    """
    pass