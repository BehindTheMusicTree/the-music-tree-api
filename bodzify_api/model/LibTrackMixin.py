#!/usr/bin/env python

from abc import abstractmethod
from django.db import models

from bodzify_api.model.base.PrivateUniqueResource import PrivateUniqueResource, Fields as PrivateResourceFields


class SpecialNames:
    ALL = 'All'
    GENRELESS = 'Genreless'
    TAGLESS = 'Tagless'


class Fields:
    MODEL = 'library_track_mixin_child'
    UUID = PrivateResourceFields.UUID
    USER = PrivateResourceFields.USER
    CREATED_ON = PrivateResourceFields.CREATED_ON
    UPDATED_ON = PrivateResourceFields.UPDATED_ON
    LIB_TRACKS = 'library_tracks'
    LIB_TRACKS_NOT_ARCHIVED = LIB_TRACKS + '_not_archived'
    LIB_TRACKS_COUNT = LIB_TRACKS + '_count'
    LIB_TRACKS_ARCHIVED_COUNT = LIB_TRACKS + '_archived_count'
    DURATION_IN_SEC = 'duration_in_sec'
    DURATION_STR_IN_HOUR_MIN_SEC = 'duration_str_in_hour_min_sec'


class LibTrackMixin(PrivateUniqueResource):

    class Meta:
        abstract = True

    @property
    @abstractmethod
    def library_tracks(self) -> models.QuerySet:
        pass

    @property
    def library_tracks_not_archived(self) -> models.QuerySet['LibraryTrack']:  # type: ignore
        return self.library_tracks.filter(archived=False)

    @property
    def library_tracks_count(self) -> int:
        return self.library_tracks.filter(archived=False).count()

    @property
    def library_tracks_archived_count(self) -> int:
        return self.library_tracks.filter(archived=True).count()

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
