
from bodzify_api.model.playlist.BasePlaylist import Fields as ModelFields


class Fields:
    CREATED_ON = ModelFields.CREATED_ON
    UPDATED_ON = ModelFields.UPDATED_ON
    UUID = ModelFields.UUID
    NAME = ModelFields.NAME
    LIB_TRACKS = ModelFields.LIB_TRACKS
    LIB_TRACKS_COUNT = ModelFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = ModelFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = ModelFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ModelFields.DURATION_STR_IN_HOUR_MIN_SEC
    PLAY_COUNT = ModelFields.PLAY_COUNT
    LAST_TRACK_LIST_UPDATE_DATE = ModelFields.LAST_TRACK_LIST_UPDATE_DATE
    TYPE_LABEL = ModelFields.TYPE_LABEL
