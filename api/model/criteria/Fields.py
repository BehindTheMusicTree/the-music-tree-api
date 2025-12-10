from api.model.track_mixin.Fields import Fields as TrackMixinFields


class Fields(TrackMixinFields):
    TRACKS_RELATED_NAME = 'tracks_of_criteria'
    ASCENDANTS = 'ascendants'
    ASCENDANTS_RELS = 'ascendants_rels'
    DESCENDANTS = 'descendants'
    DESCENDANTS_RELS = 'descendants_rels'
    ROOT = 'root'
    PARENT = 'parent'
    CHILD = 'child'
    CHILDREN = 'children'
    CRITERIA_PLAYLIST = 'criteria_playlist'
    TREE = 'tree'
