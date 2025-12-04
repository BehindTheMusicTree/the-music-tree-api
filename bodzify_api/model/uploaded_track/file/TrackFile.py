import binascii
import datetime
import os
from typing import TYPE_CHECKING, cast

import audiometa
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db import models
from django.db.models.fields.files import FieldFile
from django.db.models import F
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext as _

from bodzify_api import settings
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.model.field.foreign_key.AppForeignKey import AppForeignKey
from bodzify_api.model.field.foreign_key.AppOneToOneField import AppOneToOneField
from bodzify_api.model.field.foreign_key.PrivateOneToOneField import PrivateOneToOneField
from bodzify_api.model.musicbrainz_resource.children.recording.MbRecording import MusicbrainzRecording
from bodzify_api.model.musicbrainz_resource.children.recording.MbRecordingLookupResult import (
    MusicbrainzRecordingLookupResult
)
from bodzify_api.model.musicbrainz_resource.children.recording.missing_cause.MbRecordingMissingCause import (
    MbRecordingMissingCause
)
from bodzify_api.model.musicbrainz_resource.children.recording.missing_cause.code.MbRecordingMissingCauseCode import (
    MbRecordingMissingCauseCode
)
from bodzify_api.model.private_standard_resource.PrivateStandardResource import PrivateStandardResource
from bodzify_api.model.uploaded_track.Fields import Fields as UploadedTrackFields
from bodzify_api.model.utils import utils as model_utils
from bodzify_api.model.utils.PreserveSpacesStorage import PreserveSpacesStorage
from bodzify_api.utils import audio_fingerprinter, audio_file_metadata, musicbrainz
from bodzify_api.utils.audio_file_metadata import AppMetadata
from bodzify_api.utils.audio_file_metadata.exceptions import FileCorruptedError
from bodzify_api.validator.TrackFileValidator import TrackFileValidator

from .Fields import Fields
from .fingerprinting.FingerprintingResult import FingerprintingResult
from .fingerprinting.missing_cause.FingerprintMissingCause import FingerprintMissingCause


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
    fingerprint_memory = models.BinaryField(null=True, blank=True, default=None, editable=True)
    fingerprint_missing_cause = AppForeignKey(
        FingerprintMissingCause,  on_delete=models.DO_NOTHING, null=True, blank=True)
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

    @property
    def fingerprint_bytes(self):
        return bytes(self.fingerprint_memory) if self.fingerprint_memory else None

    def __str__(self):
        if self.file and self.file.name:
            return self.file.name + " (" + str(self.size_in_bytes) + " bytes)"
        return ""

    def _manage_fingerprint(self) -> FingerprintingResult | None:
        audio_meta_analysis_enabled_override_env_var = os.environ.get('AUDIO_META_ANALYSIS_ENABLED_OVERRIDE', None)
        if audio_meta_analysis_enabled_override_env_var:
            is_audio_meta_analysis_enabled_override = audio_meta_analysis_enabled_override_env_var.lower()
        else:
            is_audio_meta_analysis_enabled_override = 'false'

        fingerprinting_result: FingerprintingResult | None = None

        if is_audio_meta_analysis_enabled_override == 'true' or settings.AUDIO_META_ANALYSIS_ENABLED:
            fingerprinting_result = audio_fingerprinter.get_fingerprinting_result(
                user=self.user, track_file=self.file, title=self.uploaded_track.title)

            if fingerprinting_result.is_success:
                fingerprint = binascii.hexlify(fingerprinting_result.fingerprint)

                if self.uploaded_track.track_file_fingerprint_must_be_unique:
                    existing_track_file = cast(
                        'TrackFile | None',
                        self.__class__.objects.filter(user=self.user, fingerprint_memory=fingerprint).first())
                    if existing_track_file:
                        raise AppValidationException(
                            field_name='file',
                            message=_(f'The file {self.filename} has the same fingerprint as the track "'
                                      f'{existing_track_file.uploaded_track.simple_str()}"'),
                            field_validation_error_code=FieldValidationErrorCode.TRACK_FILE_FINGERPRINT_DUPLICATE)
                self.fingerprint_memory = fingerprint
            else:
                self.fingerprint_missing_cause = fingerprinting_result.missing_cause
        else:
            self.fingerprint_missing_cause = FingerprintMissingCause.objects.create(
                user=self.user, code=MbRecordingMissingCauseCode.Codes.AUDIO_META_AMALYSIS_DISABLED)

        return fingerprinting_result

    def _manage_musicbrainz_recording(self, fingerprinting_result_nullable: FingerprintingResult | None
                                      ) -> MusicbrainzRecordingLookupResult | None:
        musicbrainz_recording_lookup_result = None

        if self.fingerprint_missing_cause:
            if self.fingerprint_missing_cause.code.code == \
                    MbRecordingMissingCauseCode.Codes.AUDIO_META_AMALYSIS_DISABLED:
                self.musicbrainz_recording_missing_cause = MbRecordingMissingCause.objects.create(
                    user=self.user,
                    code=MbRecordingMissingCauseCode.Codes.AUDIO_META_AMALYSIS_DISABLED)
            else:
                self.musicbrainz_recording_missing_cause = MbRecordingMissingCause.objects.create(
                    user=self.user,
                    code=MbRecordingMissingCauseCode.Codes.TRACK_FILE_FINGERPRINTING_FAILED,
                    message=f"Fingerprinting failed.")
        else:
            fingerprinting_result: FingerprintingResult = fingerprinting_result_nullable  # type: ignore
            musicbrainz_recording_lookup_result = \
                musicbrainz.get_musicbrainz_recording_lookup_result(user=self.user,
                                                                    fingerprint=fingerprinting_result.fingerprint,
                                                                    duration_in_sec=self.duration_in_sec)

            if musicbrainz_recording_lookup_result.is_success:
                self.musicbrainz_recording = musicbrainz_recording_lookup_result.recording
            else:
                self.musicbrainz_recording_missing_cause = musicbrainz_recording_lookup_result.missing_cause

        return musicbrainz_recording_lookup_result

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
            fingerprinting_result = self._manage_fingerprint()
            self._manage_musicbrainz_recording(fingerprinting_result)
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


@receiver(pre_delete, sender=TrackFile)
def handle_pre_delete(sender, instance: TrackFile, using, **kwargs):
    instance.file.delete(False)  # type: ignore
