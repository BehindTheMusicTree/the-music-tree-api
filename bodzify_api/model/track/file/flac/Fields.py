from bodzify_api.model.track.file.Fields import Fields as TrackFileFields


class Fields:
    CREATED_ON = TrackFileFields.CREATED_ON
    UPDATED_ON = TrackFileFields.UPDATED_ON
    USER = TrackFileFields.USER
    LIB_TRACK = TrackFileFields.LIB_TRACK
    FILE = TrackFileFields.FILE
    FILENAME = TrackFileFields.FILENAME
    EXTENSION = TrackFileFields.EXTENSION
    DURATION_IN_SEC = TrackFileFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = TrackFileFields.DURATION_STR_IN_HOUR_MIN_SEC
    FINGERPRINT_MEMORY = TrackFileFields.FINGERPRINT_MEMORY
    FINGERPRINT_BYTES = TrackFileFields.FINGERPRINT_BYTES
    FINGERPRINT_MISSING_CAUSE = TrackFileFields.FINGERPRINT_MISSING_CAUSE
    SIZE_IN_BYTES = TrackFileFields.SIZE_IN_BYTES
    SIZE_IN_KO = TrackFileFields.SIZE_IN_KO
    SIZE_IN_MO = TrackFileFields.SIZE_IN_MO
    BITRATE_IN_KBPS = TrackFileFields.BITRATE_IN_KBPS
    MUSICBRAINZ_RECORDING = TrackFileFields.MUSICBRAINZ_RECORDING
    MUSICBRAINZ_RECORDING_MISSING_CAUSE = TrackFileFields.MUSICBRAINZ_RECORDING_MISSING_CAUSE

    ID3V2_TAGS_FOUND_AND_CONVERTED = 'id3v2_tags_found_and_converted'
    MD5_HAS_BEEN_CORRECTED = 'flac_md5_has_been_corrected'
