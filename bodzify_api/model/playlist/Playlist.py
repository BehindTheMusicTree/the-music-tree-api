#!/usr/bin/env python
import shortuuid
from django.db import models
from django.contrib.auth.models import User
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.playlist.PlaylistType import PlaylistType


class SPECIAL_NAMES:
    ALL = "All"
    GENRE_GENRED = "Genred"
    GENRE_GENRELESS = "Genreless"


class ATTRIBUTES_LABEL:
    NAME = "name"
    PARENT = "parent"
    TYPE = "type"
    CRITERIA_NAME = 'criteria__name'


class Playlist(models.Model):
    uuid = models.CharField(
        primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    customName = models.CharField(
        max_length=100, default=None, blank=True, null=True)
    type = models.ForeignKey(PlaylistType, on_delete=models.DO_NOTHING, editable=False)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    addedOn = models.DateTimeField(auto_now_add=True, editable=False)

    @property
    def name(self) -> str:
        if self.customName is not None:
            return self.customName
        else:
            return self.criteria.name

    @property
    def parent(self) -> 'Playlist':
        if self.criteria is None:
            return None
        elif self.criteria.parent is None:
            return None
        else:
            return Playlist.objects.get(
                user=self.user,
                type=self.type,
                criteria=self.criteria.parent)
