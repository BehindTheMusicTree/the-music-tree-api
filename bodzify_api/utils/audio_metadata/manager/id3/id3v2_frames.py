"""ID3v2 frame definitions."""


class DateFrames:
    """Version-specific frames for dates.

    ID3v2 versions handle dates differently:
    - ID3v2.4: Uses TDRC for all date information (ISO 8601)
    - ID3v2.3: Uses TYER, TDAT, TIME for date components
    """
    # ID3v2.4 uses a single frame for all date info
    V24_RECORDING_TIME = 'TDRC'

    # ID3v2.3 uses separate frames for different date parts
    V23_YEAR = 'TYER'
    V23_DATE = 'TDAT'  # Day/Month
    V23_TIME = 'TIME'  # Hours/Minutes


class Id3v2TextFrames:
    """ID3v2 frame IDs by version.

    Frame IDs and encoding can differ between versions:
    - ID3v2.4: Uses TDRC for all date information (ISO 8601)
    - ID3v2.3: Uses TYER, TDAT, TIME for date components
    """
    # Common frames across all versions
    TITLE = 'TIT2'
    ARTIST_NAME = 'TPE1'
    ALBUM_NAME = 'TALB'
    ALBUM_ARTISTS_NAMES = 'TPE2'
    GENRE_NAME = 'TCON'
    RATING = 'POPM'
    LANGUAGE = 'TLAN'
    TRACK_NUMBER = 'TRCK'  # Track number/Position in set
    BPM = 'TBPM'  # Beats Per Minute

    # Version-specific date frames
    DateFrames = DateFrames