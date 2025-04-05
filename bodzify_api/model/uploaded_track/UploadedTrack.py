from typing import TYPE_CHECKING

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import QuerySet

from bodzify_api import settings
from bodzify_api.model.album.Album import Album
from bodzify_api.model.album.Fields import Fields as AlbumFields
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.artist.Fields import Fields as ArtistFields
from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.model.criteria.Fields import Fields as CriteriaFields
from bodzify_api.model.field.AppCharField import AppCharField
from bodzify_api.model.field.foreign_key.PrivateForeignKey import PrivateForeignKey
from bodzify_api.model.field.foreign_key.PrivateManyToManyField import PrivateManyToManyField
from bodzify_api.model.playlist.Fields import Fields as PlayListFields
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.trackable_play_count.TrackablePlayCount import TrackablePlayCount
from bodzify_api.utils.audio_metadata.manager.MetadataManager import METADATA_ARTISTS_SEPARATORS
from bodzify_api.utils.audio_metadata.utils.AppMetadataKey import AppMetadataKey

from .file.TrackFile import TrackFile
from .Fields import Fields
from .UploadedTrackManager import UploadedTrackManager


if TYPE_CHECKING:
    from bodzify_api.model.uploaded_track_playlist_rel.UploadedTrackPlaylistRel import UploadedTrackPlaylistRel


class UploadedTrack(TrackablePlayCount):
    title = AppCharField(max_length=settings.UPLOADED_TRACK_TITLE_LEN_MAX)
    track_file_fingerprint_must_be_unique = models.BooleanField(default=False)
    artists = PrivateManyToManyField(Artist, blank=True, related_name=ArtistFields.UPLOADED_TRACKS_RELATED_NAME)
    album: Album = PrivateForeignKey(Album,  # type: ignore
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True,
                                     related_name=AlbumFields.UPLOADED_TRACKS_RELATED_NAME,)
    track_number = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(settings.UPLOADED_TRACK_TRACK_NUMBER_MAX)])
    genre = PrivateForeignKey(Genre,
                              on_delete=models.DO_NOTHING,
                              null=True,
                              blank=True,
                              related_name=CriteriaFields.UPLOADED_TRACKS_RELATED_NAME)
    rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(settings.UPLOADED_TRACK_RATING_VALUE_MAX)])
    language = AppCharField(max_length=settings.LANGUAGE_LEN_MAX, blank=True, default=None, null=True)
    archived = models.BooleanField(default=False)
    playlists = PrivateManyToManyField(
        Playlist, through='UploadedTrackPlaylistRel', related_name=PlayListFields.UPLOADED_TRACKS_RELATED_NAME)

    if TYPE_CHECKING:
        track_file: TrackFile
        uploaded_track_playlist_rels: models.QuerySet['UploadedTrackPlaylistRel']

    objects: UploadedTrackManager = UploadedTrackManager()

    class Meta:
        verbose_name = 'Uploaded Track'
        verbose_name_plural = 'Uploaded Tracks'
        indexes = [models.Index(fields=[Fields.USER, Fields.TITLE]),
                   models.Index(fields=[Fields.USER, Fields.GENRE]),
                   models.Index(fields=[Fields.USER, Fields.ALBUM]),]

    @property
    def relative_url(self) -> str:
        return f"library/uploaded/{self.uuid}/"

    def __str__(self):
        position_str = f"#{self.track_number}" if self.track_number else "#--"

        artists: QuerySet[Artist] = self.artists.all()
        artists_str = ", ".join(
            artist.name for artist in artists) if self.artists.exists() else f"[no {Fields.ARTISTS}]"
        album_str = str(self.album) if self.album else f"[no {Fields.ALBUM}]"

        genre_str = f"{Fields.GENRE}: {self.genre}" if self.genre else f"{Fields.GENRE}: --"
        rating_str = f"{Fields.RATING}: {self.rating}" if self.rating else f"{Fields.RATING}: --"
        language_str = f"{Fields.LANGUAGE}: {self.language}" if self.language else f"{Fields.LANGUAGE}: --"
        file_str = f"{Fields.TRACK_FILE_INTERNAL}: {self.track_file}" if self.track_file else "no track file"

        return (f"{self.uuid} | {position_str} | '{self.title}' by {artists_str} | {album_str} | "
                f"{genre_str} | {rating_str} | {language_str} | "
                + f"{Fields.CREATED_ON}: {self.created_on} | {file_str}")

    def simple_str(self) -> str:
        artists: QuerySet[Artist] = self.artists.all()
        artists_str = ", ".join(
            artist.name for artist in artists) if self.artists.exists() else f"no {Fields.ARTISTS}"
        return f"{self.uuid} | '{self.title}' by {artists_str}"

    def update_file_metadata_from_uploaded_track_instance_values(self):
        normalized_metadata = dict()
        normalized_metadata[AppMetadataKey.TITLE] = self.title

        if self.artists.count() > 0:
            artists_names_tag = ""
            artists_list: list[Artist] = list(self.artists.all())
            for artist in artists_list:
                if artists_names_tag != "":
                    artists_names_tag = artists_names_tag + METADATA_ARTISTS_SEPARATORS[0]
                artists_names_tag = artists_names_tag + artist.name
        else:
            artists_names_tag = ""
        normalized_metadata[AppMetadataKey.ARTISTS_NAMES] = artists_names_tag

        album_artists_tag = ""
        if self.album:
            album_name_tag = self.album.name
            album_artists_name_index = 0
            album_artists_list = self.album.album_artists.all()
            for album_artist in album_artists_list:
                if album_artists_name_index != 0:
                    album_artists_tag = album_artists_tag + METADATA_ARTISTS_SEPARATORS[0]
                album_artists_tag = album_artists_tag + album_artist.name
                album_artists_name_index = album_artists_name_index + 1
        else:
            album_name_tag = ""

        normalized_metadata[AppMetadataKey.ALBUM_NAME] = album_name_tag
        normalized_metadata[AppMetadataKey.ALBUM_ARTISTS_NAMES] = album_artists_tag
        normalized_metadata[AppMetadataKey.GENRE_NAME] = self.genre.name if self.genre else ""
        normalized_metadata[AppMetadataKey.RATING] = self.rating
        normalized_metadata[AppMetadataKey.LANGUAGE] = self.language if self.language else ""

        self.track_file.update_file_metadata(app_metadata=normalized_metadata)

    @property
    def playlists_with_positions(self) -> list[tuple[str, int]]:
        from bodzify_api.model.uploaded_track_playlist_rel.UploadedTrackPlaylistRel import Fields as UploadedTrackPlaylistRelFields
        from bodzify_api.model.uploaded_track_playlist_rel.UploadedTrackPlaylistRel import UploadedTrackPlaylistRel
        uploaded_track_playlist_rels = UploadedTrackPlaylistRel.objects.filter(user=self.user, uploaded_track=self)
        return list(uploaded_track_playlist_rels.values_list(UploadedTrackPlaylistRelFields.PLAYLIST + '__uuid',
                                                             UploadedTrackPlaylistRelFields.POSITION))
