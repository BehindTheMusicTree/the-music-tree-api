#!/usr/bin/env python

from typing import Optional
from django.db import models
from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL
from bodzify_api.model.criteria.CriteriaType import CriteriaType, CRITERIA_TYPES_ID
from bodzify_api.model.playlist.Playlist import Playlist, ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL


class SPECIAL_NAMES:
    GENRELESS = 'Genreless'
    TAGLESS = 'Tagless'


class TYPES_LABEL:
    GENRE = 'genre'
    TAG = 'tag'


class ATTRIBUTES_LABEL:
    PLAYLIST = 'playlist'
    PARENT = 'parent'
    CRITERIA = 'criteria'
    NAME = 'name'


class CriteriaPlaylist(models.Model):
    playlist = models.OneToOneField(
        Playlist, on_delete=models.CASCADE, primary_key=True, related_name=PLAYLIST_ATTRIBUTES_LABEL.CRITERIA_PLAYLIST)
    criteria = models.OneToOneField(Criteria,
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True,
                                    related_name=PLAYLIST_ATTRIBUTES_LABEL.CRITERIA_PLAYLIST)
    type = models.ForeignKey(CriteriaType, on_delete=models.CASCADE, blank=True, null=False)

    @property
    def name(self):
        if self.criteria is None:
            if self.type.pk == CRITERIA_TYPES_ID.GENRE:
                return SPECIAL_NAMES.GENRELESS
            elif self.type.pk == CRITERIA_TYPES_ID.TAG:
                return SPECIAL_NAMES.TAGLESS
        else:
            return self.criteria.name

    @property
    def parent(self) -> Optional['CriteriaPlaylist']:
        if self.criteria is None:
            return None
        if self.criteria.parent is None:
            return None
        else:
            return CriteriaPlaylist.objects.get(
                type=self.type,
                criteria=self.criteria.parent)
