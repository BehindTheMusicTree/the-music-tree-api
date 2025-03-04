
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

        if audio_metadata.is_flac_md5_valid(self.file):
            self.md5_has_been_corrected = False
            return ctx
        else:
            try:
                # ID3v2 metadata can be present in FLAC files, causing a mismatch in the MD5 checksum.
                # They are therefore removed which won't affect the file's metadata integrity as all the metadata
                # is stored in the Vorbis comment block.
                audio_metadata.delete_potential_id3_metadata_with_header(self.file)

                # Fix MD5 and preserve file path
                corrected_file = audio_metadata.fix_md5_checking(self.file)
                if isinstance(corrected_file, str):
                    # If we got a file path, create a new InMemoryUploadedFile
                    from django.core.files.uploadedfile import InMemoryUploadedFile
                    from io import BytesIO

                    # Read the corrected file content
                    with open(corrected_file, 'rb') as f:
                        content = f.read()

                    # Create a new BytesIO object with the content
                    file_obj = BytesIO(content)

                    # Create new InMemoryUploadedFile with same name and content type
                    self.file = InMemoryUploadedFile(
                        file=file_obj,
                        field_name=None,
                        name=getattr(self.file, 'name', corrected_file),
                        content_type='audio/x-flac',
                        size=len(content),
                        charset=None,
                        content_type_extra={}
                    )
                else:
                    # If we got an InMemoryUploadedFile, use it directly
                    self.file = corrected_file
                self.md5_has_been_corrected = True
            except FileCorruptedError as e:
                if not isinstance(e, FlacMd5CheckFailedError):
                    raise AppValidationException(
                        field_name=Fields.FILE,
                        message='The FLAC file appears to be corrupted and cannot be processed.',
                        field_validation_error_code=FieldValidationErrorCode.FILE_CORRUPTED)
        return ctx
