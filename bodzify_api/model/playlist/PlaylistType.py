#!/usr/bin/env python

import shortuuid

from django.db import models


class PlaylistTypeIds:
    GENRE = 0
    TAG = 1
    CUSTOM = 2


class PlaylistType(models.Model):
    label = models.CharField(unique=True, max_length=20, editable=False, default=None)
