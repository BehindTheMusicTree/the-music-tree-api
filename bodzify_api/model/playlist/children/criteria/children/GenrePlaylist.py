from abc import abstractmethod

from bodzify_api import settings
from bodzify_api.model import LibTrackMixin
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist


class GenrePlaylist(CriteriaPlaylist):

    class Meta(CriteriaPlaylist.Meta):
        db_table = f'{settings.APP_NAME}_genre_playlist'
        verbose_name = 'Genre Playlist'
        verbose_name_plural = 'Genre Playlists'

    @abstractmethod
    def name_when_no_criteria() -> str:
        return LibTrackMixin.SpecialNames.GENRELESS

    def __str__(self):
        return self.name
