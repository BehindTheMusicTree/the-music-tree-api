#!/usr/bin/env python

import os
import shortuuid
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import pre_delete
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.Playlist import SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.validator.LibraryTrackSizeValidator import validateTrackSize
from bodzify_api.model.criteria.Criteria import Criteria
import bodzify_api.settings as settings


def _userDirectoryPath(instance, filename):
    return '{0}{1}/{2}'.format(
        settings.LIBRARIES_DIR_NAME + '/' +
        settings.USER_LIBRARY_DIR_NAME_PREFIXE,
        instance.user.id,
        filename)


class ATTRIBUTES_LABEL:
    UUID = "uuid"
    USER = "user"
    FILE = "file"
    TITLE = "title"
    ARTIST = "artist"
    ALBUM = "album"
    GENRE = "genre"
    DURATION = "duration"
    RATING = "rating"
    PLAYLISTS = "playlists"
    LANGUAGE = "language"
    ADDED_ON = "addedOn"
    FILENAME = "filename"
    FILE_EXTENSION = "fileExtension"
    FILE_EXISTS = "fileExists"
    RELATIVE_URL = "relativeUrl"


class LibraryTrack(models.Model):

    # Django's UUIDField won't validate a shortuuid
    uuid = models.CharField(
        primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    file = models.FileField(
        upload_to=_userDirectoryPath,
        help_text="Only audio formats accepted.",
        validators=[
            FileExtensionValidator(['flac', 'wav', 'mp3']),
            validateTrackSize],
        null=True)
    title = models.CharField(
        max_length=settings.TRACK_TITLE_MAX_CHAR, default=None, null=True)
    artist = models.ForeignKey(
        'bodzify_api.Artist', on_delete=models.CASCADE, default=None, null=True)
    album = models.ForeignKey(
        'bodzify_api.Album', on_delete=models.CASCADE, default=None, null=True)
    genre = models.ForeignKey('bodzify_api.Criteria',
                              on_delete=models.DO_NOTHING,
                              default=None,
                              null=True)
    duration = models.FloatField(default=None)
    rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(settings.TRACK_RATING_MAX_VALUE)
        ])
    playlists = models.ManyToManyField('bodzify_api.Playlist')
    language = models.CharField(
        max_length=settings.TRACK_LANGUAGE_MAX_CHAR, blank=True, default=None, null=True)
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

    def str(self):
        return (self.uuid + " " + str(self.artist) + " - " + self.title + " " +
                ATTRIBUTES_LABEL.ALBUM + ": " +
                str(self.album) + " " + ATTRIBUTES_LABEL.GENRE + ": "
                + str(self.genre) + " " + ATTRIBUTES_LABEL.DURATION + ": " + str(self.duration) +
                " " + ATTRIBUTES_LABEL.RATING + ": " + str(self.rating) + " " +
                ATTRIBUTES_LABEL.LANGUAGE + ": " + self.language + " " + ATTRIBUTES_LABEL.ADDED_ON +
                ": " + str(self.addedOn) + " " + ATTRIBUTES_LABEL.FILE + ": " + self.file.name)

    def _updateGenrePlaylists(self, oldGenre: Criteria):
        
        if oldGenre is not None and self.genre is not None:
            commonGenre = self.genre.getCommonCriteria(oldGenre)
        else:
            commonGenre = None
            
        self._addTrackToGenrePlaylists(genreInTreeToStopAddingTheTrack=commonGenre)

        if oldGenre is not None:
            oldGenreTreeItem = oldGenre
            while oldGenreTreeItem != commonGenre:
                self.playlists.remove(
                    CriteriaPlaylist.objects.get(
                        user=self.user, type_id=CriteriaTypesId.GENRE, criteria=oldGenreTreeItem))
                oldGenreTreeItem = oldGenreTreeItem.parent
        else:
            self.playlists.remove(
                CriteriaPlaylist.objects.get(
                    user=self.user, type_id=CriteriaTypesId.GENRE, criteria=None))
        
        self.save()
        
    def _addTrackToGenrePlaylists(self, genreInTreeToStopAddingTheTrack=None):
        if self.genre is not None:
            newGenreTreeItem = self.genre
            while newGenreTreeItem != genreInTreeToStopAddingTheTrack:
                self.playlists.add(
                    CriteriaPlaylist.objects.get(
                        user=self.user, type_id=CriteriaTypesId.GENRE, criteria=newGenreTreeItem))
                newGenreTreeItem = newGenreTreeItem.parent
        else:
            self.playlists.add(
                CriteriaPlaylist.objects.get(
                    user=self.user, type_id=CriteriaTypesId.GENRE, criteria=None))

    def save(self, *args, **kwargs):
        try:
            oldTrack = LibraryTrack.objects.get(uuid=self.uuid)
            oldGenre = oldTrack.genre
            oldArtist = oldTrack.artist
            oldAlbum = oldTrack.album
            if oldAlbum is not None:
                oldAlbumArtists = list(oldAlbum.albumArtists.all())
            super().save(*args, **kwargs)

            if oldGenre != self.genre:
                self._updateGenrePlaylists(oldGenre=oldGenre)

            if oldAlbum != self.album and oldAlbum != None:
                oldAlbum.deleteIfNoTrackLinked()
                for albumArtist in oldAlbumArtists:
                    albumArtist.deleteIfNothingLinked()

            if oldArtist != self.artist and oldArtist != None:
                oldArtist.deleteIfNothingLinked()
        except LibraryTrack.DoesNotExist:
            super().save(*args, **kwargs)
            self.playlists.add(
                SimplePlaylist.objects.get(
                    user=self.user, name=PLAYLIST_SPECIAL_NAMES.ALL))
            self._addTrackToGenrePlaylists()


    @ receiver(pre_delete, sender='bodzify_api.LibraryTrack')
    def deleteFileIfExists(sender, instance, using, **kwargs):
        if instance.fileExists:
            instance.file.delete()

    def deleteWithCheckingAlbumAndArtistPotentialDeletion(self):
        trackArtistId = self.artist_id
        trackAlbumId = self.album_id
        self.delete()
        self._deleteEventualRelatedAlbum(trackArtistId)
        self._deleteEventualRelatedArtist(trackAlbumId)

    def deleteWithCheckingArtistPotentialDeletion(self):
        trackArtistId = self.artist_id
        self.delete()
        self._deleteEventualRelatedArtist(trackArtistId)

    def deleteWithCheckingAlbumPotentialDeletion(self):
        trackAlbumId = self.album_id
        self.delete()
        self._deleteEventualRelatedAlbum(trackAlbumId)

    def _deleteEventualRelatedArtist(self, trackArtistId):
        if trackArtistId is not None:
            self.artist.deleteIfNothingLinked()

    def _deleteEventualRelatedAlbum(self, trackAlbumId):
        if trackAlbumId is not None:
            self.album.deleteIfNoTrackLinked()
