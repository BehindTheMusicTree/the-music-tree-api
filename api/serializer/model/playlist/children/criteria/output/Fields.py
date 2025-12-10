
from api.model.playlist.children.criteria.CriteriaPlaylist import Fields as ModelFields
from api.serializer.model.playlist.children.detailed import Fields as ChildPlayListFields


class Fields:
    CREATED_ON = ChildPlayListFields.CREATED_ON
    UPDATED_ON = ChildPlayListFields.UPDATED_ON
    UUID = ChildPlayListFields.UUID
    TRACK_PLAYLIST_RELS_INTERNAL = ChildPlayListFields.TRACK_PLAYLIST_RELS_INTERNAL
    TRACK_PLAYLIST_RELS_PUBLIC = ChildPlayListFields.TRACK_PLAYLIST_RELS_PUBLIC
    TRACKS_NOT_ARCHIVED_COUNT_INTERNAL = ChildPlayListFields.TRACKS_NOT_ARCHIVED_COUNT_INTERNAL
    TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = ChildPlayListFields.TRACKS_NOT_ARCHIVED_COUNT_PUBLIC
    TRACKS_ARCHIVED_COUNT_INTERNAL = ChildPlayListFields.TRACKS_ARCHIVED_COUNT_INTERNAL
    TRACKS_ARCHIVED_COUNT_PUBLIC = ChildPlayListFields.TRACKS_ARCHIVED_COUNT_PUBLIC
    DURATION_IN_SEC = ChildPlayListFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ChildPlayListFields.DURATION_STR_IN_HOUR_MIN_SEC
    NAME = ChildPlayListFields.NAME

    CRITERIA = ModelFields.CRITERIA
    PARENT = ModelFields.PARENT
    ROOT = ModelFields.ROOT
