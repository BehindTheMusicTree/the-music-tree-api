#!/usr/bin/env python
import os

from django.db import models
from django.contrib.auth.models import User

class SongDB(models.Model):
    path = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default=None, blank=True, null=True)
    artist = models.CharField(max_length=200, default=None, blank=True, null=True)
    album = models.CharField(max_length=200, default=None, blank=True, null=True)
    genre = models.CharField(max_length=200, default=None, blank=True, null=True)
    duration = models.CharField(max_length=200, default=None, blank=True, null=True)
    rating = models.IntegerField (default=None, blank=True, null=True)
    language = models.CharField (max_length=200, default=None, blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)

    @property
    def filename(self):
        return os.path.basename(self.path)

    @property
    def fileExtension(self):
        filename, fileExtension = os.path.splitext(self.path)
        return fileExtension

class ExternalSong:
    def __init__(self, filename, title, artist, duration, date, url):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.date = date
        self.url = url
