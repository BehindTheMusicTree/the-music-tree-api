import datetime
import os
from typing import TYPE_CHECKING

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import QuerySet
from django.db.models.fields.files import FieldFile
from django.db.models import F
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from api import settings
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.exception.validation.app.AppValidationException import AppValidationException
from api.model.album.Album import Album
from api.model.album.Fields import Fields as AlbumFields
from api.model.artist.Artist import Artist
from api.model.artist.Fields import Fields as ArtistFields
from api.model.criteria.children.genre.Genre import Genre
from api.model.criteria.Fields import Fields as CriteriaFields
from api.model.field.AppCharField import AppCharField
from api.model.field.foreign_key.AppForeignKey import AppForeignKey
from api.model.field.foreign_key.AppOneToOneField import AppOneToOneField
from api.model.field.foreign_key.PrivateForeignKey import PrivateForeignKey
from api.model.field.foreign_key.PrivateManyToManyField import PrivateManyToManyField
from api.model.musicbrainz_resource.children.recording.MbRecording import MusicbrainzRecording
from api.model.musicbrainz_resource.children.recording.missing_cause.MbRecordingMissingCause import (
    MbRecordingMissingCause
)
from api.model.musicbrainz_resource.children.recording.missing_cause.code.MbRecordingMissingCauseCode import (
    MbRecordingMissingCauseCode
)
from api.model.playlist.Fields import Fields as PlayListFields
from api.model.playlist.Playlist import Playlist
from api.model.trackable_play_count.TrackablePlayCount import TrackablePlayCount
from api.model.utils import utils as model_utils
from api.model.utils.PreserveSpacesStorage import PreserveSpacesStorage

from .Fields import Fields
from .file.Fields import Fields as TrackFileFields
from .TrackManager import TrackManager


if TYPE_CHECKING:
    from api.model.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel


class Track(TrackablePlayCount):
    title = AppCharField(max_length=settings.UPLOADED_TRACK_TITLE_LEN_MAX)
    artists = PrivateManyToManyField(Artist, blank=True, related_name=ArtistFields.TRACKS_RELATED_NAME)
    album: Album = PrivateForeignKey(Album,  # type: ignore
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True,
                                     related_name=AlbumFields.TRACKS_RELATED_NAME,)
    track_number = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(settings.UPLOADED_TRACK_TRACK_NUMBER_MAX)])
    genre = PrivateForeignKey(Genre,
                              on_delete=models.DO_NOTHING,
                              null=True,
                              blank=True,
                              related_name=CriteriaFields.TRACKS_RELATED_NAME)
    rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(settings.UPLOADED_TRACK_RATING_VALUE_MAX)])
    language = AppCharField(max_length=settings.LANGUAGE_LEN_MAX, blank=True, default=None, null=True)
    archived = models.BooleanField(default=False)
    playlists = PrivateManyToManyField(
        Playlist, through='TrackPlaylistRel', related_name=PlayListFields.TRACKS_RELATED_NAME)

    file: TemporaryUploadedFile | FieldFile = models.FileField(  # type: ignore
        upload_to=model_utils.get_user_lib_path,
        storage=PreserveSpacesStorage(),
        help_text="Only audio formats accepted.",
        max_length=settings.FILE_PATH_MAX_LENGTH,
        null=True,
        blank=True)
    duration_in_sec = models.PositiveIntegerField(null=True, blank=True)
    md5_has_been_corrected = models.BooleanField(default=False)
    size_in_bytes = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    size_in_ko = models.GeneratedField(expression=F(TrackFileFields.SIZE_IN_BYTES) / 1024,  # type: ignore
                                       output_field=models.DecimalField(max_digits=8, decimal_places=2),
                                       db_persist=True,
                                       null=True)
    size_in_mo = models.GeneratedField(expression=F(TrackFileFields.SIZE_IN_BYTES) / (1024 * 1024),  # type: ignore
                                       output_field=models.DecimalField(max_digits=5, decimal_places=2),
                                       db_persist=True,
                                       null=True)
    bitrate_in_kbps = models.IntegerField(null=True, blank=True)
    musicbrainz_recording = AppForeignKey(MusicbrainzRecording, on_delete=models.DO_NOTHING, default=None, null=True)
    musicbrainz_recording_missing_cause = AppOneToOneField(
        MbRecordingMissingCause, on_delete=models.DO_NOTHING, null=True)

    if TYPE_CHECKING:
        track_playlist_rels: models.QuerySet['TrackPlaylistRel']

    objects: TrackManager = TrackManager()

    class Meta:
        verbose_name = 'Uploaded Track'
        verbose_name_plural = 'Uploaded Tracks'
        indexes = [models.Index(fields=[Fields.USER, Fields.TITLE]),
                   models.Index(fields=[Fields.USER, Fields.GENRE]),
                   models.Index(fields=[Fields.USER, Fields.ALBUM]),]

    @property
    def relative_url(self) -> str:
        return f"library/track/{self.uuid}/"

    @property
    def filename(self) -> str:
        return os.path.basename(self.file.name) if self.file and self.file.name else ""

    @property
    def extension(self) -> str:
        return os.path.splitext(self.filename)[1] if self.filename else ""

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
        file_str = f"file: {self.file.name}" if self.file and self.file.name else "no file"

        return (f"{self.uuid} | {position_str} | '{self.title}' by {artists_str} | {album_str} | "
                f"{genre_str} | {rating_str} | {language_str} | "
                + f"{Fields.CREATED_ON}: {self.created_on} | {file_str}")

    def simple_str(self) -> str:
        artists: QuerySet[Artist] = self.artists.all()
        artists_str = ", ".join(
            artist.name for artist in artists) if self.artists.exists() else f"no {Fields.ARTISTS}"
        return f"{self.uuid} | '{self.title}' by {artists_str}"

    def _manage_musicbrainz_recording(self) -> None:
        self.musicbrainz_recording_missing_cause = MbRecordingMissingCause.objects.create(
            user=self.user,
            code=MbRecordingMissingCauseCode.Codes.AUDIO_META_AMALYSIS_DISABLED)

    def _prepare_save(self, ctx) -> dict:
        if self.file:
            self.size_in_bytes = self.file.size
            self._manage_musicbrainz_recording()
        return ctx.kwargs

    @property
    def playlists_with_positions(self) -> list[tuple[str, int]]:
        from api.model.track_playlist_rel.TrackPlaylistRel import Fields as TrackPlaylistRelFields
        from api.model.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel
        track_playlist_rels = TrackPlaylistRel.objects.filter(user=self.user, track=self)
        return list(track_playlist_rels.values_list(TrackPlaylistRelFields.PLAYLIST + '__uuid',
                                                    TrackPlaylistRelFields.POSITION))


@receiver(pre_save, sender=Track)
def handle_pre_save(sender, instance: Track, **kwargs):
    if instance.file and not os.path.exists(instance.user.lib_abs_path):
        os.makedirs(instance.user.lib_abs_path)


@receiver(pre_delete, sender=Track)
def handle_pre_delete(sender, instance: Track, using, **kwargs):
    if instance.file:
        instance.file.delete(False)  # type: ignore
