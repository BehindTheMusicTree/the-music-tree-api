from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F

from bodzify_api.model.field.foreign_key.PrivateForeignKey import PrivateForeignKey
from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRelManager import LibTrackPlaylistRelManager
from bodzify_api.model.playlist.Fields import Fields as PlayListFields
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.private_standard_resource.PrivateStandardResource import PrivateStandardResource
from bodzify_api.model.track.lib.Fields import Fields as LibTrackFields
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack

from .Fields import Fields

User = get_user_model()


class LibTrackPlaylistRel(PrivateStandardResource):
    playlist = PrivateForeignKey(Playlist,
                                 on_delete=models.CASCADE,
                                 related_name=PlayListFields.LIB_TRACK_PLAYLIST_RELS_INTERNAL)
    lib_track = PrivateForeignKey(LibraryTrack,
                                  on_delete=models.CASCADE,
                                  related_name=LibTrackFields.LIB_TRACK_PLAYLIST_RELS)
    position = models.PositiveIntegerField()

    objects: LibTrackPlaylistRelManager = LibTrackPlaylistRelManager()

    class Meta:
        verbose_name = 'Library Track Playlist Relation'
        verbose_name_plural = 'Library Track Playlist Relations'
        indexes = [
            models.Index(fields=[Fields.USER, Fields.PLAYLIST]),
            models.Index(fields=[Fields.USER, Fields.LIB_TRACK_INTERNAL]),
        ]

    def __str__(self):
        return (f'User {self.user} | Playlist {self.playlist.name} | Track title {self.lib_track.title} | '
                f'Position {self.position}')

    def _perform_save(self, adding: bool, ctx) -> None:
        if adding:
            lib_track_playlist_rels = LibTrackPlaylistRel.objects.filter(user=self.user, playlist=self.playlist)
            lib_track_playlist_rels.update(position=models.F(Fields.POSITION) + 1)
            self.position = 1

    def delete(self, *args, **kwargs):
        lib_track_playlist_rels = LibTrackPlaylistRel.objects.filter(
            user=self.user, playlist=self.playlist, position__gt=self.position)
        lib_track_playlist_rels.update(position=F(Fields.POSITION) - 1)
        super().delete(*args, **kwargs)
