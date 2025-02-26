from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylistManager import CriteriaPlaylistManager


class GenrePlaylistManager(CriteriaPlaylistManager):
    def get_queryset(self):
        return super().get_queryset().filter(type_id=CriteriaTypePks.GENRE)