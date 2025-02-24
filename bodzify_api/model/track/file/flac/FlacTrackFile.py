
import os

from django.db import models

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.exception.validation.app.AppValidationError import AppValidationError
from bodzify_api.model.track.file.TrackFile import TrackFile
from bodzify_api.utils import audio_metadata
from bodzify_api.utils.audio_metadata.exceptions import FlacMd5CheckFailedError
from bodzify_api.utils.audio_metadata.TagFormat import TagFormat
from .Fields import Fields


class FlacTrackFile(TrackFile):
    id3v2_tags_found_and_converted = models.BooleanField(default=False)
    md5_has_been_corrected = models.BooleanField(default=False)

    def _prepare_save(self, ctx) -> :
        id3v2_tags = audio_metadata.get_raw_metadata(self.file, tag_format=TagFormat.ID3V2)
        if id3v2_tags:
            if not audio_metadata.delete_metadata(self.file, TagFormat.ID3V2):
                raise AppValidationError(
                    field_name=Fields.FILE,
                    message='Failed to clear ID3v2 tags from FLAC file.',
                    field_validation_error_code=FieldValidationErrorCode.FILE_CORRUPTED)

            self.id3v2_tags_found_and_converted = True

        if not audio_metadata.is_flac_md5_valid(self.file):
            try:
                audio_metadata.replace_flac_with_corrected_md5(self.file)
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
