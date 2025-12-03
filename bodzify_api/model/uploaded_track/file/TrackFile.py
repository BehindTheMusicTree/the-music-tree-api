import binascii
import datetime
import hashlib
import logging
import os
from typing import TYPE_CHECKING, cast

from django.core.files import File as DjangoFile
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db import models
from django.db.models.fields.files import FieldFile
from django.db.models import F
from django.db.models.signals import post_save, pre_delete
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
from bodzify_api.utils import audio_fingerprinter, musicbrainz
from bodzify_api.utils.audio_metadata import AppMetadata
from bodzify_api.utils.audio_metadata.exceptions import FileCorruptedError
import bodzify_api.utils.audio_metadata.audiometa_adapter as audiometa_adapter
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
        logger = logging.getLogger(__name__)

        if self.extension.lower() == '.flac':
            initial_file_path = None
            if isinstance(self.file, TemporaryUploadedFile):
                try:
                    initial_file_path = self.file.temporary_file_path()
                except Exception:
                    pass
            elif isinstance(self.file, FieldFile) and hasattr(self.file, 'file') and isinstance(self.file.file, TemporaryUploadedFile):
                try:
                    initial_file_path = self.file.file.temporary_file_path()
                except Exception:
                    pass
            elif hasattr(self.file, 'path'):
                initial_file_path = self.file.path

            is_valid_before = audiometa_adapter.is_flac_md5_valid(self.file)

            if is_valid_before:
                self.md5_has_been_corrected = False
            else:
                try:
                    logger.info(f"MD5 is invalid, starting correction process: {initial_file_path}")

                    # Calculate MD5 of original file for comparison
                    original_md5 = None
                    if initial_file_path and os.path.exists(initial_file_path):
                        with open(initial_file_path, 'rb') as f:
                            original_md5 = hashlib.md5(f.read()).hexdigest()
                        logger.info(f"Original file MD5 checksum: {original_md5}")
                        # Store in context for later comparison
                        if not hasattr(ctx, 'original_md5'):
                            ctx.original_md5 = original_md5

                    # Fix MD5 and preserve file path
                    logger.info("Calling fix_md5_checking to correct MD5")
                    corrected_file = audiometa_adapter.fix_md5_checking(self.file)

                    # Calculate MD5 of corrected file for comparison
                    corrected_md5 = None
                    if isinstance(corrected_file, TemporaryUploadedFile):
                        try:
                            corrected_path = corrected_file.temporary_file_path()
                            with open(corrected_path, 'rb') as f:
                                corrected_md5 = hashlib.md5(f.read()).hexdigest()
                            logger.info(f"Corrected file MD5 checksum: {corrected_md5}")
                            # Store in context for later comparison
                            if not hasattr(ctx, 'corrected_md5'):
                                ctx.corrected_md5 = corrected_md5
                            if original_md5:
                                if original_md5 == corrected_md5:
                                    logger.warning(
                                        f"WARNING: Original and corrected MD5 are the same! This should not happen.")
                                else:
                                    logger.info(
                                        f"MD5 changed: original={original_md5[:16]}... -> corrected={corrected_md5[:16]}...")
                        except Exception as e:
                            logger.debug(f"Could not calculate corrected file MD5: {e}")

                    corrected_file_path = None
                    if isinstance(corrected_file, TemporaryUploadedFile):
                        try:
                            corrected_file_path = corrected_file.temporary_file_path()
                        except Exception:
                            pass

                    # Verify the corrected file has valid MD5
                    if corrected_file_path:
                        import subprocess
                        verify_result = subprocess.run(
                            ['flac', '-t', corrected_file_path],
                            capture_output=True, text=True)
                        logger.info(f"FLAC tool validation of corrected file: returncode={verify_result.returncode}")
                        if verify_result.returncode != 0:
                            logger.error(f"Corrected file fails FLAC tool validation: {verify_result.stderr[:200]}")

                    logger.info(
                        f"Before assignment: self.file type={type(self.file)}, corrected_file type={type(corrected_file)}")
                    original_file_path = None
                    if isinstance(
                            self.file, FieldFile) and hasattr(
                            self.file, 'file') and isinstance(
                            self.file.file, TemporaryUploadedFile):
                        original_file_path = self.file.file.temporary_file_path()
                        logger.info(f"Original file path (before correction): {original_file_path}")

                    # CRITICAL: Assign the corrected file to self.file
                    # Django's FileField.save() will read from this TemporaryUploadedFile and write to storage
                    # This ensures Django saves the CORRECTED version, not the original
                    self.file = corrected_file
                    self.md5_has_been_corrected = True
                    logger.info(f"MD5 correction in _prepare_save completed, md5_has_been_corrected=True")

                    # Verify Django will use the corrected file (not the original)
                    corrected_file_path = None
                    if isinstance(corrected_file, TemporaryUploadedFile):
                        corrected_file_path = corrected_file.temporary_file_path()
                        logger.info(f"Corrected file path (will be saved by Django): {corrected_file_path}")
                        if original_file_path and original_file_path != corrected_file_path:
                            logger.info(
                                f"CONFIRMED: Django will save CORRECTED file ({corrected_file_path}), not original ({original_file_path})")

                    # Verify the file we're about to save has valid MD5
                    if isinstance(corrected_file, TemporaryUploadedFile):
                        try:
                            tmp_path = corrected_file.temporary_file_path()
                            final_check = subprocess.run(['flac', '-t', tmp_path], capture_output=True, text=True)
                            logger.info(
                                f"Final FLAC tool check of TemporaryUploadedFile before Django save: returncode={final_check.returncode}")
                            if final_check.returncode != 0:
                                logger.error(
                                    f"WARNING: TemporaryUploadedFile has invalid MD5 before Django save! {final_check.stderr[:200]}")
                            else:
                                logger.info(
                                    f"TemporaryUploadedFile is valid before Django save - verifying Django will use this file")

                            # Check if self.file still points to the corrected file
                            if hasattr(self.file, 'temporary_file_path'):
                                current_path = self.file.temporary_file_path()
                                logger.info(
                                    f"self.file.temporary_file_path() = {current_path}, matches corrected: {current_path == tmp_path}")
                            elif isinstance(self.file, FieldFile) and hasattr(self.file, 'file'):
                                logger.info(f"self.file is FieldFile, checking file attribute: {type(self.file.file)}")
                                if isinstance(self.file.file, TemporaryUploadedFile):
                                    field_file_path = self.file.file.temporary_file_path()
                                    logger.info(
                                        f"FieldFile.file.temporary_file_path() = {field_file_path}, matches corrected: {field_file_path == tmp_path}")
                        except Exception as e:
                            logger.debug(f"Could not verify TemporaryUploadedFile before save: {e}")

                    # Verify the file we're about to save has valid MD5
                    if isinstance(self.file, TemporaryUploadedFile):
                        try:
                            tmp_path = self.file.temporary_file_path()
                            final_check = subprocess.run(['flac', '-t', tmp_path], capture_output=True, text=True)
                            logger.info(
                                f"Final FLAC tool check before Django save: returncode={final_check.returncode}")
                            if final_check.returncode != 0:
                                logger.error(
                                    f"WARNING: File has invalid MD5 before Django save! {final_check.stderr[:200]}")
                        except Exception as e:
                            pass
                except FileCorruptedError as e:
                    logger.error(f"FileCorruptedError during MD5 fix: {e}")
                    raise AppValidationException(
                        field_name=Fields.FILE,
                        message='The FLAC file appears to be corrupted and cannot be processed.',
                        field_validation_error_code=FieldValidationErrorCode.TRACK_FILE_CORRUPTED)
        try:
            file_for_metadata = self.file
            if isinstance(
                    file_for_metadata, DjangoFile) and hasattr(
                    file_for_metadata, 'name') and not os.path.isabs(
                    file_for_metadata.name):
                expected_path = self.user.lib_abs_path / file_for_metadata.name
                if expected_path.exists():
                    file_for_metadata = str(expected_path)
            duration = audiometa_adapter.get_duration_in_sec(file_for_metadata)
            self.duration_in_sec = duration if duration > 1 else 1
            self.bitrate_in_kbps = audiometa_adapter.get_bitrate(file_for_metadata)
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
        # Ensure we use the actual file path, not the FieldFile object
        file_path = self.file.path if hasattr(self.file, 'path') else self.file
        audiometa_adapter.update_file_metadata(file=file_path,
                                               app_metadata=app_metadata,
                                               normalized_rating_max_value=settings.UPLOADED_TRACK_RATING_VALUE_MAX)

    def _post_save(self, adding: bool) -> None:
        logger = logging.getLogger(__name__)
        if adding and self.md5_has_been_corrected:
            if hasattr(self.file, 'path'):
                saved_path = self.file.path
                logger.info(f"_post_save: Django saved file to: {saved_path}")
                if saved_path and os.path.exists(saved_path) and saved_path.lower().endswith('.flac'):
                    import subprocess
                    check_result = subprocess.run(['flac', '-t', saved_path], capture_output=True, text=True)
                    logger.info(f"_post_save: FLAC tool check of saved file: returncode={check_result.returncode}")
                    if check_result.returncode != 0:
                        logger.error(
                            f"_post_save: WARNING - Django saved file has invalid MD5! This confirms Django corrupted it during save.")
                    else:
                        logger.info(f"_post_save: File is valid after Django save")
        super()._post_save(adding)

    def handle_flac_md5(self) -> bool:
        return False


@receiver(pre_delete, sender=TrackFile)
def handle_pre_delete(sender, instance: TrackFile, using, **kwargs):
    instance.file.delete(False)  # type: ignore
