#!/usr/bin/env python
import shortuuid
from django.db import models
from django.contrib.auth.models import User
from bodzify_api.model.Album import Album
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class Artist(models.Model):

    ATTRIBUTE_NAME_LABEL = 'name'

    # Django's UUIDField won't validate a shortuuid
    uuid = models.CharField(
            primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=200, default=None)

    def delete(self):
        Album.objects.filter(user=self.user, albumArtists__in=[self]).delete()
        LibraryTrack.objects.filter(user=self.user, artist=self).delete()
        return super(Artist, self).delete()
    
    def deleteIfNothingLinked(self):
        if Album.objects.filter(user=self.user, albumArtists__in=[self]).count() == 0:
            if LibraryTrack.objects.filter(user=self.user, artist=self).count() == 0:
                self.delete()

    def deleteWithAlbumsAndTracks(self):
        for album in list(Album.objects.filter(user=self.user, albumArtists__in=[self]).all()):
            album.deleteWithTracksAndEventuallyArtists()

        for track in list(LibraryTrack.objects.filter(user=self.user, artist=self).all()):
            track.deleteWithCheckingAlbumPotentialDeletion()

        self.delete()
        
    def __str__(self) -> str:
        return self.uuid + " " + self.name