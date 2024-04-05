#!/usr/bin/env python

from django.db import models
from django.db.models import F

from bodzify_api.model.playlist.Playlist import Playlist, ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.track.LibraryTrack import LibraryTrack, ATTRIBUTES_LABEL as LIB_TRACK_ATTRIBUTES_LABEL


class ATTRIBUTES_LABEL:
    MODEL = 'playlist_lib_track_relation'
    PLAYLIST = PLAYLIST_ATTRIBUTES_LABEL.MODEL
    LIB_TRACK = LIB_TRACK_ATTRIBUTES_LABEL.MODEL
    POSITION = 'position'
    ADDED_ON = 'added_on'


class PlaylistLibTrackRelation(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name=ATTRIBUTES_LABEL.MODEL + 's')
    library_track = models.ForeignKey(LibraryTrack, on_delete=models.CASCADE, related_name=ATTRIBUTES_LABEL.MODEL + 's')
    position = models.PositiveIntegerField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Playlist {self.playlist.uuid} - Track title {self.library_track.title}'

    def save(self, *args, **kwargs):
        if not self.pk:
            playlist_lib_track_relations = PlaylistLibTrackRelation.objects.filter(playlist=self.playlist)
            playlist_lib_track_relations.update(position=models.F(ATTRIBUTES_LABEL.POSITION) + 1)
            self.position = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        playlist_lib_track_relations = PlaylistLibTrackRelation.objects.filter(playlist=self.playlist,
                                                                               position__gt=self.position)
        playlist_lib_track_relations.update(position=F(ATTRIBUTES_LABEL.POSITION) - 1)
        super().delete(*args, **kwargs)
