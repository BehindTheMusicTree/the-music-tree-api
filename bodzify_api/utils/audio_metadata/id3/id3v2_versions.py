"""ID3v2 version information."""


class Id3v2Versions:
    """ID3v2 version information.

    A file can only have one version of ID3v2 tags at a time.
    Each version has different frame IDs and capabilities:
    - v2.2: Original version (obsolete)
    - v2.3: Added more frames, improved structure
    - v2.4: Latest version with additional features
    """
    V22 = "2.2"  # Original version (obsolete)
    V23 = "2.3"  # Added more frames, improved structure
    V24 = "2.4"  # Latest version with additional features