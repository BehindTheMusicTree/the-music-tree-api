from bodzify_api.model.playlist.Fields import Fields as PlaylistFields


class Fields:
    UUID = PlaylistFields.UUID
    USER = PlaylistFields.USER
    CREATED_ON = PlaylistFields.CREATED_ON
    UPDATED_ON = PlaylistFields.UPDATED_ON
    LIB_TRACKS = PlaylistFields.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = PlaylistFields.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = PlaylistFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = PlaylistFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = PlaylistFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = PlaylistFields.DURATION_STR_IN_HOUR_MIN_SEC
    PLAY_COUNT = PlaylistFields.PLAY_COUNT
    LAST_TRACK_LIST_UPDATE_DATE = PlaylistFields.LAST_TRACK_LIST_UPDATE_DATE
