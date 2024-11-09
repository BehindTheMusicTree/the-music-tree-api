from bodzify_api.model.lib_track_mixin.Fields import Fields as LibTrackMixinFields


class Fields:
    CREATED_ON = LibTrackMixinFields.CREATED_ON
    UPDATED_ON = LibTrackMixinFields.UPDATED_ON
    USER = LibTrackMixinFields.USER
    UUID = LibTrackMixinFields.UUID
    NAME = LibTrackMixinFields.NAME
    LIB_TRACKS = LibTrackMixinFields.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = LibTrackMixinFields.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = LibTrackMixinFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = LibTrackMixinFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = LibTrackMixinFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = LibTrackMixinFields.DURATION_STR_IN_HOUR_MIN_SEC
    LIB_TRACKS_RELATED_NAME = 'lib_tracks_of_criteria'
    ASCENDANTS = 'ascendants'
    ASCENDANTS_RELS = 'ascendants_rels'
    DESCENDANTS = 'descendants'
    DESCENDANTS_RELS = 'descendants_rels'
    ROOT = 'root'
    PARENT = 'parent'
    CHILD = 'child'
    CHILDREN = 'children'
    CRITERIA_PLAYLIST = 'criteria_playlist'
