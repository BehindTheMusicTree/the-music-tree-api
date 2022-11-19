#!/usr/bin/env python

import shortuuid

from django.db import models

class Playlist(models.Model):
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=200, editable=False)
    name = models.CharField(unique=True, default=shortuuid.uuid, max_length=200, editable=False)
    addedOn = models.DateTimeField(auto_now_add=True)
