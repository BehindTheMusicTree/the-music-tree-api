#!/usr/bin/env python
import shortuuid
from django.db import models
from django.contrib.auth.models import User
from bodzify_api.model.Album import Album
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class ATTRIBUTES_LABEL:
    UUID = 'uuid'
    USER = 'user' 
    NAME = 'name'


class Artist(models.Model):

    # Django's UUIDField won't validate a shortuuid
    uuid = models.CharField(
            primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=200, default=None)

    class Meta:
        constraints = [
            models.CheckConstraint(check=~models.Q(name=""), name="artist_non_empty_name")
        ]

    def delete(self):
        Album.objects.filter(user=self.user, album_artists__in=[self]).delete()
        LibraryTrack.objects.filter(user=self.user, artist=self).delete()
        return super(Artist, self).delete()
    
    def delete_if_nothing_linked(self):
        if Album.objects.filter(user=self.user, album_artists__in=[self]).count() == 0:
            if LibraryTrack.objects.filter(user=self.user, artist=self).count() == 0:
                self.delete()

    def delete_with_albums_and_tracks(self):
        for album in list(Album.objects.filter(user=self.user, album_artists__in=[self]).all()):
            album.delete_with_tracks_and_eventually_artists()

        for track in list(LibraryTrack.objects.filter(user=self.user, artist=self).all()):
            track.delete_with_checking_album_potential_deletion()

        self.delete()
        
    def __str__(self) -> str:
        return str(self.uuid) + " " + self.name