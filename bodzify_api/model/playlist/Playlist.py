#!/usr/bin/env python

import shortuuid
from django.db import models
from django.contrib.auth.models import User
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
    TRACK_COUNT = 'track_count'
    LIBRARY_TRACKS = 'librarytracks'

FOREIGN_MODEL_ATTRIBUTES_PREFIXE = 'playlist_'

class FOREIGN_MODEL_ATTRIBUTES_LABEL:
    UUID = ''
    USER = ''
    ADDED_ON = ''
    NAME = ''
    TRACK_COUNT = ''
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
    TRACK_COUNT = ''
    LIBRARY_TRACKS = ''

for attr, value in vars(ATTRIBUTES_LABEL).items():
    if not attr.startswith("__"):
        setattr(FOREIGN_MODEL_RELATIONS_STR, attr, FOREIGN_MODEL_RELATIONS_PREFIXE + value)


class Playlist(PolymorphicModel):
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    added_on = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=settings.PLAYLIST_NAME_LENGTH_MAX, blank=True, null=True)

    @property
    def track_count(self):
        return self.librarytrack_set.count()