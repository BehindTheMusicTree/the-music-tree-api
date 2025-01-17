from bodzify_api.model.lib_track_mixin.Fields import Fields as Fields


class Fields:
    CREATED_ON = Fields.CREATED_ON
    UPDATED_ON = Fields.UPDATED_ON
    UUID = Fields.UUID
    USER = Fields.USER
    NAME = Fields.NAME
    NAME_INTERNAL = Fields.NAME_INTERNAL
    LIB_TRACKS = Fields.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = Fields.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = Fields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = Fields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = Fields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = Fields.DURATION_STR_IN_HOUR_MIN_SEC
    LIB_TRACKS_RELATED_NAME = 'lib_tracks_of_artist'
    ALBUMS = 'albums'
