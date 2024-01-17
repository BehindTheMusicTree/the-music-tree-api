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
    ALBUM_ARTISTS = 'albumArtists'
    LIBRARY_TRACKS = 'libraryTracks'
    TRACK_COUNT = 'trackCount'
    DURATION = 'duration'

class Album(models.Model):

    # Django's UUIDField won't validate a shortuuid
    uuid = models.CharField(
            primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    name = models.CharField(max_length=settings.ALBUM_NAME_MAX_CHAR, default=None)
    year = models.CharField(max_length=4, default=None, null=True)
    albumArtists = models.ManyToManyField('bodzify_api.Artist')

    class Meta:
        constraints = [
            models.CheckConstraint(check=~models.Q(name=""), name="album_non_empty_name")
        ]


    def deleteWithTracksAndEventuallyArtists(self):
        artistsLinkedToAlbumAndTrack = list()
        for track in LibraryTrack.objects.filter(user=self.user, album=self):
            if track.artist_id is not None:
                if track.artist not in artistsLinkedToAlbumAndTrack:
                    artistsLinkedToAlbumAndTrack.append(track.artist)
            track.delete()
        
        for albumArtist in list(self.albumArtists.all()):
            if albumArtist not in artistsLinkedToAlbumAndTrack:
                artistsLinkedToAlbumAndTrack.append(albumArtist)

        self.delete()
        
        for artist in artistsLinkedToAlbumAndTrack:
            artist.deleteIfNothingLinked()


    def deleteIfNoTrackLinked(self):
        if LibraryTrack.objects.filter(user=self.user, album=self).count() == 0:
            self.delete()

    def __str__(self) -> str:
        string = self.uuid + " " + self.name + " by "
        for artist in list(self.albumArtists.all()):
            string = string + str(artist) + " "
        return string