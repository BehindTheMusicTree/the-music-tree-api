#!/usr/bin/env python

import shortuuid
from django.db import models
from django.contrib.auth.models import User
from polymorphic.models import PolymorphicModel


class SPECIAL_NAMES:
    ALL = "All"


class ATTRIBUTES_LABEL:
    UUID = "uuid"
    USER = "user"
    ADDED_ON = "addedOn"
    NAME = "name"


class Playlist(PolymorphicModel):
    uuid = models.CharField(
        primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    addedOn = models.DateTimeField(auto_now_add=True, editable=False)

    
    @property
    def name(self) -> str:
        return None
