
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
                import hashlib
                from django.core.files.uploadedfile import InMemoryUploadedFile

                # Save original file state
                print("=== Before MD5 fix ===")
                self.file.seek(0)
                content_before = self.file.read()
                content_hash_before = hashlib.md5(content_before).hexdigest()
                self.file.seek(0)
                md5_valid_before = audio_metadata.is_flac_md5_valid(self.file)
                print(f"Content length: {len(content_before)} bytes")
                print(f"Content hash: {content_hash_before}")
                print(f"MD5 valid: {md5_valid_before}")

                print("\n=== Attempting MD5 fix... ===")
                # Create AudioFile instance and fix MD5
                audio_file = audio_metadata.AudioFile(self.file)
                audio_file.fix_md5_checking()

                # Get the potentially new file from AudioFile instance
                if isinstance(audio_file.file, InMemoryUploadedFile):
                    print("Updating file reference with corrected file...")
                    self.file = audio_file.file
                self.md5_has_been_corrected = True

                # Check file state after fix
                print("\n=== After MD5 fix ===")
                self.file.seek(0)
                content_after = self.file.read()
                content_hash_after = hashlib.md5(content_after).hexdigest()
                self.file.seek(0)
                md5_valid_after = audio_metadata.is_flac_md5_valid(self.file)
                print(f"Content length: {len(content_after)} bytes")
                print(f"Content hash: {content_hash_after}")
                print(f"Content changed: {content_hash_before != content_hash_after}")
                print(f"MD5 valid: {md5_valid_after}")
                print(f"MD5 correction status: {'fixed' if md5_valid_after else 'still invalid'}")
                self.file.seek(0)  # Ensure file is ready for next operation
            except FileCorruptedError as e:
                if not isinstance(e, FlacMd5CheckFailedError):
                    raise AppValidationException(
                        field_name=Fields.FILE,
                        message='The FLAC file appears to be corrupted and cannot be processed.',
                        field_validation_error_code=FieldValidationErrorCode.FILE_CORRUPTED)
        return ctx
