from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from .TagPlaylistManager import TagPlaylistManager


class TagPlaylist(CriteriaPlaylist):
    objects: 'TagPlaylistManager' = TagPlaylistManager()

    class Meta:
        proxy = True