#!/usr/bin/env python

import shortuuid

from django.db import models

class PlaylistTypeLabels:
    GENRE = "genre"
    TAG = "tag"
    CUSTOM = "custom"

class PlaylistType(models.Model):
    label = models.CharField(unique=True, default=shortuuid.uuid, max_length=200, editable=False)