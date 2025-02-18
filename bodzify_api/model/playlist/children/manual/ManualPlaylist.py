from django.db import models

from bodzify_api import settings
from bodzify_api.model.field.AppCharField import AppCharField
from bodzify_api.model.field.foreign_key.PrivateOneToOneField import PrivateOneToOneField
from bodzify_api.model.lib_track_mixin.LibTrackMixinWithInternalNameManager import LibTrackMixinWithInternalNameManager
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.Fields import Fields as PlaylistFields
from bodzify_api.model.playlist.children.manual import ManualPlaylistTypeLabel
from .Fields import Fields


class ManualPlaylist(Playlist):
    playlist = PrivateOneToOneField(Playlist,
                                    on_delete=models.CASCADE,
                                    parent_link=True,
                                    related_name=PlaylistFields.MANUAL_PLAYLIST)

    _name = AppCharField(max_length=settings.MANUAL_PLAYLIST_NAME_LEN_MAX,
                         blank=False,
                         null=False,
                         db_column=Fields.NAME_PUBLIC)  # type: ignore

    objects: LibTrackMixinWithInternalNameManager = LibTrackMixinWithInternalNameManager()

    @property
    def name(self) -> str:
        return self._name

    class Meta:
        constraints = [models.CheckConstraint(check=~models.Q(_name=""), name="manual_playlist_non_empty_name")]
        verbose_name = 'Manual Playlist'
        verbose_name_plural = 'Manual Playlists'
        indexes = [models.Index(fields=[Fields.NAME_INTERNAL], name='manual_playlist_name_idx')]

    @property
    def type_label(self):
        return ManualPlaylistTypeLabel.VALUE
