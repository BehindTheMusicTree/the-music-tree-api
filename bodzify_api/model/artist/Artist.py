from typing import TYPE_CHECKING

from django.db import models

from bodzify_api import settings
from bodzify_api.model.lib_track_mixin.LibTrackMixin import LibTrackMixin
from .Fields import Fields
from .ArtistManager import ArtistManager

if TYPE_CHECKING:
    from bodzify_api.model.album.Album import Album
    from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack


class Artist(LibTrackMixin):
    _name = models.CharField(max_length=settings.ARTIST_NAME_LEN_MAX, default=None, db_column=Fields.NAME)

    @property
    def name(self) -> str:
        return self._name

    if TYPE_CHECKING:
        albums: models.QuerySet['Album']

    objects: ArtistManager = ArtistManager()

    @property
    def library_tracks(self) -> models.QuerySet['LibraryTrack']:
        return getattr(self, Fields.LIB_TRACKS_RELATED_NAME)

    class Meta:
        constraints = [models.CheckConstraint(check=~models.Q(_name=""), name="artist_non_empty_name")]

    def __str__(self) -> str:
        return f"{self.uuid} | {self._name}"
