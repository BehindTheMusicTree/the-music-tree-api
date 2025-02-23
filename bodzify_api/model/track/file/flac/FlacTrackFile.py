
import os

from django.db import models

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.exception.validation.app.AppValidationError import AppValidationError
from bodzify_api.model.track.file.TrackFile import TrackFile
from bodzify_api.utils import audio_metadata
from bodzify_api.utils.audio_metadata.exceptions import FlacMd5CheckFailedError
from .Fields import Fields


class FlacTrackFile(TrackFile):
    id3v2_tags_found_and_converted = models.BooleanField(default=False)
    md5_has_been_corrected = models.BooleanField(default=False)

    def _prepare_save(self, ctx) -> dict:
        id3v2_tags = audio_metadata.get_raw_metadata_from_file(self.file, use_id3v2=True)
        if id3v2_tags:
            self.id3v2_tags_found_and_converted = True

            raise AppValidationError(
                field_name=Fields.FILE,
                message='The FLAC file MD5 check failed. The file is probably corrupted.',
                field_validation_error_code=FieldValidationErrorCode.FILE_CORRUPTED)

        if not audio_metadata.is_md5_valid(self.file):
            try:
                audio_metadata.replace_flac_file_with_corrected_md5(self.file_path_temp_or_not)
                self.md5_has_been_corrected = True
            except FlacMd5CheckFailedError:
                raise AppValidationError(
                    field_name=Fields.FILE,
                    message='The FLAC file MD5 check failed and could not be corrected. The file is probably corrupted.',
                    field_validation_error_code=FieldValidationErrorCode.FILE_CORRUPTED)
        else:
            self.md5_has_been_corrected = False

        return super()._prepare_save(ctx)

    def handle_flac_md5(self) -> bool:

        return True

    def delete_file(self):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
