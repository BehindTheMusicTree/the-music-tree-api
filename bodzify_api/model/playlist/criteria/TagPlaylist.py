#!/usr/bin/env python

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.PlaylistType import PlaylistType, PlaylistTypeLabels
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames

class TagPlaylistSpecialNames:
    TAG_ALL = CriteriaSpecialNames.TAG_ALL

class TagPlaylist(Playlist):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.type = PlaylistType.objects.get(label=PlaylistTypeLabels.TAG)
