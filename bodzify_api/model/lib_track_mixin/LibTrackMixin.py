#!/usr/bin/env python


from abc import abstractmethod
from django.db import models

from bodzify_api.model.BaseModel import BaseModel
from bodzify_api.model.BaseModel import AttributesLabels as BaseAttributesLabel


class AttributesLabels:
    MODEL = 'library_track_mixin_child'
    UUID = BaseAttributesLabel.UUID
    USER = BaseAttributesLabel.USER
    CREATED_ON = BaseAttributesLabel.CREATED_ON
    UPDATED_ON = BaseAttributesLabel.UPDATED_ON
    LIB_TRACKS = 'library_tracks'
    LIB_TRACKS_NOT_ARCHIVED = LIB_TRACKS + '_not_archived'
    LIB_TRACKS_COUNT = LIB_TRACKS + '_count'
    LIB_TRACKS_ARCHIVED_COUNT = LIB_TRACKS + '_archived_count'
    DURATION_IN_SEC = 'duration_in_sec'
    DURATION_STR_IN_HOUR_MIN_SEC = 'duration_str_in_hour_min_sec'


class ChildAttributesLabels:
    UUID = f'{AttributesLabels.MODEL}__{AttributesLabels.UUID}'
    USER = f'{AttributesLabels.MODEL}__{AttributesLabels.USER}'
    CREATED_ON = f'{AttributesLabels.MODEL}__{AttributesLabels.CREATED_ON}'
    UPDATED_ON = f'{AttributesLabels.MODEL}__{AttributesLabels.UPDATED_ON}'
    LIB_TRACKS = f'{AttributesLabels.MODEL}__{AttributesLabels.LIB_TRACKS}'
    LIB_TRACKS_NOT_ARCHIVED = f'{AttributesLabels.MODEL}__{AttributesLabels.LIB_TRACKS_NOT_ARCHIVED}'
    LIB_TRACKS_COUNT = f'{AttributesLabels.MODEL}__{AttributesLabels.LIB_TRACKS_COUNT}'
    LIB_TRACKS_ARCHIVED_COUNT = f'{AttributesLabels.MODEL}__{AttributesLabels.LIB_TRACKS_ARCHIVED_COUNT}'
    DURATION_IN_SEC = f'{AttributesLabels.MODEL}__{AttributesLabels.DURATION_IN_SEC}'
    DURATION_STR_IN_HOUR_MIN_SEC = f'{AttributesLabels.MODEL}__{AttributesLabels.DURATION_STR_IN_HOUR_MIN_SEC}'


class LibTrackMixin(BaseModel):

    class Meta:
        abstract = True

    @property
    @abstractmethod
    def library_tracks(self) -> models.QuerySet:
        pass

    @property
    def library_tracks_not_archived(self) -> models.QuerySet:
        return self.library_tracks.filter(archived=False)

    @property
    def library_tracks_count(self) -> int:
        return self.library_tracks.filter(archived=False).count()

    @property
    def library_tracks_archived_count(self) -> int:
        return self.library_tracks.filter(archived=True).count()

    @property
    def duration_in_sec(self) -> int:
        return sum([track.duration_in_sec for track in self.library_tracks_not_archived])

    @property
    def duration_str_in_hour_min_sec(self) -> str:
        total_seconds = self.duration_in_sec
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
