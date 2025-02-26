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
    @abstractmethod
    def lib_tracks_not_archived(self) -> models.QuerySet['LibraryTrack']:
        return self.lib_tracks.filter(archived=False)

    @property
    def lib_tracks_not_archived_sorted(self) -> models.QuerySet['LibraryTrack']:
        return self.lib_tracks_not_archived.order_by(f'-{LibraryTrackFields.CREATED_ON}')

    @property
    def lib_tracks_not_archived_count(self) -> int:
        return self.lib_tracks_not_archived.count()

    @property
    def lib_tracks_archived_count(self) -> int:
        return self.lib_tracks.filter(archived=True).count()

    @property
    def duration_in_sec(self) -> int:
        return sum(
            int(lib_track.track_file.duration_in_sec or 0) if lib_track.track_file else 0
            for lib_track in self.lib_tracks_not_archived.all()
        )

    @property
    def duration_str_in_hour_min_sec(self) -> str:
        total_seconds = self.duration_in_sec
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
