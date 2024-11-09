from bodzify_api.model.criteria.Criteria import Fields as ModelFields
from bodzify_api.model.track.lib.Fields import Fields as LibTrackFields


class Fields:
    CREATED_ON = ModelFields.CREATED_ON
    UPDATED_ON = ModelFields.UPDATED_ON
    UUID = ModelFields.UUID
    NAME = ModelFields.NAME
    LIB_TRACKS = ModelFields.LIB_TRACKS
    LIB_TRACKS_COUNT = ModelFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = ModelFields.LIB_TRACKS_ARCHIVED_COUNT
    LIB_TRACKS_TITLE = LibTrackFields.TITLE
    ROOT = ModelFields.ROOT
    PARENT = ModelFields.PARENT
    ASCENDANTS = ModelFields.ASCENDANTS
    DESCENDANTS = ModelFields.DESCENDANTS
    CHILDREN = ModelFields.CHILDREN
    CRITERIA_PLAYLIST = ModelFields.CRITERIA_PLAYLIST
