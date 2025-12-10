import datetime
from typing import TYPE_CHECKING

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import QuerySet

from api import settings
from api.model.album.Album import Album
from api.model.album.Fields import Fields as AlbumFields
from api.model.artist.Artist import Artist
from api.model.artist.Fields import Fields as ArtistFields
from api.model.criteria.children.genre.Genre import Genre
from api.model.criteria.Fields import Fields as CriteriaFields
from api.model.field.AppCharField import AppCharField
from api.model.field.foreign_key.PrivateForeignKey import PrivateForeignKey
from api.model.field.foreign_key.PrivateManyToManyField import PrivateManyToManyField
from api.model.playlist.Fields import Fields as PlayListFields
from api.model.playlist.Playlist import Playlist
from api.model.trackable_play_count.TrackablePlayCount import TrackablePlayCount

from .Fields import Fields
from .TrackManager import TrackManager


if TYPE_CHECKING:
    from api.model.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel


class Track(TrackablePlayCount):
    title = AppCharField(max_length=settings.TRACK_TITLE_LEN_MAX)
    artists = PrivateManyToManyField(Artist, blank=True, related_name=ArtistFields.TRACKS_RELATED_NAME)
    album: Album = PrivateForeignKey(Album,  # type: ignore
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True,
                                     related_name=AlbumFields.TRACKS_RELATED_NAME,)
    track_number = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(settings.TRACK_TRACK_NUMBER_MAX)])
    genre = PrivateForeignKey(Genre,
                              on_delete=models.DO_NOTHING,
                              null=True,
                              blank=True,
                              related_name=CriteriaFields.TRACKS_RELATED_NAME)
    rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(settings.TRACK_RATING_VALUE_MAX)])
    language = AppCharField(max_length=settings.LANGUAGE_LEN_MAX, blank=True, default=None, null=True)
    archived = models.BooleanField(default=False)
    playlists = PrivateManyToManyField(
        Playlist, through='TrackPlaylistRel', related_name=PlayListFields.TRACKS_RELATED_NAME)

    duration_in_sec = models.PositiveIntegerField(null=True, blank=True)

    if TYPE_CHECKING:
        track_playlist_rels: models.QuerySet['TrackPlaylistRel']

    objects: TrackManager = TrackManager()

    class Meta:
        verbose_name = 'Track'
        verbose_name_plural = 'Tracks'
        indexes = [models.Index(fields=[Fields.USER, Fields.TITLE]),
                   models.Index(fields=[Fields.USER, Fields.GENRE]),
                   models.Index(fields=[Fields.USER, Fields.ALBUM]),]

    @property
    def relative_url(self) -> str:
        return f"library/track/{self.uuid}/"

    @property
    def duration_str_in_hour_min_sec(self) -> str | None:
        return str(datetime.timedelta(seconds=self.duration_in_sec)) if self.duration_in_sec else None

    def __str__(self):
        position_str = f"#{self.track_number}" if self.track_number else "#--"

        artists: QuerySet[Artist] = self.artists.all()
        artists_str = ", ".join(
            artist.name for artist in artists) if self.artists.exists() else f"[no {Fields.ARTISTS}]"
        album_str = str(self.album) if self.album else f"[no {Fields.ALBUM}]"

        genre_str = f"{Fields.GENRE}: {self.genre}" if self.genre else f"{Fields.GENRE}: --"
        rating_str = f"{Fields.RATING}: {self.rating}" if self.rating else f"{Fields.RATING}: --"
        language_str = f"{Fields.LANGUAGE}: {self.language}" if self.language else f"{Fields.LANGUAGE}: --"

        return (f"{self.uuid} | {position_str} | '{self.title}' by {artists_str} | {album_str} | "
                f"{genre_str} | {rating_str} | {language_str} | "
                + f"{Fields.CREATED_ON}: {self.created_on}")

    def simple_str(self) -> str:
        artists: QuerySet[Artist] = self.artists.all()
        artists_str = ", ".join(
            artist.name for artist in artists) if self.artists.exists() else f"no {Fields.ARTISTS}"
        return f"{self.uuid} | '{self.title}' by {artists_str}"

    @property
    def playlists_with_positions(self) -> list[tuple[str, int]]:
        from api.model.track_playlist_rel.TrackPlaylistRel import Fields as TrackPlaylistRelFields
        from api.model.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel
        track_playlist_rels = TrackPlaylistRel.objects.filter(user=self.user, track=self)
        return list(track_playlist_rels.values_list(TrackPlaylistRelFields.PLAYLIST + '__uuid',
                                                    TrackPlaylistRelFields.POSITION))
