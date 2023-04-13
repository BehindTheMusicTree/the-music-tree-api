#!/usr/bin/env python
import shortuuid
from django.db import models
from django.contrib.auth.models import User
from bodzify_api.model.playlist.PlaylistType import PlaylistType


class SPECIAL_NAMES:
    ALL = "All"


class ATTRIBUTES_LABEL:
    UUID = "uuid"
    USER = "user"
    TYPE = "type"
    ADDED_ON = "addedOn"
    NAME = "name"


class Playlist(models.Model):
    uuid = models.CharField(
        primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    type = models.ForeignKey(
        PlaylistType, on_delete=models.DO_NOTHING, editable=False)
    addedOn = models.DateTimeField(auto_now_add=True, editable=False)
    
    @property
    def name(self) -> str:
        return None
