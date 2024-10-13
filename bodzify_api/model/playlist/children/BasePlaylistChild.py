#!/usr/bin/env python

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from bodzify_api.model.playlist.BasePlaylist import AttributesLabels as BaseAttributesLabels, BasePlaylist


class AttributesLabels:
    BASE_PLAYLIST = BaseAttributesLabels.MODEL
    UUID = BaseAttributesLabels.UUID
    USER = BaseAttributesLabels.USER
    CREATED_ON = BaseAttributesLabels.CREATED_ON
    UPDATED_ON = BaseAttributesLabels.UPDATED_ON
    LIB_TRACKS = BaseAttributesLabels.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = BaseAttributesLabels.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = BaseAttributesLabels.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = BaseAttributesLabels.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = BaseAttributesLabels.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = BaseAttributesLabels.DURATION_STR_IN_HOUR_MIN_SEC
    PLAY_COUNT = BaseAttributesLabels.PLAY_COUNT
    LAST_TRACK_LIST_UPDATE_DATE = BaseAttributesLabels.LAST_TRACK_LIST_UPDATE_DATE


class BasePlaylistChild(models.Model):
    # This fields must be overriden in each child class so that the related_name is unique.
    base_playlist = models.OneToOneField(BasePlaylist,
                                         on_delete=models.CASCADE,
                                         primary_key=True)

    class Meta:
        abstract = True

    @property
    def uuid(self) -> str:
        return self.base_playlist.uuid

    @property
    def user(self) -> User:
        return self.base_playlist.user

    @property
    def created_on(self) -> timezone.datetime:
        return self.base_playlist.created_on

    @property
    def updated_on(self) -> timezone.datetime:
        return self.base_playlist.updated_on

    @property
    def library_tracks(self) -> models.QuerySet:
        return self.base_playlist.library_tracks  # type: ignore

    @property
    def library_tracks_count(self) -> int:
        return self.base_playlist.library_tracks_count

    @property
    def library_tracks_archived_count(self) -> int:
        return self.base_playlist.library_tracks_archived_count

    @property
    def duration_in_sec(self) -> int:
        return self.base_playlist.duration_in_sec

    @property
    def duration_str_in_hour_min_sec(self) -> str:
        return self.base_playlist.duration_str_in_hour_min_sec

    @property
    def play_count(self) -> int:
        return self.base_playlist.play_count

    @play_count.setter
    def play_count(self, play_count: int):
        self.base_playlist.play_count = play_count

    @property
    def last_track_list_update_date(self) -> timezone.datetime:
        return self.base_playlist.last_track_list_update_date
