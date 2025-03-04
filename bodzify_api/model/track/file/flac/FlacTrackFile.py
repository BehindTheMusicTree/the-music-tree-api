
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

        # ID3 metadata can be present in FLAC files, causing a mismatch in the MD5 checksum.
        # They are therefore removed which won't affect the file's metadata integrity as all the metadata
        # is stored in the Vorbis comment block.
        audio_metadata.delete_potential_id3_metadata_with_header(self.file)

        if audio_metadata.is_flac_md5_valid(self.file):
            self.md5_has_been_corrected = False
            return ctx
        else:
            try:
                content_before = self.file.read()
                self.file.seek(0)
                md5_valid_before = audio_metadata.is_flac_md5_valid(self.file)
                print(
                    f"File before MD5 fix - Content length: {len(content_before)} bytes, MD5 valid: {md5_valid_before}")

                audio_metadata.fix_md5_checking(self.file)
                self.md5_has_been_corrected = True

                content_after = self.file.read()
                self.file.seek(0)
                md5_valid_after = audio_metadata.is_flac_md5_valid(self.file)
                print(
                    f"File after MD5 fix - Content length: {len(content_after)} bytes, MD5 valid: {md5_valid_after}, Content changed: {content_before != content_after}")
            except FileCorruptedError as e:
                if not isinstance(e, FlacMd5CheckFailedError):
                    raise AppValidationException(
                        field_name=Fields.FILE,
                        message='The FLAC file appears to be corrupted and cannot be processed.',
                        field_validation_error_code=FieldValidationErrorCode.FILE_CORRUPTED)
        return ctx
