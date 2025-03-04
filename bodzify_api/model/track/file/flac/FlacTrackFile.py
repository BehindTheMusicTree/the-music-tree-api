import os

from django.db import models

from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.model.track.file.TrackFile import TrackFile
from bodzify_api.utils import audio_metadata
from bodzify_api.utils.audio_metadata.exceptions import FileCorruptedError, FlacMd5CheckFailedError

from .Fields import Fields


class FlacTrackFile(TrackFile):
    md5_has_been_corrected = models.BooleanField(default=False)

    def _prepare_save(self, ctx) -> dict:
        ctx = super()._prepare_save(ctx)

        # First try to validate and correct MD5 without touching ID3 metadata
        if not audio_metadata.is_flac_md5_valid(self.file):
            try:
                # Try correcting MD5 first without removing ID3
                audio_metadata.replace_flac_with_corrected_md5(self.file)
                if audio_metadata.is_flac_md5_valid(self.file):
                    self.md5_has_been_corrected = True
                    return ctx
            except (FlacMd5CheckFailedError, FileCorruptedError):
                # If direct correction failed, try removing ID3 metadata and correct again
                try:
                    audio_metadata.delete_potential_id3_metadata_with_header(self.file)
                    audio_metadata.replace_flac_with_corrected_md5(self.file)
                    if not audio_metadata.is_flac_md5_valid(self.file):
                        raise FlacMd5CheckFailedError()
                    self.md5_has_been_corrected = True
                except (FlacMd5CheckFailedError, FileCorruptedError):
                    raise AppValidationException(
                        field_name=Fields.FILE,
                        message='The FLAC file MD5 check failed and could not be corrected. The file is probably corrupted.',
                        field_validation_error_code=FieldValidationErrorCode.FILE_CORRUPTED)
        else:
            self.md5_has_been_corrected = False

        return ctx

    def handle_flac_md5(self) -> bool:

        return True

    def delete_file(self):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
