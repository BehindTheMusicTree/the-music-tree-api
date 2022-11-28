#!/usr/bin/env python

from bodzify_api.model.playlist.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.PlaylistType import PlaylistType, PlaylistTypeLabels

class GenrePlaylist(CriteriaPlaylist):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.type = PlaylistType.objects.get(label=PlaylistTypeLabels.GENRE)
