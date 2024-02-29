#!/usr/bin/env python

import os
from typing import Optional

import shortuuid
from django.contrib.auth.models import User
from django.core.validators import (FileExtensionValidator, MaxValueValidator,
                                    MinValueValidator)
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

import bodzify_api.AudioMetadataManager as AudioMetadataManager
from bodzify_api.model.Album import ATTRIBUTES_LABEL as ALBUM_ATTRIBUTES_LABEL
import bodzify_api.settings as settings
from bodzify_api.model.Artist import ATTRIBUTES_LABEL as ARTIST_ATTRIBUTES_LABEL
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL, \
    SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.validator.TrackFileValidator import validate_size


def _get_user_directory_path(instance, filename):
    return '{0}{1}/{2}'.format(
        settings.LIB_DIR_NAME + '/' +
        settings.USER_LIB_DIR_NAME_PREFIXE,
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
    ADDED_ON = "added_on"
    FILENAME = "filename"
    FILE_EXTENSION = "file_extension"
    FILE_EXISTS = "file_exists"
    RELATIVE_URL = "relative_url"


class LibraryTrack(models.Model):

    # Django's UUIDField won't validate a shortuuid
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=22, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    file = models.FileField(upload_to=_get_user_directory_path,
                            help_text="Only audio formats accepted.",
                            validators=[FileExtensionValidator(settings.LIB_TRACK_FILE_EXTENSIONS), validate_size],
                            null=True)
    title = models.CharField(max_length=settings.LIB_TRACK_TITLE_LENGTH_MAX, default=None, null=True)
    artist = models.ForeignKey('bodzify_api.Artist',
                               on_delete=models.CASCADE,
                               default=None,
                               null=True,
                               related_name=ARTIST_ATTRIBUTES_LABEL.LIBRARY_TRACKS)
    album = models.ForeignKey('bodzify_api.Album',
                              on_delete=models.CASCADE,
                              default=None,
                              null=True,
                              related_name=ALBUM_ATTRIBUTES_LABEL.LIBRARY_TRACKS)
    genre = models.ForeignKey('bodzify_api.Criteria', on_delete=models.DO_NOTHING, default=None, null=True)
    duration = models.FloatField(default=None)
    rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(settings.LIB_TRACK_RATING_VALUE_MAX)
        ])
    playlists = models.ManyToManyField('bodzify_api.Playlist', related_name=PLAYLIST_ATTRIBUTES_LABEL.LIBRARY_TRACKS)
    language = models.CharField(max_length=settings.LIB_TRACK_LANGUAGE_LENGTH_MAX, blank=True, default=None, null=True)
    added_on = models.DateTimeField(auto_now_add=True, editable=False)

    @property
    def filename(self) -> str:
        if self.file_exists:
            return os.path.basename(self.file.path)
        return ""

    @property
    def file_extension(self) -> str:
        if self.file_exists:
            filename, file_extension = os.path.splitext(self.file.name)
            return file_extension
        return ""

    @property
    def file_exists(self) -> bool:
        if self.file:
            return os.path.isfile(self.file.path)
        return False

    @property
    def relative_url(self) -> str:
        return "tracks/" + self.uuid + "/"

    def __str__(self):
        album_str = f"{ATTRIBUTES_LABEL.ALBUM}: {str(self.album)} " if self.album else ""
        genre_str = f"{ATTRIBUTES_LABEL.GENRE}: {str(self.genre)} " if self.genre else ""
        duration_str = f"{ATTRIBUTES_LABEL.DURATION}: {str(self.duration)} " if self.duration else ""
        rating_str = f"{ATTRIBUTES_LABEL.RATING}: {str(self.rating)} " if self.rating else ""
        language_str = f"{ATTRIBUTES_LABEL.LANGUAGE}: {str(self.language)} " if self.language else ""
        file_str = f"{ATTRIBUTES_LABEL.FILE}: {str(self.file.name)} " if self.file else ""
        return (f"{self.uuid} {str(self.artist)} - {self.title} {album_str}"
                f"{genre_str}{duration_str}{rating_str}{language_str}"
                f"{ATTRIBUTES_LABEL.ADDED_ON}: {str(self.added_on)} {file_str}")

    def save(self, *args, **kwargs):
        try:
            old_track = LibraryTrack.objects.get(uuid=self.uuid)
            old_album_artists = []
            if old_track.album is not None:
                old_album_artists = list(old_track.album.album_artists.all())
            super().save(*args, **kwargs)

            if old_track.genre != self.genre:
                self._update_genre_playlists(old_genre=old_track.genre)

            if old_track.album != self.album and old_track.album is not None:
                old_track.album.delete_if_no_track_linked()
                for album_artist in old_album_artists:
                    album_artist.delete_if_nothing_linked()

            if old_track.artist != self.artist and old_track.artist is not None:
                old_track.artist.delete_if_nothing_linked()

            self._update_file_tags_if_file_exists()

        except LibraryTrack.DoesNotExist:
            super().save(*args, **kwargs)
            all_simple_playlist = SimplePlaylist.objects.get(
                playlist__user=self.user, name=PLAYLIST_SPECIAL_NAMES.ALL)
            self.playlists.add(all_simple_playlist.playlist)
            self._add_track_to_genre_playlists_until_genre_limit()
            self._update_file_tags_if_file_exists()

    @receiver(pre_delete, sender='bodzify_api.LibraryTrack')
    def delete_file_if_exists(sender, instance: 'LibraryTrack', using, **kwargs):
        if instance.file_exists:
            instance.file.delete()

    def _update_genre_playlists(self, old_genre: Optional[Criteria]):
        if old_genre is not None and self.genre is not None:
            common_genre = self.genre.get_common_criteria(old_genre)
        else:
            common_genre = None

        self._add_track_to_genre_playlists_until_genre_limit(
            genre_limit=common_genre)
        self._remove_track_from_old_genre_ascendants_playlists_until_genre_limit(
            old_genre=old_genre,
            genre_limit=common_genre)

    def _remove_track_from_old_genre_ascendants_playlists_until_genre_limit(self,
                                                                            old_genre: Optional[Criteria],
                                                                            genre_limit=None):
        if old_genre is not None:
            old_genre_tree_item = old_genre
            while old_genre_tree_item != genre_limit:
                self.playlists.remove(CriteriaPlaylist.objects.get(
                    criteria=old_genre_tree_item).playlist)
                old_genre_tree_item = old_genre_tree_item.parent
        else:
            criteria_playlist = CriteriaPlaylist.objects.get(
                playlist__user=self.user, type_id=CRITERIA_TYPES_ID.GENRE, criteria=None)
            self.playlists.remove(criteria_playlist.playlist)

    def _add_track_to_genre_playlists_until_genre_limit(self, genre_limit=None):
        if self.genre is not None:
            new_genre_tree_item = self.genre
            while new_genre_tree_item != genre_limit:
                self.playlists.add(CriteriaPlaylist.objects.get(
                    criteria=new_genre_tree_item).playlist)
                new_genre_tree_item = new_genre_tree_item.parent
        else:
            genreless_criteria_playlist = CriteriaPlaylist.objects.get(
                playlist__user=self.user, type_id=CRITERIA_TYPES_ID.GENRE, criteria=None)
            self.playlists.add(genreless_criteria_playlist.playlist)

    def delete_with_checking_album_and_artist_potential_deletion(self):
        track_artist_uuid = self.artist.uuid if self.artist else None
        track_album_uuid = self.album.uuid if self.album else None
        self.delete()
        self._delete_eventual_related_album(track_album_uuid)
        self._delete_eventual_related_artist(track_artist_uuid)

    def delete_with_checking_artist_potential_deletion(self):
        track_artist_id = self.artist.id if self.artist else None
        self.delete()
        self._delete_eventual_related_artist(track_artist_id)

    def delete_with_checking_album_potential_deletion(self):
        track_album_id = self.album.id if self.album else None
        self.delete()
        self._delete_eventual_related_album(track_album_id)

    def _delete_eventual_related_artist(self, track_artist_uuid):
        if track_artist_uuid:
            from bodzify_api.model.Artist import Artist
            Artist.objects.get(
                uuid=track_artist_uuid).delete_if_nothing_linked()

    def _delete_eventual_related_album(self, track_album_uuid):
        if track_album_uuid:
            from bodzify_api.model.Album import Album
            Album.objects.get(
                uuid=track_album_uuid).delete_if_no_track_linked()

    def _update_file_tags_if_file_exists(self):
        if self.file_exists == False:
            return

        metadata_update_dict = dict()

        titleTag = self.title
        if titleTag is None:
            titleTag = ""
        metadata_update_dict[AudioMetadataManager.METADATA_DICT_KEYS.TITLE] = titleTag

        if self.artist_id is not None:
            artist_name_tag = self.artist.name
        else:
            artist_name_tag = ""
        metadata_update_dict[AudioMetadataManager.METADATA_DICT_KEYS.ARTIST_NAME] = artist_name_tag

        album_artists_tag = ""
        if self.album_id is not None:
            album_name_tag = self.album.name
            album_artists_name_index = 0
            for albumArtist in list(self.album.album_artists.all()):
                if album_artists_name_index != 0:
                    album_artists_tag = (
                        album_artists_tag + AudioMetadataManager.TAG_ARTISTS_SEPARATION_CHAR)
                album_artists_tag = album_artists_tag + albumArtist.name
                album_artists_name_index = album_artists_name_index + 1
        else:
            album_name_tag = ""

        if album_name_tag is None:
            album_name_tag = ""
        metadata_update_dict[AudioMetadataManager.METADATA_DICT_KEYS.ALBUM_NAME] = album_name_tag
        album_artists_name_key = AudioMetadataManager.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES
        metadata_update_dict[album_artists_name_key] = album_artists_tag

        if self.genre == None:
            genre_name_tag = ""
        else:
            genre_name_tag = self.genre.name
        metadata_update_dict[AudioMetadataManager.METADATA_DICT_KEYS.GENRE_NAME] = genre_name_tag

        metadata_update_dict[AudioMetadataManager.METADATA_DICT_KEYS.RATING] = self.rating

        language_tag = self.language
        if language_tag is None:
            language_tag = ""
        metadata_update_dict[AudioMetadataManager.METADATA_DICT_KEYS.LANGUAGE] = language_tag

        AudioMetadataManager.update(
            file=self.file,
            metadata_update_dict=metadata_update_dict,
            normalized_rating_max_value=settings.LIB_TRACK_RATING_VALUE_MAX)
