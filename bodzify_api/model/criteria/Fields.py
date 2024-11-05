from bodzify_api.model.lib_track_mixin.Fields import Fields as LibTrackMixinFields


class Fields:
    MODEL = 'Criteria'
    CREATED_ON = LibTrackMixinFields.CREATED_ON
    UPDATED_ON = LibTrackMixinFields.UPDATED_ON
    USER = LibTrackMixinFields.USER
    UUID = LibTrackMixinFields.UUID
    LIB_TRACKS = LibTrackMixinFields.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = LibTrackMixinFields.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = LibTrackMixinFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = LibTrackMixinFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = LibTrackMixinFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = LibTrackMixinFields.DURATION_STR_IN_HOUR_MIN_SEC
    NAME = 'name'
    PARENT = 'parent'
    CHILD = 'child'
    ASCENDANT = 'ascendant'
    ASCENDANTS = ASCENDANT + 's'
    DESCENDANT = 'descendant'
    DESCENDANTS = DESCENDANT + 's'
    CHILDREN = 'children'
    ROOT = 'root'
    CRITERIA_PLAYLIST = 'criteria_playlist'
    CRITERIA_ASCENDANT_RELATION_ASCENDANTS = 'criteria_ascendant_rel_ascendants'
    CRITERIA_ASCENDANT_RELATION_DESCENDANTS = 'criteria_ascendant_rel_descendants'
