#!/usr/bin/env python

from bodzify_api.model.playlist.criteria.CriteriaPlaylist import CriteriaPlaylist


class SPECIAL_NAMES:
    GENRELESS = "Genreless"


class GenrePlaylist(CriteriaPlaylist):
    
    TYPE_LABEL = 'genre'

    @property
    def noCriteriaName(self) -> str:
        return SPECIAL_NAMES.GENRELESS
