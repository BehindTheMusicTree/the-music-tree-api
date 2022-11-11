#!/usr/bin/env python

import os
import shortuuid

from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=200, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default=None, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, blank=True, null=True)
    addedOn = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.uuid + " " + self.name + " " + str(self.parent)

class LibraryTrack(models.Model):
    path = models.CharField(max_length=200)
    # Django's UUIDField won't validate a shortuuid
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=200, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default=None, blank=True, null=True)
    artist = models.CharField(max_length=200, default=None, blank=True, null=True)
    album = models.CharField(max_length=200, default=None, blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, default=None, null=True)
    duration = models.CharField(max_length=200, default=None, blank=True, null=True)
    rating = models.IntegerField (default=None, blank=True, null=True)
    language = models.CharField (max_length=200, default=None, blank=True, null=True)
    addedOn = models.DateTimeField(auto_now_add=True)

    @property
    def filename(self):
        return os.path.basename(self.path)

    @property
    def fileExtension(self):
        filename, fileExtension = os.path.splitext(self.path)
        return fileExtension

    @property
    def relativeUrl(self):
        return "tracks/" + self.uuid + "/"

class MineTrack:
    def __init__(self, title, artist, duration, releasedOn, url):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.releasedOn = releasedOn
        self.url = url