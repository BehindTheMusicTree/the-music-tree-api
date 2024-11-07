from django.db import models

from bodzify_api import settings
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from ..ChildPlaylistTypes import ChildPlaylistTypes
from .Fields import Fields


class ManualPlaylist(BasePlaylist):
    _name = models.CharField(max_length=settings.MANUAL_PLAYLIST_NAME_LEN_MAX, blank=False, null=False)

    class Meta:
        constraints = [models.CheckConstraint(check=~models.Q(_name=""), name="manual_playlist_non_empty_name")]
        db_table = f'{settings.APP_NAME}_manual_playlist'
        verbose_name = 'Manual Playlist'
        verbose_name_plural = 'Manual Playlists'
        indexes = [models.Index(fields=[Fields.NAME_DB], name='manual_playlist_name_idx'),]

    @property
    def type_label(self):
        return ChildPlaylistTypes.MANUAL

    @property
    def name(self):
        return self._name
