#!/usr/bin/env python

from django.db import models
from bodzify_api import settings
from bodzify_api.model.playlist.Playlist import Playlist

TYPE_LABEL = "Simple"


class SPECIAL_NAMES:
    ALL = "All"


class ATTRIBUTES_LABELS:
    PLAYLIST = 'playlist'
    NAME = 'name'


class SimplePlaylist(models.Model):
    playlist = models.OneToOneField(Playlist, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=settings.SIMPLE_PLAYLIST_NAME_LENGTH_MAX, blank=False, null=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(name=""), name="simple_playlist_non_empty_name"
            )
        ]
