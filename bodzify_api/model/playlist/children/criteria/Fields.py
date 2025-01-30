from bodzify_api.model.playlist.children.Fields import Fields as ChildFields


class Fields:
    UUID = ChildFields.UUID
    USER = ChildFields.USER
    CREATED_ON = ChildFields.CREATED_ON
    UPDATED_ON = ChildFields.UPDATED_ON
    LIB_TRACKS_INTERNAL = ChildFields.LIB_TRACKS_INTERNAL
    LIB_TRACKS_PUBLIC = ChildFields.LIB_TRACKS_PUBLIC
    LIB_TRACKS_COUNT_PUBLIC = ChildFields.LIB_TRACKS_COUNT_PUBLIC
    LIB_TRACKS_COUNT_INTERNAL = ChildFields.LIB_TRACKS_COUNT_INTERNAL
    DURATION_IN_SEC = ChildFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ChildFields.DURATION_STR_IN_HOUR_MIN_SEC
    PLAY_COUNT = ChildFields.PLAY_COUNT
    LAST_TRACK_LIST_UPDATE_DATE = ChildFields.LAST_TRACK_LIST_UPDATE_DATE
    CRITERIA = 'criteria'
    PARENT = 'parent'
    ROOT = 'root'
    NAME = 'name'
    CHILDREN = 'children'
    DESCENDANTS = 'descendants'
    ROOT_DESCENDANTS = 'root_descendants'
