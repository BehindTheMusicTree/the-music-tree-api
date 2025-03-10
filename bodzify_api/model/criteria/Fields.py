from bodzify_api.model.lib_track_mixin.Fields import Fields as LibTrackMixinFields


class Fields(LibTrackMixinFields):
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