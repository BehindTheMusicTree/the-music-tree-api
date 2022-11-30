#!/usr/bin/env python

import shortuuid

from django.db import models
from django.contrib.auth.models import User

from bodzify_api.model.criteria.Criteria import Criteria, CriteriaSpecialNames
from bodzify_api.model.playlist.PlaylistType import PlaylistType, PlaylistTypeIds

class PlaylistSpecialNames:
    GENRE_ALL = CriteriaSpecialNames.GENRE_ALL
    GENRE_GENRELESS = CriteriaSpecialNames.GENRE_GENRELESS
    TAG_ALL = CriteriaSpecialNames.TAG_ALL

class Playlist(models.Model):
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=200, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default=None, blank=None, null=False)
    type = models.ForeignKey(PlaylistType, 
        on_delete=models.DO_NOTHING, 
        default=None, 
        blank=False, 
        null=False)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    addedOn = models.DateTimeField(auto_now_add=True)

    @property
    def parent(self):
        if self.criteria is None: return None
        elif self.criteria.parent is None: return None
        else: return Playlist.objects.get(
            user=self.user, 
            type=self.type, 
            criteria=self.criteria.parent)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.criteria is not None: 
            self.name = self.criteria.name