#!/usr/bin/env python

from bodzify_api.model.playlist.TagPlaylist import TagPlaylist
from bodzify_api.model.playlist.PlaylistType import PlaylistType

PLAYLIST_TYPE_GENRE_LABEL = "genre"

class GenrePlaylist(TagPlaylist):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.type = PlaylistType.objects.get(label=PLAYLIST_TYPE_GENRE_LABEL)
