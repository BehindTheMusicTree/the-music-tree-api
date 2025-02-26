from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist

from .GenrePlaylistManager import GenrePlaylistManager


class GenrePlaylist(CriteriaPlaylist):
    objects: 'GenrePlaylistManager' = GenrePlaylistManager()

    class Meta:
        proxy = True