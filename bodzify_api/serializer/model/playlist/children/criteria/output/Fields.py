
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import \
    Fields as ModelFields
from bodzify_api.serializer.model.playlist.children.detailed import \
    Fields as ChildPlaylistFields


class Fields:
    CREATED_ON = ChildPlaylistFields.CREATED_ON
    UPDATED_ON = ChildPlaylistFields.UPDATED_ON
    UUID = ChildPlaylistFields.UUID
    LIB_TRACK_PLAYLIST_RELS_INTERNAL = ChildPlaylistFields.LIB_TRACK_PLAYLIST_RELS_INTERNAL
    LIB_TRACK_PLAYLIST_RELS_PUBLIC = ChildPlaylistFields.LIB_TRACK_PLAYLIST_RELS_PUBLIC
    LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL = ChildPlaylistFields.LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL
    LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = ChildPlaylistFields.LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC
    LIB_TRACKS_ARCHIVED_COUNT_INTERNAL = ChildPlaylistFields.LIB_TRACKS_ARCHIVED_COUNT_INTERNAL
    LIB_TRACKS_ARCHIVED_COUNT_PUBLIC = ChildPlaylistFields.LIB_TRACKS_ARCHIVED_COUNT_PUBLIC
    DURATION_IN_SEC = ChildPlaylistFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ChildPlaylistFields.DURATION_STR_IN_HOUR_MIN_SEC
    NAME = ChildPlaylistFields.NAME
    LAST_TRACK_LIST_UPDATE_DATE = ChildPlaylistFields.LAST_TRACK_LIST_UPDATE_DATE

    CRITERIA = ModelFields.CRITERIA
    PARENT = ModelFields.PARENT
    ROOT = ModelFields.ROOT
