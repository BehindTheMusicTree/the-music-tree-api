#!/usr/bin/env python
import os
import shortuuid

from django.db import models
from django.contrib.auth.models import User

class LibrarySong(models.Model):
    path = models.CharField(max_length=200)
    # Django's UUIDField won't validate a shortuuid
    uuid = models.CharField(unique=True, default=shortuuid.uuid, max_length=200)
    url = models.CharField(unique=True, max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default=None, blank=True, null=True)
    artist = models.CharField(max_length=200, default=None, blank=True, null=True)
    album = models.CharField(max_length=200, default=None, blank=True, null=True)
    genre = models.CharField(max_length=200, default=None, blank=True, null=True)
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

class MineSong:
    def __init__(self, title, artist, duration, releasedOn, url):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.releasedOn = releasedOn
        self.url = url
