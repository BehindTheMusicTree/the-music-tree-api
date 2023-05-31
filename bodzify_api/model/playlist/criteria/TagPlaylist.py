#!/usr/bin/env python

from bodzify_api.model.playlist.criteria.CriteriaPlaylist import CriteriaPlaylist


class SPECIAL_NAMES:
    TAGLESS = "Tagless"
    

class TagPlaylist(CriteriaPlaylist):

    @property
    def noCriteriaName(self) -> str:
        return SPECIAL_NAMES.TAGLESS
