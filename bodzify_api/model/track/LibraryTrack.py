#!/usr/bin/env python

import os
from typing import Optional
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
from bodzify_api.model.criteria.Criteria import Criteria
import bodzify_api.settings as settings
from bodzify_api.validator.TrackFileValidator import validate_content_type_is_audio, validate_size


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
        validators=[FileExtensionValidator(settings.TRACK_FILE_EXTENSIONS),
            validate_size],
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
        return ""

    @property
    def fileExtension(self) -> str:
        if self.fileExists:
            filename, file_extension = os.path.splitext(self.file.name)
            return file_extension
        return ""

    @property
    def fileExists(self) -> bool:
        if self.file:
            return os.path.isfile(self.file.path)
        return False

    @property
    def relativeUrl(self) -> str:
        return "tracks/{self.uuid}/"

    def __str__(self):
        album_str = f"{ATTRIBUTES_LABEL.ALBUM}: {str(self.album)} " if self.album else ""
        genre_str = f"{ATTRIBUTES_LABEL.GENRE}: {str(self.genre)} " if self.genre else ""
        duration_str = f"{ATTRIBUTES_LABEL.DURATION}: {str(self.duration)} " if self.duration else ""
        rating_str = f"{ATTRIBUTES_LABEL.RATING}: {str(self.rating)} " if self.rating else ""
        language_str = f"{ATTRIBUTES_LABEL.LANGUAGE}: {str(self.language)} " if self.language else ""
        file_str = f"{ATTRIBUTES_LABEL.FILE}: {str(self.file.name)} " if self.file else ""
        return (f"{self.uuid} {str(self.artist)} - {self.title} {album_str}"
                f"{genre_str}{duration_str}{rating_str}{language_str}"
                f"{ATTRIBUTES_LABEL.ADDED_ON}: {str(self.addedOn)} {file_str}")


    def _update_genre_playlists(self, oldGenre: Optional[Criteria]):
        
        if oldGenre is not None and self.genre is not None:
            commonGenre = self.genre.getCommonCriteria(oldGenre)
        else:
            commonGenre = None
            
        self._add_track_to_genre_playlists(genreInTreeToStopAddingTheTrack=commonGenre)

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
        
    def _add_track_to_genre_playlists(self, genreInTreeToStopAddingTheTrack=None):
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
            oldAlbumArtists = []
            if oldAlbum is not None:
                oldAlbumArtists = list(oldAlbum.albumArtists.all())
            super().save(*args, **kwargs)

            if oldGenre != self.genre:
                self._update_genre_playlists(oldGenre=oldGenre)

            if oldAlbum != self.album and oldAlbum is not None:
                oldAlbum.deleteIfNoTrackLinked()
                for albumArtist in oldAlbumArtists:
                    albumArtist.deleteIfNothingLinked()

            if oldArtist != self.artist and oldArtist is not None:
                oldArtist.deleteIfNothingLinked()
        except LibraryTrack.DoesNotExist:
            super().save(*args, **kwargs)
            self.playlists.add(
                SimplePlaylist.objects.get(
                    user=self.user, name=PLAYLIST_SPECIAL_NAMES.ALL))
            self._add_track_to_genre_playlists()


    @ receiver(pre_delete, sender='bodzify_api.LibraryTrack')
    def delete_file_if_exists(sender, instance, using, **kwargs):
        if instance.fileExists:
            instance.file.delete()

    def delete_with_checking_album_and_artist_potential_deletion(self):
        trackArtistId = self.artist.id if self.artist else None
        trackAlbumId = self.album.id if self.album else None
        self.delete()
        self._delete_eventual_related_album(trackAlbumId)
        self._delete_eventual_related_artist(trackArtistId)

    def delete_with_checking_artist_potential_deletion(self):
        trackArtistId = self.artist.id if self.artist else None
        self.delete()
        self._delete_eventual_related_artist(trackArtistId)

    def delete_with_checking_album_potential_deletion(self):
        trackAlbumId = self.album.id if self.album else None
        self.delete()
        self._delete_eventual_related_album(trackAlbumId)

    def _delete_eventual_related_artist(self, track_artist_id):
        if track_artist_id is not None:
            self.artist.deleteIfNothingLinked()

    def _delete_eventual_related_album(self, trackAlbumId):
        if trackAlbumId is not None:
            self.album.deleteIfNoTrackLinked()
