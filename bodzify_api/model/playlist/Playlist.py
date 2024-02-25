#!/usr/bin/env python

import shortuuid
from django.contrib.auth.models import User
from django.db import models
from polymorphic.models import PolymorphicModel

from bodzify_api import settings


class SPECIAL_NAMES:
    ALL = 'All'
    GENRELESS = 'Genreless'


class ATTRIBUTES_LABEL:
    UUID = 'uuid'
    USER = 'user'
    ADDED_ON = 'added_on'
    NAME = 'name'
    LIBRARY_TRACKS = 'library_tracks'
    LIBRARY_TRACKS_COUNT = LIBRARY_TRACKS + '_count'


FOREIGN_MODEL_ATTRIBUTES_PREFIXE = 'playlist_'


class FOREIGN_MODEL_ATTRIBUTES_LABEL:
    UUID = ''
    USER = ''
    ADDED_ON = ''
    NAME = ''
    LIBRARY_TRACKS = ''


for attr, value in vars(ATTRIBUTES_LABEL).items():
    if not attr.startswith("__"):
        setattr(FOREIGN_MODEL_ATTRIBUTES_LABEL, attr, FOREIGN_MODEL_ATTRIBUTES_PREFIXE + value)

FOREIGN_MODEL_RELATIONS_PREFIXE = 'playlist.'


class FOREIGN_MODEL_RELATIONS_STR:
    UUID = ''
    USER = ''
    ADDED_ON = ''
    NAME = ''
    LIBRARY_TRACKS = ''


for attr, value in vars(ATTRIBUTES_LABEL).items():
    if not attr.startswith("__"):
        setattr(FOREIGN_MODEL_RELATIONS_STR, attr, FOREIGN_MODEL_RELATIONS_PREFIXE + value)


class Playlist(PolymorphicModel):
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    added_on = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=settings.SIMPLE_PLAYLIST_NAME_LENGTH_MAX, blank=True, null=True)
