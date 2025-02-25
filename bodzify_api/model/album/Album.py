
from typing import TYPE_CHECKING

from django.db import models
from django.db.models import Q

from bodzify_api import settings
from bodzify_api.model.album.AlbumManager import AlbumManager
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.artist.Fields import Fields as ArtistFields
from bodzify_api.model.field.AppCharField import AppCharField
from bodzify_api.model.field.foreign_key.PrivateManyToManyField import \
    PrivateManyToManyField
from bodzify_api.model.lib_track_mixin.LibTrackMixin import LibTrackMixin
from bodzify_api.model.track.lib.Fields import Fields as LibraryTrackFields

from .Fields import Fields

if TYPE_CHECKING:
    from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack


class Album(LibTrackMixin):
    _name = AppCharField(max_length=settings.ALBUM_NAME_LEN_MAX, default=None, db_column=Fields.NAME_PUBLIC)
    year = AppCharField(max_length=4, default=None, null=True)
    album_artists = PrivateManyToManyField(Artist, related_name=ArtistFields.ALBUMS)  # type: ignore

    objects: AlbumManager = AlbumManager()

    @property
    def name(self) -> str:
        return self._name

    @property
    def lib_tracks(self) -> models.QuerySet['LibraryTrack']:
        return getattr(self, Fields.LIB_TRACKS_RELATED_NAME)

    @property
    def lib_tracks_not_archived_sorted(self) -> models.QuerySet['LibraryTrack']:
        return self.lib_tracks_not_archived.annotate(
            null_position=Q(track_number__isnull=True)).order_by(
            'null_position', LibraryTrackFields.TRACK_NUMBER, LibraryTrackFields.TITLE)

    class Meta:
        constraints = [models.CheckConstraint(check=~models.Q(_name=""), name="album_non_empty_name")]

    def __str__(self) -> str:
        string = f"{self.uuid} | {self._name}"

        # Get artist names directly from the database to avoid recursion
        artist_names = self.album_artists.values_list('_name', flat=True)
        if artist_names:
            string += f" by {', '.join(artist_names)}"
        else:
            string += " [No Artist]"

        tracks: list[LibraryTrack] = list(self.lib_tracks_not_archived.all())
        if tracks:
            track_details = []
            for track in tracks:
                track_position = f"{track.track_number}." if track.track_number else "--."
                track_artists = ", ".join(str(artist) for artist in track.artists.all())
                track_artists = f"{track_artists} | " if track_artists else "[No Artist] | "
                track_details.append(f"{track_position}{track_artists}{track.title}")
            track_details_str = "; ".join(track_details)
            string += f" | Tracks not archived: {track_details_str}"

        return string
