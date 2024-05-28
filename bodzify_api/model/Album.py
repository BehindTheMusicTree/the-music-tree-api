#!/usr/bin/env python

from typing import Optional

import shortuuid
from django.contrib.auth.models import User
from django.db import models

import bodzify_api.settings as settings
from bodzify_api.model.Artist import Artist, ATTRIBUTES_LABEL as ARTIST_ATTRIBUTES_LABEL


class ATTRIBUTES_LABEL:
    UUID = 'uuid'
    NAME = 'name'
    YEAR = 'year'
    ALBUM_ARTISTS = 'album_artists'
    LIB_TRACKS = 'library_tracks'
    LIB_TRACKS_COUNT = LIB_TRACKS + '_count'
    DURATION = 'duration'


class Album(models.Model):

    # Django's UUIDField won't validate a shortuuid
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=settings.UUID_LEN, editable=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    name = models.CharField(max_length=settings.ALBUM_NAME_LEN_MAX, default=None)
    year = models.CharField(max_length=4, default=None, null=True)
    album_artists = models.ManyToManyField('bodzify_api.Artist', related_name=ARTIST_ATTRIBUTES_LABEL.ALBUMS)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=~models.Q(
                name=""), name="album_non_empty_name")
        ]

    def __str__(self) -> str:
        string = str(self.uuid) + " " + self.name + " by "
        for artist in list(self.album_artists.all()):
            string = string + " " + str(artist) + " "
        return string

    @property
    def track_count(self):
        return self.library_tracks.count()

    @staticmethod
    def _get_album_from_name_and_artists_list_after_having_eventually_created_album(
            user: User, album_name: str, album_artists: list) -> 'Album':

        album_queryset = Album.objects.filter(user=user, name=album_name)
        if len(album_artists) > 0:
            for album_artist in album_artists:
                album_queryset = album_queryset.filter(
                    album_artists__in=[album_artist])
        else:
            album_queryset = album_queryset.filter(album_artists=None)

        if album_queryset.count() == 0:
            album = Album.objects.create(user=user, name=album_name)
            if album_artists is not None:
                album.album_artists.set(album_artists)
        else:
            album = album_queryset.first()
        return album

    @staticmethod
    def get_album_from_name_and_album_artists_name_list_after_eventual_creations(
            user: User, album_name: str, album_artists_name_list: Optional[list]) -> Optional['Album']:

        if album_name is None or album_name == "":
            return None
        else:
            if album_artists_name_list is not None:
                if len(album_artists_name_list) > 0:
                    album_artists = [Artist.get_artist_from_name_after_eventual_creation(
                        user=user, artist_name=artist_name) for artist_name in album_artists_name_list]
                else:
                    album_artists = []
            else:
                album_artists = []

            return Album._get_album_from_name_and_artists_list_after_having_eventually_created_album(
                user=user, album_name=album_name, album_artists=album_artists)

    def delete_with_tracks_and_eventually_artists(self):
        artists_linked_to_album_and_track = list()
        from bodzify_api.model.track.LibraryTrack import LibraryTrack
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
        from bodzify_api.model.track.LibraryTrack import LibraryTrack
        if LibraryTrack.objects.filter(album=self).count() == 0:
            self.delete()
