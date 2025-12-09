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
from api.utils import audio_file_metadata
from api.utils.audio_file_metadata.AppMetadataKey import AppMetadataKey
from api.utils.audio_file_metadata.types import AppMetadata
from api.utils.audio_file_metadata.exceptions import FileCorruptedError
from api.validator.TrackFileValidator import TrackFileValidator

from .Fields import Fields
from .file.Fields import Fields as TrackFileFields
from .UploadedTrackManager import UploadedTrackManager


if TYPE_CHECKING:
    from api.model.uploaded_track_playlist_rel.UploadedTrackPlaylistRel import UploadedTrackPlaylistRel


class UploadedTrack(TrackablePlayCount):
    title = AppCharField(max_length=settings.UPLOADED_TRACK_TITLE_LEN_MAX)
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
    
    file: TemporaryUploadedFile | FieldFile = models.FileField(  # type: ignore
        upload_to=model_utils.get_user_lib_path,
        storage=PreserveSpacesStorage(),
        help_text="Only audio formats accepted.",
        validators=[TrackFileValidator(),],
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
            if self.extension.lower() == '.flac':
                if audio_file_metadata.is_flac_md5_valid(self.file):
                    self.md5_has_been_corrected = False
                else:
                    try:
                        self.file = audio_file_metadata.fix_md5_checking(self.file)
                        self.md5_has_been_corrected = True
                    except FileCorruptedError as e:
                        raise AppValidationException(
                            field_name=TrackFileFields.FILE,
                            message='The FLAC file appears to be corrupted and cannot be processed.',
                            field_validation_error_code=FieldValidationErrorCode.TRACK_FILE_CORRUPTED)
            try:
                duration = audio_file_metadata.get_duration_in_sec(self.file)
                self.duration_in_sec = duration if duration > 1 else 1
                self.bitrate_in_kbps = audio_file_metadata.get_bitrate(self.file)
                self.size_in_bytes = self.file.size
                self._manage_musicbrainz_recording()
            except FileCorruptedError as e:
                raise AppValidationException(field_name=TrackFileFields.FILE,
                                             message="File corrupted",
                                             field_validation_error_code=FieldValidationErrorCode.TRACK_FILE_CORRUPTED)
            except Exception:
                raise
        return ctx.kwargs

    def update_file_metadata(self, app_metadata: AppMetadata):
        if self.file:
            audio_file_metadata.update_file_metadata(file=self.file,
                                                     app_metadata=app_metadata,
                                                     normalized_rating_max_value=settings.UPLOADED_TRACK_RATING_VALUE_MAX)

    def update_file_metadata_from_uploaded_track_instance_values(self):
        normalized_metadata = dict()
        normalized_metadata[AppMetadataKey.TITLE] = self.title

        if self.artists.exists():
            artists_names_tag = [artist.name for artist in self.artists.all()]
        else:
            artists_names_tag = None
        normalized_metadata[AppMetadataKey.ARTISTS_NAMES] = artists_names_tag

        if self.album:
            album_name_tag = self.album.name
            album_artists_list = self.album.album_artists.all()
            album_artists_tag = [
                album_artist.name for album_artist in album_artists_list] if album_artists_list.exists() else None
        else:
            album_name_tag = None
            album_artists_tag = None

        normalized_metadata[AppMetadataKey.ALBUM_NAME] = album_name_tag
        normalized_metadata[AppMetadataKey.ALBUM_ARTISTS_NAMES] = album_artists_tag
        normalized_metadata[AppMetadataKey.GENRE_NAME] = self.genre.name if self.genre else None
        normalized_metadata[AppMetadataKey.RATING] = self.rating
        normalized_metadata[AppMetadataKey.LANGUAGE] = self.language if self.language else None

        self.update_file_metadata(app_metadata=normalized_metadata)

    @property
    def playlists_with_positions(self) -> list[tuple[str, int]]:
        from api.model.uploaded_track_playlist_rel.UploadedTrackPlaylistRel import Fields as UploadedTrackPlaylistRelFields
        from api.model.uploaded_track_playlist_rel.UploadedTrackPlaylistRel import UploadedTrackPlaylistRel
        uploaded_track_playlist_rels = UploadedTrackPlaylistRel.objects.filter(user=self.user, uploaded_track=self)
        return list(uploaded_track_playlist_rels.values_list(UploadedTrackPlaylistRelFields.PLAYLIST + '__uuid',
                                                             UploadedTrackPlaylistRelFields.POSITION))


@receiver(pre_save, sender=UploadedTrack)
def handle_pre_save(sender, instance: UploadedTrack, **kwargs):
    if instance.file and not os.path.exists(instance.user.lib_abs_path):
        os.makedirs(instance.user.lib_abs_path)


@receiver(pre_delete, sender=UploadedTrack)
def handle_pre_delete(sender, instance: UploadedTrack, using, **kwargs):
    if instance.file:
        instance.file.delete(False)  # type: ignore
