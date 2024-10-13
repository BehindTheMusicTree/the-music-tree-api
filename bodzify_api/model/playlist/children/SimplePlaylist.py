#!/usr/bin/env python

from django.contrib.auth.models import User
from django.db import models

from bodzify_api import settings
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist, AttributesLabels as BaseAttributesLabels
from bodzify_api.model.playlist.children.BasePlaylistChild import BasePlaylistChild, \
    AttributesLabels as ChildAttributesLabels

TYPE_LABEL = "simple"


class SpecialNames:
    ALL = "All"


class AttributesLabels:
    BASE_PLAYLIST = ChildAttributesLabels.BASE_PLAYLIST
    UUID = ChildAttributesLabels.UUID
    USER = ChildAttributesLabels.USER
    CREATED_ON = ChildAttributesLabels.CREATED_ON
    UPDATED_ON = ChildAttributesLabels.UPDATED_ON
    LIB_TRACKS = ChildAttributesLabels.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = ChildAttributesLabels.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = ChildAttributesLabels.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = ChildAttributesLabels.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = ChildAttributesLabels.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ChildAttributesLabels.DURATION_STR_IN_HOUR_MIN_SEC
    PLAY_COUNT = ChildAttributesLabels.PLAY_COUNT
    LAST_TRACK_LIST_UPDATE_DATE = ChildAttributesLabels.LAST_TRACK_LIST_UPDATE_DATE
    NAME = 'name'


class SimplePlaylist(BasePlaylistChild):
    base_playlist = models.OneToOneField(BasePlaylist,
                                         on_delete=models.CASCADE,
                                         primary_key=True,
                                         related_name=BaseAttributesLabels.SIMPLE_PLAYLIST_CHILD)
    name = models.CharField(max_length=settings.SIMPLE_PLAYLIST_NAME_LEN_MAX, blank=False, null=False)

    class Meta:
        constraints = [models.CheckConstraint(check=~models.Q(name=""), name="simple_playlist_non_empty_name")]
        db_table = 'bodzify_api_simple_playlist'
        verbose_name = 'Simple Playlist'
        verbose_name_plural = 'Simple Playlists'

    @staticmethod
    def create_simple_playlist(user: User, name: str) -> 'SimplePlaylist':
        base_playlist = BasePlaylist.objects.create(user=user)
        return SimplePlaylist.objects.create(base_playlist=base_playlist, name=name)
