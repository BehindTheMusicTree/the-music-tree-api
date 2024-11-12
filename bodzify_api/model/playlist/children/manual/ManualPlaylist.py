from django.db import models

from bodzify_api import settings
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.Fields import Fields as PlaylistFields
from .Fields import Fields

TYPE_LABEL = 'manual'


class ManualPlaylist(Playlist):
    playlist = models.OneToOneField(Playlist,
                                    on_delete=models.CASCADE,
                                    parent_link=True,
                                    related_name=PlaylistFields.MANUAL_PLAYLIST)

    name = models.CharField(max_length=settings.MANUAL_PLAYLIST_NAME_LEN_MAX, blank=False, null=False)  # type: ignore

    class Meta:
        constraints = [models.CheckConstraint(check=~models.Q(name=""), name="manual_playlist_non_empty_name")]
        verbose_name = 'Manual Playlist'
        verbose_name_plural = 'Manual Playlists'
        indexes = [models.Index(fields=[Fields.NAME], name='manual_playlist_name_idx')]

    @property
    def type_label(self):
        return TYPE_LABEL
