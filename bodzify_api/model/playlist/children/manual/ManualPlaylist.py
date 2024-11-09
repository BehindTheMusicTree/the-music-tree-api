from django.db import models

from bodzify_api import settings
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from ...PlaylistTypes import PlaylistTypes
from .Fields import Fields


class ManualPlaylist(BasePlaylist):
    name = models.CharField(max_length=settings.MANUAL_PLAYLIST_NAME_LEN_MAX, blank=False, null=False)  # type: ignore

    class Meta:
        constraints = [models.CheckConstraint(check=~models.Q(name=""), name="manual_playlist_non_empty_name")]
        verbose_name = 'Manual Playlist'
        verbose_name_plural = 'Manual Playlists'
        indexes = [models.Index(fields=[Fields.NAME], name='manual_playlist_name_idx'),]

    @property
    def type_label(self):
        return PlaylistTypes.MANUAL
