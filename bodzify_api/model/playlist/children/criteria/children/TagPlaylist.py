from abc import abstractmethod
from bodzify_api import settings
from bodzify_api.model import LibTrackMixin
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist


class TagPlaylist(CriteriaPlaylist):

    class Meta(CriteriaPlaylist.Meta):
        db_table = f'{settings.APP_NAME}_tag_playlist'
        verbose_name = 'Tag Playlist'
        verbose_name_plural = 'Tag Playlists'

    @abstractmethod
    def name_when_no_criteria() -> str:
        return LibTrackMixin.SpecialNames.TAGLESS

    def __str__(self):
        return self.name
