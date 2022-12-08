#!/usr/bin/env python

import os
import shortuuid

from django.db import models
from django.contrib.auth.models import User

from upload_validator import FileTypeValidator

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.validator.track import track_size
import bodzify_api.settings as settings


def user_directory_path(instance, filename):
    return '{0}{1}/{2}'.format(
        settings.USER_LIBRARY_FOLDER_NAME_PREFIXE, 
        instance.user.id, 
        filename)


class LibraryTrack(models.Model):
    # Django's UUIDField won't validate a shortuuid
    uuid = models.CharField(
        primary_key=True,
        default=shortuuid.uuid,
        max_length=200,
        editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=user_directory_path, 
        help_text="Only audio formats accepted", 
        validators=[FileTypeValidator(allowed_types=[ 'audio/*']), track_size])
    title = models.CharField(max_length=200, default=None, blank=True, null=True)
    artist = models.CharField(max_length=200, default=None, blank=True, null=True)
    album = models.CharField(max_length=200, default=None, blank=True, null=True)
    genre = models.ForeignKey(
        Criteria, 
        on_delete=models.DO_NOTHING, 
        default=None,
        null=False)
    duration = models.CharField(max_length=200, default=None, blank=True, null=True)
    rating = models.IntegerField(default=None, blank=True, null=True)
    playlists = models.ManyToManyField(Playlist)
    language = models.CharField(max_length=200, default=None, blank=True, null=True)
    addedOn = models.DateTimeField(auto_now_add=True)
    

    @property
    def filename(self) -> str:
        return self.file.name


    @property
    def fileExtension(self) -> str:
        filename, fileExtension = os.path.splitext(self.file.name)
        return fileExtension


    @property
    def url(self) -> str:
        return self.file.url


    def __str__(self) -> str:
        return str(self.user) + " " + self.artist + " " + self.title + " " + str(self.file) 
