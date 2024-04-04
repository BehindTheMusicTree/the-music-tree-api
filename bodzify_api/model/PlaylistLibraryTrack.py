#!/usr/bin/env python

from django.db.models import Max
from django.db import models
from django.db.models import F

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class ATTRIBUTES_LABEL:
    PLAYLIST = 'playlist'
    LIB_TRACK = 'library_track'
    POSITION = 'position'
    ADDED_ON = 'added_on'


class PlaylistLibraryTrack(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    library_track = models.ForeignKey(LibraryTrack, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    added_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            max_position = PlaylistLibraryTrack.objects.filter(playlist=self.playlist).aggregate(
                Max(ATTRIBUTES_LABEL.POSITION))[f'{ATTRIBUTES_LABEL.POSITION}__max']
            self.position = (max_position or 0) + 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        PlaylistLibraryTrack.objects.filter(playlist=self.playlist, position__gt=self.position).update(
            position=F(ATTRIBUTES_LABEL.POSITION) - 1)
        super().delete(*args, **kwargs)
