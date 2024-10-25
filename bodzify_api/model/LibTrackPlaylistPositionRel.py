#!/usr/bin/env python

from django.db import models
from django.db.models import F
from django.contrib.auth import get_user_model

from bodzify_api.model.base.PrivateStandardResource \
    import PrivateStandardResource, Fields as PrivateStandardResourceFields
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist

User = get_user_model()


class Fields:
    MODEL = 'lib_track_position_relation'
    CREATED_ON = PrivateStandardResourceFields.CREATED_ON
    UPDATED_ON = PrivateStandardResourceFields.UPDATED_ON
    USER = PrivateStandardResourceFields.USER
    BASE_PLAYLIST = 'base_playlist'
    LIB_TRACK = 'library_track'
    POSITION = 'position'
    USER = 'user'


class LibTrackPlaylistPositionRel(PrivateStandardResource):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='track_playlist_positions')
    base_playlist = models.ForeignKey(BasePlaylist,
                                      on_delete=models.CASCADE,
                                      related_name=f"{Fields.MODEL}s")
    library_track = models.ForeignKey('LibraryTrack',
                                      on_delete=models.CASCADE,
                                      related_name=f"{Fields.MODEL}s")
    position = models.PositiveIntegerField()

    class Meta:
        db_table = 'bodzify_api_lib_track_playlist_position_relation'
        verbose_name = 'Library Track Playlist Position Relation'
        verbose_name_plural = 'Library Track Playlist Position Relations'
        indexes = [
            models.Index(fields=['user', 'base_playlist']),
            models.Index(fields=['user', 'library_track']),
        ]

    def __str__(self):
        from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
        library_track: LibraryTrack = self.library_track
        return f'User {self.user} - Playlist {self.base_playlist} - Track title {library_track.title} - ' \
            f'Position {self.position}'

    def save(self, *args, **kwargs):
        if not self.pk:
            lib_track_position_relations = LibTrackPlaylistPositionRel.objects.filter(
                user=self.user, base_playlist=self.base_playlist)
            lib_track_position_relations.update(position=models.F(Fields.POSITION) + 1)
            self.position = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        lib_track_position_relations = LibTrackPlaylistPositionRel.objects.filter(
            user=self.user, base_playlist=self.base_playlist, position__gt=self.position)
        lib_track_position_relations.update(position=F(Fields.POSITION) - 1)
        super().delete(*args, **kwargs)
