#!/usr/bin/env python

import shortuuid

from django.db import models
from django.contrib.auth.models import User

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.tag.Tag import Tag

TYPE_GENRE = "genre"

class TagPlaylist(models.Model):
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=200, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(unique=True, default=shortuuid.uuid, max_length=200, editable=False)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    addedOn = models.DateTimeField(auto_now_add=True)
