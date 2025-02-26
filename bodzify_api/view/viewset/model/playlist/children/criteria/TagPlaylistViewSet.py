from bodzify_api.model.playlist.children.criteria.tag.TagPlaylist import TagPlaylist
from bodzify_api.view.viewset.model.playlist.children.criteria.CriteriaPlaylistViewSet import CriteriaPlaylistViewSet


class TagPlaylistViewSet(CriteriaPlaylistViewSet):
    def __init__(self, **kwargs):
        super().__init__(model_class=TagPlaylist, **kwargs)