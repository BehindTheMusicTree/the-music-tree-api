#!/usr/bin/env python
import shortuuid
from django.db import models
from django.contrib.auth.models import User
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class Album(models.Model):

    ATTRIBUTE_UUID_LABEL = 'uuid'
    ATTRIBUTE_NAME_LABEL = 'name'
    ATTRIBUTE_YEAR_LABEL = 'year'
    ATTRIBUTE_ALBUM_ARTISTS_LABEL = 'albumArtists'
    ATTRIBUTE_LIBRARY_TRACKS_LABEL = 'libraryTracks'
    ATTRIBUTE_TRACK_COUNT_LABEL = 'trackCount'
    ATTRIBUTE_DURATION_LABEL = 'duration'

    # Django's UUIDField won't validate a shortuuid
    uuid = models.CharField(
            primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100, default=None)
    year = models.CharField(max_length=4, default=None, null=True)
    albumArtists = models.ManyToManyField('bodzify_api.Artist')


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
