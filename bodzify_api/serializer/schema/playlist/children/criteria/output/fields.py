
from bodzify_api.serializer.schema.playlist.children.detailed import Fields as ChildPlaylistFields
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import Fields as ModelFields


class Fields:
    CREATED_ON = ChildPlaylistFields.CREATED_ON
    UPDATED_ON = ChildPlaylistFields.UPDATED_ON
    UUID = ChildPlaylistFields.UUID
    LIB_TRACKS = ChildPlaylistFields.LIB_TRACKS
    LIB_TRACKS_COUNT = ChildPlaylistFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = ChildPlaylistFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = ChildPlaylistFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ChildPlaylistFields.DURATION_STR_IN_HOUR_MIN_SEC
    NAME = ChildPlaylistFields.NAME

    CRITERIA = ModelFields.CRITERIA
    PARENT = ModelFields.PARENT
    ROOT = ModelFields.ROOT
