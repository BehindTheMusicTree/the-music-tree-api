from bodzify_api.model.playlist.Fields import Fields as PlaylistFields


class Fields(PlaylistFields):
    CRITERIA = 'criteria'
    PARENT = 'parent'
    ROOT = 'root'
    NAME = 'name'
    CHILDREN = 'children'
    DESCENDANTS = 'descendants'
    ROOT_DESCENDANTS = 'root_descendants'
