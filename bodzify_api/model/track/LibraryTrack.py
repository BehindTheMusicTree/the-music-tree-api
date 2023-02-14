#!/usr/bin/env python
import os
import shortuuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from upload_validator import FileTypeValidator
from bodzify_api.validator.LibraryTrackSizeValidator import trackSize
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.PlaylistType import PlaylistType
from bodzify_api.model.playlist.PlaylistType import PlaylistTypeIds
import bodzify_api.settings as settings


def userDirectoryPath(instance, filename):
    return '{0}{1}/{2}'.format(
            settings.LIBRARIES_FOLDER_NAME + '/' + settings.USER_LIBRARY_FOLDER_NAME_PREFIXE,
            instance.user.id, 
            filename)


class LibraryTrack(models.Model):

    ATTRIBUTE_USER_LABEL = "user"
    ATTRIBUTE_FILE_LABEL = "file"
    ATTRIBUTE_TITLE_LABEL = "title"
    ATTRIBUTE_ARTIST_LABEL = "artist"
    ATTRIBUTE_ALBUM_LABEL = "album"
    ATTRIBUTE_GENRE_LABEL = "genre"
    ATTRIBUTE_DURATION_LABEL = "duration"
    ATTRIBUTE_RATING_LABEL = "rating"
    ATTRIBUTE_LANGUAGE_LABEL = "language"
    
    # Django's UUIDField won't validate a shortuuid
    uuid = models.CharField(
            primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(
            upload_to=userDirectoryPath, 
            help_text="Only audio formats accepted.", 
            validators=[
                    FileExtensionValidator(['flac', 'wav', 'mp3']), 
                    FileTypeValidator(allowed_types=[ 'audio/*']),
                    trackSize],
            null=True)
    title = models.CharField(max_length=100, default=None)
    artist = models.ForeignKey(
        'bodzify_api.Artist', on_delete=models.CASCADE, default=None, null=True)
    album = models.ForeignKey('bodzify_api.Album', on_delete=models.CASCADE, default=None, null=True)
    genre = models.ForeignKey('bodzify_api.Criteria', on_delete=models.DO_NOTHING)
    duration = models.FloatField(default=None)
    rating = models.IntegerField(
            default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    playlists = models.ManyToManyField('bodzify_api.Playlist')
    language = models.CharField(max_length=100, default=None, null=True)
    addedOn = models.DateTimeField(auto_now_add=True, editable=False)


    @property
    def filename(self) -> str:
        if self.fileExists:
            return os.path.basename(self.file.path)
        return None


    @property
    def fileExtension(self) -> str:
        if self.fileExists:
            filename, fileExtension = os.path.splitext(self.file.name)
            return fileExtension
        return None


    @property
    def fileExists(self) -> bool:
        if self.file:
            return os.path.isfile(self.file.path)
        return False


    @property
    def relativeUrl(self) -> str:
        return 'tracks/' + self.uuid + "/"
    

    def delete(self):
        if self.fileExists:
            self.file.delete()
        if self.album_id is not None:
            if LibraryTrack.objects.filter(user=self.user, album=self.album).count() == 1:
                self.album.delete()
        super().delete()


    def updatePlaylists(self, oldGenre: Criteria):
        genrePlaylistType = PlaylistType.objects.get(id=PlaylistTypeIds.GENRE)
        commonGenre = self.genre.getCommonCriteria(oldGenre)
        newGenreTreeItem = self.genre

        while newGenreTreeItem != commonGenre:
            self.playlists.add(Playlist.objects.get(
                user=self.user,
                type=genrePlaylistType,
                criteria=newGenreTreeItem))            
            newGenreTreeItem = newGenreTreeItem.parent

        oldGenreTreeItem = oldGenre

        while oldGenreTreeItem != commonGenre:
            self.playlists.remove(Playlist.objects.get(
                user=self.user,
                type=genrePlaylistType,
                criteria=oldGenreTreeItem))
            oldGenreTreeItem = oldGenreTreeItem.parent
        self.save()
