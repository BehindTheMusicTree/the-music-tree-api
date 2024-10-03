#!/usr/bin/env python

from django.db import models
from django.utils import timezone
from bodzify_api.model.BaseModel import BaseModel, AttributesLabels as BaseAttributesLabel


class AttributesLabels:
    UUID = BaseAttributesLabel.UUID
    USER = BaseAttributesLabel.USER
    CREATED_ON = BaseAttributesLabel.CREATED_ON
    UPDATED_ON = BaseAttributesLabel.UPDATED_ON
    LIB_TRACKS = 'library_tracks'
    LIB_TRACKS_NOT_ARCHIVED = LIB_TRACKS + '_not_archived'
    LIB_TRACKS_COUNT = LIB_TRACKS + '_count'
    LIB_TRACKS_COUNT_ARCHIVED = LIB_TRACKS + '_count_archived'
    DURATION_IN_SEC = 'duration_in_sec'
    DURATION_STR_IN_HOUR_MIN_SEC = 'duration_str_in_hour_min_sec'


class LibraryTrackMixin(BaseModel):

    class Meta:
        abstract = True

    @property
    def library_tracks_not_archived(self) -> 'models.QuerySet':
        return self.library_tracks.filter(archived=False)  # type: ignore

    @property
    def library_tracks_count(self) -> int:
        return self.library_tracks.filter(archived=False).count()  # type: ignore

    @property
    def library_tracks_count_archived(self) -> int:
        return self.library_tracks.filter(archived=True).count()  # type: ignore

    @property
    def duration_in_sec(self) -> int:
        from bodzify_api.model.track.LibraryTrack import AttributesLabels as LibTrackAttributesLabels
        value = self.library_tracks.filter(archived=False).aggregate(  # type: ignore
            duration_in_sec=models.Sum(LibTrackAttributesLabels.DURATION_IN_SEC))
        return value[LibTrackAttributesLabels.DURATION_IN_SEC] or 0

    @property
    def duration_str_in_hour_min_sec(self) -> str:
        return str(timezone.timedelta(seconds=self.duration_in_sec))
