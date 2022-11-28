#!/usr/bin/env python

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.PlaylistType import PlaylistType, PlaylistTypeLabels

class GenrePlaylist(Playlist):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.type = PlaylistType.objects.get(label=PlaylistTypeLabels.GENRE)
