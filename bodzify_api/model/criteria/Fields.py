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
    ASCENDANT = 'ascendant'
    ASCENDANTS = ASCENDANT + 's'
    ASCENDANTS_REL_DB = '_ascendants_rel'
    ASCENDANTS_REL = 'ascendants_rel'
    DESCENDANT = 'descendant'
    DESCENDANTS = DESCENDANT + 's'
    DESCENDANTS_REL_DB = '_descendants_rel'
    DESCENDANTS_REL = 'descendants_rel'
    ROOT_DEGREE = 'root_degree'
    ROOT = 'root'
    PARENT = 'parent'
    CHILD = 'child'
    CHILDREN = 'children'
    CRITERIA_PLAYLIST_DB = '_criteria_playlist'
    CRITERIA_PLAYLIST = 'criteria_playlist'
    criteria_lineage_rel_ascendants = 'criteria_ascendant_rel_ascendants'
    CRITERIA_ASCENDANT_RELATION_DESCENDANTS = 'criteria_ascendant_rel_descendants'
