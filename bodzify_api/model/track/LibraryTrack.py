#!/usr/bin/env python

from typing import Optional

import shortuuid
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

import bodzify_api.audiometadata as audiometadata
from bodzify_api.model.Album import ATTRIBUTES_LABEL as ALBUM_ATTRIBUTES_LABEL
from bodzify_api.model.File import File
from bodzify_api.model.playlist.Playlist import Playlist
import bodzify_api.settings as settings
from bodzify_api.model.Artist import ATTRIBUTES_LABEL as ARTIST_ATTRIBUTES_LABEL
from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist


class ATTRIBUTES_LABEL:
    MODEL = 'library_track'
    UUID = "uuid"
    USER = "user"
    FILE_OBJ = "file_obj"
    FILE_OBJ_USER_FRIENDLY = "file"
    ACOUSTIC_FINGERPRINT = "acoustic_fingerprint"
    DURATION = "duration"
    MUSICBRAINZ_RECORDING_ID = "musicbrainz_recording_id"
    TITLE = "title"
    ARTIST = "artist"
    ALBUM = "album"
    GENRE = "genre"
    RATING = "rating"
    PLAYLISTS = "playlists"
    LANGUAGE = "language"
    ADDED_ON = "added_on"
    RELATIVE_URL = "relative_url"
    PLAY_COUNT = 'play_count'


class LibraryTrack(models.Model):
    # Django's UUIDField won't validate a shortuuid
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=settings.UUID_LEN, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=settings.LIB_TRACK_TITLE_LEN_MAX)
    file_obj = models.OneToOneField(File, on_delete=models.CASCADE)
    acoustic_fingerprint = models.BinaryField(editable=True)  # default non editable
    duration = models.FloatField(default=None, null=True)
    musicbrainz_recording_id = models.UUIDField(default=None, null=True)
    artist = models.ForeignKey('bodzify_api.Artist',
                               on_delete=models.CASCADE,
                               default=None,
                               null=True,
                               related_name=ARTIST_ATTRIBUTES_LABEL.LIB_TRACKS)
    album = models.ForeignKey('bodzify_api.Album',
                              on_delete=models.CASCADE,
                              default=None,
                              null=True,
                              related_name=ALBUM_ATTRIBUTES_LABEL.LIB_TRACKS)
    genre = models.ForeignKey('bodzify_api.Criteria',
                              on_delete=models.DO_NOTHING,
                              default=None,
                              null=True,
                              related_name=CRITERIA_ATTRIBUTES_LABEL.LIB_TRACKS)
    rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(settings.LIB_TRACK_RATING_VALUE_MAX)])
    language = models.CharField(max_length=settings.LIB_TRACK_LANGUAGE_LEN_MAX, blank=True, default=None, null=True)
    added_on = models.DateTimeField(auto_now_add=True, editable=False)
    play_count = models.IntegerField(default=0)
    playlists = models.ManyToManyField(Playlist,
                                       through='PlaylistLibTrackRelation',
                                       related_name=ATTRIBUTES_LABEL.MODEL + 's')

    @property
    def relative_url(self) -> str:
        return "tracks/" + self.uuid + "/"

    def __str__(self):
        album_str = f"{ATTRIBUTES_LABEL.ALBUM}: {str(self.album)} " if self.album else ""
        genre_str = f"{ATTRIBUTES_LABEL.GENRE}: {str(self.genre)} " if self.genre else ""
        duration_str = f"{ATTRIBUTES_LABEL.DURATION}: {str(self.duration)} " if self.duration else ""
        rating_str = f"{ATTRIBUTES_LABEL.RATING}: {str(self.rating)} " if self.rating else ""
        language_str = f"{ATTRIBUTES_LABEL.LANGUAGE}: {str(self.language)} " if self.language else ""
        file_str = f"{ATTRIBUTES_LABEL.FILE_OBJ}: {str(self.file_obj)} " if self.file_obj else ""
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
            from bodzify_api.model.playlist.Playlist import SPECIAL_NAMES as PLAYLIST_SPECIAL_NAMES
            from bodzify_api.model.PlaylistLibTrackRelation import PlaylistLibTrackRelation
            all_simple_playlist = SimplePlaylist.objects.get(playlist__user=self.user, name=PLAYLIST_SPECIAL_NAMES.ALL)
            PlaylistLibTrackRelation.objects.create(playlist=all_simple_playlist.playlist, library_track=self)
            self._add_track_to_genre_playlists_until_genre_limit()
            self._update_file_tags_if_file_exists()

            if self.file_obj:
                self.duration = audiometadata.get_specific_metadata_from_file(
                    file=self.file_obj.file, normalized_metadata_key=audiometadata.NormalizedMetadataKeys.DURATION)
                super().save(update_fields=[ATTRIBUTES_LABEL.DURATION])

            super().save(update_fields=[ATTRIBUTES_LABEL.ACOUSTIC_FINGERPRINT])

    def _update_genre_playlists(self, old_genre: Optional[Criteria]):
        if old_genre is not None and self.genre is not None:
            common_genre = self.genre.get_common_criteria(old_genre)
        else:
            common_genre = None

        self._add_track_to_genre_playlists_until_genre_limit(genre_limit=common_genre)
        self._remove_track_from_old_genre_ascendants_playlists_until_genre_limit(old_genre=old_genre,
                                                                                 genre_limit=common_genre)

    def _remove_track_from_old_genre_ascendants_playlists_until_genre_limit(self,
                                                                            old_genre: Optional[Criteria],
                                                                            genre_limit=None):
        from bodzify_api.model.PlaylistLibTrackRelation import PlaylistLibTrackRelation

        update_date = timezone.now()
        if old_genre is not None:
            old_genre_tree_item = old_genre
            while old_genre_tree_item != genre_limit:
                genreless_criteria_playlist = CriteriaPlaylist.objects.get(criteria=old_genre_tree_item)
                base_playlist = genreless_criteria_playlist.playlist
                PlaylistLibTrackRelation.objects.get(playlist=base_playlist, library_track=self).delete()
                base_playlist.last_track_list_update_date = update_date
                base_playlist.save()
                old_genre_tree_item = old_genre_tree_item.parent  # type: ignore
        else:
            genreless_criteria_playlist = CriteriaPlaylist.objects.get(playlist__user=self.user,
                                                                       type_id=CRITERIA_TYPES_ID.GENRE,
                                                                       criteria=None)
            base_playlist = genreless_criteria_playlist.playlist
            base_playlist.last_track_list_update_date = update_date
            base_playlist.save()
            PlaylistLibTrackRelation.objects.get(playlist=base_playlist, library_track=self).delete()

    def _add_track_to_genre_playlists_until_genre_limit(self, genre_limit=None):
        from bodzify_api.model.PlaylistLibTrackRelation import PlaylistLibTrackRelation

        update_date = timezone.now()
        if self.genre is not None:
            new_genre_tree_item = self.genre
            while new_genre_tree_item != genre_limit:
                criteria_playlist = CriteriaPlaylist.objects.get(criteria=new_genre_tree_item)
                playlist = criteria_playlist.playlist
                PlaylistLibTrackRelation.objects.create(playlist=criteria_playlist.playlist, library_track=self)
                playlist.last_track_list_update_date = update_date
                playlist.save()
                new_genre_tree_item = new_genre_tree_item.parent
        else:
            genreless_criteria_playlist = CriteriaPlaylist.objects.get(playlist__user=self.user,
                                                                       type_id=CRITERIA_TYPES_ID.GENRE,
                                                                       criteria=None)
            genreless_parent_playlist = genreless_criteria_playlist.playlist
            PlaylistLibTrackRelation.objects.create(playlist=genreless_parent_playlist, library_track=self)
            genreless_parent_playlist.last_track_list_update_date = update_date
            genreless_parent_playlist.save()

    def _get_lib_track_playlists_with_positions(self) -> list:
        from bodzify_api.model.PlaylistLibTrackRelation \
            import PlaylistLibTrackRelation, ATTRIBUTES_LABEL as playlist_lib_track_relation_ATTRIBUTES_LABEL
        playlist_lib_track_relation_relations = PlaylistLibTrackRelation.objects.filter(library_track=self)
        return list(playlist_lib_track_relation_relations.values_list(
            playlist_lib_track_relation_ATTRIBUTES_LABEL.PLAYLIST + '__uuid',
            playlist_lib_track_relation_ATTRIBUTES_LABEL.POSITION))

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
        if self.file_obj is None:
            return

        normalized_metadata = dict()

        title_tag = self.title
        if title_tag is None:
            title_tag = ""
        normalized_metadata[audiometadata.NormalizedMetadataKeys.TITLE] = title_tag

        if self.artist_id is not None:  # type: ignore
            artist_name_tag = self.artist.name  # type: ignore
        else:
            artist_name_tag = ""
        normalized_metadata[audiometadata.NormalizedMetadataKeys.ARTIST_NAME] = artist_name_tag

        album_artists_tag = ""
        if self.album_id is not None:  # type: ignore
            album_name_tag = self.album.name  # type: ignore
            album_artists_name_index = 0
            for albumArtist in list(self.album.album_artists.all()):  # type: ignore
                if album_artists_name_index != 0:
                    album_artists_tag = (
                        album_artists_tag + audiometadata.METADATA_ARTISTS_SEPARATION_CHAR)
                album_artists_tag = album_artists_tag + albumArtist.name
                album_artists_name_index = album_artists_name_index + 1
        else:
            album_name_tag = ""

        if album_name_tag is None:
            album_name_tag = ""
        normalized_metadata[audiometadata.NormalizedMetadataKeys.ALBUM_NAME] = album_name_tag
        album_artists_name_key = audiometadata.NormalizedMetadataKeys.ALBUM_ARTISTS_NAMES
        normalized_metadata[album_artists_name_key] = album_artists_tag

        if self.genre == None:
            genre_name_tag = ""
        else:
            genre_name_tag = self.genre.name
        normalized_metadata[audiometadata.NormalizedMetadataKeys.GENRE_NAME] = genre_name_tag

        normalized_metadata[audiometadata.NormalizedMetadataKeys.RATING] = self.rating

        language_tag = self.language
        if language_tag is None:
            language_tag = ""
        normalized_metadata[audiometadata.NormalizedMetadataKeys.LANGUAGE] = language_tag

        audiometadata.update_file_metadata(
            file=self.file_obj.file,
            normalized_metadata=normalized_metadata,
            normalized_rating_max_value=settings.LIB_TRACK_RATING_VALUE_MAX)


@ receiver(pre_delete, sender=LibraryTrack)
def handle_pre_delete(sender, instance: 'LibraryTrack', using, **kwargs):
    if instance.file_obj:
        instance.file_obj.file.delete(False)

    now = timezone.now()
    for playlist in instance.playlists.all():
        playlist.last_track_list_update_date = now
        playlist.save()
