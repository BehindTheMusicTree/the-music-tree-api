
from typing import List, TYPE_CHECKING
from django.db import models
from django.db.models import Q

from bodzify_api import settings
from bodzify_api.model.album.AlbumManager import AlbumManager
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.artist.Fields import Fields as ArtistFields
from bodzify_api.model.lib_track_mixin.LibTrackMixin import LibTrackMixin
from bodzify_api.model.track.lib.Fields import Fields as LibraryTrackFields
from .Fields import Fields

if TYPE_CHECKING:
    from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack


class Album(LibTrackMixin):
    _name = models.CharField(max_length=settings.ALBUM_NAME_LEN_MAX,
                             default=None, db_column=Fields.NAME)  # type: ignore
    year = models.CharField(max_length=4, default=None, null=True)
    album_artists = models.ManyToManyField(Artist, related_name=ArtistFields.ALBUMS)  # type: ignore

    objects: AlbumManager = AlbumManager()

    @property
    def name(self) -> str:
        return self._name

    @property
    def library_tracks(self) -> models.QuerySet['LibraryTrack']:
        return getattr(self, Fields.LIB_TRACKS_RELATED_NAME)

    @property
    def lib_tracks_sorted(self) -> models.QuerySet['LibraryTrack']:
        return self.library_tracks.annotate(
            null_position=Q(position_in_album__isnull=True)).order_by(
            'null_position', LibraryTrackFields.POSITION_IN_ALBUM, LibraryTrackFields.TITLE)

    class Meta:
        constraints = [models.CheckConstraint(check=~models.Q(_name=""), name="album_non_empty_name")]

    def __str__(self) -> str:
        from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack

        string = f"{self.uuid} {self._name}"

        artists = self.album_artists.all()
        artist_names = " ".join(str(artist) for artist in artists) if artists else "[No Artist]"
        string += f" by {artist_names}"

        tracks: list[LibraryTrack] = list(self.library_tracks.all())
        if tracks:
            track_details = []
            for track in tracks:
                track_position = f"{track.position_in_album}." if track.position_in_album else "--."
                track_artists = ", ".join(str(artist) for artist in track.artists.all())
                track_artists = f"{track_artists} | " if track_artists else "[No Artist] | "
                track_details.append(f"{track_position}{track_artists}{track.title}")
            track_details_str = "; ".join(track_details)
            string += f" | Tracks: {track_details_str}"

        return string
