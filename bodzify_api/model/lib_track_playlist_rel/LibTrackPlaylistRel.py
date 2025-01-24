from django.db import models
from django.db.models import F
from django.contrib.auth import get_user_model

from bodzify_api.model.private_standard_resource.PrivateStandardResource import PrivateStandardResource
from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRelManager import LibTrackPlaylistRelManager
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.Fields import Fields as PlaylistFields
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.model.track.lib.Fields import Fields as LibTrackFields
from .Fields import Fields

User = get_user_model()


class LibTrackPlaylistRel(PrivateStandardResource):
    playlist = models.ForeignKey(Playlist,
                                 on_delete=models.CASCADE,
                                 related_name=PlaylistFields.LIB_TRACK_PLAYLIST_RELS)
    library_track = models.ForeignKey(LibraryTrack,
                                      on_delete=models.CASCADE,
                                      related_name=LibTrackFields.LIB_TRACK_PLAYLIST_RELS)
    position = models.PositiveIntegerField()

    objects: LibTrackPlaylistRelManager = LibTrackPlaylistRelManager()

    class Meta:
        verbose_name = 'Library Track Playlist Relation'
        verbose_name_plural = 'Library Track Playlist Relations'
        indexes = [
            models.Index(fields=[Fields.USER, Fields.PLAYLIST]),
            models.Index(fields=[Fields.USER, Fields.LIB_TRACK]),
        ]

    def __str__(self):
        playlist_str = f'playlist {self.playlist}' if self.playlist else 'no playlist'
        return f'user {self.user} | playlist {self.playlist.name} | track title {self.library_track.title} | ' \
            f'position {self.position}'

    def _perform_save(self, adding: bool, ctx) -> None:
        if adding:
            lib_track_playlist_rels = LibTrackPlaylistRel.objects.filter(
                user=self.user, playlist=self.playlist)
            lib_track_playlist_rels.update(position=models.F(Fields.POSITION) + 1)
            self.position = 1

    def delete(self, *args, **kwargs):
        lib_track_playlist_rels = LibTrackPlaylistRel.objects.filter(
            user=self.user, playlist=self.playlist, position__gt=self.position)
        lib_track_playlist_rels.update(position=F(Fields.POSITION) - 1)
        super().delete(*args, **kwargs)
