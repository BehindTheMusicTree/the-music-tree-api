import datetime
import os
from typing import TYPE_CHECKING

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db import models
from django.db.models.fields.files import FieldFile
from django.db.models import F
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from api import settings
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.exception.validation.app.AppValidationException import AppValidationException
from api.model.field.foreign_key.AppForeignKey import AppForeignKey
from api.model.field.foreign_key.AppOneToOneField import AppOneToOneField
from api.model.field.foreign_key.PrivateOneToOneField import PrivateOneToOneField
from api.model.musicbrainz_resource.children.recording.MbRecording import MusicbrainzRecording
from api.model.musicbrainz_resource.children.recording.missing_cause.MbRecordingMissingCause import (
    MbRecordingMissingCause
)
from api.model.musicbrainz_resource.children.recording.missing_cause.code.MbRecordingMissingCauseCode import (
    MbRecordingMissingCauseCode
)
from api.model.private_standard_resource.PrivateStandardResource import PrivateStandardResource
from api.model.uploaded_track.Fields import Fields as UploadedTrackFields
from api.model.utils import utils as model_utils
from api.model.utils.PreserveSpacesStorage import PreserveSpacesStorage
from api.utils import audio_file_metadata
from api.utils.audio_file_metadata.types import AppMetadata
from api.utils.audio_file_metadata.exceptions import FileCorruptedError
from api.validator.TrackFileValidator import TrackFileValidator

from .Fields import Fields


class TrackFile(PrivateStandardResource):
    uploaded_track = PrivateOneToOneField(  # type: ignore
        'UploadedTrack', on_delete=models.CASCADE, related_name=UploadedTrackFields.TRACK_FILE_INTERNAL)
    file: TemporaryUploadedFile | FieldFile = models.FileField(  # type: ignore
        upload_to=model_utils.get_user_lib_path,
        storage=PreserveSpacesStorage(),
        help_text="Only audio formats accepted.",
        validators=[TrackFileValidator(),],
        max_length=settings.FILE_PATH_MAX_LENGTH)
    duration_in_sec = models.PositiveIntegerField()
    md5_has_been_corrected = models.BooleanField(default=False)
    size_in_bytes = models.DecimalField(max_digits=11, decimal_places=2)
    size_in_ko = models.GeneratedField(expression=F(Fields.SIZE_IN_BYTES) / 1024,  # type: ignore
                                       output_field=models.DecimalField(max_digits=8, decimal_places=2),
                                       db_persist=True)
    size_in_mo = models.GeneratedField(expression=F(Fields.SIZE_IN_BYTES) / (1024 * 1024),  # type: ignore
                                       output_field=models.DecimalField(max_digits=5, decimal_places=2),
                                       db_persist=True)
    bitrate_in_kbps = models.IntegerField()
    musicbrainz_recording = AppForeignKey(MusicbrainzRecording, on_delete=models.DO_NOTHING, default=None, null=True)
    musicbrainz_recording_missing_cause = AppOneToOneField(
        MbRecordingMissingCause, on_delete=models.DO_NOTHING, null=True)

    if TYPE_CHECKING:
        from ..UploadedTrack import UploadedTrack
        uploaded_track: UploadedTrack

    class Meta:
        verbose_name = 'Track File'
        verbose_name_plural = 'Track Files'

    @property
    def filename(self) -> str:
        return os.path.basename(self.file.name)

    @property
    def extension(self) -> str:
        return os.path.splitext(self.filename)[1]

    @property
    def duration_str_in_hour_min_sec(self) -> str | None:
        return str(datetime.timedelta(seconds=self.duration_in_sec)) if self.duration_in_sec else None

    def __str__(self):
        if self.file and self.file.name:
            return self.file.name + " (" + str(self.size_in_bytes) + " bytes)"
        return ""

    def _manage_musicbrainz_recording(self) -> None:
        self.musicbrainz_recording_missing_cause = MbRecordingMissingCause.objects.create(
            user=self.user,
            code=MbRecordingMissingCauseCode.Codes.AUDIO_META_AMALYSIS_DISABLED)

    def _prepare_save(self, ctx) -> dict:
        if self.extension.lower() == '.flac':
            if audio_file_metadata.is_flac_md5_valid(self.file):
                self.md5_has_been_corrected = False
            else:
                try:
                    # Fix MD5 and preserve file path
                    self.file = audio_file_metadata.fix_md5_checking(self.file)
                    self.md5_has_been_corrected = True
                except FileCorruptedError as e:
                    raise AppValidationException(
                        field_name=Fields.FILE,
                        message='The FLAC file appears to be corrupted and cannot be processed.',
                        field_validation_error_code=FieldValidationErrorCode.TRACK_FILE_CORRUPTED)
        try:
            duration = audio_file_metadata.get_duration_in_sec(self.file)
            self.duration_in_sec = duration if duration > 1 else 1
            self.bitrate_in_kbps = audio_file_metadata.get_bitrate(self.file)
            self.size_in_bytes = self.file.size
            self._manage_musicbrainz_recording()
            return ctx.kwargs
        except FileCorruptedError as e:
            raise AppValidationException(field_name=Fields.FILE,
                                         message="File corrupted",
                                         field_validation_error_code=FieldValidationErrorCode.TRACK_FILE_CORRUPTED)
        except Exception:
            raise

    def update_file_metadata(self, app_metadata: AppMetadata):
        audio_file_metadata.update_file_metadata(file=self.file,
                                                 app_metadata=app_metadata,
                                                 normalized_rating_max_value=settings.UPLOADED_TRACK_RATING_VALUE_MAX)

    def handle_flac_md5(self) -> bool:
        return False


@receiver(pre_save, sender=TrackFile)
def handle_pre_save(sender, instance: TrackFile, **kwargs):
    if not os.path.exists(instance.user.lib_abs_path):
        os.makedirs(instance.user.lib_abs_path)


@receiver(pre_delete, sender=TrackFile)
def handle_pre_delete(sender, instance: TrackFile, using, **kwargs):
    instance.file.delete(False)  # type: ignore
