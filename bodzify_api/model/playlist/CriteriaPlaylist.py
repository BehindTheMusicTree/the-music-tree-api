#!/usr/bin/env python
from django.db import models
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaType
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
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
            if self.type.id == CriteriaTypesId.GENRE:
                return SPECIAL_NAMES.GENRELESS
            elif self.type.id == CriteriaTypesId.TAG:
                return SPECIAL_NAMES.TAGLESS
        return self.criteria.name
        
    @property
    def parent(self) -> 'Playlist':
        if self.criteria is None:
            return None
        if self.criteria.parent is None:
            return None
        else:
            return CriteriaPlaylist.objects.get(
                user=self.user,
                type=self.type,
                criteria=self.criteria.parent)
