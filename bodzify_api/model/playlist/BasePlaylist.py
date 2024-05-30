#!/usr/bin/env python

import shortuuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from bodzify_api import settings


class SPECIAL_NAMES:
    ALL = 'All'
    GENRELESS = 'Genreless'


class ATTRIBUTES_LABEL:
    MODEL = 'base_playlist'
    UUID = 'uuid'
    USER = 'user'
    CREATED_ON = 'created_on'
    NAME = 'name'
    TYPE = 'type'
    LIB_TRACKS = 'library_tracks'
    LIB_TRACKS_COUNT = LIB_TRACKS + '_count'
    CRITERIA_PLAYLIST = 'criteria_playlist'
    SIMPLE_PLAYLIST = 'simple_playlist'
    PLAY_COUNT = 'play_count'
    playlist_lib_track_relation_RELATIONS = 'playlist_lib_track_relation_relations'
    LAST_TRACK_LIST_UPDATE_DATE = 'last_track_list_update_date'


FOREIGN_MODEL_ATTRIBUTES_PREFIXE = 'base_playlist_'


class FOREIGN_MODEL_ATTRIBUTES_LABEL:
    UUID = ''
    USER = ''
    CREATED_ON = ''
    NAME = ''
    TYPE = ''
    LIB_TRACKS = ''
    PLAY_COUNT = ''


for attr, value in vars(ATTRIBUTES_LABEL).items():
    if not attr.startswith("__"):
        setattr(FOREIGN_MODEL_ATTRIBUTES_LABEL, attr, FOREIGN_MODEL_ATTRIBUTES_PREFIXE + value)

FOREIGN_MODEL_RELATIONS_PREFIXE = 'base_playlist.'


class FOREIGN_MODEL_RELATIONS_STR:
    UUID = ''
    USER = ''
    CREATED_ON = ''
    NAME = ''
    TYPE = ''
    LIB_TRACKS = ''
    LIB_TRACKS_COUNT = ''
    PLAY_COUNT = ''


for attr, value in vars(ATTRIBUTES_LABEL).items():
    if not attr.startswith("__"):
        setattr(FOREIGN_MODEL_RELATIONS_STR, attr, FOREIGN_MODEL_RELATIONS_PREFIXE + value)


class BasePlaylist(models.Model):
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=settings.UUID_LEN, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    play_count = models.IntegerField(default=0)
    last_track_list_update_date = models.DateTimeField(auto_now_add=True)
    created_on = models.DateTimeField(default=timezone.now, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        db_table = 'base_playlist'
        verbose_name = 'Base Playlist'
        verbose_name_plural = 'Base Playlists'

    def update_last_track_list_update_date(self):
        self.last_track_list_update_date = timezone.now()
        self.save()
        return self.last_track_list_update_date
