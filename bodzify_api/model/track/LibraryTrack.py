#!/usr/bin/env python

import os, shortuuid

from drf_spectacular.utils import extend_schema_field, OpenApiTypes

from django.db import models
from django.contrib.auth.models import User

from bodzify_api.model.tag.Tag import Tag

class LibraryTrack(models.Model):
    path = models.CharField(max_length=200)
    # Django's UUIDField won't validate a shortuuid
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=200, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default=None, blank=True, null=True)
    artist = models.CharField(max_length=200, default=None, blank=True, null=True)
    album = models.CharField(max_length=200, default=None, blank=True, null=True)
    genre = models.ForeignKey(Tag, on_delete=models.SET_NULL, default=None, null=True)
    duration = models.CharField(max_length=200, default=None, blank=True, null=True)
    rating = models.IntegerField (default=None, blank=True, null=True)
    language = models.CharField (max_length=200, default=None, blank=True, null=True)
    addedOn = models.DateTimeField(auto_now_add=True)
    
    @property
    def filename(self) -> str:
        return os.path.basename(self.path)

    @property
    def fileExtension(self) -> str:
        filename, fileExtension = os.path.splitext(self.path)
        return fileExtension

    @property
    def relativeUrl(self) -> str:
        return "tracks/" + self.uuid + "/"