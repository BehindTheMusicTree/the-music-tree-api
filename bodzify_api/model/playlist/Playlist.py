#!/usr/bin/env python

import shortuuid
from django.db import models
from django.contrib.auth.models import User
from polymorphic.models import PolymorphicModel


class SPECIAL_NAMES:
    ALL = "All"
    GENRELESS = "Genreless"


class ATTRIBUTES_LABEL:
    UUID = "uuid"
    USER = "user"
    ADDED_ON = "added_on"
    NAME = "name"
    PARENT = "parent"
    CRITERIA_NAME = "criteria__name"


class Playlist(PolymorphicModel):
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    added_on = models.DateTimeField(auto_now_add=True, editable=False)
    
    @property
    def name(self) -> str:
        return None
