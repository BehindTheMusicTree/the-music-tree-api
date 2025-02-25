from bodzify_api.model.playlist.children.criteria.genre.GenrePlaylist import \
    GenrePlaylist
from bodzify_api.view.viewset.model.playlist.children.criteria.CriteriaPlaylistViewSet import \
    CriteriaPlaylistViewSet


class GenrePlaylistViewSet(CriteriaPlaylistViewSet):
    def __init__(self, **kwargs):
        super().__init__(model_class=GenrePlaylist, **kwargs)