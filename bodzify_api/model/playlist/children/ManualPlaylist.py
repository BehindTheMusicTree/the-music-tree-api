#!/usr/bin/env python

from django.db import models

from bodzify_api import settings
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist, Fields as BasePlaylistFields
from bodzify_api.model.playlist.children.ChildPlaylist import ChildPlaylist, \
    Fields as ChildFields

TYPE_LABEL = "simple"


class SpecialNames:
    ALL = "All"


class Fields:
    BASE_PLAYLIST = ChildFields.BASE_PLAYLIST
    CREATED_ON = ChildFields.CREATED_ON
    UPDATED_ON = ChildFields.UPDATED_ON
    UUID = ChildFields.UUID
    USER = ChildFields.USER
    LIB_TRACKS = ChildFields.LIB_TRACKS
    LIB_TRACKS_COUNT = ChildFields.LIB_TRACKS_COUNT
    LIB_TRACKS_NOT_ARCHIVED = ChildFields.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_ARCHIVED_COUNT = ChildFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = ChildFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ChildFields.DURATION_STR_IN_HOUR_MIN_SEC
    PLAY_COUNT = ChildFields.PLAY_COUNT
    LAST_TRACK_LIST_UPDATE_DATE = ChildFields.LAST_TRACK_LIST_UPDATE_DATE
    NAME = 'name'


class ManualPlaylist(ChildPlaylist):
    base_playlist = models.OneToOneField(BasePlaylist,
                                         on_delete=models.CASCADE,
                                         primary_key=True,
                                         related_name=BasePlaylistFields.SIMPLE_CHILD_PLAYLIST)
    name = models.CharField(max_length=settings.MANUAL_PLAYLIST_NAME_LEN_MAX, blank=False, null=False)

    class Meta:
        constraints = [models.CheckConstraint(check=~models.Q(name=""), name="manual_playlist_non_empty_name")]
        db_table = 'bodzify_api_manual_playlist'
        verbose_name = 'Manual Playlist'
        verbose_name_plural = 'Manual Playlists'
        indexes = [models.Index(fields=[Fields.BASE_PLAYLIST, Fields.NAME], name='manual_playlist_name_idx'),]
