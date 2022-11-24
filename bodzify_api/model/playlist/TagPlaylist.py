#!/usr/bin/env python

from django.db import models

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.PlaylistType import PlaylistType
from bodzify_api.model.tag.Tag import Tag

PLAYLIST_TYPE_TAG_LABEL = "tag"

class TagPlaylist(Playlist):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name = self.tag.name
        self.type = PlaylistType.objects.get(label=PLAYLIST_TYPE_TAG_LABEL)
