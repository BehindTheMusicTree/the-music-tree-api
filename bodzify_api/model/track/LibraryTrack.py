#!/usr/bin/env python

import os, shortuuid

from django.db import models
from django.contrib.auth.models import User

from bodzify_api.model.tag.Tag import Tag
from bodzify_api.model.playlist.TagPlaylist import TagPlaylist

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
    playlists = models.ManyToManyField(TagPlaylist)
    language = models.CharField (max_length=200, default=None, blank=True, null=True)
    addedOn = models.DateTimeField(auto_now_add=True)

    __original_genre = None
    hasChangedGenre = False
    
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_genre = self.genre

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        super().save(force_insert, force_update, *args, **kwargs)
        self.hasChangedGenre = self.__original_genre != self.genre
        self.__original_genre = self.genre