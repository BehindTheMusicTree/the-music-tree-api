from typing import Optional, TYPE_CHECKING, cast
import binascii
import datetime
import os

from django.core.files.base import File as DjangoFile
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from bodzify_api import settings
from bodzify_api.utils import audio_fingerprinter, audio_metadata, musicbrainz
from bodzify_api.utils.audio_metadata.NormalizedMetadataKeys import NormalizedMetadataKeys
from bodzify_api.validator.track_file_validator \
    import validate_content_type_is_audio, validate_filename_length, validate_size
from bodzify_api.model.private_standard_resource.PrivateStandardResource import PrivateStandardResource
from bodzify_api.model.musicbrainz_resource.children.recording.MusicBrainzRecordingLookupResult \
    import MusicbrainzRecordingLookupResult
from bodzify_api.model.musicbrainz_resource.children.recording.MusicbrainzRecording import MusicbrainzRecording
from bodzify_api.model.musicbrainz_resource.children.recording.missing_cause.MusicbrainzRecordingMissingCause \
    import MusicbrainzRecordingMissingCause
from bodzify_api.model.musicbrainz_resource.children.recording.missing_cause.code.MusicbrainzRecordingMissingCauseCode \
    import MusicbrainzRecordingMissingCauseCode
from bodzify_api.model.track.lib.Fields import Fields as LibraryTrackFields
from bodzify_api.model.utils.PreserveSpacesStorage import PreserveSpacesStorage
from bodzify_api.model.utils import utils as model_utils
from .fingerprinting.missing_cause.FingerprintMissingCause import FingerprintMissingCause
from .fingerprinting.FingerprintingResult import FingerprintingResult
from .Fields import Fields

if TYPE_CHECKING:
    from ..lib.LibraryTrack import LibraryTrack


class TrackFile(PrivateStandardResource):
    library_track = models.OneToOneField('LibraryTrack',
                                         on_delete=models.CASCADE,
                                         related_name=LibraryTrackFields.TRACK_FILE,
                                         unique=True)  # Makes the track file unique for a library track
    file = models.FileField(upload_to=model_utils.get_user_lib_path,
                            storage=PreserveSpacesStorage(),
                            help_text="Only audio formats accepted.",
                            validators=[FileExtensionValidator(settings.LIB_TRACK_FILE_EXTENSIONS),
                                        validate_filename_length,
                                        validate_size,
                                        validate_content_type_is_audio],
                            max_length=settings.FILE_PATH_MAX_LENGTH)
    duration_in_sec = models.PositiveIntegerField()
    fingerprint_memory = models.BinaryField(null=True, blank=True, default=None, editable=True)
    fingerprint_missing_cause = models.ForeignKey(FingerprintMissingCause,
                                                  on_delete=models.DO_NOTHING,
                                                  null=True,
                                                  blank=True)
    flac_md5_has_been_corrected = models.BooleanField(null=True, default=None, blank=True)
    size_in_bytes = models.DecimalField(max_digits=11, decimal_places=2)
    size_in_ko = models.GeneratedField(expression=F(Fields.SIZE_IN_BYTES) / 1024,  # type: ignore
                                       output_field=models.DecimalField(max_digits=8, decimal_places=2),
                                       db_persist=True)
    size_in_mo = models.GeneratedField(expression=F(Fields.SIZE_IN_BYTES) / (1024 * 1024),  # type: ignore
                                       output_field=models.DecimalField(max_digits=5, decimal_places=2),
                                       db_persist=True)
    bitrate_in_kbps = models.IntegerField()

    musicbrainz_recording = models.ForeignKey(MusicbrainzRecording,
                                              on_delete=models.DO_NOTHING,
                                              default=None,
                                              null=True)
    musicbrainz_recording_missing_cause = models.OneToOneField(
        MusicbrainzRecordingMissingCause, on_delete=models.DO_NOTHING, null=True)

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
    def file_path_temp_or_not(self) -> DjangoFile:
        path = self.file.file or self.file.path
        return path  # type: ignore

    @property
    def duration_str_in_hour_min_sec(self) -> Optional[str]:
        return str(datetime.timedelta(seconds=self.duration_in_sec)) if self.duration_in_sec else None

    @property
    def fingerprint_bytes(self):
        return bytes(self.fingerprint_memory) if self.fingerprint_memory else None

    def __str__(self):
        if self.file and self.file.name:
            return self.file.name + " (" + str(self.size_in_bytes) + " bytes)"
        return ""

    def _get_bitrate(self) -> Optional[int]:
        return audio_metadata.get_bitrate_from_file(self.file_path_temp_or_not)

    def _manage_fingerprint(self) -> Optional[FingerprintingResult]:
        audio_meta_analysis_enabled_override_env_var = os.environ.get('AUDIO_META_ANALYSIS_ENABLED_OVERRIDE', None)
        if audio_meta_analysis_enabled_override_env_var:
            is_audio_meta_analysis_enabled_override = audio_meta_analysis_enabled_override_env_var.lower()
        else:
            is_audio_meta_analysis_enabled_override = 'false'

        fingerprinting_result: Optional[FingerprintingResult] = None

        if is_audio_meta_analysis_enabled_override == 'true' or settings.AUDIO_META_ANALYSIS_ENABLED:
            library_track: LibraryTrack = self.library_track
            fingerprinting_result = audio_fingerprinter.get_fingerprinting_result(user=self.user,
                                                                                  track_file=self.file_path_temp_or_not,
                                                                                  title=library_track.title)

            if fingerprinting_result.is_success:
                fingerprint = binascii.hexlify(fingerprinting_result.fingerprint)

                if library_track.track_file_fingerprint_must_be_unique:
                    existing_track_file = cast(
                        'Optional[TrackFile]',
                        self.__class__.objects.filter(user=self.user, fingerprint_memory=fingerprint).first()
                    )
                    if existing_track_file:
                        raise ValidationError({'file': [f"The file '{self.filename}' has the same fingerprint as "
                                                        f"the file '{existing_track_file.filename}'."]})
                self.fingerprint_memory = fingerprint
            else:
                self.fingerprint_missing_cause = fingerprinting_result.missing_cause
        else:
            self.fingerprint_missing_cause = FingerprintMissingCause.objects.create(
                user=self.user,
                code=MusicbrainzRecordingMissingCauseCode.Codes.AUDIO_META_AMALYSIS_DISABLED)

        return fingerprinting_result

    def _manage_musicbrainz_recording(self, fingerprinting_result_nullable: Optional[FingerprintingResult]
                                      ) -> Optional[MusicbrainzRecordingLookupResult]:
        musicbrainz_recording_lookup_result = None

        if self.fingerprint_missing_cause:
            if self.fingerprint_missing_cause.code == \
                    MusicbrainzRecordingMissingCauseCode.Codes.AUDIO_META_AMALYSIS_DISABLED:
                self.musicbrainz_recording_missing_cause = MusicbrainzRecordingMissingCause.objects.create(
                    user=self.user,
                    code=MusicbrainzRecordingMissingCauseCode.Codes.AUDIO_META_AMALYSIS_DISABLED)
            else:
                self.musicbrainz_recording_missing_cause = MusicbrainzRecordingMissingCause.objects.create(
                    user=self.user,
                    code=MusicbrainzRecordingMissingCauseCode.Codes.TRACK_FILE_FINGERPRINTING_FAILED,
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
        temp_file_path = self.file.file
        duration_in_sec: int = audio_metadata.get_specific_metadata_from_file(
            file=temp_file_path,
            normalized_metadata_key=NormalizedMetadataKeys.DURATION_IN_SEC)  # type: ignore
        self.duration_in_sec = int(duration_in_sec)
        self.bitrate_in_kbps = self._get_bitrate()
        self.handle_flac_md5()
        self.size_in_bytes = self.file.size
        return ctx.kwargs

    def _perform_save(self, adding: bool, ctx) -> None:
        fingerprinting_result = self._manage_fingerprint()
        self._manage_musicbrainz_recording(fingerprinting_result)

    def update_file_tags(self, normalized_metadata: dict):
        audio_metadata.update_file_metadata(file=self.file,
                                            normalized_metadata=normalized_metadata,
                                            normalized_rating_max_value=settings.LIB_TRACK_RATING_VALUE_MAX)

    def handle_flac_md5(self) -> bool:
        if not self.file or self.extension != '.flac':
            return False

        if not audio_metadata.is_flac_file_md5_valid(self.file_path_temp_or_not):
            try:
                audio_metadata.replace_flac_file_with_corrected_md5(self.file.path)
                self.flac_md5_has_been_corrected = True
            except Exception:
                raise ValidationError({'file': ["The Flac file md5 check failed and could not be corrected. The " +
                                                "file is probably corrupted."]})
        else:
            self.flac_md5_has_been_corrected = False

        return True

    def delete_file(self):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)


@receiver(pre_delete, sender=TrackFile)
def handle_pre_delete(sender, instance: TrackFile, using, **kwargs):  # type: ignore
    instance.file.delete(False)
