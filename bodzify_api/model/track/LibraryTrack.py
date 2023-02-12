#!/usr/bin/env python
import os
import shortuuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from upload_validator import FileTypeValidator
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.Artist import Artist
from bodzify_api.model.Album import Album
from bodzify_api.validator.LibraryTrackSizeValidator import trackSize
import bodzify_api.settings as settings


def userDirectoryPath(instance, filename):
    return '{0}{1}/{2}'.format(
            settings.LIBRARIES_FOLDER_NAME + '/' + settings.USER_LIBRARY_FOLDER_NAME_PREFIXE,
            instance.user.id, 
            filename)


class LibraryTrack(models.Model):
    # Django's UUIDField won't validate a shortuuid
    uuid = models.CharField(
            primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(
            upload_to=userDirectoryPath, 
            help_text="Only audio formats accepted", 
            validators=[
                    FileExtensionValidator(['flac', 'wav', 'mp3']), 
                    FileTypeValidator(allowed_types=[ 'audio/*']),
                    trackSize])
    title = models.CharField(max_length=100, default=None)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, default=None, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, default=None, null=True)
    genre = models.ForeignKey(Criteria, on_delete=models.DO_NOTHING)
    duration = models.FloatField(default=None)
    rating = models.IntegerField(
            default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    playlists = models.ManyToManyField(Playlist)
    language = models.CharField(max_length=100, default=None, null=True)
    addedOn = models.DateTimeField(auto_now_add=True, editable=False)


    @property
    def filename(self) -> str:
        return os.path.basename(self.file.path)


    @property
    def fileExtension(self) -> str:
        filename, fileExtension = os.path.splitext(self.file.name)
        return fileExtension


    @property
    def fileExists(self) -> bool:
        return os.path.isfile(self.file.path)


    @property
    def relativeUrl(self) -> str:
        return 'tracks/' + self.uuid + "/"


    def __str__(self) -> str:
        return str(self.user) + " " + self.artist + " " + self.title + " " + str(self.file)
    

    def delete(self):
        if self.fileExists:
            self.file.delete()
        if LibraryTrack.objects.filter(user=self.user, album=self.album).count() == 1:
            self.album.delete()
        else:
            super(LibraryTrack, self).delete()
