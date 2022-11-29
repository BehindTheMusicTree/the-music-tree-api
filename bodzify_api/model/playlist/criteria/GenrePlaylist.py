#!/usr/bin/env python

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.PlaylistType import PlaylistType, PlaylistTypeIds
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames

class GenrePlaylistSpecialNames:
    GENRE_ALL = CriteriaSpecialNames.GENRE_ALL
    GENRE_GENRELESS = CriteriaSpecialNames.GENRE_GENRELESS

class GenrePlaylist(Playlist):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.type = PlaylistType.objects.get(label=PlaylistTypeIds.GENRE)
