from bodzify_api.model.playlist.children.Fields import Fields as ChildFields


class Fields:
    CREATED_ON = ChildFields.CREATED_ON
    UPDATED_ON = ChildFields.UPDATED_ON
    UUID = ChildFields.UUID
    USER = ChildFields.USER
    LIB_TRACKS = ChildFields.LIB_TRACKS
    LIB_TRACKS_COUNT = ChildFields.LIB_TRACKS_COUNT
    LIB_TRACKS_NOT_ARCHIVED = ChildFields.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_ARCHIVED_COUNT = ChildFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = ChildFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ChildFields.DURATION_STR_IN_HOUR_MIN_SEC
    PLAY_COUNT = ChildFields.PLAY_COUNT
    LAST_TRACK_LIST_UPDATE_DATE = ChildFields.LAST_TRACK_LIST_UPDATE_DATE
    NAME_DB = '_name'
    NAME = 'name'
