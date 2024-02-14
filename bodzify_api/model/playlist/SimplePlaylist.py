#!/usr/bin/env python

from django.db import models
from bodzify_api import settings
from bodzify_api.model.playlist.Playlist import Playlist


class SimplePlaylist(Playlist):

    name = models.CharField(
        max_length=settings.PLAYLIST_NAME_MAX_CHAR, default=None, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(name=""), name="simple_playlist_non_empty_name")]
