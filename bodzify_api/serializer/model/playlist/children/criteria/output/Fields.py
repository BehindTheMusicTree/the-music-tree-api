
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import Fields as ModelFields
from bodzify_api.serializer.model.playlist.children.detailed import Fields as ChildPlayListFields


class Fields:
    CREATED_ON = ChildPlayListFields.CREATED_ON
    UPDATED_ON = ChildPlayListFields.UPDATED_ON
    UUID = ChildPlayListFields.UUID
    LIB_TRACK_PLAYLIST_RELS_INTERNAL = ChildPlayListFields.LIB_TRACK_PLAYLIST_RELS_INTERNAL
    LIB_TRACK_PLAYLIST_RELS_PUBLIC = ChildPlayListFields.LIB_TRACK_PLAYLIST_RELS_PUBLIC
    LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL = ChildPlayListFields.LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL
    LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = ChildPlayListFields.LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC
    LIB_TRACKS_ARCHIVED_COUNT_INTERNAL = ChildPlayListFields.LIB_TRACKS_ARCHIVED_COUNT_INTERNAL
    LIB_TRACKS_ARCHIVED_COUNT_PUBLIC = ChildPlayListFields.LIB_TRACKS_ARCHIVED_COUNT_PUBLIC
    DURATION_IN_SEC = ChildPlayListFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ChildPlayListFields.DURATION_STR_IN_HOUR_MIN_SEC
    NAME = ChildPlayListFields.NAME
    LAST_TRACK_LIST_UPDATE_DATE = ChildPlayListFields.LAST_TRACK_LIST_UPDATE_DATE

    CRITERIA = ModelFields.CRITERIA
    PARENT = ModelFields.PARENT
    ROOT = ModelFields.ROOT
