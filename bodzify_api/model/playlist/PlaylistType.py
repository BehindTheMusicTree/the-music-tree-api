#!/usr/bin/env python
from django.db import models


class PlaylistTypesId:
    GENRE = 0
    TAG = 1
    SIMPLE = 2


class PlaylistType(models.Model):
    label = models.CharField(unique=True, max_length=20,
                             editable=False, default=None)
