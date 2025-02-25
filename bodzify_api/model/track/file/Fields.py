from bodzify_api.model.private_standard_resource.Fields import \
    Fields as PrivateStandardResourceFields


class Fields:
    CREATED_ON = PrivateStandardResourceFields.CREATED_ON
    UPDATED_ON = PrivateStandardResourceFields.UPDATED_ON
    USER = PrivateStandardResourceFields.USER
    LIB_TRACK = 'lib_track'
    FILE = 'file'
    FILENAME = 'filename'
    EXTENSION = 'extension'
    DURATION_IN_SEC = 'duration_in_sec'
    DURATION_STR_IN_HOUR_MIN_SEC = 'duration_str_in_hour_min_sec'
    FINGERPRINT_MEMORY = 'fingerprint_memory'
    FINGERPRINT_BYTES = 'fingerprint_bytes'
    FINGERPRINT_MISSING_CAUSE = 'fingerprint_missing_cause'
    SIZE_IN_BYTES = 'size_in_bytes'
    SIZE_IN_KO = 'size_in_ko'
    SIZE_IN_MO = 'size_in_mo'
    BITRATE_IN_KBPS = 'bitrate_in_kbps'
    MUSICBRAINZ_RECORDING = 'musicbrainz_recording'
    MUSICBRAINZ_RECORDING_MISSING_CAUSE = 'musicbrainz_recording_missing_cause'
