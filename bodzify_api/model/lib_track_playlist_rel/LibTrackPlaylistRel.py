from django.db import models
from django.db.models import F
from django.contrib.auth import get_user_model

from bodzify_api import settings
from bodzify_api.model.private_standard_resource.PrivateStandardResource import PrivateStandardResource
from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRelManager import LibTrackPlaylistRelManager
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.model.playlist.Fields import Fields as BasePlaylistFields
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.model.track.lib.Fields import Fields as LibTrackFields
from .Fields import Fields

User = get_user_model()


class LibTrackPlaylistRel(PrivateStandardResource):
    base_playlist = models.ForeignKey(BasePlaylist,
                                      on_delete=models.CASCADE,
                                      related_name=BasePlaylistFields.LIB_TRACK_PLAYLIST_RELS_DB)
    library_track = models.ForeignKey(LibraryTrack,
                                      on_delete=models.CASCADE,
                                      related_name=LibTrackFields.LIB_TRACK_PLAYLIST_RELS_DB)
    position = models.PositiveIntegerField()

    objects: LibTrackPlaylistRelManager = LibTrackPlaylistRelManager()

    class Meta:
        verbose_name = 'Library Track Playlist Relation'
        verbose_name_plural = 'Library Track Playlist Relations'
        indexes = [
            models.Index(fields=[Fields.USER, Fields.BASE_PLAYLIST]),
            models.Index(fields=[Fields.USER, Fields.LIB_TRACK]),
        ]

    def __str__(self):
        from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
        library_track: LibraryTrack = self.library_track
        return f'user {self.user} | playlist {self.base_playlist} | track title {library_track.title} | ' \
            f'position {self.position}'

    def save(self, *args, **kwargs):
        if not self.pk:
            lib_track_playlist_rels = LibTrackPlaylistRel.objects.filter(
                user=self.user, base_playlist=self.base_playlist)
            lib_track_playlist_rels.update(position=models.F(Fields.POSITION) + 1)
            self.position = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        lib_track_playlist_rels = LibTrackPlaylistRel.objects.filter(
            user=self.user, base_playlist=self.base_playlist, position__gt=self.position)
        lib_track_playlist_rels.update(position=F(Fields.POSITION) - 1)
        super().delete(*args, **kwargs)
