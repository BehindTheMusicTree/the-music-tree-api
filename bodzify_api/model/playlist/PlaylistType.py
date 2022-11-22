#!/usr/bin/env python

import shortuuid

from django.db import models

class Playlist(models.Model):
    label = models.CharField(unique=True, default=shortuuid.uuid, max_length=200, editable=False)