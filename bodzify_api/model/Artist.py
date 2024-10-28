#!/usr/bin/env python

from bodzify_api.model.user.User import User
from django.db import models
from django.db.models import QuerySet

from bodzify_api import settings
from bodzify_api.utils.audio_metadata.MetadataManager import METADATA_ARTISTS_SEPARATION_CHAR
from bodzify_api.model.LibTrackMixin import LibTrackMixin, Fields as LibTrackMixinFields


class Fields:
    MODEL = 'artist'
    CREATED_ON = LibTrackMixinFields.CREATED_ON
    UPDATED_ON = LibTrackMixinFields.UPDATED_ON
    UUID = LibTrackMixinFields.UUID
    USER = LibTrackMixinFields.USER
    LIB_TRACKS = LibTrackMixinFields.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = LibTrackMixinFields.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = LibTrackMixinFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = LibTrackMixinFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = LibTrackMixinFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = LibTrackMixinFields.DURATION_STR_IN_HOUR_MIN_SEC
    ALBUMS = 'albums'
    NAME = 'name'


class Artist(LibTrackMixin):
    name = models.CharField(max_length=settings.ARTIST_NAME_LEN_MAX, default=None)

    class Meta:
        constraints = [models.CheckConstraint(check=~models.Q(name=""), name="artist_non_empty_name")]

    @property
    def library_tracks(self) -> models.QuerySet:
        return self.artist_library_tracks  # type: ignore

    @property
    def albums(self) -> models.QuerySet['Album']:  # type: ignore
        return self.albums

    def __str__(self) -> str:
        return f"{self.uuid} {self.name}"

    @staticmethod
    def _get_artists_names_list_from_str(names_str: str) -> list:
        names_with_eventual_spaces_around_and_duplicates = names_str.split(METADATA_ARTISTS_SEPARATION_CHAR)
        names = []
        for name_with_eventual_spaces_around in names_with_eventual_spaces_around_and_duplicates:
            name = name_with_eventual_spaces_around.strip()
            if name != "" and names.count(name) == 0:
                names.append(name)
        return names

    @staticmethod
    def get_artists_list_from_names_str_after_eventual_creation(user: User, artists_names_str: str) -> list['Artist']:
        artists_names_list = Artist._get_artists_names_list_from_str(artists_names_str)
        if len(artists_names_list) > 0:
            return [Artist.objects.get_or_create(user=user, name=artist_name)[0] for artist_name in artists_names_list]
        else:
            return []

    def delete(self):
        from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
        from bodzify_api.model.Album import Album

        albums: QuerySet[Album] = self.albums.all()
        for album in albums:
            album.delete()

        lib_tracks: QuerySet[LibraryTrack] = self.library_tracks.all()
        for lib_track in lib_tracks:
            lib_track.delete()

        return super(Artist, self).delete()

    def delete_if_nothing_linked(self):
        if self.albums.count() == 0:
            if self.library_tracks.count() == 0:
                self.delete()

    def delete_with_albums_and_tracks(self):
        from bodzify_api.model.Album import Album
        from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack

        albums: QuerySet[Album] = self.albums.all()
        for album in albums:
            album.delete_with_tracks_and_eventually_artists()

        lib_tracks: list[LibraryTrack] = list(self.library_tracks.all())
        for track in lib_tracks:
            track.delete_with_checking_album_potential_deletion()

        self.delete()
