from bodzify_api.model.playlist.Fields import Fields as BasePlaylistFields


class Fields:
    BASE_PLAYLIST = BasePlaylistFields.MODEL
    UUID = BasePlaylistFields.UUID
    USER = BasePlaylistFields.USER
    CREATED_ON = BasePlaylistFields.CREATED_ON
    UPDATED_ON = BasePlaylistFields.UPDATED_ON
    LIB_TRACKS = BasePlaylistFields.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = BasePlaylistFields.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = BasePlaylistFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = BasePlaylistFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = BasePlaylistFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = BasePlaylistFields.DURATION_STR_IN_HOUR_MIN_SEC
    PLAY_COUNT = BasePlaylistFields.PLAY_COUNT
    LAST_TRACK_LIST_UPDATE_DATE = BasePlaylistFields.LAST_TRACK_LIST_UPDATE_DATE
