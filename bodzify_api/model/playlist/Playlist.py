#!/usr/bin/env python

import shortuuid
from django.contrib.auth.models import User
from django.db import models


class SPECIAL_NAMES:
    ALL = 'All'
    GENRELESS = 'Genreless'


class ATTRIBUTES_LABEL:
    MODEL = 'playlist'
    UUID = 'uuid'
    USER = 'user'
    ADDED_ON = 'added_on'
    NAME = 'name'
    TYPE = 'type'
    LIB_TRACKS = 'library_tracks'
    LIB_TRACKS_COUNT = LIB_TRACKS + '_count'
    CRITERIA_PLAYLIST = 'criteria_playlist'
    SIMPLE_PLAYLIST = 'simple_playlist'
    PLAY_COUNT = 'play_count'
    PLAYLIST_LIB_TRACK_RELATIONS = 'playlist_lib_track_relations'


FOREIGN_MODEL_ATTRIBUTES_PREFIXE = 'playlist_'


class FOREIGN_MODEL_ATTRIBUTES_LABEL:
    UUID = ''
    USER = ''
    ADDED_ON = ''
    NAME = ''
    TYPE = ''
    LIB_TRACKS = ''
    PLAY_COUNT = ''


for attr, value in vars(ATTRIBUTES_LABEL).items():
    if not attr.startswith("__"):
        setattr(FOREIGN_MODEL_ATTRIBUTES_LABEL, attr, FOREIGN_MODEL_ATTRIBUTES_PREFIXE + value)

FOREIGN_MODEL_RELATIONS_PREFIXE = 'playlist.'


class FOREIGN_MODEL_RELATIONS_STR:
    UUID = ''
    USER = ''
    ADDED_ON = ''
    NAME = ''
    TYPE = ''
    LIB_TRACKS = ''
    LIB_TRACKS_COUNT = ''
    PLAY_COUNT = ''


for attr, value in vars(ATTRIBUTES_LABEL).items():
    if not attr.startswith("__"):
        setattr(FOREIGN_MODEL_RELATIONS_STR, attr, FOREIGN_MODEL_RELATIONS_PREFIXE + value)


class Playlist(models.Model):
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    added_on = models.DateTimeField(auto_now_add=True, editable=False)
    play_count = models.IntegerField(default=0)
