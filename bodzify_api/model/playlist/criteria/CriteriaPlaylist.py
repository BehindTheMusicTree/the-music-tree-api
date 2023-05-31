#!/usr/bin/env python
from django.db import models
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.playlist.Playlist import Playlist


class ATTRIBUTES_LABEL:
    PARENT = "parent"
    CRITERIA_NAME = 'criteria__name'


class CriteriaPlaylist(Playlist):
    
    criteria = models.ForeignKey(
        Criteria, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def name(self) -> str:
        if self.criteria is None:
            return self.noCriteriaName
        return self.criteria.name
    
    @property
    def noCriteriaName(self) -> str:
        return None

    @property
    def parent(self) -> 'Playlist':
        if self.criteria is None:
            return None
        if self.criteria.parent is None:
            return None
        else:
            return Playlist.objects.get(
                user=self.user,
                type=self.type,
                criteria=self.criteria.parent)
