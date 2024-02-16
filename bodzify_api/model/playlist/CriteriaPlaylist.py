#!/usr/bin/env python

from typing import Optional
from django.db import models
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaType
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.Playlist import Playlist

class SPECIAL_NAMES:
    GENRELESS = "Genreless"
    TAGLESS = "Tagless"
    

class TYPES_LABEL:
    GENRE = "genre"
    TAG = "tag"


class ATTRIBUTES_LABEL:
    PARENT = "parent"
    CRITERIA_NAME = 'criteria__name'


class CriteriaPlaylist(Playlist):
    criteria = models.ForeignKey(
        Criteria, on_delete=models.CASCADE, blank=True, null=True)
    type = models.ForeignKey(
        CriteriaType, on_delete=models.CASCADE, blank=True, null=False)

    @property
    def name(self) -> str:
        if self.criteria is None:
            if self.type.pk == CRITERIA_TYPES_ID.GENRE:
                return SPECIAL_NAMES.GENRELESS
            elif self.type.pk == CRITERIA_TYPES_ID.TAG:
                return SPECIAL_NAMES.TAGLESS
        else:
            return self.criteria.name
        
    @property
    def parent(self) -> Optional['Playlist']:
        if self.criteria is None:
            return None
        if self.criteria.parent is None:
            return None
        else:
            return CriteriaPlaylist.objects.get(
                type=self.type,
                criteria=self.criteria.parent)
