#!/usr/bin/env python

from typing import Optional

import shortuuid
from django.contrib.auth.models import User
from django.db import models


class ATTRIBUTES_LABEL:
    UUID = 'uuid'
    USER = 'user'
    NAME = 'name'
    ALBUMS = 'albums'
    LIB_TRACKS = 'library_tracks'
    LIB_TRACKS_COUNT = LIB_TRACKS + '_count'
    DURATION = 'duration'


class Artist(models.Model):

    # Django's UUIDField won't validate a shortuuid
    uuid = models.CharField(
        primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=200, default=None)

    class Meta:
        constraints = [
            models.CheckConstraint(check=~models.Q(
                name=""), name="artist_non_empty_name")
        ]

    def __str__(self) -> str:
        return str(self.uuid) + " " + self.name

    @staticmethod
    def get_artist_from_name_after_eventual_creation(user: User, artist_name: str) -> Optional['Artist']:
        if artist_name is None or artist_name == "":
            return None
        else:
            try:
                artist = Artist.objects.get(user=user, name=artist_name)
            except Artist.DoesNotExist:
                artist = None

            if artist is not None:
                return artist
            else:
                return Artist.objects.create(user=user, name=artist_name)

    def delete(self):
        from bodzify_api.model.Album import Album
        Album.objects.filter(user=self.user, album_artists__in=[self]).delete()

        from bodzify_api.model.track.LibraryTrack import LibraryTrack
        LibraryTrack.objects.filter(user=self.user, artist=self).delete()
        return super(Artist, self).delete()

    def delete_if_nothing_linked(self):
        from bodzify_api.model.Album import Album
        if Album.objects.filter(user=self.user, album_artists__in=[self]).count() == 0:
            from bodzify_api.model.track.LibraryTrack import LibraryTrack
            if LibraryTrack.objects.filter(user=self.user, artist=self).count() == 0:
                self.delete()

    def delete_with_albums_and_tracks(self):
        from bodzify_api.model.Album import Album
        for album in list(Album.objects.filter(user=self.user, album_artists__in=[self]).all()):
            album.delete_with_tracks_and_eventually_artists()

        from bodzify_api.model.track.LibraryTrack import LibraryTrack
        for track in list(LibraryTrack.objects.filter(user=self.user, artist=self).all()):
            track.delete_with_checking_album_potential_deletion()

        self.delete()
