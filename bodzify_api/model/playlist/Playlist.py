from abc import abstractmethod
from typing import TYPE_CHECKING, Optional

from django.db import models
from django.utils import timezone

from bodzify_api.model.playlist.PlaylistManager import PlaylistManager
from bodzify_api.model.trackable_play_count.TrackablePlayCount import TrackablePlayCount
from bodzify_api.model.lib_track_mixin.LibTrackMixin import LibTrackMixin
from .Fields import Fields

if TYPE_CHECKING:
    from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
    from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
    from .children.manual.ManualPlaylist import ManualPlaylist
    from .children.criteria.CriteriaPlaylist import CriteriaPlaylist


class Playlist(LibTrackMixin, TrackablePlayCount):
    last_track_list_update_date = models.DateTimeField(auto_now_add=True)

    objects: PlaylistManager = PlaylistManager()

    if TYPE_CHECKING:
        lib_track_playlist_rels: models.QuerySet['LibTrackPlaylistRel']
        manual_playlist: Optional['ManualPlaylist']
        criteria_playlist: Optional['CriteriaPlaylist']

    class Meta:
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'
        indexes = [models.Index(fields=[Fields.USER, Fields.UUID], name='playlist_user_uuid_idx')]

    @property
    def library_tracks(self) -> models.QuerySet['LibraryTrack']:
        return getattr(self, Fields.LIB_TRACKS_RELATED_NAME)

    @property
    def type_label(self) -> str:
        if hasattr(self, Fields.MANUAL_PLAYLIST):
            if not self.manual_playlist:
                raise ValueError('Playlist has no manual playlist')
            return self.manual_playlist.type_label
        elif hasattr(self, Fields.CRITERIA_PLAYLIST):
            if not self.criteria_playlist:
                raise ValueError('Playlist has no criteria playlist')
            return self.criteria_playlist.type_label
        else:
            raise ValueError('Playlist has no type')

    @property
    @abstractmethod
    def name(self) -> str:
        if hasattr(self, Fields.MANUAL_PLAYLIST):
            if not self.manual_playlist:
                raise ValueError('Playlist has no manual playlist')
            return self.manual_playlist.name
        elif hasattr(self, Fields.CRITERIA_PLAYLIST):
            if not self.criteria_playlist:
                raise ValueError('Playlist has no criteria playlist')
            return self.criteria_playlist.name
        else:
            raise ValueError('Playlist has no name')

    def update_last_track_list_update_date(self):
        self.last_track_list_update_date = timezone.now()
        self.save()
        return self.last_track_list_update_date
