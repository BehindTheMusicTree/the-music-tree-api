#!/usr/bin/env python

from django.db import models

from bodzify_api import settings
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist, AttributesLabel as PLAYLIST_ATTRIBUTES_LABEL

TYPE_LABEL = "simple"


class SpecialNames:
    ALL = "All"


class AttributesLabel:
    BASE_PLAYLIST = 'base_playlist'
    NAME = 'name'


class SimplePlaylist(models.Model):
    base_playlist = models.OneToOneField(BasePlaylist,
                                         on_delete=models.CASCADE,
                                         primary_key=True,
                                         related_name=PLAYLIST_ATTRIBUTES_LABEL.SIMPLE_PLAYLIST)
    name = models.CharField(max_length=settings.SIMPLE_PLAYLIST_NAME_LEN_MAX, blank=False, null=False)
    updated_on = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(name=""), name="simple_playlist_non_empty_name"
            )
        ]
        db_table = 'bodzify_api_simple_playlist'
        verbose_name = 'Simple Playlist'
        verbose_name_plural = 'Simple Playlists'
