#!/usr/bin/env python

import shortuuid

from django.db import models


class PlaylistTypeIds:
    GENRE = 1
    TAG = 2
    CUSTOM = 3


class PlaylistType(models.Model):
    label = models.CharField(unique=True, default=shortuuid.uuid, max_length=200, editable=False)