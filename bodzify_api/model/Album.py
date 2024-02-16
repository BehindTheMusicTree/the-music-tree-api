#!/usr/bin/env python

import shortuuid
from django.db import models
from django.contrib.auth.models import User
from bodzify_api.model.track.LibraryTrack import LibraryTrack
import bodzify_api.settings as settings

class ATTRIBUTES_LABEL:
    UUID = 'uuid'
    NAME = 'name'
    YEAR = 'year'
    ALBUM_ARTISTS = 'album_artists'
    LIBRARY_TRACKS = 'library_tracks'
    TRACK_COUNT = 'track_count'
    DURATION = 'duration'

class Album(models.Model):

    # Django's UUIDField won't validate a shortuuid
    uuid = models.CharField(
            primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    name = models.CharField(max_length=settings.ALBUM_NAME_LENGTH_MAX, default=None)
    year = models.CharField(max_length=4, default=None, null=True)
    album_artists = models.ManyToManyField('bodzify_api.Artist')

    class Meta:
        constraints = [
            models.CheckConstraint(check=~models.Q(name=""), name="album_non_empty_name")
        ]

    def __str__(self) -> str:
        string = str(self.uuid) + " " + self.name + " by "
        for artist in list(self.album_artists.all()):
            string = string + " " + str(artist) + " "
        return string
    
    @property
    def track_count(self):
        return self.librarytrack_set.count()
    
    def delete_with_tracks_and_eventually_artists(self):
        artists_linked_to_album_and_track = list()
        for track in LibraryTrack.objects.filter(album=self):
            if track.artist_id is not None:
                if track.artist not in artists_linked_to_album_and_track:
                    artists_linked_to_album_and_track.append(track.artist)
            track.delete()
        
        for album_artist in list(self.album_artists.all()):
            if album_artist not in artists_linked_to_album_and_track:
                artists_linked_to_album_and_track.append(album_artist)

        self.delete()
        
        for artist in artists_linked_to_album_and_track:
            artist.delete_if_nothing_linked()


    def delete_if_no_track_linked(self):
        if LibraryTrack.objects.filter(album=self).count() == 0:
            self.delete()