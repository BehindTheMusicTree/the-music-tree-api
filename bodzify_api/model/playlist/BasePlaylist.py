from typing import Optional, TYPE_CHECKING

from django.db import models
from django.utils import timezone


from bodzify_api import settings
from bodzify_api.model.trackable_play_count.TrackablePlayCount import TrackablePlayCount
from bodzify_api.model.lib_track_mixin.LibTrackMixin import LibTrackMixin
from .Fields import Fields

if TYPE_CHECKING:
    from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
    from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel


class BasePlaylist(LibTrackMixin, TrackablePlayCount):
    last_track_list_update_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Base Playlist'
        verbose_name_plural = 'Base Playlists'
        indexes = [models.Index(fields=[Fields.USER, Fields.UUID], name='base_playlist_user_uuid_idx')]

    @property
    def library_tracks(self) -> models.QuerySet['LibraryTrack']:
        return getattr(self, Fields.LIB_TRACKS_DB)

    @property
    def lib_track_playlist_rels(self) -> models.QuerySet['LibTrackPlaylistRel']:
        return getattr(self, Fields.LIB_TRACK_PLAYLIST_RELS_DB)

    @property
    def name(self) -> Optional[str]:
        raise NotImplementedError()

    def update_last_track_list_update_date(self):
        self.last_track_list_update_date = timezone.now()
        self.save()
        return self.last_track_list_update_date
