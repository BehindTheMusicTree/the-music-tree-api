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
    name = models.CharField(max_length=settings.ARTIST_NAME_LEN_MAX, default=None)  # type: ignore

    if TYPE_CHECKING:
        albums: models.QuerySet['Album']

    objects: ArtistManager = ArtistManager()

    @property
    def library_tracks(self) -> models.QuerySet['LibraryTrack']:
        return getattr(self, Fields.LIB_TRACKS_RELATED_NAME)

    class Meta:
        constraints = [models.CheckConstraint(check=~models.Q(name=""), name="artist_non_empty_name")]

    def __str__(self) -> str:
        return f"{self.uuid} | {self.name}"

    def delete_with_albums_and_tracks(self) -> tuple[int, dict[str, int]]:
        from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack

        for album in self.albums:
            album.delete_with_tracks_and_eventually_artists()

        lib_tracks: list[LibraryTrack] = list(self.library_tracks.all())
        for track in lib_tracks:
            track.delete_with_checking_album_and_artists_potential_deletion()

        return self.delete()

    def delete_if_nothing_linked(self) -> tuple[int, dict[str, int]]:
        if self.albums.count() == 0:
            if self.library_tracks.count() == 0:
                return self.delete()
        return 0, {}
