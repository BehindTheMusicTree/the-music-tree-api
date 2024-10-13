#!/usr/bin/env python

from typing import Optional

from django.contrib.auth.models import User
from django.db import models

from bodzify_api.model.lib_track_mixin.LibTrackMixin import LibTrackMixin, \
    AttributesLabels as LibTrackMixinAttributesLabels
from bodzify_api.utils.audio_metadata.MetadataManager import METADATA_ARTISTS_SEPARATION_CHAR


class AttributesLabels:
    MODEL = 'artist'
    UUID = LibTrackMixinAttributesLabels.UUID
    USER = LibTrackMixinAttributesLabels.USER
    CREATED_ON = LibTrackMixinAttributesLabels.CREATED_ON
    UPDATED_ON = LibTrackMixinAttributesLabels.UPDATED_ON
    LIB_TRACKS = LibTrackMixinAttributesLabels.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = LibTrackMixinAttributesLabels.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = LibTrackMixinAttributesLabels.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = LibTrackMixinAttributesLabels.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = LibTrackMixinAttributesLabels.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = LibTrackMixinAttributesLabels.DURATION_STR_IN_HOUR_MIN_SEC
    ALBUMS = 'albums'
    NAME = 'name'


class Artist(LibTrackMixin):
    name = models.CharField(max_length=200, default=None)

    class Meta:
        constraints = [models.CheckConstraint(check=~models.Q(name=""), name="artist_non_empty_name")]

    @property
    def library_tracks(self) -> models.QuerySet:
        return self.artist_library_tracks  # type: ignore

    def __str__(self) -> str:
        return f"{self.uuid} {self.name}"

    @staticmethod
    def _get_artists_names_list_from_str(names_str: str) -> list:
        names_with_eventual_spaces_around_and_duplicates = names_str.split(METADATA_ARTISTS_SEPARATION_CHAR)
        names = list()
        for name_with_eventual_spaces_around in names_with_eventual_spaces_around_and_duplicates:
            name = name_with_eventual_spaces_around.strip()
            if name != "" and names.count(name) == 0:
                names.append(name)
        return names

    @staticmethod
    def get_artist_from_name_after_eventual_creation(user: User, artist_name: str) -> Optional['Artist']:
        if artist_name is None or artist_name == "":
            return None
        else:
            try:
                artist = Artist.objects.get(user=user, name=artist_name)
            except Artist.DoesNotExist:
                artist = None

            return artist if artist else Artist.objects.create(user=user, name=artist_name)

    @staticmethod
    def get_artists_list_from_names_str_after_eventual_creation(user: User, artists_names_str: str) -> list:
        artists_names_list = Artist._get_artists_names_list_from_str(artists_names_str)
        if artists_names_list:
            if len(artists_names_list) > 0:
                return [Artist.get_artist_from_name_after_eventual_creation(
                    user=user, artist_name=artist_name) for artist_name in artists_names_list]
            else:
                return []
        else:
            return []

    def delete(self):
        from bodzify_api.model.Album import Album
        Album.objects.filter(user=self.user, album_artists__in=[self]).delete()

        from bodzify_api.model.track.LibraryTrack import LibraryTrack
        LibraryTrack.objects.filter(user=self.user, artists__in=[self]).delete()
        return super(Artist, self).delete()

    def delete_if_nothing_linked(self):
        from bodzify_api.model.Album import Album
        if Album.objects.filter(user=self.user, album_artists=self).count() == 0:
            from bodzify_api.model.track.LibraryTrack import LibraryTrack
            if LibraryTrack.objects.filter(user=self.user, artists=self).count() == 0:
                self.delete()

    def delete_with_albums_and_tracks(self):
        from bodzify_api.model.Album import Album
        from bodzify_api.model.track.LibraryTrack import LibraryTrack

        for album in Album.objects.filter(user=self.user, album_artists=self):
            album.delete_with_tracks_and_eventually_artists()

        for track in LibraryTrack.objects.filter(user=self.user, artists=self):
            track.delete_with_checking_album_potential_deletion()

        self.delete()
