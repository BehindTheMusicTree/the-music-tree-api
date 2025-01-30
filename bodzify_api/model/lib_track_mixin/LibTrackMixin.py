from abc import abstractmethod
from typing import TYPE_CHECKING

from django.db import models

from bodzify_api.model.private_unique_resource.PrivateUniqueResource import PrivateUniqueResource
from bodzify_api.model.track.lib.Fields import Fields as LibraryTrackFields

if TYPE_CHECKING:
    from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack


class LibTrackMixin(PrivateUniqueResource):

    class Meta:
        abstract = True

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def lib_tracks(self) -> models.QuerySet['LibraryTrack']:
        pass

    @property
    def lib_tracks_not_archived_sorted(self) -> models.QuerySet['LibraryTrack']:
        return self.lib_tracks.order_by(f'-{LibraryTrackFields.CREATED_ON}')

    @property
    def library_tracks_not_archived(self) -> models.QuerySet['LibraryTrack']:  # type: ignore
        return self.lib_tracks.filter(archived=False)

    @property
    def library_tracks_count(self) -> int:
        return self.lib_tracks.filter(archived=False).count()

    @property
    def library_tracks_archived_count(self) -> int:
        return self.lib_tracks.filter(archived=True).count()

    @property
    def duration_in_sec(self) -> int:
        from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
        lib_tracks_not_archived: models.QuerySet[LibraryTrack] = self.library_tracks_not_archived
        return sum(
            int(library_track.track_file.duration_in_sec or 0) if library_track.track_file else 0
            for library_track in lib_tracks_not_archived
        )

    @property
    def duration_str_in_hour_min_sec(self) -> str:
        total_seconds = self.duration_in_sec
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
